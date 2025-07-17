<template>
  <p-card class="semester-form-card">
    <template #title>
      <i class="mdi mdi-calendar-range-outline p-mr-2"></i> {{ isEditMode ? 'Chỉnh sửa Học kỳ' : 'Thêm Học kỳ Mới' }}
    </template>
    <template #content>
      <form @submit.prevent="submitForm" class="p-fluid p-formgrid p-grid p-jc-center">
        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-input-text id="semesterName" v-model="formData.name" :class="{'p-invalid': v$.name.$error}" />
            <label for="semesterName">Tên Học kỳ (VD: HK1 2024-2025)</label>
          </span>
          <small class="p-error" v-for="error of v$.name.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-input-text id="semesterYear" v-model="formData.year" :class="{'p-invalid': v$.year.$error}" />
            <label for="semesterYear">Năm học (VD: 2024-2025)</label>
          </span>
          <small class="p-error" v-for="error of v$.year.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-calendar id="startDate" v-model="formData.start_date" dateFormat="dd/mm/yy" :class="{'p-invalid': v$.start_date.$error}" showIcon />
            <label for="startDate">Ngày bắt đầu</label>
          </span>
          <small class="p-error" v-for="error of v$.start_date.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-calendar id="endDate" v-model="formData.end_date" dateFormat="dd/mm/yy" :class="{'p-invalid': v$.end_date.$error}" showIcon />
            <label for="endDate">Ngày kết thúc</label>
          </span>
          <small class="p-error" v-for="error of v$.end_date.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12">
          <span class="p-float-label p-mb-4">
            <p-textarea id="description" v-model="formData.description" rows="3" :class="{'p-invalid': v$.description.$error}" />
            <label for="description">Mô tả</label>
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
import { required, minLength, maxLength, helpers } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import { useNotificationStore } from '@/stores/notification';

// PrimeVue Components
import PCard from 'primevue/card';
import PInputText from 'primevue/inputtext';
import PCalendar from 'primevue/calendar';
import PTextarea from 'primevue/textarea';
import PButton from 'primevue/button';

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({
      name: '',
      year: '',
      start_date: null,
      end_date: null,
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
  }
});

const emit = defineEmits(['submit', 'cancel']);

const notificationStore = useNotificationStore();

const formData = reactive({ ...props.initialData });

// Watch initialData changes to update formData and convert date strings to Date objects
watch(() => props.initialData, (newVal) => {
  Object.assign(formData, newVal);
  if (newVal.start_date) {
    formData.start_date = new Date(newVal.start_date);
  }
  if (newVal.end_date) {
    formData.end_date = new Date(newVal.end_date);
  }
}, { immediate: true, deep: true });

// Custom validator for end_date after start_date
const endDateAfterStartDate = (value, siblings) => {
  if (!value || !siblings.start_date) return true;
  return new Date(value) >= new Date(siblings.start_date);
};

// Vuelidate rules
const rules = computed(() => ({
  name: { required, minLength: minLength(5), maxLength: maxLength(50) },
  year: { required, maxLength: maxLength(9), pattern: helpers.regex(/^\d{4}-\d{4}$/) }, // Example: 2024-2025
  start_date: { required },
  end_date: {
    required,
    endDateAfterStartDate: helpers.withMessage('Ngày kết thúc phải sau hoặc bằng ngày bắt đầu.', endDateAfterStartDate)
  },
  description: { maxLength: maxLength(500) }
}));

const v$ = useVuelidate(rules, formData);

const submitForm = async () => {
  const result = await v$.value.$validate();
  if (result) {
    const dataToSend = { ...formData };
    // Convert Date objects to ISO string or desired format (e.g., YYYY-MM-DD)
    if (dataToSend.start_date) {
      dataToSend.start_date = dataToSend.start_date.toISOString().split('T')[0];
    }
    if (dataToSend.end_date) {
      dataToSend.end_date = dataToSend.end_date.toISOString().split('T')[0];
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
.semester-form-card {
  width: 100%;
  max-width: 650px;
  margin: 0 auto;
  border-radius: var(--p-card-border-radius);
  box-shadow: var(--p-card-shadow);
}

.p-mb-4 {
  margin-bottom: 1.5rem !important;
}
</style>