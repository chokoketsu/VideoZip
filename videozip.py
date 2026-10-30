# -*- coding: utf-8 -*-
"""
VideoZip - 把视频压到指定体积，参数自动匹配
单文件 exe，双击即用。

作者 / Author : chokoketsu
主页 / GitHub : https://github.com/chokoketsu
许可 / License: MIT
"""
import os
import re
import sys
import json
import math
import glob
import time
import shutil
import zipfile
import tempfile
import threading
import subprocess
import urllib.request

ICON_B64 = (
    "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"
)

APP_NAME = "VideoZip"
VERSION = "1.0"
__author__ = "chokoketsu"
__github__ = "https://github.com/chokoketsu"
CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0

# ---------------------------------------------------------------- 路径与工具

def app_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def meipass():
    return getattr(sys, "_MEIPASS", None)


def cache_dir():
    base = os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()
    d = os.path.join(base, "VideoZip")
    try:
        os.makedirs(d, exist_ok=True)
    except Exception:
        d = tempfile.gettempdir()
    return d


def find_tool(name):
    """在多个位置查找 ffmpeg/ffprobe。"""
    exe = name + ".exe"
    cands = []
    env = os.environ.get("VIDEOZIP_FFMPEG")
    if env:
        cands.append(os.path.join(env, exe) if os.path.isdir(env) else env)

    base = app_dir()
    cands += [os.path.join(base, exe),
              os.path.join(base, "bin", exe),
              os.path.join(base, "ffmpeg", "bin", exe),
              os.path.join(base, "ffmpeg", exe)]

    mp = meipass()
    if mp:
        cands += [os.path.join(mp, exe), os.path.join(mp, "bin", exe)]

    cands.append(os.path.join(cache_dir(), "ffmpeg", "bin", exe))

    w = shutil.which(exe)
    if w:
        cands.append(w)

    la = os.environ.get("LOCALAPPDATA", "")
    patterns = [
        os.path.join(la, "Microsoft", "WinGet", "Packages", "Gyan.FFmpeg*", "**", "bin", exe),
        os.path.join(la, "Microsoft", "WinGet", "Packages", "*ffmpeg*", "**", "bin", exe),
        os.path.join(la, "Microsoft", "WinGet", "Links", exe),
        os.path.join(la, "Programs", "ffmpeg", "bin", exe),
        os.path.join("C:\\", "ffmpeg", "bin", exe),
        os.path.join("C:\\", "Program Files", "ffmpeg", "bin", exe),
        os.path.join("C:\\", "Program Files (x86)", "ffmpeg", "bin", exe),
        os.path.join("C:\\", "ProgramData", "chocolatey", "bin", exe),
    ]
    for p in patterns:
        try:
            cands += glob.glob(p, recursive=True)
        except Exception:
            pass

    for c in cands:
        try:
            if c and os.path.isfile(c):
                return c
        except Exception:
            pass
    return None


FFMPEG_UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
FFMPEG_ZIP = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"


def download_ffmpeg(progress=None):
    """下载并解压 ffmpeg 到本地缓存目录，返回 (ffmpeg, ffprobe)。"""
    dest = os.path.join(cache_dir(), "ffmpeg")
    bin_dir = os.path.join(dest, "bin")
    os.makedirs(bin_dir, exist_ok=True)
    tmp_zip = os.path.join(cache_dir(), "ffmpeg-dl.zip")
    req = urllib.request.Request(FFMPEG_ZIP, headers=FFMPEG_UA)
    with urllib.request.urlopen(req, timeout=60) as r, open(tmp_zip, "wb") as f:
        total = int(r.headers.get("Content-Length") or 0)
        got = 0
        while True:
            chunk = r.read(262144)
            if not chunk:
                break
            f.write(chunk)
            got += len(chunk)
            if progress and total:
                progress(min(got / total, 1.0), got, total)
    with zipfile.ZipFile(tmp_zip) as z:
        for n in z.namelist():
            base = os.path.basename(n)
            if base in ("ffmpeg.exe", "ffprobe.exe"):
                with z.open(n) as src, open(os.path.join(bin_dir, base), "wb") as out:
                    shutil.copyfileobj(src, out)
    try:
        os.remove(tmp_zip)
    except Exception:
        pass
    return os.path.join(bin_dir, "ffmpeg.exe"), os.path.join(bin_dir, "ffprobe.exe")


# ---------------------------------------------------------------- 探测信息

def _run(cmd, **kw):
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          creationflags=CREATE_NO_WINDOW, **kw)


