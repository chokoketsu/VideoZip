@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ============================================
echo  VideoZip build script        by chokoketsu
echo ============================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo [x] 找不到 python，请先安装 Python 3.10+ 并加入 PATH。
    exit /b 1
)

echo [1/3] 安装构建依赖...
python -m pip install --upgrade pyinstaller tkinterdnd2 >nul || goto :failed

echo [2/3] 清理旧产物...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo [3/3] 开始打包（单文件、无控制台）...
python -m PyInstaller ^
    --noconfirm --clean ^
    --onefile --windowed ^
    --name VideoZip ^
    --icon "%~dp0assets\icon.ico" ^
    --collect-all tkinterdnd2 ^
    --workpath build --distpath dist --specpath build ^
    videozip.py || goto :failed

echo.
echo [ok] 完成：%~dp0dist\VideoZip.exe
exit /b 0

:failed
echo.
echo [x] 构建失败，请查看上方输出。
exit /b 1
