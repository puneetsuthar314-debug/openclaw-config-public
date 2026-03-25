# TOOLS 详细使用手册

## aliyun_code_interpreter 远程沙箱警告
`aliyun_code_interpreter` 是在**阿里云远程沙箱**中执行代码，它的文件系统与本地服务器**完全隔离**：
- 在 code_interpreter 中下载/保存的文件**只存在于远程沙箱**，本地服务器上**不存在**
- **绝对禁止**用 code_interpreter 下载图片/文件后直接用 `[DING:IMAGE]` 发送——文件不在本地，必定失败
- 需要下载图片到本地：使用 `exec` 工具执行 `image_search.py`（`image-search-sender` 技能）
- 需要下载文件到本地：使用 `exec` 工具执行 `curl`/`wget`
- code_interpreter 适合：纯计算、数据分析、不需要本地文件落盘的场景

## 图片搜索规则（唯一权威定义）
当用户要求搜索并发送图片时，**必须且只能**使用 `image-search-sender` 技能中的 `image_search.py` 脚本：
```bash
/root/anaconda3/bin/python3 /usr/local/bin/image_search.py "关键词" --limit N --output /root/.openclaw/workspace/images --json
```

**绝对禁止**以下行为：
1. 禁止用 `curl`/`wget` 手动下载图片 URL（大量 URL 已失效，会下载到 HTML 错误页面）
2. 禁止用 `aliyun_code_interpreter` 下载图片（远程沙箱文件不在本地）
3. 禁止自己编写 Python 脚本搜索图片（image_search.py 已封装好所有搜索引擎和验证逻辑）
4. 禁止谎称"脚本不可用"而不去尝试执行（脚本已验证可用）

## 钉钉媒体标签规则（唯一权威定义）
发送图片和文件时使用以下标签，**直接写在回复文本中**：
- 图片：`[DING:IMAGE path="/root/.openclaw/workspace/images/xxx.jpg"]`
- 文件：`[DING:FILE path="/root/.openclaw/workspace/files/xxx.pdf"]`

### 必须遵守的规则
1. 标签必须直接出现在你的**回复文本**中，作为 assistant 角色的直接输出
2. 系统（monitor.js）会自动检测回复中的这些标签，将本地文件上传到钉钉并替换为真正的图片/文件消息
3. **严禁**通过 `message` 工具发送这些标签（会变成纯文本，不会被解析为图片）
4. **严禁**在 path 中使用远程 URL，只能用本地绝对路径
5. 不需要区分群聊和私聊，系统会自动路由到正确的会话

### 错误示例（绝对不要这样做）
```
message(target="manager20", message="[DING:IMAGE path=...]")  ← 错误！
```

## Python 环境说明
- 系统默认 `python3` 是 3.6.8，**所有脚本必须使用 `/root/anaconda3/bin/python3`（3.12.7）运行**
- 运行脚本命令格式：`/root/anaconda3/bin/python3 /usr/local/bin/脚本名.py`
- 禁止使用裸 `python3` 命令运行脚本，必须用完整的 conda 路径

## 信息搜索深度要求
- 搜索后不要只依赖摘要（snippet），应使用 `web_fetch` 深入阅读 2-3 篇重要文章
- 总结报告必须包含具体数据、来源引用、多角度分析

## 文件核实工具（任务完成前必用）

### 快速核实命令
**检查 outputs/ 目录是否有产出：**
```bash
ls -la /root/.openclaw/workspace/projects/项目名/outputs/
```

**检查文件是否有效（非空）：**
```bash
find /root/.openclaw/workspace/projects/项目名/outputs/ -type f -size +1k
```

**检查 PROJECT.md 状态：**
```bash
cat /root/.openclaw/workspace/projects/项目名/PROJECT.md
```

### 核实协议
**L2/L3 任务完成前，必须执行以下核实命令：**
1. `ls -la outputs/` — 确认交付物已生成
2. `cat PROJECT.md` — 确认状态与实际一致
3. 如有文件发送需求，确认 `[DING:FILE]` 标签已输出

**不执行核实 = 任务未完成。**
