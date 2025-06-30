<template>
  <div class="profile-container card">
    <Toast />
    <div class="card-header">
      <h2>Thông Tin Cá Nhân</h2>
      <div class="header-buttons">
        <Button
          :label="isEditMode ? 'Chế độ Xem' : 'Chỉnh sửa'"
          :icon="isEditMode ? 'pi pi-eye' : 'pi pi-pencil'"
          :severity="isEditMode ? 'secondary' : 'primary'"
          @click="handleProfileViewEditClick"
          class="mode-toggle-button"
          :disabled="!canEditProfile"
        />

        <Button
          v-if="userRole === 'admin'"
          :label="showFieldConfig ? 'Ẩn cấu hình' : 'Cấu hình trường'"
          :icon="showFieldConfig ? 'pi pi-times' : 'pi pi-cog'"
          :severity="showFieldConfig ? 'info' : 'secondary'"
          @click="toggleFieldConfig"
          class="mode-toggle-button"
        />

        <Button
          v-if="userRole === 'admin'"
          :label="showUserTable ? 'Ẩn danh sách' : 'Danh sách người dùng'"
          :icon="showUserTable ? 'pi pi-times' : 'pi pi-users'"
          :severity="showUserTable ? 'info' : 'secondary'"
          @click="toggleUserTable"
          class="mode-toggle-button"
        />
      </div>
    </div>

    <template v-if="!showFieldConfig && !showUserTable">
      <div class="avatar-section">
        <div class="avatar-wrapper" @click="canUploadAvatar && isEditMode ? triggerFileInput() : null">
          <img
            v-if="userProfile.profile_picture"
            :src="userProfile.profile_picture"
            alt="Avatar"
            class="avatar-preview"
          />
          <img
            v-else-if="userRole === 'admin' && adminDefaultImg"
            :src="adminDefaultImg"
            alt="Admin Default"
            class="avatar-preview"
          />
          <div v-else class="avatar-placeholder">Không có ảnh</div>
          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            style="display:none"
            @change="onFileChange"
          />
        </div>
      </div>

      <Dialog v-model:visible="showCropper" header="Cắt ảnh đại diện" modal>
        <Cropper
          v-if="tempImage"
          :src="tempImage"
          :stencil-props="{ aspectRatio: 1 }"
          :autoZoom="true"
          :stencil-component="'circle-stencil'"
          @change="onCrop"
        />
        <template #footer>
          <Button label="Hủy" @click="showCropper = false" />
          <Button label="Lưu" @click="saveCroppedImage" />
        </template>
      </Dialog>

      <table class="profile-table">
        <tbody>
          <tr v-for="(value, key) in filteredUserProfile" :key="key">
            <td class="profile-key">{{ getFieldLabel(key) }}</td>
            <td class="profile-value">
              <template v-if="isEditable(key) && isEditMode">
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
              <small class="field-description">{{ getFieldDescription(key) }}</small>
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
          class="submit-button"
          :disabled="!canEditProfile"
        />
      </div>
    </template>

    <div v-if="userRole === 'admin' && showFieldConfig" class="field-config-admin">
      <h3>Cấu hình trường hiển thị cho từng vai trò</h3>
      <table>
        <thead>
          <tr>
            <th>Trường</th>
            <th v-for="role in ['admin', 'teacher', 'student']" :key="role">{{ role }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(field, key) in fieldMap" :key="key">
            <td>{{ field.label }}</td>
            <td v-for="role in ['admin', 'teacher', 'student']" :key="role">
              <Checkbox v-model="field.roles" :value="role" />
            </td>
          </tr>
        </tbody>
      </table>
      <div class="admin-config-actions">
        <Button label="Lưu cấu hình" icon="pi pi-save" @click="saveFieldConfig" class="p-button-success" />
      </div>
    </div>

    <div
      v-if="userRole === 'admin' && showUserTable"
      class="user-list-admin"
      style="margin-top: 1rem;"
    >
      <h3>Danh sách người dùng</h3>
      <table>
        <thead>
          <tr>
            <th>STT</th>
            <th>Tên đăng nhập</th>
            <th>Họ tên</th>
            <th>Email</th>
            <th>Vai trò</th>
            <th>Chọn</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(user, idx) in userList" :key="user.id || idx">
            <td>{{ idx + 1 }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.full_name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ formatValue('role', user.role) }}</td>
            <td>
              <Button label="Chọn" @click="selectUser(user.id)" :disabled="selectedUserId === user.id" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <Dialog
      v-model:visible="showDetailListDialog"
      modal
      :draggable="false"
      class="custom-dialog"
      :style="{ width: '50vw' }"
      :breakpoints="{ '1199px': '75vw', '575px': '90vw' }"
    >
      <template #header>
        <div class="dialog-header-custom">
          <i class="pi pi-info-circle" style="font-size: 1.5rem; margin-right: 0.75rem;"></i>
          Chi Tiết Hồ Sơ
        </div>
      </template>

      <div class="p-fluid">
        <div class="p-field" v-for="(value, key) in userProfile" :key="key">
          <div v-if="fieldMap[key] && (fieldMap[key].roles.includes(userRole) || userRole === 'admin')">
            <strong>{{ getFieldLabel(key) }}:</strong>
            <span>{{ isObject(value) ? formatObjectValue(key, value) : formatValue(key, value) }}</span>
          </div>
        </div>
      </div>

      <template #footer>
        <Button
          label="Đóng"
          icon="pi pi-times"
          @click="showDetailListDialog = false"
          class="p-button-text dialog-button-margin"
        />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
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
import { Cropper } from 'vue-advanced-cropper'
import 'vue-advanced-cropper/dist/style.css'
import adminDefaultImg from '@/assets/images/admin.png'

