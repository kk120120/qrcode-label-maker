# QR Label Creator 详细设计文档

> **文档类型**：项目详细设计文档
> **适用范围**：QR标签生成器项目开发、架构说明、团队协作
> **版本**：v1.12.10
> **更新日期**：2026-05-15

---

## 1. 项目概述

### 1.1 项目信息
- **项目名称**：QR Label Creator（批量二维码标签生成器）
- **版本**：v1.12.4
- **发布日期**：2026-05-13
- **作者**：kk120120
- **邮箱**：hzwtox@hotmail.com
- **GitHub**：https://github.com/kk120120/qrcode-label-maker

### 1.2 主要功能
- 标签模板设计与编辑
- 二维码对象添加与配置
- 文本对象添加与配置
- CSV/Excel批量数据导入
- 批量标签导出（PNG/PDF）
- 模板保存与加载

### 1.3 技术栈
- Python 3.8+
- PyQt5 (GUI框架)
- qrcode (二维码生成)
- Pillow (图像处理)
- pandas (数据处理)

---

## 2. 架构设计

### 2.1 三层架构概述

项目采用严格的三层架构设计，确保代码的可维护性和可扩展性。

```
┌─────────────────────────────────────────────────────────┐
│                    L1 入口层 (entry)                     │
│        接收用户/外部事件，直接转发至L3分子层                │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    L3 分子层 (molecule)                  │
│           编排原子操作，实现完整业务动作                   │
│  保留文件：template, csv, config, image, history, draw   │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    L4 原子层 (atom)                      │
│              单一、无业务逻辑、无分支的最小单元             │
└─────────────────────────────────────────────────────────┘
```

### 2.2 依赖方向规则

```
L1 → L3 → L4
```

**强制规则**：
- ✓ 允许：L1调用L3
- ✓ 允许：L3调用L4
- ✗ 禁止：L1直接调用L4
- ✗ 禁止：分子调用分子
- ✗ 禁止：原子调用原子
- ✗ 禁止：循环依赖

**架构说明**：
- L2 调度层已合并到 L1 入口层，减少调用链层级
- entry_ui.py 直接管理分子层实例，承担原调度层职责

---

## 3. L1 入口层（entry）详解

### 3.1 职责
- 接收用户/外部事件
- 直接转发给L3分子层（合并原L2调度层职责）
- 管理分子层实例：template_manager, csv_manager, config_manager, image_manager, history_manager
- 不写任何业务逻辑
- 命名规范：`entry_界面_动作()`

### 3.2 分子管理器

入口层管理以下分子管理器实例：
- `template_manager`：模板和对象管理
- `csv_manager`：CSV/Excel数据管理
- `config_manager`：配置管理
- `image_manager`：图像导出
- `history_manager`：历史记录

### 3.3 菜单结构

L1入口层负责创建主窗口菜单系统，菜单结构如下：

```
文件
├─ 新建模板 (Ctrl+N)
├─ 打开模板 (Ctrl+O)
├─ 保存模板 (Ctrl+S)
└─ 退出

设置
└─ 基础设置

导入
├─ xlsx 导入（不易出错）(Ctrl+I)
└─ csv 导入（速度快）

导出
├─ 批量导出 (Ctrl+E)
└─ 单张导出PNG

历史
├─ 回退 (Ctrl+Z)
└─ 重做 (Ctrl+Y)

帮助
└─ 关于
```

### 3.4 对话框结构

软件包含以下对话框，用于用户交互和数据处理：

#### 3.3.1 基础设置对话框
**菜单位置**：设置 → 基础设置

```
基础设置
├── 标签尺寸 (mm)
│   ├── 宽度: [spinbox] (范围: 10-300)
│   ├── 高度: [spinbox] (范围: 10-300)
│   └── 圆角: [spinbox] (范围: 0-50)
├── DPI设置
│   └── DPI: [spinbox] (范围: 96-600)
├── 网格设置
│   ├── ☑ 显示网格   ← 复选框（勾选显示，取消勾选隐藏）
│   ├── 网格颜色: [选择颜色按钮]（默认: 绿色）
│   └── 网格线型: [下拉框]（实线/虚线/点线/点划线/双点划线，默认: 虚线）
└── [确定] [取消]
```

