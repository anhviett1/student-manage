<template>
  <p-card class="my-score-card">
    <template #title>
      <i class="mdi mdi-medal-outline p-mr-2"></i> Bảng điểm của tôi
    </template>
    <template #content>
      <div class="p-formgrid p-grid p-align-center p-mb-4">
        <div class="p-field p-col-12 p-md-6">
          <span class="p-float-label">
            <p-dropdown id="semesterScore" v-model="selectedSemesterId" :options="semesters" optionLabel="name" optionValue="id" placeholder="Chọn Học kỳ để xem điểm" @change="loadStudentScores" />
            <label for="semesterScore">Chọn Học kỳ</label>
          </span>
        </div>
      </div>

      <p-data-table :value="scores" :paginator="true" :rows="10"
                    responsiveLayout="scroll" :loading="isLoadingScores">
        <template #empty>
          <div class="p-text-center">Vui lòng chọn học kỳ để xem điểm, hoặc bạn chưa có điểm trong học kỳ này.</div>
        </template>
        <template #loading>
          Đang tải điểm. Vui lòng chờ...
        </template>
        <p-column field="semester_name" header="Học kỳ"></p-column>
        <p-column field="course_name" header="Môn học"></p-column>
        <p-column field="score" header="Điểm" sortable>
          <template #body="slotProps">
            <p-tag :value="slotProps.data.score" :severity="getScoreSeverity(slotProps.data.score)"></p-tag>
          </template>
        </p-column>
        <p-column field="notes" header="Ghi chú"></p-column>
      </p-data-table>
    </template>
  </p-card>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useNotificationStore } from '@/stores/notification';

// PrimeVue Components
import PCard from 'primevue/card';
import PDropdown from 'primevue/dropdown';
import PDataTable from 'primevue/datatable';
import PColumn from 'primevue/column';
import PTag from 'primevue/tag';

// Mock data (replace with actual API calls)
import { fetchSemesters, fetchStudentScores } from '@/services/mockStudentService'; // Use the same mock service

const notificationStore = useNotificationStore();

const semesters = ref([]);
const selectedSemesterId = ref(null);
const scores = ref([]);
const isLoadingScores = ref(false);

const studentId = ref(1); // TODO: Replace with actual logged-in student ID from auth store

// Fetch all semesters
const loadSemesters = async () => {
  try {
    const data = await fetchSemesters();
    semesters.value = data;
    // Optionally set default selected semester to current or latest
    if (data.length > 0) {
      selectedSemesterId.value = data[0].id; // Select the first semester by default
      await loadStudentScores(); // Load scores for default semester
    }
  } catch (error) {
    notificationStore.showToast('Lỗi', 'error', 'Không thể tải danh sách học kỳ.');
    console.error('Error loading semesters:', error);
  }
};

const loadStudentScores = async () => {
  isLoadingScores.value = true;
  try {
    const data = await fetchStudentScores(studentId.value, selectedSemesterId.value);
    scores.value = data;
  } catch (error) {
    notificationStore.showToast('Lỗi', 'error', 'Không thể tải điểm số.');
    console.error('Error loading student scores:', error);
    scores.value = [];
  } finally {
    isLoadingScores.value = false;
  }
};

const getScoreSeverity = (score) => {
  if (score >= 8.5) return 'success';
  if (score >= 7.0) return 'info';
  if (score >= 5.0) return 'warning';
  return 'danger';
};

onMounted(() => {
  loadSemesters();
});
</script>

<style scoped>
.my-score-card {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1.5rem;
  border-radius: var(--p-card-border-radius);
  box-shadow: var(--p-card-shadow);
}

.p-mb-4 {
  margin-bottom: 1.5rem !important;
}

.p-mr-2 {
  margin-right: 0.5rem !important;
}
</style>