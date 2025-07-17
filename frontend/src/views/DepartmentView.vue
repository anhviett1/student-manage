<template>
  <div class="card" v-if="canViewDepartments">
    <Toast />
    <TabView>
      <!-- Tab 1: Thông Tin Khoa (cho trưởng khoa hoặc người dùng có quyền) -->
      <TabPanel header="Thông Tin Khoa" v-if="isHead || isAdmin">
        <div class="profile-section">
          <div class="profile-header">
            <h2>Thông Tin Khoa</h2>
            <Button icon="pi pi-pencil" label="Chỉnh Sửa" severity="primary" @click="openEdit" v-if="!isEditing && canEditDepartments" v-tooltip="'Chỉnh sửa thông tin khoa'" />
          </div>
          <div v-if="!isEditing" class="profile-details">
            <div class="detail-item"><label>Mã Khoa:</label><span>{{ departmentDetail.department_id }}</span></div>
            <div class="detail-item"><label>Tên Khoa:</label><span>{{ departmentDetail.department_name }}</span></div>
            <div class="detail-item"><label>Mô Tả:</label><span>{{ departmentDetail.description }}</span></div>
            <div class="detail-item"><label>Trưởng Khoa:</label><span>{{ departmentDetail.head?.full_name }}</span></div>
            <div class="detail-item"><label>Hoạt Động:</label><Tag :severity="departmentDetail.is_active ? 'success' : 'warning'" :value="departmentDetail.is_active ? 'Có' : 'Không'" /></div>
          </div>
          <div v-else class="edit-form">
            <div class="field">
              <label for="department_id">Mã Khoa</label>
              <InputText id="department_id" v-model="departmentDetail.department_id" disabled />
            </div>
            <div class="field">
              <label for="department_name">Tên Khoa</label>
              <InputText id="department_name" v-model="departmentDetail.department_name" :class="{ 'p-invalid': errors.department_name }" />
              <small class="p-error" v-if="errors.department_name">{{ errors.department_name }}</small>
            </div>
            <div class="field">
              <label for="description">Mô Tả</label>
              <Textarea id="description" v-model="departmentDetail.description" rows="4" />
            </div>
            <div class="field">
              <label for="head">Trưởng Khoa</label>
              <Dropdown id="head" v-model="departmentDetail.head" :options="users" optionLabel="full_name" optionValue="id" placeholder="Chọn trưởng khoa" />
            </div>
            <div class="field">
              <label for="is_active">Đang Hoạt Động</label>
              <InputSwitch id="is_active" v-model="departmentDetail.is_active" />
            </div>
            <div class="buttons">
              <Button label="Hủy" icon="pi pi-times" text @click="cancelEdit" />
              <Button label="Lưu" icon="pi pi-check" @click="saveDepartmentDetail" />
            </div>
          </div>
        </div>
      </TabPanel>
      <!-- Tab 2: Quản Lý Khoa (admin) -->
      <TabPanel header="Quản Lý Khoa" v-if="canViewDepartments">
        <div class="header">
          <h2>Quản Lý Khoa</h2>
          <div class="action-buttons">
            <Button v-if="canEditDepartments" icon="pi pi-plus" label="Thêm Khoa" severity="primary" class="mr-2" @click="openNew" v-tooltip="'Thêm khoa mới'" />
            <Button v-if="canExportDepartments" icon="pi pi-download" label="Export" severity="success" @click="exportDepartments" v-tooltip="'Xuất danh sách khoa'" />
            <Button icon="pi pi-filter" label="Khoa Active" severity="info" class="mr-2" @click="loadActiveDepartments" v-tooltip="'Lọc khoa đang hoạt động'" />
          </div>
        </div>
        <div class="filter-bar">
          <div class="filter-group">
            <Dropdown v-model="filters.status" :options="statusOptions" optionLabel="label" optionValue="value" placeholder="Lọc trạng thái" class="filter-dropdown mr-2" @change="loadDepartments" />
            <InputText v-model="filters.global" placeholder="Tìm tên, mô tả, trưởng khoa..." class="filter-search" @input="filterDepartments" />
          </div>
        </div>
        <DataTable v-if="(departments.length > 0 || loading) && canViewDepartments" :value="departments" :loading="loading" dataKey="department_id" :paginator="true" :rows="10" :rowsPerPageOptions="[5, 10, 20]" responsiveLayout="scroll" class="p-datatable-sm">
          <template #empty>
            <div class="empty-message"><i class="pi pi-info-circle" /><span>Không tìm thấy khoa nào.</span></div>
          </template>
          <template #loading>
            <div class="loading-message"><i class="pi pi-spin pi-spinner" /><span>Đang tải dữ liệu...</span></div>
          </template>
          <Column field="department_id" header="Mã Khoa" sortable style="width: 12%" />
          <Column field="department_name" header="Tên Khoa" sortable style="width: 18%" />
          <Column field="description" header="Mô Tả" sortable style="width: 18%" />
          <Column field="head.full_name" header="Trưởng Khoa" sortable style="width: 15%" />
          <Column field="is_active" header="Hoạt Động" sortable style="width: 10%" align="center">
            <template #body="{ data }">
              <Tag :severity="data.is_active ? 'success' : 'warning'" :value="data.is_active ? 'Có' : 'Không'" />
            </template>
          </Column>
          <Column header="Hành Động" style="width: 15%" align="center">
            <template #body="{ data }">
              <Button v-if="canEditDepartments && !data.is_deleted" icon="pi pi-pencil" outlined rounded class="mr-2" severity="info" @click="editDepartment(data)" v-tooltip="'Sửa thông tin'"/>
              <Button v-if="canDeleteDepartments && !data.is_deleted" icon="pi pi-trash" outlined rounded severity="danger" class="mr-2" @click="confirmDelete(data)" v-tooltip="'Xóa mềm'" />
              <Button v-if="canDeleteDepartments && data.is_deleted" icon="pi pi-undo" outlined rounded severity="success" @click="restoreDepartment(data)" v-tooltip="'Khôi phục'"/>
            </template>
          </Column>
        </DataTable>
        <div v-else-if="!loading && departments.length === 0 && canViewDepartments" class="no-data-message">
          <p>Không có dữ liệu khoa để hiển thị.</p>
          <Button label="Tải lại" icon="pi pi-refresh" @click="loadDepartments" severity="secondary" />
        </div>
        <!-- Dialog thêm/sửa khoa -->
        <Dialog v-model:visible="departmentDialog" :header="departmentObj.department_id ? 'Sửa Khoa' : 'Thêm Khoa'" :style="{ width: '600px' }" :modal="true" class="p-fluid">
          <div class="form-section">
            <h4>Thông Tin Cơ Bản</h4>
            <div class="field">
              <label for="department_id">Mã Khoa</label>
              <InputText id="department_id" v-model="departmentObj.department_id" :class="{ 'p-invalid': errors.department_id }" :disabled="!!departmentObj.department_id" />
              <small class="p-error" v-if="errors.department_id">{{ errors.department_id }}</small>
            </div>
            <div class="field">
              <label for="department_name">Tên Khoa</label>
              <InputText id="department_name" v-model="departmentObj.department_name" :class="{ 'p-invalid': errors.department_name }" />
              <small class="p-error" v-if="errors.department_name">{{ errors.department_name }}</small>
            </div>
            <div class="field">
              <label for="description">Mô Tả</label>
              <Textarea id="description" v-model="departmentObj.description" rows="4" />
            </div>
            <div class="field">
              <label for="head">Trưởng Khoa</label>
              <Dropdown id="head" v-model="departmentObj.head" :options="users" optionLabel="full_name" optionValue="id" placeholder="Chọn trưởng khoa" />
            </div>
            <div class="field">
              <label for="is_active">Đang Hoạt Động</label>
              <InputSwitch id="is_active" v-model="departmentObj.is_active" />
            </div>
          </div>
          <template #footer>
            <Button label="Hủy" icon="pi pi-times" text @click="hideDialog" />
            <Button label="Lưu" icon="pi pi-check" @click="saveDepartment" />
          </template>
        </Dialog>
        <!-- Dialog xác nhận xóa mềm -->
        <Dialog v-model:visible="deleteDepartmentDialog" header="Xác Nhận Xóa Mềm" :style="{ width: '400px' }" :modal="true">
          <div class="confirmation-content">
            <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
            <span>Bạn có chắc muốn xóa khoa <b>{{ departmentObj.department_name }}</b>?</span>
          </div>
          <template #footer>
            <Button label="Hủy" icon="pi pi-times" text @click="deleteDepartmentDialog = false" />
            <Button label="Xóa" icon="pi pi-check" severity="danger" @click="deleteDepartment" />
          </template>
        </Dialog>
        <!-- Dialog xác nhận khôi phục -->
        <Dialog v-model:visible="restoreDepartmentDialog" header="Xác Nhận Khôi Phục" :style="{ width: '400px' }" :modal="true">
          <div class="confirmation-content">
            <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
            <span>Bạn có chắc muốn khôi phục khoa <b>{{ departmentObj.department_name }}</b>?</span>
          </div>
          <template #footer>
            <Button label="Hủy" icon="pi pi-times" text @click="restoreDepartmentDialog = false" />
            <Button label="Khôi phục" icon="pi pi-check" severity="success" @click="restoreDepartment" />
          </template>
        </Dialog>
      </TabPanel>
    </TabView>
  </div>
  <div v-else class="access-denied">
    <p>Bạn không có quyền truy cập trang này.</p>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import api, { endpoints } from '@/services/api'
