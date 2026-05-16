"""
L2 调度层 - 核心调度
功能：事件调度、分子编排
文件：schedule/schedule_core.py
"""
from typing import Optional
from molecule.molecule_template import TemplateManager
from molecule.molecule_csv import CSVManager
from molecule.molecule_config import ConfigManager
from molecule.molecule_image import ImageManager
from molecule.molecule_history import HistoryManager


class CoreScheduler:
    """核心调度器 - 事件调度、分子编排

    职责：
    - 管理所有分子管理器实例
    - 调度分子执行顺序
    - 异常处理和容错
    """

    def __init__(self):
        """初始化调度器"""
        self.template_manager = TemplateManager()
        self.csv_manager = CSVManager()
        self.config_manager = ConfigManager()
        self.image_manager = ImageManager()
        self.history_manager = HistoryManager()

    # ==================== 模板管理 ====================
    def schedule_init_template(self):
        """调度：初始化模板"""
        return self.template_manager.molecule_template_init()

    def schedule_new_template(self):
        """调度：新建模板"""
        return self.template_manager.molecule_template_new()

    def schedule_get_default_qr_position(self):
        """调度：获取二维码对象默认位置"""
        return self.template_manager.molecule_template_calculate_default_qr_position()

    def schedule_get_default_text_position(self):
        """调度：获取文本对象默认位置"""
        return self.template_manager.molecule_template_calculate_default_text_position()

    def schedule_get_template(self):
        """调度：获取模板数据"""
        return self.template_manager.molecule_template_get()

    def schedule_set_template(self, template_data: dict):
        """调度：设置模板数据"""
        return self.template_manager.molecule_template_set(template_data)

    def schedule_set_label_size(self, width: float, height: float, corner_radius: float):
        """调度：设置标签尺寸"""
        return self.template_manager.molecule_template_set_label_size(width, height, corner_radius)

    def schedule_set_dpi(self, dpi: int):
        """调度：设置DPI"""
        return self.template_manager.molecule_template_set_dpi(dpi)

    def schedule_add_qr_object(self, x: float = 0, y: float = 0, width: float = 10, height: float = 10, qr_version: str = "21x21", error_correction: str = "Q", content: str = "", batch: bool = False, csv_column: str = ""):
        """调度：添加二维码对象"""
        return self.template_manager.molecule_template_add_qr_object(x, y, width, height, qr_version, error_correction, content, batch, csv_column)

    def schedule_add_text_object(self, x: float = 0, y: float = 0, width: float = 12, height: float = 6, font: str = "Arial", font_size: float = 3, font_style: list = None, color: str = "#000000", content: str = "", batch: bool = False, csv_column: str = "", text_align: str = "left", vertical_align: str = "top"):
        """调度：添加文本对象"""
        return self.template_manager.molecule_template_add_text_object(x, y, width, height, font, font_size, font_style, color, content, batch, csv_column, text_align, vertical_align)

    def schedule_update_object(self, obj_id: str, **kwargs):
        """调度：更新对象"""
        return self.template_manager.molecule_template_update_object(obj_id, **kwargs)

    def schedule_update_object_properties(self, obj_id: str, **kwargs):
        """调度：更新对象属性"""
        return self.template_manager.molecule_template_update_object_properties(obj_id, **kwargs)

    def schedule_delete_selected_object(self):
        """调度：删除选中对象"""
        return self.template_manager.molecule_template_delete_selected_object()

    def schedule_get_selected_object(self):
        """调度：获取选中对象"""
        return self.template_manager.molecule_template_get_selected_object()

    def schedule_set_selected_object(self, obj_id: str):
        """调度：设置选中对象"""
        return self.template_manager.molecule_template_set_selected_object(obj_id)

    def schedule_get_objects(self):
        """调度：获取所有对象"""
        return self.template_manager.molecule_template_get_objects()

    def schedule_get_object_index(self, obj_id: str):
        """调度：获取对象索引"""
        return self.template_manager.molecule_template_get_object_index(obj_id)

    def schedule_update_qr_sizes(self):
        """调度：更新二维码尺寸选项"""
        return self.template_manager.molecule_template_update_qr_sizes()

    def schedule_get_qr_capacity(self, version: str, error_level: str):
        """调度：获取二维码容量"""
        return self.template_manager.molecule_template_get_qr_capacity(version, error_level)

    def schedule_open_template(self, file_path: str):
        """调度：打开模板"""
        return self.template_manager.molecule_template_open(file_path)

    def schedule_save_template(self, file_path: str):
        """调度：保存模板"""
        return self.template_manager.molecule_template_save(file_path)

    # ==================== CSV管理 ====================
    def schedule_import_csv(self, file_path: str):
        """调度：导入CSV"""
        return self.csv_manager.molecule_csv_import(file_path)

    def schedule_import_excel(self, file_path: str):
        """调度：导入Excel"""
        return self.csv_manager.molecule_csv_import_excel(file_path)

    def schedule_get_csv_handler(self):
        """调度：获取CSV处理器"""
        return self.csv_manager.molecule_csv_get_handler()

    def schedule_get_csv_columns(self):
        """调度：获取CSV列名"""
        return self.csv_manager.molecule_csv_get_columns()

    def schedule_check_csv_columns(self):
        """调度：检查是否有CSV列名"""
        return self.csv_manager.molecule_csv_check_columns()

    def schedule_get_first_row_value(self, column: str):
        """调度：获取第一行指定列的值"""
        return self.csv_manager.molecule_csv_get_first_row_value(column)

    def schedule_get_row_count(self):
        """调度：获取数据行数"""
        return self.csv_manager.molecule_csv_get_row_count()

    def schedule_get_row_value(self, column: str, index: int):
        """调度：获取指定行指定列的值"""
        return self.csv_manager.molecule_csv_get_row_value(column, index)

    # ==================== 配置管理 ====================
    def schedule_get_last_open_dir(self):
        """调度：获取最后打开的目录"""
        return self.config_manager.molecule_config_get_last_open_dir()

    def schedule_set_last_open_dir(self, dir_path: str):
        """调度：设置最后打开的目录"""
        return self.config_manager.molecule_config_set_last_open_dir(dir_path)

    def schedule_get_last_import_dir(self):
        """调度：获取最后导入的目录"""
        return self.config_manager.molecule_config_get_last_import_dir()

    def schedule_set_last_import_dir(self, dir_path: str):
        """调度：设置最后导入的目录"""
        return self.config_manager.molecule_config_set_last_import_dir(dir_path)

    def schedule_get_last_export_dir(self):
        """调度：获取最后导出的目录"""
        return self.config_manager.molecule_config_get_last_export_dir()

    def schedule_set_last_export_dir(self, dir_path: str):
        """调度：设置最后导出的目录"""
        return self.config_manager.molecule_config_set_last_export_dir(dir_path)

    # ==================== 图像管理 ====================
    def schedule_export_current(self, file_path: str, row_index: Optional[int] = None):
        """调度：导出当前标签
        
        Args:
            file_path: 保存文件路径
            row_index: 指定行索引（从0开始），None表示使用第一行
        """
        template = self.template_manager.molecule_template_get()
        csv_handler = self.csv_manager.molecule_csv_get_handler()
        return self.image_manager.molecule_image_export_current(template, file_path, csv_handler, row_index)

    def schedule_batch_export(self, output_dir: str, export_format: str = 'png', progress_callback=None):
        """调度：批量导出"""
        template = self.template_manager.molecule_template_get()
        csv_handler = self.csv_manager.molecule_csv_get_handler()
        return self.image_manager.molecule_image_batch_export(template, csv_handler, output_dir, export_format, progress_callback)

    # ==================== 历史管理 ====================
    def schedule_history_save(self):
        """调度：保存历史"""
        template = self.template_manager.molecule_template_get()
        objects = self.template_manager.molecule_template_get_objects()
        self.history_manager.molecule_history_save(template, objects)

    def schedule_history_undo(self):
        """调度：撤销历史"""
        template, objects = self.history_manager.molecule_history_undo()
        if template and objects:
            self.template_manager.molecule_template_set(template)
            self.template_manager.molecule_template_set_objects(objects)
        return template, objects

    def schedule_history_redo(self):
        """调度：重做历史"""
        template, objects = self.history_manager.molecule_history_redo()
        if template and objects:
            self.template_manager.molecule_template_set(template)
            self.template_manager.molecule_template_set_objects(objects)
        return template, objects

    def schedule_history_get_status(self):
        """调度：获取历史状态"""
        return self.history_manager.molecule_history_get_status()
