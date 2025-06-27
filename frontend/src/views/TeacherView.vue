<template>
  <div class="card" v-if="isTeacher || isAdmin">
    <Toast />
    <TabView>
      <!-- Tab for Teachers -->
      <TabPanel header="Thông Tin Cá Nhân" v-if="isTeacher">
        <div class="profile-section">
          <div class="profile-header">
            <h2 @click="navigateToHome">Thông Tin Giảng Viên</h2>
            <Button
              icon="pi pi-pencil"
              label="Chỉnh Sửa"
              severity="primary"
              @click="openEdit"
              v-if="!isEditing"
              v-tooltip="'Chỉnh sửa thông tin cá nhân'"
            />
          </div>
          <div v-if="!isEditing" class="profile-details">
            <div class="detail-item">
              <label>Mã Giảng Viên:</label>
              <span>{{ teacher.teacher_id }}</span>
            </div>
            <div class="detail-item">
              <label>Họ và Tên:</label>
              <span>{{ teacher.full_name }}</span>
            </div>
            <div class="detail-item">
              <label>Email:</label>
              <span>{{ teacher.email }}</span>
            </div>
            <div class="detail-item">
              <label>Số Điện Thoại:</label>
              <span>{{ teacher.phone }}</span>
            </div>
            <div class="detail-item">
              <label>Ngày Sinh:</label>
              <span>{{ formatDate(teacher.date_of_birth) }}</span>
            </div>
            <div class="detail-item">
              <label>Giới Tính:</label>
              <span>{{ getGenderLabel(teacher.gender) }}</span>
            </div>
            <div class="detail-item">
              <label>Địa Chỉ:</label>
              <span>{{ teacher.address }}</span>
            </div>
            <div class="detail-item">
              <label>Học Vị:</label>
              <span>{{ getDegreeLabel(teacher.degree) }}</span>
            </div>
            <div class="detail-item">
              <label>Chuyên Ngành:</label>
              <span>{{ teacher.specialization }}</span>
            </div>
            <div class="detail-item">
              <label>Trạng Thái:</label>
              <Tag :severity="getStatusSeverity(teacher.status)" :value="getStatusLabel(teacher.status)" />
            </div>
          </div>
          <div v-else class="edit-form">
            <div class="field">
              <label for="teacher_id">Mã Giảng Viên</label>
              <InputText id="teacher_id" v-model="teacher.teacher_id" disabled />
            </div>
            <div class="field">
              <label for="first_name">Tên</label>
              <InputText id="first_name" v-model="teacher.first_name" :class="{ 'p-invalid': errors.first_name }" />
              <small class="p-error" v-if="errors.first_name">{{ errors.first_name }}</small>
            </div>
            <div class="field">
              <label for="last_name">Họ</label>
              <InputText id="last_name" v-model="teacher.last_name" :class="{ 'p-invalid': errors.last_name }" />
              <small class="p-error" v-if="errors.last_name">{{ errors.last_name }}</small>
            </div>
            <div class="field">
              <label for="email">Email</label>
              <InputText id="email" v-model="teacher.email" :class="{ 'p-invalid': errors.email }" />
              <small class="p-error" v-if="errors.email">{{ errors.email }}</small>
            </div>
            <div class="field">
              <label for="phone">Số Điện Thoại</label>
              <InputText id="phone" v-model="teacher.phone" :class="{ 'p-invalid': errors.phone }" />
              <small class="p-error" v-if="errors.phone">{{ errors.phone }}</small>
            </div>
            <div class="field">
              <label for="date_of_birth">Ngày Sinh</label>
              <Calendar id="date_of_birth" v-model="teacher.date_of_birth" :showIcon="true" dateFormat="yy-mm-dd" :class="{ 'p-invalid': errors.date_of_birth }" />
              <small class="p-error" v-if="errors.date_of_birth">{{ errors.date_of_birth }}</small>
            </div>
            <div class="field">
              <label for="gender">Giới Tính</label>
              <Dropdown id="gender" v-model="teacher.gender" :options="genderOptions" optionLabel="label" optionValue="value" :class="{ 'p-invalid': errors.gender }" />
              <small class="p-error" v-if="errors.gender">{{ errors.gender }}</small>
            </div>
            <div class="field">
              <label for="address">Địa Chỉ</label>
              <Textarea id="address" v-model="teacher.address" rows="3" :class="{ 'p-invalid': errors.address }" />
              <small class="p-error" v-if="errors.address">{{ errors.address }}</small>
            </div>
            <div class="buttons">
              <Button label="Hủy" icon="pi pi-times" text @click="cancelEdit" />
              <Button label="Lưu" icon="pi pi-check" @click="saveTeacher" />
            </div>
          </div>
        </div>
      </TabPanel>

      <!-- Tab for Admins -->
      <TabPanel header="Quản Lý Giảng Viên" v-if="isAdmin">
        <div class="header">
          <h2>Quản Lý Giảng Viên</h2>
          <div class="action-buttons">
            <Button
              v-if="canEditTeachers"
              icon="pi pi-plus"
              label="Thêm Giảng Viên"
              severity="primary"
              class="mr-2"
              @click="openNew"
              v-tooltip="'Thêm giảng viên mới'"
            />
            <Button
              v-if="canExportData"
              icon="pi pi-download"
              label="Export"
              severity="success"
              @click="exportTeachers"
              v-tooltip="'Xuất danh sách giảng viên'"
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
              @change="loadTeachers"
            />
            <Dropdown
              v-model="filters.department"
              :options="departments"
              optionLabel="name"
              optionValue="id"
              placeholder="Lọc khoa"
              class="filter-dropdown mr-2"
              @change="loadTeachers"
            />
            <InputText
              v-model="filters.global"
              placeholder="Tìm mã, tên, email..."
              class="filter-search"
              @input="filterTeachers"
            />
          </div>
        </div>

        <DataTable
          v-if="canViewTeachers"
          :value="teachers"
          :loading="loading"
          dataKey="teacher_id"
          :paginator="true"
          :rows="10"
          :rowsPerPageOptions="[5, 10, 20]"
          responsiveLayout="scroll"
          class="p-datatable-sm"
        >
          <template #empty>
            <div class="empty-message">
              <i class="pi pi-info-circle" />
              <span>Không tìm thấy giảng viên nào.</span>
            </div>
          </template>
          <template #loading>
            <div class="loading-message">
              <i class="pi pi-spin pi-spinner" />
              <span>Đang tải dữ liệu...</span>
            </div>
          </template>
          <Column field="teacher_id" header="Mã Giảng Viên" sortable style="width: 12%" />
          <Column field="full_name" header="Họ và Tên" sortable style="width: 18%" />
          <Column field="email" header="Email" sortable style="width: 18%" />
          <Column field="specialization" header="Chuyên Ngành" sortable style="width: 15%" />
          <Column field="degree" header="Học Vị" sortable style="width: 10%" align="center">
            <template #body="{ data }">
              <span>{{ getDegreeLabel(data.degree) }}</span>
            </template>
          </Column>
          <Column field="status" header="Trạng Thái" sortable style="width: 12%" align="center">
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
                v-if="canEditTeachers && !data.is_deleted"
                icon="pi pi-pencil"
                outlined
                rounded
                severity="info"
                @click="editTeacher(data)"
                v-tooltip="'Sửa thông tin'"
              />
              <Button
                v-if="canDeleteTeachers && !data.is_deleted"
                icon="pi pi-trash"
                outlined
                rounded
                severity="danger"
                class="mr-2"
                @click="confirmDelete(data)"
                v-tooltip="'Xóa mềm'"
              />
              <Button
                v-if="canDeleteTeachers && data.is_deleted"
                icon="pi pi-undo"
                outlined
                rounded
                severity="success"
                @click="restoreTeacher(data)"
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

        <!-- Dialog for Adding/Editing Teacher -->
        <Dialog
          v-model:visible="teacherDialog"
          :header="teacher.teacher_id ? 'Sửa Giảng Viên' : 'Thêm Giảng Viên'"
          :style="{ width: '600px' }"
          :modal="true"
          class="p-fluid"
        >
          <div class="form-section">
            <h4>Thông Tin Cơ Bản</h4>
            <div class="field">
              <label for="teacher_id">Mã Giảng Viên</label>
              <InputText id="teacher_id" v-model="teacher.teacher_id" :class="{ 'p-invalid': errors.teacher_id }" :disabled="!!teacher.teacher_id" />
              <small class="p-error" v-if="errors.teacher_id">{{ errors.teacher_id }}</small>
            </div>
            <div class="field">
              <label for="first_name">Tên</label>
              <InputText id="first_name" v-model="teacher.first_name" :class="{ 'p-invalid': errors.first_name }" />
              <small class="p-error" v-if="errors.first_name">{{ errors.first_name }}</small>
            </div>
            <div class="field">
              <label for="last_name">Họ</label>
              <InputText id="last_name" v-model="teacher.last_name" :class="{ 'p-invalid': errors.last_name }" />
              <small class="p-error" v-if="errors.last_name">{{ errors.last_name }}</small>
            </div>
            <div class="field">
              <label for="email">Email</label>
              <InputText id="email" v-model="teacher.email" :class="{ 'p-invalid': errors.email }" />
              <small class="p-error" v-if="errors.email">{{ errors.email }}</small>
            </div>
            <div class="field">
              <label for="phone">Số Điện Thoại</label>
              <InputText id="phone" v-model="teacher.phone" :class="{ 'p-invalid': errors.phone }" />
              <small class="p-error" v-if="errors.phone">{{ errors.phone }}</small>
            </div>
            <div class="field">
              <label for="date_of_birth">Ngày Sinh</label>
              <Calendar id="date_of_birth" v-model="teacher.date_of_birth" :showIcon="true" dateFormat="yy-mm-dd" :class="{ 'p-invalid': errors.date_of_birth }" />
              <small class="p-error" v-if="errors.date_of_birth">{{ errors.date_of_birth }}</small>
            </div>
            <div class="field">
              <label for="gender">Giới Tính</label>
              <Dropdown id="gender" v-model="teacher.gender" :options="genderOptions" optionLabel="label" optionValue="value" :class="{ 'p-invalid': errors.gender }" />
              <small class="p-error" v-if="errors.gender">{{ errors.gender }}</small>
            </div>
            <div class="field">
              <label for="address">Địa Chỉ</label>
              <Textarea id="address" v-model="teacher.address" rows="3" :class="{ 'p-invalid': errors.address }" />
              <small class="p-error" v-if="errors.address">{{ errors.address }}</small>
            </div>
            <h4>Thông Tin Chuyên Môn</h4>
            <div class="field">
              <label for="degree">Học Vị</label>
              <Dropdown id="degree" v-model="teacher.degree" :options="degreeOptions" optionLabel="label" optionValue="value" :class="{ 'p-invalid': errors.degree }" />
              <small class="p-error" v-if="errors.degree">{{ errors.degree }}</small>
            </div>
            <div class="field">
              <label for="specialization">Chuyên Ngành</label>
              <InputText id="specialization" v-model="teacher.specialization" :class="{ 'p-invalid': errors.specialization }" />
              <small class="p-error" v-if="errors.specialization">{{ errors.specialization }}</small>
            </div>
            <div class="field">
              <label for="years_of_experience">Số Năm Kinh Nghiệm</label>
              <InputNumber id="years_of_experience" v-model="teacher.years_of_experience" :min="0" :max="100" :class="{ 'p-invalid': errors.years_of_experience }" />
              <small class="p-error" v-if="errors.years_of_experience">{{ errors.years_of_experience }}</small>
            </div>
            <div class="field">
              <label for="department">Khoa</label>
              <Dropdown id="department" v-model="teacher.department_id" :options="departments" optionLabel="name" optionValue="id" :class="{ 'p-invalid': errors.department_id }" />
              <small class="p-error" v-if="errors.department_id">{{ errors.department_id }}</small>
            </div>
            <h4>Thông Tin Khác</h4>
            <div class="field">
              <label for="profile_picture">Ảnh Đại Diện</label>
              <FileUpload
                id="profile_picture"
                mode="basic"
                accept="image/jpeg,image/png"
                :maxFileSize="2000000"
                @change="handleFileUpload($event)"
                :class="{ 'p-invalid': errors.profile_picture }"
              />
              <small class="p-error" v-if="errors.profile_picture">{{ errors.profile_picture }}</small>
            </div>
            <div class="field">
              <label for="bio">Tiểu Sử</label>
              <Textarea id="bio" v-model="teacher.bio" rows="4" />
            </div>
            <div class="field">
              <label for="status">Trạng Thái</label>
              <Dropdown id="status" v-model="teacher.status" :options="statusOptions" optionLabel="label" optionValue="value" :class="{ 'p-invalid': errors.status }" />
              <small class="p-error" v-if="errors.status">{{ errors.status }}</small>
            </div>
          </div>
          <template #footer>
            <Button label="Hủy" icon="pi pi-times" text @click="hideDialog" />
            <Button label="Lưu" icon="pi pi-check" @click="saveTeacher" />
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
            <span>Bạn có chắc muốn xóa giảng viên <b>{{ teacher.full_name }}</b>?</span>
          </div>
          <template #footer>
            <Button label="Hủy" icon="pi pi-times" text @click="deleteDialog = false" />
            <Button label="Xóa" icon="pi pi-check" severity="danger" @click="deleteTeacher" />
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
      </TabPanel>
    </TabView>
  </div>
  <div v-else class="access-denied">
    <p>Bạn không có quyền truy cập trang này.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { usePermissions } from '@/composables/usePermissions'
