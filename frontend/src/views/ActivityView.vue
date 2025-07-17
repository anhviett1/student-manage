<template>
  <div class="activity-view p-4">
    <Toast />
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner">
        <i class="pi pi-spin pi-spinner" style="font-size: 2rem; color: var(--primary-color);"></i>
        <p>Đang tải dữ liệu...</p>
      </div>
    </div>

    <h1 class="text-3xl font-bold mb-4 text-primary">Lịch Sử Hoạt Động</h1>

    <Card class="mb-4 shadow-1">
      <template #content>
        <div class="filters grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-3 items-end">
          <div class="col">
            <label for="search" class="block text-900 font-medium mb-1">Tìm kiếm</label>
            <InputText id="search" v-model="filters.search" placeholder="Người dùng, mô tả, IP..." class="w-full" @input="debouncedFetchActivities" />
          </div>

          <div class="col">
            <label for="activityType" class="block text-900 font-medium mb-1">Loại hoạt động</label>
            <Dropdown id="activityType" v-model="filters.activity_type" :options="activityTypes" optionLabel="label" optionValue="value" placeholder="Tất cả loại" class="w-full" @change="fetchActivities" />
          </div>

          <div class="col">
            <label for="startDate" class="block text-900 font-medium mb-1">Từ ngày</label>
            <Calendar id="startDate" v-model="filters.start_date" dateFormat="dd/mm/yy" showIcon class="w-full" @date-select="fetchActivities" @clear-click="fetchActivities" />
          </div>

          <div class="col">
            <label for="endDate" class="block text-900 font-medium mb-1">Đến ngày</label>
            <Calendar id="endDate" v-model="filters.end_date" dateFormat="dd/mm/yy" showIcon class="w-full" @date-select="fetchActivities" @clear-click="fetchActivities" />
          </div>
          
          <div class="col">
            <Button label="Xuất Excel" icon="pi pi-file-excel" class="p-button-success w-full" @click="exportActivities" :loading="isExporting" />
          </div>
        </div>
      </template>
    </Card>

    <DataTable :value="activities" paginator :rows="10" :rowsPerPageOptions="[5, 10, 20, 50]" class="p-datatable-sm shadow-1" :loading="isLoading">
      <Column field="user.username" header="Người dùng" sortable></Column>
      <Column field="activity_type_display" header="Loại hoạt động" sortable></Column>
      <Column field="description" header="Mô tả">
        <template #body="{ data }">
          {{ data.description || '-' }}
        </template>
      </Column>
      <Column field="ip_address" header="IP Address">
        <template #body="{ data }">
          {{ data.ip_address || '-' }}
        </template>
      </Column>
      <Column field="created_at" header="Ngày tạo" sortable>
        <template #body="{ data }">
          {{ formatDate(data.created_at) }}
        </template>
      </Column>
      <Column field="updated_at" header="Ngày cập nhật" sortable>
        <template #body="{ data }">
          {{ formatDate(data.updated_at) }}
        </template>
      </Column>
      <template #empty>
        <div class="text-center py-4">
          <i class="pi pi-info-circle text-2xl text-400 mb-2"></i>
          <p class="text-600">Không tìm thấy hoạt động nào.</p>
        </div>
      </template>
    </DataTable>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api, { endpoints } from '../services/api';
import { format } from 'date-fns';
import { useToast } from 'primevue/usetoast';
import Card from 'primevue/card';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import Calendar from 'primevue/calendar';
import Button from 'primevue/button';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Toast from 'primevue/toast';

// Interfaces
interface Activity {
  id: number;
  user: {
    username: string;
  };
  activity_type_display: string;
  description: string | null;
  ip_address: string | null;
  created_at: string;
  updated_at: string;
}

// State
const toast = useToast();
const activities = ref<Activity[]>([]);
const isLoading = ref(false);
const isExporting = ref(false);

const filters = ref({
  activity_type: '',
  start_date: null as Date | null, // Đổi sang Date | null để phù hợp với Calendar
  end_date: null as Date | null,   // Đổi sang Date | null để phù hợp với Calendar
  search: '',
});