const toast = useToast()
const userStore = useUserStore()
const authStore = useAuthStore()
const { canEditProfile, canUploadAvatar, userRole } = usePermissions()

const isLoading = ref(false)
const showDetailListDialog = ref(false)
const isEditMode = ref(true) // Mặc định hiển thị ở chế độ chỉnh sửa

const showFieldConfig = ref(false)
const showUserTable = ref(false)

const userProfile = ref({})
const editProfile = ref({})
const userList = ref([])
const selectedUserId = ref(null)

const showCropper = ref(false)
const tempImage = ref(null)
const croppedImage = ref(null)

const fileInput = ref(null)

const fieldMap = ref({
  id: { label: 'ID', visible: false, description: 'Mã định danh duy nhất của người dùng', roles: ['admin'] },
  username: { label: 'Tên đăng nhập', visible: false, description: 'Tên dùng để đăng nhập hệ thống', roles: ['admin'] },
  email: { label: 'Email', visible: true, description: 'Địa chỉ email để liên hệ và đăng nhập', roles: ['admin', 'teacher', 'student'] },
  full_name: { label: 'Họ và tên', visible: true, description: 'Tên đầy đủ của người dùng', roles: ['admin', 'teacher', 'student'] },
  phone: { label: 'Số điện thoại', visible: true, description: 'Số điện thoại liên hệ', roles: ['admin', 'teacher', 'student'] },
  address: { label: 'Địa chỉ', visible: true, description: 'Địa chỉ hiện tại của người dùng', roles: ['admin', 'teacher', 'student'] },
  birth_date: { label: 'Ngày sinh', visible: true, description: 'Ngày sinh theo định dạngYYYY-MM-DD', roles: ['admin', 'teacher', 'student'] },
  gender: { label: 'Giới tính', visible: true, description: 'Giới tính: Nam, Nữ hoặc Khác', roles: ['admin', 'teacher', 'student'] },
  role: { label: 'Vai trò', visible: true, description: 'Vai trò của người dùng trong hệ thống', roles: ['admin'] },
  is_active: { label: 'Hoạt động', visible: false, description: 'Trạng thái hoạt động của tài khoản', roles: ['admin'] },
  is_staff: { label: 'Nhân viên', visible: false, description: 'Người dùng có phải là nhân viên', roles: ['admin'] },
  is_superuser: { label: 'Superuser', visible: false, description: 'Người dùng có quyền quản trị', roles: ['admin'] },
  date_joined: { label: 'Ngày tạo tài khoản', visible: false, description: 'Ngày tạo tài khoản người dùng', roles: ['admin'] },
  created_at: { label: 'Ngày tạo', visible: false, description: 'Thời điểm tạo tài khoản', roles: ['admin'] },
  updated_at: { label: 'Ngày cập nhật', visible: false, description: 'Thời điểm cập nhật thông tin gần nhất', roles: ['admin'] },
  profile_picture: { label: 'Ảnh đại diện', visible: false, description: 'Ảnh đại diện của người dùng', roles: ['admin', 'teacher', 'student'] },
})

