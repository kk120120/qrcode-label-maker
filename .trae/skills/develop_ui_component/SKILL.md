---
name: "develop_ui_component"
description: "Develops PyQt5 UI components following L1 layer rules. Invoke when user asks to create or modify UI components."
---

# UI Component Development

开发 PyQt5 UI 组件时严格遵循分层架构，UI 组件只通过 entry_ui.py 与业务层交互。

## 适用场景
- 创建新的 UI 窗口
- 创建新的 UI 组件
- 修改现有 UI 组件
- 添加新的对话框

## 执行步骤（必须完整执行所有6个步骤，不得跳过任何步骤）

### 第一步：确定组件类型
1. 判断是窗口组件还是可复用组件
2. 确定组件在 UI 层中的位置

**组件类型**：
| 组件类型 | 文件位置 | 示例 |
|---------|---------|------|
| 窗口组件 | `entry/ui_window/` | MainWindow, LabelDesigner |
| 可复用组件 | `entry/ui_components/` | PropertyPanel, CSVPreviewDialog |
| 工具栏 | `entry/ui_window/` | ToolBar |
| 菜单栏 | `entry/ui_window/` | MenuBar |

### 第二步：创建组件文件
1. 在 `entry/ui_window/` 或 `entry/ui_components/` 下创建文件
2. 文件命名：`component_name.py`
3. 类名：大驼峰，如 `ComponentName`

### 第三步：编写组件代码

**组件规范**：
```python
"""
L1 入口层 - UI组件
功能：[组件功能描述]
文件：entry/ui_window/xxx.py
"""

from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from typing import Optional

class ComponentName(QWidget):
    """组件描述"""

    def __init__(self, main_window, parent: Optional[QWidget] = None):
        """初始化组件

        Args:
            main_window: 主窗口引用
            parent: 父组件
        """
        super().__init__(parent)
        self.main_window = main_window
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)

    def _connect_signals(self) -> None:
        """连接信号槽"""
        pass
```

### 第四步：与业务层交互

**正确的交互方式**：
```python
# ✅ 正确：通过 ui_entry 访问业务层
def on_button_clicked(self):
    self.main_window.ui_entry.entry_some_action(params)

# ❌ 错误：直接访问调度层
def on_button_clicked(self):
    self.main_window.scheduler.schedule_some_action(params)

# ❌ 错误：直接访问分子层
def on_button_clicked(self):
    self.main_window.some_manager.molecule_some_action(params)
```

### 第五步：注册组件
1. 在 `entry/entry_main.py` 或 `entry/ui_window/main_window.py` 中导入组件
2. 创建组件实例
3. 添加到布局或作为子窗口

### 第六步：验证（此步骤必须执行）
1. 检查是否违反分层规则
2. 检查 PEP8 规范
3. 检查信号槽连接是否正确
4. 必须更新 `new_design.md` 记录变更

## 规则
- 必须完整执行所有6个步骤，特别是第6步
- 组件文件放在 `entry/ui_window/` 或 `entry/ui_components/` 目录
- 只负责 UI 展示和交互
- 不写任何业务逻辑
- 通过 `main_window.ui_entry` 与业务层交互
- 禁止直接访问 `scheduler` 或 `molecule_manager`
- 所有函数必须有类型注解和文档字符串
- 添加文件头注释，标注 L1 层级
- 完成后必须更新 `new_design.md`

## 示例

**输入**：
```
请帮我开发一个批量导出对话框组件
```

**输出**：
```
组件设计：BatchExportDialog
文件位置：entry/ui_components/batch_export_dialog.py
层级：L1 入口层

UI 结构：
- QDialog
  - QVBoxLayout
    - 文件格式选择 (QComboBox)
    - 导出路径选择 (QLineEdit + QPushButton)
    - 进度条 (QProgressBar)
    - 按钮栏 (确定/取消)

业务交互：
- 确定 → main_window.ui_entry.entry_batch_export(...)
- 取消 → close()

**是否确认开始开发？**
```
