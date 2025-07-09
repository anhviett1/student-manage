<template>
  <div class="card" v-if="canViewSemesters">
    <Toast />
    <div class="header">
      <h2>Quản Lý Học Kỳ</h2>
      <div class="action-buttons">
        <Button
          icon="pi pi-filter"
          label="Học Kỳ Active"
          severity="info"
          class="mr-2"
          @click="loadActiveSemesters"
          v-tooltip="'Xem các học kỳ đang hoạt động'"
        />
        <Button
          v-if="canEditSemesters"
          icon="pi pi-plus"
          label="Thêm Học Kỳ"
          severity="primary"
          @click="openNew"
          v-tooltip="'Thêm học kỳ mới'"
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
          @change="loadSemesters"
        />
        <InputText
          v-model="filters.global"
          placeholder="Tìm mã, tên, năm học..."
          class="filter-search"
          @input="filterSemesters"
        />
      </div>
    </div>

    <TabView>
      <TabPanel header="Học kỳ đang hoạt động">
        <DataTable
          :value="activeSemesters"
          :loading="loading"
          dataKey="semester_id"
          :paginator="true"
          :rows="10"
          :rowsPerPageOptions="[5, 10, 20]"
          responsiveLayout="scroll"
          class="p-datatable-sm"
        >
          <template #empty>
            <div class="empty-message">
              <i class="pi pi-info-circle" />
              <span>Không tìm thấy học kỳ nào.</span>
            </div>
          </template>
          <template #loading>
            <div class="loading-message">
              <i class="pi pi-spin pi-spinner" />
              <span>Đang tải dữ liệu...</span>
            </div>
          </template>
          <Column field="semester_id" header="Mã Học Kỳ" sortable style="width: 12%" />
          <Column field="name" header="Tên Học Kỳ" sortable style="width: 18%" />
          <Column field="academic_year" header="Năm Học" sortable style="width: 12%" />
          <Column field="start_date" header="Ngày Bắt Đầu" sortable style="width: 12%" align="center">
            <template #body="{ data }">
              {{ formatDate(data.start_date) }}
            </template>
          </Column>
          <Column field="end_date" header="Ngày Kết Thúc" sortable style="width: 12%" align="center">
            <template #body="{ data }">
              {{ formatDate(data.end_date) }}
            </template>
          </Column>
          <Column field="status" header="Trạng Thái" sortable style="width: 12%" align="center">
            <template #body="{ data }">
              <Tag :severity="getStatusSeverity(data.status)" :value="getStatusLabel(data.status)" />
            </template>
          </Column>
          <Column field="is_active" header="Đang Hoạt Động" sortable style="width: 12%" align="center">
            <template #body="{ data }">
              <Tag :severity="data.is_active ? 'success' : 'warning'" :value="data.is_active ? 'Active' : 'Inactive'" />
            </template>
          </Column>
          <Column header="Hành Động" style="width: 12%" align="center">
            <template #body="{ data }">
              <Button
                v-if="canEditSemesters && !data.is_deleted"
                icon="pi pi-pencil"
                outlined
                rounded
                class="mr-2"
                severity="info"
                @click="editSemester(data)"
                v-tooltip="'Sửa học kỳ'"
              />
              <Button
                v-if="canDeleteSemesters && !data.is_deleted"
                icon="pi pi-trash"
                outlined
                rounded
                severity="danger"
                class="mr-2"
                @click="confirmDelete(data)"
                v-tooltip="'Xóa mềm'"
              />
              <Button
                v-if="canDeleteSemesters && data.is_deleted"
                icon="pi pi-undo"
                outlined
                rounded
                severity="success"
                @click="restoreSemester(data)"
                v-tooltip="'Khôi phục'"
              />
              <Button
                v-if="canEditSemesters"
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
      </TabPanel>
      <TabPanel header="Học kỳ đã kết thúc">
        <DataTable
          :value="finishedSemesters"
          :loading="loading"
          dataKey="semester_id"
          :paginator="true"
          :rows="10"
          :rowsPerPageOptions="[5, 10, 20]"
          responsiveLayout="scroll"
          class="p-datatable-sm"
        >
          <template #empty>
            <div class="empty-message">
              <i class="pi pi-info-circle" />
              <span>Không tìm thấy học kỳ nào.</span>
            </div>
          </template>
          <template #loading>
            <div class="loading-message">
              <i class="pi pi-spin pi-spinner" />
              <span>Đang tải dữ liệu...</span>
            </div>
          </template>
          <Column field="semester_id" header="Mã Học Kỳ" sortable style="width: 12%" />
          <Column field="name" header="Tên Học Kỳ" sortable style="width: 18%" />
          <Column field="academic_year" header="Năm Học" sortable style="width: 12%" />
          <Column field="start_date" header="Ngày Bắt Đầu" sortable style="width: 12%" align="center">
            <template #body="{ data }">
              {{ formatDate(data.start_date) }}
            </template>
          </Column>
          <Column field="end_date" header="Ngày Kết Thúc" sortable style="width: 12%" align="center">
            <template #body="{ data }">
              {{ formatDate(data.end_date) }}
            </template>
          </Column>
          <Column field="status" header="Trạng Thái" sortable style="width: 12%" align="center">
            <template #body="{ data }">
              <Tag :severity="getStatusSeverity(data.status)" :value="getStatusLabel(data.status)" />
            </template>
          </Column>
          <Column field="is_active" header="Đang Hoạt Động" sortable style="width: 12%" align="center">
            <template #body="{ data }">
              <Tag :severity="data.is_active ? 'success' : 'warning'" :value="data.is_active ? 'Active' : 'Inactive'" />
            </template>
          </Column>
          <Column header="Hành Động" style="width: 12%" align="center">
            <template #body="{ data }">
              <Button
                v-if="canEditSemesters && !data.is_deleted"
                icon="pi pi-pencil"
                outlined
                rounded
                class="mr-2"
                severity="info"
                @click="editSemester(data)"
                v-tooltip="'Sửa học kỳ'"
              />
              <Button
                v-if="canDeleteSemesters && !data.is_deleted"
                icon="pi pi-trash"
                outlined
                rounded
                severity="danger"
                class="mr-2"
                @click="confirmDelete(data)"
                v-tooltip="'Xóa mềm'"
              />
              <Button
                v-if="canDeleteSemesters && data.is_deleted"
                icon="pi pi-undo"
                outlined
                rounded
                severity="success"
                @click="restoreSemester(data)"
                v-tooltip="'Khôi phục'"
              />
              <Button
                v-if="canEditSemesters"
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
      </TabPanel>
      <TabPanel header="Thêm mới học kỳ">
        <form @submit.prevent="addSemester">
          <!-- ... -->
        </form>
      </TabPanel>
    </TabView>

    <!-- Dialog for Adding/Editing Semester -->
    <Dialog
      v-model:visible="semesterDialog"
      :header="semester.semester_id ? 'Sửa Học Kỳ' : 'Thêm Học Kỳ'"
      :style="{ width: '600px' }"
      :modal="true"
      class="p-fluid"
    >
      <div class="form-section">
        <h4>Thông Tin Cơ Bản</h4>
        <div class="field">
          <label for="semester_id">Mã Học Kỳ</label>
          <InputText
            id="semester_id"
            v-model.trim="semester.semester_id"
            :disabled="!!semester.semester_id"
            placeholder="VD: HK001"
            :class="{ 'p-invalid': errors.semester_id }"
          />
          <small class="p-error" v-if="errors.semester_id">{{ errors.semester_id }}</small>
        </div>
        <div class="field">
          <label for="name">Tên Học Kỳ</label>
          <InputText
            id="name"
            v-model.trim="semester.name"
            placeholder="VD: Học kỳ 1"
            :class="{ 'p-invalid': errors.name }"
          />
          <small class="p-error" v-if="errors.name">{{ errors.name }}</small>
        </div>
        <div class="field">
          <label for="academic_year">Năm Học</label>
          <InputText
            id="academic_year"
            v-model.trim="semester.academic_year"
            placeholder="VD: 2023-2024"
            :class="{ 'p-invalid': errors.academic_year }"
          />
          <small class="p-error" v-if="errors.academic_year">{{ errors.academic_year }}</small>
        </div>
        <div class="field">
          <label for="description">Mô Tả</label>
          <Textarea
            id="description"
            v-model="semester.description"
            rows="3"
            placeholder="Mô tả học kỳ (tùy chọn)"
          />
        </div>
        <div class="field">
          <label for="notes">Ghi Chú</label>
          <Textarea
            id="notes"
            v-model="semester.notes"
            rows="3"
            placeholder="Ghi chú thêm (tùy chọn)"
          />
        </div>
      </div>

      <div class="form-section">
        <h4>Thời Gian</h4>
        <div class="field">
          <label for="start_date">Ngày Bắt Đầu</label>
          <Calendar
            id="start_date"
            v-model="semester.start_date"
            :showIcon="true"
            dateFormat="yy-mm-dd"
            placeholder="Chọn ngày"
            :class="{ 'p-invalid': errors.start_date }"
          />
          <small class="p-error" v-if="errors.start_date">{{ errors.start_date }}</small>
        </div>
        <div class="field">
          <label for="end_date">Ngày Kết Thúc</label>
          <Calendar
            id="end_date"
            v-model="semester.end_date"
            :showIcon="true"
            dateFormat="yy-mm-dd"
            placeholder="Chọn ngày"
            :class="{ 'p-invalid': errors.end_date }"
          />
          <small class="p-error" v-if="errors.end_date">{{ errors.end_date }}</small>
        </div>
        <div class="field">
          <label for="registration_start">Ngày Bắt Đầu Đăng Ký</label>
          <Calendar
            id="registration_start"
            v-model="semester.registration_start"
            :showIcon="true"
            dateFormat="yy-mm-dd"
            placeholder="Chọn ngày"
            :class="{ 'p-invalid': errors.registration_start }"
          />
          <small class="p-error" v-if="errors.registration_start">{{ errors.registration_start }}</small>
        </div>
        <div class="field">
          <label for="registration_end">Ngày Kết Thúc Đăng Ký</label>
          <Calendar
            id="registration_end"
            v-model="semester.registration_end"
            :showIcon="true"
            dateFormat="yy-mm-dd"
            placeholder="Chọn ngày"
            :class="{ 'p-invalid': errors.registration_end }"
          />
          <small class="p-error" v-if="errors.registration_end">{{ errors.registration_end }}</small>
        </div>
        <div class="field">
          <label for="add_drop_deadline">Hạn Chót Thêm/Xóa Môn</label>
          <Calendar
            id="add_drop_deadline"
            v-model="semester.add_drop_deadline"
            :showIcon="true"
            dateFormat="yy-mm-dd"
            placeholder="Chọn ngày"
            :class="{ 'p-invalid': errors.add_drop_deadline }"
          />
          <small class="p-error" v-if="errors.add_drop_deadline">{{ errors.add_drop_deadline }}</small>
        </div>
      </div>

      <div class="form-section">
        <h4>Thông Tin Học Tập</h4>
        <div class="field">
          <label for="total_credits">Tổng Số Tín Chỉ</label>
          <InputNumber
            id="total_credits"
            v-model="semester.total_credits"
            :min="0"
            placeholder="VD: 20"
            :class="{ 'p-invalid': errors.total_credits }"
          />
          <small class="p-error" v-if="errors.total_credits">{{ errors.total_credits }}</small>
        </div>
        <div class="field">
          <label for="min_credits">Số Tín Chỉ Tối Thiểu</label>
          <InputNumber
            id="min_credits"
            v-model="semester.min_credits"
            :min="0"
            placeholder="VD: 12"
            :class="{ 'p-invalid': errors.min_credits }"
          />
          <small class="p-error" v-if="errors.min_credits">{{ errors.min_credits }}</small>
        </div>
        <div class="field">
          <label for="max_credits">Số Tín Chỉ Tối Đa</label>
          <InputNumber
            id="max_credits"
            v-model="semester.max_credits"
            :min="0"
            placeholder="VD: 24"
            :class="{ 'p-invalid': errors.max_credits }"
          />
          <small class="p-error" v-if="errors.max_credits">{{ errors.max_credits }}</small>
        </div>
      </div>

      <div class="form-section">
        <h4>Thông Tin Tài Chính</h4>
        <div class="field">
          <label for="tuition_deadline">Hạn Nộp Học Phí</label>
          <Calendar
            id="tuition_deadline"
            v-model="semester.tuition_deadline"
            :showIcon="true"
            dateFormat="yy-mm-dd"
            placeholder="Chọn ngày"
            :class="{ 'p-invalid': errors.tuition_deadline }"
          />
          <small class="p-error" v-if="errors.tuition_deadline">{{ errors.tuition_deadline }}</small>
        </div>
        <div class="field">
          <label for="late_fee_start">Ngày Bắt Đầu Tính Phí Trễ</label>
          <Calendar
            id="late_fee_start"
            v-model="semester.late_fee_start"
            :showIcon="true"
            dateFormat="yy-mm-dd"
            placeholder="Chọn ngày"
            :class="{ 'p-invalid': errors.late_fee_start }"
          />
          <small class="p-error" v-if="errors.late_fee_start">{{ errors.late_fee_start }}</small>
        </div>
        <div class="field">
          <label for="late_fee_amount">Phí Trễ Hạn</label>
          <InputNumber
            id="late_fee_amount"
            v-model="semester.late_fee_amount"
            :min="0"
            :step="0.01"
            :maxFractionDigits="2"
            placeholder="VD: 500000.00"
            :class="{ 'p-invalid': errors.late_fee_amount }"
          />
          <small class="p-error" v-if="errors.late_fee_amount">{{ errors.late_fee_amount }}</small>
        </div>
      </div>

      <div class="form-section">
        <h4>Trạng Thái</h4>
        <div class="field">
          <label for="status">Trạng Thái</label>
          <Dropdown
            id="status"
            v-model="semester.status"
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
          <InputSwitch id="is_active" v-model="semester.is_active" />
        </div>
      </div>

      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="hideDialog" />
        <Button label="Lưu" icon="pi pi-check" @click="saveSemester" />
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
        <span>Bạn có chắc muốn xóa học kỳ <b>{{ semester.name }}</b>?</span>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="deleteDialog = false" />
        <Button label="Xóa" icon="pi pi-check" severity="danger" @click="deleteSemester" />
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
  <div v-else class="access-denied">
    <p>Bạn không có quyền truy cập trang này.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import api, { endpoints } from '@/services/api'
