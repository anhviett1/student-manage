<template>
  <div class="auth-layout p-flex p-flex-column p-jc-center p-align-center p-min-h-screen">
    <div class="auth-container p-card p-shadow-24">
      <div class="p-card-header p-text-center p-py-3">
        <router-link to="/">
          <img src="@/assets/images/logo.png" alt="Logo" class="auth-logo" />
        </router-link>
        <h2 class="p-text-primary p-mb-0">{{ title }}</h2>
      </div>
      <div class="p-card-body p-p-4">
        <router-view /> </div>
    </div>
    <ToastNotification />
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import ToastNotification from '@/components/common/ToastNotification.vue';

// PrimeVue Components
import PCard from 'primevue/card';

defineProps({
  title: {
    type: String,
    default: 'Chào mừng'
  }
});
</script>

<style scoped>
.auth-layout {
  background: var(--p-primary-50); /* Nền màu nhẹ nhàng cho trang auth */
  background-image: linear-gradient(to bottom right, var(--p-primary-50), var(--p-primary-100));
}

.auth-container {
  width: 90%;
  max-width: 450px;
  background-color: var(--p-surface-0);
  border-radius: var(--p-border-radius);
  /* shadow 24 là một shadow mạnh mẽ của PrimeVue, rất nổi bật */
}

.auth-logo {
  width: 80px; /* Kích thước logo trên trang auth */
  height: auto;
  margin-bottom: 1rem;
}

.auth-container .p-card-header {
  border-bottom: 1px solid var(--p-surface-border);
}

/* Các lớp p-flex, p-flex-column, p-jc-center, p-align-center, p-min-h-screen, p-shadow-24, p-py-3, p-p-4 là của PrimeFlex */
</style>