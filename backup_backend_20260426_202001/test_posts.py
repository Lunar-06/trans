import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db
from models import User, Post
from auth import get_password_hash

# 测试数据库配置
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# 创建测试数据库表
Base.metadata.create_all(bind=test_engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestPosts:
    def setup_method(self):
        """每个测试方法前执行"""
        # 清空测试数据库
        Base.metadata.drop_all(bind=test_engine)
        Base.metadata.create_all(bind=test_engine)
        
        # 创建测试用户
        db = TestingSessionLocal()
        hashed_password = get_password_hash("password123")
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=hashed_password
        )
        db.add(user)
        db.commit()
        db.close()

    def get_auth_token(self):
        """获取认证令牌"""
        response = client.post("/api/auth/login", json={
            "username": "testuser",
            "password": "password123"
        })
        return response.json()["access_token"]

    def test_create_post_success(self):
        """测试创建帖子成功"""
        token = self.get_auth_token()
        
        response = client.post("/api/posts/", 
            json={
                "title": "测试帖子标题",
                "content": "这是测试帖子内容",
                "category": "travel",
                "images": ["image1.jpg", "image2.jpg"]
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "测试帖子标题"
        assert data["content"] == "这是测试帖子内容"
        assert data["category"] == "travel"
        assert data["images"] == ["image1.jpg", "image2.jpg"]
        assert data["author"]["username"] == "testuser"

    def test_create_post_without_auth(self):
        """测试未认证用户创建帖子失败"""
        response = client.post("/api/posts/", 
            json={
                "title": "测试帖子标题",
                "content": "这是测试帖子内容"
            }
        )
        
        assert response.status_code == 403  # 未认证

    def test_create_post_empty_title(self):
        """测试创建空标题帖子失败"""
        token = self.get_auth_token()
        
        response = client.post("/api/posts/", 
            json={
                "title": "",
                "content": "这是测试帖子内容"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 400
        assert "帖子标题不能为空" in response.json()["detail"]

    def test_create_post_empty_content(self):
        """测试创建空内容帖子失败"""
        token = self.get_auth_token()
        
        response = client.post("/api/posts/", 
            json={
                "title": "测试帖子标题",
                "content": ""
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 400
        assert "帖子内容不能为空" in response.json()["detail"]

    def test_get_posts_list(self):
        """测试获取帖子列表"""
        # 先创建几个测试帖子
        token = self.get_auth_token()
        
        for i in range(3):
            client.post("/api/posts/", 
                json={
                    "title": f"测试帖子 {i}",
                    "content": f"这是测试帖子内容 {i}",
                    "category": "travel"
                },
                headers={"Authorization": f"Bearer {token}"}
            )
        
        # 获取帖子列表
        response = client.get("/api/posts/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert data[0]["title"] == "测试帖子 0"
        assert data[1]["title"] == "测试帖子 1"
        assert data[2]["title"] == "测试帖子 2"

    def test_get_single_post(self):
        """测试获取单个帖子"""
        token = self.get_auth_token()
        
        # 创建帖子
        create_response = client.post("/api/posts/", 
            json={
                "title": "测试帖子",
                "content": "这是测试帖子内容",
                "category": "travel"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        post_id = create_response.json()["id"]
        
        # 获取单个帖子
        response = client.get(f"/api/posts/{post_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == post_id
        assert data["title"] == "测试帖子"
        assert data["content"] == "这是测试帖子内容"

    def test_get_nonexistent_post(self):
        """测试获取不存在的帖子"""
        response = client.get("/api/posts/999")
        
        assert response.status_code == 404
        assert "帖子不存在" in response.json()["detail"]

    def test_like_post(self):
        """测试点赞帖子"""
        token = self.get_auth_token()
        
        # 创建帖子
        create_response = client.post("/api/posts/", 
            json={
                "title": "测试帖子",
                "content": "这是测试帖子内容"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        post_id = create_response.json()["id"]
        
        # 点赞帖子
        response = client.post(f"/api/posts/{post_id}/like",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "点赞成功"
        assert data["likes"] == 1

    def test_like_nonexistent_post(self):
        """测试点赞不存在的帖子"""
        token = self.get_auth_token()
        
        response = client.post("/api/posts/999/like",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 404
        assert "帖子不存在" in response.json()["detail"]

    def test_add_comment(self):
        """测试添加评论（简化实现）"""
        token = self.get_auth_token()
        
        # 创建帖子
        create_response = client.post("/api/posts/", 
            json={
                "title": "测试帖子",
                "content": "这是测试帖子内容"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        post_id = create_response.json()["id"]
        
        # 添加评论
        response = client.post(f"/api/posts/{post_id}/comments",
            json={"content": "测试评论"},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "评论功能待完善"

    def test_posts_rate_limiting(self):
        """测试帖子相关接口限流"""
        token = self.get_auth_token()
        
        # 快速发送多个创建帖子请求
        for i in range(11):
            response = client.post("/api/posts/", 
                json={
                    "title": f"测试帖子 {i}",
                    "content": f"这是测试帖子内容 {i}"
                },
                headers={"Authorization": f"Bearer {token}"}
            )
        
        # 第11个请求应该被限流
        assert response.status_code == 429

if __name__ == "__main__":
    pytest.main([__file__])