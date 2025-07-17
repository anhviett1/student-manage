<template>
  <div class="main-layout">
    <AppNavbar />
    <main class="main-content p-container p-py-4">
      <p-card>
        <template #content>
          <router-view /> </template>
      </p-card>
    </main>
    <FooterComponent />
    <ToastNotification />
  </div>
</template>

<script setup>
import AppNavbar from '@/components/common/AppNavbar.vue';
import FooterComponent from './components/FooterComponent.vue';
import ToastNotification from '@/components/common/ToastNotification.vue';

// PrimeVue Components
import PCard from 'primevue/card';

// PrimeFlex utility classes like p-container (for max-width) will be applied here.
</script>

<style scoped>
.main-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--p-surface-50); /* Nền nhẹ */
}

.main-content {
  flex-grow: 1;
  padding: 1rem;
}

.main-content > :deep(.p-card) {
  height: 100%; /* Đảm bảo card chiếm hết chiều cao main content */
  display: flex;
  flex-direction: column;
}

.main-content > :deep(.p-card .p-card-body) {
  flex-grow: 1; /* Đảm bảo nội dung bên trong card body chiếm hết không gian */
  display: flex;
  flex-direction: column;
}

.main-content > :deep(.p-card .p-card-content) {
  flex-grow: 1;
}

/* Responsive cho main content */
@media (max-width: 768px) {
  .main-content {
    padding: 0.5rem;
  }
}
</style>