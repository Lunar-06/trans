#!/usr/bin/env python3
"""
测试数据库连接和配置
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

print("=== 数据库配置 ===")
print(f"用户: {DB_USER}")
print(f"主机: {DB_HOST}")
print(f"端口: {DB_PORT}")
print(f"数据库: {DB_NAME}")

# 测试连接
print("\n=== 尝试连接 MySQL ===")
try:
    import pymysql
    
    conn = pymysql.connect(
        host=DB_HOST,
        port=int(DB_PORT),
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset='utf8mb4'
    )
    print("✅ 连接成功！")
    
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print(f"MySQL 版本: {version[0]}")
    
    conn.close()
    print("\n🎉 数据库连接测试通过！现在可以启动后端了！")
    
except Exception as e:
    print(f"\n❌ 连接失败: {e}")
    print("\n请检查:")
    print("1. MySQL 服务是否已启动")
    print("2. 数据库 'wenyilu' 是否已创建")

