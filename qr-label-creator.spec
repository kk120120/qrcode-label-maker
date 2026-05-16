# qr-label-creator.spec
# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

block_cipher = None

# 读取版本号
app_info_file = Path('app_info.py')
VERSION = 'v1.0.0'
if app_info_file.exists():
    with open(app_info_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip().startswith('VERSION'):
                VERSION = line.split('=')[1].strip().strip('"').strip("'")
                break

# 收集所有需要包含的数据文件
datas_list = [
    ('qrconfig.ini', '.'),
    ('config.json', '.'),
    ('app_info.py', '.'),
]

# 添加 icon_path 目录下的所有文件
icon_dir = Path('icon_path')
if icon_dir.exists():
    for icon_file in icon_dir.iterdir():
        if icon_file.is_file():
            datas_list.append((str(icon_file), 'icon_path'))

# 收集所有需要的 hiddenimports
hidden_imports = [
    'PyQt5.QtWidgets',
    'PyQt5.QtGui',
    'PyQt5.QtCore',
    'PyQt5',
    'PyQt5.QtWidgets.QAction',
    'PyQt5.QtPrintSupport',
    'PIL._tkinter_finder',
    'pandas',
    'openpyxl',
    'calamine',
    'atom',
    'molecule',
    'entry',
    'schedule',
]

# 收集 atom 模块
atom_dir = Path('atom')
if atom_dir.exists():
    for py_file in atom_dir.glob('*.py'):
        if py_file.name != '__init__.py':
            module_name = f'atom.{py_file.stem}'
            hidden_imports.append(module_name)

# 收集 molecule 模块
molecule_dir = Path('molecule')
if molecule_dir.exists():
    for py_file in molecule_dir.glob('*.py'):
        if py_file.name != '__init__.py':
            module_name = f'molecule.{py_file.stem}'
            hidden_imports.append(module_name)

# 收集 entry 模块
entry_dir = Path('entry')
if entry_dir.exists():
    for py_file in entry_dir.glob('*.py'):
        if py_file.name != '__init__.py':
            module_name = f'entry.{py_file.stem}'
            hidden_imports.append(module_name)
    
    # 收集 entry.ui_window 子模块
    ui_window_dir = entry_dir / 'ui_window'
    if ui_window_dir.exists():
        for py_file in ui_window_dir.glob('*.py'):
            if py_file.name != '__init__.py':
                module_name = f'entry.ui_window.{py_file.stem}'
                hidden_imports.append(module_name)
        
        # 收集 entry.ui_window.dialog 子模块
        dialog_dir = ui_window_dir / 'dialog'
        if dialog_dir.exists():
            for py_file in dialog_dir.glob('*.py'):
                if py_file.name != '__init__.py':
                    module_name = f'entry.ui_window.dialog.{py_file.stem}'
                    hidden_imports.append(module_name)
        
        # 收集 entry.ui_window.menu 子模块
        menu_dir = ui_window_dir / 'menu'
        if menu_dir.exists():
            for py_file in menu_dir.glob('*.py'):
                if py_file.name != '__init__.py':
                    module_name = f'entry.ui_window.menu.{py_file.stem}'
                    hidden_imports.append(module_name)

# 收集 schedule 模块
schedule_dir = Path('schedule')
if schedule_dir.exists():
    for py_file in schedule_dir.glob('*.py'):
        if py_file.name != '__init__.py':
            module_name = f'schedule.{py_file.stem}'
            hidden_imports.append(module_name)

a = Analysis(['main.py'],
             pathex=['.'],
             binaries=[],
             datas=datas_list,
             hiddenimports=hidden_imports,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='qr-label-creator',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='icon_path/sw-icon.ico' )
