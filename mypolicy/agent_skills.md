# AI Agent 技能库

> **适用工具**：Trae、Cursor Agent、Subagents系统
> **参考来源**：Cursor Subagents最佳实践、Agent Harness架构、Trae Skills
> **使用方式**：将此文件放在项目根目录的 mypolicy/ 文件夹下，AI编程工具会自动识别并遵循

***

## 目录

| 序号 | Skill 名称                                         | 英文名称                   | 功能描述                  |
| -- | ------------------------------------------------ | ---------------------- | --------------------- |
| 1 | [修复问题](#bug-fix) | `bug_fix` | 理解项目结构、定位问题层级、分析调用链 |
| 2 | [添加新功能](#add-new-feature) | `add_new_feature` | 按照四层架构从原子层到UI层实现新功能 |
| 3 | [修改现有功能](#modify-feature) | `modify_feature` | 定位问题层级、只修改对应层级、保持架构完整 |
| 4 | [代码审查](#code-review) | `code_review` | 检查代码是否符合四层架构规范 |
| 5 | [UI组件开发](#develop-ui-component) | `develop_ui_component` | 开发PyQt5 UI组件，遵循分层架构 |
| 6 | [生成测试用例](#generate-test) | `generate_test` | 为原子层和分子层生成单元测试 |
| 7 | [理解代码](#understand-code) | `understand_code` | 快速理解项目结构和功能实现 |

***

## Skill 1: 修复问题 {#bug-fix}

**Skill名称**：`bug_fix`
**适用场景**：理解项目整体结构、定位 bug 或问题所在层级、分析功能调用链、接手新项目时的代码理解

### 功能描述

快速分析项目四层架构，定位问题所在层级，画出完整调用链。

### 执行步骤（必须完整执行所有7个步骤，不得跳过任何步骤）

#### 第一步：阅读项目规则

1. 阅读 `mypolicy/project_rules.md` 了解四层架构规范
2. 阅读 `new_design.md` 了解项目具体设计

#### 第二步：定位问题层级

根据问题现象判断问题所在层级：

- 按钮点击没反应 → L1 UI层 → `entry/ui_window/`
- 菜单功能异常 → L1 UI层 → `entry/ui_window/`
- 画布绘制问题 → L1 UI层 → `entry/ui_window/designer_canvas.py`
- 业务流程不对 → L2 调度层 → `schedule/schedule_core.py`
- 模板操作错误 → L3 分子层 → `molecule/molecule_template.py`
- 二维码生成失败 → L3 分子层 → `molecule/molecule_qr.py`
- 文件读写错误 → L4 原子层 → `atom/atom_file.py`
- 数据结构问题 → L4 原子层 → `atom/atom_template.py`

#### 第三步：找到相关文件

1. 根据层级定位到具体文件
2. 读取关键代码段

#### 第四步：分析调用链

从用户操作开始，追踪完整调用链：

```
UI层 → entry_ui.py (L1) → schedule_core.py (L2) → molecule_xxx.py (L3) → atom_xxx.py (L4)
```

#### 第五步：给出分析报告

1. 问题可能的原因
2. 需要修改的层级和文件
3. 修改建议

#### 第六步：执行代码修改（此步骤必须执行）

1. 严格遵守分层规则，只修改问题所在层级
2. 不要跨层修改
3. 按照分析报告进行代码修改

#### 第七步：更新文档（此步骤必须执行）

1. 无论修改完成后，必须更新 `new_design.md` 记录变更
2. 添加版本变更记录

### 规则

- 必须完整执行所有7个步骤，特别是第6步和第7步
- 严格遵守四层架构：L1 → L2 → L3 → L4
- 禁止跨层调用
- 禁止分子调用分子
- 禁止原子调用原子
- 修改后必须更新文档

### 示例

**输入**：

```
请帮我分析：修改对象高度时程序崩溃的问题
```

**输出**：

```
问题定位：L4 原子层
相关文件：atom/atom_property.py
调用链：main_window → entry_ui → schedule → molecule_property → atom_property
可能原因：...
修改建议：...
```

***

## Skill 2: 添加新功能 {#add-new-feature}
**Skill名称**：`add_new_feature`
**适用场景**：添加全新的功能模块、创建新的组件或窗口、实现新的业务流程

### 功能描述

按照四层架构标准流程，从原子层到UI层逐步实现新功能。

### 执行步骤

#### 第一步：分析架构

1. 阅读 `mypolicy/project_rules.md` 理解四层架构
2. 阅读 `new_design.md` 了解项目设计
3. 确定需要修改/新增哪些层级

#### 第二步：实现原子层（L4）

1. 在 `atom/` 目录下创建/修改对应的原子文件
2. 每个原子只做一件事
3. 使用纯函数，无副作用
4. 添加完整的类型注解
5. 添加 Google 风格文档字符串

**原子函数命名**：`atom_模块_动作()`

#### 第三步：实现分子层（L3）

1. 在 `molecule/` 目录下创建/修改对应的分子文件
2. 分子只编排原子，不调用其他分子
3. 添加完整的类型注解
4. 添加 Google 风格文档字符串

**分子方法命名**：`molecule_业务_动作()`

#### 第四步：实现调度层（L2）

1. 在 `schedule/schedule_core.py` 中添加调度方法
2. 调度方法只调用分子，不写业务逻辑
3. 添加完整的类型注解
4. 添加 Google 风格文档字符串

**调度方法命名**：`schedule_事件名称()`

#### 第五步：实现入口层（L1）

1. 在 `entry/entry_ui.py` 中添加入口方法
2. 入口方法只转发给调度层
3. 添加完整的类型注解
4. 添加 Google 风格文档字符串

**入口方法命名**：`entry_功能_动作()`

#### 第六步：实现UI层（如果需要）

1. 在 `entry/ui_window/` 下创建/修改UI组件
2. UI组件只通过 `entry_ui.py` 与业务层交互
3. 禁止直接调用分子层或原子层
4. 添加完整的类型注解
5. 添加 Google 风格文档字符串
6. 添加文件头注释，标注 L1 层级

#### 第七步：验证

1. 检查是否违反分层规则
2. 检查 PEP8 规范
3. 验证功能是否正常
4. 更新 `new_design.md` 记录变更

### 规则

- 严格遵守分层依赖：L1 → L2 → L3 → L4
- 禁止反向调用
- 禁止跨层调用
- 禁止分子调用分子
- 禁止原子调用原子
- 函数不超过 100 行
- 所有函数必须有类型注解
- 所有函数必须有文档字符串

### 四层架构示例

```
L4 原子层：纯函数
def atom_qr_calculate_capacity(version: str, error_level: str) -> tuple:
    """原子：计算二维码容量"""
    return capacities.get((version, error_level), (0, 0, 0, 0))
## Skill 3: 修改现有功能 {#modify-feature}
L3 分子层：类调用原子
class QRManager:
    def molecule_qr_get_capacity(self) -> tuple:
        """分子：获取二维码容量"""
        return atom_qr_calculate_capacity(self.current_version, self.error_level)

L2 调度层：类协调分子
class CoreScheduler:
    def schedule_get_qr_capacity(self) -> tuple:
        """调度：获取二维码容量"""
        return self.qr_manager.molecule_qr_get_capacity()

L1 入口层：类转发
class UIEntry:
    def entry_get_qr_capacity(self) -> tuple:
        """入口：获取二维码容量"""
        return self.scheduler.schedule_get_qr_capacity()
```

***

## <a id="modify-feature"></a>Skill 3: 修改现有功能

**Skill名称**：`modify_feature`
**适用场景**：修改现有功能、修复 bug、优化代码、调整业务流程

### 功能描述

先定位问题层级，再只修改对应层级，保持架构完整性。

### 执行步骤

#### 第一步：定位问题

1. 阅读 `mypolicy/project_rules.md` 理解项目架构
2. 使用问题定位速查表确定需要修改哪个层级
3. 找到相关文件

**问题定位速查表**：

| 问题现象    | 检查层级   | 先看哪个文件                               |
| ------- | ------ | ------------------------------------ |
| 按钮点击没反应 | L1 UI层 | entry/ui\_window/tool\_bar.py        |
| 菜单功能异常  | L1 UI层 | entry/ui\_window/menu\_bar.py        |
| 画布绘制问题  | L1 UI层 | entry/ui\_window/designer\_canvas.py |
| 业务流程不对  | L2 调度层 | schedule/schedule\_core.py           |
| 模板操作错误  | L3 分子层 | molecule/molecule\_template.py       |
| 二维码生成失败 | L3 分子层 | molecule/molecule\_qr.py             |
| 文件读写错误  | L4 原子层 | atom/atom\_file.py                   |
| 数据结构问题  | L4 原子层 | atom/atom\_template.py               |

#### 第二步：分析调用链

1. 从UI层开始，追踪调用链
2. 理解当前的实现方式
3. 确定需要修改的具体位置

**调用链格式**：

```
UI层 → entry_ui.py (L1) → schedule_core.py (L2) → molecule_xxx.py (L3) → atom_xxx.py (L4)
```

#### 第三步：只修改对应层级

1. 严格遵守分层规则，只修改问题所在层级
2. 不要跨层修改
3. 不要破坏现有调用链

**各层级职责**：

- **L1 入口层**：接收用户事件，转发给 L2
- **L2 调度层**：协调分子执行顺序，不写业务逻辑
- **L3 分子层**：编排原子操作，不调用其他分子
- **L4 原子层**：纯函数操作，无副作用

#### 第四步：验证修改

1. 检查是否违反分层规则
2. 检查 PEP8 规范
3. 测试功能是否正常
4. 检查是否影响其他功能

**分层检查清单**：

- [ ] 未跨层调用（只修改了问题所在层级）
- [ ] 未反向调用（L3 → L2 → L1 是禁止的）
- [ ] 未分子调用分子
- [ ] 未原子调用原子

#### 第五步：更新文档

1. 更新 `new_design.md` 记录变更
2. 添加版本变更记录

### 规则

- 严格遵守分层依赖：L1 → L2 → L3 → L4
- 禁止反向调用
- 禁止跨层直接调用
- 禁止分子调用分子
- 禁止原子调用原子
- 只修改问题所在层级，不扩大修改范围
- 修改前必须确认用户需求

### 示例

**输入**：

```
请帮我修改：文本属性面板的对齐功能
```

**输出**：

```
问题定位：L1 UI层 + L4 原子层
相关文件：
- ui_components.py (L1) - 添加对齐按钮
- atom/atom_draw.py (L4) - 实现对齐绘制

调用链分析：
main_window → entry_ui → schedule → molecule_draw → atom_draw

修改方案：
1. ui_components.py - 添加左/中/右对齐按钮
2. atom_draw.py - 修改绘制逻辑支持对齐

是否确认修改？
```

***

## <a id="code-review"></a>Skill 4: 代码审查

**Skill名称**：`code_review`
**适用场景**：代码提交前的质量检查、重构前的代码分析、优化现有代码、学习代码库

### 功能描述

检查代码是否符合项目四层架构规范，发现问题并给出重构建议。

### 执行步骤

#### 第一步：阅读项目规则

1. 阅读 `mypolicy/project_rules.md` 理解四层架构
2. 阅读 `new_design.md` 了解项目设计
3. 理解各层级的职责边界

#### 第二步：架构检查

检查文件是否正确遵循分层架构：

**检查清单**：

- [ ] 文件是否正确标注了所属层级？
- [ ] 是否有跨层调用？（L1 → L3/L4 是禁止的）
- [ ] 是否有反向调用？（L3 → L2/L1 是禁止的）
- [ ] 分子是否调用了其他分子？
- [ ] 原子是否调用了其他原子？
- [ ] UI 层是否直接写了业务逻辑？

**层级正确性检查**：

| 文件位置        | 应属层级 | 典型错误       |
| ----------- | ---- | ---------- |
| `entry/`    | L1   | 包含业务逻辑     |
| `schedule/` | L2   | 调用了原子      |
| `molecule/` | L3   | 调用了其他分子    |
| `atom/`     | L4   | 调用了其他原子或分子 |

#### 第三步：代码质量检查

**命名规范检查**：

- [ ] 函数/变量使用蛇形命名？
- [ ] 类使用大驼峰命名？
- [ ] 常量使用全大写命名？
- [ ] 方法命名符合规范？（entry\_/schedule\_/molecule\_/atom\_）

**代码规范检查**：

- [ ] 所有函数是否都有类型注解？
- [ ] 所有函数是否都有文档字符串？
- [ ] 函数是否超过 100 行？
- [ ] 是否符合 PEP8 规范？（缩进，空行、导入顺序）
- [ ] 是否有中文注释？

#### 第四步：生成审查报告

**审查报告格式**：

```markdown
# 代码审查报告

## 概览
- 审查文件：xxx.py
- 层级判定：L?
- 问题总数：N
- 严重：N | 警告：N | 建议：N

## 严重问题
### 1. [问题描述] (第X行)
**问题**：...
**违反规则**：...
**修复建议**：...

## 警告
### 2. [问题描述] (第X行)
...

## 建议
### 3. [问题描述] (第X行)
...
```

#### 第五步：确认并修改

1. 指出具体问题
2. 说明违反了哪条规则
3. 给出修改建议
4. 用户确认后进行修改
5. 更新 `new_design.md` 记录变更

### 规则

- 严格遵守四层架构：L1 → L2 → L3 → L4
- 禁止反向调用
- 禁止跨层调用
- 禁止分子调用分子
- 禁止原子调用原子
- 所有函数必须有类型注解和文档字符串
- 函数不超过 100 行

### 示例

**输入**：

```
请帮我审查：atom/atom_draw.py
```

**输出**：

````
# 代码审查报告

## 概览
- 审查文件：atom/atom_draw.py
- 层级判定：L4 原子层 ✅
- 问题总数：1
- 严重：0 | 警告：1 | 建议：0

## 警告
### 1. 函数参数缺少类型注解 (第XX行)
**问题**：函数参数没有类型注解
**违反规则**：所有函数必须加类型注解
**修复建议**：
```python
def atom_draw_objects(
    painter: QPainter,
    objects: List[Dict[str, Any]],
    ...
) -> None:
````

````

---

## <a id="develop-ui-component"></a>Skill 5: UI组件开发

**Skill名称**：`develop_ui_component`
**适用场景**：创建新的 UI 窗口、创建新的 UI 组件、修改现有 UI 组件、添加新的对话框

### 功能描述
开发 PyQt5 UI 组件时严格遵循分层架构，UI 组件只通过 entry_ui.py 与业务层交互。

### 执行步骤

#### 第一步：确定组件类型
1. 判断是窗口组件还是可复用组件
2. 确定组件在 UI 层中的位置

**组件类型**：
| 组件类型 | 文件位置 | 示例 |
|---------|---------|------|
| 窗口组件 | `entry/ui_window/` | MainWindow, LabelDesigner |
| 可复用组件 | `entry/ui_components/` | PropertyPanel, CSVPreviewDialog |
| 工具栏 | `entry/ui_window/` | ToolBar |
| 菜单栏 | `entry/ui_window/` | MenuBar |

#### 第二步：创建组件文件
1. 在 `entry/ui_window/` 或 `entry/ui_components/` 下创建文件
2. 文件命名：`component_name.py`
3. 类名：大驼峰，如 `ComponentName`

#### 第三步：编写组件代码

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
````

#### 第四步：与业务层交互

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

#### 第五步：注册组件
## Skill 6: 生成测试用例 {#generate-test}
1. 在 `entry/entry_main.py` 或 `entry/ui_window/main_window.py` 中导入组件
2. 创建组件实例
3. 添加到布局或作为子窗口

#### 第六步：验证

1. 检查是否违反分层规则
2. 检查 PEP8 规范
3. 检查信号槽连接是否正确
4. 更新 `new_design.md` 记录变更

### 规则

- 组件文件放在 `entry/ui_window/` 或 `entry/ui_components/` 目录
- 只负责 UI 展示和交互
- 不写任何业务逻辑
- 通过 `main_window.ui_entry` 与业务层交互
- 禁止直接访问 `scheduler` 或 `molecule_manager`
- 所有函数必须有类型注解和文档字符串
- 添加文件头注释，标注 L1 层级

### 示例

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

是否确认开始开发？
```

***

## <a id="generate-test"></a>Skill 6: 生成测试用例

**Skill名称**：`generate_test`
**适用场景**：为原子层函数生成单元测试、为分子层方法生成单元测试、测试驱动开发（TDD）、回归测试用例生成

### 功能描述

根据现有代码自动生成单元测试用例，重点测试原子层和分子层。

### 执行步骤

#### 第一步：分析被测代码

1. 确定是原子层还是分子层
2. 分析函数的输入输出
3. 确定测试边界条件

**测试分层**：

| 层级     | 测试重点   | 测试文件位置                 |
| ------ | ------ | ---------------------- |
| L4 原子层 | 纯函数逻辑  | `tests/test_atom/`     |
| L3 分子层 | 业务编排逻辑 | `tests/test_molecule/` |

#### 第二步：创建测试文件

1. 创建 `tests/` 目录（如果不存在）
2. 创建 `tests/test_atom/` 或 `tests/test_molecule/` 目录
3. 文件命名：`test_[原文件名].py`

#### 第三步：编写测试用例

**测试规范**：

```python
"""
L4 原子层测试 - atom_template 测试
"""
import pytest
from atom.atom_template import (
    atom_template_create_default,
    atom_template_add_object,
    atom_template_remove_object
)


class TestAtomTemplate:
    """atom_template 模块测试"""

    def test_atom_template_create_default(self):
        """测试创建默认模板"""
        result = atom_template_create_default()
        assert result is not None
        assert 'objects' in result
        assert isinstance(result['objects'], list)

    def test_atom_template_add_object(self):
        """测试添加对象到模板"""
        template = atom_template_create_default()
        obj = {'id': 'test-001', 'type': 'qr'}
        result = atom_template_add_object(template, obj)
        assert len(result['objects']) == 1
        assert result['objects'][0]['id'] == 'test-001'
```

**Arrange-Act-Assert 模式**：

```python
def test_something(self):
    # Arrange - 准备测试数据
## Skill 7: 理解代码 {#understand-code}
    expected_result = ...

    # Act - 执行被测函数
    actual_result = function_under_test(input_data)

    # Assert - 验证结果
    assert actual_result == expected_result
```

#### 第四步：处理依赖

- 原子层测试：通常无外部依赖，直接测试
- 分子层测试：需要 mock 原子函数

**Mock 示例**：

```python
from unittest.mock import patch

@patch('molecule.molecule_template.atom_template_add_object')
def test_molecule_with_mock(mock_add_object):
    mock_add_object.return_value = {'objects': []}
    # 测试分子方法
```

#### 第五步：运行测试

1. 运行单个测试文件
2. 运行所有测试
3. 修复失败的测试

### 规则

- 使用 pytest 框架
- 每个测试函数测试一个功能点
- 测试函数命名：`test_[功能描述]`
- 必须有类型注解和文档字符串
- 使用 Arrange-Act-Assert 模式
- 原子层测试不 mock
- 分子层测试可 mock 原子函数

### 示例

**输入**：

```
请帮我为 atom/atom_csv.py 生成测试用例
```

**输出**：

```
测试设计：
文件：tests/test_atom/test_atom_csv.py
测试函数：
1. test_atom_csv_read_success - 测试成功读取CSV
2. test_atom_csv_read_file_not_found - 测试文件不存在
3. test_atom_csv_get_columns - 测试获取列名
4. test_atom_csv_get_row - 测试获取行数据

是否确认生成？
```

***

## <a id="understand-code"></a>Skill 7: 理解代码

**Skill名称**：`understand_code`
**适用场景**：理解现有功能、学习代码库、接手新项目、分析复杂调用链

### 功能描述

快速理解项目结构和某个功能的完整实现，包括调用链和数据流。

### 执行步骤

#### 第一步：项目结构概览

1. 阅读 `mypolicy/project_rules.md` 理解四层架构
2. 阅读 `new_design.md` 了解项目设计
3. 理解目录结构和各层职责

**四层架构职责**：

| 层级     | 目录          | 职责        | 示例文件                           |
| ------ | ----------- | --------- | ------------------------------ |
| L1 入口层 | `entry/`    | 接收用户事件，转发 | entry\_ui.py, main\_window\.py |
| L2 调度层 | `schedule/` | 协调分子执行顺序  | schedule\_core.py              |
| L3 分子层 | `molecule/` | 编排原子操作    | molecule\_template.py          |
| L4 原子层 | `atom/`     | 纯函数操作     | atom\_template.py              |

#### 第二步：功能调用链分析

1. 从用户操作开始追踪
2. 列出完整调用链
3. 标注每个层级的文件和方法

**调用链格式**：

```
用户操作 → UI组件 (L1) → entry_ui.py (L1) → schedule_core.py (L2) → molecule_xxx.py (L3) → atom_xxx.py (L4)
```

#### 第三步：逐层级讲解

对每个层级进行详细讲解：

**L1 入口层**：

- 接收什么事件？
- 如何转发给调度层？
- 涉及哪些文件？

**L2 调度层**：

- 调用了哪些分子？
- 执行顺序是什么？
- 有什么条件判断？

**L3 分子层**：

- 编排了哪些原子函数？
- 数据如何转换？
- 返回什么？

**L4 原子层**：

- 纯函数做什么？
- 输入输出是什么？
- 有副作用吗？

#### 第四步：数据流分析

1. 数据输入在哪里？
2. 数据在每层如何变化？
3. 最终输出是什么？
4. 数据存储在哪里？

#### 第五步：总结

1. 这个功能的整体设计思路
2. 值得学习的地方
3. 如果要修改，应该从哪里入手
4. 潜在的问题和风险

### 规则

- 严格按照四层架构分析
- 追踪完整调用链
- 标注每个文件和方法
- 说明数据流向
- 指出关键代码位置

### 示例

**输入**：

```
请帮我理解：CSV导入功能的实现
```

**输出**：

```
# CSV导入功能理解

## 1. 功能概述
用户通过文件选择对话框选择CSV文件，系统解析文件内容并显示预览。

## 2. 调用链
```

CSVPreviewDialog → main\_window\.ui\_entry.entry\_import\_csv()
→ schedule\_core.schedule\_import\_csv()
→ molecule\_csv.molecule\_csv\_import()
→ atom\_csv\_read()

```

## 3. 逐层分析

### L1 入口层
**文件**：`entry/entry_ui.py`
**方法**：`entry_import_csv(file_path)`

### L2 调度层
**文件**：`schedule/schedule_core.py`
**方法**：`schedule_import_csv(file_path)`

### L3 分子层
**文件**：`molecule/molecule_csv.py`
**类**：`CSVManager`
**方法**：`molecule_csv_import(file_path)`

### L4 原子层
**文件**：`atom/atom_csv.py`
**函数**：`atom_csv_read(file_path)`

## 4. 数据流
1. 用户选择文件 → 文件路径
2. L1 转发路径
3. L2 调度
4. L3 解析 → DataFrame
5. L4 读取 → DataFrame

## 5. 修改建议
如果要修改CSV解析逻辑，修改 atom/atom_csv.py
如果要修改预览逻辑，修改 ui_components.py 中的 CSVPreviewDialog
```

***

## 快速参考

### 问题定位速查

| 问题现象                        | 检查层级   |
| --------------------------- | ------ |
| UI问题 → L1 entry/ui\_window/ | <br /> |
| 流程问题 → L2 schedule/         | <br /> |
| 业务问题 → L3 molecule/         | <br /> |
| 数据问题 → L4 atom/             | <br /> |

### 文件命名速查

- 入口方法: `entry_xxx_yyy()`
- 调度方法: `schedule_xxx_yyy()`
- 分子方法: `molecule_xxx_yyy()`
- 原子方法: `atom_xxx_yyy()`

### 调用链速查

```
用户操作 → UI组件 (entry/ui_window/) → entry_ui.py (入口转发) → schedule_core.py (调度) → molecule_xxx.py (分子) → atom_xxx.py (原子)
```