const activityTypes = [
  { value: '', label: 'Tất cả loại hoạt động' }, // Thêm tùy chọn "Tất cả"
  { value: 'login', label: 'Đăng nhập' },
  { value: 'logout', label: 'Đăng xuất' },
  { value: 'create', label: 'Tạo mới' },
  { value: 'update', label: 'Cập nhật' },
  { value: 'delete', label: 'Xóa' },
  { value: 'view', label: 'Xem' },
];

let debounceTimer: ReturnType<typeof setTimeout>;

// Methods
const getQueryParams = () => {
  const params: Record<string, string> = {};
  if (filters.value.activity_type) params.activity_type = filters.value.activity_type;
  // Format Date objects to 'YYYY-MM-DD' strings for API
  if (filters.value.start_date) params.start_date = format(filters.value.start_date, 'yyyy-MM-dd');
  if (filters.value.end_date) params.end_date = format(filters.value.end_date, 'yyyy-MM-dd');
  if (filters.value.search) params.search = filters.value.search;
  return params;
};

const fetchActivities = async () => {
  isLoading.value = true;
  try {
    const params = getQueryParams();
    const response = await api.get(endpoints.activities, { params });
    activities.value = response.data;
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Tải lịch sử hoạt động hoàn tất', life: 3000 });
  } catch (error) {
    console.error('Lỗi khi tải lịch sử hoạt động:', error);
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải lịch sử hoạt động.', life: 3000 });
  } finally {
    isLoading.value = false;
  }
};

const debouncedFetchActivities = () => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    fetchActivities();
  }, 500); // Debounce for 500ms
};

const exportActivities = async () => {
  isExporting.value = true;
  try {
    const params = getQueryParams();
    const response = await api.get(endpoints.activities + 'export/', {
      params,
      responseType: 'blob', // Quan trọng để nhận dữ liệu nhị phân (blob)
    });

    // Tạo URL đối tượng và tải về
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `lich_su_hoat_dong_${format(new Date(), 'yyyyMMdd_HHmmss')}.xlsx`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url); // Giải phóng tài nguyên

    toast.add({ severity: 'success', summary: 'Xuất Excel', detail: 'Lịch sử hoạt động đã được xuất thành công.', life: 3000 });
  } catch (error) {
    console.error('Lỗi khi xuất lịch sử hoạt động:', error);
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xuất lịch sử hoạt động.', life: 3000 });
  } finally {
    isExporting.value = false;
  }
};

const formatDate = (dateStr: string) => {
  if (!dateStr) return '-';
  try {
    return format(new Date(dateStr), 'dd/MM/yyyy HH:mm:ss'); // Thêm giây để chi tiết hơn
  } catch (e) {
    console.error('Invalid date string:', dateStr, e);
    return dateStr; // Trả về chuỗi gốc nếu không thể format
  }
};

// Lifecycle Hooks
onMounted(() => {
  fetchActivities();
});
</script>

<style scoped>
.activity-view {
  padding: 2rem;
  background-color: var(--surface-ground);
  min-height: calc(100vh - var(--navbar-height, 70px)); /* Điều chỉnh nếu cần */
}

h1 {
  color: var(--primary-color, #1e88e5); /* Sử dụng biến CSS của PrimeVue */
}

.filters {
  /* PrimeFlex grid classes handles layout, no need for custom flex/gap here */
  margin-bottom: 1.5rem;
  padding: 1.25rem;
  border-radius: var(--border-radius);
  background-color: var(--surface-card);
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  backdrop-filter: blur(2px);
}
.loading-spinner {
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}
.loading-spinner p {
  margin: 1rem 0 0 0;
  color: var(--text-color-secondary);
  font-size: 1rem;
  font-weight: 500;
}

/* Tùy chỉnh nhỏ cho DataTable */
:deep(.p-datatable .p-datatable-thead > tr > th) {
  background-color: var(--surface-200);
  color: var(--text-color-secondary);
  font-weight: 600;
}
:deep(.p-datatable .p-datatable-tbody > tr > td) {
  font-size: 0.95rem;
}
</style>