<template>
  <Sidelayout>
    <template #default>
      <div class="dashboard-topbar">
        <h2>Bảng Điều Khiển Quản Trị</h2>
        <div class="topbar-actions">
          <Button icon="pi pi-bell" text class="action-icon" @click="showNotification" />
          <Button label="Django Admin" icon="pi pi-external-link" text class="action-icon" @click="goToDjangoAdmin" />
        </div>
      </div>
      <div class="dashboard-content">
        <router-view />
      </div>
    </template>
  </Sidelayout>
</template>

<script setup>
import Button from 'primevue/button'
import Sidelayout from '@/components/Sidelayout.vue'
import { useAppEvents } from '@/composables/useAppEvents'

const { notify } = useAppEvents()

const showNotification = () => {
  notify({ severity: 'info', summary: 'Thông Báo', detail: 'Chức năng thông báo đang phát triển' })
}

const goToDjangoAdmin = () => {
  window.open('http://127.0.0.1:8000/admin/', '_blank')
}
</script>

