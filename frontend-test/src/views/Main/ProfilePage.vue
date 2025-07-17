<template>
  <div class="profile-page p-flex p-justify-center">
    <p-card class="profile-card">
      <template #title>
        <i class="mdi mdi-account-circle-outline p-mr-2"></i> Hồ sơ cá nhân
      </template>
      <template #content>
        <div v-if="authStore.user" class="p-grid p-formgrid p-gap-2">
          <div class="p-col-12 p-md-6">
            <span class="p-float-label p-mb-4">
              <p-input-text id="profileUsername" :modelValue="authStore.user.username" readonly />
              <label for="profileUsername">Tên đăng nhập</label>
            </span>
          </div>
          <div class="p-col-12 p-md-6">
            <span class="p-float-label p-mb-4">
              <p-input-text id="profileFullName" :modelValue="authStore.user.full_name" readonly />
              <label for="profileFullName">Họ và Tên</label>
            </span>
          </div>
          <div class="p-col-12 p-md-6">
            <span class="p-float-label p-mb-4">
              <p-input-text id="profileEmail" :modelValue="authStore.user.email" readonly />
              <label for="profileEmail">Email</label>
            </span>
          </div>
          <div class="p-col-12 p-md-6">
            <span class="p-float-label p-mb-4">
              <p-input-text id="profileRole" :modelValue="authStore.user.role" readonly />
              <label for="profileRole">Vai trò</label>
            </span>
          </div>
          <div v-if="authStore.user.role === 'student'" class="p-col-12 p-md-6">
            <span class="p-float-label p-mb-4">
              <p-input-text id="profileStudentId" :modelValue="authStore.user.student_id || 'N/A'" readonly />
              <label for="profileStudentId">Mã sinh viên</label>
            </span>
          </div>
          <div v-if="authStore.user.role === 'student'" class="p-col-12 p-md-6">
            <span class="p-float-label p-mb-4">
              <p-input-text id="profileMajor" :modelValue="authStore.user.major || 'N/A'" readonly />
              <label for="profileMajor">Chuyên ngành</label>
            </span>
          </div>
          <div v-if="authStore.user.role === 'teacher'" class="p-col-12 p-md-6">
            <span class="p-float-label p-mb-4">
              <p-input-text id="profileTeacherId" :modelValue="authStore.user.teacher_id || 'N/A'" readonly />
              <label for="profileTeacherId">Mã giáo viên</label>
            </span>
          </div>
          <div v-if="authStore.user.role === 'teacher'" class="p-col-12 p-md-6">
            <span class="p-float-label p-mb-4">
              <p-input-text id="profileDepartment" :modelValue="authStore.user.department || 'N/A'" readonly />
              <label for="profileDepartment">Khoa/Phòng ban</label>
            </span>
          </div>

          <div class="p-col-12 p-text-center p-mt-4">
            <p-button label="Chỉnh sửa hồ sơ" icon="pi pi-user-edit" @click="editProfile" />
          </div>
        </div>
        <div v-else class="p-text-center">
          <p>Không thể tải thông tin hồ sơ.</p>
          <router-link to="/auth/login">
            <p-button label="Đăng nhập ngay" />
          </router-link>
        </div>
      </template>
    </p-card>

    <p-dialog v-model:visible="editProfileDialogVisible" modal header="Chỉnh sửa thông tin cá nhân" :style="{ width: '50vw' }" :breakpoints="{'960px': '75vw', '641px': '100vw'}">
      <UserForm 
        :initial-data="editableUser" 
        :is-edit-mode="true" 
        :is-loading="savingProfile" 
        @submit="saveProfile" 
        @cancel="editProfileDialogVisible = false" 
      />
    </p-dialog>
  </div>
</template>

<script setup>
import { ref, watchEffect } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useNotificationStore } from '@/stores/notification';
import UserForm from '@/components/admin/UserForm.vue'; // Tái sử dụng UserForm cho chỉnh sửa

// PrimeVue Components
import PCard from 'primevue/card';
import PInputText from 'primevue/inputtext';
import PButton from 'primevue/button';
import PDialog from 'primevue/dialog';

const authStore = useAuthStore();
const notificationStore = useNotificationStore();

const editProfileDialogVisible = ref(false);
const editableUser = ref(null);
const savingProfile = ref(false);

// Cập nhật editableUser khi user trong store thay đổi
watchEffect(() => {
  if (authStore.user) {
    editableUser.value = { ...authStore.user, password: '', confirm_password: '' };
  }
});

const editProfile = () => {
  editProfileDialogVisible.value = true;
};

const saveProfile = async (formData) => {
  savingProfile.value = true;
  try {
    // API call để cập nhật hồ sơ
    // Giả lập API
    await new Promise(resolve => setTimeout(resolve, 800));
    console.log('Saving profile:', formData);
    // Sau khi lưu thành công, cập nhật lại thông tin trong authStore
    authStore.setUser({ ...authStore.user, ...formData });
    notificationStore.showToast('Hồ sơ đã được cập nhật thành công!', 'success');
    editProfileDialogVisible.value = false;
  } catch (error) {
    console.error('Error saving profile:', error);
    notificationStore.showToast('Lỗi khi cập nhật hồ sơ.', 'error');
  } finally {
    savingProfile.value = false;
  }
};
</script>

<style scoped>

.profile-card {
  width: 100%;
  max-width: 700px;
  border-radius: var(--p-border-radius);
  box-shadow: var(--p-shadow-2);
}
.p-mb-4 {
  margin-bottom: 1.5rem !important;
}
</style>