def _frac(s):
    try:
        if "/" in str(s):
            a, b = str(s).split("/")[:2]
            b = float(b)
            return float(a) / b if b else 0.0
        return float(s)
    except Exception:
        return 0.0


def probe(ffprobe, path):
    r = _run([ffprobe, "-v", "error", "-print_format", "json",
              "-show_format", "-show_streams", path])
    txt = r.stdout.decode("utf-8", "replace")
    if r.returncode != 0 or not txt.strip():
        raise RuntimeError("无法读取视频信息（文件可能损坏或格式不支持）")
    data = json.loads(txt)
    dur = float(data.get("format", {}).get("duration") or 0)
    v = None
    has_audio = False
    channels = 2
    for s in data.get("streams", []):
        if s.get("codec_type") == "video" and v is None and not s.get("disposition", {}).get("attached_pic"):
            v = s
        elif s.get("codec_type") == "audio":
            has_audio = True
            channels = max(channels, int(s.get("channels") or 2))
    if v is None:
        raise RuntimeError("文件里没有找到视频轨道")
    w = int(v.get("width") or 0)
    h = int(v.get("height") or 0)
    rot = 0
    for sd in (v.get("side_data_list") or []):
        if "rotation" in sd:
            try:
                rot = int(float(sd["rotation"]))
            except Exception:
                pass
    if not rot:
        try:
            rot = int(float((v.get("tags") or {}).get("rotate", 0)))
        except Exception:
            pass
    dw, dh = (h, w) if abs(rot) % 180 == 90 else (w, h)
    fps = _frac(v.get("avg_frame_rate")) or _frac(v.get("r_frame_rate")) or 25.0
    if not dur:
        dur = float(v.get("duration") or 0)
    size = os.path.getsize(path)
    vb = 0
    try:
        vb = int(float(v.get("bit_rate") or 0))
    except Exception:
        vb = 0
    if vb <= 0 and dur > 0:
        vb = int(size * 8.0 / dur * 0.96)
    return {"duration": dur, "w": dw, "h": dh, "fps": fps,
            "has_audio": has_audio, "channels": channels,
            "size": size, "vcodec": v.get("codec_name") or "?", "rotation": rot,
            "vbitrate": vb}


# ---------------------------------------------------------------- 方案计算

STD_HEIGHTS = [2160, 1600, 1440, 1200, 1080, 1024, 900, 800, 720, 648, 600,
               576, 540, 512, 480, 432, 400, 360, 320, 288, 240, 216, 180, 144]
BPP_GOOD = 0.078


def _bpp(vk, w, h, fps):
    if w <= 0 or h <= 0 or fps <= 0:
        return 0.0
    return vk * 1000.0 / (w * h * fps)


def make_plan(info, target_mb):
    """根据目标体积反推编码方案。"""
    d = info["duration"] or 1.0
    W, H, fps = info["w"], info["h"], info["fps"] or 25.0
    total_bps = target_mb * 1024 * 1024 * 8.0 / d
    usable = total_bps * 0.95

    if info["has_audio"] and d > 0:
        tk = usable / 1000.0
        if tk >= 2600:
            ab = 192
        elif tk >= 1600:
            ab = 160
        elif tk >= 1000:
            ab = 128
        elif tk >= 600:
            ab = 96
        elif tk >= 350:
            ab = 64
        else:
            ab = 48
        if info["channels"] <= 1:
            ab = min(ab, 96)
    else:
        ab = 0

    vb = int(usable / 1000.0 - ab - 3)
    vb = max(vb, 90)

    # 体积给得过于宽裕时，按"不超过源画质"封顶，避免体积虚高
    capped = False
    src_vb = int((info.get("vbitrate") or 0) / 1000)
    if src_vb > 0:
        ceiling = max(320, int(src_vb * 1.2))
        if vb > ceiling:
            vb = ceiling
            capped = True

    nw, nh, nfps = W, H, fps
    cur = _bpp(vb, W, H, fps)
    if cur < BPP_GOOD:
        s = math.sqrt(vb * 1000.0 / (BPP_GOOD * W * H * fps))
        ht = H * s
        pick = None
        for hh in STD_HEIGHTS:
            if hh < H and hh <= ht:
                pick = hh
                break
        if pick is None:
            lower = [hh for hh in STD_HEIGHTS if hh < H]
            pick = min(lower) if lower else H
        if pick < H:
            nh = pick
            nw = int(round(W * nh / float(H) / 2.0)) * 2
            if nw < 16:
                nw, nh = W, H
            cur = _bpp(vb, nw, nh, fps)
        if cur < 0.048 and fps > 26:
            nfps = 24.0
            cur = _bpp(vb, nw, nh, nfps)

    # 归一到标准帧率（29.97→30、23.976→24 这类，避免误降帧）
    for std in (120.0, 60.0, 50.0, 48.0, 30.0, 25.0, 24.0, 20.0, 15.0):
        if abs(nfps - std) <= 1.5:
            nfps = std
            break
    nfps = round(nfps, 3)

    if nw * nh * nfps > 1920 * 1080 * 30:
        preset = "medium"
    elif vb < 700 and d <= 900:
        preset = "slower"
    else:
        preset = "slow"

    est_bytes = (vb + ab) * 1000.0 * d / 8.0 * 1.01
    grade = "优秀" if cur >= 0.12 else "好" if cur >= 0.085 else \
            "中等" if cur >= 0.06 else "一般" if cur >= 0.042 else "偏低"

    return {"v_kbps": vb, "a_kbps": ab, "w": nw, "h": nh, "fps": nfps,
            "preset": preset, "bpp": cur, "grade": grade,
            "est_mb": est_bytes / 1024.0 / 1024.0, "capped": capped,
            "scaled": (nw, nh) != (W, H), "src_w": W, "src_h": H, "src_fps": fps}


