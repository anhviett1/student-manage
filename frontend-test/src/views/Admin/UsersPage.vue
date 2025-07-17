<template>
  <div class="users-page">
    <h2 class="p-text-primary p-mb-4">Quản lý Người dùng</h2>
    
    <div class="p-mb-4 p-flex p-justify-content-between p-align-center">
      <p-button label="Thêm người dùng mới" icon="pi pi-plus" @click="openNewUserDialog" />
    </div>
      
    <BaseTable 
      :data="users" 
      :columns="userTableColumns" 
      :loading="loadingUsers"
      :enable-pagination="true"
      :current-page="pagination.currentPage"
      :total-records="pagination.totalRecords"
      :items-per-page="pagination.itemsPerPage"
      @page-change="onPageChange"
    >
      <template #actions="{ item }">
        <p-button icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm p-mr-1" @click="editUser(item)" />
        <p-button icon="pi pi-trash" class="p-button-rounded p-button-text p-button-danger p-button-sm" @click="confirmDeleteUser(item)" />
      </template>
    </BaseTable>

    <p-dialog v-model:visible="userDialogVisible" modal :header="dialogHeader" :style="{ width: '50vw' }" :breakpoints="{'960px': '75vw', '641px': '100vw'}">
      <UserForm 
        :initial-data="selectedUser" 
        :is-edit-mode="isEditMode" 
        :is-loading="savingUser" 
        @submit="saveUser" 
        @cancel="userDialogVisible = false" 
      />
    </p-dialog>

    <ConfirmationDialog 
      :is-visible="deleteUserDialogVisible" 
      title="Xác nhận xóa người dùng" 
      :message="`Bạn có chắc chắn muốn xóa người dùng '${userToDelete?.full_name}' không?`"
      @confirm="deleteUser" 
      @cancel="deleteUserDialogVisible = false" 
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useNotificationStore } from '@/stores/notification';
import BaseTable from '@/components/common/BaseTable.vue';
import ConfirmationDialog from '@/components/common/ConfirmationDialog.vue';
import UserForm from '@/components/admin/UserForm.vue';

// PrimeVue Components
import PButton from 'primevue/button';
import PDialog from 'primevue/dialog';

// Giả lập API
const userApi = {
  getUsers: async (page, limit) => {
    const allUsers = [
      { id: 1, username: 'admin1', full_name: 'Nguyễn Văn A', email: 'a@example.com', date_of_birth: '1990-01-15', gender: 'male', role: 'admin' },
      { id: 2, username: 'teacher1', full_name: 'Trần Thị B', email: 'b@example.com', date_of_birth: '1985-03-20', gender: 'female', role: 'teacher' },
      { id: 3, username: 'student1', full_name: 'Lê Văn C', email: 'c@example.com', date_of_birth: '2000-07-01', gender: 'male', role: 'student' },
      { id: 4, username: 'student2', full_name: 'Phạm Thu D', email: 'd@example.com', date_of_birth: '2001-11-11', gender: 'female', role: 'student' },
      { id: 5, username: 'teacher2', full_name: 'Hoàng Văn E', email: 'e@example.com', date_of_birth: '1988-09-05', gender: 'male', role: 'teacher' },
    ];
    const start = (page - 1) * limit;
    const end = start + limit;
    return new Promise(resolve => setTimeout(() => {
      resolve({
        data: allUsers.slice(start, end),
        total: allUsers.length
      });
    }, 500));
  },
  createUser: async (userData) => {
    return new Promise(resolve => setTimeout(() => {
      console.log('Creating user:', userData);
      resolve({ success: true, message: 'User created successfully' });
    }, 500));
  },
  updateUser: async (id, userData) => {
    return new Promise(resolve => setTimeout(() => {
      console.log(`Updating user ${id}:`, userData);
      resolve({ success: true, message: 'User updated successfully' });
    }, 500));
  },
  deleteUser: async (id) => {
    return new Promise(resolve => setTimeout(() => {
      console.log(`Deleting user ${id}`);
      resolve({ success: true, message: 'User deleted successfully' });
    }, 500));
  }
};

const notificationStore = useNotificationStore();

const users = ref([]);
const loadingUsers = ref(false);
const userDialogVisible = ref(false);
const isEditMode = ref(false);
const selectedUser = ref(null);
const dialogHeader = ref('');
const savingUser = ref(false);

const deleteUserDialogVisible = ref(false);
const userToDelete = ref(null);

const pagination = ref({
  currentPage: 1,
  itemsPerPage: 10,
  totalRecords: 0
});

const userTableColumns = [
  { field: 'id', header: 'ID', type: 'number' },
  { field: 'username', header: 'Tên đăng nhập', type: 'string' },
  { field: 'full_name', header: 'Họ và Tên', type: 'string' },
  { field: 'email', header: 'Email', type: 'string' },
  { field: 'date_of_birth', header: 'Ngày sinh', type: 'date' },
  { field: 'gender', header: 'Giới tính', type: 'string' },
  { field: 'role', header: 'Vai trò', type: 'string' },
];

const fetchUsers = async () => {
  loadingUsers.value = true;
  try {
    const response = await userApi.getUsers(pagination.value.currentPage, pagination.value.itemsPerPage);
    users.value = response.data;
    pagination.value.totalRecords = response.total;
  } catch (error) {
    console.error('Error fetching users:', error);
    notificationStore.showToast('Không thể tải danh sách người dùng.', 'error');
  } finally {
    loadingUsers.value = false;
  }
};

const openNewUserDialog = () => {
  isEditMode.value = false;
  selectedUser.value = {
    username: '', full_name: '', email: '', date_of_birth: null, gender: null, role: null, password: '', confirm_password: ''
  };
  dialogHeader.value = 'Thêm Người dùng Mới';
  userDialogVisible.value = true;
};

const editUser = (user) => {
  isEditMode.value = true;
  selectedUser.value = { ...user };
  dialogHeader.value = `Chỉnh sửa Người dùng: ${user.full_name}`;
  userDialogVisible.value = true;
};

const saveUser = async (formData) => {
  savingUser.value = true;
  try {
    if (isEditMode.value) {
      await userApi.updateUser(selectedUser.value.id, formData);
      notificationStore.showToast('Cập nhật người dùng thành công!', 'success');
    } else {
      await userApi.createUser(formData);
      notificationStore.showToast('Thêm người dùng mới thành công!', 'success');
    }
    userDialogVisible.value = false;
    await fetchUsers();
  } catch (error) {
    console.error('Error saving user:', error);
    notificationStore.showToast('Lỗi khi lưu người dùng.', 'error');
  } finally {
    savingUser.value = false;
  }
};

const confirmDeleteUser = (user) => {
  userToDelete.value = user;
  deleteUserDialogVisible.value = true;
};

const deleteUser = async () => {
  deleteUserDialogVisible.value = false;
  if (!userToDelete.value) return;

  loadingUsers.value = true;
  try {
    await userApi.deleteUser(userToDelete.value.id);
    notificationStore.showToast('Xóa người dùng thành công!', 'success');
    await fetchUsers();
  } catch (error) {
    console.error('Error deleting user:', error);
    notificationStore.showToast('Lỗi khi xóa người dùng.', 'error');
  } finally {
    loadingUsers.value = false;
    userToDelete.value = null;
  }
};

const onPageChange = (event) => {
  pagination.value.currentPage = event.page;
  pagination.value.itemsPerPage = event.rows;
  fetchUsers();
};

onMounted(() => {
  fetchUsers();
});
</script>

<style scoped>
/* PrimeFlex và PrimeVue đã cung cấp phần lớn styling */
</style>