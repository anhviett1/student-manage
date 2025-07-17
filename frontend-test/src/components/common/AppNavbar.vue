<template>
  <p-toolbar class="app-navbar">
    <template #start>
      <router-link to="/" class="brand-link p-flex p-align-center">
        <img src="@/assets/images/logo.png" alt="Logo" class="logo" />
        <span class="p-text-bold p-text-xl">Quản lý Sinh viên</span>
      </router-link>
    </template>

    <template #end>
      <div v-if="permissions.isAuthenticated.value" class="p-flex p-align-center p-gap-3">
        <span class="p-text-lg">
          Xin chào, <strong class="p-text-primary">{{ authStore.user?.full_name || authStore.user?.username }}</strong>
          (<strong class="p-text-capitalize">{{ permissions.userRole.value }}</strong>)
        </span>
        <p-button
          label="Hồ sơ"
          icon="pi pi-user"
          text
          @click="router.push('/profile')"
          class="p-button-sm"
        />
        <p-button
          label="Đăng xuất"
          icon="pi pi-sign-out"
          severity="danger"
          text
          @click="handleLogout"
          class="p-button-sm"
        />
      </div>
      <div v-else>
        <p-button
          label="Đăng nhập"
          icon="pi pi-sign-in"
          @click="router.push('/login')"
          class="p-button-sm"
        />
      </div>
    </template>
  </p-toolbar>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { usePermissions } from '@/utils/userPermissions';
import { useNotificationStore } from '@/stores/notification';

// PrimeVue Components
import PToolbar from 'primevue/toolbar';
import PButton from 'primevue/button';

const router = useRouter();
const authStore = useAuthStore();
const permissions = usePermissions();
const notificationStore = useNotificationStore();

const handleLogout = async () => {
  try {
    await authStore.logout();
    router.push({ name: 'Login' });
    notificationStore.showToast('Đăng xuất thành công!', 'success');
  } catch (error) {
    console.error('Lỗi khi đăng xuất:', error);
    notificationStore.showToast('Không thể đăng xuất. Vui lòng thử lại.', 'error');
  }
};
</script>

<style scoped>
.app-navbar {
  /* Ghi đè màu nền mặc định của p-toolbar nếu bạn muốn một màu cụ thể */
  background-color: var(--p-primary-900); /* Ví dụ: màu xanh đậm từ theme PrimeVue */
  color: var(--p-surface-0); /* Màu chữ trắng */
  padding: 1rem 2rem; /* Tăng padding để thanh nav cao hơn */
  box-shadow: var(--p-shadow-2); /* Sử dụng shadow của PrimeVue */
  border-radius: 0; /* Đảm bảo không có bo góc nếu toolbar nằm full chiều ngang */
}

.brand-link {
  text-decoration: none;
  color: inherit; /* Kế thừa màu từ parent (.app-navbar) */
}

.logo {
  height: 2.5rem; /* Kích thước logo */
  margin-right: 0.75rem; /* Khoảng cách giữa logo và chữ */
}
</style>