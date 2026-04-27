<template>
  <div class="home">
    <section class="hero">
      <div class="hero-slides">
        <div
          class="hero-slide"
          v-for="(img, index) in slides"
          :key="index"
          :class="{ active: index === current }"
          :style="{ backgroundImage: `url(${img})` }"
        ></div>
      </div>

      <div class="hero-overlay">
        <div class="container hero-container">
          <div class="hero-content">
            <h1 class="hero-title">寻黄石文脉，阅本土风华</h1>
            <p class="hero-subtitle">
              黄石的乡音与故事，不该只留在回忆里。
              「云语智行」以方言为桥，
              带你听见黄石、读懂黄石、爱上黄石。
              从方言翻译到文创好物，从民俗风情到在地生活，
              我们陪你一起，留住乡音，传承文脉。
            </p>
            <div class="hero-actions">
              <router-link to="/translate" class="btn btn-primary">方言翻译</router-link>
              <router-link to="/shop" class="btn btn-secondary">逛文创特产</router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="features-scroll">
      <div class="container">
        <h2 class="section-title">核心功能</h2>
        <div class="feature-track">
          <article class="feature-card" @click="goTo('/translate')">
            <h3>方言翻译</h3>
            <p>语音与文本双输入，快速识别并输出黄石方言表达。</p>
          </article>
          <article class="feature-card" @click="goTo('/shop')">
            <h3>文创特产</h3>
            <p>黄石地域精选好物，统一陈列、快速浏览、便捷下单。</p>
          </article>
          <article class="feature-card" @click="goTo('/stories')">
            <h3>民俗文化</h3>
            <p>聚合历史故事、非遗技艺与节庆民俗，内容沉浸式呈现。</p>
          </article>
          <article class="feature-card" @click="goTo('/community')">
            <h3>社区精选</h3>
            <p>精选用户图文与讨论热点，形成高质量本地文化社区。</p>
          </article>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
const goTo = (path) => router.push(path)
// 轮播图
import { ref, onMounted, onUnmounted } from 'vue'
const slides = ref([
  new URL('../assets/1.png', import.meta.url).href,
  new URL('../assets/2.png', import.meta.url).href,
  new URL('../assets/3.png', import.meta.url).href,
  new URL('../assets/4.png', import.meta.url).href,
  new URL('../assets/5.png', import.meta.url).href,
  new URL('../assets/6.png', import.meta.url).href
])
const current = ref(0)
let timer = null

const start = () => {
  timer = setInterval(() => {
    current.value = (current.value + 1) % slides.value.length
  }, 3000)
}
const stop = () => clearInterval(timer)

onMounted(start)
onUnmounted(stop)
</script>

<style scoped>
/* 轮播图新增样式 */
.hero-slides {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}
.hero-slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-position: center;
  background-size: cover;
  opacity: 0;
  transition: opacity 1.2s ease;
}
.hero-slide.active {
  opacity: 1;
}
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.home {
  overflow-x: hidden;
}

/* 英雄区背景 */
.hero {
  width: 100%;
  min-height: 90vh;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

/* 👇 核心：半透明蒙版（伪元素） */
.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.35); /* 黑蒙版 35% 透明度 */
  z-index: 1;
}

/* 👇 内容要在蒙版之上（z-index:2） */
.hero-overlay {
  position: relative;
  z-index: 2;
  width: 100%;
  height: 100%;
}

.hero-content {
  color: #fff;
  max-width: 800px;
  padding: 0 20px;
  text-shadow: 0 1px 4px rgba(0,0,0,0.3);
}

.hero-title {
  font-size: 62px;
  font-weight: 800;
  margin-bottom: 34px;
  line-height: 1.3;
  color: #fff;
  text-shadow: 0 2px 8px rgba(0,0,0,0.35);
}

.hero-subtitle {
  font-size: 18px;
  line-height: 1.8;
  margin-bottom: 36px;
  color: #fff;
}

.hero-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 14px 36px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  transition: 0.3s;
  cursor: pointer;
  text-decoration: none;
}

.btn-primary {
  background: #fff;
  color: #222;
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

.btn-secondary {
  background: transparent;
  color: #fff;
  border: 1px solid #fff;
}

.btn-secondary:hover {
  background: rgba(255,255,255,0.15);
}

.section-title {
  font-size: 32px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 40px;
  color: #222;
}

.features-scroll {
  padding: 70px 0;
}

.feature-track {
  display: flex;
  gap: 24px;
  overflow-x: auto;
  padding-bottom: 10px;
}

.feature-card {
  min-width: 270px;
  background: #fff;
  padding: 30px 24px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  transition: 0.3s;
  cursor: pointer;
}

.feature-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.08);
}

.feature-card h3 {
  font-size: 22px;
  margin-bottom: 12px;
}

.feature-card p {
  font-size: 15px;
  color: #666;
  line-height: 1.7;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 34px;
  }
  .hero-actions {
    flex-direction: column;
    align-items: center;
  }
}
</style>