import api, { endpoints } from '@/services/api'
import { saveAs } from 'file-saver'
import Dropdown from 'primevue/dropdown';
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';
import Tag from 'primevue/tag';
import InputNumber from 'primevue/inputnumber';


const toast = useToast()
const {
  isAdmin,
  isTeacher,
  canViewTeachers,
  canEditTeachers,
  canDeleteTeachers,
  canExportData
} = usePermissions()

const teachers = ref([])
const teacher = ref({})
const departments = ref([])
const loading = ref(false)
const isEditing = ref(false)
const teacherDialog = ref(false)
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

const navigateToHome = () => {
  router.push('/')
}

const genderOptions = [
  { label: 'Nam', value: 'M' },
  { label: 'Nữ', value: 'F' },
  { label: 'Khác', value: 'O' },
]

const statusOptions = [
  { label: 'Đang giảng dạy', value: 'active' },
  { label: 'Tạm nghỉ', value: 'inactive' },
  { label: 'Đã nghỉ hưu', value: 'retired' },
  { label: 'Nghỉ phép', value: 'on_leave' },
]

const degreeOptions = [
  { label: 'Cử nhân', value: 'bachelor' },
  { label: 'Thạc sĩ', value: 'master' },
  { label: 'Tiến sĩ', value: 'phd' },
  { label: 'Giáo sư', value: 'professor' },
]

