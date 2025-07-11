<template>
  <div class="teacher-layout">
    <Toast />

    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner">
        <i class="pi pi-spin pi-spinner" style="font-size: 2rem; color: #3b82f6" />
        <p>Đang tải...</p>
      </div>
    </div>

    <aside class="sidebar">
      <div class="logo">
        <router-link to="/teacher-dashboard">👨‍🏫 Teacher Panel</router-link>
      </div>

      <nav class="menu">
        <router-link to="/teacher-dashboard" class="menu-item">Trang chủ</router-link>
        <router-link to="/profile" class="menu-item">Hồ sơ</router-link>
        <router-link to="/students" class="menu-item">Sinh viên</router-link>
        <router-link to="/subjects" class="menu-item">Môn học</router-link>
        <router-link to="/scores" class="menu-item">Điểm số</router-link>
        <router-link to="/schedules" class="menu-item">Thời khóa biểu</router-link>
        <router-link to="/activities" class="menu-item">Lịch sử hoạt động</router-link>
      </nav>

      <div class="footer">
        <span class="username">
          <i class="pi pi-user mr-2"></i> {{ username }}
        </span>
        <Button label="Đăng Xuất" icon="pi pi-sign-out" text @click="handleLogout" />
      </div>
    </aside>

    <main class="main-content">
      <div class="topbar">
        <h2>{{ pageTitle }}</h2>
      </div>
      <div class="content">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Toast from 'primevue/toast'
import Button from 'primevue/button'
import { useAppEvents } from '@/composables/useAppEvents'

const route = useRoute()
const { isLoading, handleLogout } = useAppEvents()

const username = computed(() => localStorage.getItem('username') || 'Giảng viên')
const pageTitle = computed(() => route.meta.title || 'Cổng thông tin giảng viên')
</script>

<style scoped>
.teacher-layout {
  display: flex;
  min-height: 100vh;
  background: #f9fafb;
}

.sidebar {
  width: 250px;
  background: #1e3a8a;
  color: #fff;
  display: flex;
  flex-direction: column;
  padding: 1rem;
}

.logo {
  font-weight: bold;
  font-size: 1.2rem;
  margin-bottom: 1rem;
}
.logo a {
  color: #fff;
  text-decoration: none;
}

.menu {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.menu-item {
  padding: 0.75rem 1rem;
  color: #cbd5e1;
  text-decoration: none;
  border-radius: 6px;
  transition: background 0.2s, transform 0.2s;
}
.menu-item:hover,
.menu-item.router-link-exact-active {
  background: #3b82f6;
  color: #fff;
  transform: translateX(4px);
}

.footer {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.username {
  font-size: 0.9rem;
  color: #d1d5db;
}

.main-content {
  margin-left: 250px;
  flex: 1;
  display: flex;
  flex-direction: column;
}
.topbar {
  background: #fff;
  padding: 1rem 2rem;
  border-bottom: 1px solid #e2e8f0;
}
.content {
  padding: 2rem;
}
.loading-overlay {
  position: fixed;
  inset: 0;
  background: rgba(255, 255, 255, 0.85);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}
.loading-spinner {
  background: #fff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  text-align: center;
}
</style>
