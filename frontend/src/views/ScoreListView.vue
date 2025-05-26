<template>
  <div class="card">
    <div class="card-header">
      <h2>Điểm Số</h2>
      <Button @click="openNew" severity="success" icon="pi pi-plus" label="Thêm Điểm" />
    </div>

    <DataTable
      :value="scores"
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
          <p>Không tìm thấy điểm số nào.</p>
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

      <Column field="midterm_score" header="Điểm Giữa Kỳ" sortable style="min-width: 12rem">
        <template #body="{ data }">
          {{ data.midterm_score || '-' }}
        </template>
      </Column>

      <Column field="final_score" header="Điểm Cuối Kỳ" sortable style="min-width: 12rem">
        <template #body="{ data }">
          {{ data.final_score || '-' }}
        </template>
      </Column>

      <Column field="average_score" header="Điểm Trung Bình" sortable style="min-width: 12rem">
        <template #body="{ data }">
          <Tag :severity="getScoreSeverity(data.average_score)" :value="formatScore(data.average_score)" />
        </template>
      </Column>

      <Column :exportable="false" style="min-width: 8rem">
        <template #body="{ data }">
          <Button icon="pi pi-pencil" outlined rounded class="mr-2" @click="editScore(data)" />
          <Button icon="pi pi-trash" outlined rounded severity="danger" @click="confirmDeleteScore(data)" />
        </template>
      </Column>
    </DataTable>

    <Dialog v-model:visible="scoreDialog" :style="{ width: '450px' }" header="Thông Tin Điểm Số" :modal="true" class="p-fluid">
      <div class="field">
        <label for="student">Học Sinh</label>
        <Dropdown
          id="student"
          v-model="score.student"
          :options="students"
          optionLabel="name"
          placeholder="Chọn học sinh"
          :class="{ 'p-invalid': submitted && !score.student }"
        />
        <small class="p-error" v-if="submitted && !score.student">Vui lòng chọn học sinh.</small>
      </div>
      <div class="field">
        <label for="subject">Môn Học</label>
        <Dropdown
          id="subject"
          v-model="score.subject"
          :options="subjects"
          optionLabel="name"
          placeholder="Chọn môn học"
          :class="{ 'p-invalid': submitted && !score.subject }"
        />
        <small class="p-error" v-if="submitted && !score.subject">Vui lòng chọn môn học.</small>
      </div>
      <div class="field">
        <label for="semester">Học Kỳ</label>
        <Dropdown
          id="semester"
          v-model="score.semester"
          :options="semesters"
          optionLabel="name"
          placeholder="Chọn học kỳ"
          :class="{ 'p-invalid': submitted && !score.semester }"
        />
        <small class="p-error" v-if="submitted && !score.semester">Vui lòng chọn học kỳ.</small>
      </div>
      <div class="field">
        <label for="midterm_score">Điểm Giữa Kỳ</label>
        <InputNumber
          id="midterm_score"
          v-model="score.midterm_score"
          :min="0"
          :max="10"
          :step="0.1"
          :class="{ 'p-invalid': submitted && score.midterm_score === null }"
        />
        <small class="p-error" v-if="submitted && score.midterm_score === null">Vui lòng nhập điểm giữa kỳ.</small>
      </div>
      <div class="field">
        <label for="final_score">Điểm Cuối Kỳ</label>
        <InputNumber
          id="final_score"
          v-model="score.final_score"
          :min="0"
          :max="10"
          :step="0.1"
          :class="{ 'p-invalid': submitted && score.final_score === null }"
        />
        <small class="p-error" v-if="submitted && score.final_score === null">Vui lòng nhập điểm cuối kỳ.</small>
      </div>

      <template #footer>
        <Button label="Hủy" icon="pi pi-times" outlined @click="hideDialog" />
        <Button label="Lưu" icon="pi pi-check" @click="saveScore" />
      </template>
    </Dialog>

    <Dialog v-model:visible="deleteScoreDialog" :style="{ width: '450px' }" header="Xác Nhận" :modal="true">
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span v-if="score">Bạn có chắc chắn muốn xóa điểm số này?</span>
      </div>
      <template #footer>
        <Button label="Không" icon="pi pi-times" outlined @click="deleteScoreDialog = false" />
        <Button label="Có" icon="pi pi-check" severity="danger" @click="deleteScore" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { api } from '@/services/api'

const toast = useToast()
const scores = ref([])
const students = ref([])
const subjects = ref([])
const semesters = ref([])
const scoreDialog = ref(false)
const deleteScoreDialog = ref(false)
const score = ref({})
const submitted = ref(false)
const loading = ref(true)
const filters = ref({})

onMounted(async () => {
  await Promise.all([loadScores(), loadStudents(), loadSubjects(), loadSemesters()])
})

const loadScores = async () => {
  try {
    loading.value = true
    scores.value = await api.getScores()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách điểm số', life: 3000 })
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
  score.value = {}
  submitted.value = false
  scoreDialog.value = true
}

const hideDialog = () => {
  scoreDialog.value = false
  submitted.value = false
}

const editScore = (data) => {
  score.value = { ...data }
  scoreDialog.value = true
}

const confirmDeleteScore = (data) => {
  score.value = data
  deleteScoreDialog.value = true
}

const saveScore = async () => {
  submitted.value = true

  if (score.value.student && score.value.subject && score.value.semester && score.value.midterm_score !== null && score.value.final_score !== null) {
    try {
      // Tính điểm trung bình
      score.value.average_score = (score.value.midterm_score + score.value.final_score) / 2

      if (score.value.id) {
        await api.updateScore(score.value.id, score.value)
        toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật điểm số thành công', life: 3000 })
      } else {
        await api.createScore(score.value)
        toast.add({ severity: 'success', summary: 'Thành công', detail: 'Thêm điểm số thành công', life: 3000 })
      }

      scoreDialog.value = false
      score.value = {}
      await loadScores()
    } catch (error) {
      toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể lưu thông tin điểm số', life: 3000 })
    }
  }
}

const deleteScore = async () => {
  try {
    await api.deleteScore(score.value.id)
    deleteScoreDialog.value = false
    score.value = {}
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa điểm số thành công', life: 3000 })
    await loadScores()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa điểm số', life: 3000 })
  }
}

const formatScore = (score) => {
  if (score === null || score === undefined) return '-'
  return score.toFixed(1)
}

const getScoreSeverity = (score) => {
  if (score === null || score === undefined) return 'info'
  if (score >= 8.5) return 'success'
  if (score >= 7) return 'info'
  if (score >= 5.5) return 'warning'
  return 'danger'
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