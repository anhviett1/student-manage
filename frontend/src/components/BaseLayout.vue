<template>
  <div class="layout-wrapper">
    <Toast />
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <router-link to="/" class="logo">
          <img :src="logo" alt="Logo" />
          Student Management
        </router-link>
      </div>
      <div class="sidebar-menu" v-if="authStore.isAuthenticated()">
        <PanelMenu :model="menuItems" class="menu" v-model:expandedKeys="expandedKeys">
          <template #item="{ item }">
            <router-link
              :to="item.to"
              class="menu-item"
              :class="{ 'active': $route.path === item.to }"
            >
              <i :class="item.icon" class="mr-2"></i>
              <span>{{ item.label }}</span>
            </router-link>
          </template>
        </PanelMenu>
      </div>
      <div class="sidebar-footer" v-if="authStore.isAuthenticated()">
        <div class="user-profile">
          <router-link to="/profile" class="profile-link">
            <i class="pi pi-user mr-2"></i>
            {{ authStore.user?.username || 'Profile' }}
          </router-link>
        </div>
        <Button
          label="Đăng Xuất"
          icon="pi pi-sign-out"
          severity="danger"
          text
          class="logout-button"
          @click="handleLogout"
        />
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <div class="topbar">
        <div class="topbar-title">
          <h2>{{ currentRouteName }}</h2>
        </div>
        <div class="topbar-actions">
          <Button
            icon="pi pi-bell"
            text
            class="action-icon"
            v-tooltip="'Notifications'"
            @click="toggleNotifications"
          />
        </div>
      </div>
      <div class="content">
        <slot></slot>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'primevue/usetoast'
import PanelMenu from 'primevue/panelmenu'
import Button from 'primevue/button'
import Toast from 'primevue/toast'
import logo from '@/assets/images/logo_min.png'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()
const toast = useToast()
const expandedKeys = ref({})



const menuItems = computed(() => [
  {
    label: 'Sinh Viên',
    icon: 'pi pi-users',
    to: '/students',
    visible: authStore.isAuthenticated(),
  },
  {
    label: 'Giảng Viên',
    icon: 'pi pi-briefcase',
    to: '/teachers',
    visible: authStore.isAuthenticated(),
  },
  {
    label: 'Lớp Học',
    icon: 'pi pi-building',
    to: '/classes',
    visible: authStore.isAuthenticated(),
  },
  {
    label: 'Môn Học',
    icon: 'pi pi-book',
    to: '/subjects',
    visible: authStore.isAuthenticated(),
  },
  {
    label: 'Ghi Danh',
    icon: 'pi pi-check-square',
    to: '/enrollments',
    visible: authStore.isAuthenticated(),
  },
  {
    label: 'Học Kỳ',
    icon: 'pi pi-calendar',
    to: '/semesters',
    visible: authStore.isAuthenticated(),
  },
  {
    label: 'Điểm Số',
    icon: 'pi pi-chart-bar',
    to: '/scores',
    visible: authStore.isAuthenticated(),
  },
].filter(item => item.visible))

const currentRouteName = computed(() => {
  return route.meta.title || 'Trang Chủ'
})

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

const toggleNotifications = () => {
  toast.add({ severity: 'info', summary: 'Thông Báo', detail: 'Chức năng thông báo đang được phát triển', life: 3000 })
}
</script>

<style scoped>
.layout-wrapper {
  display: flex;
  min-height: 100vh;
  background: #f4f6f9;
}

.sidebar {
  width: 250px;
  background: #2c3e50;
  color: #fff;
  padding: 1rem;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
}

.sidebar-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  color: #fff;
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
  display: flex;
  align-items: center;
}

.sidebar-menu {
  flex: 1;
  padding: 1rem 0;
}

.menu {
  background: transparent;
  border: none;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1.5rem;
  color: #d1d5db;
  text-decoration: none;
  transition: background-color 0.2s, color 0.2s;
}

.menu-item:hover {
  background: #34495e;
  color: #fff;
}

.menu-item.active {
  background: #3b82f6;
  color: #fff;
}

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
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
  transition: background-color 0.2s;
}

.profile-link:hover {
  background: #34495e;
  color: #fff;
}

.logout-button {
  width: 100%;
  justify-content: flex-start;
}

.main-content {
  flex: 1;
  margin-left: 250px;
  display: flex;
  flex-direction: column;
}

.topbar {
  background: #fff;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.topbar-title h2 {
  font-size: 1.5rem;
  color: #2c3e50;
  margin: 0;
}

.topbar-actions {
  display: flex;
  gap: 1rem;
}

.action-icon {
  font-size: 1.2rem;
  color: #34495e;
}

.content {
  padding: 2rem;
  background: #f4f6f9;
  flex: 1;
}
</style>