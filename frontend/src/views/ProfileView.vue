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
          <div class="card-inner">
            <h3>Thông Tin Cơ Bản</h3>
            <form @submit.prevent="updateProfile" class="p-fluid">
              <div class="field">
                <label for="username">Tên Đăng Nhập</label>
                <InputText id="username" v-model="formData.username" disabled />
              </div>
              <div class="field">
                <label for="email">Email</label>
                <InputText
                  id="email"
                  v-model="v$.email.$model"
                  :class="{ 'p-invalid': v$.email.$error }"
                  @input="v$.email.$touch()"
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
                />
                 <small class="p-error" v-if="v$.phone.phone.$invalid && v$.phone.$dirty">
                  Số điện thoại không hợp lệ (yêu cầu 10 số).
                </small>
              </div>
              <div class="field">
                <label for="role">Vai Trò</label>
                <InputText id="role" v-model="formData.role" disabled />
              </div>
            </form>
          </div>
        </div>

        <!-- Thông Tin Bổ Sung -->
        <div class="col-6">
          <div class="card-inner">
            <h3>Thông Tin Bổ Sung</h3>
            <div class="field">
              <label for="address">Địa Chỉ</label>
              <Textarea id="address" v-model="formData.address" rows="3" />
            </div>
            <div class="field">
              <label for="birth_date">Ngày Sinh</label>
              <Calendar id="birth_date" v-model="formData.birth_date" dateFormat="yy-mm-dd" :showIcon="true" />
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
              />
            </div>
            <div class="field">
              <label for="avatar">Ảnh Đại Diện</label>
              <div class="avatar-upload">
                <img v-if="formData.avatar" :src="formData.avatar" alt="Avatar" class="avatar-preview" />
                <FileUpload
                  mode="basic"
                  name="avatar"
                  accept="image/*"
                  :maxFileSize="1000000"
                  chooseLabel="Chọn ảnh"
                  @uploader="onUpload"
                  :customUpload="true"
                  class="upload-button"
                  :disabled="!canUploadAvatar"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="form-actions">
        <Button
          type="button"
          label="Cập Nhật Hồ Sơ"
          icon="pi pi-check"
          :loading="isLoading"
          class="submit-button"
          @click="updateProfile"
          :disabled="!canEditProfile"
        />
      </div>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
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
import { usePermissions } from '@/composables/usePermissions'
import api, { endpoints } from '@/services/api'
import { useAuthStore } from '@/stores/auth'

const toast = useToast()
const userStore = useUserStore()
const authStore = useAuthStore()
const isLoading = ref(false)
const { isTeacher, isStudent, canEditProfile, canUploadAvatar } = usePermissions()

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
  { label: 'Nam', value: 'M' },
  { label: 'Nữ', value: 'F' },
  { label: 'Khác', value: 'O' },
]

const phoneValidator = helpers.regex(/^(0|\+84)[3|5|7|8|9][0-9]{8}$/)

const rules = computed(() => ({
  email: { required, email },
  full_name: { required },
  phone: { phone: helpers.withMessage('Số điện thoại không hợp lệ.', phoneValidator) },
}))

const v$ = useVuelidate(rules, formData)

onMounted(async () => {
  await fetchProfile()
})

const fetchProfile = async () => {
  try {
    const user = authStore.user
    if (!user) {
       await authStore.fetchCurrentUser()
    }
    
    let profileEndpoint = ''
    if (isStudent.value) {
      profileEndpoint = `${endpoints.students}me/`
    } else if (isTeacher.value) {
      profileEndpoint = `${endpoints.teachers}me/`
    }

    if (profileEndpoint) {
      const { data } = await api.get(profileEndpoint)
      // The actual profile data might be nested
      const profileData = data.data || data
      formData.value = { ...authStore.user, ...profileData }
    } else {
      formData.value = { ...authStore.user }
    }

  } catch (error) {
    console.error('Error fetching profile:', error)
    toast.add({
      severity: 'error',
      summary: 'Lỗi',
      detail: 'Không thể tải thông tin hồ sơ',
      life: 3000,
    })
  }
}


const updateProfile = async () => {
  v$.value.$touch()
  if (v$.value.$invalid) {
     toast.add({ severity: 'warn', summary: 'Dữ liệu không hợp lệ', detail: 'Vui lòng kiểm tra lại các trường thông tin.', life: 3000 });
     return
  }

  isLoading.value = true
  try {
    const profileData = {
      email: formData.value.email,
      full_name: formData.value.full_name,
      phone: formData.value.phone,
      address: formData.value.address,
      birth_date: formData.value.birth_date ? new Date(formData.value.birth_date).toISOString().split('T')[0] : null,
      gender: formData.value.gender,
      // Include other fields specific to student/teacher if needed
    }
    
    // Determine the correct endpoint to update
    let updateEndpoint = ''
     if (isStudent.value) {
      updateEndpoint = `${endpoints.students}${formData.value.id}/`
    } else if (isTeacher.value) {
      updateEndpoint = `${endpoints.teachers}${formData.value.id}/`
    } else { // Admin
      updateEndpoint = endpoints.userProfile
    }
    
    await api.patch(updateEndpoint, profileData);

    toast.add({
      severity: 'success',
      summary: 'Thành Công',
      detail: 'Cập nhật thông tin thành công',
      life: 3000,
    })
    await authStore.fetchCurrentUser() // Refresh user data in store
  } catch (error) {
    toast.add({
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
  if (!canUploadAvatar.value) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Bạn không có quyền tải lên ảnh đại diện.', life: 3000 });
    return;
  }
  
  try {
    const file = event.files[0];
    const uploadFormData = new FormData()
    uploadFormData.append('avatar', file)

    const response = await api.post(endpoints.uploadAvatar, uploadFormData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    
    formData.value.avatar = response.data.avatar_url; // Assuming the response contains the new URL
    await authStore.fetchCurrentUser(); // Refresh auth store to get new avatar URL everywhere

    toast.add({
      severity: 'success',
      summary: 'Thành Công',
      detail: 'Cập nhật ảnh đại diện thành công',
      life: 3000,
    })
  } catch (error) {
    toast.add({
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
  text-align: center;
}

.card-header h2 {
  font-size: 2rem;
  color: #2c3e50;
  margin: 0;
}

.card-inner {
  padding: 2rem;
  background: #f9fafb;
  border-radius: 8px;
  height: 100%;
}

.card-inner h3 {
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
:deep(.p-calendar .p-inputtext),
:deep(.p-dropdown) {
  width: 100%;
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

.form-actions {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

.submit-button {
  font-size: 1rem;
  padding: 0.75rem 2.5rem;
}
</style>