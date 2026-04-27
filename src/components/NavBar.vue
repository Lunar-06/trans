<template>
  <header class="qunar-header">
    <!-- 顶部通栏 -->
    <div class="top-bar">
      <div class="container">
        <span>欢迎来到云语智行 · 黄石文旅服务平台</span>
      </div>
    </div>

    <!-- 主头部：Logo + 搜索 + 个人中心 -->
    <div class="header-main">
      <div class="container">
        <!-- 左侧Logo -->
        <router-link to="/" class="logo">
          <img src="../assets/logo.png" alt="云语智行" class="logo-image">
          <span class="logo-text">云语智行</span>
        </router-link>

        <!-- 中间搜索框 -->
        <div class="search-wrap">
          <input 
            type="text" 
            class="search-input" 
            placeholder="搜索景点、方言、特产、民俗..."
          />
          <button class="search-btn">搜索</button>
        </div>

        <!-- 右侧个人中心/登录注册 -->
        <div class="user-area">
          <template v-if="isLoggedIn">
            <router-link to="/my" class="user-link">
              <span>个人中心</span>
            </router-link>
          </template>
          <template v-else>
            <router-link to="/my" class="user-link">
              <span>登录/注册</span>
            </router-link>
          </template>
        </div>
      </div>
    </div>

    <!-- 主导航栏（点击高亮） -->
    <nav class="main-nav">
      <div class="container">
        <router-link to="/" class="nav-item" active-class="active">首页</router-link>
        <router-link to="/translate" class="nav-item" active-class="active">方言翻译</router-link>
        <router-link to="/shop" class="nav-item" active-class="active">购物</router-link>
        <router-link to="/stories" class="nav-item" active-class="active">民俗</router-link>
        <router-link to="/community" class="nav-item" active-class="active">社区</router-link>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const isLoggedIn = ref(false)
const router = useRouter()
const route = useRoute()

// 检查登录状态
const checkLoginStatus = () => {
  const token = localStorage.getItem('token')
  isLoggedIn.value = !!token
}

// 监听路由变化，检查登录状态
watch(() => route.path, () => {
  checkLoginStatus()
})

onMounted(() => {
  checkLoginStatus()
})
</script>

<style scoped>
/* 基础重置与版心 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Microsoft YaHei", Arial, sans-serif;
}
.container {
  width: 1000px;
  margin: 0 auto;
}

/* 顶部浅灰通栏 */
.top-bar {
  height: 30px;
  line-height: 30px;
  background: #f7f7f7;
  border-bottom: 1px solid #eee;
  font-size: 12px;
  color: #666;
}

/* 主头部区域 */
.header-main {
  height: 70px;
  background: #fff;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
}
.header-main .container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
}

.logo-image {
  height: 60px;
  width: auto;
}

.logo-text {
  font-size: 26px;
  font-family: '思源宋体 CN', 'Source Han Serif CN', serif;
  font-weight: 700;
  color: #8B4513;
}

/* 搜索框 */
.search-wrap {
  width: 480px;
  height: 38px;
  border: 2px solid #8B4513;
  border-radius: 4px;
  display: flex;
  overflow: hidden;
}
.search-input {
  flex: 1;
  border: none;
  outline: none;
  padding: 0 12px;
  font-size: 14px;
  color: #333;
}
.search-btn {
  width: 90px;
  background: #8B4513;
  color: #fff;
  border: none;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
}

/* 右侧个人中心 */
.user-area {
  font-size: 14px;
}
.user-link {
  color: #333;
  text-decoration: none;
}
.user-link:hover {
  color: #8B4513;
}

/* 主导航栏 */
.main-nav {
  height: 42px;
  background: #8B4513;
}
.main-nav .container {
  display: flex;
  height: 100%;
}

/* 导航项 */
.nav-item {
  padding: 0 24px;
  line-height: 42px;
  color: #fff;
  font-size: 15px;
  text-decoration: none;
  transition: background 0.2s;
}

/* 点击高亮 + 悬浮高亮 */
.nav-item:hover,
.nav-item.active {
  background: #6d3710;
  color: #fff;
  font-weight: bold;
}
</style>