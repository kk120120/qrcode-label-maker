---
name: "bug_fix"
description: "Analyzes project 4-layer architecture and locates issues. Invoke when user asks to analyze code or debug problems."
---

# Bug Fix

快速分析项目四层架构，定位问题所在层级，画出完整调用链。

## 适用场景
- 理解项目整体结构
- 定位 bug 或问题所在层级
- 分析功能调用链
- 接手新项目时的代码理解

## 执行步骤（必须完整执行所有7个步骤，不得跳过任何步骤）

### 第一步：阅读项目规则
1. 阅读 `mypolicy/project_rules.md` 了解四层架构规范
2. 阅读 `new_design.md` 了解项目具体设计

### 第二步：定位问题层级
根据问题现象判断问题所在层级：
- 按钮点击没反应 → L1 UI层 → `entry/ui_window/`
- 菜单功能异常 → L1 UI层 → `entry/ui_window/`
- 画布绘制问题 → L1 UI层 → `entry/ui_window/designer_canvas.py`
- 业务流程不对 → L2 调度层 → `schedule/schedule_core.py`
- 模板操作错误 → L3 分子层 → `molecule/molecule_template.py`
- 二维码生成失败 → L3 分子层 → `molecule/molecule_qr.py`
- 文件读写错误 → L4 原子层 → `atom/atom_file.py`
- 数据结构问题 → L4 原子层 → `atom/atom_template.py`

### 第三步：找到相关文件
1. 根据层级定位到具体文件
2. 读取关键代码段

### 第四步：分析调用链
从用户操作开始，追踪完整调用链：
```
UI层 → entry_ui.py (L1) → schedule_core.py (L2) → molecule_xxx.py (L3) → atom_xxx.py (L4)
```

### 第五步：给出分析报告
1. 问题可能的原因
2. 需要修改的层级和文件
3. 修改建议

### 第六步：执行代码修改（此步骤必须执行）
1. 严格遵守分层规则，只修改问题所在层级
2. 不要跨层修改
3. 按照分析报告进行代码修改

### 第七步：更新文档（此步骤必须执行）
1. 无论修改完成后，必须更新 `new_design.md` 记录变更
2. 添加版本变更记录

## 规则
- 必须完整执行所有7个步骤，特别是第6步和第7步
- 严格遵守四层架构：L1 → L2 → L3 → L4
- 禁止跨层调用
- 禁止分子调用分子
- 禁止原子调用原子
- 修改后必须更新文档

## 示例

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
