#!/root/anaconda3/bin/python3
"""
自动备份工作区配置
每天执行一次，备份到 /root/.openclaw/backups/
保留最近 7 天的备份
"""

import os
import shutil
import tarfile
from datetime import datetime, timedelta

WORKSPACE = "/root/.openclaw/workspace"
BACKUP_DIR = "/root/.openclaw/backups"
RETENTION_DAYS = 7

def create_backup():
    """创建备份"""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"workspace_{timestamp}.tar.gz")
    
    # 创建工作区备份
    with tarfile.open(backup_file, "w:gz") as tar:
        tar.add(WORKSPACE, arcname="workspace")
    
    print(f"✓ 备份已创建：{backup_file}")
    return backup_file

def cleanup_old_backups():
    """清理旧备份"""
    cutoff = datetime.now() - timedelta(days=RETENTION_DAYS)
    
    for filename in os.listdir(BACKUP_DIR):
        if not filename.startswith("workspace_"):
            continue
        
        filepath = os.path.join(BACKUP_DIR, filename)
        # 从文件名解析日期
        try:
            date_str = filename.replace("workspace_", "").replace(".tar.gz", "")
            file_date = datetime.strptime(date_str, "%Y%m%d_%H%M%S")
            
            if file_date < cutoff:
                os.remove(filepath)
                print(f"✓ 已删除旧备份：{filename}")
        except Exception as e:
            print(f"⚠ 无法解析 {filename}: {e}")

def main():
    print("=" * 50)
    print("开始自动备份...")
    
    # 创建备份
    backup_file = create_backup()
    
    # 清理旧备份
    cleanup_old_backups()
    
    # 列出当前备份
    backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.startswith("workspace_")])
    print(f"\n当前备份 ({len(backups)} 个):")
    for b in backups[-5:]:  # 显示最近 5 个
        size = os.path.getsize(os.path.join(BACKUP_DIR, b)) / 1024 / 1024
        print(f"  {b} ({size:.2f} MB)")
    
    print("\n" + "=" * 50)
    print("备份完成！")

if __name__ == "__main__":
    main()
