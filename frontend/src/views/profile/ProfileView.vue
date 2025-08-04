<template>
  <div class="profile-container" aria-label="Trang quản lý hồ sơ người dùng">
    <Toast aria-live="polite" />
    <ConfirmDialog aria-live="assertive" />
    <Transition name="fade">
      <router-view v-if="$route.name === 'change-password'" />
      <div v-else>
        <div v-if="userRole === 'admin'" class="tab-view-container">
          <TabView v-model:activeIndex="activeTabIndex" scrollable class="tab-view" aria-label="Tab điều hướng quản lý">
            <TabPanel header="Hồ Sơ Cá Nhân">
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
                  <UploadAvatar
                    :profilePicture="userProfile.profile_picture"
                    :userRole="userRole"
                    :canEdit="canEditProfile && isEditMode"
                    @update:avatar="updateAvatar"
                    aria-label="Quản lý ảnh đại diện"
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
            </TabPanel>
            <TabPanel header="Quản Lý Người Dùng">
              <UserManagement />
            </TabPanel>
          </TabView>
        </div>
        <div v-else-if="userRole === 'teacher' || userRole === 'student'" class="teacher-student-profile">
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
              <UploadAvatar
                :profilePicture="userProfile.profile_picture"
                :userRole="userRole"
                :canEdit="canEditProfile && isEditMode"
                @update:avatar="updateAvatar"
                aria-label="Quản lý ảnh đại diện"
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
        </div>
        <div v-else class="fallback">
          <p v-if="isLoading" class="loading-text" aria-live="polite">Đang tải thông tin...</p>
          <p v-else class="error-text" aria-live="assertive">Bạn không có quyền truy cập hoặc thông tin không hợp lệ.</p>
        </div>
        <Dialog
          v-model:visible="showDetailListDialog"
          modal
          :draggable="false"
          class="custom-dialog"
          style="width: 50vw;"
          :breakpoints="{ '1199px': '75vw', '575px': '90vw' }"
          aria-labelledby="detail-dialog-header"
        >
          <template #header>
            <div class="dialog-header-custom">
              <i class="pi pi-info-circle dialog-header-icon"></i>
              <span id="detail-dialog-header">Chi Tiết Hồ Sơ</span>
            </div>
          </template>
          <div class="dialog-content">
            <div v-for="(value, key) in userProfile" :key="key" class="dialog-row">
              <div v-if="isFieldVisible(key)">
                <strong class="dialog-label">{{ getFieldLabel(key) }}:</strong>
                <span class="dialog-value">{{ isObject(value) ? formatObjectValue(key, value) : formatValue(key, value) }}</span>
              </div>
            </div>
          </div>
          <template #footer>
            <Button
              label="Đóng"
              icon="pi pi-times"
              @click="showDetailListDialog = false"
              class="cancel-button"
              aria-label="Đóng dialog chi tiết hồ sơ"
            />
          </template>
        </Dialog>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from 'primevue/usetoast';
import { useUserStore } from '@/stores/user';
import { gsap } from 'gsap';
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';
import Toast from 'primevue/toast';
import ConfirmDialog from 'primevue/confirmdialog';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import Calendar from 'primevue/calendar';
import Textarea from 'primevue/textarea';
import UploadAvatar from '@/views/profile/UploadAvatar.vue';
import UserManagement from '@/components/UserManagement.vue';
import adminDefaultImg from '@/assets/images/admin.png';

// Khai báo baseUrl
const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const router = useRouter();
const toast = useToast();
const userStore = useUserStore();

const userRole = computed(() => userStore.currentUser?.role || ''); // Mặc định rỗng để tránh lỗi
const isLoading = ref(false);
const showDetailListDialog = ref(false);
const activeTabIndex = ref(0);
const userProfile = ref({});
const editProfile = ref({});
const isEditMode = ref(false);
const showPassword = ref(false);

const canEditProfile = computed(() => userProfile.value ? userStore.isAdmin || userProfile.value.id === userStore.currentUser?.id : false);

const filteredUserProfile = computed(() => {
  const profile = { ...userProfile.value, full_name: `${userProfile.value.last_name || ''} ${userProfile.value.first_name || ''}`.trim() };
  const visibleFields = ['username', 'password', 'first_name', 'last_name', 'full_name', 'email', 'phone', 'address', 'birth_date', 'gender', 'role'];
  return Object.keys(profile)
    .filter(key => visibleFields.includes(key))
    .reduce((obj, key) => ({ ...obj, [key]: profile[key] }), {});
});

onMounted(() => {
  gsap.from('.profile-container', { opacity: 0, y: 50, duration: 0.8, ease: 'power2.out' });
  fetchProfile();
});

watch(activeTabIndex, (newIndex) => {
  if (newIndex === 1 && userRole.value === 'admin') {
    gsap.from('.user-management-content', { opacity: 0, x: -30, duration: 0.5 });
  }
});

const fetchProfile = async (userId = null) => {
  isLoading.value = true;
  try {
    const user = userId ? await userStore.fetchUserById(userId) : await userStore.getCurrentUser();
    const updatedProfile = {
      ...user,
      password: '••••••••',
      first_name: user.first_name || '',
      last_name: user.last_name || '',
      profile_picture: user.profile_picture ? `${baseUrl}${user.profile_picture}?t=${new Date().getTime()}` : null
    };
    userProfile.value = updatedProfile;
    editProfile.value = { ...updatedProfile };
  } catch (error) {
    console.error('Fetch profile error:', error);
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải thông tin hồ sơ', life: 3000 });
  } finally {
    isLoading.value = false;
  }
};

