# 第三方组件与许可说明 / NOTICE

VideoZip 的源码以 MIT 许可发布（见 [LICENSE](LICENSE)）。本文件说明运行链条上涉及的第三方组件，以及本仓库为什么**不提交**某些文件。

## 1. 本仓库不包含的内容

| 内容 | 原因 |
| --- | --- |
| `VideoZip.exe` 及 PyInstaller 打包产物 | 内含 Python 运行时、Tcl/Tk、OpenSSL 等第三方二进制，体积约 15 MB；仓库不承载二进制，改由 GitHub Releases / CI 产物分发 |
| `python312.dll`、`tcl86t.dll`、`tk86t.dll`、`libssl-3.dll`、`libcrypto-3.dll`、`VCRUNTIME140.dll` 等 | 同上，属于 Python / Tcl-Tk / OpenSSL / MSVC 运行时的再分发物，各自许可与 NOTICE 义务应由打包者按其条款处理 |
| FFmpeg / FFprobe 可执行文件 | **不做重新分发**。程序在用户本机首次运行时检测，缺失则由用户自行确认后从上游构建站下载 |

这样做既是体积考虑，也让每个组件的许可证义务留在它本该被履行的位置。

## 2. 运行时依赖

### tkinterdnd2

- 用途：文件拖放（可选，未安装时程序自动降级为"添加视频"按钮）
- 许可：MIT
- 上游：<https://pypi.org/project/tkinterdnd2/>
- 其内置的 TkDND 扩展为 Tcl/Tk 许可（BSD-style）

### Python / Tcl / Tk

- 仅在被 PyInstaller 打包时嵌入 exe，源码运行模式下由用户自己的 Python 提供
- Python 软件基金会许可协议（PSF License），Tcl/Tk 为 BSD-style 许可

### FFmpeg、libx264、AAC 编码器

- 用途：解码输入、H.264 编码、AAC 音频编码
- VideoZip **不包含、不捆绑、不重新分发** FFmpeg 二进制
- 默认下载源：`https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip`（Windows essentials 构建）
- FFmpeg 主体为 LGPL v2.1+；启用 libx264 等 GPL 组件时整体按 GPL 分发
- 如果你的使用场景（例如闭源商业分发）对 GPL 敏感，请自行替换为 LGPL 构建或商业授权编码器，本程序通过命令行调用 `ffmpeg`，替换后端不影响其他功能
- 上游：<https://ffmpeg.org/legal.html>

## 3. 使用者的责任

1. 压缩、转码他人作品前，确认你拥有相应权利或已获授权
2. 若将本程序（含打包后的 exe）再分发，需同时满足上述各组件的许可条款，尤其是 FFmpeg 的 LGPL/GPL 义务
3. 程序仅在本机调用命令行工具处理本地文件，不上传任何内容到网络（除用户主动确认的 FFmpeg 下载外）

---

作者：chokoketsu · <https://github.com/chokoketsu>
