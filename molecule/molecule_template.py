"""
L3 分子层 - 模板管理
功能：模板加载、保存、更新，调用原子层完成功能
文件：molecule/molecule_template.py
"""

from typing import Dict, Any, List, Optional, Tuple
import json
import os
from atom.atom_template import (
    atom_template_create_default,
    atom_template_add_object,
    atom_template_remove_object,
    atom_template_get_object,
    atom_template_get_objects,
    atom_template_update_object,
    atom_template_get_label_size,
    atom_template_set_label_size,
    atom_template_get_dpi,
    atom_template_set_dpi,
    atom_template_check_boundaries,
    atom_template_generate_id
)
from atom.atom_qr import atom_qr_create
from atom.atom_text import atom_text_create
from atom.atom_property import atom_property_update_position, atom_property_update_size, atom_property_update_qr_properties, atom_property_update_text_properties


class TemplateManager:
    """模板管理器"""
    
    def __init__(self):
        self.template = atom_template_create_default()
        self.selected_object_id = None
    
    def molecule_template_init(self) -> Dict[str, Any]:
        """初始化模板

        Returns:
            初始化的模板数据
        """
        self.template = atom_template_create_default()
        return self.template
    
    def molecule_template_new(self) -> Dict[str, Any]:
        """新建模板

        Returns:
            初始化的模板数据
        """
        self.template = atom_template_create_default()
        self.selected_object_id = None
        return self.template
    
    def molecule_template_calculate_default_qr_position(self) -> Tuple[float, float]:
        """计算二维码对象默认居中位置

        Returns:
            (x, y) 元组
        """
        label_size = self.template['label_size']
        x = (label_size['width'] - 10) / 2
        y = (label_size['height'] - 10) / 2
        return x, y
    
    def molecule_template_calculate_default_text_position(self) -> Tuple[float, float]:
        """计算文本对象默认居中位置

        Returns:
            (x, y) 元组
        """
        label_size = self.template['label_size']
        x = (label_size['width'] - 30) / 2
        y = (label_size['height'] - 10) / 2
        return x, y
    
    def molecule_template_open(self, file_path: str) -> bool:
        """打开模板
        
        Args:
            file_path: 文件路径
        
        Returns:
            是否成功加载
        """
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.template = json.load(f)
                self.selected_object_id = None
                return True
        except Exception:
            pass
        return False
    
    def molecule_template_save(self, file_path: str) -> bool:
        """保存模板
        
        Args:
            file_path: 文件路径
        
        Returns:
            是否成功保存
        """
        try:
            os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.template, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
    
    def molecule_template_add_qr_object(
        self,
        x: float = 0,
        y: float = 0,
        width: float = 10,
        height: float = 10,
        qr_version: str = "21x21",
        error_correction: str = "Q",
        content: str = "",
        batch: bool = False,
        csv_column: str = ""
    ) -> str:
        """添加二维码对象
        
        Args:
            x: X坐标，默认为0表示居中
            y: Y坐标，默认为0表示居中
            width: 宽度，默认10mm
            height: 高度，默认10mm
            qr_version: 二维码版本
            error_correction: 纠错级别
            content: 内容
            batch: 是否批量
            csv_column: CSV列
        
        Returns:
            对象ID
        """
        label_size = self.template.get('label_size', {'width': 100, 'height': 100})
        label_width = label_size.get('width', 100)
        label_height = label_size.get('height', 100)
        
        if x == 0 and y == 0:
            x = (label_width - width) / 2
            y = (label_height - height) / 2
        
        objects = self.template.get('objects', [])
        max_z_index = max((obj.get('z_index', 0) for obj in objects), default=0)
        
        obj_id = atom_template_generate_id()
        qr_obj = atom_qr_create(
            obj_id, x, y, width, height, qr_version, error_correction, content, batch, csv_column, max_z_index + 1
        )
        return atom_template_add_object(self.template, qr_obj)
    
    def molecule_template_add_text_object(
        self,
        x: float = 0,
        y: float = 0,
        width: float = 12,
        height: float = 6,
        font: str = "Arial",
        font_size: float = 3,
        font_style: List[str] = None,
        color: str = "#000000",
        content: str = "",
        batch: bool = False,
        csv_column: str = "",
        text_align: str = "left",
        vertical_align: str = "top"
    ) -> str:
        """添加文本对象

        Args:
            x: X坐标，默认为0表示居中
            y: Y坐标，默认为0表示居中
            width: 宽度，默认12mm
            height: 高度，默认6mm
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
            对象ID
        """
        label_size = self.template.get('label_size', {'width': 100, 'height': 100})
        label_width = label_size.get('width', 100)
        label_height = label_size.get('height', 100)
        
        if x == 0 and y == 0:
            x = (label_width - width) / 2
            y = (label_height - height) / 2
        
        objects = self.template.get('objects', [])
        max_z_index = max((obj.get('z_index', 0) for obj in objects), default=0)
        
        obj_id = atom_template_generate_id()
        text_obj = atom_text_create(
            x, y, width, height, font, font_size, font_style, color, content, batch, csv_column, text_align, vertical_align, max_z_index + 1
        )
        text_obj["id"] = obj_id
        return atom_template_add_object(self.template, text_obj)
    
    def molecule_template_remove_object(self, obj_id: str) -> None:
        """移除对象
        
        Args:
            obj_id: 对象ID
        """
        atom_template_remove_object(self.template, obj_id)
    
    def molecule_template_get_object(self, obj_id: str) -> Optional[Dict[str, Any]]:
        """获取对象
        
        Args:
            obj_id: 对象ID
        
        Returns:
            对象
        """
        return atom_template_get_object(self.template, obj_id)
    
    def molecule_template_get_objects(self) -> List[Dict[str, Any]]:
        """获取所有对象
        
        Returns:
            对象列表
        """
        return atom_template_get_objects(self.template)
    
    def molecule_template_update_object(self, obj_id: str, **kwargs) -> bool:
        """更新对象
        
        Args:
            obj_id: 对象ID
            **kwargs: 更新参数
        
        Returns:
            是否更新成功
        """
        return atom_template_update_object(self.template, obj_id, **kwargs)
    
    def molecule_template_get_template(self) -> Dict[str, Any]:
        """获取模板
        
        Returns:
            模板数据
        """
        return self.template
    
    def molecule_template_set_size(self, width: float, height: float, corner_radius: float) -> None:
        """设置标签尺寸
        
        Args:
            width: 宽度
            height: 高度
            corner_radius: 圆角半径
        """
        atom_template_set_label_size(self.template, width, height, corner_radius)
    
    def molecule_template_set_dpi(self, dpi: int) -> None:
        """设置DPI
        
        Args:
            dpi: DPI值
        """
        atom_template_set_dpi(self.template, dpi)
    
    def molecule_template_check_boundaries(self) -> List[str]:
        """检查边界

        Returns:
            超出边界的对象ID列表
        """
        return atom_template_check_boundaries(self.template)

    def molecule_template_get_object_index(self, objects: List[Dict[str, Any]], obj_id: str) -> int:
        """获取对象在列表中的索引

        Args:
            objects: 对象列表
            obj_id: 对象ID

        Returns:
            对象索引（从1开始）
        """
        for i, obj in enumerate(objects):
            if obj.get('id') == obj_id:
                return i + 1
        return 0

    def molecule_template_update_object_properties(self, obj_id: str, **kwargs) -> bool:
        """更新对象属性

        Args:
            obj_id: 对象ID
            **kwargs: 更新参数

        Returns:
            是否更新成功
        """
        obj = atom_template_get_object(self.template, obj_id)
        if not obj:
            return False

        position = kwargs.get('position', obj.get('position', {'x': 0, 'y': 0}))
        size = kwargs.get('size', obj.get('size', {'width': 10, 'height': 10}))
        x = position.get('x', obj['position']['x']) if isinstance(position, dict) else position
        y = position.get('y', obj['position']['y']) if isinstance(position, dict) else position
        width = size.get('width', obj['size']['width']) if isinstance(size, dict) else size
        height = size.get('height', obj['size']['height']) if isinstance(size, dict) else size

        atom_property_update_position(obj, x, y)
        atom_property_update_size(obj, width, height)

        properties = {k: v for k, v in kwargs.items() if k not in ('position', 'size')}

        if obj.get('type') == 'qr' and ('qr_version' in properties or 'content' in properties):
            atom_property_update_qr_properties(
                obj,
                properties.get('qr_version', obj.get('qr_version', '21x21')),
                properties.get('error_correction', obj.get('error_correction', 'Q')),
                properties.get('content', obj.get('content', '')),
                properties.get('batch', obj.get('batch', False)),
                properties.get('csv_column', obj.get('csv_column', ''))
            )
        elif obj.get('type') == 'text' and ('font' in properties or 'content' in properties):
            atom_property_update_text_properties(
                obj,
                properties.get('font', obj.get('font', 'Arial')),
                properties.get('font_size', obj.get('font_size', 3)),
                properties.get('font_style', obj.get('font_style', ['normal'])),
                properties.get('color', obj.get('color', '#000000')),
                properties.get('content', obj.get('content', '')),
                properties.get('batch', obj.get('batch', False)),
                properties.get('csv_column', obj.get('csv_column', '')),
                properties.get('text_align', obj.get('text_align', 'left')),
                properties.get('vertical_align', obj.get('vertical_align', 'top'))
            )

        return True

    def molecule_template_get(self) -> Dict[str, Any]:
        """获取模板数据

        Returns:
            模板数据
        """
        return self.template
    
    def molecule_template_set(self, template: Dict[str, Any]) -> None:
        """设置模板数据

        Args:
            template: 模板数据
        """
        self.template = template
    
    def molecule_template_set_label_size(self, width: float, height: float, corner_radius: float) -> None:
        """设置标签尺寸
        
        Args:
            width: 宽度
            height: 高度
            corner_radius: 圆角半径
        """
        atom_template_set_label_size(self.template, width, height, corner_radius)
    
    def molecule_template_set_dpi(self, dpi: int) -> None:
        """设置DPI
        
        Args:
            dpi: DPI值
        """
        atom_template_set_dpi(self.template, dpi)
    
    def molecule_template_delete_selected_object(self) -> bool:
        """删除选中对象

        Returns:
            是否删除成功
        """
        if self.selected_object_id:
            self.molecule_template_remove_object(self.selected_object_id)
            self.selected_object_id = None
            return True
        return False
    
    def molecule_template_get_selected_object(self) -> Optional[Dict[str, Any]]:
        """获取选中对象

        Returns:
            选中的对象
        """
        if self.selected_object_id:
            return self.molecule_template_get_object(self.selected_object_id)
        return None
    
    def molecule_template_set_selected_object(self, obj_id: str) -> None:
        """设置选中对象

        Args:
            obj_id: 对象ID
        """
        self.selected_object_id = obj_id
    
    def molecule_template_get_object_index(self, obj_id: str) -> int:
        """获取对象索引

        Args:
            obj_id: 对象ID

        Returns:
            对象索引（从1开始）
        """
        objects = self.molecule_template_get_objects()
        for i, obj in enumerate(objects):
            if obj.get('id') == obj_id:
                return i + 1
        return 0
    
    def molecule_template_update_qr_sizes(self) -> List[str]:
        """更新二维码尺寸选项

        Returns:
            二维码版本列表
        """
        return ["21x21", "25x25", "29x29", "33x33"]
    
    def molecule_template_get_qr_capacity(self, version: str, error_level: str) -> tuple:
        """获取二维码容量

        Args:
            version: 二维码版本
            error_level: 纠错级别

        Returns:
            容量元组 (numeric, alphanumeric, byte, kanji)
        """
        capacities = {
            ("21x21", "L"): (41, 25, 17, 10),
            ("21x21", "M"): (34, 20, 14, 8),
            ("21x21", "Q"): (27, 16, 11, 7),
            ("21x21", "H"): (17, 10, 7, 4)
        }
        return capacities.get((version, error_level), (0, 0, 0, 0))
    
    def molecule_template_set_objects(self, objects: List[Dict[str, Any]]) -> None:
        """设置对象列表

        Args:
            objects: 对象列表
        """
        self.template['objects'] = objects
