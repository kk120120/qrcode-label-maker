"""
L3 分子层 - 历史记录管理
功能：编排历史记录原子操作，提供完整的历史记录功能
文件：molecule/molecule_history.py
"""
from typing import Dict, Any, List, Tuple, Optional
from atom.atom_history import (
    atom_history_create,
    atom_history_save,
    atom_history_undo,
    atom_history_redo,
    atom_history_can_undo,
    atom_history_can_redo,
    atom_history_get_undo_redo_status
)


class HistoryManager:
    """历史记录管理器"""

    def __init__(self):
        self.history_state = atom_history_create()

    def molecule_history_init(self) -> None:
        """
        初始化历史记录
        """
        self.history_state = atom_history_create()

    def molecule_history_save(
        self,
        template: Dict[str, Any],
        objects: List[Dict[str, Any]]
    ) -> None:
        """
        保存当前状态到历史记录

        参数:
            template: 当前模板数据
            objects: 当前对象列表
        """
        self.history_state = atom_history_save(self.history_state, template, objects)

    def molecule_history_undo(self) -> Tuple[Optional[Dict[str, Any]], Optional[List[Dict[str, Any]]]]:
        """
        执行撤销操作

        返回:
            (恢复的模板, 恢复的对象列表)，如果无法撤销返回(None, None)
        """
        self.history_state, template, objects = atom_history_undo(self.history_state)
        return template, objects

    def molecule_history_redo(self) -> Tuple[Optional[Dict[str, Any]], Optional[List[Dict[str, Any]]]]:
        """
        执行重做操作

        返回:
            (恢复的模板, 恢复的对象列表)，如果无法重做返回(None, None)
        """
        self.history_state, template, objects = atom_history_redo(self.history_state)
        return template, objects

    def molecule_history_can_undo(self) -> bool:
        """
        检查是否可以撤销

        返回:
            是否可以撤销
        """
        return atom_history_can_undo(self.history_state)

    def molecule_history_can_redo(self) -> bool:
        """
        检查是否可以重做

        返回:
            是否可以重做
        """
        return atom_history_can_redo(self.history_state)

    def molecule_history_get_status(self) -> Tuple[bool, bool]:
        """
        获取撤销重做状态

        返回:
            (能否撤销, 能否重做)
        """
        return atom_history_get_undo_redo_status(self.history_state)
