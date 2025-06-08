<template>
  <div class="admin-layout">
    <Toast />
    <!-- Sidebar -->
    <Sidebar v-model:visible="sidebarVisible" :position="'left'" class="sidebar">
      <div class="sidebar-header">
        <router-link to="/admin/dashboard" class="logo" @click="sidebarVisible = false">
          <i class="pi pi-cog mr-2"></i>
          Admin Panel
        </router-link>
      </div>
      <div class="sidebar-menu">
        <PanelMenu :model="menuItems" class="menu" v-model:expandedKeys="expandedKeys">
          <template #item="{ item }">
            <router-link
              v-if="item.to"
              :to="item.to"
              class="menu-item"
              :class="{ 'active': $route.path === item.to }"
              @click="sidebarVisible = false"
            >
              <i :class="item.icon" class="mr-2"></i>
              <span>{{ item.label }}</span>
            </router-link>
            <a
              v-else-if="item.url"
              :href="item.url"
              class="menu-item"
              :class="{ 'active': isDjangoAdminActive }"
              @click="sidebarVisible = false"
            >
              <i :class="item.icon" class="mr-2"></i>
              <span>{{ item.label }}</span>
            </a>
          </template>
        </PanelMenu>
      </div>
      <div class="sidebar-footer">
        <div class="user-profile">
          <router-link to="/profile" class="profile-link" @click="sidebarVisible = false">
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
          @click="logout"
        />
      </div>
    </Sidebar>

    <!-- Topbar -->
    <div class="topbar">
      <Button
        icon="pi pi-bars"
        text
        class="menu-toggle"
        @click="sidebarVisible = !sidebarVisible"
        v-tooltip="'Toggle Menu'"
      />
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

    <!-- Main Content -->
    <main class="main-content">
      <div class="content">
        <router-view></router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'primevue/usetoast'
import Sidebar from 'primevue/sidebar'
import PanelMenu from 'primevue/panelmenu'
import Button from 'primevue/button'
import Toast from 'primevue/toast'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const toast = useToast()
const sidebarVisible = ref(false)
const expandedKeys = ref({})

const menuItems = computed(() => [
  {
    label: 'Bảng Điều Khiển',
    icon: 'pi pi-tachometer-alt',
    to: '/admin/dashboard',
    visible: authStore.isAuthenticated,
  },
  {
    label: 'Người Dùng',
    icon: 'pi pi-users',
    to: '/admin/users',
    visible: authStore.isAuthenticated,
  },
  {
    label: 'Sinh Viên',
    icon: 'pi pi-user-graduate',
    to: '/admin/students',
    visible: authStore.isAuthenticated,
  },
  {
    label: 'Khóa Học',
    icon: 'pi pi-book',
    to: '/admin/courses',
    visible: authStore.isAuthenticated,
  },
  {
    label: 'Lớp Học',
    icon: 'pi pi-chalkboard',
    to: '/admin/classes',
    visible: authStore.isAuthenticated,
  },
  {
    label: 'Django Admin',
    icon: 'pi pi-external-link',
    url: '/admin/', // Assuming Django Admin is at /admin/
    visible: authStore.isAdmin, // Only visible to admins
  },
].filter(item => item.visible))

const currentRouteName = computed(() => {
  return route.meta.title || 'Bảng Điều Khiển'
})

const isDjangoAdminActive = computed(() => {
  return window.location.pathname.startsWith('/admin/')
})

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    toast.add({
      severity: 'error',
      summary: 'Lỗi',
      detail: 'Vui lòng đăng nhập để truy cập',
      life: 3000,
    })
    router.push('/login')
    return
  }
  if (!authStore.user) {
    await authStore.fetchCurrentUser()
  }
})

const logout = async () => {
  await authStore.logout()
  router.push('/login')
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
  window.location.href = '/admin/'
}

const toggleNotifications = () => {
  toast.add({
    severity: 'info',
    summary: 'Thông Báo',
    detail: 'Chức năng thông báo đang được phát triển',
    life: 3000,
  })
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: #f4f6f9;
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
  z-index: 1000;
}

.menu-toggle {
  font-size: 1.5rem;
  color: #34495e;
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

.sidebar {
  background: #2c3e50;
  color: #fff;
  width: 250px;
  display: flex;
  flex-direction: column;
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
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.content {
  padding: 2rem;
  background: #f4f6f9;
}

@media (max-width: 768px) {
  .topbar {
    padding: 1rem;
  }

  .topbar-title h2 {
    font-size: 1.2rem;
  }

  .content {
    padding: 1rem;
  }

  .sidebar {
    width: 200px;
  }
}
</style>