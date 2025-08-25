#!/usr/bin/env python3
"""
测试多语言功能
"""

import sys
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from utils.i18n import get_language_manager, tr

def test_language_manager():
    """测试语言管理器"""
    print("=== 测试语言管理器 ===")
    
    lm = get_language_manager()
    
    # 测试可用语言
    languages = lm.get_available_languages()
    print(f"可用语言: {list(languages.keys())}")
    
    # 测试默认语言
    current = lm.get_current_language()
    print(f"当前语言: {current}")
    
    # 测试翻译
    print(f"app_title (en): {tr('app_title')}")
    print(f"basic_title (en): {tr('basic_title')}")
    
    # 切换到中文
    lm.set_language('zh')
    print(f"切换到中文后:")
    print(f"app_title (zh): {tr('app_title')}")
    print(f"basic_title (zh): {tr('basic_title')}")
    
    # 切换回英文
    lm.set_language('en')
    print(f"切换回英文后:")
    print(f"app_title (en): {tr('app_title')}")
    print(f"basic_title (en): {tr('basic_title')}")
    
    print("语言管理器测试完成！")

if __name__ == "__main__":
    test_language_manager()
