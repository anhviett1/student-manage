<template>
  <div class="card" v-if="isStudent || isAdminOrTeacher">
    <Toast />
    <TabView>
      <!-- Tab for Students -->
      <TabPanel header="Thông Tin Cá Nhân" v-if="isStudent">
        <div class="profile-section">
          <div class="profile-header">
            <h2>Thông Tin Sinh Viên</h2>
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
              <label>Mã Sinh Viên:</label>
              <span>{{ student.student_id }}</span>
            </div>
            <div class="detail-item">
              <label>Họ và Tên:</label>
              <span>{{ student.full_name }}</span>
            </div>
            <div class="detail-item">
              <label>Email:</label>
              <span>{{ student.email }}</span>
            </div>
            <div class="detail-item">
              <label>Số Điện Thoại:</label>
              <span>{{ student.phone || 'Chưa cập nhật' }}</span>
            </div>
            <div class="detail-item">
              <label>Ngày Sinh:</label>
              <span>{{ formatDate(student.date_of_birth) }}</span>
            </div>
            <div class="detail-item">
              <label>Giới Tính:</label>
              <span>{{ getGenderLabel(student.gender) }}</span>
            </div>
            <div class="detail-item">
              <label>Địa Chỉ:</label>
              <span>{{ student.address }}, {{ student.city }}, {{ student.state }}, {{ student.country }}</span>
            </div>
            <div class="detail-item">
              <label>Chuyên Ngành:</label>
              <span>{{ student.major }}</span>
            </div>
            <div class="detail-item">
              <label>GPA:</label>
              <span>{{ student.gpa }}</span>
            </div>
            <div class="detail-item">
              <label>Trạng Thái:</label>
              <Tag :severity="getStatusSeverity(student.status)" :value="getStatusLabel(student.status)" />
            </div>
          </div>
          <div v-else class="edit-form">
            <div class="field">
              <label for="student_id">Mã Sinh Viên</label>
              <InputText id="student_id" v-model="student.student_id" disabled />
            </div>
            <div class="field">
              <label for="first_name">Tên</label>
              <InputText id="first_name" v-model="student.first_name" :class="{ 'p-invalid': errors.first_name }" />
              <small class="p-error" v-if="errors.first_name">{{ errors.first_name }}</small>
            </div>
            <div class="field">
              <label for="last_name">Họ</label>
              <InputText id="last_name" v-model="student.last_name" :class="{ 'p-invalid': errors.last_name }" />
              <small class="p-error" v-if="errors.last_name">{{ errors.last_name }}</small>
            </div>
            <div class="field">
              <label for="email">Email</label>
              <InputText id="email" v-model="student.email" :class="{ 'p-invalid': errors.email }" />
              <small class="p-error" v-if="errors.email">{{ errors.email }}</small>
            </div>
            <div class="field">
              <label for="phone">Số Điện Thoại</label>
              <InputText id="phone" v-model="student.phone" :class="{ 'p-invalid': errors.phone }" />
              <small class="p-error" v-if="errors.phone">{{ errors.phone }}</small>
            </div>
            <div class="field">
              <label for="date_of_birth">Ngày Sinh</label>
              <Calendar id="date_of_birth" v-model="student.date_of_birth" :showIcon="true" dateFormat="yy-mm-dd" :class="{ 'p-invalid': errors.date_of_birth }" />
              <small class="p-error" v-if="errors.date_of_birth">{{ errors.date_of_birth }}</small>
            </div>
            <div class="field">
              <label for="gender">Giới Tính</label>
              <Dropdown id="gender" v-model="student.gender" :options="genderOptions" optionLabel="label" optionValue="value" :class="{ 'p-invalid': errors.gender }" />
              <small class="p-error" v-if="errors.gender">{{ errors.gender }}</small>
            </div>
            <div class="field">
              <label for="address">Địa Chỉ</label>
              <Textarea id="address" v-model="student.address" rows="3" :class="{ 'p-invalid': errors.address }" />
              <small class="p-error" v-if="errors.address">{{ errors.address }}</small>
            </div>
            <div class="field">
              <label for="city">Thành Phố</label>
              <InputText id="city" v-model="student.city" :class="{ 'p-invalid': errors.city }" />
              <small class="p-error" v-if="errors.city">{{ errors.city }}</small>
            </div>
            <div class="field">
              <label for="state">Tỉnh/Thành</label>
              <InputText id="state" v-model="student.state" :class="{ 'p-invalid': errors.state }" />
              <small class="p-error" v-if="errors.state">{{ errors.state }}</small>
            </div>
            <div class="field">
              <label for="country">Quốc Gia</label>
              <InputText id="country" v-model="student.country" :class="{ 'p-invalid': errors.country }" />
              <small class="p-error" v-if="errors.country">{{ errors.country }}</small>
            </div>
            <div class="buttons">
              <Button label="Hủy" icon="pi pi-times" text @click="cancelEdit" />
              <Button label="Lưu" icon="pi pi-check" @click="saveStudent" />
            </div>
          </div>
        </div>
      </TabPanel>

      <!-- Tab for Admins/Teachers -->
      <TabPanel header="Quản Lý Sinh Viên" v-if="isAdminOrTeacher">
        <div class="header">
          <h2>Quản Lý Sinh Viên</h2>
          <div class="action-buttons">
            <Button
              v-if="canEditStudents"
              icon="pi pi-plus"
              label="Thêm Sinh Viên"
              severity="primary"
              class="mr-2"
              @click="openNew"
              v-tooltip="'Thêm sinh viên mới'"
            />
            <Button
              v-if="canExportData"
              icon="pi pi-download"
              label="Export"
              severity="success"
              @click="exportStudents"
              v-tooltip="'Xuất danh sách sinh viên'"
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
              @change="loadStudents"
            />
            <Dropdown
              v-model="filters.department"
              :options="departments"
              optionLabel="name"
              optionValue="id"
              placeholder="Lọc khoa"
              class="filter-dropdown mr-2"
              @change="loadStudents"
            />
            <InputText
              v-model="filters.global"
              placeholder="Tìm mã, tên, email..."
              class="filter-search"
              @input="filterStudents"
            />
          </div>
        </div>

        <DataTable
          v-if="(students.length > 0 || loading) && canViewStudents"
          :value="students"
          :loading="loading"
          dataKey="id"
          :paginator="true"
          :rows="10"
          :rowsPerPageOptions="[5, 10, 20]"
          responsiveLayout="scroll"
          class="p-datatable-sm"
        >
          <template #empty>
            <div class="empty-message">
              <i class="pi pi-info-circle" />
              <span>Không tìm thấy sinh viên nào.</span>
            </div>
          </template>
          <template #loading>
            <div class="loading-message">
              <i class="pi pi-spin pi-spinner" />
              <span>Đang tải dữ liệu...</span>
            </div>
          </template>
          <Column field="student_id" header="Mã Sinh Viên" sortable style="width: 12%" />
          <Column field="full_name" header="Họ và Tên" sortable style="width: 18%" />
          <Column field="email" header="Email" sortable style="width: 18%" />
          <Column field="major" header="Chuyên Ngành" sortable style="width: 15%" />
          <Column field="gpa" header="GPA" sortable style="width: 8%" align="center" />
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
                v-if="canEditStudents && !data.is_deleted"
                icon="pi pi-pencil"
                outlined
                rounded
                class="mr-2"
                severity="info"
                @click="editStudent(data)"
                v-tooltip="'Sửa thông tin'"
              />
              <Button
                v-if="canDeleteStudents && !data.is_deleted"
                icon="pi pi-trash"
                outlined
                rounded
                severity="danger"
                class="mr-2"
                @click="confirmDelete(data)"
                v-tooltip="'Xóa mềm'"
              />
              <Button
                v-if="canDeleteStudents && data.is_deleted"
                icon="pi pi-undo"
                outlined
                rounded
                severity="success"
                @click="restoreStudent(data)"
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

        <!-- Fallback when no data and not loading -->
        <div v-else-if="!loading && students.length === 0 && canViewStudents" class="no-data-message">
          <p>Không có dữ liệu sinh viên để hiển thị.</p>
          <Button 
            label="Tải lại" 
            icon="pi pi-refresh" 
            @click="loadStudents"
            severity="secondary"
          />
        </div>

        <!-- Dialog for Adding/Editing Student -->
        <Dialog
          v-model:visible="studentDialog"
          :header="student.id ? 'Sửa Sinh Viên' : 'Thêm Sinh Viên'"
          :style="{ width: '600px' }"
          :modal="true"
          class="p-fluid"
        >
          <div class="form-section">
            <h4>Thông Tin Cơ Bản</h4>
            <div class="field">
              <label for="student_id">Mã Sinh Viên</label>
              <InputText id="student_id" v-model="student.student_id" :class="{ 'p-invalid': errors.student_id }" :disabled="!!student.id" />
              <small class="p-error" v-if="errors.student_id">{{ errors.student_id }}</small>
            </div>
            <div class="field">
              <label for="first_name">Tên</label>
              <InputText id="first_name" v-model="student.first_name" :class="{ 'p-invalid': errors.first_name }" />
              <small class="p-error" v-if="errors.first_name">{{ errors.first_name }}</small>
            </div>
            <div class="field">
              <label for="last_name">Họ</label>
              <InputText id="last_name" v-model="student.last_name" :class="{ 'p-invalid': errors.last_name }" />
              <small class="p-error" v-if="errors.last_name">{{ errors.last_name }}</small>
            </div>
            <div class="field">
              <label for="email">Email</label>
              <InputText id="email" v-model="student.email" :class="{ 'p-invalid': errors.email }" />
              <small class="p-error" v-if="errors.email">{{ errors.email }}</small>
            </div>
            <div class="field">
              <label for="phone">Số Điện Thoại</label>
              <InputText id="phone" v-model="student.phone" :class="{ 'p-invalid': errors.phone }" />
              <small class="p-error" v-if="errors.phone">{{ errors.phone }}</small>
            </div>
            <div class="field">
              <label for="date_of_birth">Ngày Sinh</label>
              <Calendar id="date_of_birth" v-model="student.date_of_birth" :showIcon="true" dateFormat="yy-mm-dd" :class="{ 'p-invalid': errors.date_of_birth }" />
              <small class="p-error" v-if="errors.date_of_birth">{{ errors.date_of_birth }}</small>
            </div>
            <div class="field">
              <label for="gender">Giới Tính</label>
              <Dropdown id="gender" v-model="student.gender" :options="genderOptions" optionLabel="label" optionValue="value" :class="{ 'p-invalid': errors.gender }" />
              <small class="p-error" v-if="errors.gender">{{ errors.gender }}</small>
            </div>
            <h4>Thông Tin Học Tập</h4>
            <div class="field">
              <label for="enrollment_date">Ngày Nhập Học</label>
              <Calendar id="enrollment_date" v-model="student.enrollment_date" :showIcon="true" dateFormat="yy-mm-dd" :class="{ 'p-invalid': errors.enrollment_date }" />
              <small class="p-error" v-if="errors.enrollment_date">{{ errors.enrollment_date }}</small>
            </div>
            <div class="field">
              <label for="graduation_date">Ngày Tốt Nghiệp</label>
              <Calendar id="graduation_date" v-model="student.graduation_date" :showIcon="true" dateFormat="yy-mm-dd" :class="{ 'p-invalid': errors.graduation_date }" />
              <small class="p-error" v-if="errors.graduation_date">{{ errors.graduation_date }}</small>
            </div>
            <div class="field">
              <label for="status">Trạng Thái</label>
              <Dropdown id="status" v-model="student.status" :options="statusOptions" optionLabel="label" optionValue="value" :class="{ 'p-invalid': errors.status }" />
              <small class="p-error" v-if="errors.status">{{ errors.status }}</small>
            </div>
            <div class="field">
              <label for="major">Chuyên Ngành</label>
              <InputText id="major" v-model="student.major" :class="{ 'p-invalid': errors.major }" />
              <small class="p-error" v-if="errors.major">{{ errors.major }}</small>
            </div>
            <div class="field">
              <label for="minor">Chuyên Ngành Phụ</label>
              <InputText id="minor" v-model="student.minor" />
            </div>
            <div class="field">
              <label for="department">Khoa</label>
              <Dropdown id="department" v-model="student.department_id" :options="departments" optionLabel="name" optionValue="id" :class="{ 'p-invalid': errors.department_id }" />
              <small class="p-error" v-if="errors.department_id">{{ errors.department_id }}</small>
            </div>
            <h4>Thông Tin Liên Hệ Khẩn Cấp</h4>
            <div class="field">
              <label for="emergency_contact_name">Người Liên Hệ</label>
              <InputText id="emergency_contact_name" v-model="student.emergency_contact_name" :class="{ 'p-invalid': errors.emergency_contact_name }" />
              <small class="p-error" v-if="errors.emergency_contact_name">{{ errors.emergency_contact_name }}</small>
            </div>
            <div class="field">
              <label for="emergency_contact_phone">Số Điện Thoại</label>
              <InputText id="emergency_contact_phone" v-model="student.emergency_contact_phone" :class="{ 'p-invalid': errors.emergency_contact_phone }" />
              <small class="p-error" v-if="errors.emergency_contact_phone">{{ errors.emergency_contact_phone }}</small>
            </div>
            <div class="field">
              <label for="emergency_contact_relationship">Mối Quan Hệ</label>
              <InputText id="emergency_contact_relationship" v-model="student.emergency_contact_relationship" :class="{ 'p-invalid': errors.emergency_contact_relationship }" />
              <small class="p-error" v-if="errors.emergency_contact_relationship">{{ errors.emergency_contact_relationship }}</small>
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
              <label for="student_id_card">Mã Thẻ Sinh Viên</label>
              <InputText id="student_id_card" v-model="student.student_id_card" :class="{ 'p-invalid': errors.student_id_card }" />
              <small class="p-error" v-if="errors.student_id_card">{{ errors.student_id_card }}</small>
            </div>
            <div class="field">
              <label for="blood_type">Nhóm Máu</label>
              <InputText id="blood_type" v-model="student.blood_type" />
            </div>
            <div class="field">
              <label for="medical_conditions">Tình Trạng Sức Khỏe</label>
              <Textarea id="medical_conditions" v-model="student.medical_conditions" rows="3" />
            </div>
            <div class="field">
              <label for="allergies">Dị Ứng</label>
              <Textarea id="allergies" v-model="student.allergies" rows="3" />
            </div>
          </div>
          <template #footer>
            <Button label="Hủy" icon="pi pi-times" text @click="hideDialog" />
            <Button label="Lưu" icon="pi pi-check" @click="saveStudent" />
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
            <span>Bạn có chắc muốn xóa sinh viên <b>{{ student.full_name }}</b>?</span>
          </div>
          <template #footer>
            <Button label="Hủy" icon="pi pi-times" text @click="deleteDialog = false" />
            <Button label="Xóa" icon="pi pi-check" severity="danger" @click="deleteStudent" />
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
import { ref, onMounted, reactive, computed } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import { useUserStore } from '@/stores/user'
import api, { endpoints } from '@/services/api'
import { saveAs } from 'file-saver'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import Tag from 'primevue/tag'
import InputNumber from 'primevue/inputnumber'