onMounted(async () => {
  await fetchProfile();
  if (userRole.value === 'admin') {
    await fetchUserList();
  }
});

const fetchUserList = async () => {
  if (userRole.value === 'admin') {
    try {
      userList.value = await userStore.fetchAllUsers();
    } catch (error) {
      toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách người dùng', life: 3000 });
      console.error('Error fetching user list:', error);
    }
  }
};

const fetchProfile = async (userId = null) => {
  try {
    let user;
    if (userRole.value === 'admin' && userId) {
      user = await userStore.fetchUserById(userId);
    } else {
      user = authStore.user || await authStore.fetchCurrentUser();
    }
    userProfile.value = { ...user };
    editProfile.value = { ...user };
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải thông tin hồ sơ', life: 3000 });
    console.error('Error fetching profile:', error);
  }
};

const filteredUserProfile = computed(() => {
  const filtered = {};
  const currentUserRole = userRole.value || 'guest';

  Object.keys(userProfile.value).forEach((key) => {
    const fieldConfig = fieldMap.value[key];

    if (currentUserRole === 'admin') {
      if (fieldConfig) {
        filtered[key] = userProfile.value[key];
      }
    } else {
      if (fieldConfig && fieldConfig.roles && fieldConfig.roles.includes(currentUserRole)) {
        filtered[key] = userProfile.value[key];
      }
    }
  });
  return filtered;
});

const isEditable = (key) => {
  const editableFields = ['email', 'full_name', 'phone', 'address', 'birth_date', 'gender'];
  return editableFields.includes(key) && canEditProfile.value;
};

const getInputComponent = (key) => {
  if (key === 'gender') return Dropdown;
  if (key === 'birth_date' || key === 'date_of_birth') return Calendar;
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
  if (key === 'birth_date' || key === 'date_of_birth') {
    const dateValue = value ? new Date(value) : null;
    return {
      dateFormat: 'yy-mm-dd',
      showIcon: true,
      modelValue: dateValue
    };
  }
  if (key === 'address') {
    return {
      rows: 2,
    };
  }
  return {};
};

const isObject = (val) => val && typeof val === 'object' && !Array.isArray(val);

const formatObjectValue = (key, value) => {
  if (value && value.name) return value.name;
  return JSON.stringify(value);
};

const formatValue = (key, value) => {
  if (key === 'gender') {
    if (value === 'M') return 'Nam';
    if (value === 'F') return 'Nữ';
    if (value === 'O') return 'Khác';
  }
  if (key === 'role') {
    if (value === 'admin') return 'Quản trị viên';
    if (value === 'teacher') return 'Giáo viên';
    if (value === 'student') return 'Học sinh';
  }
  if (value === null || value === undefined || value === '') return 'N/A';
  if (typeof value === 'boolean') return value ? 'Có' : 'Không';
  if (key.includes('date') && value) {
    try {
      return new Date(value).toLocaleDateString('vi-VN', { year: 'numeric', month: '2-digit', day: '2-digit' });
    } catch (e) {
      return value;
    }
  }
  if (key.includes('time') && value) {
    try {
      return new Date(value).toLocaleTimeString('vi-VN');
    } catch (e) {
      return value;
    }
  }
  return value;
};

const getFieldLabel = (key) => {
  return fieldMap.value[key]?.label || key;
};

