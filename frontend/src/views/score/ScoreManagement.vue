<template>
  <div class="score-management-content" aria-label="Phần quản lý điểm">
    <Toolbar class="toolbar">
      <template #start>
        <h2>Quản Lý Điểm</h2>
      </template>
      <template #end>
        <Button
          v-if="canEditScores"
          icon="pi pi-plus"
          label="Thêm Điểm"
          severity="primary"
          class="mr-2"
          @click="openNewDialog"
          v-tooltip="'Thêm điểm mới'"
          aria-label="Thêm điểm mới"
        />
        <Button
          v-if="canUploadScores"
          icon="pi pi-upload"
          label="Upload Điểm"
          severity="info"
          class="mr-2"
          @click="openUploadScoreDialog"
          v-tooltip="'Tải lên điểm từ Excel'"
          aria-label="Tải lên điểm từ Excel"
        />
        <Button
          v-if="canExportScores"
          icon="pi pi-download"
          label="Export"
          severity="success"
          @click="exportScores"
          v-tooltip="'Xuất danh sách điểm'"
          aria-label="Xuất danh sách điểm"
        />
      </template>
    </Toolbar>
    <div class="filter-bar">
      <Dropdown
        v-model="filters.status"
        :options="statusOptions"
        optionLabel="label"
        optionValue="value"
        placeholder="Lọc trạng thái"
        class="filter-dropdown mr-2"
        @change="emit('loadScores')"
        aria-label="Lọc theo trạng thái"
      />
      <Dropdown
        v-model="filters.semester"
        :options="semesters"
        optionLabel="semester_name"
        optionValue="semester_id"
        placeholder="Lọc học kỳ"
        class="filter-dropdown mr-2"
        @change="emit('loadScores')"
        aria-label="Lọc theo học kỳ"
      />
      <Dropdown
        v-model="filters.subject"
        :options="subjects"
        optionLabel="subject_name"
        optionValue="subject_id"
        placeholder="Lọc môn học"
        class="filter-dropdown mr-2"
        @change="emit('loadScores')"
        aria-label="Lọc theo môn học"
      />
      <Dropdown
        v-model="filters.student"
        :options="students"
        optionLabel="full_name"
        optionValue="student_id"
        placeholder="Lọc sinh viên"
        class="filter-dropdown mr-2"
        @change="emit('loadScores')"
        aria-label="Lọc theo sinh viên"
      />
      <InputText
        v-model="filters.global"
        placeholder="Tìm sinh viên, môn học..."
        class="filter-search"
        @input="debouncedLoadScores"
        aria-label="Tìm kiếm điểm"
      />
    </div>
    <DataTable
      :value="scores"
      :loading="loading"
      dataKey="id"
      lazy
      :paginator="true"
      :rows="paginatorInfo.rows"
      :rowsPerPageOptions="[5, 10, 20]"
      :totalRecords="paginatorInfo.total"
      @page="onPage"
      class="p-datatable-sm"
      aria-label="Bảng quản lý điểm"
    >
      <template #empty>
        <div class="empty-message"><i class="pi pi-info-circle" /><span>Không tìm thấy điểm số nào.</span></div>
      </template>
      <template #loading>
        <div class="loading-message"><ProgressSpinner style="width: 24px; height: 24px;" /><span>Đang tải dữ liệu...</span></div>
      </template>
      <Column field="student.full_name" header="Sinh Viên" sortable style="width: 15%" />
      <Column field="subject.subject_name" header="Môn Học" sortable style="width: 15%" />
      <Column field="semester.semester_name" header="Học Kỳ" sortable style="width: 15%" />
      <Column field="midterm_score" header="Điểm Giữa Kỳ" sortable style="width: 10%" align="center">
        <template #body="{ data }">{{ formatScore(data.midterm_score) }}</template>
      </Column>
      <Column field="final_score" header="Điểm Cuối Kỳ" sortable style="width: 10%" align="center">
        <template #body="{ data }">{{ formatScore(data.final_score) }}</template>
      </Column>
      <Column field="total_score" header="Tổng Điểm" sortable style="width: 10%" align="center">
        <template #body="{ data }"><Tag :severity="getScoreSeverity(data.total_score)" :value="formatScore(data.total_score)" /></template>
      </Column>
      <Column field="status" header="Trạng Thái" sortable style="width: 10%" align="center">
        <template #body="{ data }"><Tag :severity="getStatusSeverity(data.status)" :value="getStatusLabel(data.status)" /></template>
      </Column>
      <Column field="notes" header="Ghi Chú" style="width: 15%" />
      <Column header="Hành Động" style="width: 15%" align="center">
        <template #body="{ data }">
          <Button
            v-if="canEditScores && !data.is_deleted"
            icon="pi pi-pencil"
            outlined
            rounded
            class="mr-2"
            severity="info"
            @click="editScore(data)"
            v-tooltip="'Sửa thông tin'"
            aria-label="Sửa điểm"
          />
          <Button
            v-if="canDeleteScores && !data.is_deleted"
            icon="pi pi-trash"
            outlined
            rounded
            severity="danger"
            class="mr-2"
            @click="confirmDelete(data)"
            v-tooltip="'Xóa mềm'"
            aria-label="Xóa mềm điểm"
          />
          <Button
            v-if="canDeleteScores && data.is_deleted"
            icon="pi pi-undo"
            outlined
            rounded
            severity="success"
            @click="confirmRestore(data)"
            v-tooltip="'Khôi phục'"
            aria-label="Khôi phục điểm"
          />
        </template>
      </Column>
    </DataTable>
    <Dialog
      v-model:visible="scoreDialog"
      :header="score.id ? 'Sửa Điểm' : 'Thêm Điểm'"
      modal
      class="p-fluid"
      style="width: 600px;"
      aria-labelledby="score-dialog-header"
    >
      <h3 id="score-dialog-header" class="sr-only">{{ score.id ? 'Sửa Điểm' : 'Thêm Điểm' }}</h3>
      <div class="form-section">
        <h4>Thông Tin Điểm</h4>
        <div class="field">
          <label for="student">Sinh Viên</label>
          <Dropdown
            id="student"
            v-model="score.student"
            :options="students"
            optionLabel="full_name"
            optionValue="student_id"
            placeholder="Chọn sinh viên"
            :class="{ 'p-invalid': errors.student }"
          />
          <small class="p-error" v-if="errors.student">{{ errors.student }}</small>
        </div>
        <div class="field">
          <label for="subject">Môn Học</label>
          <Dropdown
            id="subject"
            v-model="score.subject"
            :options="subjects"
            optionLabel="subject_name"
            optionValue="subject_id"
            placeholder="Chọn môn học"
            :class="{ 'p-invalid': errors.subject }"
          />
          <small class="p-error" v-if="errors.subject">{{ errors.subject }}</small>
        </div>
        <div class="field">
          <label for="semester">Học Kỳ</label>
          <Dropdown
            id="semester"
            v-model="score.semester"
            :options="semesters"
            optionLabel="semester_name"
            optionValue="semester_id"
            placeholder="Chọn học kỳ"
            :class="{ 'p-invalid': errors.semester }"
          />
          <small class="p-error" v-if="errors.semester">{{ errors.semester }}</small>
        </div>
        <div class="field">
          <label for="midterm_score">Điểm Giữa Kỳ</label>
          <InputNumber
            id="midterm_score"
            v-model="score.midterm_score"
            :min="0"
            :max="10"
            :step="0.1"
            :maxFractionDigits="2"
            placeholder="0.0 - 10.0"
            :class="{ 'p-invalid': errors.midterm_score }"
          />
          <small class="p-error" v-if="errors.midterm_score">{{ errors.midterm_score }}</small>
        </div>
        <div class="field">
          <label for="final_score">Điểm Cuối Kỳ</label>
          <InputNumber
            id="final_score"
            v-model="score.final_score"
            :min="0"
            :max="10"
            :step="0.1"
            :maxFractionDigits="2"
            placeholder="0.0 - 10.0"
            :class="{ 'p-invalid': errors.final_score }"
          />
          <small class="p-error" v-if="errors.final_score">{{ errors.final_score }}</small>
        </div>
        <div class="field">
          <label for="total_score">Tổng Điểm</label>
          <InputNumber
            id="total_score"
            v-model="score.total_score"
            :min="0"
            :max="10"
            :step="0.1"
            :maxFractionDigits="2"
            placeholder="0.0 - 10.0"
            :class="{ 'p-invalid': errors.total_score }"
          />
          <small class="p-error" v-if="errors.total_score">{{ errors.total_score }}</small>
        </div>
        <div class="field">
          <label for="notes">Ghi Chú</label>
          <Textarea
            id="notes"
            v-model="score.notes"
            rows="3"
            placeholder="Nhập ghi chú nếu có"
          />
        </div>
        <div class="field">
          <label for="status">Trạng Thái</label>
          <Dropdown
            id="status"
            v-model="score.status"
            :options="statusOptions"
            optionLabel="label"
            optionValue="value"
            placeholder="Chọn trạng thái"
            :class="{ 'p-invalid': errors.status }"
          />
          <small class="p-error" v-if="errors.status">{{ errors.status }}</small>
        </div>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="hideDialog" aria-label="Hủy" />
        <Button label="Lưu" icon="pi pi-check" @click="saveScore" aria-label="Lưu điểm" />
      </template>
    </Dialog>
    <Dialog
      v-model:visible="uploadScoreDialog"
      header="Tải Lên Điểm Từ Excel"
      modal
      style="width: 400px;"
      aria-labelledby="upload-score-dialog-header"
    >
      <h3 id="upload-score-dialog-header" class="sr-only">Tải Lên Điểm Từ Excel</h3>
      <div class="form-section">
        <FileUpload
          mode="basic"
          accept=".xlsx"
          :maxFileSize="10000000"
          @select="onUploadScoreFile"
          chooseLabel="Chọn file Excel"
          aria-label="Chọn file Excel để tải lên điểm"
        />
        <small class="p-info">Chỉ chấp nhận file .xlsx, tối đa 10MB.</small>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="uploadScoreDialog = false" aria-label="Hủy" />
      </template>
    </Dialog>
    <Dialog
      v-model:visible="deleteDialog"
      header="Xác Nhận Xóa"
      modal
      style="width: 400px;"
      aria-labelledby="delete-dialog-header"
    >
      <h3 id="delete-dialog-header" class="sr-only">Xác Nhận Xóa</h3>
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span v-if="score">Bạn có chắc muốn xóa điểm của <b>{{ score.student?.full_name }}</b> cho môn <b>{{ score.subject?.subject_name }}</b>?</span>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="deleteDialog = false" aria-label="Hủy" />
        <Button label="Xóa" icon="pi pi-check" severity="danger" @click="deleteScore" aria-label="Xóa điểm" />
      </template>
    </Dialog>
    <Dialog
      v-model:visible="restoreDialog"
      header="Xác Nhận Khôi Phục"
      modal
      style="width: 400px;"
      aria-labelledby="restore-dialog-header"
    >
      <h3 id="restore-dialog-header" class="sr-only">Xác Nhận Khôi Phục</h3>
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span v-if="score">Bạn có chắc muốn khôi phục điểm của <b>{{ score.student?.full_name }}</b> cho môn <b>{{ score.subject?.subject_name }}</b>?</span>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="restoreDialog = false" aria-label="Hủy" />
        <Button label="Khôi phục" icon="pi pi-check" severity="success" @click="restoreScore" aria-label="Khôi phục điểm" />
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
import Toolbar from 'primevue/toolbar';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import Textarea from 'primevue/textarea';
import Dropdown from 'primevue/dropdown';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Tag from 'primevue/tag';
import Dialog from 'primevue/dialog';
import FileUpload from 'primevue/fileupload';
import ProgressSpinner from 'primevue/progressspinner';
import api, { endpoints } from '@/services/api';

