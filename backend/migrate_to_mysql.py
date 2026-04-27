"""
从 SQLite 迁移到 MySQL 的脚本
使用方法: python migrate_to_mysql.py
"""
import sqlite3
import pymysql
from datetime import datetime

def migrate_sqlite_to_mysql(sqlite_db_path, mysql_config):
    """
    将 SQLite 数据库迁移到 MySQL
    
    Args:
        sqlite_db_path: SQLite 数据库文件路径
        mysql_config: MySQL 连接配置字典
    """
    print("开始从 SQLite 迁移到 MySQL...")
    
    # 连接 SQLite
    sqlite_conn = sqlite3.connect(sqlite_db_path)
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cursor = sqlite_conn.cursor()
    
    # 连接 MySQL
    mysql_conn = pymysql.connect(**mysql_config)
    mysql_cursor = mysql_conn.cursor()
    
    try:
        # 1. 迁移 users 表
        print("\n迁移 users 表...")
        sqlite_cursor.execute("SELECT * FROM users")
        users = sqlite_cursor.fetchall()
        
        for user in users:
            mysql_cursor.execute("""
                INSERT INTO users (id, username, email, hashed_password, avatar, is_active, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                user['id'],
                user['username'],
                user['email'],
                user['hashed_password'],
                user['avatar'],
                bool(user['is_active']),
                user['created_at'],
                user['updated_at']
            ))
        print(f"  迁移了 {len(users)} 条用户记录")
        
        # 2. 迁移 posts 表
        print("\n迁移 posts 表...")
        sqlite_cursor.execute("SELECT * FROM posts")
        posts = sqlite_cursor.fetchall()
        
        for post in posts:
            mysql_cursor.execute("""
                INSERT INTO posts (id, title, content, category, images, author_id, likes, is_liked, is_public, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                post['id'],
                post['title'],
                post['content'],
                post['category'],
                post['images'],
                post['author_id'],
                post['likes'],
                bool(post['is_liked']),
                bool(post['is_public']),
                post['created_at'],
                post['updated_at']
            ))
        print(f"  迁移了 {len(posts)} 条帖子记录")
        
        # 3. 迁移 comments 表
        print("\n迁移 comments 表...")
        sqlite_cursor.execute("SELECT * FROM comments")
        comments = sqlite_cursor.fetchall()
        
        for comment in comments:
            mysql_cursor.execute("""
                INSERT INTO comments (id, content, post_id, user_id, username, avatar, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                comment['id'],
                comment['content'],
                comment['post_id'],
                comment['user_id'],
                comment['username'],
                comment['avatar'],
                comment['created_at']
            ))
        print(f"  迁移了 {len(comments)} 条评论记录")
        
        # 提交事务
        mysql_conn.commit()
        print("\n✅ 迁移完成！")
        
    except Exception as e:
        mysql_conn.rollback()
        print(f"\n❌ 迁移失败: {e}")
        raise
    finally:
        sqlite_conn.close()
        mysql_conn.close()

def create_mysql_database(mysql_config_without_db):
    """
    创建 MySQL 数据库（如果不存在）
    """
    db_name = mysql_config_without_db.pop('database')
    
    conn = pymysql.connect(**mysql_config_without_db)
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✅ 数据库 {db_name} 已创建或已存在")
    finally:
        conn.close()
    
    mysql_config_without_db['database'] = db_name
    return mysql_config_without_db

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    # 加载环境变量
    load_dotenv()
    
    # MySQL 配置
    mysql_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'wenyilu'),
        'charset': 'utf8mb4'
    }
    
    # SQLite 数据库路径
    sqlite_db_path = "wenyilu.db"
    
    if not os.path.exists(sqlite_db_path):
        print(f"❌ SQLite 数据库文件不存在: {sqlite_db_path}")
        print("   如果是新安装，可以直接启动后端，会自动创建 MySQL 表结构")
    else:
        # 第一步：创建数据库
        print("\n=== 步骤 1: 创建 MySQL 数据库 ===")
        mysql_config = create_mysql_database(mysql_config.copy())
        
        # 第二步：先启动后端让它创建表结构
        print("\n=== 步骤 2: 请先启动后端让它创建表结构 ===")
        print("   运行: python -m uvicorn main:app --reload")
        print("   然后按 Ctrl+C 停止，再运行此脚本进行数据迁移\n")
        
        print("或者，如果您已经创建了表结构，可以继续...")
        choice = input("是否继续迁移数据？(y/n): ").strip().lower()
        
        if choice == 'y':
            # 第三步：迁移数据
            migrate_sqlite_to_mysql(sqlite_db_path, mysql_config)
