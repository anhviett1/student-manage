<template>
  <div class="card">
    <div class="card-header">
      <h2>Điểm số của tôi</h2>
    </div>

    <DataTable
      :value="scores"
      :loading="loading"
      :paginator="true"
      :rows="10"
      :rowsPerPageOptions="[5, 10, 20, 50]"
      sortMode="multiple"
      :filters="filters"
      filterDisplay="menu"
      :globalFilterFields="['subject.name', 'semester.name']"
      responsiveLayout="scroll"
      class="p-datatable-sm"
    >
      <template #header>
        <div class="flex justify-content-between">
          <span class="p-input-icon-left">
            <i class="pi pi-search" />
            <InputText
              v-model="filters['global'].value"
              placeholder="Tìm kiếm..."
              class="p-inputtext-sm"
            />
          </span>
        </div>
      </template>

      <Column field="subject.name" header="Môn học" sortable>
        <template #body="{ data }">
          {{ data.subject?.name }}
        </template>
      </Column>

      <Column field="semester.name" header="Học kỳ" sortable>
        <template #body="{ data }">
          {{ data.semester?.name }}
        </template>
      </Column>

      <Column field="midterm_score" header="Điểm giữa kỳ" sortable>
        <template #body="{ data }">
          <span :class="getScoreSeverity(data.midterm_score)">
            {{ formatScore(data.midterm_score) }}
          </span>
        </template>
      </Column>

      <Column field="final_score" header="Điểm cuối kỳ" sortable>
        <template #body="{ data }">
          <span :class="getScoreSeverity(data.final_score)">
            {{ formatScore(data.final_score) }}
          </span>
        </template>
      </Column>

      <Column field="average_score" header="Điểm trung bình" sortable>
        <template #body="{ data }">
          <span :class="getScoreSeverity(data.average_score)">
            {{ formatScore(data.average_score) }}
          </span>
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/stores/auth'
import { api } from '@/services/api'

const toast = useToast()
const authStore = useAuthStore()
const loading = ref(false)
const scores = ref([])
const filters = ref({
  global: { value: null }
})

onMounted(async () => {
  await loadScores()
})

const loadScores = async () => {
  try {
    loading.value = true
    // Lấy điểm của học sinh hiện tại
    const response = await api.getMyScores()
    scores.value = response
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Lỗi',
      detail: 'Không thể tải điểm số',
      life: 3000
    })
  } finally {
    loading.value = false
  }
}

const formatScore = (score) => {
  if (score === null || score === undefined) return '-'
  return score.toFixed(1)
}

const getScoreSeverity = (score) => {
  if (score === null || score === undefined) return 'text-gray-500'
  if (score >= 8.5) return 'text-green-500'
  if (score >= 7) return 'text-blue-500'
  if (score >= 5.5) return 'text-yellow-500'
  return 'text-red-500'
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