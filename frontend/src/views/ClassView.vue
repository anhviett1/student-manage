<template>
  <div class="card">
    <div class="card-header">
      <h3 @click="navigateToHome">Lớp Học</h3>
      <div>
        <Button @click="loadActiveClasses" severity="primary" icon="pi pi-filter" label="Lớp Active" class="mr-2" />
        <Button @click="openNew" severity="success" icon="pi pi-plus" label="Thêm Lớp" />
      </div>
    </div>

    <DataTable
      :value="classes"
      :paginator="true"
      :rows="auto"
      :loading="loading"
      dataKey="class_id"
      :filters="filters"
      filterDisplay="menu"
      :globalFilterFields="['name', 'class_id', 'description']"
      responsiveLayout="stack"
    >
      <template #empty>
        <div class="text-center p-4">
          <p>Không tìm thấy lớp học nào.</p>
        </div>
      </template>

      <template #loading>
        <div class="text-center p-4">
          <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
        </div>
      </template>

      <Column field="class_id" header="Mã Lớp" sortable style="min-width: 10rem">
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            @input="filterCallback()"
            placeholder="Tìm theo mã lớp"
            class="p-column-filter"
          />
        </template>
      </Column>

      <Column field="name" header="Tên Lớp" sortable style="min-width: 14rem">
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            @input="filterCallback()"
            placeholder="Tìm theo tên lớp"
            class="p-column-filter"
          />
        </template>
      </Column>

      <Column field="department.department_id" header="Khoa" sortable style="min-width: 12rem">
        <template #body="{ data }">
          {{ data.department?.department_id || '-' }}
        </template>
      </Column>

      <Column field="credits" header="Tín Chỉ" sortable style="min-width: 10rem" />

      <Column field="semester.semester_id" header="Học Kỳ" sortable style="min-width: 12rem">
        <template #body="{ data }">
          {{ data.semester?.semester_id || '-' }}
        </template>
      </Column>

      <Column field="subject.subject_id" header="Môn Học" sortable style="min-width: 12rem">
        <template #body="{ data }">
          {{ data.subject?.subject_id || '-' }}
        </template>
      </Column>

      <Column field="status" header="Trạng Thái" sortable style="min-width: 10rem">
        <template #body="{ data }">
          <Tag :severity="getStatusSeverity(data.status)" :value="getStatusLabel(data.status)" />
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
          <Button icon="pi pi-pencil" outlined rounded class="mr-2" @click="editClass(data)" v-tooltip="'Chỉnh sửa lớp'" />
          <Button icon="pi pi-trash" outlined rounded severity="danger" @click="confirmDeleteClass(data)" v-tooltip="'Xóa mềm lớp'" />
          <Button icon="pi pi-eraser" outlined rounded severity="warning" @click="confirmHardDeleteClass(data)" v-tooltip="'Xóa hoàn toàn lớp'" />
          <Button icon="pi pi-refresh" outlined rounded @click="openChangeStatus(data)" v-tooltip="'Thay đổi trạng thái'" />
        </template>
      </Column>
    </DataTable>

    <Dialog v-model:visible="classDialog" :style="{ width: '600px' }" header="Thông Tin Lớp Học" :modal="true" class="p-fluid">
      <div class="form-section">
        <h4>Thông Tin Cơ Bản</h4>
        <div class="field">
          <label for="class_id">Mã Lớp</label>
          <InputText
            id="class_id"
            v-model.trim="classObj.class_id"
            :disabled="!!classObj.class_id"
            required
            autofocus
            :class="{ 'p-invalid': errors.class_id }"
          />
          <small class="p-error" v-if="errors.class_id">{{ errors.class_id }}</small>
        </div>
        <div class="field">
          <label for="name">Tên Lớp</label>
          <InputText
            id="name"
            v-model.trim="classObj.name"
            required
            :class="{ 'p-invalid': errors.name }"
          />
          <small class="p-error" v-if="errors.name">{{ errors.name }}</small>
        </div>
        <div class="field">
          <label for="description">Mô Tả</label>
          <Textarea id="description" v-model="classObj.description" rows="4" />
        </div>
        <div class="field">
          <label for="department">Khoa</label>
          <Dropdown
            id="department"
            v-model="classObj.department"
            :options="departments"
            optionLabel="department_id"
            optionValue="department_id"
            placeholder="Chọn khoa"
          />
        </div>
        <div class="field">
          <label for="credits">Số Tín Chỉ</label>
          <InputNumber
            id="credits"
            v-model="classObj.credits"
            :min="1"
            required
            :class="{ 'p-invalid': errors.credits }"
          />
          <small class="p-error" v-if="errors.credits">{{ errors.credits }}</small>
        </div>
        <div class="field">
          <label for="is_active">Đang Hoạt Động</label>
          <InputSwitch id="is_active" v-model="classObj.is_active" />
        </div>
      </div>

      <div class="form-section">
        <h4>Quan Hệ</h4>
        <div class="field">
          <label for="semester">Học Kỳ</label>
          <Dropdown
            id="semester"
            v-model="classObj.semester"
            :options="semesters"
            optionLabel="semester_id"
            optionValue="semester_id"
            placeholder="Chọn học kỳ"
            required
            :class="{ 'p-invalid': errors.semester }"
          />
          <small class="p-error" v-if="errors.semester">{{ errors.semester }}</small>
        </div>
        <div class="field">
          <label for="subject">Môn Học</label>
          <Dropdown
            id="subject"
            v-model="classObj.subject"
            :options="subjects"
            optionLabel="subject_id"
            optionValue="subject_id"
            placeholder="Chọn môn học"
            required
            :class="{ 'p-invalid': errors.subject }"
          />
          <small class="p-error" v-if="errors.subject">{{ errors.subject }}</small>
        </div>
        <div class="field">
          <label for="teacher">Giảng Viên</label>
          <Dropdown
            id="teacher"
            v-model="classObj.teacher"
            :options="teachers"
            optionLabel="teacher_id"
            optionValue="teacher_id"
            placeholder="Chọn giảng viên"
          />
        </div>
        <div class="field">
          <label for="teachers">Danh Sách Giảng Viên</label>
          <MultiSelect
            id="teachers"
            v-model="classObj.teachers"
            :options="teachers"
            optionLabel="teacher_id"
            optionValue="teacher_id"
            placeholder="Chọn giảng viên"
            display="chip"
          />
        </div>
        <div class="field">
          <label for="subjects">Danh Sách Môn Học</label>
          <MultiSelect
            id="subjects"
            v-model="classObj.subjects"
            :options="subjects"
            optionLabel="subject_id"
            optionValue="subject_id"
            placeholder="Chọn môn học"
            display="chip"
          />
        </div>
      </div>

      <div class="form-section">
        <h4>Trạng Thái</h4>
        <div class="field">
          <label for="status">Trạng Thái</label>
          <Dropdown
            id="status"
            v-model="classObj.status"
            :options="statusOptions"
            optionLabel="label"
            optionValue="value"
            placeholder="Chọn trạng thái"
            required
            :class="{ 'p-invalid': errors.status }"
          />
          <small class="p-error" v-if="errors.status">{{ errors.status }}</small>
        </div>
      </div>

      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="hideDialog" />
        <Button label="Lưu" icon="pi pi-check" @click="saveClass" />
      </template>
    </Dialog>

    <Dialog v-model:visible="deleteClassDialog" :style="{ width: '450px' }" header="Xác Nhận Xóa Mềm" :modal="true">
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span v-if="classObj">Bạn có chắc chắn muốn xóa mềm lớp <b>{{ classObj.name }}</b>?</span>
      </div>
      <template #footer>
        <Button label="Không" icon="pi pi-times" text @click="deleteClassDialog = false" />
        <Button label="Có" icon="pi pi-check" severity="danger" @click="deleteClass" />
      </template>
    </Dialog>

    <Dialog v-model:visible="hardDeleteClassDialog" :style="{ width: '450px' }" header="Xác Nhận Xóa Cứng" :modal="true">
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span v-if="classObj">Bạn có chắc chắn muốn xóa hoàn toàn lớp <b>{{ classObj.name }}</b>? Hành động này không thể hoàn tác.</span>
      </div>
      <template #footer>
        <Button label="Không" icon="pi pi-times" text @click="hardDeleteClassDialog = false" />
        <Button label="Có" icon="pi pi-check" severity="danger" @click="hardDeleteClass" />
      </template>
    </Dialog>

    <Dialog v-model:visible="changeStatusDialog" :style="{ width: '450px' }" header="Thay Đổi Trạng Thái" :modal="true">
      <div class="field">
        <label for="new_status">Trạng Thái Mới</label>
        <Dropdown
          id="new_status"
          v-model="newStatus"
          :options="statusOptions"
          optionLabel="label"
          optionValue="value"
          placeholder="Chọn trạng thái mới"
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
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import api from '@/services/api'
import { saveAs } from 'file-saver'

