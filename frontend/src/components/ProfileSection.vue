<template>
  <div class="profile-section" aria-label="Phần thông tin cá nhân">
    <div class="card-header">
      <h2 class="card-title">Thông Tin Cá Nhân</h2>
      <div class="header-buttons">
        <Button
          :label="isEditMode ? 'Chế độ Xem' : 'Chỉnh sửa'"
          :icon="isEditMode ? 'pi pi-eye' : 'pi pi-pencil'"
          :severity="isEditMode ? 'secondary' : 'primary'"
          @click="handleProfileViewEditClick"
          class="mode-toggle-button"
          :disabled="!canEditProfile"
          :aria-label="isEditMode ? 'Chuyển sang chế độ xem' : 'Chuyển sang chế độ chỉnh sửa'"
        />
        <Button
          label="Đổi mật khẩu"
          icon="pi pi-key"
          severity="warning"
          @click="navigateToChangePassword"
          class="mode-toggle-button"
          aria-label="Chuyển đến trang đổi mật khẩu"
        />
      </div>
    </div>
    <div class="avatar-section">
      <div
        class="avatar-wrapper"
        @click="canEditProfile && isEditMode ? triggerFileInput() : null"
        :aria-label="canEditProfile && isEditMode ? 'Chọn ảnh đại diện' : 'Ảnh đại diện'"
        role="button"
        tabindex="0"
        @keydown.enter="canEditProfile && isEditMode ? triggerFileInput() : null"
      >
        <img
          v-if="userProfile.profile_picture"
          :src="userProfile.profile_picture"
          alt="Ảnh đại diện"
          class="avatar-preview"
        />
        <img
          v-else-if="userRole === 'admin' && adminDefaultImg"
          :src="adminDefaultImg"
          alt="Ảnh mặc định admin"
          class="avatar-preview"
        />
        <div v-else class="avatar-placeholder">Không có ảnh</div>
        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          class="hidden"
          @change="onFileChange"
          aria-label="Tải lên ảnh đại diện"
        />
      </div>
      <Dialog v-model:visible="showCropper" header="Cắt ảnh đại diện" modal class="avatar-dialog" aria-labelledby="cropper-header">
        <h3 id="cropper-header" class="sr-only">Cắt ảnh đại diện</h3>
        <Cropper
          v-if="tempImage"
          :src="tempImage"
          :stencil-props="{ aspectRatio: 1 }"
          :autoZoom="true"
          :stencil-component="'circle-stencil'"
          @change="onCrop"
          aria-label="Công cụ cắt ảnh đại diện"
        />
        <template #footer>
          <Button label="Hủy" @click="showCropper = false" class="cancel-button" aria-label="Hủy cắt ảnh" />
          <Button label="Lưu" @click="saveCroppedImage" aria-label="Lưu ảnh đã cắt" />
        </template>
      </Dialog>
    </div>
    <table class="profile-table">
      <tbody>
        <tr v-for="(value, key) in filteredUserProfile" :key="key" class="profile-row">
          <td class="profile-key">{{ getFieldLabel(key) }}</td>
          <td class="profile-value">
            <template v-if="isEditable(key) && isEditMode">
              <component
                :is="getInputComponent(key)"
                v-model="editProfile[key]"
                v-bind="getInputProps(key, value)"
                class="profile-input"
                :aria-label="getFieldLabel(key)"
                :aria-describedby="`desc-${key}`"
              />
            </template>
            <template v-else-if="key === 'password'">
              <div class="password-display">
                <span>{{ showPassword ? (value || '••••••••') : '••••••••' }}</span>
                <Button
                  :icon="showPassword ? 'pi pi-eye-slash' : 'pi pi-eye'"
                  text
                  size="small"
                  @click="togglePasswordVisibility"
                  class="toggle-password-button"
                  aria-label="Hiển thị hoặc ẩn mật khẩu"
                />
              </div>
            </template>
            <template v-else>
              <span>{{ isObject(value) ? formatObjectValue(key, value) : formatValue(key, value) }}</span>
            </template>
            <small :id="`desc-${key}`" class="field-description">{{ getFieldDescription(key) }}</small>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="form-actions" v-if="isEditMode">
      <Button
        type="submit"
        label="Lưu"
        icon="pi pi-check"
        :loading="isLoading"
        @click="updateProfile"
        class="save-button"
        :disabled="!canEditProfile"
        aria-label="Lưu thông tin hồ sơ"
      />
      <Button
        type="button"
        label="Hủy"
        icon="pi pi-times"
        :loading="false"
        @click="cancelEdit"
        class="cancel-button"
        :disabled="!canEditProfile"
        aria-label="Hủy chỉnh sửa"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from 'primevue/usetoast';
