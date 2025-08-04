<template>
  <div class="change-password-container" aria-label="Trang đổi mật khẩu">
    <Toast aria-live="polite" />
    <ConfirmDialog aria-live="assertive" />
    <div class="card">
      <div class="card-header">
        <div class="header-content">
          <Button
            icon="pi pi-arrow-left"
            text
            @click="goBack"
            class="back-button"
            v-tooltip="'Quay lại hồ sơ'"
            aria-label="Quay lại trang hồ sơ"
          />
          <h2>Đổi Mật Khẩu</h2>
        </div>
      </div>
      <form @submit.prevent="changePassword" class="p-fluid">
        <div class="field">
          <label for="current_password">Mật Khẩu Hiện Tại</label>
          <Password
            id="current_password"
            v-model="formData.current_password"
            :feedback="false"
            toggleMask
            :class="{ 'p-invalid': v$.current_password.$error }"
            @input="v$.current_password.$touch()"
            aria-describedby="current_password-error"
          />
          <small
            id="current_password-error"
            class="p-error"
            v-if="v$.current_password.required.$invalid && v$.current_password.$dirty"
          >
            Vui lòng nhập mật khẩu hiện tại.
          </small>
        </div>

        <div class="field">
          <label for="new_password">Mật Khẩu Mới</label>
          <Password
            id="new_password"
            v-model="formData.new_password"
            :feedback="true"
            toggleMask
            :class="{ 'p-invalid': v$.new_password.$error }"
            @input="v$.new_password.$touch()"
            aria-describedby="new_password-error"
          />
          <small
            id="new_password-error"
            class="p-error"
            v-if="v$.new_password.required.$invalid && v$.new_password.$dirty"
          >
            Vui lòng nhập mật khẩu mới.
          </small>
          <small
            class="p-error"
            v-if="v$.new_password.minLength.$invalid && v$.new_password.$dirty"
          >
            Mật khẩu mới phải có ít nhất 8 ký tự.
          </small>
          <small
            class="p-error"
            v-if="v$.new_password.strongPassword.$invalid && v$.new_password.$dirty"
          >
            Mật khẩu phải chứa chữ hoa, chữ thường, số và ký tự đặc biệt.
          </small>
        </div>

        <div class="field">
          <label for="confirm_password">Xác Nhận Mật Khẩu Mới</label>
          <Password
            id="confirm_password"
            v-model="formData.confirm_password"
            :feedback="false"
            toggleMask
            :class="{ 'p-invalid': v$.confirm_password.$error }"
            @input="v$.confirm_password.$touch()"
            aria-describedby="confirm_password-error"
          />
          <small
            id="confirm_password-error"
            class="p-error"
            v-if="v$.confirm_password.required.$invalid && v$.confirm_password.$dirty"
          >
            Vui lòng xác nhận mật khẩu mới.
          </small>
          <small
            class="p-error"
            v-if="v$.confirm_password.sameAsPassword.$invalid && v$.confirm_password.$dirty"
          >
            Mật khẩu xác nhận không khớp.
          </small>
        </div>

        <div class="form-actions">
          <Button
            type="submit"
            label="Đổi Mật Khẩu"
            icon="pi pi-check"
            :loading="isLoading"
            class="submit-button"
            aria-label="Lưu thay đổi mật khẩu"
          />
          <Button
            type="button"
            label="Hủy"
            icon="pi pi-times"
            :loading="false"
            @click="resetForm"
            class="cancel-button"
            aria-label="Hủy thay đổi mật khẩu"
          />
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from 'primevue/usetoast';
import { useUserStore } from '@/stores/user';
import { useVuelidate } from '@vuelidate/core';
import { required, minLength, helpers } from '@vuelidate/validators';
import Password from 'primevue/password';
import Button from 'primevue/button';
import Toast from 'primevue/toast';
import ConfirmDialog from 'primevue/confirmdialog';
import { gsap } from 'gsap';

