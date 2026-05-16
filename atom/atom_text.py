"""
L4 原子层 - 文本操作
功能：提供文本相关的纯函数原子操作
文件：atom/atom_text.py
"""

from typing import Dict, Any, List


def atom_text_create(x: float, y: float, width: float = 12, height: float = 6, font: str = "Arial", font_size: float = 3, font_style: List[str] = None, color: str = "#000000", content: str = "", batch: bool = False, csv_column: str = "", text_align: str = "left", vertical_align: str = "top", z_index: int = 0) -> Dict[str, Any]:
    """创建文本对象

    Args:
        x: X坐标
        y: Y坐标
        width: 宽度
        height: 高度
        font: 字体
        font_size: 字体大小
        font_style: 字体样式
        color: 颜色
        content: 内容
        batch: 是否批量生成
        csv_column: CSV列

    Returns:
        文本对象
    """
    if font_style is None:
        font_style = ["normal"]
    return {
        "type": "text",
        "position": {
            "x": x,
            "y": y
        },
        "size": {
            "width": width,
            "height": height
        },
        "font": font,
        "font_size": font_size,
        "font_style": font_style,
        "color": color,
        "content": content,
        "batch": batch,
        "csv_column": csv_column,
        "text_align": text_align,
        "vertical_align": vertical_align,
        "z_index": z_index
    }


def atom_text_update(obj: Dict[str, Any], **kwargs) -> bool:
    """更新文本对象

    Args:
        obj: 文本对象
        **kwargs: 要更新的属性

    Returns:
        是否更新成功
    """
    if "x" in kwargs:
        obj["position"]["x"] = kwargs["x"]
    if "y" in kwargs:
        obj["position"]["y"] = kwargs["y"]
    if "width" in kwargs:
        obj["size"]["width"] = kwargs["width"]
    if "height" in kwargs:
        obj["size"]["height"] = kwargs["height"]
    
    # 直接更新顶层属性
    for key, value in kwargs.items():
        if key not in ["x", "y", "width", "height"]:
            obj[key] = value
    
    return True


def atom_text_get_property(obj: Dict[str, Any], property_name: str) -> Any:
    """获取文本对象属性

    Args:
        obj: 文本对象
        property_name: 属性名

    Returns:
        属性值
    """
    if property_name in obj:
        return obj[property_name]
    return None


def atom_text_set_property(obj: Dict[str, Any], property_name: str, value: Any) -> bool:
    """设置文本对象属性

    Args:
        obj: 文本对象
        property_name: 属性名
        value: 属性值

    Returns:
        是否设置成功
    """
    obj[property_name] = value
    return True
