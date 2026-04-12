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

# 版本信息
VERSION = "v0.7.9"
RELEASE_DATE = "2026-04-12"
AUTHOR = "kk120120"
EMAIL = "hzwtox@hotmail.com"
GITHUB = "https://github.com/kk120120/qrcode-label-maker"

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QPixmap, QFont
from PyQt5.QtCore import Qt, QPoint, QPointF, QRectF, QTimer
import sys
import os

# 尝试导入PIL模块
try:
    from PIL import Image
    from PIL.ImageQt import ImageQt
except ImportError:
    Image = None
    ImageQt = None

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
        self.show_grid = False  # 网格显示状态
        self.grid_color = QColor(180, 180, 180)  # 默认为比淡灰色深一点的颜色
        self.zoom = 1.0  # 缩放比例
        self.pan_offset = QPointF(0, 0)  # 平移偏移
        self.is_panning = False  # 平移状态
        self.pan_start = QPointF()  # 平移起始点
        
    def paintEvent(self, event):
        """绘制事件"""
        painter = QPainter(self)
        
        # 应用平移
        painter.translate(self.pan_offset)
        
        # 绘制标签背景
        label_width = self.template.template['label_size']['width']
        label_height = self.template.template['label_size']['height']
        corner_radius = self.template.template['label_size']['corner_radius']
        
        # 计算缩放比例 - 减少边距到3mm左右
        base_scale = min(self.width() / (label_width + 6), self.height() / (label_height + 6))
        scale = base_scale * self.zoom
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
        
        # 绘制0,0点标记
        painter.setPen(QPen(QColor(255, 0, 0), 2))
        painter.drawLine(int(x_offset - 5), int(y_offset), int(x_offset + 5), int(y_offset))
        painter.drawLine(int(x_offset), int(y_offset - 5), int(x_offset), int(y_offset + 5))
        painter.setPen(QPen(QColor(255, 0, 0), 1))
        painter.drawText(int(x_offset + 5), int(y_offset - 5), "(0,0)")
        
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
            
            # 保存当前字体和画笔
            original_font = painter.font()
            original_pen = painter.pen()
            
            # 设置编号专用字体和颜色
            number_font = QFont("Arial", 8)  # 使用固定大小的字体
            painter.setFont(number_font)
            painter.setPen(QPen(QColor(255, 0, 0), 1))
            
            # 绘制编号
            painter.drawText(int(x + 5), int(y - 5), obj_name)
            
            # 恢复原始字体和画笔
            painter.setFont(original_font)
            painter.setPen(original_pen)
            
            # 绘制对象内容
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            if obj['type'] == 'qr':
                # 生成并绘制二维码图像
                content = obj['properties'].get('content', '')
                error_correction = obj['properties'].get('error_correction', 'Q')
                if content:
                    try:
                        # 生成二维码
                        qr_img = self.qr_generator.generate_qr(content, error_correction)
                        
                        # 保存为临时文件
                        import tempfile
                        import os
                        temp_fd, temp_file = tempfile.mkstemp(suffix='.png')
                        os.close(temp_fd)
                        
                        qr_img.save(temp_file)
                        
                        # 使用QPixmap直接加载
                        pixmap = QPixmap(temp_file)
                        
                        if not pixmap.isNull():
                            # 调整大小并绘制
                            scaled_pixmap = pixmap.scaled(int(width), int(height), Qt.AspectRatioMode.KeepAspectRatio)
                            painter.drawPixmap(int(x), int(y), scaled_pixmap)
                        else:
                            painter.drawText(int(x + 5), int(y + 15), "QR: Load Error")
                        
                        # 清理临时文件
                        try:
                            os.unlink(temp_file)
                        except:
                            pass
                    except Exception as e:
                        painter.drawText(int(x + 5), int(y + 15), f"QR Error: {str(e)[:15]}")
                else:
                    # 没有内容时显示QR
                    painter.drawText(int(x + 5), int(y + 15), "QR")
            elif obj['type'] == 'text':
                # 绘制文本内容预览
                content = obj['properties'].get('content', '')
                font = obj['properties'].get('font', 'Arial')
                font_size = obj['properties'].get('font_size', 3)
                font_style = obj['properties'].get('font_style', [])
                
                # 创建字体
                qfont = QFont(font, int(font_size * scale))
                if 'bold' in font_style:
                    qfont.setBold(True)
                if 'italic' in font_style:
                    qfont.setItalic(True)
                if 'underline' in font_style:
                    qfont.setUnderline(True)
                
                painter.setFont(qfont)
                
                # 设置裁剪区域，确保文本不超出对象外框
                painter.setClipRect(x, y, width, height)
                
                if content:
                    # 计算可显示的最大字符数，确保不超出宽度
                    max_width = width - 10  # 减去左右边距
                    text_to_draw = content
                    # 使用QFontMetrics计算文本宽度
                    from PyQt5.QtGui import QFontMetrics
                    fm = QFontMetrics(qfont)
                    
                    # 逐字符检查，找到适合宽度的文本
                    for i in range(len(content), 0, -1):
                        if fm.horizontalAdvance(content[:i]) <= max_width:
                            text_to_draw = content[:i]
                            break
                    else:
                        text_to_draw = ""
                    
                    # 绘制文本内容
                    painter.drawText(int(x + 5), int(y + font_size * scale + 5), text_to_draw)
                else:
                    painter.drawText(int(x + 5), int(y + font_size * scale + 5), "Text")
                
                # 取消裁剪区域
                painter.setClipping(False)
        
        # 绘制网格（放在最上层）
        if self.show_grid:
            # 网格大小：5mm
            grid_size = 5
            
            # 设置虚线笔，使用grid_color属性
            pen = QPen(self.grid_color, 0.5, Qt.PenStyle.DotLine)
            painter.setPen(pen)
            
            # 绘制水平网格线（充满整个绘图区）
            grid_step = int(grid_size * scale)
            for y in range(0, int(self.height() * 2), grid_step):
                painter.drawLine(-self.width(), y, self.width() * 2, y)
                
                # 在下侧显示网格尺寸值
                if y > 0:
                    actual_y = y / scale
                    if actual_y % 10 == 0:  # 每10mm显示一次尺寸
                        painter.drawText(5, y + 10, f"{actual_y:.0f}mm")
            
            # 绘制垂直网格线（充满整个绘图区）
            for x in range(0, int(self.width() * 2), grid_step):
                painter.drawLine(x, -self.height(), x, self.height() * 2)
                
                # 在左侧显示网格尺寸值
                if x > 0:
                    actual_x = x / scale
                    if actual_x % 10 == 0:  # 每10mm显示一次尺寸
                        painter.drawText(x - 20, 15, f"{actual_x:.0f}mm")

    def mousePressEvent(self, event):
        """鼠标按下事件"""

        
        if event.button() == Qt.MouseButton.MiddleButton:
            # 开始平移

            self.is_panning = True
            self.pan_start = event.pos()
            # 鼠标指针变为手型
            self.setCursor(Qt.CursorShape.OpenHandCursor)
        elif event.button() == Qt.MouseButton.LeftButton:
            # 计算缩放比例
            label_width = self.template.template['label_size']['width']
            label_height = self.template.template['label_size']['height']
            base_scale = min(self.width() / (label_width + 20), self.height() / (label_height + 20))
            scale = base_scale * self.zoom
            x_offset = (self.width() - label_width * scale) / 2
            y_offset = (self.height() - label_height * scale) / 2
            
            # 检查是否点击了对象
            clicked_obj = None
            objects = self.template.get_objects()

            
            # 获取原始鼠标位置
            raw_mouse_x = event.pos().x()
            raw_mouse_y = event.pos().y()
            
            # 计算缩放比例和偏移（与paintEvent保持一致）
            label_width = self.template.template['label_size']['width']
            label_height = self.template.template['label_size']['height']
            # 使用与paintEvent相同的边距计算
            base_scale = min(self.width() / (label_width + 6), self.height() / (label_height + 6))
            scale = base_scale * self.zoom
            x_offset = (self.width() - label_width * scale) / 2
            y_offset = (self.height() - label_height * scale) / 2
            
            # 计算考虑平移和缩放后的鼠标位置
            # 先减去偏移，再考虑平移
            adjusted_mouse_x = raw_mouse_x - x_offset - self.pan_offset.x()
            adjusted_mouse_y = raw_mouse_y - y_offset - self.pan_offset.y()
            

            
            # 从后往前遍历，确保上层对象先被检测
            for i in reversed(range(len(objects))):
                obj = objects[i]
                # 计算对象的实际边界（以像素为单位）
                obj_x = obj['position']['x'] * scale
                obj_y = obj['position']['y'] * scale
                obj_width = obj['size']['width'] * scale
                obj_height = obj['size']['height'] * scale
                
                # 计算对象的边界范围
                obj_left = obj_x
                obj_top = obj_y
                obj_right = obj_x + obj_width
                obj_bottom = obj_y + obj_height
                
                # 打印对象边界信息

                
                # 检查鼠标是否在对象范围内
                if obj_left <= adjusted_mouse_x <= obj_right and obj_top <= adjusted_mouse_y <= obj_bottom:
                    clicked_obj = obj

                    break
            
            if clicked_obj:
                # 设置选中对象

                self.selected_object = clicked_obj['id']
                # 设置拖动状态
                self.is_dragging = True
                self.drag_start = event.pos()
                # 强制重绘
                self.update()
                # 通知主窗口更新属性面板
                
                # 直接调用主窗口的update_property_panel方法
                if self.parent() and hasattr(self.parent(), 'update_property_panel'):

                    self.parent().update_property_panel()
                    print("===========================================")
                else:
                    # 尝试通过其他方式获取主窗口
                    main_window = self.window()
                    if main_window and hasattr(main_window, 'update_property_panel'):

                        main_window.update_property_panel()

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
        # 实时更新状态栏显示鼠标坐标
        if hasattr(self.parent(), 'statusBar'):
            # 计算缩放比例
            label_width = self.template.template['label_size']['width']
            label_height = self.template.template['label_size']['height']
            base_scale = min(self.width() / (label_width + 20), self.height() / (label_height + 20))
            scale = base_scale * self.zoom
            x_offset = (self.width() - label_width * scale) / 2
            y_offset = (self.height() - label_height * scale) / 2
            
            # 计算鼠标在设计区中的坐标
            if scale > 0:
                design_x = (event.pos().x() - x_offset - self.pan_offset.x()) / scale
                design_y = (event.pos().y() - y_offset - self.pan_offset.y()) / scale
                # 更新状态栏
                self.parent().statusBar.showMessage(f"鼠标坐标: ({design_x:.2f}, {design_y:.2f}) mm")
        
        if self.is_panning:
            # 计算平移偏移
            delta = event.pos() - self.pan_start
            self.pan_offset += delta
            self.pan_start = event.pos()
            # 强制重绘
            self.update()
        elif self.is_dragging:
            # 计算缩放比例
            label_width = self.template.template['label_size']['width']
            label_height = self.template.template['label_size']['height']
            base_scale = min(self.width() / (label_width + 20), self.height() / (label_height + 20))
            scale = base_scale * self.zoom
            x_offset = (self.width() - label_width * scale) / 2
            y_offset = (self.height() - label_height * scale) / 2
            
            # 计算新位置
            delta = event.pos() - self.drag_start
            delta_x = delta.x() / scale
            delta_y = delta.y() / scale
            
            # 更新对象位置
            if self.selected_object:
                obj = self.template.get_object(self.selected_object)
                if obj:
                    new_x = obj['position']['x'] + delta_x
                    new_y = obj['position']['y'] + delta_y
                    # 确保对象不超出标签边界
                    label_width = self.template.template['label_size']['width']
                    label_height = self.template.template['label_size']['height']
                    new_x = max(0, min(new_x, label_width - obj['size']['width']))
                    new_y = max(0, min(new_y, label_height - obj['size']['height']))
                    
                    # 更新对象位置
                    obj['position']['x'] = new_x
                    obj['position']['y'] = new_y
                    
                    # 强制重绘
                    self.update()
                    
                    # 更新状态栏信息
                    if hasattr(self.parent(), 'statusBar'):
                        self.parent().statusBar.showMessage(f"正在移动对象: ({new_x:.2f}, {new_y:.2f})")
            
            # 更新拖动起点
            self.drag_start = event.pos()

    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == Qt.MouseButton.MiddleButton:
            # 结束平移
            self.is_panning = False
            # 鼠标指针恢复为默认形状
            self.setCursor(Qt.CursorShape.ArrowCursor)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False
            # 通知主窗口更新整个属性面板
            if self.parent() and hasattr(self.parent(), 'update_property_panel'):
                self.parent().update_property_panel()
            else:
                # 尝试通过其他方式获取主窗口
                main_window = self.window()
                if main_window and hasattr(main_window, 'update_property_panel'):
                    main_window.update_property_panel()
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
    
    def wheelEvent(self, event):
        """鼠标滚轮事件，实现缩放功能"""
        # 检查是否按住Ctrl键
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # 计算缩放因子
            delta = event.angleDelta().y() / 120
            zoom_factor = 1.1 if delta > 0 else 0.9
            
            # 计算新的缩放比例
            new_zoom = self.zoom * zoom_factor
            
            # 限制缩放范围
            new_zoom = max(0.3, min(new_zoom, 3.0))  # 最小30%，最大300%
            
            if new_zoom != self.zoom:
                self.zoom = new_zoom
                self.update()
                
                # 在状态栏显示放大倍数
                if hasattr(self.parent(), 'statusBar'):
                    zoom_percent = int(self.zoom * 100)
                    self.parent().statusBar.showMessage(f"缩放: {zoom_percent}%")

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
  
        # 设置窗口图标
        import os
        icon_f = os.path.join(os.path.dirname(__file__), "icon_path/sw-icon.ico")
        if os.path.exists(icon_f):
            from PyQt5.QtGui import QIcon
            self.setWindowIcon(QIcon(icon_f))      
  
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
        
        # 网格选项
        self.grid_action = QAction("网格", self)
        self.grid_action.setCheckable(True)
        self.grid_action.triggered.connect(self.toggle_grid)
        settings_menu.addAction(self.grid_action)

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
        
        # 添加保存选项，支持快捷键 Ctrl+S
        quick_save_action = QAction("保存", self)
        quick_save_action.setShortcut("Ctrl+S")
        quick_save_action.triggered.connect(self.quick_save)
        file_menu.addAction(quick_save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 导入菜单
        import_menu = menubar.addMenu("导入")
        
        import_csv_action = QAction("csv批量导入", self)
        import_csv_action.setToolTip("大量数据时导入更快，但是容易因逗号错行")
        import_csv_action.setStatusTip("大量数据时导入更快，但是容易因逗号错行")
        import_csv_action.triggered.connect(self.import_csv)
        import_menu.addAction(import_csv_action)
        
        # 添加导入Excel功能
        import_excel_action = QAction("xlsx批量导入(推荐)", self)
        import_excel_action.triggered.connect(self.import_excel)
        import_menu.addAction(import_excel_action)
        
        # 导出菜单
        export_menu = menubar.addMenu("导出")
        
        export_current_action = QAction("导出当前标签为PNG", self)
        export_current_action.triggered.connect(self.export_current)
        export_menu.addAction(export_current_action)
        
        batch_export_action = QAction("批量导出", self)
        batch_export_action.triggered.connect(self.batch_export)
        export_menu.addAction(batch_export_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        # 添加回退和重做按钮
        self.undo_action = QAction("回退", self)
        self.undo_action.triggered.connect(self.undo)
        self.undo_action.setEnabled(False)
        menubar.addAction(self.undo_action)
        
        self.redo_action = QAction("重做", self)
        self.redo_action.triggered.connect(self.redo)
        self.redo_action.setEnabled(False)
        menubar.addAction(self.redo_action)
        
        # 初始化操作历史记录
        self.history = []
        self.history_index = -1
        self.max_history = 8
        
        # 初始化当前模板文件名
        self.current_template_file = None
        
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
        
        # 设计区 - 扩大比例
        self.designer = LabelDesigner()
        content_layout.addWidget(self.designer, 3)  # 增加权重，扩大设计区
        
        # 添加间距 - 3mm左右
        content_layout.addSpacing(10)  # 添加10像素间距，约3mm
        
        # 属性面板
        self.property_panel = PropertyPanel()
        self.property_panel.setMinimumWidth(300)  # 设置最小宽度
        self.property_panel.setMaximumWidth(300)  # 设置最大宽度，锁定宽度
        content_layout.addWidget(self.property_panel)
        
        main_layout.addLayout(content_layout)
        
        # 信号连接
        self.toolbar.qr_button.clicked.connect(self.on_qr_button_clicked)
        self.toolbar.text_button.clicked.connect(self.on_text_button_clicked)
        self.property_panel.save_button.clicked.connect(self.on_save_properties)
        self.property_panel.qr_batch_checkbox.stateChanged.connect(self.on_batch_checkbox_changed)
        self.property_panel.text_batch_checkbox.stateChanged.connect(self.on_text_batch_checkbox_changed)
        self.property_panel.color_button.clicked.connect(self.on_color_button_clicked)
        self.property_panel.qr_version_combo.currentTextChanged.connect(self.on_qr_version_changed)
        self.property_panel.error_correction_combo.currentTextChanged.connect(self.on_error_correction_changed)
        
        # 初始化网格状态
        self.designer.show_grid = True
        self.grid_action.setChecked(True)
        
        # 文本样式复选框信号连接
        self.property_panel.bold_checkbox.stateChanged.connect(self.on_save_properties)
        self.property_panel.italic_checkbox.stateChanged.connect(self.on_save_properties)
        self.property_panel.underline_checkbox.stateChanged.connect(self.on_save_properties)
        
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
            # 设置网格颜色
            if 'grid_color' in settings:
                self.designer.grid_color = QColor(settings['grid_color'])
            self.designer.update()
            self.statusBar.showMessage("基础设置已更新")
    
    def new_template(self):
        """新建模板"""
        self.designer.template = LabelTemplate()
        self.designer.selected_object = None
        self.designer.update()
        self.current_template_file = None  # 新建模板时重置文件名
        self.statusBar.showMessage("已新建模板")
    
    def open_template(self):
        """打开模板"""
        # 获取保存的目录，默认为 d:/
        last_dir = self.config_manager.get_last_open_dir() or "d:/"
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开模板", last_dir, "Label Files (*.label)"
        )
        if file_path:
            # 更新保存的目录
            self.config_manager.set_last_open_dir(os.path.dirname(file_path))
            if self.designer.template.load_template(file_path):
                self.designer.selected_object = None
                self.designer.update()
                self.current_template_file = file_path  # 更新当前模板文件名
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
                self.current_template_file = file_path  # 更新当前模板文件名
                self.statusBar.showMessage(f"已保存模板: {file_path}")
            else:
                QMessageBox.warning(self, "错误", "保存模板失败")
    
    def quick_save(self):
        """快速保存当前模板，支持快捷键 Ctrl+S"""
        if self.current_template_file:
            # 如果已有保存的模板文件，直接保存
            if self.designer.template.save_template(self.current_template_file):
                self.statusBar.showMessage(f"已保存模板: {self.current_template_file}")
            else:
                QMessageBox.warning(self, "错误", "保存模板失败")
        else:
            # 如果是新模板，调用保存模板功能
            self.save_template()
    
    def toggle_grid(self):
        """切换网格显示状态"""
        self.designer.show_grid = self.grid_action.isChecked()
        self.designer.update()
        if self.designer.show_grid:
            self.statusBar.showMessage("网格已打开")
        else:
            self.statusBar.showMessage("网格已关闭")
    
    def import_csv(self):
        """导入CSV"""
        # 获取保存的导入目录，默认为 d:/
        last_import_dir = self.config_manager.get_last_import_dir() or "d:/"
        file_path, _ = QFileDialog.getOpenFileName(
            self, "导入CSV", last_import_dir, "CSV Files (*.csv)"
        )
        if file_path:
            # 更新保存的导入目录
            self.config_manager.set_last_import_dir(os.path.dirname(file_path))
            if self.csv_handler.import_csv(file_path):
                # 显示预览对话框
                dialog = CSVPreviewDialog(self.csv_handler, self)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    # 更新属性面板中的CSV列
                    columns = self.csv_handler.get_columns()
                    self.property_panel.update_qr_csv_columns(columns)
                    self.property_panel.update_text_csv_columns(columns)
                    self.statusBar.showMessage(f"已导入CSV: {file_path}")
            else:
                QMessageBox.warning(self, "错误", "导入CSV失败")

    def import_excel(self):
        """导入Excel"""
        # 提示用户只导入第一个sheet的数据
        QMessageBox.information(self, "提示", "只导入第一个sheet的数据，默认第一行为列名")
        
        # 获取保存的导入目录，默认为 d:/
        last_import_dir = self.config_manager.get_last_import_dir() or "d:/"
        file_path, _ = QFileDialog.getOpenFileName(
            self, "导入Excel", last_import_dir, "Excel Files (*.xlsx *.xls)"
        )
        if file_path:
            # 更新保存的导入目录
            self.config_manager.set_last_import_dir(os.path.dirname(file_path))
            if self.csv_handler.import_excel(file_path):
                # 显示预览对话框
                dialog = CSVPreviewDialog(self.csv_handler, self)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    # 更新属性面板中的CSV列
                    columns = self.csv_handler.get_columns()
                    self.property_panel.update_qr_csv_columns(columns)
                    self.property_panel.update_text_csv_columns(columns)
                    self.statusBar.showMessage(f"已导入Excel: {file_path}")
            else:
                QMessageBox.warning(self, "错误", "导入Excel失败")
    
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
        obj_id = self.designer.add_qr_object(x, y)
        self.property_panel.show_qr_properties()

        self.update_property_panel()
        
        # 记录操作历史
        obj = self.designer.template.get_object(obj_id)
        if obj:
            import copy
            self.record_history("add", {"obj_id": obj_id, "obj_data": copy.deepcopy(obj)})
    
    def on_text_button_clicked(self):
        """点击文本按钮"""
        # 在设计区中心添加文本对象
        label_width = self.designer.template.template['label_size']['width']
        label_height = self.designer.template.template['label_size']['height']
        x = (label_width - 30) / 2
        y = (label_height - 10) / 2
        obj_id = self.designer.add_text_object(x, y)
        
        # 记录操作历史
        obj = self.designer.template.get_object(obj_id)
        if obj:
            import copy
            self.record_history("add", {"obj_id": obj_id, "obj_data": copy.deepcopy(obj)})
        self.property_panel.show_text_properties()

        self.update_property_panel()
    
    def on_save_properties(self):
        """保存属性"""
        obj = self.designer.get_selected_object()
        if obj:
            # 记录操作历史 - 保存旧属性
            import copy
            old_data = copy.deepcopy(obj)
            
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
                    'batch': self.property_panel.qr_batch_checkbox.isChecked(),
                    'csv_column': self.property_panel.qr_csv_column_combo.currentText()
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
            
            # 记录操作历史 - 保存新属性
            new_obj = self.designer.get_selected_object()
            if new_obj:
                new_data = copy.deepcopy(new_obj)
                self.record_history("update", {
                    "obj_id": obj['id'],
                    "old_data": old_data,
                    "new_data": new_data
                })
            
            # 强制重绘设计区，确保显示最新信息
            self.designer.update()
            
            self.statusBar.showMessage("属性已保存")
    
    def update_property_panel(self):
        """更新属性面板"""
        # 获取调用者信息
        import inspect
        caller_frame = inspect.currentframe().f_back
        caller_function = inspect.getframeinfo(caller_frame).function


        # 强制获取最新的选中对象
        selected_id = self.designer.selected_object

        
        # 直接从模板中获取对象，而不是通过get_selected_object
        objects = self.designer.template.get_objects()

        
        obj = None
        for o in objects:
            if o['id'] == selected_id:
                obj = o
                break
        # 初始化变量
        csv_column_from_obj = ""
        batch_status = False
        
        if obj:


            
            # 提前获取CSV列值和批量生成状态，以防后续操作影响
            csv_column_from_obj = obj['properties'].get('csv_column', '')
            batch_status = obj['properties'].get('batch', False)
            
            if obj['type'] == 'text':
                pass

            elif obj['type'] == 'qr':


        
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
            
            # 暂时断开所有可能触发 on_save_properties 的信号连接

            
            # 断开文本样式复选框信号
            try:
                self.property_panel.bold_checkbox.stateChanged.disconnect(self.on_save_properties)
                self.property_panel.italic_checkbox.stateChanged.disconnect(self.on_save_properties)
                self.property_panel.underline_checkbox.stateChanged.disconnect(self.on_save_properties)
            except:
                pass
            
            # 断开输入框信号
            try:
                self.property_panel.x_input.editingFinished.disconnect(self.on_save_properties)
                self.property_panel.y_input.editingFinished.disconnect(self.on_save_properties)
                self.property_panel.width_input.editingFinished.disconnect(self.on_save_properties)
                self.property_panel.height_input.editingFinished.disconnect(self.on_save_properties)
                self.property_panel.content_input.editingFinished.disconnect(self.on_save_properties)
                self.property_panel.text_content_input.editingFinished.disconnect(self.on_save_properties)
                self.property_panel.font_size_input.editingFinished.disconnect(self.on_save_properties)
            except:
                pass
            
            # 断开批量复选框信号
            if obj['type'] == 'qr':

                try:
                    self.property_panel.qr_batch_checkbox.stateChanged.disconnect(self.on_batch_checkbox_changed)
                except:
                    pass
            elif obj['type'] == 'text':

                try:
                    self.property_panel.text_batch_checkbox.stateChanged.disconnect(self.on_text_batch_checkbox_changed)
                except:
                    pass
            
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
                self.property_panel.qr_batch_checkbox.setChecked(batch_status)
                
                # 更新CSV列选择
                columns = self.csv_handler.get_columns()

                
                # 只有当下拉框为空时才更新选项，避免每次都重置下拉框
                if self.property_panel.qr_csv_column_combo.count() == 0:
                    self.property_panel.update_qr_csv_columns(columns)
                
                # 只有当csv_column不为空且在列列表中时才设置
                if csv_column_from_obj and csv_column_from_obj in columns:
                    self.property_panel.qr_csv_column_combo.setCurrentText(csv_column_from_obj)
                else:
                    # 如果csv_column为空或不在列列表中，设置为空字符串
                    self.property_panel.qr_csv_column_combo.setCurrentText("")
                    
                # 更新容量显示
                self.update_capacity_display(
                    obj['properties']['qr_version'],
                    obj['properties']['error_correction']
                )
                
                # 重新连接二维码批量复选框的信号

                self.property_panel.qr_batch_checkbox.stateChanged.connect(self.on_batch_checkbox_changed)
                
                # 重新连接所有信号

                # 重新连接文本样式复选框信号
                self.property_panel.bold_checkbox.stateChanged.connect(self.on_save_properties)
                self.property_panel.italic_checkbox.stateChanged.connect(self.on_save_properties)
                self.property_panel.underline_checkbox.stateChanged.connect(self.on_save_properties)
                # 重新连接输入框信号
                self.property_panel.x_input.editingFinished.connect(self.on_save_properties)
                self.property_panel.y_input.editingFinished.connect(self.on_save_properties)
                self.property_panel.width_input.editingFinished.connect(self.on_save_properties)
                self.property_panel.height_input.editingFinished.connect(self.on_save_properties)
                self.property_panel.content_input.editingFinished.connect(self.on_save_properties)
                self.property_panel.text_content_input.editingFinished.connect(self.on_save_properties)
                self.property_panel.font_size_input.editingFinished.connect(self.on_save_properties)
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
                self.property_panel.text_batch_checkbox.setChecked(batch_status)
                
                # 更新CSV列选择
                columns = self.csv_handler.get_columns()


                
                # 保存当前CSV列值
                current_csv_column = csv_column_from_obj

                
                # 只有当下拉框为空时才更新选项，避免每次都重置下拉框
                if self.property_panel.text_csv_column_combo.count() == 0:

                    self.property_panel.update_text_csv_columns(columns)
                
                # 根据批量生成状态启用/禁用CSV列选择，并设置相应的值
                if batch_status:

                    self.property_panel.text_csv_column_combo.setEnabled(True)
                    # 只有当csv_column不为空且在列列表中时才设置
                    if current_csv_column and current_csv_column in columns:

                        self.property_panel.text_csv_column_combo.setCurrentText(current_csv_column)
                    else:
                        # 如果csv_column为空或不在列列表中，设置为空字符串

                        self.property_panel.text_csv_column_combo.setCurrentText("")
                else:

                    self.property_panel.text_csv_column_combo.setEnabled(False)
                    # 当批量生成禁用时，强制设置为空字符串
                    self.property_panel.text_csv_column_combo.setCurrentText("")
                
                # 重新连接文本批量复选框的信号

                self.property_panel.text_batch_checkbox.stateChanged.connect(self.on_text_batch_checkbox_changed)
                
                # 重新连接所有信号

                # 重新连接文本样式复选框信号
                self.property_panel.bold_checkbox.stateChanged.connect(self.on_save_properties)
                self.property_panel.italic_checkbox.stateChanged.connect(self.on_save_properties)
                self.property_panel.underline_checkbox.stateChanged.connect(self.on_save_properties)
                # 重新连接输入框信号
                self.property_panel.x_input.editingFinished.connect(self.on_save_properties)
                self.property_panel.y_input.editingFinished.connect(self.on_save_properties)
                self.property_panel.width_input.editingFinished.connect(self.on_save_properties)
                self.property_panel.height_input.editingFinished.connect(self.on_save_properties)
                self.property_panel.content_input.editingFinished.connect(self.on_save_properties)
                self.property_panel.text_content_input.editingFinished.connect(self.on_save_properties)
                self.property_panel.font_size_input.editingFinished.connect(self.on_save_properties)
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
                    self.property_panel.qr_batch_checkbox.setChecked(False)
                else:
                    # 禁用内容输入
                    self.property_panel.content_input.setEnabled(False)
            else:
                # 启用内容输入
                self.property_panel.content_input.setEnabled(True)
        except Exception as e:
            print(f"批量生成复选框变化错误: {e}")
            # 确保复选框状态正确
            self.property_panel.qr_batch_checkbox.setChecked(False)
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
                    # 禁用内容输入，启用CSV列选择
                    self.property_panel.text_content_input.setEnabled(False)
                    self.property_panel.text_csv_column_combo.setEnabled(True)
            else:
                # 启用内容输入，禁用CSV列选择
                self.property_panel.text_content_input.setEnabled(True)
                self.property_panel.text_csv_column_combo.setEnabled(False)
        except Exception as e:
            print(f"文本批量生成复选框变化错误: {e}")
            # 确保复选框状态正确
            self.property_panel.text_batch_checkbox.setChecked(False)
            self.property_panel.text_content_input.setEnabled(True)
            self.property_panel.text_csv_column_combo.setEnabled(False)
    
    def on_color_button_clicked(self):
        """颜色选择按钮点击"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.property_panel.color_preview.setStyleSheet(f"background-color: {color.name()};")
    
    def delete_selected(self):
        """删除选中对象"""
        if self.designer.selected_object:
            # 记录操作历史
            obj = self.designer.template.get_object(self.designer.selected_object)
            if obj:
                import copy
                self.record_history("delete", {"obj_id": self.designer.selected_object, "obj_data": copy.deepcopy(obj)})
            
            self.designer.remove_selected_object()

            self.update_property_panel()
            self.statusBar.showMessage("已删除选中对象")
    
    def keyPressEvent(self, event):
        """键盘按下事件"""
        if event.key() == Qt.Key_Delete:
            self.delete_selected()
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 保存配置
        self.config_manager.save_config()
        event.accept()
    
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
        
        # 获取选择的导出格式
        export_format = dialog.get_selected_format()
        
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
        pdf_filename = None
        if export_format == "pdf":
            # 使用模板文件名作为PDF文件名
            if self.current_template_file:
                # 从模板文件路径中提取文件名（不含扩展名）
                import os
                pdf_filename = os.path.splitext(os.path.basename(self.current_template_file))[0]
            else:
                # 模板尚未保存，使用默认文件名
                pdf_filename = "notsavedTemplate"
        
        results = self.image_processor.batch_process(template, csv_data, output_dir, export_format, pdf_filename)
        
        # 完成
        if csv_data is not None:
            dialog.progress.setValue(len(csv_data))
        else:
            dialog.progress.setValue(100)
        QApplication.processEvents()  # 确保进度条更新
        
        # 根据导出格式显示不同的完成信息
        if export_format == "png":
            QMessageBox.information(self, "完成", f"已生成 {len(results)} 个PNG标签")
        else:
            QMessageBox.information(self, "完成", f"已生成 PDF 文件，包含 {len(csv_data)} 个标签")
        
        dialog.accept()
        self.statusBar.showMessage(f"批量导出完成，生成 {len(results)} 个文件")
    
    def resizeEvent(self, event):
        """窗口大小变化事件"""
        super().resizeEvent(event)
        # 主窗口大小变化时，设计器会自动更新，因为它已经有了resizeEvent处理
    
    def show_about(self):
        about_text = (
            f"Python 批量二维码标签生成器\n"
            f"版本：{VERSION}\t{RELEASE_DATE}\n"
            f"作者：{AUTHOR}\n"
            f"邮箱：{EMAIL}\n"
            f"GitHub：{GITHUB}\n\n"
            f"Copyright (C) 2026\n\n"
            f"This program is free software: you can redistribute it and/or modify\n"
            f"it under the terms of the GNU General Public License as published by\n"
            f"the Free Software Foundation, either version 3 of the License, or\n"
            f"(at your option) any later version."
        )
        QMessageBox.information(self, "关于", about_text)
    
    def record_history(self, action_type, data):
        """记录操作历史"""
        # 截断历史记录到当前索引
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        
        # 添加新操作
        self.history.append({"type": action_type, "data": data})
        
        # 限制历史记录长度
        if len(self.history) > self.max_history:
            self.history.pop(0)
        else:
            self.history_index += 1
        
        # 更新回退/重做按钮状态
        self.update_history_buttons()
    
    def update_history_buttons(self):
        """更新回退/重做按钮状态"""
        self.undo_action.setEnabled(self.history_index >= 0)
        self.redo_action.setEnabled(self.history_index < len(self.history) - 1)
    
    def undo(self):
        """回退操作"""
        if self.history_index >= 0:
            action = self.history[self.history_index]
            self.history_index -= 1
            
            if action["type"] == "add":
                # 回退添加操作 - 删除对象
                obj_id = action["data"]["obj_id"]
                self.designer.template.remove_object(obj_id)
            elif action["type"] == "delete":
                # 回退删除操作 - 重新添加对象
                obj_data = action["data"]["obj_data"]
                # 重建对象
                if obj_data["type"] == "qr":
                    self.designer.template.template["objects"].append(obj_data)
                elif obj_data["type"] == "text":
                    self.designer.template.template["objects"].append(obj_data)
            elif action["type"] == "update":
                # 回退更新操作 - 恢复旧属性
                obj_id = action["data"]["obj_id"]
                old_data = action["data"]["old_data"]
                obj = self.designer.template.get_object(obj_id)
                if obj:
                    obj.update(old_data)
            
            self.designer.selected_object = None
            self.designer.update()

            self.update_property_panel()
            self.update_history_buttons()
            self.statusBar.showMessage("已回退操作")
    
    def redo(self):
        """重做操作"""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            action = self.history[self.history_index]
            
            if action["type"] == "add":
                # 重做添加操作 - 重新添加对象
                obj_data = action["data"]["obj_data"]
                self.designer.template.template["objects"].append(obj_data)
            elif action["type"] == "delete":
                # 重做删除操作 - 删除对象
                obj_id = action["data"]["obj_id"]
                self.designer.template.remove_object(obj_id)
            elif action["type"] == "update":
                # 重做更新操作 - 应用新属性
                obj_id = action["data"]["obj_id"]
                new_data = action["data"]["new_data"]
                obj = self.designer.template.get_object(obj_id)
                if obj:
                    obj.update(new_data)
            
            self.designer.selected_object = None
            self.designer.update()

            self.update_property_panel()
            self.update_history_buttons()
            self.statusBar.showMessage("已重做操作")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
