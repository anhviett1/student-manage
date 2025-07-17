<template>
  <p-card class="grade-entry-card">
    <template #title>
      <i class="mdi mdi-pencil-box-outline p-mr-2"></i> Nhập / Chỉnh sửa Điểm
    </template>
    <template #content>
      <div class="p-formgrid p-grid p-align-center p-mb-4">
        <div class="p-field p-col-12 p-md-6">
          <span class="p-float-label">
            <p-dropdown id="assignedCourse" v-model="selectedCourseId" :options="assignedCourses" optionLabel="name" optionValue="id" placeholder="Chọn Môn học" @change="loadStudentsForGradeEntry" filter />
            <label for="assignedCourse">Môn học được phân công</label>
          </span>
        </div>
        <div class="p-field p-col-12 p-md-6">
          <span class="p-float-label">
            <p-dropdown id="semester" v-model="selectedSemesterId" :options="semesters" optionLabel="name" optionValue="id" placeholder="Chọn Học kỳ" @change="loadStudentsForGradeEntry" />
            <label for="semester">Học kỳ</label>
          </span>
        </div>
      </div>

      <p-divider v-if="selectedCourseId && selectedSemesterId" align="center">
        <span class="p-tag">Danh sách sinh viên cho {{ selectedCourseName }} - {{ selectedSemesterName }}</span>
      </p-divider>

      <p-data-table v-if="selectedCourseId && selectedSemesterId" :value="studentsWithGrades" :paginator="true" :rows="10"
                    responsiveLayout="scroll" :loading="isLoadingStudents">
        <template #empty>
          <div class="p-text-center">Vui lòng chọn môn học và học kỳ để nhập điểm.</div>
        </template>
        <template #loading>
          Đang tải danh sách sinh viên. Vui lòng chờ...
        </template>
        <p-column field="student_id" header="Mã SV"></p-column>
        <p-column field="full_name" header="Họ và Tên"></p-column>
        <p-column field="current_score" header="Điểm hiện tại">
          <template #body="slotProps">
            <p-tag v-if="slotProps.data.current_score !== null" :value="slotProps.data.current_score" :severity="getScoreSeverity(slotProps.data.current_score)"></p-tag>
            <span v-else>Chưa có điểm</span>
          </template>
        </p-column>
        <p-column header="Nhập/Chỉnh sửa điểm">
          <template #body="slotProps">
            <p-button icon="pi pi-pencil" class="p-button-rounded p-button-text" @click="editScore(slotProps.data)" />
          </template>
        </p-column>
      </p-data-table>
    </template>
  </p-card>

  <p-dialog v-model:visible="displayScoreForm" :header="scoreFormTitle" :modal="true" :style="{width: '500px'}">
    <ScoreForm
      :initialData="currentScoreData"
      :isEditMode="!!currentScoreData.id"
      :isLoading="isSavingScore"
      :students="[selectedStudentForScore]"
      :courses="[{ id: selectedCourseId, name: selectedCourseName }]"
      :semesters="[{ id: selectedSemesterId, name: selectedSemesterName }]"
      @submit="handleScoreSubmit"
      @cancel="displayScoreForm = false"
    />
  </p-dialog>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useNotificationStore } from '@/stores/notification';

// PrimeVue Components
import PCard from 'primevue/card';
import PDropdown from 'primevue/dropdown';
import PDataTable from 'primevue/datatable';
import PColumn from 'primevue/column';
import PButton from 'primevue/button';
import PDivider from 'primevue/divider';
import PDialog from 'primevue/dialog';
import PTag from 'primevue/tag';

// Custom Form Component
import ScoreForm from '@/components/forms/ScoreForm.vue';

// Mock data (replace with actual API calls)
import { fetchTeacherAssignedCourses, fetchSemesters, fetchStudentsForCourseAndSemester, saveStudentScore } from '@/services/mockTeacherService'; // Create this mock service

const notificationStore = useNotificationStore();

