<template>
  <div class="card">
    <Toast />
    <div class="header">
      <h2>Quản Lý Môn Học</h2>
      <div class="action-buttons">
        <Button
          icon="pi pi-plus"
          label="Thêm Môn Học"
          severity="primary"
          class="mr-2"
          @click="openNew"
          v-tooltip="'Thêm môn học mới'"
        />
        <Button
          icon="pi pi-download"
          label="Export"
          severity="success"
          @click="exportSubjects"
          v-tooltip="'Xuất danh sách môn học'"
        />
      </div>
    </div>

    <div class="filter-bar">
      <div class="filter-group">
        <Dropdown
          v-model="filters.status"
          :options="statusOptions"
          optionLabel="label"
          optionValue="value"
          placeholder="Lọc trạng thái"
          class="filter-dropdown mr-2"
          @change="loadSubjects"
        />
        <Dropdown
          v-model="filters.department"
          :options="departments"
          optionLabel="name"
          optionValue="id"
          placeholder="Lọc khoa"
          class="filter-dropdown mr-2"
          @change="loadSubjects"
        />
        <InputText
          v-model="filters.global"
          placeholder="Tìm mã, tên môn học..."
          class="filter-search"
          @input="filterSubjects"
        />
      </div>
    </div>

    <DataTable
      :value="subjects"
      :loading="loading"
      dataKey="subject_id"
      :paginator="true"
      :rows="10"
      :rowsPerPageOptions="[5, 10, 20]"
      responsiveLayout="scroll"
      class="p-datatable-sm"
    >
      <template #empty>
        <div class="empty-message">
          <i class="pi pi-info-circle" />
          <span>Không tìm thấy môn học nào.</span>
        </div>
      </template>
      <template #loading>
        <div class="loading-message">
          <i class="pi pi-spin pi-spinner" />
          <span>Đang tải dữ liệu...</span>
        </div>
      </template>
      <Column field="subject_id" header="Mã Môn Học" sortable style="width: 15%" />
      <Column field="name" header="Tên Môn Học" sortable style="width: 25%" />
      <Column field="credits" header="Số Tín Chỉ" sortable style="width: 10%" align="center" />
      <Column field="semester.name" header="Học Kỳ" sortable style="width: 15%" />
      <Column field="department.name" header="Khoa" sortable style="width: 15%" />
      <Column field="status" header="Trạng Thái" sortable style="width: 10%" align="center">
        <template #body="{ data }">
          <Tag :severity="getStatusSeverity(data.status)" :value="getStatusLabel(data.status)" />
        </template>
      </Column>
      <Column field="is_active" header="Hoạt Động" sortable style="width: 10%" align="center">
        <template #body="{ data }">
          <Tag :severity="data.is_active ? 'success' : 'warning'" :value="data.is_active ? 'Active' : 'Inactive'" />
        </template>
      </Column>
      <Column header="Hành Động" style="width: 15%" align="center">
        <template #body="{ data }">
          <Button
            icon="pi pi-pencil"
            outlined
            rounded
            class="mr-2"
            severity="info"
            @click="editSubject(data)"
            v-if="!data.is_deleted"
            v-tooltip="'Sửa thông tin'"
          />
          <Button
            icon="pi pi-trash"
            outlined
            rounded
            severity="danger"
            class="mr-2"
            @click="confirmDelete(data)"
            v-if="!data.is_deleted"
            v-tooltip="'Xóa mềm'"
          />
          <Button
            icon="pi pi-undo"
            outlined
            rounded
            severity="success"
            @click="restoreSubject(data)"
            v-if="data.is_deleted"
            v-tooltip="'Khôi phục'"
          />
          <Button
            icon="pi pi-refresh"
            outlined
            rounded
            severity="secondary"
            @click="openChangeStatus(data)"
            v-tooltip="'Thay đổi trạng thái'"
          />
        </template>
      </Column>
    </DataTable>

    <!-- Dialog for Adding/Editing Subject -->
    <Dialog
      v-model:visible="subjectDialog"
      :header="subject.subject_id ? 'Sửa Môn Học' : 'Thêm Môn Học'"
      :style="{ width: '500px' }"
      :modal="true"
      class="p-fluid"
    >
      <div class="form-section">
        <div class="field">
          <label for="subject_id">Mã Môn Học</label>
          <InputText id="subject_id" v-model="subject.subject_id" :class="{ 'p-invalid': errors.subject_id }" :disabled="!!subject.subject_id" />
          <small class="p-error" v-if="errors.subject_id">{{ errors.subject_id }}</small>
        </div>
        <div class="field">
          <label for="name">Tên Môn Học</label>
          <InputText id="name" v-model="subject.name" :class="{ 'p-invalid': errors.name }" />
          <small class="p-error" v-if="errors.name">{{ errors.name }}</small>
        </div>
        <div class="field">
          <label for="description">Mô Tả</label>
          <Textarea id="description" v-model="subject.description" rows="4" />
        </div>
        <div class="field">
          <label for="credits">Số Tín Chỉ</label>
          <InputNumber id="credits" v-model="subject.credits" :min="1" :max="10" :class="{ 'p-invalid': errors.credits }" />
          <small class="p-error" v-if="errors.credits">{{ errors.credits }}</small>
        </div>
        <div class="field">
          <label for="semester">Học Kỳ</label>
          <Dropdown id="semester" v-model="subject.semester_id" :options="semesters" optionLabel="name" optionValue="id" placeholder="Chọn học kỳ" :class="{ 'p-invalid': errors.semester_id }" />
          <small class="p-error" v-if="errors.semester_id">{{ errors.semester_id }}</small>
        </div>
        <div class="field">
          <label for="department">Khoa</label>
          <Dropdown id="department" v-model="subject.department_id" :options="departments" optionLabel="name" optionValue="id" placeholder="Chọn khoa" :class="{ 'p-invalid': errors.department_id }" />
          <small class="p-error" v-if="errors.department_id">{{ errors.department_id }}</small>
        </div>
        <div class="field">
          <label for="status">Trạng Thái</label>
          <Dropdown id="status" v-model="subject.status" :options="statusOptions" optionLabel="label" optionValue="value" :class="{ 'p-invalid': errors.status }" />
          <small class="p-error" v-if="errors.status">{{ errors.status }}</small>
        </div>
        <div class="field-checkbox">
          <Checkbox id="is_active" v-model="subject.is_active" :binary="true" />
          <label for="is_active" class="ml-2">Đang Hoạt Động</label>
        </div>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="hideDialog" />
        <Button label="Lưu" icon="pi pi-check" @click="saveSubject" />
      </template>
    </Dialog>

    <!-- Delete Confirmation Dialog -->
    <Dialog
      v-model:visible="deleteDialog"
      header="Xác Nhận Xóa"
      :style="{ width: '400px' }"
      :modal="true"
    >
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span>Bạn có chắc muốn xóa môn học <b>{{ subject.name }}</b>?</span>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="deleteDialog = false" />
        <Button label="Xóa" icon="pi pi-check" severity="danger" @click="deleteSubject" />
      </template>
    </Dialog>

    <!-- Change Status Dialog -->
    <Dialog
      v-model:visible="changeStatusDialog"
      header="Thay Đổi Trạng Thái"
      :style="{ width: '400px' }"
      :modal="true"
    >
      <div class="field">
        <label for="new_status">Trạng Thái Mới</label>
        <Dropdown
          id="new_status"
          v-model="newStatus"
          :options="statusOptions"
          optionLabel="label"
          optionValue="value"
          placeholder="Chọn trạng thái"
          :class="{ 'p-invalid': submitted && !newStatus }"
        />
        <small class="p-error" v-if="submitted && !newStatus">Vui lòng chọn trạng thái mới.</small>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="changeStatusDialog = false" />
        <Button label="Cập Nhật" icon="pi pi-check" @click="changeStatus" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import api from '@/api'

