# TALYS Visualizer 编译打包分发指南

## 概述
本文档详细说明如何将开发完成的TALYS Visualizer编译打包并分发给最终用户。

## 编译准备

### 1. 代码结构优化
确保代码结构适合Nuitka编译：

```python
# 优化导入语句，避免动态导入
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QThread, pyqtSignal
import numpy as np
import matplotlib.pyplot as plt

# 避免使用 __import__ 或 importlib
# 避免使用 eval() 或 exec()
# 使用类型提示提高编译效率
```

### 2. 资源文件组织
```
resources/
├── icons/
│   ├── app.ico              # Windows图标
│   ├── app.png              # Linux图标
│   └── app.icns             # macOS图标
├── templates/
│   ├── basic_calculation.inp
│   ├── astrophysics.inp
│   └── fission_analysis.inp
└── talys_binaries/
    ├── windows/
    │   └── talys.exe
    ├── linux/
    │   └── talys
    └── macos/
        └── talys
```

## 编译脚本

### Windows编译
```python
# build/build_windows.py
import subprocess
import sys
import os
from pathlib import Path

def build_windows():
    """编译Windows版本"""
    
    # 确保在项目根目录
    os.chdir(Path(__file__).parent.parent)
    
    # Nuitka编译命令
    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",                    # 独立可执行文件
        "--onefile",                      # 单文件模式
        "--enable-plugin=pyqt6",          # PyQt6插件
        "--windows-disable-console",      # 隐藏控制台窗口
        "--windows-icon-from-ico=resources/icons/app.ico",
        "--include-data-dir=resources=resources",
        "--include-data-file=resources/talys_binaries/windows/talys.exe=talys.exe",
        "--output-filename=TalysVisualizer.exe",
        "--output-dir=dist/windows",
        "--assume-yes-for-downloads",     # 自动下载依赖
        "--show-progress",                # 显示进度
        "main.py"
    ]
    
    print("🔨 开始编译Windows版本...")
    print("⏳ 首次编译可能需要10-30分钟...")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Windows版本编译成功!")
        exe_path = Path("dist/windows/TalysVisualizer.exe")
        print(f"📁 可执行文件: {exe_path.absolute()}")
        print(f"📊 文件大小: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
        return True
    else:
        print("❌ 编译失败!")
        print("错误信息:")
        print(result.stderr)
        return False

if __name__ == "__main__":
    build_windows()
```

### Linux编译
```python
# build/build_linux.py
import subprocess
import sys
import os
from pathlib import Path

def build_linux():
    """编译Linux版本"""
    
    os.chdir(Path(__file__).parent.parent)
    
    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        "--onefile",
        "--enable-plugin=pyqt6",
        "--include-data-dir=resources=resources",
        "--include-data-file=resources/talys_binaries/linux/talys=talys",
        "--output-filename=TalysVisualizer",
        "--output-dir=dist/linux",
        "--assume-yes-for-downloads",
        "--show-progress",
        "main.py"
    ]
    
    print("🔨 开始编译Linux版本...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Linux版本编译成功!")
        exe_path = Path("dist/linux/TalysVisualizer")
        exe_path.chmod(0o755)  # 设置可执行权限
        print(f"📁 可执行文件: {exe_path.absolute()}")
        return True
    else:
        print("❌ 编译失败!")
        print(result.stderr)
        return False

if __name__ == "__main__":
    build_linux()
```

## 安装包制作

### Windows安装包 (NSIS)
```nsis
; installer/windows/installer.nsi
!define APP_NAME "TALYS Visualizer"
!define APP_VERSION "1.0.0"
!define APP_PUBLISHER "Your Name"
!define APP_EXE "TalysVisualizer.exe"
!define APP_ICON "resources\icons\app.ico"

Name "${APP_NAME}"
OutFile "dist\TalysVisualizer_${APP_VERSION}_Setup.exe"
InstallDir "$PROGRAMFILES64\${APP_NAME}"
RequestExecutionLevel admin

; 现代UI
!include "MUI2.nsh"
!define MUI_ICON "${APP_ICON}"
!define MUI_UNICON "${APP_ICON}"

; 安装页面
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; 卸载页面
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; 语言
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "SimpChinese"

Section "MainSection" SEC01
    SetOutPath "$INSTDIR"
    File "dist\windows\${APP_EXE}"
    File "README.md"
    File "LICENSE.txt"
    
    ; 创建开始菜单快捷方式
    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortCut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}"
    CreateShortCut "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk" "$INSTDIR\uninstall.exe"
    
    ; 创建桌面快捷方式
    CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}"
    
    ; 注册表信息
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName" "${APP_NAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayVersion" "${APP_VERSION}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "Publisher" "${APP_PUBLISHER}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" "$INSTDIR\uninstall.exe"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoRepair" 1
    
    WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\${APP_EXE}"
    Delete "$INSTDIR\README.md"
    Delete "$INSTDIR\LICENSE.txt"
    Delete "$INSTDIR\uninstall.exe"
    RMDir "$INSTDIR"
    
    Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk"
    RMDir "$SMPROGRAMS\${APP_NAME}"
    Delete "$DESKTOP\${APP_NAME}.lnk"
    
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
SectionEnd
```

