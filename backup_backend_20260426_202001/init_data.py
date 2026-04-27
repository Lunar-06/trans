"""
初始化模拟数据到数据库
"""
import sys
import json
from datetime import datetime, timedelta
from passlib.context import CryptContext
import os

# 确保可以导入后端模块
sys.path.insert(0, '')

# 临时禁用 SQL 日志以避免编码问题
os.environ['PYTHONIOENCODING'] = 'utf-8'

from database import SessionLocal, engine, Base
from models import User, Post, Comment

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 模拟数据（从前端提取）
MOCK_USERS = [
    {
        "username": "旅行爱好者",
        "email": "travel@example.com",
        "password": "123456",
        "avatar": "🧑"
    },
    {
        "username": "美食家",
        "email": "food@example.com",
        "password": "123456",
        "avatar": "🍔"
    },
    {
        "username": "文化爱好者",
        "email": "culture@example.com",
        "password": "123456",
        "avatar": "🎨"
    },
    {
        "username": "历史迷",
        "email": "history@example.com",
        "password": "123456",
        "avatar": "📚"
    },
    {
        "username": "旅游达人",
        "email": "expert@example.com",
        "password": "123456",
        "avatar": "👩"
    },
    {
        "username": "小吃货",
        "email": "snack@example.com",
        "password": "123456",
        "avatar": "🍟"
    },
    {
        "username": "黄石人",
        "email": "local@example.com",
        "password": "123456",
        "avatar": "🏠"
    }
]

MOCK_POSTS = [
    {
        "title": "黄石西塞山一日游攻略",
        "content": "上周去了黄石西塞山，风景真的很美！特别是望江亭，可以俯瞰整个长江。建议早上9点出发，中午在山上野餐，下午可以去附近的磁湖散步。门票只要20元，非常值得一去！",
        "category": "travel",
        "author_username": "旅行爱好者",
        "likes": 12,
        "is_liked": False,
        "images": [
            "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=Huangshi%20Xisai%20Mountain%20scenic%20view%20with%20Yangtze%20River%20in%20background&image_size=landscape_16_9",
            "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=望江亭%20on%20Xisai%20Mountain%20with%20panoramic%20view&image_size=landscape_16_9"
        ],
        "hours_ago": 2,
        "comments": [
            {
                "username": "旅游达人",
                "avatar": "👩",
                "content": "我也去过，确实很美！推荐大家去看看桃花洞。",
                "hours_ago": 1
            }
        ]
    },
    {
        "title": "黄石港饼真的太好吃了！",
        "content": "在购物平台买了黄石港饼，真的太好吃了！酥脆香甜，甜而不腻。包装也很精美，送朋友很合适。强烈推荐大家试试！",
        "category": "shopping",
        "author_username": "美食家",
        "likes": 28,
        "is_liked": True,
        "images": [
            "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=Huangshi%20gang%20cake%20traditional%20pastry&image_size=square"
        ],
        "hours_ago": 5,
        "comments": [
            {
                "username": "小吃货",
                "avatar": "🍟",
                "content": "我也买了，确实不错！",
                "hours_ago": 4
            },
            {
                "username": "黄石人",
                "avatar": "🏠",
                "content": "作为黄石人，港饼是我们的骄傲！",
                "hours_ago": 3
            }
        ]
    },
    {
        "title": "阳新布贴手工艺品推荐",
        "content": "在阳新旅游时买了一些布贴手工艺品，做工非常精细，色彩鲜艳。听当地艺人介绍，这是国家级非物质文化遗产，每一件都是手工制作的，非常有收藏价值。",
        "category": "shopping",
        "author_username": "文化爱好者",
        "likes": 15,
        "is_liked": False,
        "images": [
            "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=Yangxin%20cloth%20patchwork%20handicraft%20traditional%20art&image_size=square"
        ],
        "hours_ago": 24,
        "comments": []
    },
    {
        "title": "大冶铁矿国家矿山公园游记",
        "content": "大冶铁矿国家矿山公园真的很震撼！可以看到巨大的露天采矿坑，还有博物馆展示矿冶历史。适合带孩子来学习工业历史，门票60元，值得一游。",
        "category": "travel",
        "author_username": "历史迷",
        "likes": 9,
        "is_liked": False,
        "images": [
            "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=Daye%20Iron%20Mine%20National%20Mining%20Park%20open%20pit&image_size=landscape_16_9"
        ],
        "hours_ago": 48,
        "comments": []
    }
]


