#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""翔鹭钨业早盘走势图生成脚本"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os

# 确保输出目录存在
output_dir = "/root/.openclaw/workspace/images"
os.makedirs(output_dir, exist_ok=True)

# 翔鹭钨业 (002842) 近期股价数据
data = [
    ("2026-01-20", 20.94),
    ("2026-01-21", 22.60),
    ("2026-01-22", 21.78),
    ("2026-01-23", 22.28),
    ("2026-01-26", 24.51),
    ("2026-01-27", 26.22),
    ("2026-01-28", 28.84),
    ("2026-01-29", 27.84),
    ("2026-01-30", 26.12),
    ("2026-02-02", 27.10),
    ("2026-02-03", 27.06),
    ("2026-02-04", 26.80),
    ("2026-02-05", 25.87),
    ("2026-02-06", 28.46),
    ("2026-02-09", 30.20),
    ("2026-02-10", 31.83),
    ("2026-02-11", 35.01),
    ("2026-02-12", 38.51),
    ("2026-02-13", 36.38),
    ("2026-02-24", 35.85),
    ("2026-02-25", 37.50),
    ("2026-02-26", 37.78),
    ("2026-02-27", 41.56),
    ("2026-03-02", 45.72),
    ("2026-03-03", 43.68),
    ("2026-03-04", 46.05),
    ("2026-03-05", 41.82),
    ("2026-03-06", 43.01),
    ("2026-03-09", 41.39),
    ("2026-03-10", 41.39),
]

# 解析日期和价格
dates = [datetime.strptime(d, "%Y-%m-%d") for d, _ in data]
prices = [p for _, p in data]

# 创建图表
fig, ax = plt.subplots(figsize=(12, 6))

# 绘制股价线
ax.plot(dates, prices, linewidth=2, color='#d62728', marker='o', markersize=4)

# 填充区域
ax.fill_between(dates, prices, alpha=0.3, color='#d62728')

# 设置标题和标签
ax.set_title('翔鹭钨业 (002842.SZ) 近期股价走势', fontsize=14, fontweight='bold')
ax.set_xlabel('日期', fontsize=12)
ax.set_ylabel('股价 (元)', fontsize=12)

# 设置 x 轴日期格式
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
plt.xticks(rotation=45)

# 添加网格
ax.grid(True, alpha=0.3)

# 添加当前价格标注
current_price = prices[-1]
current_date = dates[-1]
ax.annotate(f'最新：{current_price}元', 
            xy=(current_date, current_price),
            xytext=(current_date, current_price + 2),
            fontsize=10,
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

# 调整布局
plt.tight_layout()

# 保存图片
output_path = os.path.join(output_dir, "xianglu_002842_chart.png")
plt.savefig(output_path, dpi=150, bbox_inches='tight')
plt.close()

print(f"图表已保存至：{output_path}")
