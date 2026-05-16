"""
L3 分子层 - CSV处理
功能：编排原子操作，实现完整业务动作
文件：molecule/molecule_csv.py
"""

import pandas as pd
from typing import Optional, List, Any, Tuple
from atom.atom_csv import atom_csv_read, atom_excel_read, atom_csv_get_columns, atom_csv_get_row


class CSVManager:
    """CSV管理器"""
    def __init__(self):
        self.data: Optional[pd.DataFrame] = None
        self.error_message: Optional[str] = None
        self.file_path: Optional[str] = None

    def molecule_csv_import(self, file_path: str) -> Tuple[Optional[pd.DataFrame], Optional['CSVManager']]:
        """导入CSV文件

        Args:
            file_path: 文件路径

        Returns:
            (数据, CSVManager实例)，成功时数据不为None
        """
        data, error = atom_csv_read(file_path)
        if data is not None:
            self.data = data
            self.error_message = None
            self.file_path = file_path
            return data, self
        self.error_message = error
        return None, None

    def molecule_csv_import_excel(self, file_path: str) -> Tuple[Optional[pd.DataFrame], Optional['CSVManager']]:
        """导入Excel文件

        Args:
            file_path: 文件路径

        Returns:
            (数据, CSVManager实例)，成功时数据不为None
        """
        data, error = atom_excel_read(file_path, sheet_name=0)
        if data is not None:
            self.data = data
            self.error_message = None
            self.file_path = file_path
            return data, self
        self.error_message = error
        return None, None
    
    def molecule_csv_get_handler(self) -> Optional['CSVManager']:
        """获取CSV处理器

        Returns:
            CSVManager实例
        """
        return self
    
    def molecule_csv_check_columns(self) -> bool:
        """检查是否有CSV列名

        Returns:
            是否有列名
        """
        return self.data is not None and len(atom_csv_get_columns(self.data)) > 0

    def molecule_csv_get_data(self) -> Optional[pd.DataFrame]:
        """获取数据"""
        return self.data

    def molecule_csv_get_columns(self) -> List[str]:
        """获取列名"""
        return atom_csv_get_columns(self.data)

    def molecule_csv_get_row(self, index: int) -> Optional[pd.Series]:
        """获取指定行数据"""
        return atom_csv_get_row(self.data, index)

    def molecule_csv_get_first_row_value(self, column: str) -> Optional[Any]:
        """获取第一行指定列的值
        
        Args:
            column: 列名
            
        Returns:
            第一行指定列的值，无数据时返回None
        """
        if self.data is not None and column in self.data.columns and len(self.data) > 0:
            return str(self.data.iloc[0][column])
        return None

    def molecule_csv_get_row_value(self, column: str, index: int) -> Optional[Any]:
        """获取指定行指定列的值
        
        Args:
            column: 列名
            index: 行索引（从0开始）
            
        Returns:
            指定行指定列的值，无数据时返回None
        """
        if (self.data is not None and 
            column in self.data.columns and 
            len(self.data) > 0 and 
            0 <= index < len(self.data)):
            return str(self.data.iloc[index][column])
        return None

    def molecule_csv_get_row_count(self) -> int:
        """获取数据行数"""
        if self.data is not None:
            return len(self.data)
        return 0

    def get_row_count(self) -> int:
        """获取数据行数（供UI调用）"""
        return self.molecule_csv_get_row_count()

    def get_preview_data(self, start_row: int, num_rows: int):
        """获取预览数据

        Args:
            start_row: 起始行号（1-based）
            num_rows: 行数

        Returns:
            DataFrame 或 None
        """
        if self.data is not None:
            start_idx = max(0, start_row - 1)
            end_idx = min(len(self.data), start_idx + num_rows)
            return self.data.iloc[start_idx:end_idx]
        return None