const props = defineProps({
  scores: { type: Array, required: true },
  filters: { type: Object, required: true },
  paginatorInfo: { type: Object, required: true },
});
const emit = defineEmits(['update:scores', 'loadScores']);

const userStore = useUserStore();
const toast = useToast();

const score = ref({ status: 'active' });
const scoreDialog = ref(false);
const uploadScoreDialog = ref(false);
const deleteDialog = ref(false);
const restoreDialog = ref(false);
const loading = ref(false);
const errors = ref({});
const semesters = ref([]);
const students = ref([]);
const subjects = ref([]);

const statusOptions = [
  { label: 'Đang hoạt động', value: 'active' },
  { label: 'Không hoạt động', value: 'inactive' },
  { label: 'Đang xử lý', value: 'pending' },
];

const canEditScores = computed(() => userStore.isAdmin || userStore.isTeacher);
const canDeleteScores = computed(() => userStore.isAdmin);
const canUploadScores = computed(() => userStore.isAdmin);
const canExportScores = computed(() => userStore.isAdmin || userStore.isTeacher);

const debouncedLoadScores = debounce(() => emit('loadScores'), 500);

onMounted(async () => {
  await Promise.all([loadSemesters(), loadStudents(), loadSubjects()]);
});

const loadSemesters = async () => {
  try {
    const response = await api.get(endpoints.semesters, { params: { active: true } });
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

const openNewDialog = () => {
  score.value = { status: 'active' };
  errors.value = {};
  scoreDialog.value = true;
};

const editScore = (data) => {
  score.value = {
    ...data,
    student: data.student.student_id,
    subject: data.subject.subject_id,
    semester: data.semester.semester_id,
  };
  errors.value = {};
  scoreDialog.value = true;
};

const confirmDelete = (data) => {
  score.value = { ...data };
  deleteDialog.value = true;
};

const confirmRestore = (data) => {
  score.value = { ...data };
  restoreDialog.value = true;
};

const hideDialog = () => {
  scoreDialog.value = false;
  errors.value = {};
  score.value = { status: 'active' };
};

const validateScore = () => {
  errors.value = {};
  if (!score.value.student) errors.value.student = 'Vui lòng chọn sinh viên';
  if (!score.value.subject) errors.value.subject = 'Vui lòng chọn môn học';
  if (!score.value.semester) errors.value.semester = 'Vui lòng chọn học kỳ';
  if (score.value.midterm_score != null && (score.value.midterm_score < 0 || score.value.midterm_score > 10)) {
    errors.value.midterm_score = 'Điểm giữa kỳ từ 0.0 - 10.0';
  }
  if (score.value.final_score != null && (score.value.final_score < 0 || score.value.final_score > 10)) {
    errors.value.final_score = 'Điểm cuối kỳ từ 0.0 - 10.0';
  }
  if (score.value.total_score != null && (score.value.total_score < 0 || score.value.total_score > 10)) {
    errors.value.total_score = 'Tổng điểm từ 0.0 - 10.0';
  }
  if (!score.value.status) errors.value.status = 'Vui lòng chọn trạng thái';
};

const saveScore = async () => {
  validateScore();
  if (Object.keys(errors.value).length > 0) return;
  try {
    const payload = { ...score.value };
    let updatedScores;
    if (score.value.id) {
      const response = await api.patch(`${endpoints.scores}${score.value.id}/`, payload);
      updatedScores = props.scores.map(s => s.id === score.value.id ? response.data : s);
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật điểm thành công', life: 3000 });
    } else {
      const response = await api.post(endpoints.scores, payload);
      updatedScores = [...props.scores, response.data];
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Thêm điểm thành công', life: 3000 });
    }
    emit('update:scores', updatedScores);
    hideDialog();
  } catch (error) {
    const errorMsg = error.response?.data?.detail || Object.values(error.response?.data || {}).join(', ') || 'Không thể lưu điểm';
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errorMsg, life: 3000 });
  }
};

