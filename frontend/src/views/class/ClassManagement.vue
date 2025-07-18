<template>
  <div class="class-management-content" aria-label="Phần quản lý lớp học">
    <Toolbar class="toolbar">
      <template #start>
        <h2>Quản Lý Lớp Học</h2>
      </template>
      <template #end>
        <Button v-if="canEditClasses" icon="pi pi-plus" label="Thêm Lớp" severity="primary" class="mr-2" @click="openNew" v-tooltip="'Thêm lớp mới'" aria-label="Thêm lớp mới" />
        <Button v-if="canExportData" icon="pi pi-download" label="Export" severity="success" @click="exportClasses" v-tooltip="'Xuất danh sách lớp'" aria-label="Xuất danh sách lớp" />
        <Button icon="pi pi-filter" label="Lớp Active" severity="info" class="mr-2" @click="loadActiveClasses" v-tooltip="'Lọc lớp đang hoạt động'" aria-label="Lọc lớp đang hoạt động" />
      </template>
    </Toolbar>
    <div class="filter-bar">
      <Dropdown v-model="filters.status" :options="statusOptions" optionLabel="label" optionValue="value" placeholder="Lọc trạng thái" class="filter-dropdown mr-2" @change="emit('loadClasses')" />
      <Dropdown v-model="filters.department" :options="departments" optionLabel="department_name" optionValue="department_id" placeholder="Lọc khoa" class="filter-dropdown mr-2" @change="emit('loadClasses')" />
      <Dropdown v-model="filters.semester" :options="semesters" optionLabel="semester_name" optionValue="semester_id" placeholder="Lọc học kỳ" class="filter-dropdown mr-2" @change="emit('loadClasses')" />
      <Dropdown v-model="filters.subject" :options="subjects" optionLabel="subject_name" optionValue="subject_id" placeholder="Lọc môn học" class="filter-dropdown mr-2" @change="emit('loadClasses')" />
      <InputText v-model="filters.global" placeholder="Tìm mã, tên, mô tả..." class="filter-search" @input="debouncedLoadClasses" aria-label="Tìm kiếm lớp học" />
    </div>
    <DataTable
      :value="classes"
      :loading="loading"
      dataKey="class_id"
      lazy
      :paginator="true"
      :rows="paginatorInfo.rows"
      :rowsPerPageOptions="[5, 10, 20]"
      :totalRecords="paginatorInfo.total"
      @page="onPage"
      class="p-datatable-sm"
      aria-label="Bảng danh sách lớp học"
    >
      <template #empty>
        <div class="empty-message"><i class="pi pi-info-circle" /><span>Không tìm thấy lớp học nào.</span></div>
      </template>
      <template #loading>
        <div class="loading-message"><ProgressSpinner style="width: 24px; height: 24px;" /><span>Đang tải dữ liệu...</span></div>
      </template>
      <Column field="class_id" header="Mã Lớp" sortable style="width: 12%" />
      <Column field="class_name" header="Tên Lớp" sortable style="width: 18%" />
      <Column field="description" header="Mô Tả" sortable style="width: 18%" />
      <Column field="department.department_name" header="Khoa" sortable style="width: 15%" />
      <Column field="credits" header="Tín Chỉ" sortable style="width: 8%" align="center" />
      <Column field="semester.semester_name" header="Học Kỳ" sortable style="width: 12%" align="center" />
      <Column field="subject.subject_name" header="Môn Học" sortable style="width: 12%" align="center" />
      <Column field="status" header="Trạng Thái" sortable style="width: 120px" align="center">
        <template #body="{ data }">
          <Tag :severity="getStatusSeverity(data.status)" :value="getStatusLabel(data.status)" />
        </template>
      </Column>
      <Column field="is_active" header="Hoạt Động" sortable style="width: 110px" align="center">
        <template #body="{ data }">
          <Tag :severity="data.is_active ? 'success' : 'warning'" :value="data.is_active ? 'Có' : 'Không'" />
        </template>
      </Column>
      <Column header="Hành Động" style="width: 15%" align="center">
        <template #body="{ data }">
          <Button v-if="canEditClasses && !data.is_deleted" icon="pi pi-pencil" outlined rounded class="mr-2" severity="info" @click="editClass(data)" v-tooltip="'Sửa thông tin'" aria-label="Sửa lớp" />
          <Button v-if="canDeleteClasses && !data.is_deleted" icon="pi pi-trash" outlined rounded severity="danger" class="mr-2" @click="confirmDelete(data)" v-tooltip="'Xóa mềm'" aria-label="Xóa mềm lớp" />
          <Button v-if="canDeleteClasses && data.is_deleted" icon="pi pi-undo" outlined rounded severity="success" @click="restoreClass(data)" v-tooltip="'Khôi phục'" aria-label="Khôi phục lớp" />
          <Button icon="pi pi-sync" outlined rounded severity="secondary" @click="openChangeStatus(data)" v-tooltip="'Thay đổi trạng thái'" aria-label="Thay đổi trạng thái lớp" />
        </template>
      </Column>
    </DataTable>
    <Dialog v-model:visible="classDialog" :header="classObj.class_id ? 'Sửa Lớp' : 'Thêm Lớp'" modal class="p-fluid" style="width: 600px;" aria-labelledby="class-dialog-header">
      <h3 id="class-dialog-header" class="sr-only">{{ classObj.class_id ? 'Sửa Lớp' : 'Thêm Lớp' }}</h3>
      <div class="form-section">
        <h4>Thông Tin Cơ Bản</h4>
        <div class="field">
          <label for="class_id">Mã Lớp</label>
          <InputText id="class_id" v-model="classObj.class_id" :class="{ 'p-invalid': errors.class_id }" :disabled="!!classObj.class_id" />
          <small class="p-error" v-if="errors.class_id">{{ errors.class_id }}</small>
        </div>
        <div class="field">
          <label for="class_name">Tên Lớp</label>
          <InputText id="class_name" v-model="classObj.class_name" :class="{ 'p-invalid': errors.class_name }" />
          <small class="p-error" v-if="errors.class_name">{{ errors.class_name }}</small>
        </div>
        <div class="field">
          <label for="description">Mô Tả</label>
          <Textarea id="description" v-model="classObj.description" rows="4" />
        </div>
        <div class="field">
          <label for="department">Khoa</label>
          <Dropdown id="department" v-model="classObj.department" :options="departments" optionLabel="department_name" optionValue="department_id" placeholder="Chọn khoa" />
        </div>
        <div class="field">
          <label for="credits">Số Tín Chỉ</label>
          <InputNumber id="credits" v-model="classObj.credits" :min="1" :class="{ 'p-invalid': errors.credits }" />
          <small class="p-error" v-if="errors.credits">{{ errors.credits }}</small>
        </div>
        <div class="field">
          <label for="is_active">Đang Hoạt Động</label>
          <InputSwitch id="is_active" v-model="classObj.is_active" />
        </div>
      </div>
      <div class="form-section">
        <h4>Quan Hệ</h4>
        <div class="field">
          <label for="semester">Học Kỳ</label>
          <Dropdown id="semester" v-model="classObj.semester" :options="semesters" optionLabel="semester_name" optionValue="semester_id" placeholder="Chọn học kỳ" :class="{ 'p-invalid': errors.semester }" />
          <small class="p-error" v-if="errors.semester">{{ errors.semester }}</small>
        </div>
        <div class="field">
          <label for="subject">Môn Học</label>
          <Dropdown id="subject" v-model="classObj.subject" :options="subjects" optionLabel="subject_name" optionValue="subject_id" placeholder="Chọn môn học" :class="{ 'p-invalid': errors.subject }" />
          <small class="p-error" v-if="errors.subject">{{ errors.subject }}</small>
        </div>
        <div class="field">
          <label for="teacher">Giảng Viên</label>
          <Dropdown id="teacher" v-model="classObj.teacher" :options="teachers" optionLabel="last_name" optionValue="teacher_id" placeholder="Chọn giảng viên" />
        </div>
        <div class="field">
          <label for="teachers">Danh Sách Giảng Viên</label>
          <MultiSelect id="teachers" v-model="classObj.teachers" :options="teachers" optionLabel="last_name" optionValue="teacher_id" placeholder="Chọn giảng viên" display="chip" />
        </div>
        <div class="field">
          <label for="subjects">Danh Sách Môn Học</label>
          <MultiSelect id="subjects" v-model="classObj.subjects" :options="subjects" optionLabel="subject_name" optionValue="subject_id" placeholder="Chọn môn học" display="chip" />
        </div>
      </div>
      <div class="form-section">
        <h4>Trạng Thái</h4>
        <div class="field">
          <label for="status">Trạng Thái</label>
          <Dropdown id="status" v-model="classObj.status" :options="statusOptions" optionLabel="label" optionValue="value" placeholder="Chọn trạng thái" :class="{ 'p-invalid': errors.status }" />
          <small class="p-error" v-if="errors.status">{{ errors.status }}</small>
        </div>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="hideDialog" aria-label="Hủy" />
        <Button label="Lưu" icon="pi pi-check" @click="saveClass" aria-label="Lưu lớp" />
      </template>
    </Dialog>
    <Dialog v-model:visible="deleteClassDialog" header="Xác Nhận Xóa Mềm" modal style="width: 400px;" aria-labelledby="delete-dialog-header">
      <h3 id="delete-dialog-header" class="sr-only">Xác Nhận Xóa Mềm</h3>
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span>Bạn có chắc muốn xóa lớp <b>{{ classObj.class_name }}</b>?</span>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="deleteClassDialog = false" aria-label="Hủy" />
        <Button label="Xóa" icon="pi pi-check" severity="danger" @click="deleteClass" aria-label="Xóa mềm lớp" />
      </template>
    </Dialog>
    <Dialog v-model:visible="hardDeleteClassDialog" header="Xác Nhận Xóa Cứng" modal style="width: 400px;" aria-labelledby="hard-delete-dialog-header">
      <h3 id="hard-delete-dialog-header" class="sr-only">Xác Nhận Xóa Cứng</h3>
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span>Bạn có chắc muốn xóa hoàn toàn lớp <b>{{ classObj.class_name }}</b>? Hành động này không thể hoàn tác.</span>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="hardDeleteClassDialog = false" aria-label="Hủy" />
        <Button label="Xóa" icon="pi pi-check" severity="danger" @click="hardDeleteClass" aria-label="Xóa cứng lớp" />
      </template>
    </Dialog>
    <Dialog v-model:visible="changeStatusDialog" header="Thay Đổi Trạng Thái" modal style="width: 400px;" aria-labelledby="status-dialog-header">
      <h3 id="status-dialog-header" class="sr-only">Thay Đổi Trạng Thái</h3>
      <div class="field">
        <label for="new_status">Trạng Thái Mới</label>
        <Dropdown id="new_status" v-model="newStatus" :options="statusOptions" optionLabel="label" optionValue="value" placeholder="Chọn trạng thái mới" :class="{ 'p-invalid': submitted && !newStatus }" />
        <small class="p-error" v-if="submitted && !newStatus">Vui lòng chọn trạng thái mới.</small>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="changeStatusDialog = false" aria-label="Hủy" />
        <Button label="Cập Nhật" icon="pi pi-check" @click="changeStatus" aria-label="Cập nhật trạng thái" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useUserStore } from '@/stores/user';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';
