<template>
  <footer class="footer">
    <!-- 上半部分：APP/公众号/功能入口 -->
    <div class="footer-top">

      <!-- 右侧：公众号二维码 -->
      <div class="footer-qrcode">
        <p class="title">关注我们</p>
        <div class="qrcode-group">
          <div class="qrcode-item">
            <img src="../assets/images/weixin.png" alt="公众号二维码">
          </div>
        </div>
      </div>
    </div>

    <!-- 中间：导航链接 -->
    <div class="footer-nav">
      <div class="nav-column">
        <h4>关于我们</h4>
        <ul>
          <li><a href="#">平台简介</a></li>
          <li><a href="#">联系我们</a></li>
          <li><a href="#">合作伙伴</a></li>
        </ul>
      </div>
      <div class="nav-column">
        <h4>平台条款</h4>
        <ul>
          <li><a href="#">用户协议</a></li>
          <li><a href="#">社区规范</a></li>
          <li><a href="#">版权声明</a></li>
          <li><a href="#">免责声明</a></li>
        </ul>
      </div>
      <div class="nav-column">
        <h4>帮助中心</h4>
        <ul>
          <li><a href="#">新手上路</a></li>
          <li><a href="#">使用帮助</a></li>
          <li><a href="#">网站地图</a></li>
          <li><a href="#">意见反馈</a></li>
        </ul>
      </div>
    </div>

    <!-- 底部：版权信息 -->
    <div class="footer-bottom">
      <p class="copyright">
        © 2026 云语智行平台. All rights reserved.
        <span class="icp-info">鄂ICP备XXXXXXXX号 | 鄂公网安备XXXXXXXXXX号</span>
      </p>
      <div class="cert-list">
        <span class="cert-item">诚信网站</span>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background-color: var(--color-secondary);
  color: var(--color-text);
  margin-top: auto;
  padding: 30px 20px 20px;
  border-top: 1px solid var(--color-border);
  font-size: 14px;
}

/* 顶部模块布局 */
.footer-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  max-width: 1200px;
  margin: 0 auto 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--color-border);
}

.footer-app .title,
.footer-qrcode .title {
  font-size: 18px;
  color: var(--color-primary);
  margin-bottom: 16px;
}

.app-list, .qrcode-group {
  display: flex;
  gap: 30px;
}

.app-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.icon-box {
  width: 60px;
  height: 60px;
  background: var(--color-card);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  border: 1px solid var(--color-border);
}

.qrcode-placeholder {
  width: 80px;
  height: 80px;
  background: var(--color-card);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  border: 1px solid var(--color-border);
}

/* 导航链接区域 */
.footer-nav {
  display: flex;
  gap: 40px;
  max-width: 1200px;
  margin: 0 auto 30px;
}

.nav-column h4 {
  color: var(--color-primary);
  margin-bottom: 12px;
  font-size: 15px;
}

.nav-column ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-column li {
  margin-bottom: 8px;
}

.nav-column a {
  color: var(--color-text-light);
  text-decoration: none;
  transition: color 0.3s ease;
}

.nav-column a:hover {
  color: var(--color-primary);
}

/* 底部版权信息 */
.footer-bottom {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid var(--color-border);
}

.copyright {
  font-size: 13px;
  letter-spacing: 0.01em;
  margin: 0 0 10px;
  color: var(--color-text-light);
}

.icp-info {
  margin-left: 12px;
  color: var(--color-text-light);
}

.cert-list {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 10px;
}

.cert-item {
  font-size: 12px;
  color: var(--color-text-light);
}
</style>