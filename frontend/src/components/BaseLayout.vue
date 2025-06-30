<template>
  <div class="layout-wrapper">
    <Toast />
    
    <!-- Loading overlay -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner">
        <i class="pi pi-spin pi-spinner" style="font-size: 2rem; color: #3b82f6;"></i>
        <p>Đang tải...</p>
      </div>
    </div>
    
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
              :class="{ active: isActiveRoute(item.to) }"
            >
              <i :class="item.icon" class="mr-2"></i>
              <span>{{ item.label }}</span>
            </router-link>
          </template>
        </PanelMenu>
      </div>
      <div class="sidebar-footer" v-if="authStore.isAuthenticated && !isSidebarCollapsed">
        <div class="user-profile">
          <router-link :to="{ name: 'profile' }" class="profile-link">
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
          <Button
            v-if="authStore.isAdmin"
            label="Django Admin"
            icon="pi pi-external-link"
            text
            class="action-icon"
            @click="goToDjangoAdmin"
            v-tooltip="'Go to Django Admin'"
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
import { ref, computed, onMounted, onUnmounted } from 'vue'
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
const isMobile = ref(false)
const isLoading = ref(true)

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

// Optimized menu items with better performance
const menuItems = computed(() => {
  const items = [
    {
      label: 'Trang Chủ',
      icon: 'pi pi-home',
      to: { name: 'home' },
      visible: true,
    },
    {
      label: 'Hồ Sơ',
      icon: 'pi pi-user',
      to: { name: 'profile' },
      visible: authStore.isAuthenticated,
    },
    {
      label: 'Sinh Viên',
      icon: 'pi pi-users',
      to: { name: 'students' },
      visible: canViewStudents.value,
    },
    {
      label: 'Giảng Viên',
      icon: 'pi pi-briefcase',
      to: { name: 'teachers'},
      visible: canViewTeachers.value,
    },
    {
      label: 'Lớp Học',
      icon: 'pi pi-building',
      to: { name: 'classes' },
      visible: canViewClasses.value,
    },
    {
      label: 'Môn Học',
      icon: 'pi pi-book',
      to: { name: 'subjects' },
      visible: canViewSubjects.value,
    },
    {
      label: 'Ghi Danh',
      icon: 'pi pi-check-square',
      to: { name: 'enrollments' },
      visible: canViewEnrollments.value,
    },
    {
      label: 'Học Kỳ',
      icon: 'pi pi-calendar',
      to: { name: 'semesters' },
      visible: canViewSemesters.value,
    },
    {
      label: 'Điểm Số',
      icon: 'pi pi-chart-bar',
      to: { name: 'scores' },
      visible: canViewScores.value || isStudent.value,
    },
    {
      label: 'Lịch Học',
      icon: 'pi pi-calendar-alt',
      to: { name: 'schedules' },
      visible: canViewSchedules.value,
    },
  ]
  
  return items.filter(item => item.visible)
})

const currentRouteName = computed(() => {
  return route.meta.title || 'Trang Chủ'
})

const isActiveRoute = (routeTo) => {
  if (routeTo.name === 'profile') {
    return route.name === 'profile' || route.name === 'profile-change-password'
  }
  return route.name === routeTo.name
}

const handleLogout = async () => {
  try {
    await authStore.logout()
    router.push('/login')
  } catch (error) {
    console.error('Logout error:', error)
  }
}

const toggleNotifications = () => {
  toast.add({
    severity: 'info',
    summary: 'Thông Báo',
    detail: 'Chức năng thông báo đang được phát triển',
    life: 3000,
  })
}

const goToDjangoAdmin = () => {
  if (!authStore.isAdmin) {
    toast.add({
      severity: 'error',
      summary: 'Lỗi',
      detail: 'Bạn không có quyền truy cập Django Admin',
      life: 3000,
    })
    return
  }
  window.open('http://127.0.0.1:8000/admin/', '_blank')
}

const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

// Optimized resize handler
const handleResize = () => {
  const newIsMobile = window.innerWidth <= 768
  if (newIsMobile !== isMobile.value) {
    isMobile.value = newIsMobile
    if (isMobile.value) {
      isSidebarCollapsed.value = true
    } else {
      isSidebarCollapsed.value = false
    }
  }
}

