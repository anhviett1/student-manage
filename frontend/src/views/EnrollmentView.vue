<template>
  <div>
    <Toast />
    <div v-if="canViewEnrollments || isStudent" class="card">
      <TabView>
        <!-- Tab 1: Đăng Ký Của Tôi (cho sinh viên) -->
        <TabPanel header="Đăng Ký Của Tôi" v-if="isStudent">
          <div class="profile-section">
            <div class="profile-header">
              <h2>Đăng Ký Của Tôi</h2>
            </div>
            <div class="filter-bar">
              <div class="filter-group">
                <Dropdown v-model="selectedSemester" :options="semesters" optionLabel="semester_name" optionValue="semester_id" placeholder="Chọn học kỳ" class="filter-dropdown" @change="loadMyEnrollments" />
                <InputText v-model="globalFilter" placeholder="Tìm môn học, lớp..." class="filter-search" @input="loadMyEnrollments" />
              </div>
            </div>
          </div>
          <div v-if="(myEnrollments.length > 0 || loading) && isStudent">
            <DataTable :value="myEnrollments" :loading="loading" dataKey="enrollment_id" :paginator="true" :rows="10" :rowsPerPageOptions="[5, 10, 20]" responsiveLayout="scroll" class="p-datatable-sm">
              <template #empty>
                <div class="empty-message"><i class="pi pi-info-circle" /><span>Không tìm thấy đăng ký nào.</span></div>
              </template>
              <template #loading>
                <div class="loading-message"><i class="pi pi-spin pi-spinner" /><span>Đang tải dữ liệu...</span></div>
              </template>
              <Column field="subject.subject_name" header="Môn Học" sortable style="width: 20%" />
              <Column field="class_obj.class_id" header="Lớp" sortable style="width: 15%" />
              <Column field="semester.semester_name" header="Học Kỳ" sortable style="width: 15%" />
              <Column field="enrollment_date" header="Ngày Đăng Ký" sortable style="width: 15%" align="center">
                <template #body="{ data }">{{ formatDate(data.enrollment_date) }}</template>
              </Column>
              <Column field="status" header="Trạng Thái" sortable style="width: 15%" align="center">
                <template #body="{ data }"><Tag :severity="getStatusSeverity(data.status)" :value="getStatusLabel(data.status)" /></template>
              </Column>
              <Column field="notes" header="Ghi Chú" style="width: 20%" />
            </DataTable>
          </div>
          <div v-else-if="!loading && myEnrollments.length === 0 && isStudent">
            <div class="no-data-message">
              <p>Không có dữ liệu đăng ký để hiển thị.</p>
              <Button label="Tải lại" icon="pi pi-refresh" @click="loadMyEnrollments" severity="secondary" />
            </div>
          </div>
        </TabPanel>
        <!-- Tab 2: Quản Lý Đăng Ký (admin/giáo viên) -->
        <TabPanel header="Quản Lý Đăng Ký" v-if="isAdminOrTeacher">
          <div class="header">
            <h2>Quản Lý Đăng Ký</h2>
            <div class="action-buttons">
              <Button v-if="canEditEnrollments" icon="pi pi-plus" label="Thêm Đăng Ký" severity="primary" class="mr-2" @click="openNew" v-tooltip="'Thêm đăng ký mới'" />
              <Button v-if="canExportData" icon="pi pi-download" label="Export" severity="success" @click="exportEnrollments" v-tooltip="'Xuất danh sách đăng ký'" />
            </div>
          </div>
          <div class="filter-bar">
            <div class="filter-group">
              <Dropdown v-model="filters.status" :options="statusOptions" optionLabel="label" optionValue="value" placeholder="Lọc trạng thái" class="filter-dropdown mr-2" @change="loadEnrollments" />
              <Dropdown v-model="filters.semester" :options="semesters" optionLabel="semester_name" optionValue="semester_id" placeholder="Lọc học kỳ" class="filter-dropdown mr-2" @change="loadEnrollments" />
              <InputText v-model="filters.global" placeholder="Tìm sinh viên, môn học, lớp..." class="filter-search" @input="filterEnrollments" />
            </div>
          </div>
          <div v-if="(enrollments.length > 0 || loading) && isAdminOrTeacher">
            <DataTable :value="enrollments" :loading="loading" dataKey="enrollment_id" :paginator="true" :rows="10" :rowsPerPageOptions="[5, 10, 20]" responsiveLayout="scroll" class="p-datatable-sm">
              <template #empty>
                <div class="empty-message"><i class="pi pi-info-circle" /><span>Không tìm thấy đăng ký nào.</span></div>
              </template>
              <template #loading>
                <div class="loading-message"><i class="pi pi-spin pi-spinner" /><span>Đang tải dữ liệu...</span></div>
              </template>
              <Column field="student.full_name" header="Sinh Viên" sortable style="width: 15%" />
              <Column field="subject.subject_name" header="Môn Học" sortable style="width: 15%" />
              <Column field="class_obj.class_id" header="Lớp" sortable style="width: 10%" />
              <Column field="semester.semester_name" header="Học Kỳ" sortable style="width: 15%" />
              <Column field="enrollment_date" header="Ngày Đăng Ký" sortable style="width: 12%" align="center">
                <template #body="{ data }">{{ formatDate(data.enrollment_date) }}</template>
              </Column>
              <Column field="status" header="Trạng Thái" sortable style="width: 12%" align="center">
                <template #body="{ data }"><Tag :severity="getStatusSeverity(data.status)" :value="getStatusLabel(data.status)" /></template>
              </Column>
              <Column field="is_active" header="Hoạt Động" sortable style="width: 10%" align="center">
                <template #body="{ data }"><Tag :severity="data.is_active ? 'success' : 'warning'" :value="data.is_active ? 'Có' : 'Không'" /></template>
              </Column>
              <Column header="Hành Động" style="width: 15%" align="center">
                <template #body="{ data }">
                  <Button v-if="canEditEnrollments && !data.is_deleted" icon="pi pi-pencil" outlined rounded class="mr-2" severity="info" @click="editEnrollment(data)" v-tooltip="'Sửa thông tin'"/>
                  <Button v-if="canDeleteEnrollments && !data.is_deleted" icon="pi pi-trash" outlined rounded severity="danger" class="mr-2" @click="confirmDelete(data)" v-tooltip="'Xóa mềm'"/>
                  <Button v-if="canDeleteEnrollments && data.is_deleted" icon="pi pi-undo" outlined rounded severity="success" @click="restoreEnrollment(data)" v-tooltip="'Khôi phục'"/>
                </template>
              </Column>
            </DataTable>
          </div>
          <div v-else-if="!loading && enrollments.length === 0 && isAdminOrTeacher">
            <div class="no-data-message">
              <p>Không có dữ liệu đăng ký để hiển thị.</p>
              <Button label="Tải lại" icon="pi pi-refresh" @click="loadEnrollments" severity="secondary" />
            </div>
          </div>
          <!-- Dialog thêm/sửa đăng ký -->
          <Dialog v-model:visible="enrollmentDialog" :header="enrollmentObj.enrollment_id ? 'Sửa Đăng Ký' : 'Thêm Đăng Ký'" :style="{ width: '600px' }" :modal="true" class="p-fluid">
            <div class="form-section">
              <h4>Thông Tin Đăng Ký</h4>
              <div class="field">
                <label for="student">Sinh Viên</label>
                <Dropdown id="student" v-model="enrollmentObj.student" :options="students" optionLabel="full_name" optionValue="student_id" placeholder="Chọn sinh viên" :class="{ 'p-invalid': errors.student }" />
                <small class="p-error" v-if="errors.student">{{ errors.student }}</small>
              </div>
              <div class="field">
                <label for="subject">Môn Học</label>
                <Dropdown id="subject" v-model="enrollmentObj.subject" :options="subjects" optionLabel="subject_name" optionValue="subject_id" placeholder="Chọn môn học" :class="{ 'p-invalid': errors.subject }" />
                <small class="p-error" v-if="errors.subject">{{ errors.subject }}</small>
              </div>
              <div class="field">
                <label for="semester">Học Kỳ</label>
                <Dropdown id="semester" v-model="enrollmentObj.semester" :options="semesters" optionLabel="semester_name" optionValue="semester_id" placeholder="Chọn học kỳ" :class="{ 'p-invalid': errors.semester }" />
                <small class="p-error" v-if="errors.semester">{{ errors.semester }}</small>
              </div>
              <div class="field">
                <label for="class_obj">Lớp</label>
                <Dropdown id="class_obj" v-model="enrollmentObj.class_obj" :options="classes" optionLabel="class_id" optionValue="class_id" placeholder="Chọn lớp" :class="{ 'p-invalid': errors.class_obj }" />
                <small class="p-error" v-if="errors.class_obj">{{ errors.class_obj }}</small>
              </div>
              <div class="field">
                <label for="enrollment_date">Ngày Đăng Ký</label>
                <Calendar id="enrollment_date" v-model="enrollmentObj.enrollment_date" :showIcon="true" dateFormat="yy-mm-dd" placeholder="Chọn ngày" :class="{ 'p-invalid': errors.enrollment_date }" />
                <small class="p-error" v-if="errors.enrollment_date">{{ errors.enrollment_date }}</small>
              </div>
              <div class="field">
                <label for="notes">Ghi Chú</label>
                <Textarea id="notes" v-model="enrollmentObj.notes" rows="3" placeholder="Ghi chú thêm (tùy chọn)" />
              </div>
              <div class="field">
                <label for="status">Trạng Thái</label>
                <Dropdown id="status" v-model="enrollmentObj.status" :options="statusOptions" optionLabel="label" optionValue="value" placeholder="Chọn trạng thái" :class="{ 'p-invalid': errors.status }" />
                <small class="p-error" v-if="errors.status">{{ errors.status }}</small>
              </div>
              <div class="field">
                <label for="is_active">Đang Hoạt Động</label>
                <InputSwitch id="is_active" v-model="enrollmentObj.is_active" />
              </div>
            </div>
            <template #footer>
              <Button label="Hủy" icon="pi pi-times" text @click="hideDialog" />
              <Button label="Lưu" icon="pi pi-check" @click="saveEnrollment" />
            </template>
          </Dialog>
          <!-- Dialog xác nhận xóa mềm -->
          <Dialog v-model:visible="deleteDialog" header="Xác Nhận Xóa" :style="{ width: '400px' }" :modal="true">
            <div class="confirmation-content">
              <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
              <span>Bạn có chắc muốn xóa đăng ký của <b>{{ enrollmentObj.student?.full_name }}</b> cho môn <b>{{ enrollmentObj.subject?.subject_name }}</b>?</span>
            </div>
            <template #footer>
              <Button label="Hủy" icon="pi pi-times" text @click="deleteDialog = false" />
              <Button label="Xóa" icon="pi pi-check" severity="danger" @click="deleteEnrollment" />
            </template>
          </Dialog>
          <!-- Dialog xác nhận khôi phục -->
          <Dialog v-model:visible="restoreDialog" header="Xác Nhận Khôi Phục" :style="{ width: '400px' }" :modal="true">
            <div class="confirmation-content">
              <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
              <span>Bạn có chắc muốn khôi phục đăng ký của <b>{{ enrollmentObj.student?.full_name }}</b> cho môn <b>{{ enrollmentObj.subject?.subject_name }}</b>?</span>
            </div>
            <template #footer>
              <Button label="Hủy" icon="pi pi-times" text @click="restoreDialog = false" />
              <Button label="Khôi phục" icon="pi pi-check" severity="success" @click="restoreEnrollment" />
            </template>
          </Dialog>
          <!-- Dialog đổi trạng thái -->
          <Dialog v-model:visible="changeStatusDialog" header="Thay Đổi Trạng Thái" :style="{ width: '400px' }" :modal="true">
            <div class="field">
              <label for="new_status">Trạng Thái Mới</label>
              <Dropdown id="new_status" v-model="newStatus" :options="statusOptions" optionLabel="label" optionValue="value" placeholder="Chọn trạng thái mới" :class="{ 'p-invalid': submitted && !newStatus }" />
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
const { isStudent, isAdminOrTeacher, canViewEnrollments, canEditEnrollments, canDeleteEnrollments, canExportData } = computed(() => ({
  isStudent: false, 
  isAdminOrTeacher: false, 
  canViewEnrollments: false, 
  canEditEnrollments: false, 
  canDeleteEnrollments: false, 
  canExportData: false 
}))

