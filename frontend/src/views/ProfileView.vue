<template>
    <div class="profile-container card">
      <Toast />
      <div class="card-header">
        <h2>Thông Tin Cá Nhân</h2>
      </div>
      <div class="avatar-section" style="text-align:center; margin-bottom:2rem;">
        <img v-if="userProfile.profile_picture" :src="userProfile.profile_picture" alt="Avatar" class="avatar-preview" />
        <div v-else class="avatar-placeholder">Không có ảnh</div>
        <FileUpload v-if="canUploadAvatar"
          mode="basic"
          name="avatar"
          accept="image/*"
          :maxFileSize="1000000"
          chooseLabel="Chọn ảnh"
          @uploader="onUpload"
          :customUpload="true"
          class="upload-button"
        />
        <Button 
        v-if="userProfile.profile_picture"
        label="Xóa ảnh" 
        severity="danger"
        @click="deleteAvatar"
        :disabled="!canUploadAvatar"
      />
      </div>
      <form @submit.prevent="updateProfile">
        <table class="profile-table">
          <tbody>
            <tr v-for="(value, key) in userProfile" :key="key">
              <td class="profile-key">{{ getFieldLabel(key) }}</td>
              <td class="profile-value">
                <template v-if="isEditable(key)">
                  <component
                    :is="getInputComponent(key)"
                    v-model="editProfile[key]"
                    v-bind="getInputProps(key, value)"
                  />
                </template>
                <template v-else>
                  <span v-if="isObject(value)">{{ formatObjectValue(key, value) }}</span>
                  <span v-else>{{ formatValue(key, value) }}</span>
                </template>
              </td>
            </tr>
          </tbody>
        </table>
        <div class="form-actions">
          <Button
            type="submit"
            label="Lưu"
            icon="pi pi-check"
            :loading="isLoading"
            class="submit-button"
            :disabled="!canEditProfile"
          />
        </div>
      </form>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useUserStore } from '@/stores/user'
import { usePermissions } from '@/composables/usePermissions'
import { useAuthStore } from '@/stores/auth'
import FileUpload from 'primevue/fileupload'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Dropdown from 'primevue/dropdown'
import Calendar from 'primevue/calendar'
import Textarea from 'primevue/textarea'

const toast = useToast()
const userStore = useUserStore()
const authStore = useAuthStore()
const { canEditProfile, canUploadAvatar } = usePermissions()
const isLoading = ref(false)

const userProfile = ref({})
const editProfile = ref({})

onMounted(async () => {
  await fetchProfile()
})

const fetchProfile = async () => {
  try {
    let user = authStore.user
    if (!user) {
      user = await authStore.fetchCurrentUser()
    }
    userProfile.value = { ...user }
    editProfile.value = { ...user }
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải thông tin hồ sơ', life: 3000 })
  }
}

const isEditable = (key) => {
  // Chỉ cho phép chỉnh sửa các trường này, bạn có thể mở rộng thêm
  const editableFields = ['email', 'full_name', 'phone', 'address', 'birth_date', 'gender']
  return editableFields.includes(key)
}

const getInputComponent = (key) => {
  if (key === 'gender') return Dropdown
  if (key === 'birth_date' || key === 'date_of_birth') return Calendar
  if (key === 'address') return Textarea
  return InputText
}

const getInputProps = (key, value) => {
  if (key === 'gender') {
    return {
      options: [
        { label: 'Nam', value: 'M' },
        { label: 'Nữ', value: 'F' },
        { label: 'Khác', value: 'O' },
      ],
      optionLabel: 'label',
      optionValue: 'value',
      placeholder: 'Chọn giới tính',
    }
  }
  if (key === 'birth_date' || key === 'date_of_birth') {
    return {
      dateFormat: 'yy-mm-dd',
      showIcon: true,
    }
  }
  if (key === 'address') {
    return {
      rows: 2,
    }
  }
  return {}
}

const isObject = (val) => val && typeof val === 'object' && !Array.isArray(val)

const formatObjectValue = (key, value) => {
  // Nếu là object có trường name thì hiển thị name, không thì stringify
  if (value && value.name) return value.name
  return JSON.stringify(value)
}

const formatValue = (key, value) => {
  if (key === 'gender') {
    if (value === 'M') return 'Nam'
    if (value === 'F') return 'Nữ'
    if (value === 'O') return 'Khác'
  }
  return value
}

const getFieldLabel = (key) => {
  // Map key sang label tiếng Việt, có thể mở rộng thêm
  const map = {
    username: 'Tên đăng nhập',
    email: 'Email',
    full_name: 'Họ và tên',
    phone: 'Số điện thoại',
    role: 'Vai trò',
    address: 'Địa chỉ',
    birth_date: 'Ngày sinh',
    date_of_birth: 'Ngày sinh',
    gender: 'Giới tính',
    avatar: 'Ảnh đại diện',
    id: 'ID',
    is_active: 'Hoạt động',
    is_staff: 'Nhân viên',
    is_superuser: 'Superuser',
    last_login: 'Đăng nhập gần nhất',
    date_joined: 'Ngày tạo',
    permissions: 'Quyền',
    groups: 'Nhóm',
  }
  return map[key] || key
}

const updateProfile = async () => {
  isLoading.value = true
  try {
    // Chỉ gửi các trường cho phép chỉnh sửa
    const payload = {}
    Object.keys(editProfile.value).forEach((key) => {
      if (isEditable(key)) payload[key] = editProfile.value[key]
    })
    await userStore.updateProfile(payload)
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật thông tin thành công', life: 3000 })
    await fetchProfile()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể cập nhật thông tin', life: 3000 })
  } finally {
    isLoading.value = false
  }
}

const onUpload = async (event) => {
  if (!canUploadAvatar.value) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Bạn không có quyền tải lên ảnh đại diện.', life: 3000 })
    return
  }
  try {
    const file = event.files[0]
    const formData = new FormData()
    formData.append('avatar', file)  // Đúng tên field mà backend mong đợi

    // Gọi API uploadAvatar riêng biệt
    const response = await api.post(endpoints.uploadAvatar, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    // Cập nhật avatar_url mới
    const avatarUrl = response.data.avatar_url
    if (avatarUrl) {
      userProfile.value.profile_picture = avatarUrl  // Sửa thành profile_picture
    }

    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật ảnh đại diện thành công', life: 3000 })
    await fetchProfile()  // Tải lại profile
  } catch (error) {
    let errorMessage = 'Không thể tải lên ảnh đại diện'
    if (error.response?.data?.error) {
      errorMessage = error.response.data.error
    }
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errorMessage, life: 3000 })
  }
}

const deleteAvatar = async () => {
  try {
    await api.delete(endpoints.uploadAvatar)
    userProfile.value.profile_picture = null
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Đã xóa ảnh đại diện', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Xóa ảnh thất bại', life: 3000 })
  }
}
</script>

<style scoped>
.profile-container {
  max-width: 900px;
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
.avatar-section {
  margin-bottom: 2rem;
}
.avatar-preview {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #d1d5db;
  margin-bottom: 1rem;
}
.profile-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 2rem;
}
.profile-key {
  font-weight: 500;
  color: #34495e;
  padding: 0.75rem 1rem;
  background: #f8fafb;
  width: 200px;
}
.profile-value {
  padding: 0.75rem 1rem;
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