# QR Label Creator - Code Wiki

> 批量二维码标签生成器 - 完整代码文档

---

## 目录

1. [项目概述](#项目概述)
2. [技术栈](#技术栈)
3. [架构设计](#架构设计)
4. [项目结构](#项目结构)
5. [.trae 目录分析](#trae-目录分析)
6. [核心模块详解](#核心模块详解)
7. [数据流与调用链](#数据流与调用链)
8. [开发指南](#开发指南)
9. [常见问题](#常见问题)

---

## 项目概述

### 项目简介

QR Label Creator 是一款基于 Python + PyQt5 开发的桌面二维码标签生成工具，支持：
- 以毫米(mm)为单位的精确标签尺寸设计
- 可视化拖拽编辑
- 二维码参数自定义（尺寸、纠错等级、数据容量提示）
- 文本全样式自定义（字体、大小、颜色、样式）
- CSV/Excel 数据导入与批量绑定
- 模板本地保存/加载
- 单张/批量导出（PNG/PDF格式）

### 项目背景

在互联网上难以找到满足以下需求的免费工具：
1. 支持批量 CSV 内容生成 QR 码
2. 支持用户自定义标签尺寸、设计二维码/文本元素
3. 实现单张/批量二维码标签 PNG 导出

该项目旨在填补这一空白。

---

## 技术栈

| 类别 | 技术/库 | 用途 |
|------|---------|------|
| 开发语言 | Python 3.8+ | 核心开发语言 |
| GUI 框架 | PyQt5 | 桌面界面开发 |
| 二维码生成 | qrcode[pil] | 二维码图像生成 |
| 图像处理 | Pillow | 图像合成与处理 |
| 数据处理 | pandas | CSV/Excel 数据处理 |
| Excel 读取 | openpyxl, python-calamine | Excel 文件读写 |
| 配置解析 | json | 模板配置存储 |

---

## 架构设计

### 四层架构 (4-Layer Architecture)

项目采用严格的四层架构设计，确保职责分离和代码可维护性：

```
┌─────────────────────────────────────────────┐
│   L1: 入口层 (Entry Layer)                  │
│   - main.py                                 │
│   - entry/entry_main.py                     │
│   - entry/entry_ui.py                       │
│   - entry/ui_window/*                       │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│   L2: 调度层 (Scheduler Layer)              │
│   - schedule/schedule_core.py               │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│   L3: 分子层 (Molecule Layer)               │
│   - molecule/molecule_*.py                  │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│   L4: 原子层 (Atom Layer)                   │
│   - atom/atom_*.py                          │
└─────────────────────────────────────────────┘
```

### 架构规则

1. **单向依赖**：只能上层调用下层，禁止反向调用
2. **禁止跨层**：L1 不能直接调用 L3/L4，必须通过 L2
3. **分子隔离**：分子之间不能互相调用，必须通过调度层
4. **原子纯净**：原子层使用纯函数，无副作用

### 各层职责

| 层级 | 职责 | 示例 |
|------|------|------|
| L1 入口层 | 接收用户事件、转发给调度层、组装 UI | entry_ui.py, main_window.py |
| L2 调度层 | 事件调度、编排分子执行顺序、异常处理 | schedule_core.py |
| L3 分子层 | 完整业务动作、编排原子操作、管理状态 | molecule_template.py |
| L4 原子层 | 单一职责纯函数、原子操作 | atom_qr.py, atom_template.py |

---

## 项目结构

```
qr-label-creator/
├── main.py                           # [L1] 总入口
├── requirements.txt                  # 依赖列表
├── config.json                       # 配置文件
├── app.log                           # 日志文件
├── LICENSE                           # 许可证
├── README.md                         # 用户文档
├── CODE_WIKI.md                      # 开发者文档 (本文件)
│
├── .trae/                            # Trae IDE 配置目录
│   ├── rules/                        # 项目规则
│   │   └── myqrproj.md.disabled      # 项目架构规范 (已禁用)
│   └── skills/                       # AI 技能定义
│       ├── add_new_feature/          # 添加新功能技能
│       ├── bug_fix/                  # 问题修复技能
│       ├── code_review/              # 代码审查技能
│       ├── develop_ui_component/     # UI 组件开发技能
│       ├── generate_test/            # 测试生成技能
│       ├── modify_feature/           # 功能修改技能
│       └── understand_code/          # 代码理解技能
│
├── entry/                            # [L1] 入口层
│   ├── entry_main.py                 # 主窗口入口
│   ├── entry_ui.py                   # UI 事件入口
│   └── ui_window/                    # UI 组件
│       ├── main_window.py            # 主窗口
│       ├── designer_canvas.py        # 设计画布
│       ├── property_panel.py         # 属性面板
│       ├── toolbar.py                # 工具栏
│       ├── dialog/                   # 对话框
│       │   ├── basic_settings_dialog.py
│       │   ├── csv_preview_dialog.py
│       │   ├── batch_export_dialog.py
│       │   └── preview_dialog.py
│       └── menu/                     # 菜单
│           ├── menu_file.py
│           ├── menu_settings.py
│           ├── menu_import.py
│           ├── menu_export.py
│           ├── menu_history.py
│           └── menu_help.py
│
├── schedule/                         # [L2] 调度层
│   └── schedule_core.py              # 核心调度器
│
├── molecule/                         # [L3] 分子层
│   ├── molecule_template.py          # 模板管理
│   ├── molecule_csv.py               # CSV 管理
│   ├── molecule_config.py            # 配置管理
│   ├── molecule_image.py             # 图像管理
│   ├── molecule_history.py           # 历史记录管理
│   └── molecule_draw.py              # 绘制管理
│
├── atom/                             # [L4] 原子层
│   ├── atom_template.py              # 模板操作
│   ├── atom_qr.py                    # 二维码操作
│   ├── atom_text.py                  # 文本操作
│   ├── atom_image.py                 # 图像操作
│   ├── atom_csv.py                   # CSV 操作
│   ├── atom_config.py                # 配置操作
│   ├── atom_history.py               # 历史记录操作
│   ├── atom_property.py              # 属性操作
│   ├── atom_file.py                  # 文件操作
│   └── atom_init.py                  # 初始化操作
│
├── icon_path/                        # 图标资源
│   ├── sw-icon.ico
│   └── sw-icon.png
│
├── mypolicy/                         # 开发策略
│   ├── project_rules.md              # 项目规范
│   ├── personal_rules.md
│   └── agent_skills.md
│
└── mywork/                           # 工作目录 (示例数据)
    ├── batchQR/                      # 批量生成示例
    ├── qrconfig.ini
    └── create_icon.py
```

---

## .trae 目录分析

### 目录概述

`.trae/` 目录是 Trae IDE 的配置目录，用于存储项目特定的规则和 AI 技能定义。该目录帮助 AI 助手更好地理解项目架构和开发流程。

### 目录结构

```
.trae/
├── rules/                    # 项目规则定义
│   └── myqrproj.md.disabled  # 项目架构规范 (已禁用)
└── skills/                   # AI 技能定义
    ├── add_new_feature/      # 添加新功能技能
    ├── bug_fix/              # 问题修复技能
    ├── code_review/          # 代码审查技能
    ├── develop_ui_component/ # UI 组件开发技能
    ├── generate_test/        # 测试生成技能
    ├── modify_feature/       # 功能修改技能
    └── understand_code/      # 代码理解技能
```

### rules/ 目录

**文件**: [.trae/rules/myqrproj.md.disabled](file:///e:/99_pri_sync/python项目/qr-label-creator/.trae/rules/myqrproj.md.disabled)

**说明**: 该文件包含项目的完整架构规范，与 `mypolicy/project_rules.md` 内容相同。由于文件后缀为 `.disabled`，该规则当前未被 Trae IDE 自动应用。

**主要内容**:
- 四层架构铁律
- 各层职责详解
- 编程范式与四层架构结合
- 编码规范
- AI 开发工作流
- 问题定位速查表

### skills/ 目录详解

每个技能目录包含一个 `SKILL.md` 文件，定义了特定开发任务的执行流程。

#### 1. add_new_feature 技能

**文件**: [.trae/skills/add_new_feature/SKILL.md](file:///e:/99_pri_sync/python项目/qr-label-creator/.trae/skills/add_new_feature/SKILL.md)

**适用场景**: 添加全新功能模块、创建新组件或窗口、实现新业务流程

**执行步骤**:
1. 分析架构 - 阅读项目规则确定需要修改的层级
2. 实现原子层 (L4) - 在 `atom/` 中创建纯函数
3. 实现分子层 (L3) - 在 `molecule/` 中编排原子操作
4. 实现调度层 (L2) - 在 `schedule_core.py` 添加调度方法
5. 实现入口层 (L1) - 在 `entry_ui.py` 添加入口方法
6. 实现 UI 层 - 在 UI 组件中添加交互
7. 验证 - 检查规范、测试功能、更新文档

**核心规则**:
- 严格遵守分层依赖：L1 → L2 → L3 → L4
- 禁止反向调用和跨层调用
- 所有函数必须有类型注解和文档字符串
- 完成后必须更新 `new_design.md`

#### 2. bug_fix 技能

**文件**: [.trae/skills/bug_fix/SKILL.md](file:///e:/99_pri_sync/python项目/qr-label-creator/.trae/skills/bug_fix/SKILL.md)

**适用场景**: 理解项目结构、定位 bug、分析功能调用链、接手新项目

**执行步骤**:
1. 阅读项目规则 - 理解四层架构
2. 定位问题层级 - 使用问题定位速查表
3. 找到相关文件 - 定位到具体文件
4. 分析调用链 - 追踪完整调用路径
5. 给出分析报告 - 问题原因和修改建议
6. 执行代码修改 - 只修改问题所在层级
7. 更新文档 - 更新 `new_design.md`

**问题定位速查表**:
| 问题现象 | 检查层级 | 先看哪个文件 |
|---------|---------|-------------|
| 按钮点击没反应 | L1 UI层 | entry/ui_window/tool_bar.py |
| 菜单功能异常 | L1 UI层 | entry/ui_window/menu_bar.py |
| 画布绘制问题 | L1 UI层 | entry/ui_window/designer_canvas.py |
| 业务流程不对 | L2 调度层 | schedule/schedule_core.py |
| 模板操作错误 | L3 分子层 | molecule/molecule_template.py |
| 二维码生成失败 | L3 分子层 | molecule/molecule_qr.py |
| 文件读写错误 | L4 原子层 | atom/atom_file.py |
| 数据结构问题 | L4 原子层 | atom/atom_template.py |

#### 3. code_review 技能

**文件**: [.trae/skills/code_review/SKILL.md](file:///e:/99_pri_sync/python项目/qr-label-creator/.trae/skills/code_review/SKILL.md)

**适用场景**: 代码提交前质量检查、重构前分析、优化现有代码、学习代码库

**检查清单**:
- 文件是否正确标注所属层级
- 是否有跨层调用
- 是否有反向调用
- 分子是否调用其他分子
- 原子是否调用其他原子
- UI 层是否直接写业务逻辑
- 命名是否符合规范
- 函数是否有类型注解和文档字符串
- 函数是否超过 100 行
- 是否符合 PEP8 规范

#### 4. develop_ui_component 技能

**文件**: [.trae/skills/develop_ui_component/SKILL.md](file:///e:/99_pri_sync/python项目/qr-label-creator/.trae/skills/develop_ui_component/SKILL.md)

**适用场景**: 创建新 UI 窗口、创建新 UI 组件、修改现有 UI 组件、添加新对话框

**组件位置规范**:
| 组件类型 | 文件位置 |
|---------|---------|
| 窗口组件 | `entry/ui_window/` |
| 可复用组件 | `entry/ui_components/` |
| 工具栏 | `entry/ui_window/` |
| 菜单栏 | `entry/ui_window/` |

**UI 交互规范**:
- ✅ 正确：通过 `main_window.ui_entry` 访问业务层
- ❌ 错误：直接访问调度层
- ❌ 错误：直接访问分子层

#### 5. generate_test 技能

**文件**: [.trae/skills/generate_test/SKILL.md](file:///e:/99_pri_sync/python项目/qr-label-creator/.trae/skills/generate_test/SKILL.md)

**适用场景**: 为原子层生成单元测试、为分子层生成单元测试、测试驱动开发、回归测试

**测试分层**:
| 层级 | 测试重点 | 测试文件位置 |
|-----|---------|-------------|
| L4 原子层 | 纯函数逻辑 | `tests/test_atom/` |
| L3 分子层 | 业务编排逻辑 | `tests/test_molecule/` |

**测试规范**:
- 使用 pytest 框架
- 使用 Arrange-Act-Assert 模式
- 原子层测试不 mock
- 分子层测试可 mock 原子函数

#### 6. modify_feature 技能

**文件**: [.trae/skills/modify_feature/SKILL.md](file:///e:/99_pri_sync/python项目/qr-label-creator/.trae/skills/modify_feature/SKILL.md)

**适用场景**: 修改现有功能、修复 bug、优化代码、调整业务流程

**执行步骤**:
1. 定位问题 - 使用问题定位速查表
2. 分析调用链 - 追踪完整调用路径
3. 只修改对应层级 - 严格遵守分层规则，不跨层修改
4. 验证修改 - 检查规范、测试功能
5. 更新文档 - 更新 `new_design.md`

**各层职责**:
- **L1 入口层**: 接收用户事件，转发给 L2
- **L2 调度层**: 协调分子执行顺序，不写业务逻辑
- **L3 分子层**: 编排原子操作，不调用其他分子
- **L4 原子层**: 纯函数操作，无副作用

#### 7. understand_code 技能

**文件**: [.trae/skills/understand_code/SKILL.md](file:///e:/99_pri_sync/python项目/qr-label-creator/.trae/skills/understand_code/SKILL.md)

**适用场景**: 理解现有功能、学习代码库、接手新项目、分析复杂调用链

**执行步骤**:
1. 项目结构概览 - 理解四层架构
2. 功能调用链分析 - 从用户操作开始追踪
3. 逐层级讲解 - 分析每个层级的实现
4. 数据流分析 - 追踪数据在各层的变化
5. 总结 - 给出整体设计思路和修改建议

**四层架构职责表**:
| 层级 | 目录 | 职责 | 示例文件 |
|-----|------|------|---------|
| L1 入口层 | `entry/` | 接收用户事件，转发 | entry_ui.py, main_window.py |
| L2 调度层 | `schedule/` | 协调分子执行顺序 | schedule_core.py |
| L3 分子层 | `molecule/` | 编排原子操作 | molecule_template.py |
| L4 原子层 | `atom/` | 纯函数操作 | atom_template.py |

### .trae 目录的重要性

1. **AI 助手指导**: 为 Trae IDE 的 AI 助手提供明确的开发流程指导
2. **架构一致性**: 确保所有开发人员遵循相同的四层架构
3. **开发效率**: 通过预定义的技能模板加速常见开发任务
4. **知识沉淀**: 将项目最佳实践和编码规范文档化

### 与 mypolicy/ 目录的关系

`.trae/` 目录与 `mypolicy/` 目录内容相似，但用途不同：
- `.trae/` 目录专门为 Trae IDE 配置，技能文件可被 IDE 自动识别和调用
- `mypolicy/` 目录为通用项目规范，供开发者阅读和参考

---

## 核心模块详解

### L1 入口层 (Entry Layer)

#### main.py

**文件**: [main.py](file:///e:/99_pri_sync/python项目/qr-label-creator/main.py)

**职责**: 程序总入口，负责：
- 初始化日志系统
- 检查依赖版本
- 加载/保存配置
- 创建 QApplication
- 调用 L1 层启动界面

**核心函数**:

| 函数 | 说明 |
|------|------|
| `check_dependencies()` | 检查并记录依赖库版本 |
| `load_config()` | 加载 config.json 配置 |
| `save_config(config)` | 保存配置到文件 |
| `main()` | 程序主入口 |

#### entry_main.py

**文件**: [entry/entry_main.py](file:///e:/99_pri_sync/python项目/qr-label-creator/entry/entry_main.py)

**职责**: 创建和管理主窗口

**核心类**: `EntryMain`

| 方法 | 说明 |
|------|------|
| `create_main_window()` | 创建并返回主窗口 |
| `show_window()` | 显示主窗口 |
| `close_window()` | 关闭主窗口 |

#### entry_ui.py

**文件**: [entry/entry_ui.py](file:///e:/99_pri_sync/python项目/qr-label-creator/entry/entry_ui.py)

**职责**: UI 事件入口，所有用户操作都通过此类转发给调度层

**核心类**: `UIEntry`

| 方法 | 说明 |
|------|------|
| `entry_init_template()` | 初始化模板 |
| `entry_new_template()` | 新建模板 |
| `entry_open_template(file_path)` | 打开模板文件 |
| `entry_save_template(file_path)` | 保存模板文件 |
| `entry_add_qr_object(x, y, ...)` | 添加二维码对象 |
| `entry_add_text_object(x, y, ...)` | 添加文本对象 |
| `entry_update_object(obj_id, **kwargs)` | 更新对象属性 |
| `entry_import_csv(file_path)` | 导入 CSV |
| `entry_import_excel(file_path)` | 导入 Excel |
| `entry_export_current(file_path)` | 导出当前标签 |
| `entry_batch_export(output_dir, ...)` | 批量导出 |
| `entry_history_save()` | 保存历史记录 |
| `entry_history_undo()` | 撤销操作 |
| `entry_history_redo()` | 重做操作 |

#### main_window.py

**文件**: [entry/ui_window/main_window.py](file:///e:/99_pri_sync/python项目/qr-label-creator/entry/ui_window/main_window.py)

**职责**: 主窗口 UI 组件，组装所有 UI 元素并管理用户交互

**核心类**: `MainWindow(QMainWindow)`

| 组件 | 说明 |
|------|------|
| `FileMenu` | 文件菜单 (新建/打开/保存) |
| `SettingsMenu` | 设置菜单 (基础设置) |
| `ImportMenu` | 导入菜单 (CSV/Excel) |
| `ExportMenu` | 导出菜单 (单张/批量) |
| `HistoryMenu` | 历史菜单 (撤销/重做) |
| `HelpMenu` | 帮助菜单 (关于) |
| `DesignerToolbar` | 工具栏 (QR/文本/预览) |
| `LabelDesigner` | 设计画布 |
| `PropertyPanel` | 属性面板 |

**核心方法**:

| 方法 | 说明 |
|------|------|
| `init_ui()` | 初始化 UI 布局 |
| `new_template()` | 新建模板 |
| `open_template()` | 打开模板 |
| `save_template()` | 保存模板 |
| `import_csv()` / `import_excel()` | 导入数据 |
| `export_current_label()` | 单张导出 |
| `open_batch_export_dialog()` | 批量导出 |
| `save_object_properties()` | 保存对象属性 |
| `undo()` / `redo()` | 撤销/重做 |

---

### L2 调度层 (Scheduler Layer)

#### schedule_core.py

**文件**: [schedule/schedule_core.py](file:///e:/99_pri_sync/python项目/qr-label-creator/schedule/schedule_core.py)

**职责**: 核心调度器，管理所有分子管理器，编排业务流程

**核心类**: `CoreScheduler`

**成员变量**:

| 成员 | 类型 | 说明 |
|------|------|------|
| `template_manager` | TemplateManager | 模板管理器 |
| `csv_manager` | CSVManager | CSV 管理器 |
| `config_manager` | ConfigManager | 配置管理器 |
| `image_manager` | ImageManager | 图像管理器 |
| `history_manager` | HistoryManager | 历史记录管理器 |

**核心方法**:

| 方法 | 说明 |
|------|------|
| `schedule_init_template()` | 初始化模板 |
| `schedule_new_template()` | 新建模板 |
| `schedule_add_qr_object(...)` | 调度添加二维码 |
| `schedule_add_text_object(...)` | 调度添加文本 |
| `schedule_update_object(...)` | 调度更新对象 |
| `schedule_import_csv(file_path)` | 调度导入 CSV |
| `schedule_export_current(file_path)` | 调度单张导出 |
| `schedule_batch_export(...)` | 调度批量导出 |
| `schedule_history_save()` | 保存历史 |
| `schedule_history_undo()` | 撤销历史 |
| `schedule_history_redo()` | 重做历史 |

---

### L3 分子层 (Molecule Layer)

#### molecule_template.py

**文件**: [molecule/molecule_template.py](file:///e:/99_pri_sync/python项目/qr-label-creator/molecule/molecule_template.py)

**职责**: 模板管理器，负责模板数据的创建、加载、保存、更新

**核心类**: `TemplateManager`

**成员变量**:

| 成员 | 类型 | 说明 |
|------|------|------|
| `template` | dict | 模板数据 |
| `selected_object_id` | str or None | 选中对象 ID |

**核心方法**:

| 方法 | 说明 |
|------|------|
| `molecule_template_init()` | 初始化模板 |
| `molecule_template_new()` | 新建模板 |
| `molecule_template_open(file_path)` | 打开模板文件 |
| `molecule_template_save(file_path)` | 保存模板文件 |
| `molecule_template_add_qr_object(...)` | 添加二维码对象 |
| `molecule_template_add_text_object(...)` | 添加文本对象 |
| `molecule_template_remove_object(obj_id)` | 移除对象 |
| `molecule_template_update_object_properties(...)` | 更新对象属性 |
| `molecule_template_set_label_size(...)` | 设置标签尺寸 |
| `molecule_template_set_dpi(dpi)` | 设置 DPI |
| `molecule_template_get_qr_capacity(...)` | 获取二维码容量 |

**模板数据结构**:

```python
{
    "label_size": {
        "width": 50.0,      # 宽度 (mm)
        "height": 30.0,     # 高度 (mm)
        "corner_radius": 2.0  # 圆角半径 (mm)
    },
    "dpi": 300,             # 分辨率
    "objects": [            # 对象列表
        {
            "id": "...",
            "type": "qr",   # 或 "text"
            "position": {"x": 0, "y": 0},
            "size": {"width": 10, "height": 10},
            "z_index": 0,
            # QR 特有属性:
            "qr_version": "21x21",
            "error_correction": "Q",
            "content": "",
            "batch": False,
            "csv_column": ""
            # Text 特有属性:
            "font": "Arial",
            "font_size": 3.0,
            "font_style": ["normal"],
            "color": "#000000",
            "text_align": "left",
            "vertical_align": "top"
        }
    ]
}
```

#### molecule_csv.py

**文件**: [molecule/molecule_csv.py](file:///e:/99_pri_sync/python项目/qr-label-creator/molecule/molecule_csv.py)

**职责**: CSV/Excel 数据管理

**核心类**: `CSVManager`

**成员变量**:

| 成员 | 类型 | 说明 |
|------|------|------|
| `data` | pd.DataFrame or None | CSV 数据 |
| `error_message` | str or None | 错误信息 |
| `file_path` | str or None | 文件路径 |

**核心方法**:

| 方法 | 说明 |
|------|------|
| `molecule_csv_import(file_path)` | 导入 CSV |
| `molecule_csv_import_excel(file_path)` | 导入 Excel |
| `molecule_csv_get_columns()` | 获取列名 |
| `molecule_csv_get_first_row_value(column)` | 获取第一行值 |
| `molecule_csv_get_row_count()` | 获取行数 |

#### molecule_image.py

**文件**: [molecule/molecule_image.py](file:///e:/99_pri_sync/python项目/qr-label-creator/molecule/molecule_image.py)

**职责**: 图像合成与导出

**核心类**: `ImageManager`

**核心方法**:

| 方法 | 说明 |
|------|------|
| `molecule_image_create_label(...)` | 创建标签图像 |
| `molecule_image_add_qr(...)` | 添加二维码到标签 |
| `molecule_image_add_text(...)` | 添加文本到标签 |
| `molecule_image_export_current(...)` | 导出当前标签 |
| `molecule_image_batch_export(...)` | 批量导出标签 |

**批量导出流程**:
1. 验证输入数据和模板
2. 遍历每一行 CSV 数据
3. 对每一行数据生成完整标签
4. 保存为 PNG 或合并为 PDF

#### molecule_history.py

**职责**: 历史记录管理（撤销/重做）

**核心功能**:
- 保存模板状态到历史栈
- 撤销操作（从历史栈恢复）
- 重做操作（从撤销栈恢复）

---

### L4 原子层 (Atom Layer)

#### atom_template.py

**文件**: [atom/atom_template.py](file:///e:/99_pri_sync/python项目/qr-label-creator/atom/atom_template.py)

**职责**: 提供模板相关的纯函数原子操作

**核心函数**:

| 函数 | 说明 |
|------|------|
| `atom_template_create_default(...)` | 创建默认模板 |
| `atom_template_generate_id()` | 生成唯一对象 ID |
| `atom_template_add_object(template, obj)` | 添加对象到模板 |
| `atom_template_remove_object(template, obj_id)` | 移除对象 |
| `atom_template_get_object(template, obj_id)` | 获取对象 |
| `atom_template_get_objects(template)` | 获取所有对象 |
| `atom_template_update_object(template, obj_id, **kwargs)` | 更新对象 |
| `atom_template_set_label_size(template, ...)` | 设置标签尺寸 |
| `atom_template_set_dpi(template, dpi)` | 设置 DPI |
| `atom_template_check_boundaries(template)` | 检查边界溢出 |

#### atom_qr.py

**文件**: [atom/atom_qr.py](file:///e:/99_pri_sync/python项目/qr-label-creator/atom/atom_qr.py)

**职责**: 提供二维码相关的纯函数原子操作

**核心函数**:

| 函数 | 说明 |
|------|------|
| `atom_qr_generate(content, ...)` | 生成二维码图像 |
| `atom_qr_get_capacity(version, error_level)` | 获取二维码容量 |
| `atom_qr_create(obj_id, ...)` | 创建二维码对象 |

**二维码版本容量表**:

| 版本 | L 纠错 | M 纠错 | Q 纠错 | H 纠错 |
|------|-------|-------|-------|-------|
| 21x21 | 41 | 34 | 27 | 17 |
| 25x25 | 47 | 37 | 29 | 22 |
| 29x29 | 77 | 61 | 47 | 35 |
| ... | ... | ... | ... | ... |

#### atom_image.py

**职责**: 提供图像处理的纯函数原子操作

**核心函数**:

| 函数 | 说明 |
|------|------|
| `atom_image_create_label(...)` | 创建标签画布 |
| `atom_image_add_qr(...)` | 合成二维码 |
| `atom_image_add_text(...)` | 合成文本 |
| `atom_image_save(img, file_path)` | 保存图像 |
| `atom_image_convert_rgb(img)` | 转换为 RGB 模式 |

#### atom_csv.py

**职责**: 提供 CSV/Excel 读取的纯函数原子操作

**核心函数**:

| 函数 | 说明 |
|------|------|
| `atom_csv_read(file_path)` | 读取 CSV 文件 |
| `atom_excel_read(file_path, sheet_name)` | 读取 Excel 文件 |
| `atom_csv_get_columns(data)` | 获取列名 |
| `atom_csv_get_row(data, index)` | 获取行数据 |

---

## 数据流与调用链

### 典型调用链示例

#### 1. 添加二维码对象

```
用户点击工具栏 QR 按钮
    ↓
main_window.on_qr_button_clicked()
    ↓
ui_entry.entry_add_qr_object(x, y)
    ↓
scheduler.schedule_add_qr_object(x, y, ...)
    ↓
template_manager.molecule_template_add_qr_object(...)
    ↓
atom_qr_create(...)  →  创建对象
atom_template_add_object(template, obj)  →  添加到模板
    ↓
返回 obj_id
    ↓
designer.update()  →  刷新画布显示
```

#### 2. 批量导出流程

```
用户点击批量导出
    ↓
main_window.open_batch_export_dialog()
    ↓
main_window.on_batch_export_start(dialog)
    ↓
ui_entry.entry_batch_export(output_dir, ...)
    ↓
scheduler.schedule_batch_export(...)
    ↓
image_manager.molecule_image_batch_export(...)
    ↓
遍历每一行 CSV:
    ↓
    atom_image_create_label(...)  →  创建画布
    遍历每个对象:
        ↓
        如果是 QR:
            atom_qr_generate(...)  →  生成 QR
            atom_image_add_qr(...)  →  合成 QR
        如果是 Text:
            atom_image_add_text(...)  →  合成文本
    ↓
    atom_image_save(...)  →  保存 PNG
    或
    _save_as_pdf(...)  →  保存 PDF
    ↓
返回结果
```

#### 3. 撤销操作流程

```
用户点击撤销
    ↓
main_window.undo()
    ↓
ui_entry.entry_history_undo()
    ↓
scheduler.schedule_history_undo()
    ↓
history_manager.molecule_history_undo()
    ↓
返回 (template, objects)
    ↓
scheduler.template_manager.molecule_template_set(template)
scheduler.template_manager.molecule_template_set_objects(objects)
    ↓
designer.update()  →  刷新画布
```

---

## 开发指南

### 添加新功能的标准流程

1. **确认架构**: 首先在项目规则中确认需要修改的层级
2. **实现原子层**: 如需新的原子操作，先在 `atom/` 中实现
3. **实现分子层**: 在 `molecule/` 中编排原子操作
4. **实现调度层**: 在 `schedule_core.py` 中添加调度方法
5. **实现入口层**: 在 `entry_ui.py` 中添加入口方法
6. **实现 UI**: 在 `main_window.py` 或相关 UI 组件中添加交互
7. **测试**: 完整流程测试

### 代码规范

#### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 文件 | 蛇形命名，前缀标识层级 | `molecule_template.py`, `atom_qr.py` |
| 函数 | 蛇形命名，前缀标识层级 | `molecule_template_add_qr_object()`, `atom_qr_create()` |
| 类 | 大驼峰命名 | `TemplateManager`, `CoreScheduler` |
| 常量 | 全大写，下划线分隔 | `DEFAULT_WIDTH`, `MAX_DPI` |

#### 文档字符串

每个函数必须包含 Google 风格的文档字符串：

```python
def atom_template_add_object(template: dict, obj: dict) -> str:
    """向模板添加对象

    Args:
        template: 模板对象
        obj: 要添加的对象

    Returns:
        添加的对象 ID
    """
    # 实现...
```

#### 类型注解

所有函数必须添加类型注解：

```python
from typing import Dict, Any, Optional

def example_function(param1: int, param2: str) -> Optional[Dict[str, Any]]:
    # 实现...
```

### 调试技巧

1. **日志查看**: 查看 `app.log` 获取程序运行日志
2. **断点调试**: 在各层入口处设置断点跟踪调用链
3. **状态检查**: 在调度层检查各分子管理器的状态
4. **UI 调试**: 检查属性面板更新和画布重绘

---

## 常见问题

### Q: 如何添加新的对象类型？

A: 按以下步骤：
1. 在 `atom/` 添加新对象的创建和操作函数
2. 在 `molecule_template.py` 添加添加/更新方法
3. 在 `molecule_image.py` 添加合成方法
4. 在 `molecule_draw.py` 添加绘制方法
5. 在 UI 层添加工具栏按钮和属性面板
6. 更新模板数据结构定义

### Q: 如何添加新的导出格式？

A: 在 `molecule_image.py` 的 `_batch_process()` 方法中添加新格式的处理逻辑，参考 PNG 和 PDF 的实现。

### Q: 如何修改 UI 主题或样式？

A: UI 样式主要在 `entry/ui_window/` 目录下的各组件中定义，使用 Qt Style Sheets (QSS) 修改样式。

### Q: 依赖安装失败怎么办？

A: 尝试以下步骤：
1. 使用国内 PyPI 镜像源
2. 单独安装失败的依赖
3. 检查 Python 版本是否 >= 3.8

---

## 更新日志

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0.0 | 2026-04-12 | 初始版本 |

---

## 许可证

GNU General Public License v3.0

---

## 联系方式

- 作者: kk120120
- 邮箱: hzwtox@hotmail.com
- GitHub: https://github.com/kk120120/qrcode-label-maker
