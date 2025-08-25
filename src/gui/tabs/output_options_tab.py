"""
输出选项标签页
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

class OutputOptionsTab(BaseParameterTab):
    """输出选项标签页"""
    
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
        title = QLabel("输出选项设置")
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
        description = QLabel("控制TALYS计算的输出文件和数据格式。选择需要的输出类型以获得相应的计算结果。")
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
        self.create_basic_output_group(scroll_layout)
        self.create_detailed_output_group(scroll_layout)
        self.create_special_output_group(scroll_layout)
        
        # 弹性空间
        scroll_layout.addStretch()
        
        # 设置滚动内容
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        
        # 设置默认值
        self.set_default_values()
        
    def create_basic_output_group(self, parent_layout):
        """创建基础输出选项组"""
        group, _ = self.create_group_box("基础输出选项")
        layout = QVBoxLayout()
        
        # 主要输出
        self.flagmain_checkbox = self.create_check_box(
            "主要输出 (flagmain)", True, 
            "输出主要的计算结果，包括截面和反应道信息"
        )
        layout.addWidget(self.flagmain_checkbox)
        self.widgets['flagmain'] = self.flagmain_checkbox
        
        # 基础信息
        self.flagbasic_checkbox = self.create_check_box(
            "基础信息 (flagbasic)", True,
            "输出基础的核结构和模型信息"
        )
        layout.addWidget(self.flagbasic_checkbox)
        self.widgets['flagbasic'] = self.flagbasic_checkbox
        
        # 反应道信息
        self.channels_checkbox = self.create_check_box(
            "反应道信息 (channels)", True,
            "输出详细的反应道信息到channels.out文件"
        )
        layout.addWidget(self.channels_checkbox)
        self.widgets['channels'] = self.channels_checkbox
        
        # 布居信息
        self.flagpop_checkbox = self.create_check_box(
            "布居信息 (flagpop)", False,
            "输出能级布居信息"
        )
        layout.addWidget(self.flagpop_checkbox)
        self.widgets['flagpop'] = self.flagpop_checkbox
        parent_layout.addWidget(group)
        
    def create_detailed_output_group(self, parent_layout):
        """创建详细输出选项组"""
        group, _ = self.create_group_box("详细输出选项")
        layout = QVBoxLayout()
        
        # 能谱输出
        self.outspectra_checkbox = self.create_check_box(
            "粒子发射能谱 (outspectra)", False,
            "输出粒子发射能谱到*.spe文件"
        )
        layout.addWidget(self.outspectra_checkbox)
        self.widgets['outspectra'] = self.outspectra_checkbox
        
        # 角分布输出
        self.outangle_checkbox = self.create_check_box(
            "角分布信息 (outangle)", False,
            "输出角分布信息到*.ang文件"
        )
        layout.addWidget(self.outangle_checkbox)
        self.widgets['outangle'] = self.outangle_checkbox
        
        # 双微分截面
        self.flagddx_checkbox = self.create_check_box(
            "双微分截面 (flagddx)", False,
            "输出双微分截面数据"
        )
        layout.addWidget(self.flagddx_checkbox)
        self.widgets['flagddx'] = self.flagddx_checkbox
        
        # 离散能级
        self.outlevels_checkbox = self.create_check_box(
            "离散能级信息 (outlevels)", False,
            "输出离散能级的详细信息"
        )
        layout.addWidget(self.outlevels_checkbox)
        self.widgets['outlevels'] = self.outlevels_checkbox
        
        # 伽马级联
        self.flaggamma_checkbox = self.create_check_box(
            "伽马级联 (flaggamma)", False,
            "输出伽马级联信息"
        )
        layout.addWidget(self.flaggamma_checkbox)
        self.widgets['flaggamma'] = self.flaggamma_checkbox
        parent_layout.addWidget(group)
        
    def create_special_output_group(self, parent_layout):
        """创建特殊输出选项组"""
        group, _ = self.create_group_box("特殊输出选项")
        layout = QVBoxLayout()
        
        # 反冲信息
        self.flagrecoil_checkbox = self.create_check_box(
            "反冲信息 (flagrecoil)", False,
            "输出反冲核的信息"
        )
        layout.addWidget(self.flagrecoil_checkbox)
        self.widgets['flagrecoil'] = self.flagrecoil_checkbox
        
        # 裂变信息
        self.flagfission_checkbox = self.create_check_box(
            "裂变信息 (flagfission)", False,
            "输出裂变相关信息（如果适用）"
        )
        layout.addWidget(self.flagfission_checkbox)
        self.widgets['flagfission'] = self.flagfission_checkbox
        
        # 数值检查
        self.flagcheck_checkbox = self.create_check_box(
            "数值检查 (flagcheck)", False,
            "输出数值检查和调试信息"
        )
        layout.addWidget(self.flagcheck_checkbox)
        self.widgets['flagcheck'] = self.flagcheck_checkbox
        
        # 天体物理学
        self.flagastro_checkbox = self.create_check_box(
            "天体物理学 (flagastro)", False,
            "输出天体物理学相关的反应率"
        )
        layout.addWidget(self.flagastro_checkbox)
        self.widgets['flagastro'] = self.flagastro_checkbox
        
        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)
        
        # 输出文件预览
        preview_label = QLabel("预期输出文件:")
        preview_label.setStyleSheet("font-weight: bold; margin-top: 8px;")
        layout.addWidget(preview_label)
        
        self.file_preview = QLabel()
        self.file_preview.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 8px;
                color: #495057;
                font-family: 'Courier New', monospace;
                font-size: 10px;
            }
        """)
        self.file_preview.setWordWrap(True)
        layout.addWidget(self.file_preview)
        parent_layout.addWidget(group)
        
    def connect_signals(self):
        """连接信号"""
        # 所有复选框的变化都触发参数更新和文件预览更新
        for widget in self.widgets.values():
            if isinstance(widget, QCheckBox):
                widget.toggled.connect(self.on_parameter_changed)
                
    def on_parameter_changed(self):
        """参数改变处理"""
        self.update_file_preview()
        self.emit_parameters_changed()
        
    def update_file_preview(self):
        """更新输出文件预览"""
        files = []
        
        # 基础文件（总是生成）
        files.append("total.tot - 总截面")
        files.append("elastic.tot - 弹性散射截面")
        files.append("nonelastic.tot - 非弹性截面")
        
        # 根据选项添加文件
        if self.channels_checkbox.isChecked():
            files.append("channels.out - 反应道信息")
            
        if self.outspectra_checkbox.isChecked():
            files.append("*.spe - 粒子发射能谱")
            
        if self.outangle_checkbox.isChecked():
            files.append("*.ang - 角分布数据")
            
        if self.outlevels_checkbox.isChecked():
            files.append("levels.out - 能级信息")
            
        if self.flagddx_checkbox.isChecked():
            files.append("*.ddx - 双微分截面")
            
        if self.flaggamma_checkbox.isChecked():
            files.append("gamma.out - 伽马级联")
            
        if self.flagrecoil_checkbox.isChecked():
            files.append("recoil.out - 反冲信息")
            
        if self.flagfission_checkbox.isChecked():
            files.append("fission.out - 裂变信息")
            
        if self.flagastro_checkbox.isChecked():
            files.append("astro.out - 天体物理学反应率")
            
        if self.flagcheck_checkbox.isChecked():
            files.append("check.out - 数值检查信息")
        
        preview_text = '\n'.join(files)
        self.file_preview.setText(preview_text)
        
    def set_default_values(self):
        """设置默认值"""
        # 根据TALYS默认值设置
        self.flagmain_checkbox.setChecked(True)
        self.flagbasic_checkbox.setChecked(True)
        self.channels_checkbox.setChecked(True)
        self.flagpop_checkbox.setChecked(False)
        
        self.outspectra_checkbox.setChecked(False)
        self.outangle_checkbox.setChecked(False)
        self.flagddx_checkbox.setChecked(False)
        self.outlevels_checkbox.setChecked(False)
        self.flaggamma_checkbox.setChecked(False)
        
        self.flagrecoil_checkbox.setChecked(False)
        self.flagfission_checkbox.setChecked(False)
        self.flagcheck_checkbox.setChecked(False)
        self.flagastro_checkbox.setChecked(False)
        
        self.update_file_preview()
        
    def get_parameters(self) -> Dict[str, Any]:
        """获取当前参数"""
        parameters = {
            'flagmain': self.flagmain_checkbox.isChecked(),
            'flagbasic': self.flagbasic_checkbox.isChecked(),
            'channels': self.channels_checkbox.isChecked(),
            'flagpop': self.flagpop_checkbox.isChecked(),
            'outspectra': self.outspectra_checkbox.isChecked(),
            'outangle': self.outangle_checkbox.isChecked(),
            'flagddx': self.flagddx_checkbox.isChecked(),
            'outlevels': self.outlevels_checkbox.isChecked(),
            'flaggamma': self.flaggamma_checkbox.isChecked(),
            'flagrecoil': self.flagrecoil_checkbox.isChecked(),
            'flagfission': self.flagfission_checkbox.isChecked(),
            'flagcheck': self.flagcheck_checkbox.isChecked(),
            'flagastro': self.flagastro_checkbox.isChecked(),
        }
        
        return parameters
    
    def set_parameters(self, parameters: Dict[str, Any]):
        """设置参数值"""
        for param_name, value in parameters.items():
            if param_name in self.widgets:
                widget = self.widgets[param_name]
                if isinstance(widget, QCheckBox):
                    widget.setChecked(bool(value))
        
        self.update_file_preview()
    
    def get_relevant_parameters(self, global_params: Dict[str, Any]) -> Dict[str, Any]:
        """获取与本标签页相关的参数"""
        relevant_keys = [
            'flagmain', 'flagbasic', 'channels', 'flagpop',
            'outspectra', 'outangle', 'flagddx', 'outlevels', 'flaggamma',
            'flagrecoil', 'flagfission', 'flagcheck', 'flagastro'
        ]
        return {k: v for k, v in global_params.items() if k in relevant_keys}
    
    def validate_parameters(self) -> tuple[bool, str]:
        """验证当前参数"""
        # 输出选项通常不需要特殊验证，都是布尔值
        return True, ""
    
    def reset_to_defaults(self):
        """重置到默认值"""
        self.set_default_values()