const getFieldDescription = (key) => {
  return fieldMap.value[key]?.description || '';
};

// Hàm xử lý click vào nút "Chỉnh sửa" / "Chế độ Xem"
const handleProfileViewEditClick = () => {
  // Khi click vào nút này, đảm bảo ẩn các bảng admin khác
  showFieldConfig.value = false;
  showUserTable.value = false;

  if (isEditMode.value) {
    // Nếu đang ở chế độ chỉnh sửa (nút hiển thị "Chế độ Xem")
    // Chuyển sang chế độ xem và hiển thị dialog chi tiết
    isEditMode.value = false;
    showDetailListDialog.value = true;
  } else {
    // Nếu đang ở chế độ xem (nút hiển thị "Chỉnh sửa")
    // Chuyển sang chế độ chỉnh sửa và ẩn dialog chi tiết
    isEditMode.value = true;
    showDetailListDialog.value = false;
  }
};

const toggleFieldConfig = () => {
  // Khi click "Cấu hình trường", toggle nó và ẩn các phần khác
  showFieldConfig.value = !showFieldConfig.value;
  if (showFieldConfig.value) {
    isEditMode.value = false; // Ẩn chế độ chỉnh sửa/xem chính
    showDetailListDialog.value = false; // Ẩn dialog chi tiết
    showUserTable.value = false; // Ẩn bảng danh sách người dùng
  }
};

const saveFieldConfig = () => {
  toast.add({ severity: 'success', summary: 'Thành công', detail: 'Đã cập nhật cấu hình trường hiển thị', life: 3000 });
};

const updateProfile = async () => {
  isLoading.value = true;
  try {
    const payload = {};
    Object.keys(editProfile.value).forEach((key) => {
      if (isEditable(key)) {
        payload[key] = editProfile.value[key];
      }
    });

    if (userRole.value === 'admin' && selectedUserId.value) {
      await userStore.updateUserProfile(selectedUserId.value, payload);
      await fetchUserList(); // Cập nhật lại danh sách nếu là admin
    } else {
      await userStore.updateProfile(payload);
    }
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật thông tin thành công', life: 3000 });
    await fetchProfile(selectedUserId.value); // Tải lại profile sau khi update
    isEditMode.value = false; // Sau khi lưu, chuyển về chế độ xem
  } catch (error) {
    let errorMessage = 'Không thể cập nhật thông tin';
    if (error.response?.data?.message) {
      errorMessage = error.response.data.message;
    } else if (error.message) {
      errorMessage = error.message;
    }
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errorMessage, life: 3000 });
    console.error('Update profile error:', error);
  } finally {
    isLoading.value = false;
  }
};

const triggerFileInput = () => {
  if (canUploadAvatar.value && isEditMode.value) {
    fileInput.value && fileInput.value.click();
  } else if (!canUploadAvatar.value) {
    toast.add({ severity: 'info', summary: 'Thông báo', detail: 'Bạn không có quyền tải lên ảnh đại diện.', life: 3000 });
  }
};

const onFileChange = (e) => {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (event) => {
      tempImage.value = event.target.result;
      showCropper.value = true;
    };
    reader.readAsDataURL(file);
  }
};

const onCrop = ({ canvas }) => {
  if (canvas) {
    croppedImage.value = canvas.toDataURL('image/jpeg');
  }
};

const saveCroppedImage = async () => {
  if (!croppedImage.value) return;
  const blob = await (await fetch(croppedImage.value)).blob();
  const formData = new FormData();
  formData.append('avatar', blob, 'avatar.jpg');
  await userStore.uploadAvatar(formData);
  showCropper.value = false;
  await fetchProfile(selectedUserId.value); // Tải lại profile để cập nhật ảnh
  toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật ảnh đại diện thành công', life: 3000 });
};


