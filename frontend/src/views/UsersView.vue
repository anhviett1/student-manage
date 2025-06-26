<template>
  <div v-if="isAdmin">
    <div class="card">
      <Toast />
      <ConfirmDialog></ConfirmDialog>

      <div class="header">
        <h2>Quản Lý Người Dùng</h2>
        <Button
          icon="pi pi-plus"
          label="Thêm Người Dùng"
          severity="primary"
          @click="openNew"
          v-tooltip="'Thêm người dùng mới'"
        />
      </div>

      <div class="filter-bar">
        <div class="filter-group">
          <Dropdown
            v-model="filters.role"
            :options="roleOptions"
            optionLabel="label"
            optionValue="value"
            placeholder="Lọc theo vai trò"
            class="filter-dropdown"
            showClear
            @change="loadUsers"
          />
          <InputText
            v-model="filters.search"
            placeholder="Tìm theo tên, email..."
            class="filter-search"
            @input="onSearchInput"
          />
        </div>
      </div>

      <DataTable
        :value="userStore.users"
        :loading="userStore.isLoading"
        dataKey="id"
        paginator
        :rows="10"
        :rowsPerPageOptions="[5, 10, 20]"
        responsiveLayout="scroll"
        class="p-datatable-sm"
      >
        <template #empty>
          <div class="empty-message">Không tìm thấy người dùng nào.</div>
        </template>
        <template #loading>
          <div class="loading-message">Đang tải dữ liệu...</div>
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
              v-tooltip="'Sửa'"
            />
            <Button
              icon="pi pi-trash"
              outlined
              rounded
              severity="danger"
              class="ml-2"
              @click="confirmDeleteUser(data)"
              v-tooltip="'Xóa'"
            />
          </template>
        </Column>
      </DataTable>

      <!-- Create/Edit Dialog -->
      <Dialog
        v-model:visible="userDialog"
        :header="isEditing ? 'Sửa Người Dùng' : 'Thêm Người Dùng'"
        :style="{ width: '500px' }"
        modal
        class="p-fluid"
      >
        <div class="field">
          <label for="username">Tên Đăng Nhập</label>
          <InputText id="username" v-model.trim="form.username" required :class="{ 'p-invalid': errors.username }" />
          <small class="p-error" v-if="errors.username">{{ errors.username }}</small>
        </div>
        <div class="field">
          <label for="email">Email</label>
          <InputText id="email" v-model.trim="form.email" type="email" required :class="{ 'p-invalid': errors.email }" />
          <small class="p-error" v-if="errors.email">{{ errors.email }}</small>
        </div>
        <div class="field">
          <label for="role">Vai Trò</label>
          <Dropdown
            id="role"
            v-model="form.role"
            :options="roleOptions"
            optionLabel="label"
            optionValue="value"
            placeholder="Chọn vai trò"
            required
            :class="{ 'p-invalid': errors.role }"
          />
          <small class="p-error" v-if="errors.role">{{ errors.role }}</small>
        </div>
        <div class="field">
          <label for="password">Mật Khẩu</label>
          <Password
            id="password"
            v-model="form.password"
            :required="!isEditing"
            :feedback="false"
            toggleMask
            :placeholder="isEditing ? 'Bỏ trống nếu không đổi' : 'Nhập mật khẩu'"
            :class="{ 'p-invalid': errors.password }"
          />
          <small class="p-error" v-if="errors.password">{{ errors.password }}</small>
        </div>
        <div class="field-checkbox">
          <Checkbox id="is_active" v-model="form.is_active" :binary="true" />
          <label for="is_active" class="ml-2">Hoạt động</label>
        </div>
        <template #footer>
          <Button label="Hủy" icon="pi pi-times" text @click="hideDialog" />
          <Button :label="isEditing ? 'Cập Nhật' : 'Tạo'" icon="pi pi-check" @click="handleSubmit" />
        </template>
      </Dialog>
    </div>
  </div>
  <div v-else class="access-denied">
    <h2>Truy Cập Bị Từ Chối</h2>
    <p>Bạn không có quyền truy cập vào trang này.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useUserStore } from '@/stores/user';
