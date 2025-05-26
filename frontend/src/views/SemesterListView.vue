<template>
  <div class="card">
    <div class="card-header">
      <h2>Học Kỳ</h2>
      <Button @click="openNew" severity="success" icon="pi pi-plus" label="Thêm Học Kỳ" />
    </div>

    <DataTable
      :value="semesters"
      :paginator="true"
      :rows="10"
      :loading="loading"
      dataKey="id"
      :filters="filters"
      filterDisplay="menu"
      :globalFilterFields="['name', 'year']"
      responsiveLayout="scroll"
    >
      <template #empty>
        <div class="text-center p-4">
          <p>Không tìm thấy học kỳ nào.</p>
        </div>
      </template>

      <template #loading>
        <div class="text-center p-4">
          <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
        </div>
      </template>

      <Column field="name" header="Tên Học Kỳ" sortable style="min-width: 14rem">
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            @input="filterCallback()"
            placeholder="Tìm theo tên học kỳ"
            class="p-column-filter"
          />
        </template>
      </Column>

      <Column field="year" header="Năm Học" sortable style="min-width: 12rem">
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            @input="filterCallback()"
            placeholder="Tìm theo năm học"
            class="p-column-filter"
          />
        </template>
      </Column>

      <Column field="start_date" header="Ngày Bắt Đầu" sortable style="min-width: 12rem">
        <template #body="{ data }">
          {{ formatDate(data.start_date) }}
        </template>
      </Column>

      <Column field="end_date" header="Ngày Kết Thúc" sortable style="min-width: 12rem">
        <template #body="{ data }">
          {{ formatDate(data.end_date) }}
        </template>
      </Column>

      <Column field="status" header="Trạng Thái" sortable style="min-width: 10rem">
        <template #body="{ data }">
          <Tag :severity="getStatusSeverity(data.status)" :value="getStatusLabel(data.status)" />
        </template>
      </Column>

      <Column :exportable="false" style="min-width: 8rem">
        <template #body="{ data }">
          <Button icon="pi pi-pencil" outlined rounded class="mr-2" @click="editSemester(data)" />
          <Button icon="pi pi-trash" outlined rounded severity="danger" @click="confirmDeleteSemester(data)" />
        </template>
      </Column>
    </DataTable>

    <Dialog v-model:visible="semesterDialog" :style="{ width: '450px' }" header="Thông Tin Học Kỳ" :modal="true" class="p-fluid">
      <div class="field">
        <label for="name">Tên Học Kỳ</label>
        <InputText id="name" v-model.trim="semester.name" required autofocus :class="{ 'p-invalid': submitted && !semester.name }" />
        <small class="p-error" v-if="submitted && !semester.name">Vui lòng nhập tên học kỳ.</small>
      </div>
      <div class="field">
        <label for="year">Năm Học</label>
        <InputText id="year" v-model.trim="semester.year" required :class="{ 'p-invalid': submitted && !semester.year }" />
        <small class="p-error" v-if="submitted && !semester.year">Vui lòng nhập năm học.</small>
      </div>
      <div class="field">
        <label for="start_date">Ngày Bắt Đầu</label>
        <Calendar id="start_date" v-model="semester.start_date" dateFormat="dd/mm/yy" required :class="{ 'p-invalid': submitted && !semester.start_date }" />
        <small class="p-error" v-if="submitted && !semester.start_date">Vui lòng chọn ngày bắt đầu.</small>
      </div>
      <div class="field">
        <label for="end_date">Ngày Kết Thúc</label>
        <Calendar id="end_date" v-model="semester.end_date" dateFormat="dd/mm/yy" required :class="{ 'p-invalid': submitted && !semester.end_date }" />
        <small class="p-error" v-if="submitted && !semester.end_date">Vui lòng chọn ngày kết thúc.</small>
      </div>
      <div class="field">
        <label for="status">Trạng Thái</label>
        <Dropdown
          id="status"
          v-model="semester.status"
          :options="statusOptions"
          optionLabel="label"
          optionValue="value"
          placeholder="Chọn trạng thái"
          :class="{ 'p-invalid': submitted && !semester.status }"
        />
        <small class="p-error" v-if="submitted && !semester.status">Vui lòng chọn trạng thái.</small>
      </div>

      <template #footer>
        <Button label="Hủy" icon="pi pi-times" outlined @click="hideDialog" />
        <Button label="Lưu" icon="pi pi-check" @click="saveSemester" />
      </template>
    </Dialog>

    <Dialog v-model:visible="deleteSemesterDialog" :style="{ width: '450px' }" header="Xác Nhận" :modal="true">
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span v-if="semester">Bạn có chắc chắn muốn xóa học kỳ <b>{{ semester.name }}</b>?</span>
      </div>
      <template #footer>
        <Button label="Không" icon="pi pi-times" outlined @click="deleteSemesterDialog = false" />
        <Button label="Có" icon="pi pi-check" severity="danger" @click="deleteSemester" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { api } from '@/services/api'

const toast = useToast()
const semesters = ref([])
const semesterDialog = ref(false)
const deleteSemesterDialog = ref(false)
const semester = ref({})
const submitted = ref(false)
const loading = ref(true)
const filters = ref({})

const statusOptions = [
  { label: 'Chưa bắt đầu', value: 'not_started' },
  { label: 'Đang diễn ra', value: 'in_progress' },
  { label: 'Đã kết thúc', value: 'completed' }
]

onMounted(async () => {
  await loadSemesters()
})

const loadSemesters = async () => {
  try {
    loading.value = true
    semesters.value = await api.getSemesters()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách học kỳ', life: 3000 })
  } finally {
    loading.value = false
  }
}

const openNew = () => {
  semester.value = {
    status: 'not_started'
  }
  submitted.value = false
  semesterDialog.value = true
}

const hideDialog = () => {
  semesterDialog.value = false
  submitted.value = false
}

const editSemester = (data) => {
  semester.value = { ...data }
  semesterDialog.value = true
}

const confirmDeleteSemester = (data) => {
  semester.value = data
  deleteSemesterDialog.value = true
}

const saveSemester = async () => {
  submitted.value = true

  if (semester.value.name?.trim() && semester.value.year?.trim() && semester.value.start_date && semester.value.end_date && semester.value.status) {
    try {
      if (semester.value.id) {
        await api.updateSemester(semester.value.id, semester.value)
        toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật học kỳ thành công', life: 3000 })
      } else {
        await api.createSemester(semester.value)
        toast.add({ severity: 'success', summary: 'Thành công', detail: 'Thêm học kỳ thành công', life: 3000 })
      }

      semesterDialog.value = false
      semester.value = {}
      await loadSemesters()
    } catch (error) {
      toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể lưu thông tin học kỳ', life: 3000 })
    }
  }
}

const deleteSemester = async () => {
  try {
    await api.deleteSemester(semester.value.id)
    deleteSemesterDialog.value = false
    semester.value = {}
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa học kỳ thành công', life: 3000 })
    await loadSemesters()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa học kỳ', life: 3000 })
  }
}

const getStatusLabel = (status) => {
  const option = statusOptions.find(opt => opt.value === status)
  return option ? option.label : status
}

const getStatusSeverity = (status) => {
  switch (status) {
    case 'not_started':
      return 'info'
    case 'in_progress':
      return 'success'
    case 'completed':
      return 'warning'
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