<template>
  <div class="user-management-content" aria-label="Phần quản lý người dùng">
    <div class="header">
      <h2 class="section-title">Quản Lý Người Dùng</h2>
      <Button
        icon="pi pi-plus"
        label="Thêm Người Dùng"
        severity="primary"
        @click="openNewUser"
        class="add-user-button"
        aria-label="Thêm người dùng mới"
        :disabled="!userStore.isAdmin"
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
      :value="userStore.users"
      :loading="userStore.isLoading"
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
            :disabled="!userStore.isAdmin"
          />
          <Button
            icon="pi pi-trash"
            outlined
            rounded
            severity="danger"
            @click="confirmDeleteUser(data)"
            class="action-button"
            aria-label="Xóa người dùng"
            :disabled="!userStore.isAdmin"
          />
        </template>
      </Column>
    </DataTable>
    <Dialog
      v-model:visible="userDialog"
      :header="isEditing ? 'Sửa Người Dùng' : 'Thêm Người Dùng'"
      modal
      class="user-dialog"
      aria-labelledby="user-dialog-header"
    >
      <h3 id="user-dialog-header" class="sr-only">{{ isEditing ? 'Sửa Người Dùng' : 'Thêm Người Dùng' }}</h3>
      <div class="field">
        <label for="username" class="field-label">Tên Đăng Nhập</label>
        <InputText
          id="username"
          v-model.trim="userForm.username"
          class="field-input"
          :class="{ 'invalid': userErrors.username }"
          aria-describedby="username-desc"
        />
        <small id="username-desc" class="field-error" v-if="userErrors.username">{{ userErrors.username }}</small>
      </div>
      <div class="field">
        <label for="email" class="field-label">Email</label>
        <InputText
          id="email"
          v-model.trim="userForm.email"
          type="email"
          class="field-input"
          :class="{ 'invalid': userErrors.email }"
          aria-describedby="email-desc"
        />
        <small id="email-desc" class="field-error" v-if="userErrors.email">{{ userErrors.email }}</small>
      </div>
      <div class="field">
        <label for="role" class="field-label">Vai Trò</label>
        <Dropdown
          id="role"
          v-model="userForm.role"
          :options="roleOptions"
          optionLabel="label"
          optionValue="value"
          placeholder="Chọn vai trò"
          class="field-input"
          :class="{ 'invalid': userErrors.role }"
          aria-describedby="role-desc"
        />
        <small id="role-desc" class="field-error" v-if="userErrors.role">{{ userErrors.role }}</small>
      </div>
      <div class="field">
        <label for="password" class="field-label">Mật Khẩu</label>
        <Password
          id="password"
          v-model="userForm.password"
          :required="!isEditing"
          :feedback="false"
          toggleMask
          :placeholder="isEditing ? 'Bỏ trống nếu không đổi' : 'Nhập mật khẩu'"
          class="field-input"
          :class="{ 'invalid': userErrors.password }"
          aria-describedby="password-desc"
        />
        <small id="password-desc" class="field-error" v-if="userErrors.password">{{ userErrors.password }}</small>
      </div>
      <div class="field-checkbox">
        <Checkbox id="is_active" v-model="userForm.is_active" :binary="true" aria-label="Trạng thái hoạt động" />
        <label for="is_active" class="checkbox-label">Hoạt động</label>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="userDialog = false" aria-label="Hủy" />
        <Button
          :label="isEditing ? 'Cập Nhật' : 'Tạo'"
          icon="pi pi-check"
          @click="handleUserSubmit"
          :aria-label="isEditing ? 'Cập nhật người dùng' : 'Tạo người dùng'"
        />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';
import { useUserStore } from '@/stores/user';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import Password from 'primevue/password';
import Checkbox from 'primevue/checkbox';
import Tag from 'primevue/tag';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Dialog from 'primevue/dialog';

const toast = useToast();
const confirm = useConfirm();
const userStore = useUserStore();

const userDialog = ref(false);
const isEditing = ref(false);
const userForm = ref({ username: '', email: '', role: null, password: '', is_active: true });
const userErrors = ref({});
const userFilters = ref({ search: '', role: null });
const paginatorInfo = ref({ rows: 10, page: 1, total: 0 });

const roleOptions = [
  { label: 'Admin', value: 'admin' },
  { label: 'Teacher', value: 'teacher' },
  { label: 'Student', value: 'student' },
];