import Tag from 'primevue/tag'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import InputNumber from 'primevue/inputnumber'
import InputSwitch from 'primevue/inputswitch'
import MultiSelect from 'primevue/multiselect'

const toast = useToast()

const semesters = ref([])
const semesterDialog = ref(false)
const deleteDialog = ref(false)
const changeStatusDialog = ref(false)
const semester = ref({})
const newStatus = ref('')
const submitted = ref(false)
const loading = ref(false)
const errors = ref({})
const filters = ref({
  status: null,
  global: ''
})

const statusOptions = [
  { label: 'Sắp tới', value: 'upcoming' },
  { label: 'Đang diễn ra', value: 'current' },
  { label: 'Đã kết thúc', value: 'completed' },
  { label: 'Đã hủy', value: 'cancelled' }
]

onMounted(async () => {
  // Removed: if (canViewSemesters.value) {
    await loadSemesters()
  // }
})

const loadSemesters = async () => {
  try {
    loading.value = true
    const params = {}
    if (filters.value.status) params.status = filters.value.status
    if (filters.value.global) params.search = filters.value.global
    const response = await api.get(endpoints.semesters, { params })
    semesters.value = Array.isArray(response.data.results) ? response.data.results : response.data
    console.log('semesters.value:', semesters.value)
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách học kỳ', life: 3000 })
  } finally {
    loading.value = false
  }
}