import { useUserStore } from '@/stores/user';
import { gsap } from 'gsap';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import Calendar from 'primevue/calendar';
import Textarea from 'primevue/textarea';
import Dialog from 'primevue/dialog';
import { Cropper } from 'vue-advanced-cropper';
import 'vue-advanced-cropper/dist/style.css';
import adminDefaultImg from '@/assets/images/admin.png';

const props = defineProps({
  userProfile: { type: Object, required: true },
  editProfile: { type: Object, required: true },
  userRole: { type: String, required: true },
});

const emit = defineEmits(['update:userProfile', 'update:editProfile']);

const router = useRouter();
const toast = useToast();
const userStore = useUserStore();

const isLoading = ref(false);
const isEditMode = ref(false);
const showCropper = ref(false);
const tempImage = ref(null);
const croppedImage = ref(null);
const fileInput = ref(null);
const showPassword = ref(false);

const canEditProfile = computed(() => props.userProfile ? userStore.isAdmin || props.userProfile.id === userStore.currentUser?.id : false);

const filteredUserProfile = computed(() => {
  const profile = { ...props.userProfile, full_name: `${props.userProfile.last_name || ''} ${props.userProfile.first_name || ''}`.trim() };
  const visibleFields = ['username', 'password', 'first_name', 'last_name', 'full_name', 'email', 'phone', 'address', 'birth_date', 'gender', 'role'];
  return Object.keys(profile)
    .filter(key => visibleFields.includes(key))
    .reduce((obj, key) => ({ ...obj, [key]: profile[key] }), {});
});

onMounted(() => {
  gsap.from('.profile-section', { opacity: 0, y: 20, duration: 0.5 });
});

const fetchProfile = async (userId = null) => {
  isLoading.value = true;
  try {
    const user = userId ? await userStore.fetchUserById(userId) : await userStore.getCurrentUser();
    const updatedProfile = { ...user, password: '••••••••', first_name: user.first_name || '', last_name: user.last_name || '' };
    emit('update:userProfile', updatedProfile);
    emit('update:editProfile', { ...updatedProfile });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải thông tin hồ sơ', life: 3000 });
  } finally {
    isLoading.value = false;
  }
};

const updateProfile = async () => {
  isLoading.value = true;
  try {
    const payload = Object.keys(props.editProfile)
      .filter(key => isEditable(key))
      .reduce((obj, key) => ({ ...obj, [key]: props.editProfile[key] }), {});
    await userStore.updateProfile(payload);
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật hồ sơ thành công', life: 3000 });
    isEditMode.value = false;
    fetchProfile();
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: error.response?.data?.message || 'Cập nhật thất bại', life: 3000 });
  } finally {
    isLoading.value = false;
  }
};

const cancelEdit = () => {
  isEditMode.value = false;
  emit('update:editProfile', { ...props.userProfile });
  toast.add({ severity: 'info', summary: 'Hủy', detail: 'Đã hủy chỉnh sửa', life: 3000 });
};

const triggerFileInput = () => {
  if (!fileInput.value || !canEditProfile.value) {
    toast.add({ severity: 'info', summary: 'Thông báo', detail: 'Bạn không có quyền tải lên ảnh đại diện.', life: 3000 });
    return;
  }
  fileInput.value.click();
};

const onFileChange = (e) => {
  const file = e.target.files[0];
  if (file) {
    tempImage.value = URL.createObjectURL(file);
    showCropper.value = true;
  }
};

const onCrop = ({ canvas }) => {
  if (canvas) croppedImage.value = canvas.toDataURL('image/jpeg');
};

const saveCroppedImage = async () => {
  if (!croppedImage.value) return;
  try {
    const blob = await (await fetch(croppedImage.value)).blob();
    const formData = new FormData();
    formData.append('avatar', blob, 'avatar.jpg');
    await userStore.uploadAvatar(formData);
    showCropper.value = false;
    fetchProfile();
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật ảnh đại diện thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Cập nhật ảnh đại diện thất bại', life: 3000 });
  }
};

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

const getFieldLabel = (key) => {
  const labels = {
    id: 'ID',
    username: 'Tên đăng nhập',
    password: 'Mật khẩu',
    first_name: 'Tên',
    last_name: 'Họ',
    full_name: 'Họ và tên',
    email: 'Email',
    phone: 'Số điện thoại',
    address: 'Địa chỉ',
    birth_date: 'Ngày sinh',
    gender: 'Giới tính',
    role: 'Vai trò',
  };
  return labels[key] || key;
};

