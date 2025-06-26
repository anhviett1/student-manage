<template>
  <div class="card">
    <Toast />
    <TabView v-if="canViewEnrollments || isStudent">
      <!-- Tab for Students -->
      <TabPanel header="Đăng Ký Của Tôi" v-if="isStudent">
        <div class="filter-bar">
          <div class="filter-group">
            <label for="semesterFilter">Học Kỳ</label>
            <Dropdown
              id="semesterFilter"
              v-model="selectedSemester"
              :options="semesters"
              optionLabel="name"
              optionValue="semester_id"
              placeholder="Chọn học kỳ"
              class="filter-dropdown"
              @change="loadMyEnrollments"
            />
          </div>
          <InputText
            v-model="globalFilter"
            placeholder="Tìm môn học, lớp..."
            class="filter-search"
            @input="loadMyEnrollments"
          />
        </div>
        <DataTable
          :value="myEnrollments"
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
              <span>Không tìm thấy đăng ký nào.</span>
            </div>
          </template>
          <template #loading>
            <div class="loading-message">
              <i class="pi pi-spin pi-spinner" />
              <span>Đang tải dữ liệu...</span>
            </div>
          </template>
          <Column field="subject.name" header="Môn Học" sortable style="width: 20%" />
          <Column field="class_obj.class_id" header="Lớp" sortable style="width: 15%" />
          <Column field="semester.name" header="Học Kỳ" sortable style="width: 15%" />
          <Column field="enrollment_date" header="Ngày Đăng Ký" sortable style="width: 15%" align="center">
            <template #body="{ data }">
              {{ formatDate(data.enrollment_date) }}
            </template>
          </Column>
          <Column field="status" header="Trạng Thái" sortable style="width: 15%" align="center">
            <template #body="{ data }">
              <Tag :severity="getStatusSeverity(data.status)" :value="getStatusLabel(data.status)" />
            </template>
          </Column>
          <Column field="notes" header="Ghi Chú" style="width: 20%" />
        </DataTable>
      </TabPanel>

      <!-- Tab for Admins/Teachers -->
      <TabPanel header="Quản Lý Đăng Ký" v-if="isAdminOrTeacher">
        <div class="header">
          <h2>Quản Lý Đăng Ký</h2>
          <div class="action-buttons">
            <Button
              v-if="canEditEnrollments"
              icon="pi pi-plus"
              label="Thêm Đăng Ký"
              severity="primary"
              class="mr-2"
              @click="openNew"
              v-tooltip="'Thêm đăng ký mới'"
            />
            <Button
              v-if="canExportData"
              icon="pi pi-download"
              label="Export"
              severity="success"
              @click="exportEnrollments"
              v-tooltip="'Xuất danh sách đăng ký'"
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
              @change="loadEnrollments"
            />
            <Dropdown
              v-model="filters.semester"
              :options="semesters"
              optionLabel="name"
              optionValue="semester_id"
              placeholder="Lọc học kỳ"
              class="filter-dropdown mr-2"
              @change="loadEnrollments"
            />
            <InputText
              v-model="filters.global"
              placeholder="Tìm sinh viên, môn học, lớp..."
              class="filter-search"
              @input="filterEnrollments"
            />
          </div>
        </div>

        <DataTable
          :value="enrollments"
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
              <span>Không tìm thấy đăng ký nào.</span>
            </div>
          </template>
          <template #loading>
            <div class="loading-message">
              <i class="pi pi-spin pi-spinner" />
              <span>Đang tải dữ liệu...</span>
            </div>
          </template>
          <Column field="student.student_id" header="Sinh Viên" sortable style="width: 15%">
            <template #body="{ data }">
              {{ data.student.student_id }} - {{ data.student.name }}
            </template>
          </Column>
          <Column field="subject.name" header="Môn Học" sortable style="width: 15%" />
          <Column field="class_obj.class_id" header="Lớp" sortable style="width: 10%" />
          <Column field="semester.name" header="Học Kỳ" sortable style="width: 15%" />
          <Column field="enrollment_date" header="Ngày Đăng Ký" sortable style="width: 12%" align="center">
            <template #body="{ data }">
              {{ formatDate(data.enrollment_date) }}
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
          <Column header="Hành Động" style="width: 12%" align="center">
            <template #body="{ data }">
              <Button
                v-if="canEditEnrollments && !data.is_deleted"
                icon="pi pi-pencil"
                outlined
                rounded
                class="mr-2"
                severity="info"
                @click="editEnrollment(data)"
                v-tooltip="'Sửa đăng ký'"
              />
              <Button
                v-if="canDeleteEnrollments && !data.is_deleted"
                icon="pi pi-trash"
                outlined
                rounded
                severity="danger"
                class="mr-2"
                @click="confirmDelete(data)"
                v-tooltip="'Xóa mềm'"
              />
              <Button
                v-if="canDeleteEnrollments && data.is_deleted"
                icon="pi pi-undo"
                outlined
                rounded
                severity="success"
                @click="restoreEnrollment(data)"
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

        <!-- Dialog for Adding/Editing Enrollment -->
        <Dialog
          v-model:visible="enrollmentDialog"
          :header="enrollment.id ? 'Sửa Đăng Ký' : 'Thêm Đăng Ký'"
          :style="{ width: '500px' }"
          :modal="true"
          class="p-fluid"
        >
          <div class="form-section">
            <h4>Thông Tin Đăng Ký</h4>
            <div class="field">
              <label for="student">Sinh Viên</label>
              <Dropdown
                id="student"
                v-model="enrollment.student_id"
                :options="students"
                optionLabel="name"
                optionValue="student_id"
                placeholder="Chọn sinh viên"
                :class="{ 'p-invalid': errors.student_id }"
              />
              <small class="p-error" v-if="errors.student_id">{{ errors.student_id }}</small>
            </div>
            <div class="field">
              <label for="subject">Môn Học</label>
              <Dropdown
                id="subject"
                v-model="enrollment.subject_id"
                :options="subjects"
                optionLabel="name"
                optionValue="subject_id"
                placeholder="Chọn môn học"
                :class="{ 'p-invalid': errors.subject_id }"
              />
              <small class="p-error" v-if="errors.subject_id">{{ errors.subject_id }}</small>
            </div>
            <div class="field">
              <label for="semester">Học Kỳ</label>
              <Dropdown
                id="semester"
                v-model="enrollment.semester_id"
                :options="semesters"
                optionLabel="name"
                optionValue="semester_id"
                placeholder="Chọn học kỳ"
                :class="{ 'p-invalid': errors.semester_id }"
              />
              <small class="p-error" v-if="errors.semester_id">{{ errors.semester_id }}</small>
            </div>
            <div class="field">
              <label for="class_obj">Lớp</label>
              <Dropdown
                id="class_obj"
                v-model="enrollment.class_id"
                :options="classes"
                optionLabel="class_id"
                optionValue="class_id"
                placeholder="Chọn lớp"
                :class="{ 'p-invalid': errors.class_id }"
              />
              <small class="p-error" v-if="errors.class_id">{{ errors.class_id }}</small>
            </div>
            <div class="field">
              <label for="enrollment_date">Ngày Đăng Ký</label>
              <Calendar
                id="enrollment_date"
                v-model="enrollment.enrollment_date"
                :showIcon="true"
                dateFormat="yy-mm-dd"
                placeholder="Chọn ngày"
                :class="{ 'p-invalid': errors.enrollment_date }"
              />
              <small class="p-error" v-if="errors.enrollment_date">{{ errors.enrollment_date }}</small>
            </div>
            <div class="field">
              <label for="notes">Ghi Chú</label>
              <Textarea
                id="notes"
                v-model="enrollment.notes"
                rows="3"
                placeholder="Ghi chú thêm (tùy chọn)"
              />
            </div>
            <div class="field">
              <label for="status">Trạng Thái</label>
              <Dropdown
                id="status"
                v-model="enrollment.status"
                :options="statusOptions"
                optionLabel="label"
                optionValue="value"
                placeholder="Chọn trạng thái"
                :class="{ 'p-invalid': errors.status }"
              />
              <small class="p-error" v-if="errors.status">{{ errors.status }}</small>
            </div>
            <div class="field">
              <label for="is_active">Đang Hoạt Động</label>
              <InputSwitch id="is_active" v-model="enrollment.is_active" />
            </div>
          </div>
          <template #footer>
            <Button label="Hủy" icon="pi pi-times" text @click="hideDialog" />
            <Button label="Lưu" icon="pi pi-check" @click="saveEnrollment" />
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
            <span>Bạn có chắc muốn xóa đăng ký của <b>{{ enrollment.student?.name }}</b> cho môn <b>{{ enrollment.subject?.name }}</b>?</span>
          </div>
          <template #footer>
            <Button label="Hủy" icon="pi pi-times" text @click="deleteDialog = false" />
            <Button label="Xóa" icon="pi pi-check" severity="danger" @click="deleteEnrollment" />
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
    <div v-else class="access-denied">
      <p>Bạn không có quyền truy cập trang này.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { usePermissions } from '@/composables/usePermissions'
