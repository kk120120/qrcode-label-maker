"""
L4 原子层 - 绘制操作
功能：提供绘制相关的纯函数原子操作
文件：atom/atom_draw.py
"""

from typing import Dict, Any, List, Optional, Callable
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt
from atom.atom_qr import atom_qr_generate


def atom_draw_label(painter: QPainter, template: Dict[str, Any], scale: float, x_offset: float, y_offset: float) -> None:
    """绘制标签

    Args:
        painter: 画笔对象
        template: 模板数据
        scale: 缩放比例
        x_offset: X偏移
        y_offset: Y偏移
    """
    label_width = template['label_size']['width'] * scale
    label_height = template['label_size']['height'] * scale
    corner_radius = template['label_size']['corner_radius'] * scale

    # 绘制标签背景
    painter.setBrush(QColor(255, 255, 255))
    painter.setPen(QColor(200, 200, 200))
    painter.drawRoundedRect(
        int(x_offset), int(y_offset),
        int(label_width), int(label_height),
        corner_radius, corner_radius
    )


def atom_draw_objects(painter: QPainter, objects: List[Dict[str, Any]], selected_object: str, out_of_bounds: List[str], scale: float, x_offset: float, y_offset: float, dpi: int, get_first_row_value: Optional[Callable[[str], Optional[str]]] = None) -> None:
    """绘制对象

    Args:
        painter: 画笔对象
        objects: 对象列表
        selected_object: 选中的对象ID
        out_of_bounds: 超出边界的对象ID列表
        scale: 缩放比例
        x_offset: X偏移
        y_offset: Y偏移
        dpi: 分辨率
        get_first_row_value: 获取第一行数据的回调函数（可选）
    """
    for obj in objects:
        obj_id = obj['id']
        x = x_offset + obj['position']['x'] * scale
        y = y_offset + obj['position']['y'] * scale
        width = obj['size']['width'] * scale
        height = obj['size']['height'] * scale

        # 绘制超出边界警告
        if obj_id in out_of_bounds:
            painter.setBrush(QColor(255, 0, 0, 20))
            painter.setPen(QColor(255, 0, 0))
            painter.drawRect(int(x), int(y), int(width), int(height))

        # 绘制对象边框
        if obj_id == selected_object:
            painter.setPen(QColor(0, 120, 215))
            painter.setBrush(QColor(0, 120, 215, 20))
        else:
            painter.setPen(QColor(150, 150, 150))
            painter.setBrush(QColor(200, 200, 200, 50))
        painter.drawRect(int(x), int(y), int(width), int(height))

        # 绘制对象内容
        if obj['type'] == 'qr':
            content = obj.get('content', '')
            # 如果是批量生成且有数据列，使用第一行数据
            batch = obj.get('batch', False)
            csv_column = obj.get('csv_column', '')
            if batch and csv_column and get_first_row_value:
                first_value = get_first_row_value(csv_column)
                if first_value:
                    content = first_value
            
            qr_img = atom_qr_generate(
                content,
                obj.get('error_correction', 'Q'),
                obj.get('qr_version', '21x21')
            )
            if qr_img:
                # 在PyQt5中绘制PIL图像
                from PyQt5.QtGui import QPixmap, QImage
                qt_img = qr_img.convert("RGBA")
                qt_img_data = qt_img.tobytes("raw", "RGBA")
                qt_pixmap = QPixmap.fromImage(
                    QImage(qt_img_data, qt_img.width, qt_img.height, QImage.Format_RGBA8888)
                )
                painter.drawPixmap(
                    int(x), int(y),
                    qt_pixmap.scaled(int(width), int(height), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
            else:
                # 绘制占位符
                painter.setPen(QColor(100, 100, 100))
                painter.setFont(QFont("Arial", int(10 * scale)))
                painter.drawText(int(x), int(y), int(width), int(height), Qt.AlignCenter, "QR Code")

        elif obj['type'] == 'text':
            content = obj.get('content', '')
            # 如果是批量生成且有数据列，使用第一行数据
            batch = obj.get('batch', False)
            csv_column = obj.get('csv_column', '')
            if batch and csv_column and get_first_row_value:
                first_value = get_first_row_value(csv_column)
                if first_value:
                    content = first_value
            
            font_size = obj.get('font_size', 3) * scale
            font = QFont(obj.get('font', 'Arial'), int(font_size))

            font_style = obj.get('font_style', ['normal'])
            if 'bold' in font_style:
                font.setBold(True)
            if 'italic' in font_style:
                font.setItalic(True)
            if 'underline' in font_style:
                font.setUnderline(True)

            text_align = obj.get('text_align', 'left')
            vertical_align = obj.get('vertical_align', 'top')

            h_align_flags = {
                'left': Qt.AlignLeft,
                'center': Qt.AlignHCenter,
                'right': Qt.AlignRight
            }.get(text_align, Qt.AlignLeft)

            v_align_flags = {
                'top': Qt.AlignTop,
                'middle': Qt.AlignVCenter,
                'bottom': Qt.AlignBottom
            }.get(vertical_align, Qt.AlignTop)

            align_flags = h_align_flags | v_align_flags

            painter.setPen(QColor(obj.get('color', '#000000')))
            painter.setFont(font)
            
            font_metrics = painter.fontMetrics()
            line_height = font_metrics.height()
            lines = _wrap_text(content, painter, font, int(width))
            total_text_height = len(lines) * line_height
            
            if vertical_align == 'middle':
                start_y = int(y) + (int(height) - total_text_height) // 2
            elif vertical_align == 'bottom':
                start_y = int(y) + int(height) - total_text_height
            else:
                start_y = int(y)
            
            for i, line in enumerate(lines):
                line_y = start_y + i * line_height
                painter.drawText(
                    int(x), line_y, int(width), line_height,
                    h_align_flags,
                    line
                )

        # 绘制对象ID（左上角）
        id_font = QFont("Arial", int(1 * scale))
        id_font.setBold(True)
        painter.setPen(QColor(255, 180, 180, 180))
        painter.setFont(id_font)
        text_x = int(x)
        text_y = int(y)
        painter.drawText(text_x, text_y, obj['id'][:8])


def atom_draw_grid(painter: QPainter, width: int, height: int, scale: float, x_offset: float, y_offset: float, grid_color: QColor, grid_line_style) -> None:
    """绘制网格（覆盖在对象上层）

    Args:
        painter: 画笔对象
        width: 绘图区宽度
        height: 绘图区高度
        scale: 缩放比例
        x_offset: X偏移
        y_offset: Y偏移
        grid_color: 网格颜色
        grid_line_style: 网格线型
    """
    pen = painter.pen()
    painter.setPen(grid_color)
    new_pen = painter.pen()
    new_pen.setStyle(grid_line_style)
    painter.setPen(new_pen)

    grid_size = 10 * scale

    # 绘制竖线
    for i in range(-100, 100):
        x = x_offset + i * grid_size
        if 0 <= x <= width:
            painter.drawLine(int(x), 0, int(x), height)

    # 绘制横线
    for i in range(-100, 100):
        y = y_offset + i * grid_size
        if 0 <= y <= height:
            painter.drawLine(0, int(y), width, int(y))


def _wrap_text(text: str, painter, font, max_width: int) -> list:
    """文本自动换行（内部函数）

    Args:
        text: 文本内容
        painter: 画笔对象
        font: 字体对象
        max_width: 最大宽度（像素）

    Returns:
        换行后的文本行列表
    """
    if not text:
        return []
    
    lines = []
    current_line = ""
    
    for char in text:
        char_width = painter.fontMetrics().width(char)
        
        if char_width > max_width:
            if current_line:
                lines.append(current_line)
                current_line = ""
            continue
        
        test_line = current_line + char
        test_width = painter.fontMetrics().width(test_line)
        
        if test_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = char
    
    if current_line:
        lines.append(current_line)
    
    return lines
