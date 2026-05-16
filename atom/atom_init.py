"""
L4 原子层 - 初始化操作
功能：提供初始化相关的纯函数原子操作
文件：atom/atom_init.py
"""

from typing import Dict, Any


def atom_init_template() -> Dict[str, Any]:
    """初始化模板数据

    Returns:
        初始化的模板数据
    """
    return {
        'label_size': {
            'width': 80,
            'height': 50,
            'corner_radius': 2
        },
        'dpi': 300,
        'objects': []
    }


def atom_init_designer_state() -> Dict[str, Any]:
    """初始化设计器状态

    Returns:
        初始化的设计器状态
    """
    return {
        'selected_object': None,
        'is_dragging': False,
        'drag_start': None,
        'show_grid': True,
        'grid_color': '#B4B4B4',  # 默认为比淡灰色深一点的颜色
        'zoom': 1.0,
        'pan_offset': {'x': 0, 'y': 0},
        'is_panning': False,
        'pan_start': None
    }


def atom_init_property_panel() -> Dict[str, Any]:
    """初始化属性面板状态

    Returns:
        初始化的属性面板状态
    """
    return {
        'object_info_label': '未选择对象',
        'qr_group_visible': False,
        'text_group_visible': False,
        'x_input': 0,
        'y_input': 0,
        'width_input': 0,
        'height_input': 0,
        'qr_version_combo': '21x21',
        'error_correction_combo': 'Q',
        'content_input': '',
        'qr_batch_checkbox': False,
        'qr_csv_column_combo': '',
        'font_combo': 'Arial',
        'font_size_input': 3,
        'bold_checkbox': False,
        'italic_checkbox': False,
        'underline_checkbox': False,
        'color_preview': '#000000',
        'text_content_input': '',
        'text_batch_checkbox': False,
        'text_csv_column_combo': ''
    }
