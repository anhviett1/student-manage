<template>
  <div class="not-found-page p-flex p-flex-column p-align-center p-justify-center p-text-center p-py-5">
    <i class="mdi mdi-alert-circle-outline p-text-8xl p-text-primary p-mb-3"></i>
    <h1 class="p-text-8xl p-text-bold p-mb-2">404</h1>
    <h2 class="p-text-4xl p-mb-4">Không tìm thấy trang</h2>
    <p class="p-text-lg p-text-color-secondary p-mb-5">
      Rất tiếc, trang bạn đang tìm kiếm không tồn tại.
    </p>
    <router-link to="/">
      <p-button label="Quay về trang chủ" icon="pi pi-home" />
    </router-link>
  </div>
</template>

<script setup>
// PrimeVue Components
import PButton from 'primevue/button';
</script>

<style scoped>
.not-found-page {
  /* Các lớp PrimeFlex đã lo phần lớn bố cục */
  min-height: calc(100vh - var(--app-navbar-height) - var(--app-footer-height)); /* Điều chỉnh để nằm giữa */
}
</style>