import { saveAs } from 'file-saver';
import api, { endpoints } from '@/services/api';
import Toolbar from 'primevue/toolbar';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import MultiSelect from 'primevue/multiselect';
import Tag from 'primevue/tag';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Dialog from 'primevue/dialog';
import ProgressSpinner from 'primevue/progressspinner';
import { debounce } from 'lodash';

const props = defineProps({
  classes: { type: Array, required: true },
  filters: { type: Object, required: true },
  paginatorInfo: { type: Object, required: true },
});
const emit = defineEmits(['update:classes', 'loadClasses']);

const userStore = useUserStore();
const toast = useToast();
const confirm = useConfirm();

const classObj = ref({ status: 'active', is_active: true, credits: 3 });
const classDialog = ref(false);
const deleteClassDialog = ref(false);
const hardDeleteClassDialog = ref(false);
const changeStatusDialog = ref(false);
const loading = ref(false);
const errors = ref({});
const newStatus = ref('');
const submitted = ref(false);
const departments = ref([]);
const semesters = ref([]);
const subjects = ref([]);
const teachers = ref([]);

const canEditClasses = computed(() => userStore.isAdmin || userStore.isTeacher);
const canDeleteClasses = computed(() => userStore.isAdmin);
const canExportData = computed(() => userStore.isAdmin);

