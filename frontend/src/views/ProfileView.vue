<template>
  <div class="card">
    <div class="card-header">
      <h2>Thông Tin Cá Nhân</h2>
    </div>

    <div class="grid">
      <div class="col-12 md:col-6">
        <div class="card">
          <h3>Thông Tin Cơ Bản</h3>
          <div class="field">
            <label for="username">Tên Đăng Nhập</label>
            <InputText id="username" v-model="profile.username" disabled />
          </div>
          <div class="field">
            <label for="email">Email</label>
            <InputText id="email" v-model="profile.email" :class="{ 'p-invalid': submitted && !profile.email }" />
            <small class="p-error" v-if="submitted && !profile.email">Vui lòng nhập email.</small>
          </div>
          <div class="field">
            <label for="full_name">Họ và Tên</label>
            <InputText id="full_name" v-model="profile.full_name" :class="{ 'p-invalid': submitted && !profile.full_name }" />
            <small class="p-error" v-if="submitted && !profile.full_name">Vui lòng nhập họ và tên.</small>
          </div>
          <div class="field">
            <label for="phone">Số Điện Thoại</label>
            <InputText id="phone" v-model="profile.phone" :class="{ 'p-invalid': submitted && !profile.phone }" />
            <small class="p-error" v-if="submitted && !profile.phone">Vui lòng nhập số điện thoại.</small>
          </div>
          <div class="field">
            <label for="role">Vai Trò</label>
            <InputText id="role" v-model="profile.role" disabled />
          </div>
          <div class="flex justify-content-end">
            <Button label="Cập Nhật" icon="pi pi-check" @click="updateProfile" />
          </div>
        </div>
      </div>

      <div class="col-12 md:col-6">
        <div class="card">
          <h3>Thông Tin Bổ Sung</h3>
          <div class="field">
            <label for="address">Địa Chỉ</label>
            <Textarea id="address" v-model="profile.address" rows="3" />
          </div>
          <div class="field">
            <label for="birth_date">Ngày Sinh</label>
            <Calendar id="birth_date" v-model="profile.birth_date" dateFormat="dd/mm/yy" />
          </div>
          <div class="field">
            <label for="gender">Giới Tính</label>
            <Dropdown
              id="gender"
              v-model="profile.gender"
              :options="genderOptions"
              optionLabel="label"
              optionValue="value"
              placeholder="Chọn giới tính"
            />
          </div>
          <div class="field">
            <label for="avatar">Ảnh Đại Diện</label>
            <div class="flex align-items-center gap-3">
              <img v-if="profile.avatar" :src="profile.avatar" alt="Avatar" class="avatar-preview" />
              <FileUpload
                mode="basic"
                name="avatar"
                accept="image/*"
                :maxFileSize="1000000"
                chooseLabel="Chọn ảnh"
                @upload="onUpload"
                :auto="true"
                customUpload
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { api } from '@/services/api'

const toast = useToast()
const profile = ref({})
const submitted = ref(false)

const genderOptions = [
  { label: 'Nam', value: 'male' },
  { label: 'Nữ', value: 'female' },
  { label: 'Khác', value: 'other' }
]

onMounted(async () => {
  await loadProfile()
})

const loadProfile = async () => {
  try {
    profile.value = await api.getProfile()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải thông tin cá nhân', life: 3000 })
  }
}

const updateProfile = async () => {
  submitted.value = true

  if (profile.value.email?.trim() && profile.value.full_name?.trim() && profile.value.phone?.trim()) {
    try {
      await api.updateProfile(profile.value)
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật thông tin thành công', life: 3000 })
      submitted.value = false
    } catch (error) {
      toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể cập nhật thông tin', life: 3000 })
    }
  }
}

const onUpload = async (event) => {
  try {
    const formData = new FormData()
    formData.append('avatar', event.files[0])
    const response = await api.uploadAvatar(formData)
    profile.value.avatar = response.avatar_url
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật ảnh đại diện thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải lên ảnh đại diện', life: 3000 })
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

.card h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  font-size: 1.25rem;
  color: var(--text-color);
}

.field {
  margin-bottom: 1.5rem;
}

.field label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.avatar-preview {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
}

:deep(.p-fileupload-buttonbar) {
  padding: 0;
}

:deep(.p-fileupload-content) {
  padding: 0;
}
</style> 