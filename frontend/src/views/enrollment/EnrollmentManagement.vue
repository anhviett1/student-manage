<template>
  <div class="enrollment-management-content" aria-label="Phần quản lý đăng ký">
    <Toolbar class="toolbar">
      <template #start>
        <h2>Quản Lý Đăng Ký</h2>
      </template>
      <template #end>
        <Button v-if="canEditEnrollments" icon="pi pi-plus" label="Thêm Đăng Ký" severity="primary" class="mr-2" @click="openNew" v-tooltip="'Thêm đăng ký mới'" aria-label="Thêm đăng ký mới" />
        <Button v-if="canExportData" icon="pi pi-download" label="Export" severity="success" @click="exportEnrollments" v-tooltip="'Xuất danh sách đăng ký'" aria-label="Xuất danh sách đăng ký" />
      </template>
    </Toolbar>
    <div class="filter-bar">
      <Dropdown v-model="filters.status" :options="statusOptions" optionLabel="label" optionValue="value" placeholder="Lọc trạng thái" class="filter-dropdown mr-2" @change="emit('loadEnrollments')" aria-label="Lọc theo trạng thái" />
      <Dropdown v-model="filters.semester" :options="semesters" optionLabel="semester_name" optionValue="semester_id" placeholder="Lọc học kỳ" class="filter-dropdown mr-2" @change="emit('loadEnrollments')" aria-label="Lọc theo học kỳ" />
      <InputText v-model="filters.global" placeholder="Tìm sinh viên, môn học, lớp..." class="filter-search" @input="debouncedLoadEnrollments" aria-label="Tìm kiếm đăng ký" />
    </div>
    <DataTable
      :value="enrollments"
      :loading="loading"
      dataKey="enrollment_id"
      lazy
      :paginator="true"
      :rows="paginatorInfo.rows"
      :rowsPerPageOptions="[5, 10, 20]"
      :totalRecords="paginatorInfo.total"
      @page="onPage"
      class="p-datatable-sm"
      aria-label="Bảng quản lý đăng ký"
    >
      <template #empty>
        <div class="empty-message"><i class="pi pi-info-circle" /><span>Không tìm thấy đăng ký nào.</span></div>
      </template>
      <template #loading>
        <div class="loading-message"><ProgressSpinner style="width: 24px; height: 24px;" /><span>Đang tải dữ liệu...</span></div>
      </template>
      <Column field="student.full_name" header="Sinh Viên" sortable style="width: 15%" />
      <Column field="subject.subject_name" header="Môn Học" sortable style="width: 15%" />
      <Column field="class_obj.class_id" header="Lớp" sortable style="width: 10%" />
      <Column field="semester.semester_name" header="Học Kỳ" sortable style="width: 15%" />
      <Column field="enrollment_date" header="Ngày Đăng Ký" sortable style="width: 12%" align="center">
        <template #body="{ data }">{{ formatDate(data.enrollment_date) }}</template>
      </Column>
      <Column field="status" header="Trạng Thái" sortable style="width: 12%" align="center">
        <template #body="{ data }"><Tag :severity="getStatusSeverity(data.status)" :value="getStatusLabel(data.status)" /></template>
      </Column>
      <Column field="is_active" header="Hoạt Động" sortable style="width: 10%" align="center">
        <template #body="{ data }"><Tag :severity="data.is_active ? 'success' : 'warning'" :value="data.is_active ? 'Có' : 'Không'" /></template>
      </Column>
      <Column header="Hành Động" style="width: 15%" align="center">
        <template #body="{ data }">
          <Button v-if="canEditEnrollments && !data.is_deleted" icon="pi pi-pencil" outlined rounded class="mr-2" severity="info" @click="editEnrollment(data)" v-tooltip="'Sửa thông tin'" aria-label="Sửa đăng ký" />
          <Button v-if="canDeleteEnrollments && !data.is_deleted" icon="pi pi-trash" outlined rounded severity="danger" class="mr-2" @click="confirmDelete(data)" v-tooltip="'Xóa mềm'" aria-label="Xóa mềm đăng ký" />
          <Button v-if="canDeleteEnrollments && data.is_deleted" icon="pi pi-undo" outlined rounded severity="success" @click="confirmRestore(data)" v-tooltip="'Khôi phục'" aria-label="Khôi phục đăng ký" />
          <Button icon="pi pi-sync" outlined rounded severity="secondary" @click="openChangeStatus(data)" v-tooltip="'Thay đổi trạng thái'" aria-label="Thay đổi trạng thái đăng ký" />
        </template>
      </Column>
    </DataTable>
    <Dialog v-model:visible="enrollmentDialog" :header="enrollmentObj.enrollment_id ? 'Sửa Đăng Ký' : 'Thêm Đăng Ký'" modal class="p-fluid" style="width: 600px;" aria-labelledby="enrollment-dialog-header">
      <h3 id="enrollment-dialog-header" class="sr-only">{{ enrollmentObj.enrollment_id ? 'Sửa Đăng Ký' : 'Thêm Đăng Ký' }}</h3>
      <div class="form-section">
        <h4>Thông Tin Đăng Ký</h4>
        <div class="field">
          <label for="student">Sinh Viên</label>
          <Dropdown id="student" v-model="enrollmentObj.student" :options="students" optionLabel="full_name" optionValue="student_id" placeholder="Chọn sinh viên" :class="{ 'p-invalid': errors.student }" />
          <small class="p-error" v-if="errors.student">{{ errors.student }}</small>
        </div>
        <div class="field">
          <label for="subject">Môn Học</label>
          <Dropdown id="subject" v-model="enrollmentObj.subject" :options="subjects" optionLabel="subject_name" optionValue="subject_id" placeholder="Chọn môn học" :class="{ 'p-invalid': errors.subject }" />
          <small class="p-error" v-if="errors.subject">{{ errors.subject }}</small>
        </div>
        <div class="field">
          <label for="semester">Học Kỳ</label>
          <Dropdown id="semester" v-model="enrollmentObj.semester" :options="semesters" optionLabel="semester_name" optionValue="semester_id" placeholder="Chọn học kỳ" :class="{ 'p-invalid': errors.semester }" />
          <small class="p-error" v-if="errors.semester">{{ errors.semester }}</small>
        </div>
        <div class="field">
          <label for="class_obj">Lớp</label>
          <Dropdown id="class_obj" v-model="enrollmentObj.class_obj" :options="classes" optionLabel="class_id" optionValue="class_id" placeholder="Chọn lớp" :class="{ 'p-invalid': errors.class_obj }" />
          <small class="p-error" v-if="errors.class_obj">{{ errors.class_obj }}</small>
        </div>
        <div class="field">
          <label for="enrollment_date">Ngày Đăng Ký</label>
          <Calendar id="enrollment_date" v-model="enrollmentObj.enrollment_date" :showIcon="true" dateFormat="yy-mm-dd" placeholder="Chọn ngày" :class="{ 'p-invalid': errors.enrollment_date }" />
          <small class="p-error" v-if="errors.enrollment_date">{{ errors.enrollment_date }}</small>
        </div>
        <div class="field">
          <label for="notes">Ghi Chú</label>
          <Textarea id="notes" v-model="enrollmentObj.notes" rows="3" placeholder="Ghi chú thêm (tùy chọn)" />
        </div>
        <div class="field">
          <label for="status">Trạng Thái</label>
          <Dropdown id="status" v-model="enrollmentObj.status" :options="statusOptions" optionLabel="label" optionValue="value" placeholder="Chọn trạng thái" :class="{ 'p-invalid': errors.status }" />
          <small class="p-error" v-if="errors.status">{{ errors.status }}</small>
        </div>
        <div class="field">
          <label for="is_active">Đang Hoạt Động</label>
          <InputSwitch id="is_active" v-model="enrollmentObj.is_active" />
        </div>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="hideDialog" aria-label="Hủy" />
        <Button label="Lưu" icon="pi pi-check" @click="saveEnrollment" aria-label="Lưu đăng ký" />
      </template>
    </Dialog>
    <Dialog v-model:visible="deleteDialog" header="Xác Nhận Xóa" modal style="width: 400px;" aria-labelledby="delete-dialog-header">
      <h3 id="delete-dialog-header" class="sr-only">Xác Nhận Xóa</h3>
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span>Bạn có chắc muốn xóa đăng ký của <b>{{ enrollmentObj.student?.full_name }}</b> cho môn <b>{{ enrollmentObj.subject?.subject_name }}</b>?</span>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="deleteDialog = false" aria-label="Hủy" />
        <Button label="Xóa" icon="pi pi-check" severity="danger" @click="deleteEnrollment" aria-label="Xóa đăng ký" />
      </template>
    </Dialog>
    <Dialog v-model:visible="restoreDialog" header="Xác Nhận Khôi Phục" modal style="width: 400px;" aria-labelledby="restore-dialog-header">
      <h3 id="restore-dialog-header" class="sr-only">Xác Nhận Khôi Phục</h3>
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span>Bạn có chắc muốn khôi phục đăng ký của <b>{{ enrollmentObj.student?.full_name }}</b> cho môn <b>{{ enrollmentObj.subject?.subject_name }}</b>?</span>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="restoreDialog = false" aria-label="Hủy" />
        <Button label="Khôi phục" icon="pi pi-check" severity="success" @click="restoreEnrollment" aria-label="Khôi phục đăng ký" />
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
import { saveAs } from 'file-saver';
import { debounce } from 'lodash';
import api, { endpoints } from '@/services/api';
import Toolbar from 'primevue/toolbar';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import InputSwitch from 'primevue/inputswitch';
import Tag from 'primevue/tag';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Dialog from 'primevue/dialog';
import Calendar from 'primevue/calendar';
import Textarea from 'primevue/textarea';
import ProgressSpinner from 'primevue/progressspinner';

