<template>
  <div>
    <Toast />
    <div v-if="canViewSchedules" class="card">
      <TabView>
        <!-- Tab 1: Lịch Học Của Tôi (sinh viên) -->
        <TabPanel header="Lịch Học Của Tôi" v-if="isStudent">
          <div class="profile-section">
            <div class="profile-header">
              <h2>Lịch Học Của Tôi</h2>
            </div>
            <div class="filter-bar">
              <div class="filter-group">
                <Dropdown v-model="studentFilters.semester" :options="semesters" optionLabel="name" optionValue="semester_id" placeholder="Chọn học kỳ" class="filter-dropdown" @change="loadMySchedules" />
                <Dropdown v-model="studentFilters.status" :options="statusOptions" optionLabel="label" optionValue="value" placeholder="Lọc trạng thái" class="filter-dropdown mr-2" @change="loadMySchedules" />
                <InputText v-model="studentFilters.global" placeholder="Tìm lớp, phòng, giảng viên..." class="filter-search" @input="loadMySchedules" />
                <Button v-if="canExportSchedules" icon="pi pi-download" label="Export" severity="success" @click="exportSchedules" v-tooltip="'Xuất lịch học cá nhân'" />
              </div>
            </div>
          </div>
          <div v-if="(mySchedules.length > 0 || loading) && isStudent">
            <DataTable :value="mySchedules" :loading="loading" dataKey="schedule_id" :paginator="true" :rows="10" :rowsPerPageOptions="[5, 10, 20]" responsiveLayout="scroll" class="p-datatable-sm">
              <template #empty>
                <div class="empty-message"><i class="pi pi-info-circle" /><span>Không tìm thấy lịch học nào.</span></div>
              </template>
              <template #loading>
                <div class="loading-message"><i class="pi pi-spin pi-spinner" /><span>Đang tải dữ liệu...</span></div>
              </template>
              <Column field="class_assigned.class_name" header="Lớp Học" sortable />
              <Column field="teacher.full_name" header="Giảng Viên" sortable />
              <Column field="day_of_week" header="Ngày" sortable>
                <template #body="{ data }">{{ getDayLabel(data.day_of_week) }}</template>
              </Column>
              <Column field="start_time" header="Giờ Bắt Đầu" sortable />
              <Column field="end_time" header="Giờ Kết Thúc" sortable />
              <Column field="room" header="Phòng Học" sortable />
              <Column field="semester.name" header="Học Kỳ" sortable />
              <Column field="status" header="Trạng Thái" sortable>
                <template #body="{ data }"><Tag :severity="getStatusSeverity(data.status)" :value="getStatusLabel(data.status)" /></template>
              </Column>
            </DataTable>
          </div>
          <div v-else-if="!loading && mySchedules.length === 0 && isStudent">
            <div class="no-data-message">
              <p>Không có dữ liệu lịch học để hiển thị.</p>
              <Button label="Tải lại" icon="pi pi-refresh" @click="loadMySchedules" severity="secondary" />
            </div>
          </div>
        </TabPanel>
        <!-- Tab 2: Lịch Giảng Dạy (giáo viên) -->
        <TabPanel header="Lịch Giảng Dạy" v-if="isTeacher">
          <div class="profile-section">
            <div class="profile-header">
              <h2>Lịch Giảng Dạy</h2>
            </div>
            <div class="filter-bar">
              <div class="filter-group">
                <Dropdown v-model="teacherFilters.semester" :options="semesters" optionLabel="name" optionValue="semester_id" placeholder="Chọn học kỳ" class="filter-dropdown" @change="loadTeacherSchedules" />
                <Dropdown v-model="teacherFilters.status" :options="statusOptions" optionLabel="label" optionValue="value" placeholder="Lọc trạng thái" class="filter-dropdown mr-2" @change="loadTeacherSchedules" />
                <InputText v-model="teacherFilters.global" placeholder="Tìm lớp, phòng..." class="filter-search" @input="loadTeacherSchedules" />
                <Button v-if="canExportSchedules" icon="pi pi-download" label="Export" severity="success" @click="exportSchedules" v-tooltip="'Xuất lịch giảng dạy'" />
              </div>
            </div>
          </div>
          <div v-if="(teacherSchedules.length > 0 || loading) && isTeacher">
            <DataTable :value="teacherSchedules" :loading="loading" dataKey="schedule_id" :paginator="true" :rows="10" :rowsPerPageOptions="[5, 10, 20]" responsiveLayout="scroll" class="p-datatable-sm">
              <template #empty>
                <div class="empty-message"><i class="pi pi-info-circle" /><span>Không tìm thấy lịch giảng dạy nào.</span></div>
              </template>
              <template #loading>
                <div class="loading-message"><i class="pi pi-spin pi-spinner" /><span>Đang tải dữ liệu...</span></div>
              </template>
              <Column field="class_assigned.class_name" header="Lớp Học" sortable />
              <Column field="day_of_week" header="Ngày" sortable>
                <template #body="{ data }">{{ getDayLabel(data.day_of_week) }}</template>
              </Column>
              <Column field="start_time" header="Giờ Bắt Đầu" sortable />
              <Column field="end_time" header="Giờ Kết Thúc" sortable />
              <Column field="room" header="Phòng Học" sortable />
              <Column field="semester.name" header="Học Kỳ" sortable />
              <Column field="status" header="Trạng Thái" sortable>
                <template #body="{ data }"><Tag :severity="getStatusSeverity(data.status)" :value="getStatusLabel(data.status)" /></template>
              </Column>
            </DataTable>
          </div>
          <div v-else-if="!loading && teacherSchedules.length === 0 && isTeacher">
            <div class="no-data-message">
              <p>Không có dữ liệu lịch giảng dạy để hiển thị.</p>
              <Button label="Tải lại" icon="pi pi-refresh" @click="loadTeacherSchedules" severity="secondary" />
            </div>
          </div>
        </TabPanel>
        <!-- Tab 3: Quản Lý Lịch Học (admin) -->
        <TabPanel header="Quản Lý Lịch Học" v-if="isAdmin">
          <div class="header">
            <h2>Quản Lý Lịch Học</h2>
            <div class="action-buttons">
              <Button v-if="canEditSchedules" icon="pi pi-plus" label="Thêm Lịch Học" severity="primary" class="mr-2" @click="openNew" v-tooltip="'Thêm lịch học mới'" />
              <Button v-if="canExportSchedules" icon="pi pi-download" label="Export" severity="success" @click="exportSchedules" v-tooltip="'Xuất danh sách lịch học'" />
            </div>
          </div>
          <div class="filter-bar">
            <div class="filter-group">
              <Dropdown v-model="filters.status" :options="statusOptions" optionLabel="label" optionValue="value" placeholder="Lọc trạng thái" class="filter-dropdown mr-2" @change="loadSchedules" />
              <Dropdown v-model="filters.semester" :options="semesters" optionLabel="name" optionValue="semester_id" placeholder="Lọc học kỳ" class="filter-dropdown mr-2" @change="loadSchedules" />
              <Dropdown v-model="filters.class_assigned" :options="classes" optionLabel="class_name" optionValue="class_id" placeholder="Lọc lớp học" class="filter-dropdown mr-2" @change="loadSchedules" />
              <Dropdown v-model="filters.teacher" :options="teachers" optionLabel="full_name" optionValue="teacher_id" placeholder="Lọc giảng viên" class="filter-dropdown mr-2" @change="loadSchedules" />
              <Dropdown v-model="filters.day_of_week" :options="dayOptions" optionLabel="label" optionValue="value" placeholder="Lọc ngày" class="filter-dropdown mr-2" @change="loadSchedules" />
              <InputText v-model="filters.global" placeholder="Tìm kiếm..." class="filter-search" @input="loadSchedules" />
            </div>
          </div>
          <div v-if="(schedules.length > 0 || loading) && isAdmin">
            <DataTable :value="schedules" :loading="loading" dataKey="schedule_id" :paginator="true" :rows="10" :rowsPerPageOptions="[5, 10, 20]" responsiveLayout="scroll" class="p-datatable-sm">
              <template #empty>
                <div class="empty-message"><i class="pi pi-info-circle" /><span>Không tìm thấy lịch học nào.</span></div>
              </template>
              <template #loading>
                <div class="loading-message"><i class="pi pi-spin pi-spinner" /><span>Đang tải dữ liệu...</span></div>
              </template>
              <Column field="class_assigned.class_name" header="Lớp Học" sortable />
              <Column field="teacher.full_name" header="Giảng Viên" sortable />
              <Column field="day_of_week" header="Ngày" sortable>
                <template #body="{ data }">{{ getDayLabel(data.day_of_week) }}</template>
              </Column>
              <Column field="start_time" header="Giờ Bắt Đầu" sortable />
              <Column field="end_time" header="Giờ Kết Thúc" sortable />
              <Column field="room" header="Phòng Học" sortable />
              <Column field="semester.name" header="Học Kỳ" sortable />
              <Column field="status" header="Trạng Thái" sortable>
                <template #body="{ data }"><Tag :severity="getStatusSeverity(data.status)" :value="getStatusLabel(data.status)" /></template>
              </Column>
              <Column header="Hành Động" style="width: 15%" align="center">
                <template #body="{ data }">
                  <Button v-if="canEditSchedules && !data.is_deleted" icon="pi pi-pencil" outlined rounded class="mr-2" severity="info" @click="editSchedule(data)" v-tooltip="'Sửa thông tin'" />
                  <Button v-if="canDeleteSchedules && !data.is_deleted" icon="pi pi-trash" outlined rounded severity="danger" class="mr-2" @click="confirmDelete(data)" v-tooltip="'Xóa mềm'" />
                  <Button v-if="canDeleteSchedules && data.is_deleted" icon="pi pi-undo" outlined rounded severity="success" @click="restoreSchedule(data)" v-tooltip="'Khôi phục'" />
                </template>
              </Column>
            </DataTable>
          </div>
          <div v-else-if="!loading && schedules.length === 0 && isAdmin">
            <div class="no-data-message">
              <p>Không có dữ liệu lịch học để hiển thị.</p>
              <Button label="Tải lại" icon="pi pi-refresh" @click="loadSchedules" severity="secondary" />
            </div>
          </div>
          <!-- Dialog thêm/sửa lịch học -->
          <Dialog v-model:visible="scheduleDialog" :header="schedule.schedule_id ? 'Sửa Lịch Học' : 'Thêm Lịch Học'" :style="{ width: '600px' }" :modal="true" class="p-fluid">
            <div class="form-section">
              <h4>Thông Tin Lịch Học</h4>
              <div class="field">
                <label for="class_assigned">Lớp Học</label>
                <Dropdown id="class_assigned" v-model="schedule.class_assigned" :options="classes" optionLabel="class_name" optionValue="class_id" placeholder="Chọn lớp học" :class="{ 'p-invalid': errors.class_assigned }" />
                <small class="p-error" v-if="errors.class_assigned">{{ errors.class_assigned }}</small>
              </div>
              <div class="field">
                <label for="teacher">Giảng Viên</label>
                <Dropdown id="teacher" v-model="schedule.teacher" :options="teachers" optionLabel="full_name" optionValue="teacher_id" placeholder="Chọn giảng viên" :class="{ 'p-invalid': errors.teacher }" />
                <small class="p-error" v-if="errors.teacher">{{ errors.teacher }}</small>
              </div>
              <div class="field">
                <label for="semester">Học Kỳ</label>
                <Dropdown id="semester" v-model="schedule.semester" :options="semesters" optionLabel="name" optionValue="semester_id" placeholder="Chọn học kỳ" :class="{ 'p-invalid': errors.semester }" />
                <small class="p-error" v-if="errors.semester">{{ errors.semester }}</small>
              </div>
              <div class="field">
                <label for="day_of_week">Ngày Trong Tuần</label>
                <Dropdown id="day_of_week" v-model="schedule.day_of_week" :options="dayOptions" optionLabel="label" optionValue="value" placeholder="Chọn ngày" :class="{ 'p-invalid': errors.day_of_week }" />
                <small class="p-error" v-if="errors.day_of_week">{{ errors.day_of_week }}</small>
              </div>
              <div class="field">
                <label for="start_time">Giờ Bắt Đầu</label>
                <InputText id="start_time" v-model="schedule.start_time" type="time" :class="{ 'p-invalid': errors.start_time }" />
                <small class="p-error" v-if="errors.start_time">{{ errors.start_time }}</small>
              </div>
              <div class="field">
                <label for="end_time">Giờ Kết Thúc</label>
                <InputText id="end_time" v-model="schedule.end_time" type="time" :class="{ 'p-invalid': errors.end_time }" />
                <small class="p-error" v-if="errors.end_time">{{ errors.end_time }}</small>
              </div>
              <div class="field">
                <label for="room">Phòng Học</label>
                <InputText id="room" v-model="schedule.room" :class="{ 'p-invalid': errors.room }" />
                <small class="p-error" v-if="errors.room">{{ errors.room }}</small>
              </div>
              <div class="field">
                <label for="status">Trạng Thái</label>
                <Dropdown id="status" v-model="schedule.status" :options="statusOptions" optionLabel="label" optionValue="value" placeholder="Chọn trạng thái" :class="{ 'p-invalid': errors.status }" />
                <small class="p-error" v-if="errors.status">{{ errors.status }}</small>
              </div>
            </div>
            <template #footer>
              <Button label="Hủy" icon="pi pi-times" text @click="hideDialog" />
              <Button label="Lưu" icon="pi pi-check" @click="saveSchedule" />
            </template>
          </Dialog>
          <!-- Dialog xác nhận xóa mềm -->
          <Dialog v-model:visible="deleteScheduleDialog" header="Xác Nhận Xóa Mềm" :style="{ width: '400px' }" :modal="true">
            <div class="confirmation-content">
              <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
              <span v-if="schedule">Bạn có chắc chắn muốn xóa mềm lịch học <b>{{ schedule.class_assigned?.class_name }}</b>?</span>
            </div>
            <template #footer>
              <Button label="Không" icon="pi pi-times" text @click="deleteScheduleDialog = false" />
              <Button label="Có" icon="pi pi-check" severity="danger" @click="deleteSchedule" />
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
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { usePermissions } from '@/composables/usePermissions'
import { useAuthStore } from '@/stores/auth'
import api, { endpoints } from '@/services/api'
import Tag from 'primevue/tag'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import Toast from 'primevue/toast'
import Dropdown from 'primevue/dropdown'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tooltip from 'primevue/tooltip'


