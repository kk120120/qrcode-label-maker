"""
L1 入口层 - 设计器画布UI组件
功能：接收用户鼠标、键盘事件，转发给入口层，显示绘制结果
文件：entry/ui_window/designer_canvas.py
"""

from typing import Optional, Dict, Any
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QPoint, QPointF


class LabelDesigner(QWidget):
    """标签设计器 - UI组件

    职责：
    - 接收用户鼠标、键盘事件
    - 转发事件给入口层
    - 显示绘制结果
    """

    def __init__(self, parent=None):
        """标签设计器初始化

        Args:
            parent: 父窗口
        """
        super().__init__(parent)
        self.main_window = parent
        self.setMinimumSize(600, 400)

        # 选中的对象ID
        self.selected_object: Optional[str] = None
        # 是否正在拖拽对象
        self.is_dragging: bool = False
        # 拖拽起始点
        self.drag_start: QPoint = QPoint()
        # 是否显示网格
        self.show_grid: bool = True
        # 网格颜色
        self.grid_color: QColor = QColor(0, 255, 0)  # 绿色
        # 网格线型
        self.grid_line_style: Qt.PenStyle = Qt.PenStyle.DashLine  # 虚线
        # 缩放比例
        self.zoom: float = 1.0
        # 平移偏移量
        self.pan_offset: QPointF = QPointF(0, 0)
        # 是否正在平移
        self.is_panning: bool = False
        # 平移起始点
        self.pan_start: QPointF = QPointF()
        # 启用鼠标追踪
        self.setMouseTracking(True)

    def paintEvent(self, event):
        """绘制事件 - 调用入口层绘制所有内容

        Args:
            event: 绘制事件对象
        """
        painter = QPainter(self)
        if self.main_window and hasattr(self.main_window, 'ui_entry'):
            template = self.main_window.ui_entry.entry_get_template()
            out_of_bounds = self.main_window.ui_entry.entry_check_boundaries()
            objects = self.main_window.ui_entry.entry_get_objects()
            scale, x_offset, y_offset = self.calculate_transform(template)
            self.main_window.ui_entry.entry_draw_all(
                painter, template, objects, self.selected_object, out_of_bounds,
                self.width(), self.height(), scale, x_offset, y_offset,
                self.show_grid, self.grid_color, self.grid_line_style
            )

    def calculate_transform(self, template):
        """计算缩放和偏移变换

        Args:
            template: 模板数据

        Returns:
            tuple: (scale, x_offset, y_offset)
        """
        label_width = template['label_size']['width']
        label_height = template['label_size']['height']
        base_scale = min(self.width() / (label_width + 20), self.height() / (label_height + 20))
        scale = base_scale * self.zoom
        x_offset = (self.width() - label_width * scale) / 2 + self.pan_offset.x()
        y_offset = (self.height() - label_height * scale) / 2 + self.pan_offset.y()
        return scale, x_offset, y_offset

    def mousePressEvent(self, event):
        """鼠标按下事件 - 处理中键平移和左键选择/拖拽对象

        Args:
            event: 鼠标事件对象
        """
        if event.button() == Qt.MouseButton.MiddleButton:
            self.is_panning = True
            self.pan_start = event.pos()
            self.setCursor(Qt.CursorShape.OpenHandCursor)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.handle_left_button_press(event)

    def handle_left_button_press(self, event):
        """处理左键按下 - 选择或准备拖拽对象

        Args:
            event: 鼠标事件对象
        """
        if not (self.main_window and hasattr(self.main_window, 'ui_entry')):
            return

        template = self.main_window.ui_entry.entry_get_template()
        objects = self.main_window.ui_entry.entry_get_objects()
        scale, x_offset, y_offset = self.calculate_transform(template)

        clicked_object = self.detect_clicked_object(event.pos(), objects, scale, x_offset, y_offset)

        if clicked_object:
            self.selected_object = clicked_object['id']
            self.is_dragging = True
            self.drag_start = event.pos()
            if hasattr(self.main_window, 'update_property_panel'):
                self.main_window.update_property_panel()
        else:
            self.selected_object = None
            if hasattr(self.main_window, 'update_property_panel'):
                self.main_window.update_property_panel()
        self.update()

    def detect_clicked_object(self, pos, objects, scale, x_offset, y_offset):
        """检测点击的对象

        Args:
            pos: 鼠标位置
            objects: 对象列表
            scale: 缩放比例
            x_offset: X偏移
            y_offset: Y偏移

        Returns:
            点击的对象，如果没有则返回None
        """
        for obj in reversed(objects):
            obj_x = x_offset + obj['position']['x'] * scale
            obj_y = y_offset + obj['position']['y'] * scale
            obj_w = obj['size']['width'] * scale
            obj_h = obj['size']['height'] * scale
            if obj_x <= pos.x() <= obj_x + obj_w and obj_y <= pos.y() <= obj_y + obj_h:
                return obj
        return None

    def mouseMoveEvent(self, event):
        """鼠标移动事件 - 更新状态栏坐标、平移或拖拽对象

        Args:
            event: 鼠标事件对象
        """
        self.update_status_bar_position(event.pos())

        if self.is_panning:
            self.handle_panning(event.pos())
        elif self.is_dragging:
            self.handle_dragging(event.pos())

    def update_status_bar_position(self, pos):
        """更新状态栏显示鼠标坐标

        Args:
            pos: 鼠标位置
        """
        if not (hasattr(self.main_window, 'statusBar') and hasattr(self.main_window, 'ui_entry')):
            return

        template = self.main_window.ui_entry.entry_get_template()
        scale, x_offset, y_offset = self.calculate_transform(template)

        if scale > 0:
            design_x = (pos.x() - x_offset) / scale
            design_y = (pos.y() - y_offset) / scale
            self.main_window.statusBar().showMessage(f"鼠标坐标: ({design_x:.2f}, {design_y:.2f}) mm")

    def handle_panning(self, pos):
        """处理平移

        Args:
            pos: 鼠标位置
        """
        delta = pos - self.pan_start
        self.pan_offset += delta
        self.pan_start = pos
        self.update()

    def handle_dragging(self, pos):
        """处理拖拽对象

        Args:
            pos: 鼠标位置（画布像素坐标）
        """
        if not (self.main_window and hasattr(self.main_window, 'ui_entry')):
            return

        if not self.selected_object:
            return

        obj = self.main_window.ui_entry.entry_get_object(self.selected_object)
        if not obj:
            return

        template = self.main_window.ui_entry.entry_get_template()
        scale, x_offset, y_offset = self.calculate_transform(template)

        delta = pos - self.drag_start
        delta_x = delta.x() / scale
        delta_y = delta.y() / scale

        current_x = obj['position']['x']
        current_y = obj['position']['y']

        new_x = current_x + delta_x
        new_y = current_y + delta_y

        self.main_window.ui_entry.entry_update_object(self.selected_object, x=new_x, y=new_y)
        self.update()
        if hasattr(self.main_window, 'statusBar'):
            self.main_window.statusBar().showMessage(f"正在移动对象: ({new_x:.2f}, {new_y:.2f})")

        self.drag_start = pos

    def mouseReleaseEvent(self, event):
        """鼠标释放事件 - 结束平移或拖拽

        Args:
            event: 鼠标事件对象
        """
        if event.button() == Qt.MouseButton.MiddleButton:
            self.is_panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False
            if hasattr(self.main_window, 'update_property_panel'):
                self.main_window.update_property_panel()
            if hasattr(self.main_window, 'statusBar'):
                self.main_window.statusBar().clearMessage()

    def keyPressEvent(self, event):
        """键盘事件 - 方向键移动对象，Delete键删除对象

        Args:
            event: 键盘事件对象
        """
        if not (self.selected_object and hasattr(self.main_window, 'ui_entry')):
            return

        obj = self.main_window.ui_entry.entry_get_object(self.selected_object)
        if not obj:
            return

        step = 0.1
        if event.key() == Qt.Key.Key_Left:
            new_x = obj['position']['x'] - step
            self.main_window.ui_entry.entry_update_object(self.selected_object, x=new_x)
        elif event.key() == Qt.Key.Key_Right:
            new_x = obj['position']['x'] + step
            self.main_window.ui_entry.entry_update_object(self.selected_object, x=new_x)
        elif event.key() == Qt.Key.Key_Up:
            new_y = obj['position']['y'] - step
            self.main_window.ui_entry.entry_update_object(self.selected_object, y=new_y)
        elif event.key() == Qt.Key.Key_Down:
            new_y = obj['position']['y'] + step
            self.main_window.ui_entry.entry_update_object(self.selected_object, y=new_y)
        elif event.key() == Qt.Key.Key_Delete:
            self.main_window.save_to_history()
            self.main_window.ui_entry.entry_remove_object(self.selected_object)
            self.selected_object = None
            self.update()
            if hasattr(self.main_window, 'update_property_panel'):
                self.main_window.update_property_panel()

    def wheelEvent(self, event):
        """滚轮事件 - Ctrl+滚轮缩放

        Args:
            event: 滚轮事件对象
        """
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.zoom *= 1.1
            else:
                self.zoom *= 0.9
            self.zoom = max(0.1, min(10, self.zoom))
            self.update()

    def add_qr_object(self, x: float, y: float):
        """添加二维码对象

        Args:
            x: x坐标
            y: y坐标
        """
        if hasattr(self.main_window, 'ui_entry'):
            self.main_window.save_to_history()
            obj_id = self.main_window.ui_entry.entry_add_qr_object(x, y)
            self.selected_object = obj_id
            self.update()
            if hasattr(self.main_window, 'update_property_panel'):
                self.main_window.update_property_panel()

    def add_text_object(self, x: float, y: float):
        """添加文本对象

        Args:
            x: x坐标
            y: y坐标
        """
        if hasattr(self.main_window, 'ui_entry'):
            self.main_window.save_to_history()
            obj_id = self.main_window.ui_entry.entry_add_text_object(x, y)
            self.selected_object = obj_id
            self.update()
            if hasattr(self.main_window, 'update_property_panel'):
                self.main_window.update_property_panel()

    def get_selected_object(self) -> Optional[Dict[str, Any]]:
        """获取选中的对象

        Returns:
            选中的对象数据，如果没有选中则返回None
        """
        if self.selected_object and hasattr(self.main_window, 'ui_entry'):
            return self.main_window.ui_entry.entry_get_object(self.selected_object)
        return None

    def update_selected_object(self, **kwargs):
        """更新选中的对象

        Args:
            **kwargs: 要更新的属性
        """
        if self.selected_object and hasattr(self.main_window, 'ui_entry'):
            self.main_window.ui_entry.entry_update_object(self.selected_object, **kwargs)
            self.update()

    def remove_selected_object(self):
        """移除选中的对象"""
        if self.selected_object and hasattr(self.main_window, 'ui_entry'):
            self.main_window.ui_entry.entry_remove_object(self.selected_object)
            self.selected_object = None
            self.update()
