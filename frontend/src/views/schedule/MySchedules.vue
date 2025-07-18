<template>
  <div class="my-schedules-section" :aria-label="isTeacherView ? 'Phần lịch giảng dạy' : 'Phần lịch học của tôi'">
    <div class="profile-header">
      <h2>{{ isTeacherView ? 'Lịch Giảng Dạy' : 'Lịch Học Của Tôi' }}</h2>
    </div>
    <Toolbar class="toolbar">
      <template #start>
        <div class="filter-bar">
          <Dropdown
            v-model="studentFilters.semester"
            :options="semesters"
            optionLabel="name"
            optionValue="semester_id"
            placeholder="Chọn học kỳ"
            class="filter-dropdown"
            @change="emit('loadMySchedules')"
            aria-label="Lọc theo học kỳ"
          />
          <Dropdown
            v-model="studentFilters.status"
            :options="statusOptions"
            optionLabel="label"
            optionValue="value"
            placeholder="Lọc trạng thái"
            class="filter-dropdown mr-2"
            @change="emit('loadMySchedules')"
            aria-label="Lọc theo trạng thái"
          />
          <InputText
            v-model="studentFilters.global"
            :placeholder="isTeacherView ? 'Tìm lớp, phòng...' : 'Tìm lớp, phòng, giảng viên...'"
            class="filter-search"
            @input="debouncedLoadSchedules"
            aria-label="Tìm kiếm lịch học"
          />
        </div>
      </template>
      <template #end>
        <Button
          v-if="canExportSchedules"
          icon="pi pi-download"
          label="Export"
          severity="success"
          @click="exportSchedules"
          v-tooltip="'Xuất lịch học'"
          :aria-label="isTeacherView ? 'Xuất lịch giảng dạy' : 'Xuất lịch học cá nhân'"
        />
      </template>
    </Toolbar>
    <DataTable
      :value="mySchedules"
      :loading="loading"
      dataKey="schedule_id"
      lazy
      :paginator="true"
      :rows="paginatorInfo.rows"
      :rowsPerPageOptions="[5, 10, 20]"
      :totalRecords="paginatorInfo.total"
      @page="onPage"
      class="p-datatable-sm"
      :aria-label="isTeacherView ? 'Bảng lịch giảng dạy' : 'Bảng lịch học của tôi'"
    >
      <template #empty>
        <div class="empty-message"><i class="pi pi-info-circle" /><span>Không tìm thấy lịch học nào.</span></div>
      </template>
      <template #loading>
        <div class="loading-message"><ProgressSpinner style="width: 24px; height: 24px;" /><span>Đang tải dữ liệu...</span></div>
      </template>
      <Column field="class_assigned.class_name" header="Lớp Học" sortable />
      <Column v-if="!isTeacherView" field="teacher.full_name" header="Giảng Viên" sortable />
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
    </DataTable>
    <div v-if="!loading && mySchedules.length === 0" class="no-data-message">
      <p>Không có dữ liệu lịch học để hiển thị.</p>
      <Button label="Tải lại" icon="pi pi-refresh" @click="emit('loadMySchedules')" severity="secondary" :aria-label="isTeacherView ? 'Tải lại lịch giảng dạy' : 'Tải lại lịch học'" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useUserStore } from '@/stores/user';
import { useToast } from 'primevue/usetoast';
import { saveAs } from 'file-saver';
import { debounce } from 'lodash';
import Toolbar from 'primevue/toolbar';
import Dropdown from 'primevue/dropdown';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Tag from 'primevue/tag';
import ProgressSpinner from 'primevue/progressspinner';
import api, { endpoints } from '@/services/api';

const props = defineProps({
  mySchedules: { type: Array, required: true },
  studentFilters: { type: Object, required: true },
  paginatorInfo: { type: Object, required: true },
  isTeacherView: { type: Boolean, default: false },
});
const emit = defineEmits(['update:mySchedules', 'loadMySchedules']);

const userStore = useUserStore();
const toast = useToast();
const loading = ref(false);
const semesters = ref([]);

const statusOptions = [
  { label: 'Đang hoạt động', value: 'active' },
  { label: 'Không hoạt động', value: 'inactive' },
  { label: 'Đang chờ duyệt', value: 'pending' },
];

const canExportSchedules = computed(() => userStore.isAdmin || userStore.isTeacher || userStore.isStudent);

const debouncedLoadSchedules = debounce(() => emit('loadMySchedules'), 500);

onMounted(async () => {
  gsap.from('.my-schedules-section', { opacity: 0, y: 20, duration: 0.5 });
  await loadSemesters();
});

const loadSemesters = async () => {
  try {
    const response = await api.get(endpoints.semesters);
    semesters.value = Array.isArray(response.data) ? response.data : response.data.results || [];
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải học kỳ', life: 3000 });
  }
};

const onPage = (event) => {
  emit('loadMySchedules', event.page + 1, event.rows);
};

const exportSchedules = async () => {
  try {
    const params = {
      semester: props.studentFilters.semester || undefined,
      status: props.studentFilters.status || undefined,
      search: props.studentFilters.global || undefined,
      format: 'xlsx',
      [props.isTeacherView ? 'teacher' : 'student']: userStore.user?.id,
    };
    const response = await api.get(`${endpoints.schedules}export/`, { params, responseType: 'blob' });
    const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
    saveAs(blob, `lich_hoc_${new Date().toISOString().split('T')[0]}.xlsx`);
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xuất lịch học thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xuất lịch học', life: 3000 });
  }
};

const getDayLabel = (day) => {
  const dayOptions = [
    { label: 'Thứ Hai', value: 'mon' },
    { label: 'Thứ Ba', value: 'tue' },
    { label: 'Thứ Tư', value: 'wed' },
    { label: 'Thứ Năm', value: 'thu' },
    { label: 'Thứ Sáu', value: 'fri' },
    { label: 'Thứ Bảy', value: 'sat' },
    { label: 'Chủ Nhật', value: 'sun' },
  ];
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
.my-schedules-section {
  padding: 24px;
}
.profile-header {
  margin-bottom: 24px;
  border-bottom: 1px solid #e5e7eb;
}
.profile-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
}
.toolbar {
  margin-bottom: 16px;
}
.filter-bar {
  display: flex;
  justify-content: flex-start;
  gap: 12px;
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
.no-data-message {
  text-align: center;
  padding: 24px;
  background: #f8f9fa;
  border-radius: 8px;
  margin: 16px 0;
}
.no-data-message p {
  margin-bottom: 12px;
  color: #6b7280;
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
</style>