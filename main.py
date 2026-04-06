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

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QPixmap
from PyQt5.QtCore import Qt, QPoint, QRectF, QTimer
import sys
import os

from ui_components import (
    DrawToolBar, PropertyPanel, BasicSettingsDialog, 
    CSVPreviewDialog, BatchExportDialog
)
from label_template import LabelTemplate
from csv_handler import CSVHandler
from image_processor import ImageProcessor
from qr_generator import QRGenerator
from config_manager import ConfigManager

class LabelDesigner(QWidget):
    """标签设计器"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.template = LabelTemplate()
        self.selected_object = None
        self.is_dragging = False
        self.drag_start = QPoint()
        self.qr_generator = QRGenerator()
        
    def paintEvent(self, event):
        """绘制事件"""
        painter = QPainter(self)
        
        # 绘制标签背景
        label_width = self.template.template['label_size']['width']
        label_height = self.template.template['label_size']['height']
        corner_radius = self.template.template['label_size']['corner_radius']
        
        # 计算缩放比例
        scale = min(self.width() / (label_width + 20), self.height() / (label_height + 20))
        x_offset = (self.width() - label_width * scale) / 2
        y_offset = (self.height() - label_height * scale) / 2
        
        # 绘制标签边框
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawRoundedRect(
            int(x_offset), int(y_offset), 
            int(label_width * scale), int(label_height * scale), 
            int(corner_radius * scale), int(corner_radius * scale)
        )
        
        # 绘制对象
        out_of_bounds = self.template.check_boundaries()
        objects = self.template.get_objects()
        
        for i, obj in enumerate(objects):
            x = int(obj['position']['x'] * scale + x_offset)
            y = int(obj['position']['y'] * scale + y_offset)
            width = int(obj['size']['width'] * scale)
            height = int(obj['size']['height'] * scale)
            
            # 检查是否超出边界
            is_out_of_bounds = obj['id'] in out_of_bounds
            
            # 绘制对象边框
            if obj['id'] == self.selected_object:
                painter.setPen(QPen(QColor(0, 0, 255), 2))
            elif is_out_of_bounds:
                painter.setPen(QPen(QColor(255, 0, 0), 2))
            else:
                painter.setPen(QPen(QColor(0, 0, 0), 1))
            
            painter.setBrush(QBrush(QColor(240, 240, 240, 100)))
            painter.drawRect(x, y, width, height)
            
            # 绘制对象类型简称和序号
            obj_type = "QR" if obj['type'] == 'qr' else "Text"
            obj_name = f"{obj_type} #{i+1}"
            painter.setPen(QPen(QColor(255, 0, 0), 1))
            painter.drawText(int(x + 5), int(y - 5), obj_name)
            
            # 绘制对象内容
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            if obj['type'] == 'qr':
                # 生成并绘制二维码图像
                content = obj['properties'].get('content', '')
                error_correction = obj['properties'].get('error_correction', 'Q')
                if content:
                    try:
                        qr_img = self.qr_generator.generate_qr(content, error_correction)
                        # 转换PIL图像为QPixmap
                        from PIL.ImageQt import ImageQt
                        qt_img = ImageQt(qr_img)
                        pixmap = QPixmap.fromImage(qt_img)
                        # 调整大小并绘制
                        scaled_pixmap = pixmap.scaled(int(width), int(height), Qt.AspectRatioMode.KeepAspectRatio)
                        painter.drawPixmap(int(x), int(y), scaled_pixmap)
                    except Exception as e:
                        painter.drawText(int(x + 5), int(y + 15), "QR")
                else:
                    painter.drawText(int(x + 5), int(y + 15), "QR")
            elif obj['type'] == 'text':
                # 绘制文本内容预览
                content = obj['properties'].get('content', '')
                if content:
                    painter.drawText(int(x + 5), int(y + 15), content[:20])  # 显示前20个字符
                else:
                    painter.drawText(int(x + 5), int(y + 15), "Text")
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            # 计算缩放比例
            label_width = self.template.template['label_size']['width']
            label_height = self.template.template['label_size']['height']
            scale = min(self.width() / (label_width + 20), self.height() / (label_height + 20))
            x_offset = (self.width() - label_width * scale) / 2
            y_offset = (self.height() - label_height * scale) / 2
            
            # 检查是否点击了对象
            clicked_obj = None
            objects = self.template.get_objects()
            # 从后往前遍历，确保上层对象先被检测
            for i in reversed(range(len(objects))):
                obj = objects[i]
                x = int(obj['position']['x'] * scale + x_offset)
                y = int(obj['position']['y'] * scale + y_offset)
                width = int(obj['size']['width'] * scale)
                height = int(obj['size']['height'] * scale)
                
                # 创建矩形区域
                rect = QRectF(x, y, width, height)
                # 检查鼠标是否在矩形内
                if rect.contains(event.pos()):
                    clicked_obj = obj
                    break
            
            if clicked_obj:
                # 设置选中对象
                self.selected_object = clicked_obj['id']
                # 暂时不设置is_dragging，只有在鼠标移动时才设置
                self.drag_start = event.pos()
                # 强制重绘
                self.update()
                # 通知主窗口更新属性面板
                
                # 直接调用主窗口的update_property_panel方法
                if self.parent() and hasattr(self.parent(), 'update_property_panel'):
                    self.parent().update_property_panel()
                    # 再次强制更新，确保属性面板正确显示
                    QTimer.singleShot(100, lambda: self.parent().update_property_panel())
                else:
                    # 尝试通过其他方式获取主窗口
                    main_window = self.window()
                    if main_window and hasattr(main_window, 'update_property_panel'):
                        main_window.update_property_panel()
                        QTimer.singleShot(100, lambda: main_window.update_property_panel())
            else:
                # 未点击对象，取消选择
                self.selected_object = None
                # 强制重绘
                self.update()
                # 通知主窗口更新属性面板
                if hasattr(self.parent(), 'update_property_panel'):
                    self.parent().update_property_panel()
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if self.selected_object:
            # 如果是首次移动，设置is_dragging为True
            if not self.is_dragging:
                self.is_dragging = True
            
            # 计算缩放比例
            label_width = self.template.template['label_size']['width']
            label_height = self.template.template['label_size']['height']
            scale = min(self.width() / (label_width + 20), self.height() / (label_height + 20))
            
            # 计算移动距离
            delta_x = (event.x() - self.drag_start.x()) / scale
            delta_y = (event.y() - self.drag_start.y()) / scale
            
            # 更新对象位置
            obj = self.template.get_object(self.selected_object)
            if obj:
                new_x = obj['position']['x'] + delta_x
                new_y = obj['position']['y'] + delta_y
                self.template.update_object(self.selected_object, x=new_x, y=new_y)
                self.drag_start = event.pos()
                
                # 在状态栏显示当前坐标
                if hasattr(self.parent(), 'statusBar'):
                    self.parent().statusBar.showMessage(f"坐标: X={new_x:.2f} mm, Y={new_y:.2f} mm")
                
                # 实时更新属性面板中的位置信息
                if hasattr(self.parent(), 'property_panel'):
                    self.parent().property_panel.x_input.setValue(new_x)
                    self.parent().property_panel.y_input.setValue(new_y)
                
                self.update()
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False
            # 通知主窗口更新属性面板
            if hasattr(self.parent(), 'update_property_panel'):
                self.parent().update_property_panel()
            # 清除状态栏信息
            if hasattr(self.parent(), 'statusBar'):
                self.parent().statusBar.clearMessage()
    
    def keyPressEvent(self, event):
        """键盘按下事件"""
        if self.selected_object:
            obj = self.template.get_object(self.selected_object)
            if obj:
                step = 0.1  # 微调步长，使用小数以支持更精细的调整
                if event.key() == Qt.Key.Key_Left:
                    new_x = obj['position']['x'] - step
                    self.template.update_object(self.selected_object, x=new_x)
                elif event.key() == Qt.Key.Key_Right:
                    new_x = obj['position']['x'] + step
                    self.template.update_object(self.selected_object, x=new_x)
                elif event.key() == Qt.Key.Key_Up:
                    new_y = obj['position']['y'] - step
                    self.template.update_object(self.selected_object, y=new_y)
                elif event.key() == Qt.Key.Key_Down:
                    new_y = obj['position']['y'] + step
                    self.template.update_object(self.selected_object, y=new_y)
                elif event.key() == Qt.Key.Key_Delete:
                    # 删除选中对象
                    self.template.remove_object(self.selected_object)
                    self.selected_object = None
                    # 通知主窗口更新属性面板
                    if hasattr(self.parent(), 'update_property_panel'):
                        self.parent().update_property_panel()
                self.update()
    
    def add_qr_object(self, x, y):
        """添加二维码对象"""
        obj_id = self.template.add_qr_object(x, y)
        self.selected_object = obj_id
        self.update()
        return obj_id
    
    def add_text_object(self, x, y):
        """添加文本对象"""
        obj_id = self.template.add_text_object(x, y)
        self.selected_object = obj_id
        self.update()
        return obj_id
    
    def get_selected_object(self):
        """获取选中的对象"""
        if self.selected_object:
            return self.template.get_object(self.selected_object)
        return None
    
    def update_object_properties(self, **kwargs):
        """更新对象属性"""
        if self.selected_object:
            self.template.update_object(self.selected_object, **kwargs)
            self.update()
    
    def remove_selected_object(self):
        """删除选中的对象"""
        if self.selected_object:
            self.template.remove_object(self.selected_object)
            self.selected_object = None
            self.update()
    
    def resizeEvent(self, event):
        """窗口大小变化事件"""
        super().resizeEvent(event)
        self.update()

class MainWindow(QMainWindow):
    """主窗口"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python 批量二维码标签生成器")
        self.setGeometry(100, 100, 1200, 800)
        
        # 初始化组件
        self.init_ui()
        
        # 初始化模块
        self.csv_handler = CSVHandler()
        self.image_processor = ImageProcessor()
        self.config_manager = ConfigManager()
        
        # 初始化属性面板的二维码尺寸
        self.update_qr_sizes()
    
    def init_ui(self):
        """初始化界面"""
        # 菜单栏
        menubar = self.menuBar()
        
        # 设置菜单
        settings_menu = menubar.addMenu("设置")
        
        basic_settings_action = QAction("基础设置", self)
        basic_settings_action.triggered.connect(self.open_basic_settings)
        settings_menu.addAction(basic_settings_action)
        
        # 文件菜单
        file_menu = menubar.addMenu("文件")
        
        new_action = QAction("新建", self)
        new_action.triggered.connect(self.new_template)
        file_menu.addAction(new_action)
        
        open_action = QAction("打开", self)
        open_action.triggered.connect(self.open_template)
        file_menu.addAction(open_action)
        
        save_action = QAction("保存模板", self)
        save_action.triggered.connect(self.save_template)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 数据菜单
        data_menu = menubar.addMenu("数据")
        
        import_csv_action = QAction("导入CSV", self)
        import_csv_action.triggered.connect(self.import_csv)
        data_menu.addAction(import_csv_action)
        
        # 导出菜单
        export_menu = menubar.addMenu("导出")
        
        export_current_action = QAction("导出当前标签为PNG", self)
        export_current_action.triggered.connect(self.export_current)
        export_menu.addAction(export_current_action)
        
        batch_export_action = QAction("批量导出", self)
        batch_export_action.triggered.connect(self.batch_export)
        export_menu.addAction(batch_export_action)
        
        # 编辑菜单
        edit_menu = menubar.addMenu("编辑")
        
        delete_action = QAction("删除选中对象", self)
        delete_action.triggered.connect(self.delete_selected)
        edit_menu.addAction(delete_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        # 状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("就绪")
        
        # 中央窗口
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 工具栏
        self.toolbar = DrawToolBar()
        main_layout.addWidget(self.toolbar)
        
        # 主要内容区
        content_layout = QHBoxLayout()
        
        # 设计区
        self.designer = LabelDesigner()
        content_layout.addWidget(self.designer, 2)
        
        # 预览区
        self.preview = QWidget()
        content_layout.addWidget(self.preview, 1)
        
        # 属性面板
        self.property_panel = PropertyPanel()
        content_layout.addWidget(self.property_panel, 1)
        
        main_layout.addLayout(content_layout)
        
        # 信号连接
        self.toolbar.qr_button.clicked.connect(self.on_qr_button_clicked)
        self.toolbar.text_button.clicked.connect(self.on_text_button_clicked)
        self.property_panel.save_button.clicked.connect(self.on_save_properties)
        self.property_panel.batch_checkbox.stateChanged.connect(self.on_batch_checkbox_changed)
        self.property_panel.text_batch_checkbox.stateChanged.connect(self.on_text_batch_checkbox_changed)
        self.property_panel.color_button.clicked.connect(self.on_color_button_clicked)
        self.property_panel.qr_version_combo.currentTextChanged.connect(self.on_qr_version_changed)
        self.property_panel.error_correction_combo.currentTextChanged.connect(self.on_error_correction_changed)
        
        # 为输入框添加回车键信号连接
        self.property_panel.x_input.editingFinished.connect(self.on_save_properties)
        self.property_panel.y_input.editingFinished.connect(self.on_save_properties)
        self.property_panel.width_input.editingFinished.connect(self.on_save_properties)
        self.property_panel.height_input.editingFinished.connect(self.on_save_properties)
        self.property_panel.content_input.editingFinished.connect(self.on_save_properties)
        self.property_panel.text_content_input.editingFinished.connect(self.on_save_properties)
        self.property_panel.font_size_input.editingFinished.connect(self.on_save_properties)
    
    def open_basic_settings(self):
        """打开基础设置对话框"""
        template = self.designer.template.get_template()
        dialog = BasicSettingsDialog(
            self, 
            label_size=template['label_size'],
            dpi=template['dpi']
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            settings = dialog.get_settings()
            self.designer.template.set_label_size(
                settings['width'],
                settings['height'],
                settings['corner_radius']
            )
            self.designer.template.set_dpi(settings['dpi'])
            self.designer.update()
            self.statusBar.showMessage("基础设置已更新")
    
    def new_template(self):
        """新建模板"""
        self.designer.template = LabelTemplate()
        self.designer.selected_object = None
        self.designer.update()
        self.statusBar.showMessage("已新建模板")
    
    def open_template(self):
        """打开模板"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开模板", "d:/", "Label Files (*.label)"
        )
        if file_path:
            if self.designer.template.load_template(file_path):
                self.designer.selected_object = None
                self.designer.update()
                self.statusBar.showMessage(f"已打开模板: {file_path}")
            else:
                QMessageBox.warning(self, "错误", "加载模板失败")
    
    def save_template(self):
        """保存模板"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存模板", "d:/", "Label Files (*.label)"
        )
        if file_path:
            if self.designer.template.save_template(file_path):
                self.statusBar.showMessage(f"已保存模板: {file_path}")
            else:
                QMessageBox.warning(self, "错误", "保存模板失败")
    
    def import_csv(self):
        """导入CSV"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "导入CSV", "d:/", "CSV Files (*.csv)"
        )
        if file_path:
            if self.csv_handler.import_csv(file_path):
                # 显示预览对话框
                dialog = CSVPreviewDialog(self.csv_handler, self)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    # 更新属性面板中的CSV列
                    columns = self.csv_handler.get_columns()
                    self.property_panel.update_csv_columns(columns)
                    self.statusBar.showMessage(f"已导入CSV: {file_path}")
            else:
                QMessageBox.warning(self, "错误", "导入CSV失败")
    
    def update_qr_sizes(self):
        """更新二维码尺寸选择"""
        sizes = self.config_manager.get_qr_sizes()
        self.property_panel.qr_version_combo.clear()
        self.property_panel.qr_version_combo.addItems(sizes)
        # 默认选择第一个尺寸
        if sizes:
            self.property_panel.qr_version_combo.setCurrentIndex(0)
            self.on_qr_version_changed(sizes[0])
        # 默认纠错级别设置为Q
        self.property_panel.error_correction_combo.setCurrentText("Q")
    
    def on_qr_version_changed(self, version):
        """二维码尺寸变化"""
        error_level = self.property_panel.error_correction_combo.currentText()
        self.update_capacity_display(version, error_level)
    
    def on_error_correction_changed(self, error_level):
        """纠错级别变化"""
        version = self.property_panel.qr_version_combo.currentText()
        self.update_capacity_display(version, error_level)
    
    def update_capacity_display(self, version, error_level):
        """更新容量显示"""
        capacity = self.config_manager.get_capacity(version, error_level)
        if capacity:
            self.property_panel.update_capacity(*capacity)
    
    def on_qr_button_clicked(self):
        """点击二维码按钮"""
        # 在设计区中心添加二维码对象
        label_width = self.designer.template.template['label_size']['width']
        label_height = self.designer.template.template['label_size']['height']
        x = (label_width - 10) / 2
        y = (label_height - 10) / 2
        self.designer.add_qr_object(x, y)
        self.property_panel.show_qr_properties()
        self.update_property_panel()
    
    def on_text_button_clicked(self):
        """点击文本按钮"""
        # 在设计区中心添加文本对象
        label_width = self.designer.template.template['label_size']['width']
        label_height = self.designer.template.template['label_size']['height']
        x = (label_width - 30) / 2
        y = (label_height - 10) / 2
        self.designer.add_text_object(x, y)
        self.property_panel.show_text_properties()
        self.update_property_panel()
    
    def on_save_properties(self):
        """保存属性"""
        obj = self.designer.get_selected_object()
        if obj:
            # 更新基本属性
            x = self.property_panel.x_input.value()
            y = self.property_panel.y_input.value()
            width = self.property_panel.width_input.value()
            height = self.property_panel.height_input.value()
            
            if obj['type'] == 'qr':
                # 更新二维码属性
                properties = {
                    'qr_version': self.property_panel.qr_version_combo.currentText(),
                    'error_correction': self.property_panel.error_correction_combo.currentText(),
                    'content': self.property_panel.content_input.text(),
                    'batch': self.property_panel.batch_checkbox.isChecked(),
                    'csv_column': self.property_panel.csv_column_combo.currentText()
                }
                
                # 如果是批量生成，使用CSV第一行数据预览
                if properties['batch'] and self.csv_handler.get_data() is not None:
                    csv_data = self.csv_handler.get_data()
                    if not csv_data.empty:
                        column = properties['csv_column']
                        if column in csv_data.columns:
                            properties['content'] = str(csv_data.iloc[0][column])
            elif obj['type'] == 'text':
                # 更新文本属性
                font_style = []
                if self.property_panel.bold_checkbox.isChecked():
                    font_style.append('bold')
                if self.property_panel.italic_checkbox.isChecked():
                    font_style.append('italic')
                if self.property_panel.underline_checkbox.isChecked():
                    font_style.append('underline')
                
                # 确保文本内容使用UTF-8格式
                content = self.property_panel.text_content_input.text()
                try:
                    # 确保内容是字符串格式
                    content = str(content)
                except:
                    content = ""
                
                properties = {
                    'font': self.property_panel.font_combo.currentText(),
                    'font_size': self.property_panel.font_size_input.value(),
                    'font_style': font_style,
                    'color': self.property_panel.color_preview.styleSheet().split(':')[-1].strip().strip(';'),
                    'content': content,
                    'batch': self.property_panel.text_batch_checkbox.isChecked(),
                    'csv_column': self.property_panel.text_csv_column_combo.currentText()
                }
                
                # 如果是批量生成，使用CSV第一行数据预览
                if properties['batch'] and self.csv_handler.get_data() is not None:
                    csv_data = self.csv_handler.get_data()
                    if not csv_data.empty:
                        column = properties['csv_column']
                        if column in csv_data.columns:
                            properties['content'] = str(csv_data.iloc[0][column])
            
            self.designer.update_object_properties(
                x=x, y=y, width=width, height=height, properties=properties
            )
            self.statusBar.showMessage("属性已保存")
    
    def update_property_panel(self):
        """更新属性面板"""
        # 强制获取最新的选中对象
        selected_id = self.designer.selected_object
        
        # 直接从模板中获取对象，而不是通过get_selected_object
        objects = self.designer.template.get_objects()
        
        obj = None
        for o in objects:
            if o['id'] == selected_id:
                obj = o
                break
        
        if obj:
            # 查找对象在列表中的索引
            obj_index = -1
            for i, o in enumerate(objects):
                if o['id'] == obj['id']:
                    obj_index = i + 1  # 从1开始编号
                    break
            
            # 更新对象信息标签
            obj_type = "QR" if obj['type'] == 'qr' else "Text"
            self.property_panel.object_info_label.setText(f"选中对象: {obj_type} #{obj_index}")
            
            # 强制隐藏所有属性面板，然后再显示正确的面板
            self.property_panel.qr_group.setVisible(False)
            self.property_panel.text_group.setVisible(False)
            
            # 强制重新布局
            self.property_panel.layout.update()
            self.property_panel.layout.activate()
            
            # 确保显示正确的属性面板
            if obj['type'] == 'qr':
                self.property_panel.qr_group.setVisible(True)
                self.property_panel.text_group.setVisible(False)
            else:
                self.property_panel.qr_group.setVisible(False)
                self.property_panel.text_group.setVisible(True)
            
            # 再次强制重新布局
            self.property_panel.layout.update()
            self.property_panel.layout.activate()
            
            # 更新基本属性
            self.property_panel.x_input.setValue(obj['position']['x'])
            self.property_panel.y_input.setValue(obj['position']['y'])
            self.property_panel.width_input.setValue(obj['size']['width'])
            self.property_panel.height_input.setValue(obj['size']['height'])
            
            if obj['type'] == 'qr':
                # 更新二维码属性
                self.property_panel.qr_version_combo.setCurrentText(obj['properties']['qr_version'])
                self.property_panel.error_correction_combo.setCurrentText(obj['properties']['error_correction'])
                self.property_panel.content_input.setText(obj['properties']['content'])
                self.property_panel.batch_checkbox.setChecked(obj['properties']['batch'])
                
                # 更新CSV列选择
                columns = self.csv_handler.get_columns()
                self.property_panel.update_csv_columns(columns)
                if obj['properties']['csv_column'] in columns:
                    self.property_panel.csv_column_combo.setCurrentText(obj['properties']['csv_column'])
                    
                # 更新容量显示
                self.update_capacity_display(
                    obj['properties']['qr_version'],
                    obj['properties']['error_correction']
                )
            elif obj['type'] == 'text':
                # 更新文本属性
                self.property_panel.font_combo.setCurrentText(obj['properties']['font'])
                self.property_panel.font_size_input.setValue(obj['properties']['font_size'])
                
                # 更新字体样式
                self.property_panel.bold_checkbox.setChecked('bold' in obj['properties']['font_style'])
                self.property_panel.italic_checkbox.setChecked('italic' in obj['properties']['font_style'])
                self.property_panel.underline_checkbox.setChecked('underline' in obj['properties']['font_style'])
                
                # 更新颜色
                self.property_panel.color_preview.setStyleSheet(f"background-color: {obj['properties']['color']};")
                self.property_panel.text_content_input.setText(obj['properties']['content'])
                self.property_panel.text_batch_checkbox.setChecked(obj['properties']['batch'])
                
                # 更新CSV列选择
                columns = self.csv_handler.get_columns()
                self.property_panel.update_csv_columns(columns)
                if obj['properties']['csv_column'] in columns:
                    self.property_panel.text_csv_column_combo.setCurrentText(obj['properties']['csv_column'])
        else:
            # 未选择对象时更新标签
            self.property_panel.object_info_label.setText("未选择对象")
            # 隐藏所有属性面板
            self.property_panel.qr_group.setVisible(False)
            self.property_panel.text_group.setVisible(False)
    
    def on_batch_checkbox_changed(self, state):
        """批量生成复选框变化"""
        try:
            if state == Qt.CheckState.Checked:
                # 检查是否已导入CSV
                if not self.csv_handler.get_columns():
                    QMessageBox.warning(self, "提示", "请先导入CSV文件")
                    self.property_panel.batch_checkbox.setChecked(False)
                else:
                    # 禁用内容输入
                    self.property_panel.content_input.setEnabled(False)
            else:
                # 启用内容输入
                self.property_panel.content_input.setEnabled(True)
        except Exception as e:
            print(f"批量生成复选框变化错误: {e}")
            # 确保复选框状态正确
            self.property_panel.batch_checkbox.setChecked(False)
            self.property_panel.content_input.setEnabled(True)

    def on_text_batch_checkbox_changed(self, state):
        """文本批量生成复选框变化"""
        try:
            if state == Qt.CheckState.Checked:
                # 检查是否已导入CSV
                if not self.csv_handler.get_columns():
                    QMessageBox.warning(self, "提示", "请先导入CSV文件")
                    self.property_panel.text_batch_checkbox.setChecked(False)
                else:
                    # 禁用内容输入
                    self.property_panel.text_content_input.setEnabled(False)
            else:
                # 启用内容输入
                self.property_panel.text_content_input.setEnabled(True)
        except Exception as e:
            print(f"文本批量生成复选框变化错误: {e}")
            # 确保复选框状态正确
            self.property_panel.text_batch_checkbox.setChecked(False)
            self.property_panel.text_content_input.setEnabled(True)
    
    def on_color_button_clicked(self):
        """颜色选择按钮点击"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.property_panel.color_preview.setStyleSheet(f"background-color: {color.name()};")
    
    def delete_selected(self):
        """删除选中对象"""
        self.designer.remove_selected_object()
        self.statusBar.showMessage("已删除选中对象")
    
    def export_current(self):
        """导出当前标签"""
        # 保存为PNG
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出当前标签", "d:/", "PNG Files (*.png)"
        )
        if file_path:
            # 生成标签图像
            template = self.designer.template.get_template()
            img = self.image_processor.create_label(
                template['label_size']['width'],
                template['label_size']['height'],
                template['label_size']['corner_radius'],
                template['dpi']
            )
            
            # 添加对象
            for obj in template['objects']:
                if obj['type'] == 'qr':
                    qr_gen = QRGenerator()
                    qr_img = qr_gen.generate_qr(
                        obj['properties']['content'],
                        obj['properties']['error_correction']
                    )
                    img = self.image_processor.add_qr_to_label(
                        img, qr_img,
                        obj['position']['x'], obj['position']['y'],
                        obj['size']['width'], obj['size']['height'],
                        template['dpi']
                    )
                elif obj['type'] == 'text':
                    img = self.image_processor.add_text_to_label(
                        img, obj['properties']['content'],
                        obj['position']['x'], obj['position']['y'],
                        obj['size']['width'], obj['size']['height'],
                        obj['properties']['font'],
                        obj['properties']['font_size'],
                        obj['properties']['font_style'],
                        obj['properties']['color'],
                        template['dpi']
                    )
            
            # 保存图像
            self.image_processor.save_label(img, file_path)
            self.statusBar.showMessage(f"已导出标签: {file_path}")
    
    def batch_export(self):
        """批量导出"""
        # 检查是否满足条件
        has_csv = bool(self.csv_handler.get_columns())
        has_batch_objects = any(
            obj['properties']['batch'] for obj in self.designer.template.get_objects()
        )
        
        if not has_csv:
            QMessageBox.warning(self, "提示", "请先导入CSV文件")
            return
        
        if not has_batch_objects:
            QMessageBox.warning(self, "提示", "请至少选择一个批量生成的对象")
            return
        
        # 显示批量导出对话框
        dialog = BatchExportDialog(self)
        dialog.start_button.clicked.connect(lambda: self.on_batch_export_start(dialog))
        if dialog.exec() == QDialog.DialogCode.Accepted:
            pass
    
    def on_batch_export_start(self, dialog):
        """开始批量导出"""
        output_dir = dialog.folder_input.text()
        if not output_dir:
            QMessageBox.warning(self, "提示", "请选择目标文件夹")
            return
        
        # 开始批量处理
        template = self.designer.template.get_template()
        csv_data = self.csv_handler.get_data()
        
        # 创建并显示进度条 - 判定条件是output_dir不为空
        from PyQt5.QtWidgets import QProgressDialog, QApplication
        if output_dir is not None:
            dialog.progress = QProgressDialog("正在生成标签...", "取消", 0, len(csv_data), self)
        else:
            dialog.progress = QProgressDialog("正在生成标签...", "取消", 0, 100, self)
        
        dialog.progress.setWindowTitle("批量生成")
        dialog.progress.show()
        QApplication.processEvents()  # 确保进度窗及时显示
        
        # 批量处理
        results = self.image_processor.batch_process(template, csv_data, output_dir)
        
        # 完成
        if csv_data is not None:
            dialog.progress.setValue(len(csv_data))
        else:
            dialog.progress.setValue(100)
        QApplication.processEvents()  # 确保进度条更新
        QMessageBox.information(self, "完成", f"已生成 {len(results)} 个标签")
        dialog.accept()
        self.statusBar.showMessage(f"批量导出完成，生成 {len(results)} 个标签")
    
    def resizeEvent(self, event):
        """窗口大小变化事件"""
        super().resizeEvent(event)
        # 主窗口大小变化时，设计器会自动更新，因为它已经有了resizeEvent处理
    
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.information(self, "关于", f"Python 批量二维码标签生成器\n版本：V0.7.1\t2026-04-06\n作者：kk120120\n邮箱：hzwtox@hotmail.com\n\nCopyright (C) 2026\n\nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
