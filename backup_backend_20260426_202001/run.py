#!/usr/bin/env python3
"""
文旅电商平台后端启动脚本
"""

import os
import sys
import uvicorn
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def main():
    """主启动函数"""
    # 检查环境变量
    jwt_secret = os.getenv("JWT_SECRET_KEY")
    if jwt_secret == "your-super-secret-jwt-key-change-in-production":
        print("⚠️  警告: 请修改 .env 文件中的 JWT_SECRET_KEY")
        print("   当前使用的是默认密钥，生产环境不安全！")
    
    # 启动服务器
    print("🚀 启动文旅电商平台后端服务...")
    print(f"📊 服务地址: http://localhost:8001")
    print(f"📖 API文档: http://localhost:8001/docs")
    print(f"🔧 重载模式: 启用")
    print("-" * 50)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,  # 改为8001端口避免冲突
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)