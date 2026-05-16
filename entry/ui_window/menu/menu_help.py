"""
L1 入口层 - 帮助菜单
功能：创建和管理帮助菜单
文件：entry/ui_window/menu/menu_help.py
"""
from PyQt5.QtWidgets import QAction, QMenuBar

class HelpMenu:
    """帮助菜单"""
    def __init__(self, parent_window):
        self.parent = parent_window
        
    def init(self, menubar: QMenuBar):
        """初始化帮助菜单"""
        help_menu = menubar.addMenu("帮助")
        about_action = QAction("关于", self.parent)
        about_action.triggered.connect(self.parent.show_about)
        help_menu.addAction(about_action)