const updateProfile = async () => {
  isLoading.value = true;
  try {
    const payload = Object.keys(editProfile.value)
      .filter(key => isEditable(key))
      .reduce((obj, key) => ({ ...obj, [key]: editProfile.value[key] }), {});
    await userStore.updateProfile(payload);
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật hồ sơ thành công', life: 3000 });
    isEditMode.value = false;
    fetchProfile();
  } catch (error) {
    console.error('Update profile error:', error);
    toast.add({ severity: 'error', summary: 'Lỗi', detail: error.response?.data?.message || 'Cập nhật thất bại', life: 3000 });
  } finally {
    isLoading.value = false;
  }
};

const updateAvatar = async (avatarUrl) => {
  userProfile.value.profile_picture = avatarUrl;
  editProfile.value.profile_picture = avatarUrl;
  try {
    // Đảm bảo relativeUrl đúng định dạng /media/profile_pictures/...
    const relativeUrl = avatarUrl.replace(`${baseUrl}`, '').split('?')[0];
    if (!relativeUrl) {
      throw new Error('Đường dẫn ảnh không hợp lệ');
    }
    await userStore.updateProfile({ profile_picture: relativeUrl });
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Đồng bộ ảnh đại diện thành công', life: 3000 });
    await fetchProfile(); // Làm mới profile để đảm bảo đồng bộ
  } catch (error) {
    console.error('Sync avatar error:', error);
    toast.add({ severity: 'error', summary: 'Lỗi', detail: error.message || 'Không thể đồng bộ ảnh đại diện', life: 5000 });
  }
};

const cancelEdit = () => {
  isEditMode.value = false;
  editProfile.value = { ...userProfile.value };
  toast.add({ severity: 'info', summary: 'Hủy', detail: 'Đã hủy chỉnh sửa', life: 3000 });
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

const navigateToChangePassword = () => {
  const routeName = userRole.value === 'admin' ? 'AdminChangePassword' :
                    userRole.value === 'teacher' ? 'TeacherChangePassword' :
                    userRole.value === 'student' ? 'StudentChangePassword' : '';
  router.push({ name: routeName });
};

const handleProfileViewEditClick = () => {
  isEditMode.value = !isEditMode.value;
  if (isEditMode.value) {
    gsap.from('.profile-table', { opacity: 0, y: 20, duration: 0.5 });
  }
};

const isFieldVisible = (key) => {
  const visibleFields = ['username', 'password', 'first_name', 'last_name', 'full_name', 'email', 'phone', 'address', 'birth_date', 'gender', 'role'];
  return visibleFields.includes(key) && (userRole.value === 'admin' || ['admin', 'teacher', 'student'].includes(userRole.value));
};

const props = defineProps({
  userRole: { type: String, default: '' },
});

</script>

<style scoped>
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  white-space: nowrap;
  border: 0;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.profile-container {
  max-width: 896px;
  margin: 0 auto;
  padding: 24px;
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}
.tab-view .p-tabview-nav {
  background-color: #f3f4f6;
  border-bottom: 2px solid #e5e7eb;
  border-radius: 8px 8px 0 0;
}
.tab-view .p-tabview-nav-link {
  padding: 12px 16px;
  font-weight: 500;
  color: #4b5563;
  transition: background-color 0.2s ease, color 0.2s ease;
}
.tab-view .p-tabview-nav-link:hover {
  background-color: #e5e7eb;
  color: #1f2937;
}
.tab-view .p-tabview-nav-link.p-highlight {
  background-color: #3b82f6;
  color: #ffffff;
  border-radius: 6px 6px 0 0;
}
.tab-view .p-tabview-panels {
  padding: 24px;
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 0 0 8px 8px;
}
.fallback {
  text-align: center;
  padding: 24px;
}
.loading-text {
  color: #6b7280;
  animation: pulse 1.5s infinite;
}
.dark-theme .loading-text {
  color: #d1d5db;
}
.error-text {
  color: #ef4444;
  font-weight: 500;
}
.dark-theme .error-text {
  color: #f87171;
}
.custom-dialog {
  border-radius: 8px;
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.2);
}
.dialog-header-custom {
  display: flex;
  align-items: center;
  background-color: #3b82f6;
  color: #ffffff;
  padding: 16px;
  border-radius: 8px 8px 0 0;
}
.dialog-header-icon {
  margin-right: 12px;
  font-size: 20px;
}
.dialog-content {
  padding: 16px;
}
.dialog-row {
  margin-bottom: 12px;
}
.dialog-label {
  color: #374151;
  font-weight: 500;
}
.dark-theme .dialog-label {
  color: #e5e7eb;
}
.dialog-value {
  margin-left: 8px;
}
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
@media (max-width: 1024px) {
  .tab-view .p-tabview-nav {
    flex-direction: column;
  }
  .tab-view .p-tabview-nav-link {
    border-radius: 6px;
    margin-bottom: 8px;
  }
}
@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}
</style>