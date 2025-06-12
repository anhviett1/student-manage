<template>
  <div class="login-container">
    <Toast />
    <div class="login-card">
      <h1>Đăng Nhập</h1>
      <form @submit.prevent="handleSubmit" class="login-form">
        <div class="form-group">
          <label for="username">Tên đăng nhập</label>
          <input
            type="text"
            id="username"
            v-model="form.username"
            class="form-control"
            :class="{ 'is-invalid': v$.username.$error }"
          />
          <div class="invalid-feedback" v-if="v$.username.$error">
            {{ v$.username.$errors[0].$message }}
          </div>
        </div>

        <div class="form-group">
          <label for="password">Mật khẩu</label>
          <input
            type="password"
            id="password"
            v-model="form.password"
            class="form-control"
            :class="{ 'is-invalid': v$.password.$error }"
          />
          <div class="invalid-feedback" v-if="v$.password.$error">
            {{ v$.password.$errors[0].$message }}
          </div>
        </div>
        <div class="form-group">
          <input type="checkbox" id="rememberMe" v-model="form.rememberMe" />
          <label for="rememberMe">Ghi nhớ tôi</label>
        </div>
        <button type="submit" class="btn btn-primary" :disabled="isLoading">
          <span v-if="isLoading" class="spinner"></span>
          {{ isLoading ? 'Đang đăng nhập...' : 'Đăng Nhập' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/stores/auth'
import { useVuelidate } from '@vuelidate/core'
import { required, minLength } from '@vuelidate/validators'
import Toast from 'primevue/toast'

const router = useRouter()
const route = useRoute()
const toast = useToast()
const authStore = useAuthStore()
const isLoading = ref(false)

const form = reactive({
  username: '',
  password: '',
})

const rules = {
  username: { required, minLength: minLength(3) },
  password: { required, minLength: minLength(6) },
}

const v$ = useVuelidate(rules, form)

const handleSubmit = async () => {
  const isFormCorrect = await v$.value.$validate()
  if (!isFormCorrect) return

  try {
    isLoading.value = true
    await authStore.login(form)
    form.password = '' 
    const redirectPath = route.query.redirect || '/'
    router.push(redirectPath)
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
  if (form.rememberMe) {
    localStorage.setItem('rememberedUsername', form.username);
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
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #4a5568;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-control:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-control.is-invalid {
  border-color: #ef4444;
}

.invalid-feedback {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.btn {
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
  transform: translateY(-1px);
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
.spinner {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border: 2px solid #fff;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-right: 0.5rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
@media (max-width: 400px) {
  .login-card {
    padding: 1.5rem;
  }

  .login-card h1 {
    font-size: 1.5rem;
  }

  .form-control {
    height: 44px;
    font-size: 0.9375rem;
  }

  .btn {
    height: 44px;
    font-size: 0.9375rem;
  }
}
</style>