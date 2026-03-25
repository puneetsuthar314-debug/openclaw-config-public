# 编码规范相关教训

## 2026-03-09: Python 版本路径修复
**问题**：系统默认 python3 是 3.6.8，太老了，导致 image_search.py 和 enhanced_search.py 都报错。
**修复**：统一使用 Conda Python `/root/anaconda3/bin/python3`（3.12.7），修改了所有脚本 shebang。
**教训**：所有 Python 脚本必须用 `/root/anaconda3/bin/python3` 运行，不要用系统 python3。
