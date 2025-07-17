<template>
  <div class="home-page p-text-center p-py-5">
    <h1 class="p-text-primary p-mb-3">Chào mừng đến với Hệ thống Quản lý Sinh viên!</h1>
    <p class="p-text-lg p-text-color-secondary p-mb-4">
      Đây là nơi bạn có thể quản lý thông tin sinh viên, giáo viên, môn học và phòng ban một cách hiệu quả.
    </p>
    <div class="p-flex p-justify-center p-gap-3">
      <router-link to="/auth/login">
        <p-button label="Đăng nhập" icon="pi pi-sign-in" severity="primary" />
      </router-link>
      <router-link to="/auth/register">
        <p-button label="Đăng ký" icon="pi pi-user-plus" severity="secondary" outlined />
      </router-link>
    </div>
  </div>
</template>

<script setup>
// PrimeVue Components
import PButton from 'primevue/button';
</script>

<style scoped>
.home-page {
  /* Các lớp PrimeFlex đã lo phần lớn bố cục */
  background-color: var(--p-surface-0);
  border-radius: var(--p-border-radius);
  box-shadow: var(--p-shadow-1);
}
</style>