const toast = useToast()
const subjects = ref([])
const departments = ref([])
const semesters = ref([])
const subject = ref({})
const loading = ref(false)
const subjectDialog = ref(false)
const deleteDialog = ref(false)
const changeStatusDialog = ref(false)
const errors = ref({})
const newStatus = ref('')
const submitted = ref(false)
const filters = ref({
  status: null,
  department: null,
  global: '',
})

const statusOptions = [
  { label: 'Đang hoạt động', value: 'active' },
  { label: 'Không hoạt động', value: 'inactive' },
  { label: 'Đang chờ duyệt', value: 'pending' },
]

onMounted(async () => {
  await Promise.all([loadDepartments(), loadSemesters(), loadSubjects()])
})

const loadDepartments = async () => {
  try {
    const response = await api.get('/api/v1/departments/')
    departments.value = response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách khoa', life: 3000 })
  }
}

const loadSemesters = async () => {
  try {
    const response = await api.get('/api/v1/semesters/')
    semesters.value = response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách học kỳ', life: 3000 })
  }
}

const loadSubjects = async () => {
  try {
    loading.value = true
    let url = '/api/v1/subjects/'
    const params = {}
    if (filters.value.status) params.status = filters.value.status
    if (filters.value.department) params.department__id = filters.value.department
    if (filters.value.global) params.search = filters.value.global
    const response = await api.get(url, { params })
    subjects.value = response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách môn học', life: 3000 })
  } finally {
    loading.value = false
  }
}

const filterSubjects = () => {
  loadSubjects()
}

const openNew = () => {
  subject.value = {
    status: 'pending',
    is_active: true,
    credits: 3,
    department_id: null,
    semester_id: null,
  }
  errors.value = {}
  subjectDialog.value = true
}

