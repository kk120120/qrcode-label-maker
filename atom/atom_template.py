"""
L4 原子层 - 模板操作
功能：提供模板管理的纯函数原子操作，不调用其他原子
文件：atom/atom_template.py
"""

from typing import Dict, Any, List, Optional
import uuid


def atom_template_create_default(label_width: float = 50, label_height: float = 30, corner_radius: float = 2, dpi: int = 300) -> Dict[str, Any]:
    """创建默认模板

    Args:
        label_width: 标签宽度(mm)
        label_height: 标签高度(mm)
        corner_radius: 圆角半径
        dpi: 分辨率
    
    Returns:
        默认模板对象
    """
    return {
        "label_size": {
            "width": label_width,
            "height": label_height,
            "corner_radius": corner_radius
        },
        "dpi": dpi,
        "objects": []
    }


def atom_template_create_empty() -> Dict[str, Any]:
    """创建空模板

    Returns:
        空模板对象
    """
    return {
        "label_size": {"width": 50, "height": 30, "corner_radius": 2},
        "dpi": 300,
        "objects": []
    }


def atom_template_generate_id() -> str:
    """生成唯一对象ID

    Returns:
        唯一ID字符串
    """
    return str(uuid.uuid4())[:8]


def atom_template_add_object(template: Dict[str, Any], obj: Dict[str, Any]) -> str:
    """向模板添加对象

    Args:
        template: 模板对象
        obj: 要添加的对象
    
    Returns:
        添加的对象ID
    """
    template["objects"].append(obj)
    return obj.get("id", "")


def atom_template_remove_object(template: Dict[str, Any], obj_id: str) -> bool:
    """从模板移除对象

    Args:
        template: 模板对象
        obj_id: 对象ID
    
    Returns:
        是否成功移除
    """
    original_count = len(template["objects"])
    template["objects"] = [obj for obj in template["objects"] if obj.get("id") != obj_id]
    return len(template["objects"]) < original_count


def atom_template_get_object(template: Dict[str, Any], obj_id: str) -> Optional[Dict[str, Any]]:
    """从模板获取对象

    Args:
        template: 模板对象
        obj_id: 对象ID
    
    Returns:
        对象对象，不存在则返回None
    """
    for obj in template["objects"]:
        if obj.get("id") == obj_id:
            return obj
    return None


def atom_template_get_objects(template: Dict[str, Any]) -> List[Dict[str, Any]]:
    """获取所有对象

    Args:
        template: 模板对象
    
    Returns:
        所有对象列表
    """
    return template["objects"]


def atom_template_update_object(template: Dict[str, Any], obj_id: str, **kwargs) -> bool:
    """更新模板对象

    Args:
        template: 模板对象
        obj_id: 对象ID
        **kwargs: 要更新的属性，可以是：
            - position: dict，位置字典 {"x": x, "y": y}
            - x: float，X坐标（会更新position["x"]）
            - y: float，Y坐标（会更新position["y"]）
            - size: dict，大小字典 {"width": w, "height": h}
            - width: float，宽度（会更新size["width"]）
            - height: float，高度（会更新size["height"]）
            - 其他属性直接更新

    Returns:
        是否成功更新
    """
    obj = atom_template_get_object(template, obj_id)
    if not obj:
        return False

    # 处理 position 字典
    if "position" in kwargs:
        obj["position"] = kwargs["position"]
    # 处理单独的 x, y 参数
    if "x" in kwargs or "y" in kwargs:
        if "position" not in obj:
            obj["position"] = {"x": 0, "y": 0}
        if "x" in kwargs:
            obj["position"]["x"] = kwargs["x"]
        if "y" in kwargs:
            obj["position"]["y"] = kwargs["y"]

    # 处理 size 字典
    if "size" in kwargs:
        obj["size"] = kwargs["size"]
    # 处理单独的 width, height 参数
    if "width" in kwargs or "height" in kwargs:
        if "size" not in obj:
            obj["size"] = {"width": 0, "height": 0}
        if "width" in kwargs:
            obj["size"]["width"] = kwargs["width"]
        if "height" in kwargs:
            obj["size"]["height"] = kwargs["height"]

    # 处理 properties
    if "properties" in kwargs:
        if "properties" not in obj:
            obj["properties"] = {}
        obj["properties"].update(kwargs["properties"])

    # 支持直接更新属性（排除已处理的键）
    handled_keys = {"position", "x", "y", "size", "width", "height", "properties"}
    for key, value in kwargs.items():
        if key not in handled_keys:
            obj[key] = value

    return True


def atom_template_get_label_size(template: Dict[str, Any]) -> Dict[str, float]:
    """获取标签尺寸

    Args:
        template: 模板对象
    
    Returns:
        标签尺寸信息
    """
    return template["label_size"]


def atom_template_set_label_size(template: Dict[str, Any], width: float, height: float, corner_radius: float) -> None:
    """设置标签尺寸

    Args:
        template: 模板对象
        width: 宽度
        height: 高度
        corner_radius: 圆角半径
    """
    template["label_size"]["width"] = width
    template["label_size"]["height"] = height
    template["label_size"]["corner_radius"] = corner_radius


def atom_template_get_dpi(template: Dict[str, Any]) -> int:
    """获取模板DPI

    Args:
        template: 模板对象
    
    Returns:
        DPI值
    """
    return template["dpi"]


def atom_template_set_dpi(template: Dict[str, Any], dpi: int) -> None:
    """设置模板DPI

    Args:
        template: 模板对象
        dpi: DPI值
    """
    template["dpi"] = dpi


def atom_template_check_boundaries(template: Dict[str, Any]) -> List[str]:
    """检查边界溢出

    Args:
        template: 模板对象
    
    Returns:
        溢出边界的对象ID列表
    """
    overflow = []
    label_width = template["label_size"]["width"]
    label_height = template["label_size"]["height"]
    for obj in template["objects"]:
        x = obj["position"]["x"]
        y = obj["position"]["y"]
        w = obj["size"]["width"]
        h = obj["size"]["height"]
        if x < 0 or y < 0 or x + w > label_width or y + h > label_height:
            overflow.append(obj["id"])
    return overflow
