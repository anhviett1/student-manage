<template>
  <div class="classes-page">
    <h2 class="p-text-primary p-mb-4">Quản lý Lớp học</h2>

    <div class="p-mb-4 p-flex p-justify-content-between p-align-center">
      <p-button label="Thêm lớp học mới" icon="pi pi-plus" @click="openNewClassDialog" />
    </div>

    <BaseTable
      :data="classes"
      :columns="classTableColumns"
      :loading="loadingClasses"
      :enable-pagination="true"
      :current-page="pagination.currentPage"
      :total-records="pagination.totalRecords"
      :items-per-page="pagination.itemsPerPage"
      @page-change="onPageChange"
    >
      <template #actions="{ item }">
        <p-button icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm p-mr-1" @click="editClass(item)" />
        <p-button icon="pi pi-trash" class="p-button-rounded p-button-text p-button-danger p-button-sm" @click="confirmDeleteClass(item)" />
      </template>
    </BaseTable>

    <p-dialog v-model:visible="classDialogVisible" modal :header="dialogHeader" :style="{ width: '50vw' }" :breakpoints="{'960px': '75vw', '641px': '100vw'}">
      <ClassForm
        :initial-data="selectedClass"
        :is-edit-mode="isEditMode"
        :is-loading="savingClass"
        :departments="departments"
        @submit="saveClass"
        @cancel="classDialogVisible = false"
      />
    </p-dialog>

    <ConfirmationDialog
      :is-visible="deleteClassDialogVisible"
      title="Xác nhận xóa lớp học"
      :message="`Bạn có chắc chắn muốn xóa lớp học '${classToDelete?.name} (${classToDelete?.code})' không?`"
      @confirm="deleteClass"
      @cancel="deleteClassDialogVisible = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useNotificationStore } from '@/stores/notification';
import BaseTable from '@/components/common/BaseTable.vue'; // Giả định đường dẫn
import ConfirmationDialog from '@/components/common/ConfirmationDialog.vue'; // Giả định đường dẫn
import ClassForm from './ClassForm.vue'; // Đường dẫn đến ClassForm.vue

// PrimeVue Components
import PButton from 'primevue/button';
import PDialog from 'primevue/dialog';

// Giả lập API cho lớp học
const classApi = {
  getClasses: async (page, limit) => {
    const allClasses = [
      { id: 1, name: 'CNTT K20', code: 'IT20A', department_id: 1, department_name: 'Công nghệ thông tin', max_students: 80, current_students: 75, description: 'Lớp học ngành Công nghệ thông tin khóa 20.' },
      { id: 2, name: 'KT K21', code: 'EC21B', department_id: 2, department_name: 'Kinh tế', max_students: 60, current_students: 58, description: 'Lớp học ngành Kinh tế khóa 21.' },
      { id: 3, name: 'ĐTVT K19', code: 'EE19C', department_id: 4, department_name: 'Điện - Điện tử', max_students: 70, current_students: 65, description: 'Lớp học ngành Điện tử Viễn thông khóa 19.' },
      { id: 4, name: 'CNTT K22', code: 'IT22A', department_id: 1, department_name: 'Công nghệ thông tin', max_students: 80, current_students: 70, description: 'Lớp học ngành Công nghệ thông tin khóa 22.' },
      { id: 5, name: 'QLKD K20', code: 'BM20A', department_id: 2, department_name: 'Kinh tế', max_students: 60, current_students: 50, description: 'Lớp học ngành Quản lý Kinh doanh khóa 20.' },
    ];
    const start = (page - 1) * limit;
    const end = start + limit;
    return new Promise(resolve => setTimeout(() => {
      resolve({
        data: allClasses.slice(start, end),
        total: allClasses.length
      });
    }, 500));
  },
  createClass: async (classData) => {
    // Simulate API call
    console.log('Creating class:', classData);
    return new Promise(resolve => setTimeout(() => resolve({ success: true, id: Math.floor(Math.random() * 1000) }), 300));
  },
  updateClass: async (id, classData) => {
    // Simulate API call
    console.log(`Updating class ${id}:`, classData);
    return new Promise(resolve => setTimeout(() => resolve({ success: true }), 300));
  },
  deleteClass: async (id) => {
    // Simulate API call
    console.log('Deleting class with ID:', id);
    return new Promise(resolve => setTimeout(() => resolve({ success: true }), 300));
  }
};

// Giả lập API cho khoa/phòng ban (dùng cho dropdown trong form)
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

const classes = ref([]);
const loadingClasses = ref(false);
const classDialogVisible = ref(false);
const isEditMode = ref(false);
const selectedClass = ref(null);
const dialogHeader = ref('');
const savingClass = ref(false);

