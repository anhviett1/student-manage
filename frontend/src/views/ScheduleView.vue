<template>
  <div class="card">
    <TabView v-if="canViewSchedules">
      <TabPanel header="Lịch Học Của Tôi" v-if="isStudent">
        <DataTable :value="mySchedules" :loading="loading" :rows="10" paginator>
          <Column field="class_assigned.name" header="Lớp Học" sortable></Column>
          <Column field="teacher.full_name" header="Giảng Viên" sortable>
            <template #body="{ data }">
              {{ data.teacher?.full_name || '-' }}
            </template>
          </Column>
          <Column field="day_of_week" header="Ngày" sortable>
            <template #body="{ data }">
              {{ getDayLabel(data.day_of_week) }}
            </template>
          </Column>
          <Column field="start_time" header="Giờ Bắt Đầu" sortable></Column>
          <Column field="end_time" header="Giờ Kết Thúc" sortable></Column>
          <Column field="room" header="Phòng Học" sortable></Column>
          <Column field="semester.name" header="Học Kỳ" sortable></Column>
        </DataTable>
      </TabPanel>
      <TabPanel header="Lịch Giảng Dạy" v-if="isTeacher">
        <DataTable :value="teacherSchedules" :loading="loading" :rows="10" paginator>
          <Column field="class_assigned.name" header="Lớp Học" sortable></Column>
          <Column field="day_of_week" header="Ngày" sortable>
            <template #body="{ data }">
              {{ getDayLabel(data.day_of_week) }}
            </template>
          </Column>
          <Column field="start_time" header="Giờ Bắt Đầu" sortable></Column>
          <Column field="end_time" header="Giờ Kết Thúc" sortable></Column>
          <Column field="room" header="Phòng Học" sortable></Column>
          <Column field="semester.name" header="Học Kỳ" sortable></Column>
        </DataTable>
      </TabPanel>
      <TabPanel header="Quản Lý Lịch Học" v-if="isAdmin">
        <div class="card-header">
          <div>
            <Button v-if="canEditSchedules" icon="pi pi-plus" label="Thêm lịch học" @click="openNew" severity="success" />
            <Button v-if="canImportSchedules" icon="pi pi-upload" label="Import" @click="openImport" class="mr-2" />
            <Button v-if="canExportSchedules" icon="pi pi-download" label="Export" @click="exportCSV" />
          </div>
        </div>
        <DataTable :value="schedules" :loading="loading" :rows="10" paginator>
          <Column field="class_assigned.name" header="Lớp Học" sortable></Column>
          <Column field="teacher.full_name" header="Giảng Viên" sortable>
            <template #body="{ data }">
              {{ data.teacher?.full_name || '-' }}
            </template>
          </Column>
          <Column field="day_of_week" header="Ngày" sortable>
            <template #body="{ data }">
              {{ getDayLabel(data.day_of_week) }}
            </template>
          </Column>
          <Column field="start_time" header="Giờ Bắt Đầu" sortable></Column>
          <Column field="end_time" header="Giờ Kết Thúc" sortable></Column>
          <Column field="room" header="Phòng Học" sortable></Column>
          <Column field="semester.name" header="Học Kỳ" sortable></Column>
          <Column field="status" header="Trạng Thái" sortable>
            <template #body="{ data }">
              <Tag :severity="getStatusSeverity(data.status)" :value="getStatusLabel(data.status)" />
            </template>
          </Column>
          <Column>
            <template #body="{ data }">
              <Button v-if="canEditSchedules && !data.is_deleted" icon="pi pi-pencil" outlined rounded severity="info" @click="editSchedule(data)" v-tooltip="'Sửa thông tin'" />
              <Button v-if="canDeleteSchedules && !data.is_deleted" icon="pi pi-trash" outlined rounded severity="danger" class="mr-2" @click="confirmDelete(data)" v-tooltip="'Xóa mềm'" />
              <Button v-if="canDeleteSchedules && data.is_deleted" icon="pi pi-undo" outlined rounded severity="success" @click="restoreSchedule(data)" v-tooltip="'Khôi phục'" />
            </template>
          </Column>
        </DataTable>
        <Dialog v-model:visible="scheduleDialog" :style="{ width: '600px' }" header="Thông Tin Lịch Học" :modal="true" class="p-fluid">
          <div class="form-section">
            <h4>Thông Tin Lịch Học</h4>
            <div class="field">
              <label for="class_assigned">Lớp Học</label>
              <Dropdown id="class_assigned" v-model="schedule.class_assigned" :options="classes" optionLabel="name" optionValue="class_id" placeholder="Chọn lớp học" :class="{ 'p-invalid': errors.class_assigned }" />
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
        <Dialog v-model:visible="deleteScheduleDialog" :style="{ width: '450px' }" header="Xác Nhận Xóa Mềm" :modal="true">
          <div class="confirmation-content">
            <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
            <span v-if="schedule">Bạn có chắc chắn muốn xóa mềm lịch học <b>{{ schedule.class_assigned?.name }}</b>?</span>
          </div>
          <template #footer>
            <Button label="Không" icon="pi pi-times" text @click="deleteScheduleDialog = false" />
            <Button label="Có" icon="pi pi-check" severity="danger" @click="deleteSchedule" />
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
import { useAuthStore } from '@/stores/auth'
import api, { endpoints } from '@/services/api'

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

onMounted(async () => {
  if (canViewSchedules.value) {
    await Promise.all([loadSchedules(), loadClasses(), loadTeachers(), loadSemesters()])
  }
})

const loadSchedules = async () => {
  try {
    loading.value = true
    const response = await api.get(endpoints.schedules)
    const allSchedules = response.data
    const currentUserId = authStore.user?.id

    if (isAdmin.value) {
      schedules.value = allSchedules
    }
    if (isStudent.value && currentUserId) {
      mySchedules.value = allSchedules.filter(s => s.class_assigned?.students?.includes(currentUserId))
    }
    if (isTeacher.value && currentUserId) {
      teacherSchedules.value = allSchedules.filter(s => s.teacher?.id === currentUserId)
    }
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách lịch học', life: 3000 })
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

const openImport = () => {
  toast.add({ severity: 'info', summary: 'Chức năng', detail: 'Chức năng import đang được phát triển', life: 3000 })
}

const exportCSV = () => {
  toast.add({ severity: 'info', summary: 'Chức năng', detail: 'Chức năng export đang được phát triển', life: 3000 })
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
.card-header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-bottom: 1rem;
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
</style>