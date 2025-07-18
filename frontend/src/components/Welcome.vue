<template>
  <div class="welcome-container">
    <Toast />

    <!-- Intro ban đầu -->
    <div v-if="!showLogin" class="intro-content">
      <h1>👋 Chào mừng bạn đến với hệ thống</h1>
      <p>Hãy click nút dưới để tiếp tục đăng nhập</p>

      <button
        :disabled="isLoading"
        @click="showLoginForm"
        class="btn"
      >
        {{ isLoading ? '⏳ Đang tải...' : '🔐 Đăng nhập' }}
      </button>
    </div>

    <!-- Hiển thị login + banner -->
    <transition name="fade">
      <div v-if="showLogin" class="login-banner-wrapper">
        <div class="login-section">
          <LoginView />
        </div>
        <div class="banner-section">
          <img src="@/assets/images/banner.svg" alt="Banner" />
        </div>
      </div>
    </transition>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import Toast from 'primevue/toast'
import LoginView from '@/views/auth/LoginView.vue'

const isLoading = ref(false)
const showLogin = ref(false)

function showLoginForm() {
  isLoading.value = true
  setTimeout(() => {
    isLoading.value = false
    showLogin.value = true
  }, 500)
}
</script>

<style scoped>
.welcome-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #e0f7fa, #ffffff);
  font-family: 'Segoe UI', sans-serif;
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

/* Intro lúc đầu */
.intro-content {
  text-align: center;
  background-color: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  width: 400px;
  max-width: 100%;
}

.btn {
  padding: 12px 24px;
  font-size: 16px;
  background-color: #007acc;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.btn:hover {
  background-color: #005f99;
}

.btn:disabled {
  background-color: #b0bec5;
  cursor: not-allowed;
}

/* Layout hiển thị Login + Banner */
.login-banner-wrapper {
  width: 380vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  position: relative;
}

/* LoginView hiển thị phía trên */
.login-section {
  z-index: 2;
  background-color: rgb(129, 23, 190);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  padding: 0.5rem;
  border-radius: 16px;
  margin-top: 15rem;
  width: 90%;
  max-width: 480px;
}

/* Banner ở dưới chiếm toàn bộ phần còn lại */
.banner-section {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 90%;
}

.banner-section img {
  width: 90%;
  height: auto;
  object-fit: cover;
}

/* Transition mượt */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
