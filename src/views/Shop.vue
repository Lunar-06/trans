<template>
  <div class="shop-page">
    <div class="container">
      <header class="page-header">
        <h1 class="page-title">畅享购物</h1>
      </header>
      <br>
      <br>

      <!-- 改成穷游式布局：左侧分类栏 + 右侧商品区 -->
      <div class="shop-layout">
        <!-- 左侧分类导航（穷游式侧边栏） -->
        <aside class="sidebar">
          <nav class="category-nav">
            <button
              v-for="cat in categories"
              :key="cat.id"
              class="category-btn"
              :class="{ active: selectedCategory === cat.id }"
              @click="selectedCategory = cat.id"
            >
              <span class="cat-name">{{ cat.name }}</span>
            </button>
          </nav>
        </aside>

        <!-- 右侧商品主区域 -->
        <main class="product-main">
          <!-- 购物车悬浮按钮（穷游风格固定在右侧） -->
          <div class="cart-float" @click="showCart = true">
            <div class="cart-icon">🛒</div>
            <span class="cart-badge" v-if="cartStore.totalItems > 0">
              {{ cartStore.totalItems }}
            </span>
          </div>

          <!-- 商品瀑布流区域 -->
          <div class="products-section">
            <div class="products-grid">
              <div
                v-for="product in filteredProducts"
                :key="product.id"
                class="product-card"
                @click="showProductDetail(product)"
              >
                <div class="product-image">
                  <span class="product-tag" v-if="product.tag">{{ product.tag }}</span>
                    <img :src="product.image" alt="商品图片" style="max-width: 100%; max-height: 100%;">
                </div>
                <div class="product-info">
                  <h3 class="product-name">{{ product.name }}</h3>
                  <p class="product-origin">{{ product.origin }}</p>
                  <div class="product-bottom">
                    <span class="product-price">¥{{ product.price }}</span>
                    <button class="btn-add-cart" @click.stop="addToCart(product)">
                      加入购物车
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>

      <!-- 以下购物车、结算弹窗逻辑完全保留，无需修改 -->
      <transition name="slide">
        <div class="cart-sidebar" v-if="showCart">
          <div class="cart-header">
            <h3>购物车</h3>
            <button class="btn-close" @click="showCart = false">×</button>
          </div>

          <div class="cart-items" v-if="cartStore.items.length > 0">
            <div
              v-for="item in cartStore.items"
              :key="item.id"
              class="cart-item"
              @click="showProductDetailFromCart(item)"
            >
              <div class="item-icon">{{ item.icon }}</div>
              <div class="item-info">
                <h4>{{ item.name }}</h4>
                <p class="item-price">¥{{ item.price }}</p>
              </div>
              <div class="item-quantity">
                <button @click.stop="decreaseQty(item)">-</button>
                <span>{{ item.quantity }}</span>
                <button @click.stop="increaseQty(item)">+</button>
              </div>
              <button class="btn-remove" @click.stop="removeFromCart(item)">×</button>
            </div>
          </div>

          <div class="cart-empty" v-else>
            <div class="empty-icon">🛒</div>
            <p>购物车是空的</p>
            <button class="btn-continue" @click="showCart = false">继续购物</button>
          </div>

          <div class="cart-footer" v-if="cartStore.items.length > 0">
            <div class="cart-total-row">
              <span>总计</span>
              <span class="total-amount">¥{{ cartStore.totalPrice }}</span>
            </div>
            <button class="btn-checkout" @click="handleCheckout">
              去结算
            </button>
          </div>
        </div>
      </transition>

      <div class="cart-overlay" v-if="showCart" @click="showCart = false"></div>

      <!-- 商品详情弹窗 -->
      <transition name="fade">
        <div class="product-detail-modal" v-if="selectedProduct">
          <div class="modal-content">
            <div class="modal-header">
              <h3>{{ selectedProduct.name }}</h3>
              <button class="btn-close" @click="selectedProduct = null">×</button>
            </div>

            <div class="modal-body product-detail-body">
              <!-- 左侧图片区域 -->
              <div class="product-image-section">
                <div class="main-image">
                  <img :src="selectedProduct.image" alt="商品图片">
                </div>
                <div class="thumbnail-images">
                  <div class="thumbnail" v-for="(img, index) in selectedProduct.images || [selectedProduct.image]" :key="index">
                    <img :src="img" alt="缩略图">
                  </div>
                </div>
              </div>

              <!-- 右侧商品信息 -->
              <div class="product-info-section">
                <div class="product-price">¥{{ selectedProduct.price * productQuantity }}</div>
                <div class="product-origin">{{ selectedProduct.origin }}</div>
                <div class="product-tag" v-if="selectedProduct.tag">{{ selectedProduct.tag }}</div>

                <!-- 规格选择 -->
                <div class="spec-section" v-if="selectedProduct.specs && selectedProduct.specs.length > 0">
                  <h4>规格选择</h4>
                  <div class="spec-options">
                    <button 
                      v-for="spec in selectedProduct.specs" 
                      :key="spec.id"
                      class="spec-btn"
                      :class="{ active: selectedSpec === spec.id }"
                      @click="selectedSpec = spec.id"
                    >
                      {{ spec.name }}
                    </button>
                  </div>
                </div>

                <!-- 商品数量 -->
                <div class="quantity-section">
                  <h4>数量</h4>
                  <div class="quantity-control">
                    <button @click="decreaseDetailQty" :disabled="productQuantity <= 1">-</button>
                    <span>{{ productQuantity }}</span>
                    <button @click="increaseDetailQty">+</button>
                  </div>
                </div>

                <!-- 操作按钮 -->
                <div class="action-buttons">
                  <button class="btn-add-cart-detail" @click="addToCartFromDetail">加入购物车</button>
                  <button class="btn-buy-now">立即购买</button>
                </div>
              </div>
            </div>

            <!-- 商品详情和评论 -->
            <div class="product-tabs">
              <button 
                class="tab-btn" 
                :class="{ active: activeTab === 'detail' }"
                @click="activeTab = 'detail'"
              >
                商品详情
              </button>
              <button 
                class="tab-btn" 
                :class="{ active: activeTab === 'reviews' }"
                @click="activeTab = 'reviews'"
              >
                用户评价 ({{ selectedProduct.reviews ? selectedProduct.reviews.length : 0 }})
              </button>
            </div>

            <div class="tab-content">
              <!-- 商品详情内容 -->
              <div v-if="activeTab === 'detail'" class="detail-content">
                <div v-if="selectedProduct.description" v-html="selectedProduct.description"></div>
                <div v-else>
                  <h4>商品描述</h4>
                  <p>{{ selectedProduct.name }}是一款优质的产品，来自{{ selectedProduct.origin }}，品质保证，值得信赖。</p>
                </div>
              </div>

              <!-- 评论内容 -->
              <div v-if="activeTab === 'reviews'" class="reviews-content">
                <div v-if="selectedProduct.reviews && selectedProduct.reviews.length > 0">
                  <div v-for="review in selectedProduct.reviews" :key="review.id" class="review-item">
                    <div class="review-header">
                      <span class="reviewer">{{ review.reviewer }}</span>
                      <span class="review-date">{{ review.date }}</span>
                      <div class="review-rating">
                        <span v-for="i in 5" :key="i" class="star" :class="{ active: i <= review.rating }">&#9733;</span>
                      </div>
                    </div>
                    <div class="review-content">{{ review.content }}</div>
                  </div>
                </div>
                <div v-else class="no-reviews">
                  <p>暂无评价</p>
                </div>

                <!-- 发表评论 -->
                <div class="add-review">
                  <h4>发表评价</h4>
                  <div class="review-form">
                    <div class="rating-input">
                      <span>评分：</span>
                      <div class="rating-stars">
                        <span v-for="i in 5" :key="i" class="star" :class="{ active: i <= reviewRating }" @click="reviewRating = i">&#9733;</span>
                      </div>
                    </div>
                    <textarea v-model="reviewContent" placeholder="请输入您的评价..."></textarea>
                    <button class="btn-submit-review" @click="submitReview">提交评价</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </transition>

      <div class="modal-overlay" v-if="selectedProduct" @click="selectedProduct = null"></div>

      <transition name="fade">
        <div class="checkout-modal" v-if="showCheckout">
          <div class="modal-content">
            <div class="modal-header">
              <h3>确认订单</h3>
              <button class="btn-close" @click="showCheckout = false">×</button>
            </div>

            <div class="modal-body">
              <div class="order-items">
                <div v-for="item in cartStore.items" :key="item.id" class="order-item">
                  <span>{{ item.icon }} {{ item.name }}</span>
                  <span>x{{ item.quantity }}</span>
                  <span>¥{{ item.price * item.quantity }}</span>
                </div>
              </div>

              <div class="order-form">
                <div class="form-row">
                  <label>收货人</label>
                  <input type="text" v-model="orderForm.name" placeholder="请输入收货人姓名" />
                </div>
                <div class="form-row">
                  <label>联系电话</label>
                  <input type="tel" v-model="orderForm.phone" placeholder="请输入联系电话" />
                </div>
                <div class="form-row">
                  <label>收货地址</label>
                  <input type="text" v-model="orderForm.address" placeholder="请输入详细地址" />
                </div>
              </div>

              <div class="order-summary">
                <div class="summary-row">
                  <span>商品总额</span>
                  <span>¥{{ cartStore.totalPrice }}</span>
                </div>
                <div class="summary-row">
                  <span>运费</span>
                  <span>¥{{ shipping }}</span>
                </div>
                <div class="summary-row total">
                  <span>应付总额</span>
                  <span>¥{{ cartStore.totalPrice + shipping }}</span>
                </div>
              </div>
            </div>

            <div class="modal-footer">
              <button class="btn-cancel" @click="showCheckout = false">取消</button>
              <button class="btn-submit" @click="submitOrder">提交订单</button>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCartStore } from '../stores/cart'