const router = useRouter();
const toast = useToast();
const userStore = useUserStore();

const userRole = computed(() => userStore.currentUser?.role || null);

const formData = ref({
  current_password: '',
  new_password: '',
  confirm_password: '',
});

const isLoading = ref(false);

const strongPassword = helpers.regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/);

const rules = computed(() => ({
  current_password: { required },
  new_password: {
    required,
    minLength: minLength(8),
    strongPassword: helpers.withMessage('Mật khẩu phải mạnh', strongPassword),
  },
  confirm_password: {
    required,
    sameAsPassword: helpers.withMessage('Mật khẩu xác nhận không khớp', (value) => value === formData.value.new_password),
  },
}));

const v$ = useVuelidate(rules, formData);

const changePassword = async () => {
  v$.value.$touch();
  if (v$.value.$invalid) return;

  isLoading.value = true;
  try {
    await userStore.changePassword({
      old_password: formData.value.current_password,
      new_password: formData.value.new_password,
    });
    toast.add({
      severity: 'success',
      summary: 'Thành công',
      detail: 'Đổi mật khẩu thành công',
      life: 3000,
    });
    resetForm();
    goBack();
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Lỗi',
      detail: error.response?.data?.detail || 'Không thể đổi mật khẩu',
      life: 3000,
    });
  } finally {
    isLoading.value = false;
  }
};

const resetForm = () => {
  formData.value = {
    current_password: '',
    new_password: '',
    confirm_password: '',
  };
  v$.value.$reset();
};

const goBack = () => {
  const routeName = userRole.value === 'admin' ? 'AdminProfile' :
                    userRole.value === 'teacher' ? 'TeacherProfile' :
                    userRole.value === 'student' ? 'StudentProfile' : 'Profile';
  router.push({ name: routeName });
};

onMounted(() => {
  gsap.from('.change-password-container', { opacity: 0, y: 50, duration: 0.8, ease: 'power2.out' });
  if (!userStore.currentUser) {
    router.push('/login');
  }
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
.change-password-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 24px;
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}
.card {
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
.dark-theme .card-header {
  border-bottom-color: #6b7280;
}
.header-content {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
}
.card-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
  flex: 1;
  text-align: center;
}
.dark-theme .card-header h2 {
  color: #f3f4f6;
}
.back-button {
  font-size: 1.2rem;
  color: #6b7280;
  transition: color 0.3s ease;
}
.back-button:hover {
  color: #374151;
}
.dark-theme .back-button {
  color: #d1d5db;
}
.dark-theme .back-button:hover {
  color: #e5e7eb;
}
.field {
  margin-bottom: 24px;
}
.field label {
  display: block;
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
}
.dark-theme .field label {
  color: #e5e7eb;
}
:deep(.p-password) {
  width: 100%;
}
:deep(.p-password-input) {
  width: 100%;
  padding: 12px;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  transition: border-color 0.3s, box-shadow 0.3s;
}
:deep(.p-password-input:focus) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
.dark-theme :deep(.p-password-input) {
  background-color: #374151;
  border-color: #6b7280;
  color: #ffffff;
}
:deep(.p-invalid .p-password-input) {
  border-color: #ef4444;
}
.p-error {
  font-size: 12px;
  color: #ef4444;
  margin-top: 4px;
  display: block;
}
.form-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 24px;
}
.submit-button {
  padding: 12px 24px;
  border-radius: 6px;
  background-color: #10b981;
  color: #ffffff;
  transition: transform 0.2s ease;
}
.submit-button:hover {
  transform: scale(1.05);
}
.submit-button:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}
.cancel-button {
  padding: 12px 24px;
  border-radius: 6px;
}
@media (max-width: 575px) {
  .change-password-container {
    padding: 16px;
  }
  .card {
    padding: 16px;
  }
  .card-header h2 {
    font-size: 20px;
  }
  .header-content {
    flex-direction: column;
    gap: 8px;
  }
}
</style>