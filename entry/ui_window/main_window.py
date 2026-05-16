"""
L1 入口层 - 主窗口UI组件
功能：组装所有UI组件，管理事件转发
文件：entry/ui_window/main_window.py
"""

import os
from typing import Optional
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QMenuBar, QAction, QFileDialog, QMessageBox, QDialog,
    QStatusBar, QSizePolicy, QColorDialog
)
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt
from entry.ui_window.toolbar import DesignerToolbar
from entry.ui_window.property_panel import PropertyPanel
from entry.ui_window.dialog.basic_settings_dialog import BasicSettingsDialog
from entry.ui_window.dialog.csv_preview_dialog import CSVPreviewDialog
from entry.ui_window.dialog.batch_export_dialog import BatchExportDialog
from entry.ui_window.dialog.preview_dialog import PreviewDialog
from entry.ui_window.menu.menu_file import FileMenu
from entry.ui_window.menu.menu_settings import SettingsMenu
from entry.ui_window.menu.menu_import import ImportMenu
from entry.ui_window.menu.menu_export import ExportMenu
from entry.ui_window.menu.menu_help import HelpMenu
from entry.ui_window.menu.menu_history import HistoryMenu
from entry.ui_window.designer_canvas import LabelDesigner


VERSION = "v1.0.0"
RELEASE_DATE = "2026-04-12"
AUTHOR = "kk120120"
EMAIL = "hzwtox@hotmail.com"
GITHUB = "https://github.com/kk120120/qrcode-label-maker"


