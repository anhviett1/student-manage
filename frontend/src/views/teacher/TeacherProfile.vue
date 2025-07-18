<template>
  <div class="teacher-profile-container" aria-label="Thông tin giảng viên">
    <div class="profile-header">
      <h2>Thông Tin Giảng Viên</h2>
      <Button
        icon="pi pi-pencil"
        label="Chỉnh Sửa"
        severity="primary"
        @click="openEdit"
        v-if="!isEditing"
        v-tooltip="'Chỉnh sửa thông tin cá nhân'"
      />
    </div>
    <div v-if="!isEditing" class="profile-details">
      <div class="detail-item">
        <label>Mã Giảng Viên:</label>
        <span>{{ teacher.teacher_id }}</span>
      </div>
      <div class="detail-item">
        <label>Họ và Tên:</label>
        <span>{{ teacher.full_name }}</span>
      </div>
      <div class="detail-item">
        <label>Email:</label>
        <span>{{ teacher.email }}</span>
      </div>
      <div class="detail-item">
        <label>Số Điện Thoại:</label>
        <span>{{ teacher.phone }}</span>
      </div>
      <div class="detail-item">
        <label>Ngày Sinh:</label>
        <span>{{ formatDate(teacher.date_of_birth) }}</span>
      </div>
      <div class="detail-item">
        <label>Giới Tính:</label>
        <span>{{ getGenderLabel(teacher.gender) }}</span>
      </div>
      <div class="detail-item">
        <label>Địa Chỉ:</label>
        <span>{{ teacher.address }}</span>
      </div>
      <div class="detail-item">
        <label>Học Vị:</label>
        <span>{{ getDegreeLabel(teacher.degree) }}</span>
      </div>
      <div class="detail-item">
        <label>Chuyên Ngành:</label>
        <span>{{ teacher.specialization }}</span>
      </div>
      <div class="detail-item">
        <label>Trạng Thái:</label>
        <Tag :severity="getStatusSeverity(teacher.status)" :value="getStatusLabel(teacher.status)" />
      </div>
    </div>
    <div v-else class="edit-form">
      <div class="field">
        <label for="teacher_id">Mã Giảng Viên</label>
        <InputText id="teacher_id" v-model="teacher.teacher_id" disabled />
      </div>
      <div class="field">
        <label for="first_name">Tên</label>
        <InputText id="first_name" v-model="teacher.first_name" :class="{ 'p-invalid': errors.first_name }" />
        <small class="p-error" v-if="errors.first_name">{{ errors.first_name }}</small>
      </div>
      <div class="field">
        <label for="last_name">Họ</label>
        <InputText id="last_name" v-model="teacher.last_name" :class="{ 'p-invalid': errors.last_name }" />
        <small class="p-error" v-if="errors.last_name">{{ errors.last_name }}</small>
      </div>
      <div class="field">
        <label for="email">Email</label>
        <InputText id="email" v-model="teacher.email" :class="{ 'p-invalid': errors.email }" />
        <small class="p-error" v-if="errors.email">{{ errors.email }}</small>
      </div>
      <div class="field">
        <label for="phone">Số Điện Thoại</label>
        <InputText id="phone" v-model="teacher.phone" :class="{ 'p-invalid': errors.phone }" />
        <small class="p-error" v-if="errors.phone">{{ errors.phone }}</small>
      </div>
      <div class="field">
        <label for="date_of_birth">Ngày Sinh</label>
        <Calendar id="date_of_birth" v-model="teacher.date_of_birth" :showIcon="true" dateFormat="yy-mm-dd" :class="{ 'p-invalid': errors.date_of_birth }" />
        <small class="p-error" v-if="errors.date_of_birth">{{ errors.date_of_birth }}</small>
      </div>
      <div class="field">
        <label for="gender">Giới Tính</label>
        <Dropdown id="gender" v-model="teacher.gender" :options="genderOptions" optionLabel="label" optionValue="value" :class="{ 'p-invalid': errors.gender }" />
        <small class="p-error" v-if="errors.gender">{{ errors.gender }}</small>
      </div>
      <div class="field">
        <label for="address">Địa Chỉ</label>
        <Textarea id="address" v-model="teacher.address" rows="3" :class="{ 'p-invalid': errors.address }" />
        <small class="p-error" v-if="errors.address">{{ errors.address }}</small>
      </div>
      <div class="buttons">
        <Button label="Hủy" icon="pi pi-times" text @click="cancelEdit" />
        <Button label="Lưu" icon="pi pi-check" @click="saveTeacher" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref } from 'vue';
import { useToast } from 'primevue/usetoast';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Calendar from 'primevue/calendar';
import Dropdown from 'primevue/dropdown';
import Textarea from 'primevue/textarea';
import Tag from 'primevue/tag';
import api, { endpoints } from '@/services/api';

const props = defineProps({
  teacher: { type: Object, required: true },
});

const emit = defineEmits(['update:teacher', 'loadProfile']);
const toast = useToast();
const isEditing = ref(false);
const errors = ref({});

const genderOptions = [
  { label: 'Nam', value: 'M' },
  { label: 'Nữ', value: 'F' },
  { label: 'Khác', value: 'O' },
];

const openEdit = () => {
  isEditing.value = true;
  errors.value = {};
};

const cancelEdit = () => {
  isEditing.value = false;
  emit('loadProfile');
};

const saveTeacher = async () => {
  try {
    const response = await api.put(`${endpoints.teachers}${props.teacher.teacher_id}/`, props.teacher);
    emit('update:teacher', response.data.data);
    isEditing.value = false;
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật thông tin giảng viên thành công', life: 3000 });
  } catch (error) {
    errors.value = error.response?.data || {};
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể cập nhật thông tin giảng viên', life: 3000 });
  }
};

const formatDate = (date) => {
  if (!date) return '';
  const d = new Date(date);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
};

const getGenderLabel = (gender) => {
  const map = { M: 'Nam', F: 'Nữ', O: 'Khác' };
  return map[gender] || gender;
};

const getStatusLabel = (status) => {
  const map = {
    active: 'Đang giảng dạy',
    inactive: 'Tạm nghỉ',
    retired: 'Đã nghỉ hưu',
    on_leave: 'Nghỉ phép',
  };
  return map[status] || status;
};

const getStatusSeverity = (status) => {
  const map = {
    active: 'success',
    inactive: 'warning',
    retired: 'info',
    on_leave: 'secondary',
  };
  return map[status] || 'info';
};

const getDegreeLabel = (degree) => {
  const map = {
    bachelor: 'Cử nhân',
    master: 'Thạc sĩ',
    phd: 'Tiến sĩ',
    professor: 'Giáo sư',
  };
  return map[degree] || degree;
};
</script>

<style scoped>
.teacher-profile-container {
  padding: 16px;
}
.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}
.profile-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}
.detail-item {
  padding: 0.5rem;
}
.detail-item label {
  font-weight: bold;
  margin-right: 0.5rem;
}
.edit-form {
  display: grid;
  gap: 1rem;
}
.field {
  display: flex;
  flex-direction: column;
}
.buttons {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}
.p-tag {
  font-size: 0.95em;
  padding: 0.2em 0.7em;
}
</style>