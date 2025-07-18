<template>
  <div class="my-enrollments-section" aria-label="Phần đăng ký của tôi">
    <div class="profile-header">
      <h2>Đăng Ký Của Tôi</h2>
    </div>
    <div class="filter-bar">
      <Dropdown v-model="selectedSemester" :options="semesters" optionLabel="semester_name" optionValue="semester_id" placeholder="Chọn học kỳ" class="filter-dropdown" @change="emit('loadMyEnrollments')" aria-label="Lọc theo học kỳ" />
      <InputText v-model="globalFilter" placeholder="Tìm môn học, lớp..." class="filter-search" @input="debouncedLoadEnrollments" aria-label="Tìm kiếm đăng ký" />
    </div>
    <DataTable
      :value="myEnrollments"
      :loading="loading"
      dataKey="enrollment_id"
      lazy
      :paginator="true"
      :rows="paginatorInfo.rows"
      :rowsPerPageOptions="[5, 10, 20]"
      :totalRecords="paginatorInfo.total"
      @page="onPage"
      class="p-datatable-sm"
      aria-label="Bảng đăng ký của tôi"
    >
      <template #empty>
        <div class="empty-message"><i class="pi pi-info-circle" /><span>Không tìm thấy đăng ký nào.</span></div>
      </template>
      <template #loading>
        <div class="loading-message"><ProgressSpinner style="width: 24px; height: 24px;" /><span>Đang tải dữ liệu...</span></div>
      </template>
      <Column field="subject.subject_name" header="Môn Học" sortable style="width: 20%" />
      <Column field="class_obj.class_id" header="Lớp" sortable style="width: 15%" />
      <Column field="semester.semester_name" header="Học Kỳ" sortable style="width: 15%" />
      <Column field="enrollment_date" header="Ngày Đăng Ký" sortable style="width: 15%" align="center">
        <template #body="{ data }">{{ formatDate(data.enrollment_date) }}</template>
      </Column>
      <Column field="status" header="Trạng Thái" sortable style="width: 15%" align="center">
        <template #body="{ data }"><Tag :severity="getStatusSeverity(data.status)" :value="getStatusLabel(data.status)" /></template>
      </Column>
      <Column field="notes" header="Ghi Chú" style="width: 20%" />
    </DataTable>
    <div v-if="!loading && myEnrollments.length === 0" class="no-data-message">
      <p>Không có dữ liệu đăng ký để hiển thị.</p>
      <Button label="Tải lại" icon="pi pi-refresh" @click="emit('loadMyEnrollments')" severity="secondary" aria-label="Tải lại danh sách đăng ký" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useToast } from 'primevue/usetoast';
import { gsap } from 'gsap';
import { debounce } from 'lodash';
import Dropdown from 'primevue/dropdown';
import InputText from 'primevue/inputtext';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Tag from 'primevue/tag';
import Button from 'primevue/button';
import ProgressSpinner from 'primevue/progressspinner';
import api, { endpoints } from '@/services/api';

const props = defineProps({
  myEnrollments: { type: Array, required: true },
  selectedSemester: { type: [String, Number, null], required: true },
  globalFilter: { type: String, required: true },
  paginatorInfo: { type: Object, required: true },
});
const emit = defineEmits(['update:myEnrollments', 'loadMyEnrollments']);

const toast = useToast();
const loading = ref(false);
const semesters = ref([]);

const statusOptions = [
  { label: 'Chờ xử lý', value: 'pending' },
  { label: 'Đã duyệt', value: 'approved' },
  { label: 'Từ chối', value: 'rejected' },
];

const debouncedLoadEnrollments = debounce(() => emit('loadMyEnrollments'), 500);

onMounted(async () => {
  gsap.from('.my-enrollments-section', { opacity: 0, y: 20, duration: 0.5 });
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
  emit('loadMyEnrollments', event.page + 1, event.rows);
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
.my-enrollments-section {
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