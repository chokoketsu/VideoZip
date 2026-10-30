# Changelog

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.0] - 2026-10-30

首个公开版本。

### 新增

- 目标体积反推编码参数：按 `目标字节 × 8 / 时长` 计算总码率，预留 5% 容器开销
- 音频码率按预算自动分档（48 / 64 / 96 / 128 / 160 / 192 kbps），单声道上限 96
- bpp 画质守卫：低于 0.078 自动降到标准分辨率档，仍不足且帧率 > 26 时降至 24 fps
- 源画质封顶：码率不超过源码率 1.2 倍，避免"压缩后变大"
- 双遍 ABR 编码（`-maxrate` 1.5×、`-bufsize` 2.5×），`+faststart` 前置索引
- 批量队列、拖放添加、实时进度、中途取消
- ffmpeg/ffprobe 自动探测（环境变量、程序目录、PATH、winget、常见安装路径）
- ffmpeg 缺失时一键下载到 `%LOCALAPPDATA%\VideoZip`
- `--selftest` 命令行自检：探测、出方案、编码一次并核对体积偏差
- 作者标识：窗口右上角 `@chokoketsu`，点击跳转 GitHub 主页

[1.0.0]: https://github.com/chokoketsu