**默认值**：
- 显示网格: ☑ 是（默认勾选）
- 网格颜色: 绿色 (#00FF00)
- 网格线型: 虚线

#### 3.3.2 CSV预览对话框
**菜单位置**：导入 → xlsx 导入 / csv 导入

```
CSV预览
├── 控制区
│   ├── 开始行: [spinbox]
│   └── [预览按钮]
├── 表格区
│   └── [数据预览表格，只读]
└── [确认] [取消]
```

#### 3.3.3 批量导出对话框
**菜单位置**：导出 → 批量导出

```
批量导出
├── 导出格式
│   ├── ○ PNG - 每张标签单独导出为PNG文件（默认选中）
│   └── ○ PDF - 将所有标签合并到一个PDF文件
├── 目标文件夹
│   ├── [文本输入框]
│   └── [浏览按钮]
├── 导出进度（点击开始后显示）
│   ├── 状态标签: "正在导出... X/Y"
│   └── 进度条
└── [开始] [确认] [取消]
```

### 3.5 主窗口布局

主窗口采用以下布局结构：

```
┌─────────────────────────────────────────────────────────┐
│ 菜单栏                                                 │
├─────────────────────────────────────────────────────────┤
│ 工具栏 (固定高度 60px)                                  │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐                   │
│ │矩形QR对象│ │多行文本  │ │  预览    │                   │
│ └──────────┘ └──────────┘ └──────────┘                   │
├─────────────────────────────────────────────────────────┤
│ 设计器区域 (中间工作区，可扩展) │ 属性面板 (最小宽度 280px) │
│                                 │ ┌────────────────────┐ │
│                                 │ │ 已选择/未选择对象  │ │
│                                 │ ├────────────────────┤ │
│                                 │ │ 位置               │ │
│                                 │ │ x: [spinbox]       │ │
│                                 │ │ y: [spinbox]       │ │
│                                 │ ├────────────────────┤ │
│                                 │ │ 大小               │ │
│                                 │ │ w: [spinbox]       │ │
│                                 │ │ h: [spinbox]       │ │
│                                 │ ├────────────────────┤ │
│                                 │ │ 二维码属性/文本属性 │ │
│                                 │ │ (根据对象类型显示)  │ │
│                                 │ ├────────────────────┤ │
│                                 │ │ [保存按钮]          │ │
│                                 │ └────────────────────┘ │
└─────────────────────────────────────────────────────────┘
│ 状态栏                                                 │
└─────────────────────────────────────────────────────────┘
```

### 3.5 入口清单

L1入口层对应文件：`entry/entry_ui.py`，类：`UIEntry`

入口函数按用户交互流程分为11个分组，共43个函数。

#### 分组1：初始化阶段 (4个)

| 入口函数 | 功能说明 | 调用调度 |
|---------|---------|---------|
| `entry_init_template()` | 初始化模板 | `schedule_init_template()` |
| `entry_init_designer()` | 初始化设计器 | `schedule_init_designer()` |
| `entry_init_property_panel()` | 初始化属性面板 | `schedule_init_property_panel()` |
#### 分组2：模板管理 (10个)

| 入口函数 | 功能说明 | 调用调度 |
|---------|---------|---------|
| `entry_new_template()` | 新建模板 | `schedule_new_template()` |
| `entry_get_default_qr_position()` | 获取QR对象默认位置 | `schedule_get_default_qr_position()` |
| `entry_get_default_text_position()` | 获取文本对象默认位置 | `schedule_get_default_text_position()` |
| `entry_open_template(file_path)` | 打开模板 | `schedule_open_template()` |
| `entry_save_template(file_path)` | 保存模板 | `schedule_save_template()` |
| `entry_get_last_open_dir()` | 获取上次打开目录 | `schedule_get_last_open_dir()` |
| `entry_set_last_open_dir(dir_path)` | 设置上次打开目录 | `schedule_set_last_open_dir()` |
| `entry_get_last_import_dir()` | 获取上次导入目录 | `schedule_get_last_import_dir()` |
| `entry_set_last_import_dir(dir_path)` | 设置上次导入目录 | `schedule_set_last_import_dir()` |
| `entry_get_last_export_dir()` | 获取上次导出目录 | `schedule_get_last_export_dir()` |
| `entry_set_last_export_dir(dir_path)` | 设置上次导出目录 | `schedule_set_last_export_dir()` |

#### 分组3：标签属性设置 (2个)

| 入口函数 | 功能说明 | 调用调度 |
|---------|---------|---------|
| `entry_set_label_size(w,h,r)` | 设置标签尺寸 | `schedule_set_label_size()` |
| `entry_set_dpi(dpi)` | 设置DPI | `schedule_set_dpi()` |

#### 分组4：二维码管理 (3个)

| 入口函数 | 功能说明 | 调用调度 |
|---------|---------|---------|
| `entry_get_qr_sizes()` | 获取二维码尺寸列表 | `schedule_get_qr_sizes()` |
| `entry_update_qr_sizes()` | 更新二维码尺寸列表 | `schedule_update_qr_sizes()` |
| `entry_get_qr_capacity(v,e)` | 获取二维码容量 | `schedule_get_qr_capacity()` |

#### 分组5：对象添加 (2个)

| 入口函数 | 功能说明 | 调用调度 |
|---------|---------|---------|
| `entry_add_qr_object(x,y,...)` | 添加二维码对象 | `schedule_add_qr_object()` |
| `entry_add_text_object(x,y,...)` | 添加文本对象 | `schedule_add_text_object()` |

#### 分组6：对象编辑 (4个)

| 入口函数 | 功能说明 | 调用调度 |
|---------|---------|---------|
| `entry_update_object(obj_id,**kwargs)` | 更新对象 | `schedule_update_object()` |
| `entry_update_object_properties(obj_id,**kwargs)` | 更新对象属性 | `schedule_update_object_properties()` |
| `entry_remove_object(obj_id)` | 删除对象 | `schedule_remove_object()` |
| `entry_get_object_index(objects,obj_id)` | 获取对象索引 | `schedule_get_object_index()` |

#### 分组7：数据导入 (6个)

| 入口函数 | 功能说明 | 调用调度 |
|---------|---------|---------|
| `entry_import_csv(file_path)` | 导入CSV文件 | `schedule_import_csv()` |
| `entry_import_excel(file_path)` | 导入Excel文件 | `schedule_import_excel()` |
| `entry_get_csv_columns()` | 获取CSV列名 | `schedule_get_csv_columns()` |
| `entry_get_csv_data()` | 获取CSV数据 | `schedule_get_csv_data()` |
| `entry_check_csv_columns()` | 检查CSV列 | `schedule_check_csv_columns()` |
| `entry_get_first_row_value(column)` | 获取第一行指定列值 | `schedule_get_first_row_value()` |

#### 分组8：标签导出 (2个)

| 入口函数 | 功能说明 | 调用调度 |
|---------|---------|---------|
| `entry_export_current(file_path)` | 导出当前标签 | `schedule_export_current()` |
| `entry_batch_export(dir,fmt)` | 批量导出标签 | `schedule_batch_export()` |

#### 分组9：数据查询 (4个)

| 入口函数 | 功能说明 | 调用调度 |
|---------|---------|---------|
| `entry_get_template()` | 获取模板数据 | `schedule_get_template()` |
| `entry_get_object(obj_id)` | 获取单个对象 | `schedule_get_object()` |
| `entry_get_objects()` | 获取所有对象 | `schedule_get_objects()` |
| `entry_check_boundaries()` | 检查边界溢出 | `schedule_check_boundaries()` |

#### 分组10：UI更新 (3个)

| 入口函数 | 功能说明 | 调用调度 |
|---------|---------|---------|
| `entry_update_property_panel(obj_id)` | 更新属性面板 | `schedule_update_property_panel()` |
| `entry_draw_all(...)` | 绘制所有内容 | `schedule_draw_all()` |
| `entry_draw_all_with_callback(...)` | 带回调的绘制（含预览） | `schedule_draw_all()` |

**入口函数总数：43个**

### 3.3 入口清单流程图

```
用户操作
    │
    ▼
┌─────────────────────┐
│   UI界面事件触发      │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  entry_xxx() 入口函数 │ ── 验证参数 ──► 转发至L2调度
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ schedule_xxx() 调度  │
└─────────────────────┘
```

### 3.4 用户交互流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                     1. 初始化阶段                                 │
│  entry_init_template → entry_init_designer → entry_init_property_panel │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     2. 模板管理                                   │
│  entry_new_template / entry_open_template / entry_save_template    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     3. 标签属性设置                               │
│  entry_set_label_size / entry_set_dpi                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     4. 二维码管理                                 │
│  entry_get_qr_sizes / entry_update_qr_sizes / entry_get_qr_capacity │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     5. 对象添加                                   │
│  entry_add_qr_object / entry_add_text_object                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     6. 对象编辑                                   │
│  entry_update_object / entry_remove_object / entry_get_object_index │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     7. 数据导入                                   │
│  entry_import_csv / entry_import_excel / entry_check_csv_columns │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     8. 标签导出                                   │
│  entry_export_current / entry_batch_export                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     9. 数据查询                                  │
│  entry_get_template / entry_get_object / entry_get_objects      │
│  entry_check_boundaries                                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     10. UI更新                                   │
│  entry_update_property_panel / entry_draw_all                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. L1+L2 架构说明（原L2调度层已合并）

> **重要变更**：L2调度层已合并到L1入口层，减少调用链层级。

### 4.1 合并原因
- 原 L2 调度层（schedule_core.py）只是1:1转发，无实际业务逻辑
- 多个 molecule 文件（file, init, qr, property）是空壳，只是简单调用 atom
- 合并后减少一层调用，提高性能

### 4.2 新的架构

**简化前**（4层调用）：
```
L1 entry_ui.py → L2 schedule_core.py (10个manager) → L3 molecule_*.py (10个文件) → L4 atom_*.py
```

**简化后**（3层调用）：
```
L1 entry_ui.py → L3 molecule_*.py (6个有实际逻辑的文件) → L4 atom_*.py
```

### 4.3 入口层管理的分子管理器

L1入口层现在直接管理以下分子管理器：
- `template_manager` - 模板和对象管理（核心）
- `csv_manager` - CSV/Excel数据管理
- `config_manager` - 配置管理
- `image_manager` - 图像导出
- `history_manager` - 历史记录

绘制管理（DrawManager）按需创建，不长期持有实例。

### 4.4 调用示例

```python
# 旧架构（通过L2调度）
self.scheduler.schedule_add_qr_object(x, y)

# 新架构（直接调用L3）
self.template_manager.molecule_template_add_qr_object(x, y)
```

---

## 5. L3 分子层（molecule）详解

### 5.1 职责
- 编排原子操作
- 实现完整业务动作
- 分子内部允许：if/else、for/while、异常处理
- 分子内部禁止：调用其他分子、调用调度层、跨模块决策
- 命名规范：`molecule_业务_动作()`

### 5.2 分子模块清单

L3分子层共9个模块文件，总计48个公共方法。

| 模块名 | 分子类 | 文件 | 方法数 | 业务职责 |
|-------|--------|------|-------|---------|
| 模板管理 | `TemplateManager` | `molecule_template.py` | 13 | 模板的创建、修改、保存、加载 |
| CSV处理 | `CSVManager` | `molecule_csv.py` | 6 | CSV/Excel数据导入和解析 |
| 配置管理 | `ConfigManager` | `molecule_config.py` | 8 | 配置文件读写和应用设置 |
| 二维码管理 | `QRManager` | `molecule_qr.py` | 2 | 二维码生成和容量查询 |
| 图像管理 | `ImageManager` | `molecule_image.py` | 7 | 标签图像创建、导出、批量处理 |
| 绘制管理 | `DrawManager` | `molecule_draw.py` | 4 | 标签和对象的绘制 |
| 文件管理 | `FileManager` | `molecule_file.py` | 5 | 文件系统基本操作 |
| 属性管理 | `PropertyManager` | `molecule_property.py` | 2 | 对象属性更新 |
| 初始化管理 | `InitManager` | `molecule_init.py` | 4 | 初始化状态数据 |

### 5.3 分子方法清单

#### TemplateManager (molecule_template.py) - 13个方法

| 方法 | 功能说明 | 返回值 |
|-----|---------|-------|
| `molecule_template_create()` | 创建新模板 | `None` |
| `molecule_template_set_size(w,h,r)` | 设置标签尺寸 | `None` |
| `molecule_template_set_dpi(dpi)` | 设置DPI | `None` |
| `molecule_template_add_qr_object(...)` | 添加二维码对象 | `str` 对象ID |
| `molecule_template_add_text_object(...)` | 添加文本对象 | `str` 对象ID |
| `molecule_template_update_object(id,**k)` | 更新对象属性 | `bool` |
| `molecule_template_remove_object(id)` | 删除对象 | `None` |
| `molecule_template_get_object(id)` | 获取对象 | `Dict/None` |
| `molecule_template_get_objects()` | 获取所有对象 | `List[Dict]` |
| `molecule_template_save(path)` | 保存模板 | `bool` |
| `molecule_template_load(path)` | 加载模板 | `bool` |
| `molecule_template_check_boundaries()` | 检查边界 | `List[str]` |
| `molecule_template_get_template()` | 获取模板数据 | `Dict` |

#### CSVManager (molecule_csv.py) - 6个方法

| 方法 | 功能说明 | 返回值 |
|-----|---------|-------|
| `molecule_csv_import(path)` | 导入CSV文件 | `tuple` |
| `molecule_csv_import_excel(path)` | 导入Excel文件 | `tuple` |
| `molecule_csv_get_data()` | 获取数据 | `DataFrame/None` |
| `molecule_csv_get_columns()` | 获取列名 | `List[str]` |
| `molecule_csv_get_row(idx)` | 获取指定行 | `Series/None` |
| `molecule_csv_get_first_row_value(col)` | 获取第一行指定列值 | `str/None` |

#### ConfigManager (molecule_config.py) - 8个方法

| 方法 | 功能说明 | 返回值 |
|-----|---------|-------|
| `molecule_config_get_qr_sizes()` | 获取二维码尺寸列表 | `List[str]` |
| `molecule_config_get_capacity(v,e)` | 获取二维码容量 | `Tuple/None` |
| `molecule_config_get_last_open_dir()` | 获取上次打开目录 | `str/None` |
| `molecule_config_set_last_open_dir(d)` | 设置上次打开目录 | `None` |
| `molecule_config_get_last_import_dir()` | 获取上次导入目录 | `str/None` |
| `molecule_config_set_last_import_dir(d)` | 设置上次导入目录 | `None` |
| `molecule_config_get_last_export_dir()` | 获取上次导出目录 | `str/None` |
| `molecule_config_set_last_export_dir(d)` | 设置上次导出目录 | `None` |

#### QRManager (molecule_qr.py) - 2个方法

| 方法 | 功能说明 | 返回值 |
|-----|---------|-------|
| `molecule_qr_generate(c,ec)` | 生成二维码 | `Image/None` |
| `molecule_qr_get_capacity(v,e)` | 获取二维码容量 | `Tuple` |

#### ImageManager (molecule_image.py) - 7个公共方法

| 方法 | 功能说明 | 返回值 |
|-----|---------|-------|
| `molecule_image_create_label(w,h,r,dpi)` | 创建标签图像 | `Image` |
| `molecule_image_add_qr(...)` | 添加二维码到标签 | `Image` |
| `molecule_image_add_text(...)` | 添加文本到标签 | `Image` |
| `molecule_image_save(img,path)` | 保存标签图像 | `str` |
| `molecule_image_qr_generate(c,ec)` | 生成二维码图像 | `Image/None` |
| `molecule_image_export_single(path)` | 导出单个标签 | `bool` |
| `molecule_image_batch_export(dir,fmt)` | 批量导出 | `bool` |

> 注：还有3个内部方法 `_batch_process()`, `_process_single_object()`, `_save_as_pdf()` 不对外暴露

#### DrawManager (molecule_draw.py) - 4个方法

| 方法 | 功能说明 | 返回值 |
|-----|---------|-------|
| `molecule_draw_label(...)` | 绘制标签 | `None` |
| `molecule_draw_objects(...)` | 绘制所有对象（含文本对齐） | `None` |
| `molecule_draw_grid(...)` | 绘制网格 | `None` |
| `molecule_draw_all(...)` | 绘制所有内容 | `None` |

#### FileManager (molecule_file.py) - 5个方法

| 方法 | 功能说明 | 返回值 |
|-----|---------|-------|
| `molecule_file_exists(path)` | 检查文件是否存在 | `bool` |
| `molecule_file_get_directory(path)` | 获取文件目录 | `str` |
| `molecule_file_join_path(*parts)` | 拼接路径 | `str` |
| `molecule_file_get_basename(path)` | 获取文件名 | `str` |
| `molecule_file_make_directory(dir)` | 创建目录 | `bool` |

#### PropertyManager (molecule_property.py) - 2个方法

| 方法 | 功能说明 | 返回值 |
|-----|---------|-------|
| `molecule_property_get_object_index(objs,id)` | 获取对象索引 | `int` |
| `molecule_property_update_object(...)` | 更新对象属性 | `Dict` |

#### InitManager (molecule_init.py) - 4个方法

| 方法 | 功能说明 | 返回值 |
|-----|---------|-------|
| `molecule_init_template()` | 初始化模板 | `Dict` |
| `molecule_init_designer()` | 初始化设计器 | `Dict` |
| `molecule_init_property_panel()` | 初始化属性面板 | `Dict` |
| `molecule_init_designer_area(...)` | 初始化设计器区域 | `None` |

### 5.4 分子操作流程图

#### 5.3.1 图像导出流程

```
molecule_image_export_single(file_path)
    │
    ▼
┌────────────────────────────────────────┐
│  template_mgr.molecule_template_get_template()  │
└────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────┐
│  template_mgr.molecule_template_get_objects()   │
└────────────────────────────────────────┘
    │
    ├─► 遍历每个对象
    │        │
    │        ├─► [QR对象]
    │        │      │
    │        │      ▼
    │        │  ┌────────────────────────────────┐
    │        │  │ qr_mgr.molecule_qr_generate()   │
    │        │  └────────────────────────────────┘
    │        │      │
    │        │      ▼
    │        │  ┌────────────────────────────────┐
    │        │  │ self.molecule_image_add_qr()  │
    │        │  └────────────────────────────────┘
    │        │
    │        └─► [Text对象]
    │               │
    │               ▼
    │          ┌────────────────────────────────┐
    │          │ self.molecule_image_add_text() │
    │          └────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────┐
│  self.molecule_image_save(img, path)   │
└────────────────────────────────────────┘
```

#### 5.3.2 批量导出流程

```
molecule_image_batch_export(output_dir, export_format)
    │
    ▼
┌────────────────────────────────────────┐
│  获取模板数据 + CSV数据                  │
└────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────┐
│  _batch_process(template, csv_data,    │
│                  output_dir, format)    │
└────────────────────────────────────────┘
    │
    ├─► 遍历CSV每一行
    │        │
    │        ▼
    │    ┌────────────────────────────────┐
    │    │ 创建空白标签图像                │
    │    └────────────────────────────────┘
    │        │
    │        ▼
    │    ┌────────────────────────────────┐
    │    │ _process_single_object()      │
    │    │ (处理每个模板对象)              │
    │    └────────────────────────────────┘
    │        │
    │        ├─► [PNG格式] 保存单个文件
    │        └─► [PDF格式] 收集到图像列表
    │
    ▼
┌────────────────────────────────────────┐
│  [PDF格式] 调用_save_as_pdf()          │
└────────────────────────────────────────┘
```

#### 5.3.3 属性更新流程

```
molecule_property_update_object(obj, x, y, w, h, props)
    │
    ├─► atom_property_update_position(obj, x, y)
    │        │
    │        ▼
    │    更新obj['position']
    │
    ├─► atom_property_update_size(obj, w, h)
    │        │
    │        ▼
    │    更新obj['size']
    │
    └─► [QR对象] atom_property_update_qr_properties()
         或
         [Text对象] atom_property_update_text_properties()
              │
              ▼
         更新obj['properties']
```

---

## 6. L4 原子层（atom）详解

### 6.1 职责
- 单一动作，无业务逻辑
- 无 if/else、无循环、无分支
- 禁止调用其他原子/分子/调度
- 命名规范：`atom_模块_动作()`
- 纯函数、无副作用

### 6.2 原子模块清单

L4原子层共10个模块文件，总计48个原子函数。

| 模块名 | 文件 | 函数数 | 功能说明 |
|-------|------|-------|---------|
| 模板原子 | `atom_template.py` | 12 | 模板数据操作 |
| CSV原子 | `atom_csv.py` | 4 | CSV/Excel文件读取 |
| 配置原子 | `atom_config.py` | 3 | 配置文件读取 |
| 二维码原子 | `atom_qr.py` | 2 | 二维码生成 |
| 图像原子 | `atom_image.py` | 7 | 图像处理操作 |
| 文本原子 | `atom_text.py` | 4 | 文本对象操作 |
| 文件原子 | `atom_file.py` | 5 | 文件系统操作 |
| 属性原子 | `atom_property.py` | 5 | 对象属性更新 |
| 初始化原子 | `atom_init.py` | 3 | 初始化数据 |
| 绘制原子 | `atom_draw.py` | 3 | 绘制操作 |

### 6.3 原子函数清单

#### 6.3.1 模板原子（atom_template.py） - 12个

| 原子函数 | 功能说明 | 返回值 |
|---------|---------|-------|
| `atom_template_create()` | 创建新模板 | `Dict` |
| `atom_template_set_size(t,w,h,r)` | 设置标签尺寸 | `Dict` |
| `atom_template_set_dpi(t,d)` | 设置DPI | `Dict` |
| `atom_template_add_qr_object(...)` | 添加二维码对象 | `str` |
| `atom_template_add_text_object(...)` | 添加文本对象 | `str` |
| `atom_template_update_object(t,id,**k)` | 更新对象属性 | `bool` |
| `atom_template_remove_object(t,id)` | 删除对象 | `None` |
| `atom_template_get_object(t,id)` | 获取对象 | `Dict/None` |
| `atom_template_get_objects(t)` | 获取所有对象 | `List` |
| `atom_template_save(t,path)` | 保存模板到文件 | `bool` |
| `atom_template_load(path)` | 从文件加载模板 | `Dict/None` |
| `atom_template_check_boundaries(t)` | 检查边界 | `List[str]` |

#### 6.3.2 二维码原子（atom_qr.py） - 2个

| 原子函数 | 功能说明 | 返回值 |
|---------|---------|-------|
| `atom_qr_generate(c,ec,qv)` | 生成二维码 | `Image/None` |
| `atom_qr_get_capacity(v,e)` | 获取二维码容量 | `Tuple[int,3]` |

#### 6.3.3 图像原子（atom_image.py） - 7个

| 原子函数 | 功能说明 | 返回值 |
|---------|---------|-------|
| `atom_image_create_label(w,h,r,dpi)` | 创建标签图像 | `Image` |
| `atom_image_add_qr(...)` | 添加二维码到标签 | `Image` |
| `atom_image_add_text(...)` | 添加文本到标签 | `Image` |
| `atom_image_save(img,f)` | 保存标签图像 | `str` |
| `atom_image_resize(img,w,h)` | 调整图像大小 | `Image` |
| `atom_image_paste(bg,fg,x,y)` | 粘贴图像 | `Image` |
| `atom_image_convert_rgb(img)` | 转换RGB模式 | `Image` |

#### 6.3.4 文本原子（atom_text.py） - 4个

| 原子函数 | 功能说明 | 返回值 |
|---------|---------|-------|
| `atom_text_create(...)` | 创建文本对象 | `Dict` |
| `atom_text_update(obj,**k)` | 更新文本对象 | `bool` |
| `atom_text_get_property(obj,p)` | 获取文本属性 | `Any` |
| `atom_text_set_property(obj,p,v)` | 设置文本属性 | `bool` |

#### 6.3.5 配置原子（atom_config.py） - 3个

| 原子函数 | 功能说明 | 返回值 |
|---------|---------|-------|
| `atom_config_read(ini_path)` | 读取配置文件 | `ConfigParser/None` |
| `atom_config_get_qr_sizes(c)` | 获取二维码尺寸列表 | `List[str]` |
| `atom_config_get_capacity(c,v,e)` | 获取二维码容量 | `Tuple/None` |

#### 6.3.6 文件原子（atom_file.py） - 5个

| 原子函数 | 功能说明 | 返回值 |
|---------|---------|-------|
| `atom_file_exists(path)` | 检查文件是否存在 | `bool` |
| `atom_file_get_directory(path)` | 获取文件目录 | `str` |
| `atom_file_join_path(*parts)` | 拼接路径 | `str` |
| `atom_file_get_basename(path)` | 获取文件名 | `str` |
| `atom_file_make_directory(dir)` | 创建目录 | `bool` |

#### 6.3.7 CSV原子（atom_csv.py） - 4个

| 原子函数 | 功能说明 | 返回值 |
|---------|---------|-------|
| `atom_csv_read(path)` | 读取CSV文件 | `Tuple[data,error]` |
| `atom_excel_read(path,sheet)` | 读取Excel文件 | `Tuple[data,error]` |
| `atom_csv_get_columns(data)` | 获取列名 | `List[str]` |
| `atom_csv_get_row(data,idx)` | 获取指定行 | `Series/None` |

#### 6.3.8 绘制原子（atom_draw.py） - 3个

| 原子函数 | 功能说明 | 返回值 |
|---------|---------|-------|
| `atom_draw_label(p,t,s,xo,yo)` | 绘制标签边框 | `None` |
| `atom_draw_objects(...)` | 绘制所有对象（含ID显示） | `None` |
| `atom_draw_grid(...)` | 绘制网格 | `None` |

#### 6.3.9 属性原子（atom_property.py） - 5个

| 原子函数 | 功能说明 | 返回值 |
|---------|---------|-------|
| `atom_property_update_position(obj,x,y)` | 更新位置 | `Dict` |
| `atom_property_update_size(obj,w,h)` | 更新大小 | `Dict` |
| `atom_property_update_qr_properties(...)` | 更新QR属性 | `Dict` |
| `atom_property_update_text_properties(...)` | 更新Text属性 | `Dict` |
| `atom_property_get_object_index(objs,id)` | 获取对象索引 | `int` |

#### 6.3.10 初始化原子（atom_init.py） - 3个

| 原子函数 | 功能说明 | 返回值 |
|---------|---------|-------|
| `atom_init_template()` | 初始化模板数据 | `Dict` |
| `atom_init_designer_state()` | 初始化设计器状态 | `Dict` |
| `atom_init_property_panel()` | 初始化属性面板状态 | `Dict` |

---

## 7. 目录结构

### 7.1 完整目录结构

```
qr-label-creator/                          # 项目根目录
├── main.py                                 # 总入口（仅启动程序）
├── entry/                                 # L1 入口层
│   ├── entry_main.py                      # 主窗口入口（EntryMain类）
│   ├── entry_ui.py                        # UI事件转发入口（UIEntry类）
│   └── ui_window/                         # UI窗口子层
│       ├── __init__.py                    # 子包初始化
│       ├── main_window.py                 # 主窗口（MainWindow类）
│       └── designer_canvas.py             # 设计器画布（LabelDesigner类）
├── schedule/                              # L2 调度层
│   └── schedule_core.py                   # 核心调度器（CoreScheduler类）
├── molecule/                              # L3 分子层
│   ├── molecule_template.py               # 模板管理（TemplateManager类）
│   ├── molecule_qr.py                     # 二维码管理（QRManager类）
│   ├── molecule_file.py                   # 文件管理（FileManager类）
│   ├── molecule_config.py                 # 配置管理（ConfigManager类）
│   ├── molecule_csv.py                   # CSV处理（CSVManager类）
│   ├── molecule_draw.py                   # 绘制管理（DrawManager类）
│   ├── molecule_image.py                  # 图像管理（ImageManager类）
│   ├── molecule_property.py               # 属性管理（PropertyManager类）
│   ├── molecule_history.py                # 历史记录管理（HistoryManager类）
│   └── molecule_init.py                   # 初始化管理（InitManager类）
├── atom/                                  # L4 原子层
│   ├── atom_template.py                   # 模板原子（12个函数）
│   ├── atom_qr.py                         # 二维码原子（2个函数）
│   ├── atom_image.py                      # 图像原子（7个函数）
│   ├── atom_text.py                       # 文本原子（4个函数）
│   ├── atom_config.py                     # 配置原子（3个函数）
│   ├── atom_file.py                       # 文件原子（5个函数）
│   ├── atom_csv.py                        # CSV原子（4个函数）
│   ├── atom_draw.py                       # 绘制原子（3个函数）
│   ├── atom_property.py                   # 属性原子（5个函数）
│   └── atom_init.py                       # 初始化原子（3个函数）
├── ui_components.py                       # UI可复用组件（对话框等）
├── icon_path/                              # 图标资源
├── mypolicy/                              # 策略目录
│   ├── personal_rules.md                  # 个人规则
│   ├── project_rules.md                   # 项目规则
│   └── agent_skills.md                   # Agent技能
├── mywork/                               # 工作目录
├── config.json                            # 配置文件
├── qrconfig.ini                          # QR配置
├── requirements.txt                       # 依赖项
└── new_design.md                          # 本设计文档
```

### 7.2 模块依赖关系图

#### 层级依赖关系

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              main.py                                         │
│                          (总入口，仅启动)                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          L1 入口层 (entry/)                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │
│  │  EntryMain      │  │  UIEntry        │  │  MainWindow     │            │
│  │ (创建窗口)        │  │ (事件转发)       │  │ (组装UI组件)     │            │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘            │
│           │                    │                    │                      │
│           └────────────────────┼────────────────────┘                      │
│                                │                                              │
│                                ▼                                              │
│                    ┌───────────────────────┐                                 │
│                    │    ui_window/         │                                 │
│                    │  LabelDesigner        │                                 │
│                    │  (设计器画布)          │                                 │
│                    └───────────────────────┘                                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          L2 调度层 (schedule/)                               │
│  ┌─────────────────────────────────────────────────────────────────┐        │
│  │                     CoreScheduler                                 │        │
│  │  (协调9个分子管理器，按正确顺序调度分子)                             │        │
│  └─────────────────────────────────────────────────────────────────┘        │
│           │        │        │        │        │        │        │         │
│           ▼        ▼        ▼        ▼        ▼        ▼        ▼         │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐  │
│  │Template│ │ QR  │ │File │ │Config│ │ CSV │ │Draw │ │Image│ │Prop │ │Init │  │
│  │Manager │ │Manager│ │Manager│ │Manager│ │Manager│ │Manager│ │Manager│ │erty│ │Manager│  │
│  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          L3 分子层 (molecule/)                              │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  分子管理器（每个管理一个业务领域的状态和行为）                          │    │
│  │  TemplateManager ──── QRManager ──── FileManager ──── ConfigManager│    │
│  │  CSVManager ──── DrawManager ──── ImageManager ──── PropertyManager│    │
│  │  HistoryManager ──── InitManager                                     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                        │
│                                    ▼                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          L4 原子层 (atom/)                                  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  原子函数（纯函数，无状态，无副作用）                                   │    │
│  │  atom_template │ atom_qr │ atom_image │ atom_text │ atom_config    │    │
│  │  atom_file │ atom_csv │ atom_draw │ atom_property │ atom_init      │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 调用关系详细图

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         L1 → L2 调用链                                        │
│                                                                              │
│   UIEntry.entry_xxx()  ──────────────────────────────────►  CoreScheduler.schedule_xxx()  │
│          │                                                              │      │
│          │  (只转发，不含业务逻辑)                                          │      │
│          │                                                              │      │
│          ▼                                                              ▼      │
│   ┌─────────────┐                                              ┌─────────────┐  │
│   │ entry_ui.py │                                              │schedule_    │  │
│   │  (33个方法)  │                                              │core.py      │  │
│   └─────────────┘                                              │ (33个方法)   │  │
│                                                                   └─────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│                         L2 → L3 调用链                                        │
│                                                                              │
│   CoreScheduler.schedule_xxx()  ──────────────────────────────────►  MoleculeManager.molecule_xxx()  │
│              │                                                                │              │
│              │  (只调度分子，不直接调用原子)                                    │              │
│              │                                                                │              │
│              ▼                                                                ▼              │
│   ┌─────────────────────┐                                        ┌─────────────────────┐  │
│   │ schedule_core.py     │                                        │ molecule_xxx.py      │  │
│   │ 组合9个分子管理器     │                                        │  (编排原子调用)       │  │
│   │ • template_manager   │                                        └─────────────────────┘  │
│   │ • qr_manager         │                                                    │         │
│   │ • file_manager       │                                                    │         │
│   │ • config_manager     │                                                    ▼         │
│   │ • csv_manager        │                                        ┌─────────────────────┐  │
│   │ • draw_manager       │                                        │ 调用 atom_xxx()     │  │
│   │ • image_manager      │                                        └─────────────────────┘  │
│   │ • property_manager   │                                                    │         │
│   │ • init_manager       │                                                    ▼         │
│   └─────────────────────┘                                        ┌─────────────────────┐  │
│                                                                    │ atom_xxx()          │  │
│                                                                    │ (纯函数，无状态)      │  │
│                                                                    └─────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│                         L3 → L4 调用链                                        │
│                                                                              │
│   MoleculeManager.molecule_xxx()  ──────────────────────────────────►  atom_xxx()  │
│              │                                                               │      │
│              │  (编排原子调用，不直接实现逻辑)                                  │      │
│              │                                                               │      │
│              ▼                                                               ▼      │
│   ┌─────────────────────┐                                         ┌─────────────────┐  │
│   │ molecule_xxx.py    │                                         │ atom_xxx.py     │  │
│   │ 组合多个原子函数     │                                         │ 纯函数           │  │
│   │ 实现业务动作         │                                         │ 无副作用          │  │
│   └─────────────────────┘                                         └─────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 7.3 文件与层级对应表

| 文件路径 | 所属层级 | 类/模块名 | 职责 |
|---------|---------|----------|------|
| `main.py` | 总入口 | - | 程序启动、依赖检查 |
| `entry/entry_main.py` | L1 | `EntryMain` | 创建主窗口 |
| `entry/entry_ui.py` | L1 | `UIEntry` | UI事件转发入口 |
| `entry/ui_window/main_window.py` | L1 | `MainWindow` | 组装UI组件 |
| `entry/ui_window/designer_canvas.py` | L1 | `LabelDesigner` | 设计器画布交互 |
| `schedule/schedule_core.py` | L2 | `CoreScheduler` | 协调分子执行顺序 |
| `molecule/molecule_template.py` | L3 | `TemplateManager` | 模板业务逻辑 |
| `molecule/molecule_qr.py` | L3 | `QRManager` | 二维码业务逻辑 |
| `molecule/molecule_image.py` | L3 | `ImageManager` | 图像业务逻辑 |
| `atom/atom_template.py` | L4 | 函数模块 | 模板数据操作 |
| `atom/atom_qr.py` | L4 | 函数模块 | 二维码生成 |
| `atom/atom_image.py` | L4 | 函数模块 | 图像处理 |

### 7.4 目录结构现状对比

| 目录/文件 | 规则要求位置 | 实际位置 | 状态 |
|----------|-------------|---------|------|
| UIEntry | `entry/entry_ui.py` | `entry/entry_ui.py` | ✅ 正确 |
| MainWindow | `entry/ui_window/main_window.py` | `entry/ui_window/main_window.py` | ✅ 正确 |
| LabelDesigner | `entry/ui_window/designer_canvas.py` | `entry/ui_window/designer_canvas.py` | ✅ 正确 |
| CoreScheduler | `schedule/schedule_core.py` | `schedule/schedule_core.py` | ✅ 正确 |
| UI组件 | `entry/ui_components/ui_components.py` | `ui_components.py`（根目录） | ❌ 需移动 |

### 7.5 待修复问题

**问题**：`ui_components.py` 位置错误

**当前**：`ui_components.py` 在项目根目录

**应改为**：`entry/ui_components/ui_components.py`

**影响**：`entry/ui_window/main_window.py` 第16行直接从根目录导入

**修复步骤**：
1. 创建 `entry/ui_components/` 目录
2. 移动 `ui_components.py` 到 `entry/ui_components/`
3. 更新 `entry/ui_window/main_window.py` 的导入语句为 `from entry.ui_components.ui_components import ...`

---

## 8. 架构重构计划

### 8.1 架构问题清单

#### 问题1：UI组件耦合在入口层（严重 - P0）

**位置**：`entry/entry_main.py`

**问题描述**：
- `LabelDesigner`类（设计器画布）直接在入口层
- `MainWindow`类（主窗口）直接在入口层
- 这两个类应该移动到 `entry/ui_window/` 目录

**违反规则**：
- `project_rules.md` 1.2 目录结构说明
- `project_rules.md` 2.2 L1入口层职责

**修改建议**：
1. 创建 `entry/ui_window/` 目录
2. 将 `LabelDesigner` 移动到 `entry/ui_window/designer_canvas.py`
3. 将 `MainWindow` 移动到 `entry/ui_window/main_window.py`
4. `entry/entry_main.py` 仅保留 `EntryMain` 类

---

#### 问题2：UI组件包含业务逻辑（严重 - P0）

**位置**：`LabelDesigner` 类

**问题描述**：
- `paintEvent()` 包含缩放计算
- `mousePressEvent()` 包含碰撞检测
- `mouseMoveEvent()` 包含坐标转换
- 这些业务逻辑应该拆分到L2/L3/L4层

**违反规则**：
- `project_rules.md` 2.2 L1入口层职责：不写任何业务逻辑
- `project_rules.md` 六、禁止事项：UI层写业务逻辑

**修改建议**：
1. 将碰撞检测逻辑移动到 `atom/atom_template.py`
2. 将坐标计算逻辑移动到 `molecule/molecule_draw.py`
3. 将缩放控制逻辑移动到 `molecule/molecule_draw.py`
4. UI层仅负责：接收用户事件、转发事件、更新显示

---

#### 问题3：缺少类型注解（严重 - P0）

**位置**：所有函数

**问题描述**：
- 几乎所有函数都缺少类型注解
- 违反 `project_rules.md` 3.1 PEP8规范

**修改建议**：
- 为所有函数添加完整的类型注解

---

#### 问题4：缺少文档字符串（严重 - P0）

**位置**：所有函数

**问题描述**：
- 只有 `EntryMain` 类的方法有简单的文档字符串
- 其他所有函数都缺少文档字符串

**修改建议**：
- 为所有函数添加 Google风格文档字符串
- 包含功能说明、参数说明、返回值说明

---

#### 问题5：函数过长（中等 - P1）

**位置**：
- `mousePressEvent()` - ~39行
- `mouseMoveEvent()` - ~45行
- `update_property_panel()` - ~51行
- `save_object_properties()` - ~43行

**问题描述**：
- 这些函数很长，不符合单一职责原则
- 应该拆分成更小的函数

**修改建议**：
- 将长函数拆分成多个小函数
- 每个函数只负责一个单一功能

---

#### 问题6：缺少中文注释（中等 - P2）

**位置**：整个文件

**问题描述**：
- 几乎没有中文注释
- 复杂逻辑难以理解

**修改建议**：
- 为复杂逻辑添加中文注释

---

### 8.2 重构实施步骤

#### 阶段1：补充代码质量（优先）

1. 为所有函数添加类型注解
2. 为所有函数添加文档字符串
3. 为复杂逻辑添加中文注释
4. 拆分过长的函数

**估计工作量**：1-2天

---

#### 阶段2：UI组件重构（重要）

1. 创建 `entry/ui_window/` 目录
2. 将 `LabelDesigner` 移动到 `designer_canvas.py`
3. 将 `MainWindow` 移动到 `main_window.py`
4. 简化 `entry/entry_main.py` 只保留 `EntryMain`
5. 更新所有引用路径

**估计工作量**：1-2天

---

#### 阶段3：业务逻辑拆分（关键）

1. 分析 `LabelDesigner` 中的业务逻辑
2. 将碰撞检测逻辑移动到 `atom/atom_template.py`
3. 将坐标计算逻辑移动到 `molecule/molecule_draw.py`
4. 将缩放控制逻辑移动到 `molecule/molecule_draw.py`
5. 更新 `entry_ui.py` 添加新的入口函数
6. 更新 `schedule_core.py` 添加新的调度函数

**估计工作量**：2-3天

---

#### 阶段4：测试和验证

1. 测试所有功能是否正常
2. 检查是否违反分层规则
3. 更新文档

**估计工作量**：1天

---

### 8.3 重构优先级

| 优先级 | 任务 | 原因 |
|-------|------|-----|
| P0 | 补充类型注解 | 严重违反规则，影响代码质量和可维护性 |
| P0 | 补充文档字符串 | 严重违反规则，影响代码理解和协作 |
| P0 | UI组件解耦重构 | 架构问题，影响后续开发和维护 |
| P1 | 业务逻辑拆分 | 架构问题，影响代码组织和分层 |
| P1 | 拆分过长函数 | 代码质量问题，提升可读性和可维护性 |
| P2 | 补充中文注释 | 代码质量问题，提升可读性和可维护性 |

---

## 9. 核心功能详细流程

### 9.1 模板管理流程

#### 9.1.1 新建模板

```
L1: entry_new_template()
    │
    ▼
L2: schedule_new_template()
    │
    ▼
L3: TemplateManager.molecule_template_create()
    │
    ▼
L4: atom_template_create() → 返回默认模板{
        label_size: {width:50, height:30, corner_radius:2},
        dpi: 300,
        objects: []
    }
```

#### 9.1.2 打开模板

```
L1: entry_open_template("path/to/template.label")
    │
    ▼
L2: schedule_open_template("path/to/template.label")
    │
    ├─► FileManager.molecule_file_exists() 检查文件
    │
    ├─► FileManager.molecule_file_get_directory() 获取目录
    │
    └─► ConfigManager.molecule_config_set_last_open_dir() 保存目录
            │
            ▼
        TemplateManager.molecule_template_load() → L4: atom_template_load()
```

#### 9.1.3 保存模板

```
L1: entry_save_template("path/to/template.label")
    │
    ▼
L2: schedule_save_template("path/to/template.label")
    │
    ▼
L3: TemplateManager.molecule_template_save()
    │
    ▼
L4: atom_template_save() → JSON文件
```

### 9.2 对象操作流程

#### 9.2.1 添加二维码对象

```
L1: LabelDesigner.add_qr_object(x, y)
    │
    ▼
L1: MainWindow.save_to_history()
    │
    ▼
L1: entry_add_qr_object(x, y)
    │
    ▼
L2: schedule_add_qr_object(x, y)
    │
    ▼
L3: TemplateManager.molecule_template_add_qr_object()
    │
    ├─► L4: atom_template_generate_id() → 生成对象ID
    │
    ├─► L4: atom_qr_create(...) → 创建二维码对象数据结构
    │
    └─► L4: atom_template_add_object() → 添加对象到模板
```

#### 9.2.2 拖拽移动对象

```
UI事件: mousePressEvent
    │
    ▼
L1: LabelDesigner.mousePressEvent(event)
    ├─► 计算缩放和偏移量
    ├─► 碰撞检测找到点击的对象
    └─► 设置 self.is_dragging = True
    │
    ▼
UI事件: mouseMoveEvent
    │
    ▼
L1: LabelDesigner.mouseMoveEvent(event)
    ├─► 计算移动量 delta_x, delta_y
    ├─► 计算新位置 new_x, new_y (无边界限制)
    └─► 调用 entry_update_object(obj_id, x=new_x, y=new_y)
    │
    ▼
L1: entry_update_object(obj_id, x, y)
    │
    ▼
L2: schedule_update_object(obj_id, x, y)
    │
    ▼
L3: TemplateManager.molecule_template_update_object(obj_id, x, y)
    │
    ▼
L4: atom_template_update_object(template, obj_id, x, y)
    ├─► 获取对象
    ├─► 更新 obj["position"]["x"] = x
    └─► 更新 obj["position"]["y"] = y
```

#### 9.2.3 删除对象

```
L1: LabelDesigner.keyPressEvent(event) [Delete键]
    │
    ▼
L1: MainWindow.save_to_history()
    │
    ▼
L1: entry_remove_object(obj_id)
    │
    ▼
L2: schedule_remove_object(obj_id)
    │
    ▼
L3: TemplateManager.molecule_template_remove_object(obj_id)
    │
    ▼
L4: atom_template_remove_object(template, obj_id)
```

#### 9.2.4 更新对象属性

```
L1: MainWindow.save_object_properties()
    │
    ▼
L1: entry_update_object_properties(obj_id, **kwargs)
    │
    ▼
L2: schedule_update_object_properties(obj_id, **kwargs)
    │
    ▼
L3: PropertyManager.molecule_property_update_object(obj, **kwargs)
    │   ├─► L4: atom_property_update_position()
    │   ├─► L4: atom_property_update_size()
    │   └─► L4: atom_property_update_qr_properties() 或 atom_property_update_text_properties()
    │
    ▼
L3: TemplateManager.molecule_template_update_object(obj_id, **kwargs)
    │
    ▼
L4: atom_template_update_object(template, obj_id, **kwargs)
```

### 9.3 批量导出流程

```
L1: entry_batch_export("output_dir", "png")
    │
    ▼
L2: schedule_batch_export("output_dir", "png")
    │
    ▼
L3: ImageManager.molecule_image_batch_export()
    │
    ├─► 获取模板数据
    │
    ├─► 获取CSV数据
    │
    └─► 调用_batch_process()进行批量处理
            │
            ├─► 遍历CSV每一行
            │      │
            │      ▼
            │    创建空白标签图像 (atom_image_create_label)
            │      │
            │      ▼
            │    遍历模板中每个对象
            │      │
            │      ├─► [QR对象] 调用QRManager生成二维码 → 添加到标签
            │      └─► [Text对象] 直接添加文本到标签
            │      │
            │      ▼
            │    [PNG] 保存单个文件
            │    [PDF] 收集到图像列表
            │
            ▼
        [PDF] 调用_save_as_pdf()合并为PDF
```

---

## 10. 已知问题与修复记录

### 10.1 对象拖拽移动问题（已修复）

**问题描述**：
点击工具栏添加QR对象后，在设计器标签区域内无法通过拖拽移动对象位置。

**根本原因**：
`atom_template_update_object` 函数只处理了 `position`、`size`、`properties` 字典参数的更新，没有处理单独的 `x`、`y`、`width`、`height` 参数。

**修复方案**：
修改 `atom/atom_template.py` 中的 `atom_template_update_object` 函数，增强参数处理逻辑：

```python
# 处理 position 字典
if "position" in kwargs:
    obj["position"] = kwargs["position"]

# 处理单独的 x, y 参数
if "x" in kwargs or "y" in kwargs:
    if "position" not in obj:
        obj["position"] = {"x": 0, "y": 0}
    if "x" in kwargs:
        obj["position"]["x"] = kwargs["x"]
    if "y" in kwargs:
        obj["position"]["y"] = kwargs["y"]

# 处理 size 字典
if "size" in kwargs:
    obj["size"] = kwargs["size"]

# 处理单独的 width, height 参数
if "width" in kwargs or "height" in kwargs:
    if "size" not in obj:
        obj["size"] = {"width": 0, "height": 0}
    if "width" in kwargs:
        obj["size"]["width"] = kwargs["width"]
    if "height" in kwargs:
        obj["size"]["height"] = kwargs["height"]
```

**修改文件**：
- `atom/atom_template.py` - 增强 `atom_template_update_object` 函数
- `entry/entry_main.py` - 添加调试输出到 `mousePressEvent` 和 `mouseMoveEvent`

**调试信息**：
在拖拽过程中会输出以下调试信息：
- `mousePressEvent`: 鼠标按钮和位置
- 选中的对象信息（ID、类型、位置、大小、屏幕位置）
- `mouseMoveEvent`: 拖拽状态和鼠标位置
- 对象移动信息（原位置、移动量、新位置）

### 10.2 移除对象边界限制（已完成）

**问题描述**：
对象在拖拽时被限制在标签边界内，无法拖到标签区域外。

**修复方案**：
在 `entry/entry_main.py` 中移除了边界限制代码：

```python
# 原来限制在标签边界内，现在已移除
# new_x = max(0, min(new_x, label_width - obj['size']['width']))
# new_y = max(0, min(new_y, label_height - obj['size']['height']))
```

**修改文件**：
- `entry/entry_main.py` - 移除第226-227行的边界限制代码

**功能说明**：
现在对象可以自由拖拽到标签外的任何位置，不再受边界限制。

---

## 11. 类型注解规范

### 11.1 函数类型注解要求

所有函数**必须**包含类型注解，包括：
- 参数类型
- 返回值类型

### 11.2 类型注解示例

```python
# L4 原子层示例
def atom_qr_generate(
    content: str,
    error_correction: str = "Q",
    qr_version: str = "21x21"
) -> Optional[Image.Image]:
    """生成二维码图像

    Args:
        content: 二维码内容
        error_correction: 纠错级别 (L/M/Q/H)
        qr_version: 二维码版本

    Returns:
        二维码图像，失败返回None
    """
    pass

# L3 分子层示例
def molecule_image_add_qr(
    self,
    label_img: Image.Image,
    qr_img: Image.Image,
    x: float,
    y: float,
    width: float,
    height: float,
    dpi: int = 300
) -> Image.Image:
    """将二维码添加到标签"""
    return atom_image_add_qr(label_img, qr_img, x, y, width, height, dpi)

# L2 调度层示例
def schedule_add_qr_object(
    self,
    x: float,
    y: float,
    width: float = 10,
    height: float = 10,
    qr_version: str = "21x21",
    error_correction: str = "Q",
    content: str = "",
    batch: bool = False,
    csv_column: str = ""
) -> str:
    """调度：添加二维码对象"""
    return self.template_manager.molecule_template_add_qr_object(...)

# L1 入口层示例
def entry_add_qr_object(
    self,
    x: float,
    y: float,
    width: float = 10,
    height: float = 10,
    qr_version: str = "21x21",
    error_correction: str = "Q",
    content: str = "",
    batch: bool = False,
    csv_column: str = ""
) -> str:
    """入口：添加二维码对象"""
    return self.scheduler.schedule_add_qr_object(...)
```

---

## 12. 代码风格规范

### 12.1 命名规范

| 类型 | 规范 | 示例 |
|-----|------|------|
| 变量 | 驼峰命名 | `userName`, `orderList` |
| 常量 | 全大写+下划线 | `MAX_SIZE`, `API_URL` |
| 函数/方法 | 动词开头驼峰 | `getUserInfo`, `calculateTotal` |
| 类名 | 大驼峰 | `LabelPropertyLoader` |
| 原子函数 | `atom_模块_动作` | `atom_qr_generate` |
| 分子方法 | `molecule_业务_动作` | `molecule_template_create` |
| 调度函数 | `schedule_事件名称` | `schedule_new_template` |
| 入口函数 | `entry_界面_动作` | `entry_new_template` |

### 12.2 格式规范

- 缩进：4空格
- 行宽：≤88字符
- 函数间空2行
- 类内方法空1行
- 运算符两侧空格
- 逗号后空格

### 10.3 导入顺序

```python
# 1. 标准库
import json
import os
from typing import Dict, Any, List

# 2. 第三方库
import pandas as pd
from PIL import Image

# 3. 本地导入（按层级从高到低）
from atom.atom_template import atom_template_create
from molecule.molecule_template import TemplateManager
from schedule.schedule_core import CoreScheduler
```

---

## 13. 架构验证清单

### 13.1 分层依赖验证（L2已合并到L1）

- [ ] L1只调用L3，不直接调用L4
- [ ] L3只调用L4，不调用L1
- [ ] L4不调用任何层
- [ ] 禁止反向调用（L3→L1）
- [ ] 禁止分子调用分子
- [ ] 禁止原子调用原子

### 13.2 原子层验证

- [ ] 每个函数≤80行
- [ ] 无if/else分支
- [ ] 无for/while循环
- [ ] 无业务逻辑判断
- [ ] 纯函数无副作用
- [ ] 完整类型注解
- [ ] 符合命名规范

### 13.3 分子层验证

- [ ] 只编排原子调用
- [ ] 内部允许业务逻辑（if/for）
- [ ] 不调用其他分子
- [ ] 不做跨模块决策
- [ ] 完整类型注解
- [ ] 符合命名规范

### 13.4 入口层验证

- [ ] 接收用户事件并转发到L3
- [ ] 管理分子管理器实例
- [ ] 不写业务逻辑
- [ ] 完整类型注解
- [ ] 符合命名规范（`entry_界面_动作()`）

---

## 14. 版本变更记录

### v1.12.10 (2026-05-15)
- **UI优化**：调整属性面板显示宽度
- **修改内容**：
  1. 属性面板最小宽度从 280px 增加到 340px（+60px，约4个汉字宽度）
  2. 分割器初始大小从 [700, 220] 调整为 [600, 340]，确保属性面板完整显示
- **修改文件**：
  - 更新 `entry/ui_window/main_window.py` - 修改属性面板最小宽度和分割器初始大小

### v1.12.9 (2026-05-15)
- **功能优化**：修复预览对话框回车键导致窗口关闭的问题
- **问题描述**：当用户在页码数字框输入数字后按回车，预览窗口会意外关闭
- **根本原因**：回车后焦点移动到关闭按钮，触发按钮点击事件
- **修复内容**：
  1. 创建自定义 `PageSpinBox` 类，继承自 `QSpinBox`
  2. 在 `PageSpinBox` 中拦截回车键（`Key_Return` 和 `Key_Enter`）
  3. 回车时只调用预览刷新回调，不传播事件到其他控件
  4. 刷新后保持焦点在页码控件上
- **修改文件**：
  - 更新 `entry/ui_window/dialog/preview_dialog.py` - 添加 PageSpinBox 类，拦截回车键

### v1.12.8 (2026-05-15)
- **Bug修复**：修复 `schedule_core.py` 中 `Optional` 类型未导入的错误
- **修复内容**：
  1. 在 `schedule_core.py` 开头添加 `from typing import Optional` 导入语句
- **修改文件**：
  - 更新 `schedule/schedule_core.py` - 添加 Optional 类型导入

### v1.12.7 (2026-05-13)
- **代码审查修复**：根据code_review技能审查结果进行修复
- **修复内容**：
  1. 将 `main_window.py` 中计算QR/文本对象默认位置的逻辑移到 `molecule_template.py`
  2. 在 `molecule_template.py` 添加 `molecule_template_calculate_default_qr_position()` 和 `molecule_template_calculate_default_text_position()` 方法
  3. 在 `schedule_core.py` 添加 `schedule_get_default_qr_position()` 和 `schedule_get_default_text_position()` 方法
  4. 在 `entry_ui.py` 添加 `entry_get_default_qr_position()` 和 `entry_get_default_text_position()` 方法
  5. 修改 `main_window.py` 的 `on_qr_button_clicked()` 和 `on_text_button_clicked()` 使用新的入口方法
- **修改文件**：
  - 更新 `molecule/molecule_template.py` - 添加计算默认位置方法
  - 更新 `schedule/schedule_core.py` - 添加调度方法
  - 更新 `entry/entry_ui.py` - 添加入口方法
  - 更新 `entry/ui_window/main_window.py` - 使用新的入口方法

### v1.12.6 (2026-05-13)
- **代码审查修复**：根据code_review技能审查结果进行修复
- **修复内容**：
  1. 删除 `entry_ui.py` 中的重复方法 `entry_init_designer_area()`
  2. 为 `entry_get_csv_data()` 添加返回类型注解 `Optional[Any]`
- **修改文件**：
  - 更新 `entry/entry_ui.py` - 删除重复方法，添加类型注解

### v1.12.3 (2026-05-13)
- **文档更新**：全面更新 `new_design.md` 文档内容为最新状态
- **更新内容**：
  - 更新版本信息为 v1.12.2
  - 更新架构验证清单，反映L2已合并到L1的现状
  - 更新分子模块方法数量统计
  - 更新入口函数清单（33个→43个）
  - 更新菜单结构和对话框结构说明
- **修改文件**：
  - 更新 `new_design.md` - 全面更新文档

### v1.12.2 (2026-05-13)
- **UI优化**：属性面板最小宽度从250增加到280（增加约2个汉字宽度），确保内容完整显示
- **修改文件**：
  - 更新 `entry/ui_window/main_window.py` - 修改属性面板最小宽度

### v1.12.1 (2026-05-13)
- **UI优化**：将导入菜单中 "xlsx 导入（推荐）" 改为 "xlsx 导入（不易出错）"
- **修改文件**：
  - 更新 `entry/ui_window/menu/menu_import.py` - 修改菜单文字

### v1.12.0 (2026-05-13)
- **功能完善**：保存上次打开/导入/导出目录
- **功能详情**：
  1. 打开/保存模板文件时，记住上次使用的目录
  2. 导入CSV/Excel文件时，记住上次使用的目录
  3. 批量导出时，记住上次选择的导出目录
  4. 下次打开软件时，自动定位到上次使用的目录
- **打包配置**：
  - 添加GitHub Actions工作流配置，支持自动构建发布
  - 优化用户配置文件路径管理，确保打包后配置可正常读写
- **代码优化**：
  - 修复 `entry_ui.py` 中跨层调用问题，统一通过 `schedule_` 调度层调用
- **修改文件**：
  - 更新 `entry/entry_ui.py` - 添加导出目录入口方法，修复跨层调用
  - 更新 `entry/ui_window/main_window.py` - 导出时保存目录，打开时加载目录
  - 更新 `atom/atom_config.py` - 添加获取用户配置路径的功能
  - 更新 `molecule/molecule_config.py` - 添加导出目录配置方法
  - 更新 `schedule/schedule_core.py` - 添加导出目录调度方法
  - 新增 `.github/workflows/build.yml` - GitHub Actions工作流配置

### v1.11.0 (2026-05-03)
- **新功能**：添加预览功能和批量导出进度显示
- **功能详情**：
  1. 将工具栏"预留4"按钮改为"预览"按钮
  2. 点击预览按钮，显示当前标签的PNG预览
  3. 关闭预览窗口后，自动删除临时PNG文件
  4. 批量导出对话框点击开始后，在同一对话框内显示导出进度
  5. 导出完成后用户点击确认，关闭批量导出对话框
- **修改文件**：
  - 更新 `entry/ui_window/toolbar.py` - 修改预留4按钮为预览按钮
  - 新增 `entry/ui_window/dialog/preview_dialog.py` - 预览对话框
  - 更新 `entry/ui_window/dialog/batch_export_dialog.py` - 合并进度显示功能
  - 更新 `molecule/molecule_image.py` - 添加进度回调支持
  - 更新 `schedule/schedule_core.py` - 添加进度回调传递
  - 更新 `entry/entry_ui.py` - 添加进度回调参数
  - 更新 `entry/ui_window/main_window.py` - 添加预览功能和进度处理

### v1.10.2 (2026-05-03)
- **Bug修复**：设计器中多行文本显示重叠，第一行文字底部约1/3被遮挡
- **问题原因**：使用固定的 `font_size * 1.2` 作为行高，对于某些字体可能不够容纳完整字符
- **修复内容**：使用 `QFontMetrics.height()` 获取准确的字体高度作为行高，确保每行文本都能完整显示
- **修改文件**：
  - 更新 `atom/atom_draw.py` - 修改文本绘制逻辑，使用字体度量获取准确行高

### v1.10.1 (2026-05-03)
- **功能修改**：优化文本自动换行功能
- **修改内容**：
  - 行间距统一设置为字高的1.2倍
  - 导出PNG时也使用相同的对齐设置（支持水平对齐和垂直对齐）
  - 修复最后一个字符显示不全的问题（跳过宽度超过容器的字符）
- **修改文件**：
  - 更新 `atom/atom_draw.py` - 修改 `_wrap_text()` 函数，添加字符宽度检查
  - 更新 `atom/atom_image.py` - 修改 `atom_image_add_text()` 函数，添加对齐参数支持
  - 更新 `molecule/molecule_image.py` - 传递对齐参数

### v1.10.0 (2026-05-03)
- **Bug修复**：导出PDF时出现JPEG错误
- **问题原因**：虽然已经在 `atom_image_add_qr()` 中添加了模式转换，但在PDF导出流程中，某些图像可能仍然不是纯RGB模式，导致Pillow保存PDF时内部尝试用JPEG编码失败
- **修复内容**：在 `_save_as_pdf()` 方法中添加双重检查，确保所有图像都被正确转换为RGB模式，并显式指定保存格式为PDF
- **修改文件**：
  - 更新 `molecule/molecule_image.py` - 完善PDF保存逻辑

### v1.9.9 (2026-05-03)
- **功能修改**：文本对象绘制支持自动换行
- **修改内容**：
  - 当文本内容超出文本对象宽度时，自动进行换行显示
  - 支持垂直对齐（top/middle/bottom）
  - 添加 `_wrap_text()` 辅助函数实现按字符换行
- **修改文件**：
  - 更新 `atom/atom_draw.py` - 修改文本绘制逻辑，添加自动换行功能

### v1.9.8 (2026-05-03)
- **Bug修复**：批量导出失败，错误信息为 `'JPEG'`
- **问题原因**：二维码图像生成后默认为 P 模式（调色板模式），而标签图像为 RGB 模式，模式不匹配导致保存失败
- **修复内容**：在 `atom_image_add_qr()` 函数中添加图像模式转换，确保二维码图像与标签图像模式一致
- **修改文件**：
  - 更新 `atom/atom_image.py` - 添加模式转换逻辑

### v1.9.7 (2026-05-03)
- **功能修改**：当选择批量生成且选择数据列时，在标签设计区显示第一行数据
- **功能详情**：
  - QR对象：如果batch=True且有csv_column，则显示第一行数据
  - Text对象：如果batch=True且有csv_column，则显示第一行数据
- **修改内容**：
  - `molecule/molecule_csv.py - 添加 `molecule_csv_get_first_row_value()
  - `schedule/schedule_core.py` - 添加调度方法
  - `entry/entry_ui.py` - 添加入口方法和传递回调
  - `atom/atom_draw.py` - 更新绘制逻辑支持第一行数据
  - `molecule/molecule_draw.py` - 更新绘制管理器

### v1.9.6 (2026-05-03)
- **Bug修复**：导入CSV后点击text对象时内容被清空
- **问题原因**：`update_qr_csv_columns` 和 `update_text_csv_columns` 方法中 `clear()` 和 `addItem()` 触发信号
- **修复内容**：为两个方法的 CSV 列操作添加信号阻塞

### v1.9.5 (2026-05-03)
- **功能修改**：属性面板默认宽度增加1/4
- **修改内容**：`setMinimumWidth` 从 200 改为 250

### v1.9.4 (2026-05-03)
- **代码重构**：将信号阻塞代码封装为辅助方法
- **重构内容**：
  - `_set_basic_signals_blocked(blocked)` - 基本属性控件信号阻塞
  - `_set_qr_signals_blocked(blocked)` - 二维码属性控件信号阻塞
  - `_set_text_signals_blocked(blocked)` - 文本属性控件信号阻塞
- **修改文件**：
  - 更新 `entry/ui_window/property_panel.py` - 封装信号阻塞逻辑

### v1.9.3 (2026-05-03)
- **Bug修复**：导入CSV/XLSX后点击对象时属性被清空的问题
- **修复内容**：为文本属性的对齐按钮（左/中/右、上/中/下）添加信号阻塞
- **修改文件**：
  - 更新 `entry/ui_window/property_panel.py` - 完善信号阻塞逻辑

### v1.9.2 (2026-05-03)
- **代码重构**：将 `property_panel.py` 的 `__init__` 方法拆分为多个私有方法
- **重构内容**：
  - `_init_layout()` - 初始化布局
  - `_init_object_info()` - 对象信息标签
  - `_init_basic_properties()` - 基本属性面板（位置、尺寸）
  - `_init_qr_properties()` - 二维码属性面板
  - `_init_text_properties()` - 文本属性面板
  - `_init_save_button()` - 保存按钮
- **修改文件**：
  - 更新 `entry/ui_window/property_panel.py` - 拆分 `__init__` 方法提升可读性

### v1.9.1 (2026-05-03)
- **Bug修复**：选择存在的 text 对象时，属性面板"内容"会被清空的问题
- **Bug修复**：属性面板更新时信号触发导致的属性覆盖问题
- **修复方案**：在 `property_panel.py` 的 `_update_qr_properties` 和 `_update_text_properties` 方法中添加信号阻塞
- **修改文件**：
  - 更新 `entry/ui_window/property_panel.py` - 为所有输入控件添加 `blockSignals(True/False)` 包裹

### v1.9.0 (2026-05-03)
- **项目重构**：按用户逻辑结构重新组织代码
- **目录结构**：
  - `entry/ui_window/menu/` - 所有菜单独立文件
  - `entry/ui_window/dialog/` - 所有对话框独立文件
  - `entry/ui_window/toolbar.py` - 工具栏独立文件
  - `entry/ui_window/property_panel.py` - 属性面板独立文件
- **恢复 L2 调度层**：`schedule/schedule_core.py` 负责事件调度
- **完善四层架构**：main → L1 → L2 → L3 → L4 完整调用链
- **修改文件**：
  - 创建 `entry/ui_window/menu/menu_file.py`
  - 创建 `entry/ui_window/menu/menu_settings.py`
  - 创建 `entry/ui_window/menu/menu_import.py`
  - 创建 `entry/ui_window/menu/menu_export.py`
  - 创建 `entry/ui_window/menu/menu_help.py`
  - 创建 `entry/ui_window/menu/menu_history.py`
  - 创建 `entry/ui_window/dialog/basic_settings_dialog.py`
  - 创建 `entry/ui_window/dialog/csv_preview_dialog.py`
  - 创建 `entry/ui_window/dialog/batch_export_dialog.py`
  - 创建 `entry/ui_window/toolbar.py`
  - 创建 `entry/ui_window/property_panel.py`
  - 创建 `schedule/schedule_core.py`
  - 更新 `entry/entry_ui.py` - 调用 L2 调度层
  - 更新 `entry/ui_window/main_window.py` - 使用新导入和菜单类
  - 更新 `molecule/molecule_template.py` - 添加新方法
  - 更新 `molecule/molecule_csv.py` - 添加新方法
  - 更新 `molecule/molecule_image.py` - 更新方法签名
  - 删除 `ui_components.py` - 已拆分到独立文件

### v1.8.1 (2026-05-03)
- **代码重构**：
  - 属性面板更新逻辑重构，从 `main_window.py` 迁移到 `PropertyPanel` 类
  - 在 `PropertyPanel` 类中添加 `update_from_object()` 方法，实现数据绑定封装
  - 提取辅助方法：`_update_position_inputs()`、`_update_qr_properties()`、`_update_text_properties()`
  - `update_property_panel` 函数从 85 行简化为 15 行

- **修改文件**：
  - `ui_components.py`：
    - 添加 `update_from_object()` 方法
    - 添加 `_update_position_inputs()` 方法
    - 添加 `_update_qr_properties()` 方法
    - 添加 `_update_text_properties()` 方法
    - 添加 `clear()` 方法
  - `entry/ui_window/main_window.py`：
    - 简化 `update_property_panel()` 方法，调用 PropertyPanel 的更新方法

### v1.8.0 (2026-05-03)
- **配置优化**：
  - 修改默认新标签尺寸配置：50mm x 30mm，圆角2mm，DPI300
  - 原有默认圆角10mm，现在改为2mm，更加美观

- **修改文件**：
  - `atom/atom_template.py`：
    - `atom_template_create_default` 函数 `corner_radius` 默认参数从 10 改为 2
    - `atom_template_create_empty` 函数硬编码 `corner_radius` 从 10 改为 2

### v1.7.0 (2026-05-03)
- **架构简化**：
  - 删除 L2 调度层（schedule_core.py），合并到 L1 入口层
  - 删除空壳 molecule 文件：molecule_file.py, molecule_init.py, molecule_qr.py, molecule_property.py
  - 保留有实际业务逻辑的 molecule 文件：
    - molecule_template.py：模板管理 + 属性更新
    - molecule_csv.py：CSV数据管理
    - molecule_config.py：配置管理
    - molecule_image.py：图像导出
    - molecule_history.py：历史记录
    - molecule_draw.py：绘制管理
  - entry_ui.py 直接调用 molecule 层，减少调用链层级

- **简化前架构**（4层，调用链复杂）：
  ```
  L1 entry_ui.py → L2 schedule_core.py (10个manager) → L3 molecule_*.py (10个文件) → L4 atom_*.py
  ```

- **简化后架构**（3层，调用链清晰）：
  ```
  L1 entry_ui.py → L3 molecule_*.py (6个有实际逻辑的文件) → L4 atom_*.py
  ```

- **删除的文件**：
  - schedule/schedule_core.py
  - molecule/molecule_file.py
  - molecule/molecule_init.py
  - molecule/molecule_qr.py
  - molecule/molecule_property.py

- **修改的文件**：
  - `entry/entry_ui.py`：直接调用 molecule 层，管理5个 manager 实例
  - `molecule/molecule_template.py`：合并属性更新功能，添加 molecule_template_update_object_properties、molecule_template_get_object_index、molecule_template_set_template 方法
  - `molecule/molecule_draw.py`：保留（entry_ui.py 仍需调用）

### v1.6.0 (2026-05-03)
- **Bug修复**：
  - 修复导入CSV数据后，点击任意对象会覆盖对象属性的问题
  - 问题根源：`update_property_panel` 更新输入框值时触发 `editingFinished` 信号
  - 信号处理函数 `save_object_properties` 将旧输入框值保存到**新选中**的对象上
  - 解决方案：在 `update_property_panel` 设置输入框值前，先使用 `blockSignals(True)` 阻塞信号
  - 设置完成后再 `blockSignals(False)` 恢复信号

- **修改文件**：
  - `entry/ui_window/main_window.py`：在 `update_property_panel` 中为 x/y/width/height 输入框阻塞信号
  - `ui_components.py`：移除 `show_qr_properties` 和 `show_text_properties` 中的调试打印语句

### v1.2.0 (2026-05-01)
- **重构内容**：
  - 重构 entry/entry_main.py，将UI组件拆分到 entry/ui_window/ 目录
  - 符合 project_rules.md 1.2 目录结构规范
  - 实现方案A的完整架构重构

- **主要变更**：
  1. `entry/ui_window/main_window.py`：创建 MainWindow 类，负责组装UI组件
  2. `entry/ui_window/designer_canvas.py`：创建 LabelDesigner 类，负责设计器画布
  3. `entry/ui_window/__init__.py`：创建子包初始化文件
  4. `entry/entry_main.py`：简化为只包含 EntryMain 类，专注创建和显示窗口

- **目录结构**：
  ```
  entry/
  ├── entry_main.py          # 主窗口入口（仅EntryMain类）
  ├── entry_ui.py            # UI事件转发入口
  └── ui_window/             # UI窗口子层
      ├── __init__.py
      ├── main_window.py     # MainWindow类
      └── designer_canvas.py # LabelDesigner类
  ```

- **重构优点**：
  - UI组件独立成文件，便于维护
  - 符合四层架构的目录结构规范
  - 便于团队协作和AI编程
  - 代码职责更加清晰

### v1.5.0 (2026-05-01)
- **Bug修复**：
  - 修复导入 CSV/Excel 文件功能导致异常退出的问题
  - 问题根源：`molecule_csv_import` 返回值不匹配
  - 原返回值：`(bool, error_message)` - 与调用方期望的 `(csv_data, csv_handler)` 不匹配
  - 修改后返回值：`(data, CSVManager实例)` - 正确返回数据和处理器

- **Bug修复**：
  - 修复 `CSVManager` 缺少 `get_row_count()` 方法导致异常退出
  - 新增 `get_row_count()` 和 `get_preview_data()` 方法供 UI 层调用

- **Bug修复**：
  - 修复绘制对象时 `KeyError: 'content'` 导致程序崩溃
  - 问题根源：`atom_draw_objects` 直接访问 `obj['content']` 等键，未使用默认值
  - 修改后使用 `obj.get('content', '')` 等安全访问方式

- **修改文件**：
  - `molecule/molecule_csv.py`：修复 `molecule_csv_import` 和 `molecule_excel_import` 返回值
  - 新增 `molecule_csv_get_row_count()` 和 `get_row_count()` 方法
  - `atom/atom_draw.py`：为 QR 和文本对象的所有属性添加默认值处理

### v1.4.0 (2026-05-01)
- **功能优化**：
  - 完善属性面板的自动更新功能
  - 当回车、焦点转移、或点击保存时，自动根据当前变化的属性值，更新标签设计区的文本对象
  - 补充缺失的信号连接

- **Bug修复**：
  - 修复基本属性、文本属性、QR属性修改后未触发重绘标签区对象的问题
  - 问题根源：`schedule_update_object_properties` 方法参数结构不匹配
  - 修改后正确处理嵌套结构（position, size）和其他扁平属性

- **Bug修复**：
  - 修复修改对象高度时程序异常退出的问题
  - 问题根源：`atom_property_update_text_properties` 错误地访问 `obj['properties']['font']`
  - 文本对象的 `font`、`font_size` 等属性存储在顶层，不是嵌套在 `properties` 下
  - 修改后直接更新 `obj['font']` 等，而不是 `obj['properties']['font']`

- **修改文件**：
  - `entry/ui_window/main_window.py`：添加额外的信号连接
  - `schedule/schedule_core.py`：修复 `schedule_update_object_properties` 方法参数处理
  - `atom/atom_property.py`：修复 `atom_property_update_text_properties` 直接更新顶层属性

- **实现说明**：
  - 新增信号包括：font_combo.currentTextChanged
  - 新增信号包括：align_button_group.buttonClicked
  - 新增信号包括：qr_csv_column_combo.currentTextChanged
  - 新增信号包括：text_csv_column_combo.currentTextChanged
  - 调度层方法现在正确提取 position.size 中的嵌套值
  - 文本对象属性结构：顶层存储（如 `obj['font']`），不是嵌套在 `obj['properties']` 下

### v1.3.0 (2026-05-01)
- **功能新增**：
  - 在对象上方靠左上角显示对象ID（如 `9da2a3d5`）
  - 字体：Arial，高3mm
  - 颜色：深蓝色半透明 (0, 0, 139, 180)
  - 显示前8位字符

- **功能优化**：
  - 文本属性面板样式选项改为垂直排列（每个选项单独一行）
  - 新增文本对齐功能（左对齐、中对齐、右对齐）

- **修改文件**：
  - `ui_components.py`：修改文本属性面板布局，新增对齐按钮组
  - `main_window.py`：保存和加载文本对齐属性
  - `atom/atom_draw.py`：支持文本对齐绘制（`text_align` 属性）

- **实现说明**：
  - 样式选项从水平排列改为垂直排列
  - 使用 `QButtonGroup` 管理三个对齐按钮
  - 对齐值存储为 `text_align`: 'left'/'center'/'right'

### v1.2.0 (2026-05-03)
- **新增功能**：
  - 文本属性增加垂直对齐选项（上/中/下）

- **Bug修复**：
  - 修复属性面板宽度和高度不能实时调整的问题：将 `editingFinished` 信号改为 `valueChanged` 信号
  - 修复属性面板顶部紧贴菜单行的问题：添加布局边距 `setContentsMargins(5, 5, 5, 5)`

- **布局优化**：
  - 移除工具栏与工作区之间的5px间距，让属性面板上部紧贴菜单行，右侧紧贴窗口边缘
  - 移除工具栏底部边距（从5px改为0px），使属性面板紧贴工具栏
  - 属性面板支持拖动调整宽度（使用QSplitter），支持垂直滚动（使用QScrollArea）
  - 属性面板内容靠上边缘对齐（设置`setAlignment(Qt.AlignTop)`）
  - 属性面板仅保留左侧浅灰色分割线边框（`border-left: 1px solid #e0e0e0`），移除 QScrollArea 默认边框
  - 点击对象时检测批量生成状态，未导入CSV数据时自动取消勾选并提示，同时取消 is_dragging 状态
  - 批量导出失败时显示详细错误原因（未导入数据/标签尺寸无效/无对象/数据列不匹配/权限错误等）
  - Bug修复：批量导出时标签尺寸检查逻辑错误，模板尺寸在 `label_size` 字典中而非根级别
  - Bug修复：属性面板加载时 CSV 列下拉框为空且未设置已选数据列，将 CSV 列加载移到对象属性设置之前，并添加 `csv_column` 设置逻辑

- **修改文件**：
  - `atom/atom_text.py`：添加 `vertical_align` 默认值
  - `atom/atom_property.py`：添加 `vertical_align` 参数
  - `molecule/molecule_property.py`：传递 `vertical_align` 参数
  - `molecule/molecule_template.py`：添加 `vertical_align` 参数
  - `atom/atom_draw.py`：实现垂直对齐绘制（使用 `Qt.AlignTop`/`AlignVCenter`/`AlignBottom`）
  - `ui_components.py`：添加垂直对齐按钮组（上/中/下）和布局边距
  - `main_window.py`：保存/加载垂直对齐属性，修改信号连接（editingFinished→valueChanged），移除spacer让布局紧贴窗口边缘，使用QSplitter和QScrollArea实现属性面板可调整宽度和垂直滚动
  - `molecule/molecule_image.py`：修改 `molecule_image_batch_export` 返回详细错误信息
  - `schedule/schedule_core.py`：修改 `schedule_batch_export` 传递详细错误信息
  - `entry/entry_ui.py`：修改 `entry_batch_export` 传递详细错误信息

- **实现说明**：
  - 垂直对齐使用 PyQt5 的 `Qt.AlignTop`、`Qt.AlignVCenter`、`Qt.AlignBottom` 标志
  - 与水平对齐组合使用：`align_flags = h_align_flags | v_align_flags`

---

### v1.1.0 (2026-04-30)
- **重构内容**：
  - 修复L2调度层违规调用L4原子层的问题
  - 修复L3分子层职责不纯的问题
  - 修复L4原子层函数过于复杂的问题
  - 添加缺失的原子函数
  - 完善类型注解

- **主要变更**：
  1. `schedule_core.py`：移除直接调用`atom_qr_generate()`，改用`ImageManager`分子方法
  2. `molecule_image.py`：重构为包含完整业务逻辑的分子，添加`_batch_process()`等内部方法
  3. `atom_image.py`：拆分复杂函数，添加辅助原子函数
  4. `atom_qr.py`：添加完整的`qr_version`参数支持

---

## 15. 总结

本设计文档详细描述了QR Label Creator项目的四层架构设计，通过严格的分层规范确保代码的可维护性和可扩展性。

**核心原则**：
1. 每层只依赖其下一层
2. 原子层是最小单元，无业务逻辑
3. 分子层编排原子，实现完整业务
4. 调度层协调分子，不含业务逻辑
5. 入口层转发事件，不含业务逻辑

**架构优势**：
- 代码职责清晰
- 便于单元测试
- 易于扩展功能
- 支持并行开发
- 降低代码耦合度
