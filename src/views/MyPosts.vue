<template>
  <div class="sub-page">
    <div class="container">
      <header class="sub-header">
        <h1>我的发布</h1>
      </header>
      <section class="waterfall">
        <article v-for="item in posts" :key="item.id" class="post-card">
          <img :src="item.image" :alt="item.title" />
          <div class="meta">
            <h3>{{ item.title }}</h3>
            <p>{{ item.time }}</p>
            <p>👍 {{ item.likes }} · 💬 {{ item.comments }}</p>
          </div>
        </article>
      </section>
    </div>
  </div>
</template>

<script>
</script>

<style scoped>
.sub-page { padding: 20px 0 36px; }
.sub-header h1 { font-size: 32px; color: var(--color-auxiliary); margin-bottom: 18px; }
.waterfall { column-count: 2; column-gap: 16px; }
.post-card { break-inside: avoid; margin-bottom: 16px; background: #fffaf2; border: 1px solid var(--color-border); border-radius: var(--radius-md); overflow: hidden; }
.post-card img { width: 100%; height: 180px; object-fit: cover; }
.meta { padding: 12px; }
.meta h3 { font-size: 16px; margin-bottom: 6px; }
.meta p { font-size: 13px; color: var(--color-text-light); margin-bottom: 4px; }
@media (max-width: 768px) { .waterfall { column-count: 1; } }
</style>