import { saveAs } from 'file-saver'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import Tag from 'primevue/tag'
import InputSwitch from 'primevue/inputswitch'

const toast = useToast()
const isHead = computed(() => false) 

const departments = ref([])
const departmentObj = ref({})
const departmentDetail = ref({})
const departmentDialog = ref(false)
const deleteDepartmentDialog = ref(false)
const restoreDepartmentDialog = ref(false)
const isEditing = ref(false)
const loading = ref(false)
const errors = ref({})
const users = ref([])
const filters = reactive({
  global: '',
  status: 'active',
})
const statusOptions = [
  { label: 'Đang hoạt động', value: 'active' },
  { label: 'Không hoạt động', value: 'inactive' }
]

onMounted(async () => {
  await Promise.all([
    loadDepartments(),
    loadUsers()
  ])
  if (isHead.value || isAdmin.value) {
    if (departments.value.length > 0) {
      departmentDetail.value = { ...departments.value[0] }
    }
  }
})

const loadDepartments = async () => {
  if (!canViewDepartments.value) return
  try {
    loading.value = true
    const params = {}
    if (filters.status) params.is_active = filters.status === 'active'
    if (filters.global) params.search = filters.global
    const response = await api.get(endpoints.departments, { params })
    if (Array.isArray(response.data)) {
      departments.value = response.data
    } else if (response.data && response.data.results && Array.isArray(response.data.results)) {
      departments.value = response.data.results
    } else {
      departments.value = []
    }
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách khoa', life: 3000 })
    departments.value = []
  } finally {
    loading.value = false
  }
}

