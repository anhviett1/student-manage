<template>
  <div class="card">
    <Toast />
    <TabView v-if="canViewScores || isStudent">
      <!-- Tab for Students -->
      <TabPanel header="Điểm Của Tôi" v-if="isStudent">
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
              @change="loadMyScores"
            />
          </div>
          <InputText
            v-model="globalFilter"
            placeholder="Tìm theo môn học..."
            class="filter-search"
            @input="loadMyScores"
          />
        </div>
        <DataTable
          :value="myScores"
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
              <span>Không tìm thấy điểm số nào.</span>
            </div>
          </template>
          <template #loading>
            <div class="loading-message">
              <i class="pi pi-spin pi-spinner" />
              <span>Đang tải dữ liệu...</span>
            </div>
          </template>
          <Column field="subject.name" header="Môn Học" sortable style="width: 20%" />
          <Column field="semester.name" header="Học Kỳ" sortable style="width: 15%" />
          <Column field="midterm_score" header="Điểm Giữa Kỳ" sortable style="width: 15%" align="center">
            <template #body="{ data }">
              {{ formatScore(data.midterm_score) }}
            </template>
          </Column>
          <Column field="final_score" header="Điểm Cuối Kỳ" sortable style="width: 15%" align="center">
            <template #body="{ data }">
              {{ formatScore(data.final_score) }}
            </template>
          </Column>
          <Column field="total_score" header="Tổng Điểm" sortable style="width: 15%" align="center">
            <template #body="{ data }">
              <Tag :severity="getScoreSeverity(data.total_score)" :value="formatScore(data.total_score)" />
            </template>
          </Column>
          <Column field="notes" header="Ghi Chú" style="width: 20%" />
        </DataTable>
      </TabPanel>

      <!-- Tab for Admins/Teachers -->
      <TabPanel header="Quản Lý Điểm" v-if="isAdminOrTeacher">
        <div class="action-bar">
          <div class="action-buttons">
            <Button
              v-if="canEditScores"
              icon="pi pi-plus"
              label="Thêm Điểm"
              severity="primary"
              class="mr-2"
              @click="openNewDialog"
              v-tooltip.top="'Thêm điểm số mới'"
            />
            <Button
              v-if="canUploadScores"
              icon="pi pi-upload"
              label="Upload Sinh Viên"
              severity="info"
              class="mr-2"
              @click="openUploadStudentDialog"
              v-tooltip="'Tải lên danh sách sinh viên từ Excel'"
            />
            <Button
              v-if="canUploadScores"
              icon="pi pi-upload"
              label="Upload Điểm"
              severity="info"
              class="mr-2"
              @click="openUploadScoreDialog"
              v-tooltip="'Tải lên điểm số từ Excel'"
            />
            <Button
              v-if="canExportData"
              icon="pi pi-download"
              label="Export Điểm"
              severity="success"
              @click="exportScores"
              v-tooltip="'Xuất điểm số ra Excel'"
            />
            <Button
              icon="pi pi-file-excel"
              label="Tải File Mẫu"
              severity="secondary"
              outlined
              @click="downloadSampleExcel"
              v-tooltip="'Tải file mẫu Excel cho upload điểm'"
            />
          </div>
          <div class="filter-group">
            <Dropdown
              v-model="filters.status"
              :options="statusOptions"
              optionLabel="label"
              optionValue="value"
              placeholder="Lọc trạng thái"
              class="filter-dropdown mr-2"
              @change="loadScores"
            />
            <InputText
              v-model="filters.global"
              placeholder="Tìm sinh viên, môn học..."
              class="filter-search"
              @input="filterScores"
            />
          </div>
        </div>
        <DataTable
          :value="scores"
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
              <span>Không tìm thấy điểm số nào.</span>
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
          <Column field="semester.name" header="Học Kỳ" sortable style="width: 15%" />
          <Column field="midterm_score" header="Điểm Giữa Kỳ" sortable style="width: 10%" align="center">
            <template #body="{ data }">
              {{ formatScore(data.midterm_score) }}
            </template>
          </Column>
          <Column field="final_score" header="Điểm Cuối Kỳ" sortable style="width: 10%" align="center">
            <template #body="{ data }">
              {{ formatScore(data.final_score) }}
            </template>
          </Column>
          <Column field="total_score" header="Tổng Điểm" sortable style="width: 10%" align="center">
            <template #body="{ data }">
              <Tag :severity="getScoreSeverity(data.total_score)" :value="formatScore(data.total_score)" />
            </template>
          </Column>
          <Column field="status" header="Trạng Thái" sortable style="width: 10%" align="center">
            <template #body="{ data }">
              <Tag :severity="getStatusSeverity(data.status)" :value="getStatusLabel(data.status)" />
            </template>
          </Column>
          <Column field="notes" header="Ghi Chú" style="width: 15%" />
          <Column header="Hành Động" style="width: 10%" align="center">
            <template #body="{ data }">
              <Button
                v-if="canEditScores && !data.is_deleted"
                icon="pi pi-pencil"
                outlined
                rounded
                class="mr-2"
                severity="info"
                @click="editScore(data)"
                v-tooltip="'Sửa điểm'"
              />
              <Button
                v-if="canDeleteScores && !data.is_deleted"
                icon="pi pi-trash"
                outlined
                rounded
                severity="danger"
                class="mr-2"
                @click="confirmDelete(data)"
                v-tooltip="'Xóa mềm'"
              />
              <Button
                v-if="canDeleteScores && data.is_deleted"
                icon="pi pi-undo"
                outlined
                rounded
                severity="success"
                @click="restoreScore(data)"
                v-tooltip="'Khôi phục'"
              />
            </template>
          </Column>
        </DataTable>

        <!-- Dialog for Adding/Editing Score -->
        <Dialog
          v-model:visible="scoreDialog"
          :header="score.id ? 'Sửa Điểm' : 'Thêm Điểm'"
          :style="{ width: '500px' }"
          :modal="true"
          class="p-fluid"
        >
          <div class="field">
            <label for="student">Sinh Viên</label>
            <Dropdown
              id="student"
              v-model="score.student"
              :options="students"
              optionLabel="name"
              optionValue="student_id"
              placeholder="Chọn sinh viên"
              :class="{ 'p-invalid': errors.student }"
            />
            <small class="p-error" v-if="errors.student">{{ errors.student }}</small>
          </div>
          <div class="field">
            <label for="subject">Môn Học</label>
            <Dropdown
              id="subject"
              v-model="score.subject"
              :options="subjects"
              optionLabel="name"
              optionValue="subject_id"
              placeholder="Chọn môn học"
              :class="{ 'p-invalid': errors.subject }"
            />
            <small class="p-error" v-if="errors.subject">{{ errors.subject }}</small>
          </div>
          <div class="field">
            <label for="semester">Học Kỳ</label>
            <Dropdown
              id="semester"
              v-model="score.semester"
              :options="semesters"
              optionLabel="name"
              optionValue="semester_id"
              placeholder="Chọn học kỳ"
              :class="{ 'p-invalid': errors.semester }"
            />
            <small class="p-error" v-if="errors.semester">{{ errors.semester }}</small>
          </div>
          <div class="field">
            <label for="midterm_score">Điểm Giữa Kỳ</label>
            <InputNumber
              id="midterm_score"
              v-model="score.midterm_score"
              :min="0"
              :max="10"
              :step="0.1"
              :maxFractionDigits="2"
              placeholder="0.0 - 10.0"
              :class="{ 'p-invalid': errors.midterm_score }"
            />
            <small class="p-error" v-if="errors.midterm_score">{{ errors.midterm_score }}</small>
          </div>
          <div class="field">
            <label for="final_score">Điểm Cuối Kỳ</label>
            <InputNumber
              id="final_score"
              v-model="score.final_score"
              :min="0"
              :max="10"
              :step="0.1"
              :maxFractionDigits="2"
              placeholder="0.0 - 10.0"
              :class="{ 'p-invalid': errors.final_score }"
            />
            <small class="p-error" v-if="errors.final_score">{{ errors.final_score }}</small>
          </div>
          <div class="field">
            <label for="notes">Ghi Chú</label>
            <Textarea id="notes" v-model="score.notes" rows="3" placeholder="Nhập ghi chú nếu có" />
          </div>
          <div class="field">
            <label for="status">Trạng Thái</label>
            <Dropdown
              id="status"
              v-model="score.status"
              :options="statusOptions"
              optionLabel="label"
              optionValue="value"
              placeholder="Chọn trạng thái"
              :class="{ 'p-invalid': errors.status }"
            />
            <small class="p-error" v-if="errors.status">{{ errors.status }}</small>
          </div>
          <template #footer>
            <Button label="Hủy" icon="pi pi-times" text @click="hideDialog" />
            <Button label="Lưu" icon="pi pi-check" @click="saveScore" />
          </template>
        </Dialog>

        <!-- Dialog for Uploading Student List -->
        <Dialog
          v-model:visible="uploadStudentDialog"
          header="Tải Danh Sách Sinh Viên"
          :style="{ width: '400px' }"
          :modal="true"
        >
          <div class="field">
            <label>Chọn file Excel</label>
            <FileUpload
              mode="basic"
              accept=".xlsx,.xls"
              :maxFileSize="1000000"
              @change="onUploadStudentFile"
              chooseLabel="Chọn File"
              auto
              class="p-button-info"
            />
            <small class="p-info">File cần có cột: student_id, name</small>
          </div>
          <template #footer>
            <Button label="Đóng" icon="pi pi-times" text @click="uploadStudentDialog = false" />
          </template>
        </Dialog>

        <!-- Dialog for Uploading Scores -->
        <Dialog
          v-model:visible="uploadScoreDialog"
          header="Tải Điểm Số"
          :style="{ width: '400px' }"
          :modal="true"
        >
          <div class="field">
            <label>Chọn file Excel</label>
            <FileUpload
              mode="basic"
              accept=".xlsx,.xls"
              :maxFileSize="1000000"
              @change="onUploadScoreFile"
              chooseLabel="Chọn File"
              auto
              class="p-button-info"
            />
            <small class="p-info">File cần có cột: student_id, subject_id, semester_id, midterm_score, final_score, notes</small>
          </div>
          <template #footer>
            <Button label="Đóng" icon="pi pi-times" text @click="uploadScoreDialog = false" />
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
            <span>Bạn có chắc muốn xóa điểm của <b>{{ score.student?.name }}</b> cho môn <b>{{ score.subject?.name }}</b>?</span>
          </div>
          <template #footer>
            <Button label="Hủy" icon="pi pi-times" text @click="deleteDialog = false" />
            <Button label="Xóa" icon="pi pi-check" severity="danger" @click="deleteScore" />
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
import { saveAs } from 'file-saver'
import { useAuthStore } from '@/stores/auth'
import Tag from 'primevue/tag'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import InputNumber from 'primevue/inputnumber'


