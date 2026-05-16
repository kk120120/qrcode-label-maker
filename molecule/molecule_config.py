"""
L3 分子层 - 配置管理
功能：编排原子操作，实现完整业务动作
文件：molecule/molecule_config.py
"""

import configparser
import os
import shutil
from typing import Optional, List, Tuple
from atom.atom_config import (
    atom_config_read, 
    atom_config_get_qr_sizes, 
    atom_config_get_capacity,
    atom_config_get_user_path
)


class ConfigManager:
    """配置管理器"""
    def __init__(self, ini_path: str = None):
        if ini_path is None:
            # 使用用户配置路径
            self.ini_path = atom_config_get_user_path()
        else:
            self.ini_path = ini_path
        
        # 如果用户配置不存在，尝试从默认位置复制
        if not os.path.exists(self.ini_path) and ini_path is None:
            try:
                # 尝试找到默认配置文件
                default_path = "qrconfig.ini"
                if os.path.exists(default_path):
                    shutil.copy(default_path, self.ini_path)
            except Exception:
                pass
        
        self.config = atom_config_read(self.ini_path)

    def molecule_config_get_qr_sizes(self) -> List[str]:
        """获取二维码尺寸列表"""
        if self.config:
            return atom_config_get_qr_sizes(self.config)
        return []

    def molecule_config_get_capacity(self, version: str, error_level: str) -> Optional[Tuple[int, float]]:
        """获取二维码容量"""
        if self.config:
            capacity = atom_config_get_capacity(self.config, version, error_level)
            if capacity:
                return capacity
        # 如果配置文件中没有，使用原子层的默认值
        from atom.atom_qr import atom_qr_get_capacity
        return atom_qr_get_capacity(version, error_level)

    def molecule_config_get_last_open_dir(self) -> Optional[str]:
        """获取上次打开目录"""
        if self.config and 'SETTINGS' in self.config:
            return self.config['SETTINGS'].get('last_open_dir')
        return None

    def molecule_config_set_last_open_dir(self, directory: str) -> None:
        """设置上次打开目录"""
        if not self.config:
            self.config = configparser.ConfigParser()
        if 'SETTINGS' not in self.config:
            self.config['SETTINGS'] = {}
        self.config['SETTINGS']['last_open_dir'] = directory
        self._save_config()

    def molecule_config_get_last_import_dir(self) -> Optional[str]:
        """获取上次导入目录"""
        if self.config and 'SETTINGS' in self.config:
            return self.config['SETTINGS'].get('last_import_dir')
        return None

    def molecule_config_set_last_import_dir(self, directory: str) -> None:
        """设置上次导入目录"""
        if not self.config:
            self.config = configparser.ConfigParser()
        if 'SETTINGS' not in self.config:
            self.config['SETTINGS'] = {}
        self.config['SETTINGS']['last_import_dir'] = directory
        self._save_config()

    def molecule_config_get_last_export_dir(self) -> Optional[str]:
        """获取上次导出目录"""
        if self.config and 'SETTINGS' in self.config:
            return self.config['SETTINGS'].get('last_export_dir')
        return None

    def molecule_config_set_last_export_dir(self, directory: str) -> None:
        """设置上次导出目录"""
        if not self.config:
            self.config = configparser.ConfigParser()
        if 'SETTINGS' not in self.config:
            self.config['SETTINGS'] = {}
        self.config['SETTINGS']['last_export_dir'] = directory
        self._save_config()

    def _save_config(self) -> None:
        """保存配置"""
        try:
            with open(self.ini_path, 'w', encoding='utf-8') as f:
                self.config.write(f)
        except Exception:
            pass
