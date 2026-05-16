"""
L1 入口层 - 批量导出对话框
功能：提供批量导出对话框，包含进度显示
文件：entry/ui_window/dialog/batch_export_dialog.py
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel,
    QLineEdit, QPushButton, QRadioButton, QButtonGroup, QFileDialog,
    QProgressBar
)
from PyQt5.QtCore import Qt


class BatchExportDialog(QDialog):
    """批量导出对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("批量导出")
        self.setGeometry(100, 100, 600, 350)
        self._canceled = False
        self._completed = False
        
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # 格式选择
        format_group = QGroupBox("导出格式")
        format_layout = QVBoxLayout()
        format_group.setLayout(format_layout)
        
        self.format_group = QButtonGroup()
        
        self.png_radio = QRadioButton("PNG - 每张标签单独导出为PNG文件")
        self.png_radio.setChecked(True)
        self.pdf_radio = QRadioButton("PDF - 将所有标签合并到一个PDF文件")
        
        self.format_group.addButton(self.png_radio)
        self.format_group.addButton(self.pdf_radio)
        
        format_layout.addWidget(self.png_radio)
        format_layout.addWidget(self.pdf_radio)
        
        # 目标文件夹
        folder_layout = QHBoxLayout()
        self.folder_label = QLabel("目标文件夹:")
        self.folder_input = QLineEdit()
        self.folder_button = QPushButton("浏览")
        
        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(self.folder_button)
        
        # 进度区域 - 初始隐藏
        self.progress_widget = QGroupBox("导出进度")
        self.progress_layout = QVBoxLayout()
        self.progress_widget.setLayout(self.progress_layout)
        
        self.status_label = QLabel("正在导出中...")
        self.status_label.setAlignment(Qt.AlignCenter)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        
        self.progress_layout.addWidget(self.status_label)
        self.progress_layout.addWidget(self.progress_bar)
        self.progress_widget.setVisible(False)
        
        # 按钮
        self.button_layout = QHBoxLayout()
        self.start_button = QPushButton("开始")
        self.ok_button = QPushButton("确认")
        self.cancel_button = QPushButton("取消")
        
        self.ok_button.setVisible(False)
        
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)
        
        self.layout.addWidget(format_group)
        self.layout.addLayout(folder_layout)
        self.layout.addWidget(self.progress_widget)
        self.layout.addStretch()
        self.layout.addLayout(self.button_layout)
        
        # 信号连接
        self.folder_button.clicked.connect(self.select_folder)
        self.cancel_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.accept)
    
    def get_selected_format(self):
        """获取选中的导出格式"""
        if self.png_radio.isChecked():
            return "png"
        elif self.pdf_radio.isChecked():
            return "pdf"
        return "png"
    
    def select_folder(self):
        """选择文件夹"""
        folder = QFileDialog.getExistingDirectory(self, "选择目标文件夹", "d:/")
        if folder:
            self.folder_input.setText(folder)
    
    def start_export(self):
        """开始导出，显示进度区域"""
        self.start_button.setVisible(False)
        self.png_radio.setEnabled(False)
        self.pdf_radio.setEnabled(False)
        self.folder_button.setEnabled(False)
        self.progress_widget.setVisible(True)
        self.status_label.setText("正在导出中...")
        self.progress_bar.setValue(0)
    
    def update_progress(self, current: int, total: int):
        """更新进度"""
        if total > 0:
            progress = int((current / total) * 100)
            self.progress_bar.setValue(progress)
            self.status_label.setText(f"正在导出... {current}/{total}")
    
    def set_completed(self, success: bool, message: str):
        """设置导出完成"""
        self._completed = True
        if success:
            self.status_label.setText("导出完成！")
        else:
            self.status_label.setText(f"导出失败: {message}")
        self.progress_bar.setValue(100)
        self.ok_button.setVisible(True)
        self.cancel_button.setVisible(False)
    
    def is_canceled(self) -> bool:
        """检查是否已取消"""
        return self._canceled