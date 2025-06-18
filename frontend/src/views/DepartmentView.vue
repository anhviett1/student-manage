<template>
  <div>
    <div class="card-header">
      <div>
        <Button @click="loadActiveDepartments" severity="primary" icon="pi pi-filter" label="Khoa Active" class="mr-2" />
        <Button v-if="canEditDepartments" @click="openNew" severity="success" icon="pi pi-plus" label="Thêm Khoa" />
        <Button v-if="canImportDepartments" icon="pi pi-upload" label="Import" @click="openImport" class="mr-2" />
        <Button v-if="canExportDepartments" icon="pi pi-download" label="Export" @click="exportCSV" />
      </div>
    </div>
    <DataTable
      v-if="canViewDepartments"
      :value="departments"
      :paginator="true"
      :rows="10"
      :loading="loading"
      dataKey="code"
      :filters="filters"
      filterDisplay="menu"
      :globalFilterFields="['name', 'code', 'description']"
      responsiveLayout="stack"
    >
      <template #empty>
        <div class="text-center p-4">
          <p>Không tìm thấy khoa nào.</p>
        </div>
      </template>
      <template #loading>
        <div class="text-center p-4">
          <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
        </div>
      </template>
      <Column field="code" header="Mã Khoa" sortable style="min-width: 10rem">
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            @input="filterCallback()"
            placeholder="Tìm theo mã khoa"
            class="p-column-filter"
          />
        </template>
      </Column>
      <Column field="name" header="Tên Khoa" sortable style="min-width: 14rem">
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            @input="filterCallback()"
            placeholder="Tìm theo tên khoa"
            class="p-column-filter"
          />
        </template>
      </Column>
      <Column field="head.full_name" header="Trưởng Khoa" sortable style="min-width: 12rem">
        <template #body="{ data }">
          {{ data.head?.full_name || '-' }}
        </template>
      </Column>
      <Column field="status" header="Trạng Thái" sortable style="min-width: 10rem">
        <template #body="{ data }">
          <Tag :severity="getStatusSeverity(data.is_active ? 'active' : 'inactive')" :value="data.is_active ? 'Đang hoạt động' : 'Không hoạt động'" />
        </template>
        <template #filter="{ filterModel, filterCallback }">
          <Dropdown
            v-model="filterModel.value"
            :options="statusOptions"
            optionLabel="label"
            optionValue="value"
            placeholder="Chọn trạng thái"
            @change="filterCallback()"
            class="p-column-filter"
          />
        </template>
      </Column>
      <Column :exportable="false" style="min-width: 12rem">
        <template #body="{ data }">
          <Button
            v-if="canEditDepartments && !data.is_deleted"
            icon="pi pi-pencil"
            outlined
            rounded
            severity="info"
            @click="editDepartment(data)"
            v-tooltip="'Sửa thông tin'"
          />
          <Button
            v-if="canDeleteDepartments && !data.is_deleted"
            icon="pi pi-trash"
            outlined
            rounded
            severity="danger"
            class="mr-2"
            @click="confirmDelete(data)"
            v-tooltip="'Xóa mềm'"
          />
          <Button
            v-if="canDeleteDepartments && data.is_deleted"
            icon="pi pi-undo"
            outlined
            rounded
            severity="success"
            @click="restoreDepartment(data)"
            v-tooltip="'Khôi phục'"
          />
        </template>
      </Column>
    </DataTable>
    <Dialog v-model:visible="departmentDialog" :style="{ width: '600px' }" header="Thông Tin Khoa" :modal="true" class="p-fluid">
      <div class="form-section">
        <h4>Thông Tin Cơ Bản</h4>
        <div class="field">
          <label for="code">Mã Khoa</label>
          <InputText
            id="code"
            v-model.trim="department.code"
            :disabled="!!department.code"
            required
            autofocus
            :class="{ 'p-invalid': errors.code }"
          />
          <small class="p-error" v-if="errors.code">{{ errors.code }}</small>
        </div>
        <div class="field">
          <label for="name">Tên Khoa</label>
          <InputText
            id="name"
            v-model.trim="department.name"
            required
            :class="{ 'p-invalid': errors.name }"
          />
          <small class="p-error" v-if="errors.name">{{ errors.name }}</small>
        </div>
        <div class="field">
          <label for="description">Mô Tả</label>
          <Textarea id="description" v-model="department.description" rows="4" />
        </div>
        <div class="field">
          <label for="head">Trưởng Khoa</label>
          <Dropdown
            id="head"
            v-model="department.head"
            :options="users"
            optionLabel="full_name"
            optionValue="id"
            placeholder="Chọn trưởng khoa"
          />
        </div>
        <div class="field">
          <label for="is_active">Đang Hoạt Động</label>
          <InputSwitch id="is_active" v-model="department.is_active" />
        </div>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="hideDialog" />
        <Button label="Lưu" icon="pi pi-check" @click="saveDepartment" />
      </template>
    </Dialog>
    <Dialog v-model:visible="deleteDepartmentDialog" :style="{ width: '450px' }" header="Xác Nhận Xóa Mềm" :modal="true">
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span v-if="department">Bạn có chắc chắn muốn xóa mềm khoa <b>{{ department.name }}</b>?</span>
      </div>
      <template #footer>
        <Button label="Không" icon="pi pi-times" text @click="deleteDepartmentDialog = false" />
        <Button label="Có" icon="pi pi-check" severity="danger" @click="deleteDepartment" />
      </template>
    </Dialog>
    <Dialog v-model:visible="restoreDepartmentDialog" :style="{ width: '450px' }" header="Xác Nhận Khôi Phục" :modal="true">
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span v-if="department">Bạn có chắc chắn muốn khôi phục khoa <b>{{ department.name }}</b>?</span>
      </div>
      <template #footer>
        <Button label="Không" icon="pi pi-times" text @click="restoreDepartmentDialog = false" />
        <Button label="Có" icon="pi pi-check" severity="success" @click="restoreDepartment" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { usePermissions } from '@/composables/usePermissions'
