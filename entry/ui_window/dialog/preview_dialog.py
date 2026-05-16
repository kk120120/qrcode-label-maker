"""
L1 入口层 - 预览对话框
功能：显示标签PNG预览
文件：entry/ui_window/dialog/preview_dialog.py
"""
import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QWidget, QSpinBox
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class PageSpinBox(QSpinBox):
    """页码输入框 - 拦截回车键防止传播到其他按钮"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.preview_callback = None
    
    def keyPressEvent(self, event):
        """拦截回车键，只刷新预览，不传播事件"""
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            if self.preview_callback:
                self.preview_callback()
            event.accept()
            return
        super().keyPressEvent(event)


class PreviewDialog(QDialog):
    """标签预览对话框"""
    def __init__(self, temp_file: str, parent=None, total_rows=0, refresh_callback=None):
        super().__init__(parent)
        self.temp_file = temp_file
        self.total_rows = total_rows
        self.refresh_callback = refresh_callback
        self.current_row = 1
        self.setWindowTitle("标签预览")
        self.setMinimumSize(800, 600)
        
        self.init_ui()
        self.load_image()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        scroll.setWidget(self.image_label)
        
        # 页码控件
        page_layout = QHBoxLayout()
        
        page_label = QLabel("页码:")
        self.page_spinbox = PageSpinBox()
        self.page_spinbox.setMinimum(1)
        self.page_spinbox.setMaximum(max(1, self.total_rows))
        self.page_spinbox.setValue(1)
        self.page_spinbox.setEnabled(self.total_rows > 0)
        # 回车时刷新预览
        self.page_spinbox.preview_callback = self.on_page_changed
        
        total_label = QLabel(f"/ {self.total_rows}" if self.total_rows > 0 else "/ 0")
        
        page_layout.addWidget(page_label)
        page_layout.addWidget(self.page_spinbox)
        page_layout.addWidget(total_label)
        page_layout.addStretch()
        
        # 关闭按钮
        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.close_and_cleanup)
        
        layout.addLayout(page_layout)
        layout.addWidget(scroll)
        layout.addWidget(close_button)
    
    def on_page_changed(self):
        """页码改变事件"""
        if self.refresh_callback:
            new_row = self.page_spinbox.value()
            if new_row != self.current_row:
                self.current_row = new_row
                self.refresh_callback(new_row - 1, self.temp_file)
                self.load_image()
        # 刷新后保持焦点在页码控件
        self.page_spinbox.setFocus()
    
    def update_image(self, temp_file: str):
        """更新图像"""
        self.temp_file = temp_file
        self.load_image()
    
    def load_image(self):
        """加载并显示图像"""
        if os.path.exists(self.temp_file):
            pixmap = QPixmap(self.temp_file)
            # 缩放以适应窗口，但保持宽高比
            scaled_pixmap = pixmap.scaled(
                780, 550,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
    
    def close_and_cleanup(self):
        """关闭对话框并清理临时文件"""
        if os.path.exists(self.temp_file):
            try:
                os.remove(self.temp_file)
            except:
                pass
        self.accept()
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        self.close_and_cleanup()
        event.accept()