const toast = useToast()
const classes = ref([])
const semesters = ref([])
const subjects = ref([])
const teachers = ref([])
const departments = ref([])
const classDialog = ref(false)
const deleteClassDialog = ref(false)
const hardDeleteClassDialog = ref(false)
const changeStatusDialog = ref(false)
const classObj = ref({})
const newStatus = ref('')
const submitted = ref(false)
const loading = ref(true)
const errors = ref({})
const filters = ref({
  class_id: { value: null, matchMode: 'contains' },
  name: { value: null, matchMode: 'contains' },
  status: { value: null, matchMode: 'equals' }
})

const navigateToHome = () => {
  router.push('/')
}
    
const statusOptions = [
  { label: 'Đang hoạt động', value: 'active' },
  { label: 'Không hoạt động', value: 'inactive' },
  { label: 'Đang chờ duyệt', value: 'pending' }
]

onMounted(async () => {
  await Promise.all([
    loadClasses(),
    loadSemesters(),
    loadSubjects(),
    loadTeachers(),
    loadDepartments()
  ])
})

const loadClasses = async () => {
  try {
    loading.value = true
    const response = await api.get('/classes')
    classes.value = response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách lớp học', life: 3000 })
  } finally {
    loading.value = false
  }
}

const loadSemesters = async () => {
  try {
    const response = await api.get('/semesters')
    semesters.value = response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách học kỳ', life: 3000 })
  }
}

