<template>
  <p-card class="my-schedule-card">
    <template #title>
      <i class="mdi mdi-calendar-check-outline p-mr-2"></i> Lịch học của tôi
    </template>
    <template #content>
      <div class="p-formgrid p-grid p-align-center p-mb-4">
        <div class="p-field p-col-12 p-md-6">
          <span class="p-float-label">
            <p-dropdown id="semesterSchedule" v-model="selectedSemesterId" :options="semesters" optionLabel="name" optionValue="id" placeholder="Chọn Học kỳ để xem lịch" @change="loadStudentSchedule" />
            <label for="semesterSchedule">Chọn Học kỳ</label>
          </span>
        </div>
      </div>

      <p-data-table :value="schedule" :paginator="true" :rows="10"
                    responsiveLayout="scroll" :loading="isLoadingSchedule">
        <template #empty>
          <div class="p-text-center">Vui lòng chọn học kỳ để xem lịch học, hoặc bạn chưa có lịch học trong học kỳ này.</div>
        </template>
        <template #loading>
          Đang tải lịch học. Vui lòng chờ...
        </template>
        <p-column field="semester_name" header="Học kỳ"></p-column>
        <p-column field="course_name" header="Môn học"></p-column>
        <p-column field="teacher_name" header="Giáo viên"></p-column>
        <p-column field="class_name" header="Lớp"></p-column>
        <p-column field="day_of_week" header="Ngày"></p-column>
        <p-column field="start_time" header="Bắt đầu"></p-column>
        <p-column field="end_time" header="Kết thúc"></p-column>
        <p-column field="room" header="Phòng"></p-column>
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
import { fetchSemesters, fetchStudentSchedule } from '@/services/mockStudentService'; // Use the same mock service

const notificationStore = useNotificationStore();

const semesters = ref([]);
const selectedSemesterId = ref(null);
const schedule = ref([]);
const isLoadingSchedule = ref(false);

const studentId = ref(1); // TODO: Replace with actual logged-in student ID from auth store

// Fetch all semesters
const loadSemesters = async () => {
  try {
    const data = await fetchSemesters();
    semesters.value = data;
    // Optionally set default selected semester to current or latest
    if (data.length > 0) {
      selectedSemesterId.value = data[0].id; // Select the first semester by default
      await loadStudentSchedule(); // Load schedule for default semester
    }
  } catch (error) {
    notificationStore.showToast('Lỗi', 'error', 'Không thể tải danh sách học kỳ.');
    console.error('Error loading semesters:', error);
  }
};

const loadStudentSchedule = async () => {
  if (!selectedSemesterId.value) {
    schedule.value = [];
    return;
  }

  isLoadingSchedule.value = true;
  try {
    const data = await fetchStudentSchedule(studentId.value, selectedSemesterId.value);
    schedule.value = data;
  } catch (error) {
    notificationStore.showToast('Lỗi', 'error', 'Không thể tải lịch học.');
    console.error('Error loading student schedule:', error);
    schedule.value = [];
  } finally {
    isLoadingSchedule.value = false;
  }
};

onMounted(() => {
  loadSemesters();
});
</script>

<style scoped>
.my-schedule-card {
  max-width: 1000px;
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