<template>
  <div class="translate-page">
    <header class="page-header">
        <h1 class="page-title">AI 语音翻译器</h1>
    </header>
    <br>
    <br>
    <div class="container main-layout">
      <div class="left-panel">

        <!-- 上传/录制区域 -->
        <div class="upload-area" @click="fileInput?.click()">
          <div class="upload-icon">🎙️</div>
          <p class="upload-text">点击或拖拽上传您的文件</p>
          <p class="upload-hint">支持格式：MP3、WAV、WebM</p>
          <button class="record-btn" @click.stop="toggleRecording">录制音频</button>
          <input
            ref="fileInput"
            type="file"
            class="hidden-input"
            accept="audio/*"
            @change="handleFileUpload"
          />
        </div>

        <!-- 录制/上传状态 -->
        <div v-if="isRecording" class="status-tip">
          <span class="recording-dot"></span> 正在录音...
        </div>
        <div v-else-if="uploadedFile" class="status-tip">
          {{ uploadedFile.name }}
          <button class="btn-remove" @click="removeFile">×</button>
        </div>

        <!-- 语言选择 -->
        <div class="lang-select-group">
          <div class="select-item">
            <label>输入语言</label>
            <select v-model="sourceLang" class="form-select">
              <option value="wu">大冶话</option>
              <option value="mandarin">普通话</option>
            </select>
          </div>
          <div class="select-item">
            <label>输出语言</label>
            <select v-model="targetLang" class="form-select">
              <option value="mandarin">普通话</option>
              <option value="english">英语</option>
            </select>
          </div>
        </div>

        <!-- 翻译按钮 -->
        <button class="btn-translate" @click="handleTranslate" :disabled="isTranslating">
          <span v-if="isTranslating" class="loading-spinner"></span>
          <span v-else>转换</span>
        </button>
      </div>

      <!-- 右侧：结果 + 历史记录 -->
      <div class="right-panel">
        <header class="panel-header">
          <h2 class="panel-title">历史记录</h2>
          <div class="header-actions">
            <input type="text" class="search-input" placeholder="搜索我的历史记录..." />
            <button class="btn-filter">筛选</button>
          </div>
        </header>

        <!-- 空状态 -->
        <div v-if="!translatedText && historyList.length === 0" class="empty-state">
          <h3>真实 AI 语音翻译，消除语言障碍</h3>
          <p>将您的声音翻译成多种语言，音质真实且语义准确。AI语音翻译器在确保语音翻译精准的同时，能完美保留音调、语速和清晰度。</p>
        </div>

        <!-- 当前翻译结果 -->
        <div v-if="translatedText" class="current-result">
          <div class="result-box">
            <p class="result-text">{{ translatedText }}</p>
          </div>
          <div class="output-actions">
            <button class="btn-copy" @click="copyResult">
              <span class="copy-icon">📋</span> 复制结果
            </button>
          </div>
        </div>

        <!-- 历史记录列表 -->
        <div class="history-container" v-if="historyList.length > 0">
          <div class="history-list">
            <div
              v-for="(item, index) in historyList"
              :key="index"
              class="history-item"
              @click="loadHistoryItem(index)"
            >
              <p class="history-text">{{ item.text }}</p>
              <span class="history-time">{{ item.time }}</span>
            </div>
          </div>
          <button class="btn-clear-history" @click="clearHistory">清空所有记录</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'

const sourceLang = ref('wu')
const targetLang = ref('mandarin')
const inputText = ref('')
const translatedText = ref('')
const isTranslating = ref(false)
const isRecording = ref(false)
const uploadedFile = ref(null)
const fileInput = ref(null)
const historyList = ref([])

let mediaRecorder = null
let audioStream = null
let audioChunks = []

// 切换录制状态
const toggleRecording = async () => {
  if (isRecording.value) {
    stopRecording()
  } else {
    await startRecording()
  }
}

const startRecording = async () => {
  try {
    audioStream = await navigator.mediaDevices.getUserMedia({
      audio: { echoCancellation: true, noiseSuppression: true }
    })
    audioChunks = []
    mediaRecorder = new MediaRecorder(audioStream, { mimeType: 'audio/webm' })
    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) audioChunks.push(e.data)
    }
    mediaRecorder.start()
    isRecording.value = true
  } catch (err) {
    alert('❌ 麦克风启动失败：' + err.message)
  }
}

const stopRecording = () => {
  if (!mediaRecorder) return
  mediaRecorder.stop()
  isRecording.value = false
  mediaRecorder.onstop = () => {
    audioStream.getTracks().forEach(track => track.stop())
    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' })
    const audioFile = new File([audioBlob], 'recording.webm', { type: 'audio/webm' })
    sendAudioToBackend(audioFile)
  }
}

// 文件上传
const handleFileUpload = (e) => {
  const file = e.target.files[0]
  if (file) {
    uploadedFile.value = file
    sendAudioToBackend(file)
  }
}

const removeFile = () => {
  uploadedFile.value = null
  fileInput.value.value = ''
}