const selectUser = async (userId) => {
  selectedUserId.value = userId;
  isEditMode.value = true; // Khi chọn user, chuyển sang chế độ chỉnh sửa user đó
  showUserTable.value = false; // Tự động ẩn bảng user list sau khi chọn
  showFieldConfig.value = false; // Ẩn bảng cấu hình
  showDetailListDialog.value = false; // Ẩn dialog chi tiết (nếu đang mở)
  await fetchProfile(userId); // Load thông tin user mới
};

const toggleUserTable = async () => {
  // Khi click "Danh sách người dùng", toggle nó và ẩn các phần khác
  showUserTable.value = !showUserTable.value;
  if (showUserTable.value) {
    isEditMode.value = false; // Ẩn chế độ chỉnh sửa/xem chính
    showDetailListDialog.value = false; // Ẩn dialog chi tiết
    showFieldConfig.value = false; // Ẩn bảng cấu hình trường
    if (userList.value.length === 0 && userRole.value === 'admin') {
      await fetchUserList(); // Tải danh sách user nếu chưa có và là admin
    }
  }
};

// Watcher cho selectedUserId để tải profile khi Admin chọn user khác
watch(selectedUserId, (newVal, oldVal) => {
  if (newVal !== oldVal && newVal !== null) {
    fetchProfile(newVal);
  } else if (newVal === null && userRole.value !== 'admin') {
    // Nếu selectedUserId được reset về null và không phải admin, tải profile của user hiện tại
    fetchProfile();
  }
}, { immediate: false });

// Watcher cho userRole để tải danh sách user khi vai trò là admin
watch(userRole, (newRole) => {
  if (newRole === 'admin' && userList.value.length === 0) { // Thêm kiểm tra userList.value.length để tránh fetch lại không cần thiết
    fetchUserList();
  }
}, { immediate: true });
</script>

<style scoped>
.profile-container {
  max-width: 960px;
  margin: 2rem auto;
  padding: 2rem 2.5rem;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 1rem;
}
.card-header h2 {
  font-size: 1.75rem;
  font-weight: 600;
  color: #2c3e50;
}

.header-buttons {
  display: flex;
  gap: 1rem; /* Khoảng cách giữa các nút trong header */
  flex-wrap: wrap; /* Cho phép các nút xuống dòng nếu không đủ chỗ */
  justify-content: flex-end; /* Căn phải các nút */
}

.avatar-section {
  text-align: center;
  margin-bottom: 2rem;
}

.avatar-wrapper {
  display: inline-block;
  cursor: pointer;
  position: relative;
}

.avatar-preview, .avatar-placeholder {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #d1d5db;
  margin-bottom: 1rem;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.95rem;
  color: #9ca3af;
}

.hidden-upload-button {
  display: none; /* Hide the default file upload button */
}

.p-button-sm {
    padding: 0.4rem 1rem;
    font-size: 0.8rem;
    margin-top: 0.5rem; /* Margin for the delete button */
}

.p-button-danger-alt {
  background-color: #ef4444;
  border-color: #ef4444;
}
.p-button-danger-alt:hover {
  background-color: #dc2626;
  border-color: #dc2626;
}


.profile-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 2rem;
  font-size: 0.95rem;
}

.profile-key {
  font-weight: 500;
  color: #34495e;
  padding: 0.75rem 1rem;
  background: #f9fafb;
  width: 220px;
  border-bottom: 1px solid #e5e7eb;
  vertical-align: top;
}

