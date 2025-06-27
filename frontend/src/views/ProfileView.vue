<template>
  <div class="profile-container card">
    <Toast />
    <div class="card-header">
      <h2>Thông Tin Cá Nhân</h2>
      <div>
        <Button 
          :label="isEditMode ? 'Chế độ Xem' : 'Chỉnh sửa'" 
          :icon="isEditMode ? 'pi pi-eye' : 'pi pi-pencil'"
          :severity="isEditMode ? 'secondary' : 'primary'"
          @click="toggleEditMode"
          class="mode-toggle-button"
          :disabled="!canEditProfile"
        />
        <Button 
          label="Quản lý trường hiển thị" 
          icon="pi pi-cog"
          severity="secondary"
          @click="showFieldConfig = true"
          class="field-config-button"
        />
      </div>
    </div>
    <div class="avatar-section" style="text-align:center; margin-bottom:2rem;">
      <img v-if="userProfile.profile_picture" :src="userProfile.profile_picture" alt="Avatar" class="avatar-preview" />
      <div v-else class="avatar-placeholder">Không có ảnh</div>
      <FileUpload v-if="canUploadAvatar && isEditMode"
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
        v-if="userProfile.profile_picture && isEditMode"
        label="Xóa ảnh" 
        severity="danger"
        @click="deleteAvatar"
        :disabled="!canUploadAvatar"
      />
    </div>
    <form @submit.prevent="updateProfile" v-if="isEditMode">
      <table class="profile-table">
        <tbody>
          <tr v-for="(value, key) in filteredUserProfile" :key="key">
            <td class="profile-key">{{ getFieldLabel(key) }}</td>
            <td class="profile-value">
              <template v-if="isEditable(key)">
                <component
                  :is="getInputComponent(key)"
                  v-model="editProfile[key]"
                  v-bind="getInputProps(key, value)"
                />
                <small class="field-description">{{ getFieldDescription(key) }}</small>
              </template>
              <template v-else>
                <span v-if="isObject(value)">{{ formatObjectValue(key, value) }}</span>
                <span v-else>{{ formatValue(key, value) }}</span>
                <small class="field-description">{{ getFieldDescription(key) }}</small>
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
    <table v-else class="profile-table">
      <tbody>
        <tr v-for="(value, key) in filteredUserProfile" :key="key">
          <td class="profile-key">{{ getFieldLabel(key) }}</td>
          <td class="profile-value">
            <span v-if="isObject(value)">{{ formatObjectValue(key, value) }}</span>
            <span v-else>{{ formatValue(key, value) }}</span>
            <small class="field-description">{{ getFieldDescription(key) }}</small>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Modal cho cấu hình trường -->
    <Dialog v-model:visible="showFieldConfig" header="Quản lý trường hiển thị" modal :style="{ width: '500px' }">
      <div class="field-config">
        <div v-for="(field, key) in fieldMap" :key="key" class="field-config-item">
          <Checkbox v-model="field.visible" :inputId="key" :value="true" />
          <label :for="key" class="ml-2">{{ field.label }}</label>
          <InputText
            v-model="field.label"
            class="ml-2"
            placeholder="Tên hiển thị"
            style="width: 200px"
          />
        </div>
      </div>
      <template #footer>
        <Button label="Lưu" icon="pi pi-check" @click="saveFieldConfig" />
        <Button label="Hủy" icon="pi pi-times" severity="secondary" @click="showFieldConfig = false" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useUserStore } from '@/stores/user'
import { useAuthStore } from '@/stores/auth'
import { usePermissions } from '@/composables/usePermissions'
import FileUpload from 'primevue/fileupload'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Dropdown from 'primevue/dropdown'
import Calendar from 'primevue/calendar'
import Textarea from 'primevue/textarea'
import Dialog from 'primevue/dialog'
import Checkbox from 'primevue/checkbox'

const toast = useToast()
const userStore = useUserStore()
const authStore = useAuthStore()
const { canEditProfile, canUploadAvatar } = usePermissions()
const isLoading = ref(false)
const showFieldConfig = ref(false)
const isEditMode = ref(false) // Thêm biến trạng thái chế độ chỉnh sửa

