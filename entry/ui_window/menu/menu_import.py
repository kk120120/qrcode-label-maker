"""
L1 入口层 - 导入菜单
功能：创建和管理导入菜单
文件：entry/ui_window/menu/menu_import.py
"""
from PyQt5.QtWidgets import QAction, QMenuBar

class ImportMenu:
    """导入菜单"""
    def __init__(self, parent_window):
        self.parent = parent_window
        
    def init(self, menubar: QMenuBar):
        """初始化导入菜单"""
        import_menu = menubar.addMenu("导入")

        import_excel_action = QAction("xlsx 导入（不易出错）", self.parent)
        import_excel_action.setShortcut("Ctrl+I")
        import_excel_action.triggered.connect(self.parent.import_excel)
        import_menu.addAction(import_excel_action)

        import_csv_action = QAction("csv 导入（速度快）", self.parent)
        import_csv_action.triggered.connect(self.parent.import_csv)
        import_menu.addAction(import_csv_action)
