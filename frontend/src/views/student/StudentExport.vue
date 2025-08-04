<template>
  <div class="student-export-section" aria-label="Phần xuất dữ liệu sinh viên">
    <Toast aria-live="polite" />
    <ConfirmDialog aria-live="assertive" />
    
    <div class="card">
      <h2>Xuất Dữ Liệu Sinh Viên</h2>
      
      <div class="export-filters">
        <div class="filter-group">
          <label for="status-filter">Trạng thái:</label>
          <Dropdown
            id="status-filter"
            v-model="filters.status"
            :options="statusOptions"
            optionLabel="label"
            optionValue="value"
            placeholder="Tất cả trạng thái"
            class="filter-dropdown"
            aria-label="Lọc theo trạng thái"
          />
        </div>
        
        <div class="filter-group">
          <label for="department-filter">Khoa:</label>
          <Dropdown
            id="department-filter"
            v-model="filters.department"
            :options="departments"
            optionLabel="name"
            optionValue="id"
            placeholder="Tất cả khoa"
            class="filter-dropdown"
            aria-label="Lọc theo khoa"
          />
        </div>
        
        <div class="filter-group">
          <label for="year-filter">Năm học:</label>
          <Dropdown
            id="year-filter"
            v-model="filters.year"
            :options="yearOptions"
            optionLabel="label"
            optionValue="value"
            placeholder="Tất cả năm học"
            class="filter-dropdown"
            aria-label="Lọc theo năm học"
          />
        </div>
      </div>
      
      <div class="export-options">
        <h3>Tùy chọn xuất:</h3>
        
        <div class="format-selection">
          <label>Định dạng file:</label>
          <div class="format-buttons">
            <Button
              v-for="format in exportFormats"
              :key="format.value"
              :label="format.label"
              :icon="format.icon"
              :severity="selectedFormat === format.value ? 'primary' : 'secondary'"
              :outlined="selectedFormat !== format.value"
              @click="selectedFormat = format.value"
              class="format-button"
              :aria-label="`Chọn định dạng ${format.label}`"
            />
          </div>
        </div>
        
        <div class="field-selection">
          <label>Trường dữ liệu:</label>
          <div class="field-checkboxes">
            <div v-for="field in availableFields" :key="field.value" class="field-checkbox">
              <Checkbox
                :modelValue="selectedFields.includes(field.value)"
                @update:modelValue="toggleField(field.value)"
                :binary="true"
                :inputId="field.value"
              />
              <label :for="field.value">{{ field.label }}</label>
            </div>
          </div>
        </div>
        
        <div class="export-actions">
          <Button
            icon="pi pi-download"
            label="Xuất dữ liệu"
            severity="success"
            :loading="exporting"
            :disabled="selectedFields.length === 0 || exporting"
            @click="exportData"
            class="mr-2"
            aria-label="Xuất dữ liệu sinh viên"
          />
          <Button
            icon="pi pi-refresh"
            label="Làm mới"
            severity="secondary"
            outlined
            @click="resetFilters"
            :disabled="exporting"
            aria-label="Làm mới bộ lọc"
          />
        </div>
      </div>
      
      <div v-if="exportHistory.length > 0" class="export-history">
        <h3>Lịch sử xuất:</h3>
        <DataTable :value="exportHistory" class="p-datatable-sm">
          <Column field="filename" header="Tên file" />
          <Column field="format" header="Định dạng" />
          <Column field="created_at" header="Thời gian" />
          <Column field="status" header="Trạng thái">
            <template #body="{ data }">
              <Tag :severity="getStatusSeverity(data.status)" :value="getStatusLabel(data.status)" />
            </template>
          </Column>
          <Column header="Hành động">
            <template #body="{ data }">
              <Button
                v-if="data.status === 'completed'"
                icon="pi pi-download"
                rounded
                outlined
                severity="info"
                @click="downloadFile(data)"
                aria-label="Tải xuống file"
              />
            </template>
          </Column>
        </DataTable>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import { api, endpoints } from '@/services/api'

const toast = useToast()
const confirm = useConfirm()

// Reactive data
const filters = reactive({
  status: null,
  department: null,
  year: null
})

const selectedFormat = ref('excel')
const selectedFields = ref(['student_id', 'full_name', 'email', 'major', 'gpa', 'status'])
const exporting = ref(false)
const departments = ref([])
const exportHistory = ref([])

// Options
const statusOptions = ref([
  { label: 'Tất cả', value: null },
  { label: 'Đang học', value: 'active' },
  { label: 'Tốt nghiệp', value: 'graduated' },
  { label: 'Tạm nghỉ', value: 'suspended' },
  { label: 'Thôi học', value: 'dropped' }
])

const yearOptions = ref([
  { label: 'Tất cả', value: null },
  { label: '2024', value: '2024' },
  { label: '2023', value: '2023' },
  { label: '2022', value: '2022' },
  { label: '2021', value: '2021' }
])

const exportFormats = ref([
  { label: 'Excel', value: 'excel', icon: 'pi pi-file-excel' },
  { label: 'CSV', value: 'csv', icon: 'pi pi-file' },
  { label: 'PDF', value: 'pdf', icon: 'pi pi-file-pdf' }
])

