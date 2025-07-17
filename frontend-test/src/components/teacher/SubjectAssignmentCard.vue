<template>
  <p-card class="subject-assignment-card">
    <template #title>
      <i class="mdi mdi-book-account-outline p-mr-2"></i> Môn học được phân công
    </template>
    <template #content>
      <div class="p-formgrid p-grid p-align-center p-mb-4">
        <div class="p-field p-col-12 p-md-6">
          <span class="p-float-label">
            <p-dropdown id="semesterAssignment" v-model="selectedSemesterId" :options="semesters" optionLabel="name" optionValue="id" placeholder="Chọn Học kỳ để xem phân công" @change="loadAssignedSubjects" />
            <label for="semesterAssignment">Chọn Học kỳ</label>
          </span>
        </div>
      </div>

      <p-data-table :value="assignedSubjects" :paginator="true" :rows="10"
                    responsiveLayout="scroll" :loading="isLoadingAssignments">
        <template #empty>
          <div class="p-text-center">Vui lòng chọn học kỳ để xem phân công, hoặc bạn chưa được phân công môn học nào trong học kỳ này.</div>
        </template>
        <template #loading>
          Đang tải phân công môn học. Vui lòng chờ...
        </template>
        <p-column field="semester_name" header="Học kỳ"></p-column>
        <p-column field="course_name" header="Môn học"></p-column>
        <p-column field="course_code" header="Mã môn"></p-column>
        <p-column field="class_name" header="Lớp"></p-column>
        <p-column field="room" header="Phòng học"></p-column>
        <p-column field="day_of_week" header="Ngày"></p-column>
        <p-column field="start_time" header="Bắt đầu"></p-column>
        <p-column field="end_time" header="Kết thúc"></p-column>
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

// Mock data (replace with actual API calls)
import { fetchSemesters, fetchTeacherAssignedSubjects } from '@/services/mockTeacherService'; // Use the same mock service

const notificationStore = useNotificationStore();

const semesters = ref([]);
const selectedSemesterId = ref(null);
const assignedSubjects = ref([]);
const isLoadingAssignments = ref(false);

const teacherId = ref(1); // TODO: Replace with actual logged-in teacher ID from auth store

// Fetch all semesters
const loadSemesters = async () => {
  try {
    const data = await fetchSemesters();
    semesters.value = data;
    // Optionally set default selected semester to current or latest
    if (data.length > 0) {
      selectedSemesterId.value = data[0].id; // Select the first semester by default
      await loadAssignedSubjects(); // Load assignments for default semester
    }
  } catch (error) {
    notificationStore.showToast('Lỗi', 'error', 'Không thể tải danh sách học kỳ.');
    console.error('Error loading semesters:', error);
  }
};

const loadAssignedSubjects = async () => {
  if (!selectedSemesterId.value) {
    assignedSubjects.value = [];
    return;
  }

  isLoadingAssignments.value = true;
  try {
    const data = await fetchTeacherAssignedSubjects(teacherId.value, selectedSemesterId.value);
    assignedSubjects.value = data;
  } catch (error) {
    notificationStore.showToast('Lỗi', 'error', 'Không thể tải phân công môn học.');
    console.error('Error loading assigned subjects:', error);
    assignedSubjects.value = [];
  } finally {
    isLoadingAssignments.value = false;
  }
};

onMounted(() => {
  loadSemesters();
});
</script>

<style scoped>
.subject-assignment-card {
  max-width: 1100px;
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