<template>
  <div class="community-page">
    <div class="banner-wrapper">
      <!-- 背景轮播 -->
      <!-- <div class="bg-carousel">
        <div 
          class="carousel-slide" 
          :class="{ active: currentBgIndex === index }"
          v-for="(color, index) in bgColors" 
          :key="index"
          :style="{ background: color }"
        ></div>
      </div> -->
      <div class="banner-content">
        <h1 class="page-title">文旅社区</h1>
      </div>
      <br />
      <br />
      <!-- 搜索框 -->
      <div class="search-box">
        <input 
          type="text" 
          v-model="searchKeyword" 
          class="search-input" 
          placeholder="搜索帖子标题/内容..."
        />
        <button class="search-btn">
          <img src="../assets/image.png" alt="搜索" class="search-icon">
        </button>
      </div>
      <br />
      <br />
    </div>

    <div class="container">
      <div class="community-layout" v-if="!selectedPost">
        <!-- 左侧：筛选栏 -->
        <aside class="left-sidebar">
          <div class="filter-box">
            <h4>筛选分类</h4>
            <div class="filter-list">
              <button 
                v-for="category in categories" 
                :key="category.id"
                class="filter-item"
                :class="{ active: selectedCategory === category.id }"
                @click="selectedCategory = category.id"
              >
                {{ category.name }}
              </button>
            </div>
          </div>
        </aside>

        <!-- 中间：帖子列表 -->
        <main class="post-main">
          <div class="loading-container" v-if="loading">
            <div class="loading-spinner"></div>
            <p>加载中...</p>
          </div>

          <div class="posts-list">
            <div 
              v-for="post in filteredPosts" 
              :key="post.id"
              class="post-card"
              @click="viewPostDetail(post)"
            >
              <div class="post-header">
                <div class="user-info">
                  <div class="user-avatar">
                    <span class="avatar-icon">{{ post.userAvatar }}</span>
                  </div>
                  <div class="user-details">
                    <h4 class="username">{{ post.username }}</h4>
                    <span class="post-time">{{ post.createTime }}</span>
                  </div>
                </div>
                <div class="post-category">
                  <span class="category-tag" :class="post.category">
                    {{ getCategoryName(post.category) }}
                  </span>
                </div>
              </div>
              <h3 class="post-title">{{ post.title }}</h3>
              <div class="post-content">{{ post.content }}</div>
              
              <div class="post-images" v-if="post.images && post.images.length > 0">
                <div class="images-grid">
                  <img 
                    v-for="(image, index) in post.images" 
                    :key="index"
                    :src="image"
                    :alt="'图片 ' + (index + 1)"
                    class="post-image"
                  />
                </div>
              </div>
              
              <div class="post-footer">
                <div class="post-actions">
                  <button class="action-btn like-btn" @click.stop="toggleLike(post.id)">
                    <span class="action-icon">{{ post.isLiked ? '❤️' : '🤍' }}</span>
                    <span class="action-text">{{ post.likeCount }}</span>
                  </button>
                  <button class="action-btn comment-btn" @click.stop="toggleComments(post.id)">
                    <span class="action-icon">💬</span>
                    <span class="action-text">{{ post.commentCount }}</span>
                  </button>
                  <button class="action-btn share-btn" @click.stop="sharePost(post.id)">
                    <span class="action-icon">📤</span>
                    <span class="action-text">分享</span>
                  </button>
                </div>
                <div class="view-detail">
                  <span>查看详情 →</span>
                </div>
              </div>

              <div class="comments-section" v-if="post.showComments">
                <div class="comments-list">
                  <div 
                    v-for="(comment, index) in post.comments" 
                    :key="index"
                    class="comment-item"
                  >
                    <div class="comment-user">
                      <span class="comment-avatar">{{ comment.avatar }}</span>
                      <span class="comment-username">{{ comment.username }}</span>
                    </div>
                    <div class="comment-content">{{ comment.content }}</div>
                    <span class="comment-time">{{ comment.createTime }}</span>
                  </div>
                </div>
                <div class="comment-form" v-if="isLoggedIn">
                  <input 
                    type="text" 
                    v-model="commentInput[post.id]"
                    class="form-input comment-input"
                    placeholder="写下你的评论..."
                    @keyup.enter="addComment(post.id)"
                  />
                  <button class="btn-comment" @click="addComment(post.id)" :disabled="commentSubmitting">
                    {{ commentSubmitting ? '发送中...' : '评论' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </main>

        <!-- 右侧：发布按钮 -->
        <aside class="right-sidebar">
          <button class="publish-btn-big" @click="showPublishModal = true">
            <span class="plus">+</span>
            <span>发布帖子</span>
          </button>
        </aside>
      </div>

      <!-- 帖子详情 -->
      <div class="post-detail" v-else>
        <button class="btn-back" @click="selectedPost = null">
          ← 返回社区
        </button>
        <div class="post-detail-card">
          <div class="post-header">
            <div class="user-info">
              <div class="user-avatar">
                <span class="avatar-icon">{{ selectedPost.userAvatar }}</span>
              </div>
              <div class="user-details">
                <h4 class="username">{{ selectedPost.username }}</h4>
                <span class="post-time">{{ selectedPost.createTime }}</span>
              </div>
            </div>
            <div class="post-category">
              <span class="category-tag" :class="selectedPost.category">
                {{ getCategoryName(selectedPost.category) }}
              </span>
            </div>
          </div>
          <h1 class="post-title-detail">{{ selectedPost.title }}</h1>
          <div class="post-content-detail">{{ selectedPost.content }}</div>
          
          <div class="post-images-detail" v-if="selectedPost.images && selectedPost.images.length > 0">
            <div class="images-grid-detail">
              <img 
                v-for="(image, index) in selectedPost.images" 
                :key="index"
                :src="image"
                :alt="'图片 ' + (index + 1)"
                class="post-image-detail"
                @click="openImageViewer(image)"
              />
            </div>
          </div>
          
          <div class="post-footer">
            <div class="post-actions">
              <button class="action-btn like-btn" @click="toggleLike(selectedPost.id)">
                <span class="action-icon">{{ selectedPost.isLiked ? '❤️' : '🤍' }}</span>
                <span class="action-text">{{ selectedPost.likeCount }}</span>
              </button>
              <button class="action-btn comment-btn" @click="toggleComments(selectedPost.id)">
                <span class="action-icon">💬</span>
                <span class="action-text">{{ selectedPost.commentCount }}</span>
              </button>
              <button class="action-btn share-btn" @click="sharePost(selectedPost.id)">
                <span class="action-icon">📤</span>
                <span class="action-text">分享</span>
              </button>
            </div>
          </div>
          
          <div class="comments-section" v-if="selectedPost.showComments">
            <h3 class="comments-title">评论 ({{ selectedPost.commentCount }})</h3>
            <div class="comments-list">
              <div 
                v-for="(comment, index) in selectedPost.comments" 
                :key="index"
                class="comment-item"
              >
                <div class="comment-user">
                  <span class="comment-avatar">{{ comment.avatar }}</span>
                  <span class="comment-username">{{ comment.username }}</span>
                </div>
                <div class="comment-content">{{ comment.content }}</div>
                <span class="comment-time">{{ comment.createTime }}</span>
              </div>
            </div>
            <div class="comment-form" v-if="isLoggedIn">
              <input 
                type="text" 
                v-model="commentInput[selectedPost.id]"
                class="form-input comment-input"
                placeholder="写下你的评论..."
                @keyup.enter="addComment(selectedPost.id)"
              />
              <button class="btn-comment" @click="addComment(selectedPost.id)" :disabled="commentSubmitting">
                {{ commentSubmitting ? '发送中...' : '评论' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 登录弹窗 -->
      <transition name="fade">
        <div class="login-modal" v-if="showLoginModal">
          <div class="modal-content">
            <div class="modal-header">
              <h3>登录后参与社区</h3>
              <button class="btn-close" @click="showLoginModal = false">×</button>
            </div>
            <div class="modal-body">
              <p>请先登录账户，然后发布帖子和评论。</p>
              <div class="modal-actions">
                <button class="btn-cancel" @click="showLoginModal = false">取消</button>
                <router-link to="/my" class="btn-login">去登录</router-link>
              </div>
            </div>
          </div>
        </div>
      </transition>

      <!-- 发布帖子弹窗 -->
      <transition name="fade">
        <div class="publish-modal" v-if="showPublishModal" @click.self="showPublishModal = false">
          <div class="publish-modal-content" @click.stop>
            <div class="modal-header">
              <h3>发布新帖子</h3>
              <button class="btn-close" @click="showPublishModal = false">×</button>
            </div>
            <div class="post-form">
              <input 
                type="text" 
                v-model="newPost.title" 
                class="form-input title-input" 
                placeholder="请输入标题"
              />
              <textarea 
                v-model="newPost.content" 
                class="form-input content-input" 
                placeholder="分享你的旅游体验或购物心得..."
                rows="4"
              ></textarea>
              <div class="image-upload">
                <label class="upload-btn">
                  <input type="file" accept="image/*" @change="handleImageUpload">
                  <span class="upload-icon">📷</span>
                  <span>添加图片</span>
                </label>
                <div class="uploaded-images" v-if="newPost.images.length > 0">
                  <div 
                    v-for="(image, index) in newPost.images" 
                    :key="index"
                    class="uploaded-image"
                  >
                    <img :src="image" :alt="'图片 ' + (index + 1)" />
                    <button class="remove-image" @click="removeImage(index)">×</button>
                  </div>
                </div>
              </div>
              <div class="post-actions">
                <select v-model="newPost.category" class="form-select">
                  <option value="travel">旅游体验</option>
                  <option value="shopping">购物心得</option>
                  <option value="other">其他</option>
                </select>
                <button class="btn-submit" @click="handleCreatePost" :disabled="submitting">
                  {{ submitting ? '发布中...' : '发布' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </transition>

      <!-- 图片查看器 -->
      <transition name="fade">
        <div class="image-viewer" v-if="selectedImage" @click="selectedImage = null">
          <div class="image-viewer-content" @click.stop>
            <img :src="selectedImage" alt="预览图片" />
            <button class="btn-close-image" @click="selectedImage = null">×</button>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { postApi } from '../services/api.js'

const isLoggedIn = ref(false)
const selectedCategory = ref('all')
const showLoginModal = ref(false)
const selectedPost = ref(null)
const selectedImage = ref(null)
const searchKeyword = ref('')
const showPublishModal = ref(false)

const newPost = ref({
  title: '',
  content: '',
  category: 'travel',
  images: []
})

const commentInput = ref({})
const posts = ref([])

const loading = ref(false)
const submitting = ref(false)
const commentSubmitting = ref(false)
const error = ref(null)

const categories = ref([
  { id: 'all', name: '全部' },
  { id: 'travel', name: '旅游体验' },
  { id: 'shopping', name: '购物心得' },
  { id: 'other', name: '其他' }
])

// 背景轮播
const bgColors = ref([
  '#e3f2fd',
  '#e8f5e9',
  '#fff3e0',
  '#f3e5f5',
  '#ede7f6',
  '#e0f7fa'
])
const currentBgIndex = ref(0)
let bgCarouselTimer = null

onMounted(() => {
  const user = localStorage.getItem('user')
  isLoggedIn.value = !!user
  fetchPosts()

  bgCarouselTimer = setInterval(() => {
    currentBgIndex.value = (currentBgIndex.value + 1) % bgColors.value.length
  }, 3000)
})

onUnmounted(() => {
  clearInterval(bgCarouselTimer)
})

// 格式化帖子数据，适配后端格式
const formatPost = (post) => {
  return {
    id: post.id,
    title: post.title,
    content: post.content,
    category: post.category,
    username: post.author ? post.author.username : '匿名',
    userAvatar: post.author ? (post.author.avatar || '👤') : '👤',
    createTime: post.created_at ? new Date(post.created_at).toLocaleString('zh-CN') : '刚刚',
    likeCount: post.likes || 0,
    commentCount: post.comments ? post.comments.length : 0,
    isLiked: false,
    images: post.images || [],
    comments: (post.comments || []).map(comment => ({
      username: comment.username,
      avatar: comment.avatar || '👤',
      content: comment.content,
      createTime: comment.created_at ? new Date(comment.created_at).toLocaleString('zh-CN') : '刚刚'
    })),
    showComments: false
  }
}

// 获取帖子
const fetchPosts = async () => {
  loading.value = true
  try {
    const data = await postApi.getPosts()
    posts.value = data.map(item => formatPost(item))
  } catch (err) {
    console.error(err)
    error.value = '获取帖子失败'
  } finally {
    loading.value = false
  }
}

// 发布帖子（弹窗版）
const handleCreatePost = async () => {
  if (!isLoggedIn.value) {
    showPublishModal.value = false
    showLoginModal.value = true
    return
  }
  if (!newPost.value.title || !newPost.value.content) {
    alert('请填写标题和内容')
    return
  }

  submitting.value = true
  try {
    const postData = {
      title: newPost.value.title,
      content: newPost.value.content,
      category: newPost.value.category,
      images: newPost.value.images,
      is_public: true
    }
    const newPostData = await postApi.createPost(postData)
    await fetchPosts()
    newPost.value = { title: '', content: '', category: 'travel', images: [] }
    showPublishModal.value = false
    alert('发布成功')
  } catch (err) {
    console.error(err)
    alert('发布失败')
  } finally {
    submitting.value = false
  }
}

// 点赞
const toggleLike = async (postId) => {
  if (!isLoggedIn.value) { showLoginModal.value = true; return }
  try {
    await postApi.likePost(postId)
    await fetchPosts()
  } catch (err) { 
    console.error(err)
    alert('点赞失败') 
  }
}

// 评论
const addComment = async (postId) => {
  const content = commentInput.value[postId]
  if (!isLoggedIn.value) { showLoginModal.value = true; return }
  if (!content) return

  commentSubmitting.value = true
  try {
    await postApi.addComment(postId, { content })
    commentInput.value[postId] = ''
    await fetchPosts()
  } catch (err) { 
    console.error(err)
    alert('评论失败') 
  }
  finally { commentSubmitting.value = false }
}

// 筛选
const filteredPosts = computed(() => {
  let list = posts.value
  if (selectedCategory.value !== 'all') {
    list = list.filter(p => p.category === selectedCategory.value)
  }
  const kw = searchKeyword.value.trim().toLowerCase()
  if (kw) {
    list = list.filter(p => 
      p.title.toLowerCase().includes(kw) || 
      p.content.toLowerCase().includes(kw)
    )
  }
  return list
})

// 图片上传
const handleImageUpload = (e) => {
  const files = e.target.files
  for (let i = 0; i < files.length; i++) {
    const reader = new FileReader()
    reader.onload = (ev) => newPost.value.images.push(ev.target.result)
    reader.readAsDataURL(files[i])
  }
}
const removeImage = (index) => newPost.value.images.splice(index, 1)

const viewPostDetail = (post) => selectedPost.value = post
const openImageViewer = (img) => selectedImage.value = img
const sharePost = () => {
  navigator.clipboard.writeText(location.href)
  alert('链接已复制')
}

const toggleComments = (postId) => {
  const p = posts.value.find(x => x.id === postId)
  if (p) p.showComments = !p.showComments
  if (selectedPost.value?.id === postId)
    selectedPost.value.showComments = !selectedPost.value.showComments
}

const getCategoryName = (catId) => {
  const cat = categories.value.find(c => c.id === catId)
  return cat ? cat.name : '其他'
}
</script>

<style scoped>
.community-page {
  min-height: 100vh;
  background: transparent;
  padding: 0;
  margin: 0;
}

/* 横幅 */
.banner-wrapper {
  position: relative;
  height: 360px;
  width: 100%;
}
.bg-carousel {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  z-index: 0;
}
.banner-content {
  position: relative; z-index: 1;
  text-align: center; padding-top: 70px;
}
.page-title {
  font-family: var(--font-serif);
  font-size: 40px;
  font-weight: 700;
  color: var(--color-auxiliary);
  margin-bottom: 16px;
}

/* 搜索框 */
.search-box {
  position: relative;
  margin: 0 auto 24px;
  display: flex; align-items: center;
  background: #fff; border-radius: 30px;
  padding: 4px; width: min(850px, 94%);
}
.search-input {
  flex: 1; border: none; outline: none;
  padding: 12px 16px; font-size: 15px;
}
.search-btn {
  background: transparent;
  color: #999;
  border: none;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  padding: 0 16px;
}

.search-btn:hover {
  color: #666;
}

.search-icon {
  width: 20px;
  height: 20px;
  object-fit: contain;
  transition: all 0.3s ease;
}

.search-btn:hover .search-icon {
  opacity: 0.8;
}

.container {
  background: transparent;
  padding: 20px 30px;
  max-width: 1400px;
  margin: 0 auto;
}

/* 三栏布局 */
.community-layout {
  display: grid;
  grid-template-columns: 220px 1fr 200px;
  gap: 30px;
}

/* 左侧筛选 */
.left-sidebar {
  padding-top: 10px;
}
.filter-box {
  background: rgba(255, 255, 255, 0.8);
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.filter-box h4 {
  margin: 0 0 14px;
  font-size: 16px;
  color: #333;
}
.filter-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.filter-item {
  padding: 10px 14px;
  border: none;
  background: #f8f5f2;
  text-align: left;
  cursor: pointer;
  font-size: 14px;
}
.filter-item.active {
  background: #8B4513;
  color: #fff;
}

/* 中间帖子 */
.post-main {
  padding-top: 10px;
}
.posts-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.post-card {
  background: rgba(255, 255, 255, 0.8);
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  cursor: pointer;
}
.post-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}
.user-info {
  display: flex; align-items: center; gap: 12px;
}
.user-avatar {
  width: 44px; height: 44px;
  border-radius: 50%; background: #d4b29a;
  display: flex; align-items: center; justify-content: center;
}
.avatar-icon { font-size: 18px; color: #fff; }
.username { font-size: 15px; font-weight: 600; margin: 0; }
.post-time { font-size: 12px; color: #888; }
.category-tag {
  padding: 4px 10px;
  font-size: 12px; background: #f5f5f5;
}
.category-tag.travel { color: #1976D2; }
.category-tag.shopping { color: #388E3C; }
.post-title {
  font-size: 18px; font-weight: 600;
  margin: 0 0 10px; color: #222;
}
.post-content {
  font-size: 15px; line-height: 1.6;
  color: #444; margin-bottom: 16px;
}
.images-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
  gap: 8px;
}
.post-image {
  width: 100%; height: 110px;
  object-fit: cover; border-radius: 6px;
}
.post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
}
.post-actions { display: flex; gap: 16px; }
.action-btn {
  display: flex; align-items: center; gap: 6px;
  background: transparent; border: none;
  color: #888; cursor: pointer;
}
.action-btn:hover { color: #d4b29a; }
.view-detail { color: #d4b29a; }

/* 评论 */
.comments-section {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px dashed #eee;
}
.comment-item {
  display: flex; flex-direction: column; gap: 6px;
  margin-bottom: 10px;
}
.comment-user {
  display: flex; align-items: center; gap: 8px;
}
.comment-avatar {
  width: 22px; height: 22px; border-radius: 50%;
  background: #d4b29a; color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-size: 12px;
}
.comment-content { font-size: 14px; color: #555; }
.comment-time { font-size: 12px; color: #999; }
.comment-input {
  padding: 8px 12px; border: 1px solid #ddd;
  flex: 1;
}
.btn-comment {
  padding: 8px 16px; background: #d4b29a;
  color: #fff; border: none;
}

/* 右侧发布按钮 */
.right-sidebar {
  padding-top: 10px;
}
.publish-btn-big {
  width: 100%;
  padding: 20px;
  background: #8B4513;
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 12px rgba(212, 178, 154, 0.3);
  position: sticky;
  top: 20px;
}
.publish-btn-big .plus {
  font-size: 28px;
  line-height: 1;
}
.publish-btn-big:hover {
  background: #c9a286;
}

/* 详情页 */
.post-detail {
  max-width: 900px;
  margin: 0 auto;
}
.btn-back {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 20px; background: rgba(255, 255, 255, 0.8);
  border: 1px solid #ddd; border-radius: 8px;
  margin-bottom: 20px; cursor: pointer;
}
.post-detail-card {
  background: rgba(255, 255, 255, 0.8); border-radius: 12px;
  padding: 30px; box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}
.post-title-detail {
  font-size: 26px; font-weight: 700;
  margin: 20px 0; color: #222;
}
.post-content-detail {
  font-size: 16px; line-height: 1.8; color: #333;
}

/* 发布弹窗 */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.publish-modal, .login-modal {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex; align-items: center; justify-content: center;
  z-index: 1000;
}
.publish-modal-content, .modal-content {
  background: #fff; border-radius: 12px;
  padding: 28px; max-width: 600px; width: 90%;
  max-height: 80vh; overflow-y: auto;
}
.modal-header {
  display: flex; justify-content: space-between;
  align-items: center; margin-bottom: 20px;
}
.btn-close {
  background: none; border: none;
  font-size: 20px; cursor: pointer; color: #666;
}
.post-form { display: flex; flex-direction: column; gap: 14px; }
.form-input {
  padding: 12px 16px; border: 1px solid #ddd;
  border-radius: 8px; font-size: 15px;
}
.content-input { resize: vertical; min-height: 100px; }
.upload-btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 20px; background: #f8f8f8;
  border: 1px dashed #ddd; border-radius: 8px; cursor: pointer;
}
.uploaded-images {
  display: flex; gap: 10px; margin-top: 10px;
}
.uploaded-image {
  position: relative; width: 80px; height: 80px;
  border-radius: 6px; overflow: hidden;
}
.uploaded-image img {
  width: 100%; height: 100%; object-fit: cover;
}
.remove-image {
  position: absolute; top: 4px; right: 4px;
  width: 22px; height: 22px;
  background: rgba(0,0,0,0.5); color: #fff;
  border: none; border-radius: 50%; cursor: pointer;
}
.form-select {
  padding: 10px; border: 1px solid #ddd;
  border-radius: 8px;
}
.btn-submit {
  padding: 10px 24px; background: #d4b29a;
  color: #fff; font-weight: 600;
  border: none; border-radius: 8px;
}
.btn-cancel {
  padding: 8px 18px; background: #f5f5f5;
  border: 1px solid #ddd; border-radius: 6px; cursor: pointer;
}
.btn-login {
  padding: 8px 18px; background: #d4b29a;
  color: #fff; border-radius: 6px; text-decoration: none;
}

/* 图片查看器 */
.image-viewer {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.9); display: flex;
  align-items: center; justify-content: center; z-index: 2000;
}
.image-viewer-content img {
  max-width: 90%; max-height: 80vh; border-radius: 8px;
}
.btn-close-image {
  position: absolute; top: 20px; right: 20px;
  background: rgba(255,255,255,0.2); color: #fff;
  border: none; width: 40px; height: 40px;
  border-radius: 50%; font-size: 20px; cursor: pointer;
}

/* 加载 */
.loading-container {
  display: flex; flex-direction: column;
  align-items: center; padding: 40px 0; gap: 16px;
}
.loading-spinner {
  width: 36px; height: 36px;
  border: 4px solid #e0d0bc;
  border-top: 4px solid #d4b29a;
  border-radius: 50%; animation: spin 1s linear infinite;
}
@keyframes spin { 100% { transform: rotate(360deg); } }

/* 禁用 */
.btn-submit:disabled, .btn-comment:disabled {
  opacity: 0.6; cursor: not-allowed;
}

/* 响应式 */
@media (max-width: 1024px) {
  .community-layout {
    grid-template-columns: 180px 1fr;
  }
  .right-sidebar {
    display: none;
  }
}
</style>