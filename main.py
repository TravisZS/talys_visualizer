#!/usr/bin/env python3
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
