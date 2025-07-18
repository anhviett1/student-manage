<template>
  <div class="profile-container" aria-label="Trang quản lý hồ sơ người dùng">
    <Toast aria-live="polite" />
    <ConfirmDialog aria-live="assertive" />
    <Transition name="fade">
      <router-view v-if="$route.name === 'change-password'" />
      <div v-else>
        <div v-if="userRole === 'admin' " class="tab-view-container">
          <TabView v-model:activeIndex="activeTabIndex" scrollable class="tab-view" aria-label="Tab điều hướng quản lý">
            <TabPanel header="Hồ Sơ Cá Nhân">
              <ProfileSection
                :userProfile="userProfile"
                :editProfile="editProfile"
                :userRole="userRole"
                @update:userProfile="userProfile = $event"
                @update:editProfile="editProfile = $event"
              />
            </TabPanel>
            <TabPanel header="Quản Lý Người Dùng">
              <UserManagement />
            </TabPanel>
          </TabView>
        </div>
        <div v-else-if="userRole === 'teacher' || userRole === 'student'" class="teacher-student-profile">
          <ProfileSection
            :userProfile="userProfile"
            :editProfile="editProfile"
            :userRole="userRole"
            @update:userProfile="userProfile = $event"
            @update:editProfile="editProfile = $event"
          />
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
import ProfileSection from '@/components/ProfileSection.vue';
import UserManagement from '@/components/UserManagement.vue';

const router = useRouter();
const toast = useToast();
const userStore = useUserStore();

const userRole = computed(() => userStore.currentUser?.role || null);
const isLoading = ref(false);
const showDetailListDialog = ref(false);
const activeTabIndex = ref(0);
const userProfile = ref({});
const editProfile = ref({});

onMounted(() => {
  gsap.from('.profile-container', { opacity: 0, y: 50, duration: 0.8, ease: 'power2.out' });
  fetchProfile();
});

watch(activeTabIndex, (newIndex) => {
  if (newIndex === 1 && userRole.value === 'admin') {
    gsap.from('.user-management-content', { opacity: 0, x: -30, duration: 0.5 });
  }
});

const fetchProfile = async () => {
  isLoading.value = true;
  try {
    const user = await userStore.getCurrentUser();
    userProfile.value = { ...user, password: '••••••••', first_name: user.first_name || '', last_name: user.last_name || '' };
    editProfile.value = { ...userProfile.value };
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải thông tin hồ sơ', life: 3000 });
  } finally {
    isLoading.value = false;
  }
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

const isFieldVisible = (key) => {
  const visibleFields = ['username', 'password', 'first_name', 'last_name', 'full_name', 'email', 'phone', 'address', 'birth_date', 'gender', 'role'];
  return visibleFields.includes(key) && (userRole.value === 'admin' || ['admin', 'teacher', 'student'].includes(userRole.value));
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
.cancel-button {
  padding: 8px 16px;
  border-radius: 6px;
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