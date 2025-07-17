<template>
  <p-card class="enrollment-form-card">
    <template #title>
      <i class="mdi mdi-account-plus-outline p-mr-2"></i> {{ isEditMode ? 'Chỉnh sửa Đăng ký' : 'Thêm Đăng ký Mới' }}
    </template>
    <template #content>
      <form @submit.prevent="submitForm" class="p-fluid p-formgrid p-grid p-jc-center">
        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-dropdown id="student" v-model="formData.student_id" :options="students" optionLabel="full_name" optionValue="id" placeholder="Chọn Sinh viên" :class="{'p-invalid': v$.student_id.$error}" filter />
            <label for="student">Sinh viên</label>
          </span>
          <small class="p-error" v-for="error of v$.student_id.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-dropdown id="course" v-model="formData.course_id" :options="courses" optionLabel="name" optionValue="id" placeholder="Chọn Môn học" :class="{'p-invalid': v$.course_id.$error}" filter />
            <label for="course">Môn học</label>
          </span>
          <small class="p-error" v-for="error of v$.course_id.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-dropdown id="semester" v-model="formData.semester_id" :options="semesters" optionLabel="name" optionValue="id" placeholder="Chọn Học kỳ" :class="{'p-invalid': v$.semester_id.$error}" />
            <label for="semester">Học kỳ</label>
          </span>
          <small class="p-error" v-for="error of v$.semester_id.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>
        
        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-calendar id="enrollDate" v-model="formData.enrollment_date" dateFormat="dd/mm/yy" :class="{'p-invalid': v$.enrollment_date.$error}" showIcon />
            <label for="enrollDate">Ngày đăng ký</label>
          </span>
          <small class="p-error" v-for="error of v$.enrollment_date.$errors" :key="error.$uid">{{ error.$message }}</small>
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
import { required } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import { useNotificationStore } from '@/stores/notification';

// PrimeVue Components
import PCard from 'primevue/card';
import PDropdown from 'primevue/dropdown';
import PCalendar from 'primevue/calendar';
import PButton from 'primevue/button';

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({
      student_id: null,
      course_id: null,
      semester_id: null,
      enrollment_date: null
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
  students: {
    type: Array,
    default: () => [] // Danh sách sinh viên { id: ..., full_name: ... }
  },
  courses: {
    type: Array,
    default: () => [] // Danh sách môn học { id: ..., name: ... }
  },
  semesters: {
    type: Array,
    default: () => [] // Danh sách học kỳ { id: ..., name: ... }
  }
});

const emit = defineEmits(['submit', 'cancel']);

const notificationStore = useNotificationStore();

const formData = reactive({ ...props.initialData });

watch(() => props.initialData, (newVal) => {
  Object.assign(formData, newVal);
  if (newVal.enrollment_date) {
    formData.enrollment_date = new Date(newVal.enrollment_date);
  }
}, { immediate: true, deep: true });

const rules = computed(() => ({
  student_id: { required },
  course_id: { required },
  semester_id: { required },
  enrollment_date: { required }
}));

const v$ = useVuelidate(rules, formData);

const submitForm = async () => {
  const result = await v$.value.$validate();
  if (result) {
    const dataToSend = { ...formData };
    if (dataToSend.enrollment_date) {
      dataToSend.enrollment_date = dataToSend.enrollment_date.toISOString().split('T')[0]; // Format YYYY-MM-DD
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
.enrollment-form-card {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  border-radius: var(--p-card-border-radius);
  box-shadow: var(--p-card-shadow);
}

.p-mb-4 {
  margin-bottom: 1.5rem !important;
}
</style>