def plan_text(info, plan, target_mb):
    if plan["scaled"]:
        res = "%d×%d → %d×%d" % (info["w"], info["h"], plan["w"], plan["h"])
    else:
        res = "%d×%d（原尺寸）" % (plan["w"], plan["h"])
    fps_txt = "%g fps" % plan["fps"]
    if abs(plan["fps"] - info["fps"]) > 0.5:
        fps_txt += "（原 %g）" % info["fps"]
    a = ("音频 %d kbps" % plan["a_kbps"]) if plan["a_kbps"] else "无音轨"
    txt = ("%s · %s · 视频 %d kbps · %s · 预计 %.1f MB · 画质 %s"
           % (res, fps_txt, plan["v_kbps"], a, plan["est_mb"], plan["grade"]))
    if plan.get("capped"):
        txt += "（源画质封顶）"
    return txt


# ---------------------------------------------------------------- 编码

def fmt_dur(sec):
    sec = int(sec or 0)
    return "%d:%02d" % (sec // 60, sec % 60)


def unique_out(src, target_mb, out_dir=None):
    d = out_dir or os.path.dirname(os.path.abspath(src))
    stem = os.path.splitext(os.path.basename(src))[0]
    tag = ("%g" % target_mb).replace(".", "_")
    base = "%s_%sMB" % (stem, tag)
    p = os.path.join(d, base + ".mp4")
    i = 2
    while os.path.exists(p):
        p = os.path.join(d, "%s(%d).mp4" % (base, i))
        i += 1
    return p


def encode(ffmpeg, ffprobe, src, out, target_mb, on_log=None, on_prog=None,
           cancel=None, info=None, plan=None):
    def log(msg):
        if on_log:
            on_log(msg)

    info = info or probe(ffprobe, src)
    plan = plan or make_plan(info, target_mb)
    d = info["duration"] or 1.0

    vf = []
    if plan["scaled"]:
        vf.append("scale=%d:%d:flags=lanczos" % (plan["w"], plan["h"]))
    if abs(plan["fps"] - info["fps"]) > 0.5:
        vf.append("fps=%g" % plan["fps"])
    vf_arg = ["-vf", ",".join(vf)] if vf else []

    tmp = tempfile.mkdtemp(prefix="videozip_")
    passlog = os.path.join(tmp, "p")
    p1out = os.path.join(tmp, "p1.mp4")
    vb = plan["v_kbps"]
    common = [ffmpeg, "-hide_banner", "-y", "-i", src,
              "-map", "0:v:0", "-map", "0:a:0?",
              "-c:v", "libx264", "-preset", plan["preset"],
              "-profile:v", "high", "-pix_fmt", "yuv420p",
              "-b:v", "%dk" % vb, "-maxrate", "%dk" % int(vb * 1.5),
              "-bufsize", "%dk" % int(vb * 2.5),
              "-x264-params", "keyint=60:min-keyint=24:scenecut=40:ref=3"]
    common += vf_arg

    def run_pass(args, weight_from, weight_to, label):
        cmd = common + args + ["-progress", "pipe:1", "-nostats"]
        log(label)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             creationflags=CREATE_NO_WINDOW)
        last_err = []
        for raw in iter(p.stdout.readline, b""):
            if cancel is not None and cancel.is_set():
                try:
                    p.kill()
                except Exception:
                    pass
                break
            line = raw.decode("utf-8", "replace").strip()
            m = re.match(r"out_time_us=(\d+)", line)
            if m and on_prog:
                r = min(float(m.group(1)) / 1e6 / d, 1.0)
                on_prog(weight_from + (weight_to - weight_from) * r)
            elif line and "=" not in line:
                last_err.append(line)
                del last_err[:-6]
        p.wait()
        try:
            p.stdout.close()
        except Exception:
            pass
        return p.returncode, last_err

    try:
        # 第一遍
        rc, err = run_pass(["-pass", "1", "-passlogfile", passlog, "-an",
                            "-f", "mp4", p1out], 0.0, 0.45, "第一遍：分析画面，分配码率…")
        if cancel is not None and cancel.is_set():
            return None
        if rc != 0:
            raise RuntimeError("编码失败：\n" + "\n".join(err[-4:]))

        # 第二遍
        aargs = (["-c:a", "aac", "-b:a", "%dk" % plan["a_kbps"], "-ac", "2", "-ar", "44100"]
                 if plan["a_kbps"] else ["-an"])
        rc, err = run_pass(["-pass", "2", "-passlogfile", passlog] + aargs +
                           ["-movflags", "+faststart", "-f", "mp4", out],
                           0.45, 1.0, "第二遍：正式编码…")
        if cancel is not None and cancel.is_set():
            try:
                os.remove(out)
            except Exception:
                pass
            return None
        if rc != 0:
            raise RuntimeError("编码失败：\n" + "\n".join(err[-4:]))
        return out
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------- 界面

