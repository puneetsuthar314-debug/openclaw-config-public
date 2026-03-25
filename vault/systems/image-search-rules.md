# 图片搜索与发送规则

当用户要求搜索/发送图片时，**必须且只能**执行以下命令：
```bash
/root/anaconda3/bin/python3 /usr/local/bin/image_search.py "关键词" --limit N --output /root/.openclaw/workspace/images --json
```
然后为每张下载成功的图片写一个 `[DING:IMAGE path="..."]` 标签。

**绝对禁止的行为（违反即失败）：**
1. **禁止** 用 `curl`/`wget` 手动下载图片 URL
2. **禁止** 用 `aliyun_code_interpreter` 下载图片（远程沙箱文件不在本地）
3. **禁止** 自己编写 Python 脚本搜索图片
4. **禁止** 不尝试就声称脚本不可用
