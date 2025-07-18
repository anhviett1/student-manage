<template>
  <div class="dashboard-wrapper">
    <Toast />
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner">
        <i class="pi pi-spin pi-spinner" style="font-size: 2rem; color: #3b82f6;"></i>
        <p>Đang tải...</p>
      </div>
    </div>
    <aside class="dashboard-sidebar">
      <div class="sidebar-header">
        <div class="logo-container">
          <router-link to="/student-dashboard" class="logo">
            <span>Student Management</span>
          </router-link>
        </div>
      </div>
      <nav class="dashboard-menu">
        <router-link to="/student-dashboard" class="menu-item">Bảng điều khiển</router-link>
        <router-link to="/profile" class="menu-item">Hồ sơ</router-link>
        <router-link to="/scores" class="menu-item">Điểm số</router-link>
        <router-link to="/schedules" class="menu-item">Lịch học</router-link> 
      </nav>
      <div class="sidebar-footer">
        <div class="user-profile">
          <span class="profile-link">
            <i class="pi pi-user mr-2"></i>
            {{ username }}
          </span>
        </div>
        <Button label="Đăng Xuất" icon="pi pi-sign-out" severity="danger" text class="logout-button" @click="handleLogout" />
      </div>
    </aside>
    <main class="dashboard-main">
      <div class="dashboard-topbar">
        <h2>Bảng Điều Khiển Sinh Viên</h2>
        <div class="topbar-actions">
          <Button icon="pi pi-bell" text class="action-icon" @click="notify({severity: 'info', summary: 'Thông Báo', detail: 'Chức năng thông báo đang phát triển'})" />
        </div>
      </div>
      <div class="dashboard-content">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import Button from 'primevue/button'
import Toast from 'primevue/toast'
import { usePermissions } from '@/composables/usePermissions'
import { useAppEvents } from '@/composables/useAppEvents'

const { isStudent } = usePermissions()
const { isLoading, notify, handleLogout } = useAppEvents()

const username = computed(() => {
  return localStorage.getItem('username') || 'Student'
})
</script>

<style scoped>
/* Copy the same styles as in AdminDashboardView.vue for consistency */
.dashboard-wrapper {
  display: flex;
  min-height: 100vh;
  background: #f4f6f9;
}
.dashboard-sidebar {
  width: 250px;
  background: #2c3e50;
  color: #fff;
  padding: 1rem;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  display: flex;
  flex-direction: column;
  z-index: 1000;
  overflow-y: auto;
  overflow-x: hidden;
}
.sidebar-header {
  padding: 0.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-height: 60px;
}
.logo-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}
.logo {
  color: #fff;
  font-size: 1.2rem;
  font-weight: bold;
  text-decoration: none;
  display: flex;
  align-items: center;
  transition: opacity 0.2s ease;
}
.logo:hover {
  opacity: 0.8;
}
.dashboard-menu {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  background: #f8fafc;
  border-radius: 10px;
  padding: 1.5rem 1rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(44, 62, 80, 0.08);
  max-width: 320px;
}
.dashboard-menu .menu-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1.25rem;
  color: #34495e;
  text-decoration: none;
  border-radius: 6px;
  font-size: 1.1rem;
  font-weight: 500;
  transition: all 0.2s;
  background: transparent;
  box-shadow: none;
  outline: none;
}
.dashboard-menu .menu-item:hover,
.dashboard-menu .menu-item:focus {
  background: #e0e7ef;
  color: #2563eb;
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.08);
}
.dashboard-menu .menu-item.router-link-exact-active,
.dashboard-menu .menu-item.active {
  background: #3b82f6;
  color: #fff;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
}
.dashboard-menu .menu-item:active {
  background: #2563eb;
  color: #fff;
}
.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: auto;
}
.user-profile {
  margin-bottom: 1rem;
}
.profile-link {
  color: #d1d5db;
  text-decoration: none;
  display: flex;
  align-items: center;
  padding: 0.5rem;
  border-radius: 4px;
  transition: all 0.2s ease;
}
.profile-link:hover {
  background: #34495e;
  color: #fff;
  transform: translateX(2px);
}
.logout-button {
  width: 100%;
  justify-content: flex-start;
  transition: all 0.2s ease;
}
.logout-button:hover {
  transform: translateX(2px);
}
.dashboard-main {
  flex: 1;
  margin-left: 250px;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
.dashboard-topbar {
  background: #fff;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
  min-height: 70px;
}
.dashboard-topbar h2 {
  font-size: 1.5rem;
  color: #2c3e50;
  margin: 0;
  font-weight: 600;
}
.topbar-actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}
.action-icon {
  font-size: 1.1rem;
  color: #34495e;
  padding: 0.5rem;
  border-radius: 4px;
  transition: all 0.2s ease;
}
.action-icon:hover {
  background-color: #f8f9fa;
  color: #2c3e50;
  transform: translateY(-1px);
}
.dashboard-content {
  padding: 2rem;
}
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  backdrop-filter: blur(2px);
}
.loading-spinner {
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}
.loading-spinner p {
  margin: 1rem 0 0 0;
  color: #6b7280;
  font-size: 1rem;
  font-weight: 500;
}
</style> 