const filterDepartments = () => {
  loadDepartments()
}

const loadUsers = async () => {
  try {
    const response = await api.get(endpoints.users, { params: { role: 'department_head,admin' } })
    if (Array.isArray(response.data)) {
      users.value = response.data
    } else if (response.data && response.data.results && Array.isArray(response.data.results)) {
      users.value = response.data.results
    } else {
      users.value = []
    }
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách người dùng', life: 3000 })
    users.value = []
  }
}

const loadActiveDepartments = async () => {
  try {
    loading.value = true
    const response = await api.get(endpoints.departments, { params: { is_active: true } })
    if (Array.isArray(response.data)) {
      departments.value = response.data
    } else if (response.data && response.data.results && Array.isArray(response.data.results)) {
      departments.value = response.data.results
    } else {
      departments.value = []
    }
    toast.add({ severity: 'info', summary: 'Thành công', detail: 'Hiển thị các khoa đang hoạt động', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải khoa đang hoạt động', life: 3000 })
  } finally {
    loading.value = false
  }
}

const openNew = () => {
  departmentObj.value = { is_active: true }
  errors.value = {}
  departmentDialog.value = true
}

const hideDialog = () => {
  departmentDialog.value = false
  errors.value = {}
}

const editDepartment = (data) => {
  departmentObj.value = { ...data }
  errors.value = {}
  departmentDialog.value = true
}

const confirmDelete = (data) => {
  departmentObj.value = { ...data }
  deleteDepartmentDialog.value = true
}

const restoreDepartment = async () => {
  try {
    const response = await api.post(`${endpoints.departments}${departmentObj.value.department_id}/restore/`)
    departments.value = departments.value.map(d => d.department_id === departmentObj.value.department_id ? response.data : d)
    restoreDepartmentDialog.value = false
    departmentObj.value = {}
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Khôi phục khoa thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể khôi phục khoa', life: 3000 })
  }
}

const validateDepartment = () => {
  errors.value = {}
  if (!departmentObj.value.department_id?.trim()) errors.value.department_id = 'Vui lòng nhập mã khoa'
  if (!departmentObj.value.department_name?.trim()) errors.value.department_name = 'Vui lòng nhập tên khoa'
}

const saveDepartment = async () => {
  validateDepartment()
  if (Object.keys(errors.value).length > 0) return
  try {
    const payload = { ...departmentObj.value }
    if (departmentObj.value.department_id) {
      const updatedDepartment = (await api.patch(`${endpoints.departments}${departmentObj.value.department_id}/`, payload)).data
      departments.value = departments.value.map(d => d.department_id === updatedDepartment.department_id ? updatedDepartment : d)
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật khoa thành công', life: 3000 })
    } else {
      const newDepartment = (await api.post(endpoints.departments, payload)).data
      departments.value.push(newDepartment)
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Thêm khoa thành công', life: 3000 })
    }
    departmentDialog.value = false
    departmentObj.value = {}
  } catch (error) {
    const errorMsg = error.response?.data?.detail || Object.values(error.response?.data || {}).join(', ') || 'Không thể lưu thông tin khoa'
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errorMsg, life: 5000 })
  }
}