const myEnrollments = ref([])
const enrollments = ref([])
const enrollmentObj = ref({})
const enrollmentDialog = ref(false)
const deleteDialog = ref(false)
const restoreDialog = ref(false)
const changeStatusDialog = ref(false)
const isEditing = ref(false)
const loading = ref(false)
const errors = ref({})
const newStatus = ref('')
const submitted = ref(false)
const students = ref([])
const subjects = ref([])
const classes = ref([])
const semesters = ref([])
const selectedSemester = ref(null)
const globalFilter = ref('')
const filters = reactive({
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
  await Promise.all([
    loadSemesters(),
    loadSubjects(),
    loadClasses()
  ])
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
    const response = await api.get(endpoints.semesters)
    semesters.value = Array.isArray(response.data) ? response.data : response.data.results || []
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải học kỳ', life: 3000 })
    semesters.value = []
  }
}

const loadStudents = async () => {
  try {
    const response = await api.get(endpoints.students)
    students.value = Array.isArray(response.data) ? response.data : response.data.results || []
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách sinh viên', life: 3000 })
    students.value = []
  }
}

const loadSubjects = async () => {
  try {
    const response = await api.get(endpoints.subjects)
    subjects.value = Array.isArray(response.data) ? response.data : response.data.results || []
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách môn học', life: 3000 })
    subjects.value = []
  }
}

