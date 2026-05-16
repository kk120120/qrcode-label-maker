"""
L1 入口层 - 文件菜单
功能：创建和管理文件菜单
文件：entry/ui_window/menu/menu_file.py
"""
from PyQt5.QtWidgets import QAction, QMenuBar

class FileMenu:
    """文件菜单"""
    def __init__(self, parent_window):
        self.parent = parent_window
        
    def init(self, menubar: QMenuBar):
        """初始化文件菜单"""
        file_menu = menubar.addMenu("文件")

        new_action = QAction("新建模板", self.parent)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.parent.new_template)
        file_menu.addAction(new_action)

        open_action = QAction("打开模板", self.parent)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.parent.open_template)
        file_menu.addAction(open_action)

        save_action = QAction("保存模板", self.parent)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.parent.save_template)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        exit_action = QAction("退出", self.parent)
        exit_action.triggered.connect(self.parent.close)
        file_menu.addAction(exit_action)
