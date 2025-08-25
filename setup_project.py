#!/usr/bin/env python3
"""
TALYS Visualizer 项目初始化脚本
根据 Phase1_Implementation_Guide.md 创建完整的项目结构
"""

import os
from pathlib import Path

def create_directory_structure():
    """创建项目目录结构"""
    
    directories = [
        # 主要源代码目录
        "src",
        "src/core",
        "src/gui", 
        "src/visualization",
        "src/utils",
        
        # 配置目录
        "config",
        
        # 测试目录
        "tests",
        
        # 构建脚本目录
        "build",
        
        # 安装包制作目录
        "installer",
        "installer/windows",
        "installer/linux", 
        "installer/macos",
        
        # 文档目录
        "docs",
        
        # 资源目录
        "resources",
        "resources/icons",
        "resources/templates",
        "resources/examples",
        "resources/talys_binaries",
        "resources/talys_binaries/windows",
        "resources/talys_binaries/linux",
        "resources/talys_binaries/macos",
        
        # 输出目录
        "dist",
        "logs",
        "temp"
    ]
    
    print("📁 创建项目目录结构...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory}/")
    
    # 创建 __init__.py 文件
    init_files = [
        "src/__init__.py",
        "src/core/__init__.py", 
        "src/gui/__init__.py",
        "src/visualization/__init__.py",
        "src/utils/__init__.py",
        "tests/__init__.py"
    ]
    
    for init_file in init_files:
        Path(init_file).touch()
        print(f"   ✅ {init_file}")

def create_requirements_txt():
    """创建 requirements.txt"""
    
    requirements = """PyQt6>=6.4.0
matplotlib>=3.6.0
numpy>=1.21.0
pandas>=1.5.0
scipy>=1.9.0
pyqtgraph>=0.13.0
nuitka>=1.8.0
"""
    
    with open("requirements.txt", "w") as f:
        f.write(requirements)
    
    print("✅ requirements.txt")

def create_main_py():
    """创建主程序入口文件"""
    
    main_content = '''#!/usr/bin/env python3
"""
TALYS Visualizer - 主程序入口
"""

import sys
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# 添加src目录到Python路径
sys.path.insert(0, 'src')

from gui.main_window import MainWindow
from utils.logger import setup_logger
from config.settings import Settings

def main():
    """主函数"""
    # 设置日志
    setup_logger()
    logger = logging.getLogger(__name__)
    
    # 创建应用
    app = QApplication(sys.argv)
    app.setApplicationName(Settings.APP_NAME)
    app.setApplicationVersion(Settings.APP_VERSION)
    
    # 设置应用样式
    app.setStyle('Fusion')
    
    try:
        # 创建主窗口
        main_window = MainWindow()
        main_window.show()
        
        logger.info(f"{Settings.APP_NAME} started successfully")
        
        # 运行应用
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Application failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    with open("main.py", "w") as f:
        f.write(main_content)
    
    print("✅ main.py")

def create_config_files():
    """创建配置文件"""
    
    # settings.py
    settings_content = '''"""
TALYS Visualizer 配置文件
"""

import os
from pathlib import Path

class Settings:
    """应用程序设置"""
    
    # 应用信息
    APP_NAME = "TALYS Visualizer"
    APP_VERSION = "0.1.0"
    APP_AUTHOR = "TALYS Visualizer Team"
    
    # 路径设置
    BASE_DIR = Path(__file__).parent.parent
    CONFIG_DIR = BASE_DIR / "config"
    RESOURCES_DIR = BASE_DIR / "resources"
    TEMP_DIR = BASE_DIR / "temp"
    LOGS_DIR = BASE_DIR / "logs"
    
    # TALYS设置
    TALYS_EXECUTABLE = "talys"  # 可在GUI中配置
    TALYS_TIMEOUT = 300  # 5分钟超时
    
    # GUI设置
    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 900
    WINDOW_MIN_WIDTH = 1000
    WINDOW_MIN_HEIGHT = 700
    
    # 日志设置
    LOG_LEVEL = "INFO"
    LOG_FILE = LOGS_DIR / "talys_visualizer.log"
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5
    
    # 绘图设置
    PLOT_DPI = 100
    PLOT_STYLE = "default"
    
    # 数据设置
    MAX_DATA_POINTS = 10000
    DATA_CACHE_SIZE = 100
    
    @classmethod
    def ensure_directories(cls):
        """确保必要的目录存在"""
        cls.TEMP_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)
