"""
标签页基类
"""

import logging
from typing import Dict, Any
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class BaseParameterTab(QWidget):
    """标签页基类"""
    
    # 信号定义
    parameters_changed = pyqtSignal(dict)  # 参数改变时发出
    calculation_requested = pyqtSignal()   # 请求计算时发出
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.parameters = {}
        self.widgets = {}  # 存储控件引用
        self.init_ui()
        self.connect_signals()
        self.logger.debug(f"{self.__class__.__name__} 初始化完成")
        
    def init_ui(self):
        """初始化用户界面 - 子类必须实现"""
        raise NotImplementedError("子类必须实现 init_ui 方法")
    
    def connect_signals(self):
        """连接信号 - 子类可以重写"""
        pass
    
    def get_parameters(self) -> Dict[str, Any]:
        """获取当前标签页的参数 - 子类必须实现"""
        raise NotImplementedError("子类必须实现 get_parameters 方法")
    
    def set_parameters(self, params: Dict[str, Any]):
        """设置标签页参数 - 子类必须实现"""
        raise NotImplementedError("子类必须实现 set_parameters 方法")
    
    def update_from_global_parameters(self, global_params: Dict[str, Any]):
        """从全局参数更新本标签页 - 子类可以重写"""
        # 默认实现：只更新与本标签页相关的参数
        relevant_params = self.get_relevant_parameters(global_params)
        if relevant_params:
            self.set_parameters(relevant_params)
    
    def get_relevant_parameters(self, global_params: Dict[str, Any]) -> Dict[str, Any]:
        """获取与本标签页相关的参数 - 子类可以重写"""
        # 默认实现：返回所有参数
        return global_params
    
    def validate_parameters(self) -> tuple[bool, str]:
        """验证当前参数 - 子类可以重写"""
        # 默认实现：总是返回有效
        return True, ""
    
    def reset_to_defaults(self):
        """重置到默认值 - 子类可以重写"""
        pass
    
    def emit_parameters_changed(self):
        """发出参数改变信号"""
        try:
            params = self.get_parameters()
            self.parameters.update(params)
            self.parameters_changed.emit(params)
            self.logger.debug(f"发出参数变化信号: {params}")
        except Exception as e:
            self.logger.error(f"获取参数时发生错误: {e}")
    
    def create_group_box(self, title: str, layout_type=QVBoxLayout) -> tuple[QGroupBox, QLayout]:
        """创建标准样式的分组框，返回分组框和布局"""
        group = QGroupBox(title)
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px 0 8px;
                color: #495057;
                background-color: #ffffff;
            }
        """)

        layout = layout_type()
        layout.setSpacing(8)
        layout.setContentsMargins(12, 16, 12, 12)
        group.setLayout(layout)

        return group, layout
    
    def create_form_layout(self) -> QFormLayout:
        """创建标准的表单布局"""
        layout = QFormLayout()
        layout.setSpacing(8)
        layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        layout.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        return layout
    
    def create_spin_box(self, min_val: int, max_val: int, default_val: int, 
                       tooltip: str = "") -> QSpinBox:
        """创建标准的整数输入框"""
        spinbox = QSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(default_val)
        if tooltip:
            spinbox.setToolTip(tooltip)
        spinbox.setStyleSheet("""
            QSpinBox {
                padding: 4px 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QSpinBox:focus {
                border-color: #80bdff;
                border-width: 2px;
            }
        """)
        return spinbox
    
    def create_double_spin_box(self, min_val: float, max_val: float, 
                              default_val: float, decimals: int = 3,
                              tooltip: str = "") -> QDoubleSpinBox:
        """创建标准的浮点数输入框"""
        spinbox = QDoubleSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(default_val)
        spinbox.setDecimals(decimals)
        if tooltip:
            spinbox.setToolTip(tooltip)
        spinbox.setStyleSheet("""
            QDoubleSpinBox {
                padding: 4px 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QDoubleSpinBox:focus {
                border-color: #80bdff;
                border-width: 2px;
            }
        """)
        return spinbox
    
    def create_combo_box(self, items: list, tooltip: str = "") -> QComboBox:
        """创建标准的下拉框"""
        combo = QComboBox()
        for item in items:
            if isinstance(item, tuple):
                combo.addItem(item[0], item[1])  # (显示文本, 数据)
            else:
                combo.addItem(str(item))
        if tooltip:
            combo.setToolTip(tooltip)
        combo.setStyleSheet("""
            QComboBox {
                padding: 4px 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                background-color: #ffffff;
                min-width: 120px;
            }
            QComboBox:focus {
                border-color: #80bdff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #6c757d;
                margin-right: 5px;
            }
        """)
        return combo
    
    def create_check_box(self, text: str, checked: bool = False, 
                        tooltip: str = "") -> QCheckBox:
        """创建标准的复选框"""
        checkbox = QCheckBox(text)
        checkbox.setChecked(checked)
        if tooltip:
            checkbox.setToolTip(tooltip)
        checkbox.setStyleSheet("""
            QCheckBox {
                spacing: 8px;
                color: #495057;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #ced4da;
                border-radius: 3px;
                background-color: #ffffff;
            }
            QCheckBox::indicator:checked {
                background-color: #007bff;
                border-color: #007bff;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEwIDNMNC41IDguNUwyIDYiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
            }
            QCheckBox::indicator:hover {
                border-color: #80bdff;
            }
        """)
        return checkbox
    
    def create_radio_button(self, text: str, checked: bool = False,
                           tooltip: str = "") -> QRadioButton:
        """创建标准的单选按钮"""
        radio = QRadioButton(text)
        radio.setChecked(checked)
        if tooltip:
            radio.setToolTip(tooltip)
        radio.setStyleSheet("""
            QRadioButton {
                spacing: 8px;
                color: #495057;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #ced4da;
                border-radius: 8px;
                background-color: #ffffff;
            }
            QRadioButton::indicator:checked {
                background-color: #007bff;
                border-color: #007bff;
            }
            QRadioButton::indicator:checked::after {
                content: '';
                width: 6px;
                height: 6px;
                border-radius: 3px;
                background-color: #ffffff;
                margin: 4px;
            }
            QRadioButton::indicator:hover {
                border-color: #80bdff;
            }
        """)
        return radio
    
    def create_line_edit(self, placeholder: str = "", tooltip: str = "") -> QLineEdit:
        """创建标准的文本输入框"""
        line_edit = QLineEdit()
        if placeholder:
            line_edit.setPlaceholderText(placeholder)
        if tooltip:
            line_edit.setToolTip(tooltip)
        line_edit.setStyleSheet("""
            QLineEdit {
                padding: 6px 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border-color: #80bdff;
                border-width: 2px;
            }
        """)
        return line_edit
    
    def create_push_button(self, text: str, primary: bool = False,
                          tooltip: str = "") -> QPushButton:
        """创建标准的按钮"""
        button = QPushButton(text)
        if tooltip:
            button.setToolTip(tooltip)
        
        if primary:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #007bff;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: 500;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
                QPushButton:pressed {
                    background-color: #004085;
                }
                QPushButton:disabled {
                    background-color: #6c757d;
                }
            """)
        else:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #f8f9fa;
                    color: #495057;
                    border: 1px solid #ced4da;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: 500;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #e9ecef;
                    border-color: #adb5bd;
                }
                QPushButton:pressed {
                    background-color: #dee2e6;
                }
                QPushButton:disabled {
                    background-color: #e9ecef;
                    color: #6c757d;
                }
            """)
        
        return button
    
    def show_info_message(self, title: str, message: str):
        """显示信息消息"""
        QMessageBox.information(self, title, message)
    
    def show_warning_message(self, title: str, message: str):
        """显示警告消息"""
        QMessageBox.warning(self, title, message)
    
    def show_error_message(self, title: str, message: str):
        """显示错误消息"""
        QMessageBox.critical(self, title, message)

    def update_language(self):
        """更新界面语言 - 子类可以重写"""
        pass
