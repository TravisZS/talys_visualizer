"""
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
