"""
基础参数标签页
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
from utils.i18n import tr

class BasicParametersTab(BaseParameterTab):
    """基础参数标签页"""
    
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
        self.title_label = QLabel(tr('basic_title'))
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #212529;
                margin-bottom: 8px;
            }
        """)
        scroll_layout.addWidget(self.title_label)

        # 说明文字
        self.description_label = QLabel(tr('basic_description'))
        self.description_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 12px;
                margin-bottom: 16px;
            }
        """)
        self.description_label.setWordWrap(True)
        scroll_layout.addWidget(self.description_label)
        
        # 创建参数组
        self.create_target_group(scroll_layout)
        self.create_projectile_group(scroll_layout)
        self.create_energy_group(scroll_layout)
        self.create_calculation_group(scroll_layout)
        
        # 弹性空间
        scroll_layout.addStretch()
        
        # 设置滚动内容
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        
        # 设置默认值
        self.set_default_values()
        
    def create_target_group(self, parent_layout):
        """创建目标核参数组"""
        group, _ = self.create_group_box(tr('group_target'))
        layout = self.create_form_layout()

        # 原子序数
        self.z_spinbox = self.create_spin_box(1, 118, 1, tr('tooltip_atomic_number'))
        self.z_label = QLabel(tr('label_atomic_number'))
        layout.addRow(self.z_label, self.z_spinbox)
        self.widgets['z'] = self.z_spinbox

        # 质量数
        self.a_spinbox = self.create_spin_box(1, 300, 1, tr('tooltip_mass_number'))
        self.a_label = QLabel(tr('label_mass_number'))
        layout.addRow(self.a_label, self.a_spinbox)
        self.widgets['mass'] = self.a_spinbox

        # 元素符号（自动更新）
        self.element_label = QLabel("H")
        self.element_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #28a745;
                font-size: 14px;
                padding: 4px 8px;
                background-color: #d4edda;
                border: 1px solid #c3e6cb;
                border-radius: 4px;
            }
        """)
        self.element_row_label = QLabel(tr('label_element'))
        layout.addRow(self.element_row_label, self.element_label)

        # 核素表示
        self.nuclide_label = QLabel("¹H")
        self.nuclide_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #495057;
                font-size: 16px;
                padding: 4px 8px;
            }
        """)
        self.nuclide_row_label = QLabel(tr('label_nuclide'))
        layout.addRow(self.nuclide_row_label, self.nuclide_label)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)

    def create_projectile_group(self, parent_layout):
        """创建入射粒子参数组"""
        group, _ = self.create_group_box(tr('group_projectile'))
        layout = self.create_form_layout()

        # 粒子类型
        self.projectiles_data = [
            (tr('projectile_neutron'), 'n'),
            (tr('projectile_proton'), 'p'),
            (tr('projectile_deuteron'), 'd'),
            (tr('projectile_triton'), 't'),
            (tr('projectile_helium3'), 'h'),
            (tr('projectile_alpha'), 'a'),
            (tr('projectile_gamma'), 'g')
        ]

        self.projectile_combo = self.create_combo_box(self.projectiles_data, tr('tooltip_particle_type', "选择入射粒子类型"))
        self.projectile_label = QLabel(tr('label_particle_type'))
        layout.addRow(self.projectile_label, self.projectile_combo)
        self.widgets['projectile'] = self.projectile_combo

        # 粒子信息显示
        self.projectile_info = QLabel(tr('info_neutron', "中子：电荷=0，质量=1.008665 u"))
        self.projectile_info.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 11px;
                font-style: italic;
                padding: 4px;
            }
        """)
        layout.addRow("", self.projectile_info)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)

    def create_energy_group(self, parent_layout):
        """创建能量参数组"""
        group, layout = self.create_group_box(tr('group_energy'))


        # 能量模式选择
        mode_layout = QHBoxLayout()
        self.single_energy_radio = self.create_radio_button(tr('radio_single_energy'), True, tr('tooltip_single_energy'))
        self.energy_range_radio = self.create_radio_button(tr('radio_energy_range'), False, tr('tooltip_energy_range'))
        self.energy_range_radio.setEnabled(False)  # 暂时禁用

        mode_layout.addWidget(self.single_energy_radio)
        mode_layout.addWidget(self.energy_range_radio)
        mode_layout.addStretch()
        layout.addLayout(mode_layout)

        # 单一能量输入
        single_layout = QHBoxLayout()
        self.energy_label = QLabel(tr('label_energy'))
        single_layout.addWidget(self.energy_label)

        self.single_energy_spinbox = self.create_double_spin_box(
            0.001, 200.0, 1.0, 3, tr('tooltip_energy')
        )
        self.single_energy_spinbox.setSuffix(" MeV")
        single_layout.addWidget(self.single_energy_spinbox)
        self.widgets['energy'] = self.single_energy_spinbox

        single_layout.addStretch()
        layout.addLayout(single_layout)
        
        # 能量范围输入（暂时隐藏）
        range_widget = QWidget()
        range_layout = QHBoxLayout(range_widget)
        self.energy_min_label = QLabel(tr('label_min'))
        range_layout.addWidget(self.energy_min_label)

        self.energy_min_spinbox = self.create_double_spin_box(
            0.001, 200.0, 1.0, 3, tr('tooltip_min_energy')
        )
        self.energy_min_spinbox.setSuffix(" MeV")
        self.energy_min_spinbox.setEnabled(False)
        range_layout.addWidget(self.energy_min_spinbox)

        self.energy_max_label = QLabel(tr('label_max'))
        range_layout.addWidget(self.energy_max_label)

        self.energy_max_spinbox = self.create_double_spin_box(
            0.001, 200.0, 20.0, 3, tr('tooltip_max_energy')
        )
        self.energy_max_spinbox.setSuffix(" MeV")
        self.energy_max_spinbox.setEnabled(False)
        range_layout.addWidget(self.energy_max_spinbox)

        range_layout.addStretch()
        layout.addWidget(range_widget)
        range_widget.setVisible(False)  # 暂时隐藏

        parent_layout.addWidget(group)

    def create_calculation_group(self, parent_layout):
        """创建计算控制组"""
        group, layout = self.create_group_box(tr('group_calculation'))


        # 快速计算按钮
        button_layout = QHBoxLayout()

        self.run_button = self.create_push_button(tr('button_run_calculation'), True, tr('tooltip_run_calculation'))
        self.run_button.clicked.connect(self.on_run_calculation)
        button_layout.addWidget(self.run_button)

        self.validate_button = self.create_push_button(tr('button_validate'), False, tr('tooltip_validate'))
        self.validate_button.clicked.connect(self.on_validate_parameters)
        button_layout.addWidget(self.validate_button)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        # 参数摘要
        self.summary_label = QLabel()
        self.summary_label.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 12px;
                color: #495057;
                font-family: 'Courier New', monospace;
                font-size: 11px;
            }
        """)
        self.summary_title_label = QLabel(tr('label_parameter_summary'))
        layout.addWidget(self.summary_title_label)
        layout.addWidget(self.summary_label)

        parent_layout.addWidget(group)
        
    def connect_signals(self):
        """连接信号"""
        # 原子序数改变时更新元素符号
        self.z_spinbox.valueChanged.connect(self.update_element_info)
        self.a_spinbox.valueChanged.connect(self.update_element_info)
        
        # 入射粒子改变时更新信息
        self.projectile_combo.currentTextChanged.connect(self.update_projectile_info)
        
        # 能量模式切换
        self.single_energy_radio.toggled.connect(self.on_energy_mode_changed)
        
        # 参数改变时发出信号和更新摘要
        self.z_spinbox.valueChanged.connect(self.on_parameter_changed)
        self.a_spinbox.valueChanged.connect(self.on_parameter_changed)
        self.projectile_combo.currentTextChanged.connect(self.on_parameter_changed)
        self.single_energy_spinbox.valueChanged.connect(self.on_parameter_changed)
        
    def set_default_values(self):
        """设置默认值"""
        self.z_spinbox.setValue(1)  # 氢
        self.a_spinbox.setValue(1)
        self.projectile_combo.setCurrentIndex(0)  # 中子
        self.single_energy_spinbox.setValue(1.0)
        self.update_element_info()
        self.update_projectile_info()
        self.update_parameter_summary()
        
    def update_element_info(self):
        """根据原子序数更新元素信息"""
        z = self.z_spinbox.value()
        a = self.a_spinbox.value()
        
        # 简化的元素符号映射
        elements = {
            1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'B', 6: 'C', 7: 'N', 8: 'O',
            9: 'F', 10: 'Ne', 11: 'Na', 12: 'Mg', 13: 'Al', 14: 'Si', 15: 'P',
            16: 'S', 17: 'Cl', 18: 'Ar', 19: 'K', 20: 'Ca', 26: 'Fe', 29: 'Cu',
            47: 'Ag', 79: 'Au', 82: 'Pb', 92: 'U'
        }
        
        symbol = elements.get(z, f'Z{z}')
        self.element_label.setText(symbol)
        self.nuclide_label.setText(f'{a}{symbol}')
        
    def update_projectile_info(self):
        """更新入射粒子信息"""
        projectile_data = self.projectile_combo.currentData()

        info_map = {
            'n': tr('info_neutron'),
            'p': tr('info_proton'),
            'd': tr('info_deuteron'),
            't': tr('info_triton'),
            'h': tr('info_helium3'),
            'a': tr('info_alpha'),
            'g': tr('info_gamma')
        }

        info = info_map.get(projectile_data, tr('info_unknown_particle'))
        self.projectile_info.setText(info)
        
    def on_energy_mode_changed(self):
        """能量模式改变处理"""
        single_mode = self.single_energy_radio.isChecked()
        
        self.single_energy_spinbox.setEnabled(single_mode)
        self.energy_min_spinbox.setEnabled(not single_mode)
        self.energy_max_spinbox.setEnabled(not single_mode)
        
        self.on_parameter_changed()
        
    def on_parameter_changed(self):
        """参数改变处理"""
        self.update_parameter_summary()
        self.emit_parameters_changed()
        
    def update_parameter_summary(self):
        """更新参数摘要"""
        try:
            params = self.get_parameters()
            summary_lines = [
                tr('summary_target', f"目标核: {params['element']}-{params['mass']}"),
                tr('summary_projectile', f"入射粒子: {params['projectile']}"),
                tr('summary_energy', f"入射能量: {params['energy']} MeV")
            ]
            self.summary_label.setText('\n'.join(summary_lines))
        except Exception as e:
            self.summary_label.setText(tr('summary_error', f"参数摘要更新失败: {e}"))

    def on_run_calculation(self):
        """运行计算按钮点击"""
        self.calculation_requested.emit()

    def on_validate_parameters(self):
        """验证参数按钮点击"""
        is_valid, message = self.validate_parameters()
        if is_valid:
            self.show_info_message(tr('validation_title'), tr('validation_success'))
        else:
            self.show_warning_message(tr('validation_title'), tr('validation_failed', f"参数验证失败：{message}"))
            
    def get_parameters(self) -> Dict[str, Any]:
        """获取当前参数"""
        # 获取入射粒子代码
        projectile_code = self.projectile_combo.currentData()
        
        # 获取元素符号
        element = self.element_label.text()
        
        # 获取能量
        energy = self.single_energy_spinbox.value()
        
        parameters = {
            'projectile': projectile_code,
            'element': element,
            'mass': self.a_spinbox.value(),
            'energy': energy,
        }
        
        return parameters
    
    def set_parameters(self, parameters: Dict[str, Any]):
        """设置参数值"""
        if 'projectile' in parameters:
            # 找到对应的projectile选项
            for i in range(self.projectile_combo.count()):
                if self.projectile_combo.itemData(i) == parameters['projectile']:
                    self.projectile_combo.setCurrentIndex(i)
                    break
        
        if 'mass' in parameters:
            self.a_spinbox.setValue(parameters['mass'])
        
        if 'energy' in parameters:
            self.single_energy_spinbox.setValue(float(parameters['energy']))
            
        # 更新显示
        self.update_element_info()
        self.update_projectile_info()
        self.update_parameter_summary()
    
    def get_relevant_parameters(self, global_params: Dict[str, Any]) -> Dict[str, Any]:
        """获取与本标签页相关的参数"""
        relevant_keys = ['projectile', 'element', 'mass', 'energy']
        return {k: v for k, v in global_params.items() if k in relevant_keys}
    
    def validate_parameters(self) -> tuple[bool, str]:
        """验证当前参数"""
        try:
            params = self.get_parameters()
            
            # 检查必需参数
            required = ['projectile', 'element', 'mass', 'energy']
            for param in required:
                if param not in params or params[param] is None:
                    return False, f"缺少必需参数: {param}"
            
            # 检查数值范围
            if params['mass'] < 1 or params['mass'] > 300:
                return False, "质量数必须在1-300之间"
                
            if params['energy'] < 0.001 or params['energy'] > 200.0:
                return False, "入射能量必须在0.001-200.0 MeV之间"
            
            return True, ""
            
        except Exception as e:
            return False, f"验证时发生错误: {str(e)}"
    
    def reset_to_defaults(self):
        """重置到默认值"""
        self.set_default_values()

    def update_language(self):
        """更新界面语言"""
        # 更新标题和描述
        self.title_label.setText(tr('basic_title'))
        self.description_label.setText(tr('basic_description'))

        # 更新按钮文本
        self.run_button.setText(tr('button_run'))
        self.validate_button.setText(tr('button_validate'))

        # 更新工具提示
        self.run_button.setToolTip(tr('tooltip_run_calculation'))
        self.validate_button.setToolTip(tr('tooltip_validate_params'))

        # 更新参数摘要
        self.update_parameter_summary()
