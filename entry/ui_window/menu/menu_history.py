"""
L1 入口层 - 历史菜单
功能：创建和管理历史菜单
文件：entry/ui_window/menu/menu_history.py
"""
from PyQt5.QtWidgets import QAction, QMenuBar

class HistoryMenu:
    """历史菜单"""
    def __init__(self, parent_window):
        self.parent = parent_window
        self.undo_action = None
        self.redo_action = None
        
    def init(self, menubar: QMenuBar):
        """初始化历史菜单"""
        history_menu = menubar.addMenu("历史")

        self.undo_action = QAction("回退", self.parent)
        self.undo_action.setShortcut("Ctrl+Z")
        self.undo_action.setEnabled(False)
        self.undo_action.triggered.connect(self.parent.undo)
        history_menu.addAction(self.undo_action)

        self.redo_action = QAction("重做", self.parent)
        self.redo_action.setShortcut("Ctrl+Y")
        self.redo_action.setEnabled(False)
        self.redo_action.triggered.connect(self.parent.redo)
        history_menu.addAction(self.redo_action)
    
    def update_undo_redo_actions(self, can_undo: bool, can_redo: bool):
        """更新撤销重做按钮状态"""
        if self.undo_action:
            self.undo_action.setEnabled(can_undo)
        if self.redo_action:
            self.redo_action.setEnabled(can_redo)
