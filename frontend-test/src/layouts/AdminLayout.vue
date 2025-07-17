<template>
  <div class="admin-layout">
    <AppNavbar class="admin-navbar" />
    <div class="admin-content-wrapper">
      <AppSidebar :menu-items="adminMenuItems" title="Admin Dashboard" class="admin-sidebar" />
      <main class="admin-main-content p-card">
        <p-card>
          <template #content>
            <router-view /> </template>
        </p-card>
      </main>
    </div>
    <FooterComponent />
    <ToastNotification /> </div>
</template>

<script setup>
import AppNavbar from '@/components/common/AppNavbar.vue';
import AppSidebar from '@/components/common/AppSidebar.vue';
import FooterComponent from './components/FooterComponent.vue';
import ToastNotification from '@/components/common/ToastNotification.vue'; // Toast toàn cục

// PrimeVue Components
import PCard from 'primevue/card';

// Menu items cho Admin
const adminMenuItems = [
  { title: 'Dashboard', to: '/admin/dashboard', icon: 'mdi mdi-view-dashboard-outline' },
  { title: 'Quản lý Người dùng', to: '/admin/users', icon: 'mdi mdi-account-group-outline' },
  { title: 'Quản lý Sinh viên', to: '/admin/students', icon: 'mdi mdi-account-school-outline' },
  { title: 'Quản lý Giáo viên', to: '/admin/teachers', icon: 'mdi mdi-account-tie-outline' },
  { title: 'Quản lý Môn học', to: '/admin/courses', icon: 'mdi mdi-book-open-variant' },
  { title: 'Quản lý Lớp học', to: '/admin/classes', icon: 'mdi mdi-chair-school' },
  { title: 'Cài đặt hệ thống', to: '/admin/settings', icon: 'mdi mdi-cog-outline' }
];
</script>

<style scoped>
.admin-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* Đảm bảo layout chiếm toàn bộ chiều cao màn hình */
  background-color: var(--p-surface-50); /* Nền nhẹ cho toàn bộ trang */
}

.admin-navbar {
  flex-shrink: 0; /* Ngăn navbar bị co lại */
}

.admin-content-wrapper {
  display: flex;
  flex-grow: 1; /* Cho phép phần nội dung wrapper chiếm hết không gian còn lại */
  padding: 1rem; /* Padding xung quanh nội dung chính */
  gap: 1rem; /* Khoảng cách giữa sidebar và main content */
}

.admin-sidebar {
  flex-shrink: 0; /* Ngăn sidebar bị co lại */
  border-radius: var(--p-border-radius);
  box-shadow: var(--p-shadow-1);
}

.admin-main-content {
  flex-grow: 1; /* Cho phép nội dung chính chiếm hết không gian còn lại */
  padding: 1rem; /* Padding bên trong main content */
  background-color: var(--p-surface-0);
  border-radius: var(--p-border-radius);
  box-shadow: var(--p-shadow-1);
  overflow: auto; /* Cho phép cuộn nếu nội dung quá dài */
}

.admin-main-content > :deep(.p-card) {
  height: 100%; /* Đảm bảo card chiếm hết chiều cao main content */
  display: flex;
  flex-direction: column;
}

.admin-main-content > :deep(.p-card .p-card-body) {
  flex-grow: 1; /* Đảm bảo nội dung bên trong card body chiếm hết không gian */
  display: flex;
  flex-direction: column;
}

.admin-main-content > :deep(.p-card .p-card-content) {
  flex-grow: 1;
}

/* Responsive adjustments */
@media (max-width: 992px) {
  .admin-content-wrapper {
    flex-direction: column; /* Sidebar và nội dung xếp chồng lên nhau */
    padding: 0.5rem;
    gap: 0.5rem;
  }
  .admin-sidebar {
    width: 100%; /* Sidebar chiếm toàn bộ chiều rộng */
    border-radius: 0; /* Bo góc 0 để trông như một phần của nav */
    box-shadow: none;
    margin-bottom: 0.5rem;
  }
  .admin-main-content {
    padding: 0.5rem;
    border-radius: 0;
    box-shadow: none;
  }
}
</style>