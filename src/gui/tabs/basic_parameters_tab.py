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
from core.talys_interface import TalysInterface, TalysCalculationError, TalysInterfaceError

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
        group, group_layout = self.create_group_box(tr('group_target'))

        # 创建表单布局
        form_layout = self.create_form_layout()

        # 原子序数
        self.z_spinbox = self.create_spin_box(1, 118, 1, tr('tooltip_atomic_number'))
        self.z_label = QLabel(tr('label_atomic_number'))
        form_layout.addRow(self.z_label, self.z_spinbox)
        self.widgets['z'] = self.z_spinbox

        # 质量数
        self.a_spinbox = self.create_spin_box(1, 300, 1, tr('tooltip_mass_number'))
        self.a_label = QLabel(tr('label_mass_number'))
        form_layout.addRow(self.a_label, self.a_spinbox)
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
        form_layout.addRow(self.element_row_label, self.element_label)

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
        form_layout.addRow(self.nuclide_row_label, self.nuclide_label)

        # 将表单布局添加到组布局中
        group_layout.addLayout(form_layout)
        parent_layout.addWidget(group)

    def create_projectile_group(self, parent_layout):
        """创建入射粒子参数组"""
        group, group_layout = self.create_group_box(tr('group_projectile'))

        # 创建表单布局
        form_layout = self.create_form_layout()

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
        form_layout.addRow(self.projectile_label, self.projectile_combo)
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
        form_layout.addRow("", self.projectile_info)

        # 将表单布局添加到组布局中
        group_layout.addLayout(form_layout)
        parent_layout.addWidget(group)

    def create_energy_group(self, parent_layout):
        """创建能量参数组"""
        group, group_layout = self.create_group_box(tr('group_energy'))


        # 能量模式选择
        mode_layout = QHBoxLayout()
        self.single_energy_radio = self.create_radio_button(tr('radio_single_energy'), True, tr('tooltip_single_energy'))
        self.energy_range_radio = self.create_radio_button(tr('radio_energy_range'), False, tr('tooltip_energy_range'))
        # 启用能量范围功能
        self.energy_range_radio.setEnabled(True)

        mode_layout.addWidget(self.single_energy_radio)
        mode_layout.addWidget(self.energy_range_radio)
        mode_layout.addStretch()
        group_layout.addLayout(mode_layout)

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
        group_layout.addLayout(single_layout)
        
        # 能量范围输入
        self.range_widget = QWidget()
        range_layout = QHBoxLayout(self.range_widget)
        self.energy_min_label = QLabel(tr('label_min'))
        range_layout.addWidget(self.energy_min_label)

        self.energy_min_spinbox = self.create_double_spin_box(
            0.001, 200.0, 1.0, 3, tr('tooltip_min_energy')
        )
        self.energy_min_spinbox.setSuffix(" MeV")
        range_layout.addWidget(self.energy_min_spinbox)

        self.energy_max_label = QLabel(tr('label_max'))
        range_layout.addWidget(self.energy_max_label)

        self.energy_max_spinbox = self.create_double_spin_box(
            0.001, 200.0, 20.0, 3, tr('tooltip_max_energy')
        )
        self.energy_max_spinbox.setSuffix(" MeV")
        range_layout.addWidget(self.energy_max_spinbox)

        # 能量步长
        self.energy_step_label = QLabel(tr('label_step', "步长:"))
        range_layout.addWidget(self.energy_step_label)

        self.energy_step_spinbox = self.create_double_spin_box(
            0.001, 10.0, 1.0, 3, tr('tooltip_energy_step', "能量步长 (MeV)")
        )
        self.energy_step_spinbox.setSuffix(" MeV")
        range_layout.addWidget(self.energy_step_spinbox)

        range_layout.addStretch()
        group_layout.addWidget(self.range_widget)

        # 默认隐藏能量范围输入
        self.range_widget.setVisible(False)

        parent_layout.addWidget(group)

    def create_calculation_group(self, parent_layout):
        """创建参数摘要组"""
        group, group_layout = self.create_group_box(tr('label_parameter_summary'))

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
        group_layout.addWidget(self.summary_label)

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
        self.energy_min_spinbox.valueChanged.connect(self.on_parameter_changed)
        self.energy_max_spinbox.valueChanged.connect(self.on_parameter_changed)
        self.energy_step_spinbox.valueChanged.connect(self.on_parameter_changed)
        
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

        # 完整的元素符号映射表（前118个元素）
        elements = {
            1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'B', 6: 'C', 7: 'N', 8: 'O',
            9: 'F', 10: 'Ne', 11: 'Na', 12: 'Mg', 13: 'Al', 14: 'Si', 15: 'P',
            16: 'S', 17: 'Cl', 18: 'Ar', 19: 'K', 20: 'Ca', 21: 'Sc', 22: 'Ti',
            23: 'V', 24: 'Cr', 25: 'Mn', 26: 'Fe', 27: 'Co', 28: 'Ni', 29: 'Cu',
            30: 'Zn', 31: 'Ga', 32: 'Ge', 33: 'As', 34: 'Se', 35: 'Br', 36: 'Kr',
            37: 'Rb', 38: 'Sr', 39: 'Y', 40: 'Zr', 41: 'Nb', 42: 'Mo', 43: 'Tc',
            44: 'Ru', 45: 'Rh', 46: 'Pd', 47: 'Ag', 48: 'Cd', 49: 'In', 50: 'Sn',
            51: 'Sb', 52: 'Te', 53: 'I', 54: 'Xe', 55: 'Cs', 56: 'Ba', 57: 'La',
            58: 'Ce', 59: 'Pr', 60: 'Nd', 61: 'Pm', 62: 'Sm', 63: 'Eu', 64: 'Gd',
            65: 'Tb', 66: 'Dy', 67: 'Ho', 68: 'Er', 69: 'Tm', 70: 'Yb', 71: 'Lu',
            72: 'Hf', 73: 'Ta', 74: 'W', 75: 'Re', 76: 'Os', 77: 'Ir', 78: 'Pt',
            79: 'Au', 80: 'Hg', 81: 'Tl', 82: 'Pb', 83: 'Bi', 84: 'Po', 85: 'At',
            86: 'Rn', 87: 'Fr', 88: 'Ra', 89: 'Ac', 90: 'Th', 91: 'Pa', 92: 'U',
            93: 'Np', 94: 'Pu', 95: 'Am', 96: 'Cm', 97: 'Bk', 98: 'Cf', 99: 'Es',
            100: 'Fm', 101: 'Md', 102: 'No', 103: 'Lr', 104: 'Rf', 105: 'Db',
            106: 'Sg', 107: 'Bh', 108: 'Hs', 109: 'Mt', 110: 'Ds', 111: 'Rg',
            112: 'Cn', 113: 'Nh', 114: 'Fl', 115: 'Mc', 116: 'Lv', 117: 'Ts',
            118: 'Og'
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

        # 显示/隐藏相应的输入控件
        if single_mode:
            # 单一能量模式
            self.single_energy_spinbox.setEnabled(True)
            self.range_widget.setVisible(False)
        else:
            # 能量范围模式
            self.single_energy_spinbox.setEnabled(False)
            self.range_widget.setVisible(True)
            self.energy_min_spinbox.setEnabled(True)
            self.energy_max_spinbox.setEnabled(True)
            self.energy_step_spinbox.setEnabled(True)

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
                f"目标核: {params['element']}-{params['mass']}",
                f"入射粒子: {params['projectile']}",
            ]

            # 根据能量模式显示不同的能量信息
            if 'energy' in params:
                # 单一能量模式
                summary_lines.append(f"入射能量: {params['energy']} MeV")
            elif 'energy_mode' in params and params['energy_mode'] == 'range':
                # 能量范围模式
                energy_info = f"能量范围: {params['energy_min']}-{params['energy_max']} MeV (步长: {params['energy_step']} MeV)"
                summary_lines.append(energy_info)

            self.summary_label.setText('\n'.join(summary_lines))
        except Exception as e:
            self.summary_label.setText(f"参数摘要更新失败: {e}")


            
    def get_parameters(self) -> Dict[str, Any]:
        """获取当前参数"""
        # 获取入射粒子代码
        projectile_code = self.projectile_combo.currentData()

        # 获取元素符号
        element = self.element_label.text()

        # 基础参数
        parameters = {
            'projectile': projectile_code,
            'element': element,
            'mass': self.a_spinbox.value(),
        }

        # 根据能量模式获取能量参数
        if self.single_energy_radio.isChecked():
            # 单一能量模式
            parameters['energy'] = self.single_energy_spinbox.value()
        else:
            # 能量范围模式
            parameters['energy_min'] = self.energy_min_spinbox.value()
            parameters['energy_max'] = self.energy_max_spinbox.value()
            parameters['energy_step'] = self.energy_step_spinbox.value()
            parameters['energy_mode'] = 'range'

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

        # 更新参数摘要
        self.update_parameter_summary()
