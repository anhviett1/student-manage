<template>
  <div class="schedule-management-content" aria-label="Phần quản lý lịch học">
    <Toolbar class="toolbar">
      <template #start>
        <h2>Quản Lý Lịch Học</h2>
      </template>
      <template #end>
        <Button
          v-if="canEditSchedules"
          icon="pi pi-plus"
          label="Thêm Lịch Học"
          severity="primary"
          class="mr-2"
          @click="openNew"
          v-tooltip="'Thêm lịch học mới'"
          aria-label="Thêm lịch học mới"
        />
        <Button
          v-if="canExportSchedules"
          icon="pi pi-download"
          label="Export"
          severity="success"
          @click="exportSchedules"
          v-tooltip="'Xuất danh sách lịch học'"
          aria-label="Xuất danh sách lịch học"
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
        @change="emit('loadSchedules')"
        aria-label="Lọc theo trạng thái"
      />
      <Dropdown
        v-model="filters.semester"
        :options="semesters"
        optionLabel="name"
        optionValue="semester_id"
        placeholder="Lọc học kỳ"
        class="filter-dropdown mr-2"
        @change="emit('loadSchedules')"
        aria-label="Lọc theo học kỳ"
      />
      <Dropdown
        v-model="filters.class_assigned"
        :options="classes"
        optionLabel="class_name"
        optionValue="class_id"
        placeholder="Lọc lớp học"
        class="filter-dropdown mr-2"
        @change="emit('loadSchedules')"
        aria-label="Lọc theo lớp học"
      />
      <Dropdown
        v-model="filters.teacher"
        :options="teachers"
        optionLabel="full_name"
        optionValue="teacher_id"
        placeholder="Lọc giảng viên"
        class="filter-dropdown mr-2"
        @change="emit('loadSchedules')"
        aria-label="Lọc theo giảng viên"
      />
      <Dropdown
        v-model="filters.day_of_week"
        :options="dayOptions"
        optionLabel="label"
        optionValue="value"
        placeholder="Lọc ngày"
        class="filter-dropdown mr-2"
        @change="emit('loadSchedules')"
        aria-label="Lọc theo ngày"
      />
      <InputText
        v-model="filters.global"
        placeholder="Tìm kiếm..."
        class="filter-search"
        @input="debouncedLoadSchedules"
        aria-label="Tìm kiếm lịch học"
      />
    </div>
    <DataTable
      :value="schedules"
      :loading="loading"
      dataKey="schedule_id"
      lazy
      :paginator="true"
      :rows="paginatorInfo.rows"
      :rowsPerPageOptions="[5, 10, 20]"
      :totalRecords="paginatorInfo.total"
      @page="onPage"
      class="p-datatable-sm"
      aria-label="Bảng quản lý lịch học"
    >
      <template #empty>
        <div class="empty-message"><i class="pi pi-info-circle" /><span>Không tìm thấy lịch học nào.</span></div>
      </template>
      <template #loading>
        <div class="loading-message"><ProgressSpinner style="width: 24px; height: 24px;" /><span>Đang tải dữ liệu...</span></div>
      </template>
      <Column field="class_assigned.class_name" header="Lớp Học" sortable />
      <Column field="teacher.full_name" header="Giảng Viên" sortable />
      <Column field="day_of_week" header="Ngày" sortable>
        <template #body="{ data }">{{ getDayLabel(data.day_of_week) }}</template>
      </Column>
      <Column field="start_time" header="Giờ Bắt Đầu" sortable />
      <Column field="end_time" header="Giờ Kết Thúc" sortable />
      <Column field="room" header="Phòng Học" sortable />
      <Column field="semester.name" header="Học Kỳ" sortable />
      <Column field="status" header="Trạng Thái" sortable>
        <template #body="{ data }"><Tag :severity="getStatusSeverity(data.status)" :value="getStatusLabel(data.status)" /></template>
      </Column>
      <Column header="Hành Động" style="width: 15%" align="center">
        <template #body="{ data }">
          <Button
            v-if="canEditSchedules && !data.is_deleted"
            icon="pi pi-pencil"
            outlined
            rounded
            class="mr-2"
            severity="info"
            @click="editSchedule(data)"
            v-tooltip="'Sửa thông tin'"
            aria-label="Sửa lịch học"
          />
          <Button
            v-if="canDeleteSchedules && !data.is_deleted"
            icon="pi pi-trash"
            outlined
            rounded
            severity="danger"
            class="mr-2"
            @click="confirmDelete(data)"
            v-tooltip="'Xóa mềm'"
            aria-label="Xóa mềm lịch học"
          />
          <Button
            v-if="canDeleteSchedules && data.is_deleted"
            icon="pi pi-undo"
            outlined
            rounded
            severity="success"
            @click="confirmRestore(data)"
            v-tooltip="'Khôi phục'"
            aria-label="Khôi phục lịch học"
          />
        </template>
      </Column>
    </DataTable>
    <Dialog
      v-model:visible="scheduleDialog"
      :header="schedule.schedule_id ? 'Sửa Lịch Học' : 'Thêm Lịch Học'"
      modal
      class="p-fluid"
      style="width: 600px;"
      aria-labelledby="schedule-dialog-header"
    >
      <h3 id="schedule-dialog-header" class="sr-only">{{ schedule.schedule_id ? 'Sửa Lịch Học' : 'Thêm Lịch Học' }}</h3>
      <div class="form-section">
        <h4>Thông Tin Lịch Học</h4>
        <div class="field">
          <label for="class_assigned">Lớp Học</label>
          <Dropdown
            id="class_assigned"
            v-model="schedule.class_assigned"
            :options="classes"
            optionLabel="class_name"
            optionValue="class_id"
            placeholder="Chọn lớp học"
            :class="{ 'p-invalid': errors.class_assigned }"
          />
          <small class="p-error" v-if="errors.class_assigned">{{ errors.class_assigned }}</small>
        </div>
        <div class="field">
          <label for="teacher">Giảng Viên</label>
          <Dropdown
            id="teacher"
            v-model="schedule.teacher"
            :options="teachers"
            optionLabel="full_name"
            optionValue="teacher_id"
            placeholder="Chọn giảng viên"
            :class="{ 'p-invalid': errors.teacher }"
          />
          <small class="p-error" v-if="errors.teacher">{{ errors.teacher }}</small>
        </div>
        <div class="field">
          <label for="semester">Học Kỳ</label>
          <Dropdown
            id="semester"
            v-model="schedule.semester"
            :options="semesters"
            optionLabel="name"
            optionValue="semester_id"
            placeholder="Chọn học kỳ"
            :class="{ 'p-invalid': errors.semester }"
          />
          <small class="p-error" v-if="errors.semester">{{ errors.semester }}</small>
        </div>
        <div class="field">
          <label for="day_of_week">Ngày Trong Tuần</label>
          <Dropdown
            id="day_of_week"
            v-model="schedule.day_of_week"
            :options="dayOptions"
            optionLabel="label"
            optionValue="value"
            placeholder="Chọn ngày"
            :class="{ 'p-invalid': errors.day_of_week }"
          />
          <small class="p-error" v-if="errors.day_of_week">{{ errors.day_of_week }}</small>
        </div>
        <div class="field">
          <label for="start_time">Giờ Bắt Đầu</label>
          <InputMask
            id="start_time"
            v-model="schedule.start_time"
            mask="99:99"
            placeholder="HH:MM"
            :class="{ 'p-invalid': errors.start_time }"
          />
          <small class="p-error" v-if="errors.start_time">{{ errors.start_time }}</small>
        </div>
        <div class="field">
          <label for="end_time">Giờ Kết Thúc</label>
          <InputMask
            id="end_time"
            v-model="schedule.end_time"
            mask="99:99"
            placeholder="HH:MM"
            :class="{ 'p-invalid': errors.end_time }"
          />
          <small class="p-error" v-if="errors.end_time">{{ errors.end_time }}</small>
        </div>
        <div class="field">
          <label for="room">Phòng Học</label>
          <InputText
            id="room"
            v-model="schedule.room"
            :class="{ 'p-invalid': errors.room }"
          />
          <small class="p-error" v-if="errors.room">{{ errors.room }}</small>
        </div>
        <div class="field">
          <label for="status">Trạng Thái</label>
          <Dropdown
            id="status"
            v-model="schedule.status"
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
        <Button label="Lưu" icon="pi pi-check" @click="saveSchedule" aria-label="Lưu lịch học" />
      </template>
    </Dialog>
    <Dialog
      v-model:visible="deleteScheduleDialog"
      header="Xác Nhận Xóa Mềm"
      modal
      style="width: 400px;"
      aria-labelledby="delete-dialog-header"
    >
      <h3 id="delete-dialog-header" class="sr-only">Xác Nhận Xóa Mềm</h3>
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span v-if="schedule">Bạn có chắc chắn muốn xóa mềm lịch học <b>{{ schedule.class_assigned?.class_name }}</b>?</span>
      </div>
      <template #footer>
        <Button label="Không" icon="pi pi-times" text @click="deleteScheduleDialog = false" aria-label="Hủy" />
        <Button label="Có" icon="pi pi-check" severity="danger" @click="deleteSchedule" aria-label="Xóa lịch học" />
      </template>
    </Dialog>
    <Dialog
      v-model:visible="restoreScheduleDialog"
      header="Xác Nhận Khôi Phục"
      modal
      style="width: 400px;"
      aria-labelledby="restore-dialog-header"
    >
      <h3 id="restore-dialog-header" class="sr-only">Xác Nhận Khôi Phục</h3>
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span v-if="schedule">Bạn có chắc chắn muốn khôi phục lịch học <b>{{ schedule.class_assigned?.class_name }}</b>?</span>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="restoreScheduleDialog = false" aria-label="Hủy" />
        <Button label="Khôi phục" icon="pi pi-check" severity="success" @click="restoreSchedule" aria-label="Khôi phục lịch học" />
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
import InputMask from 'primevue/inputmask';
import Dropdown from 'primevue/dropdown';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Tag from 'primevue/tag';
import Dialog from 'primevue/dialog';
import ProgressSpinner from 'primevue/progressspinner';
import api, { endpoints } from '@/services/api';

