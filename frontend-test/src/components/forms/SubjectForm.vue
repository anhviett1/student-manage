<template>
  <p-card class="subject-form-card">
    <template #title>
      <i class="mdi mdi-book-open-variant p-mr-2"></i> {{ isEditMode ? 'Chỉnh sửa Môn học' : 'Thêm Môn học Mới' }}
    </template>
    <template #content>
      <form @submit.prevent="submitForm" class="p-fluid p-formgrid p-grid p-jc-center">
        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-input-text id="subjectName" v-model="formData.name" :class="{'p-invalid': v$.name.$error}" />
            <label for="subjectName">Tên Môn học</label>
          </span>
          <small class="p-error" v-for="error of v$.name.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-input-text id="subjectCode" v-model="formData.code" :class="{'p-invalid': v$.code.$error}" />
            <label for="subjectCode">Mã Môn học (duy nhất)</label>
          </span>
          <small class="p-error" v-for="error of v$.code.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-input-number id="credits" v-model="formData.credits" :class="{'p-invalid': v$.credits.$error}" mode="whole" :min="1" :max="10" />
            <label for="credits">Số tín chỉ</label>
          </span>
          <small class="p-error" v-for="error of v$.credits.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-input-number id="lectureHours" v-model="formData.lecture_hours" :class="{'p-invalid': v$.lecture_hours.$error}" mode="whole" :min="0" />
            <label for="lectureHours">Số giờ lý thuyết</label>
          </span>
          <small class="p-error" v-for="error of v$.lecture_hours.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-input-number id="labHours" v-model="formData.lab_hours" :class="{'p-invalid': v$.lab_hours.$error}" mode="whole" :min="0" />
            <label for="labHours">Số giờ thực hành</label>
          </span>
          <small class="p-error" v-for="error of v$.lab_hours.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-dropdown id="department" v-model="formData.department_id" :options="departments" optionLabel="name" optionValue="id" placeholder="Chọn Khoa/Bộ môn" :class="{'p-invalid': v$.department_id.$error}" />
            <label for="department">Khoa/Bộ môn quản lý</label>
          </span>
          <small class="p-error" v-for="error of v$.department_id.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12">
          <span class="p-float-label p-mb-4">
            <p-textarea id="description" v-model="formData.description" rows="3" :class="{'p-invalid': v$.description.$error}" />
            <label for="description">Mô tả môn học</label>
          </span>
          <small class="p-error" v-for="error of v$.description.$errors" :key="error.$uid">{{ error.$message }}</small>
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
import { required, minLength, maxLength, integer, minValue } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import { useNotificationStore } from '@/stores/notification';

// PrimeVue Components
import PCard from 'primevue/card';
import PInputText from 'primevue/inputtext';
import PInputNumber from 'primevue/inputnumber';
import PDropdown from 'primevue/dropdown';
import PTextarea from 'primevue/textarea';
import PButton from 'primevue/button';

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({
      name: '',
      code: '',
      credits: null,
      lecture_hours: null,
      lab_hours: null,
      department_id: null,
      description: ''
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
  departments: { // Danh sách các khoa/bộ môn
    type: Array,
    default: () => [] // Ví dụ: [{ id: 1, name: 'Công nghệ thông tin' }]
  }
});

const emit = defineEmits(['submit', 'cancel']);

const notificationStore = useNotificationStore();

const formData = reactive({ ...props.initialData });

// Watch initialData changes to update formData
watch(() => props.initialData, (newVal) => {
  Object.assign(formData, newVal);
}, { immediate: true, deep: true });

// Vuelidate rules
const rules = computed(() => ({
  name: { required, minLength: minLength(3), maxLength: maxLength(100) },
  code: { required, minLength: minLength(2), maxLength: maxLength(20) },
  credits: { required, integer, minValue: minValue(1), maxValue: maxValue(10) },
  lecture_hours: { required, integer, minValue: minValue(0) },
  lab_hours: { required, integer, minValue: minValue(0) },
  department_id: { required },
  description: { maxLength: maxLength(500) }
}));

const v$ = useVuelidate(rules, formData);

const submitForm = async () => {
  const result = await v$.value.$validate();
  if (result) {
    emit('submit', { ...formData });
  } else {
    notificationStore.showToast('Vui lòng kiểm tra lại các trường bị lỗi!', 'error', 'Lỗi nhập liệu');
  }
};

const cancelForm = () => {
  emit('cancel');
};
</script>

<style scoped>
.subject-form-card {
  width: 100%;
  max-width: 700px;
  margin: 0 auto;
  border-radius: var(--p-card-border-radius);
  box-shadow: var(--p-card-shadow);
}

.p-mb-4 {
  margin-bottom: 1.5rem !important;
}
</style>