"""
参数同步器 - 管理各标签页间的参数同步
"""

import logging
from typing import Dict, Any, List
from PyQt6.QtCore import QObject, pyqtSignal

class ParameterSynchronizer(QObject):
    """参数同步器类"""
    
    # 信号定义
    parameters_updated = pyqtSignal(dict)  # 参数更新时发出
    parameter_validation_failed = pyqtSignal(str, str)  # 参数验证失败时发出
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.parameters = {}
        self.tabs = []
        self.validation_rules = {}
        self._setup_default_parameters()
        self._setup_validation_rules()
        
    def _setup_default_parameters(self):
        """设置默认参数"""
        self.parameters = {
            # 必需参数
            'projectile': 'n',
            'element': 'H', 
            'mass': 1,
            'energy': 1.0,
            
            # 基础输出选项
            'channels': True,
            'outspectra': False,
            'outangle': False,
            'outlevels': False,
            
            # 高级模型参数
            'ldmodel': 1,
            'strength': 9,
            'alphaomp': 1,
            'deuteronomp': 1,
            
            # 数值计算参数
            'bins': 40,
            'maxlevelstar': 30,
            
            # 输出控制
            'flagmain': True,
            'flagbasic': True,
            'flagpop': False,
            'flagcheck': False,
        }
        
    def _setup_validation_rules(self):
        """设置参数验证规则"""
        self.validation_rules = {
            'projectile': {
                'type': 'choice',
                'choices': ['n', 'p', 'd', 't', 'h', 'a', 'g'],
                'description': '入射粒子类型'
            },
            'mass': {
                'type': 'int',
                'range': [1, 300],
                'description': '目标核质量数'
            },
            'energy': {
                'type': 'float',
                'range': [0.001, 200.0],
                'description': '入射能量(MeV)'
            },
            'ldmodel': {
                'type': 'choice',
                'choices': [1, 2, 3, 4, 5, 6],
                'description': '能级密度模型'
            },
            'strength': {
                'type': 'choice',
                'choices': list(range(1, 11)),
                'description': 'E1伽马强度函数模型'
            },
            'bins': {
                'type': 'int',
                'range': [10, 200],
                'description': '能量分格数'
            },
            'maxlevelstar': {
                'type': 'int',
                'range': [1, 100],
                'description': '最大激发能级数'
            }
        }
        
    def register_tab(self, tab):
        """注册标签页"""
        if hasattr(tab, 'parameters_changed'):
            self.tabs.append(tab)
            tab.parameters_changed.connect(self.on_parameters_changed)
            self.logger.debug(f"注册标签页: {tab.__class__.__name__}")
        else:
            self.logger.warning(f"标签页 {tab.__class__.__name__} 没有 parameters_changed 信号")
    
    def on_parameters_changed(self, params: Dict[str, Any]):
        """处理参数变化"""
        sender_tab = self.sender()
        self.logger.debug(f"收到参数变化: {params} 来自 {sender_tab.__class__.__name__}")
        
        # 验证参数
        validation_errors = self.validate_parameters(params)
        if validation_errors:
            for param_name, error_msg in validation_errors.items():
                self.parameter_validation_failed.emit(param_name, error_msg)
                self.logger.warning(f"参数验证失败: {param_name} - {error_msg}")
            return
        
        # 更新全局参数
        old_params = self.parameters.copy()
        self.parameters.update(params)
        
        # 检查是否有实际变化
        if old_params != self.parameters:
            # 通知其他标签页更新（除了发送者）
            for tab in self.tabs:
                if tab != sender_tab and hasattr(tab, 'update_from_global_parameters'):
                    try:
                        tab.update_from_global_parameters(self.parameters)
                    except Exception as e:
                        self.logger.error(f"更新标签页 {tab.__class__.__name__} 失败: {e}")
            
            # 发出全局参数更新信号
            self.parameters_updated.emit(self.parameters.copy())
            self.logger.debug("全局参数已更新并同步到所有标签页")
    
    def validate_parameters(self, params: Dict[str, Any]) -> Dict[str, str]:
        """验证参数"""
        errors = {}
        
        for param_name, value in params.items():
            if param_name in self.validation_rules:
                rule = self.validation_rules[param_name]
                error = self._validate_single_parameter(param_name, value, rule)
                if error:
                    errors[param_name] = error
        
        return errors
    
    def _validate_single_parameter(self, name: str, value: Any, rule: Dict) -> str:
        """验证单个参数"""
        param_type = rule['type']
        description = rule.get('description', name)
        
        try:
            if param_type == 'choice':
                if value not in rule['choices']:
                    return f"{description}必须是以下值之一: {rule['choices']}"
                    
            elif param_type == 'int':
                if not isinstance(value, int):
                    try:
                        value = int(value)
                    except (ValueError, TypeError):
                        return f"{description}必须是整数"
                
                if 'range' in rule:
                    min_val, max_val = rule['range']
                    if not (min_val <= value <= max_val):
                        return f"{description}必须在 {min_val} 到 {max_val} 之间"
                        
            elif param_type == 'float':
                if not isinstance(value, (int, float)):
                    try:
                        value = float(value)
                    except (ValueError, TypeError):
                        return f"{description}必须是数字"
                
                if 'range' in rule:
                    min_val, max_val = rule['range']
                    if not (min_val <= value <= max_val):
                        return f"{description}必须在 {min_val} 到 {max_val} 之间"
                        
        except Exception as e:
            return f"{description}验证时发生错误: {str(e)}"
        
        return ""  # 无错误
    
    def get_all_parameters(self) -> Dict[str, Any]:
        """获取所有参数"""
        return self.parameters.copy()
    
    def set_parameters(self, params: Dict[str, Any], validate: bool = True):
        """设置参数"""
        if validate:
            validation_errors = self.validate_parameters(params)
            if validation_errors:
                for param_name, error_msg in validation_errors.items():
                    self.parameter_validation_failed.emit(param_name, error_msg)
                return False
        
        self.parameters.update(params)
        
        # 通知所有标签页更新
        for tab in self.tabs:
            if hasattr(tab, 'update_from_global_parameters'):
                try:
                    tab.update_from_global_parameters(self.parameters)
                except Exception as e:
                    self.logger.error(f"更新标签页 {tab.__class__.__name__} 失败: {e}")
        
        # 发出全局参数更新信号
        self.parameters_updated.emit(self.parameters.copy())
        return True
    
    def reset_parameters(self):
        """重置参数到默认值"""
        self.logger.info("重置参数到默认值")
        self._setup_default_parameters()
        
        # 通知所有标签页更新
        for tab in self.tabs:
            if hasattr(tab, 'update_from_global_parameters'):
                try:
                    tab.update_from_global_parameters(self.parameters)
                except Exception as e:
                    self.logger.error(f"重置标签页 {tab.__class__.__name__} 失败: {e}")
        
        # 发出全局参数更新信号
        self.parameters_updated.emit(self.parameters.copy())
    
    def get_parameter(self, name: str, default=None):
        """获取单个参数"""
        return self.parameters.get(name, default)
    
    def set_parameter(self, name: str, value: Any, validate: bool = True):
        """设置单个参数"""
        return self.set_parameters({name: value}, validate)
    
    def has_parameter(self, name: str) -> bool:
        """检查是否存在指定参数"""
        return name in self.parameters
    
    def get_validation_rule(self, name: str) -> Dict:
        """获取参数验证规则"""
        return self.validation_rules.get(name, {})
    
    def add_validation_rule(self, name: str, rule: Dict):
        """添加参数验证规则"""
        self.validation_rules[name] = rule
        self.logger.debug(f"添加验证规则: {name}")
    
    def remove_validation_rule(self, name: str):
        """移除参数验证规则"""
        if name in self.validation_rules:
            del self.validation_rules[name]
            self.logger.debug(f"移除验证规则: {name}")
    
    def get_required_parameters(self) -> List[str]:
        """获取必需参数列表"""
        return ['projectile', 'element', 'mass', 'energy']
    
    def validate_required_parameters(self) -> List[str]:
        """验证必需参数是否完整"""
        missing = []
        required = self.get_required_parameters()
        
        for param in required:
            if param not in self.parameters or self.parameters[param] is None:
                missing.append(param)
        
        return missing
    
    def is_ready_for_calculation(self) -> tuple[bool, List[str]]:
        """检查是否准备好进行计算"""
        missing_required = self.validate_required_parameters()
        
        if missing_required:
            return False, missing_required
        
        # 验证所有参数
        validation_errors = self.validate_parameters(self.parameters)
        if validation_errors:
            return False, list(validation_errors.keys())
        
        return True, []
    
    def export_to_dict(self) -> Dict[str, Any]:
        """导出参数到字典（用于保存项目文件）"""
        return {
            'parameters': self.parameters.copy(),
            'validation_rules': self.validation_rules.copy(),
            'version': '1.0'
        }
    
    def import_from_dict(self, data: Dict[str, Any]) -> bool:
        """从字典导入参数（用于加载项目文件）"""
        try:
            if 'parameters' in data:
                self.set_parameters(data['parameters'], validate=True)
            
            if 'validation_rules' in data:
                self.validation_rules.update(data['validation_rules'])
            
            self.logger.info("成功导入参数")
            return True
            
        except Exception as e:
            self.logger.error(f"导入参数失败: {e}")
            return False