const loadClasses = async () => {
  try {
    const response = await api.get(endpoints.classes)
    classes.value = Array.isArray(response.data) ? response.data : response.data.results || []
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách lớp', life: 3000 })
    classes.value = []
  }
}

const loadMyEnrollments = async () => {
  try {
    loading.value = true
    const params = {}
    if (selectedSemester.value) params.semester_id = selectedSemester.value
    if (globalFilter.value) params.search = globalFilter.value
    const response = await api.get(endpoints.enrollments, { params })
    myEnrollments.value = Array.isArray(response.data.results) ? response.data.results : response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải đăng ký', life: 3000 })
    myEnrollments.value = []
  } finally {
    loading.value = false
  }
}

const loadEnrollments = async () => {
  try {
    loading.value = true
    const params = {}
    if (filters.status) params.status = filters.status
    if (filters.semester) params.semester_id = filters.semester
    if (filters.global) params.search = filters.global
    const response = await api.get(endpoints.enrollments, { params })
    enrollments.value = Array.isArray(response.data.results) ? response.data.results : response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải đăng ký', life: 3000 })
    enrollments.value = []
  } finally {
    loading.value = false
  }
}

const filterEnrollments = () => {
  loadEnrollments()
}

const openNew = () => {
  enrollmentObj.value = { status: 'pending', is_active: true, enrollment_date: new Date() }
  errors.value = {}
  enrollmentDialog.value = true
}

