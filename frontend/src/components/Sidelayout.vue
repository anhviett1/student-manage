<template>
  <div class="dashboard-wrapper">
    <Toast />
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner">
        <i class="pi pi-spin pi-spinner" style="font-size: 2rem; color: #3b82f6;"></i>
        <p>Đang tải...</p>
      </div>
    </div>

    <Sidebar>
      <template #menu>
        <SideMenu />
      </template>
    </Sidebar>

    <main class="dashboard-main">
      <div class="dashboard-content">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
import Toast from 'primevue/toast'
import Sidebar from './Sidebar.vue'
import SideMenu from './SideMenu.vue'
import { useAppEvents } from '@/composables/useAppEvents'

const { isLoading, notify } = useAppEvents()

const showNotification = () => {
  notify({
    severity: 'info',
    summary: 'Thông Báo',
    detail: 'Chức năng thông báo đang phát triển',
  })
}
</script>

<style scoped>
.dashboard-wrapper {
  display: flex;
  min-height: 100vh;
  background: #f4f6f9;
}

.dashboard-main {
  flex: 1;
  margin-left: 250px;
  display: flex;
  flex-direction: column;
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
}

.action-icon {
  padding: 0.5rem;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.action-icon:hover {
  background: #f8f9fa;
  transform: translateY(-1px);
}

.dashboard-content {
  padding: 2rem;
  flex: 1;
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
}

.loading-spinner {
  text-align: center;
  padding: 2rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.loading-spinner p {
  margin: 1rem 0 0;
  color: #6b7280;
  font-size: 1rem;
  font-weight: 500;
}

@media (max-width: 768px) {
  .dashboard-main {
    margin-left: 200px;
  }
}

</style>
