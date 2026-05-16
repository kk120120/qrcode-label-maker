# Python 批量二维码标签生成器
# Copyright (C) 2026
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pandas as pd
import os

class CSVHandler:
    def __init__(self):
        self.data = None
        self.columns = []
    
    def import_csv(self, file_path):
        """导入CSV文件"""
        try:
            # 尝试不同编码读取
            encodings = ['utf-8', 'gbk', 'latin1']
            for encoding in encodings:
                try:
                    self.data = pd.read_csv(file_path, encoding=encoding)
                    break
                except:
                    continue
            
            if self.data is not None:
                # 清理数据：删除全为空值的行和列
                self.data = self.data.dropna(how='all').dropna(axis=1, how='all')
                self.columns = list(self.data.columns)
                return True
            return False
        except Exception as e:
            return False
    
    def import_excel(self, file_path):
        """导入Excel文件"""
        try:
            # 只导入第一个sheet（使用序号0），默认第一行为列名
            # 使用sheet序号0表示第一个sheet，而不是使用sheet名称
            # 使用calamine引擎提高读取速度
            try:
                # 尝试使用calamine引擎
                self.data = pd.read_excel(file_path, sheet_name=0, engine='calamine')
            except Exception as e:
                # 如果calamine引擎不可用，回退到默认引擎
                self.data = pd.read_excel(file_path, sheet_name=0)
            
            if self.data is not None:
                # 清理数据：删除全为空值的行和列
                self.data = self.data.dropna(how='all').dropna(axis=1, how='all')
                self.columns = list(self.data.columns)
                return True
            return False
        except Exception as e:
            return False
    
    def get_columns(self):
        """获取CSV列名"""
        return self.columns
    
    def get_data(self):
        """获取CSV数据"""
        return self.data
    
    def get_preview_data(self, start_row=2, row_count=5):
        """获取预览数据"""
        if self.data is None:
            return None
        
        end_row = start_row + row_count - 1
        if start_row < 1:
            start_row = 1
        
        # 转换为0-based索引
        start_idx = start_row - 1
        end_idx = min(start_idx + row_count, len(self.data))
        
        return self.data.iloc[start_idx:end_idx]
    
    def get_row_count(self):
        """获取数据行数"""
        if self.data is None:
            return 0
        return len(self.data)
