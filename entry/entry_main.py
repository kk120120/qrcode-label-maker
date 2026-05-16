"""
L1 入口层 - 主窗口入口
功能：创建和管理UI，只负责UI组装和事件转发
文件：entry/entry_main.py
"""

from typing import Optional
from entry.ui_window.main_window import MainWindow


class EntryMain:
    """L1入口层 - 主入口

    负责：创建和显示主窗口
    """

    def __init__(self):
        """入口初始化"""
        self.window: Optional[MainWindow] = None

    def create_main_window(self) -> MainWindow:
        """创建主窗口

        Returns:
            创建的主窗口对象
        """
        self.window = MainWindow()
        return self.window

    def show_window(self):
        """显示主窗口"""
        if self.window:
            self.window.show()

    def close_window(self):
        """关闭主窗口"""
        if self.window:
            self.window.close()
