<template>
  <div class="class-info-section" aria-label="Phần thông tin lớp học">
    <div class="card-header">
      <h2>Thông Tin Lớp</h2>
      <Button
        v-if="!isEditing && canEditClasses"
        icon="pi pi-pencil"
        label="Chỉnh Sửa"
        severity="primary"
        @click="openEdit"
        v-tooltip="'Chỉnh sửa thông tin lớp'"
        aria-label="Chỉnh sửa thông tin lớp"
      />
    </div>
    <div v-if="!isEditing" class="profile-details">
      <div class="detail-item"><label>Mã Lớp:</label><span>{{ classDetail.class_id }}</span></div>
      <div class="detail-item"><label>Tên Lớp:</label><span>{{ classDetail.class_name }}</span></div>
      <div class="detail-item"><label>Mô Tả:</label><span>{{ classDetail.description || 'N/A' }}</span></div>
      <div class="detail-item"><label>Khoa:</label><span>{{ classDetail.department?.department_name || 'N/A' }}</span></div>
      <div class="detail-item"><label>Số Tín Chỉ:</label><span>{{ classDetail.credits || 'N/A' }}</span></div>
      <div class="detail-item"><label>Học Kỳ:</label><span>{{ classDetail.semester?.semester_name || 'N/A' }}</span></div>
      <div class="detail-item"><label>Môn Học:</label><span>{{ classDetail.subject?.subject_name || 'N/A' }}</span></div>
      <div class="detail-item"><label>Giảng Viên:</label><span>{{ classDetail.teacher?.last_name }} {{ classDetail.teacher?.first_name || 'N/A' }}</span></div>
      <div class="detail-item"><label>Trạng Thái:</label><Tag :severity="getStatusSeverity(classDetail.status)" :value="getStatusLabel(classDetail.status)" /></div>
      <div class="detail-item"><label>Hoạt Động:</label><Tag :severity="classDetail.is_active ? 'success' : 'warning'" :value="classDetail.is_active ? 'Có' : 'Không'" /></div>
    </div>
    <div v-else class="edit-form">
      <div class="field">
        <label for="class_id">Mã Lớp</label>
        <InputText id="class_id" v-model="classDetail.class_id" disabled />
      </div>
      <div class="field">
        <label for="class_name">Tên Lớp</label>
        <InputText id="class_name" v-model="classDetail.class_name" :class="{ 'p-invalid': errors.class_name }" />
        <small class="p-error" v-if="errors.class_name">{{ errors.class_name }}</small>
      </div>
      <div class="field">
        <label for="description">Mô Tả</label>
        <Textarea id="description" v-model="classDetail.description" rows="4" />
      </div>
      <div class="field">
        <label for="department">Khoa</label>
        <Dropdown id="department" v-model="classDetail.department" :options="departments" optionLabel="department_name" optionValue="department_id" placeholder="Chọn khoa" />
      </div>
      <div class="field">
        <label for="credits">Số Tín Chỉ</label>
        <InputNumber id="credits" v-model="classDetail.credits" :min="1" :class="{ 'p-invalid': errors.credits }" />
        <small class="p-error" v-if="errors.credits">{{ errors.credits }}</small>
      </div>
      <div class="field">
        <label for="is_active">Đang Hoạt Động</label>
        <InputSwitch id="is_active" v-model="classDetail.is_active" />
      </div>
      <div class="field">
        <label for="semester">Học Kỳ</label>
        <Dropdown id="semester" v-model="classDetail.semester" :options="semesters" optionLabel="semester_name" optionValue="semester_id" placeholder="Chọn học kỳ" :class="{ 'p-invalid': errors.semester }" />
        <small class="p-error" v-if="errors.semester">{{ errors.semester }}</small>
      </div>
      <div class="field">
        <label for="subject">Môn Học</label>
        <Dropdown id="subject" v-model="classDetail.subject" :options="subjects" optionLabel="subject_name" optionValue="subject_id" placeholder="Chọn môn học" :class="{ 'p-invalid': errors.subject }" />
        <small class="p-error" v-if="errors.subject">{{ errors.subject }}</small>
      </div>
      <div class="field">
        <label for="teacher">Giảng Viên</label>
        <Dropdown id="teacher" v-model="classDetail.teacher" :options="teachers" optionLabel="last_name" optionValue="teacher_id" placeholder="Chọn giảng viên" />
      </div>
      <div class="buttons">
        <Button label="Hủy" icon="pi pi-times" text @click="cancelEdit" aria-label="Hủy chỉnh sửa" />
        <Button label="Lưu" icon="pi pi-check" @click="saveClassDetail" aria-label="Lưu thông tin lớp" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useUserStore } from '@/stores/user';