const toast = useToast()
const authStore = useAuthStore()
const {
  isAdmin,
  isTeacher,
  isStudent,
  canViewSchedules,
  canEditSchedules,
  canDeleteSchedules,
  canImportSchedules,
  canExportSchedules,
} = usePermissions()

const schedules = ref([])
const mySchedules = ref([])
const teacherSchedules = ref([])
const classes = ref([])
const teachers = ref([])
const semesters = ref([])
const scheduleDialog = ref(false)
const deleteScheduleDialog = ref(false)
const schedule = ref({})
const errors = ref({})
const loading = ref(true)

const dayOptions = [
  { label: 'Thứ Hai', value: 'mon' }, { label: 'Thứ Ba', value: 'tue' }, { label: 'Thứ Tư', value: 'wed' },
  { label: 'Thứ Năm', value: 'thu' }, { label: 'Thứ Sáu', value: 'fri' }, { label: 'Thứ Bảy', value: 'sat' }, { label: 'Chủ Nhật', value: 'sun' }
]
const statusOptions = [
  { label: 'Đang hoạt động', value: 'active' }, { label: 'Không hoạt động', value: 'inactive' }, { label: 'Đang chờ duyệt', value: 'pending' }
]

const studentFilters = ref({
  semester: null,
  status: null,
  global: null,
})

