"""
L3 分子层 - 绘制管理
功能：编排原子操作，实现完整业务动作
文件：molecule/molecule_draw.py
"""

from typing import Dict, Any, List, Optional, Callable
from PyQt5.QtGui import QPainter, QColor
from atom.atom_draw import atom_draw_label, atom_draw_objects, atom_draw_grid


class DrawManager:
    """绘制管理器"""
    def __init__(self):
        pass

    def molecule_draw_label(self, painter: QPainter, template: Dict[str, Any], scale: float, x_offset: float, y_offset: float) -> None:
        """绘制标签

        Args:
            painter: 画笔对象
            template: 模板数据
            scale: 缩放比例
            x_offset: X偏移
            y_offset: Y偏移
        """
        atom_draw_label(painter, template, scale, x_offset, y_offset)

    def molecule_draw_objects(self, painter: QPainter, objects: List[Dict[str, Any]], selected_object: str, out_of_bounds: List[str], scale: float, x_offset: float, y_offset: float, dpi: int, get_first_row_value: Optional[Callable[[str], Optional[str]]] = None) -> None:
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
        atom_draw_objects(painter, objects, selected_object, out_of_bounds, scale, x_offset, y_offset, dpi, get_first_row_value)

    def molecule_draw_grid(self, painter: QPainter, width: int, height: int, scale: float, x_offset: float, y_offset: float, grid_color: QColor, grid_line_style) -> None:
        """绘制网格

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
        atom_draw_grid(painter, width, height, scale, x_offset, y_offset, grid_color, grid_line_style)

    def molecule_draw_all(self, painter: QPainter, template: Dict[str, Any], objects: List[Dict[str, Any]], selected_object: str, out_of_bounds: List[str], width: int, height: int, scale: float, x_offset: float, y_offset: float, show_grid: bool, grid_color: QColor, grid_line_style, get_first_row_value: Optional[Callable[[str], Optional[str]]] = None) -> None:
        """绘制所有内容

        Args:
            painter: 画笔对象
            template: 模板数据
            objects: 对象列表
            selected_object: 选中的对象ID
            out_of_bounds: 超出边界的对象ID列表
            width: 绘图区宽度
            height: 绘图区高度
            scale: 缩放比例
            x_offset: X偏移
            y_offset: Y偏移
            show_grid: 是否显示网格
            grid_color: 网格颜色
            grid_line_style: 网格线型
            get_first_row_value: 获取第一行数据的回调函数（可选）
        """
        self.molecule_draw_label(painter, template, scale, x_offset, y_offset)
        self.molecule_draw_objects(painter, objects, selected_object, out_of_bounds, scale, x_offset, y_offset, template['dpi'], get_first_row_value)
        if show_grid:
            self.molecule_draw_grid(painter, width, height, scale, x_offset, y_offset, grid_color, grid_line_style)