import api, { endpoints } from '@/services/api'

const toast = useToast()
const {
  isStudent,
  isAdminOrTeacher,
  canViewEnrollments,
  canEditEnrollments,
  canDeleteEnrollments,
  canExportData,
} = usePermissions()

const myEnrollments = ref([])
const enrollments = ref([])
const semesters = ref([])
const students = ref([])
const subjects = ref([])
const classes = ref([])
const loading = ref(false)
const enrollmentDialog = ref(false)
const deleteDialog = ref(false)
const changeStatusDialog = ref(false)
const enrollment = ref({})
const newStatus = ref('')
const submitted = ref(false)
const errors = ref({})
const selectedSemester = ref(null)
const globalFilter = ref('')
const filters = ref({
  status: null,
  semester: null,
  global: ''
})

const statusOptions = [
  { label: 'Chờ xử lý', value: 'pending' },
  { label: 'Đã duyệt', value: 'approved' },
  { label: 'Từ chối', value: 'rejected' }
]

onMounted(async () => {
  if (canViewEnrollments.value || isStudent.value) {
    await loadSemesters()
    await loadSubjects()
    await loadClasses()
  }

  if (isAdminOrTeacher.value) {
    await loadStudents()
    await loadEnrollments()
  }

  if (isStudent.value) {
    await loadMyEnrollments()
  }
})

