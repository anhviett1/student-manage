<template>
  <div class="teacher-management-container" aria-label="Quản lý giảng viên">
    <h2>Quản Lý Giảng Viên</h2>
    <div class="header">
      <div class="action-buttons">
        <Button
          icon="pi pi-plus"
          label="Thêm Giảng Viên"
          severity="primary"
          class="mr-2"
          @click="openNew"
          v-tooltip="'Thêm giảng viên mới'"
        />
        <Button
          icon="pi pi-download"
          label="Export"
          severity="success"
          @click="exportTeachers"
          v-tooltip="'Xuất danh sách giảng viên'"
        />
      </div>
    </div>
    <div class="filter-bar">
      <div class="filter-group">
        <Dropdown
          v-model="filters.status"
          :options="statusOptions"
          optionLabel="label"
          optionValue="value"
          placeholder="Lọc trạng thái"
          class="filter-dropdown mr-2"
          @change="emit('loadTeachers')"
        />
        <Dropdown
          v-model="filters.department"
          :options="departments"
          optionLabel="name"
          optionValue="id"
          placeholder="Lọc khoa"
          class="filter-dropdown mr-2"
          @change="emit('loadTeachers')"
        />
        <Dropdown
          v-model="filters.degree"
          :options="degreeOptions"
          optionLabel="label"
          optionValue="value"
          placeholder="Lọc học vị"
          class="filter-dropdown mr-2"
          @change="emit('loadTeachers')"
        />
        <Dropdown
          v-model="filters.gender"
          :options="genderOptions"
          optionLabel="label"
          optionValue="value"
          placeholder="Lọc giới tính"
          class="filter-dropdown mr-2"
          @change="emit('loadTeachers')"
        />
        <InputText
          v-model="filters.searchTerm"
          placeholder="Tìm mã, tên, email..."
          class="filter-search"
          @input="emit('loadTeachers')"
        />
      </div>
    </div>
    <DataTable
      :value="teachers"
      :paginator="true"
      :rows="paginatorInfo.rows"
      :totalRecords="paginatorInfo.total"
      :lazy="true"
      @page="onPage($event)"
      dataKey="teacher_id"
      responsiveLayout="scroll"
      class="p-datatable-sm"
      aria-label="Bảng danh sách giảng viên"
    >
      <template #empty>
        <div class="empty-message">
          <i class="pi pi-info-circle" />
          <span>Không tìm thấy giảng viên nào.</span>
        </div>
      </template>
      <template #loading>
        <div class="loading-message">
          <i class="pi pi-spin pi-spinner" />
          <span>Đang tải dữ liệu...</span>
        </div>
      </template>
      <Column field="teacher_id" header="Mã Giảng Viên" sortable style="width: 12%" />
      <Column field="full_name" header="Họ và Tên" sortable style="width: 18%" />
      <Column field="email" header="Email" sortable style="width: 18%" />
      <Column field="specialization" header="Chuyên Ngành" sortable style="width: 15%" />
      <Column field="degree" header="Học Vị" sortable style="width: 10%" align="center">
        <template #body="{ data }">
          <span>{{ getDegreeLabel(data.degree) }}</span>
        </template>
      </Column>
      <Column field="status" header="Trạng Thái" sortable style="width: 12%" align="center">
        <template #body="{ data }">
          <Tag :severity="getStatusSeverity(data.status)" :value="getStatusLabel(data.status)" />
        </template>
      </Column>
      <Column header="Hành Động" style="width: 15%" align="center">
        <template #body="{ data }">
          <Button
            icon="pi pi-pencil"
            outlined
            rounded
            severity="info"
            @click="editTeacher(data)"
            v-tooltip="'Sửa thông tin'"
          />
          <Button
            v-if="!data.is_deleted"
            icon="pi pi-trash"
            outlined
            rounded
            severity="danger"
            class="mr-2"
            @click="confirmDelete(data)"
            v-tooltip="'Xóa mềm'"
          />
          <Button
            v-if="data.is_deleted"
            icon="pi pi-undo"
            outlined
            rounded
            severity="success"
            @click="restoreTeacher(data)"
            v-tooltip="'Khôi phục'"
          />
        </template>
      </Column>
    </DataTable>
    <Dialog
      v-model:visible="teacherDialog"
      :header="teacher.teacher_id ? 'Sửa Giảng Viên' : 'Thêm Giảng Viên'"
      :style="{ width: '600px' }"
      :modal="true"
      class="p-fluid"
    >
      <div class="form-section">
        <h4>Thông Tin Cơ Bản</h4>
        <div class="field">
          <label for="teacher_id">Mã Giảng Viên</label>
          <InputText id="teacher_id" v-model="teacher.teacher_id" :class="{ 'p-invalid': errors.teacher_id }" :disabled="!!teacher.teacher_id" />
          <small class="p-error" v-if="errors.teacher_id">{{ errors.teacher_id }}</small>
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
        <h4>Thông Tin Chuyên Môn</h4>
        <div class="field">
          <label for="degree">Học Vị</label>
          <Dropdown id="degree" v-model="teacher.degree" :options="degreeOptions" optionLabel="label" optionValue="value" :class="{ 'p-invalid': errors.degree }" />
          <small class="p-error" v-if="errors.degree">{{ errors.degree }}</small>
        </div>
        <div class="field">
          <label for="specialization">Chuyên Ngành</label>
          <InputText id="specialization" v-model="teacher.specialization" :class="{ 'p-invalid': errors.specialization }" />
          <small class="p-error" v-if="errors.specialization">{{ errors.specialization }}</small>
        </div>
        <div class="field">
          <label for="department">Khoa</label>
          <Dropdown id="department" v-model="teacher.department_id" :options="departments" optionLabel="name" optionValue="id" :class="{ 'p-invalid': errors.department_id }" />
          <small class="p-error" v-if="errors.department_id">{{ errors.department_id }}</small>
        </div>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="hideDialog" />
        <Button label="Lưu" icon="pi pi-check" @click="saveTeacher" />
      </template>
    </Dialog>
    <Dialog
      v-model:visible="deleteDialog"
      header="Xác Nhận Xóa"
      :style="{ width: '400px' }"
      :modal="true"
    >
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span>Bạn có chắc muốn xóa giảng viên <b>{{ teacher.full_name }}</b>?</span>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="deleteDialog = false" />
        <Button label="Xóa" icon="pi pi-check" severity="danger" @click="deleteTeacher" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref } from 'vue';
