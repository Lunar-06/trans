# 文旅电商平台后端API

基于FastAPI框架的后端系统，为文旅电商平台提供用户认证和帖子管理功能。

## 功能特性

- 🔐 **JWT身份认证** - 安全的用户登录和注册
- 📝 **帖子管理** - 创建、查看、点赞帖子
- 🛡️ **安全防护** - 密码哈希、请求限流、CORS策略
- 📊 **自动文档** - FastAPI自动生成API文档
- 🧪 **完整测试** - 单元测试覆盖核心功能

## 技术栈

- **框架**: FastAPI 0.104.1
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **ORM**: SQLAlchemy 2.0
- **认证**: JWT + bcrypt
- **测试**: pytest

## 快速开始

### 1. 环境要求

- Python 3.8+
- pip 包管理器

### 2. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 3. 配置环境

复制环境变量文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，修改JWT密钥等配置。

### 4. 启动服务

```bash
# 开发模式（自动重载）
python main.py

# 或使用uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

服务将在 `http://localhost:8000` 启动。

## API文档

启动服务后访问：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 核心API接口

### 认证接口

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/auth/register` | 用户注册 |
| POST | `/api/auth/login` | 用户登录 |
| GET | `/api/auth/me` | 获取当前用户信息 |
| POST | `/api/auth/logout` | 用户登出 |

### 帖子接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/posts/` | 获取帖子列表 |
| POST | `/api/posts/` | 创建新帖子 |
| GET | `/api/posts/{id}` | 获取单个帖子 |
| POST | `/api/posts/{id}/like` | 点赞帖子 |
| POST | `/api/posts/{id}/comments` | 添加评论 |

## 数据库模型

### User (用户)
- id: 主键
- username: 用户名 (唯一)
- email: 邮箱 (唯一)
- hashed_password: 密码哈希
- avatar: 头像表情
- is_active: 是否激活
- created_at: 创建时间

### Post (帖子)
- id: 主键
- title: 标题
- content: 内容
- category: 分类
- images: 图片URL列表
- author_id: 作者ID
- likes: 点赞数
- created_at: 创建时间

## 安全特性

### 密码安全
- 使用bcrypt进行密码哈希
- 禁止明文存储密码

### JWT认证
- 令牌有效期30分钟
- 自动令牌验证
- 安全的密钥管理

### 请求限流
- 注册: 5次/分钟
- 登录: 10次/分钟
- 发帖: 10次/分钟
- 其他: 30次/分钟

### CORS策略
- 允许前端域名访问
- 支持凭证传输

## 测试

运行所有测试：

```bash
# 运行认证测试
python test_auth.py

# 运行帖子测试
python test_posts.py

# 使用pytest运行所有测试
pytest
```

## 部署

### 生产环境配置

1. 修改JWT密钥
2. 配置生产数据库
3. 设置环境变量
4. 使用生产级服务器 (uvicorn + gunicorn)

### Docker部署

```dockerfile
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 开发指南

### 代码结构

```
backend/
├── main.py              # 应用入口
├── database.py          # 数据库配置
├── models.py           # 数据模型
├── schemas.py          # Pydantic模型
├── auth.py             # 认证逻辑
├── routers/            # 路由模块
│   ├── auth.py         # 认证路由
│   └── posts.py        # 帖子路由
├── test_auth.py        # 认证测试
├── test_posts.py       # 帖子测试
├── requirements.txt    # 依赖列表
└── README.md          # 项目文档
```

### 添加新功能

1. 在 `models.py` 中添加数据模型
2. 在 `schemas.py` 中添加Pydantic模型
3. 在 `routers/` 中创建新路由文件
4. 在 `main.py` 中注册路由
5. 编写单元测试

## 故障排除

### 常见问题

1. **端口占用**: 修改端口或停止占用进程
2. **数据库连接失败**: 检查数据库配置
3. **JWT验证失败**: 检查密钥配置
4. **CORS错误**: 检查前端域名配置

### 日志查看

启用SQL日志：
```python
# 在 database.py 中设置 echo=True
engine = create_engine(..., echo=True)
```

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

MIT License