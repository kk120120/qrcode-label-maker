---
name: "understand_code"
description: "Explains project structure and feature implementation with call chains. Invoke when user asks to understand or explain code."
---

# Understand Code

快速理解项目结构和某个功能的完整实现，包括调用链和数据流。

## 适用场景
- 理解现有功能
- 学习代码库
- 接手新项目
- 分析复杂调用链

## 执行步骤（必须完整执行所有5个步骤，不得跳过任何步骤）

### 第一步：项目结构概览
1. 阅读 `mypolicy/project_rules.md` 理解四层架构
2. 阅读 `new_design.md` 了解项目设计
3. 理解目录结构和各层职责

**四层架构职责**：
| 层级 | 目录 | 职责 | 示例文件 |
|-----|------|------|---------|
| L1 入口层 | `entry/` | 接收用户事件，转发 | entry_ui.py, main_window.py |
| L2 调度层 | `schedule/` | 协调分子执行顺序 | schedule_core.py |
| L3 分子层 | `molecule/` | 编排原子操作 | molecule_template.py |
| L4 原子层 | `atom/` | 纯函数操作 | atom_template.py |

### 第二步：功能调用链分析
1. 从用户操作开始追踪
2. 列出完整调用链
3. 标注每个层级的文件和方法

**调用链格式**：
```
用户操作 → UI组件 (L1) → entry_ui.py (L1) → schedule_core.py (L2) → molecule_xxx.py (L3) → atom_xxx.py (L4)
```

### 第三步：逐层级讲解
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

### 第四步：数据流分析
1. 数据输入在哪里？
2. 数据在每层如何变化？
3. 最终输出是什么？
4. 数据存储在哪里？

### 第五步：总结
1. 这个功能的整体设计思路
2. 值得学习的地方
3. 如果要修改，应该从哪里入手
4. 潜在的问题和风险

## 规则
- 必须完整执行所有5个步骤
- 严格按照四层架构分析
- 追踪完整调用链
- 标注每个文件和方法
- 说明数据流向
- 指出关键代码位置

## 讲解模板

```markdown
# 功能理解：[功能名称]

## 1. 功能概述
[功能做什么]

## 2. 调用链
```
用户操作 → [L1文件] → [L2文件] → [L3文件] → [L4文件]
```

## 3. 逐层分析

### L1 入口层
**文件**：`entry/xxx.py`
**关键方法**：
- `entry_xxx()` - [功能]

### L2 调度层
**文件**：`schedule/schedule_core.py`
**关键方法**：
- `schedule_xxx()` - [功能]

### L3 分子层
**文件**：`molecule/xxx.py`
**关键方法**：
- `molecule_xxx()` - [功能]

### L4 原子层
**文件**：`atom/xxx.py`
**关键函数**：
- `atom_xxx()` - [功能]

## 4. 数据流
[数据如何流动]

## 5. 修改建议
[如果要修改，应该...]
```

## 示例

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
CSVPreviewDialog → main_window.ui_entry.entry_import_csv()
→ schedule_core.schedule_import_csv()
→ molecule_csv.molecule_csv_import()
→ atom_csv_read()
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
