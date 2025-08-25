"""
可视化标签页
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

class VisualizationTab(BaseParameterTab):
    """可视化标签页"""

    def __init__(self):
        super().__init__()

    def init_ui(self):
        """初始化用户界面"""
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 标题
        title = QLabel(tr('visualization_title'))
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #212529;
                margin-bottom: 8px;
            }
        """)
        main_layout.addWidget(title)

        # 说明文字
        description = QLabel(tr('visualization_description'))
        description.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 12px;
                margin-bottom: 16px;
            }
        """)
        description.setWordWrap(True)
        main_layout.addWidget(description)
        
        # 创建可视化区域
        self.create_visualization_area(main_layout)
        
    def create_visualization_area(self, parent_layout):
        """创建可视化区域"""
        # 创建标签页组件用于不同类型的可视化
        self.viz_tabs = QTabWidget()
        self.viz_tabs.setTabPosition(QTabWidget.TabPosition.North)
        
        # 截面图标签页
        self.cross_section_tab = self.create_cross_section_tab()
        self.viz_tabs.addTab(self.cross_section_tab, "📈 截面图")
        
        # 能谱图标签页
        self.spectra_tab = self.create_spectra_tab()
        self.viz_tabs.addTab(self.spectra_tab, "📊 能谱图")
        
        # 角分布标签页
        self.angular_tab = self.create_angular_tab()
        self.viz_tabs.addTab(self.angular_tab, "🎯 角分布")
        
        # 文件查看器标签页
        self.file_viewer_tab = self.create_file_viewer_tab()
        self.viz_tabs.addTab(self.file_viewer_tab, "📁 文件查看")
        
        parent_layout.addWidget(self.viz_tabs)
        
    def create_cross_section_tab(self) -> QWidget:
        """创建截面图标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 工具栏
        toolbar = QHBoxLayout()
        
        self.plot_type_combo = self.create_combo_box([
            "总截面",
            "弹性散射截面", 
            "非弹性截面",
            "分反应道截面"
        ], "选择要显示的截面类型")
        toolbar.addWidget(QLabel("图表类型:"))
        toolbar.addWidget(self.plot_type_combo)
        
        self.log_scale_checkbox = self.create_check_box("对数坐标", False, "使用对数坐标显示")
        toolbar.addWidget(self.log_scale_checkbox)
        
        toolbar.addStretch()
        
        self.export_button = self.create_push_button("导出图表", False, "导出当前图表")
        toolbar.addWidget(self.export_button)
        
        layout.addLayout(toolbar)
        
        # 图表区域占位符
        self.cross_section_placeholder = QLabel("运行TALYS计算后，截面图将在此处显示")
        self.cross_section_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cross_section_placeholder.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-style: italic;
                font-size: 14px;
                border: 2px dashed #dee2e6;
                border-radius: 8px;
                padding: 40px;
                background-color: #f8f9fa;
            }
        """)
        layout.addWidget(self.cross_section_placeholder)
        
        return tab
        
    def create_spectra_tab(self) -> QWidget:
        """创建能谱图标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 工具栏
        toolbar = QHBoxLayout()
        
        self.particle_combo = self.create_combo_box([
            "中子能谱",
            "质子能谱",
            "α粒子能谱",
            "伽马射线能谱"
        ], "选择粒子类型")
        toolbar.addWidget(QLabel("粒子类型:"))
        toolbar.addWidget(self.particle_combo)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        # 能谱图占位符
        self.spectra_placeholder = QLabel("选择输出能谱选项并运行计算后，能谱图将在此处显示")
        self.spectra_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spectra_placeholder.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-style: italic;
                font-size: 14px;
                border: 2px dashed #dee2e6;
                border-radius: 8px;
                padding: 40px;
                background-color: #f8f9fa;
            }
        """)
        layout.addWidget(self.spectra_placeholder)
        
        return tab
        
    def create_angular_tab(self) -> QWidget:
        """创建角分布标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 角分布图占位符
        self.angular_placeholder = QLabel("选择角分布输出选项并运行计算后，角分布图将在此处显示")
        self.angular_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.angular_placeholder.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-style: italic;
                font-size: 14px;
                border: 2px dashed #dee2e6;
                border-radius: 8px;
                padding: 40px;
                background-color: #f8f9fa;
            }
        """)
        layout.addWidget(self.angular_placeholder)
        
        return tab
        
    def create_file_viewer_tab(self) -> QWidget:
        """创建文件查看器标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 文件列表和内容查看器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧文件列表
        file_list_widget = QWidget()
        file_list_layout = QVBoxLayout(file_list_widget)
        
        file_list_layout.addWidget(QLabel("输出文件:"))
        self.file_list = QListWidget()
        self.file_list.setMaximumWidth(200)
        file_list_layout.addWidget(self.file_list)
        
        splitter.addWidget(file_list_widget)
        
        # 右侧文件内容
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        content_layout.addWidget(QLabel("文件内容:"))
        self.file_content = QTextEdit()
        self.file_content.setReadOnly(True)
        self.file_content.setFont(QFont("Courier New", 10))
        content_layout.addWidget(self.file_content)
        
        splitter.addWidget(content_widget)
        splitter.setSizes([200, 600])
        
        layout.addWidget(splitter)
        
        return tab
        
    def connect_signals(self):
        """连接信号"""
        # 文件列表选择变化
        self.file_list.currentItemChanged.connect(self.on_file_selected)
        
        # 图表选项变化
        self.plot_type_combo.currentTextChanged.connect(self.update_cross_section_plot)
        self.log_scale_checkbox.toggled.connect(self.update_cross_section_plot)
        self.particle_combo.currentTextChanged.connect(self.update_spectra_plot)
        
        # 导出按钮
        self.export_button.clicked.connect(self.export_current_plot)
        
    def on_file_selected(self, current, previous):
        """文件选择变化处理"""
        if current:
            filename = current.text()
            # TODO: 加载并显示文件内容
            self.file_content.setPlainText(f"文件: {filename}\n\n文件内容加载功能开发中...")
            
    def update_cross_section_plot(self):
        """更新截面图"""
        # TODO: 实现截面图更新逻辑
        plot_type = self.plot_type_combo.currentText()
        log_scale = self.log_scale_checkbox.isChecked()
        self.cross_section_placeholder.setText(
            f"更新{plot_type}图表中...\n对数坐标: {'是' if log_scale else '否'}"
        )
        
    def update_spectra_plot(self):
        """更新能谱图"""
        # TODO: 实现能谱图更新逻辑
        particle_type = self.particle_combo.currentText()
        self.spectra_placeholder.setText(f"更新{particle_type}图表中...")
        
    def export_current_plot(self):
        """导出当前图表"""
        # TODO: 实现图表导出功能
        self.show_info_message("导出图表", "图表导出功能开发中...")
        
    def update_visualization(self, results: Dict[str, Any]):
        """更新可视化内容"""
        # 更新文件列表
        output_files = results.get('output_files', [])
        self.file_list.clear()
        for file in output_files:
            self.file_list.addItem(file)
            
        # 更新截面图
        if 'total_cross_section' in results:
            self.cross_section_placeholder.setText("截面数据已加载，图表生成中...")
            
        # 切换到截面图标签页
        self.viz_tabs.setCurrentIndex(0)
        
    def get_parameters(self) -> Dict[str, Any]:
        """获取当前参数（可视化标签页通常不需要参数）"""
        return {}
    
    def set_parameters(self, parameters: Dict[str, Any]):
        """设置参数值（可视化标签页通常不需要设置参数）"""
        pass
    
    def get_relevant_parameters(self, global_params: Dict[str, Any]) -> Dict[str, Any]:
        """获取与本标签页相关的参数"""
        return {}
    
    def validate_parameters(self) -> tuple[bool, str]:
        """验证当前参数"""
        return True, ""
    
    def reset_to_defaults(self):
        """重置到默认值"""
        pass