import { useToast } from 'primevue/usetoast';
import { saveAs } from 'file-saver';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';
import InputText from 'primevue/inputtext';
import Dialog from 'primevue/dialog';
import Tag from 'primevue/tag';
import Textarea from 'primevue/textarea';
import Calendar from 'primevue/calendar';
import api, { endpoints } from '@/services/api';

const props = defineProps({
  teachers: { type: Array, required: true },
  filters: { type: Object, required: true },
  paginatorInfo: { type: Object, required: true },
  departments: { type: Array, required: true },
});

const emit = defineEmits(['update:teachers', 'loadTeachers', 'loadDepartments']);
const toast = useToast();
const teacher = ref({});
const teacherDialog = ref(false);
const deleteDialog = ref(false);

const genderOptions = [
  { label: 'Nam', value: 'M' },
  { label: 'Nữ', value: 'F' },
  { label: 'Khác', value: 'O' },
];

const statusOptions = [
  { label: 'Đang giảng dạy', value: 'active' },
  { label: 'Tạm nghỉ', value: 'inactive' },
  { label: 'Đã nghỉ hưu', value: 'retired' },
  { label: 'Nghỉ phép', value: 'on_leave' },
];

const degreeOptions = [
  { label: 'Cử nhân', value: 'bachelor' },
  { label: 'Thạc sĩ', value: 'master' },
  { label: 'Tiến sĩ', value: 'phd' },
  { label: 'Giáo sư', value: 'professor' },
];

