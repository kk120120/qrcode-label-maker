"""
L4 原子层 - 配置操作
功能：提供配置相关的纯函数原子操作
文件：atom/atom_config.py
"""

import configparser
import os
import sys
from typing import Optional, List


def atom_config_get_user_path() -> str:
    """获取用户配置文件路径"""
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    config_dir = os.path.join(base_dir)
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, "qrconfig.ini")


def atom_config_read(ini_path: str) -> Optional[configparser.ConfigParser]:
    """读取配置文件"""
    try:
        config = configparser.ConfigParser()
        if os.path.exists(ini_path):
            config.read(ini_path, encoding='utf-8')
        return config
    except Exception:
        return None


def atom_config_get_qr_sizes(config: configparser.ConfigParser) -> List[str]:
    """获取二维码尺寸列表"""
    try:
        if 'QR_SIZES' in config:
            return [size.strip() for size in config['QR_SIZES']['sizes'].split(',')]
        return []
    except Exception:
        return []


def atom_config_get_capacity(config: configparser.ConfigParser, version: str, error_level: str) -> Optional[tuple]:
    """获取二维码容量"""
    try:
        if 'CAPACITY' in config:
            key = f"{version}_{error_level}"
            if key in config['CAPACITY']:
                values = config['CAPACITY'][key].split(',')
                if len(values) >= 2:
                    return int(values[0]), float(values[1])
        return None
    except Exception:
        return None