def main_gui():
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox

    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    try:
        from tkinterdnd2 import TkinterDnD, DND_FILES
        root = TkinterDnD.Tk()
        dnd_ok = True
    except Exception:
        root = tk.Tk()
        dnd_ok = False

    BG = "#F6F3EF"
    CARD = "#FFFFFF"
    LINE = "#E3DCD2"
    TXT = "#2E2A26"
    SUB = "#8A8078"
    ACC = "#D9704F"
    ACC_D = "#C25F3F"

    root.title("VideoZip · 视频体积压缩  —  by chokoketsu")
    try:
        import base64 as _b64
        _ico = tk.PhotoImage(data=_b64.b64decode(ICON_B64))
        root.iconphoto(True, _ico)
        root._vz_icon = _ico
    except Exception:
        pass
    root.configure(bg=BG)
    root.geometry("780x740")
    root.minsize(700, 560)

    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass
    style.configure("TEntry", fieldbackground="#FFFFFF", bordercolor=LINE,
                    lightcolor=LINE, darkcolor=LINE, padding=4)
    style.configure("TCombobox", fieldbackground="#FFFFFF", bordercolor=LINE, padding=3)
    style.configure("Peach.Horizontal.TProgressbar", troughcolor="#EFE8DF",
                    background=ACC, bordercolor="#EFE8DF", lightcolor=ACC,
                    darkcolor=ACC, thickness=10)
    style.configure("TCombobox", arrowsize=12)

    files = []
    running = {"proc": False, "cancel": None}
    state = {"info": None, "plan": None}

    # ---------- 布局辅助
    def card(parent, pady=(0, 10)):
        f = tk.Frame(parent, bg=CARD, highlightbackground=LINE,
                     highlightthickness=1, bd=0)
        f.pack(fill="x", pady=pady)
        return f

    def section(parent, text):
        tk.Label(parent, text=text, bg=CARD, fg=SUB, font=("Microsoft YaHei UI", 9, "bold"),
                 anchor="w").pack(fill="x", padx=14, pady=(12, 6))

    head = tk.Frame(root, bg=BG)
    head.pack(fill="x", padx=18, pady=(16, 8))
    tk.Label(head, text="VideoZip", bg=BG, fg=TXT,
             font=("Microsoft YaHei UI", 19, "bold")).pack(side="left")
    tk.Label(head, text="  把视频压到指定体积，参数自动匹配", bg=BG, fg=SUB,
             font=("Microsoft YaHei UI", 10)).pack(side="left", pady=(6, 0))

    def open_github():
        try:
            import webbrowser
            webbrowser.open(__github__)
        except Exception:
            pass

    # 作者标识：点击直达 GitHub 主页
    _gh = tk.Label(head, text="@chokoketsu", bg=BG, fg=ACC, cursor="hand2",
                   font=("Microsoft YaHei UI", 10, "underline"))
    _gh.pack(side="right", pady=(8, 0))
    _gh.bind("<Button-1>", lambda e: open_github())
    _gh.bind("<Enter>", lambda e: _gh.configure(fg=ACC_D))
    _gh.bind("<Leave>", lambda e: _gh.configure(fg=ACC))
    tk.Label(head, text="github.com/", bg=BG, fg=SUB,
             font=("Microsoft YaHei UI", 10)).pack(side="right", pady=(8, 0))

    body = tk.Frame(root, bg=BG)
    body.pack(fill="both", expand=True, padx=18, pady=(0, 4))

    # ---------- 卡片 1：文件
    c1 = card(body)
    section(c1, "视频文件")
    row = tk.Frame(c1, bg=CARD)
    row.pack(fill="x", padx=14)
    lb = tk.Listbox(row, height=4, bg="#FCFAF7", fg=TXT, bd=1, relief="flat",
                    highlightthickness=1, highlightbackground=LINE,
                    highlightcolor=LINE, font=("Microsoft YaHei UI", 9),
                    selectbackground="#F3D9CE", selectforeground=TXT,
                    activestyle="none")
    lb.pack(side="left", fill="both", expand=True)
    sb = ttk.Scrollbar(row, orient="vertical", command=lb.yview)
    sb.pack(side="left", fill="y")
    lb.configure(yscrollcommand=sb.set)

    btns = tk.Frame(row, bg=CARD)
    btns.pack(side="left", fill="y", padx=(10, 0))

    def flat_btn(parent, text, cmd, accent=False, w=10):
        b = tk.Label(parent, text=text, bg=ACC if accent else "#F1EBE3",
                     fg="#FFFFFF" if accent else TXT,
                     font=("Microsoft YaHei UI", 9), cursor="hand2",
                     padx=10, pady=7, width=w)
        b.pack(fill="x", pady=3)
        b.bind("<Button-1>", lambda e: cmd())
        if accent:
            b.bind("<Enter>", lambda e: b.configure(bg=ACC_D))
            b.bind("<Leave>", lambda e: b.configure(bg=ACC))
        else:
            b.bind("<Enter>", lambda e: b.configure(bg="#E7DFD5"))
            b.bind("<Leave>", lambda e: b.configure(bg="#F1EBE3"))
        return b

    hint = tk.Label(c1, text="提示：可以直接把视频文件拖进来（支持多个）", bg=CARD,
                    fg=SUB, font=("Microsoft YaHei UI", 8), anchor="w")
    hint.pack(fill="x", padx=14, pady=(6, 10))

    # ---------- 卡片 2：目标体积
    c2 = card(body)
    section(c2, "目标体积")
    prow = tk.Frame(c2, bg=CARD)
    prow.pack(fill="x", padx=14)
    target_var = tk.StringVar(value="20")
    preset_btns = []

    def set_target(v):
        target_var.set(str(v))
        refresh_buttons()
        update_preview()

    for v in (10, 20, 25, 40, 50, 80, 100):
        b = tk.Label(prow, text="%d MB" % v, bg="#F1EBE3", fg=TXT,
                     font=("Microsoft YaHei UI", 9), padx=12, pady=6, cursor="hand2")
        b.pack(side="left", padx=(0, 6))
        b.bind("<Button-1>", lambda e, v=v: set_target(v))
        preset_btns.append((v, b))

    tk.Label(prow, text="自定义", bg=CARD, fg=SUB,
             font=("Microsoft YaHei UI", 9)).pack(side="left", padx=(10, 4))
    ent = ttk.Entry(prow, textvariable=target_var, width=8)
    ent.pack(side="left")
    tk.Label(prow, text="MB", bg=CARD, fg=SUB,
             font=("Microsoft YaHei UI", 9)).pack(side="left", padx=(4, 0))

    def refresh_buttons():
        for v, b in preset_btns:
            on = str(v) == target_var.get().strip()
            b.configure(bg=ACC if on else "#F1EBE3", fg="#FFFFFF" if on else TXT)

    info_lbl = tk.Label(c2, text="尚未选择文件", bg=CARD, fg=SUB, justify="left",
                        anchor="w", wraplength=660,
                        font=("Microsoft YaHei UI", 9))
    info_lbl.pack(fill="x", padx=14, pady=(10, 12))

    # ---------- 卡片 3：输出与执行
    c3 = card(body, pady=(0, 16))
    section(c3, "输出")
    orow = tk.Frame(c3, bg=CARD)
    orow.pack(fill="x", padx=14)
    same_dir = tk.BooleanVar(value=True)
    out_dir_var = tk.StringVar(value="")

    def pick_dir():
        d = filedialog.askdirectory(title="选择输出文件夹")
        if d:
            out_dir_var.set(d)
            same_dir.set(False)
            lb_out.configure(text=d)

    lb_out = tk.Label(orow, text="与源文件同一文件夹", bg="#FCFAF7", fg=TXT, anchor="w",
                      font=("Microsoft YaHei UI", 9), padx=8, pady=6,
                      highlightbackground=LINE, highlightthickness=1)
    lb_out.pack(side="left", fill="x", expand=True)
    flat_btn(orow, "选择…", pick_dir, w=7)

    arow = tk.Frame(c3, bg=CARD)
    arow.pack(fill="x", padx=14, pady=(12, 4))
    pb = ttk.Progressbar(arow, style="Peach.Horizontal.TProgressbar",
                         mode="determinate", maximum=100)
    pb.pack(side="left", fill="x", expand=True)
    pct = tk.Label(arow, text="0%", bg=CARD, fg=SUB, width=5,
                   font=("Microsoft YaHei UI", 9))
    pct.pack(side="left", padx=(8, 10))

    act = tk.Frame(c3, bg=CARD)
    act.pack(fill="x", padx=14, pady=(12, 6))

    def start():
        if running["proc"]:
            return
        if not files:
            messagebox.showinfo("VideoZip", "先添加一个视频文件吧。")
            return
        try:
            mb = float(target_var.get().strip())
            if mb <= 0:
                raise ValueError
        except Exception:
            messagebox.showwarning("VideoZip", "目标体积请填一个大于 0 的数字（单位 MB）。")
            return
        if mb > 2048:
            messagebox.showwarning("VideoZip", "目标体积太大了，这不像是在压缩 :)")
            return
        ffmpeg = find_tool("ffmpeg")
        ffprobe = find_tool("ffprobe")
        if not ffmpeg or not ffprobe:
            if messagebox.askyesno("VideoZip",
                                   "没有找到 ffmpeg。\n\n要现在自动下载吗？（约 100 MB，只需一次，"
                                   "下载后会保存在本机，以后不用再下）"):
                do_download()
            return
        run_batch(ffmpeg, ffprobe, mb)

    def flat_btn2(parent, text, cmd, accent=False, w=10):
        b = tk.Label(parent, text=text, bg=ACC if accent else "#F1EBE3",
                     fg="#FFFFFF" if accent else TXT,
                     font=("Microsoft YaHei UI", 10, "bold" if accent else "normal"),
                     cursor="hand2", padx=14, pady=9, width=w)
        b.pack(side="left", padx=(0, 8))
        b.bind("<Button-1>", lambda e: cmd())
        if accent:
            b.bind("<Enter>", lambda e: b.configure(bg=ACC_D))
            b.bind("<Leave>", lambda e: b.configure(bg=ACC))
        else:
            b.bind("<Enter>", lambda e: b.configure(bg="#E7DFD5"))
            b.bind("<Leave>", lambda e: b.configure(bg="#F1EBE3"))
        return b

    logs = tk.Text(c3, height=5, bg="#FCFAF7", fg="#5C554E", bd=0,
                   highlightthickness=1, highlightbackground=LINE,
                   font=("Consolas", 9), wrap="word", state="disabled")
    logs.pack(fill="both", expand=True, padx=14, pady=(6, 12))

    def log(msg):
        logs.configure(state="normal")
        logs.insert("end", msg.rstrip() + "\n")
        logs.see("end")
        logs.configure(state="disabled")

    # ---------- 行为

    def add_paths(paths):
        added = 0
        for p in paths:
            p = p.strip().strip('"')
            if not p or not os.path.isfile(p):
                continue
            if p.lower() in [f.lower() for f in files]:
                continue
            files.append(p)
            lb.insert("end", "  " + os.path.basename(p) + "   （" +
                      ("%.1f MB" % (os.path.getsize(p) / 1048576.0)) + "）")
            added += 1
        if added:
            update_preview()

    def add_dialog():
        paths = filedialog.askopenfilenames(
            title="选择视频",
            filetypes=[("视频文件", "*.mp4 *.mov *.mkv *.avi *.m4v *.wmv *.flv *.webm *.ts *.mpg *.mpeg"),
                       ("所有文件", "*.*")])
        add_paths(list(paths))

    def clear_all():
        if running["proc"]:
            return
        files.clear()
        lb.delete(0, "end")
        info_lbl.configure(text="尚未选择文件", fg=SUB)
        state["info"] = None
        state["plan"] = None

    def remove_sel():
        if running["proc"]:
            return
        sel = list(lb.curselection())
        for i in reversed(sel):
            lb.delete(i)
            files.pop(i)
        update_preview()

    def on_select(e=None):
        update_preview()

    def current_mb():
        try:
            v = float(target_var.get().strip())
            return v if v > 0 else None
        except Exception:
            return None

    def update_preview():
        refresh_buttons()
        ffprobe = find_tool("ffprobe")
        sel = lb.curselection()
        idx = sel[0] if sel else 0
        if not files or idx >= len(files):
            if not files:
                info_lbl.configure(text="尚未选择文件", fg=SUB)
            return
        mb = current_mb()
        if not ffprobe:
            info_lbl.configure(text="需要 ffmpeg 才能分析视频，请点击「开始压缩」按提示安装。", fg="#B4643F")
            return
        try:
            info = probe(ffprobe, files[idx])
        except Exception as e:
            info_lbl.configure(text="读取失败：%s" % e, fg="#B4643F")
            return
        dur = fmt_dur(info["duration"])
        src_mb = info["size"] / 1048576.0
        base = "源文件：%s · %s · %d×%d · %g fps · %.1f MB" % (
            os.path.basename(files[idx]), dur, info["w"], info["h"], info["fps"], src_mb)
        if not mb:
            info_lbl.configure(text=base, fg=SUB)
            return
        plan = make_plan(info, mb)
        state["info"], state["plan"] = info, plan
        txt = base + "\n方案：" + plan_text(info, plan, mb)
        if plan["est_mb"] > src_mb:
            txt += "\n注意：目标体积比源文件还大，压缩后反而会变大。"
        info_lbl.configure(text=txt, fg=TXT)

    def run_batch(ffmpeg, ffprobe, mb):
        running["proc"] = True
        running["cancel"] = threading.Event()
        cancel = running["cancel"]
        out_dir = None if same_dir.get() else (out_dir_var.get() or None)

        def tlog(msg):
            on_ui(log, msg)

        def worker():
            total_n = len(files)
            ok, fail = 0, []
            for i, src in enumerate(files, 1):
                if cancel.is_set():
                    tlog("已取消。")
                    break
                try:
                    info = probe(ffprobe, src)
                    plan = make_plan(info, mb)
                    out = unique_out(src, mb, out_dir)
                    tlog("─" * 46)
                    tlog("[%d/%d] %s（%s）" % (i, total_n, os.path.basename(src),
                                              fmt_dur(info["duration"])))
                    tlog("方案：" + plan_text(info, plan, mb))
                    tlog("输出：" + out)
                    t0 = time.time()
                    encode(ffmpeg, ffprobe, src, out, mb, on_log=tlog,
                           on_prog=lambda p: on_ui(set_prog, p / total_n + (i - 1) / total_n),
                           cancel=cancel, info=info, plan=plan)
                    if cancel.is_set():
                        tlog("已取消。")
                        break
                    real = os.path.getsize(out) / 1048576.0
                    tlog("完成：%.2f MB（目标 %g MB）· 耗时 %.0f 秒"
                         % (real, mb, time.time() - t0))
                    ok += 1
                except Exception as e:
                    fail.append(os.path.basename(src))
                    tlog("失败：%s" % e)
            on_ui(finish, ok, fail, cancel.is_set())

        threading.Thread(target=worker, daemon=True).start()

    def on_ui(fn, *a):
        root.after(0, lambda: fn(*a))

    def set_prog(p):
        pb["value"] = max(0.0, min(1.0, p)) * 100
        pct.configure(text="%d%%" % int(pb["value"]))

    def finish(ok, fail, cancelled):
        running["proc"] = False
        set_prog(1.0 if not cancelled else pb["value"] / 100.0)
        if cancelled:
            return
        set_prog(1.0)
        msg = "全部完成：成功 %d 个" % ok
        if fail:
            msg += "，失败 %d 个（%s）" % (len(fail), "、".join(fail))
        log("─" * 46)
        log(msg)
        if ok and messagebox.askyesno("VideoZip", msg + "\n\n要打开输出文件夹吗？"):
            d = out_dir or os.path.dirname(os.path.abspath(files[0]))
            try:
                os.startfile(d)
            except Exception:
                pass

    def do_cancel():
        if running["cancel"]:
            running["cancel"].set()
            log("正在停止…")

    flat_btn2(act, "开始压缩", start, accent=True, w=9)
    flat_btn2(act, "取消", do_cancel, w=6)

    # 下载 ffmpeg
    dl_state = {"busy": False}

    def do_download():
        if dl_state["busy"]:
            return
        dl_state["busy"] = True
        log("开始下载 ffmpeg（约 100 MB），请保持网络畅通…")
        pb.configure(mode="determinate")
        set_prog(0)

        def hook(frac, got, total):
            on_ui(set_prog, frac)

        def work():
            try:
                f, p = download_ffmpeg(progress=hook)
                on_ui(log, "ffmpeg 已就绪：%s" % f)
                on_ui(set_prog, 1.0)
                on_ui(lambda: messagebox.showinfo("VideoZip", "ffmpeg 安装完成，现在可以开始压缩了。"))
                on_ui(update_preview)
            except Exception as e:
                on_ui(log, "下载失败：%s" % e)
                on_ui(lambda: messagebox.showerror(
                    "VideoZip", "自动下载失败：%s\n\n可以手动安装 ffmpeg 后放进本程序同目录，或加入 PATH。" % e))
            finally:
                dl_state["busy"] = False

        threading.Thread(target=work, daemon=True).start()

    # 文件区按钮（依赖上面的函数，放在这里挂载）
    flat_btn(btns, "添加视频", add_dialog, accent=True)
    flat_btn(btns, "移除选中", remove_sel)
    flat_btn(btns, "清空", clear_all)

    lb.bind("<<ListboxSelect>>", on_select)
    target_var.trace_add("write", lambda *a: update_preview())

    # 拖放
    if dnd_ok:
        def on_drop(event):
            try:
                paths = root.tk.splitlist(event.data)
            except Exception:
                paths = re.findall(r"\{([^}]*)\}", event.data) or event.data.split()
            add_paths([p for p in paths])
        for w in (lb, hint, c1):
            try:
                w.drop_target_register(DND_FILES)
                w.dnd_bind("<<Drop>>", on_drop)
            except Exception:
                pass
    else:
        hint.configure(text="提示：点「添加视频」选择文件（支持多选）")

    set_target(20)
    refresh_buttons()
    _pre = [a for a in sys.argv[1:] if a.lower().endswith(
        (".mp4", ".mov", ".mkv", ".avi", ".m4v", ".wmv", ".flv", ".webm", ".ts", ".mpg", ".mpeg"))
        and os.path.isfile(a)]
    if _pre:
        add_paths(_pre)
        lb.selection_set(0)
    log("准备就绪。选择视频 → 设置目标体积 → 开始压缩。")

    ffmpeg = find_tool("ffmpeg")
    if not ffmpeg:
        log("未检测到 ffmpeg，第一次使用时会自动下载安装。")

    root.update_idletasks()
    _need_h = root.winfo_reqheight()
    _need_w = max(760, root.winfo_reqwidth())
    _cap = int(root.winfo_screenheight() * 0.9)
    root.geometry("%dx%d" % (_need_w, min(_need_h, _cap)))
    root.minsize(min(720, _need_w), min(600, _need_h))

    root.mainloop()