const getFieldDescription = (key) => {
  const descriptions = {
    username: 'Tên dùng để đăng nhập hệ thống',
    password: 'Mật khẩu đăng nhập hệ thống',
    email: 'Địa chỉ email để liên hệ và đăng nhập',
    phone: 'Số điện thoại liên hệ',
    address: 'Địa chỉ hiện tại của người dùng',
    birth_date: 'Ngày sinh theo định dạng YYYY-MM-DD',
    gender: 'Giới tính: Nam, Nữ hoặc Khác',
    role: 'Vai trò của người dùng trong hệ thống',
  };
  return descriptions[key] || '';
};

const isEditable = (key) => ['email', 'first_name', 'last_name', 'phone', 'address', 'birth_date', 'gender'].includes(key) && canEditProfile.value;

const getInputComponent = (key) => {
  if (key === 'gender') return Dropdown;
  if (key === 'birth_date') return Calendar;
  if (key === 'address') return Textarea;
  return InputText;
};

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
    };
  }
  if (key === 'birth_date') {
    return { dateFormat: 'yy-mm-dd', showIcon: true, modelValue: value ? new Date(value) : null };
  }
  if (key === 'address') {
    return { rows: 2 };
  }
  return {};
};

const isObject = (val) => val && typeof val === 'object' && !Array.isArray(val);
const formatObjectValue = (key, value) => (value && value.name) ? value.name : JSON.stringify(value);
const formatValue = (key, value) => {
  if (key === 'gender') return { 'M': 'Nam', 'F': 'Nữ', 'O': 'Khác' }[value] || 'N/A';
  if (key === 'role') return { admin: 'Quản trị viên', teacher: 'Giáo viên', student: 'Học sinh' }[value] || 'N/A';
  if (value === null || value === undefined || value === '') return 'N/A';
  if (typeof value === 'boolean') return value ? 'Có' : 'Không';
  if (key.includes('date') && value) {
    try {
      return new Date(value).toLocaleDateString('vi-VN', { year: 'numeric', month: '2-digit', day: '2-digit' });
    } catch (e) {
      return value;
    }
  }
  return value;
};

const navigateToChangePassword = () => router.push({ name: 'change-password' });
const handleProfileViewEditClick = () => {
  isEditMode.value = !isEditMode.value;
  if (isEditMode.value) {
    gsap.from('.profile-table', { opacity: 0, y: 20, duration: 0.5 });
  }
};
</script>

<style scoped>
.profile-section {
  padding: 24px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e5e7eb;
}
.card-header.dark-theme {
  border-bottom-color: #6b7280;
}
.card-title {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
}
.dark-theme .card-title {
  color: #f3f4f6;
}
.header-buttons {
  display: flex;
  gap: 12px;
}
.mode-toggle-button {
  font-size: 14px;
  padding: 8px 16px;
  border-radius: 6px;
  transition: transform 0.2s ease;
}
.mode-toggle-button:hover {
  transform: scale(1.05);
}
.avatar-section {
  text-align: center;
  margin-bottom: 24px;
}
.avatar-wrapper {
  display: inline-block;
  position: relative;
  cursor: pointer;
  transition: transform 0.2s ease;
}
.avatar-wrapper:hover {
  transform: scale(1.05);
}
.avatar-preview, .avatar-placeholder {
  width: 128px;
  height: 128px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #d1d5db;
  background-color: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  font-size: 14px;
}
.dark-theme .avatar-preview, .dark-theme .avatar-placeholder {
  border-color: #6b7280;
  background-color: #4b5563;
  color: #d1d5db;
}
.avatar-dialog {
  border-radius: 8px;
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.2);
}
.hidden {
  display: none;
}
.profile-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 24px;
}
.profile-row:hover {
  background-color: #f9fafb;
}
.dark-theme .profile-row:hover {
  background-color: #374151;
}
.profile-key {
  font-weight: 500;
  color: #374151;
  padding: 12px;
  background-color: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
  width: 192px;
}
.dark-theme .profile-key {
  color: #e5e7eb;
  background-color: #374151;
  border-bottom-color: #6b7280;
}
.profile-value {
  padding: 12px;
  border-bottom: 1px solid #e5e7eb;
}
.dark-theme .profile-value {
  border-bottom-color: #6b7280;
}
.profile-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
}
.profile-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
}
.dark-theme .profile-input {
  background-color: #374151;
  border-color: #6b7280;
  color: #ffffff;
}
.form-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 24px;
}
.field-description {
  display: block;
  color: #6b7280;
  font-size: 12px;
  margin-top: 4px;
  font-style: italic;
}
.dark-theme .field-description {
  color: #9ca3af;
}
.password-display {
  display: flex;
  align-items: center;
  gap: 8px;
}
.toggle-password-button {
  font-size: 12px;
}
.save-button {
  padding: 12px 24px;
  border-radius: 6px;
  background-color: #10b981;
  color: #ffffff;
}
.save-button:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}
.cancel-button {
  padding: 12px 24px;
  border-radius: 6px;
}
</style>