const toast = useToast()
const {
  isTeacher,
  isStudent,
  isAdminOrTeacher,
  canViewScores,
  canEditScores,
  canDeleteScores,
  canUploadScores,
  canExportData,
} = usePermissions()
const myScores = ref([])
const scores = ref([])
const semesters = ref([])
const students = ref([])
const subjects = ref([])
const loading = ref(false)
const scoreDialog = ref(false)
const uploadStudentDialog = ref(false)
const uploadScoreDialog = ref(false)
const deleteDialog = ref(false)
const score = ref({})
const errors = ref({})
const selectedSemester = ref(null)
const globalFilter = ref('')
const filters = ref({
  status: null,
  global: ''
})

const statusOptions = [
  { label: 'Đang hoạt động', value: 'active' },
  { label: 'Không hoạt động', value: 'inactive' },
  { label: 'Đang xử lý', value: 'pending' }
]

onMounted(async () => {
  if (canViewScores.value || isStudent.value) {
    await loadSemesters()
  }

  if (isAdminOrTeacher.value) {
    await loadStudents()
    await loadSubjects()
    await loadScores()
  }

  if (isStudent.value) {
    await loadMyScores()
  }
})

const loadSemesters = async () => {
  try {
    const response = await api.get(endpoints.semesters, { params: { active: true } })
    
    // Ensure semesters.value is always an array
    if (response.data && Array.isArray(response.data)) {
      semesters.value = response.data
    } else if (response.data && response.data.results && Array.isArray(response.data.results)) {
      semesters.value = response.data.results
    } else if (response.data && response.data.data && Array.isArray(response.data.data)) {
      semesters.value = response.data.data
    } else {
      semesters.value = []
    }
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải học kỳ', life: 3000 })
    semesters.value = []
  }
}

