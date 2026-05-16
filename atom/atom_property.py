"""
L4 原子层 - 属性操作
功能：提供属性相关的纯函数原子操作
文件：atom/atom_property.py
"""

from typing import Dict, Any, List


def atom_property_update_position(obj: Dict[str, Any], x: float, y: float) -> Dict[str, Any]:
    """更新对象位置

    Args:
        obj: 对象数据
        x: X坐标
        y: Y坐标

    Returns:
        更新后的对象数据
    """
    obj['position']['x'] = x
    obj['position']['y'] = y
    return obj


def atom_property_update_size(obj: Dict[str, Any], width: float, height: float) -> Dict[str, Any]:
    """更新对象大小

    Args:
        obj: 对象数据
        width: 宽度
        height: 高度

    Returns:
        更新后的对象数据
    """
    obj['size']['width'] = width
    obj['size']['height'] = height
    return obj


def atom_property_update_qr_properties(
    obj: Dict[str, Any],
    qr_version: str,
    error_correction: str,
    content: str,
    batch: bool,
    csv_column: str
) -> Dict[str, Any]:
    """更新二维码属性

    Args:
        obj: 对象数据
        qr_version: 二维码版本
        error_correction: 纠错级别
        content: 内容
        batch: 是否批量
        csv_column: CSV列

    Returns:
        更新后的对象数据
    """
    obj['qr_version'] = qr_version
    obj['error_correction'] = error_correction
    obj['content'] = content
    obj['batch'] = batch
    obj['csv_column'] = csv_column
    return obj


def atom_property_update_text_properties(
    obj: Dict[str, Any],
    font: str,
    font_size: float,
    font_style: List[str],
    color: str,
    content: str,
    batch: bool,
    csv_column: str,
    text_align: str = "left",
    vertical_align: str = "top"
) -> Dict[str, Any]:
    """更新文本属性

    Args:
        obj: 对象数据
        font: 字体
        font_size: 字体大小
        font_style: 字体样式
        color: 颜色
        content: 内容
        batch: 是否批量
        csv_column: CSV列
        text_align: 水平对齐方式
        vertical_align: 垂直对齐方式

    Returns:
        更新后的对象数据
    """
    obj['font'] = font
    obj['font_size'] = font_size
    obj['font_style'] = font_style
    obj['color'] = color
    obj['content'] = content
    obj['batch'] = batch
    obj['csv_column'] = csv_column
    obj['text_align'] = text_align
    obj['vertical_align'] = vertical_align
    return obj


def atom_property_get_object_index(objects: List[Dict[str, Any]], obj_id: str) -> int:
    """获取对象在列表中的索引

    Args:
        objects: 对象列表
        obj_id: 对象ID

    Returns:
        对象索引（从1开始）
    """
    for i, obj in enumerate(objects):
        if obj['id'] == obj_id:
            return i + 1
    return 0
