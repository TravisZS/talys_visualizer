"""
计算进度对话框
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from utils.i18n import tr
from core.talys_interface import TalysInterface, TalysCalculationError, TalysInterfaceError

class CalculationWorker(QThread):
    """计算工作线程"""
    
    # 信号定义
    progress_updated = pyqtSignal(str)  # 进度更新
    calculation_finished = pyqtSignal(dict)  # 计算完成
    calculation_failed = pyqtSignal(str)  # 计算失败
    
    def __init__(self, parameters):
        super().__init__()
        self.parameters = parameters
        self.talys_interface = None
        self._is_cancelled = False
        
    def run(self):
        """运行计算"""
        try:
            self.progress_updated.emit("初始化TALYS接口...")
            
            # 创建TALYS接口
            self.talys_interface = TalysInterface()
            
            if self._is_cancelled:
                return
                
            self.progress_updated.emit("验证参数...")
            
            # 验证参数
            is_valid, message = self.talys_interface.validate_parameters(self.parameters)
            if not is_valid:
                self.calculation_failed.emit(f"参数验证失败: {message}")
                return
            
            if self._is_cancelled:
                return
                
            self.progress_updated.emit("生成输入文件...")
            
            # 运行计算
            self.progress_updated.emit("运行TALYS计算...")
            results = self.talys_interface.run_calculation(self.parameters)
            
            if not self._is_cancelled:
                self.progress_updated.emit("计算完成")
                self.calculation_finished.emit(results)
                
        except TalysCalculationError as e:
            if not self._is_cancelled:
                self.calculation_failed.emit(f"计算失败: {str(e)}")
        except TalysInterfaceError as e:
            if not self._is_cancelled:
                self.calculation_failed.emit(f"接口错误: {str(e)}")
        except Exception as e:
            if not self._is_cancelled:
                self.calculation_failed.emit(f"未知错误: {str(e)}")
        finally:
            # 清理资源
            if self.talys_interface:
                self.talys_interface.cleanup_temp_directory()
                
    def cancel(self):
        """取消计算"""
        self._is_cancelled = True
        if self.talys_interface:
            self.talys_interface.stop_calculation()

class CalculationProgressDialog(QDialog):
    """计算进度对话框"""
    
    # 信号定义
    calculation_completed = pyqtSignal(dict)  # 计算完成信号
    
    def __init__(self, parameters, parent=None):
        super().__init__(parent)
        self.parameters = parameters
        self.worker = None
        self.init_ui()
        self.start_calculation()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle(tr('calculation_progress_title', "TALYS计算进度"))
        self.setModal(True)
        self.setFixedSize(400, 200)
        
        # 主布局
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title = QLabel("正在运行TALYS计算...")
        title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        layout.addWidget(title)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # 不确定进度
        layout.addWidget(self.progress_bar)
        
        # 状态标签
        self.status_label = QLabel("初始化...")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.status_label)
        
        # 参数显示
        params_text = self.format_parameters()
        params_label = QLabel(params_text)
        params_label.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 8px;
                font-family: monospace;
                font-size: 10px;
            }
        """)
        layout.addWidget(params_label)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.cancel_calculation)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
    def format_parameters(self):
        """格式化参数显示"""
        lines = []
        lines.append(f"入射粒子: {self.parameters.get('projectile', 'N/A')}")
        lines.append(f"目标核: {self.parameters.get('element', 'N/A')}-{self.parameters.get('mass', 'N/A')}")
        lines.append(f"入射能量: {self.parameters.get('energy', 'N/A')} MeV")
        return '\n'.join(lines)
        
    def start_calculation(self):
        """开始计算"""
        self.worker = CalculationWorker(self.parameters)
        
        # 连接信号
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.calculation_finished.connect(self.on_calculation_finished)
        self.worker.calculation_failed.connect(self.on_calculation_failed)
        
        # 启动线程
        self.worker.start()
        
    def update_progress(self, message):
        """更新进度"""
        self.status_label.setText(message)
        
    def on_calculation_finished(self, results):
        """计算完成"""
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(1)
        self.status_label.setText("计算完成！")
        self.cancel_button.setText("关闭")
        
        # 发出完成信号
        self.calculation_completed.emit(results)
        
        # 自动关闭对话框
        QTimer.singleShot(1000, self.accept)
        
    def on_calculation_failed(self, error_message):
        """计算失败"""
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(0)
        self.status_label.setText("计算失败")
        self.cancel_button.setText("关闭")
        
        # 显示错误消息
        QMessageBox.critical(self, "计算失败", error_message)
        self.reject()
        
    def cancel_calculation(self):
        """取消计算"""
        if self.worker and self.worker.isRunning():
            self.status_label.setText("正在取消...")
            self.worker.cancel()
            self.worker.wait(5000)  # 等待最多5秒
        
        self.reject()
        
    def closeEvent(self, event):
        """关闭事件"""
        if self.worker and self.worker.isRunning():
            reply = QMessageBox.question(
                self, "确认", "计算正在进行中，确定要取消吗？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.cancel_calculation()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
