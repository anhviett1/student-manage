<template>
  <p-card class="department-form-card">
    <template #title>
      <i class="mdi mdi-office-building-outline p-mr-2"></i> {{ isEditMode ? 'Chỉnh sửa Phòng ban' : 'Thêm Phòng ban Mới' }}
    </template>
    <template #content>
      <form @submit.prevent="submitForm" class="p-fluid p-formgrid p-grid p-jc-center">
        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-input-text id="deptName" v-model="formData.name" :class="{'p-invalid': v$.name.$error}" />
            <label for="deptName">Tên Phòng ban</label>
          </span>
          <small class="p-error" v-for="error of v$.name.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-input-text id="deptCode" v-model="formData.code" :class="{'p-invalid': v$.code.$error}" />
            <label for="deptCode">Mã Phòng ban (duy nhất)</label>
          </span>
          <small class="p-error" v-for="error of v$.code.$errors" :key="error.$uid">{{ error.$message }}</small>
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
import { required, minLength, maxLength } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import { useNotificationStore } from '@/stores/notification'; // Giả sử bạn có notification store

// PrimeVue Components
import PCard from 'primevue/card';
import PInputText from 'primevue/inputtext';
import PTextarea from 'primevue/textarea';
import PButton from 'primevue/button';

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({
      name: '',
      code: '',
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

// Watch initialData changes to update formData (important when opening form in edit mode)
watch(() => props.initialData, (newVal) => {
  Object.assign(formData, newVal);
}, { immediate: true, deep: true });

// Rules for Vuelidate
const rules = computed(() => ({
  name: { required, minLength: minLength(3), maxLength: maxLength(100) },
  code: { required, minLength: minLength(2), maxLength: maxLength(10) },
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
.department-form-card {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  border-radius: var(--p-card-border-radius);
  box-shadow: var(--p-card-shadow);
}

.p-mb-4 {
  margin-bottom: 1.5rem !important; /* Khoảng cách giữa các input */
}
</style>