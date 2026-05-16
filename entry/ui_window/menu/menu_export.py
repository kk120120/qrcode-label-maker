"""
L1 入口层 - 导出菜单
功能：创建和管理导出菜单
文件：entry/ui_window/menu/menu_export.py
"""
from PyQt5.QtWidgets import QAction, QMenuBar

class ExportMenu:
    """导出菜单"""
    def __init__(self, parent_window):
        self.parent = parent_window
        
    def init(self, menubar: QMenuBar):
        """初始化导出菜单"""
        export_menu = menubar.addMenu("导出")

        batch_export_action = QAction("批量导出", self.parent)
        batch_export_action.setShortcut("Ctrl+E")
        batch_export_action.triggered.connect(self.parent.open_batch_export_dialog)
        export_menu.addAction(batch_export_action)

        export_current_action = QAction("单张导出PNG", self.parent)
        export_current_action.triggered.connect(self.parent.export_current_label)
        export_menu.addAction(export_current_action)
