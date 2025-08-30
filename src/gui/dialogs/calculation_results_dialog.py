"""
计算结果显示对话框
"""

import sys
from pathlib import Path
from typing import Dict, Any
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from utils.i18n import tr

class CalculationResultsDialog(QDialog):
    """计算结果显示对话框"""
    
    def __init__(self, results: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.results = results
        self.init_ui()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle(tr('calculation_results_title', "计算结果"))
        self.setModal(True)
        self.resize(800, 600)
        
        # 主布局
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title = QLabel(tr('calculation_results_title', "TALYS计算结果"))
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(title)
        
        # 创建标签页
        self.create_tabs(layout)
        
        # 按钮区域
        self.create_buttons(layout)
        
    def create_tabs(self, parent_layout):
        """创建标签页"""
        self.tab_widget = QTabWidget()
        
        # 基本信息标签页
        self.create_summary_tab()
        
        # 截面数据标签页
        if 'total_cross_section' in self.results:
            self.create_cross_section_tab()
        
        # 能谱数据标签页
        if 'spectra' in self.results:
            self.create_spectra_tab()
        
        # 输出文件标签页
        self.create_files_tab()
        
        parent_layout.addWidget(self.tab_widget)
        
    def create_summary_tab(self):
        """创建摘要标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 计算信息
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setMaximumHeight(200)
        
        summary_lines = []
        if 'calculation_time' in self.results:
            summary_lines.append(f"计算时间: {self.results['calculation_time']:.2f} 秒")
        
        if 'output_files' in self.results:
            summary_lines.append(f"输出文件数量: {len(self.results['output_files'])}")
        
        # 添加数据类型统计
        data_types = []
        if 'total_cross_section' in self.results:
            data_types.append("总截面")
        if 'spectra' in self.results:
            data_types.append(f"能谱 ({len(self.results['spectra'])}种)")
        if 'angular' in self.results:
            data_types.append(f"角分布 ({len(self.results['angular'])}个)")
        if 'residual_production' in self.results:
            data_types.append(f"残余核产生 ({len(self.results['residual_production'])}个)")
        
        if data_types:
            summary_lines.append(f"数据类型: {', '.join(data_types)}")
        
        info_text.setPlainText('\n'.join(summary_lines))
        layout.addWidget(QLabel("计算摘要:"))
        layout.addWidget(info_text)
        
        # 标准输出
        if 'stdout' in self.results and self.results['stdout']:
            stdout_text = QTextEdit()
            stdout_text.setReadOnly(True)
            stdout_text.setPlainText(self.results['stdout'])
            stdout_text.setFont(QFont("Courier", 9))
            layout.addWidget(QLabel("TALYS输出:"))
            layout.addWidget(stdout_text)
        
        self.tab_widget.addTab(widget, "📊 摘要")
        
    def create_cross_section_tab(self):
        """创建截面数据标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 总截面数据
        if 'total_cross_section' in self.results:
            cs_data = self.results['total_cross_section']
            if cs_data['energy'] and cs_data['cross_section']:
                table = QTableWidget()
                table.setColumnCount(2)
                table.setHorizontalHeaderLabels(["能量 (MeV)", "截面 (mb)"])
                table.setRowCount(len(cs_data['energy']))
                
                for i, (energy, cs) in enumerate(zip(cs_data['energy'], cs_data['cross_section'])):
                    table.setItem(i, 0, QTableWidgetItem(f"{energy:.3f}"))
                    table.setItem(i, 1, QTableWidgetItem(f"{cs:.6e}"))
                
                table.resizeColumnsToContents()
                layout.addWidget(QLabel("总截面数据:"))
                layout.addWidget(table)
            else:
                layout.addWidget(QLabel("未找到总截面数据"))
        
        self.tab_widget.addTab(widget, "📈 截面")
        
    def create_spectra_tab(self):
        """创建能谱数据标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        spectra_data = self.results['spectra']
        
        # 创建子标签页
        spectra_tabs = QTabWidget()
        
        for particle, data in spectra_data.items():
            if data['energy'] and data['intensity']:
                particle_widget = QWidget()
                particle_layout = QVBoxLayout(particle_widget)
                
                table = QTableWidget()
                table.setColumnCount(2)
                table.setHorizontalHeaderLabels(["能量 (MeV)", "强度"])
                table.setRowCount(len(data['energy']))
                
                for i, (energy, intensity) in enumerate(zip(data['energy'], data['intensity'])):
                    table.setItem(i, 0, QTableWidgetItem(f"{energy:.3f}"))
                    table.setItem(i, 1, QTableWidgetItem(f"{intensity:.6e}"))
                
                table.resizeColumnsToContents()
                particle_layout.addWidget(table)
                
                spectra_tabs.addTab(particle_widget, particle)
        
        if spectra_tabs.count() > 0:
            layout.addWidget(spectra_tabs)
        else:
            layout.addWidget(QLabel("未找到能谱数据"))
        
        self.tab_widget.addTab(widget, "🌈 能谱")
        
    def create_files_tab(self):
        """创建文件列表标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        if 'output_files' in self.results:
            file_list = QListWidget()
            for filename in sorted(self.results['output_files']):
                file_list.addItem(filename)
            
            layout.addWidget(QLabel(f"输出文件 ({len(self.results['output_files'])} 个):"))
            layout.addWidget(file_list)
        else:
            layout.addWidget(QLabel("未找到输出文件信息"))
        
        self.tab_widget.addTab(widget, "📁 文件")
        
    def create_buttons(self, parent_layout):
        """创建按钮区域"""
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # 导出按钮
        export_button = QPushButton("导出数据")
        export_button.clicked.connect(self.export_data)
        button_layout.addWidget(export_button)
        
        # 关闭按钮
        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.accept)
        close_button.setDefault(True)
        button_layout.addWidget(close_button)
        
        parent_layout.addLayout(button_layout)
        
    def export_data(self):
        """导出数据"""
        # TODO: 实现数据导出功能
        QMessageBox.information(self, "导出", "数据导出功能开发中...")
