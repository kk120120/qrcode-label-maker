"""
L4 原子层 - 文件操作
功能：提供文件相关的纯函数原子操作
文件：atom/atom_file.py
"""

import os
from typing import Optional


def atom_file_exists(file_path: str) -> bool:
    """检查文件是否存在"""
    return os.path.exists(file_path)


def atom_file_get_directory(file_path: str) -> str:
    """获取文件所在目录"""
    return os.path.dirname(file_path)


def atom_file_join_path(*parts) -> str:
    """拼接路径"""
    return os.path.join(*parts)


def atom_file_get_basename(file_path: str) -> str:
    """获取文件名"""
    return os.path.basename(file_path)


def atom_file_make_directory(directory: str) -> bool:
    """创建目录"""
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        return True
    except Exception:
        return False