const props = defineProps({
  enrollments: { type: Array, required: true },
  filters: { type: Object, required: true },
  paginatorInfo: { type: Object, required: true },
});
const emit = defineEmits(['update:enrollments', 'loadEnrollments']);

const userStore = useUserStore();
const toast = useToast();

const enrollmentObj = ref({ status: 'pending', is_active: true, enrollment_date: new Date() });
const enrollmentDialog = ref(false);
const deleteDialog = ref(false);
const restoreDialog = ref(false);
const changeStatusDialog = ref(false);
const loading = ref(false);
const errors = ref({});
const newStatus = ref('');
const submitted = ref(false);
const students = ref([]);
const subjects = ref([]);
const classes = ref([]);
const semesters = ref([]);

const canEditEnrollments = computed(() => userStore.isAdmin || userStore.isTeacher);
const canDeleteEnrollments = computed(() => userStore.isAdmin);
const canExportData = computed(() => userStore.isAdmin);

const statusOptions = [
  { label: 'Chờ xử lý', value: 'pending' },
  { label: 'Đã duyệt', value: 'approved' },
  { label: 'Từ chối', value: 'rejected' },
];

const debouncedLoadEnrollments = debounce(() => emit('loadEnrollments'), 500);

onMounted(async () => {
  await Promise.all([loadSemesters(), loadSubjects(), loadClasses(), loadStudents()]);
});