const loadStudents = async () => {
  try {
    const response = await api.get(endpoints.students)
    
    // Ensure students.value is always an array
    if (response.data && Array.isArray(response.data)) {
      students.value = response.data
    } else if (response.data && response.data.results && Array.isArray(response.data.results)) {
      students.value = response.data.results
    } else if (response.data && response.data.data && Array.isArray(response.data.data)) {
      students.value = response.data.data
    } else {
      students.value = []
    }
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách sinh viên', life: 3000 })
    students.value = []
  }
}

const loadSubjects = async () => {
  try {
    const response = await api.get(endpoints.subjects)
    
    // Ensure subjects.value is always an array
    if (response.data && Array.isArray(response.data)) {
      subjects.value = response.data
    } else if (response.data && response.data.results && Array.isArray(response.data.results)) {
      subjects.value = response.data.results
    } else if (response.data && response.data.data && Array.isArray(response.data.data)) {
      subjects.value = response.data.data
    } else {
      subjects.value = []
    }
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách môn học', life: 3000 })
    subjects.value = []
  }
}

const loadMyScores = async () => {
  try {
    loading.value = true
    const params = {}
    if (selectedSemester.value) params.semester_id = selectedSemester.value
    if (globalFilter.value) params.search = globalFilter.value
    // Backend sẽ tự lọc điểm của user đang đăng nhập dựa trên token
    const response = await api.get(endpoints.scores, { params })
    myScores.value = response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải điểm số', life: 3000 })
  } finally {
    loading.value = false
  }
}

