<template>
  <div class="semesters-page">
    <h2 class="p-text-primary p-mb-4">Quản lý Học kỳ</h2>

    <div class="p-mb-4 p-flex p-justify-content-between p-align-center">
      <p-button label="Thêm học kỳ mới" icon="pi pi-plus" @click="openNewSemesterDialog" />
    </div>

    <BaseTable
      :data="semesters"
      :columns="semesterTableColumns"
      :loading="loadingSemesters"
      :enable-pagination="true"
      :current-page="pagination.currentPage"
      :total-records="pagination.totalRecords"
      :items-per-page="pagination.itemsPerPage"
      @page-change="onPageChange"
    >
      <template #actions="{ item }">
        <p-button icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm p-mr-1" @click="editSemester(item)" />
        <p-button icon="pi pi-trash" class="p-button-rounded p-button-text p-button-danger p-button-sm" @click="confirmDeleteSemester(item)" />
      </template>
    </BaseTable>

    <p-dialog v-model:visible="semesterDialogVisible" modal :header="dialogHeader" :style="{ width: '50vw' }" :breakpoints="{'960px': '75vw', '641px': '100vw'}">
      <SemesterForm
        :initial-data="selectedSemester"
        :is-edit-mode="isEditMode"
        :is-loading="savingSemester"
        @submit="saveSemester"
        @cancel="semesterDialogVisible = false"
      />
    </p-dialog>

    <ConfirmationDialog
      :is-visible="deleteSemesterDialogVisible"
      title="Xác nhận xóa học kỳ"
      :message="`Bạn có chắc chắn muốn xóa học kỳ '${semesterToDelete?.name}' không?`"
      @confirm="deleteSemester"
      @cancel="deleteSemesterDialogVisible = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useNotificationStore } from '@/stores/notification';
import BaseTable from '@/components/common/BaseTable.vue'; // Giả định đường dẫn
import ConfirmationDialog from '@/components/common/ConfirmationDialog.vue'; // Giả định đường dẫn
import SemesterForm from './SemesterForm.vue'; // Đường dẫn đến SemesterForm.vue

// PrimeVue Components
import PButton from 'primevue/button';
import PDialog from 'primevue/dialog';

// Giả lập API cho học kỳ
const semesterApi = {
  getSemesters: async (page, limit) => {
    const allSemesters = [
      { id: 1, name: 'HK1 2023-2024', year: '2023-2024', start_date: '2023-09-04', end_date: '2024-01-15', description: 'Học kỳ 1 của năm học 2023-2024' },
      { id: 2, name: 'HK2 2023-2024', year: '2023-2024', start_date: '2024-02-01', end_date: '2024-06-15', description: 'Học kỳ 2 của năm học 2023-2024' },
      { id: 3, name: 'HK hè 2024', year: '2023-2024', start_date: '2024-07-01', end_date: '2024-08-15', description: 'Học kỳ hè 2024' },
      { id: 4, name: 'HK1 2024-2025', year: '2024-2025', start_date: '2024-09-02', end_date: '2025-01-10', description: 'Học kỳ 1 của năm học 2024-2025' },
      { id: 5, name: 'HK2 2024-2025', year: '2024-2025', start_date: '2025-02-03', end_date: '2025-06-20', description: 'Học kỳ 2 của năm học 2024-2025' },
    ];
    const start = (page - 1) * limit;
    const end = start + limit;
    return new Promise(resolve => setTimeout(() => {
      resolve({
        data: allSemesters.slice(start, end),
        total: allSemesters.length
      });
    }, 500));
  },
  createSemester: async (semesterData) => {
    // Simulate API call
    console.log('Creating semester:', semesterData);
    return new Promise(resolve => setTimeout(() => resolve({ success: true, id: Math.floor(Math.random() * 1000) }), 300));
  },
  updateSemester: async (id, semesterData) => {
    // Simulate API call
    console.log(`Updating semester ${id}:`, semesterData);
    return new Promise(resolve => setTimeout(() => resolve({ success: true }), 300));
  },
  deleteSemester: async (id) => {
    // Simulate API call
    console.log('Deleting semester with ID:', id);
    return new Promise(resolve => setTimeout(() => resolve({ success: true }), 300));
  }
};

const notificationStore = useNotificationStore();

const semesters = ref([]);
const loadingSemesters = ref(false);
const semesterDialogVisible = ref(false);
const isEditMode = ref(false);
const selectedSemester = ref(null);
const dialogHeader = ref('');
const savingSemester = ref(false);

