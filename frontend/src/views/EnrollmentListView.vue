<template>
  <div class="card">
    <div class="card-header">
      <h2>Đăng Ký Học</h2>
      <Button @click="openNew" severity="success" icon="pi pi-plus" label="Thêm Đăng Ký" />
    </div>

    <DataTable
      :value="enrollments"
      :paginator="true"
      :rows="10"
      :loading="loading"
      dataKey="id"
      :filters="filters"
      filterDisplay="menu"
      :globalFilterFields="['student.name', 'subject.name', 'semester.name']"
      responsiveLayout="scroll"
    >
      <template #empty>
        <div class="text-center p-4">
          <p>Không tìm thấy đăng ký học nào.</p>
        </div>
      </template>

      <template #loading>
        <div class="text-center p-4">
          <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
        </div>
      </template>

      <Column field="student.name" header="Học Sinh" sortable style="min-width: 14rem">
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            @input="filterCallback()"
            placeholder="Tìm theo tên học sinh"
            class="p-column-filter"
          />
        </template>
      </Column>

      <Column field="subject.name" header="Môn Học" sortable style="min-width: 14rem">
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            @input="filterCallback()"
            placeholder="Tìm theo tên môn"
            class="p-column-filter"
          />
        </template>
      </Column>

      <Column field="semester.name" header="Học Kỳ" sortable style="min-width: 12rem">
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            @input="filterCallback()"
            placeholder="Tìm theo học kỳ"
            class="p-column-filter"
          />
        </template>
      </Column>

      <Column field="status" header="Trạng Thái" sortable style="min-width: 10rem">
        <template #body="{ data }">
          <Tag :severity="getStatusSeverity(data.status)" :value="getStatusLabel(data.status)" />
        </template>
      </Column>

      <Column field="enrollment_date" header="Ngày Đăng Ký" sortable style="min-width: 12rem">
        <template #body="{ data }">
          {{ formatDate(data.enrollment_date) }}
        </template>
      </Column>

      <Column :exportable="false" style="min-width: 8rem">
        <template #body="{ data }">
          <Button icon="pi pi-pencil" outlined rounded class="mr-2" @click="editEnrollment(data)" />
          <Button icon="pi pi-trash" outlined rounded severity="danger" @click="confirmDeleteEnrollment(data)" />
        </template>
      </Column>
    </DataTable>

    <Dialog v-model:visible="enrollmentDialog" :style="{ width: '450px' }" header="Thông Tin Đăng Ký" :modal="true" class="p-fluid">
      <div class="field">
        <label for="student">Học Sinh</label>
        <Dropdown
          id="student"
          v-model="enrollment.student"
          :options="students"
          optionLabel="name"
          placeholder="Chọn học sinh"
          :class="{ 'p-invalid': submitted && !enrollment.student }"
        />
        <small class="p-error" v-if="submitted && !enrollment.student">Vui lòng chọn học sinh.</small>
      </div>
      <div class="field">
        <label for="subject">Môn Học</label>
        <Dropdown
          id="subject"
          v-model="enrollment.subject"
          :options="subjects"
          optionLabel="name"
          placeholder="Chọn môn học"
          :class="{ 'p-invalid': submitted && !enrollment.subject }"
        />
        <small class="p-error" v-if="submitted && !enrollment.subject">Vui lòng chọn môn học.</small>
      </div>
      <div class="field">
        <label for="semester">Học Kỳ</label>
        <Dropdown
          id="semester"
          v-model="enrollment.semester"
          :options="semesters"
          optionLabel="name"
          placeholder="Chọn học kỳ"
          :class="{ 'p-invalid': submitted && !enrollment.semester }"
        />
        <small class="p-error" v-if="submitted && !enrollment.semester">Vui lòng chọn học kỳ.</small>
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
          :class="{ 'p-invalid': submitted && !enrollment.status }"
        />
        <small class="p-error" v-if="submitted && !enrollment.status">Vui lòng chọn trạng thái.</small>
      </div>

      <template #footer>
        <Button label="Hủy" icon="pi pi-times" outlined @click="hideDialog" />
        <Button label="Lưu" icon="pi pi-check" @click="saveEnrollment" />
      </template>
    </Dialog>

    <Dialog v-model:visible="deleteEnrollmentDialog" :style="{ width: '450px' }" header="Xác Nhận" :modal="true">
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span v-if="enrollment">Bạn có chắc chắn muốn xóa đăng ký học này?</span>
      </div>
      <template #footer>
        <Button label="Không" icon="pi pi-times" outlined @click="deleteEnrollmentDialog = false" />
        <Button label="Có" icon="pi pi-check" severity="danger" @click="deleteEnrollment" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { api } from '@/services/api'