const teacherFilters = ref({
  semester: null,
  status: null,
  global: null,
})

const filters = ref({
  status: null,
  semester: null,
  class_assigned: null,
  teacher: null,
  day_of_week: null,
  global: null,
})

onMounted(async () => {
  if (canViewSchedules.value) {
    await Promise.all([loadSchedules(), loadClasses(), loadTeachers(), loadSemesters()])
  }
})

const loadSchedules = async () => {
  try {
    loading.value = true
    const params = {
      status: filters.value.status,
      semester: filters.value.semester,
      class_assigned: filters.value.class_assigned,
      teacher: filters.value.teacher,
      day_of_week: filters.value.day_of_week,
      global: filters.value.global,
    }
    const response = await api.get(endpoints.schedules, { params })
    schedules.value = response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách lịch học', life: 3000 })
  } finally {
    loading.value = false
  }
}

const loadMySchedules = async () => {
  try {
    loading.value = true
    const params = {
      ...studentFilters.value,
      student: authStore.user?.id,
    }
    const response = await api.get(endpoints.schedules, { params })
    mySchedules.value = response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải lịch học của bạn', life: 3000 })
  } finally {
    loading.value = false
  }
}

const loadTeacherSchedules = async () => {
  try {
    loading.value = true
    const params = {
      ...teacherFilters.value,
      teacher: authStore.user?.id,
    }
    const response = await api.get(endpoints.schedules, { params })
    teacherSchedules.value = response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải lịch giảng dạy của bạn', life: 3000 })
  } finally {
    loading.value = false
  }
}

