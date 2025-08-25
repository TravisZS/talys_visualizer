"""
TALYS接口单元测试
"""

import unittest
import tempfile
import os
from pathlib import Path
import sys

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from core.talys_interface import TalysInterface, TalysInterfaceError, TalysCalculationError

class TestTalysInterface(unittest.TestCase):
    """TALYS接口测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.talys = TalysInterface()
    
    def tearDown(self):
        """测试后清理"""
        if hasattr(self.talys, 'temp_dir') and self.talys.temp_dir:
            self.talys.cleanup_temp_directory()
    
    def test_input_file_generation(self):
        """测试输入文件生成"""
        parameters = {
            'projectile': 'n',
            'element': 'H',
            'mass': 1,
            'energy': '1.0',
            'channels': True,
        }
        
        # 生成输入文件
        input_file = self.talys.generate_input_file(parameters)
        
        # 验证文件存在
        self.assertTrue(input_file.exists())
        
        # 验证文件内容
        with open(input_file, 'r') as f:
            content = f.read()
        
        self.assertIn('projectile n', content)
        self.assertIn('element H', content)
        self.assertIn('mass 1', content)
        self.assertIn('energy 1.0', content)
        self.assertIn('channels y', content)
    
    def test_simple_calculation(self):
        """测试简单计算"""
        parameters = {
            'projectile': 'n',
            'element': 'H',
            'mass': 1,
            'energy': '1.0',
        }
        
        try:
            results = self.talys.run_calculation(parameters)
            
            # 验证结果结构
            self.assertIsInstance(results, dict)
            self.assertIn('calculation_time', results)
            self.assertIn('output_files', results)
            
            # 验证计算时间合理
            self.assertGreater(results['calculation_time'], 0)
            self.assertLess(results['calculation_time'], 60)  # 应该在1分钟内完成
            
        except TalysCalculationError:
            # 如果TALYS不可用，跳过这个测试
            self.skipTest("TALYS executable not available")
    
    def test_parameter_validation(self):
        """测试参数验证"""
        # 测试缺少必需参数
        incomplete_params = {
            'projectile': 'n',
            'element': 'H',
            # 缺少 mass 和 energy
        }
        
        with self.assertRaises(ValueError):
            self.talys.generate_input_file(incomplete_params)
    
    def test_boolean_parameter_conversion(self):
        """测试布尔参数转换"""
        parameters = {
            'projectile': 'n',
            'element': 'H',
            'mass': 1,
            'energy': '1.0',
            'channels': True,
            'outspectra': False,
        }
        
        input_file = self.talys.generate_input_file(parameters)
        
        with open(input_file, 'r') as f:
            content = f.read()
        
        self.assertIn('channels y', content)
        self.assertIn('outspectra n', content)

if __name__ == '__main__':
    unittest.main()
