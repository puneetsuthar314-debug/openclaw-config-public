# Excel 技能学习笔记

_学习日期：2026-03-09 08:05_  
_优先级：🔴 高（仅次于 content-writer）_  
_变现方式：数据分析/报表制作_

---

## 📚 核心知识点

### 1. 库选择原则
| 库 | 用途 |
|---|---|
| **pandas** | 数据分析、批量操作、简单导出 |
| **openpyxl** | 复杂格式、公式、Excel 特有功能 |

### 2. 关键陷阱（必须记住！）

#### ❌ 错误：Python 计算后硬编码
```python
# 错！这样 Excel 就失去动态性了
total = df['Sales'].sum()
sheet['B10'] = total  # 写死 5000
```

#### ✅ 正确：使用 Excel 公式
```python
# 对！让 Excel 自己计算
sheet['B10'] = '=SUM(B2:B9)'
```

### 3. 公式 recalculaiton（强制步骤）
openpyxl 创建的公式只是字符串，需要用 LibreOffice 重新计算：
```bash
python scripts/recalc.py output.xlsx
```

### 4. 金融建模标准

#### 颜色编码
| 颜色 | 用途 |
|------|------|
| 蓝色 | 硬编码输入/假设 |
| 黑色 | 所有公式 |
| 绿色 | 链接到其他工作表 |
| 红色 | 链接到其他文件 |
| 黄色背景 | 关键假设 |

#### 数字格式
- 年份：文本字符串 "2024"（不是"2,024"）
- 货币：`$#,##0` → $1,234
- 百分比：`0.0%` → 12.3%
- 负数：括号 (123) 不是 -123

### 5. 专业设计系统

#### 主题色系统（选一个）
| 主题 | 颜色 | 用途 |
|------|------|------|
| Elegant Black | #2D2D2D | 奢侈品/时尚/高端（推荐默认） |
| Corporate Blue | #1F4E79 | 金融/企业 |
| Forest Green | #2E5A4C | 环保/可持续 |

#### 布局规则
- 左边距：A 列留空（宽度 3）
- 上边距：第 1 行留空
- 内容起点：B2 单元格
- 章节间距：1 行空白
- 表格间距：2 行空白

#### 边框系统（仅水平风格）
- 外框：四边细线 #D1D1D1
- 表头底部：中等粗细，主题色
- 内部水平：细线，每行之间
- 内部垂直：**无**（更干净）

### 6. Excel 基础常识

| 知识点 | 说明 |
|--------|------|
| 日期存储 | 序列号（1900-01-01 以来的天数） |
| 1900 闰年 bug | Excel 错误地把 1900 当闰年 |
| 精度限制 | 超过 15 位的数字会截断（用 TEXT 格式） |
| 合并单元格 | 只有左上角单元格有值 |
| 最大行数 | XLSX: 1,048,576 行 |

---

## 🛠️ 代码模板

### 读取 Excel
```python
import pandas as pd
from openpyxl import load_workbook

# pandas（数据分析）
df = pd.read_excel('file.xlsx')

# openpyxl（保留公式）
wb = load_workbook('file.xlsx')
```

### 创建专业 Excel
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

wb = Workbook()
ws = wb.active

# 留白边距
ws.row_dimensions[1].height = 15
ws.column_dimensions['A'].width = 3

# 标题（B2 开始）
ws['B2'] = '报告标题'
ws['B2'].font = Font(bold=True, size=18, color='2D2D2D')

# 表头
ws['B4'] = '项目'
ws['C4'] = '数值'
ws['B4'].font = Font(bold=True, color='FFFFFF')
ws['B4'].fill = PatternFill('solid', start_color='2D2D2D')

# 公式（关键！）
ws['C5'] = '=SUM(C6:C15)'

# 冻结窗格
ws.freeze_panes = 'B5'

# 自动筛选
ws.auto_filter.ref = 'B4:C100'

wb.save('output.xlsx')
```

---

## ✅ 交付前检查清单

- [ ] 所有数字单元格设置了 number_format
- [ ] 同一列精度一致
- [ ] 公式单元格有明确格式
- [ ] 数据来源和时间范围已记录
- [ ] 生成日期在页脚
- [ ] 无公式错误（#REF!, #DIV/0! 等）
- [ ] 用 LibreOffice 重新计算了公式

---

## 💰 变现思路

### 1. 企业报表自动化
- 财务月报/季报自动生成
- 销售数据可视化仪表板
- 预算 vs 实际对比分析

### 2. 数据分析服务
- 电商销售数据分析
- 用户行为数据整理
- 市场调研数据可视化

### 3. 模板销售
- 财务报表模板
- 项目管理模板
- 个人理财模板

### 4. 培训教程
- Excel 公式进阶教程
- 金融建模实战
- 数据可视化技巧

---

## 📈 下一步实践

1. **本周**：用 openpyxl 创建一个专业的财务分析报告
2. **下周**：开发一个自动化脚本，从 CSV 生成 Excel 报表
3. **本月**：掌握条件格式、数据验证、图表制作

---

_备注：这是根据 MEMORY.md 自我提升原则必须掌握的技能，优先级🔴高_
