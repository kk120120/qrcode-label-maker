---
name: "modify_feature"
description: "Locates issue layer and modifies only that layer to fix bugs/features. Invoke when user asks to modify existing functionality."
---

# Modify Existing Feature

先定位问题层级，再只修改对应层级，保持架构完整性。

## 适用场景
- 修改现有功能
- 修复 bug
- 优化代码
- 调整业务流程

## 执行步骤（必须完整执行所有5个步骤，不得跳过任何步骤）

### 第一步：定位问题
1. 阅读 `mypolicy/project_rules.md` 理解项目架构
2. 使用问题定位速查表确定需要修改哪个层级
3. 找到相关文件

**问题定位速查表**：
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

### 第二步：分析调用链
1. 从UI层开始，追踪调用链
2. 理解当前的实现方式
3. 确定需要修改的具体位置

**调用链格式**：
```
UI层 → entry_ui.py (L1) → schedule_core.py (L2) → molecule_xxx.py (L3) → atom_xxx.py (L4)
```

### 第三步：只修改对应层级（此步骤必须执行）
1. 严格遵守分层规则，只修改问题所在层级
2. 不要跨层修改
3. 不要破坏现有调用链
4. 必须先询问用户确认修改方案

**各层级职责**：
- **L1 入口层**：接收用户事件，转发给 L2
- **L2 调度层**：协调分子执行顺序，不写业务逻辑
- **L3 分子层**：编排原子操作，不调用其他分子
- **L4 原子层**：纯函数操作，无副作用

### 第四步：验证修改
1. 检查是否违反分层规则
2. 检查 PEP8 规范
3. 测试功能是否正常
4. 检查是否影响其他功能

**分层检查清单**：
- [ ] 未跨层调用（只修改了问题所在层级）
- [ ] 未反向调用（L3 → L2 → L1 是禁止的）
- [ ] 未分子调用分子
- [ ] 未原子调用原子

### 第五步：更新文档（此步骤必须执行）
1. 必须更新 `new_design.md` 记录变更
2. 添加版本变更记录
3. 更新 app_info.py 中的版本号

## 规则
- 必须完整执行所有5个步骤，特别是第3步和第5步
- 严格遵守分层依赖：L1 → L2 → L3 → L4
- 禁止反向调用
- 禁止跨层直接调用
- 禁止分子调用分子
- 禁止原子调用原子
- 只修改问题所在层级，不扩大修改范围
- 修改前必须确认用户需求
- 修改后必须更新文档

## 示例

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

**是否确认修改？**
```