.profile-value {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.profile-value .p-inputtext,
.profile-value .p-dropdown,
.profile-value .p-calendar,
.profile-value .p-textarea {
  width: 100%; /* Ensure input fields take full width */
}

.field-description {
  display: block;
  color: #6b7280;
  font-size: 0.78rem;
  margin-top: 0.25rem;
  font-style: italic;
}

/* Các nút điều khiển chế độ và hiển thị */
.mode-toggle-button {
  font-size: 0.85rem;
  padding: 0.45rem 1.2rem;
  border-radius: 6px;
  white-space: nowrap; /* Ngăn không cho chữ trong nút bị xuống dòng */
}

.submit-button {
  font-size: 1rem;
  padding: 0.7rem 2rem;
  border-radius: 6px;
}
.form-actions {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

/* Custom Dialog Styling - vẫn giữ nguyên cho dialog ví dụ */
.custom-dialog .p-dialog-header {
  background-color: #42b983;
  color: white;
  padding: 1.5rem;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.custom-dialog .p-dialog-header-icon {
  color: white;
}

.dialog-header-custom {
  display: flex;
  align-items: center;
  font-size: 1.25rem;
  font-weight: 600;
  color: white;
}

.custom-dialog .p-dialog-content {
  padding: 2rem 2.5rem;
  font-size: 1.05rem;
  color: #333;
}

.custom-dialog .p-dialog-footer {
  background-color: #f8f9fa;
  padding: 1rem 2rem;
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
}

.custom-dialog {
  border-radius: 10px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
}

.dialog-button-margin {
    margin: 0 10px;
}

/* Admin Field Configuration Table */
.field-config-admin {
  margin-top: 2.5rem; /* Tăng khoảng cách từ phần trên */
  padding: 1.5rem;
  background-color: #f3f9f3; /* Lighter green background for admin config */
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.field-config-admin h3 {
  font-size: 1.35rem;
  font-weight: 600;
  color: #2e8b57; /* Darker green */
  margin-bottom: 1.25rem;
  text-align: center;
}

.field-config-admin table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1.5rem;
  table-layout: fixed; /* Giúp các cột có độ rộng cố định */
}

.field-config-admin table th,
.field-config-admin table td {
  padding: 0.8rem 1rem;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

.field-config-admin table th {
  background-color: #e6ffe6; /* Very light green for headers */
  font-weight: 500;
  color: #3c763d;
}

/* Định nghĩa độ rộng cột cho bảng cấu hình */
.field-config-admin table th:first-child,
.field-config-admin table td:first-child {
    width: 40%; /* Cột tên trường */
}
.field-config-admin table th:not(:first-child),
.field-config-admin table td:not(:first-child) {
    width: 20%; /* Các cột vai trò */
    text-align: center; /* Căn giữa checkbox */
}


.field-config-admin table tr:last-child td {
  border-bottom: none;
}

.field-config-admin .p-checkbox {
  display: inline-flex; /* Đảm bảo checkbox hiển thị đúng */
  vertical-align: middle; /* Căn giữa theo chiều dọc */
  align-items: center;
  justify-content: center;
  width: 100%; /* Giúp checkbox chiếm toàn bộ ô để căn giữa */
  height: 100%;
}

.admin-config-actions {
  display: flex;
  justify-content: flex-end;
  padding-top: 1rem;
  border-top: 1px solid #e0e0e0;
}

/* User List Admin Table */
.user-list-admin {
  margin-top: 2.5rem; /* Tăng khoảng cách từ phần trên */
  padding: 1.5rem;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.user-list-admin h3 {
  font-size: 1.35rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 1.25rem;
  text-align: center;
}

.user-list-admin table {
  width: 100%;
  border-collapse: collapse;
}

.user-list-admin table thead {
  background-color: #f3f4f6;
}

.user-list-admin table th,
.user-list-admin table td {
  padding: 0.8rem 1rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.user-list-admin table th {
  font-weight: 500;
  color: #34495e;
}

.user-list-admin table tr:last-child td {
  border-bottom: none;
}

.user-list-admin table button {
  padding: 0.5rem 1rem;
  font-size: 0.8rem;
}

/* Các nút điều khiển tổng thể (không còn là show-user-table-btn riêng lẻ) */
/* Cập nhật selector để áp dụng cho tất cả các nút mode-toggle-button */
.mode-toggle-button {
  font-size: 0.85rem;
  padding: 0.45rem 1.2rem;
  border-radius: 6px;
}

/* Thêm responsive cho header-buttons nếu cần */
@media (max-width: 768px) {
    .header-buttons {
        flex-direction: column; /* Xếp các nút theo cột trên màn hình nhỏ */
        gap: 0.5rem; /* Giảm khoảng cách */
        align-items: stretch; /* Kéo dãn các nút cho đầy đủ chiều rộng */
    }
}
</style>