class MainWindow(QMainWindow):
    """主窗口 - UI组件

    职责：
    - 组装所有UI组件
    - 管理事件转发
    - 接收用户输入
    """

    def __init__(self):
        """主窗口初始化"""
        super().__init__()
        self.setWindowTitle("QR Label Creator - 批量二维码标签生成器")
        self.setGeometry(100, 100, 1200, 800)

        icon_path = os.path.join(os.path.dirname(__file__), "../../icon_path/sw-icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        from entry.entry_ui import UIEntry
        self.ui_entry = UIEntry()
        self.ui_entry.entry_init_template()

        self.current_template_file: Optional[str] = None

        self.init_ui()
        self.update_qr_sizes()
        self.designer.update()
        self.update_undo_redo_actions()

    def init_ui(self):
        """初始化用户界面"""
        menubar = self.menuBar()
        
        self.file_menu = FileMenu(self)
        self.file_menu.init(menubar)
        
        self.settings_menu = SettingsMenu(self)
        self.settings_menu.init(menubar)
        
        self.import_menu = ImportMenu(self)
        self.import_menu.init(menubar)
        
        self.export_menu = ExportMenu(self)
        self.export_menu.init(menubar)
        
        self.history_menu = HistoryMenu(self)
        self.history_menu.init(menubar)
        
        self.help_menu = HelpMenu(self)
        self.help_menu.init(menubar)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")

        self.toolbar = DesignerToolbar()
        self.toolbar.qr_button.clicked.connect(self.on_qr_button_clicked)
        self.toolbar.text_button.clicked.connect(self.on_text_button_clicked)
        self.toolbar.preview_button.clicked.connect(self.on_preview_button_clicked)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)

        self.toolbar.setFixedHeight(60)
        self.toolbar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        main_layout.addWidget(self.toolbar)

        from PyQt5.QtWidgets import QSplitter, QScrollArea

        self.splitter = QSplitter(Qt.Horizontal)

        self.designer = LabelDesigner(self)
        self.designer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.property_panel = PropertyPanel()
        self.property_panel.setMinimumWidth(340)
        self.property_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        scroll_area = QScrollArea()
        scroll_area.setWidget(self.property_panel)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumWidth(200)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
            }
        """)

        self.splitter.addWidget(self.designer)
        self.splitter.addWidget(scroll_area)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 0)
        self.splitter.setSizes([600, 340])
        self.splitter.setHandleWidth(5)

        main_layout.addWidget(self.splitter, 1)

        self._connect_signals()



    def _connect_signals(self):
        """连接信号槽"""
        self.property_panel.save_button.clicked.connect(self.save_object_properties)
        self.property_panel.qr_batch_checkbox.stateChanged.connect(self.on_batch_checkbox_changed)
        self.property_panel.text_batch_checkbox.stateChanged.connect(self.on_text_batch_checkbox_changed)
        self.property_panel.color_button.clicked.connect(self.on_color_button_clicked)
        self.property_panel.qr_version_combo.currentTextChanged.connect(self.on_qr_version_changed)
        self.property_panel.error_correction_combo.currentTextChanged.connect(self.on_error_correction_changed)

        self.property_panel.bold_checkbox.stateChanged.connect(self.save_object_properties)
        self.property_panel.italic_checkbox.stateChanged.connect(self.save_object_properties)
        self.property_panel.underline_checkbox.stateChanged.connect(self.save_object_properties)

        self.property_panel.x_input.editingFinished.connect(self.save_object_properties)
        self.property_panel.y_input.editingFinished.connect(self.save_object_properties)
        self.property_panel.width_input.editingFinished.connect(self.save_object_properties)
        self.property_panel.height_input.editingFinished.connect(self.save_object_properties)
        self.property_panel.content_input.editingFinished.connect(self.save_object_properties)
        self.property_panel.text_content_input.editingFinished.connect(self.save_object_properties)
        self.property_panel.font_size_input.editingFinished.connect(self.save_object_properties)

        self.property_panel.font_combo.currentTextChanged.connect(self.save_object_properties)
        self.property_panel.align_button_group.buttonClicked.connect(self.save_object_properties)
        self.property_panel.qr_csv_column_combo.currentTextChanged.connect(self.save_object_properties)
        self.property_panel.text_csv_column_combo.currentTextChanged.connect(self.save_object_properties)

    def on_qr_button_clicked(self):
        """工具栏二维码按钮点击事件"""
        x, y = self.ui_entry.entry_get_default_qr_position()
        self.designer.add_qr_object(x, y)
        self.property_panel.show_qr_properties()
        self.update_property_panel()

    def on_text_button_clicked(self):
        """工具栏文本按钮点击事件"""
        x, y = self.ui_entry.entry_get_default_text_position()
        self.designer.add_text_object(x, y)
        self.property_panel.show_text_properties()
        self.update_property_panel()
    
    def on_preview_button_clicked(self):
        """预览按钮点击事件"""
        import tempfile
        # 生成临时文件
        temp_file = tempfile.NamedTemporaryFile(
            suffix='.png', delete=False
        )
        temp_file.close()
        
        # 获取数据总行数
        total_rows = self.ui_entry.entry_get_row_count()
        
        try:
            # 默认使用第一行（索引0）
            success = self.ui_entry.entry_export_current(temp_file.name, 0)
            if success:
                # 定义刷新回调函数
                def refresh_preview(row_idx, file_path):
                    """刷新预览图像"""
                    try:
                        self.ui_entry.entry_export_current(file_path, row_idx)
                    except Exception as e:
                        QMessageBox.warning(self, "错误", f"刷新预览失败: {str(e)}")
                
                dialog = PreviewDialog(temp_file.name, self, total_rows, refresh_preview)
                dialog.exec()
            else:
                QMessageBox.warning(self, "错误", "无法生成预览图像")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"生成预览失败: {str(e)}")

    def new_template(self):
        """新建模板"""
        self.ui_entry.entry_new_template()
        self.designer.selected_object = None
        self.designer.update()
        self.update_property_panel()
        self.current_template_file = None
        self.status_bar.showMessage("已新建模板")

    def open_template(self):
        """打开模板文件"""
        last_dir = self.ui_entry.entry_get_last_open_dir()
        file_path, _ = QFileDialog.getOpenFileName(self, "打开标签模板", last_dir or "d:/", "标签文件 (*.label)")
        if file_path:
            import os
            self.ui_entry.entry_set_last_open_dir(os.path.dirname(file_path))
            if self.ui_entry.entry_open_template(file_path):
                self.designer.selected_object = None
                self.designer.update()
                self.update_property_panel()
                self.current_template_file = file_path
                self.status_bar.showMessage(f"已打开模板: {file_path}")
            else:
                QMessageBox.warning(self, "错误", "无法打开模板文件")

    def save_template(self):
        """保存模板文件"""
        last_dir = self.ui_entry.entry_get_last_open_dir()
        file_path, _ = QFileDialog.getSaveFileName(self, "保存标签模板", last_dir or "d:/", "标签文件 (*.label)")
        if file_path:
            import os
            self.ui_entry.entry_set_last_open_dir(os.path.dirname(file_path))
            if self.ui_entry.entry_save_template(file_path):
                self.current_template_file = file_path
                self.status_bar.showMessage(f"已保存模板: {file_path}")
            else:
                QMessageBox.warning(self, "错误", "无法保存模板文件")

    def import_csv(self):
        """导入CSV文件"""
        last_dir = self.ui_entry.entry_get_last_import_dir()
        file_path, _ = QFileDialog.getOpenFileName(self, "选择CSV文件", last_dir or "d:/", "CSV文件 (*.csv)")
        if file_path:
            import os
            self.ui_entry.entry_set_last_import_dir(os.path.dirname(file_path))
            csv_data, csv_handler = self.ui_entry.entry_import_csv(file_path)
            if csv_data is not None:
                dialog = CSVPreviewDialog(csv_handler, self)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    self.designer.update()
                    self.update_qr_sizes()
                    self.status_bar.showMessage(f"已导入CSV: {file_path}")
            else:
                QMessageBox.warning(self, "错误", "无法导入CSV文件")

    def import_excel(self):
        """导入Excel文件"""
        last_dir = self.ui_entry.entry_get_last_import_dir()
        file_path, _ = QFileDialog.getOpenFileName(self, "选择Excel文件", last_dir or "d:/", "Excel文件 (*.xlsx *.xls)")
        if file_path:
            import os
            self.ui_entry.entry_set_last_import_dir(os.path.dirname(file_path))
            excel_data, csv_handler = self.ui_entry.entry_import_excel(file_path)
            if excel_data is not None:
                dialog = CSVPreviewDialog(csv_handler, self)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    self.designer.update()
                    self.update_qr_sizes()
                    self.status_bar.showMessage(f"已导入Excel: {file_path}")
            else:
                QMessageBox.warning(self, "错误", "无法导入Excel文件")

    def export_current_label(self):
        """导出当前标签为PNG"""
        file_path, _ = QFileDialog.getSaveFileName(self, "导出标签", "d:/", "PNG图像 (*.png)")
        if file_path:
            if self.ui_entry.entry_export_current(file_path):
                self.status_bar.showMessage(f"已导出标签: {file_path}")
            else:
                QMessageBox.warning(self, "错误", "无法导出标签")

    def open_batch_export_dialog(self):
        """打开批量导出对话框"""
        dialog = BatchExportDialog(self)
        last_export_dir = self.ui_entry.entry_get_last_export_dir()
        if last_export_dir:
            dialog.folder_input.setText(last_export_dir)
        dialog.start_button.clicked.connect(lambda: self.on_batch_export_start(dialog))
        if dialog.exec() == QDialog.DialogCode.Accepted:
            pass

    def on_batch_export_start(self, dialog: BatchExportDialog):
        """批量导出开始"""
        output_dir = dialog.folder_input.text()
        if not output_dir:
            QMessageBox.warning(self, "提示", "请选择目标文件夹")
            return
        export_format = dialog.get_selected_format()
        
        # 保存导出目录
        self.ui_entry.entry_set_last_export_dir(output_dir)
        
        # 显示进度区域
        dialog.start_export()
        
        # 定义进度回调函数
        def progress_callback(current, total):
            dialog.update_progress(current, total)
            from PyQt5.QtWidgets import QApplication
            QApplication.processEvents()
        
        # 执行导出
        success, error_msg = self.ui_entry.entry_batch_export(
            output_dir, export_format, progress_callback
        )
        
        # 设置完成状态
        dialog.set_completed(success, error_msg if not success else "")
        
        if success:
            self.status_bar.showMessage(f"已批量导出标签到: {output_dir}")

    def open_basic_settings(self):
        """打开基础设置对话框"""
        template = self.ui_entry.entry_get_template()
        dialog = BasicSettingsDialog(
            self,
            label_size=template['label_size'],
            dpi=template['dpi'],
            grid_color=self.designer.grid_color,
            show_grid=self.designer.show_grid,
            grid_line_style=self.designer.grid_line_style
        )
        if dialog.exec() == QDialog.DialogCode.Accepted:
            settings = dialog.get_settings()
            self.ui_entry.entry_set_label_size(settings['width'], settings['height'], settings['corner_radius'])
            self.ui_entry.entry_set_dpi(settings['dpi'])
            self.designer.grid_color = QColor(settings['grid_color'])
            self.designer.show_grid = settings['show_grid']
            self.designer.grid_line_style = settings['grid_line_style']
            self.designer.update()
            self.status_bar.showMessage("已更新设置")

    def update_property_panel(self):
        """更新属性面板显示"""
        obj = self.designer.get_selected_object()
        
        if obj:
            csv_columns = self.ui_entry.entry_get_csv_columns()
            has_csv_data = self.ui_entry.entry_check_csv_columns()
            
            def update_callback(obj_id, **kwargs):
                self.ui_entry.entry_update_object(obj_id, **kwargs)
                self.designer.is_dragging = False
                self.designer.update()
            
            self.property_panel.update_from_object(obj, csv_columns, has_csv_data, update_callback)
        else:
            self.property_panel.clear()

    def update_qr_sizes(self):
        """更新二维码尺寸选项"""
        sizes = self.ui_entry.entry_update_qr_sizes()
        self.property_panel.qr_version_combo.clear()
        self.property_panel.qr_version_combo.addItems(sizes)
        if sizes:
            self.property_panel.qr_version_combo.setCurrentIndex(0)
            self.on_qr_version_changed(sizes[0])
        self.property_panel.error_correction_combo.setCurrentText("Q")

    def on_qr_version_changed(self, version: str):
        """二维码版本改变事件"""
        error_level = self.property_panel.error_correction_combo.currentText()
        capacity = self.ui_entry.entry_get_qr_capacity(version, error_level)
        if capacity:
            self.property_panel.update_capacity(*capacity)

    def on_error_correction_changed(self, error_level: str):
        """纠错级别改变事件"""
        version = self.property_panel.qr_version_combo.currentText()
        self.on_qr_version_changed(version)

    def on_batch_checkbox_changed(self, state: int):
        """二维码批量复选框改变事件"""
        if state == Qt.CheckState.Checked:
            if not self.ui_entry.entry_check_csv_columns():
                QMessageBox.warning(self, "提示", "请先导入CSV文件")
                self.property_panel.qr_batch_checkbox.setChecked(False)
            else:
                self.property_panel.content_input.setEnabled(False)
        else:
            self.property_panel.content_input.setEnabled(True)

    def on_text_batch_checkbox_changed(self, state: int):
        """文本批量复选框改变事件"""
        if state == Qt.CheckState.Checked:
            if not self.ui_entry.entry_check_csv_columns():
                QMessageBox.warning(self, "提示", "请先导入CSV文件")
                self.property_panel.text_batch_checkbox.setChecked(False)
            else:
                self.property_panel.text_content_input.setEnabled(False)
                self.property_panel.text_csv_column_combo.setEnabled(True)
        else:
            self.property_panel.text_content_input.setEnabled(True)
            self.property_panel.text_csv_column_combo.setEnabled(False)

    def on_color_button_clicked(self):
        """颜色选择按钮点击事件"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.property_panel.color_preview.setStyleSheet(f"background-color: {color.name()};")

    def save_object_properties(self):
        """保存对象属性"""
        obj = self.designer.get_selected_object()
        if not obj:
            return

        self.save_to_history()

        if obj['type'] == 'qr':
            new_obj = {
                'position': {'x': self.property_panel.x_input.value(), 'y': self.property_panel.y_input.value()},
                'size': {'width': self.property_panel.width_input.value(), 'height': self.property_panel.height_input.value()},
                'qr_version': self.property_panel.qr_version_combo.currentText(),
                'error_correction': self.property_panel.error_correction_combo.currentText(),
                'content': self.property_panel.content_input.text(),
                'batch': self.property_panel.qr_batch_checkbox.isChecked(),
                'csv_column': self.property_panel.qr_csv_column_combo.currentText()
            }
            self.ui_entry.entry_update_object_properties(obj['id'], **new_obj)
        elif obj['type'] == 'text':
            font_style = []
            if self.property_panel.bold_checkbox.isChecked():
                font_style.append('bold')
            if self.property_panel.italic_checkbox.isChecked():
                font_style.append('italic')
            if self.property_panel.underline_checkbox.isChecked():
                font_style.append('underline')
            if not font_style:
                font_style = ['normal']

            align_map = {0: 'left', 1: 'center', 2: 'right'}
            align_value = align_map.get(
                self.property_panel.align_button_group.checkedId(), 'left'
            )

            new_obj = {
                'position': {'x': self.property_panel.x_input.value(), 'y': self.property_panel.y_input.value()},
                'size': {'width': self.property_panel.width_input.value(), 'height': self.property_panel.height_input.value()},
                'font': self.property_panel.font_combo.currentText(),
                'font_size': self.property_panel.font_size_input.value(),
                'font_style': font_style,
                'text_align': align_value,
                'color': '#000000',
                'content': self.property_panel.text_content_input.text(),
                'batch': self.property_panel.text_batch_checkbox.isChecked(),
                'csv_column': self.property_panel.text_csv_column_combo.currentText()
            }
            self.ui_entry.entry_update_object_properties(obj['id'], **new_obj)

        self.designer.update()
        self.status_bar.showMessage("已更新对象属性")

    def show_about(self):
        """显示关于对话框"""
        about_text = (
            f"Python 批量二维码标签生成器\n"
            f"版本：{VERSION}\t{RELEASE_DATE}\n"
            f"作者：{AUTHOR}\n"
            f"邮箱：{EMAIL}\n"
            f"GitHub：{GITHUB}\n\n"
            f"Copyright (C) 2026"
        )
        QMessageBox.information(self, "关于", about_text)

    def save_to_history(self):
        """保存当前状态到历史记录"""
        self.ui_entry.entry_history_save()
        self.update_undo_redo_actions()

    def undo(self):
        """撤销操作"""
        template, objects = self.ui_entry.entry_history_undo()
        if template is not None and objects is not None:
            self.designer.selected_object = None
            self.designer.update()
            self.update_property_panel()
            self.update_undo_redo_actions()
            self.status_bar.showMessage("已撤销")

    def redo(self):
        """重做操作"""
        template, objects = self.ui_entry.entry_history_redo()
        if template is not None and objects is not None:
            self.designer.selected_object = None
            self.designer.update()
            self.update_property_panel()
            self.update_undo_redo_actions()
            self.status_bar.showMessage("已重做")

    def update_undo_redo_actions(self):
        """更新撤销重做按钮状态"""
        can_undo, can_redo = self.ui_entry.entry_history_get_status()
        self.history_menu.update_undo_redo_actions(can_undo, can_redo)
