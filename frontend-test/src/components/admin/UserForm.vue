<template>
  <p-card class="user-form-card">
    <template #title>
      <i class="mdi mdi-account-edit-outline p-mr-2"></i> {{ isEditMode ? 'Chỉnh sửa Người dùng' : 'Thêm Người dùng Mới' }}
    </template>
    <template #content>
      <form @submit.prevent="submitForm" class="p-fluid p-formgrid p-grid p-jc-center">
        <div class="p-col-12 p-md-6 p-lg-4">
          <span class="p-float-label p-mb-4">
            <p-input-text id="username" v-model="formData.username" :class="{'p-invalid': v$.username.$error}" />
            <label for="username">Tên đăng nhập</label>
          </span>
          <small class="p-error" v-for="error of v$.username.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6 p-lg-4">
          <span class="p-float-label p-mb-4">
            <p-input-text id="fullName" v-model="formData.full_name" :class="{'p-invalid': v$.full_name.$error}" />
            <label for="fullName">Họ và Tên</label>
          </span>
          <small class="p-error" v-for="error of v$.full_name.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6 p-lg-4">
          <span class="p-float-label p-mb-4">
            <p-input-text id="email" v-model="formData.email" :class="{'p-invalid': v$.email.$error}" />
            <label for="email">Email</label>
          </span>
          <small class="p-error" v-for="error of v$.email.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6 p-lg-4">
          <span class="p-float-label p-mb-4">
            <p-calendar id="dateOfBirth" v-model="formData.date_of_birth" showIcon :class="{'p-invalid': v$.date_of_birth.$error}" />
            <label for="dateOfBirth">Ngày sinh</label>
          </span>
          <small class="p-error" v-for="error of v$.date_of_birth.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6 p-lg-4">
          <span class="p-float-label p-mb-4">
            <p-dropdown id="gender" v-model="formData.gender" :options="genderOptions" optionLabel="label" optionValue="value" :class="{'p-invalid': v$.gender.$error}" />
            <label for="gender">Giới tính</label>
          </span>
          <small class="p-error" v-for="error of v$.gender.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6 p-lg-4">
          <span class="p-float-label p-mb-4">
            <p-dropdown id="role" v-model="formData.role" :options="roleOptions" optionLabel="label" optionValue="value" :class="{'p-invalid': v$.role.$error}" />
            <label for="role">Vai trò</label>
          </span>
          <small class="p-error" v-for="error of v$.role.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>
        
        <div class="p-col-12 p-md-6 p-lg-4" v-if="!isEditMode || (isEditMode && isPasswordChange)">
          <span class="p-float-label p-mb-4">
            <p-password id="password" v-model="formData.password" toggleMask :class="{'p-invalid': v$.password.$error}" :feedback="false" />
            <label for="password">Mật khẩu</label>
          </span>
          <small class="p-error" v-for="error of v$.password.$errors" :key="error.$uid">{{ error.$message }}</small>
          <p-checkbox v-if="isEditMode" v-model="isPasswordChange" :binary="true" inputId="changePassword" class="p-mt-2" />
          <label v-if="isEditMode" for="changePassword" class="p-ml-2"> Thay đổi mật khẩu</label>
        </div>

        <div class="p-col-12 p-md-6 p-lg-4" v-if="!isEditMode || (isEditMode && isPasswordChange)">
          <span class="p-float-label p-mb-4">
            <p-password id="confirmPassword" v-model="formData.confirm_password" toggleMask :class="{'p-invalid': v$.confirm_password.$error}" :feedback="false" />
            <label for="confirmPassword">Xác nhận mật khẩu</label>
          </span>
          <small class="p-error" v-for="error of v$.confirm_password.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-text-center p-mt-4">
          <p-button type="submit" :label="isEditMode ? 'Cập nhật' : 'Thêm mới'" icon="pi pi-check" :loading="isLoading" />
          <p-button type="button" label="Hủy" icon="pi pi-times" severity="secondary" outlined class="p-ml-2" @click="cancelForm" />
        </div>
      </form>
    </template>
  </p-card>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue';