onMounted(async () => {
  if (isAdmin.value || isTeacher.value) {
    await loadDepartments()
  }
  if (isTeacher.value) {
    await loadTeacherProfile()
  }
  if (isAdmin.value) {
    await loadTeachers()
  }
})

const loadDepartments = async () => {
  try {
    const response = await api.get(endpoints.departments)
    departments.value = response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách khoa', life: 3000 })
  }
}

const loadTeacherProfile = async () => {
  try {
    loading.value = true
    const response = await api.get(`${endpoints.teachers}me/`)
    teacher.value = response.data.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải thông tin cá nhân', life: 3000 })
  } finally {
    loading.value = false
  }
}

const loadTeachers = async () => {
  try {
    loading.value = true
    const params = {}
    if (filters.value.status) params.status = filters.value.status
    if (filters.value.department) params.department_id = filters.value.department
    if (filters.value.global) params.search = filters.value.global
    const response = await api.get(endpoints.teachers, { params })
    teachers.value = response.data.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách giảng viên', life: 3000 })
  } finally {
    loading.value = false
  }
}

const filterTeachers = () => {
  loadTeachers()
}

const openEdit = () => {
  isEditing.value = true
  errors.value = {}
}

const cancelEdit = () => {
  isEditing.value = false
  loadTeacherProfile()
}

