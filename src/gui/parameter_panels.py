"""
参数设置面板组件
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils.logger import LoggerMixin

class BasicParameterPanel(QWidget, LoggerMixin):
    """基础参数设置面板"""
    
    # 定义信号
    parameters_changed = pyqtSignal(dict)  # 参数改变时发出
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.connect_signals()
        
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 标题
        title = QLabel("基础参数设置")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)
        
        # 目标核参数组
        target_group = self.create_target_group()
        layout.addWidget(target_group)
        
        # 入射粒子参数组
        projectile_group = self.create_projectile_group()
        layout.addWidget(projectile_group)
        
        # 能量参数组
        energy_group = self.create_energy_group()
        layout.addWidget(energy_group)
        
        # 输出选项组
        output_group = self.create_output_group()
        layout.addWidget(output_group)
        
        # 弹性空间
        layout.addStretch()
        
        # 设置默认值
        self.set_default_values()
        
    def create_target_group(self) -> QGroupBox:
        """创建目标核参数组"""
        group = QGroupBox("目标核")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QFormLayout(group)
        layout.setSpacing(10)
        
        # 原子序数
        self.z_spinbox = QSpinBox()
        self.z_spinbox.setRange(1, 118)
        self.z_spinbox.setValue(1)
        self.z_spinbox.setToolTip("目标核的原子序数 (1-118)")
        layout.addRow("原子序数 (Z):", self.z_spinbox)
        
        # 质量数
        self.a_spinbox = QSpinBox()
        self.a_spinbox.setRange(1, 300)
        self.a_spinbox.setValue(1)
        self.a_spinbox.setToolTip("目标核的质量数 (1-300)")
        layout.addRow("质量数 (A):", self.a_spinbox)
        
        # 元素符号（自动更新）
        self.element_label = QLabel("H")
        self.element_label.setStyleSheet("font-weight: bold; color: #27ae60;")
        layout.addRow("元素符号:", self.element_label)
        
        return group
    
    def create_projectile_group(self) -> QGroupBox:
        """创建入射粒子参数组"""
        group = QGroupBox("入射粒子")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QFormLayout(group)
        
        # 粒子类型
        self.projectile_combo = QComboBox()
        projectiles = [
            ('n', '中子'),
            ('p', '质子'),
            ('d', '氘核'),
            ('t', '氚核'),
            ('h', '氦-3'),
            ('a', 'α粒子'),
            ('g', '伽马射线')
        ]
        
        for code, name in projectiles:
            self.projectile_combo.addItem(f"{name} ({code})", code)
        
        self.projectile_combo.setToolTip("选择入射粒子类型")
        layout.addRow("粒子类型:", self.projectile_combo)
        
        return group
    
    def create_energy_group(self) -> QGroupBox:
        """创建能量参数组"""
        group = QGroupBox("入射能量")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout(group)
        
        # 能量模式选择
        mode_layout = QHBoxLayout()
        self.single_energy_radio = QRadioButton("单一能量")
        self.energy_range_radio = QRadioButton("能量范围")
        self.single_energy_radio.setChecked(True)
        
        mode_layout.addWidget(self.single_energy_radio)
        mode_layout.addWidget(self.energy_range_radio)
        layout.addLayout(mode_layout)
        
        # 单一能量输入
        single_layout = QHBoxLayout()
        self.single_energy_spinbox = QDoubleSpinBox()
        self.single_energy_spinbox.setRange(0.001, 200.0)
        self.single_energy_spinbox.setValue(1.0)
        self.single_energy_spinbox.setSuffix(" MeV")
        self.single_energy_spinbox.setDecimals(3)
        single_layout.addWidget(QLabel("能量:"))
        single_layout.addWidget(self.single_energy_spinbox)
        layout.addLayout(single_layout)
        
        # 能量范围输入
        range_layout = QHBoxLayout()
        self.energy_min_spinbox = QDoubleSpinBox()
        self.energy_min_spinbox.setRange(0.001, 200.0)
        self.energy_min_spinbox.setValue(1.0)
        self.energy_min_spinbox.setSuffix(" MeV")
        self.energy_min_spinbox.setDecimals(3)
        self.energy_min_spinbox.setEnabled(False)
        
        self.energy_max_spinbox = QDoubleSpinBox()
        self.energy_max_spinbox.setRange(0.001, 200.0)
        self.energy_max_spinbox.setValue(20.0)
        self.energy_max_spinbox.setSuffix(" MeV")
        self.energy_max_spinbox.setDecimals(3)
        self.energy_max_spinbox.setEnabled(False)
        
        range_layout.addWidget(QLabel("最小:"))
        range_layout.addWidget(self.energy_min_spinbox)
        range_layout.addWidget(QLabel("最大:"))
        range_layout.addWidget(self.energy_max_spinbox)
        layout.addLayout(range_layout)
        
        return group
    
    def create_output_group(self) -> QGroupBox:
        """创建输出选项组"""
        group = QGroupBox("输出选项")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout(group)
        
        # 输出选项复选框
        self.channels_checkbox = QCheckBox("反应道信息 (channels)")
        self.channels_checkbox.setChecked(True)
        self.channels_checkbox.setToolTip("输出反应道信息")
        
        self.spectra_checkbox = QCheckBox("能谱输出 (outspectra)")
        self.spectra_checkbox.setToolTip("输出粒子发射能谱")
        
        self.angular_checkbox = QCheckBox("角分布输出 (outangle)")
        self.angular_checkbox.setToolTip("输出角分布信息")
        
        self.levels_checkbox = QCheckBox("能级信息 (outlevels)")
        self.levels_checkbox.setToolTip("输出能级信息")
        
        layout.addWidget(self.channels_checkbox)
        layout.addWidget(self.spectra_checkbox)
        layout.addWidget(self.angular_checkbox)
        layout.addWidget(self.levels_checkbox)
        
        return group
    
    def connect_signals(self):
        """连接信号"""
        # 原子序数改变时更新元素符号
        self.z_spinbox.valueChanged.connect(self.update_element_symbol)
        
        # 能量模式切换
        self.single_energy_radio.toggled.connect(self.on_energy_mode_changed)
        self.energy_range_radio.toggled.connect(self.on_energy_mode_changed)
        
        # 参数改变时发出信号
        self.z_spinbox.valueChanged.connect(self.emit_parameters_changed)
        self.a_spinbox.valueChanged.connect(self.emit_parameters_changed)
        self.projectile_combo.currentTextChanged.connect(self.emit_parameters_changed)
        self.single_energy_spinbox.valueChanged.connect(self.emit_parameters_changed)
        self.energy_min_spinbox.valueChanged.connect(self.emit_parameters_changed)
        self.energy_max_spinbox.valueChanged.connect(self.emit_parameters_changed)
        
        # 复选框改变
        self.channels_checkbox.toggled.connect(self.emit_parameters_changed)
        self.spectra_checkbox.toggled.connect(self.emit_parameters_changed)
        self.angular_checkbox.toggled.connect(self.emit_parameters_changed)
        self.levels_checkbox.toggled.connect(self.emit_parameters_changed)
    
    def set_default_values(self):
        """设置默认值"""
        self.z_spinbox.setValue(1)  # 氢
        self.a_spinbox.setValue(1)
        self.projectile_combo.setCurrentIndex(0)  # 中子
        self.single_energy_spinbox.setValue(1.0)
        self.update_element_symbol()
    
    def update_element_symbol(self):
        """根据原子序数更新元素符号"""
        z = self.z_spinbox.value()
        
        # 简化的元素符号映射
        elements = {
            1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'B', 6: 'C', 7: 'N', 8: 'O',
            9: 'F', 10: 'Ne', 11: 'Na', 12: 'Mg', 13: 'Al', 14: 'Si', 15: 'P',
            16: 'S', 17: 'Cl', 18: 'Ar', 19: 'K', 20: 'Ca', 26: 'Fe', 29: 'Cu',
            47: 'Ag', 79: 'Au', 82: 'Pb', 92: 'U'
        }
        
        symbol = elements.get(z, f'Z{z}')
        self.element_label.setText(symbol)
    
    def on_energy_mode_changed(self):
        """能量模式改变处理"""
        single_mode = self.single_energy_radio.isChecked()
        
        self.single_energy_spinbox.setEnabled(single_mode)
        self.energy_min_spinbox.setEnabled(not single_mode)
        self.energy_max_spinbox.setEnabled(not single_mode)
        
        self.emit_parameters_changed()
    
    def emit_parameters_changed(self):
        """发出参数改变信号"""
        parameters = self.get_parameters()
        self.parameters_changed.emit(parameters)
    
    def get_parameters(self) -> dict:
        """获取当前参数"""
        # 获取入射粒子代码
        projectile_code = self.projectile_combo.currentData()
        
        # 获取元素符号
        element = self.element_label.text()
        
        # 获取能量
        if self.single_energy_radio.isChecked():
            energy = str(self.single_energy_spinbox.value())
        else:
            energy = f"{self.energy_min_spinbox.value()} {self.energy_max_spinbox.value()}"
        
        parameters = {
            'projectile': projectile_code,
            'element': element,
            'mass': self.a_spinbox.value(),
            'energy': energy,
            'channels': self.channels_checkbox.isChecked(),
            'outspectra': self.spectra_checkbox.isChecked(),
            'outangle': self.angular_checkbox.isChecked(),
            'outlevels': self.levels_checkbox.isChecked(),
        }
        
        return parameters
    
    def set_parameters(self, parameters: dict):
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
            energy_str = str(parameters['energy'])
            if ' ' in energy_str:
                # 能量范围
                parts = energy_str.split()
                if len(parts) >= 2:
                    self.energy_range_radio.setChecked(True)
                    self.energy_min_spinbox.setValue(float(parts[0]))
                    self.energy_max_spinbox.setValue(float(parts[1]))
            else:
                # 单一能量
                self.single_energy_radio.setChecked(True)
                self.single_energy_spinbox.setValue(float(energy_str))
        
        # 设置输出选项
        self.channels_checkbox.setChecked(parameters.get('channels', False))
        self.spectra_checkbox.setChecked(parameters.get('outspectra', False))
        self.angular_checkbox.setChecked(parameters.get('outangle', False))
        self.levels_checkbox.setChecked(parameters.get('outlevels', False))
