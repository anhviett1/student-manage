<template>
  <div class="login-container">
    <Toast />
    <div class="login-card">
      <h1>Đăng Nhập</h1>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Tên Người Dùng</label>
          <InputText
            id="username"
            v-model="v$.username.$model"
            :class="{ 'p-invalid': v$.username.$error }"
            @input="v$.username.$touch()"
            autofocus
          />
          <small class="p-error" v-if="v$.username.required.$invalid && v$.username.$dirty">
            Tên người dùng là bắt buộc.
          </small>
        </div>

        <div class="form-group">
          <label for="password">Mật Khẩu</label>
          <Password
            id="password"
            v-model="v$.password.$model"
            :feedback="false"
            toggleMask
            :class="{ 'p-invalid': v$.password.$error }"
            @input="v$.password.$touch()"
          />
          <small class="p-error" v-if="v$.password.required.$invalid && v$.password.$dirty">
            Mật khẩu là bắt buộc.
          </small>
        </div>

        <div class="form-actions">
          <Button
            type="submit"
            label="Đăng Nhập"
            icon="pi pi-sign-in"
            :loading="isLoading"
            class="login-button"
          />
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/stores/auth'
import { useVuelidate } from '@vuelidate/core'
import { required } from '@vuelidate/validators'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Button from 'primevue/button'
import Toast from 'primevue/toast'

const router = useRouter()
const toast = useToast()
const authStore = useAuthStore()

const formData = ref({
  username: '',
  password: '',
})

const isLoading = ref(false)

const rules = computed(() => ({
  username: { required },
  password: { required },
}))

const v$ = useVuelidate(rules, formData)

const handleLogin = async () => {
  v$.value.$touch()
  if (v$.value.$invalid) return

  isLoading.value = true
  try {
    await authStore.login(formData.value)
    router.push('/home')
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Lỗi',
      detail: error.response?.data?.detail || 'Thông tin đăng nhập không hợp lệ',
      life: 3000,
    })
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  position: fixed;
  top: 0;
  left: 0;
  overflow: hidden;
}

.login-card {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  width: 90%;
  max-width: 400px;
  min-width: 280px;
  margin: 1rem;
}

.login-card h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 2rem;
  font-size: 1.75rem;
  font-weight: 600;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: #34495e;
  text-align: left;
}

:deep(.p-inputtext),
:deep(.p-password-input) {
  width: 100%;
  height: 48px;
  padding: 0.75rem;
  font-size: 1rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  transition: border-color 0.3s;
}

:deep(.p-inputtext:focus),
:deep(.p-password-input:focus) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

:deep(.p-password) {
  width: 100%;
}

:deep(.p-invalid) {
  border-color: #ef4444 !important;
}

.p-error {
  color: #ef4444;
  font-size: 0.875rem;
}

.form-actions {
  margin-top: 1.5rem;
}

.login-button {
  width: 100%;
  height: 48px;
  font-size: 1rem;
  background: #3b82f6;
  border: none;
  border-radius: 6px;
  transition: background 0.3s;
}

.login-button:hover {
  background: #2563eb;
}

@media (max-width: 480px) {
  .login-card {
    padding: 1.5rem;
  }

  .login-card h1 {
    font-size: 1.5rem;
  }

  :deep(.p-inputtext),
  :deep(.p-password-input) {
    height: 44px;
    font-size: 0.9375rem;
  }

  .login-button {
    height: 44px;
    font-size: 0.9375rem;
  }
}
</style>