<template>
  <div class="sub-page">
    <div class="container">
      <header class="sub-header"><h1>设置中心</h1></header>
      <section class="setting-list">
        <article v-for="s in settings" :key="s" class="setting-item">
          <span>{{ s }}</span>
          <span class="arrow">›</span>
        </article>
      </section>
    </div>
  </div>
</template>

<script setup>
const settings = ['账号安全', '隐私设置', '通知设置', '通用设置', '清理缓存']
</script>

<style scoped>
.sub-page { padding: 20px 0 36px; }
.sub-header h1 { font-size: 32px; color: var(--color-auxiliary); margin-bottom: 16px; }
.setting-list { display: flex; flex-direction: column; gap: 10px; }
.setting-item { display: flex; align-items: center; justify-content: space-between; padding: 14px 12px; border: 1px solid var(--color-border); border-radius: var(--radius-md); background: #fffaf2; }
.arrow { color: var(--color-text-light); font-size: 20px; }
</style>