'''
    
    with open("config/settings.py", "w") as f:
        f.write(settings_content)
    
    # __init__.py for config
    with open("config/__init__.py", "w") as f:
        f.write('"""配置模块"""')
    
    print("✅ config/settings.py")
    print("✅ config/__init__.py")

def create_readme():
    """创建 README.md"""
    
    readme_content = '''# TALYS Visualizer

一个用于TALYS核反应计算的可视化桌面应用程序。

## 项目状态

🚧 **开发中** - 当前处于 Phase 1: 基础架构开发阶段

## 技术栈

- **GUI框架**: PyQt6
- **绘图库**: Matplotlib, PyQtGraph  
- **数据处理**: NumPy, Pandas
- **编译工具**: Nuitka
- **Python版本**: 3.8+

## 开发环境设置

### 1. 克隆项目
```bash
git clone <repository-url>
cd talys_visualizer
```

### 2. 创建虚拟环境
```bash
python -m venv talys_visualizer_env
source talys_visualizer_env/bin/activate  # Linux/Mac
# 或
talys_visualizer_env\\Scripts\\activate     # Windows
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 运行程序
```bash
python main.py
```

## 项目结构

```
talys_visualizer/
├── main.py                     # 程序入口
├── requirements.txt            # Python依赖
├── config/                     # 配置文件
├── src/                        # 源代码
│   ├── core/                   # 核心逻辑
│   ├── gui/                    # GUI组件
│   ├── visualization/          # 可视化组件
│   └── utils/                  # 工具函数
├── tests/                      # 测试文件
├── build/                      # 构建脚本
├── installer/                  # 安装包制作
├── docs/                       # 文档
└── resources/                  # 资源文件
```

## 开发文档

- [开发计划](TALYS_Visualizer_Development_Plan.md)
- [Phase 1 实施指南](Phase1_Implementation_Guide.md)
- [参数提取计划](TALYS_Default_Parameters.md)
- [构建分发指南](Build_and_Distribution_Guide.md)
- [开发规则](talys-visualizer-development-rules.md)

## 许可证

[待定]

## 贡献

请参阅开发文档了解贡献指南。
'''
    
    with open("README.md", "w") as f:
        f.write(readme_content)
    
    print("✅ README.md")

def create_gitignore():
    """创建 .gitignore"""
    
    gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Virtual environments
talys_visualizer_env/
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
logs/
temp/
*.log
*.tmp

# TALYS files
talys.inp
talys.out
*.tot
*.spe
*.ang
*.ddx
*.gam

# Compiled binaries
*.exe
*.app
*.AppImage
*.dmg
'''
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    
    print("✅ .gitignore")

def main():
    """主函数"""
    print("🚀 TALYS Visualizer 项目初始化")
    print("=" * 50)
    
    # 创建目录结构
    create_directory_structure()
    print()
    
    # 创建配置文件
    print("📝 创建配置文件...")
    create_requirements_txt()
    create_main_py()
    create_config_files()
    create_readme()
    create_gitignore()
    print()
    
    print("✅ 项目初始化完成!")
    print()
    print("📋 下一步:")
    print("1. 创建虚拟环境: python -m venv talys_visualizer_env")
    print("2. 激活虚拟环境: source talys_visualizer_env/bin/activate")
    print("3. 安装依赖: pip install -r requirements.txt")
    print("4. 开始开发核心模块")

if __name__ == "__main__":
    main()
