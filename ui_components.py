# Python 批量二维码标签生成器
# Copyright (C) 2026
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QLineEdit, QComboBox, QCheckBox,
    QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QSpinBox,
    QDoubleSpinBox, QColorDialog, QTableWidget, QTableWidgetItem,
    QFileDialog, QProgressDialog, QMessageBox, QScrollArea, QDialog,
    QRadioButton
)
from PyQt5.QtWidgets import QButtonGroup
from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
import os

class DrawToolBar(QWidget):
    """绘制工具栏"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout()
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
        for i in range(4):
            btn = QPushButton(f"预留{i+1}")
            btn.setFixedSize(80, 40)
            btn.setEnabled(False)
            self.layout.addWidget(btn)
        
        self.layout.addStretch()

class PropertyPanel(QWidget):
    """属性面板"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # 对象信息标签
        self.object_info_label = QLabel("未选择对象")
        self.object_info_label.setStyleSheet("font-weight: bold; color: #4CAF50;")
        self.layout.addWidget(self.object_info_label)
        
        # 基本属性
        self.basic_group = QGroupBox("基本属性")
        self.basic_layout = QGridLayout()
        self.basic_group.setLayout(self.basic_layout)
        
        self.x_label = QLabel("X坐标 (mm):")
        self.x_input = QDoubleSpinBox()
        self.x_input.setRange(0, 200)
        self.x_input.setSingleStep(0.1)
        
        self.y_label = QLabel("Y坐标 (mm):")
        self.y_input = QDoubleSpinBox()
        self.y_input.setRange(0, 200)
        self.y_input.setSingleStep(0.1)
        
        self.width_label = QLabel("宽度 (mm):")
        self.width_input = QDoubleSpinBox()
        self.width_input.setRange(2, 200)
        self.width_input.setSingleStep(0.1)
        
        self.height_label = QLabel("高度 (mm):")
        self.height_input = QDoubleSpinBox()
        self.height_input.setRange(2, 200)
        self.height_input.setSingleStep(0.1)
        
        self.basic_layout.addWidget(self.x_label, 0, 0)
        self.basic_layout.addWidget(self.x_input, 0, 1)
        self.basic_layout.addWidget(self.y_label, 1, 0)
        self.basic_layout.addWidget(self.y_input, 1, 1)
        self.basic_layout.addWidget(self.width_label, 2, 0)
        self.basic_layout.addWidget(self.width_input, 2, 1)
        self.basic_layout.addWidget(self.height_label, 3, 0)
        self.basic_layout.addWidget(self.height_input, 3, 1)
        
        self.layout.addWidget(self.basic_group)
        
        # 二维码属性
        self.qr_group = QGroupBox("二维码属性")
        self.qr_layout = QGridLayout()
        self.qr_group.setLayout(self.qr_layout)
        
        self.qr_version_label = QLabel("尺寸:")
        self.qr_version_combo = QComboBox()
        
        self.error_correction_label = QLabel("纠错级别:")
        self.error_correction_combo = QComboBox()
        self.error_correction_combo.addItems(["L", "M", "Q", "H"])
        
        # 容量显示
        self.capacity_group = QGroupBox("数据容量")
        self.capacity_layout = QGridLayout()
        self.capacity_group.setLayout(self.capacity_layout)
        
        self.numeric_label = QLabel("数字模式:")
        self.numeric_value = QLabel("0")
        self.alphanumeric_label = QLabel("字母数字模式:")
        self.alphanumeric_value = QLabel("0")
        self.byte_label = QLabel("字节模式:")
        self.byte_value = QLabel("0")
        self.kanji_label = QLabel("汉字模式:")
        self.kanji_value = QLabel("0")
        
        self.capacity_layout.addWidget(self.numeric_label, 0, 0)
        self.capacity_layout.addWidget(self.numeric_value, 0, 1)
        self.capacity_layout.addWidget(self.alphanumeric_label, 1, 0)
        self.capacity_layout.addWidget(self.alphanumeric_value, 1, 1)
        self.capacity_layout.addWidget(self.byte_label, 2, 0)
        self.capacity_layout.addWidget(self.byte_value, 2, 1)
        self.capacity_layout.addWidget(self.kanji_label, 3, 0)
        self.capacity_layout.addWidget(self.kanji_value, 3, 1)
        
        self.content_label = QLabel("内容:")
        self.content_input = QLineEdit()
        
        self.qr_batch_checkbox = QCheckBox("批量生成")
        self.qr_csv_column_label = QLabel("关联导入数据列:")
        self.qr_csv_column_combo = QComboBox()
        
        self.qr_layout.addWidget(self.qr_version_label, 0, 0)
        self.qr_layout.addWidget(self.qr_version_combo, 0, 1)
        self.qr_layout.addWidget(self.error_correction_label, 1, 0)
        self.qr_layout.addWidget(self.error_correction_combo, 1, 1)
        self.qr_layout.addWidget(self.capacity_group, 2, 0, 1, 2)
        self.qr_layout.addWidget(self.content_label, 3, 0)
        self.qr_layout.addWidget(self.content_input, 3, 1)
        self.qr_layout.addWidget(self.qr_batch_checkbox, 4, 0)
        self.qr_layout.addWidget(self.qr_csv_column_label, 5, 0)
        self.qr_layout.addWidget(self.qr_csv_column_combo, 5, 1)
        
        self.layout.addWidget(self.qr_group)
        
        # 文本属性
        self.text_group = QGroupBox("文本属性")
        self.text_layout = QGridLayout()
        self.text_group.setLayout(self.text_layout)
        
        self.font_label = QLabel("字体:")
        self.font_combo = QComboBox()
        self.font_combo.addItems(["Arial", "SimHei", "Microsoft YaHei", "Times New Roman"])
        
        self.font_size_label = QLabel("大小 (mm):")
        self.font_size_input = QDoubleSpinBox()
        self.font_size_input.setRange(1, 20)
        self.font_size_input.setSingleStep(0.5)
        
        self.font_style_label = QLabel("样式:")
        self.bold_checkbox = QCheckBox("粗体")
        self.italic_checkbox = QCheckBox("斜体")
        self.underline_checkbox = QCheckBox("下划线")
        
        self.color_label = QLabel("颜色:")
        self.color_button = QPushButton("选择")
        self.color_preview = QLabel()
        self.color_preview.setFixedSize(30, 20)
        self.color_preview.setStyleSheet("background-color: #000000;")
        
        self.text_content_label = QLabel("内容:")
        self.text_content_input = QLineEdit()
        
        self.text_batch_checkbox = QCheckBox("批量生成")
        self.text_csv_column_label = QLabel("关联导入数据列:")
        self.text_csv_column_combo = QComboBox()
        
        self.text_layout.addWidget(self.font_label, 0, 0)
        self.text_layout.addWidget(self.font_combo, 0, 1)
        self.text_layout.addWidget(self.font_size_label, 1, 0)
        self.text_layout.addWidget(self.font_size_input, 1, 1)
        self.text_layout.addWidget(self.font_style_label, 2, 0)
        style_layout = QHBoxLayout()
        style_layout.addWidget(self.bold_checkbox)
        style_layout.addWidget(self.italic_checkbox)
        style_layout.addWidget(self.underline_checkbox)
        self.text_layout.addLayout(style_layout, 2, 1)
        self.text_layout.addWidget(self.color_label, 3, 0)
        color_layout = QHBoxLayout()
        color_layout.addWidget(self.color_button)
        color_layout.addWidget(self.color_preview)
        self.text_layout.addLayout(color_layout, 3, 1)
        self.text_layout.addWidget(self.text_content_label, 4, 0)
        self.text_layout.addWidget(self.text_content_input, 4, 1)
        self.text_layout.addWidget(self.text_batch_checkbox, 5, 0, 1, 2)
        self.text_layout.addWidget(self.text_csv_column_label, 6, 0)
        self.text_layout.addWidget(self.text_csv_column_combo, 6, 1)
        
        self.layout.addWidget(self.text_group)
        
        # 默认隐藏文本属性面板
        self.text_group.setVisible(False)
        
        # 保存按钮
        self.save_button = QPushButton("保存")
        self.layout.addWidget(self.save_button)
        
        self.layout.addStretch()
    
    def show_qr_properties(self, show=True):
        """显示/隐藏二维码属性"""
        self.qr_group.setVisible(show)
        self.text_group.setVisible(not show)
    
    def show_text_properties(self, show=True):
        """显示/隐藏文本属性"""
        self.text_group.setVisible(show)
        self.qr_group.setVisible(not show)
    
    def update_qr_csv_columns(self, columns):
        """更新二维码CSV列选择"""
        self.qr_csv_column_combo.clear()
        self.qr_csv_column_combo.addItems(columns)
    
    def update_text_csv_columns(self, columns):
        """更新文本CSV列选择"""
        self.text_csv_column_combo.clear()
        # 添加一个空字符串选项，用于表示未选择任何列
        self.text_csv_column_combo.addItem("")
        self.text_csv_column_combo.addItems(columns)
    
    def update_capacity(self, numeric, alphanumeric, byte, kanji):
        """更新容量显示"""
        self.numeric_value.setText(str(numeric))
        self.alphanumeric_value.setText(str(alphanumeric))
        self.byte_value.setText(str(byte))
        self.kanji_value.setText(str(kanji))