import { usePermissions } from '@/composables/usePermissions';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import Checkbox from 'primevue/checkbox';
import Password from 'primevue/password';
import Tag from 'primevue/tag';
import Toast from 'primevue/toast';
import ConfirmDialog from 'primevue/confirmdialog';

const userStore = useUserStore();
const { isAdmin } = usePermissions();
const toast = useToast();
const confirm = useConfirm();

const filters = ref({
  search: '',
  role: null,
});
const userDialog = ref(false);
const isEditing = ref(false);
const form = ref({
  id: null,
  username: '',
  email: '',
  role: 'student',
  password: '',
  is_active: true,
});
const errors = ref({});
let searchTimeout = null;

const roleOptions = [
  { label: 'Admin', value: 'admin' },
  { label: 'Teacher', value: 'teacher' },
  { label: 'Student', value: 'student' },
];

onMounted(() => {
  if (isAdmin.value) {
    loadUsers();
  }
});

const loadUsers = async () => {
  const params = {
    search: filters.value.search,
    role: filters.value.role,
  };
  try {
    await userStore.fetchUsers(params);
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách người dùng', life: 3000 });
  }
};

const onSearchInput = () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    loadUsers();
  }, 500);
};

const openNew = () => {
  isEditing.value = false;
  form.value = {
    id: null,
    username: '',
    email: '',
    role: 'student',
    password: '',
    is_active: true,
  };
  errors.value = {};
  userDialog.value = true;
};

const editUser = (user) => {
  isEditing.value = true;
  form.value = { ...user, password: '' }; // Clear password for editing
  errors.value = {};
  userDialog.value = true;
};

const hideDialog = () => {
  userDialog.value = false;
};

const handleSubmit = async () => {
  errors.value = {};
  try {
    if (isEditing.value) {
      // Don't send empty password
      const payload = { ...form.value };
      if (!payload.password) {
        delete payload.password;
      }
      await userStore.updateUser(form.value.id, payload);
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật người dùng thành công', life: 3000 });
    } else {
      await userStore.createUser(form.value);
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Tạo người dùng thành công', life: 3000 });
    }
    hideDialog();
    loadUsers();
  } catch (error) {
    const errorData = error.response?.data;
    if (errorData) {
      errors.value = errorData;
    }
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errorData?.detail || 'Lưu người dùng thất bại', life: 3000 });
  }
};

const confirmDeleteUser = (user) => {
  confirm.require({
    message: `Bạn có chắc muốn xóa người dùng "${user.username}"?`,
    header: 'Xác nhận xóa',
    icon: 'pi pi-exclamation-triangle',
    acceptClass: 'p-button-danger',
    accept: async () => {
      try {
        await userStore.deleteUser(user.id);
        toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa người dùng thành công', life: 3000 });
        loadUsers();
      } catch (error) {
        toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Xóa người dùng thất bại', life: 3000 });
      }
    },
  });
};

const getRoleSeverity = (role) => {
  if (role === 'admin') return 'danger';
  if (role === 'teacher') return 'info';
  return 'success';
};
</script>

<style scoped>
.card {
  padding: 1.5rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.header h2 {
  margin: 0;
  font-size: 1.8rem;
  color: #333;
}

.filter-bar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.filter-dropdown {
  width: 200px;
}

.filter-search {
  width: 250px;
}

.p-datatable-sm :deep(.p-datatable-tbody > tr > td) {
  padding: 0.75rem;
  font-size: 0.9rem;
}

.p-datatable-sm :deep(.p-datatable-thead > tr > th) {
  background: #f8f9fa;
  padding: 0.75rem;
  font-size: 0.95rem;
}

.field {
  margin-bottom: 1.2rem;
}

.field-checkbox {
  display: flex;
  align-items: center;
  margin-top: 1rem;
}

.access-denied {
  text-align: center;
  padding: 3rem;
  color: #6c757d;
}
.access-denied h2 {
  color: #dc3545;
}
</style> 