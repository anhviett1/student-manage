<template>
  <div class="user-management-section card">
    <div class="header">
      <h2 class="section-title">Quản Lý Người Dùng</h2>
      <Button
        icon="pi pi-plus"
        label="Thêm Người Dùng"
        severity="primary"
        @click="openNewUser"
        class="add-user-button"
        aria-label="Thêm người dùng mới"
      />
    </div>
    <div class="filter-bar">
      <Dropdown
        v-model="userFilters.role"
        :options="roleOptions"
        optionLabel="label"
        optionValue="value"
        placeholder="Lọc theo vai trò"
        class="filter-dropdown"
        showClear
        @change="loadUsers"
        aria-label="Lọc theo vai trò"
      />
      <InputText
        v-model="userFilters.search"
        placeholder="Tìm theo tên, email..."
        class="filter-input"
        @input="debouncedLoadUsers"
        aria-label="Tìm kiếm người dùng"
      />
    </div>
    <DataTable
      :value="usersList"
      :loading="isLoading"
      dataKey="id"
      paginator
      :rows="paginatorInfo.rows"
      :rowsPerPageOptions="[5, 10, 20]"
      :totalRecords="paginatorInfo.total"
      :lazy="true"
      @page="onPage"
      class="user-table"
      aria-label="Bảng danh sách người dùng"
    >
      <template #empty>
        <div class="empty-table" aria-live="polite">Không tìm thấy người dùng nào.</div>
      </template>
      <template #loading>
        <div class="loading-table" aria-live="polite">Đang tải dữ liệu...</div>
      </template>
      <Column field="id" header="ID" sortable style="width: 8%" />
      <Column field="username" header="Tên Đăng Nhập" sortable style="width: 20%" />
      <Column field="email" header="Email" sortable style="width: 25%" />
      <Column field="role" header="Vai Trò" sortable style="width: 15%">
        <template #body="{ data }">
          <Tag :severity="getRoleSeverity(data.role)" :value="data.role" />
        </template>
      </Column>
      <Column field="is_active" header="Trạng Thái" sortable style="width: 12%">
        <template #body="{ data }">
          <Tag :severity="data.is_active ? 'success' : 'danger'" :value="data.is_active ? 'Active' : 'Inactive'" />
        </template>
      </Column>
      <Column header="Hành Động" style="width: 15%" align="center">
        <template #body="{ data }">
          <Button
            icon="pi pi-pencil"
            outlined
            rounded
            severity="info"
            @click="editUser(data)"
            class="action-button"
            aria-label="Sửa người dùng"
          />
          <Button
            icon="pi pi-trash"
            outlined
            rounded
            severity="danger"
            @click="confirmDeleteUser(data)"
            class="action-button"
            aria-label="Xóa người dùng"
          />
        </template>
      </Column>
    </DataTable>
    <Dialog
      v-model:visible="userStore.userDialog"
      :header="userStore.isEditing ? 'Sửa Người Dùng' : 'Thêm Người Dùng'"
      modal
      class="user-dialog"
      aria-labelledby="user-dialog-header"
    >
      <h3 id="user-dialog-header" class="sr-only">{{ userStore.isEditing ? 'Sửa Người Dùng' : 'Thêm Người Dùng' }}</h3>
      <div class="field">
        <label for="username" class="field-label">Tên Đăng Nhập</label>
        <InputText
          id="username"
          v-model.trim="userStore.userForm.username"
          class="field-input"
          :class="{ 'invalid': userStore.userErrors.username }"
          aria-describedby="username-desc"
        />
        <small id="username-desc" class="field-error" v-if="userStore.userErrors.username">{{ userStore.userErrors.username }}</small>
      </div>
      <div class="field">
        <label for="email" class="field-label">Email</label>
        <InputText
          id="email"
          v-model.trim="userStore.userForm.email"
          type="email"
          class="field-input"
          :class="{ 'invalid': userStore.userErrors.email }"
          aria-describedby="email-desc"
        />
        <small id="email-desc" class="field-error" v-if="userStore.userErrors.email">{{ userStore.userErrors.email }}</small>
      </div>
      <div class="field">
        <label for="role" class="field-label">Vai Trò</label>
        <Dropdown
          id="role"
          v-model="userStore.userForm.role"
          :options="roleOptions"
          optionLabel="label"
          optionValue="value"
          placeholder="Chọn vai trò"
          class="field-input"
          :class="{ 'invalid': userStore.userErrors.role }"
          aria-describedby="role-desc"
        />
        <small id="role-desc" class="field-error" v-if="userStore.userErrors.role">{{ userStore.userErrors.role }}</small>
      </div>
      <div class="field">
        <label for="password" class="field-label">Mật Khẩu</label>
        <Password
          id="password"
          v-model="userStore.userForm.password"
          :required="!userStore.isEditing"
          :feedback="false"
          toggleMask
          :placeholder="userStore.isEditing ? 'Bỏ trống nếu không đổi' : 'Nhập mật khẩu'"
          class="field-input"
          :class="{ 'invalid': userStore.userErrors.password }"
          aria-describedby="password-desc"
        />
        <small id="password-desc" class="field-error" v-if="userStore.userErrors.password">{{ userStore.userErrors.password }}</small>
      </div>
      <div class="field-checkbox">
        <Checkbox id="is_active" v-model="userStore.userForm.is_active" :binary="true" aria-label="Trạng thái hoạt động" />
        <label for="is_active" class="checkbox-label">Hoạt động</label>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="userStore.userDialog = false" aria-label="Hủy" />
        <Button :label="userStore.isEditing ? 'Cập Nhật' : 'Tạo'" icon="pi pi-check" @click="handleUserSubmit" :aria-label="userStore.isEditing ? 'Cập nhật người dùng' : 'Tạo người dùng'" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';