class BasicSettingsDialog(QDialog):
    """基础设置对话框"""
    def __init__(self, parent=None, label_size=None, dpi=None, grid_color=None):
        super().__init__(parent)
        self.setWindowTitle("基础设置")
        self.setGeometry(200, 200, 400, 300)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 标签尺寸
        size_group = QGroupBox("标签尺寸 (mm)")
        size_layout = QGridLayout()
        size_group.setLayout(size_layout)
        
        self.width_label = QLabel("宽度:")
        self.width_input = QSpinBox()
        self.width_input.setRange(10, 300)
        self.width_input.setSingleStep(1)
        
        self.height_label = QLabel("高度:")
        self.height_input = QSpinBox()
        self.height_input.setRange(10, 300)
        self.height_input.setSingleStep(1)
        
        self.corner_label = QLabel("圆角:")
        self.corner_input = QSpinBox()
        self.corner_input.setRange(0, 50)
        self.corner_input.setSingleStep(1)
        
        size_layout.addWidget(self.width_label, 0, 0)
        size_layout.addWidget(self.width_input, 0, 1)
        size_layout.addWidget(self.height_label, 1, 0)
        size_layout.addWidget(self.height_input, 1, 1)
        size_layout.addWidget(self.corner_label, 2, 0)
        size_layout.addWidget(self.corner_input, 2, 1)
        
        # DPI设置
        dpi_group = QGroupBox("DPI设置")
        dpi_layout = QGridLayout()
        dpi_group.setLayout(dpi_layout)
        
        self.dpi_label = QLabel("DPI:")
        self.dpi_input = QSpinBox()
        self.dpi_input.setRange(96, 600)
        self.dpi_input.setSingleStep(1)
        
        dpi_layout.addWidget(self.dpi_label, 0, 0)
        dpi_layout.addWidget(self.dpi_input, 0, 1)
        
        # 网格设置
        grid_group = QGroupBox("网格设置")
        grid_layout = QGridLayout()
        grid_group.setLayout(grid_layout)
        
        self.grid_color_label = QLabel("网格颜色:")
        self.grid_color_button = QPushButton("选择颜色")
        self.grid_color = grid_color if grid_color else QColor(180, 180, 180)  # 默认为比淡灰色深一点的颜色
        
        # 设置按钮样式以显示当前颜色
        def update_color_button():
            style = f"background-color: {self.grid_color.name()}"
            self.grid_color_button.setStyleSheet(style)
        
        update_color_button()
        
        def choose_color():
            color = QColorDialog.getColor(self.grid_color, self, "选择网格颜色")
            if color.isValid():
                self.grid_color = color
                update_color_button()
        
        self.grid_color_button.clicked.connect(choose_color)
        
        grid_layout.addWidget(self.grid_color_label, 0, 0)
        grid_layout.addWidget(self.grid_color_button, 0, 1)
        
        # 按钮
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("确定")
        self.cancel_button = QPushButton("取消")
        
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addWidget(size_group)
        layout.addWidget(dpi_group)
        layout.addWidget(grid_group)
        layout.addLayout(button_layout)
        
        # 初始化值
        if label_size:
            self.width_input.setValue(label_size['width'])
            self.height_input.setValue(label_size['height'])
            self.corner_input.setValue(label_size['corner_radius'])
        if dpi:
            self.dpi_input.setValue(dpi)
        
        # 信号连接
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
    
    def get_settings(self):
        """获取设置值"""
        return {
            'width': self.width_input.value(),
            'height': self.height_input.value(),
            'corner_radius': self.corner_input.value(),
            'dpi': self.dpi_input.value(),
            'grid_color': self.grid_color.name()
        }

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

class BatchExportDialog(QDialog):
    """批量导出对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("批量导出")
        self.setGeometry(100, 100, 600, 350)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 格式选择
        format_group = QGroupBox("导出格式")
        format_layout = QVBoxLayout()
        format_group.setLayout(format_layout)
        
        self.format_group = QButtonGroup()
        
        self.png_radio = QRadioButton("PNG - 每张标签单独导出为PNG文件")
        self.png_radio.setChecked(True)  # 默认选中PNG
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
        
        # 进度条 - 初始化为None，在点击开始后创建
        self.progress = None
        
        # 按钮
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("开始")
        self.cancel_button = QPushButton("取消")
        
        button_layout.addStretch()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addWidget(format_group)
        layout.addLayout(folder_layout)
        layout.addStretch()
        layout.addLayout(button_layout)
        
        # 信号连接
        self.folder_button.clicked.connect(self.select_folder)
        self.cancel_button.clicked.connect(self.reject)
    
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