const toast = useToast()
const confirm = useConfirm()
const userStore = useUserStore()

const students = ref([])
const student = ref({})
const departments = ref([])
const loading = ref(false)
const isEditing = ref(false)
const studentDialog = ref(false)
const deleteDialog = ref(false)
const changeStatusDialog = ref(false)
const errors = ref({})
const newStatus = ref('')
const submitted = ref(false)
const filters = reactive({
  global: '',
  status: 'active',
  department: null,
})

const { isStudent, isAdminOrTeacher } = computed(() => ({
  isStudent: userStore.currentUser?.is_student,
  isAdminOrTeacher: userStore.currentUser?.is_admin || userStore.currentUser?.is_teacher,
}))

const canViewStudents = computed(() => isAdminOrTeacher.value)
const canEditStudents = computed(
  () => isAdminOrTeacher.value,
)
const canDeleteStudents = computed(
  () => isAdminOrTeacher.value,
)
const canExportData = computed(() => isAdminOrTeacher.value)

const genderOptions = [
  { label: 'Nam', value: 'M' },
  { label: 'Nữ', value: 'F' },
  { label: 'Khác', value: 'O' },
  { label: 'Đình chỉ', value: 'suspended' },
]

const statusOptions = [
  { label: 'Đang học', value: 'active' },
  { label: 'Tạm nghỉ', value: 'inactive' },
  { label: 'Đã tốt nghiệp', value: 'graduated' },
  { label: 'Bị đình chỉ', value: 'suspended' },
  { label: 'Nghỉ phép', value: 'on_leave' },
]

