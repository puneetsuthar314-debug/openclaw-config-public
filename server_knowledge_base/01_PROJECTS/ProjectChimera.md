> **核心洞察**：这是一个**正在积极开发中**的 AI 游戏项目。它的后端服务以开发模式运行，依赖一个庞大但脆弱的 Anaconda 环境，并且缺少规范的依赖管理。操作时需格外小心，**首要任务是为其生成 `requirements.txt`**。

# 01 - 项目：ProjectChimera
**最后更新**: `2026-03-25`

## 1. 设计背景与决策 (The "Why")
- **AI 驱动**: 项目的核心是探索 AI 在游戏 NPC 行为和世界动态中的应用。因此，后端服务包含了大量与 LLM、向量数据库 (FAISS) 和事件驱动逻辑相关的代码。
- **开发模式优先**: 后端服务使用 `--reload` 标志启动，是为了方便开发者快速迭代。这也意味着它**不是生产状态**，任何文件变动都可能触发服务重启，且性能和稳定性较低。
- **单体 Python 环境**: 项目直接依赖 Anaconda 的 `base` 环境，可能是为了快速启动项目。这是一个技术债，理想情况下应有独立的项目环境。

## 2. 操作风险与雷区 (The "Gotchas")
| 风险点 | 描述与后果 |
|---|---|
| **启动目录** | 后端启动命令**必须在 `/root` 目录下执行**。这是因为代码内部可能使用了相对路径来解析模块，在其他位置启动会导致 `ModuleNotFoundError`。 |
| **僵尸进程** | 启动后会产生一个僵尸进程。**可以安全地忽略它**。这不影响服务功能，但反映了父进程未正确处理子进程退出信号，是一个待修复的 bug。 |
| **数据库文件** | `chimera.db` 包含了所有游戏的核心数据。**绝对不能手动删除或修改**，除非你知道你在做什么。 |
| **游戏存档** | `backend/data/saves/` 目录下的 `.json` 文件是玩家的游戏存档。删除它们将导致玩家进度丢失。 |
| **FAISS 索引** | `faiss_index/` 目录下的 `.index` 文件是 NPC 记忆的向量索引。如果损坏，NPC 的记忆和对话能力会受损，但可以通过重新运行索引构建脚本来恢复。 |

## 3. 故障排查指南 (The "How-To")
- **如果服务无法启动**: 
  1.  **检查启动目录**：确认你是否在 `/root` 目录下执行的命令。
  2.  **检查 Anaconda 环境**：确认 `python3` 指向的是 `/root/anaconda3/bin/python3`。
  3.  **检查日志**：查看 `/tmp/chimera_backend.log` 中的具体错误信息。
- **如果 NPC 对话异常**:
  1.  **检查 API 密钥**：确认 `/config/.env` 中的 `OPENAI_API_KEY` 是否有效。
  2.  **检查 FAISS 索引**：查看索引文件是否存在且可读。

## 4. 关键操作：使用工具箱脚本
- **安全重启服务**: 不要手动执行 `kill` 和 `uvicorn` 命令。请使用工具箱中的脚本：
  ```bash
  /root/scripts/restart_chimera_backend.sh
  ```
- **运行测试**: 
  ```bash
  cd /root/ProjectChimera && pytest
  ```

## 5. [高优先级] 待办事项：生成依赖文件
在进行任何其他开发工作之前，请务必为项目生成 `requirements.txt` 文件。
```bash
# 激活环境
source /root/anaconda3/bin/activate base
# 进入后端目录
cd /root/ProjectChimera/backend
# 生成依赖文件
pip freeze > requirements.txt
```