const loadSemesters = async () => {
  try {
    const response = await api.get(endpoints.semesters, { params: { active: true } })
    semesters.value = response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải học kỳ', life: 3000 })
  }
}

const loadStudents = async () => {
  try {
    const response = await api.get(endpoints.students)
    students.value = response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách sinh viên', life: 3000 })
  }
}

const loadSubjects = async () => {
  try {
    const response = await api.get(endpoints.subjects)
    subjects.value = response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách môn học', life: 3000 })
  }
}

const loadClasses = async () => {
  try {
    const response = await api.get(endpoints.classes)
    classes.value = response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách lớp', life: 3000 })
  }
}

const loadMyEnrollments = async () => {
  try {
    loading.value = true
    const params = {}
    if (selectedSemester.value) params.semester__semester_id = selectedSemester.value
    if (globalFilter.value) params.search = globalFilter.value
    // Backend sẽ tự lọc dựa trên token
    const response = await api.get(endpoints.enrollments, { params })
    myEnrollments.value = response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải đăng ký', life: 3000 })
  } finally {
    loading.value = false
  }
}

const loadEnrollments = async () => {
  try {
    loading.value = true
    const params = {}
    if (filters.value.status) params.status = filters.value.status
    if (filters.value.semester) params.semester__semester_id = filters.value.semester
    if (filters.value.global) params.search = filters.value.global
    const response = await api.get(endpoints.enrollments, { params })
    enrollments.value = response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải đăng ký', life: 3000 })
  } finally {
    loading.value = false
  }
}

const filterEnrollments = () => {
  loadEnrollments()
}

const openNew = () => {
  enrollment.value = { status: 'pending', is_active: true, enrollment_date: new Date() }
  errors.value = {}
  enrollmentDialog.value = true
}

const editEnrollment = (data) => {
  enrollment.value = {
    ...data,
    student_id: data.student.student_id,
    subject_id: data.subject.subject_id,
    semester_id: data.semester.semester_id,
    class_id: data.class_obj.class_id,
    enrollment_date: new Date(data.enrollment_date)
  }
  errors.value = {}
  enrollmentDialog.value = true
}

const hideDialog = () => {
  enrollmentDialog.value = false
  enrollment.value = {}
  errors.value = {}
}

const confirmDelete = (data) => {
  enrollment.value = data
  deleteDialog.value = true
}

