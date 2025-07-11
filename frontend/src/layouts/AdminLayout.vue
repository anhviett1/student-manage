<template>
  <div class="admin-layout">
    <Toast />
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner">
        <i class="pi pi-spin pi-spinner" style="font-size: 2rem; color: #3b82f6"></i>
        <p>Đang tải...</p>
      </div>
    </div>

    <aside class="sidebar">
      <div class="logo">
        <router-link to="/admin/dashboard">Student Manager</router-link>
      </div>
      <nav class="menu">
        <router-link to="/admin/dashboard" class="menu-item">Dashboard</router-link>
        <router-link to="/admin/students" class="menu-item">Quản lý Sinh viên</router-link>
        <router-link to="/admin/teachers" class="menu-item">Quản lý Giảng viên</router-link>
        <router-link to="/admin/classes" class="menu-item">Lớp học</router-link>
        <router-link to="/admin/subjects" class="menu-item">Môn học</router-link>
        <router-link to="/admin/scores" class="menu-item">Điểm số</router-link>
        <router-link to="/admin/schedules" class="menu-item">Thời khóa biểu</router-link>
        <router-link to="/admin/departments" class="menu-item">Khoa</router-link>
        <router-link to="/admin/enrollments" class="menu-item">Ghi danh</router-link>
        <router-link to="/admin/semesters" class="menu-item">Học kỳ</router-link>
        <router-link to="/admin/activities" class="menu-item">Hoạt động</router-link>
        <router-link to="/admin/profile" class="menu-item">Hồ sơ cá nhân</router-link>
      </nav>
      <div class="footer">
        <span class="username">
          <i class="pi pi-user mr-2"></i> {{ username }}
        </span>
        <Button label="Đổi mật khẩu" icon="pi pi-key" text @click="goToChangePassword"/>
        <Button label="Đăng Xuất" icon="pi pi-sign-out" text @click="handleLogout" />
      </div>
    </aside>

    <main class="main-content">
      <div class="topbar">
        <h2>{{ pageTitle }}</h2>
        <Button
          label="Django Admin"
          icon="pi pi-external-link"
          text
          @click="goToDjangoAdmin"
        />
      </div>

      <div class="content">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import Button from 'primevue/button'
import Toast from 'primevue/toast'
import { useAppEvents } from '@/composables/useAppEvents'
import { usePermissions } from '@/composables/usePermissions'

const { isAdmin } = usePermissions()

if (!isAdmin.value) {
  // Redirect nếu không phải admin
  window.location.href = '/'
}

const { isLoading, handleLogout } = useAppEvents()
const route = useRoute()

const pageTitle = computed(() => route.meta.title || 'Admin')
const username = computed(() => localStorage.getItem('username') || 'Admin')

const goToChangePassword = () => {
  router.push('../auth/change-password')
}
const goToDjangoAdmin = () => {
  window.open('http://127.0.0.1:8000/admin/', '_blank')
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: #f4f6f9;
}

.sidebar {
  width: 260px;
  background: #2c3e50;
  color: #fff;
  display: flex;
  flex-direction: column;
  padding: 1rem;
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
}

.logo {
  font-weight: bold;
  font-size: 1.2rem;
  margin-bottom: 1rem;
  color: #fff;
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
  color: #d1d5db;
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
  margin-left: 260px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.topbar {
  background: #fff;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e5e7eb;
}

.content {
  padding: 2rem;
  background: #f9fafb;
  flex: 1;
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