const editEnrollment = (data) => {
  enrollmentObj.value = {
    ...data,
    student: data.student?.student_id,
    subject: data.subject?.subject_id,
    semester: data.semester?.semester_id,
    class_obj: data.class_obj?.class_id,
    enrollment_date: new Date(data.enrollment_date)
  }
  errors.value = {}
  enrollmentDialog.value = true
}

const hideDialog = () => {
  enrollmentDialog.value = false
  enrollmentObj.value = {}
  errors.value = {}
}

const confirmDelete = (data) => {
  enrollmentObj.value = { ...data }
  deleteDialog.value = true
}

const restoreEnrollment = async () => {
  try {
    const response = await api.post(`${endpoints.enrollments}${enrollmentObj.value.enrollment_id}/restore/`)
    enrollments.value = enrollments.value.map(e => e.enrollment_id === enrollmentObj.value.enrollment_id ? response.data : e)
    restoreDialog.value = false
    enrollmentObj.value = {}
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Khôi phục đăng ký thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể khôi phục đăng ký', life: 3000 })
  }
}

const validateEnrollment = () => {
  errors.value = {}
  if (!enrollmentObj.value.student) errors.value.student = 'Vui lòng chọn sinh viên'
  if (!enrollmentObj.value.subject) errors.value.subject = 'Vui lòng chọn môn học'
  if (!enrollmentObj.value.semester) errors.value.semester = 'Vui lòng chọn học kỳ'
  if (!enrollmentObj.value.class_obj) errors.value.class_obj = 'Vui lòng chọn lớp'
  if (!enrollmentObj.value.enrollment_date) errors.value.enrollment_date = 'Vui lòng chọn ngày đăng ký'
  if (!enrollmentObj.value.status) errors.value.status = 'Vui lòng chọn trạng thái'
  if (enrollmentObj.value.status === 'rejected' && enrollmentObj.value.is_active) {
    errors.value.is_active = 'Đăng ký bị từ chối không thể ở trạng thái hoạt động'
  }
}