const props = defineProps({
  schedules: { type: Array, required: true },
  filters: { type: Object, required: true },
  paginatorInfo: { type: Object, required: true },
});
const emit = defineEmits(['update:schedules', 'loadSchedules']);

const userStore = useUserStore();
const toast = useToast();

const schedule = ref({ status: 'active', is_active: true });
const scheduleDialog = ref(false);
const deleteScheduleDialog = ref(false);
const restoreScheduleDialog = ref(false);
const loading = ref(false);
const errors = ref({});
const classes = ref([]);
const teachers = ref([]);
const semesters = ref([]);

const statusOptions = [
  { label: 'Đang hoạt động', value: 'active' },
  { label: 'Không hoạt động', value: 'inactive' },
  { label: 'Đang chờ duyệt', value: 'pending' },
];

const dayOptions = [
  { label: 'Thứ Hai', value: 'mon' },
  { label: 'Thứ Ba', value: 'tue' },
  { label: 'Thứ Tư', value: 'wed' },
  { label: 'Thứ Năm', value: 'thu' },
  { label: 'Thứ Sáu', value: 'fri' },
  { label: 'Thứ Bảy', value: 'sat' },
  { label: 'Chủ Nhật', value: 'sun' },
];

const canEditSchedules = computed(() => userStore.isAdmin);
const canDeleteSchedules = computed(() => userStore.isAdmin);
const canExportSchedules = computed(() => userStore.isAdmin);

