<template>
  <div class="layout-wrapper">
    <Toast />
    <!-- Sidebar -->
    <aside class="sidebar" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
      <div class="sidebar-header">
        <div class="logo-container">
          <router-link to="/" class="logo">
            <img :src="logo" alt="Logo" class="logo-image" />
            <span v-if="!isSidebarCollapsed">Student Management</span>
          </router-link>
          <Button
            icon="pi pi-bars"
            class="menu-toggle"
            text
            @click="toggleSidebar"
            v-if="isMobile"
          />
        </div>
      </div>
      <div class="sidebar-menu" v-if="authStore.isAuthenticated && !isSidebarCollapsed">
        <PanelMenu :model="menuItems" class="menu" v-model:expandedKeys="expandedKeys">
          <template #item="{ item }">
            <router-link
              v-if="item.visible"
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
      <div class="sidebar-footer" v-if="authStore.isAuthenticated && !isSidebarCollapsed">
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
    <main class="main-content" :class="{ 'main-content-full': isSidebarCollapsed }">
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
        <router-view></router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'primevue/usetoast'
import { usePermissions } from '@/composables/usePermissions'
import PanelMenu from 'primevue/panelmenu'
import Button from 'primevue/button'
import Toast from 'primevue/toast'
import logo from '@/assets/images/logo_min.png'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()
const toast = useToast()
const expandedKeys = ref({})
const isSidebarCollapsed = ref(false)
const isMobile = ref(window.innerWidth <= 768)

const {
  canViewStudents,
  canViewTeachers,
  canViewClasses,
  canViewSubjects,
  canViewEnrollments,
  canViewSemesters,
  canViewScores,
  canViewSchedules,
  isStudent,
  isTeacher,
  isAdmin,
} = usePermissions()

const menuItems = computed(() =>
  [
    {
      label: 'Trang Chủ',
      icon: 'pi pi-home',
      to: '/home',
      visible: true,
    },
    {
      label: 'Sinh Viên',
      icon: 'pi pi-users',
      to: '/students',
      visible: canViewStudents.value,
    },
    {
      label: 'Giảng Viên',
      icon: 'pi pi-briefcase',
      to: '/teachers',
      visible: canViewTeachers.value,
    },
    {
      label: 'Lớp Học',
      icon: 'pi pi-building',
      to: '/classes',
      visible: canViewClasses.value,
    },
    {
      label: 'Môn Học',
      icon: 'pi pi-book',
      to: '/subjects',
      visible: canViewSubjects.value,
    },
    {
      label: 'Ghi Danh',
      icon: 'pi pi-check-square',
      to: '/enrollments',
      visible: canViewEnrollments.value,
    },
    {
      label: 'Học Kỳ',
      icon: 'pi pi-calendar',
      to: '/semesters',
      visible: canViewSemesters.value,
    },
    {
      label: 'Điểm Số',
      icon: 'pi pi-chart-bar',
      to: '/scores',
      visible: canViewScores.value || isStudent.value,
    },
    {
      label: 'Lịch Học',
      icon: 'pi pi-calendar-alt',
      to: '/schedules',
      visible: canViewSchedules.value,
    },
    {
      label: 'Quản lý người dùng',
      icon: 'pi pi-cog',
      to: '/users',
      visible: isAdmin.value,
    },
  ].filter((item) => item.visible),
)

const currentRouteName = computed(() => {
  return route.meta.title || 'Trang Chủ'
})

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

const toggleNotifications = () => {
  toast.add({
    severity: 'info',
    summary: 'Thông Báo',
    detail: 'Chức năng thông báo đang được phát triển',
    life: 3000,
  })
}

const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

// Handle window resize for responsiveness
const handleResize = () => {
  isMobile.value = window.innerWidth <= 768
  if (isMobile.value) {
    isSidebarCollapsed.value = true
  } else {
    isSidebarCollapsed.value = false
  }
}

window.addEventListener('resize', handleResize)

// Cleanup event listener on component unmount
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
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
  transition: width 0.3s ease;
  display: flex;
  flex-direction: column;
}

.sidebar-collapsed {
  width: 60px;
}

.sidebar-header {
  padding: 0.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
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
}

.logo-image {
  width: 32px;
  height: 32px;
  margin-right: 0.5rem;
}

.menu-toggle {
  color: #fff;
  font-size: 1.2rem;
}

.sidebar-menu {
  flex: 1;
  padding: 1rem 0;
  overflow-y: auto;
}

.menu {
  background: transparent;
  border: none;
}

.menu :deep(.p-panelmenu-header-action) {
  background: transparent !important;
  color: #d1d5db !important;
}
.menu :deep(.p-panelmenu-header-action:hover) {
  background: #34495e !important;
  color: #fff !important;
}
.menu :deep(.p-menuitem-icon),
.menu :deep(.p-menuitem-text) {
  color: #d1d5db !important;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  color: #d1d5db;
  text-decoration: none;
  transition: background-color 0.2s, color 0.2s;
  border-radius: 6px;
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
  transition: margin-left 0.3s ease;
}

.main-content-full {
  margin-left: 60px;
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

@media (max-width: 768px) {
  .sidebar {
    width: 60px;
  }
  .main-content {
    margin-left: 60px;
  }
  .sidebar-collapsed {
    width: 0;
    overflow: hidden;
  }
  .main-content-full {
    margin-left: 0;
  }
}
</style>