const loadSemesters = async () => {
  try {
    const response = await api.get(endpoints.semesters);
    semesters.value = Array.isArray(response.data) ? response.data : response.data.results || [];
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải học kỳ', life: 3000 });
  }
};

const loadStudents = async () => {
  try {
    const response = await api.get(endpoints.students);
    students.value = Array.isArray(response.data) ? response.data : response.data.results || [];
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách sinh viên', life: 3000 });
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

const loadClasses = async () => {
  try {
    const response = await api.get(endpoints.classes);
    classes.value = Array.isArray(response.data) ? response.data : response.data.results || [];
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách lớp', life: 3000 });
  }
};

const openNew = () => {
  enrollmentObj.value = { status: 'pending', is_active: true, enrollment_date: new Date() };
  errors.value = {};
  submitted.value = false;
  enrollmentDialog.value = true;
};

const editEnrollment = (data) => {
  enrollmentObj.value = {
    ...data,
    student: data.student?.student_id,
    subject: data.subject?.subject_id,
    semester: data.semester?.semester_id,
    class_obj: data.class_obj?.class_id,
    enrollment_date: new Date(data.enrollment_date),
  };
  errors.value = {};
  submitted.value = false;
  enrollmentDialog.value = true;
};

const hideDialog = () => {
  enrollmentDialog.value = false;
  enrollmentObj.value = {};
  errors.value = {};
};

const confirmDelete = (data) => {
  enrollmentObj.value = { ...data };
  deleteDialog.value = true;
};

const confirmRestore = (data) => {
  enrollmentObj.value = { ...data };
  restoreDialog.value = true;
};

const openChangeStatus = (data) => {
  enrollmentObj.value = { ...data };
  newStatus.value = data.status;
  submitted.value = false;
  changeStatusDialog.value = true;
};

const validateEnrollment = () => {
  errors.value = {};
  if (!enrollmentObj.value.student) errors.value.student = 'Vui lòng chọn sinh viên';
  if (!enrollmentObj.value.subject) errors.value.subject = 'Vui lòng chọn môn học';
  if (!enrollmentObj.value.semester) errors.value.semester = 'Vui lòng chọn học kỳ';
  if (!enrollmentObj.value.class_obj) errors.value.class_obj = 'Vui lòng chọn lớp';
  if (!enrollmentObj.value.enrollment_date) errors.value.enrollment_date = 'Vui lòng chọn ngày đăng ký';
  if (!enrollmentObj.value.status) errors.value.status = 'Vui lòng chọn trạng thái';
  if (enrollmentObj.value.status === 'rejected' && enrollmentObj.value.is_active) {
    errors.value.is_active = 'Đăng ký bị từ chối không thể ở trạng thái hoạt động';
  }
};

const saveEnrollment = async () => {
  submitted.value = true;
  validateEnrollment();
  if (Object.keys(errors.value).length > 0) return;
  try {
    const payload = {
      ...enrollmentObj.value,
      enrollment_date: enrollmentObj.value.enrollment_date instanceof Date ? enrollmentObj.value.enrollment_date.toISOString().split('T')[0] : enrollmentObj.value.enrollment_date,
    };
    let updatedEnrollments;
    if (enrollmentObj.value.enrollment_id) {
      const response = await api.patch(`${endpoints.enrollments}${enrollmentObj.value.enrollment_id}/`, payload);
      updatedEnrollments = props.enrollments.map(e => e.enrollment_id === enrollmentObj.value.enrollment_id ? response.data : e);
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật đăng ký thành công', life: 3000 });
    } else {
      const response = await api.post(endpoints.enrollments, payload);
      updatedEnrollments = [...props.enrollments, response.data];
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Thêm đăng ký thành công', life: 3000 });
    }
    emit('update:enrollments', updatedEnrollments);
    hideDialog();
  } catch (error) {
    const errorMsg = error.response?.data?.detail || Object.values(error.response?.data || {}).join(', ') || 'Không thể lưu đăng ký';
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errorMsg, life: 3000 });
  }
};

