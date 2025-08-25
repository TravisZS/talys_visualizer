#!/usr/bin/env python3
"""
修复布局问题的脚本
"""

import re
from pathlib import Path

def fix_layout_issues():
    """修复所有标签页的布局问题"""
    
    # 需要修复的文件
    files_to_fix = [
        "src/gui/tabs/advanced_parameters_tab.py",
        "src/gui/tabs/output_options_tab.py", 
        "src/gui/tabs/expert_mode_tab.py"
    ]
    
    for file_path in files_to_fix:
        full_path = Path(file_path)
        if not full_path.exists():
            print(f"文件不存在: {file_path}")
            continue
            
        print(f"修复文件: {file_path}")
        
        # 读取文件内容
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 修复 create_group_box 调用
        content = re.sub(
            r'group = self\.create_group_box\("([^"]+)"\)',
            r'group, _ = self.create_group_box("\1")',
            content
        )
        
        # 修复带布局类型的调用
        content = re.sub(
            r'group = self\.create_group_box\("([^"]+)", ([^)]+)\)',
            r'group, layout = self.create_group_box("\1", \2)',
            content
        )
        
        # 移除重复的 group.setLayout(layout) 调用
        content = re.sub(
            r'\s+group\.setLayout\(layout\)\s+',
            '\n        ',
            content
        )
        
        # 写回文件
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"已修复: {file_path}")

if __name__ == "__main__":
    fix_layout_issues()
    print("所有布局问题已修复！")
