<template>
  <div class="students-page">
    <h2 class="p-text-primary p-mb-4">Quản lý Sinh viên</h2>
    
    <div class="p-mb-4 p-flex p-justify-content-between p-align-center">
      <p-button label="Thêm sinh viên mới" icon="pi pi-plus" @click="openNewStudentDialog" />
    </div>

    <BaseTable 
      :data="students" 
      :columns="studentTableColumns" 
      :loading="loadingStudents"
      :enable-pagination="true"
      :current-page="pagination.currentPage"
      :total-records="pagination.totalRecords"
      :items-per-page="pagination.itemsPerPage"
      @page-change="onPageChange"
    >
      <template #actions="{ item }">
        <p-button icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm p-mr-1" @click="editStudent(item)" />
        <p-button icon="pi pi-trash" class="p-button-rounded p-button-text p-button-danger p-button-sm" @click="confirmDeleteStudent(item)" />
      </template>
    </BaseTable>

    <p-dialog v-model:visible="studentDialogVisible" modal :header="dialogHeader" :style="{ width: '50vw' }" :breakpoints="{'960px': '75vw', '641px': '100vw'}">
      <UserForm 
        :initial-data="selectedStudent" 
        :is-edit-mode="isEditMode" 
        :is-loading="savingStudent" 
        :role-options="[{label: 'Sinh viên', value: 'student'}]"
        @submit="saveStudent" 
        @cancel="studentDialogVisible = false" 
      />
    </p-dialog>

    <ConfirmationDialog 
      :is-visible="deleteStudentDialogVisible" 
      title="Xác nhận xóa sinh viên" 
      :message="`Bạn có chắc chắn muốn xóa sinh viên '${studentToDelete?.full_name}' không?`"
      @confirm="deleteStudent" 
      @cancel="deleteStudentDialogVisible = false" 
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useNotificationStore } from '@/stores/notification';
import BaseTable from '@/components/common/BaseTable.vue';
import ConfirmationDialog from '@/components/common/ConfirmationDialog.vue';
import UserForm from '@/components/admin/UserForm.vue'; // Tái sử dụng UserForm

// PrimeVue Components
import PButton from 'primevue/button';
import PDialog from 'primevue/dialog';

// Giả lập API cho sinh viên
const studentApi = {
  getStudents: async (page, limit) => {
    const allStudents = [
      { id: 3, username: 'student1', full_name: 'Lê Văn C', email: 'c@example.com', date_of_birth: '2000-07-01', gender: 'male', role: 'student', student_id: 'SV001', major: 'CNTT' },
      { id: 4, username: 'student2', full_name: 'Phạm Thu D', email: 'd@example.com', date_of_birth: '2001-11-11', gender: 'female', role: 'student', student_id: 'SV002', major: 'QTKD' },
      { id: 6, username: 'student3', full_name: 'Nguyễn Thanh H', email: 'h@example.com', date_of_birth: '2002-05-22', gender: 'male', role: 'student', student_id: 'SV003', major: 'DTVT' },
    ];
    const start = (page - 1) * limit;
    const end = start + limit;
    return new Promise(resolve => setTimeout(() => {
      resolve({
        data: allStudents.slice(start, end),
        total: allStudents.length
      });
    }, 500));
  },
  createStudent: async (studentData) => { /* ... API call */ return { success: true }; },
  updateStudent: async (id, studentData) => { /* ... API call */ return { success: true }; },
  deleteStudent: async (id) => { /* ... API call */ return { success: true }; }
};

const notificationStore = useNotificationStore();

const students = ref([]);
const loadingStudents = ref(false);
const studentDialogVisible = ref(false);
const isEditMode = ref(false);
const selectedStudent = ref(null);
const dialogHeader = ref('');
const savingStudent = ref(false);

const deleteStudentDialogVisible = ref(false);
const studentToDelete = ref(null);

const pagination = ref({
  currentPage: 1,
  itemsPerPage: 10,
  totalRecords: 0
});

const studentTableColumns = [
  { field: 'id', header: 'ID', type: 'number' },
  { field: 'student_id', header: 'Mã SV', type: 'string' }, // Trường đặc thù cho sinh viên
  { field: 'full_name', header: 'Họ và Tên', type: 'string' },
  { field: 'email', header: 'Email', type: 'string' },
  { field: 'major', header: 'Chuyên ngành', type: 'string' }, // Trường đặc thù
  { field: 'date_of_birth', header: 'Ngày sinh', type: 'date' },
  { field: 'gender', header: 'Giới tính', type: 'string' },
];

const fetchStudents = async () => {
  loadingStudents.value = true;
  try {
    const response = await studentApi.getStudents(pagination.value.currentPage, pagination.value.itemsPerPage);
    students.value = response.data;
    pagination.value.totalRecords = response.total;
  } catch (error) {
    console.error('Error fetching students:', error);
    notificationStore.showToast('Không thể tải danh sách sinh viên.', 'error');
  } finally {
    loadingStudents.value = false;
  }
};

const openNewStudentDialog = () => {
  isEditMode.value = false;
  selectedStudent.value = {
    username: '', full_name: '', email: '', date_of_birth: null, gender: 'male', role: 'student', password: '', confirm_password: '', student_id: '', major: '' // Thêm các trường đặc thù
  };
  dialogHeader.value = 'Thêm Sinh viên Mới';
  studentDialogVisible.value = true;
};

const editStudent = (student) => {
  isEditMode.value = true;
  selectedStudent.value = { ...student };
  dialogHeader.value = `Chỉnh sửa Sinh viên: ${student.full_name}`;
  studentDialogVisible.value = true;
};

const saveStudent = async (formData) => {
  savingStudent.value = true;
  try {
    if (isEditMode.value) {
      await studentApi.updateStudent(selectedStudent.value.id, formData);
      notificationStore.showToast('Cập nhật sinh viên thành công!', 'success');
    } else {
      await studentApi.createStudent(formData);
      notificationStore.showToast('Thêm sinh viên mới thành công!', 'success');
    }
    studentDialogVisible.value = false;
    await fetchStudents();
  } catch (error) {
    console.error('Error saving student:', error);
    notificationStore.showToast('Lỗi khi lưu sinh viên.', 'error');
  } finally {
    savingStudent.value = false;
  }
};

const confirmDeleteStudent = (student) => {
  studentToDelete.value = student;
  deleteStudentDialogVisible.value = true;
};

const deleteStudent = async () => {
  deleteStudentDialogVisible.value = false;
  if (!studentToDelete.value) return;

  loadingStudents.value = true;
  try {
    await studentApi.deleteStudent(studentToDelete.value.id);
    notificationStore.showToast('Xóa sinh viên thành công!', 'success');
    await fetchStudents();
  } catch (error) {
    console.error('Error deleting student:', error);
    notificationStore.showToast('Lỗi khi xóa sinh viên.', 'error');
  } finally {
    loadingStudents.value = false;
    studentToDelete.value = null;
  }
};

const onPageChange = (event) => {
  pagination.value.currentPage = event.page;
  pagination.value.itemsPerPage = event.rows;
  fetchStudents();
};

onMounted(() => {
  fetchStudents();
});
</script>

<style scoped>
/* PrimeFlex và PrimeVue đã cung cấp phần lớn styling */
</style>