<template>
  <div class="login-container">
    <div class="login-card">
      <h1>Login</h1>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Username</label>
          <InputText
            id="username"
            v-model="credentials.username"
            :class="{ 'p-invalid': submitted && !credentials.username }"
            required
            autofocus
          />
          <small class="p-error" v-if="submitted && !credentials.username">Username is required.</small>
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <Password
            id="password"
            v-model="credentials.password"
            :feedback="false"
            toggleMask
            :class="{ 'p-invalid': submitted && !credentials.password }"
            required
          />
          <small class="p-error" v-if="submitted && !credentials.password">Password is required.</small>
        </div>

        <div class="form-actions">
          <Button
            type="submit"
            label="Login"
            icon="pi pi-sign-in"
            :loading="loading"
            class="w-full"
          />
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/stores/auth'
import { api } from '@/services/api'

const router = useRouter()
const toast = useToast()
const authStore = useAuthStore()

const credentials = ref({
  username: '',
  password: ''
})
const submitted = ref(false)
const loading = ref(false)

const handleLogin = async () => {
  submitted.value = true

  if (credentials.value.username && credentials.value.password) {
    try {
      loading.value = true
      const response = await api.login(credentials.value)
      
      authStore.setToken(response.token)
      authStore.setUser(response.user)
      
      toast.add({
        severity: 'success',
        summary: 'Success',
        detail: 'Login successful',
        life: 3000
      })

      router.push('/')
    } catch (error) {
      toast.add({
        severity: 'error',
        summary: 'Error',
        detail: error.message || 'Invalid credentials',
        life: 3000
      })
    } finally {
      loading.value = false
    }
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
  padding: 1rem;
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.login-card h1 {
  text-align: center;
  color: var(--text-color);
  margin-bottom: 2rem;
  font-size: 1.75rem;
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

.form-group label {
  font-weight: 500;
  color: var(--text-color);
}

.form-actions {
  margin-top: 1rem;
}

:deep(.p-password) {
  width: 100%;
}

:deep(.p-password-input) {
  width: 100%;
}

:deep(.p-button) {
  width: 100%;
}
</style> 