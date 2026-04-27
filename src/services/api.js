// API服务层

// 基础API URL
const API_BASE_URL = '/api';  // 使用Vite代理配置，自动转发到后端端口8001

// 获取存储的token
const getToken = () => localStorage.getItem('token');

// 通用请求函数
async function request(endpoint, options = {}) {
  try {
    const token = getToken();
    
    // 设置请求超时（10秒）
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000);
    
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : '',
        ...options.headers
      }
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      // 处理FastAPI返回的错误格式（detail可能是字符串或数组）
      let errorMsg;
      if (typeof errorData.detail === 'string') {
        errorMsg = errorData.detail;
      } else if (Array.isArray(errorData.detail)) {
        errorMsg = errorData.detail.map(e => e.msg || JSON.stringify(e)).join('; ');
      } else if (errorData.detail) {
        errorMsg = JSON.stringify(errorData.detail);
      } else {
        errorMsg = `HTTP error! status: ${response.status}`;
      }
      throw new Error(errorMsg);
    }

    return await response.json();
  } catch (error) {
    console.error('API request failed:', error);
    
    // 提供更友好的错误信息
    if (error.name === 'AbortError') {
      throw new Error('请求超时，请检查网络连接');
    } else if (error.message.includes('Failed to fetch')) {
      throw new Error('无法连接到服务器，请检查网络连接');
    }
    
    throw error;
  }
}

// 加密函数（前端模拟）
const encryptData = (data) => {
  // 这里只是简单的Base64编码，实际项目中应该使用更安全的加密方式
  return btoa(JSON.stringify(data));
};

// 解密函数（前端模拟）
const decryptData = (encryptedData) => {
  try {
    return JSON.parse(atob(encryptedData));
  } catch (error) {
    console.error('Decryption failed:', error);
    return null;
  }
};

// 帖子相关API
export const postApi = {
  // 获取帖子列表
  async getPosts() {
    return request('/posts/');
  },

  // 创建新帖子
  async createPost(postData) {
    return request('/posts/', {
      method: 'POST',
      body: JSON.stringify(postData)
    });
  },

  // 点赞帖子
  async likePost(postId) {
    return request(`/posts/${postId}/like`, {
      method: 'POST'
    });
  },

  // 添加评论
  async addComment(postId, commentData) {
    return request(`/posts/${postId}/comments`, {
      method: 'POST',
      body: JSON.stringify(commentData)
    });
  }
};

// 用户相关API
export const userApi = {
  // 登录
  async login(credentials) {
    // 直接发送原始密码，后端会进行哈希处理
    const response = await request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials)
    });
    // 存储token（后端返回字段是 access_token）
    const token = response.access_token || response.token;
    if (token) {
      localStorage.setItem('token', token);
      localStorage.setItem('user', JSON.stringify(response.user));
    }
    return response;
  },

  // 注册
  async register(userData) {
    // 直接发送原始密码，后端会进行哈希处理
    const response = await request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData)
    });
    // 存储token（后端返回字段是 access_token）
    const token = response.access_token || response.token;
    if (token) {
      localStorage.setItem('token', token);
      localStorage.setItem('user', JSON.stringify(response.user));
    }
    return response;
  },

  // 获取用户基本信息
  async getUserInfo() {
    return request('/user/profile');
  },

  // 获取用户真实统计数据
  async getUserStats() {
    return request('/user/stats');
  },

  // 更新用户设置
  async updateSettings(settings) {
    return request('/user/settings', {
      method: 'PUT',
      body: JSON.stringify(settings)
    });
  },

  // 退出登录
  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('theme'); // 清除主题设置
  }
};

// 模拟数据（当后端API不可用时使用）
export const mockData = {
  posts: [
    {
      id: 1,
      title: '黄石西塞山一日游攻略',
      content: '上周去了黄石西塞山，风景真的很美！特别是望江亭，可以俯瞰整个长江。建议早上9点出发，中午在山上野餐，下午可以去附近的磁湖散步。门票只要20元，非常值得一去！',
      category: 'travel',
      username: '旅行爱好者',
      userAvatar: '🧑',
      time: '2小时前',
      likes: 12,
      isLiked: false,
      images: [
        'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=Huangshi%20Xisai%20Mountain%20scenic%20view%20with%20Yangtze%20River%20in%20background&image_size=landscape_16_9',
        'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=望江亭%20on%20Xisai%20Mountain%20with%20panoramic%20view&image_size=landscape_16_9'
      ],
      comments: [
        {
          username: '旅游达人',
          avatar: '👩',
          content: '我也去过，确实很美！推荐大家去看看桃花洞。',
          time: '1小时前'
        }
      ],
      showComments: false
    },
    {
      id: 2,
      title: '黄石港饼真的太好吃了！',
      content: '在购物平台买了黄石港饼，真的太好吃了！酥脆香甜，甜而不腻。包装也很精美，送朋友很合适。强烈推荐大家试试！',
      category: 'shopping',
      username: '美食家',
      userAvatar: '🍔',
      time: '5小时前',
      likes: 28,
      isLiked: true,
      images: [
        'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=Huangshi%20gang%20cake%20traditional%20pastry&image_size=square'
      ],
      comments: [
        {
          username: '小吃货',
          avatar: '🍟',
          content: '我也买了，确实不错！',
          time: '4小时前'
        },
        {
          username: '黄石人',
          avatar: '🏠',
          content: '作为黄石人，港饼是我们的骄傲！',
          time: '3小时前'
        }
      ],
      showComments: false
    },
    {
      id: 3,
      title: '阳新布贴手工艺品推荐',
      content: '在阳新旅游时买了一些布贴手工艺品，做工非常精细，色彩鲜艳。听当地艺人介绍，这是国家级非物质文化遗产，每一件都是手工制作的，非常有收藏价值。',
      category: 'shopping',
      username: '文化爱好者',
      userAvatar: '🎨',
      time: '1天前',
      likes: 15,
      isLiked: false,
      images: [
        'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=Yangxin%20cloth%20patchwork%20handicraft%20traditional%20art&image_size=square'
      ],
      comments: [],
      showComments: false
    },
    {
      id: 4,
      title: '大冶铁矿国家矿山公园游记',
      content: '大冶铁矿国家矿山公园真的很震撼！可以看到巨大的露天采矿坑，还有博物馆展示矿冶历史。适合带孩子来学习工业历史，门票60元，值得一游。',
      category: 'travel',
      username: '历史迷',
      userAvatar: '📚',
      time: '2天前',
      likes: 9,
      isLiked: false,
      images: [
        'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=Daye%20Iron%20Mine%20National%20Mining%20Park%20open%20pit&image_size=landscape_16_9'
      ],
      comments: [],
      showComments: false
    }
  ]
};