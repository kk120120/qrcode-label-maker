"""
L1 入口层 - 属性面板
功能：提供对象属性编辑面板
文件：entry/ui_window/property_panel.py
"""
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QLineEdit, QComboBox, QCheckBox,
    QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QDoubleSpinBox,
    QColorDialog, QButtonGroup, QRadioButton, QSizePolicy
)
from PyQt5.QtCore import Qt


class PropertyPanel(QWidget):
    """属性面板"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_layout()
        self._init_object_info()
        self._init_basic_properties()
        self._init_qr_properties()
        self._init_text_properties()
        self._init_save_button()

    def _init_layout(self):
        """初始化布局"""
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(5, 0, 5, 5)
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)
        self.setStyleSheet("""
            PropertyPanel {
                border-left: 1px solid #e0e0e0;
            }
        """)

    def _init_object_info(self):
        """初始化对象信息标签"""
        self.object_info_label = QLabel("未选择对象")
        self.object_info_label.setStyleSheet("font-weight: bold; color: #4CAF50;")
        self.layout.addWidget(self.object_info_label)

    def _init_basic_properties(self):
        """初始化基本属性面板（位置、尺寸）"""
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

    def _init_qr_properties(self):
        """初始化二维码属性面板"""
        self.qr_group = QGroupBox("二维码属性")
        self.qr_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.qr_layout = QGridLayout()
        self.qr_group.setLayout(self.qr_layout)

        self.qr_version_label = QLabel("尺寸:")
        self.qr_version_combo = QComboBox()

        self.error_correction_label = QLabel("纠错级别:")
        self.error_correction_combo = QComboBox()
        self.error_correction_combo.addItems(["L", "M", "Q", "H"])

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
        self.qr_layout.addWidget(self.content_label, 3, 0, 1, 2)
        self.qr_layout.addWidget(self.content_input, 4, 0, 1, 2)
        self.qr_layout.addWidget(self.qr_batch_checkbox, 5, 0)
        self.qr_layout.addWidget(self.qr_csv_column_label, 6, 0, 1, 2)
        self.qr_layout.addWidget(self.qr_csv_column_combo, 7, 0, 1, 2)

        self.layout.addWidget(self.qr_group)

    def _init_text_properties(self):
        """初始化文本属性面板"""
        self.text_group = QGroupBox("文本属性")
        self.text_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
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

        self.text_align_label = QLabel("对齐:")
        self.align_left_button = QRadioButton("左")
        self.align_center_button = QRadioButton("中")
        self.align_right_button = QRadioButton("右")
        self.align_button_group = QButtonGroup()
        self.align_button_group.addButton(self.align_left_button, 0)
        self.align_button_group.addButton(self.align_center_button, 1)
        self.align_button_group.addButton(self.align_right_button, 2)
        self.align_left_button.setChecked(True)

        self.vertical_align_label = QLabel("垂直:")
        self.align_top_button = QRadioButton("上")
        self.align_middle_button = QRadioButton("中")
        self.align_bottom_button = QRadioButton("下")
        self.vertical_align_button_group = QButtonGroup()
        self.vertical_align_button_group.addButton(self.align_top_button, 0)
        self.vertical_align_button_group.addButton(self.align_middle_button, 1)
        self.vertical_align_button_group.addButton(self.align_bottom_button, 2)
        self.align_top_button.setChecked(True)

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
        self.text_layout.addWidget(self.font_style_label, 2, 0, 1, 2)
        self.text_layout.addWidget(self.bold_checkbox, 3, 0, 1, 2)
        self.text_layout.addWidget(self.italic_checkbox, 4, 0, 1, 2)
        self.text_layout.addWidget(self.underline_checkbox, 5, 0, 1, 2)
        self.text_layout.addWidget(self.text_align_label, 6, 0)
        align_layout = QHBoxLayout()
        align_layout.addWidget(self.align_left_button)
        align_layout.addWidget(self.align_center_button)
        align_layout.addWidget(self.align_right_button)
        self.text_layout.addLayout(align_layout, 6, 1)
        self.text_layout.addWidget(self.vertical_align_label, 7, 0)
        vertical_align_layout = QHBoxLayout()
        vertical_align_layout.addWidget(self.align_top_button)
        vertical_align_layout.addWidget(self.align_middle_button)
        vertical_align_layout.addWidget(self.align_bottom_button)
        self.text_layout.addLayout(vertical_align_layout, 7, 1)
        self.text_layout.addWidget(self.color_label, 8, 0)
        color_layout = QHBoxLayout()
        color_layout.addWidget(self.color_button)
        color_layout.addWidget(self.color_preview)
        self.text_layout.addLayout(color_layout, 8, 1)
        self.text_layout.addWidget(self.text_content_label, 9, 0, 1, 2)
        self.text_layout.addWidget(self.text_content_input, 10, 0, 1, 2)
        self.text_layout.addWidget(self.text_batch_checkbox, 11, 0, 1, 2)
        self.text_layout.addWidget(self.text_csv_column_label, 12, 0, 1, 2)
        self.text_layout.addWidget(self.text_csv_column_combo, 13, 0, 1, 2)

        self.layout.addWidget(self.text_group)
        self.text_group.setVisible(False)

    def _init_save_button(self):
        """初始化保存按钮"""
        self.save_button = QPushButton("保存")
        self.layout.addWidget(self.save_button)

    def _set_basic_signals_blocked(self, blocked: bool):
        """设置基本属性控件的信号阻塞状态

        Args:
            blocked: True 阻塞信号，False 恢复信号
        """
        for control in [self.x_input, self.y_input, self.width_input, self.height_input]:
            control.blockSignals(blocked)

    def _set_qr_signals_blocked(self, blocked: bool):
        """设置二维码属性控件的信号阻塞状态

        Args:
            blocked: True 阻塞信号，False 恢复信号
        """
        for control in [self.qr_version_combo, self.error_correction_combo,
                         self.content_input, self.qr_batch_checkbox, self.qr_csv_column_combo]:
            control.blockSignals(blocked)

    def _set_text_signals_blocked(self, blocked: bool):
        """设置文本属性控件的信号阻塞状态

        Args:
            blocked: True 阻塞信号，False 恢复信号
        """
        for control in [self.font_combo, self.font_size_input, self.text_content_input,
                         self.bold_checkbox, self.italic_checkbox, self.underline_checkbox,
                         self.align_left_button, self.align_center_button, self.align_right_button,
                         self.align_top_button, self.align_middle_button, self.align_bottom_button,
                         self.text_batch_checkbox, self.text_csv_column_combo]:
            control.blockSignals(blocked)

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
        self.qr_csv_column_combo.blockSignals(True)
        self.qr_csv_column_combo.clear()
        self.qr_csv_column_combo.addItems(columns)
        self.qr_csv_column_combo.blockSignals(False)

    def update_text_csv_columns(self, columns):
        """更新文本CSV列选择"""
        self.text_csv_column_combo.blockSignals(True)
        self.text_csv_column_combo.clear()
        self.text_csv_column_combo.addItem("")
        self.text_csv_column_combo.addItems(columns)
        self.text_csv_column_combo.blockSignals(False)

    def update_capacity(self, numeric, alphanumeric, byte, kanji):
        """更新容量显示"""
        self.numeric_value.setText(str(numeric))
        self.alphanumeric_value.setText(str(alphanumeric))
        self.byte_value.setText(str(byte))
        self.kanji_value.setText(str(kanji))

    def update_from_object(self, obj, csv_columns=None, has_csv_data=False, update_callback=None):
        """从对象数据更新属性面板

        Args:
            obj: 对象数据
            csv_columns: CSV列名列表
            has_csv_data: 是否有CSV数据
            update_callback: 更新对象的回调函数 (obj_id, **kwargs) -> None
        """
        self._update_position_inputs(obj)

        if csv_columns:
            self.update_qr_csv_columns(csv_columns)
            self.update_text_csv_columns(csv_columns)

        if obj['type'] == 'qr':
            self._update_qr_properties(obj, has_csv_data, update_callback)
        elif obj['type'] == 'text':
            self._update_text_properties(obj, has_csv_data, update_callback)

        self.object_info_label.setText(f"已选择对象 ({obj['id']})")

    def _update_position_inputs(self, obj):
        """更新位置和尺寸输入框"""
        self._set_basic_signals_blocked(True)
        self.x_input.setValue(obj['position']['x'])
        self.y_input.setValue(obj['position']['y'])
        self.width_input.setValue(obj['size']['width'])
        self.height_input.setValue(obj['size']['height'])
        self._set_basic_signals_blocked(False)

    def _update_qr_properties(self, obj, has_csv_data=False, update_callback=None):
        """更新二维码属性"""
        from PyQt5.QtWidgets import QMessageBox
        self.show_qr_properties()

        self._set_qr_signals_blocked(True)
        self.qr_version_combo.setCurrentText(obj.get('qr_version', '21x21'))
        self.error_correction_combo.setCurrentText(obj.get('error_correction', 'Q'))
        self.content_input.setText(obj.get('content', ''))

        batch_enabled = obj.get('batch', False)
        if batch_enabled and not has_csv_data:
            QMessageBox.warning(None, "提示", "请先导入CSV文件")
            self.qr_batch_checkbox.setChecked(False)
            if update_callback:
                update_callback(obj['id'], batch=False)
        else:
            self.qr_batch_checkbox.setChecked(batch_enabled)
            csv_column = obj.get('csv_column', '')
            if csv_column:
                self.qr_csv_column_combo.setCurrentText(csv_column)
            else:
                self.qr_csv_column_combo.setCurrentIndex(-1)
        self._set_qr_signals_blocked(False)

        self.update_capacity(27, 16, 11, 7)

    def _update_text_properties(self, obj, has_csv_data=False, update_callback=None):
        """更新文本属性"""
        from PyQt5.QtGui import QColor
        from PyQt5.QtWidgets import QMessageBox

        self.show_text_properties()

        self._set_text_signals_blocked(True)
        self.font_combo.setCurrentText(obj.get('font', 'Arial'))
        self.font_size_input.setValue(obj.get('font_size', 3))
        self.text_content_input.setText(obj.get('content', ''))

        batch_enabled = obj.get('batch', False)
        if batch_enabled and not has_csv_data:
            QMessageBox.warning(None, "提示", "请先导入CSV文件")
            self.text_batch_checkbox.setChecked(False)
            if update_callback:
                update_callback(obj['id'], batch=False)
        else:
            self.text_batch_checkbox.setChecked(batch_enabled)
            csv_column = obj.get('csv_column', '')
            if csv_column:
                self.text_csv_column_combo.setCurrentText(csv_column)
            else:
                self.text_csv_column_combo.setCurrentIndex(-1)

        text_color = QColor(obj.get('color', '#000000'))
        self.color_preview.setStyleSheet(f"background-color: {text_color.name()};")

        font_style = obj.get('font_style', ['normal'])
        self.bold_checkbox.setChecked('bold' in font_style)
        self.italic_checkbox.setChecked('italic' in font_style)
        self.underline_checkbox.setChecked('underline' in font_style)

        text_align = obj.get('text_align', 'left')
        align_buttons = {
            'left': self.align_left_button,
            'center': self.align_center_button,
            'right': self.align_right_button
        }
        align_buttons.get(text_align, self.align_left_button).setChecked(True)

        vertical_align = obj.get('vertical_align', 'top')
        vertical_align_buttons = {
            'top': self.align_top_button,
            'middle': self.align_middle_button,
            'bottom': self.align_bottom_button
        }
        vertical_align_buttons.get(vertical_align, self.align_top_button).setChecked(True)
        self._set_text_signals_blocked(False)

    def clear(self):
        """清空属性面板"""
        self.object_info_label.setText("未选择对象")
        self.show_qr_properties(False)