const deleteDepartment = async () => {
  try {
    await api.delete(`${endpoints.departments}${departmentObj.value.department_id}/`)
    departments.value = departments.value.filter(d => d.department_id !== departmentObj.value.department_id)
    deleteDepartmentDialog.value = false
    departmentObj.value = {}
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa mềm khoa thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa khoa', life: 3000 })
  }
}

const openEdit = () => {
  isEditing.value = true
  errors.value = {}
}

const cancelEdit = () => {
  isEditing.value = false
  // reload lại departmentDetail nếu cần
}

const saveDepartmentDetail = async () => {
  try {
    isEditing.value = false
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật thông tin khoa thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể cập nhật thông tin khoa', life: 3000 })
  }
}

const exportDepartments = async () => {
  try {
    const response = await api.get(`${endpoints.departments}export/`, { responseType: 'blob' })
    const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    saveAs(blob, `departments_${new Date().toISOString().split('T')[0]}.xlsx`)
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xuất danh sách khoa thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xuất danh sách khoa', life: 3000 })
  }
}
</script>

<style scoped>
.card, .content {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(44, 62, 80, 0.08);
  padding: 2rem;
  margin-bottom: 2rem;
}
.header, .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}
.header h2, .card-header h3 {
  font-size: 1.6rem;
  color: #2c3e50;
  margin: 0;
  font-weight: 700;
}
.action-buttons {
  display: flex;
  gap: 0.75rem;
}
.filter-bar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
  flex-wrap: wrap;
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
.empty-message, .loading-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 2rem;
  color: #666;
  font-size: 1.1rem;
}
@media (max-width: 768px) {
  .card, .content {
    padding: 1rem;
  }
  .header h2, .card-header h3 {
    font-size: 1.2rem;
  }
  .filter-search, .filter-dropdown {
    width: 100%;
  }
}
.profile-section {
  max-width: 800px;
  margin: 0 auto;
}
.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}
.profile-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}
.detail-item {
  padding: 0.5rem;
}
.detail-item label {
  font-weight: bold;
  margin-right: 0.5rem;
}
.edit-form {
  display: grid;
  gap: 1rem;
}
.field {
  display: flex;
  flex-direction: column;
}
.buttons {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}
.confirmation-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.access-denied {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #ef4444;
}
.no-data-message {
  text-align: center;
  padding: 3rem;
  color: #666;
  background: #f8f9fa;
  border-radius: 8px;
  margin: 1rem 0;
}
.no-data-message p {
  margin-bottom: 1rem;
  font-size: 1.1rem;
}
.action-buttons, .p-datatable-sm :deep(td .p-button) {
  gap: 0.25rem !important;
}
.p-datatable-sm :deep(td .p-button) {
  min-width: 28px !important;
  height: 28px !important;
  width: 28px !important;
  padding: 0 !important;
  font-size: 0.9rem !important;
  border-radius: 50% !important;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.25rem !important;
}
.p-datatable-sm :deep(td .p-button:last-child) {
  margin-right: 0 !important;
}
.p-datatable-sm :deep(td .p-button .pi) {
  font-size: 0.9rem !important;
}
.p-datatable-sm :deep(td .p-button:hover) {
  box-shadow: 0 0 0 2px #c7d2fe;
}
.p-datatable-sm :deep(td .p-button + .p-button) {
  margin-left: 0.15rem !important;
}
.p-tag {
  font-size: 0.95em;
  padding: 0.2em 0.7em;
}
.p-datatable-sm :deep(.p-datatable-tbody > tr > td),
.p-datatable-sm :deep(.p-datatable-thead > tr > th) {
  padding: 0.85rem 1.1rem;
}
.p-datatable-sm :deep(.p-datatable-thead > tr > th) {
  background: #f8f9fa;
  font-size: 1rem;
  border-right: 1px solid #f1f1f1;
}
.p-datatable-sm :deep(.p-datatable-tbody > tr > td) {
  border-right: 1px solid #f4f4f4;
}
.p-datatable-sm :deep(.p-datatable-tbody > tr > td:last-child),
.p-datatable-sm :deep(.p-datatable-thead > tr > th:last-child) {
  border-right: none;
}
@media (max-width: 768px) {
  .p-datatable-sm :deep(td .p-button) {
    min-width: 24px !important;
    height: 24px !important;
    width: 24px !important;
    font-size: 0.8rem !important;
  }
  .p-datatable-sm :deep(td),
  .p-datatable-sm :deep(th) {
    padding: 0.5em 0.4em;
  }
}
</style>