// 核心翻译逻辑（保留原接口）
const sendAudioToBackend = async (audioFile) => {
  isTranslating.value = true
  inputText.value = ''
  translatedText.value = ''

  try {
    const formData = new FormData()
    formData.append('file', audioFile)
    formData.append('use_gpu', '1')
    formData.append('beam_size', '3')
    formData.append('nbest', '1')
    formData.append('decode_max_len', '0')
    formData.append('softmax_smoothing', '1.0')
    formData.append('aed_length_penalty', '0.0')
    formData.append('eos_penalty', '1.0')

    const res = await fetch('/api/dialect-recognition', {
      method: 'POST',
      body: formData
    })

    const data = await res.json()
    if (data.success && data.results && data.results.length > 0) {
      const firstResult = data.results[0]
      inputText.value = firstResult.text || ''
      translatedText.value = firstResult.text || ''
      // 加入历史记录
      addToHistory(translatedText.value)
    } else {
      translatedText.value = '识别失败'
    }
  } catch (err) {
    console.error(err)
    translatedText.value = '请求失败'
  } finally {
    isTranslating.value = false
  }
}

// 工具函数
const handleTranslate = () => {
  // 按钮点击触发，逻辑在 sendAudioToBackend 中
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const copyResult = async () => {
  try {
    await navigator.clipboard.writeText(translatedText.value)
    alert('复制成功')
  } catch {
    alert('复制失败')
  }
}

// 历史记录管理
const addToHistory = (text) => {
  historyList.value.unshift({
    text: text,
    time: new Date().toLocaleString()
  })
}

const loadHistoryItem = (index) => {
  const item = historyList.value[index]
  if (item) translatedText.value = item.text
}

const clearHistory = () => {
  historyList.value = []
  translatedText.value = ''
}

// 页面销毁清理
onUnmounted(() => {
  if (mediaRecorder) mediaRecorder.stop()
  if (audioStream) audioStream.getTracks().forEach(track => track.stop())
})
</script>

<style scoped>
.page-title {
  font-family: var(--font-serif);
  font-size: 40px;
  font-weight: 700;
  color: var(--color-auxiliary);
  margin-bottom: 16px;
}
/* 主色调完全沿用你原来的风格 */
.page-header {
  text-align: center;
  margin-bottom: 32px;
}
.translate-page {
  padding: 40px 0 80px;
}

.main-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  max-width: 1500px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 左右面板基础样式 */
.left-panel,
.right-panel {
  background: var(--color-white);
  padding: 24px;
  box-shadow: var(--shadow-md);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.panel-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-auxiliary);
  margin: 0;
}

/* 左侧上传区域 */
.upload-area {
  border: 2px dashed var(--color-border);
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: border-color var(--transition-normal);
}

.upload-area:hover {
  border-color: var(--color-accent);
  background: rgba(255, 255, 255, 0.5);
}

.upload-icon {
  font-size: 40px;
  margin-bottom: 16px;
  color: var(--color-text-light);
}

.upload-text {
  font-size: 16px;
  font-weight: 500;
  color: var(--color-text);
  margin: 0 0 8px;
}

.upload-hint {
  font-size: 13px;
  color: var(--color-text-light);
  margin: 0 0 20px;
}

.record-btn {
  background: var(--color-background);
  color: var(--color-text);
  border: 1px solid var(--color-border);
  padding: 10px 20px;
  cursor: pointer;
}

.hidden-input {
  display: none;
}

.status-tip {
  margin-top: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--color-text-light);
}

.recording-dot {
  width: 10px;
  height: 10px;
  background: #E53935;
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.btn-remove {
  background: none;
  border: none;
  color: #E53935;
  font-size: 18px;
  cursor: pointer;
}

/* 语言选择 */
.lang-select-group {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin: 24px 0;
}

.select-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-select {
  padding: 12px 16px;
  border: 1px solid var(--color-border);
  font-size: 15px;
  background: var(--color-white);
  cursor: pointer;
}

.form-select:focus {
  border-color: var(--color-accent);
}

/* 转换按钮 */
.btn-translate {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
  color: var(--color-white);
  border: none;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-translate:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: var(--color-white);
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 右侧结果与历史区 */
.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.search-input {
  background: var(--color-background);
  border: 1px solid var(--color-border);
  padding: 8px 12px;
  font-size: 14px;
}

.btn-filter {
  background: none;
  border: none;
  color: var(--color-text-light);
  font-size: 18px;
  cursor: pointer;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
}

.empty-state h3 {
  font-size: 22px;
  color: var(--color-auxiliary);
  margin-bottom: 12px;
}

.empty-state p {
  color: var(--color-text-light);
  line-height: 1.6;
}

.current-result {
  margin-bottom: 24px;
}

.result-box {
  min-height: 150px;
  padding: 20px;
  background: var(--color-background);
  border: 1px solid var(--color-border);
}

.result-text {
  font-size: 16px;
  line-height: 1.8;
  color: var(--color-text);
  white-space: pre-wrap;
}

.output-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 12px;
}

.btn-copy {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: var(--color-white);
  border: 1px solid var(--color-border);
  font-size: 14px;
  color: var(--color-text);
  transition: all var(--transition-fast);
}

.btn-copy:hover {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.copy-icon {
  font-size: 14px;
}

/* 历史记录 */
.history-container {
  border-top: 1px solid var(--color-border);
  padding-top: 20px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.history-item {
  padding: 12px;
  background: var(--color-background);
  border: 1px solid var(--color-border);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.history-item:hover {
  border-color: var(--color-accent);
  background: rgba(255, 255, 255, 0.6);
}

.history-text {
  font-size: 14px;
  color: var(--color-text);
  margin-bottom: 4px;
}

.history-time {
  font-size: 12px;
  color: var(--color-text-light);
}

.btn-clear-history {
  background: none;
  border: 1px solid #E53935;
  color: #E53935;
  padding: 8px 16px;
  cursor: pointer;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .main-layout {
    grid-template-columns: 1fr;
  }
}
</style>