<template>
  <div class="subject-management-container" aria-label="Quản lý môn học">
    <h2>Quản Lý Môn Học</h2>
    <div class="header">
      <div class="action-buttons">
        <Button
          icon="pi pi-plus"
          label="Thêm Môn Học"
          severity="primary"
          class="mr-2"
          @click="openNew"
          v-tooltip="'Thêm môn học mới'"
        />
        <Button
          icon="pi pi-download"
          label="Export"
          severity="success"
          @click="exportSubjects"
          v-tooltip="'Xuất danh sách môn học'"
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
          @change="emit('loadSubjects')"
        />
        <Dropdown
          v-model="filters.department"
          :options="departments"
          optionLabel="name"
          optionValue="id"
          placeholder="Lọc khoa"
          class="filter-dropdown mr-2"
          @change="emit('loadSubjects')"
        />
        <InputText
          v-model="filters.global"
          placeholder="Tìm mã, tên môn học..."
          class="filter-search"
          @input="emit('loadSubjects')"
        />
      </div>
    </div>
    <DataTable
      :value="subjects"
      :paginator="true"
      :rows="paginatorInfo.rows"
      :totalRecords="paginatorInfo.total"
      :lazy="true"
      @page="onPage($event)"
      dataKey="subject_id"
      responsiveLayout="scroll"
      class="p-datatable-sm"
      aria-label="Bảng danh sách môn học"
    >
      <template #empty>
        <div class="empty-message">
          <i class="pi pi-info-circle" />
          <span>Không tìm thấy môn học nào.</span>
        </div>
      </template>
      <template #loading>
        <div class="loading-message">
          <i class="pi pi-spin pi-spinner" />
          <span>Đang tải dữ liệu...</span>
        </div>
      </template>
      <Column field="subject_id" header="Mã Môn Học" sortable style="width: 15%" />
      <Column field="name" header="Tên Môn Học" sortable style="width: 25%" />
      <Column field="credits" header="Số Tín Chỉ" sortable style="width: 10%" align="center" />
      <Column field="semester.name" header="Học Kỳ" sortable style="width: 15%" />
      <Column field="department.name" header="Khoa" sortable style="width: 15%" />
      <Column field="status" header="Trạng Thái" sortable style="width: 10%" align="center">
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
            class="mr-2"
            severity="info"
            @click="editSubject(data)"
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
            @click="restoreSubject(data)"
            v-tooltip="'Khôi phục'"
          />
        </template>
      </Column>
    </DataTable>
    <div v-if="!subjects.length && !loading" class="no-data-message">
      <p>Không có dữ liệu môn học để hiển thị.</p>
      <Button label="Tải lại" icon="pi pi-refresh" @click="emit('loadSubjects')" severity="secondary" />
    </div>
    <Dialog
      v-model:visible="subjectDialog"
      :header="subject.subject_id ? 'Sửa Môn Học' : 'Thêm Môn Học'"
      :style="{ width: '500px' }"
      :modal="true"
      class="p-fluid"
    >
      <div class="form-section">
        <div class="field">
          <label for="subject_id">Mã Môn Học</label>
          <InputText id="subject_id" v-model="subject.subject_id" :class="{ 'p-invalid': errors.subject_id }" :disabled="!!subject.subject_id" />
          <small class="p-error" v-if="errors.subject_id">{{ errors.subject_id }}</small>
        </div>
        <div class="field">
          <label for="name">Tên Môn Học</label>
          <InputText id="name" v-model="subject.name" :class="{ 'p-invalid': errors.name }" />
          <small class="p-error" v-if="errors.name">{{ errors.name }}</small>
        </div>
        <div class="field">
          <label for="description">Mô Tả</label>
          <Textarea id="description" v-model="subject.description" rows="4" />
        </div>
        <div class="field">
          <label for="credits">Số Tín Chỉ</label>
          <InputNumber id="credits" v-model="subject.credits" :min="1" :max="10" :class="{ 'p-invalid': errors.credits }" />
          <small class="p-error" v-if="errors.credits">{{ errors.credits }}</small>
        </div>
        <div class="field">
          <label for="semester">Học Kỳ</label>
          <Dropdown id="semester" v-model="subject.semester_id" :options="semesters" optionLabel="name" optionValue="id" placeholder="Chọn học kỳ" :class="{ 'p-invalid': errors.semester_id }" />
          <small class="p-error" v-if="errors.semester_id">{{ errors.semester_id }}</small>
        </div>
        <div class="field">
          <label for="department">Khoa</label>
          <Dropdown id="department" v-model="subject.department_id" :options="departments" optionLabel="name" optionValue="id" placeholder="Chọn khoa" :class="{ 'p-invalid': errors.department_id }" />
          <small class="p-error" v-if="errors.department_id">{{ errors.department_id }}</small>
        </div>
        <div class="field">
          <label for="status">Trạng Thái</label>
          <Dropdown id="status" v-model="subject.status" :options="statusOptions" optionLabel="label" optionValue="value" :class="{ 'p-invalid': errors.status }" />
          <small class="p-error" v-if="errors.status">{{ errors.status }}</small>
        </div>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="hideDialog" />
        <Button label="Lưu" icon="pi pi-check" @click="saveSubject" />
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
        <span>Bạn có chắc muốn xóa môn học <b>{{ subject.name }}</b>?</span>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="deleteDialog = false" />
        <Button label="Xóa" icon="pi pi-check" severity="danger" @click="deleteSubject" />
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
import InputNumber from 'primevue/inputnumber';
import api, { endpoints } from '@/services/api';