const availableFields = ref([
  { label: 'Mã sinh viên', value: 'student_id' },
  { label: 'Họ và tên', value: 'full_name' },
  { label: 'Email', value: 'email' },
  { label: 'Số điện thoại', value: 'phone' },
  { label: 'Ngày sinh', value: 'birth_date' },
  { label: 'Giới tính', value: 'gender' },
  { label: 'Địa chỉ', value: 'address' },
  { label: 'Khoa', value: 'department' },
  { label: 'Chuyên ngành', value: 'major' },
  { label: 'GPA', value: 'gpa' },
  { label: 'Trạng thái', value: 'status' },
  { label: 'Ngày nhập học', value: 'enrollment_date' },
  { label: 'Ngày tạo', value: 'created_at' },
  { label: 'Ngày cập nhật', value: 'updated_at' }
])

// Methods
const toggleField = (fieldValue) => {
  const index = selectedFields.value.indexOf(fieldValue)
  if (index > -1) {
    selectedFields.value.splice(index, 1)
  } else {
    selectedFields.value.push(fieldValue)
  }
}

const exportData = async () => {
  if (selectedFields.value.length === 0) {
    toast.add({
      severity: 'warn',
      summary: 'Cảnh báo',
      detail: 'Vui lòng chọn ít nhất một trường dữ liệu',
      life: 3000
    })
    return
  }
  
  exporting.value = true
  
  try {
    const params = {
      format: selectedFormat.value,
      fields: selectedFields.value.join(','),
      ...filters
    }
    
    // Loại bỏ các giá trị null
    Object.keys(params).forEach(key => {
      if (params[key] === null) {
        delete params[key]
      }
    })
    
    const response = await api.get(endpoints.studentsExport, { params })
    
    // Tạo và tải xuống file
    const blob = new Blob([response.data], {
      type: getMimeType(selectedFormat.value)
    })
    
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `students_export_${new Date().toISOString().split('T')[0]}.${getFileExtension(selectedFormat.value)}`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    toast.add({
      severity: 'success',
      summary: 'Thành công',
      detail: 'Xuất dữ liệu sinh viên thành công',
      life: 3000
    })
    
    // Cập nhật lịch sử xuất
    await loadExportHistory()
    
  } catch (error) {
    console.error('Export error:', error)
    let errorMessage = 'Có lỗi xảy ra khi xuất dữ liệu'
    
    if (error.response?.data?.detail) {
      errorMessage = error.response.data.detail
    }
    
    toast.add({
      severity: 'error',
      summary: 'Lỗi',
      detail: errorMessage,
      life: 5000
    })
  } finally {
    exporting.value = false
  }
}

const getMimeType = (format) => {
  switch (format) {
    case 'excel':
      return 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    case 'csv':
      return 'text/csv'
    case 'pdf':
      return 'application/pdf'
    default:
      return 'application/octet-stream'
  }
}

const getFileExtension = (format) => {
  switch (format) {
    case 'excel':
      return 'xlsx'
    case 'csv':
      return 'csv'
    case 'pdf':
      return 'pdf'
    default:
      return 'txt'
  }
}

const resetFilters = () => {
  filters.status = null
  filters.department = null
  filters.year = null
  selectedFields.value = ['student_id', 'full_name', 'email', 'major', 'gpa', 'status']
  selectedFormat.value = 'excel'
}

const loadDepartments = async () => {
  try {
    const response = await api.get(endpoints.departments)
    departments.value = response.data.results || response.data
  } catch (error) {
    console.error('Error loading departments:', error)
  }
}

const loadExportHistory = async () => {
  try {
    const response = await api.get(`${endpoints.studentsExport}history/`)
    exportHistory.value = response.data
  } catch (error) {
    console.error('Error loading export history:', error)
  }
}

const downloadFile = (fileData) => {
  // Implement file download logic
  toast.add({
    severity: 'info',
    summary: 'Thông báo',
    detail: 'Tính năng tải xuống file sẽ được cập nhật',
    life: 3000
  })
}

const getStatusSeverity = (status) => {
  switch (status) {
    case 'completed':
      return 'success'
    case 'processing':
      return 'info'
    case 'failed':
      return 'danger'
    default:
      return 'warning'
  }
}

const getStatusLabel = (status) => {
  switch (status) {
    case 'completed':
      return 'Hoàn thành'
    case 'processing':
      return 'Đang xử lý'
    case 'failed':
      return 'Thất bại'
    default:
      return 'Chờ xử lý'
  }
}

// Lifecycle
onMounted(() => {
  loadDepartments()
  loadExportHistory()
})
</script>

<style scoped>
.student-export-section {
  padding: 1rem;
}

.card {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card h2 {
  margin-bottom: 2rem;
  color: #333;
  font-size: 1.5rem;
}

.export-filters {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 500;
  color: #555;
}

.filter-dropdown {
  width: 100%;
}

.export-options {
  margin-bottom: 2rem;
}

.export-options h3 {
  margin-bottom: 1rem;
  color: #333;
  font-size: 1.2rem;
}

.format-selection,
.field-selection {
  margin-bottom: 1.5rem;
}

.format-selection label,
.field-selection label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #555;
}

.format-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.format-button {
  min-width: 100px;
}

.field-checkboxes {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.5rem;
}

.field-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border-radius: 4px;
  background: #f8f9fa;
}

.field-checkbox label {
  margin: 0;
  cursor: pointer;
  font-weight: normal;
}

.export-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.export-history {
  margin-top: 2rem;
}

.export-history h3 {
  margin-bottom: 1rem;
  color: #333;
  font-size: 1.2rem;
}

@media (max-width: 768px) {
  .export-filters {
    grid-template-columns: 1fr;
  }
  
  .format-buttons {
    flex-direction: column;
  }
  
  .field-checkboxes {
    grid-template-columns: 1fr;
  }
  
  .export-actions {
    flex-direction: column;
  }
}
</style>
