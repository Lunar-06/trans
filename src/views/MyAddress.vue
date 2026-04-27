<template>
  <div class="sub-page">
    <div class="container">
      <header class="sub-header"><h1>地址管理</h1></header>
      <section class="address-list">
        <article v-for="a in addresses" :key="a.id" class="address-item">
          <div>
            <p class="name">{{ a.name }} {{ a.phone }}</p>
            <p class="detail">{{ a.detail }}</p>
          </div>
          <div class="ops">
            <button>编辑</button>
            <button>删除</button>
          </div>
        </article>
      </section>
      <button class="add-btn">新增地址</button>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.sub-page { padding: 20px 0 36px; }
.sub-header h1 { font-size: 32px; color: var(--color-auxiliary); margin-bottom: 16px; }
.address-list { display: flex; flex-direction: column; gap: 10px; margin-bottom: 18px; }
.address-item { display: flex; justify-content: space-between; gap: 12px; align-items: center; padding: 12px; border: 1px solid var(--color-border); border-radius: var(--radius-md); background: #fffaf2; }
.name { font-weight: 600; margin-bottom: 4px; }
.detail { color: var(--color-text-light); font-size: 13px; }
.ops { display: flex; gap: 8px; }
.ops button { padding: 6px 10px; border: 1px solid var(--color-border); border-radius: 8px; background: #fff; }
.add-btn { position: sticky; bottom: 12px; width: 100%; padding: 12px; border-radius: var(--radius-md); background: linear-gradient(135deg, var(--color-primary), var(--color-accent)); color: #fff; }
</style>