const cartStore = useCartStore()
const showCart = ref(false)
const showCheckout = ref(false)

const selectedCategory = ref('all')

// 商品详情相关状态
const selectedProduct = ref(null)
const selectedSpec = ref(null)
const productQuantity = ref(1)
const activeTab = ref('detail')
const reviewRating = ref(5)
const reviewContent = ref('')

const categories = [
  { id: 'all', name: '全部' },
  { id: 'food', name: '特色美食' },
  { id: 'handcraft', name: '手工艺品' },
  { id: 'tea', name: '茶叶茶具' },
  { id: 'snack', name: '零食小吃' },
  { id: 'hhh', name: '特色农产品' },
  { id: 'cloth', name: '民族服饰' },
]

const products = [
  { id: 1, name: '黄石港饼', origin: '湖北黄石', price: 35, category: 'snack', image: new URL('../assets/港饼.jpg', import.meta.url).href, tag: '热卖' },
  { id: 2, name: '阳新布贴手工艺品', origin: '湖北黄石阳新', price: 188, category: 'handcraft', image: new URL('../assets/布贴.jpg', import.meta.url).href, tag: '非遗' },
  { id: 3, name: '大冶劲酒', origin: '湖北黄石大冶', price: 88, category: 'food', image: new URL('../assets/劲酒.png', import.meta.url).href },
  { id: 4, name: '珍珠果米酒', origin: '湖北黄石', price: 88, category: 'food', image: new URL('../assets/珍珠果米酒.jpg', import.meta.url).href },
  { id: 5, name: '白鸭松花皮蛋', origin: '湖北黄石', price: 45, category: 'food', image: new URL('../assets/松花皮蛋.jpg', import.meta.url).href },
  { id: 6, name: '阳新白茶', origin: '湖北黄石阳新', price: 268, category: 'tea', image: new URL('../assets/阳新白茶.png', import.meta.url).href, tag: '精品' },
  { id: 7, name: '黄石珍珠项链', origin: '湖北黄石', price: 398, category: 'handcraft', image: new URL('../assets/珍珠项链.png', import.meta.url).href },
  { id: 8, name: '黄石团城山竹笋', origin: '湖北黄石', price: 28, category: 'food', image: new URL('../assets/竹笋.jpg', import.meta.url).href }, 
  { id: 9, name: '铁矿明信片', origin: '铁矿明信片', price: 158, category: 'handcraft', image: new URL('../assets/明信片.jpg', import.meta.url).href },  
  { id: 10, name: '阳新富川山茶油', origin: '湖北黄石阳新', price: 128, category: 'food', image: new URL('../assets/茶油.png', import.meta.url).href },
  { id: 11, name: '黄石西塞山文创书签', origin: '湖北黄石', price: 25, category: 'handcraft', image: new URL('../assets/书签.jpg', import.meta.url).href },
  { id: 12, name: '鱼面丝', origin: '湖北黄石', price: 328, category: 'hhh', image: new URL('../assets/鱼面丝.jpg', import.meta.url).href },
  { id: 13, name: '白萝卜', origin: '湖北黄石大冶', price: 168, category: 'hhh', image: new URL('../assets/白萝卜.jpg', import.meta.url).href, tag: '精品' },
  { id: 14, name: '油面', origin: '湖北黄石阳新', price: 168, category: 'hhh', image: new URL('../assets/油面.jpg', import.meta.url).href },
  { id: 15, name: '芝麻喜饼', origin: '湖北黄石', price: 168, category: 'snack', image: new URL('../assets/芝麻喜饼.jpg', import.meta.url).href },
  { id: 16, name: '大冶印字粑', origin: '湖北黄石', price: 168, category: 'snack', image: new URL('../assets/印子粑.jpg', import.meta.url).href }
]

