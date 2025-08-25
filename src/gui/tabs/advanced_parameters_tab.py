"""
高级参数标签页
"""

import sys
from pathlib import Path
from typing import Dict, Any
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from .base_tab import BaseParameterTab

class AdvancedParametersTab(BaseParameterTab):
    """高级参数标签页"""
    
    def __init__(self):
        super().__init__()
        
    def init_ui(self):
        """初始化用户界面"""
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 创建滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        # 滚动内容
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(16)
        
        # 标题
        title = QLabel("高级参数设置")
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #212529;
                margin-bottom: 8px;
            }
        """)
        scroll_layout.addWidget(title)
        
        # 说明文字
        description = QLabel("配置TALYS的物理模型和高级计算选项。这些参数影响计算的精度和物理模型选择。")
        description.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 12px;
                margin-bottom: 16px;
            }
        """)
        description.setWordWrap(True)
        scroll_layout.addWidget(description)
        
        # 创建参数组
        self.create_level_density_group(scroll_layout)
        self.create_gamma_strength_group(scroll_layout)
        self.create_optical_model_group(scroll_layout)
        self.create_numerical_group(scroll_layout)
        
        # 弹性空间
        scroll_layout.addStretch()
        
        # 设置滚动内容
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        
        # 设置默认值
        self.set_default_values()
        
    def create_level_density_group(self, parent_layout):
        """创建能级密度模型组"""
        group, _ = self.create_group_box("能级密度模型")
        layout = self.create_form_layout()
        
        # 能级密度模型选择
        ldmodel_items = [
            ("CTM模型 (默认)", 1),
            ("Fermi gas模型", 2),
            ("Gilbert-Cameron模型", 3),
            ("微观模型", 4),
            ("Goriely模型", 5),
            ("温度相关模型", 6)
        ]
        
        self.ldmodel_combo = self.create_combo_box(ldmodel_items, "选择能级密度模型")
        layout.addRow("主模型 (ldmodel):", self.ldmodel_combo)
        self.widgets['ldmodel'] = self.ldmodel_combo
        
        # 复合核特殊模型
        self.ldmodelcn_combo = self.create_combo_box([
            ("使用主模型", 0),
            ("CTM模型", 1),
            ("Fermi gas模型", 2)
        ], "复合核能级密度模型")
        layout.addRow("复合核模型 (ldmodelcn):", self.ldmodelcn_combo)
        self.widgets['ldmodelcn'] = self.ldmodelcn_combo
        parent_layout.addWidget(group)
        
    def create_gamma_strength_group(self, parent_layout):
        """创建伽马强度函数组"""
        group, _ = self.create_group_box("伽马强度函数")
        layout = self.create_form_layout()
        
        # E1强度函数
        strength_items = [
            ("Kopecky-Uhl模型", 1),
            ("Brink-Axel模型", 2),
            ("Hartree-Fock BCS模型", 3),
            ("Hartree-Fock-Bogoliubov模型", 4),
            ("Goriely HFB模型", 5),
            ("Goriely HFB+QRPA模型", 6),
            ("Gogny HFB+QRPA模型", 7),
            ("Skyrme HFB+QRPA模型", 8),
            ("混合模型 (默认)", 9),
            ("Goriely混合模型", 10)
        ]
        
        self.strength_combo = self.create_combo_box(strength_items, "E1伽马强度函数模型")
        layout.addRow("E1强度函数 (strength):", self.strength_combo)
        self.widgets['strength'] = self.strength_combo
        
        # M1强度函数
        strengthm1_items = [
            ("标准模型", 1),
            ("增强模型", 2),
            ("Goriely模型 (默认)", 3)
        ]
        
        self.strengthm1_combo = self.create_combo_box(strengthm1_items, "M1伽马强度函数模型")
        layout.addRow("M1强度函数 (strengthm1):", self.strengthm1_combo)
        self.widgets['strengthm1'] = self.strengthm1_combo
        parent_layout.addWidget(group)
        
    def create_optical_model_group(self, parent_layout):
        """创建光学模型组"""
        group, _ = self.create_group_box("光学模型参数")
        layout = self.create_form_layout()
        
        # α粒子光学模型
        self.alphaomp_combo = self.create_combo_box([
            ("McFadden-Satchler (默认)", 1),
            ("Avrigeanu", 2),
            ("Nolte", 3)
        ], "α粒子光学模型")
        layout.addRow("α粒子模型 (alphaomp):", self.alphaomp_combo)
        self.widgets['alphaomp'] = self.alphaomp_combo
        
        # 氘核光学模型
        self.deuteronomp_combo = self.create_combo_box([
            ("Daehnick (默认)", 1),
            ("Bojowald", 2),
            ("Han-Shi-Shen", 3)
        ], "氘核光学模型")
        layout.addRow("氘核模型 (deuteronomp):", self.deuteronomp_combo)
        self.widgets['deuteronomp'] = self.deuteronomp_combo
        
        # 局域光学模型
        self.localomp_checkbox = self.create_check_box("使用局域光学模型", True, 
                                                      "使用局域而非全局光学模型")
        layout.addRow("局域模型 (localomp):", self.localomp_checkbox)
        self.widgets['localomp'] = self.localomp_checkbox
        parent_layout.addWidget(group)
        
    def create_numerical_group(self, parent_layout):
        """创建数值计算参数组"""
        group, _ = self.create_group_box("数值计算参数")
        layout = self.create_form_layout()
        
        # 能量分格数
        self.bins_spinbox = self.create_spin_box(10, 200, 40, "能量分格数量")
        layout.addRow("能量分格数 (bins):", self.bins_spinbox)
        self.widgets['bins'] = self.bins_spinbox
        
        # 最大激发能级数
        self.maxlevelstar_spinbox = self.create_spin_box(1, 100, 30, "最大激发能级数")
        layout.addRow("最大能级数 (maxlevelstar):", self.maxlevelstar_spinbox)
        self.widgets['maxlevelstar'] = self.maxlevelstar_spinbox
        
        # 最大转动量子数
        self.maxrot_spinbox = self.create_spin_box(0, 10, 2, "最大转动量子数")
        layout.addRow("最大转动数 (maxrot):", self.maxrot_spinbox)
        self.widgets['maxrot'] = self.maxrot_spinbox
        parent_layout.addWidget(group)
        
    def connect_signals(self):
        """连接信号"""
        # 所有控件的变化都触发参数更新
        for widget in self.widgets.values():
            if isinstance(widget, QComboBox):
                widget.currentTextChanged.connect(self.emit_parameters_changed)
            elif isinstance(widget, QSpinBox):
                widget.valueChanged.connect(self.emit_parameters_changed)
            elif isinstance(widget, QCheckBox):
                widget.toggled.connect(self.emit_parameters_changed)
                
    def set_default_values(self):
        """设置默认值"""
        # 根据TALYS默认值设置
        self.ldmodel_combo.setCurrentIndex(0)  # CTM模型
        self.ldmodelcn_combo.setCurrentIndex(0)  # 使用主模型
        self.strength_combo.setCurrentIndex(8)  # 混合模型 (strength=9)
        self.strengthm1_combo.setCurrentIndex(2)  # Goriely模型 (strengthm1=3)
        self.alphaomp_combo.setCurrentIndex(0)  # McFadden-Satchler
        self.deuteronomp_combo.setCurrentIndex(0)  # Daehnick
        self.localomp_checkbox.setChecked(True)
        self.bins_spinbox.setValue(40)
        self.maxlevelstar_spinbox.setValue(30)
        self.maxrot_spinbox.setValue(2)
        
    def get_parameters(self) -> Dict[str, Any]:
        """获取当前参数"""
        parameters = {
            'ldmodel': self.ldmodel_combo.currentData(),
            'ldmodelcn': self.ldmodelcn_combo.currentData(),
            'strength': self.strength_combo.currentData(),
            'strengthm1': self.strengthm1_combo.currentData(),
            'alphaomp': self.alphaomp_combo.currentData(),
            'deuteronomp': self.deuteronomp_combo.currentData(),
            'localomp': self.localomp_checkbox.isChecked(),
            'bins': self.bins_spinbox.value(),
            'maxlevelstar': self.maxlevelstar_spinbox.value(),
            'maxrot': self.maxrot_spinbox.value(),
        }
        
        return parameters
    
    def set_parameters(self, parameters: Dict[str, Any]):
        """设置参数值"""
        for param_name, value in parameters.items():
            if param_name in self.widgets:
                widget = self.widgets[param_name]
                
                if isinstance(widget, QComboBox):
                    # 根据数据值设置选择
                    for i in range(widget.count()):
                        if widget.itemData(i) == value:
                            widget.setCurrentIndex(i)
                            break
                elif isinstance(widget, QSpinBox):
                    widget.setValue(int(value))
                elif isinstance(widget, QCheckBox):
                    widget.setChecked(bool(value))
    
    def get_relevant_parameters(self, global_params: Dict[str, Any]) -> Dict[str, Any]:
        """获取与本标签页相关的参数"""
        relevant_keys = [
            'ldmodel', 'ldmodelcn', 'strength', 'strengthm1',
            'alphaomp', 'deuteronomp', 'localomp',
            'bins', 'maxlevelstar', 'maxrot'
        ]
        return {k: v for k, v in global_params.items() if k in relevant_keys}
    
    def validate_parameters(self) -> tuple[bool, str]:
        """验证当前参数"""
        try:
            params = self.get_parameters()
            
            # 检查数值范围
            if params['bins'] < 10 or params['bins'] > 200:
                return False, "能量分格数必须在10-200之间"
                
            if params['maxlevelstar'] < 1 or params['maxlevelstar'] > 100:
                return False, "最大能级数必须在1-100之间"
                
            if params['maxrot'] < 0 or params['maxrot'] > 10:
                return False, "最大转动数必须在0-10之间"
            
            return True, ""
            
        except Exception as e:
            return False, f"验证时发生错误: {str(e)}"
    
    def reset_to_defaults(self):
        """重置到默认值"""
        self.set_default_values()