const userProfile = ref({})
const editProfile = ref({})
const fieldMap = ref({
  id: { label: 'ID', visible: false, description: 'Mã định danh duy nhất của người dùng' },
  username: { label: 'Tên đăng nhập', visible: false, description: 'Tên dùng để đăng nhập hệ thống' },
  email: { label: 'Email', visible: true, description: 'Địa chỉ email để liên hệ và đăng nhập' },
  full_name: { label: 'Họ và tên', visible: true, description: 'Tên đầy đủ của người dùng' },
  phone: { label: 'Số điện thoại', visible: true, description: 'Số điện thoại liên hệ' },
  address: { label: 'Địa chỉ', visible: true, description: 'Địa chỉ hiện tại của người dùng' },
  birth_date: { label: 'Ngày sinh', visible: true, description: 'Ngày sinh theo định dạng YYYY-MM-DD' },
  gender: { label: 'Giới tính', visible: true, description: 'Giới tính: Nam, Nữ hoặc Khác' },
  role: { label: 'Vai trò', visible: false, description: 'Vai trò của người dùng trong hệ thống' },
  is_active: { label: 'Hoạt động', visible: false, description: 'Trạng thái hoạt động của tài khoản' },
  is_staff: { label: 'Nhân viên', visible: false, description: 'Người dùng có phải là nhân viên' },
  is_superuser: { label: 'Superuser', visible: false, description: 'Người dùng có quyền quản trị' },
  last_login: { label: 'Đăng nhập gần nhất', visible: false, description: 'Thời điểm đăng nhập gần nhất' },
  last_login_ip: { label: 'IP đăng nhập gần nhất', visible: false, description: 'Địa chỉ IP của lần đăng nhập gần nhất' },
  date_joined: { label: 'Ngày tạo tài khoản', visible: false, description: 'Ngày tạo tài khoản người dùng' },
  created_at: { label: 'Ngày tạo', visible: false, description: 'Thời điểm tạo tài khoản' },
  updated_at: { label: 'Ngày cập nhật', visible: false, description: 'Thời điểm cập nhật thông tin gần nhất' },
  profile_picture: { label: 'Ảnh đại diện', visible: false, description: 'Ảnh đại diện của người dùng' },
})

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

const filteredUserProfile = computed(() => {
  const filtered = {}
  Object.keys(userProfile.value).forEach((key) => {
    if (fieldMap.value[key]?.visible) {
      filtered[key] = userProfile.value[key]
    }
  })
  return filtered
})

const isEditable = (key) => {
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
  return fieldMap.value[key]?.label || key
}

const getFieldDescription = (key) => {
  return fieldMap.value[key]?.description || ''
}

const saveFieldConfig = () => {
  showFieldConfig.value = false
  toast.add({ severity: 'success', summary: 'Thành công', detail: 'Đã cập nhật cấu hình trường hiển thị', life: 3000 })
}

const toggleEditMode = () => {
  isEditMode.value = !isEditMode.value
  if (!isEditMode.value) {
    editProfile.value = { ...userProfile.value } // Reset editProfile khi thoát chế độ chỉnh sửa
  }
}

const updateProfile = async () => {
  isLoading.value = true
  try {
    const payload = {}
    Object.keys(editProfile.value).forEach((key) => {
      if (isEditable(key)) payload[key] = editProfile.value[key]
    })
    await userStore.updateProfile(payload)
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật thông tin thành công', life: 3000 })
    await fetchProfile()
    isEditMode.value = false // Chuyển về chế độ xem sau khi lưu
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
    formData.append('avatar', file)
    const response = await api.post(endpoints.uploadAvatar, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    const avatarUrl = response.data.avatar_url
    if (avatarUrl) {
      userProfile.value.profile_picture = avatarUrl
    }
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật ảnh đại diện thành công', life: 3000 })
    await fetchProfile()
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
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.mode-toggle-button, .field-config-button {
  font-size: 0.9rem;
  padding: 0.5rem 1.5rem;
  margin-left: 1rem;
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
.field-description {
  display: block;
  color: #6b7280;
  font-size: 0.8rem;
  margin-top: 0.5rem;
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
.field-config-item {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}
</style>