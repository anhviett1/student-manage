<template>
  <div class="login-card">
    <Toast />
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

      <div class="form-group remember-me">
        <input type="checkbox" id="rememberMe" v-model="form.rememberMe" /> 
        <label for="rememberMe">Ghi nhớ tôi</label>
        
      </div>

      <button type="submit" class="btn btn-primary" :disabled="isLoading">
        <span v-if="isLoading" class="spinner"></span>
        {{ isLoading ? 'Đang đăng nhập...' : 'Đăng Nhập' }}
      </button>
    </form>
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
  rememberMe: false,
})

const rules = {
  username: { required, minLength: minLength(3) },
  password: { required, minLength: minLength(6) },
}

const v$ = useVuelidate(rules, form)

const handleSubmit = async () => {
  const isFormCorrect = await v$.value.$validate()
  if (!isFormCorrect) return

  isLoading.value = true
  try {
    await authStore.login(form)
    const role = authStore.user?.role
    if (role === 'admin') {
      router.push('/admin')
    } else if (role === 'teachers') {
      router.push('/teacher')
    } else if (role === 'students') {
      router.push('/student')
    } else {
      router.push('/')
    }
  } catch (error) {
    // toast will be triggered inside auth store
  } finally {
    isLoading.value = false
  }

  if (form.rememberMe) {
    localStorage.setItem('rememberedUsername', form.username)
  }
}
</script>

<style scoped>
.login-card {
  background: #e0dada;
  padding: 2.5rem;
  border-radius: 10px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 400px;
  margin: auto;
  transition: all 0.3s ease;
  border: 0px solid #e2e8f0;
}

.login-card h1 {
  text-align: center;
  color: #1e293b;
  margin-bottom: 2rem;
  font-size: 2.25rem;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  color: #334155;
  font-weight: 600;
  font-size: 1rem;
}

.form-control {
  width: 100%;
  padding: 0.9rem 1rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.375rem;
  font-size: 1rem;
  background-color: #f7f7f8;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.form-control:focus {
  outline: none;
  border-color: #3b82f6;
  background-color: rgb(245, 240, 240);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

.form-control.is-invalid {
  border-color: #ef4444;
  background-color: #fff1f2;
}

.invalid-feedback {
  color: #dc2626;
  font-size: 0.875rem;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
  color: #4a678f;
}

.btn {
  width: 100%;
  padding: 0.85rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 1.125rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
}

.btn-primary {
  background: #2563eb;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #1d4ed8;
  transform: translateY(-2px);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  display: inline-block;
  width: 1.1rem;
  height: 1.1rem;
  border: 3px solid #ffffff;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-right: 0.6rem;
  vertical-align: middle;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .login-card {
    max-width: 100%;
    padding: 1rem;
  }

  .login-card h1 {
    font-size: 1.75rem;
  }

  .btn {
    font-size: 1rem;
  }
}
</style>