const toast = useToast()
const enrollments = ref([])
const students = ref([])
const subjects = ref([])
const semesters = ref([])
const enrollmentDialog = ref(false)
const deleteEnrollmentDialog = ref(false)
const enrollment = ref({})
const submitted = ref(false)
const loading = ref(true)
const filters = ref({})

const statusOptions = [
  { label: 'Đã đăng ký', value: 'registered' },
  { label: 'Đã duyệt', value: 'approved' },
  { label: 'Đã hủy', value: 'cancelled' }
]

onMounted(async () => {
  await Promise.all([loadEnrollments(), loadStudents(), loadSubjects(), loadSemesters()])
})

const loadEnrollments = async () => {
  try {
    loading.value = true
    enrollments.value = await api.getEnrollments()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách đăng ký học', life: 3000 })
  } finally {
    loading.value = false
  }
}

const loadStudents = async () => {
  try {
    students.value = await api.getStudents()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách học sinh', life: 3000 })
  }
}

const loadSubjects = async () => {
  try {
    subjects.value = await api.getSubjects()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách môn học', life: 3000 })
  }
}

const loadSemesters = async () => {
  try {
    semesters.value = await api.getSemesters()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách học kỳ', life: 3000 })
  }
}

const openNew = () => {
  enrollment.value = {
    status: 'registered',
    enrollment_date: new Date().toISOString().split('T')[0]
  }
  submitted.value = false
  enrollmentDialog.value = true
}

const hideDialog = () => {
  enrollmentDialog.value = false
  submitted.value = false
}

const editEnrollment = (data) => {
  enrollment.value = { ...data }
  enrollmentDialog.value = true
}

const confirmDeleteEnrollment = (data) => {
  enrollment.value = data
  deleteEnrollmentDialog.value = true
}

const saveEnrollment = async () => {
  submitted.value = true

  if (enrollment.value.student && enrollment.value.subject && enrollment.value.semester && enrollment.value.status) {
    try {
      if (enrollment.value.id) {
        await api.updateEnrollment(enrollment.value.id, enrollment.value)
        toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật đăng ký học thành công', life: 3000 })
      } else {
        await api.createEnrollment(enrollment.value)
        toast.add({ severity: 'success', summary: 'Thành công', detail: 'Thêm đăng ký học thành công', life: 3000 })
      }

      enrollmentDialog.value = false
      enrollment.value = {}
      await loadEnrollments()
    } catch (error) {
      toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể lưu thông tin đăng ký học', life: 3000 })
    }
  }
}

const deleteEnrollment = async () => {
  try {
    await api.deleteEnrollment(enrollment.value.id)
    deleteEnrollmentDialog.value = false
    enrollment.value = {}
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa đăng ký học thành công', life: 3000 })
    await loadEnrollments()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa đăng ký học', life: 3000 })
  }
}

const getStatusLabel = (status) => {
  const option = statusOptions.find(opt => opt.value === status)
  return option ? option.label : status
}

const getStatusSeverity = (status) => {
  switch (status) {
    case 'registered':
      return 'info'
    case 'approved':
      return 'success'
    case 'cancelled':
      return 'danger'
    default:
      return 'info'
  }
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('vi-VN')
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.card-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: var(--text-color);
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
  border-width: 1px 0 1px 0;
  padding: 1rem;
}

:deep(.p-datatable .p-datatable-thead > tr > th) {
  background: #f8fafc;
  color: #1e293b;
  font-weight: 600;
}

:deep(.p-datatable .p-datatable-tbody > tr > td) {
  padding: 1rem;
}

:deep(.p-datatable .p-datatable-tbody > tr:hover) {
  background: #f1f5f9;
}
</style> 