const debouncedLoadSchedules = debounce(() => emit('loadSchedules'), 500);

onMounted(async () => {
  await Promise.all([loadClasses(), loadTeachers(), loadSemesters()]);
});

const loadClasses = async () => {
  try {
    const response = await api.get(endpoints.classes);
    classes.value = Array.isArray(response.data) ? response.data : response.data.results || [];
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách lớp học', life: 3000 });
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

const loadSemesters = async () => {
  try {
    const response = await api.get(endpoints.semesters);
    semesters.value = Array.isArray(response.data) ? response.data : response.data.results || [];
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách học kỳ', life: 3000 });
  }
};

const openNew = () => {
  schedule.value = { status: 'active', is_active: true };
  errors.value = {};
  scheduleDialog.value = true;
};

const editSchedule = (data) => {
  schedule.value = { ...data };
  errors.value = {};
  scheduleDialog.value = true;
};

const confirmDelete = (data) => {
  schedule.value = { ...data };
  deleteScheduleDialog.value = true;
};

const confirmRestore = (data) => {
  schedule.value = { ...data };
  restoreScheduleDialog.value = true;
};

const hideDialog = () => {
  scheduleDialog.value = false;
  errors.value = {};
  schedule.value = { status: 'active', is_active: true };
};

const validateSchedule = () => {
  errors.value = {};
  if (!schedule.value.class_assigned) errors.value.class_assigned = 'Vui lòng chọn lớp học';
  if (!schedule.value.teacher) errors.value.teacher = 'Vui lòng chọn giảng viên';
  if (!schedule.value.semester) errors.value.semester = 'Vui lòng chọn học kỳ';
  if (!schedule.value.day_of_week) errors.value.day_of_week = 'Vui lòng chọn ngày trong tuần';
  if (!schedule.value.start_time) errors.value.start_time = 'Vui lòng nhập giờ bắt đầu';
  else if (!/^([0-1][0-9]|2[0-3]):[0-5][0-9]$/.test(schedule.value.start_time)) errors.value.start_time = 'Giờ bắt đầu không hợp lệ';
  if (!schedule.value.end_time) errors.value.end_time = 'Vui lòng nhập giờ kết thúc';
  else if (!/^([0-1][0-9]|2[0-3]):[0-5][0-9]$/.test(schedule.value.end_time)) errors.value.end_time = 'Giờ kết thúc không hợp lệ';
  if (!schedule.value.room?.trim()) errors.value.room = 'Vui lòng nhập phòng học';
  if (!schedule.value.status) errors.value.status = 'Vui lòng chọn trạng thái';
};

const saveSchedule = async () => {
  validateSchedule();
  if (Object.keys(errors.value).length > 0) return;
  try {
    const payload = {
      class_assigned: schedule.value.class_assigned,
      teacher: schedule.value.teacher,
      semester: schedule.value.semester,
      day_of_week: schedule.value.day_of_week,
      start_time: schedule.value.start_time,
      end_time: schedule.value.end_time,
      room: schedule.value.room,
      status: schedule.value.status,
      is_active: schedule.value.is_active,
    };
    let updatedSchedules;
    if (schedule.value.schedule_id) {
      const response = await api.patch(`${endpoints.schedules}${schedule.value.schedule_id}/`, payload);
      updatedSchedules = props.schedules.map(s => s.schedule_id === schedule.value.schedule_id ? response.data : s);
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật lịch học thành công', life: 3000 });
    } else {
      const response = await api.post(endpoints.schedules, payload);
      updatedSchedules = [...props.schedules, response.data];
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Thêm lịch học thành công', life: 3000 });
    }
    emit('update:schedules', updatedSchedules);
    hideDialog();
  } catch (error) {
    const errorMsg = error.response?.data?.detail || Object.values(error.response?.data || {}).join(', ') || 'Không thể lưu lịch học';
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errorMsg, life: 3000 });
  }
};