const filteredProducts = computed(() => {
  if (selectedCategory.value === 'all') {
    return products
  }
  return products.filter(p => p.category === selectedCategory.value)
})

const orderForm = ref({
  name: '',
  phone: '',
  address: ''
})

const shipping = computed(() => {
  return cartStore.totalPrice >= 199 ? 0 : 15
})

const addToCart = (product) => {
  cartStore.addItem({ ...product })
}

const increaseQty = (item) => {
  cartStore.updateQuantity(item.id, item.quantity + 1)
}

const decreaseQty = (item) => {
  if (item.quantity > 1) {
    cartStore.updateQuantity(item.id, item.quantity - 1)
  } else {
    removeFromCart(item)
  }
}

const removeFromCart = (item) => {
  cartStore.removeItem(item.id)
}

const handleCheckout = () => {
  showCart.value = false
  showCheckout.value = true
}

// 商品详情相关方法
const showProductDetail = (product) => {
  selectedProduct.value = product
  selectedSpec.value = product.specs && product.specs.length > 0 ? product.specs[0].id : null
  productQuantity.value = 1
  activeTab.value = 'detail'
  reviewRating.value = 5
  reviewContent.value = ''
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const showProductDetailFromCart = (cartItem) => {
  // 从products数组中找到对应的商品详情
  const product = products.find(p => p.id === cartItem.id)
  if (product) {
    selectedProduct.value = product
    selectedSpec.value = product.specs && product.specs.length > 0 ? product.specs[0].id : null
    productQuantity.value = cartItem.quantity
    activeTab.value = 'detail'
    reviewRating.value = 5
    reviewContent.value = ''
    showCart.value = false // 关闭购物车
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const decreaseDetailQty = () => {
  if (productQuantity.value > 1) {
    productQuantity.value--
  }
}

const increaseDetailQty = () => {
  productQuantity.value++
}

const addToCartFromDetail = () => {
  if (selectedProduct.value) {
    const productToAdd = {
      ...selectedProduct.value,
      quantity: productQuantity.value
    }
    if (selectedSpec.value) {
      const selectedSpecObj = selectedProduct.value.specs.find(spec => spec.id === selectedSpec.value)
      if (selectedSpecObj) {
        productToAdd.name = `${selectedProduct.value.name} - ${selectedSpecObj.name}`
      }
    }
    cartStore.addItem(productToAdd)
    alert('已加入购物车')
  }
}

const submitReview = () => {
  if (selectedProduct.value && reviewContent.value.trim()) {
    if (!selectedProduct.value.reviews) {
      selectedProduct.value.reviews = []
    }
    selectedProduct.value.reviews.push({
      id: Date.now(),
      reviewer: '匿名用户',
      date: new Date().toLocaleDateString(),
      rating: reviewRating.value,
      content: reviewContent.value
    })
    alert('评价提交成功！')
    reviewRating.value = 5
    reviewContent.value = ''
  } else {
    alert('请输入评价内容')
  }
}

const submitOrder = () => {
  if (!orderForm.value.name || !orderForm.value.phone || !orderForm.value.address) {
    alert('请填写完整的收货信息')
    return
  }

  alert('订单提交成功！\n收货人：' + orderForm.value.name + '\n我们将尽快为您发货。')
  cartStore.clearCart()
  showCheckout.value = false
  orderForm.value = { name: '', phone: '', address: '' }
}
</script>

<style scoped>
/* 老式电商平台样式 */
.shop-page {
  padding: 40px 0 80px;
  background-color: transparent;
}

.page-header {
  text-align: center;
  margin-bottom: 32px;
}

.page-title {
  font-family: var(--font-serif);
  font-size: 40px;
  font-weight: 700;
  color: var(--color-auxiliary);
  margin-bottom: 16px;
}

.page-desc {
  font-size: 16px;
  color: var(--color-text-light);
}

/* 老式电商平台左右布局 */
.shop-layout {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

/* 左侧分类导航（固定侧边栏） */
.sidebar {
  position: sticky;
  top: 100px;
  height: fit-content;
}

.category-nav {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid var(--color-border);
  padding: 0;
}

.category-btn {
  display: block;
  width: 100%;
  padding: 12px 16px;
  background: transparent;
  text-align: left;
  border: none;
  border-bottom: 1px solid var(--color-border);
  font-family: Arial, sans-serif;
  font-size: 14px;
  color: var(--color-text);
  cursor: pointer;
  transition: all 0.3s ease;
}

.category-btn:last-child {
  border-bottom: none;
}

.category-btn:hover {
  background: rgba(93, 64, 55, 0.05);
}

.category-btn.active {
  background: var(--color-primary);
  color: #fff;
}

.cat-icon {
  margin-right: 8px;
  font-size: 14px;
}

.cat-name {
  font-size: 14px;
}

/* 右侧主区域 */
.product-main {
  position: relative;
}

/* 右侧悬浮固定购物车图标按钮 */
.cart-float {
  position: fixed;
  right: 40px;
  top: 50%;
  transform: translateY(-50%);
  width: 50px;
  height: 50px;
  background: var(--color-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 24px;
  cursor: pointer;
  z-index: 99;
  border: 1px solid var(--color-accent);
}

.cart-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: #d35400;
  color: #fff;
  font-size: 12px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 商品网格布局 */
.products-section {
  background: rgba(255, 255, 255, 0.8);
  padding: 24px;
  border: 1px solid var(--color-border);
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

/* 商品卡片 */
.product-card {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid var(--color-border);
  overflow: hidden;
}

.product-image {
  position: relative;
  height: 180px;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid var(--color-border);
  overflow: hidden;
}

.product-tag {
  position: absolute;
  top: 8px;
  left: 8px;
  padding: 4px 12px;
  background: var(--color-primary);
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  z-index: 1;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-placeholder img {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover;
}

.product-info {
  padding: 16px;
}

.product-name {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--color-text);
  line-height: 1.4;
}

.product-origin {
  font-size: 12px;
  color: var(--color-text-light);
  margin-bottom: 12px;
}

.product-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.product-price {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-primary);
}

.btn-add-cart {
  padding: 6px 16px;
  background: var(--color-primary);
  color: #fff;
  font-size: 12px;
  border: none;
  cursor: pointer;
  font-weight: 500;
}

.btn-add-cart:hover {
  background: var(--color-accent);
}

/* 购物车侧边栏、结算弹窗样式 */
.cart-sidebar {
  position: fixed;
  top: 0;
  right: 0;
  width: 400px;
  height: 100vh;
  background: var(--color-card);
  z-index: 1001;
  display: flex;
  flex-direction: column;
  border-left: 1px solid var(--color-border);
}

.cart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-bg-light);
}

.cart-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-primary);
}

.btn-close {
  width: 32px;
  height: 32px;
  background: transparent;
  font-size: 24px;
  color: var(--color-text-light);
  border: none;
  cursor: pointer;
}

.btn-close:hover {
  color: var(--color-text);
}

.cart-items {
  flex: 1;
  overflow-y: auto;
  padding: 16px 24px;
}

.cart-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 0;
  border-bottom: 1px solid var(--color-border);
}

