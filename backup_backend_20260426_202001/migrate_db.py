"""
数据库迁移脚本 - 为 posts 表添加 is_public 列
"""
import sys
import os

# 确保可以导入后端模块
sys.path.insert(0, '')

from database import engine
from sqlalchemy import text

def migrate_database():
    """执行数据库迁移"""
    print("=" * 50)
    print("文旅电商平台 - 数据库迁移")
    print("=" * 50)
    
    try:
        # 连接数据库
        with engine.connect() as conn:
            # 检查 is_public 列是否已存在
            result = conn.execute(text("PRAGMA table_info(posts)"))
            columns = [row[1] for row in result.fetchall()]
            
            if 'is_public' in columns:
                print("✓ is_public 列已存在，跳过迁移")
                return
            
            print("正在为 posts 表添加 is_public 列...")
            
            # 添加 is_public 列，默认值为 True (1)
            conn.execute(text("ALTER TABLE posts ADD COLUMN is_public BOOLEAN DEFAULT 1"))
            conn.commit()
            
            print("✓ 迁移成功！is_public 列已添加")
            print("✓ 所有现有帖子默认为公开可见")
            
    except Exception as e:
        print(f"✗ 迁移失败: {e}")
        raise

if __name__ == "__main__":
    migrate_database()
    print("\n完成!")