const statusOptions = [
  { label: 'Đang hoạt động', value: 'active' },
  { label: 'Không hoạt động', value: 'inactive' },
  { label: 'Đang chờ duyệt', value: 'pending' },
];

const debouncedLoadClasses = debounce(() => emit('loadClasses'), 500);

onMounted(async () => {
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

const loadActiveClasses = async () => {
  try {
    loading.value = true;
    const response = await api.get(`${endpoints.classes}active/`);
    emit('update:classes', response.data);
    toast.add({ severity: 'info', summary: 'Thành công', detail: 'Hiển thị các lớp đang hoạt động', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải lớp đang hoạt động', life: 3000 });
  } finally {
    loading.value = false;
  }
};

const openNew = () => {
  classObj.value = { status: 'active', is_active: true, credits: 3, teachers: [], subjects: [] };
  errors.value = {};
  submitted.value = false;
  classDialog.value = true;
};

const hideDialog = () => {
  classDialog.value = false;
  errors.value = {};
  submitted.value = false;
};

const editClass = (data) => {
  classObj.value = { ...data, teachers: data.teachers || [], subjects: data.subjects || [] };
  errors.value = {};
  submitted.value = false;
  classDialog.value = true;
};

const confirmDelete = (data) => {
  classObj.value = { ...data };
  deleteClassDialog.value = true;
};

const confirmHardDelete = (data) => {
  classObj.value = { ...data };
  hardDeleteClassDialog.value = true;
};

const openChangeStatus = (data) => {
  classObj.value = { ...data };
  newStatus.value = data.status;
  submitted.value = false;
  changeStatusDialog.value = true;
};

const validateClass = () => {
  errors.value = {};
  if (!classObj.value.class_id?.trim()) errors.value.class_id = 'Vui lòng nhập mã lớp';
  if (!classObj.value.class_name?.trim()) errors.value.class_name = 'Vui lòng nhập tên lớp';
  if (!classObj.value.credits || classObj.value.credits < 1) errors.value.credits = 'Số tín chỉ phải lớn hơn 0';
  if (!classObj.value.semester) errors.value.semester = 'Vui lòng chọn học kỳ';
  if (!classObj.value.subject) errors.value.subject = 'Vui lòng chọn môn học';
  if (!classObj.value.status) errors.value.status = 'Vui lòng chọn trạng thái';
  if (classObj.value.status === 'active' && !classObj.value.is_active) {
    errors.value.is_active = 'Lớp đang hoạt động phải có trạng thái is_active là True';
  }
};

const saveClass = async () => {
  submitted.value = true;
  validateClass();
  if (Object.keys(errors.value).length > 0) return;
  try {
    const payload = {
      ...classObj.value,
      teachers: classObj.value.teachers || [],
      subjects: classObj.value.subjects || [],
    };
    let updatedClasses;
    if (classObj.value.class_id) {
      const updatedClass = (await api.patch(`${endpoints.classes}${classObj.value.class_id}/`, payload)).data;
      updatedClasses = props.classes.map(c => c.class_id === updatedClass.class_id ? updatedClass : c);
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật lớp học thành công', life: 3000 });
    } else {
      const newClass = (await api.post(endpoints.classes, payload)).data;
      updatedClasses = [...props.classes, newClass];
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Thêm lớp học thành công', life: 3000 });
    }
    emit('update:classes', updatedClasses);
    classDialog.value = false;
    classObj.value = {};
  } catch (error) {
    const errorMsg = error.response?.data?.detail || Object.values(error.response?.data || {}).join(', ') || 'Không thể lưu thông tin lớp học';
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errorMsg, life: 5000 });
  }
};

const deleteClass = async () => {
  try {
    await api.delete(`${endpoints.classes}${classObj.value.class_id}/`);
    const updatedClasses = props.classes.filter(c => c.class_id !== classObj.value.class_id);
    emit('update:classes', updatedClasses);
    deleteClassDialog.value = false;
    classObj.value = {};
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa mềm lớp học thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa lớp học', life: 3000 });
  }
};

const hardDeleteClass = async () => {
  try {
    await api.delete(`${endpoints.classes}${classObj.value.class_id}/hard-delete/`);
    const updatedClasses = props.classes.filter(c => c.class_id !== classObj.value.class_id);
    emit('update:classes', updatedClasses);
    hardDeleteClassDialog.value = false;
    classObj.value = {};
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa hoàn toàn lớp học thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa hoàn toàn lớp học', life: 3000 });
  }
};

const changeStatus = async () => {
  submitted.value = true;
  if (!newStatus.value) return;
  try {
    const updatedClass = (await api.post(`${endpoints.classes}${classObj.value.class_id}/change-status/`, { status: newStatus.value })).data;
    const updatedClasses = props.classes.map(c => c.class_id === updatedClass.class_id ? updatedClass : c);
    emit('update:classes', updatedClasses);
    changeStatusDialog.value = false;
    classObj.value = {};
    newStatus.value = '';
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật trạng thái thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể cập nhật trạng thái', life: 3000 });
  }
};

const restoreClass = async (data) => {
  try {
    const response = await api.post(`${endpoints.classes}${data.class_id}/restore/`);
    emit('loadClasses');
    toast.add({ severity: 'success', summary: 'Thành công', detail: response.data.message || 'Khôi phục lớp học thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể khôi phục lớp học', life: 3000 });
  }
};

const exportClasses = async () => {
  try {
    const response = await api.get(`${endpoints.classes}export/`, { responseType: 'blob' });
    const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
    saveAs(blob, `classes_${new Date().toISOString().split('T')[0]}.xlsx`);
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xuất danh sách lớp học thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xuất danh sách lớp học', life: 3000 });
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
.class-management-content {
  padding: 24px;
  background-color: #f9fafb;
  border-radius: 8px;
}
.toolbar {
  margin-bottom: 16px;
}
.filter-bar {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-bottom: 16px;
}
.filter-dropdown {
  width: 200px;
}
.filter-search {
  width: 250px;
  padding: 8px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
}
.empty-message, .loading-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px;
  color: #6b7280;
}
.form-section {
  margin-bottom: 24px;
}
.form-section h4 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 16px;
}
.field {
  margin-bottom: 16px;
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
.confirmation-content {
  display: flex;
  align-items: center;
  gap: 12px;
}
.p-datatable-sm :deep(.p-datatable-tbody > tr > td),
.p-datatable-sm :deep(.p-datatable-thead > tr > th) {
  padding: 12px;
}
.p-datatable-sm :deep(.p-datatable-thead > tr > th) {
  background: #f8f9fa;
  font-size: 14px;
  font-weight: 500;
}
.p-datatable-sm :deep(.p-datatable-tbody > tr > td) {
  border-right: 1px solid #f4f4f4;
}
.p-datatable-sm :deep(.p-button) {
  width: 28px;
  height: 28px;
  padding: 0;
  font-size: 14px;
}
</style>