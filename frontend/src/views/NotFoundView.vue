<template>
    <div class="not-found-container" aria-label="Trang không tìm thấy">
      <h1 class="error-code">404</h1>
      <h2 class="error-message">Không tìm thấy trang</h2>
      <p class="error-description">
        Trang bạn đang tìm kiếm không tồn tại hoặc đã bị di chuyển. Vui lòng kiểm tra lại URL hoặc quay về trang chính.
      </p>
      <div class="action-buttons">
        <Button v-if="isAuthenticated" label="Quay về Bảng điều khiển" severity="primary" icon="pi pi-home" @click="goToDashboard" class="action-button" aria-label="Quay về bảng điều khiển" />
        <Button v-else label="Đăng nhập" severity="primary" icon="pi pi-sign-in" @click="goToLogin" class="action-button" aria-label="Đăng nhập" />
        <Button label="Trang chủ" severity="secondary" icon="pi pi-arrow-left" @click="goToHome" class="action-button" aria-label="Quay về trang chủ" />
      </div>
    </div>
  </template>

  <script setup>
  import { computed } from 'vue';
  import { useRouter } from 'vue-router';
  import { useAuthStore } from '@/stores/auth';
  import Button from 'primevue/button';
  
  const router = useRouter();
  const authStore = useAuthStore();
  const isAuthenticated = computed(() => authStore.isAuthenticated);
  const goToDashboard = () => {
    const role = authStore.user?.role || 'student';
    router.push(
      role === 'admin' ? '/admin-dashboard' :
      role === 'teacher' ? '/teacher-dashboard' : '/student-dashboard'
    );
  };
  
  const goToLogin = () => {
    router.push('/login');
  };
  
  const goToHome = () => {
    router.push('/');
  };
  </script>
  
  <style scoped>
  .not-found-container {
    max-width: 600px;
    margin: 100px auto;
    padding: 24px;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    text-align: center;
  }
  
  .error-code {
    font-size: 96px;
    font-weight: bold;
    color: #dc3545;
    margin-bottom: 16px;
  }
  
  .error-message {
    font-size: 24px;
    font-weight: 600;
    color: #343a40;
    margin-bottom: 16px;
  }
  
  .error-description {
    font-size: 16px;
    color: #6c757d;
    margin-bottom: 24px;
  }
  
  .action-buttons {
    display: flex;
    justify-content: center;
    gap: 16px;
  }
  
  .action-button {
    font-size: 16px;
  }
  </style>