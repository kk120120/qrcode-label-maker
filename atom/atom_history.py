"""
L4 原子层 - 历史记录操作
功能：提供历史记录的纯函数操作
文件：atom/atom_history.py
"""
from typing import List, Dict, Any, Tuple
import copy


def atom_history_create() -> Dict[str, Any]:
    """
    创建新的历史记录状态

    返回:
        初始化的历史记录状态字典
    """
    return {
        "history": [],
        "history_index": -1,
        "max_history": 20
    }


def atom_history_save(
    history_state: Dict[str, Any],
    template: Dict[str, Any],
    objects: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    保存当前状态到历史记录

    参数:
        history_state: 历史记录状态
        template: 当前模板数据
        objects: 当前对象列表

    返回:
        更新后的历史记录状态
    """
    new_state = copy.deepcopy(history_state)

    if new_state["history_index"] < len(new_state["history"]) - 1:
        new_state["history"] = new_state["history"][:new_state["history_index"] + 1]

    new_state["history"].append({
        "template": copy.deepcopy(template),
        "objects": copy.deepcopy(objects)
    })

    if len(new_state["history"]) > new_state["max_history"]:
        new_state["history"].pop(0)
    else:
        new_state["history_index"] = len(new_state["history"]) - 1

    return new_state


def atom_history_undo(history_state: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any], List[Dict[str, Any]]]:
    """
    执行撤销操作

    参数:
        history_state: 历史记录状态

    返回:
        (更新后的历史状态, 恢复的模板, 恢复的对象列表)
        如果无法撤销, 返回(原状态, None, None)
    """
    if not atom_history_can_undo(history_state):
        return history_state, None, None

    new_state = copy.deepcopy(history_state)
    new_state["history_index"] -= 1

    target = new_state["history"][new_state["history_index"]]
    return new_state, copy.deepcopy(target["template"]), copy.deepcopy(target["objects"])


def atom_history_redo(history_state: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any], List[Dict[str, Any]]]:
    """
    执行重做操作

    参数:
        history_state: 历史记录状态

    返回:
        (更新后的历史状态, 恢复的模板, 恢复的对象列表)
        如果无法重做, 返回(原状态, None, None)
    """
    if not atom_history_can_redo(history_state):
        return history_state, None, None

    new_state = copy.deepcopy(history_state)
    new_state["history_index"] += 1

    target = new_state["history"][new_state["history_index"]]
    return new_state, copy.deepcopy(target["template"]), copy.deepcopy(target["objects"])


def atom_history_can_undo(history_state: Dict[str, Any]) -> bool:
    """
    检查是否可以撤销

    参数:
        history_state: 历史记录状态

    返回:
        是否可以撤销
    """
    return history_state["history_index"] > 0


def atom_history_can_redo(history_state: Dict[str, Any]) -> bool:
    """
    检查是否可以重做

    参数:
        history_state: 历史记录状态

    返回:
        是否可以重做
    """
    return history_state["history_index"] < len(history_state["history"]) - 1


def atom_history_get_undo_redo_status(history_state: Dict[str, Any]) -> Tuple[bool, bool]:
    """
    获取撤销重做状态

    参数:
        history_state: 历史记录状态

    返回:
        (能否撤销, 能否重做)
    """
    return atom_history_can_undo(history_state), atom_history_can_redo(history_state)
