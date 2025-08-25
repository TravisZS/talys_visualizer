"""
TALYS Visualizer 主窗口
"""

import sys
import logging
from pathlib import Path
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config.settings import Settings
from utils.logger import LoggerMixin
from .parameter_panels import BasicParameterPanel
from .calculation_widget import CalculationControlWidget

class MainWindow(QMainWindow, LoggerMixin):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.logger.info("主窗口初始化完成")
        
    def init_ui(self):
        """初始化用户界面"""
        # 设置窗口基本属性
        self.setWindowTitle(f"{Settings.APP_NAME} v{Settings.APP_VERSION}")
        self.setGeometry(100, 100, Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)
        self.setMinimumSize(Settings.WINDOW_MIN_WIDTH, Settings.WINDOW_MIN_HEIGHT)
        
        # 设置窗口图标（如果存在）
        icon_path = Settings.RESOURCES_DIR / "icons" / "app.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # 左侧参数面板（占1/4宽度）
        self.parameter_panel = self.create_parameter_panel()
        main_layout.addWidget(self.parameter_panel, 1)
        
        # 右侧可视化区域（占3/4宽度）
        self.visualization_area = self.create_visualization_area()
        main_layout.addWidget(self.visualization_area, 3)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建工具栏
        self.create_toolbar()
        
        # 创建状态栏
        self.create_status_bar()
        
        # 应用样式
        self.apply_style()
        
    def create_parameter_panel(self) -> QWidget:
        """创建参数设置面板"""
        panel = QWidget()
        panel.setMaximumWidth(450)
        panel.setMinimumWidth(350)

        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        layout.setContentsMargins(5, 5, 5, 5)

        # 基础参数面板
        self.basic_params = BasicParameterPanel()
        layout.addWidget(self.basic_params)

        # 计算控制组件
        self.calculation_control = CalculationControlWidget()
        layout.addWidget(self.calculation_control)

        # 连接信号
        self.basic_params.parameters_changed.connect(
            self.calculation_control.update_parameters
        )
        self.calculation_control.calculation_completed.connect(
            self.on_calculation_completed
        )

        return panel
    
    def create_visualization_area(self) -> QWidget:
        """创建可视化区域"""
        area = QWidget()
        
        layout = QVBoxLayout(area)
        
        # 标题
        title = QLabel("可视化结果")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # 临时占位内容
        placeholder = QLabel("可视化区域\n(开发中...)")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("color: gray; font-style: italic; font-size: 24px;")
        layout.addWidget(placeholder)
        
        return area
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件(&F)')
        
        # 新建
        new_action = QAction('新建(&N)', self)
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip('创建新的计算项目')
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)
        
        # 打开
        open_action = QAction('打开(&O)', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('打开现有项目')
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)
        
        # 保存
        save_action = QAction('保存(&S)', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('保存当前项目')
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        # 退出
        exit_action = QAction('退出(&X)', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('退出程序')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 计算菜单
        calc_menu = menubar.addMenu('计算(&C)')
        
        run_action = QAction('运行TALYS(&R)', self)
        run_action.setShortcut('F5')
        run_action.setStatusTip('运行TALYS计算')
        run_action.triggered.connect(self.run_calculation)
        calc_menu.addAction(run_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助(&H)')
        
        about_action = QAction('关于(&A)', self)
        about_action.setStatusTip('关于TALYS Visualizer')
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = self.addToolBar('主工具栏')
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        
        # 运行按钮
        run_action = QAction('运行', self)
        run_action.setStatusTip('运行TALYS计算')
        run_action.triggered.connect(self.run_calculation)
        toolbar.addAction(run_action)
        
        toolbar.addSeparator()
        
        # 停止按钮
        stop_action = QAction('停止', self)
        stop_action.setStatusTip('停止当前计算')
        stop_action.triggered.connect(self.stop_calculation)
        toolbar.addAction(stop_action)
    
    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('就绪')
        
        # 添加进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumWidth(200)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # 添加状态标签
        self.status_label = QLabel('未连接TALYS')
        self.status_bar.addPermanentWidget(self.status_label)
    
    def apply_style(self):
        """应用样式"""
        # 设置现代化的样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 10pt;
            }
            QLabel {
                color: #333333;
            }
            QMenuBar {
                background-color: #ffffff;
                border-bottom: 1px solid #cccccc;
            }
            QMenuBar::item {
                padding: 4px 8px;
                background-color: transparent;
            }
            QMenuBar::item:selected {
                background-color: #e0e0e0;
            }
            QToolBar {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                spacing: 3px;
            }
            QStatusBar {
                background-color: #ffffff;
                border-top: 1px solid #cccccc;
            }
        """)
    
    # 槽函数
    def new_project(self):
        """新建项目"""
        self.logger.info("新建项目")
        self.status_bar.showMessage('新建项目', 2000)
    
    def open_project(self):
        """打开项目"""
        self.logger.info("打开项目")
        self.status_bar.showMessage('打开项目', 2000)
    
    def save_project(self):
        """保存项目"""
        self.logger.info("保存项目")
        self.status_bar.showMessage('保存项目', 2000)
    
    def run_calculation(self):
        """运行计算"""
        self.logger.info("通过菜单运行TALYS计算")
        # 触发计算控制组件的计算
        if hasattr(self, 'calculation_control'):
            self.calculation_control.start_calculation()
        else:
            self.status_bar.showMessage('计算组件未初始化', 2000)
    
    def stop_calculation(self):
        """停止计算"""
        self.logger.info("停止计算")
        self.status_bar.showMessage('停止计算', 2000)
    
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(self, '关于', 
                         f'{Settings.APP_NAME} v{Settings.APP_VERSION}\n\n'
                         f'TALYS核反应计算可视化工具\n'
                         f'作者: {Settings.APP_AUTHOR}')
    
    def on_calculation_completed(self, results: dict):
        """计算完成处理"""
        self.logger.info("收到计算完成信号")

        # 更新状态栏
        calc_time = results.get('calculation_time', 0)
        file_count = len(results.get('output_files', []))
        self.status_bar.showMessage(
            f'计算完成 - 耗时: {calc_time:.2f}秒, 输出文件: {file_count}个',
            5000
        )

        # 更新可视化区域
        self.update_visualization_area(results)

    def update_visualization_area(self, results: dict):
        """更新可视化区域显示计算结果"""
        # 创建结果显示内容
        result_text = []
        result_text.append("🎉 TALYS计算完成!")
        result_text.append("")
        result_text.append(f"⏱️ 计算耗时: {results.get('calculation_time', 0):.2f} 秒")
        result_text.append(f"📁 输出文件数: {len(results.get('output_files', []))}")

        if 'total_cross_section' in results:
            xs_data = results['total_cross_section']
            data_points = len(xs_data.get('energy', []))
            result_text.append(f"📊 截面数据点: {data_points}")

        result_text.append("")
        result_text.append("📋 生成的文件:")

        output_files = results.get('output_files', [])
        for i, file in enumerate(output_files[:10]):  # 显示前10个文件
            result_text.append(f"  • {file}")

        if len(output_files) > 10:
            result_text.append(f"  ... 还有 {len(output_files) - 10} 个文件")

        # 更新可视化区域的占位符
        if hasattr(self, 'visualization_area'):
            # 清除现有内容
            layout = self.visualization_area.layout()
            if layout:
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()

            # 添加新的结果显示
            title = QLabel("计算结果")
            title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
            layout.addWidget(title)

            result_label = QLabel('\n'.join(result_text))
            result_label.setStyleSheet("""
                QLabel {
                    background-color: #e8f5e8;
                    border: 2px solid #27ae60;
                    border-radius: 10px;
                    padding: 20px;
                    font-size: 12px;
                    line-height: 1.5;
                }
            """)
            result_label.setWordWrap(True)
            layout.addWidget(result_label)

            # 添加"查看详细结果"按钮
            view_button = QPushButton("查看详细结果")
            view_button.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    font-weight: bold;
                    margin: 10px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            view_button.clicked.connect(lambda: self.show_detailed_results(results))
            layout.addWidget(view_button)

            layout.addStretch()

    def show_detailed_results(self, results: dict):
        """显示详细结果对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("详细计算结果")
        dialog.setModal(True)
        dialog.resize(600, 400)

        layout = QVBoxLayout(dialog)

        # 创建文本显示区域
        text_area = QTextEdit()
        text_area.setReadOnly(True)
        text_area.setFont(QFont("Courier", 10))

        # 格式化详细结果
        detailed_text = []
        detailed_text.append("TALYS 计算结果详情")
        detailed_text.append("=" * 50)
        detailed_text.append(f"计算耗时: {results.get('calculation_time', 0):.3f} 秒")
        detailed_text.append(f"输出文件总数: {len(results.get('output_files', []))}")
        detailed_text.append("")

        # 显示所有输出文件
        detailed_text.append("输出文件列表:")
        detailed_text.append("-" * 30)
        for file in results.get('output_files', []):
            detailed_text.append(f"  {file}")

        # 显示截面数据（如果有）
        if 'total_cross_section' in results:
            xs_data = results['total_cross_section']
            energies = xs_data.get('energy', [])
            cross_sections = xs_data.get('cross_section', [])

            detailed_text.append("")
            detailed_text.append("总截面数据:")
            detailed_text.append("-" * 30)
            detailed_text.append(f"数据点数: {len(energies)}")

            if energies and cross_sections:
                detailed_text.append(f"能量范围: {min(energies):.3f} - {max(energies):.3f} MeV")
                detailed_text.append(f"截面范围: {min(cross_sections):.3e} - {max(cross_sections):.3e} mb")

                # 显示前几个数据点
                detailed_text.append("")
                detailed_text.append("前10个数据点:")
                detailed_text.append("能量(MeV)    截面(mb)")
                for i in range(min(10, len(energies))):
                    detailed_text.append(f"{energies[i]:8.3f}    {cross_sections[i]:12.3e}")

        text_area.setPlainText('\n'.join(detailed_text))
        layout.addWidget(text_area)

        # 关闭按钮
        close_button = QPushButton("关闭")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)

        dialog.exec()

    def closeEvent(self, event):
        """窗口关闭事件"""
        # 停止正在进行的计算
        if hasattr(self, 'calculation_control'):
            self.calculation_control.stop_calculation()

        self.logger.info("程序退出")
        event.accept()
