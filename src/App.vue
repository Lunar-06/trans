<template>
  <div id="app-container" class="app-shell">
    <NavBar />
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <FooterBar />
  </div>
</template>

<script setup>
import NavBar from './components/NavBar.vue'
import FooterBar from './components/FooterBar.vue'
import bgImage from './assets/背景图.png'

// 设置body背景图片
document.body.style.backgroundImage = `url(${bgImage})`
document.body.style.backgroundSize = 'cover'
document.body.style.backgroundPosition = 'center'
document.body.style.backgroundAttachment = 'fixed'
</script>

<style>
/* 全局样式 */
:root {
  /* 主色调 */
  --color-primary: #5d4037; /* 暖棕色 */
  --color-secondary: #f5e6c8; /* 浅米黄色 */
  --color-accent: #8d6e63; /* 浅褐色 */
  
  /* 辅助色 */
  --color-title: #2e7d32; /* 深绿色（标题） */
  --color-card: #ffffff; /* 白色（卡片） */
  
  /* 文本颜色 */
  --color-text: #5d4037; /* 主文本 */
  --color-text-light: #8d6e63; /* 次要文本 */
  
  /* 背景颜色 */
  --color-bg: #f9f5e9; /* 暖米白 */
  --color-bg-light: #f5e6c8; /* 浅米黄色 */
  
  /* 边框颜色 */
  --color-border: #d3c4a8; /* 浅褐色边框 */
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  background-color: var(--color-bg);
  background-image: url('./assets/背景图.png');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  color: var(--color-text);
  line-height: 1.6;
}

/* 标题样式 */
h1, h2, h3, h4, h5, h6 {
  color: var(--color-title);
  font-family: Arial, sans-serif;
  font-weight: 600;
  margin-bottom: 16px;
}

/* 链接样式 */
a {
  color: var(--color-primary);
  text-decoration: none;
  transition: color 0.3s ease;
}

a:hover {
  color: var(--color-accent);
}

/* 按钮样式 */
button {
  font-family: Arial, sans-serif;
  cursor: pointer;
}
</style>

<style scoped>
#app-container {
  min-height: 100vh;
  background-image: url('./assets/背景图.png') !important;
  background-size: cover !important;
  background-position: center !important;
  background-attachment: fixed !important;
  background-color: transparent !important;
}

.app-shell {
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding-top: 0;
  padding-bottom: 40px;
  background-color: rgba(249, 245, 233, 0.5);
}
</style>
