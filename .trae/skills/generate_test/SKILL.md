---
name: "generate_test"
description: "Generates unit tests for atom (L4) and molecule (L3) layers. Invoke when user asks to generate tests."
---

# Generate Test Cases

根据现有代码自动生成单元测试用例，重点测试原子层和分子层。

## 适用场景
- 为原子层函数生成单元测试
- 为分子层方法生成单元测试
- 测试驱动开发（TDD）
- 回归测试用例生成

## 执行步骤（必须完整执行所有5个步骤，不得跳过任何步骤）

### 第一步：分析被测代码
1. 确定是原子层还是分子层
2. 分析函数的输入输出
3. 确定测试边界条件

**测试分层**：
| 层级 | 测试重点 | 测试文件位置 |
|-----|---------|-------------|
| L4 原子层 | 纯函数逻辑 | `tests/test_atom/` |
| L3 分子层 | 业务编排逻辑 | `tests/test_molecule/` |

### 第二步：创建测试文件
1. 创建 `tests/` 目录（如果不存在）
2. 创建 `tests/test_atom/` 或 `tests/test_molecule/` 目录
3. 文件命名：`test_[原文件名].py`

### 第三步：编写测试用例

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
    input_data = ...
    expected_result = ...

    # Act - 执行被测函数
    actual_result = function_under_test(input_data)

    # Assert - 验证结果
    assert actual_result == expected_result
```

### 第四步：处理依赖
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

### 第五步：运行测试（此步骤必须执行）
1. 运行单个测试文件
2. 运行所有测试
3. 修复失败的测试
4. 必须更新 `new_design.md` 记录变更

## 规则
- 必须完整执行所有5个步骤，特别是第5步
- 使用 pytest 框架
- 每个测试函数测试一个功能点
- 测试函数命名：`test_[功能描述]`
- 必须有类型注解和文档字符串
- 使用 Arrange-Act-Assert 模式
- 原子层测试不 mock
- 分子层测试可 mock 原子函数
- 完成后必须更新 `new_design.md`

## 测试用例模板

### 原子层测试模板
```python
"""
L4 原子层测试 - [模块名] 测试
"""
import pytest
from atom.atom_[module] import (
    atom_[function1],
    atom_[function2]
)


class TestAtom[Module]:
    """[模块]原子测试"""

    def test_atom_[function1](self):
        """测试：[函数功能]"""
        # Arrange
        ...

        # Act
        result = atom_[function1](...)

        # Assert
        assert result == expected
```

### 分子层测试模板
```python
"""
L3 分子层测试 - [管理器名] 测试
"""
import pytest
from unittest.mock import patch
from molecule.molecule_[module] import [ManagerClass]


class Test[ManagerClass]:
    """[管理器]分子测试"""

    @patch('molecule.molecule_[module].atom_[function]')
    def test_molecule_[function](self, mock_function):
        """测试：[方法功能]"""
        # Arrange
        mock_function.return_value = ...

        # Act
        manager = [ManagerClass]()
        result = manager.molecule_[function](...)

        # Assert
        assert result == expected
        mock_function.assert_called_once()
```

## 示例

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

**是否确认生成？**
```
