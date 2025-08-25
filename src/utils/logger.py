"""
TALYS Visualizer 日志系统
提供统一的日志记录功能
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional

# 添加config目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config.settings import Settings

def setup_logger(
    name: Optional[str] = None,
    level: str = None,
    log_file: Optional[Path] = None
) -> logging.Logger:
    """
    设置日志记录器
    
    Args:
        name: 日志记录器名称，默认为根记录器
        level: 日志级别，默认使用配置文件中的设置
        log_file: 日志文件路径，默认使用配置文件中的设置
    
    Returns:
        配置好的日志记录器
    """
    
    # 确保日志目录存在
    Settings.ensure_directories()
    
    # 获取日志记录器
    logger = logging.getLogger(name)
    
    # 如果已经配置过，直接返回
    if logger.handlers:
        return logger
    
    # 设置日志级别
    log_level = level or Settings.LOG_LEVEL
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # 创建格式化器
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器（带轮转）
    file_path = log_file or Settings.LOG_FILE
    file_handler = logging.handlers.RotatingFileHandler(
        filename=file_path,
        maxBytes=Settings.LOG_MAX_SIZE,
        backupCount=Settings.LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # 防止日志传播到父记录器
    logger.propagate = False
    
    logger.info(f"日志系统初始化完成 - 级别: {log_level}")
    logger.info(f"日志文件: {file_path}")
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """
    获取指定名称的日志记录器
    
    Args:
        name: 日志记录器名称
    
    Returns:
        日志记录器
    """
    return logging.getLogger(name)

class LoggerMixin:
    """
    日志记录器混入类
    为类提供日志记录功能
    """
    
    @property
    def logger(self) -> logging.Logger:
        """获取当前类的日志记录器"""
        return get_logger(self.__class__.__name__)

# 示例使用
if __name__ == "__main__":
    # 设置根日志记录器
    logger = setup_logger()
    
    # 测试日志记录
    logger.debug("这是调试信息")
    logger.info("这是信息")
    logger.warning("这是警告")
    logger.error("这是错误")
    
    # 测试类混入
    class TestClass(LoggerMixin):
        def test_method(self):
            self.logger.info("测试类日志记录")
    
    test = TestClass()
    test.test_method()