const deleteScore = async () => {
  try {
    await api.delete(`${endpoints.scores}${score.value.id}/`);
    const updatedScores = props.scores.filter(s => s.id !== score.value.id);
    emit('update:scores', updatedScores);
    deleteDialog.value = false;
    score.value = { status: 'active' };
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa điểm thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa điểm', life: 3000 });
  }
};

const restoreScore = async () => {
  try {
    const response = await api.post(`${endpoints.scores}${score.value.id}/restore/`);
    emit('loadScores');
    restoreDialog.value = false;
    score.value = { status: 'active' };
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Khôi phục điểm thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể khôi phục điểm', life: 3000 });
  }
};

const openUploadScoreDialog = () => {
  uploadScoreDialog.value = true;
};

const onUploadScoreFile = async (event) => {
  const file = event.files[0];
  if (!file) return;
  const formData = new FormData();
  formData.append('file', file);
  try {
    const response = await api.post(endpoints.scoreManagement, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    toast.add({ severity: 'success', summary: 'Thành công', detail: response.data.message || 'Tải lên điểm thành công', life: 3000 });
    emit('loadScores');
    uploadScoreDialog.value = false;
  } catch (error) {
    const errors = error.response?.data?.errors || [error.response?.data?.error || 'Không thể tải file'];
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errors.join('; '), life: 5000 });
  }
};

const exportScores = async () => {
  try {
    const params = {
      status: props.filters.status || undefined,
      semester_id: props.filters.semester || undefined,
      subject_id: props.filters.subject || undefined,
      student_id: props.filters.student || undefined,
      search: props.filters.global || undefined,
      format: 'xlsx',
    };
    const response = await api.get(`${endpoints.scores}export/`, { params, responseType: 'blob' });
    saveAs(response.data, `diem_${new Date().toISOString().split('T')[0]}.xlsx`);
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xuất điểm thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xuất điểm', life: 3000 });
  }
};

const onPage = (event) => {
  emit('loadScores', event.page + 1, event.rows);
};

const formatScore = (score) => {
  return score != null ? score.toFixed(2) : '-';
};

const getScoreSeverity = (score) => {
  if (score == null) return 'info';
  if (score < 5) return 'danger';
  if (score < 7) return 'warning';
  return 'success';
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
.score-management-content {
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
  flex-wrap: wrap;
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