const openNew = () => {
  teacher.value = {
    teacher_id: '',
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    date_of_birth: null,
    gender: 'M',
    address: '',
    degree: 'master',
    specialization: '',
    years_of_experience: 0,
    bio: '',
    status: 'active',
    is_active: true,
    department_id: null,
  }
  teacherDialog.value = true
  errors.value = {}
}

const editTeacher = (data) => {
  teacher.value = { ...data, department_id: data.department_id }
  teacherDialog.value = true
  errors.value = {}
}

const hideDialog = () => {
  teacherDialog.value = false
  teacher.value = {}
  errors.value = {}
}

const saveTeacher = async () => {
  try {
    const formData = new FormData()
    Object.keys(teacher.value).forEach((key) => {
      if (teacher.value[key] !== null && teacher.value[key] !== undefined) {
        formData.append(key, teacher.value[key])
      }
    })

    let response
    if (teacher.value.teacher_id) {
      response = await api.put(`${endpoints.teachers}${teacher.value.teacher_id}/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      if (isTeacher.value) {
        isEditing.value = false
        teacher.value = response.data.data
      }
    } else {
      response = await api.post(endpoints.teachers, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      teacherDialog.value = false
    }
    toast.add({ severity: 'success', summary: 'Thành công', detail: response.data.message, life: 3000 })
    if (isAdmin.value) await loadTeachers()
  } catch (error) {
    if (error.response && error.response.data) {
      errors.value = error.response.data
      toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Vui lòng kiểm tra các trường thông tin', life: 3000 })
    } else {
      toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Có lỗi xảy ra khi lưu giảng viên', life: 3000 })
    }
  }
}

const confirmDelete = (data) => {
  teacher.value = { ...data }
  deleteDialog.value = true
}

const deleteTeacher = async () => {
  try {
    await api.delete(`${endpoints.teachers}${teacher.value.teacher_id}/`)
    deleteDialog.value = false
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa giảng viên thành công', life: 3000 })
    await loadTeachers()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa giảng viên', life: 3000 })
  }
}

const restoreTeacher = async (data) => {
  try {
    const response = await api.post(`${endpoints.teachers}${data.teacher_id}/restore/`)
    toast.add({ severity: 'success', summary: 'Thành công', detail: response.data.message, life: 3000 })
    await loadTeachers()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể khôi phục giảng viên', life: 3000 })
  }
}

const openChangeStatus = (data) => {
  teacher.value = { ...data }
  newStatus.value = ''
  submitted.value = false
  changeStatusDialog.value = true
}

const changeStatus = async () => {
  submitted.value = true
  if (!newStatus.value) return

  try {
    const response = await api.post(`${endpoints.teachers}${teacher.value.teacher_id}/change-status/`, { status: newStatus.value })
    changeStatusDialog.value = false
    toast.add({ severity: 'success', summary: 'Thành công', detail: response.data.message, life: 3000 })
    await loadTeachers()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể cập nhật trạng thái', life: 3000 })
  }
}

const exportTeachers = async () => {
  try {
    const response = await api.get(`${endpoints.teachers}export/`, { responseType: 'blob' })
    const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    saveAs(blob, `teachers_${new Date().toISOString().split('T')[0]}.xlsx`)
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xuất danh sách giảng viên thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xuất danh sách giảng viên', life: 3000 })
  }
}

const handleFileUpload = (event) => {
  const file = event.files[0]
  if (file) {
    teacher.value.profile_picture = file
  }
}

const formatDate = (date) => {
  if (!date) return ''
  const d = new Date(date)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

const getGenderLabel = (gender) => {
  const map = { M: 'Nam', F: 'Nữ', O: 'Khác' }
  return map[gender] || gender
}

const getStatusLabel = (status) => {
  const map = {
    active: 'Đang giảng dạy',
    inactive: 'Tạm nghỉ',
    retired: 'Đã nghỉ hưu',
    on_leave: 'Nghỉ phép',
  }
  return map[status] || status
}

const getStatusSeverity = (status) => {
  const map = {
    active: 'success',
    inactive: 'warning',
    retired: 'info',
    on_leave: 'secondary',
  }
  return map[status] || 'info'
}

const getDegreeLabel = (degree) => {
  const map = {
    bachelor: 'Cử nhân',
    master: 'Thạc sĩ',
    phd: 'Tiến sĩ',
    professor: 'Giáo sư',
  }
  return map[degree] || degree
}
</script>

<style scoped>
.card {
  padding: 1rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.action-buttons {
  display: flex;
  gap: 0.5rem;
}
.filter-bar {
  margin-bottom: 1rem;
}
.filter-group {
  display: flex;
  gap: 1rem;
}
.filter-dropdown {
  width: 200px;
}
.filter-search {
  width: 200px;
}
.empty-message, .loading-message {
  text-align: center;
  padding: 2rem;
  color: #333;
}
.empty-message i, .loading-message i {
  margin-right: 1rem;
}
.form-section h4 {
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  color: #333;
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
</style>