const deleteClassDialogVisible = ref(false);
const classToDelete = ref(null);

const departments = ref([]); // Dùng để lưu danh sách khoa/phòng ban

const pagination = ref({
  currentPage: 1,
  itemsPerPage: 10,
  totalRecords: 0
});

// Định nghĩa cột cho bảng lớp học
const classTableColumns = [
  { field: 'id', header: 'ID', type: 'number' },
  { field: 'name', header: 'Tên Lớp', type: 'string' },
  { field: 'code', header: 'Mã Lớp', type: 'string' },
  { field: 'department_name', header: 'Khoa/Phòng ban', type: 'string' }, // Hiển thị tên khoa
  { field: 'max_students', header: 'SV Tối đa', type: 'number' },
  { field: 'current_students', header: 'SV Hiện tại', type: 'number' }, // Có thể thêm trường này nếu dữ liệu có
  { field: 'description', header: 'Mô tả', type: 'string' },
];

// --- Lifecycle Hook ---
onMounted(() => {
  fetchClasses();
  fetchDepartments(); // Lấy danh sách khoa/phòng ban khi component được mount
});

// --- Data Fetching Functions ---
const fetchClasses = async () => {
  loadingClasses.value = true;
  try {
    const response = await classApi.getClasses(pagination.value.currentPage, pagination.value.itemsPerPage);
    classes.value = response.data;
    pagination.value.totalRecords = response.total;
    notificationStore.showToast('Thành công', 'Tải danh sách lớp học thành công!', 'success');
  } catch (error) {
    console.error('Error fetching classes:', error);
    notificationStore.showToast('Lỗi', 'Không thể tải danh sách lớp học.', 'error');
  } finally {
    loadingClasses.value = false;
  }
};

const fetchDepartments = async () => {
  try {
    departments.value = await departmentApi.getDepartments();
  } catch (error) {
    console.error('Error fetching departments:', error);
    notificationStore.showToast('Lỗi', 'Không thể tải danh sách khoa/phòng ban.', 'error');
  }
};

// --- Dialog and Form Control Functions ---
const openNewClassDialog = () => {
  isEditMode.value = false;
  selectedClass.value = {
    name: '', code: '', department_id: null, max_students: 50, description: ''
  };
  dialogHeader.value = 'Thêm Lớp học Mới';
  classDialogVisible.value = true;
};

const editClass = (classItem) => {
  isEditMode.value = true;
  // Sao chép sâu để tránh mutation trực tiếp
  selectedClass.value = { ...classItem };
  dialogHeader.value = `Chỉnh sửa Lớp học: ${classItem.name}`;
  classDialogVisible.value = true;
};

const saveClass = async (formData) => {
  savingClass.value = true;
  try {
    if (isEditMode.value) {
      await classApi.updateClass(selectedClass.value.id, formData);
      notificationStore.showToast('Thành công', 'Cập nhật lớp học thành công!', 'success');
    } else {
      await classApi.createClass(formData);
      notificationStore.showToast('Thành công', 'Thêm lớp học mới thành công!', 'success');
    }
    classDialogVisible.value = false;
    await fetchClasses(); // Cập nhật lại bảng sau khi lưu
  } catch (error) {
    console.error('Error saving class:', error);
    notificationStore.showToast('Lỗi', 'Có lỗi xảy ra khi lưu lớp học.', 'error');
  } finally {
    savingClass.value = false;
  }
};

// --- Delete Class Functions ---
const confirmDeleteClass = (classItem) => {
  classToDelete.value = classItem;
  deleteClassDialogVisible.value = true;
};

const deleteClass = async () => {
  deleteClassDialogVisible.value = false;
  if (!classToDelete.value) return;

  loadingClasses.value = true; // Hiển thị loading khi xóa
  try {
    await classApi.deleteClass(classToDelete.value.id);
    notificationStore.showToast('Thành công', 'Xóa lớp học thành công!', 'success');
    await fetchClasses(); // Cập nhật lại bảng sau khi xóa
  } catch (error) {
    console.error('Error deleting class:', error);
    notificationStore.showToast('Lỗi', 'Không thể xóa lớp học.', 'error');
  } finally {
    loadingClasses.value = false;
    classToDelete.value = null; // Xóa đối tượng cần xóa
  }
};

// --- Pagination Handler ---
const onPageChange = (event) => {
  pagination.value.currentPage = event.page + 1; // PrimeVue page starts from 0
  pagination.value.itemsPerPage = event.rows;
  fetchClasses();
};
</script>

<style scoped>
.classes-page {
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