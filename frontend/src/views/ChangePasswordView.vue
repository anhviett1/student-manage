<template>
  <div class="change-password-container">
    <Toast />
    <div class="card">
      <div class="card-header">
        <h2>Đổi Mật Khẩu</h2>
      </div>
      <form @submit.prevent="changePassword" class="p-fluid">
        <div class="field">
          <label for="current_password">Mật Khẩu Hiện Tại</label>
          <Password
            id="current_password"
            v-model="formData.current_password"
            :feedback="false"
            toggleMask
            :class="{ 'p-invalid': v$.current_password.$error }"
            @input="v$.current_password.$touch()"
          />
          <small class="p-error" v-if="v$.current_password.required.$invalid && v$.current_password.$dirty">
            Vui lòng nhập mật khẩu hiện tại.
          </small>
        </div>

        <div class="field">
          <label for="new_password">Mật Khẩu Mới</label>
          <Password
            id="new_password"
            v-model="formData.new_password"
            :feedback="true"
            toggleMask
            :class="{ 'p-invalid': v$.new_password.$error }"
            @input="v$.new_password.$touch()"
          />
          <small class="p-error" v-if="v$.new_password.required.$invalid && v$.new_password.$dirty">
            Vui lòng nhập mật khẩu mới.
          </small>
          <small class="p-error" v-if="v$.new_password.minLength.$invalid && v$.new_password.$dirty">
            Mật khẩu mới phải có ít nhất 8 ký tự.
          </small>
          <small class="p-error" v-if="v$.new_password.strongPassword.$invalid && v$.new_password.$dirty">
            Mật khẩu phải chứa chữ hoa, chữ thường, số và ký tự đặc biệt.
          </small>
        </div>

        <div class="field">
          <label for="confirm_password">Xác Nhận Mật Khẩu Mới</label>
          <Password
            id="confirm_password"
            v-model="formData.confirm_password"
            :feedback="false"
            toggleMask
            :class="{ 'p-invalid': v$.confirm_password.$error }"
            @input="v$.confirm_password.$touch()"
          />
          <small class="p-error" v-if="v$.confirm_password.required.$invalid && v$.confirm_password.$dirty">
            Vui lòng xác nhận mật khẩu mới.
          </small>
          <small class="p-error" v-if="v$.confirm_password.sameAsPassword.$invalid && v$.confirm_password.$dirty">
            Mật khẩu xác nhận không khớp.
          </small>
        </div>

        <div class="form-actions">
          <Button
            type="submit"
            label="Đổi Mật Khẩu"
            icon="pi pi-check"
            :loading="isLoading"
            class="submit-button"
          />
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useUserStore } from '@/stores/user'
import { useVuelidate } from '@vuelidate/core'
import { required, minLength, helpers } from '@vuelidate/validators'
import Password from 'primevue/password'
import Button from 'primevue/button'
import Toast from 'primevue/toast'

const toast = useToast()
const userStore = useUserStore()

const formData = ref({
  current_password: '',
  new_password: '',
  confirm_password: '',
})

const isLoading = ref(false)

const strongPassword = helpers.regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/)

const rules = computed(() => ({
  current_password: { required },
  new_password: {
    required,
    minLength: minLength(8),
    strongPassword: helpers.withMessage('Mật khẩu phải mạnh', strongPassword),
  },
  confirm_password: {
    required,
    sameAsPassword: helpers.withMessage('Mật khẩu xác nhận không khớp', (value) => value === formData.value.new_password),
  },
}))

const v$ = useVuelidate(rules, formData)

const changePassword = async () => {
  v$.value.$touch()
  if (v$.value.$invalid) return

  isLoading.value = true
  try {
    await userStore.changePassword({
      old_password: formData.value.current_password,
      new_password: formData.value.new_password,
    })
    toast.add({
      severity: 'success',
      summary: 'Thành Công',
      detail: 'Đổi mật khẩu thành công',
      life: 3000,
    })
    // Reset form
    formData.value = {
      current_password: '',
      new_password: '',
      confirm_password: '',
    }
    v$.value.$reset()
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Lỗi',
      detail: error.response?.data?.detail || 'Không thể đổi mật khẩu',
      life: 3000,
    })
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.change-password-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f4f6f9;
  padding: 1rem;
}

.card {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  width: 100%;
}

.card-header {
  margin-bottom: 1.5rem;
}

.card-header h2 {
  font-size: 1.75rem;
  color: #2c3e50;
  margin: 0;
  text-align: center;
}

.field {
  margin-bottom: 1.5rem;
}

.field label {
  display: block;
  font-weight: 500;
  color: #34495e;
  margin-bottom: 0.5rem;
}

:deep(.p-password) {
  width: 100%;
}

:deep(.p-password-input) {
  width: 100%;
  padding: 0.75rem;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  transition: border-color 0.3s;
}

:deep(.p-password-input:focus) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

:deep(.p-invalid .p-password-input) {
  border-color: #ef4444;
}

.p-error {
  font-size: 0.875rem;
  color: #ef4444;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

.submit-button {
  font-size: 1rem;
  padding: 0.75rem 1.5rem;
}

@media (max-width: 480px) {
  .card {
    padding: 1.5rem;
  }

  .card-header h2 {
    font-size: 1.5rem;
  }
}
</style>