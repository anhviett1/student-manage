<template>
  <p-card class="student-form-card">
    <template #title>
      <i class="mdi mdi-account-school-outline p-mr-2"></i> {{ isEditMode ? 'Chỉnh sửa Sinh viên' : 'Thêm Sinh viên Mới' }}
    </template>
    <template #content>
      <form @submit.prevent="submitForm" class="p-fluid p-formgrid p-grid">
        <div class="p-col-12 p-text-bold p-text-lg p-mb-3">Thông tin tài khoản</div>
        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-input-text id="username" v-model="formData.username" :class="{'p-invalid': v$.username.$error}" :disabled="isEditMode" />
            <label for="username">Tên đăng nhập</label>
          </span>
          <small class="p-error" v-for="error of v$.username.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-input-text id="email" v-model="formData.email" :class="{'p-invalid': v$.email.$error}" />
            <label for="email">Email</label>
          </span>
          <small class="p-error" v-for="error of v$.email.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <template v-if="!isEditMode">
          <div class="p-col-12 p-md-6">
            <span class="p-float-label p-mb-4">
              <p-password id="password" v-model="formData.password" toggleMask :feedback="false" :class="{'p-invalid': v$.password.$error}" />
              <label for="password">Mật khẩu</label>
            </span>
            <small class="p-error" v-for="error of v$.password.$errors" :key="error.$uid">{{ error.$message }}</small>
          </div>
          <div class="p-col-12 p-md-6">
            <span class="p-float-label p-mb-4">
              <p-password id="confirmPassword" v-model="formData.confirm_password" toggleMask :feedback="false" :class="{'p-invalid': v$.confirm_password.$error}" />
              <label for="confirmPassword">Xác nhận mật khẩu</label>
            </span>
            <small class="p-error" v-for="error of v$.confirm_password.$errors" :key="error.$uid">{{ error.$message }}</small>
          </div>
        </template>
        
        <div class="p-col-12 p-text-bold p-text-lg p-mb-3 p-mt-4">Thông tin cá nhân</div>
        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-input-text id="fullName" v-model="formData.full_name" :class="{'p-invalid': v$.full_name.$error}" />
            <label for="fullName">Họ và Tên</label>
          </span>
          <small class="p-error" v-for="error of v$.full_name.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-calendar id="dateOfBirth" v-model="formData.date_of_birth" dateFormat="dd/mm/yy" :class="{'p-invalid': v$.date_of_birth.$error}" showIcon />
            <label for="dateOfBirth">Ngày sinh</label>
          </span>
          <small class="p-error" v-for="error of v$.date_of_birth.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-dropdown id="gender" v-model="formData.gender" :options="genderOptions" optionLabel="label" optionValue="value" placeholder="Chọn Giới tính" :class="{'p-invalid': v$.gender.$error}" />
            <label for="gender">Giới tính</label>
          </span>
          <small class="p-error" v-for="error of v$.gender.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-input-text id="phone" v-model="formData.phone_number" :class="{'p-invalid': v$.phone_number.$error}" />
            <label for="phone">Số điện thoại</label>
          </span>
          <small class="p-error" v-for="error of v$.phone_number.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>
        
        <div class="p-col-12">
          <span class="p-float-label p-mb-4">
            <p-textarea id="address" v-model="formData.address" rows="3" :class="{'p-invalid': v$.address.$error}" />
            <label for="address">Địa chỉ</label>
          </span>
          <small class="p-error" v-for="error of v$.address.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-text-bold p-text-lg p-mb-3 p-mt-4">Thông tin học tập</div>
        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-input-text id="studentId" v-model="formData.student_id" :class="{'p-invalid': v$.student_id.$error}" />
            <label for="studentId">Mã sinh viên</label>
          </span>
          <small class="p-error" v-for="error of v$.student_id.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>
        
        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-dropdown id="major" v-model="formData.major_id" :options="majors" optionLabel="name" optionValue="id" placeholder="Chọn Chuyên ngành" :class="{'p-invalid': v$.major_id.$error}" filter />
            <label for="major">Chuyên ngành</label>
          </span>
          <small class="p-error" v-for="error of v$.major_id.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-dropdown id="class" v-model="formData.class_id" :options="classes" optionLabel="name" optionValue="id" placeholder="Chọn Lớp học" :class="{'p-invalid': v$.class_id.$error}" filter />
            <label for="class">Lớp học</label>
          </span>
          <small class="p-error" v-for="error of v$.class_id.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-calendar id="admissionDate" v-model="formData.admission_date" dateFormat="dd/mm/yy" :class="{'p-invalid': v$.admission_date.$error}" showIcon />
            <label for="admissionDate">Ngày nhập học</label>
          </span>
          <small class="p-error" v-for="error of v$.admission_date.$errors" :key="error.$uid">{{ error.$message }}</small>
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
import { required, email, minLength, maxLength, sameAs, helpers } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import { useNotificationStore } from '@/stores/notification';

