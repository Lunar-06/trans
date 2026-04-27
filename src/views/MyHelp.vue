<template>
  <div class="sub-page">
    <div class="container">
      <header class="sub-header"><h1>客服帮助</h1></header>
      <section class="help-block">
        <h3>常见问题</h3>
        <details v-for="f in faqs" :key="f.q" class="faq-item">
          <summary>{{ f.q }}</summary>
          <p>{{ f.a }}</p>
        </details>
      </section>
      <section class="help-block">
        <h3>联系客服</h3>
        <button class="contact-btn">在线客服入口</button>
      </section>
    </div>
  </div>
</template>

<script setup>
const faqs = [
  { q: '订单多久发货？', a: '通常 24 小时内处理，节假日顺延。' },
  { q: '收藏内容如何删除？', a: '进入我的收藏，切换分类后可取消收藏。' },
  { q: '地址信息如何修改？', a: '在地址管理页点击编辑即可。' }
]
</script>

<style scoped>
.sub-page { padding: 20px 0 36px; }
.sub-header h1 { font-size: 32px; color: var(--color-auxiliary); margin-bottom: 16px; }
.help-block { background: #fffaf2; border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 14px; margin-bottom: 12px; }
.help-block h3 { margin-bottom: 10px; }
.faq-item { border-top: 1px solid var(--color-border); padding: 8px 0; }
.faq-item:first-of-type { border-top: none; }
summary { cursor: pointer; font-weight: 500; }
.faq-item p { margin-top: 6px; color: var(--color-text-light); font-size: 14px; }
.contact-btn { margin-top: 6px; padding: 10px 14px; border-radius: 10px; background: linear-gradient(135deg, var(--color-primary), var(--color-accent)); color: #fff; }
</style>
