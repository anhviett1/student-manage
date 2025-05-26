<template>
  <div class="card">
    <div class="card-header">
      <h2>Đổi Mật Khẩu</h2>
    </div>

    <div class="card">
      <form @submit.prevent="changePassword" class="p-fluid">
        <div class="field">
          <label for="current_password">Mật Khẩu Hiện Tại</label>
          <Password
            id="current_password"
            v-model="password.current_password"
            :feedback="false"
            toggleMask
            :class="{ 'p-invalid': submitted && !password.current_password }"
          />
          <small class="p-error" v-if="submitted && !password.current_password">Vui lòng nhập mật khẩu hiện tại.</small>
        </div>

        <div class="field">
          <label for="new_password">Mật Khẩu Mới</label>
          <Password
            id="new_password"
            v-model="password.new_password"
            toggleMask
            :class="{ 'p-invalid': submitted && !password.new_password }"
          />
          <small class="p-error" v-if="submitted && !password.new_password">Vui lòng nhập mật khẩu mới.</small>
        </div>

        <div class="field">
          <label for="confirm_password">Xác Nhận Mật Khẩu Mới</label>
          <Password
            id="confirm_password"
            v-model="password.confirm_password"
            :feedback="false"
            toggleMask
            :class="{ 'p-invalid': submitted && !password.confirm_password }"
          />
          <small class="p-error" v-if="submitted && !password.confirm_password">Vui lòng xác nhận mật khẩu mới.</small>
          <small class="p-error" v-if="submitted && password.new_password !== password.confirm_password">
            Mật khẩu xác nhận không khớp.
          </small>
        </div>

        <div class="flex justify-content-end">
          <Button type="submit" label="Đổi Mật Khẩu" icon="pi pi-check" />
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useToast } from 'primevue/usetoast'
import { api } from '@/services/api'

const toast = useToast()
const password = ref({
  current_password: '',
  new_password: '',
  confirm_password: ''
})
const submitted = ref(false)

const changePassword = async () => {
  submitted.value = true

  if (
    password.value.current_password?.trim() &&
    password.value.new_password?.trim() &&
    password.value.confirm_password?.trim() &&
    password.value.new_password === password.value.confirm_password
  ) {
    try {
      await api.changePassword(password.value)
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Đổi mật khẩu thành công', life: 3000 })
      // Reset form
      password.value = {
        current_password: '',
        new_password: '',
        confirm_password: ''
      }
      submitted.value = false
    } catch (error) {
      toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể đổi mật khẩu', life: 3000 })
    }
  }
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.card-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: var(--text-color);
}

.card {
  padding: 1.5rem;
}

.field {
  margin-bottom: 1.5rem;
}

.field label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

:deep(.p-password) {
  width: 100%;
}

:deep(.p-password-input) {
  width: 100%;
}
</style> 