import { useToast } from 'primevue/usetoast';
import { gsap } from 'gsap';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';
import Dropdown from 'primevue/dropdown';
import InputNumber from 'primevue/inputnumber';
import InputSwitch from 'primevue/inputswitch';
import Tag from 'primevue/tag';
import api, { endpoints } from '@/services/api';

const props = defineProps({
  classDetail: { type: Object, required: true },
  isEditing: { type: Boolean, required: true },
});
const emit = defineEmits(['update:classDetail', 'update:isEditing']);

const userStore = useUserStore();
const toast = useToast();

const errors = ref({});
const departments = ref([]);
const semesters = ref([]);
const subjects = ref([]);
const teachers = ref([]);

const canEditClasses = computed(() => userStore.isAdmin || userStore.isTeacher);
const isTeacher = computed(() => userStore.isTeacher);
const isStudent = computed(() => userStore.isStudent);

onMounted(async () => {
  gsap.from('.class-info-section', { opacity: 0, y: 20, duration: 0.5 });
  await Promise.all([loadDepartments(), loadSemesters(), loadSubjects(), loadTeachers()]);
});

const loadDepartments = async () => {
  try {
    const response = await api.get(endpoints.departments);
    departments.value = Array.isArray(response.data) ? response.data : response.data.results || [];
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách khoa', life: 3000 });
  }
};

const loadSemesters = async () => {
  try {
    const response = await api.get(endpoints.semesters);
    semesters.value = Array.isArray(response.data) ? response.data : response.data.results || [];
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách học kỳ', life: 3000 });
  }
};

const loadSubjects = async () => {
  try {
    const response = await api.get(endpoints.subjects);
    subjects.value = Array.isArray(response.data) ? response.data : response.data.results || [];
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách môn học', life: 3000 });
  }
};

const loadTeachers = async () => {
  try {
    const response = await api.get(endpoints.teachers);
    teachers.value = Array.isArray(response.data) ? response.data : response.data.results || [];
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách giảng viên', life: 3000 });
  }
};

const openEdit = () => {
  emit('update:isEditing', true);
  errors.value = {};
};

const cancelEdit = () => {
  emit('update:isEditing', false);
  emit('update:classDetail', { ...props.classDetail });
  toast.add({ severity: 'info', summary: 'Hủy', detail: 'Đã hủy chỉnh sửa', life: 3000 });
};

const saveClassDetail = async () => {
  errors.value = {};
  if (!props.classDetail.class_name?.trim()) errors.value.class_name = 'Vui lòng nhập tên lớp';
  if (!props.classDetail.credits || props.classDetail.credits < 1) errors.value.credits = 'Số tín chỉ phải lớn hơn 0';
  if (!props.classDetail.semester) errors.value.semester = 'Vui lòng chọn học kỳ';
  if (!props.classDetail.subject) errors.value.subject = 'Vui lòng chọn môn học';
  if (Object.keys(errors.value).length > 0) return;

  try {
    const payload = {
      class_name: props.classDetail.class_name,
      description: props.classDetail.description,
      department: props.classDetail.department,
      credits: props.classDetail.credits,
      is_active: props.classDetail.is_active,
      semester: props.classDetail.semester,
      subject: props.classDetail.subject,
      teacher: props.classDetail.teacher,
    };
    const response = await api.patch(`${endpoints.classes}${props.classDetail.class_id}/`, payload);
    emit('update:classDetail', response.data);
    emit('update:isEditing', false);
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật thông tin lớp thành công', life: 3000 });
  } catch (error) {
    const errorMsg = error.response?.data?.detail || Object.values(error.response?.data || {}).join(', ') || 'Không thể cập nhật thông tin lớp';
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errorMsg, life: 5000 });
  }
};

const getStatusLabel = (status) => {
  const map = { active: 'Đang hoạt động', inactive: 'Không hoạt động', pending: 'Đang chờ duyệt' };
  return map[status] || status;
};

const getStatusSeverity = (status) => {
  const map = { active: 'success', inactive: 'warning', pending: 'info' };
  return map[status] || 'info';
};
</script>

<style scoped>
.class-info-section {
  padding: 24px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  border-bottom: 1px solid #e5e7eb;
}
.card-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
}
.profile-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}
.detail-item {
  padding: 12px;
}
.detail-item label {
  font-weight: 500;
  margin-right: 8px;
  color: #374151;
}
.edit-form {
  display: grid;
  gap: 16px;
}
.field {
  display: flex;
  flex-direction: column;
}
.field label {
  font-weight: 500;
  margin-bottom: 4px;
  color: #374151;
}
.buttons {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 16px;
}
</style>