.item-icon {
  font-size: 32px;
}

.item-info {
  flex: 1;
}

.item-info h4 {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 4px;
  color: var(--color-text);
}

.item-price {
  font-size: 14px;
  color: var(--color-primary);
  font-weight: 600;
}

.item-quantity {
  display: flex;
  align-items: center;
  gap: 8px;
}

.item-quantity button {
  width: 28px;
  height: 28px;
  background: var(--color-bg-light);
  border: 1px solid var(--color-border);
  font-size: 16px;
  cursor: pointer;
}

.item-quantity button:hover {
  background: var(--color-primary);
  color: #fff;
  border-color: var(--color-primary);
}

.item-quantity span {
  font-size: 14px;
  font-weight: 600;
  min-width: 20px;
  text-align: center;
}

.btn-remove {
  width: 24px;
  height: 24px;
  background: transparent;
  color: var(--color-text-light);
  font-size: 18px;
  border: none;
  cursor: pointer;
}

.btn-remove:hover {
  color: #d35400;
}

.cart-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.empty-icon {
  font-size: 64px;
  opacity: 0.5;
}

.cart-empty p {
  color: var(--color-text-light);
}

.btn-continue {
  padding: 10px 24px;
  background: var(--color-primary);
  color: #fff;
  font-weight: 500;
  border: none;
  cursor: pointer;
}

