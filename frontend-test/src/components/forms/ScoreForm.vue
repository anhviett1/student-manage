<template>
  <p-card class="score-form-card">
    <template #title>
      <i class="mdi mdi-scoreboard-outline p-mr-2"></i> {{ isEditMode ? 'Chỉnh sửa Điểm' : 'Thêm Điểm Mới' }}
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
            <p-input-number id="score" v-model="formData.score" :class="{'p-invalid': v$.score.$error}" mode="decimal" :min="0" :max="10" :minFractionDigits="0" :maxFractionDigits="2" />
            <label for="score">Điểm số</label>
          </span>
          <small class="p-error" v-for="error of v$.score.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12">
          <span class="p-float-label p-mb-4">
            <p-textarea id="notes" v-model="formData.notes" rows="3" :class="{'p-invalid': v$.notes.$error}" />
            <label for="notes">Ghi chú</label>
          </span>
          <small class="p-error" v-for="error of v$.notes.$errors" :key="error.$uid">{{ error.$message }}</small>
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
import { required, minValue, maxValue, decimal, maxLength } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import { useNotificationStore } from '@/stores/notification';

// PrimeVue Components
import PCard from 'primevue/card';
import PDropdown from 'primevue/dropdown';
import PInputNumber from 'primevue/inputnumber';
import PTextarea from 'primevue/textarea';
import PButton from 'primevue/button';

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({
      student_id: null,
      course_id: null,
      semester_id: null,
      score: null,
      notes: ''
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
}, { immediate: true, deep: true });

const rules = computed(() => ({
  student_id: { required },
  course_id: { required },
  semester_id: { required },
  score: { required, decimal, minValue: minValue(0), maxValue: maxValue(10) },
  notes: { maxLength: maxLength(500) }
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
.score-form-card {
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