const deleteEnrollment = async () => {
  try {
    await api.delete(`${endpoints.enrollments}${enrollmentObj.value.enrollment_id}/`);
    const updatedEnrollments = props.enrollments.filter(e => e.enrollment_id !== enrollmentObj.value.enrollment_id);
    emit('update:enrollments', updatedEnrollments);
    deleteDialog.value = false;
    enrollmentObj.value = {};
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa đăng ký thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa đăng ký', life: 3000 });
  }
};

const restoreEnrollment = async () => {
  try {
    const response = await api.post(`${endpoints.enrollments}${enrollmentObj.value.enrollment_id}/restore/`);
    emit('loadEnrollments');
    restoreDialog.value = false;
    enrollmentObj.value = {};
    toast.add({ severity: 'success', summary: 'Thành công', detail: response.data.message || 'Khôi phục đăng ký thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể khôi phục đăng ký', life: 3000 });
  }
};

const changeStatus = async () => {
  submitted.value = true;
  if (!newStatus.value) return;
  try {
    const response = await api.post(`${endpoints.enrollments}${enrollmentObj.value.enrollment_id}/change-status/`, { status: newStatus.value });
    const updatedEnrollments = props.enrollments.map(e => e.enrollment_id === enrollmentObj.value.enrollment_id ? response.data : e);
    emit('update:enrollments', updatedEnrollments);
    changeStatusDialog.value = false;
    newStatus.value = '';
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật trạng thái thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể cập nhật trạng thái', life: 3000 });
  }
};

const exportEnrollments = async () => {
  try {
    const response = await api.get(`${endpoints.enrollments}export/`, { responseType: 'blob' });
    const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
    saveAs(blob, `enrollments_${new Date().toISOString().split('T')[0]}.xlsx`);
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xuất đăng ký thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xuất đăng ký', life: 3000 });
  }
};

const onPage = (event) => {
  emit('loadEnrollments', event.page + 1, event.rows);
};

const formatDate = (date) => {
  if (!date) return '';
  const d = new Date(date);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
};

const getStatusLabel = (status) => {
  const option = statusOptions.find(opt => opt.value === status);
  return option ? option.label : status;
};

const getStatusSeverity = (status) => {
  const map = { pending: 'info', approved: 'success', rejected: 'danger' };
  return map[status] || 'info';
};
</script>

<style scoped>
.enrollment-management-content {
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
.p-datatable-sm :deep(.p-button) {
  width: 28px;
  height: 28px;
  padding: 0;
  font-size: 14px;
}
</style>