onMounted(async () => {
  if (isStudent.value) {
    await loadCurrentStudentProfile()
  }
  if (isAdminOrTeacher.value) {
    await loadStudents()
    await loadDepartments()
  }
})

const loadDepartments = async () => {
  try {
    const response = await api.get(endpoints.departments)
    
    // Ensure departments.value is always an array
    if (response.data && Array.isArray(response.data)) {
      departments.value = response.data
    } else if (response.data && response.data.results && Array.isArray(response.data.results)) {
      departments.value = response.data.results
    } else if (response.data && response.data.data && Array.isArray(response.data.data)) {
      departments.value = response.data.data
    } else {
      departments.value = []
    }
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách khoa', life: 3000 })
    departments.value = []
  }
}

const loadCurrentStudentProfile = async () => {
  loading.value = true
  try {
    if (!userStore.currentUser) {
      await userStore.getCurrentUser()
    }
    student.value = userStore.currentUser?.student_profile || {}
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Lỗi',
      detail: 'Không thể tải thông tin cá nhân.',
      life: 3000,
    })
  } finally {
    loading.value = false
  }
}

const loadStudents = async () => {
  if (!canViewStudents.value) return
  try {
    loading.value = true
    const params = {}
    if (filters.status) params.status = filters.status
    if (filters.department) params.department_id = filters.department
    if (filters.global) params.search = filters.global
    const response = await api.get(endpoints.students, { params })
    
    // Ensure students.value is always an array
    if (response.data && Array.isArray(response.data)) {
      students.value = response.data
    } else if (response.data && response.data.data && Array.isArray(response.data.data)) {
      students.value = response.data.data
    } else if (response.data && response.data.results && Array.isArray(response.data.results)) {
      students.value = response.data.results
    } else {
      students.value = []
    }
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách sinh viên', life: 3000 })
    students.value = []
  } finally {
    loading.value = false
  }
}