.cart-footer {
  padding: 20px 24px;
  border-top: 1px solid var(--color-border);
  background: var(--color-bg-light);
}

.cart-total-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
  font-size: 16px;
}

.total-amount {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-primary);
}

.btn-checkout {
  width: 100%;
  padding: 14px;
  background: var(--color-primary);
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  border: none;
  cursor: pointer;
}

.btn-checkout:hover {
  background: var(--color-accent);
}

.cart-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
}

.checkout-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1002;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-content {
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  background: var(--color-card);
  border: 1px solid var(--color-border);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-bg-light);
}

.modal-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-primary);
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.order-items {
  margin-bottom: 24px;
}

.order-item {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid var(--color-border);
  font-size: 14px;
}

.order-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

.form-row {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-row label {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text);
}

.form-row input {
  padding: 12px;
  border: 1px solid var(--color-border);
  font-size: 14px;
  background: var(--color-card);
}

.form-row input:focus {
  border-color: var(--color-primary);
  outline: none;
}

.order-summary {
  background: var(--color-bg-light);
  padding: 16px;
  border: 1px solid var(--color-border);
}

.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 14px;
}

.summary-row.total {
  border-top: 1px solid var(--color-border);
  margin-top: 8px;
  padding-top: 16px;
  font-size: 16px;
  font-weight: 600;
}