const onPage = (event) => {
  emit('loadTeachers', event.page + 1, event.rows);
};

const openNew = () => {
  teacher.value = {
    teacher_id: '',
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    date_of_birth: null,
    gender: 'M',
    address: '',
    degree: 'master',
    specialization: '',
    department_id: null,
    status: 'active',
  };
  teacherDialog.value = true;
};

const editTeacher = (data) => {
  teacher.value = { ...data };
  teacherDialog.value = true;
};

const hideDialog = () => {
  teacherDialog.value = false;
  teacher.value = {};
};

const saveTeacher = async () => {
  try {
    const formData = new FormData();
    Object.keys(teacher.value).forEach((key) => {
      if (teacher.value[key] !== null && teacher.value[key] !== undefined) {
        formData.append(key, teacher.value[key]);
      }
    });

    let response;
    if (teacher.value.teacher_id) {
      response = await api.put(`${endpoints.teachers}${teacher.value.teacher_id}/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
    } else {
      response = await api.post(endpoints.teachers, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
    }
    teacherDialog.value = false;
    toast.add({ severity: 'success', summary: 'Thành công', detail: response.data.message, life: 3000 });
    emit('loadTeachers');
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể lưu giảng viên', life: 3000 });
  }
};

const confirmDelete = (data) => {
  teacher.value = { ...data };
  deleteDialog.value = true;
};

const deleteTeacher = async () => {
  try {
    await api.delete(`${endpoints.teachers}${teacher.value.teacher_id}/`);
    deleteDialog.value = false;
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa giảng viên thành công', life: 3000 });
    emit('loadTeachers');
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa giảng viên', life: 3000 });
  }
};

const restoreTeacher = async (data) => {
  try {
    const response = await api.post(`${endpoints.teachers}${data.teacher_id}/restore/`);
    toast.add({ severity: 'success', summary: 'Thành công', detail: response.data.message, life: 3000 });
    emit('loadTeachers');
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể khôi phục giảng viên', life: 3000 });
  }
};

const exportTeachers = async () => {
  try {
    const params = {};
    if (props.filters.status) params.status = props.filters.status;
    if (props.filters.department) params.department_id = props.filters.department;
    if (props.filters.degree) params.degree = props.filters.degree;
    if (props.filters.gender) params.gender = props.filters.gender;
    if (props.filters.searchTerm) params.search = props.filters.searchTerm;
    const response = await api.get(`${endpoints.teachers}export/`, { params, responseType: 'blob' });
    const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
    saveAs(blob, `teachers_${new Date().toISOString().split('T')[0]}.xlsx`);
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xuất danh sách giảng viên thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xuất danh sách giảng viên', life: 3000 });
  }
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
.teacher-management-container {
  padding: 16px;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.action-buttons {
  display: flex;
  gap: 0.5rem;
}
.filter-bar {
  margin-bottom: 1rem;
}
.filter-group {
  display: flex;
  gap: 1rem;
}
.filter-dropdown {
  width: 200px;
}
.filter-search {
  width: 250px;
}
.empty-message, .loading-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 2rem;
  color: #666;
}
.form-section h4 {
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  color: #333;
}
.confirmation-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.p-datatable-sm :deep(.p-datatable-thead > tr > th) {
  background: #f8f9fa;
  padding: 0.85rem 1.1rem;
}
.p-datatable-sm :deep(.p-datatable-tbody > tr > td) {
  padding: 0.85rem 1.1rem;
}
.p-datatable-sm :deep(td .p-button) {
  min-width: 28px;
  height: 28px;
  width: 28px;
  padding: 0;
  font-size: 0.9rem;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.25rem;
}
.p-datatable-sm :deep(td .p-button:last-child) {
  margin-right: 0;
}
.p-datatable-sm :deep(td .p-button:hover) {
  box-shadow: 0 0 0 2px #c7d2fe;
}
.p-tag {
  font-size: 0.95em;
  padding: 0.2em 0.7em;
}
</style>