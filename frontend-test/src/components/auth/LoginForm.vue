<template>
  <p-card class="login-card">
    <template #title>
      <div class="p-d-flex p-jc-center p-ai-center">
        <i class="mdi mdi-account-circle p-mr-2" style="font-size: 2rem;"></i> Đăng nhập Hệ thống
      </div>
    </template>
    <template #content>
      <form @submit.prevent="handleSubmit" class="p-fluid">
        <div class="p-field p-mb-4">
          <span class="p-float-label">
            <p-input-text id="username" v-model="v$.username.$model" :class="{'p-invalid': v$.username.$error}" aria-describedby="username-help" />
            <label for="username">Tên đăng nhập</label>
          </span>
          <small id="username-help" class="p-error" v-for="error of v$.username.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-field p-mb-4">
          <span class="p-float-label">
            <p-password id="password" v-model="v$.password.$model" toggleMask :class="{'p-invalid': v$.password.$error}" aria-describedby="password-help" :feedback="false" />
            <label for="password">Mật khẩu</label>
          </span>
          <small id="password-help" class="p-error" v-for="error of v$.password.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <p-button type="submit" label="Đăng nhập" icon="pi pi-sign-in" class="p-mt-4" :loading="isLoading" />

        <div class="p-d-flex p-jc-between p-mt-3">
          <p-button label="Quên mật khẩu?" class="p-button-text p-button-sm" @click="handleForgotPassword" />
          <p-button label="Đăng ký tài khoản" class="p-button-text p-button-sm" @click="handleRegister" />
        </div>
      </form>
    </template>
  </p-card>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import { useVuelidate } from '@vuelidate/core';
import { required, minLength, email } from '@vuelidate/validators';
import { useNotificationStore } from '@/stores/notification'; // Import the notification store
import { useRouter } from 'vue-router'; // Import useRouter for navigation

// PrimeVue Components
import PCard from 'primevue/card';
import PInputText from 'primevue/inputtext';
import PPassword from 'primevue/password';
import PButton from 'primevue/button';

// Mock API service for authentication (replace with actual API calls)
import { loginUser } from '@/services/mockAuthService';

const notificationStore = useNotificationStore();
const router = useRouter();

const formData = reactive({
  username: '',
  password: ''
});

const isLoading = ref(false);

// Vuelidate rules
const rules = computed(() => ({
  username: { required, minLength: minLength(3) }, // You might adjust minLength
  password: { required, minLength: minLength(6) }
}));

const v$ = useVuelidate(rules, formData);

const handleSubmit = async () => {
  const result = await v$.value.$validate();
  if (result) {
    isLoading.value = true;
    try {
      // Call your authentication service here
      const response = await loginUser(formData.username, formData.password); // Mock API call
      
      if (response.success) {
        notificationStore.showToast('Thành công', 'success', 'Đăng nhập thành công!');
        // TODO: Store user token/info in Pinia store or local storage
        // TODO: Redirect to dashboard based on user role (e.g., /admin, /teacher, /student)
        router.push('/dashboard'); // Example redirect
      } else {
        notificationStore.showToast('Lỗi đăng nhập', 'error', response.message || 'Tên đăng nhập hoặc mật khẩu không đúng.');
      }
    } catch (error) {
      notificationStore.showToast('Lỗi hệ thống', 'error', 'Có lỗi xảy ra khi đăng nhập. Vui lòng thử lại.');
      console.error('Login error:', error);
    } finally {
      isLoading.value = false;
    }
  } else {
    notificationStore.showToast('Lỗi nhập liệu', 'warn', 'Vui lòng điền đầy đủ và chính xác thông tin đăng nhập.');
  }
};

const handleForgotPassword = () => {
  notificationStore.showToast('Thông báo', 'info', 'Chức năng quên mật khẩu đang được phát triển.');
  // TODO: Implement navigation to forgot password page
  // router.push('/forgot-password');
};

const handleRegister = () => {
  notificationStore.showToast('Thông báo', 'info', 'Chức năng đăng ký tài khoản đang được phát triển.');
  // TODO: Implement navigation to registration page
  // router.push('/register');
};
</script>

<style scoped>
.login-card {
  max-width: 400px;
  margin: 5rem auto; /* Center the card vertically and horizontally */
  padding: 2rem;
  border-radius: var(--p-card-border-radius);
  box-shadow: var(--p-card-shadow);
}

.p-d-flex {
  display: flex;
}

.p-jc-center {
  justify-content: center;
}

.p-ai-center {
  align-items: center;
}

.p-mb-4 {
  margin-bottom: 1.5rem !important;
}

.p-mt-4 {
  margin-top: 1.5rem !important;
}

.p-mt-3 {
  margin-top: 1rem !important;
}

.p-mr-2 {
  margin-right: 0.5rem !important;
}

.p-button-sm {
  font-size: 0.875rem;
  padding: 0.5rem 0.75rem;
}
</style>