const loadActiveSemesters = async () => {
  try {
    loading.value = true
    const response = await api.get(endpoints.semesters, { params: { active: true } })
    semesters.value = response.data
    toast.add({ severity: 'info', summary: 'Thành công', detail: 'Hiển thị các học kỳ đang hoạt động', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải học kỳ active', life: 3000 })
  } finally {
    loading.value = false
  }
}

const filterSemesters = () => {
  loadSemesters()
}

const openNew = () => {
  semester.value = { status: 'upcoming', is_active: true }
  errors.value = {}
  semesterDialog.value = true
}

const editSemester = (data) => {
  semester.value = {
    ...data,
    start_date: new Date(data.start_date),
    end_date: new Date(data.end_date),
    registration_start: new Date(data.registration_start),
    registration_end: new Date(data.registration_end),
    add_drop_deadline: new Date(data.add_drop_deadline),
    tuition_deadline: new Date(data.tuition_deadline),
    late_fee_start: new Date(data.late_fee_start)
  }
  errors.value = {}
  semesterDialog.value = true
}

const hideDialog = () => {
  semesterDialog.value = false
  semester.value = {}
  errors.value = {}
}

const confirmDelete = (data) => {
  semester.value = data
  deleteDialog.value = true
}

const openChangeStatus = (data) => {
  semester.value = data
  newStatus.value = data.status
  submitted.value = false
  changeStatusDialog.value = true
}

const validateSemester = () => {
  errors.value = {}
  if (!semester.value.semester_id?.trim()) errors.value.semester_id = 'Vui lòng nhập mã học kỳ'
  if (!semester.value.name?.trim()) errors.value.name = 'Vui lòng nhập tên học kỳ'
  if (!semester.value.academic_year?.trim()) errors.value.academic_year = 'Vui lòng nhập năm học'
  if (!semester.value.start_date) errors.value.start_date = 'Vui lòng chọn ngày bắt đầu'
  if (!semester.value.end_date) errors.value.end_date = 'Vui lòng chọn ngày kết thúc'
  if (!semester.value.registration_start) errors.value.registration_start = 'Vui lòng chọn ngày bắt đầu đăng ký'
  if (!semester.value.registration_end) errors.value.registration_end = 'Vui lòng chọn ngày kết thúc đăng ký'
  if (!semester.value.add_drop_deadline) errors.value.add_drop_deadline = 'Vui lòng chọn hạn chót thêm/xóa môn'
  if (!semester.value.tuition_deadline) errors.value.tuition_deadline = 'Vui lòng chọn hạn nộp học phí'
  if (!semester.value.late_fee_start) errors.value.late_fee_start = 'Vui lòng chọn ngày bắt đầu tính phí trễ'
  if (semester.value.late_fee_amount == null) errors.value.late_fee_amount = 'Vui lòng nhập phí trễ hạn'
  if (semester.value.total_credits == null) errors.value.total_credits = 'Vui lòng nhập tổng số tín chỉ'
  if (semester.value.min_credits == null) errors.value.min_credits = 'Vui lòng nhập số tín chỉ tối thiểu'
  if (semester.value.max_credits == null) errors.value.max_credits = 'Vui lòng nhập số tín chỉ tối đa'
  if (!semester.value.status) errors.value.status = 'Vui lòng chọn trạng thái'

  if (semester.value.start_date && semester.value.end_date && new Date(semester.value.start_date) > new Date(semester.value.end_date)) {
    errors.value.start_date = 'Ngày bắt đầu phải trước ngày kết thúc'
  }
  if (semester.value.registration_start && semester.value.registration_end && new Date(semester.value.registration_start) > new Date(semester.value.registration_end)) {
    errors.value.registration_start = 'Ngày bắt đầu đăng ký phải trước ngày kết thúc đăng ký'
  }
  if (semester.value.tuition_deadline && semester.value.late_fee_start && new Date(semester.value.tuition_deadline) > new Date(semester.value.late_fee_start)) {
    errors.value.tuition_deadline = 'Hạn nộp học phí phải trước ngày bắt đầu tính phí trễ'
  }
  if (semester.value.min_credits && semester.value.max_credits && semester.value.min_credits > semester.value.max_credits) {
    errors.value.min_credits = 'Số tín chỉ tối thiểu không được vượt quá số tín chỉ tối đa'
  }
  if (semester.value.status === 'current' && !semester.value.is_active) {
    errors.value.is_active = 'Học kỳ hiện tại phải có trạng thái hoạt động'
  }
}

const saveSemester = async () => {
  validateSemester()
  if (Object.keys(errors.value).length > 0) return

  try {
    const payload = {
      ...semester.value,
      start_date: semester.value.start_date.toISOString().split('T')[0],
      end_date: semester.value.end_date.toISOString().split('T')[0],
      registration_start: semester.value.registration_start.toISOString().split('T')[0],
      registration_end: semester.value.registration_end.toISOString().split('T')[0],
      add_drop_deadline: semester.value.add_drop_deadline.toISOString().split('T')[0],
      tuition_deadline: semester.value.tuition_deadline.toISOString().split('T')[0],
      late_fee_start: semester.value.late_fee_start.toISOString().split('T')[0]
    }
    if (semester.value.semester_id) {
      const response = await api.patch(`${endpoints.semesters}${semester.value.semester_id}/`, payload)
      semesters.value = semesters.value.map(s => s.semester_id === semester.value.semester_id ? response.data : s)
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật học kỳ thành công', life: 3000 })
    } else {
      const response = await api.post(endpoints.semesters, payload)
      semesters.value.push(response.data)
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Thêm học kỳ thành công', life: 3000 })
    }
    hideDialog()
  } catch (error) {
    const errorMsg = error.response?.data?.detail || Object.values(error.response?.data || {}).join(', ') || 'Không thể lưu học kỳ'
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errorMsg, life: 3000 })
  }
}

