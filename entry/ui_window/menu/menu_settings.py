"""
L1 入口层 - 设置菜单
功能：创建和管理设置菜单
文件：entry/ui_window/menu/menu_settings.py
"""
from PyQt5.QtWidgets import QAction, QMenuBar

class SettingsMenu:
    """设置菜单"""
    def __init__(self, parent_window):
        self.parent = parent_window
        
    def init(self, menubar: QMenuBar):
        """初始化设置菜单"""
        settings_menu = menubar.addMenu("设置")
        basic_settings_action = QAction("基础设置", self.parent)
        basic_settings_action.triggered.connect(self.parent.open_basic_settings)
        settings_menu.addAction(basic_settings_action)