// Initialize layout
const initializeLayout = async () => {
  try {
    isLoading.value = true
    
    // Initialize mobile state
    isMobile.value = window.innerWidth <= 768
    if (isMobile.value) {
      isSidebarCollapsed.value = true
    }
    
    // Fetch current user if authenticated
    if (authStore.isAuthenticated && !authStore.user) {
      await authStore.fetchCurrentUser()
    }
    
    // Add event listener
    window.addEventListener('resize', handleResize)
    
  } catch (error) {
    console.error('Layout initialization error:', error)
    toast.add({
      severity: 'error',
      summary: 'Lỗi',
      detail: 'Không thể khởi tạo giao diện',
      life: 3000,
    })
  } finally {
    // Add a small delay to ensure smooth transition
    setTimeout(() => {
      isLoading.value = false
    }, 300)
  }
}

// Proper lifecycle management
onMounted(() => {
  initializeLayout()
})

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
  transition: width 0.3s ease, transform 0.3s ease;
  display: flex;
  flex-direction: column;
  z-index: 1000;
  overflow-y: auto;
  overflow-x: hidden;
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

.logo-image {
  width: 32px;
  height: 32px;
  margin-right: 0.5rem;
  flex-shrink: 0;
}

.menu-toggle {
  color: #fff;
  font-size: 1.2rem;
  padding: 0.5rem;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.menu-toggle:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.sidebar-menu {
  flex: 1;
  padding: 1rem 0;
  overflow-y: auto;
  overflow-x: hidden;
}

.menu {
  background: transparent;
  border: none;
}

.menu :deep(.p-panelmenu-header-action) {
  background: transparent !important;
  color: #d1d5db !important;
  border: none !important;
  padding: 0.75rem 1rem !important;
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
  transition: all 0.2s ease;
  border-radius: 6px;
  margin: 0.25rem 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.menu-item:hover {
  background: #34495e;
  color: #fff;
  transform: translateX(4px);
}

.menu-item.active {
  background: #3b82f6;
  color: #fff;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
}

.menu-item i {
  margin-right: 0.75rem;
  flex-shrink: 0;
  width: 16px;
  text-align: center;
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

.main-content {
  flex: 1;
  margin-left: 250px;
  display: flex;
  flex-direction: column;
  transition: margin-left 0.3s ease;
  min-height: 100vh;
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
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
  min-height: 70px;
}

.topbar-title h2 {
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

.content {
  padding: 2rem;
  background: #f4f6f9;
  flex: 1;
  min-height: calc(100vh - 70px);
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
    width: 250px;
  }
  
  .sidebar:not(.sidebar-collapsed) {
    transform: translateX(0);
  }
  
  .sidebar-collapsed {
    transform: translateX(-100%);
  }
  
  .main-content {
    margin-left: 0;
  }
  
  .main-content-full {
    margin-left: 0;
  }
  
  .topbar {
    padding: 1rem;
  }
  
  .topbar-title h2 {
    font-size: 1.2rem;
  }
  
  .content {
    padding: 1rem;
  }
  
  .topbar-actions {
    gap: 0.5rem;
  }
  
  .action-icon {
    font-size: 1rem;
    padding: 0.4rem;
  }
}

/* Tablet Responsive */
@media (min-width: 769px) and (max-width: 1024px) {
  .sidebar {
    width: 200px;
  }
  
  .main-content {
    margin-left: 200px;
  }
  
  .main-content-full {
    margin-left: 60px;
  }
  
  .content {
    padding: 1.5rem;
  }
}

/* Performance optimizations */
.sidebar * {
  will-change: transform, opacity;
}

.menu-item {
  will-change: transform, background-color;
}

/* Smooth scrolling for sidebar */
.sidebar-menu {
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.3) transparent;
}

.sidebar-menu::-webkit-scrollbar {
  width: 4px;
}

.sidebar-menu::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-menu::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
}

.sidebar-menu::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

/* Loading overlay */
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

/* Animation for loading */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.loading-spinner {
  animation: fadeIn 0.3s ease-out;
}
</style>
