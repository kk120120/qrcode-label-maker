---
name: "add_new_feature"
description: "Implements new features following 4-layer architecture (L1→L2→L3→L4). Invoke when user asks to add new functionality."
---

# Add New Feature

按照四层架构标准流程，从原子层到UI层逐步实现新功能。

## 适用场景
- 添加全新的功能模块
- 创建新的组件或窗口
- 实现新的业务流程

## 执行步骤（必须完整执行所有7个步骤，不得跳过任何步骤）

### 第一步：分析架构
1. 阅读 `mypolicy/project_rules.md` 理解四层架构
2. 阅读 `new_design.md` 了解项目设计
3. 确定需要修改/新增哪些层级

### 第二步：实现原子层（L4）
1. 在 `atom/` 目录下创建/修改对应的原子文件
2. 每个原子只做一件事
3. 使用纯函数，无副作用
4. 添加完整的类型注解
5. 添加 Google 风格文档字符串

**原子函数命名**：`atom_模块_动作()`

### 第三步：实现分子层（L3）
1. 在 `molecule/` 目录下创建/修改对应的分子文件
2. 分子只编排原子，不调用其他分子
3. 添加完整的类型注解
4. 添加 Google 风格文档字符串

**分子方法命名**：`molecule_业务_动作()`

### 第四步：实现调度层（L2）
1. 在 `schedule/schedule_core.py` 中添加调度方法
2. 调度方法只调用分子，不写业务逻辑
3. 添加完整的类型注解
4. 添加 Google 风格文档字符串

**调度方法命名**：`schedule_事件名称()`

### 第五步：实现入口层（L1）
1. 在 `entry/entry_ui.py` 中添加入口方法
2. 入口方法只转发给调度层
3. 添加完整的类型注解
4. 添加 Google 风格文档字符串

**入口方法命名**：`entry_功能_动作()`

### 第六步：实现UI层（如果需要）
1. 在 `entry/ui_window/` 下创建/修改UI组件
2. UI组件只通过 `entry_ui.py` 与业务层交互
3. 禁止直接调用分子层或原子层
4. 添加完整的类型注解
5. 添加 Google 风格文档字符串
6. 添加文件头注释，标注 L1 层级

### 第七步：验证（此步骤必须执行）
1. 检查是否违反分层规则
2. 检查 PEP8 规范
3. 验证功能是否正常
4. 必须更新 `new_design.md` 记录变更

## 规则
- 必须完整执行所有7个步骤，特别是第7步
- 严格遵守分层依赖：L1 → L2 → L3 → L4
- 禁止反向调用
- 禁止跨层调用
- 禁止分子调用分子
- 禁止原子调用原子
- 函数不超过 100 行
- 所有函数必须有类型注解
- 所有函数必须有文档字符串
- 完成后必须更新 `new_design.md`

## 四层架构示例

```
L4 原子层：纯函数
def atom_qr_calculate_capacity(version: str, error_level: str) -> tuple:
    """原子：计算二维码容量"""
    return capacities.get((version, error_level), (0, 0, 0, 0))

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

## 示例

**输入**：
```
请帮我添加新功能：批量导出功能
```

**输出**：
```
层级分析：需要修改 L3 分子层和 L2 调度层
实现步骤：
1. atom/atom_file.py - 添加文件导出原子函数
2. molecule/molecule_file.py - 添加批量导出分子方法
3. schedule/schedule_core.py - 添加调度方法
4. entry/entry_ui.py - 添加入口方法
5. entry/ui_window/main_window.py - 添加UI入口
```