const deleteSemester = async () => {
  try {
    await api.delete(`${endpoints.semesters}${semester.value.semester_id}/`)
    semesters.value = semesters.value.filter(s => s.semester_id !== semester.value.semester_id)
    deleteDialog.value = false
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa học kỳ thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa học kỳ', life: 3000 })
  }
}

const restoreSemester = async (data) => {
  try {
    const response = await api.post(`${endpoints.semesters}${data.semester_id}/restore/`)
    semesters.value = semesters.value.map(s => s.semester_id === data.semester_id ? response.data.data : s)
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Khôi phục học kỳ thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: error.response?.data?.error || 'Không thể khôi phục học kỳ', life: 3000 })
  }
}

const changeStatus = async () => {
  submitted.value = true
  if (!newStatus.value) return

  try {
    const response = await api.post(`${endpoints.semesters}${semester.value.semester_id}/change-status/`, { status: newStatus.value })
    semesters.value = semesters.value.map(s => s.semester_id === semester.value.semester_id ? response.data.data : s)
    changeStatusDialog.value = false
    newStatus.value = ''
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật trạng thái thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể cập nhật trạng thái', life: 3000 })
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
    case 'upcoming': return 'info'
    case 'current': return 'success'
    case 'completed': return 'warning'
    case 'cancelled': return 'danger'
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

.action-buttons {
  display: flex;
  gap: 0.5rem;
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

.form-section {
  margin-bottom: 1.5rem;
}

.form-section h4 {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  color: #333;
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
.access-denied {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #ef4444;
}
</style>