const loadSubjects = async () => {
  try {
    const response = await api.get('/subjects')
    subjects.value = response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách môn học', life: 3000 })
  }
}

const loadTeachers = async () => {
  try {
    const response = await api.get('/teachers')
    teachers.value = response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách giảng viên', life: 3000 })
  }
}

const loadDepartments = async () => {
  try {
    const response = await api.get('/departments')
    departments.value = response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách khoa', life: 3000 })
  }
}

const loadActiveClasses = async () => {
  try {
    loading.value = true
    const response = await api.get('/classes/active/')
    classes.value = response.data
    toast.add({ severity: 'info', summary: 'Thành công', detail: 'Hiển thị các lớp đang hoạt động', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải lớp đang hoạt động', life: 3000 })
  } finally {
    loading.value = false
  }
}

const openNew = () => {
  classObj.value = {
    status: 'active',
    is_active: true,
    credits: 3
  }
  errors.value = {}
  submitted.value = false
  classDialog.value = true
}

const hideDialog = () => {
  classDialog.value = false
  errors.value = {}
  submitted.value = false
}

const editClass = (data) => {
  classObj.value = { ...data }
  errors.value = {}
  submitted.value = false
  classDialog.value = true
}

const confirmDeleteClass = (data) => {
  classObj.value = data
  deleteClassDialog.value = true
}

const confirmHardDeleteClass = (data) => {
  classObj.value = data
  hardDeleteClassDialog.value = true
}

const openChangeStatus = (data) => {
  classObj.value = data
  newStatus.value = data.status
  submitted.value = false
  changeStatusDialog.value = true
}

const validateClass = () => {
  errors.value = {}
  if (!classObj.value.class_id?.trim()) errors.value.class_id = 'Vui lòng nhập mã lớp'
  if (!classObj.value.name?.trim()) errors.value.name = 'Vui lòng nhập tên lớp'
  if (!classObj.value.credits || classObj.value.credits < 1) errors.value.credits = 'Số tín chỉ phải lớn hơn 0'
  if (!classObj.value.semester) errors.value.semester = 'Vui lòng chọn học kỳ'
  if (!classObj.value.subject) errors.value.subject = 'Vui lòng chọn môn học'
  if (!classObj.value.status) errors.value.status = 'Vui lòng chọn trạng thái'
  if (classObj.value.status === 'active' && !classObj.value.is_active) {
    errors.value.is_active = 'Lớp đang hoạt động phải có trạng thái is_active là True'
  }
}

const saveClass = async () => {
  submitted.value = true
  validateClass()

  if (Object.keys(errors.value).length > 0) {
    return
  }

  try {
    const payload = {
      ...classObj.value,
      teachers: classObj.value.teachers || [],
      subjects: classObj.value.subjects || []
    }
    if (classObj.value.class_id) {
      const updatedClass = (await api.patch(`/classes/${classObj.value.class_id}/`, payload)).data
      classes.value = classes.value.map(c => c.class_id === updatedClass.class_id ? updatedClass : c)
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật lớp học thành công', life: 3000 })
    } else {
      const newClass = (await api.post('/classes/', payload)).data
      classes.value.push(newClass)
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Thêm lớp học thành công', life: 3000 })
    }
    classDialog.value = false
    classObj.value = {}
  } catch (error) {
    const errorMsg = error.response?.data?.detail || Object.values(error.response?.data || {}).join(', ') || 'Không thể lưu thông tin lớp học'
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errorMsg, life: 5000 })
  }
}

