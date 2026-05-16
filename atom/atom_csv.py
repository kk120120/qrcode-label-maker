"""
L4 原子层 - CSV/Excel操作
功能：提供CSV/Excel相关的纯函数原子操作
文件：atom/atom_csv.py
"""

import pandas as pd
from typing import Optional, List


def atom_csv_read(file_path: str) -> tuple:
    """读取CSV文件

    Args:
        file_path: 文件路径

    Returns:
        (数据, 错误信息)，成功时错误信息为None
    """
    try:
        return pd.read_csv(file_path, encoding='utf-8'), None
    except Exception as e:
        try:
            # 尝试其他编码
            return pd.read_csv(file_path, encoding='gbk'), None
        except Exception as e2:
            return None, f"CSV文件读取失败: {str(e2)}"


def atom_excel_read(file_path: str, sheet_name: int = 0) -> tuple:
    """读取Excel文件

    Args:
        file_path: 文件路径
        sheet_name: 工作表索引

    Returns:
        (数据, 错误信息)，成功时错误信息为None
    """
    try:
        return pd.read_excel(file_path, sheet_name=sheet_name), None
    except Exception as e:
        return None, f"Excel文件读取失败: {str(e)}"


def atom_csv_get_columns(data: pd.DataFrame) -> List[str]:
    """获取列名

    Args:
        data: 数据

    Returns:
        列名列表
    """
    if data is not None:
        return list(data.columns)
    return []


def atom_csv_get_row(data: pd.DataFrame, index: int) -> Optional[pd.Series]:
    """获取指定行数据

    Args:
        data: 数据
        index: 行索引

    Returns:
        行数据，失败返回None
    """
    if data is not None and 0 <= index < len(data):
        return data.iloc[index]
    return None