const editSubject = (data) => {
  subject.value = {
    ...data,
    department_id: data.department ? data.department.id : null,
    semester_id: data.semester ? data.semester.id : null,
  }
  errors.value = {}
  subjectDialog.value = true
}

const hideDialog = () => {
  subjectDialog.value = false
  subject.value = {}
  errors.value = {}
}

const confirmDelete = (data) => {
  subject.value = data
  deleteDialog.value = true
}

const openChangeStatus = (data) => {
  subject.value = data
  newStatus.value = data.status
  submitted.value = false
  changeStatusDialog.value = true
}

const validateSubject = () => {
  errors.value = {}
  if (!subject.value.subject_id) errors.value.subject_id = 'Vui lòng nhập mã môn học'
  if (!subject.value.subject_id.startsWith('MH')) errors.value.subject_id = 'Mã môn học phải bắt đầu bằng "MH"'
  if (!subject.value.name) errors.value.name = 'Vui lòng nhập tên môn học'
  if (subject.value.name && (subject.value.name.length < 3 || subject.value.name.length > 200)) {
    errors.value.name = 'Tên môn học phải từ 3 đến 200 ký tự'
  }
  if (!subject.value.credits) errors.value.credits = 'Vui lòng nhập số tín chỉ'
  if (subject.value.credits < 1 || subject.value.credits > 10) errors.value.credits = 'Số tín chỉ phải từ 1 đến 10'
  if (!subject.value.department_id) errors.value.department_id = 'Vui lòng chọn khoa'
  if (!subject.value.status) errors.value.status = 'Vui lòng chọn trạng thái'
  if (subject.value.status === 'inactive' && subject.value.is_active) {
    errors.value.is_active = 'Môn học không hoạt động không thể ở trạng thái đang hoạt động'
  }
}

const saveSubject = async () => {
  validateSubject()
  if (Object.keys(errors.value).length > 0) return

  try {
    const payload = { ...subject.value }
    if (subject.value.subject_id) {
      const response = await api.patch(`/api/v1/subjects/${subject.value.subject_id}/`, payload)
      subjects.value = subjects.value.map(s => s.subject_id === subject.value.subject_id ? response.data : s)
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật môn học thành công', life: 3000 })
    } else {
      const response = await api.post('/api/v1/subjects/', payload)
      subjects.value.push(response.data)
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Thêm môn học thành công', life: 3000 })
    }
    hideDialog()
  } catch (error) {
    const errorMsg = error.response?.data?.detail || Object.values(error.response?.data || {}).join(', ') || 'Không thể lưu môn học'
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errorMsg, life: 3000 })
  }
}

const deleteSubject = async () => {
  try {
    await api.delete(`/api/v1/subjects/${subject.value.subject_id}/`)
    subjects.value = subjects.value.filter(s => s.subject_id !== subject.value.subject_id)
    deleteDialog.value = false
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa môn học thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa môn học', life: 3000 })
  }
}

const restoreSubject = async (data) => {
  try {
    const response = await api.post(`/api/v1/subjects/${data.subject_id}/restore/`)
    subjects.value = subjects.value.map(s => s.subject_id === data.subject_id ? response.data.data : s)
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Khôi phục môn học thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: error.response?.data?.error || 'Không thể khôi phục môn học', life: 3000 })
  }
}

const changeStatus = async () => {
  submitted.value = true
  if (!newStatus.value) return

  try {
    const response = await api.post(`/api/v1/subjects/${subject.value.subject_id}/change_status/`, { status: newStatus.value })
    subjects.value = subjects.value.map(s => s.subject_id === subject.value.subject_id ? response.data.data : s)
    changeStatusDialog.value = false
    newStatus.value = ''
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật trạng thái thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể cập nhật trạng thái', life: 3000 })
  }
}

const exportSubjects = async () => {
  try {
    const response = await api.get('/api/v1/subjects/export', { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `subjects_${new Date().toISOString().split('T')[0]}.xlsx`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xuất danh sách môn học thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xuất danh sách môn học', life: 3000 })
  }
}

const getStatusLabel = (status) => {
  const option = statusOptions.find(opt => opt.value === status)
  return option ? option.label : status
}

const getStatusSeverity = (status) => {
  switch (status) {
    case 'active': return 'success'
    case 'inactive': return 'warning'
    case 'pending': return 'info'
    default: return 'info'
  }
}
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

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.empty-message, .loading-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 2rem;
  color: #666;
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

.form-section {
  margin-bottom: 1.5rem;
}

.field {
  margin-bottom: 1.2rem;
}

.field label {
  display: block;
  margin-bottom: 0.3rem;
  font-weight: bold;
}

.field-checkbox {
  display: flex;
  align-items: center;
  margin-bottom: 1.2rem;
}

.confirmation-content {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
}
</style>