const deleteClass = async () => {
  try {
    await api.delete(`/classes/${classObj.value.class_id}/`)
    classes.value = classes.value.filter(c => c.class_id !== classObj.value.class_id)
    deleteClassDialog.value = false
    classObj.value = {}
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa mềm lớp học thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa lớp học', life: 3000 })
  }
}

const hardDeleteClass = async () => {
  try {
    await api.delete(`/classes/${classObj.value.class_id}/hard-delete/`)
    classes.value = classes.value.filter(c => c.class_id !== classObj.value.class_id)
    hardDeleteClassDialog.value = false
    classObj.value = {}
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa hoàn toàn lớp học thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa hoàn toàn lớp học', life: 3000 })
  }
}

const changeStatus = async () => {
  submitted.value = true
  if (!newStatus.value) {
    return
  }
  try {
    const updatedClass = (await api.post(`/classes/${classObj.value.class_id}/change-status/`, { status: newStatus.value })).data
    classes.value = classes.value.map(c => c.class_id === updatedClass.class_id ? updatedClass : c)
    changeStatusDialog.value = false
    classObj.value = {}
    newStatus.value = ''
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật trạng thái thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể cập nhật trạng thái', life: 3000 })
  }
}

const getStatusLabel = (status) => {
  const option = statusOptions.find(opt => opt.value === status)
  return option ? option.label : status
}

const getStatusSeverity = (status) => {
  switch (status) {
    case 'active':
      return 'success'
    case 'inactive':
      return 'warning'
    case 'pending':
      return 'info'
    default:
      return 'info'
  }
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.card-header h3 {
  margin: 0;
  font-size: 1.5rem;
  color: inherit;
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
