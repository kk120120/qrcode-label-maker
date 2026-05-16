"""
L1 入口层 - 基础设置对话框
功能：提供基础设置对话框
文件：entry/ui_window/dialog/basic_settings_dialog.py
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox,
    QLabel, QSpinBox, QCheckBox, QPushButton, QColorDialog, QComboBox
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

class BasicSettingsDialog(QDialog):
    """基础设置对话框"""
    def __init__(self, parent=None, label_size=None, dpi=None, grid_color=None, show_grid=False, grid_line_style=None):
        super().__init__(parent)
        self.setWindowTitle("基础设置")
        self.setGeometry(200, 200, 400, 350)

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

        self.show_grid_checkbox = QCheckBox("显示网格")
        self.show_grid_checkbox.setChecked(show_grid)

        self.grid_color_label = QLabel("网格颜色:")
        self.grid_color_button = QPushButton("选择颜色")
        self.grid_color = grid_color if grid_color else QColor(0, 255, 0)

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

        self.grid_line_style_label = QLabel("网格线型:")
        self.grid_line_style_combo = QComboBox()
        self.grid_line_style_combo.addItem("实线", Qt.PenStyle.SolidLine)
        self.grid_line_style_combo.addItem("虚线", Qt.PenStyle.DashLine)
        self.grid_line_style_combo.addItem("点线", Qt.PenStyle.DotLine)
        self.grid_line_style_combo.addItem("点划线", Qt.PenStyle.DashDotLine)
        self.grid_line_style_combo.addItem("双点划线", Qt.PenStyle.DashDotDotLine)

        if grid_line_style:
            index = self.grid_line_style_combo.findData(grid_line_style)
            if index >= 0:
                self.grid_line_style_combo.setCurrentIndex(index)
        else:
            self.grid_line_style_combo.setCurrentIndex(1)

        grid_layout.addWidget(self.show_grid_checkbox, 0, 0, 1, 2)
        grid_layout.addWidget(self.grid_color_label, 1, 0)
        grid_layout.addWidget(self.grid_color_button, 1, 1)
        grid_layout.addWidget(self.grid_line_style_label, 2, 0)
        grid_layout.addWidget(self.grid_line_style_combo, 2, 1)

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
            'grid_color': self.grid_color.name(),
            'show_grid': self.show_grid_checkbox.isChecked(),
            'grid_line_style': self.grid_line_style_combo.currentData()
        }
