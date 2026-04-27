<template>
  <div class="sub-page">
    <div class="container">
      <header class="sub-header"><h1>购物订单</h1></header>
      <section class="order-list">
        <article v-for="o in orders" :key="o.id" class="order-card">
          <img :src="o.image" alt="order" />
          <div class="order-meta">
            <p>订单编号：{{ o.id }}</p>
            <p>下单时间：{{ o.time }}</p>
            <p>状态：{{ o.status }}</p>
            <p class="price">总价：￥{{ o.price }}</p>
          </div>
        </article>
      </section>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.sub-page { padding: 20px 0 36px; }
.sub-header h1 { font-size: 32px; color: var(--color-auxiliary); margin-bottom: 16px; }
.order-list { display: flex; flex-direction: column; gap: 12px; }
.order-card { display: grid; grid-template-columns: 88px 1fr; gap: 12px; padding: 12px; background: #fffaf2; border: 1px solid var(--color-border); border-radius: var(--radius-md); }
.order-card img { width: 88px; height: 88px; object-fit: cover; border-radius: 10px; }
.order-meta p { margin-bottom: 4px; color: var(--color-text-light); font-size: 13px; }
.order-meta .price { color: var(--color-primary); font-weight: 700; }
</style>
