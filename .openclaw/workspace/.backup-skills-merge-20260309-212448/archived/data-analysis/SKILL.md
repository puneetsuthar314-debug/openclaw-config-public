---
name: data-analysis
description: "Analyze structured data, create visualizations, and generate insights. Supports CSV, Excel, JSON, and database data. Use when user needs data analysis, charts, statistics, or data processing. Triggers: analyze data, 分析数据, make chart, 画图表, statistics, 统计, visualize, 可视化, process CSV, process Excel"
allowed-tools: Bash, Computer, Write, Read
---

# Data Analysis — 数据分析与可视化

## 核心能力
使用 pandas + matplotlib + openpyxl 进行数据分析和可视化。

## 支持的数据格式

| 格式 | 读取方式 |
|------|----------|
| CSV | `pd.read_csv('file.csv')` |
| Excel | `pd.read_excel('file.xlsx')` |
| JSON | `pd.read_json('file.json')` |
| HTML 表格 | `pd.read_html('url')` |
| SQL | `pd.read_sql(query, conn)` |

## 标准工作流

```bash
python3.12 << 'PYEOF'
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 无头模式
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']  # 中文支持
plt.rcParams['axes.unicode_minus'] = False

# 1. 读取数据
df = pd.read_csv('/path/to/data.csv')  # 或 read_excel

# 2. 基础统计
print("=== 数据概览 ===")
print(f"行数: {len(df)}, 列数: {len(df.columns)}")
print(f"列名: {list(df.columns)}")
print(df.describe())

# 3. 可视化
fig, ax = plt.subplots(figsize=(10, 6))
# ... 根据数据类型选择图表
plt.tight_layout()
plt.savefig('/root/.openclaw/workspace/files/charts/analysis.png', dpi=150)
print("Chart saved!")

# 4. 导出结果
df_result.to_excel('/root/.openclaw/workspace/files/data/result.xlsx', index=False)
PYEOF
```

## 环境说明
- Python: `python3.12`（/root/anaconda3/bin/python）
- 已安装: pandas, numpy, matplotlib, openpyxl, lxml