const saveEnrollment = async () => {
  validateEnrollment()
  if (Object.keys(errors.value).length > 0) return
  try {
    const payload = {
      ...enrollmentObj.value,
      enrollment_date: enrollmentObj.value.enrollment_date instanceof Date ? enrollmentObj.value.enrollment_date.toISOString().split('T')[0] : enrollmentObj.value.enrollment_date
    }
    if (enrollmentObj.value.enrollment_id) {
      const response = await api.patch(`${endpoints.enrollments}${enrollmentObj.value.enrollment_id}/`, payload)
      enrollments.value = enrollments.value.map(e => e.enrollment_id === enrollmentObj.value.enrollment_id ? response.data : e)
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
    await api.delete(`${endpoints.enrollments}${enrollmentObj.value.enrollment_id}/`)
    enrollments.value = enrollments.value.filter(e => e.enrollment_id !== enrollmentObj.value.enrollment_id)
    deleteDialog.value = false
    enrollmentObj.value = {}
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa đăng ký thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa đăng ký', life: 3000 })
  }
}

const openChangeStatus = (data) => {
  enrollmentObj.value = { ...data }
  newStatus.value = data.status
  submitted.value = false
  changeStatusDialog.value = true
}

const changeStatus = async () => {
  submitted.value = true
  if (!newStatus.value) return
  try {
    const response = await api.post(`${endpoints.enrollments}${enrollmentObj.value.enrollment_id}/change-status/`, { status: newStatus.value })
    enrollments.value = enrollments.value.map(e => e.enrollment_id === enrollmentObj.value.enrollment_id ? response.data : e)
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
    const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    saveAs(blob, `enrollments_${new Date().toISOString().split('T')[0]}.xlsx`)
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xuất đăng ký thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xuất đăng ký', life: 3000 })
  }
}

const formatDate = (date) => {
  if (!date) return ''
  const d = new Date(date)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
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