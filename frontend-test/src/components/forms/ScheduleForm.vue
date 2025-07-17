<template>
  <p-card class="schedule-form-card">
    <template #title>
      <i class="mdi mdi-calendar-clock-outline p-mr-2"></i> {{ isEditMode ? 'Chỉnh sửa Lịch học' : 'Thêm Lịch học Mới' }}
    </template>
    <template #content>
      <form @submit.prevent="submitForm" class="p-fluid p-formgrid p-grid p-jc-center">
        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-dropdown id="course" v-model="formData.course_id" :options="courses" optionLabel="name" optionValue="id" placeholder="Chọn Môn học" :class="{'p-invalid': v$.course_id.$error}" filter />
            <label for="course">Môn học</label>
          </span>
          <small class="p-error" v-for="error of v$.course_id.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-dropdown id="teacher" v-model="formData.teacher_id" :options="teachers" optionLabel="full_name" optionValue="id" placeholder="Chọn Giáo viên" :class="{'p-invalid': v$.teacher_id.$error}" filter />
            <label for="teacher">Giáo viên</label>
          </span>
          <small class="p-error" v-for="error of v$.teacher_id.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-dropdown id="class" v-model="formData.class_id" :options="classes" optionLabel="name" optionValue="id" placeholder="Chọn Lớp" :class="{'p-invalid': v$.class_id.$error}" filter />
            <label for="class">Lớp học</label>
          </span>
          <small class="p-error" v-for="error of v$.class_id.$errors" :key="error.$uid">{{ error.$message }}</small>
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
            <p-dropdown id="dayOfWeek" v-model="formData.day_of_week" :options="dayOptions" placeholder="Chọn Ngày trong tuần" :class="{'p-invalid': v$.day_of_week.$error}" />
            <label for="dayOfWeek">Ngày trong tuần</label>
          </span>
          <small class="p-error" v-for="error of v$.day_of_week.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-calendar id="startTime" v-model="formData.start_time" dateFormat="HH:mm" timeOnly :class="{'p-invalid': v$.start_time.$error}" showIcon />
            <label for="startTime">Giờ bắt đầu</label>
          </span>
          <small class="p-error" v-for="error of v$.start_time.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-calendar id="endTime" v-model="formData.end_time" dateFormat="HH:mm" timeOnly :class="{'p-invalid': v$.end_time.$error}" showIcon />
            <label for="endTime">Giờ kết thúc</label>
          </span>
          <small class="p-error" v-for="error of v$.end_time.$errors" :key="error.$uid">{{ error.$message }}</small>
        </div>

        <div class="p-col-12 p-md-6">
          <span class="p-float-label p-mb-4">
            <p-input-text id="room" v-model="formData.room" :class="{'p-invalid': v$.room.$error}" />
            <label for="room">Phòng học</label>
          </span>
          <small class="p-error" v-for="error of v$.room.$errors" :key="error.$uid">{{ error.$message }}</small>
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
import { required, maxLength } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import { useNotificationStore } from '@/stores/notification';

// PrimeVue Components
import PCard from 'primevue/card';
import PDropdown from 'primevue/dropdown';
import PCalendar from 'primevue/calendar';
import PInputText from 'primevue/inputtext';
import PButton from 'primevue/button';

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({
      course_id: null,
      teacher_id: null,
      class_id: null,
      semester_id: null,
      day_of_week: null,
      start_time: null,
      end_time: null,
      room: ''
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
  courses: {
    type: Array,
    default: () => [] // Danh sách môn học { id: ..., name: ... }
  },
  teachers: {
    type: Array,
    default: () => [] // Danh sách giáo viên { id: ..., full_name: ... }
  },
  classes: {
    type: Array,
    default: () => [] // Danh sách lớp học { id: ..., name: ... }
  },
  semesters: {
    type: Array,
    default: () => [] // Danh sách học kỳ { id: ..., name: ... }
  }
});

const emit = defineEmits(['submit', 'cancel']);

const notificationStore = useNotificationStore();

const formData = reactive({ ...props.initialData });

// Convert time strings to Date objects for PCalendar
watch(() => props.initialData, (newVal) => {
  Object.assign(formData, newVal);
  if (newVal.start_time) {
    formData.start_time = new Date(`2000-01-01T${newVal.start_time}`);
  }
  if (newVal.end_time) {
    formData.end_time = new Date(`2000-01-01T${newVal.end_time}`);
  }
}, { immediate: true, deep: true });

const dayOptions = ref([
  'Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy', 'Chủ Nhật'
]);

const rules = computed(() => ({
  course_id: { required },
  teacher_id: { required },
  class_id: { required },
  semester_id: { required },
  day_of_week: { required },
  start_time: { required },
  end_time: { required },
  room: { required, maxLength: maxLength(50) }
}));

const v$ = useVuelidate(rules, formData);

const submitForm = async () => {
  const result = await v$.value.$validate();
  if (result) {
    const dataToSend = { ...formData };
    // Format Date objects back to time strings (HH:mm)
    dataToSend.start_time = dataToSend.start_time ? dataToSend.start_time.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false }) : null;
    dataToSend.end_time = dataToSend.end_time ? dataToSend.end_time.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false }) : null;
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
.schedule-form-card {
  width: 100%;
  max-width: 750px;
  margin: 0 auto;
  border-radius: var(--p-card-border-radius);
  box-shadow: var(--p-card-shadow);
}

.p-mb-4 {
  margin-bottom: 1.5rem !important;
}
</style>