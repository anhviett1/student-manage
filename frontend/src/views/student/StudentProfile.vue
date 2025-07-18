<template>
  <div class="student-profile-section" aria-label="Phần thông tin cá nhân sinh viên">
    <Toast aria-live="polite" />
    <div class="profile-section">
      <Toolbar class="toolbar">
        <template #start>
          <h2>Thông Tin Sinh Viên</h2>
        </template>
        <template #end>
          <Button
            v-if="!isEditing"
            icon="pi pi-pencil"
            label="Chỉnh Sửa"
            severity="primary"
            @click="openEdit"
            v-tooltip="'Chỉnh sửa thông tin cá nhân'"
            aria-label="Chỉnh sửa thông tin cá nhân"
          />
        </template>
      </Toolbar>
      <div v-if="!isEditing" class="profile-details">
        <div class="detail-item">
          <label>Mã Sinh Viên:</label>
          <span>{{ student.student_id }}</span>
        </div>
        <div class="detail-item">
          <label>Họ và Tên:</label>
          <span>{{ student.full_name }}</span>
        </div>
        <div class="detail-item">
          <label>Email:</label>
          <span>{{ student.email }}</span>
        </div>
        <div class="detail-item">
          <label>Số Điện Thoại:</label>
          <span>{{ student.phone || 'Chưa cập nhật' }}</span>
        </div>
        <div class="detail-item">
          <label>Ngày Sinh:</label>
          <span>{{ formatDate(student.date_of_birth) }}</span>
        </div>
        <div class="detail-item">
          <label>Giới Tính:</label>
          <span>{{ getGenderLabel(student.gender) }}</span>
        </div>
        <div class="detail-item">
          <label>Địa Chỉ:</label>
          <span>{{ student.address || '' }}, {{ student.city || '' }}, {{ student.state || '' }}, {{ student.country || '' }}</span>
        </div>
        <div class="detail-item">
          <label>Chuyên Ngành:</label>
          <span>{{ student.major }}</span>
        </div>
        <div class="detail-item">
          <label>GPA:</label>
          <span>{{ student.gpa }}</span>
        </div>
        <div class="detail-item">
          <label>Trạng Thái:</label>
          <Tag :severity="getStatusSeverity(student.status)" :value="getStatusLabel(student.status)" />
        </div>
      </div>
      <div v-else class="edit-form">
        <div class="form-section">
          <h4>Thông Tin Cá Nhân</h4>
          <div class="field">
            <label for="student_id">Mã Sinh Viên</label>
            <InputText id="student_id" v-model="editStudent.student_id" disabled />
          </div>
          <div class="field">
            <label for="first_name">Tên</label>
            <InputText id="first_name" v-model="editStudent.first_name" :class="{ 'p-invalid': errors.first_name }" />
            <small class="p-error" v-if="errors.first_name">{{ errors.first_name }}</small>
          </div>
          <div class="field">
            <label for="last_name">Họ</label>
            <InputText id="last_name" v-model="editStudent.last_name" :class="{ 'p-invalid': errors.last_name }" />
            <small class="p-error" v-if="errors.last_name">{{ errors.last_name }}</small>
          </div>
          <div class="field">
            <label for="email">Email</label>
            <InputText id="email" v-model="editStudent.email" :class="{ 'p-invalid': errors.email }" />
            <small class="p-error" v-if="errors.email">{{ errors.email }}</small>
          </div>
          <div class="field">
            <label for="phone">Số Điện Thoại</label>
            <InputText id="phone" v-model="editStudent.phone" :class="{ 'p-invalid': errors.phone }" />
            <small class="p-error" v-if="errors.phone">{{ errors.phone }}</small>
          </div>
          <div class="field">
            <label for="date_of_birth">Ngày Sinh</label>
            <Calendar id="date_of_birth" v-model="editStudent.date_of_birth" :showIcon="true" dateFormat="yy-mm-dd" :class="{ 'p-invalid': errors.date_of_birth }" />
            <small class="p-error" v-if="errors.date_of_birth">{{ errors.date_of_birth }}</small>
          </div>
          <div class="field">
            <label for="gender">Giới Tính</label>
            <Dropdown id="gender" v-model="editStudent.gender" :options="genderOptions" optionLabel="label" optionValue="value" :class="{ 'p-invalid': errors.gender }" />
            <small class="p-error" v-if="errors.gender">{{ errors.gender }}</small>
          </div>
          <div class="field">
            <label for="address">Địa Chỉ</label>
            <Textarea id="address" v-model="editStudent.address" rows="3" :class="{ 'p-invalid': errors.address }" />
            <small class="p-error" v-if="errors.address">{{ errors.address }}</small>
          </div>
          <div class="field">
            <label for="city">Thành Phố</label>
            <InputText id="city" v-model="editStudent.city" :class="{ 'p-invalid': errors.city }" />
            <small class="p-error" v-if="errors.city">{{ errors.city }}</small>
          </div>
          <div class="field">
            <label for="state">Tỉnh/Thành</label>
            <InputText id="state" v-model="editStudent.state" :class="{ 'p-invalid': errors.state }" />
            <small class="p-error" v-if="errors.state">{{ errors.state }}</small>
          </div>
          <div class="field">
            <label for="country">Quốc Gia</label>
            <InputText id="country" v-model="editStudent.country" :class="{ 'p-invalid': errors.country }" />
            <small class="p-error" v-if="errors.country">{{ errors.country }}</small>
          </div>
        </div>
        <div class="buttons">
          <Button label="Hủy" icon="pi pi-times" text @click="cancelEdit" aria-label="Hủy chỉnh sửa" />
          <Button label="Lưu" icon="pi pi-check" @click="saveStudent" aria-label="Lưu thông tin sinh viên" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useToast } from 'primevue/usetoast';
