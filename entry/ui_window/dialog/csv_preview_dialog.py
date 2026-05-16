"""
L1 入口层 - CSV预览对话框
功能：提供CSV数据预览对话框
文件：entry/ui_window/dialog/csv_preview_dialog.py
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QSpinBox, QPushButton, QTableWidget, QTableWidgetItem
)

class CSVPreviewDialog(QDialog):
    """CSV预览对话框"""
    def __init__(self, csv_handler, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CSV预览")
        self.setGeometry(100, 100, 800, 500)
        
        self.csv_handler = csv_handler
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 控制区
        control_layout = QHBoxLayout()
        self.start_row_label = QLabel("开始行:")
        self.start_row_input = QSpinBox()
        self.start_row_input.setMinimum(1)
        self.start_row_input.setMaximum(csv_handler.get_row_count())
        self.start_row_input.setValue(2)
        self.preview_button = QPushButton("预览")
        
        control_layout.addWidget(self.start_row_label)
        control_layout.addWidget(self.start_row_input)
        control_layout.addWidget(self.preview_button)
        control_layout.addStretch()
        
        # 表格
        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        # 按钮
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("确认")
        self.cancel_button = QPushButton("取消")
        
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(control_layout)
        layout.addWidget(self.table)
        layout.addLayout(button_layout)
        
        # 初始预览
        self.update_preview()
        
        # 信号连接
        self.preview_button.clicked.connect(self.update_preview)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
    
    def update_preview(self):
        """更新预览数据"""
        start_row = self.start_row_input.value()
        data = self.csv_handler.get_preview_data(start_row, 10)
        
        if data is not None:
            # 清空表格并重新设置
            self.table.clear()
            self.table.setRowCount(len(data))
            self.table.setColumnCount(len(data.columns))
            self.table.setHorizontalHeaderLabels(data.columns)
            
            # 更新表格内容和行号
            for i, (index, row) in enumerate(data.iterrows()):
                # 设置行号为实际的数据行号
                self.table.setVerticalHeaderItem(i, QTableWidgetItem(str(index + 1)))
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.table.setItem(i, j, item)
        else:
            # 清空表格
            self.table.clear()
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