const loadUsers = async (page = 1, rows = paginatorInfo.value.rows) => {
  try {
    const response = await userStore.fetchUsers({
      page,
      page_size: rows,
      search: userFilters.value.search,
      role: userFilters.value.role,
    });
    paginatorInfo.value = { rows, page, total: response.length || 0 };
  } catch (error) {
    // Error handled in userStore
  }
};

const onPage = (event) => {
  paginatorInfo.value.page = event.page + 1;
  paginatorInfo.value.rows = event.rows;
  loadUsers(event.page + 1, event.rows);
};

const debouncedLoadUsers = () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => loadUsers(), 500);
};
let searchTimeout = null;

const openNewUser = () => {
  if (!userStore.isAdmin) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Bạn không có quyền tạo người dùng', life: 3000 });
    return;
  }
  userForm.value = { username: '', email: '', role: null, password: '', is_active: true };
  userErrors.value = {};
  isEditing.value = false;
  userDialog.value = true;
};

const editUser = (user) => {
  if (!userStore.isAdmin) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Bạn không có quyền chỉnh sửa người dùng', life: 3000 });
    return;
  }
  userForm.value = { ...user, password: '' };
  userErrors.value = {};
  isEditing.value = true;
  userDialog.value = true;
};

const handleUserSubmit = async () => {
  userErrors.value = {};
  try {
    if (isEditing.value) {
      const payload = { ...userForm.value };
      if (!payload.password) delete payload.password;
      await userStore.updateUser(userForm.value.id, payload);
    } else {
      await userStore.createUser(userForm.value);
    }
    userDialog.value = false;
    loadUsers();
  } catch (error) {
    userErrors.value = error.response?.data || {};
    // Error toast handled in userStore
  }
};

const confirmDeleteUser = (user) => {
  if (!userStore.isAdmin) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Bạn không có quyền xóa người dùng', life: 3000 });
    return;
  }
  confirm.require({
    message: `Bạn có chắc muốn xóa người dùng "${user.username}"?`,
    header: 'Xác nhận xóa',
    icon: 'pi pi-exclamation-triangle',
    acceptClass: 'p-button-danger',
    accept: async () => {
      try {
        await userStore.deleteUser(user.id);
        loadUsers();
      } catch (error) {
        // Error toast handled in userStore
      }
    },
    acceptLabel: 'Xóa',
    rejectLabel: 'Hủy',
  });
};

const getRoleSeverity = (role) => {
  if (role === 'admin') return 'danger';
  if (role === 'teacher') return 'info';
  return 'success';
};
</script>

<style scoped>
.user-management-content {
  padding: 24px;
  background-color: #f9fafb;
  border-radius: 8px;
}
.dark-theme .user-management-content {
  background-color: #374151;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.section-title {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
}
.dark-theme .section-title {
  color: #f3f4f6;
}
.filter-bar {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-bottom: 16px;
}
.filter-dropdown {
  width: 192px;
}
.filter-input {
  width: 256px;
  padding: 8px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
}
.dark-theme .filter-input {
  background-color: #374151;
  border-color: #6b7280;
  color: #ffffff;
}
.user-table .p-datatable-tbody > tr > td {
  padding: 12px;
  font-size: 14px;
}
.user-table .p-datatable-thead > tr > th {
  padding: 12px;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  background-color: #f9fafb;
}
.dark-theme .user-table .p-datatable-thead > tr > th {
  color: #e5e7eb;
  background-color: #4b5563;
}
.empty-table, .loading-table {
  text-align: center;
  padding: 16px;
  color: #6b7280;
}
.dark-theme .empty-table, .dark-theme .loading-table {
  color: #d1d5db;
}
.add-user-button {
  padding: 8px 16px;
  border-radius: 6px;
  background-color: #3b82f6;
  color: #ffffff;
}
.action-button {
  margin-right: 8px;
}
.user-dialog {
  width: 100%;
  max-width: 448px;
}
.field {
  margin-bottom: 16px;
}
.field-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 4px;
}
.dark-theme .field-label {
  color: #e5e7eb;
}
.field-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
}
.dark-theme .field-input {
  background-color: #374151;
  border-color: #6b7280;
  color: #ffffff;
}
.field-input.invalid {
  border-color: #ef4444;
}
.field-error {
  color: #ef4444;
  font-size: 12px;
}
.field-checkbox {
  display: flex;
  align-items: center;
}
.checkbox-label {
  margin-left: 8px;
  font-size: 14px;
  color: #374151;
}
.dark-theme .checkbox-label {
  color: #e5e7eb;
}
</style>