def init_data():
    """初始化模拟数据到数据库"""
    # 临时禁用 SQL 日志
    from sqlalchemy import event
    old_echo = engine.echo
    engine.echo = False
    
    # 创建数据库表（如果不存在）
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("正在检查数据库中是否已有数据...")
        
        # 检查是否已有用户
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"数据库中已有 {existing_users} 个用户，跳过初始化。")
            print("如果想要重新初始化，请先删除数据库文件 wenyilu.db")
            return
        
        print("开始初始化模拟数据...")
        
        # 1. 创建用户
        user_map = {}  # username -> User 对象
        for user_data in MOCK_USERS:
            hashed_password = pwd_context.hash(user_data["password"])
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=hashed_password,
                avatar=user_data["avatar"],
                is_active=True
            )
            db.add(user)
            db.flush()  # 获取 id
            user_map[user.username] = user
            print(f"  [OK] 创建用户: {user.username}")
        
        db.commit()
        print(f"[OK] 成功创建 {len(user_map)} 个用户")
        
        # 2. 创建帖子和评论
        post_count = 0
        comment_count = 0
        
        for post_data in MOCK_POSTS:
            # 找到作者
            author = user_map.get(post_data["author_username"])
            if not author:
                print(f"  [ERROR] 找不到用户: {post_data['author_username']}")
                continue
            
            # 计算创建时间
            created_at = datetime.now() - timedelta(hours=post_data["hours_ago"])
            
            # 创建帖子
            post = Post(
                title=post_data["title"],
                content=post_data["content"],
                category=post_data["category"],
                images=json.dumps(post_data["images"], ensure_ascii=False),
                author_id=author.id,
                likes=post_data["likes"],
                is_liked=post_data["is_liked"],
                is_public=True,  # 默认公开
                created_at=created_at,
                updated_at=created_at
            )
            db.add(post)
            db.flush()  # 获取 id
            post_count += 1
            print(f"  [OK] 创建帖子: {post.title}")
            
            # 创建评论
            for comment_data in post_data["comments"]:
                # 找到评论用户
                comment_user = user_map.get(comment_data["username"])
                if not comment_user:
                    # 如果找不到，创建一个临时用户或使用第一个用户
                    comment_user = author
                
                comment_created_at = datetime.now() - timedelta(hours=comment_data["hours_ago"])
                comment = Comment(
                    content=comment_data["content"],
                    post_id=post.id,
                    user_id=comment_user.id,
                    username=comment_data["username"],
                    avatar=comment_data["avatar"],
                    created_at=comment_created_at
                )
                db.add(comment)
                comment_count += 1
                print(f"    [OK] 创建评论: {comment.username}")
        
        db.commit()
        print(f"\n[OK] 成功初始化数据!")
        print(f"  - 用户: {len(user_map)} 个")
        print(f"  - 帖子: {post_count} 个")
        print(f"  - 评论: {comment_count} 个")
        
        print("\n测试账号（密码都是 123456）:")
        for user_data in MOCK_USERS:
            print(f"  - 用户名: {user_data['username']}")
        
    except Exception as e:
        print(f"[ERROR] 初始化失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()
        engine.echo = old_echo


if __name__ == "__main__":
    print("=" * 50)
    print("文旅电商平台 - 数据初始化脚本")
    print("=" * 50)
    init_data()
    print("\n完成!")