# ---------------------------------------------------------------- 自检/命令行

def selftest(path, target_mb, logfile):
    lines = []

    def w(s):
        lines.append(str(s))
        try:
            with open(logfile, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
        except Exception:
            pass

    try:
        ffmpeg = find_tool("ffmpeg")
        ffprobe = find_tool("ffprobe")
        w("ffmpeg=%s" % ffmpeg)
        w("ffprobe=%s" % ffprobe)
        if not ffmpeg or not ffprobe:
            w("RESULT=FAIL no ffmpeg")
            return 1
        info = probe(ffprobe, path)
        w("probe=%s" % info)
        plan = make_plan(info, target_mb)
        w("plan=%s" % plan)
        w("text=%s" % plan_text(info, plan, target_mb))
        out = os.path.join(tempfile.gettempdir(), "videozip_selftest_out.mp4")
        encode(ffmpeg, ffprobe, path, out, target_mb,
               on_log=lambda m: w("[log] " + m),
               on_prog=lambda p: None, info=info, plan=plan)
        real = os.path.getsize(out) / 1048576.0
        w("out=%s size=%.2fMB" % (out, real))
        w("RESULT=%s" % ("OK" if abs(real - target_mb) / target_mb < 0.08 else "SIZE_OFF"))
        return 0
    except Exception as e:
        import traceback
        w("EXCEPTION=%s" % e)
        w(traceback.format_exc())
        w("RESULT=FAIL")
        return 2


def main():
    if "--selftest" in sys.argv:
        i = sys.argv.index("--selftest")
        path = sys.argv[i + 1]
        mb = float(sys.argv[i + 2]) if len(sys.argv) > i + 2 else 20
        log = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "selftest.log")
        sys.exit(selftest(path, mb, log))
    main_gui()


if __name__ == "__main__":
    main()
