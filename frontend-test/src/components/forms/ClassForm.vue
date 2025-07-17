<template>
  <p-card class="class-form-card">
    <template #title>
      <i class="mdi mdi-google-classroom p-mr-2"></i> {{ isEditMode ? 'Chỉnh sửa Lớp học' : 'Thêm Lớp học Mới' }}
    </template>
    <template #content>
      <form @submit.prevent="submitForm" class="p-fluid p-formgrid p-grid p-jc-center">
        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-input-text id="className" v-model="formData.name" :class="{'p-invalid': v$.name.$error}" />
            <label for="className">Tên Lớp</label>
          </span>
          <small class="p-error" v-for="error of v$.name.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-input-text id="classCode" v-model="formData.code" :class="{'p-invalid': v$.code.$error}" />
            <label for="classCode">Mã Lớp (duy nhất)</label>
          </span>
          <small class="p-error" v-for="error of v$.code.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-dropdown id="department" v-model="formData.department_id" :options="departments" optionLabel="name" optionValue="id" placeholder="Chọn Khoa/Phòng ban" :class="{'p-invalid': v$.department_id.$error}" />
            <label for="department">Khoa/Phòng ban</label>
          </span>
          <small class="p-error" v-for="error of v$.department_id.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-input-number id="maxStudents" v-model="formData.max_students" :class="{'p-invalid': v$.max_students.$error}" mode="whole" :min="1" />
            <label for="maxStudents">Số lượng sinh viên tối đa</label>
          </span>
          <small class="p-error" v-for="error of v$.max_students.$errors" :key="error.$uid">{{ error.$message }}</small>
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
import { required, minLength, maxLength, integer, minValue } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import { useNotificationStore } from '@/stores/notification';

// PrimeVue Components
import PCard from 'primevue/card';
import PInputText from 'primevue/inputtext';
import PTextarea from 'primevue/textarea';
import PInputNumber from 'primevue/inputnumber';
import PDropdown from 'primevue/dropdown';
import PButton from 'primevue/button';

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({
      name: '',
      code: '',
      department_id: null,
      max_students: 50,
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
  // Danh sách các khoa/phòng ban để chọn
  departments: {
    type: Array,
    default: () => []
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
  department_id: { required },
  max_students: { required, integer, minValue: minValue(1) },
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
.class-form-card {
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