const openChangeStatus = (data) => {
  enrollment.value = data
  newStatus.value = data.status
  submitted.value = false
  changeStatusDialog.value = true
}

const validateEnrollment = () => {
  errors.value = {}
  if (!enrollment.value.student_id) errors.value.student_id = 'Vui lòng chọn sinh viên'
  if (!enrollment.value.subject_id) errors.value.subject_id = 'Vui lòng chọn môn học'
  if (!enrollment.value.semester_id) errors.value.semester_id = 'Vui lòng chọn học kỳ'
  if (!enrollment.value.class_id) errors.value.class_id = 'Vui lòng chọn lớp'
  if (!enrollment.value.enrollment_date) errors.value.enrollment_date = 'Vui lòng chọn ngày đăng ký'
  if (!enrollment.value.status) errors.value.status = 'Vui lòng chọn trạng thái'
  if (enrollment.value.enrollment_date > new Date()) errors.value.enrollment_date = 'Ngày đăng ký không được là ngày tương lai'
  if (enrollment.value.status === 'rejected' && enrollment.value.is_active) {
    errors.value.is_active = 'Đăng ký bị từ chối không thể ở trạng thái hoạt động'
  }
}

const saveEnrollment = async () => {
  validateEnrollment()
  if (Object.keys(errors.value).length > 0) return

  try {
    const payload = {
      ...enrollment.value,
      enrollment_date: enrollment.value.enrollment_date.toISOString().split('T')[0]
    }
    if (enrollment.value.id) {
      const response = await api.patch(`${endpoints.enrollments}${enrollment.value.id}/`, payload)
      enrollments.value = enrollments.value.map(e => e.id === enrollment.value.id ? response.data : e)
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật đăng ký thành công', life: 3000 })
    } else {
      const response = await api.post(endpoints.enrollments, payload)
      enrollments.value.push(response.data)
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Thêm đăng ký thành công', life: 3000 })
    }
    hideDialog()
  } catch (error) {
    const errorMsg = error.response?.data?.detail || Object.values(error.response?.data || {}).join(', ') || 'Không thể lưu đăng ký'
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errorMsg, life: 3000 })
  }
}

const deleteEnrollment = async () => {
  try {
    await api.delete(`${endpoints.enrollments}${enrollment.value.id}/`)
    enrollments.value = enrollments.value.filter(e => e.id !== enrollment.value.id)
    deleteDialog.value = false
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa đăng ký thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa đăng ký', life: 3000 })
  }
}

const restoreEnrollment = async (data) => {
  try {
    const response = await api.post(`${endpoints.enrollments}${data.id}/restore/`)
    enrollments.value = enrollments.value.map(e => e.id === data.id ? response.data.data : e)
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Khôi phục đăng ký thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: error.response?.data?.error || 'Không thể khôi phục đăng ký', life: 3000 })
  }
}

const changeStatus = async () => {
  submitted.value = true
  if (!newStatus.value) return

  try {
    const response = await api.post(`${endpoints.enrollments}${enrollment.value.id}/change-status/`, { status: newStatus.value })
    enrollments.value = enrollments.value.map(e => e.id === enrollment.value.id ? response.data.data : e)
    changeStatusDialog.value = false
    newStatus.value = ''
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật trạng thái thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể cập nhật trạng thái', life: 3000 })
  }
}

const exportEnrollments = async () => {
  try {
    const response = await api.get(`${endpoints.enrollments}export/`, { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `enrollments_${new Date().toISOString().split('T')[0]}.xlsx`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xuất đăng ký thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xuất đăng ký', life: 3000 })
  }
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('vi-VN', { year: 'numeric', month: '2-digit', day: '2-digit' })
}

const getStatusLabel = (status) => {
  const option = statusOptions.find(opt => opt.value === status)
  return option ? option.label : status
}

const getStatusSeverity = (status) => {
  switch (status) {
    case 'pending': return 'info'
    case 'approved': return 'success'
    case 'rejected': return 'danger'
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

.form-section h4 {
  font-size: 1rem;
  margin-bottom: 1rem;
  color: #333;
}

.field {
  margin-bottom: 1.2rem;
}

.field label {
  display: block;
  margin-bottom: 0.3rem;
  font-weight: bold;
}

.confirmation-content {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
}
.access-denied {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #ef4444;
}
</style>