const deleteSemesterDialogVisible = ref(false);
const semesterToDelete = ref(null);

const pagination = ref({
  currentPage: 1,
  itemsPerPage: 10,
  totalRecords: 0
});

// Định nghĩa cột cho bảng học kỳ
const semesterTableColumns = [
  { field: 'id', header: 'ID', type: 'number' },
  { field: 'name', header: 'Tên Học kỳ', type: 'string' },
  { field: 'year', header: 'Năm học', type: 'string' },
  { field: 'start_date', header: 'Ngày bắt đầu', type: 'date' },
  { field: 'end_date', header: 'Ngày kết thúc', type: 'date' },
  { field: 'description', header: 'Mô tả', type: 'string' },
];

// --- Lifecycle Hook ---
onMounted(() => {
  fetchSemesters();
});

// --- Data Fetching Functions ---
const fetchSemesters = async () => {
  loadingSemesters.value = true;
  try {
    const response = await semesterApi.getSemesters(pagination.value.currentPage, pagination.value.itemsPerPage);
    semesters.value = response.data;
    pagination.value.totalRecords = response.total;
    notificationStore.showToast('Thành công', 'Tải danh sách học kỳ thành công!', 'success');
  } catch (error) {
    console.error('Error fetching semesters:', error);
    notificationStore.showToast('Lỗi', 'Không thể tải danh sách học kỳ.', 'error');
  } finally {
    loadingSemesters.value = false;
  }
};

// --- Dialog and Form Control Functions ---
const openNewSemesterDialog = () => {
  isEditMode.value = false;
  selectedSemester.value = {
    name: '', year: '', start_date: null, end_date: null, description: ''
  };
  dialogHeader.value = 'Thêm Học kỳ Mới';
  semesterDialogVisible.value = true;
};

const editSemester = (semester) => {
  isEditMode.value = true;
  // Sao chép sâu để tránh mutation trực tiếp và đảm bảo dữ liệu mới
  selectedSemester.value = { ...semester };
  // SemesterForm sẽ tự động chuyển đổi chuỗi ngày thành Date objects nhờ watch bên trong nó
  dialogHeader.value = `Chỉnh sửa Học kỳ: ${semester.name}`;
  semesterDialogVisible.value = true;
};

const saveSemester = async (formData) => {
  savingSemester.value = true;
  try {
    if (isEditMode.value) {
      await semesterApi.updateSemester(selectedSemester.value.id, formData);
      notificationStore.showToast('Thành công', 'Cập nhật học kỳ thành công!', 'success');
    } else {
      await semesterApi.createSemester(formData);
      notificationStore.showToast('Thành công', 'Thêm học kỳ mới thành công!', 'success');
    }
    semesterDialogVisible.value = false;
    await fetchSemesters(); // Cập nhật lại bảng sau khi lưu
  } catch (error) {
    console.error('Error saving semester:', error);
    notificationStore.showToast('Lỗi', 'Có lỗi xảy ra khi lưu học kỳ.', 'error');
  } finally {
    savingSemester.value = false;
  }
};

// --- Delete Semester Functions ---
const confirmDeleteSemester = (semester) => {
  semesterToDelete.value = semester;
  deleteSemesterDialogVisible.value = true;
};

const deleteSemester = async () => {
  deleteSemesterDialogVisible.value = false;
  if (!semesterToDelete.value) return;

  loadingSemesters.value = true; // Hiển thị loading khi xóa
  try {
    await semesterApi.deleteSemester(semesterToDelete.value.id);
    notificationStore.showToast('Thành công', 'Xóa học kỳ thành công!', 'success');
    await fetchSemesters(); // Cập nhật lại bảng sau khi xóa
  } catch (error) {
    console.error('Error deleting semester:', error);
    notificationStore.showToast('Lỗi', 'Không thể xóa học kỳ.', 'error');
  } finally {
    loadingSemesters.value = false;
    semesterToDelete.value = null; // Xóa đối tượng cần xóa
  }
};

// --- Pagination Handler ---
const onPageChange = (event) => {
  pagination.value.currentPage = event.page + 1; // PrimeVue page starts from 0
  pagination.value.itemsPerPage = event.rows;
  fetchSemesters();
};
</script>

<style scoped>
.semesters-page {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.p-mb-4 {
  margin-bottom: 1.5rem !important;
}

.p-flex {
    display: flex;
}

.p-justify-content-between {
    justify-content: space-between;
}

.p-align-center {
    align-items: center;
}
</style>