import api from '@/services/api'

const toast = useToast()
const { canViewDepartments, canEditDepartments, canDeleteDepartments, canImportDepartments, canExportDepartments } = usePermissions()
const departments = ref([])
const users = ref([])
const departmentDialog = ref(false)
const deleteDepartmentDialog = ref(false)
const restoreDepartmentDialog = ref(false)
const department = ref({})
const loading = ref(true)
const errors = ref({})
const filters = ref({
  code: { value: null, matchMode: 'contains' },
  name: { value: null, matchMode: 'contains' },
  status: { value: null, matchMode: 'equals' }
})
const statusOptions = [
  { label: 'Đang hoạt động', value: 'active' },
  { label: 'Không hoạt động', value: 'inactive' }
]

onMounted(async () => {
  await Promise.all([loadDepartments(), loadUsers()])
})

const loadDepartments = async () => {
  try {
    loading.value = true
    const response = await api.get('/departments')
    departments.value = response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách khoa', life: 3000 })
  } finally {
    loading.value = false
  }
}

const loadUsers = async () => {
  try {
    const response = await api.get('/users', { params: { role: 'department_head,admin' } })
    users.value = response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách người dùng', life: 3000 })
  }
}

const loadActiveDepartments = async () => {
  try {
    loading.value = true
    const response = await api.get('/departments', { params: { status: 'active' } })
    departments.value = response.data
    toast.add({ severity: 'info', summary: 'Thành công', detail: 'Hiển thị các khoa đang hoạt động', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải khoa đang hoạt động', life: 3000 })
  } finally {
    loading.value = false
  }
}

const openNew = () => {
  department.value = { is_active: true }
  errors.value = {}
  departmentDialog.value = true
}

const hideDialog = () => {
  departmentDialog.value = false
  errors.value = {}
}

const editDepartment = (data) => {
  department.value = { ...data }
  errors.value = {}
  departmentDialog.value = true
}

const confirmDelete = (data) => {
  department.value = data
  deleteDepartmentDialog.value = true
}

const restoreDepartment = async () => {
  try {
    const response = await api.post(`/departments/${department.value.code}/restore/`)
    departments.value = departments.value.map(d => d.code === department.value.code ? response.data : d)
    restoreDepartmentDialog.value = false
    department.value = {}
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Khôi phục khoa thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể khôi phục khoa', life: 3000 })
  }
}

const validateDepartment = () => {
  errors.value = {}
  if (!department.value.code?.trim()) errors.value.code = 'Vui lòng nhập mã khoa'
  if (!department.value.name?.trim()) errors.value.name = 'Vui lòng nhập tên khoa'
}

const saveDepartment = async () => {
  validateDepartment()
  if (Object.keys(errors.value).length > 0) return
  try {
    const payload = { ...department.value }
    if (department.value.code) {
      const updatedDepartment = (await api.patch(`/departments/${department.value.code}/`, payload)).data
      departments.value = departments.value.map(d => d.code === updatedDepartment.code ? updatedDepartment : d)
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật khoa thành công', life: 3000 })
    } else {
      const newDepartment = (await api.post('/departments/', payload)).data
      departments.value.push(newDepartment)
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Thêm khoa thành công', life: 3000 })
    }
    departmentDialog.value = false
    department.value = {}
  } catch (error) {
    const errorMsg = error.response?.data?.detail || Object.values(error.response?.data || {}).join(', ') || 'Không thể lưu thông tin khoa'
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errorMsg, life: 5000 })
  }
}

const deleteDepartment = async () => {
  try {
    await api.delete(`/departments/${department.value.code}/`)
    departments.value = departments.value.filter(d => d.code !== department.value.code)
    deleteDepartmentDialog.value = false
    department.value = {}
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa mềm khoa thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa khoa', life: 3000 })
  }
}

const openImport = () => {
  toast.add({ severity: 'info', summary: 'Chức năng', detail: 'Chức năng import đang được phát triển', life: 3000 })
}

const exportCSV = () => {
  toast.add({ severity: 'info', summary: 'Chức năng', detail: 'Chức năng export đang được phát triển', life: 3000 })
}

const getStatusSeverity = (status) => {
  return status === 'active' ? 'success' : 'warning'
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-bottom: 1rem;
}
.form-section {
  margin-bottom: 1.5rem;
}
.form-section h4 {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  color: #333;
}
.confirmation-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}
:deep(.p-datatable .p-datatable-header) {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  padding: 1rem;
}
:deep(.p-datatable .p-datatable-thead > tr > th) {
  background: #f8fafc;
  color: #1e293b;
  font-weight: bold;
}
:deep(.p-datatable .p-datatable-tbody > tr > td) {
  padding: 1rem;
}
:deep(.p-datatable .p-datatable-tbody > tr:hover) {
  background: #f1f5f9;
}
</style>