import { required, email, minLength, sameAs } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import { useNotificationStore } from '@/stores/notification'; // Giả sử bạn có notification store

// PrimeVue Components
import PCard from 'primevue/card';
import PInputText from 'primevue/inputtext';
import PCalendar from 'primevue/calendar';
import PDropdown from 'primevue/dropdown';
import PPassword from 'primevue/password';
import PButton from 'primevue/button';
import PCheckbox from 'primevue/checkbox';

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({
      username: '',
      full_name: '',
      email: '',
      date_of_birth: null,
      gender: null,
      role: null,
      password: '',
      confirm_password: ''
    })
  },
  isEditMode: {
    type: Boolean,
    default: false
  },
  isLoading: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['submit', 'cancel']);

const notificationStore = useNotificationStore();

const formData = reactive({ ...props.initialData });
const isPasswordChange = ref(false); // Theo dõi trạng thái muốn thay đổi mật khẩu khi ở chế độ chỉnh sửa

// Watch initialData changes to update formData when in edit mode
watch(() => props.initialData, (newVal) => {
  Object.assign(formData, newVal);
  if (props.isEditMode) {
    formData.password = ''; // Xóa mật khẩu khi chỉnh sửa để người dùng nhập lại nếu muốn thay đổi
    formData.confirm_password = '';
    isPasswordChange.value = false;
  }
}, { immediate: true, deep: true });

// Rules for Vuelidate
const rules = computed(() => {
  const baseRules = {
    username: { required },
    full_name: { required },
    email: { required, email },
    date_of_birth: { required },
    gender: { required },
    role: { required }
  };

  if (!props.isEditMode || (props.isEditMode && isPasswordChange.value)) {
    baseRules.password = { required, minLength: minLength(6) };
    baseRules.confirm_password = { required, sameAsPassword: sameAs(formData.password) };
  } else {
    // Nếu không thay đổi mật khẩu, không yêu cầu password và confirm_password
    baseRules.password = {};
    baseRules.confirm_password = {};
  }
  return baseRules;
});

const v$ = useVuelidate(rules, formData);

const genderOptions = ref([
  { label: 'Nam', value: 'male' },
  { label: 'Nữ', value: 'female' },
  { label: 'Khác', value: 'other' }
]);

const roleOptions = ref([
  { label: 'Admin', value: 'admin' },
  { label: 'Giáo viên', value: 'teacher' },
  { label: 'Sinh viên', value: 'student' }
]);

const submitForm = async () => {
  const result = await v$.value.$validate();
  if (result) {
    // Tạo bản sao dữ liệu để tránh mutation trực tiếp props hoặc reactive object
    const dataToSubmit = { ...formData };
    
    // Xóa password và confirm_password nếu không muốn thay đổi trong chế độ chỉnh sửa
    if (props.isEditMode && !isPasswordChange.value) {
      delete dataToSubmit.password;
      delete dataToSubmit.confirm_password;
    }
    
    emit('submit', dataToSubmit);
  } else {
    notificationStore.showToast('Vui lòng kiểm tra lại các trường bị lỗi!', 'error', 'Lỗi nhập liệu');
  }
};

const cancelForm = () => {
  emit('cancel');
};
</script>

<style scoped>
.user-form-card {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  border-radius: var(--p-border-radius);
  box-shadow: var(--p-shadow-2);
}

.p-fluid .p-col-12 {
  padding-bottom: 0; /* Giảm padding dưới để kiểm soát khoảng cách bằng p-mb-4 */
}

.p-mb-4 {
  margin-bottom: 1.5rem !important; /* Khoảng cách giữa các input */
}

/* Tùy chỉnh nhỏ cho Calendar icon */
:deep(.p-calendar .p-inputtext) {
  width: 100%;
}
</style>