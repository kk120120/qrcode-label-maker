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

import configparser
import os
import sys

class ConfigManager:
    def __init__(self, config_file='qrconfig.ini'):
        # 获取正确的配置文件路径
        if getattr(sys, 'frozen', False):
            # 打包后的exe环境
            if hasattr(sys, '_MEIPASS'):
                # PyInstaller 打包后的临时目录
                base_path = sys._MEIPASS
            else:
                # 备选路径
                base_path = os.path.dirname(sys.executable)
            self.config_file = os.path.join(base_path, config_file)
        else:
            # 开发环境
            self.config_file = config_file
        self.config = configparser.ConfigParser()
        self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file, encoding='utf-8')
    
    def get_qr_sizes(self):
        """获取所有二维码尺寸"""
        return self.config.sections()
    
    def get_error_levels(self, size):
        """获取指定尺寸的纠错级别"""
        if size in self.config:
            return self.config[size].sections() if hasattr(self.config[size], 'sections') else list(self.config[size].keys())
        return []
    
    def get_capacity(self, size, error_level):
        """获取指定尺寸和纠错级别的数据容量"""
        if size in self.config and error_level in self.config[size]:
            capacity_str = self.config[size][error_level]
            return list(map(int, capacity_str.split(',')))
        return [0, 0, 0, 0]
    
    def get_max_capacity(self, size, error_level, mode):
        """获取指定尺寸、纠错级别和模式的最大容量"""
        capacities = self.get_capacity(size, error_level)
        mode_index = {'numeric': 0, 'alphanumeric': 1, 'byte': 2, 'kanji': 3}
        if mode in mode_index and mode_index[mode] < len(capacities):
            return capacities[mode_index[mode]]
        return 0