const loadClasses = async () => {
  try {
    const response = await api.get(endpoints.classes)
    classes.value = response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách lớp học', life: 3000 })
  }
}

const loadTeachers = async () => {
  try {
    const response = await api.get(endpoints.teachers)
    teachers.value = response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách giảng viên', life: 3000 })
  }
}

const loadSemesters = async () => {
  try {
    const response = await api.get(endpoints.semesters)
    semesters.value = response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách học kỳ', life: 3000 })
  }
}

const validateSchedule = () => {
  errors.value = {}
  if (!schedule.value.class_assigned) errors.value.class_assigned = 'Vui lòng chọn lớp học'
  if (!schedule.value.teacher) errors.value.teacher = 'Vui lòng chọn giảng viên'
  if (!schedule.value.semester) errors.value.semester = 'Vui lòng chọn học kỳ'
  if (!schedule.value.day_of_week) errors.value.day_of_week = 'Vui lòng chọn ngày trong tuần'
  if (!schedule.value.start_time) errors.value.start_time = 'Vui lòng nhập giờ bắt đầu'
  if (!schedule.value.end_time) errors.value.end_time = 'Vui lòng nhập giờ kết thúc'
  if (!schedule.value.room?.trim()) errors.value.room = 'Vui lòng nhập phòng học'
  if (!schedule.value.status) errors.value.status = 'Vui lòng chọn trạng thái'
}

