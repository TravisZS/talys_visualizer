"""
TALYS Visualizer 分栏式主窗口
基于XFresco设计的标签页布局
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
from utils.i18n import get_language_manager, tr
from .tabs.basic_parameters_tab import BasicParametersTab
from .tabs.advanced_parameters_tab import AdvancedParametersTab
from .tabs.output_options_tab import OutputOptionsTab
from .tabs.visualization_tab import VisualizationTab
from .tabs.expert_mode_tab import ExpertModeTab
from .parameter_synchronizer import ParameterSynchronizer

class TabbedMainWindow(QMainWindow, LoggerMixin):
    """分栏式主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.parameter_sync = ParameterSynchronizer()
        self.language_manager = get_language_manager()
        self.init_ui()
        self.connect_language_signals()
        self.logger.info("分栏式主窗口初始化完成")
        
    def init_ui(self):
        """初始化用户界面"""
        # 设置窗口基本属性
        self.setWindowTitle(f"{tr('app_title')} v{Settings.APP_VERSION}")
        self.setGeometry(100, 100, Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)
        self.setMinimumSize(Settings.WINDOW_MIN_WIDTH, Settings.WINDOW_MIN_HEIGHT)
        
        # 设置窗口图标（如果存在）
        icon_path = Settings.RESOURCES_DIR / "icons" / "app.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        # 创建中央标签页组件
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        
        # 设置标签页样式
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        self.tab_widget.setTabsClosable(False)
        self.tab_widget.setMovable(False)
        
        # 添加各个标签页
        self.add_tabs()
        self.update_ui_language()
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建工具栏
        self.create_toolbar()
        
        # 创建状态栏
        self.create_status_bar()
        
        # 应用样式
        self.apply_style()
        
        # 连接信号
        self.connect_signals()
        
    def add_tabs(self):
        """添加所有标签页"""
        # 基础参数标签页
        self.basic_tab = BasicParametersTab()
        self.tab_widget.addTab(self.basic_tab, "🎯 基础参数")
        self.parameter_sync.register_tab(self.basic_tab)
        
        # 高级参数标签页
        self.advanced_tab = AdvancedParametersTab()
        self.tab_widget.addTab(self.advanced_tab, "⚙️ 高级参数")
        self.parameter_sync.register_tab(self.advanced_tab)
        
        # 输出选项标签页
        self.output_tab = OutputOptionsTab()
        self.tab_widget.addTab(self.output_tab, "📄 输出选项")
        self.parameter_sync.register_tab(self.output_tab)
        
        # 可视化标签页
        self.visualization_tab = VisualizationTab()
        self.tab_widget.addTab(self.visualization_tab, "📊 可视化")
        
        # 专家模式标签页
        self.expert_tab = ExpertModeTab()
        self.tab_widget.addTab(self.expert_tab, "🔧 专家模式")
        
        # 设置标签页工具提示
        self.tab_widget.setTabToolTip(0, "设置目标核、入射粒子和基本计算参数")
        self.tab_widget.setTabToolTip(1, "配置物理模型和高级计算选项")
        self.tab_widget.setTabToolTip(2, "控制输出文件和数据格式")
        self.tab_widget.setTabToolTip(3, "查看和分析计算结果")
        self.tab_widget.setTabToolTip(4, "直接编辑TALYS输入文件和高级选项")
        
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu(tr('menu_file'))
        
        # 新建
        new_action = QAction('新建项目(&N)', self)
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip('创建新的计算项目')
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)
        
        # 打开
        open_action = QAction('打开项目(&O)', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('打开现有项目')
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)
        
        # 保存
        save_action = QAction('保存项目(&S)', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('保存当前项目')
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        # 导入/导出
        import_action = QAction('导入参数(&I)', self)
        import_action.setStatusTip('从文件导入参数设置')
        import_action.triggered.connect(self.import_parameters)
        file_menu.addAction(import_action)
        
        export_action = QAction('导出参数(&E)', self)
        export_action.setStatusTip('导出当前参数设置')
        export_action.triggered.connect(self.export_parameters)
        file_menu.addAction(export_action)
        
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
        
        stop_action = QAction('停止计算(&T)', self)
        stop_action.setShortcut('Ctrl+Break')
        stop_action.setStatusTip('停止当前计算')
        stop_action.triggered.connect(self.stop_calculation)
        calc_menu.addAction(stop_action)
        
        calc_menu.addSeparator()
        
        validate_action = QAction('验证参数(&V)', self)
        validate_action.setStatusTip('验证当前参数设置')
        validate_action.triggered.connect(self.validate_parameters)
        calc_menu.addAction(validate_action)
        
        # 视图菜单
        view_menu = menubar.addMenu('视图(&V)')
        
        # 标签页快速切换
        for i in range(self.tab_widget.count()):
            tab_name = self.tab_widget.tabText(i)
            action = QAction(f'切换到{tab_name}(&{i+1})', self)
            action.setShortcut(f'Ctrl+{i+1}')
            action.triggered.connect(lambda checked, idx=i: self.tab_widget.setCurrentIndex(idx))
            view_menu.addAction(action)
        
        view_menu.addSeparator()
        
        fullscreen_action = QAction('全屏模式(&F)', self)
        fullscreen_action.setShortcut('F11')
        fullscreen_action.setCheckable(True)
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)

        # 语言菜单
        language_menu = menubar.addMenu(tr('menu_language'))
        self.create_language_menu(language_menu)

        # 帮助菜单
        help_menu = menubar.addMenu(tr('menu_help'))
        
        help_action = QAction('用户手册(&H)', self)
        help_action.setShortcut('F1')
        help_action.setStatusTip('打开用户手册')
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)
        
        about_action = QAction('关于(&A)', self)
        about_action.setStatusTip('关于TALYS Visualizer')
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_language_menu(self, language_menu):
        """创建语言菜单"""
        available_languages = self.language_manager.get_available_languages()
        current_language = self.language_manager.get_current_language()

        # 创建语言动作组（单选）
        self.language_group = QActionGroup(self)

        for lang_code, lang_info in available_languages.items():
            action = QAction(f"{lang_info['flag']} {lang_info['native_name']}", self)
            action.setCheckable(True)
            action.setData(lang_code)

            if lang_code == current_language:
                action.setChecked(True)

            action.triggered.connect(lambda checked, code=lang_code: self.change_language(code))

            self.language_group.addAction(action)
            language_menu.addAction(action)
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = self.addToolBar('主工具栏')
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        
        # 新建项目
        new_action = QAction('新建', self)
        new_action.setStatusTip('创建新项目')
        new_action.triggered.connect(self.new_project)
        toolbar.addAction(new_action)
        
        # 打开项目
        open_action = QAction('打开', self)
        open_action.setStatusTip('打开项目')
        open_action.triggered.connect(self.open_project)
        toolbar.addAction(open_action)
        
        # 保存项目
        save_action = QAction('保存', self)
        save_action.setStatusTip('保存项目')
        save_action.triggered.connect(self.save_project)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # 运行计算
        run_action = QAction('▶️ 运行', self)
        run_action.setStatusTip('运行TALYS计算')
        run_action.triggered.connect(self.run_calculation)
        toolbar.addAction(run_action)
        
        # 停止计算
        stop_action = QAction('⏹️ 停止', self)
        stop_action.setStatusTip('停止当前计算')
        stop_action.triggered.connect(self.stop_calculation)
        toolbar.addAction(stop_action)
        
        toolbar.addSeparator()
        
        # 验证参数
        validate_action = QAction('✅ 验证', self)
        validate_action.setStatusTip('验证参数设置')
        validate_action.triggered.connect(self.validate_parameters)
        toolbar.addAction(validate_action)
    
    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('就绪')
        
        # 添加进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumWidth(200)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # 添加当前标签页指示器
        self.tab_indicator = QLabel('基础参数')
        self.tab_indicator.setStyleSheet("QLabel { color: #666; font-style: italic; }")
        self.status_bar.addPermanentWidget(self.tab_indicator)
        
        # 添加TALYS状态标签
        self.talys_status = QLabel('TALYS: 未连接')
        self.status_bar.addPermanentWidget(self.talys_status)
    
    def apply_style(self):
        """应用样式"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                background-color: white;
                border-radius: 4px;
            }
            QTabWidget::tab-bar {
                alignment: left;
            }
            QTabBar::tab {
                background-color: #e9ecef;
                border: 1px solid #dee2e6;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 16px;
                margin-right: 2px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 1px solid white;
            }
            QTabBar::tab:hover {
                background-color: #f8f9fa;
            }
            QMenuBar {
                background-color: #ffffff;
                border-bottom: 1px solid #dee2e6;
            }
            QMenuBar::item {
                padding: 6px 12px;
                background-color: transparent;
            }
            QMenuBar::item:selected {
                background-color: #e9ecef;
                border-radius: 4px;
            }
            QToolBar {
                background-color: #ffffff;
                border: 1px solid #dee2e6;
                spacing: 4px;
                padding: 4px;
            }
            QStatusBar {
                background-color: #f8f9fa;
                border-top: 1px solid #dee2e6;
            }
        """)
    
    def connect_signals(self):
        """连接信号"""
        # 标签页切换信号
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        # 参数同步信号
        self.parameter_sync.parameters_updated.connect(self.on_parameters_updated)
        
        # 计算相关信号
        self.basic_tab.calculation_requested.connect(self.run_calculation)
        
    def on_tab_changed(self, index: int):
        """标签页切换处理"""
        tab_names = ['基础参数', '高级参数', '输出选项', '可视化', '专家模式']
        if 0 <= index < len(tab_names):
            self.tab_indicator.setText(tab_names[index])
            self.logger.debug(f"切换到标签页: {tab_names[index]}")
    
    def on_parameters_updated(self, parameters: dict):
        """参数更新处理"""
        self.logger.debug("全局参数已更新")
        # 可以在这里添加参数验证逻辑
        
    # 槽函数实现
    def new_project(self):
        """新建项目"""
        self.logger.info("新建项目")
        self.parameter_sync.reset_parameters()
        self.status_bar.showMessage('新建项目', 2000)
    
    def open_project(self):
        """打开项目"""
        self.logger.info("打开项目")
        # TODO: 实现项目文件打开逻辑
        self.status_bar.showMessage('打开项目', 2000)
    
    def save_project(self):
        """保存项目"""
        self.logger.info("保存项目")
        # TODO: 实现项目文件保存逻辑
        self.status_bar.showMessage('保存项目', 2000)
    
    def import_parameters(self):
        """导入参数"""
        self.logger.info("导入参数")
        # TODO: 实现参数导入逻辑
        self.status_bar.showMessage('导入参数', 2000)
    
    def export_parameters(self):
        """导出参数"""
        self.logger.info("导出参数")
        # TODO: 实现参数导出逻辑
        self.status_bar.showMessage('导出参数', 2000)
    
    def run_calculation(self):
        """运行计算"""
        self.logger.info("运行TALYS计算")
        parameters = self.parameter_sync.get_all_parameters()
        
        # 切换到可视化标签页显示结果
        self.tab_widget.setCurrentIndex(3)
        
        # TODO: 启动计算线程
        self.status_bar.showMessage('正在运行TALYS计算...', 5000)
    
    def stop_calculation(self):
        """停止计算"""
        self.logger.info("停止计算")
        # TODO: 实现计算停止逻辑
        self.status_bar.showMessage('计算已停止', 2000)
    
    def validate_parameters(self):
        """验证参数"""
        self.logger.info("验证参数")
        parameters = self.parameter_sync.get_all_parameters()
        # TODO: 实现参数验证逻辑
        self.status_bar.showMessage('参数验证完成', 2000)
    
    def toggle_fullscreen(self, checked: bool):
        """切换全屏模式"""
        if checked:
            self.showFullScreen()
        else:
            self.showNormal()
    
    def show_help(self):
        """显示帮助"""
        self.logger.info("显示帮助")
        # TODO: 实现帮助系统
        QMessageBox.information(self, '帮助', '用户手册功能开发中...')
    
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(self, '关于', 
                         f'{Settings.APP_NAME} v{Settings.APP_VERSION}\n\n'
                         f'TALYS核反应计算可视化工具\n'
                         f'采用分栏式界面设计，提供专业的参数设置和结果可视化功能\n\n'
                         f'作者: {Settings.APP_AUTHOR}')
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 停止正在进行的计算
        self.stop_calculation()
        
        self.logger.info("程序退出")
        event.accept()

    def connect_language_signals(self):
        """连接语言相关信号"""
        self.language_manager.language_changed.connect(self.on_language_changed)

    def change_language(self, language_code: str):
        """切换语言"""
        if self.language_manager.set_language(language_code):
            self.logger.info(f"语言已切换到: {language_code}")

    def on_language_changed(self, language_code: str):
        """语言改变处理"""
        self.update_ui_language()

    def update_ui_language(self):
        """更新UI语言"""
        # 更新窗口标题
        self.setWindowTitle(f"{tr('app_title')} v{Settings.APP_VERSION}")

        # 更新标签页文本
        if hasattr(self, 'tab_widget'):
            self.tab_widget.setTabText(0, tr('tab_basic'))
            self.tab_widget.setTabText(1, tr('tab_advanced'))
            self.tab_widget.setTabText(2, tr('tab_output'))
            self.tab_widget.setTabText(3, tr('tab_visualization'))
            self.tab_widget.setTabText(4, tr('tab_expert'))

            # 更新工具提示
            self.tab_widget.setTabToolTip(0, tr('tooltip_basic_tab', "设置目标核、入射粒子和基本计算参数"))
            self.tab_widget.setTabToolTip(1, tr('tooltip_advanced_tab', "配置物理模型和高级计算选项"))
            self.tab_widget.setTabToolTip(2, tr('tooltip_output_tab', "控制输出文件和数据格式"))
            self.tab_widget.setTabToolTip(3, tr('tooltip_viz_tab', "查看和分析计算结果"))
            self.tab_widget.setTabToolTip(4, tr('tooltip_expert_tab', "直接编辑TALYS输入文件和高级选项"))

        # 更新状态栏
        if hasattr(self, 'status_bar'):
            self.status_bar.showMessage(tr('status_ready'))

        if hasattr(self, 'talys_status'):
            self.talys_status.setText(f"TALYS: {tr('status_disconnected', '未连接')}")

        # 通知所有标签页更新语言
        if hasattr(self, 'basic_tab'):
            self.basic_tab.update_language()
        if hasattr(self, 'advanced_tab'):
            self.advanced_tab.update_language()
        if hasattr(self, 'output_tab'):
            self.output_tab.update_language()
        if hasattr(self, 'visualization_tab'):
            self.visualization_tab.update_language()
        if hasattr(self, 'expert_tab'):
            self.expert_tab.update_language()