const assignedCourses = ref([]);
const semesters = ref([]);
const selectedCourseId = ref(null);
const selectedSemesterId = ref(null);
const studentsWithGrades = ref([]);
const isLoadingStudents = ref(false);
const displayScoreForm = ref(false);
const currentScoreData = ref({});
const selectedStudentForScore = ref({});
const isSavingScore = ref(false);

const teacherId = ref(1); // TODO: Replace with actual logged-in teacher ID from auth store

const selectedCourseName = computed(() => {
  const course = assignedCourses.value.find(c => c.id === selectedCourseId.value);
  return course ? course.name : '';
});

const selectedSemesterName = computed(() => {
  const semester = semesters.value.find(s => s.id === selectedSemesterId.value);
  return semester ? semester.name : '';
});

const scoreFormTitle = computed(() => {
  return currentScoreData.value.id ? 'Chỉnh sửa điểm' : 'Nhập điểm mới';
});

const getScoreSeverity = (score) => {
  if (score >= 8.5) return 'success';
  if (score >= 7.0) return 'info';
  if (score >= 5.0) return 'warning';
  return 'danger';
};

// Fetch assigned courses for the teacher
const loadAssignedCourses = async () => {
  try {
    const data = await fetchTeacherAssignedCourses(teacherId.value);
    assignedCourses.value = data;
    if (data.length > 0) {
      selectedCourseId.value = data[0].id;
    }
  } catch (error) {
    notificationStore.showToast('Lỗi', 'error', 'Không thể tải danh sách môn học được phân công.');
    console.error('Error loading assigned courses:', error);
  }
};

// Fetch all semesters
const loadSemesters = async () => {
  try {
    const data = await fetchSemesters();
    semesters.value = data;
    if (data.length > 0) {
      selectedSemesterId.value = data[0].id;
    }
  } catch (error) {
    notificationStore.showToast('Lỗi', 'error', 'Không thể tải danh sách học kỳ.');
    console.error('Error loading semesters:', error);
  }
};

const loadStudentsForGradeEntry = async () => {
  if (!selectedCourseId.value || !selectedSemesterId.value) {
    studentsWithGrades.value = [];
    return;
  }

  isLoadingStudents.value = true;
  try {
    const data = await fetchStudentsForCourseAndSemester(selectedCourseId.value, selectedSemesterId.value);
    studentsWithGrades.value = data.map(s => ({
      ...s,
      current_score: s.score || null // Assuming 'score' comes from the API if exists
    }));
  } catch (error) {
    notificationStore.showToast('Lỗi', 'error', 'Không thể tải danh sách sinh viên để nhập điểm.');
    console.error('Error loading students for grade entry:', error);
    studentsWithGrades.value = [];
  } finally {
    isLoadingStudents.value = false;
  }
};

const editScore = (student) => {
  selectedStudentForScore.value = student;
  // Prepare data for ScoreForm
  currentScoreData.value = {
    id: student.score_id, // Score ID if it exists (for editing)
    student_id: student.id,
    course_id: selectedCourseId.value,
    semester_id: selectedSemesterId.value,
    score: student.current_score,
    notes: student.notes || ''
  };
  displayScoreForm.value = true;
};

const handleScoreSubmit = async (scoreData) => {
  isSavingScore.value = true;
  try {
    await saveStudentScore(scoreData); // Mock API call
    notificationStore.showToast('Thành công', 'success', 'Điểm đã được cập nhật.');
    displayScoreForm.value = false;
    await loadStudentsForGradeEntry(); // Reload students and their grades
  } catch (error) {
    notificationStore.showToast('Lỗi', 'error', 'Không thể lưu điểm.');
    console.error('Error saving score:', error);
  } finally {
    isSavingScore.value = false;
  }
};

// Initial load
onMounted(async () => {
  await loadAssignedCourses();
  await loadSemesters();
  // Ensure both are loaded before attempting to load students
  if (selectedCourseId.value && selectedSemesterId.value) {
    await loadStudentsForGradeEntry();
  }
});
</script>

<style scoped>
.grade-entry-card {
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