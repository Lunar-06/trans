import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db

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

class TestAuth:
    def setup_method(self):
        """每个测试方法前执行"""
        # 清空测试数据库
        Base.metadata.drop_all(bind=test_engine)
        Base.metadata.create_all(bind=test_engine)

    def test_register_success(self):
        """测试用户注册成功"""
        response = client.post("/api/auth/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "avatar": "🧑"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["username"] == "testuser"
        assert data["user"]["email"] == "test@example.com"

    def test_register_duplicate_username(self):
        """测试重复用户名注册失败"""
        # 第一次注册
        client.post("/api/auth/register", json={
            "username": "testuser",
            "email": "test1@example.com",
            "password": "password123"
        })
        
        # 第二次注册相同用户名
        response = client.post("/api/auth/register", json={
            "username": "testuser",
            "email": "test2@example.com",
            "password": "password123"
        })
        
        assert response.status_code == 400
        assert "用户名已存在" in response.json()["detail"]

    def test_register_duplicate_email(self):
        """测试重复邮箱注册失败"""
        # 第一次注册
        client.post("/api/auth/register", json={
            "username": "testuser1",
            "email": "test@example.com",
            "password": "password123"
        })
        
        # 第二次注册相同邮箱
        response = client.post("/api/auth/register", json={
            "username": "testuser2",
            "email": "test@example.com",
            "password": "password123"
        })
        
        assert response.status_code == 400
        assert "邮箱已被注册" in response.json()["detail"]

    def test_register_weak_password(self):
        """测试弱密码注册失败"""
        response = client.post("/api/auth/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "123"  # 密码太短
        })
        
        assert response.status_code == 422  # Pydantic验证错误

    def test_login_success(self):
        """测试登录成功"""
        # 先注册用户
        client.post("/api/auth/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        })
        
        # 登录
        response = client.post("/api/auth/login", json={
            "username": "testuser",
            "password": "password123"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self):
        """测试错误密码登录失败"""
        # 先注册用户
        client.post("/api/auth/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        })
        
        # 使用错误密码登录
        response = client.post("/api/auth/login", json={
            "username": "testuser",
            "password": "wrongpassword"
        })
        
        assert response.status_code == 401
        assert "用户名或密码错误" in response.json()["detail"]

    def test_login_nonexistent_user(self):
        """测试不存在的用户登录失败"""
        response = client.post("/api/auth/login", json={
            "username": "nonexistent",
            "password": "password123"
        })
        
        assert response.status_code == 401
        assert "用户名或密码错误" in response.json()["detail"]

    def test_get_current_user_with_valid_token(self):
        """测试使用有效令牌获取用户信息"""
        # 注册并登录获取令牌
        register_response = client.post("/api/auth/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        })
        
        token = register_response.json()["access_token"]
        
        # 使用令牌获取用户信息
        response = client.get("/api/auth/me", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"

    def test_get_current_user_with_invalid_token(self):
        """测试使用无效令牌获取用户信息失败"""
        response = client.get("/api/auth/me", headers={
            "Authorization": "Bearer invalid_token"
        })
        
        assert response.status_code == 401
        assert "无效的认证令牌" in response.json()["detail"]

    def test_rate_limiting(self):
        """测试限流功能"""
        # 快速发送多个请求
        for _ in range(6):
            response = client.post("/api/auth/register", json={
                "username": f"user{_}",
                "email": f"user{_}@example.com",
                "password": "password123"
            })
        
        # 第6个请求应该被限流
        assert response.status_code == 429

if __name__ == "__main__":
    pytest.main([__file__])