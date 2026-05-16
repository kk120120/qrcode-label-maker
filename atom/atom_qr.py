"""
L4 原子层 - 二维码操作
功能：提供二维码相关的纯函数原子操作
文件：atom/atom_qr.py
"""

import qrcode
from PIL import Image
from typing import Optional, Tuple, Dict, Any


def atom_qr_generate(
    content: str,
    error_correction: str = "Q",
    qr_version: str = "21x21"
) -> Optional[Image.Image]:
    """生成二维码图像

    Args:
        content: 二维码内容
        error_correction: 纠错级别 (L/M/Q/H)
        qr_version: 二维码版本

    Returns:
        二维码图像，失败返回None
    """
    error_level_map = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H
    }

    error_level = error_level_map.get(
        error_correction,
        qrcode.constants.ERROR_CORRECT_Q
    )

    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=error_level,
            box_size=10,
            border=4,
        )
        qr.add_data(content)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        return img
    except Exception:
        return None


def atom_qr_get_capacity(
    version: str,
    error_level: str
) -> Tuple[int, int, int, int]:
    """获取二维码容量

    Args:
        version: 二维码版本
        error_level: 纠错级别

    Returns:
        (数字模式容量, 字母数字模式容量, 字节模式容量, 汉字模式容量)
    """
    capacity_map = {
        "21x21": {"L": 25, "M": 20, "Q": 16, "H": 12},
        "25x25": {"L": 47, "M": 37, "Q": 29, "H": 22},
        "29x29": {"L": 77, "M": 61, "Q": 47, "H": 35},
        "33x33": {"L": 114, "M": 90, "Q": 72, "H": 53},
        "37x37": {"L": 154, "M": 122, "Q": 97, "H": 71},
        "41x41": {"L": 202, "M": 158, "Q": 125, "H": 93},
        "45x45": {"L": 255, "M": 202, "Q": 158, "H": 119},
        "49x49": {"L": 313, "M": 252, "Q": 194, "H": 143},
        "53x53": {"L": 377, "M": 308, "Q": 235, "H": 173},
        "57x57": {"L": 446, "M": 367, "Q": 279, "H": 205},
        "61x61": {"L": 520, "M": 429, "Q": 327, "H": 241},
        "65x65": {"L": 598, "M": 495, "Q": 379, "H": 278},
        "69x69": {"L": 681, "M": 565, "Q": 434, "H": 317},
        "73x73": {"L": 770, "M": 638, "Q": 493, "H": 359},
        "77x77": {"L": 864, "M": 716, "Q": 555, "H": 403},
        "81x81": {"L": 963, "M": 798, "Q": 621, "H": 450},
        "85x85": {"L": 1067, "M": 884, "Q": 691, "H": 499},
        "89x89": {"L": 1177, "M": 975, "Q": 765, "H": 551},
        "93x93": {"L": 1291, "M": 1071, "Q": 842, "H": 605},
        "97x97": {"L": 1411, "M": 1172, "Q": 924, "H": 662},
        "101x101": {"L": 1535, "M": 1278, "Q": 1011, "H": 721},
        "105x105": {"L": 1664, "M": 1388, "Q": 1101, "H": 783},
        "109x109": {"L": 1798, "M": 1503, "Q": 1195, "H": 847},
        "113x113": {"L": 1938, "M": 1622, "Q": 1293, "H": 914},
        "117x117": {"L": 2082, "M": 1745, "Q": 1395, "H": 983},
        "121x121": {"L": 2232, "M": 1873, "Q": 1501, "H": 1055},
        "125x125": {"L": 2386, "M": 2005, "Q": 1611, "H": 1130},
        "129x129": {"L": 2546, "M": 2141, "Q": 1725, "H": 1207},
        "133x133": {"L": 2710, "M": 2282, "Q": 1843, "H": 1287},
        "137x137": {"L": 2879, "M": 2428, "Q": 1965, "H": 1370},
        "141x141": {"L": 3053, "M": 2578, "Q": 2091, "H": 1455},
        "145x145": {"L": 3232, "M": 2733, "Q": 2221, "H": 1543},
        "149x149": {"L": 3415, "M": 2892, "Q": 2355, "H": 1633},
        "153x153": {"L": 3603, "M": 3056, "Q": 2493, "H": 1727},
        "157x157": {"L": 3795, "M": 3224, "Q": 2635, "H": 1824},
        "161x161": {"L": 3992, "M": 3396, "Q": 2781, "H": 1924},
        "165x165": {"L": 4194, "M": 3573, "Q": 2931, "H": 2027},
        "169x169": {"L": 4400, "M": 3754, "Q": 3085, "H": 2133},
        "173x173": {"L": 4611, "M": 3940, "Q": 3243, "H": 2242},
        "177x177": {"L": 4827, "M": 4131, "Q": 3405, "H": 2354},
        "181x181": {"L": 5047, "M": 4326, "Q": 3571, "H": 2469},
        "185x185": {"L": 5272, "M": 4525, "Q": 3741, "H": 2587},
        "189x189": {"L": 5501, "M": 4729, "Q": 3915, "H": 2708},
        "193x193": {"L": 5735, "M": 4937, "Q": 4093, "H": 2832},
        "197x197": {"L": 5973, "M": 5150, "Q": 4275, "H": 2959}
    }

    if version in capacity_map and error_level in capacity_map[version]:
        capacity = capacity_map[version][error_level]
        return (
            capacity,
            int(capacity * 0.7),
            int(capacity * 0.5),
            int(capacity * 0.3)
        )
    return (0, 0, 0, 0)


def atom_qr_create(
    obj_id: str,
    x: float,
    y: float,
    width: float = 10,
    height: float = 10,
    qr_version: str = "21x21",
    error_correction: str = "Q",
    content: str = "",
    batch: bool = False,
    csv_column: str = "",
    z_index: int = 0
) -> Dict[str, Any]:
    """创建二维码对象

    Args:
        obj_id: 对象ID
        x: X坐标
        y: Y坐标
        width: 宽度
        height: 高度
        qr_version: 二维码版本
        error_correction: 纠错级别
        content: 内容
        batch: 是否批量生成
        csv_column: CSV列

    Returns:
        二维码对象
    """
    return {
        "id": obj_id,
        "type": "qr",
        "position": {"x": x, "y": y},
        "size": {"width": width, "height": height},
        "qr_version": qr_version,
        "error_correction": error_correction,
        "content": content,
        "batch": batch,
        "csv_column": csv_column,
        "z_index": z_index
    }
