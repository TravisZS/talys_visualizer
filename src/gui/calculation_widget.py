"""
计算控制组件
负责管理TALYS计算的执行、进度显示和结果处理
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from core.talys_interface import TalysInterface, TalysCalculationError, TalysInterfaceError
from utils.logger import LoggerMixin

class CalculationWorker(QThread, LoggerMixin):
    """TALYS计算工作线程"""
    
    # 定义信号
    calculation_started = pyqtSignal()
    calculation_finished = pyqtSignal(dict)  # 计算完成，传递结果
    calculation_failed = pyqtSignal(str)     # 计算失败，传递错误信息
    progress_updated = pyqtSignal(str)       # 进度更新，传递状态信息
    
    def __init__(self, parameters: dict):
        super().__init__()
        self.parameters = parameters
        self.talys_interface = None
        self._is_cancelled = False
    
    def run(self):
        """运行计算"""
        try:
            self.calculation_started.emit()
            self.progress_updated.emit("初始化TALYS接口...")
            
            # 创建TALYS接口
            self.talys_interface = TalysInterface()
            
            self.progress_updated.emit("生成输入文件...")
            
            # 运行计算
            self.progress_updated.emit("运行TALYS计算...")
            results = self.talys_interface.run_calculation(self.parameters)
            
            if not self._is_cancelled:
                self.progress_updated.emit("计算完成")
                self.calculation_finished.emit(results)
            
        except TalysCalculationError as e:
            if not self._is_cancelled:
                self.logger.error(f"TALYS计算失败: {e}")
                self.calculation_failed.emit(f"计算失败: {e}")
        except TalysInterfaceError as e:
            if not self._is_cancelled:
                self.logger.error(f"TALYS接口错误: {e}")
                self.calculation_failed.emit(f"接口错误: {e}")
        except Exception as e:
            if not self._is_cancelled:
                self.logger.error(f"未知错误: {e}")
                self.calculation_failed.emit(f"未知错误: {e}")
        finally:
            # 清理资源
            if self.talys_interface:
                self.talys_interface.cleanup_temp_directory()
    
    def cancel(self):
        """取消计算"""
        self._is_cancelled = True
        if self.talys_interface:
            self.talys_interface.stop_calculation()
        self.progress_updated.emit("计算已取消")

class CalculationControlWidget(QWidget, LoggerMixin):
    """计算控制组件"""
    
    # 定义信号
    calculation_completed = pyqtSignal(dict)  # 计算完成信号
    
    def __init__(self):
        super().__init__()
        self.current_worker = None
        self.current_parameters = {}
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 标题
        title = QLabel("计算控制")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)
        
        # 参数预览区域
        self.create_parameter_preview(layout)
        
        # 控制按钮区域
        self.create_control_buttons(layout)
        
        # 进度显示区域
        self.create_progress_area(layout)
        
        # 结果摘要区域
        self.create_result_summary(layout)
        
        layout.addStretch()
    
    def create_parameter_preview(self, layout):
        """创建参数预览区域"""
        group = QGroupBox("当前参数")
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
        
        group_layout = QVBoxLayout(group)
        
        # 参数显示标签
        self.parameter_display = QLabel("未设置参数")
        self.parameter_display.setStyleSheet("""
            QLabel {
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                border-radius: 3px;
                padding: 10px;
                font-family: monospace;
            }
        """)
        self.parameter_display.setWordWrap(True)
        self.parameter_display.setMinimumHeight(100)
        
        group_layout.addWidget(self.parameter_display)
        layout.addWidget(group)
    
    def create_control_buttons(self, layout):
        """创建控制按钮"""
        button_layout = QHBoxLayout()
        
        # 运行按钮
        self.run_button = QPushButton("运行计算")
        self.run_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            QPushButton:pressed {
                background-color: #229954;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.run_button.clicked.connect(self.start_calculation)
        self.run_button.setEnabled(False)
        
        # 停止按钮
        self.stop_button = QPushButton("停止计算")
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.stop_button.clicked.connect(self.stop_calculation)
        self.stop_button.setEnabled(False)
        
        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
    
    def create_progress_area(self, layout):
        """创建进度显示区域"""
        group = QGroupBox("计算进度")
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
        
        group_layout = QVBoxLayout(group)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # 不确定进度
        self.progress_bar.setVisible(False)
        group_layout.addWidget(self.progress_bar)
        
        # 状态标签
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        group_layout.addWidget(self.status_label)
        
        layout.addWidget(group)
    
    def create_result_summary(self, layout):
        """创建结果摘要区域"""
        group = QGroupBox("计算结果摘要")
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
        
        group_layout = QVBoxLayout(group)
        
        # 结果显示标签
        self.result_display = QLabel("暂无计算结果")
        self.result_display.setStyleSheet("""
            QLabel {
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                border-radius: 3px;
                padding: 10px;
                font-family: monospace;
            }
        """)
        self.result_display.setWordWrap(True)
        self.result_display.setMinimumHeight(80)
        
        group_layout.addWidget(self.result_display)
        layout.addWidget(group)
    
    def update_parameters(self, parameters: dict):
        """更新参数显示"""
        self.current_parameters = parameters.copy()
        
        # 格式化参数显示
        param_text = []
        param_text.append(f"入射粒子: {parameters.get('projectile', 'N/A')}")
        param_text.append(f"目标核: {parameters.get('element', 'N/A')}-{parameters.get('mass', 'N/A')}")
        param_text.append(f"能量: {parameters.get('energy', 'N/A')} MeV")
        
        # 输出选项
        output_options = []
        if parameters.get('channels', False):
            output_options.append('反应道')
        if parameters.get('outspectra', False):
            output_options.append('能谱')
        if parameters.get('outangle', False):
            output_options.append('角分布')
        if parameters.get('outlevels', False):
            output_options.append('能级')
        
        if output_options:
            param_text.append(f"输出选项: {', '.join(output_options)}")
        else:
            param_text.append("输出选项: 基础输出")
        
        self.parameter_display.setText('\n'.join(param_text))
        
        # 启用运行按钮
        self.run_button.setEnabled(True)
    
    def start_calculation(self):
        """开始计算"""
        if not self.current_parameters:
            QMessageBox.warning(self, "警告", "请先设置计算参数")
            return
        
        self.logger.info("开始TALYS计算")
        
        # 创建工作线程
        self.current_worker = CalculationWorker(self.current_parameters)
        
        # 连接信号
        self.current_worker.calculation_started.connect(self.on_calculation_started)
        self.current_worker.calculation_finished.connect(self.on_calculation_finished)
        self.current_worker.calculation_failed.connect(self.on_calculation_failed)
        self.current_worker.progress_updated.connect(self.on_progress_updated)
        
        # 启动线程
        self.current_worker.start()
    
    def stop_calculation(self):
        """停止计算"""
        if self.current_worker and self.current_worker.isRunning():
            self.logger.info("停止TALYS计算")
            self.current_worker.cancel()
            self.current_worker.wait(5000)  # 等待5秒
            if self.current_worker.isRunning():
                self.current_worker.terminate()
    
    def on_calculation_started(self):
        """计算开始处理"""
        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.status_label.setText("计算进行中...")
        self.result_display.setText("计算进行中，请稍候...")
    
    def on_calculation_finished(self, results: dict):
        """计算完成处理"""
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.status_label.setText("计算完成")
        
        # 显示结果摘要
        summary_text = []
        summary_text.append(f"计算耗时: {results.get('calculation_time', 0):.2f} 秒")
        summary_text.append(f"输出文件数: {len(results.get('output_files', []))}")
        
        if 'total_cross_section' in results:
            xs_data = results['total_cross_section']
            data_points = len(xs_data.get('energy', []))
            summary_text.append(f"截面数据点: {data_points}")
        
        if results.get('output_files'):
            summary_text.append("生成文件:")
            for file in results['output_files'][:5]:  # 只显示前5个
                summary_text.append(f"  • {file}")
            if len(results['output_files']) > 5:
                summary_text.append(f"  ... 还有 {len(results['output_files']) - 5} 个文件")
        
        self.result_display.setText('\n'.join(summary_text))
        
        # 发出计算完成信号
        self.calculation_completed.emit(results)
        
        self.logger.info("TALYS计算完成")
    
    def on_calculation_failed(self, error_message: str):
        """计算失败处理"""
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.status_label.setText("计算失败")
        self.result_display.setText(f"计算失败:\n{error_message}")
        
        # 显示错误对话框
        QMessageBox.critical(self, "计算失败", f"TALYS计算失败:\n\n{error_message}")
        
        self.logger.error(f"TALYS计算失败: {error_message}")
    
    def on_progress_updated(self, message: str):
        """进度更新处理"""
        self.status_label.setText(message)
