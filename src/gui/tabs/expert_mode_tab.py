"""
专家模式标签页
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

class ExpertModeTab(BaseParameterTab):
    """专家模式标签页"""

    def __init__(self):
        super().__init__()

    def init_ui(self):
        """初始化用户界面"""
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 标题
        title = QLabel(tr('expert_mode_title'))
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #212529;
                margin-bottom: 8px;
            }
        """)
        main_layout.addWidget(title)

        # 警告信息
        warning = QLabel(tr('expert_mode_warning'))
        warning.setStyleSheet("""
            QLabel {
                color: #856404;
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 4px;
                padding: 8px;
                font-size: 12px;
                margin-bottom: 16px;
            }
        """)
        warning.setWordWrap(True)
        main_layout.addWidget(warning)
        
        # 创建标签页
        self.expert_tabs = QTabWidget()
        
        # 输入文件编辑器
        self.input_editor_tab = self.create_input_editor_tab()
        self.expert_tabs.addTab(self.input_editor_tab, "📝 输入文件编辑")
        
        # 高级选项
        self.advanced_options_tab = self.create_advanced_options_tab()
        self.expert_tabs.addTab(self.advanced_options_tab, "⚙️ 高级选项")
        
        # 调试信息
        self.debug_tab = self.create_debug_tab()
        self.expert_tabs.addTab(self.debug_tab, "🐛 调试信息")
        
        main_layout.addWidget(self.expert_tabs)
        
    def create_input_editor_tab(self) -> QWidget:
        """创建输入文件编辑器标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 工具栏
        toolbar = QHBoxLayout()
        
        self.load_button = self.create_push_button("加载文件", False, "从文件加载TALYS输入")
        self.save_button = self.create_push_button("保存文件", False, "保存TALYS输入到文件")
        self.generate_button = self.create_push_button("生成输入", True, "根据当前参数生成TALYS输入")
        self.validate_input_button = self.create_push_button("验证输入", False, "验证TALYS输入语法")
        
        toolbar.addWidget(self.load_button)
        toolbar.addWidget(self.save_button)
        toolbar.addWidget(self.generate_button)
        toolbar.addWidget(self.validate_input_button)
        toolbar.addStretch()
        
        layout.addLayout(toolbar)
        
        # 输入文件编辑器
        self.input_editor = QTextEdit()
        self.input_editor.setFont(QFont("Courier New", 11))
        self.input_editor.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 8px;
                line-height: 1.4;
            }
        """)
        
        # 设置默认内容
        self.input_editor.setPlainText("""# TALYS输入文件
# 由TALYS Visualizer生成

# 必需参数
projectile n
element H
mass 1
energy 1.0

# 输出选项
channels y
flagmain y
flagbasic y

# 在此添加更多TALYS参数...
""")
        
        layout.addWidget(self.input_editor)
        
        # 状态信息
        self.input_status = QLabel("就绪")
        self.input_status.setStyleSheet("""
            QLabel {
                color: #495057;
                font-size: 11px;
                padding: 4px;
                background-color: #e9ecef;
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.input_status)
        
        return tab
        
    def create_advanced_options_tab(self) -> QWidget:
        """创建高级选项标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 创建滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # TALYS可执行文件设置
        talys_group, _ = self.create_group_box("TALYS可执行文件设置")
        talys_layout = self.create_form_layout()
        
        self.talys_path_edit = self.create_line_edit("", "TALYS可执行文件的完整路径")
        self.talys_path_edit.setText("talys")
        browse_button = self.create_push_button("浏览...", False, "浏览选择TALYS可执行文件")
        
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.talys_path_edit)
        path_layout.addWidget(browse_button)
        
        talys_layout.addRow("TALYS路径:", path_layout)
        
        self.timeout_spinbox = self.create_spin_box(10, 3600, 300, "计算超时时间（秒）")
        talys_layout.addRow("超时时间:", self.timeout_spinbox)
        
        talys_group.setLayout(talys_layout)
        scroll_layout.addWidget(talys_group)
        
        # 计算环境设置
        env_group, _ = self.create_group_box("计算环境设置")
        env_layout = self.create_form_layout()
        
        self.work_dir_edit = self.create_line_edit("", "TALYS工作目录")
        self.work_dir_edit.setText("./temp")
        work_dir_button = self.create_push_button("浏览...", False, "选择工作目录")
        
        work_dir_layout = QHBoxLayout()
        work_dir_layout.addWidget(self.work_dir_edit)
        work_dir_layout.addWidget(work_dir_button)
        
        env_layout.addRow("工作目录:", work_dir_layout)
        
        self.keep_files_checkbox = self.create_check_box("保留临时文件", False, "计算完成后保留临时文件")
        env_layout.addRow("", self.keep_files_checkbox)
        
        env_group.setLayout(env_layout)
        scroll_layout.addWidget(env_group)
        
        # 高级TALYS选项
        advanced_group, _ = self.create_group_box("高级TALYS选项")
        advanced_layout = QVBoxLayout()
        
        # 自定义参数编辑器
        custom_label = QLabel("自定义TALYS参数 (每行一个参数):")
        advanced_layout.addWidget(custom_label)
        
        self.custom_params_editor = QTextEdit()
        self.custom_params_editor.setMaximumHeight(150)
        self.custom_params_editor.setFont(QFont("Courier New", 10))
        self.custom_params_editor.setPlaceholderText("例如:\nldmodel 2\nstrength 5\nbins 50")
        advanced_layout.addWidget(self.custom_params_editor)
        
        advanced_group.setLayout(advanced_layout)
        scroll_layout.addWidget(advanced_group)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        return tab
        
    def create_debug_tab(self) -> QWidget:
        """创建调试信息标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 调试选项
        debug_options = QHBoxLayout()
        
        self.verbose_checkbox = self.create_check_box("详细输出", False, "启用详细的调试输出")
        self.trace_checkbox = self.create_check_box("跟踪执行", False, "跟踪TALYS执行过程")
        self.timing_checkbox = self.create_check_box("性能计时", True, "显示各阶段执行时间")
        
        debug_options.addWidget(self.verbose_checkbox)
        debug_options.addWidget(self.trace_checkbox)
        debug_options.addWidget(self.timing_checkbox)
        debug_options.addStretch()
        
        layout.addLayout(debug_options)
        
        # 调试信息显示
        self.debug_output = QTextEdit()
        self.debug_output.setReadOnly(True)
        self.debug_output.setFont(QFont("Courier New", 9))
        self.debug_output.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
            }
        """)
        self.debug_output.setPlainText("调试信息将在此处显示...\n")
        
        layout.addWidget(self.debug_output)
        
        # 调试控制按钮
        debug_controls = QHBoxLayout()
        
        self.clear_debug_button = self.create_push_button("清除日志", False, "清除调试输出")
        self.save_debug_button = self.create_push_button("保存日志", False, "保存调试信息到文件")
        
        debug_controls.addWidget(self.clear_debug_button)
        debug_controls.addWidget(self.save_debug_button)
        debug_controls.addStretch()
        
        layout.addLayout(debug_controls)
        
        return tab
        
    def connect_signals(self):
        """连接信号"""
        # 输入文件编辑器按钮
        self.load_button.clicked.connect(self.load_input_file)
        self.save_button.clicked.connect(self.save_input_file)
        self.generate_button.clicked.connect(self.generate_input_from_params)
        self.validate_input_button.clicked.connect(self.validate_input_syntax)
        
        # 输入文件内容变化
        self.input_editor.textChanged.connect(self.on_input_changed)
        
        # 调试控制按钮
        self.clear_debug_button.clicked.connect(self.clear_debug_output)
        self.save_debug_button.clicked.connect(self.save_debug_output)
        
    def load_input_file(self):
        """加载输入文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "加载TALYS输入文件", "", "TALYS输入文件 (*.inp);;所有文件 (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.input_editor.setPlainText(content)
                self.input_status.setText(f"已加载: {Path(file_path).name}")
            except Exception as e:
                self.show_error_message("加载失败", f"无法加载文件: {str(e)}")
                
    def save_input_file(self):
        """保存输入文件"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存TALYS输入文件", "talys.inp", "TALYS输入文件 (*.inp);;所有文件 (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.input_editor.toPlainText())
                self.input_status.setText(f"已保存: {Path(file_path).name}")
            except Exception as e:
                self.show_error_message("保存失败", f"无法保存文件: {str(e)}")
                
    def generate_input_from_params(self):
        """根据当前参数生成输入文件"""
        # TODO: 从参数同步器获取当前参数并生成输入文件
        self.input_status.setText("正在生成输入文件...")
        # 这里应该调用参数同步器获取所有参数
        self.show_info_message("生成输入", "输入文件生成功能开发中...")
        
    def validate_input_syntax(self):
        """验证输入文件语法"""
        content = self.input_editor.toPlainText()
        
        # 简单的语法检查
        lines = content.split('\n')
        errors = []
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split()
                if len(parts) < 2:
                    errors.append(f"第{i}行: 参数格式不正确")
                    
        if errors:
            error_msg = '\n'.join(errors[:10])  # 只显示前10个错误
            if len(errors) > 10:
                error_msg += f"\n... 还有{len(errors)-10}个错误"
            self.show_warning_message("语法错误", error_msg)
            self.input_status.setText(f"发现{len(errors)}个语法错误")
        else:
            self.show_info_message("语法检查", "输入文件语法正确！")
            self.input_status.setText("语法检查通过")
            
    def on_input_changed(self):
        """输入内容变化处理"""
        self.input_status.setText("已修改")
        
    def clear_debug_output(self):
        """清除调试输出"""
        self.debug_output.clear()
        
    def save_debug_output(self):
        """保存调试输出"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存调试日志", "debug.log", "日志文件 (*.log);;所有文件 (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.debug_output.toPlainText())
                self.show_info_message("保存成功", f"调试日志已保存到: {file_path}")
            except Exception as e:
                self.show_error_message("保存失败", f"无法保存日志: {str(e)}")
                
    def add_debug_message(self, message: str):
        """添加调试消息"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.debug_output.append(f"[{timestamp}] {message}")
        
    def get_parameters(self) -> Dict[str, Any]:
        """获取当前参数"""
        return {
            'talys_path': self.talys_path_edit.text(),
            'timeout': self.timeout_spinbox.value(),
            'work_dir': self.work_dir_edit.text(),
            'keep_files': self.keep_files_checkbox.isChecked(),
            'custom_params': self.custom_params_editor.toPlainText(),
            'verbose': self.verbose_checkbox.isChecked(),
            'trace': self.trace_checkbox.isChecked(),
            'timing': self.timing_checkbox.isChecked(),
        }
    
    def set_parameters(self, parameters: Dict[str, Any]):
        """设置参数值"""
        if 'talys_path' in parameters:
            self.talys_path_edit.setText(str(parameters['talys_path']))
        if 'timeout' in parameters:
            self.timeout_spinbox.setValue(int(parameters['timeout']))
        if 'work_dir' in parameters:
            self.work_dir_edit.setText(str(parameters['work_dir']))
        if 'keep_files' in parameters:
            self.keep_files_checkbox.setChecked(bool(parameters['keep_files']))
        if 'custom_params' in parameters:
            self.custom_params_editor.setPlainText(str(parameters['custom_params']))
        if 'verbose' in parameters:
            self.verbose_checkbox.setChecked(bool(parameters['verbose']))
        if 'trace' in parameters:
            self.trace_checkbox.setChecked(bool(parameters['trace']))
        if 'timing' in parameters:
            self.timing_checkbox.setChecked(bool(parameters['timing']))
    
    def get_relevant_parameters(self, global_params: Dict[str, Any]) -> Dict[str, Any]:
        """获取与本标签页相关的参数"""
        # 专家模式参数通常是独立的
        return {}
    
    def validate_parameters(self) -> tuple[bool, str]:
        """验证当前参数"""
        # 检查TALYS路径
        talys_path = self.talys_path_edit.text().strip()
        if not talys_path:
            return False, "TALYS可执行文件路径不能为空"
            
        # 检查超时时间
        timeout = self.timeout_spinbox.value()
        if timeout < 10:
            return False, "超时时间不能少于10秒"
            
        return True, ""
    
    def reset_to_defaults(self):
        """重置到默认值"""
        self.talys_path_edit.setText("talys")
        self.timeout_spinbox.setValue(300)
        self.work_dir_edit.setText("./temp")
        self.keep_files_checkbox.setChecked(False)
        self.custom_params_editor.clear()
        self.verbose_checkbox.setChecked(False)
        self.trace_checkbox.setChecked(False)
        self.timing_checkbox.setChecked(True)