### Linux AppImage创建
```bash
#!/bin/bash
# installer/linux/create_appimage.sh

set -e

APP_NAME="TalysVisualizer"
APP_VERSION="1.0.0"
ARCH="x86_64"

echo "📦 创建Linux AppImage..."

# 创建AppDir结构
rm -rf AppDir
mkdir -p AppDir/usr/bin
mkdir -p AppDir/usr/share/applications
mkdir -p AppDir/usr/share/icons/hicolor/256x256/apps
mkdir -p AppDir/usr/share/metainfo

# 复制可执行文件
cp dist/linux/TalysVisualizer AppDir/usr/bin/

# 创建.desktop文件
cat > AppDir/usr/share/applications/talysvisualizer.desktop << EOF
[Desktop Entry]
Type=Application
Name=TALYS Visualizer
Comment=Nuclear reaction calculation visualization tool
Exec=TalysVisualizer
Icon=talysvisualizer
Categories=Science;Education;Physics;
Keywords=nuclear;physics;reaction;calculation;TALYS;
StartupNotify=true
EOF

# 复制图标
cp resources/icons/app.png AppDir/usr/share/icons/hicolor/256x256/apps/talysvisualizer.png

# 创建AppStream元数据
cat > AppDir/usr/share/metainfo/talysvisualizer.appdata.xml << EOF
<?xml version="1.0" encoding="UTF-8"?>
<component type="desktop-application">
  <id>talysvisualizer</id>
  <name>TALYS Visualizer</name>
  <summary>Nuclear reaction calculation visualization tool</summary>
  <description>
    <p>A comprehensive visualization tool for TALYS nuclear reaction calculations.</p>
  </description>
  <categories>
    <category>Science</category>
    <category>Education</category>
  </categories>
</component>
EOF

# 下载AppImageTool
if [ ! -f "appimagetool-${ARCH}.AppImage" ]; then
    echo "📥 下载AppImageTool..."
    wget -q https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-${ARCH}.AppImage
    chmod +x appimagetool-${ARCH}.AppImage
fi

# 创建AppImage
echo "🔨 构建AppImage..."
./appimagetool-${ARCH}.AppImage AppDir dist/TalysVisualizer-${APP_VERSION}-${ARCH}.AppImage

echo "✅ AppImage创建完成!"
echo "📁 输出文件: dist/TalysVisualizer-${APP_VERSION}-${ARCH}.AppImage"

# 清理
rm -rf AppDir
```

## 自动化构建

### 统一构建脚本
```python
# build/build_all.py
import platform
import subprocess
import sys
import os
from pathlib import Path

def get_platform():
    """检测当前平台"""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "darwin":
        return "macos"
    else:
        return "linux"

def build_executable():
    """构建可执行文件"""
    current_platform = get_platform()
    
    scripts = {
        "windows": "build_windows.py",
        "linux": "build_linux.py",
        "macos": "build_macos.py"
    }
    
    script = scripts.get(current_platform)
    if not script:
        print(f"❌ 不支持的平台: {current_platform}")
        return False
    
    print(f"🎯 检测到平台: {current_platform}")
    
    # 运行对应的构建脚本
    result = subprocess.run([sys.executable, script], cwd=Path(__file__).parent)
    return result.returncode == 0

def create_installer():
    """创建安装包"""
    current_platform = get_platform()
    
    if current_platform == "windows":
        return create_windows_installer()
    elif current_platform == "linux":
        return create_linux_appimage()
    elif current_platform == "macos":
        return create_macos_dmg()
    
    return False

def create_windows_installer():
    """创建Windows安装包"""
    print("📦 创建Windows安装包...")
    
    # 检查NSIS是否安装
    try:
        subprocess.run(["makensis", "/VERSION"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ 请先安装NSIS: https://nsis.sourceforge.io/")
        return False
    
    # 运行NSIS脚本
    result = subprocess.run([
        "makensis",
        "installer/windows/installer.nsi"
    ])
    
    return result.returncode == 0

def create_linux_appimage():
    """创建Linux AppImage"""
    print("📦 创建Linux AppImage...")
    
    result = subprocess.run([
        "bash",
        "installer/linux/create_appimage.sh"
    ])
    
    return result.returncode == 0

def main():
    """主函数"""
    print("🚀 开始自动化构建...")
    
    # 1. 构建可执行文件
    if not build_executable():
        print("❌ 可执行文件构建失败")
        return 1
    
    # 2. 创建安装包
    if not create_installer():
        print("❌ 安装包创建失败")
        return 1
    
    print("✅ 构建完成!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

## 使用说明

### 开发者使用
```bash
# 1. 安装构建依赖
pip install nuitka

# 2. 构建当前平台版本
python build/build_all.py

# 3. 手动构建特定平台
python build/build_windows.py  # Windows
python build/build_linux.py    # Linux
python build/build_macos.py    # macOS
```

### 最终用户分发
1. **Windows**: 提供 `TalysVisualizer_Setup.exe` 安装程序
2. **Linux**: 提供 `TalysVisualizer-x.x.x-x86_64.AppImage` 文件
3. **macOS**: 提供 `TalysVisualizer.dmg` 磁盘映像

### 文件大小预期
- Windows exe: 50-80 MB
- Linux AppImage: 60-90 MB  
- macOS app: 70-100 MB

## 注意事项

1. **首次编译时间较长**: Nuitka首次编译可能需要20-30分钟
2. **依赖库处理**: 确保所有依赖都能被Nuitka正确识别
3. **资源文件**: 使用 `--include-data-dir` 包含所有必要的资源文件
4. **TALYS可执行文件**: 需要为每个平台准备对应的TALYS二进制文件
5. **测试**: 在目标平台上充分测试编译后的程序
