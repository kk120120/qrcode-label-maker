"""
L1 入口层 - UI入口
功能：接收用户事件，转发给L2调度层，不实现业务逻辑
文件：entry/entry_ui.py
"""
from typing import Optional, Dict, Any, List, Tuple
from schedule.schedule_core import CoreScheduler


class UIEntry:
    """UI入口"""

    def __init__(self):
        self.scheduler = CoreScheduler()

    def entry_init_template(self) -> Dict[str, Any]:
        """入口：初始化模板"""
        init_data = self.scheduler.schedule_init_template()
        return init_data

    def entry_init_designer(self) -> Dict[str, Any]:
        """入口：初始化设计器"""
        return {"show_grid": True, "grid_color": "#00FF00", "grid_line_style": "dash"}

    def entry_init_property_panel(self) -> Dict[str, Any]:
        """入口：初始化属性面板"""
        return {}

    def entry_new_template(self) -> None:
        """入口：新建模板"""
        self.scheduler.schedule_new_template()
        self.scheduler.history_manager.molecule_history_init()

    def entry_get_default_qr_position(self) -> tuple:
        """入口：获取二维码对象默认位置"""
        return self.scheduler.schedule_get_default_qr_position()

    def entry_get_default_text_position(self) -> tuple:
        """入口：获取文本对象默认位置"""
        return self.scheduler.schedule_get_default_text_position()

    def entry_open_template(self, file_path: str) -> bool:
        """入口：打开模板"""
        return self.scheduler.schedule_open_template(file_path)

    def entry_save_template(self, file_path: str) -> bool:
        """入口：保存模板"""
        return self.scheduler.schedule_save_template(file_path)

    def entry_get_last_open_dir(self) -> Optional[str]:
        """入口：获取上次打开目录"""
        return self.scheduler.schedule_get_last_open_dir()

    def entry_get_last_import_dir(self) -> Optional[str]:
        """入口：获取上次导入目录"""
        return self.scheduler.schedule_get_last_import_dir()
    
    def entry_set_last_open_dir(self, dir_path: str) -> None:
        """入口：设置上次打开目录"""
        return self.scheduler.schedule_set_last_open_dir(dir_path)
    
    def entry_set_last_import_dir(self, dir_path: str) -> None:
        """入口：设置上次导入目录"""
        return self.scheduler.schedule_set_last_import_dir(dir_path)
    
    def entry_get_last_export_dir(self) -> Optional[str]:
        """入口：获取上次导出目录"""
        return self.scheduler.schedule_get_last_export_dir()
    
    def entry_set_last_export_dir(self, dir_path: str) -> None:
        """入口：设置上次导出目录"""
        return self.scheduler.schedule_set_last_export_dir(dir_path)

    def entry_set_label_size(self, width: float, height: float, corner_radius: float) -> None:
        """入口：设置标签尺寸"""
        self.scheduler.schedule_set_label_size(width, height, corner_radius)

    def entry_set_dpi(self, dpi: int) -> None:
        """入口：设置DPI"""
        self.scheduler.schedule_set_dpi(dpi)

    def entry_get_qr_sizes(self) -> List[str]:
        """入口：获取二维码尺寸列表"""
        return self.scheduler.config_manager.molecule_config_get_qr_sizes()

    def entry_update_qr_sizes(self) -> list:
        """入口：更新二维码尺寸列表"""
        return self.scheduler.schedule_update_qr_sizes()

    def entry_get_qr_capacity(self, version: str, error_level: str) -> tuple:
        """入口：获取二维码容量"""
        return self.scheduler.schedule_get_qr_capacity(version, error_level)

    def entry_add_qr_object(self, x: float, y: float, width: float = 10, height: float = 10, qr_version: str = "21x21", error_correction: str = "Q", content: str = "", batch: bool = False, csv_column: str = "") -> str:
        """入口：添加二维码对象"""
        return self.scheduler.schedule_add_qr_object(x, y, width, height, qr_version, error_correction, content, batch, csv_column)

    def entry_add_text_object(self, x: float, y: float, width: float = 12, height: float = 6, font: str = "Arial", font_size: float = 3, font_style: List[str] = None, color: str = "#000000", content: str = "", batch: bool = False, csv_column: str = "", text_align: str = "left", vertical_align: str = "top") -> str:
        """入口：添加文本对象"""
        return self.scheduler.schedule_add_text_object(x, y, width, height, font, font_size, font_style, color, content, batch, csv_column, text_align, vertical_align)

    def entry_update_object(self, obj_id: str, **kwargs) -> bool:
        """入口：更新对象"""
        return self.scheduler.schedule_update_object(obj_id, **kwargs)

    def entry_update_object_properties(self, obj_id: str, **kwargs) -> bool:
        """入口：更新对象属性"""
        return self.scheduler.schedule_update_object_properties(obj_id, **kwargs)

    def entry_remove_object(self, obj_id: str) -> None:
        """入口：删除对象"""
        self.scheduler.template_manager.molecule_template_remove_object(obj_id)

    def entry_get_object_index(self, objects: List[Dict[str, Any]], obj_id: str) -> int:
        """入口：获取对象索引"""
        return self.scheduler.schedule_get_object_index(obj_id)

    def entry_import_csv(self, file_path: str) -> tuple:
        """入口：导入CSV文件"""
        return self.scheduler.schedule_import_csv(file_path)

    def entry_import_excel(self, file_path: str) -> tuple:
        """入口：导入Excel文件"""
        return self.scheduler.schedule_import_excel(file_path)

    def entry_get_csv_columns(self) -> List[str]:
        """入口：获取CSV列名"""
        return self.scheduler.schedule_get_csv_columns()

    def entry_get_csv_data(self) -> "Optional[Any]":
        """入口：获取CSV数据"""
        return self.scheduler.csv_manager.molecule_csv_get_data()

    def entry_check_csv_columns(self) -> list:
        """入口：检查CSV列"""
        return self.scheduler.schedule_check_csv_columns()

    def entry_get_first_row_value(self, column: str) -> Optional[str]:
        """入口：获取第一行指定列的值"""
        return self.scheduler.schedule_get_first_row_value(column)

    def entry_get_row_count(self) -> int:
        """入口：获取CSV数据行数"""
        return self.scheduler.schedule_get_row_count()

    def entry_get_row_value(self, column: str, index: int) -> Optional[str]:
        """入口：获取指定行指定列的值"""
        return self.scheduler.schedule_get_row_value(column, index)

    def entry_export_current(self, file_path: str, row_index: Optional[int] = None) -> bool:
        """入口：导出当前标签
        
        Args:
            file_path: 保存文件路径
            row_index: 指定行索引（从0开始），None表示使用第一行
        """
        return self.scheduler.schedule_export_current(file_path, row_index)

    def entry_batch_export(self, output_dir: str, export_format: str, progress_callback=None) -> tuple[bool, str]:
        """入口：批量导出标签"""
        return self.scheduler.schedule_batch_export(output_dir, export_format, progress_callback)

    def entry_get_template(self) -> Dict[str, Any]:
        """入口：获取模板数据"""
        return self.scheduler.schedule_get_template()

    def entry_get_object(self, obj_id: str) -> Optional[Dict[str, Any]]:
        """入口：获取单个对象"""
        return self.scheduler.template_manager.molecule_template_get_object(obj_id)

    def entry_get_objects(self) -> List[Dict[str, Any]]:
        """入口：获取所有对象"""
        return self.scheduler.schedule_get_objects()

    def entry_check_boundaries(self) -> List[str]:
        """入口：检查边界溢出"""
        return self.scheduler.template_manager.molecule_template_check_boundaries()

    def entry_update_property_panel(self, obj_id: str) -> dict:
        """入口：更新属性面板"""
        obj = self.scheduler.template_manager.molecule_template_get_object(obj_id)
        if obj:
            return obj
        return {}

    def entry_draw_all(self, painter, template: Dict[str, Any], objects: List[Dict[str, Any]], selected_object: str, out_of_bounds: List[str], width: int, height: int, scale: float, x_offset: float, y_offset: float, show_grid: bool, grid_color, grid_line_style) -> None:
        """入口：绘制所有内容"""
        from molecule.molecule_draw import DrawManager
        draw_manager = DrawManager()
        # 传递获取第一行数据的回调
        get_first_row_value = self.entry_get_first_row_value
        draw_manager.molecule_draw_all(painter, template, objects, selected_object, out_of_bounds, width, height, scale, x_offset, y_offset, show_grid, grid_color, grid_line_style, get_first_row_value)

    def entry_history_save(self) -> None:
        """入口：保存当前状态到历史记录"""
        self.scheduler.schedule_history_save()

    def entry_history_undo(self) -> Tuple[Optional[Dict[str, Any]], Optional[List[Dict[str, Any]]]]:
        """入口：执行撤销操作"""
        return self.scheduler.schedule_history_undo()

    def entry_history_redo(self) -> Tuple[Optional[Dict[str, Any]], Optional[List[Dict[str, Any]]]]:
        """入口：执行重做操作"""
        return self.scheduler.schedule_history_redo()

    def entry_history_can_undo(self) -> bool:
        """入口：检查是否可以撤销"""
        return self.scheduler.history_manager.molecule_history_can_undo()

    def entry_history_can_redo(self) -> bool:
        """入口：检查是否可以重做"""
        return self.scheduler.history_manager.molecule_history_can_redo()

    def entry_history_get_status(self) -> Tuple[bool, bool]:
        """入口：获取撤销重做状态"""
        return self.scheduler.schedule_history_get_status()

    def entry_restore_state(self, template: Dict[str, Any], objects: List[Dict[str, Any]]) -> None:
        """入口：恢复状态"""
        self.scheduler.template_manager.molecule_template_set(template)
        self.scheduler.template_manager.molecule_template_set_objects(objects)