const loadScores = async () => {
  try {
    loading.value = true
    const params = {}
    if (filters.value.status) params.status = filters.value.status
    if (filters.value.global) params.search = filters.value.global
    const response = await api.get(endpoints.scores, { params })
    scores.value = response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải điểm số', life: 3000 })
  } finally {
    loading.value = false
  }
}

const filterScores = () => {
  loadScores()
}

const openNewDialog = () => {
  score.value = { status: 'active' }
  errors.value = {}
  scoreDialog.value = true
}

const editScore = (data) => {
  score.value = { ...data, student: data.student.student_id, subject: data.subject.subject_id, semester: data.semester.semester_id }
  errors.value = {}
  scoreDialog.value = true
}

const hideDialog = () => {
  scoreDialog.value = false
  score.value = {}
  errors.value = {}
}

const validateScore = () => {
  errors.value = {}
  if (!score.value.student) errors.value.student = 'Vui lòng chọn sinh viên'
  if (!score.value.subject) errors.value.subject = 'Vui lòng chọn môn học'
  if (!score.value.semester) errors.value.semester = 'Vui lòng chọn học kỳ'
  if (score.value.midterm_score && (score.value.midterm_score < 0 || score.value.midterm_score > 10)) {
    errors.value.midterm_score = 'Điểm giữa kỳ từ 0.0 - 10.0'
  }
  if (score.value.final_score && (score.value.final_score < 0 || score.value.final_score > 10)) {
    errors.value.final_score = 'Điểm cuối kỳ từ 0.0 - 10.0'
  }
  if (!score.value.status) errors.value.status = 'Vui lòng chọn trạng thái'
}

