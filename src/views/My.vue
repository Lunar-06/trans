<template>
  <div class="my-page">
    <div class="container">
      <header class="page-header">
        <h1 class="page-title">个人中心</h1>
        <p class="page-desc">管理您的账户和设置</p>
      </header>

      <div class="user-section" v-if="!isLoggedIn">
        <div class="auth-card">
          <div class="auth-tabs">
            <button 
              class="tab-btn" 
              :class="{ active: activeTab === 'login' }" 
              @click="activeTab = 'login'"
            >
              登录
            </button>
            <button 
              class="tab-btn" 
              :class="{ active: activeTab === 'register' }" 
              @click="activeTab = 'register'"
            >
              注册
            </button>
          </div>

          <div class="auth-form" v-if="activeTab === 'login'">
            <div class="form-group">
              <label class="form-label">用户名</label>
              <input 
                type="text" 
                v-model="loginForm.username" 
                class="form-input" 
                placeholder="请输入用户名"
              />
            </div>
            <div class="form-group">
              <label class="form-label">密码</label>
              <input 
                type="password" 
                v-model="loginForm.password" 
                class="form-input" 
                placeholder="请输入密码"
              />
            </div>
            <button class="btn-submit" @click="handleLogin" :disabled="loading">
              {{ loading ? '登录中...' : '登录' }}
            </button>
          </div>

          <div class="auth-form" v-else>
            <div class="form-group">
              <label class="form-label">用户名</label>
              <input 
                type="text" 
                v-model="registerForm.username" 
                class="form-input" 
                placeholder="请输入用户名"
              />
            </div>
            <div class="form-group">
              <label class="form-label">密码</label>
              <input 
                type="password" 
                v-model="registerForm.password" 
                class="form-input" 
                placeholder="请输入密码"
              />
            </div>
            <div class="form-group">
              <label class="form-label">确认密码</label>
              <input 
                type="password" 
                v-model="registerForm.confirmPassword" 
                class="form-input" 
                placeholder="请确认密码"
              />
            </div>
            <button class="btn-submit" @click="handleRegister" :disabled="loading">
              {{ loading ? '注册中...' : '注册' }}
            </button>
          </div>
        </div>
      </div>

      <div class="user-section" v-else>
        <div class="profile-top-card">
          <div class="profile-row">
            <div class="avatar large">
              <span class="avatar-icon">🙋</span>
            </div>
            <div class="profile-info">
              <h3 class="username">{{ currentUser.username }}</h3>
              <p class="user-level">普通会员</p>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ userStats.orders }}</span>
              <span class="stat-label">订单数</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ userStats.points }}</span>
              <span class="stat-label">积分</span>
            </div>
            <button class="btn-logout" @click="handleLogout">退出</button>
          </div>
        </div>

        <div class="menu-card">
          <h3 class="card-title">功能菜单</h3>
          <div class="menu-grid">
            <button
              v-for="item in profileMenus"
              :key="item.key"
              class="menu-item"
              @click="goToMenu(item.path)"
            >
              <span class="menu-icon">{{ item.icon }}</span>
              <span class="menu-label">{{ item.label }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { userApi } from '../services/api.js'

const isLoggedIn = ref(false)
const router = useRouter()
const activeTab = ref('login')
const currentUser = ref({ username: '' })
const userStats = ref({ orders: 0, favorites: 0, points: 0 })
const profileMenus = [
  { key: 'posts', label: '我的发布', icon: '📝', path: '/my/posts' },
  { key: 'orders', label: '购物订单', icon: '📦', path: '/my/orders' },
  { key: 'address', label: '地址管理', icon: '📍', path: '/my/address' },
  { key: 'settings', label: '设置中心', icon: '⚙️', path: '/my/settings' },
  { key: 'service', label: '客服帮助', icon: '💬', path: '/my/help' }
]

const loginForm = ref({
  username: '',
  password: ''
})

const registerForm = ref({
  username: '',
  password: '',
  confirmPassword: ''
})

const loading = ref(false)
const error = ref(null)

onMounted(async () => {
  // 检查本地存储中的登录状态
  const user = localStorage.getItem('user')
  if (user) {
    isLoggedIn.value = true
    currentUser.value = JSON.parse(user)
    await loadUserStats()
  }
  
})

const handleLogin = async () => {
  if (!loginForm.value.username || !loginForm.value.password) {
    alert('请输入用户名和密码')
    return
  }
  
  loading.value = true
  error.value = null
  
  try {
    // 调用API登录
    const response = await userApi.login({
      username: loginForm.value.username,
      password: loginForm.value.password
    })
    
    isLoggedIn.value = true
    currentUser.value = response.user
    localStorage.setItem('user', JSON.stringify(response.user))
    localStorage.setItem('token', response.access_token || response.token)
    await loadUserStats()
    alert('登录成功')
    
    // 重置表单
    loginForm.value = {
      username: '',
      password: ''
    }
  } catch (err) {
    console.error('Login failed:', err)
    error.value = err.message || '登录失败，请检查用户名和密码'
    alert(error.value)
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  if (!registerForm.value.username || !registerForm.value.password) {
    alert('请输入用户名和密码')
    return
  }
  
  if (registerForm.value.password !== registerForm.value.confirmPassword) {
    alert('两次输入的密码不一致')
    return
  }
  
  loading.value = true
  error.value = null
  
  try {
    // 调用API注册
    const response = await userApi.register({
      username: registerForm.value.username,
      password: registerForm.value.password,
      email: `${registerForm.value.username}@example.com`
    })
    
    isLoggedIn.value = true
    currentUser.value = response.user
    localStorage.setItem('user', JSON.stringify(response.user))
    localStorage.setItem('token', response.access_token || response.token)
    await loadUserStats()
    alert('注册成功')
    
    // 重置表单
    registerForm.value = {
      username: '',
      password: '',
      confirmPassword: ''
    }
    activeTab.value = 'login'
  } catch (err) {
    console.error('Register failed:', err)
    error.value = err.message || '注册失败，请稍后再试'
    alert(error.value)
  } finally {
    loading.value = false
  }
}

const handleLogout = async () => {
  try {
    // 调用API退出登录
    await userApi.logout()
  } catch (err) {
    console.error('Logout failed:', err)
  } finally {
    // 清除本地存储
    localStorage.removeItem('user')
    localStorage.removeItem('token')
    isLoggedIn.value = false
    currentUser.value = { username: '' }
    userStats.value = { orders: 0, favorites: 0, points: 0 }
    alert('已退出登录')
  }
}

const goToMenu = (path) => {
  router.push(path)
}

const loadUserStats = async () => {
  loading.value = true
  error.value = null
  try {
    // 尝试从API获取用户统计数据
    const stats = await userApi.getUserStats()
    userStats.value = {
      orders: stats.orders_count || 0,
      favorites: stats.favorites_count || 0,
      points: stats.points || 0
    }
  } catch (err) {
    console.error('Failed to load user stats:', err)
    // 当API调用失败时，使用默认值
    userStats.value = {
      orders: 0,
      favorites: 0,
      points: 0
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.my-page {
  padding: 40px 0 80px;
}

.page-header {
  text-align: center;
  margin-bottom: 48px;
}

.page-title {
  font-family: var(--font-serif);
  font-size: 40px;
  font-weight: 700;
  color: var(--color-auxiliary);
  margin-bottom: 16px;
}

.page-desc {
  font-size: 18px;
  color: var(--color-text-light);
}

.user-section {
  margin-bottom: 32px;
}

.auth-card {
  background: var(--color-white);
  border-radius: var(--radius-lg);
  padding: 32px;
  box-shadow: var(--shadow-md);
  max-width: 400px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .auth-card {
    max-width: 90%;
    padding: 24px;
  }
}

.auth-tabs {
  display: flex;
  margin-bottom: 24px;
  border-bottom: 1px solid var(--color-border);
}

.tab-btn {
  flex: 1;
  padding: 12px;
  background: none;
  border: none;
  font-size: 16px;
  font-weight: 500;
  color: var(--color-text-light);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.tab-btn.active {
  color: var(--color-primary);
  border-bottom: 2px solid var(--color-primary);
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text);
}

.form-input {
  padding: 14px 16px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: 15px;
  transition: all var(--transition-fast);
}

.form-input:focus {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 2px rgba(139, 69, 19, 0.1);
}

.btn-submit {
  padding: 14px;
  background: var(--color-primary);
  color: var(--color-white);
  font-size: 16px;
  font-weight: 600;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  margin-top: 8px;
}

.btn-submit:hover {
  background: var(--color-accent);
  box-shadow: 0 4px 12px rgba(139, 69, 19, 0.2);
  transform: none;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-submit:disabled:hover {
  background: var(--color-primary);
  box-shadow: none;
  transform: none;
}

.profile-top-card {
  background: var(--color-white);
  border-radius: var(--radius-md);
  padding: 20px;
  box-shadow: var(--shadow-sm);
  margin-bottom: 24px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

@media (max-width: 768px) {
  .profile-top-card {
    max-width: 90%;
    padding: 16px;
  }
}

.profile-row {
  display: flex;
  align-items: center;
  gap: 18px;
  flex-wrap: wrap;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar.large {
  width: 72px;
  height: 72px;
}

.avatar-icon {
  font-size: 28px;
}

.profile-info {
  flex: 1;
}

.username {
  font-size: 24px;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 4px;
}

.user-level {
  font-size: 14px;
  color: var(--color-text-light);
}

.btn-logout {
  padding: 8px 14px;
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-size: 14px;
  color: var(--color-text);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-logout:hover {
  border-color: #E53935;
  color: #E53935;
}

.stat-item {
  text-align: center;
  min-width: 72px;
}

.stat-value {
  display: block;
  font-size: 24px;
  font-weight: 700;
  color: var(--color-primary);
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: var(--color-text-light);
}

.menu-card {
  background: var(--color-white);
  border-radius: var(--radius-md);
  padding: 24px;
  box-shadow: var(--shadow-md);
  margin-bottom: 32px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 24px;
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.menu-item {
  min-height: 94px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-background);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all var(--transition-fast);
}

.menu-item:hover {
  border-color: var(--color-accent);
  transform: translateY(-2px);
}

.menu-icon {
  font-size: 22px;
}

.menu-label {
  font-size: 14px;
  color: var(--color-text);
}

@media (max-width: 768px) {
  .profile-row {
    gap: 12px;
  }

  .username {
    font-size: 20px;
  }
}
</style>