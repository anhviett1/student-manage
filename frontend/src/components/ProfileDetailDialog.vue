<template>
  <div class="profile-section card">
    <div class="card-header">
      <h2 class="card-title">Thông Tin Cá Nhân</h2>
      <div class="header-buttons">
        <Button
          :label="isEditMode ? 'Chế độ Xem' : 'Chỉnh sửa'"
          :icon="isEditMode ? 'pi pi-eye' : 'pi pi-pencil'"
          :severity="isEditMode ? 'secondary' : 'primary'"
          @click="$emit('toggle-edit-mode')"
          class="mode-toggle-button"
          :disabled="!canEditProfile"
          :aria-label="isEditMode ? 'Chuyển sang chế độ xem' : 'Chuyển sang chế độ chỉnh sửa'"
        />
        <Button
          label="Đổi mật khẩu"
          icon="pi pi-key"
          severity="warning"
          @click="$emit('navigate-to-change-password')"
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
      <ProfileAvatarCropperDialog
        :isVisible="showCropper"
        :tempImage="tempImage"
        @crop="onCrop"
        @save="saveCroppedImage"
        @close="showCropper = false"
      />
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
      <Button type="submit" label="Lưu" icon="pi pi-check" :loading="isLoading" @click="$emit('update-profile')" class="save-button" :disabled="!canEditProfile" aria-label="Lưu thông tin hồ sơ" />
      <Button type="button" label="Hủy" icon="pi pi-times" :loading="false" @click="$emit('cancel-edit')" class="delete-button" :disabled="!canEditProfile" aria-label="Hủy chỉnh sửa" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import Calendar from 'primevue/calendar';
import Textarea from 'primevue/textarea';
import Checkbox from 'primevue/checkbox';
import Password from 'primevue/password';
import ProfileAvatarCropperDialog from './ProfileAvatarCropperDialog.vue'; // Đổi tên file
import adminDefaultImg from '@/assets/images/admin.png'; // Đảm bảo đường dẫn đúng

const props = defineProps({
  userProfile: {
    type: Object,
    required: true
  },
  userRole: {
    type: String,
    required: true
  },
  isEditMode: {
    type: Boolean,
    required: true
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  canEditProfile: {
    type: Boolean,
    default: false
  },
  fieldMap: { // Truyền fieldMap từ cha
    type: Object,
    required: true
  }
});

const emit = defineEmits([
  'toggle-edit-mode',
  'navigate-to-change-password',
  'update-profile',
  'cancel-edit',
  'update-profile-picture'
]);

const editProfile = ref({ ...props.userProfile });
const showPassword = ref(false);
const showCropper = ref(false);
const tempImage = ref(null);
const croppedImage = ref(null);
const fileInput = ref(null);

watch(() => props.userProfile, (newVal) => {
  editProfile.value = { ...newVal };
}, { deep: true });

const filteredUserProfile = computed(() => {
  const filtered = {};
  for (const key in props.userProfile) {
    if (props.fieldMap[key] && (props.fieldMap[key].roles.includes(props.userRole) || props.userRole === 'admin' || props.fieldMap[key].visible)) {
      filtered[key] = props.userProfile[key];
    }
  }
  return filtered;
});

const getFieldLabel = (key) => props.fieldMap[key]?.label || key;
const getFieldDescription = (key) => props.fieldMap[key]?.description || '';

const isEditable = (key) => {
  const nonEditableFields = ['id', 'username', 'role', 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'created_at', 'updated_at', 'profile_picture', 'password'];
  return !nonEditableFields.includes(key) && props.canEditProfile;
};

const getInputComponent = (key) => {
  if (key === 'birth_date') return Calendar;
  if (key === 'address') return Textarea;
  if (key === 'gender') return Dropdown;
  return InputText;
};

const getInputProps = (key, value) => {
  const props = {
    class: 'p-inputtext p-component'
  };
  if (key === 'gender') {
    props.options = [{ label: 'Nam', value: 'male' }, { label: 'Nữ', value: 'female' }, { label: 'Khác', value: 'other' }];
    props.optionLabel = 'label';
    props.optionValue = 'value';
    props.placeholder = 'Chọn giới tính';
  } else if (key === 'birth_date') {
    props.dateFormat = 'yy-mm-dd';
    props.showIcon = true;
  }
  if (key === 'email') {
    props.type = 'email';
  } else if (key === 'phone') {
    props.type = 'tel';
  }
  return props;
};

const isObject = (value) => typeof value === 'object' && value !== null;

const formatObjectValue = (key, value) => {
  if (key === 'groups' || key === 'user_permissions') {
    return value.map(item => item.name).join(', ') || 'N/A';
  }
  return JSON.stringify(value);
};

const formatValue = (key, value) => {
  if (key === 'birth_date' && value) {
    try {
      return new Date(value).toLocaleDateString('vi-VN');
    } catch {
      return value;
    }
  }
  if (key === 'date_joined' || key === 'created_at' || key === 'updated_at') {
    return value ? new Date(value).toLocaleString('vi-VN') : 'N/A';
  }
  if (typeof value === 'boolean') {
    return value ? 'Có' : 'Không';
  }
  return value || 'N/A';
};

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

const triggerFileInput = () => {
  if (fileInput.value) {
    fileInput.value.click();
  }
};

const onFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    tempImage.value = URL.createObjectURL(file);
    showCropper.value = true;
  }
};

const onCrop = ({ coordinates, canvas }) => {
  if (canvas) {
    croppedImage.value = canvas.toDataURL();
  }
};

const saveCroppedImage = () => {
  if (croppedImage.value) {
    emit('update-profile-picture', croppedImage.value);
    showCropper.value = false;
  }
};
</script>

<style scoped>
/* Styles from ProfileView.vue related to ProfileSection */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.card-title {
  font-size: 1.8em;
  color: #333;
  margin: 0;
}

.header-buttons .p-button {
  margin-left: 10px;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
}

.avatar-wrapper {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  overflow: hidden;
  position: relative;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease-in-out;
}

.avatar-wrapper:hover {
  transform: scale(1.05);
}

.avatar-preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background-color: #f0f0f0;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #888;
  font-size: 1.1em;
}

.hidden {
  display: none;
}

.profile-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.profile-row:nth-child(even) {
  background-color: #f9f9f9;
}

.profile-key,
.profile-value {
  padding: 12px 15px;
  border-bottom: 1px solid #eee;
  text-align: left;
}

.profile-key {
  font-weight: bold;
  color: #555;
  width: 30%;
}

.profile-value {
  color: #333;
  width: 70%;
}

.profile-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.password-display {
  display: flex;
  align-items: center;
  gap: 5px;
}

.field-description {
  display: block;
  color: #888;
  font-size: 0.85em;
  margin-top: 5px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 30px;
}

.save-button, .delete-button {
  min-width: 120px;
}
</style>