<template>
  <aside class="dashboard-sidebar">
    <div class="sidebar-header">
      <router-link to="/dashboard" class="logo">
        <span>Student Management</span>
      </router-link>
    </div>
    <slot name="menu"></slot>
    <div class="sidebar-footer">
      <div class="user-profile">
        <router-link to="/profile" class="profile-link">
          <i class="pi pi-user mr-2"></i>
          {{ username }}
        </router-link>
      </div>
      <Button label="Đăng Xuất" icon="pi pi-sign-out" severity="danger" text class="logout-button" @click="handleLogout" />
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import Button from 'primevue/button'
import { useAppEvents } from '@/composables/useAppEvents'

const { handleLogout } = useAppEvents()
const username = computed(() => localStorage.getItem('username') || 'User')
</script>

<style scoped>
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
}

.sidebar-header {
  padding: 0.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
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

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: auto;
}

.profile-link {
  color: #fff;
  text-decoration: none;
  display: flex;
  align-items: center;
  padding: 0.5rem;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.profile-link:hover {
  background: #34495e;
}

.logout-button {
  width: 100%;
  justify-content: flex-start;
}

@media (max-width: 768px) {
  .dashboard-sidebar {
    width: 200px;
  }
}
</style>