import { useUserStore } from '@/stores/user';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import Tag from 'primevue/tag';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Dialog from 'primevue/dialog';
import Password from 'primevue/password';
import Checkbox from 'primevue/checkbox';

const toast = useToast();
const confirm = useConfirm();
const userStore = useUserStore();

const isLoading = ref(false);
const usersList = ref([]);
const userFilters = ref({ search: '', role: null });
const paginatorInfo = ref({ rows: 10, page: 1, total: 0 });

const roleOptions = [
  { label: 'Admin', value: 'admin' },
  { label: 'Teacher', value: 'teacher' },
  { label: 'Student', value: 'student' },
];

let searchTimeout = null;

onMounted(() => {
  loadUsers();
});

const loadUsers = async () => {
  isLoading.value = true;
  try {
    const fetchedUsers = await userStore.fetchAllUsers();
    let filteredUsers = fetchedUsers;

    if (userFilters.value.role) {
      filteredUsers = filteredUsers.filter(user => user.role === userFilters.value.role);
    }
    if (userFilters.value.search) {
      const searchTerm = userFilters.value.search.toLowerCase();
      filteredUsers = filteredUsers.filter(user =>
        user.username.toLowerCase().includes(searchTerm) ||
        user.email.toLowerCase().includes(searchTerm) ||
        (user.first_name && user.first_name.toLowerCase().includes(searchTerm)) ||
        (user.last_name && user.last_name.toLowerCase().includes(searchTerm))
      );
    }

    usersList.value = filteredUsers.sort((a, b) => a.id - b.id);
    paginatorInfo.value = { rows: usersList.value.length, page: 1, total: usersList.value.length };
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: error.response?.data?.message || 'Không thể tải danh sách người dùng', life: 3000 });
  } finally {
    isLoading.value = false;
  }
};

const onPage = (event) => {
  paginatorInfo.value.page = event.page + 1;
  paginatorInfo.value.rows = event.rows;
  // Note: For actual pagination with backend, you'd pass event.page and event.rows to your API
  // For this example, we re-filter the already loaded list.
  // In a real app, you'd fetch a specific page of data.
};

const debouncedLoadUsers = () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => loadUsers(), 500);
};

const openNewUser = () => {
  userStore.resetUserForm();
  userStore.userDialog = true;
};

const editUser = (user) => {
  userStore.setUserForm({ ...user, password: '' }); // Clear password for editing
  userStore.userDialog = true;
};

const handleUserSubmit = async () => {
  userStore.userErrors = {}; // Clear previous errors
  try {
    if (userStore.isEditing) {
      const payload = { ...userStore.userForm };
      if (!payload.password) delete payload.password; // Don't send empty password if not changed
      await userStore.updateUser(userStore.userForm.id, payload);
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật người dùng thành công', life: 3000 });
    } else {
      await userStore.createUser(userStore.userForm);
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Tạo người dùng thành công', life: 3000 });
    }
    userStore.userDialog = false;
    loadUsers(); // Reload the user list
  } catch (error) {
    const errorDetail = error.response?.data?.message || error.message || 'Thao tác thất bại';
    if (error.response?.data?.errors) {
      userStore.userErrors = error.response.data.errors; // Set validation errors
    }
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errorDetail, life: 5000 });
  }
};

const confirmDeleteUser = (user) => {
  confirm.require({
    message: `Bạn có chắc chắn muốn xóa người dùng "${user.username}" không?`,
    header: 'Xác nhận xóa',
    icon: 'pi pi-exclamation-triangle',
    acceptClass: 'p-button-danger',
    acceptLabel: 'Xóa',
    rejectLabel: 'Hủy',
    accept: async () => {
      try {
        await userStore.deleteUser(user.id);
        toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa người dùng thành công', life: 3000 });
        loadUsers();
      } catch (error) {
        toast.add({ severity: 'error', summary: 'Lỗi', detail: error.response?.data?.message || 'Xóa người dùng thất bại', life: 3000 });
      }
    },
    reject: () => {
      toast.add({ severity: 'info', summary: 'Hủy bỏ', detail: 'Hành động xóa đã bị hủy', life: 3000 });
    }
  });
};

const getRoleSeverity = (role) => {
  switch (role) {
    case 'admin': return 'danger';
    case 'teacher': return 'warning';
    case 'student': return 'info';
    default: return null;
  }
};
</script>

<style scoped>
/* Styles from ProfileView.vue related to User Management */
.user-management-section {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  font-size: 1.6em;
  color: #333;
  margin: 0;
}

.filter-bar {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.filter-dropdown, .filter-input {
  flex-grow: 1;
  min-width: 200px;
}

.user-table {
  width: 100%;
}

.action-button {
  margin-right: 5px;
}

.user-dialog .field {
  margin-bottom: 15px;
}

.user-dialog .field-label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.user-dialog .field-input {
  width: 100%;
}

.user-dialog .field-error {
  color: var(--p-red-500);
  font-size: 0.85em;
  margin-top: 5px;
  display: block;
}

.user-dialog .field-input.invalid {
  border-color: var(--p-red-500);
}

.field-checkbox {
  display: flex;
  align-items: center;
  margin-top: 20px;
}

.field-checkbox .checkbox-label {
  margin-left: 8px;
}

.empty-table, .loading-table {
  text-align: center;
  padding: 20px;
  color: #666;
}
</style>