const deleteSchedule = async () => {
  try {
    await api.delete(`${endpoints.schedules}${schedule.value.schedule_id}/`);
    const updatedSchedules = props.schedules.filter(s => s.schedule_id !== schedule.value.schedule_id);
    emit('update:schedules', updatedSchedules);
    deleteScheduleDialog.value = false;
    schedule.value = { status: 'active', is_active: true };
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa mềm lịch học thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa lịch học', life: 3000 });
  }
};

const restoreSchedule = async () => {
  try {
    const response = await api.post(`${endpoints.schedules}${schedule.value.schedule_id}/restore/`);
    emit('loadSchedules');
    restoreScheduleDialog.value = false;
    schedule.value = { status: 'active', is_active: true };
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Khôi phục lịch học thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể khôi phục lịch học', life: 3000 });
  }
};

const exportSchedules = async () => {
  try {
    const params = {
      status: props.filters.status || undefined,
      semester: props.filters.semester || undefined,
      class_assigned: props.filters.class_assigned || undefined,
      teacher: props.filters.teacher || undefined,
      day_of_week: props.filters.day_of_week || undefined,
      search: props.filters.global || undefined,
      format: 'xlsx',
    };
    const response = await api.get(`${endpoints.schedules}export/`, { params, responseType: 'blob' });
    const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
    saveAs(blob, `lich_hoc_${new Date().toISOString().split('T')[0]}.xlsx`);
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xuất lịch học thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xuất lịch học', life: 3000 });
  }
};

const onPage = (event) => {
  emit('loadSchedules', event.page + 1, event.rows);
};

const getDayLabel = (day) => {
  const option = dayOptions.find(opt => opt.value === day);
  return option ? option.label : day;
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
.schedule-management-content {
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