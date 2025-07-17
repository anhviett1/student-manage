<template>
  <div class="subjects-page">
    <h2 class="p-text-primary p-mb-4">Quản lý Môn học</h2>

    <div class="p-mb-4 p-flex p-justify-content-between p-align-center">
      <p-button label="Thêm môn học mới" icon="pi pi-plus" @click="openNewSubjectDialog" />
    </div>

    <BaseTable
      :data="subjects"
      :columns="subjectTableColumns"
      :loading="loadingSubjects"
      :enable-pagination="true"
      :current-page="pagination.currentPage"
      :total-records="pagination.totalRecords"
      :items-per-page="pagination.itemsPerPage"
      @page-change="onPageChange"
    >
      <template #actions="{ item }">
        <p-button icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm p-mr-1" @click="editSubject(item)" />
        <p-button icon="pi pi-trash" class="p-button-rounded p-button-text p-button-danger p-button-sm" @click="confirmDeleteSubject(item)" />
      </template>
    </BaseTable>

    <p-dialog v-model:visible="subjectDialogVisible" modal :header="dialogHeader" :style="{ width: '50vw' }" :breakpoints="{'960px': '75vw', '641px': '100vw'}">
      <SubjectForm
        :initial-data="selectedSubject"
        :is-edit-mode="isEditMode"
        :is-loading="savingSubject"
        :departments="departments"
        @submit="saveSubject"
        @cancel="subjectDialogVisible = false"
      />
    </p-dialog>

    <ConfirmationDialog
      :is-visible="deleteSubjectDialogVisible"
      title="Xác nhận xóa môn học"
      :message="`Bạn có chắc chắn muốn xóa môn học '${subjectToDelete?.name} (${subjectToDelete?.code})' không?`"
      @confirm="deleteSubject"
      @cancel="deleteSubjectDialogVisible = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useNotificationStore } from '@/stores/notification';
import BaseTable from '@/components/common/BaseTable.vue'; // Giả định đường dẫn
import ConfirmationDialog from '@/components/common/ConfirmationDialog.vue'; // Giả định đường dẫn
import SubjectForm from './SubjectForm.vue'; // Đường dẫn đến SubjectForm.vue

// PrimeVue Components
import PButton from 'primevue/button';
import PDialog from 'primevue/dialog';

// Giả lập API cho môn học
const subjectApi = {
  getSubjects: async (page, limit) => {
    const allSubjects = [
      { id: 101, name: 'Lập trình Web', code: 'IT4001', credits: 3, lecture_hours: 30, lab_hours: 15, department_id: 1, department_name: 'Công nghệ thông tin', description: 'Giới thiệu về phát triển ứng dụng web.' },
      { id: 102, name: 'Cấu trúc dữ liệu', code: 'CS3002', credits: 4, lecture_hours: 45, lab_hours: 30, department_id: 1, department_name: 'Công nghệ thông tin', description: 'Nghiên cứu các cấu trúc dữ liệu cơ bản.' },
      { id: 103, name: 'Kinh tế vi mô', code: 'EC2001', credits: 3, lecture_hours: 45, lab_hours: 0, department_id: 2, department_name: 'Kinh tế', description: 'Phân tích hành vi của các cá nhân và doanh nghiệp.' },
      { id: 104, name: 'Toán cao cấp A1', code: 'MA1001', credits: 4, lecture_hours: 60, lab_hours: 0, department_id: 3, department_name: 'Toán ứng dụng', description: 'Đại số tuyến tính và giải tích.' },
      { id: 105, name: 'Mạng máy tính', code: 'IT4005', credits: 3, lecture_hours: 30, lab_hours: 15, department_id: 1, department_name: 'Công nghệ thông tin', description: 'Nguyên lý và kiến trúc mạng máy tính.' },
    ];
    const start = (page - 1) * limit;
    const end = start + limit;
    return new Promise(resolve => setTimeout(() => {
      resolve({
        data: allSubjects.slice(start, end),
        total: allSubjects.length
      });
    }, 500));
  },
  createSubject: async (subjectData) => {
    // Simulate API call
    console.log('Creating subject:', subjectData);
    return new Promise(resolve => setTimeout(() => resolve({ success: true, id: Math.floor(Math.random() * 1000) }), 300));
  },
  updateSubject: async (id, subjectData) => {
    // Simulate API call
    console.log(`Updating subject ${id}:`, subjectData);
    return new Promise(resolve => setTimeout(() => resolve({ success: true }), 300));
  },
  deleteSubject: async (id) => {
    // Simulate API call
    console.log('Deleting subject with ID:', id);
    return new Promise(resolve => setTimeout(() => resolve({ success: true }), 300));
  }
};

// Giả lập API cho khoa/bộ môn (dùng cho dropdown trong form)
const departmentApi = {
  getDepartments: async () => {
    return new Promise(resolve => setTimeout(() => {
      resolve([
        { id: 1, name: 'Công nghệ thông tin' },
        { id: 2, name: 'Kinh tế' },
        { id: 3, name: 'Toán ứng dụng' },
        { id: 4, name: 'Điện - Điện tử' }
      ]);
    }, 200));
  }
};