const saveScore = async () => {
  validateScore()
  if (Object.keys(errors.value).length > 0) return

  try {
    const payload = { ...score.value }
    if (score.value.id) {
      const response = await api.patch(`${endpoints.scores}${score.value.id}/`, payload)
      scores.value = scores.value.map(s => s.id === score.value.id ? response.data : s)
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật điểm số thành công', life: 3000 })
    } else {
      const response = await api.post(endpoints.scores, payload)
      scores.value.push(response.data)
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Thêm điểm số thành công', life: 3000 })
    }
    hideDialog()
  } catch (error) {
    const errorMsg = error.response?.data?.detail || Object.values(error.response?.data || {}).join(', ') || 'Không thể lưu điểm số'
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errorMsg, life: 3000 })
  }
}

const confirmDelete = (data) => {
  score.value = data
  deleteDialog.value = true
}

const deleteScore = async () => {
  try {
    await api.delete(`${endpoints.scores}${score.value.id}/`)
    scores.value = scores.value.filter(s => s.id !== score.value.id)
    deleteDialog.value = false
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa điểm số thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa điểm số', life: 3000 })
  }
}

const restoreScore = async (data) => {
  try {
    const response = await api.post(`${endpoints.scores}${data.id}/restore/`)
    scores.value = scores.value.map(s => s.id === data.id ? response.data.data : s)
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Khôi phục điểm số thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: error.response?.data?.error || 'Không thể khôi phục điểm số', life: 3000 })
  }
}

const openUploadStudentDialog = () => {
  uploadStudentDialog.value = true
}

const openUploadScoreDialog = () => {
  uploadScoreDialog.value = true
}

const onUploadStudentFile = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  const formData = new FormData()
  formData.append('file', file)
  try {
    const response = await api.post(endpoints.scoreManagement, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    toast.add({ severity: 'success', summary: 'Thành công', detail: response.data.message, life: 3000 })
    await loadStudents()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: error.response?.data?.error || 'Không thể tải file', life: 3000 })
  }
}

const onUploadScoreFile = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  const formData = new FormData()
  formData.append('file', file)
  try {
    const response = await api.post(endpoints.scoreManagement, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    toast.add({ severity: 'success', summary: 'Thành công', detail: response.data.message, life: 3000 })
    await loadScores()
  } catch (error) {
    const errors = error.response?.data?.errors || [error.response?.data?.error || 'Không thể tải file']
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errors.join('; '), life: 5000 })
  }
}

const exportScores = async () => {
  try {
    const response = await api.get(`${endpoints.scores}export/`, { responseType: 'blob' })
    saveAs(response.data, 'scores.xlsx')
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xuất điểm số thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xuất điểm số', life: 3000 })
  }
}

const downloadSampleExcel = () => {
  const sampleData = [
    { student_id: 'S001', subject_id: 'SUBJ001', semester_id: 'HK001', midterm_score: 8.5, final_score: 9.0, notes: 'Hoàn thành tốt' }
  ]
  const blob = new Blob([JSON.stringify(sampleData, null, 2)], { type: 'application/json' })
  saveAs(blob, 'score_sample.json')
}

const formatScore = (score) => {
  return score != null ? score.toFixed(2) : '-'
}

const getScoreSeverity = (score) => {
  if (score == null) return 'info'
  if (score < 5) return 'danger'
  if (score < 7) return 'warning'
  return 'success'
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

.filter-bar, .action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
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
  flex-wrap: wrap;
}

.empty-message, .loading-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
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

.field {
  margin-bottom: 1.2rem;
}

.field label {
  display: block;
  margin-bottom: 0.3rem;
  font-weight: 500;
}

.confirmation-content {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
}

.p-info {
  color: #666;
  font-size: 0.85rem;
}
.access-denied {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #ef4444;
}
</style>