const filterStudents = () => {
  loadStudents()
}

const openEdit = () => {
  isEditing.value = true
  errors.value = {}
}

const cancelEdit = () => {
  isEditing.value = false
  loadCurrentStudentProfile()
}

const openNew = () => {
  student.value = {
    student_id: '',
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    date_of_birth: null,
    gender: 'M',
    address: '',
    city: '',
    state: '',
    postal_code: '',
    country: '',
    enrollment_date: new Date().toISOString().split('T')[0],
    graduation_date: null,
    status: 'active',
    major: '',
    minor: '',
    emergency_contact_name: '',
    emergency_contact_phone: '',
    emergency_contact_relationship: '',
    student_id_card: '',
    blood_type: '',
    medical_conditions: '',
    allergies: '',
    department_id: null,
    is_active: true,
  }
  studentDialog.value = true
  errors.value = {}
}

const editStudent = (data) => {
  student.value = { ...data, department_id: data.department_id }
  studentDialog.value = true
  errors.value = {}
}

const hideDialog = () => {
  studentDialog.value = false
  student.value = {}
  errors.value = {}
}

const saveStudent = async () => {
  try {
    const formData = new FormData()
    Object.keys(student.value).forEach((key) => {
      if (student.value[key] !== null && student.value[key] !== undefined) {
        formData.append(key, student.value[key])
      }
    })

    let response
    if (student.value.id) {
      response = await api.put(`${endpoints.students}${student.value.id}/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      if (isStudent.value) {
        isEditing.value = false
        student.value = response.data.data
      }
    } else {
      response = await api.post(endpoints.students, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      studentDialog.value = false
    }
    toast.add({ severity: 'success', summary: 'Thành công', detail: response.data.message, life: 3000 })
    if (isAdminOrTeacher.value) await loadStudents()
  } catch (error) {
    if (error.response && error.response.data) {
      errors.value = error.response.data
      toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Vui lòng kiểm tra các trường thông tin', life: 3000 })
    } else {
      toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Có lỗi xảy ra khi lưu sinh viên', life: 3000 })
    }
  }
}

const confirmDelete = (data) => {
  student.value = { ...data }
  deleteDialog.value = true
}

const deleteStudent = async () => {
  try {
    await api.delete(`${endpoints.students}${student.value.id}/`)
    deleteDialog.value = false
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa sinh viên thành công', life: 3000 })
    await loadStudents()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa sinh viên', life: 3000 })
  }
}

const restoreStudent = async (data) => {
  try {
    const response = await api.post(`${endpoints.students}${data.id}/restore/`)
    toast.add({ severity: 'success', summary: 'Thành công', detail: response.data.message, life: 3000 })
    await loadStudents()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể khôi phục sinh viên', life: 3000 })
  }
}

const openChangeStatus = (data) => {
  student.value = { ...data }
  newStatus.value = ''
  submitted.value = false
  changeStatusDialog.value = true
}

const changeStatus = async () => {
  submitted.value = true
  if (!newStatus.value) return

  try {
    const response = await api.post(`${endpoints.students}${student.value.id}/change-status/`, { status: newStatus.value })
    changeStatusDialog.value = false
    toast.add({ severity: 'success', summary: 'Thành công', detail: response.data.message, life: 3000 })
    await loadStudents()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể cập nhật trạng thái', life: 3000 })
  }
}

const exportStudents = async () => {
  try {
    const response = await api.get(`${endpoints.students}export/`, { responseType: 'blob' })
    const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    saveAs(blob, `students_${new Date().toISOString().split('T')[0]}.xlsx`)
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xuất danh sách sinh viên thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xuất danh sách sinh viên', life: 3000 })
  }
}

const handleFileUpload = (event) => {
  const file = event.files[0]
  if (file) {
    student.value.profile_picture = file
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
    active: 'Đang học',
    inactive: 'Tạm nghỉ',
    graduated: 'Đã tốt nghiệp',
    suspended: 'Bị đình chỉ',
    on_leave: 'Nghỉ phép',
  }
  return map[status] || status
}

const getStatusSeverity = (status) => {
  const map = {
    active: 'success',
    inactive: 'warning',
    graduated: 'info',
    suspended: 'danger',
    on_leave: 'secondary',
  }
  return map[status] || 'info'
}
</script>

<style scoped>
/* Style chung cho card, header, action-buttons, filter-bar */
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
.p-datatable-sm :deep(td .p-button) {
  margin-right: 0.25rem !important;
}
.p-datatable-sm :deep(td .p-button:last-child) {
  margin-right: 0 !important;
}
@media (max-width: 768px) {
  .p-datatable-sm :deep(td .p-button) {
    min-width: 24px !important;
    height: 24px !important;
    width: 24px !important;
    font-size: 0.8rem !important;
  }
}
</style>