const notificationStore = useNotificationStore();

const subjects = ref([]);
const loadingSubjects = ref(false);
const subjectDialogVisible = ref(false);
const isEditMode = ref(false);
const selectedSubject = ref(null);
const dialogHeader = ref('');
const savingSubject = ref(false);

const deleteSubjectDialogVisible = ref(false);
const subjectToDelete = ref(null);

const departments = ref([]); // Dùng để lưu danh sách khoa/bộ môn

const pagination = ref({
  currentPage: 1,
  itemsPerPage: 10,
  totalRecords: 0
});

// Định nghĩa cột cho bảng môn học
const subjectTableColumns = [
  { field: 'id', header: 'ID', type: 'number' },
  { field: 'name', header: 'Tên Môn học', type: 'string' },
  { field: 'code', header: 'Mã Môn học', type: 'string' },
  { field: 'credits', header: 'Số tín chỉ', type: 'number' },
  { field: 'lecture_hours', header: 'Giờ lý thuyết', type: 'number' },
  { field: 'lab_hours', header: 'Giờ thực hành', type: 'number' },
  { field: 'department_name', header: 'Khoa quản lý', type: 'string' }, // Hiển thị tên khoa
  { field: 'description', header: 'Mô tả', type: 'string' },
];

// --- Lifecycle Hook ---
onMounted(() => {
  fetchSubjects();
  fetchDepartments(); // Lấy danh sách khoa khi component được mount
});

// --- Data Fetching Functions ---
const fetchSubjects = async () => {
  loadingSubjects.value = true;
  try {
    const response = await subjectApi.getSubjects(pagination.value.currentPage, pagination.value.itemsPerPage);
    subjects.value = response.data;
    pagination.value.totalRecords = response.total;
    notificationStore.showToast('Thành công', 'Tải danh sách môn học thành công!', 'success');
  } catch (error) {
    console.error('Error fetching subjects:', error);
    notificationStore.showToast('Lỗi', 'Không thể tải danh sách môn học.', 'error');
  } finally {
    loadingSubjects.value = false;
  }
};

const fetchDepartments = async () => {
  try {
    departments.value = await departmentApi.getDepartments();
  } catch (error) {
    console.error('Error fetching departments:', error);
    notificationStore.showToast('Lỗi', 'Không thể tải danh sách khoa/bộ môn.', 'error');
  }
};

// --- Dialog and Form Control Functions ---
const openNewSubjectDialog = () => {
  isEditMode.value = false;
  selectedSubject.value = {
    name: '', code: '', credits: null, lecture_hours: null, lab_hours: null, department_id: null, description: ''
  };
  dialogHeader.value = 'Thêm Môn học Mới';
  subjectDialogVisible.value = true;
};

const editSubject = (subject) => {
  isEditMode.value = true;
  // Sao chép sâu để tránh mutation trực tiếp và đảm bảo dữ liệu mới
  selectedSubject.value = { ...subject };
  dialogHeader.value = `Chỉnh sửa Môn học: ${subject.name}`;
  subjectDialogVisible.value = true;
};

const saveSubject = async (formData) => {
  savingSubject.value = true;
  try {
    if (isEditMode.value) {
      await subjectApi.updateSubject(selectedSubject.value.id, formData);
      notificationStore.showToast('Thành công', 'Cập nhật môn học thành công!', 'success');
    } else {
      await subjectApi.createSubject(formData);
      notificationStore.showToast('Thành công', 'Thêm môn học mới thành công!', 'success');
    }
    subjectDialogVisible.value = false;
    await fetchSubjects(); // Cập nhật lại bảng sau khi lưu
  } catch (error) {
    console.error('Error saving subject:', error);
    notificationStore.showToast('Lỗi', 'Có lỗi xảy ra khi lưu môn học.', 'error');
  } finally {
    savingSubject.value = false;
  }
};

// --- Delete Subject Functions ---
const confirmDeleteSubject = (subject) => {
  subjectToDelete.value = subject;
  deleteSubjectDialogVisible.value = true;
};

const deleteSubject = async () => {
  deleteSubjectDialogVisible.value = false;
  if (!subjectToDelete.value) return;

  loadingSubjects.value = true; // Hiển thị loading khi xóa
  try {
    await subjectApi.deleteSubject(subjectToDelete.value.id);
    notificationStore.showToast('Thành công', 'Xóa môn học thành công!', 'success');
    await fetchSubjects(); // Cập nhật lại bảng sau khi xóa
  } catch (error) {
    console.error('Error deleting subject:', error);
    notificationStore.showToast('Lỗi', 'Không thể xóa môn học.', 'error');
  } finally {
    loadingSubjects.value = false;
    subjectToDelete.value = null; // Xóa đối tượng cần xóa
  }
};

// --- Pagination Handler ---
const onPageChange = (event) => {
  pagination.value.currentPage = event.page + 1; // PrimeVue page starts from 0
  pagination.value.itemsPerPage = event.rows;
  fetchSubjects();
};
</script>

<style scoped>
.subjects-page {
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