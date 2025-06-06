<template>
  <div class="login-container">
    <div class="login-card">
      <h1>Đăng nhập</h1>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Tên người dùng</label>
          <InputText
            id="username"
            v-model="credentials.username"
            :class="{ 'p-invalid': submitted && !credentials.username }"
            required
            autofocus
          />
          <small class="p-error" v-if="submitted && !credentials.username">Tên người dùng là bắt buộc.</small>
        </div>

        <div class="form-group">
          <label for="password">Mật khẩu</label>
          <Password
            id="password"
            v-model="credentials.password"
            :feedback="false"
            toggleMask
            :class="{ 'p-invalid': submitted && !credentials.password }"
            required
          />
          <small class="p-error" v-if="submitted && !credentials.password">Mật khẩu là bắt buộc.</small>
        </div>

        <div class="form-actions">
          <Button
            type="submit"
            label="Đăng nhập"
            icon="pi pi-sign-in"
            :loading="loading"
            class="w-full debug-login-button"
          />
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from 'primevue/usetoast';
import { useAuthStore } from '@/stores/auth';
import { api } from '@/services/api';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Button from 'primevue/button';

const router = useRouter();
const toast = useToast();
const authStore = useAuthStore();

const credentials = ref({
  username: '',
  password: ''
});
const submitted = ref(false);
const loading = ref(false);

const handleLogin = async () => {
  submitted.value = true;

  if (credentials.value.username && credentials.value.password) {
    try {
      loading.value = true;
      const response = await api.login(credentials.value);

      // Kiểm tra nếu response không hợp lệ
      if (!response.ok) {
        throw new Error('Phản hồi từ server không hợp lệ');
      }

      const data = await response.json(); // Parse JSON
      console.log('Dữ liệu từ API:', data); // Debug dữ liệu

      authStore.setToken(data.token);
      authStore.setUser(data.user);

      toast.add({
        severity: 'success',
        summary: 'Thành công',
        detail: 'Đăng nhập thành công',
        life: 3000
      });

      router.push('/home');
    } catch (error) {
      console.error('Lỗi đăng nhập:', error); // Debug lỗi
      toast.add({
        severity: 'error',
        summary: 'Lỗi',
        detail: error.message || 'Thông tin đăng nhập không hợp lệ',
        life: 3000
      });
    } finally {
      loading.value = false; // Đảm bảo loading được reset
    }
  }
};
</script>

<style scoped>
/* Full-screen container */
.login-container {
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-image: url('@/assets/images/banner-background.jpg');
  overflow: hidden;
  position: fixed;
  top: 0;
  left: 0;
}

/* Responsive login card */
.login-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 400px;
  min-width: 300px;
  margin: 1rem;
}

/* Title styling */
.login-card h1 {
  text-align: center;
  color: #333;
  margin-bottom: 2rem;
  font-size: 1.75rem;
  font-weight: 600;
}

/* Form layout */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

/* Form group spacing */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

/* Label styling */
.form-group label {
  font-weight: 500;
  color: #333;
  text-align: left;
}

/* Style for input fields */
:deep(.p-inputtext),
:deep(.p-password-input) {
  width: 100% !important;
  height: 48px;
  padding: 0.75rem;
  font-size: 1rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  transition: border-color 0.3s;
}

/* Focus state for inputs */
:deep(.p-inputtext:focus),
:deep(.p-password-input:focus) {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Ensure password field container is visible */
:deep(.p-password) {
  width: 100% !important;
  display: block !important;
}

/* Error state for inputs */
:deep(.p-invalid) {
  border-color: #ef4444 !important;
}

/* Error message styling */
.p-error {
  color: #ef4444;
  font-size: 0.875rem;
}

/* Style for the button */
:deep(.p-button) {
  width: 100% !important;
  height: 48px;
  font-size: 1rem;
  border-radius: 6px;
  display: block !important; /* Đảm bảo nút luôn hiển thị */
}

/* Form actions spacing */
.form-actions {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
}

/* Responsive adjustments */
@media (max-width: 480px) {
  .login-card {
    padding: 1.5rem;
    min-width: 280px;
  }

  .login-card h1 {
    font-size: 1.5rem;
  }

  :deep(.p-inputtext),
  :deep(.p-password-input),
  :deep(.p-button) {
    height: 44px;
    font-size: 0.9375rem;
  }
}
:deep(.p-button.debug-login-button) {
  width: 100% !important;
  height: 48px;
  font-size: 1rem;
  font-weight: 600;
  color: #fff;
  background: linear-gradient(to right, #3b82f6, #2563eb);
  border: none;
  border-radius: 6px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

:deep(.p-button.debug-login-button):hover {
  background: linear-gradient(to right, #2563eb, #1d4ed8);
  transform: translateY(-1px);
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.15);
}

:deep(.p-button .p-button-icon) {
  font-size: 1.25rem;
}

</style>