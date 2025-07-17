<template>
  <div class="p-grid">
    <div class="p-col-12">
      <h2 class="p-text-primary p-mb-4">Quản lý Phòng ban</h2>
      
      <p-button label="Thêm phòng ban mới" icon="pi pi-plus" @click="openNewDepartmentDialog" class="p-mb-4" />
      
      <BaseTable 
        :data="departments" 
        :columns="departmentTableColumns" 
        :loading="loadingDepartments"
        :enable-pagination="true"
        :current-page="pagination.currentPage"
        :total-records="pagination.totalRecords"
        :items-per-page="pagination.itemsPerPage"
        @page-change="onPageChange"
      >
        <template #actions="{ item }">
          <p-button icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm p-mr-1" @click="editDepartment(item)" />
          <p-button icon="pi pi-trash" class="p-button-rounded p-button-text p-button-danger p-button-sm" @click="confirmDeleteDepartment(item)" />
        </template>
      </BaseTable>

      <p-dialog v-model:visible="departmentDialogVisible" modal :header="dialogHeader" :style="{ width: '40vw' }" :breakpoints="{'960px': '60vw', '641px': '90vw'}">
        <DepartmentForm 
          :initial-data="selectedDepartment" 
          :is-edit-mode="isEditMode" 
          :is-loading="savingDepartment" 
          @submit="saveDepartment" 
          @cancel="departmentDialogVisible = false" 
        />
      </p-dialog>

      <ConfirmationDialog 
        :is-visible="deleteDepartmentDialogVisible" 
        title="Xác nhận xóa phòng ban" 
        :message="`Bạn có chắc chắn muốn xóa phòng ban '${departmentToDelete?.name}' không?`"
        @confirm="deleteDepartment" 
        @cancel="deleteDepartmentDialogVisible = false" 
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useNotificationStore } from '@/stores/notification';
import BaseTable from '@/components/common/BaseTable.vue';
import ConfirmationDialog from '@/components/common/ConfirmationDialog.vue';
import DepartmentForm from '@/components/admin/DepartmentForm.vue'; // Component DepartmentForm

// PrimeVue Components
import PButton from 'primevue/button';
import PDialog from 'primevue/dialog';

// Giả lập API
const departmentApi = {
  getDepartments: async (page, limit) => {
    const allDepartments = [
      { id: 1, name: 'Công nghệ thông tin', code: 'CNTT', description: 'Khoa Công nghệ thông tin' },
      { id: 2, name: 'Điện tử viễn thông', code: 'DTVT', description: 'Khoa Điện tử viễn thông' },
      { id: 3, name: 'Quản trị kinh doanh', code: 'QTKD', description: 'Khoa Quản trị kinh doanh' },
    ];
    const start = (page - 1) * limit;
    const end = start + limit;
    return new Promise(resolve => setTimeout(() => {
      resolve({
        data: allDepartments.slice(start, end),
        total: allDepartments.length
      });
    }, 500));
  },
  createDepartment: async (deptData) => {
    return new Promise(resolve => setTimeout(() => {
      console.log('Creating department:', deptData);
      resolve({ success: true, message: 'Department created successfully' });
    }, 500));
  },
  updateDepartment: async (id, deptData) => {
    return new Promise(resolve => setTimeout(() => {
      console.log(`Updating department ${id}:`, deptData);
      resolve({ success: true, message: 'Department updated successfully' });
    }, 500));
  },
  deleteDepartment: async (id) => {
    return new Promise(resolve => setTimeout(() => {
      console.log(`Deleting department ${id}`);
      resolve({ success: true, message: 'Department deleted successfully' });
    }, 500));
  }
};

const notificationStore = useNotificationStore();

const departments = ref([]);
const loadingDepartments = ref(false);
const departmentDialogVisible = ref(false);
const isEditMode = ref(false);
const selectedDepartment = ref(null);
const dialogHeader = ref('');
const savingDepartment = ref(false);

const deleteDepartmentDialogVisible = ref(false);
const departmentToDelete = ref(null);

const pagination = ref({
  currentPage: 1,
  itemsPerPage: 10,
  totalRecords: 0
});

const departmentTableColumns = [
  { field: 'id', header: 'ID', type: 'number' },
  { field: 'name', header: 'Tên Phòng ban', type: 'string' },
  { field: 'code', header: 'Mã Phòng ban', type: 'string' },
  { field: 'description', header: 'Mô tả', type: 'string' },
];

const fetchDepartments = async () => {
  loadingDepartments.value = true;
  try {
    const response = await departmentApi.getDepartments(pagination.value.currentPage, pagination.value.itemsPerPage);
    departments.value = response.data;
    pagination.value.totalRecords = response.total;
  } catch (error) {
    console.error('Error fetching departments:', error);
    notificationStore.showToast('Không thể tải danh sách phòng ban.', 'error');
  } finally {
    loadingDepartments.value = false;
  }
};

const openNewDepartmentDialog = () => {
  isEditMode.value = false;
  selectedDepartment.value = { name: '', code: '', description: '' };
  dialogHeader.value = 'Thêm Phòng ban Mới';
  departmentDialogVisible.value = true;
};

const editDepartment = (dept) => {
  isEditMode.value = true;
  selectedDepartment.value = { ...dept };
  dialogHeader.value = `Chỉnh sửa Phòng ban: ${dept.name}`;
  departmentDialogVisible.value = true;
};

const saveDepartment = async (formData) => {
  savingDepartment.value = true;
  try {
    if (isEditMode.value) {
      await departmentApi.updateDepartment(selectedDepartment.value.id, formData);
      notificationStore.showToast('Cập nhật phòng ban thành công!', 'success');
    } else {
      await departmentApi.createDepartment(formData);
      notificationStore.showToast('Thêm phòng ban mới thành công!', 'success');
    }
    departmentDialogVisible.value = false;
    await fetchDepartments();
  } catch (error) {
    console.error('Error saving department:', error);
    notificationStore.showToast('Lỗi khi lưu phòng ban.', 'error');
  } finally {
    savingDepartment.value = false;
  }
};

const confirmDeleteDepartment = (dept) => {
  departmentToDelete.value = dept;
  deleteDepartmentDialogVisible.value = true;
};

const deleteDepartment = async () => {
  deleteDepartmentDialogVisible.value = false;
  if (!departmentToDelete.value) return;

  loadingDepartments.value = true;
  try {
    await departmentApi.deleteDepartment(departmentToDelete.value.id);
    notificationStore.showToast('Xóa phòng ban thành công!', 'success');
    await fetchDepartments();
  } catch (error) {
    console.error('Error deleting department:', error);
    notificationStore.showToast('Lỗi khi xóa phòng ban.', 'error');
  } finally {
    loadingDepartments.value = false;
    departmentToDelete.value = null;
  }
};

const onPageChange = (event) => {
  pagination.value.currentPage = event.page;
  pagination.value.itemsPerPage = event.rows;
  fetchDepartments();
};

onMounted(() => {
  fetchDepartments();
});
</script>

<style scoped>
/* Không cần nhiều style ở đây vì các component con và PrimeFlex đã lo phần lớn */
</style>