import { gsap } from 'gsap';
import Toolbar from 'primevue/toolbar';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';
import Dropdown from 'primevue/dropdown';
import Calendar from 'primevue/calendar';
import Tag from 'primevue/tag';
import Toast from 'primevue/toast';
import api, { endpoints } from '@/services/api';

const props = defineProps({
  student: { type: Object, required: true },
});
const emit = defineEmits(['update:student', 'loadProfile']);

const toast = useToast();
const isEditing = ref(false);
const editStudent = ref({});
const errors = ref({});

const genderOptions = [
  { label: 'Nam', value: 'M' },
  { label: 'Nữ', value: 'F' },
  { label: 'Khác', value: 'O' },
];

const statusOptions = [
  { label: 'Đang học', value: 'active' },
  { label: 'Tạm nghỉ', value: 'inactive' },
  { label: 'Đã tốt nghiệp', value: 'graduated' },
  { label: 'Bị đình chỉ', value: 'suspended' },
  { label: 'Nghỉ phép', value: 'on_leave' },
];

onMounted(() => {
  gsap.from('.student-profile-section', { opacity: 0, y: 20, duration: 0.5 });
  editStudent.value = { ...props.student };
});

const openEdit = () => {
  isEditing.value = true;
  editStudent.value = {
    ...props.student,
    date_of_birth: props.student.date_of_birth ? new Date(props.student.date_of_birth) : null,
  };
  errors.value = {};
};

const cancelEdit = () => {
  isEditing.value = false;
  editStudent.value = { ...props.student };
  emit('loadProfile');
};

const validateStudent = () => {
  errors.value = {};
  if (!editStudent.value.first_name?.trim()) errors.value.first_name = 'Vui lòng nhập tên';
  if (!editStudent.value.last_name?.trim()) errors.value.last_name = 'Vui lòng nhập họ';
  if (!editStudent.value.email?.trim()) errors.value.email = 'Vui lòng nhập email';
  else if (!/\S+@\S+\.\S+/.test(editStudent.value.email)) errors.value.email = 'Email không hợp lệ';
  if (editStudent.value.phone && !/^\d{10,11}$/.test(editStudent.value.phone)) errors.value.phone = 'Số điện thoại không hợp lệ';
  if (!editStudent.value.date_of_birth) errors.value.date_of_birth = 'Vui lòng chọn ngày sinh';
  if (!editStudent.value.gender) errors.value.gender = 'Vui lòng chọn giới tính';
  if (!editStudent.value.address?.trim()) errors.value.address = 'Vui lòng nhập địa chỉ';
  if (!editStudent.value.city?.trim()) errors.value.city = 'Vui lòng nhập thành phố';
  if (!editStudent.value.state?.trim()) errors.value.state = 'Vui lòng nhập tỉnh/thành';
  if (!editStudent.value.country?.trim()) errors.value.country = 'Vui lòng nhập quốc gia';
};

const saveStudent = async () => {
  validateStudent();
  if (Object.keys(errors.value).length > 0) return;
  try {
    const formData = new FormData();
    Object.keys(editStudent.value).forEach((key) => {
      if (editStudent.value[key] !== null && editStudent.value[key] !== undefined) {
        if (key === 'date_of_birth' && editStudent.value[key]) {
          formData.append(key, editStudent.value[key].toISOString().split('T')[0]);
        } else {
          formData.append(key, editStudent.value[key]);
        }
      }
    });
    const response = await api.put(`${endpoints.students}${editStudent.value.id}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    emit('update:student', response.data);
    isEditing.value = false;
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật thông tin thành công', life: 3000 });
  } catch (error) {
    const errorMsg = error.response?.data?.detail || Object.values(error.response?.data || {}).join(', ') || 'Không thể lưu thông tin';
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errorMsg, life: 3000 });
  }
};

const formatDate = (date) => {
  if (!date) return 'Chưa cập nhật';
  return new Date(date).toLocaleDateString('vi-VN', { year: 'numeric', month: '2-digit', day: '2-digit' });
};

const getGenderLabel = (gender) => {
  const map = { M: 'Nam', F: 'Nữ', O: 'Khác' };
  return map[gender] || gender;
};

const getStatusLabel = (status) => {
  const map = {
    active: 'Đang học',
    inactive: 'Tạm nghỉ',
    graduated: 'Đã tốt nghiệp',
    suspended: 'Bị đình chỉ',
    on_leave: 'Nghỉ phép',
  };
  return map[status] || status;
};

const getStatusSeverity = (status) => {
  const map = {
    active: 'success',
    inactive: 'warning',
    graduated: 'info',
    suspended: 'danger',
    on_leave: 'secondary',
  };
  return map[status] || 'info';
};
</script>

<style scoped>
.student-profile-section {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px;
}
.toolbar {
  margin-bottom: 16px;
}
.profile-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}
.detail-item {
  padding: 8px;
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
.form-section h4 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 16px;
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
.field .p-error {
  font-size: 12px;
  color: #ef4444;
}
.buttons {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>