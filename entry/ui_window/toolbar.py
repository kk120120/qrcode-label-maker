"""
L1 入口层 - 工具栏
功能：提供添加对象的工具栏
文件：entry/ui_window/toolbar.py
"""
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel

class DesignerToolbar(QWidget):
    """设计器工具栏"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 0)
        self.setLayout(self.layout)
        
        # 二维码按钮
        self.qr_button = QPushButton("矩形QR对象")
        self.qr_button.setFixedSize(100, 40)
        self.layout.addWidget(self.qr_button)
        
        # 文本按钮
        self.text_button = QPushButton("多行文本对象")
        self.text_button.setFixedSize(100, 40)
        self.layout.addWidget(self.text_button)
        
        # 预留按钮
        for i in range(3):
            btn = QPushButton(f"预留{i+1}")
            btn.setFixedSize(80, 40)
            btn.setEnabled(False)
            self.layout.addWidget(btn)
        
        # 预览按钮
        self.preview_button = QPushButton("预览")
        self.preview_button.setFixedSize(80, 40)
        self.layout.addWidget(self.preview_button)
        
        self.layout.addStretch()
