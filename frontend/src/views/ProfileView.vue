<template>
  <BaseLayout>
    <div class="profile-container card">
      <Toast />
      <div class="card-header">
        <h2>Thông Tin Cá Nhân</h2>
      </div>
      <div class="grid">
        <!-- Thông Tin Cơ Bản -->
        <div class="col-6">
          <div class="card">
            <h3>Thông Tin Cơ Bản</h3>
            <form @submit.prevent="updateProfile" class="p-fluid">
              <div class="field">
                <label for="username">Tên Đăng Nhập</label>
                <InputText
                  id="username"
                  v-model="v$.username.$model"
                  disabled
                  class="p-inputtext-lg"
                />
              </div>
              <div class="field">
                <label for="email">Email</label>
                <InputText
                  id="email"
                  v-model="v$.email.$model"
                  :class="{ 'p-invalid': v$.email.$error }"
                  @input="v$.email.$touch()"
                  class="p-inputtext-lg"
                />
                <small class="p-error" v-if="v$.email.required.$invalid && v$.email.$dirty">
                  Vui lòng nhập email.
                </small>
                <small class="p-error" v-if="v$.email.email.$invalid && v$.email.$dirty">
                  Email không hợp lệ.
                </small>
              </div>
              <div class="field">
                <label for="full_name">Họ và Tên</label>
                <InputText
                  id="full_name"
                  v-model="v$.full_name.$model"
                  :class="{ 'p-invalid': v$.full_name.$error }"
                  @input="v$.full_name.$touch()"
                  class="p-inputtext-lg"
                />
                <small class="p-error" v-if="v$.full_name.required.$invalid && v$.full_name.$dirty">
                  Vui lòng nhập họ và tên.
                </small>
              </div>
              <div class="field">
                <label for="phone">Số Điện Thoại</label>
                <InputText
                  id="phone"
                  v-model="v$.phone.$model"
                  :class="{ 'p-invalid': v$.phone.$error }"
                  @input="v$.phone.$touch()"
                  class="p-inputtext-lg"
                />
                <small class="p-error" v-if="v$.phone.required.$invalid && v$.phone.$dirty">
                  Vui lòng nhập số điện thoại.
                </small>
                <small class="p-error" v-if="v$.phone.phone.$invalid && v$.phone.$dirty">
                  Số điện thoại không hợp lệ.
                </small>
              </div>
              <div class="field">
                <label for="role">Vai Trò</label>
                <InputText
                  id="role"
                  v-model="v$.role.$model"
                  disabled
                  class="p-inputtext-lg"
                />
              </div>
              <div class="form-actions">
                <Button
                  type="submit"
                  label="Cập Nhật"
                  icon="pi pi-check"
                  :loading="isLoading"
                  class="submit-button"
                />
              </div>
            </form>
          </div>
        </div>

        <!-- Thông Tin Bổ Sung -->
        <div class="col-6">
          <div class="card">
            <h3>Thông Tin Bổ Sung</h3>
            <div class="field">
              <label for="address">Địa Chỉ</label>
              <Textarea
                id="address"
                v-model="formData.address"
                rows="3"
                class="p-inputtext-lg"
              />
            </div>
            <div class="field">
              <label for="birth_date">Ngày Sinh</label>
              <Calendar
                id="birth_date"
                v-model="formData.birth_date"
                dateFormat="dd/mm/yy"
                :showIcon="true"
                class="p-inputtext-lg"
              />
            </div>
            <div class="field">
              <label for="gender">Giới Tính</label>
              <Dropdown
                id="gender"
                v-model="formData.gender"
                :options="genderOptions"
                optionLabel="label"
                optionValue="value"
                placeholder="Chọn giới tính"
                class="p-inputtext-lg"
              />
            </div>
            <div class="field">
              <label for="avatar">Ảnh Đại Diện</label>
              <div class="avatar-upload">
                <img
                  v-if="formData.avatar"
                  :src="formData.avatar"
                  alt="Avatar"
                  class="avatar-preview"
                />
                <FileUpload
                  mode="basic"
                  name="avatar"
                  accept="image/*"
                  :maxFileSize="1000000"
                  chooseLabel="Chọn ảnh"
                  @uploader="onUpload"
                  :customUpload="true"
                  class="upload-button"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from '@/composables/useToast'
import { useUserStore } from '@/stores/user'
import { useVuelidate } from '@vuelidate/core'
import { required, email, helpers } from '@vuelidate/validators'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import Calendar from 'primevue/calendar'
import Dropdown from 'primevue/dropdown'
import FileUpload from 'primevue/fileupload'
import Button from 'primevue/button'
import Toast from 'primevue/toast'
import BaseLayout from '@/components/BaseLayout.vue'

