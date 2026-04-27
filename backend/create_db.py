#!/usr/bin/env python3
"""
创建 MySQL 数据库
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

# 读取配置
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "wenyilu")

print("=== 创建数据库 ===")
print(f"用户: {DB_USER}")
print(f"主机: {DB_HOST}")
print(f"端口: {DB_PORT}")
print(f"数据库: {DB_NAME}")

try:
    import pymysql
    
    # 先连接到 MySQL (不指定数据库)
    print("\n正在连接 MySQL...")
    conn = pymysql.connect(
        host=DB_HOST,
        port=int(DB_PORT),
        user=DB_USER,
        password=DB_PASSWORD,
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    
    # 创建数据库
    print(f"\n正在创建数据库 '{DB_NAME}'...")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print("✅ 数据库创建成功！")
    
    # 验证
    cursor.execute("SHOW DATABASES")
    databases = [d[0] for d in cursor.fetchall()]
    if DB_NAME in databases:
        print(f"✅ 数据库 '{DB_NAME}' 已存在或创建成功！")
    else:
        print(f"❌ 数据库 '{DB_NAME}' 创建失败")
    
    conn.close()
    print("\n🎉 完成！现在可以运行 test_db.py 测试连接了！")
    
except Exception as e:
    print(f"\n❌ 操作失败: {e}")