const props = defineProps({
  subjects: { type: Array, required: true },
  filters: { type: Object, required: true },
  paginatorInfo: { type: Object, required: true },
  departments: { type: Array, required: true },
  semesters: { type: Array, required: true },
});

const emit = defineEmits(['update:subjects', 'loadSubjects', 'loadDepartments', 'loadSemesters']);
const toast = useToast();
const subject = ref({});
const subjectDialog = ref(false);
const deleteDialog = ref(false);
const errors = ref({});

const statusOptions = [
  { label: 'Đang hoạt động', value: 'active' },
  { label: 'Không hoạt động', value: 'inactive' },
  { label: 'Đang chờ duyệt', value: 'pending' },
];

const onPage = (event) => {
  emit('loadSubjects', event.page + 1, event.rows);
};

const openNew = () => {
  subject.value = {
    status: 'pending',
    is_active: true,
    credits: 3,
    department_id: null,
    semester_id: null,
  };
  errors.value = {};
  subjectDialog.value = true;
};

const editSubject = (data) => {
  subject.value = {
    ...data,
    department_id: data.department ? data.department.id : null,
    semester_id: data.semester ? data.semester.id : null,
  };
  errors.value = {};
  subjectDialog.value = true;
};

const hideDialog = () => {
  subjectDialog.value = false;
  subject.value = {};
  errors.value = {};
};

const confirmDelete = (data) => {
  subject.value = data;
  deleteDialog.value = true;
};

const validateSubject = () => {
  errors.value = {};
  if (!subject.value.subject_id) errors.value.subject_id = 'Vui lòng nhập mã môn học';
  if (!subject.value.subject_id.startsWith('MH')) errors.value.subject_id = 'Mã môn học phải bắt đầu bằng "MH"';
  if (!subject.value.name) errors.value.name = 'Vui lòng nhập tên môn học';
  if (subject.value.name && (subject.value.name.length < 3 || subject.value.name.length > 200)) {
    errors.value.name = 'Tên môn học phải từ 3 đến 200 ký tự';
  }
  if (!subject.value.credits) errors.value.credits = 'Vui lòng nhập số tín chỉ';
  if (subject.value.credits < 1 || subject.value.credits > 10) errors.value.credits = 'Số tín chỉ phải từ 1 đến 10';
  if (!subject.value.department_id) errors.value.department_id = 'Vui lòng chọn khoa';
  if (!subject.value.status) errors.value.status = 'Vui lòng chọn trạng thái';
};

const saveSubject = async () => {
  validateSubject();
  if (Object.keys(errors.value).length > 0) return;

  try {
    const payload = { ...subject.value };
    let response;
    if (subject.value.subject_id) {
      response = await api.patch(`${endpoints.subjects}${subject.value.subject_id}/`, payload);
      emit('update:subjects', props.subjects.map(s => s.subject_id === subject.value.subject_id ? response.data : s));
    } else {
      response = await api.post(endpoints.subjects, payload);
      emit('update:subjects', [...props.subjects, response.data]);
    }
    toast.add({ severity: 'success', summary: 'Thành công', detail: `Cập nhật môn học thành công`, life: 3000 });
    hideDialog();
  } catch (error) {
    const errorMsg = error.response?.data?.detail || Object.values(error.response?.data || {}).join(', ') || 'Không thể lưu môn học';
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errorMsg, life: 3000 });
  }
};

const deleteSubject = async () => {
  try {
    await api.delete(`${endpoints.subjects}${subject.value.subject_id}/`);
    emit('update:subjects', props.subjects.filter(s => s.subject_id !== subject.value.subject_id));
    deleteDialog.value = false;
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa môn học thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa môn học', life: 3000 });
  }
};

const restoreSubject = async (data) => {
  try {
    const response = await api.post(`${endpoints.subjects}${data.subject_id}/restore/`);
    emit('update:subjects', props.subjects.map(s => s.subject_id === data.subject_id ? response.data.data : s));
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Khôi phục môn học thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: error.response?.data?.error || 'Không thể khôi phục môn học', life: 3000 });
  }
};

const exportSubjects = async () => {
  try {
    const params = {};
    if (props.filters.status) params.status = props.filters.status;
    if (props.filters.department) params.department_id = props.filters.department;
    if (props.filters.global) params.search = props.filters.global;
    const response = await api.get(`${endpoints.subjects}export/`, { params, responseType: 'blob' });
    const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
    saveAs(blob, `subjects_${new Date().toISOString().split('T')[0]}.xlsx`);
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xuất danh sách môn học thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xuất danh sách môn học', life: 3000 });
  }
};

const getStatusLabel = (status) => {
  const option = statusOptions.find(opt => opt.value === status);
  return option ? option.label : status;
};

const getStatusSeverity = (status) => {
  const map = { active: 'success', inactive: 'warning', pending: 'info' };
  return map[status] || 'info';
};
</script>

<style scoped>
.subject-management-container {
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
.no-data-message {
  text-align: center;
  padding: 3rem;
  color: #666;
  background: #f8f9fa;
  border-radius: 8px;
  margin: 1rem 0;
}
.no-data-message p {
  margin-bottom: 1rem;
  font-size: 1.1rem;
}
.form-section {
  margin-bottom: 1.5rem;
}
.field {
  margin-bottom: 1.2rem;
}
.field label {
  display: block;
  margin-bottom: 0.3rem;
  font-weight: bold;
}
.confirmation-content {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
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