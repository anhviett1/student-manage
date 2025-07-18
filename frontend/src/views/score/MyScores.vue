<template>
  <div class="my-scores-section" aria-label="Phần điểm của tôi">
    <div class="profile-header">
      <h2>Điểm Của Tôi</h2>
    </div>
    <Toolbar class="toolbar">
      <template #start>
        <div class="filter-bar">
          <Dropdown
            v-model="filters.semester"
            :options="semesters"
            optionLabel="semester_name"
            optionValue="semester_id"
            placeholder="Chọn học kỳ"
            class="filter-dropdown"
            @change="emit('loadMyScores')"
            aria-label="Lọc theo học kỳ"
          />
          <InputText
            v-model="filters.global"
            placeholder="Tìm môn học, trạng thái..."
            class="filter-search"
            @input="debouncedLoadScores"
            aria-label="Tìm kiếm điểm"
          />
        </div>
      </template>
      <template #end>
        <Button
          v-if="canExportScores"
          icon="pi pi-download"
          label="Export"
          severity="success"
          @click="exportScores"
          v-tooltip="'Xuất điểm cá nhân'"
          aria-label="Xuất điểm cá nhân"
        />
      </template>
    </Toolbar>
    <DataTable
      :value="myScores"
      :loading="loading"
      dataKey="id"
      lazy
      :paginator="true"
      :rows="paginatorInfo.rows"
      :rowsPerPageOptions="[5, 10, 20]"
      :totalRecords="paginatorInfo.total"
      @page="onPage"
      class="p-datatable-sm"
      aria-label="Bảng điểm của tôi"
    >
      <template #empty>
        <div class="empty-message"><i class="pi pi-info-circle" /><span>Không tìm thấy điểm số nào.</span></div>
      </template>
      <template #loading>
        <div class="loading-message"><ProgressSpinner style="width: 24px; height: 24px;" /><span>Đang tải dữ liệu...</span></div>
      </template>
      <Column field="subject.subject_name" header="Môn Học" sortable style="width: 20%" />
      <Column field="semester.semester_name" header="Học Kỳ" sortable style="width: 15%" />
      <Column field="midterm_score" header="Điểm Giữa Kỳ" sortable style="width: 15%" align="center">
        <template #body="{ data }">{{ formatScore(data.midterm_score) }}</template>
      </Column>
      <Column field="final_score" header="Điểm Cuối Kỳ" sortable style="width: 15%" align="center">
        <template #body="{ data }">{{ formatScore(data.final_score) }}</template>
      </Column>
      <Column field="total_score" header="Tổng Điểm" sortable style="width: 15%" align="center">
        <template #body="{ data }"><Tag :severity="getScoreSeverity(data.total_score)" :value="formatScore(data.total_score)" /></template>
      </Column>
      <Column field="status" header="Trạng Thái" sortable style="width: 10%" align="center">
        <template #body="{ data }"><Tag :severity="getStatusSeverity(data.status)" :value="getStatusLabel(data.status)" /></template>
      </Column>
      <Column field="notes" header="Ghi Chú" style="width: 20%" />
    </DataTable>
    <div v-if="!loading && myScores.length === 0" class="no-data-message">
      <p>Không có dữ liệu điểm để hiển thị.</p>
      <Button label="Tải lại" icon="pi pi-refresh" @click="emit('loadMyScores')" severity="secondary" aria-label="Tải lại điểm" />
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
  myScores: { type: Array, required: true },
  filters: { type: Object, required: true },
  paginatorInfo: { type: Object, required: true },
});
const emit = defineEmits(['update:myScores', 'loadMyScores']);

const userStore = useUserStore();
const toast = useToast();
const loading = ref(false);
const semesters = ref([]);

const statusOptions = [
  { label: 'Đang hoạt động', value: 'active' },
  { label: 'Không hoạt động', value: 'inactive' },
  { label: 'Đang xử lý', value: 'pending' },
];

const canExportScores = computed(() => userStore.isStudent || userStore.isAdmin || userStore.isTeacher);

const debouncedLoadScores = debounce(() => emit('loadMyScores'), 500);

onMounted(async () => {
  gsap.from('.my-scores-section', { opacity: 0, y: 20, duration: 0.5 });
  await loadSemesters();
});

const loadSemesters = async () => {
  try {
    const response = await api.get(endpoints.semesters, { params: { active: true } });
    semesters.value = Array.isArray(response.data) ? response.data : response.data.results || [];
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải học kỳ', life: 3000 });
  }
};

const onPage = (event) => {
  emit('loadMyScores', event.page + 1, event.rows);
};

const exportScores = async () => {
  try {
    const params = {
      semester_id: props.filters.semester || undefined,
      search: props.filters.global || undefined,
      student_id: userStore.user?.id,
      format: 'xlsx',
    };
    const response = await api.get(`${endpoints.scores}export/`, { params, responseType: 'blob' });
    saveAs(response.data, `diem_${new Date().toISOString().split('T')[0]}.xlsx`);
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xuất điểm thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xuất điểm', life: 3000 });
  }
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
.my-scores-section {
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