const openNew = () => {
  schedule.value = { status: 'active', is_active: true }
  errors.value = {}
  scheduleDialog.value = true
}

const hideDialog = () => {
  scheduleDialog.value = false
  errors.value = {}
}

const editSchedule = (data) => {
  schedule.value = { ...data }
  scheduleDialog.value = true
}

const confirmDelete = (data) => {
  schedule.value = data
  deleteScheduleDialog.value = true
}

const saveSchedule = async () => {
  validateSchedule()
  if (Object.keys(errors.value).length > 0) return
  try {
    const payload = {
      class_assigned: schedule.value.class_assigned,
      teacher: schedule.value.teacher,
      semester: schedule.value.semester,
      day_of_week: schedule.value.day_of_week,
      start_time: schedule.value.start_time,
      end_time: schedule.value.end_time,
      room: schedule.value.room,
      status: schedule.value.status,
      is_active: schedule.value.is_active
    }
    if (schedule.value.schedule_id) {
      const updatedSchedule = (await api.patch(`${endpoints.schedules}${schedule.value.schedule_id}/`, payload)).data
      schedules.value = schedules.value.map(s => s.schedule_id === schedule.value.schedule_id ? updatedSchedule : s)
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật lịch học thành công', life: 3000 })
    } else {
      const newSchedule = (await api.post(endpoints.schedules, payload)).data
      schedules.value.push(newSchedule)
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Thêm lịch học thành công', life: 3000 })
    }
    scheduleDialog.value = false
    schedule.value = {}
  } catch (error) {
    const errorMsg = error.response?.data?.detail || Object.values(error.response?.data || {}).join(', ') || 'Không thể lưu thông tin lịch học'
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errorMsg, life: 5000 })
  }
}

const deleteSchedule = async () => {
  try {
    await api.delete(`${endpoints.schedules}${schedule.value.schedule_id}/`)
    schedules.value = schedules.value.filter(s => s.schedule_id !== schedule.value.schedule_id)
    deleteScheduleDialog.value = false
    schedule.value = {}
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa mềm lịch học thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa lịch học', life: 3000 })
  }
}

const restoreSchedule = async (data) => {
  try {
    const response = await api.post(`${endpoints.schedules}${data.schedule_id}/restore/`)
    schedules.value = schedules.value.map(s => s.schedule_id === data.schedule_id ? response.data : s)
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Khôi phục lịch học thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể khôi phục lịch học', life: 3000 })
  }
}

const exportSchedules = async () => {
  try {
    const params = {
      ...filters.value,
      format: 'csv', // or 'xlsx'
    }
    const response = await api.get(`${endpoints.schedules}export/`, { params, responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `lich_hoc_${new Date().toISOString().slice(0, 10)}.csv`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xuất dữ liệu thành công', life: 3000 })
  } catch (error) {
    const errorMsg = error.response?.data?.detail || Object.values(error.response?.data || {}).join(', ') || 'Không thể xuất dữ liệu'
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errorMsg, life: 5000 })
  }
}

const getDayLabel = (day) => {
  const option = dayOptions.find(opt => opt.value === day)
  return option ? option.label : day
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
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}
.profile-section {
  margin-bottom: 1.5rem;
}
.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.profile-header h2 {
  font-size: 1.5rem;
  color: #333;
  margin: 0;
}
.filter-bar {
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
  flex-wrap: wrap;
  gap: 0.5rem;
}
.filter-dropdown {
  min-width: 150px;
}
.filter-search {
  min-width: 250px;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.header h2 {
  font-size: 1.5rem;
  color: #333;
  margin: 0;
}
.action-buttons {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.no-data-message {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
}
.no-data-message p {
  margin-bottom: 1rem;
}
.empty-message {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  color: #9ca3af;
}
.empty-message i {
  margin-right: 0.5rem;
}
.loading-message {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  color: #6b7280;
}
.loading-message i {
  margin-right: 0.5rem;
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
.access-denied {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #ef4444;
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