.summary-row.total span:last-child {
  color: var(--color-primary);
  font-size: 20px;
}

.modal-footer {
  display: flex;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid var(--color-border);
  background: var(--color-bg-light);
}

.btn-cancel,
.btn-submit {
  flex: 1;
  padding: 12px;
  font-size: 15px;
  font-weight: 500;
  border: none;
  cursor: pointer;
}

.btn-cancel {
  background: var(--color-bg);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}

.btn-cancel:hover {
  background: var(--color-border);
}

.btn-submit {
  background: var(--color-primary);
  color: #fff;
}

.btn-submit:hover {
  background: var(--color-accent);
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 响应式适配 */
@media (max-width: 1024px) {
  .products-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .shop-layout {
    grid-template-columns: 1fr;
  }

  .sidebar {
    position: static;
  }

  .category-nav {
    display: flex;
    overflow-x: auto;
    gap: 0;
  }

  .category-btn {
    white-space: nowrap;
    border-bottom: none;
    border-right: 1px solid var(--color-border);
  }

  .category-btn:last-child {
    border-right: none;
  }

  .cart-float {
    right: 20px;
    bottom: 20px;
    top: auto;
    transform: none;
  }
}

@media (max-width: 480px) {
  .products-grid {
    grid-template-columns: 1fr;
  }
}

/* 商品详情弹窗 */
.product-detail-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1002;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.product-detail-modal .modal-content {
  width: 100%;
  max-width: 1000px;
  max-height: 90vh;
  background: var(--color-card);
  border: 1px solid var(--color-border);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.product-detail-body {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  padding: 24px;
  overflow-y: auto;
}

.product-image-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.main-image {
  height: 400px;
  background: var(--color-bg-light);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.main-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.thumbnail-images {
  display: flex;
  gap: 8px;
  overflow-x: auto;
}

.thumbnail {
  width: 80px;
  height: 80px;
  background: var(--color-bg-light);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.thumbnail:hover {
  border-color: var(--color-primary);
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-info-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.product-info-section .product-price {
  font-size: 32px;
  font-weight: 700;
  color: var(--color-primary);
}

.product-info-section .product-origin {
  font-size: 14px;
  color: var(--color-text-light);
}

.product-info-section .product-tag {
  display: inline-block;
  padding: 4px 12px;
  background: var(--color-primary);
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  border-radius: 4px;
  width: fit-content;
}

.spec-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.spec-section h4 {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text);
}

.spec-options {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.spec-btn {
  padding: 8px 16px;
  background: var(--color-bg-light);
  border: 1px solid var(--color-border);
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.spec-btn:hover {
  border-color: var(--color-primary);
}

.spec-btn.active {
  background: var(--color-primary);
  color: #fff;
  border-color: var(--color-primary);
}

.quantity-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.quantity-section h4 {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text);
}

.quantity-control {
  display: flex;
  align-items: center;
  gap: 8px;
}

.quantity-control button {
  width: 32px;
  height: 32px;
  background: var(--color-bg-light);
  border: 1px solid var(--color-border);
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.quantity-control button:hover {
  background: var(--color-primary);
  color: #fff;
  border-color: var(--color-primary);
}

.quantity-control button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quantity-control button:disabled:hover {
  background: var(--color-bg-light);
  color: var(--color-text);
  border-color: var(--color-border);
}

.quantity-control span {
  min-width: 40px;
  text-align: center;
  font-size: 14px;
  font-weight: 600;
}

.action-buttons {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.btn-add-cart-detail {
  flex: 1;
  padding: 14px;
  background: #ff9500;
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-add-cart-detail:hover {
  background: #ff7a00;
}

.btn-buy-now {
  flex: 1;
  padding: 14px;
  background: #ff4757;
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-buy-now:hover {
  background: #ff3742;
}

.product-tabs {
  display: flex;
  border-bottom: 1px solid var(--color-border);
}

.tab-btn {
  flex: 1;
  padding: 16px;
  background: var(--color-bg-light);
  border: none;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text);
  cursor: pointer;
  transition: all 0.3s ease;
  border-bottom: 2px solid transparent;
}

.tab-btn:hover {
  background: var(--color-background);
}

.tab-btn.active {
  background: var(--color-card);
  color: var(--color-primary);
  border-bottom-color: var(--color-primary);
}

.tab-content {
  padding: 24px;
  overflow-y: auto;
  flex: 1;
}

.detail-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-content h4 {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-auxiliary);
}

.detail-content p {
  font-size: 16px;
  line-height: 1.8;
  color: var(--color-text);
  text-align: justify;
}

.reviews-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.review-item {
  padding: 16px;
  background: var(--color-bg-light);
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.review-header {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.reviewer {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text);
}

.review-date {
  font-size: 12px;
  color: var(--color-text-light);
}

.review-rating {
  display: flex;
  gap: 2px;
}

.star {
  font-size: 14px;
  color: #ddd;
  cursor: pointer;
  transition: all 0.3s ease;
}

.star.active {
  color: #ffd700;
}

.review-content {
  font-size: 14px;
  line-height: 1.6;
  color: var(--color-text);
}

.no-reviews {
  text-align: center;
  padding: 40px;
  color: var(--color-text-light);
}

.add-review {
  margin-top: 24px;
  padding: 20px;
  background: var(--color-bg-light);
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.add-review h4 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text);
}

.review-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.rating-input {
  display: flex;
  align-items: center;
  gap: 12px;
}

.rating-input span {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text);
}

.rating-stars {
  display: flex;
  gap: 4px;
}

.rating-stars .star {
  font-size: 18px;
}

.review-form textarea {
  padding: 12px;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  font-size: 14px;
  resize: vertical;
  min-height: 100px;
  font-family: Arial, sans-serif;
}

.btn-submit-review {
  align-self: flex-start;
  padding: 8px 24px;
  background: var(--color-primary);
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-submit-review:hover {
  background: var(--color-accent);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1001;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .product-detail-body {
    grid-template-columns: 1fr;
  }

  .main-image {
    height: 300px;
  }

  .action-buttons {
    flex-direction: column;
  }

  .btn-add-cart-detail,
  .btn-buy-now {
    width: 100%;
  }
}
</style>