// PrimeVue Components
import PCard from 'primevue/card';
import PInputText from 'primevue/inputtext';
import PPassword from 'primevue/password';
import PCalendar from 'primevue/calendar';
import PDropdown from 'primevue/dropdown';
import PTextarea from 'primevue/textarea';
import PButton from 'primevue/button';

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({
      username: '',
      email: '',
      password: '',
      confirm_password: '',
      full_name: '',
      date_of_birth: null,
      gender: null,
      phone_number: '',
      address: '',
      student_id: '',
      major_id: null,
      class_id: null,
      admission_date: null
    })
  },
  isEditMode: {
    type: Boolean,
    default: false
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  majors: { // Dùng cho dropdown chuyên ngành
    type: Array,
    default: () => [] // Ví dụ: [{ id: 1, name: 'Công nghệ phần mềm' }]
  },
  classes: { // Dùng cho dropdown lớp học
    type: Array,
    default: () => [] // Ví dụ: [{ id: 1, name: 'CNTT K20' }]
  }
});

const emit = defineEmits(['submit', 'cancel']);

const notificationStore = useNotificationStore();

const formData = reactive({ ...props.initialData });

// Watch initialData changes to update formData and convert date strings to Date objects
watch(() => props.initialData, (newVal) => {
  Object.assign(formData, newVal);
  if (newVal.date_of_birth) {
    formData.date_of_birth = new Date(newVal.date_of_birth);
  }
  if (newVal.admission_date) {
    formData.admission_date = new Date(newVal.admission_date);
  }
}, { immediate: true, deep: true });


const genderOptions = ref([
  { label: 'Nam', value: 'male' },
  { label: 'Nữ', value: 'female' },
  { label: 'Khác', value: 'other' }
]);

// Vuelidate rules
const rules = computed(() => {
  const commonRules = {
    username: { required, minLength: minLength(3), maxLength: maxLength(50) },
    email: { required, email, maxLength: maxLength(100) },
    full_name: { required, minLength: minLength(3), maxLength: maxLength(100) },
    date_of_birth: { required },
    gender: { required },
    phone_number: {
      maxLength: maxLength(15),
      isValidPhone: helpers.withMessage('Số điện thoại không hợp lệ.', helpers.regex(/^[0-9]{9,15}$/))
    },
    address: { maxLength: maxLength(255) },
    student_id: { required, minLength: minLength(5), maxLength: maxLength(20) },
    major_id: { required },
    class_id: { required },
    admission_date: { required }
  };

  if (!props.isEditMode) {
    return {
      ...commonRules,
      password: { required, minLength: minLength(6) },
      confirm_password: {
        required,
        sameAsPassword: helpers.withMessage('Mật khẩu xác nhận không khớp.', sameAs(formData.password))
      }
    };
  }
  return commonRules;
});

const v$ = useVuelidate(rules, formData);

const submitForm = async () => {
  const result = await v$.value.$validate();
  if (result) {
    const dataToSend = { ...formData };
    // Convert Date objects to ISO string or desired format (e.g., YYYY-MM-DD)
    if (dataToSend.date_of_birth) {
      dataToSend.date_of_birth = dataToSend.date_of_birth.toISOString().split('T')[0];
    }
    if (dataToSend.admission_date) {
      dataToSend.admission_date = dataToSend.admission_date.toISOString().split('T')[0];
    }
    
    // Remove password fields if in edit mode and they are empty
    if (props.isEditMode && (!dataToSend.password || dataToSend.password === '')) {
      delete dataToSend.password;
      delete dataToSend.confirm_password;
    }

    emit('submit', dataToSend);
  } else {
    notificationStore.showToast('Vui lòng kiểm tra lại các trường bị lỗi!', 'error', 'Lỗi nhập liệu');
  }
};

const cancelForm = () => {
  emit('cancel');
};
</script>

<style scoped>
.student-form-card {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  border-radius: var(--p-card-border-radius);
  box-shadow: var(--p-card-shadow);
}

.p-mb-4 {
  margin-bottom: 1.5rem !important;
}
</style>