const toast = useToast()
const userStore = useUserStore()
const isLoading = ref(false)

const formData = ref({
  username: '',
  email: '',
  full_name: '',
  phone: '',
  role: '',
  address: '',
  birth_date: null,
  gender: null,
  avatar: null,
})

const genderOptions = [
  { label: 'Nam', value: 'male' },
  { label: 'Nữ', value: 'female' },
  { label: 'Khác', value: 'other' },
]

const phoneValidator = helpers.regex(/^[0-9]{10}$/)

const rules = computed(() => ({
  username: { required },
  email: { required, email },
  full_name: { required },
  phone: {
    required,
    phone: helpers.withMessage('Số điện thoại phải là 10 chữ số', phoneValidator),
  },
  role: { required },
}))

const v$ = useVuelidate(rules, formData)

onMounted(async () => {
  await loadProfile()
})

const loadProfile = async () => {
  try {
    const user = await userStore.fetchCurrentUserProfile()
    if (user) {
      formData.value = {
        username: user.username || '',
        email: user.email || '',
        full_name: user.full_name || '',
        phone: user.phone || '',
        role: user.role || '',
        address: user.address || '',
        birth_date: user.birth_date ? new Date(user.birth_date) : null,
        gender: user.gender || null,
        avatar: user.avatar || null,
      }
    }
  } catch (error) {
    toast.addToast({
      severity: 'error',
      summary: 'Lỗi',
      detail: 'Không thể tải thông tin cá nhân',
      life: 3000,
    })
  }
}

const updateProfile = async () => {
  v$.value.$touch()
  if (v$.value.$invalid) return

  isLoading.value = true
  try {
    const profileData = {
      email: formData.value.email,
      full_name: formData.value.full_name,
      phone: formData.value.phone,
      address: formData.value.address,
      birth_date: formData.value.birth_date ? formData.value.birth_date.toISOString().split('T')[0] : null,
      gender: formData.value.gender,
    }
    await userStore.updateProfile(profileData)
    toast.addToast({
      severity: 'success',
      summary: 'Thành Công',
      detail: 'Cập nhật thông tin thành công',
      life: 3000,
    })
  } catch (error) {
    toast.addToast({
      severity: 'error',
      summary: 'Lỗi',
      detail: error.response?.data?.detail || 'Không thể cập nhật thông tin',
      life: 3000,
    })
  } finally {
    isLoading.value = false
  }
}

const onUpload = async (event) => {
  try {
    const formData = new FormData()
    formData.append('avatar', event.files[0])
    const response = await api.post('/api/upload-avatar/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    formData.value.avatar = response.data.avatar_url
    toast.addToast({
      severity: 'success',
      summary: 'Thành Công',
      detail: 'Cập nhật ảnh đại diện thành công',
      life: 3000,
    })
  } catch (error) {
    toast.addToast({
      severity: 'error',
      summary: 'Lỗi',
      detail: 'Không thể tải lên ảnh đại diện',
      life: 3000,
    })
  }
}
</script>

<style scoped>
.profile-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 2rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.card-header {
  margin-bottom: 2rem;
}

.card-header h2 {
  font-size: 2rem;
  color: #2c3e50;
  margin: 0;
  text-align: center;
}

.card {
  padding: 2rem;
  background: #f9fafb;
  border-radius: 8px;
}

.card h3 {
  font-size: 1.5rem;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.grid {
  display: flex;
  gap: 2rem;
}

.col-6 {
  flex: 1;
}

.field {
  margin-bottom: 1.5rem;
}

.field label {
  display: block;
  font-weight: 500;
  color: #34495e;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

:deep(.p-inputtext),
:deep(.p-textarea),
:deep(.p-calendar),
:deep(.p-dropdown) {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  transition: border-color 0.3s;
}

:deep(.p-inputtext:focus),
:deep(.p-textarea:focus),
:deep(.p-calendar .p-inputtext:focus),
:deep(.p-dropdown:focus) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

:deep(.p-invalid) {
  border-color: #ef4444 !important;
}

.p-error {
  color: #ef4444;
  font-size: 0.875rem;
}

.avatar-upload {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.avatar-preview {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #d1d5db;
}

.upload-button {
  font-size: 1rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 2rem;
}

.submit-button {
  font-size: 1rem;
  padding: 0.75rem 1.5rem;
  background: #3b82f6;
  border: none;
  border-radius: 6px;
  transition: background 0.3s;
}

.submit-button:hover {
  background: #2563eb;
}
</style>