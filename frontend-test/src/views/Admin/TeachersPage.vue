<template>
  <div class="teachers-page">
    <h2 class="p-text-primary p-mb-4">Quản lý Giáo viên</h2>
    
    <div class="p-mb-4 p-flex p-justify-content-between p-align-center">
      <p-button label="Thêm giáo viên mới" icon="pi pi-plus" @click="openNewTeacherDialog" />
    </div>

    <BaseTable 
      :data="teachers" 
      :columns="teacherTableColumns" 
      :loading="loadingTeachers"
      :enable-pagination="true"
      :current-page="pagination.currentPage"
      :total-records="pagination.totalRecords"
      :items-per-page="pagination.itemsPerPage"
      @page-change="onPageChange"
    >
      <template #actions="{ item }">
        <p-button icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm p-mr-1" @click="editTeacher(item)" />
        <p-button icon="pi pi-trash" class="p-button-rounded p-button-text p-button-danger p-button-sm" @click="confirmDeleteTeacher(item)" />
      </template>
    </BaseTable>

    <p-dialog v-model:visible="teacherDialogVisible" modal :header="dialogHeader" :style="{ width: '50vw' }" :breakpoints="{'960px': '75vw', '641px': '100vw'}">
      <UserForm 
        :initial-data="selectedTeacher" 
        :is-edit-mode="isEditMode" 
        :is-loading="savingTeacher" 
        :role-options="[{label: 'Giáo viên', value: 'teacher'}]"
        @submit="saveTeacher" 
        @cancel="teacherDialogVisible = false" 
      />
    </p-dialog>

    <ConfirmationDialog 
      :is-visible="deleteTeacherDialogVisible" 
      title="Xác nhận xóa giáo viên" 
      :message="`Bạn có chắc chắn muốn xóa giáo viên '${teacherToDelete?.full_name}' không?`"
      @confirm="deleteTeacher" 
      @cancel="deleteTeacherDialogVisible = false" 
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

// Giả lập API cho giáo viên
const teacherApi = {
  getTeachers: async (page, limit) => {
    const allTeachers = [
      { id: 2, username: 'teacher1', full_name: 'Trần Thị B', email: 'b@example.com', date_of_birth: '1985-03-20', gender: 'female', role: 'teacher', teacher_id: 'GV001', department: 'CNTT' },
      { id: 5, username: 'teacher2', full_name: 'Hoàng Văn E', email: 'e@example.com', date_of_birth: '1988-09-05', gender: 'male', role: 'teacher', teacher_id: 'GV002', department: 'DTVT' },
    ];
    const start = (page - 1) * limit;
    const end = start + limit;
    return new Promise(resolve => setTimeout(() => {
      resolve({
        data: allTeachers.slice(start, end),
        total: allTeachers.length
      });
    }, 500));
  },
  createTeacher: async (teacherData) => { /* ... API call */ return { success: true }; },
  updateTeacher: async (id, teacherData) => { /* ... API call */ return { success: true }; },
  deleteTeacher: async (id) => { /* ... API call */ return { success: true }; }
};

const notificationStore = useNotificationStore();

const teachers = ref([]);
const loadingTeachers = ref(false);
const teacherDialogVisible = ref(false);
const isEditMode = ref(false);
const selectedTeacher = ref(null);
const dialogHeader = ref('');
const savingTeacher = ref(false);

const deleteTeacherDialogVisible = ref(false);
const teacherToDelete = ref(null);

const pagination = ref({
  currentPage: 1,
  itemsPerPage: 10,
  totalRecords: 0
});

const teacherTableColumns = [
  { field: 'id', header: 'ID', type: 'number' },
  { field: 'teacher_id', header: 'Mã GV', type: 'string' }, // Trường đặc thù cho giáo viên
  { field: 'full_name', header: 'Họ và Tên', type: 'string' },
  { field: 'email', header: 'Email', type: 'string' },
  { field: 'department', header: 'Phòng ban', type: 'string' }, // Trường đặc thù
  { field: 'date_of_birth', header: 'Ngày sinh', type: 'date' },
  { field: 'gender', header: 'Giới tính', type: 'string' },
];

const fetchTeachers = async () => {
  loadingTeachers.value = true;
  try {
    const response = await teacherApi.getTeachers(pagination.value.currentPage, pagination.value.itemsPerPage);
    teachers.value = response.data;
    pagination.value.totalRecords = response.total;
  } catch (error) {
    console.error('Error fetching teachers:', error);
    notificationStore.showToast('Không thể tải danh sách giáo viên.', 'error');
  } finally {
    loadingTeachers.value = false;
  }
};

const openNewTeacherDialog = () => {
  isEditMode.value = false;
  selectedTeacher.value = {
    username: '', full_name: '', email: '', date_of_birth: null, gender: 'male', role: 'teacher', password: '', confirm_password: '', teacher_id: '', department: '' // Thêm các trường đặc thù
  };
  dialogHeader.value = 'Thêm Giáo viên Mới';
  teacherDialogVisible.value = true;
};

const editTeacher = (teacher) => {
  isEditMode.value = true;
  selectedTeacher.value = { ...teacher };
  dialogHeader.value = `Chỉnh sửa Giáo viên: ${teacher.full_name}`;
  teacherDialogVisible.value = true;
};

const saveTeacher = async (formData) => {
  savingTeacher.value = true;
  try {
    if (isEditMode.value) {
      await teacherApi.updateTeacher(selectedTeacher.value.id, formData);
      notificationStore.showToast('Cập nhật giáo viên thành công!', 'success');
    } else {
      await teacherApi.createTeacher(formData);
      notificationStore.showToast('Thêm giáo viên mới thành công!', 'success');
    }
    teacherDialogVisible.value = false;
    await fetchTeachers();
  } catch (error) {
    console.error('Error saving teacher:', error);
    notificationStore.showToast('Lỗi khi lưu giáo viên.', 'error');
  } finally {
    savingTeacher.value = false;
  }
};

const confirmDeleteTeacher = (teacher) => {
  teacherToDelete.value = teacher;
  deleteTeacherDialogVisible.value = true;
};

const deleteTeacher = async () => {
  deleteTeacherDialogVisible.value = false;
  if (!teacherToDelete.value) return;

  loadingTeachers.value = true;
  try {
    await teacherApi.deleteTeacher(teacherToDelete.value.id);
    notificationStore.showToast('Xóa giáo viên thành công!', 'success');
    await fetchTeachers();
  } catch (error) {
    console.error('Error deleting teacher:', error);
    notificationStore.showToast('Lỗi khi xóa giáo viên.', 'error');
  } finally {
    loadingTeachers.value = false;
    teacherToDelete.value = null;
  }
};

const onPageChange = (event) => {
  pagination.value.currentPage = event.page;
  pagination.value.itemsPerPage = event.rows;
  fetchTeachers();
};

onMounted(() => {
  fetchTeachers();
});
</script>

<style scoped>
/* PrimeFlex và PrimeVue đã cung cấp phần lớn styling */
</style>