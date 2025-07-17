<template>
  <div class="p-fluid course-registration-container">
    <p-card>
      <template #title>
        <i class="mdi mdi-clipboard-list-outline p-mr-2"></i> Đăng ký Môn học
      </template>
      <template #content>
        <div class="p-formgrid p-grid p-align-center p-mb-4">
          <div class="p-field p-col-12 p-md-6">
            <span class="p-float-label">
              <p-dropdown id="semesterSelection" v-model="selectedSemesterId" :options="semesters" optionLabel="name" optionValue="id" placeholder="Chọn Học kỳ để đăng ký" :class="{'p-invalid': v$.selectedSemesterId.$error}" @change="loadAvailableCourses" />
              <label for="semesterSelection">Chọn Học kỳ</label>
            </span>
            <small class="p-error" v-for="error of v$.selectedSemesterId.$errors" :key="error.$uid">{{ error.$message }}</small>
          </div>
        </div>

        <p-divider v-if="selectedSemesterId" align="center">
          <span class="p-tag">Môn học có thể đăng ký trong {{ selectedSemesterName }}</span>
        </p-divider>

        <p-data-table v-if="selectedSemesterId" :value="availableCourses" :paginator="true" :rows="10"
                      v-model:selection="selectedCoursesToRegister" dataKey="id"
                      responsiveLayout="scroll" :loading="isLoadingCourses">
          <template #empty>
            <div class="p-text-center">Không có môn học nào khả dụng trong học kỳ này hoặc bạn đã đăng ký.</div>
          </template>
          <template #loading>
            Đang tải môn học khả dụng. Vui lòng chờ...
          </template>
          <p-column selectionMode="multiple" headerStyle="width: 3em"></p-column>
          <p-column field="name" header="Tên Môn học"></p-column>
          <p-column field="code" header="Mã Môn học"></p-column>
          <p-column field="credits" header="Tín chỉ"></p-column>
          <p-column field="department_name" header="Khoa/Bộ môn"></p-column>
          <p-column field="description" header="Mô tả"></p-column>
        </p-data-table>

        <div v-if="selectedSemesterId && availableCourses.length > 0" class="p-d-flex p-jc-end p-mt-4">
          <p-button label="Đăng ký Môn học đã chọn" icon="pi pi-check" @click="confirmRegistration" :disabled="selectedCoursesToRegister.length === 0" :loading="isRegistering" />
        </div>
      </template>
    </p-card>

    <p-dialog v-model:visible="displayConfirmDialog" header="Xác nhận Đăng ký" :modal="true" :style="{width: '450px'}">
      <div class="p-d-flex p-ai-center p-jc-center p-mb-4">
        <i class="pi pi-exclamation-triangle p-mr-3" style="font-size: 2rem" />
        <span>Bạn có chắc chắn muốn đăng ký **{{ selectedCoursesToRegister.length }}** môn học đã chọn cho học kỳ **{{ selectedSemesterName }}** không?</span>
      </div>
      <template #footer>
        <p-button label="Hủy" icon="pi pi-times" @click="displayConfirmDialog = false" class="p-button-text" />
        <p-button label="Xác nhận" icon="pi pi-check" @click="handleRegistration" autofocus />
      </template>
    </p-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue';
import { useVuelidate } from '@vuelidate/core';
import { required } from '@vuelidate/validators';
import { useNotificationStore } from '@/stores/notification';

// PrimeVue Components
import PCard from 'primevue/card';
import PDropdown from 'primevue/dropdown';
import PDataTable from 'primevue/datatable';
import PColumn from 'primevue/column';
import PButton from 'primevue/button';
import PDivider from 'primevue/divider';
import PDialog from 'primevue/dialog';
import PTag from 'primevue/tag'; // Used for the divider tag

// Mock data (replace with actual API calls)
import { fetchSemesters, fetchAvailableCoursesForSemester, registerStudentForCourses } from '@/services/mockStudentService'; // Create this mock service

const notificationStore = useNotificationStore();

const semesters = ref([]);
const selectedSemesterId = ref(null);
const availableCourses = ref([]);
const selectedCoursesToRegister = ref([]);
const isLoadingCourses = ref(false);
const isRegistering = ref(false);
const displayConfirmDialog = ref(false);

const studentId = ref(1); // TODO: Replace with actual logged-in student ID from auth store

// Vuelidate rules
const rules = computed(() => ({
  selectedSemesterId: { required: required }
}));

const v$ = useVuelidate(rules, { selectedSemesterId });

const selectedSemesterName = computed(() => {
  const semester = semesters.value.find(s => s.id === selectedSemesterId.value);
  return semester ? semester.name : '';
});

// Fetch all semesters on component mount
const loadSemesters = async () => {
  try {
    const data = await fetchSemesters();
    semesters.value = data;
  } catch (error) {
    notificationStore.showToast('Lỗi', 'error', 'Không thể tải danh sách học kỳ.');
    console.error('Error loading semesters:', error);
  }
};

const loadAvailableCourses = async () => {
  if (!selectedSemesterId.value) {
    availableCourses.value = [];
    return;
  }

  isLoadingCourses.value = true;
  selectedCoursesToRegister.value = []; // Clear selection when semester changes
  try {
    // In a real app, this API would filter out already registered courses for the student
    const data = await fetchAvailableCoursesForSemester(selectedSemesterId.value, studentId.value);
    availableCourses.value = data;
  } catch (error) {
    notificationStore.showToast('Lỗi', 'error', 'Không thể tải môn học khả dụng.');
    console.error('Error loading available courses:', error);
    availableCourses.value = [];
  } finally {
    isLoadingCourses.value = false;
  }
};

const confirmRegistration = async () => {
  const result = await v$.value.$validate();
  if (result) {
    displayConfirmDialog.value = true;
  } else {
    notificationStore.showToast('Vui lòng chọn học kỳ.', 'error', 'Lỗi nhập liệu');
  }
};

const handleRegistration = async () => {
  displayConfirmDialog.value = false;
  isRegistering.value = true;
  try {
    const registrationData = selectedCoursesToRegister.value.map(course => ({
      student_id: studentId.value,
      course_id: course.id,
      semester_id: selectedSemesterId.value,
      enrollment_date: new Date().toISOString().split('T')[0] // Current date
    }));

    await registerStudentForCourses(registrationData); // Mock API call
    notificationStore.showToast('Thành công', 'success', 'Đăng ký môn học thành công!');
    await loadAvailableCourses(); // Reload courses to reflect changes
    selectedCoursesToRegister.value = []; // Clear selection
  } catch (error) {
    notificationStore.showToast('Lỗi', 'error', 'Đăng ký môn học thất bại.');
    console.error('Error during course registration:', error);
  } finally {
    isRegistering.value = false;
  }
};

// Initial load
loadSemesters();
</script>

<style scoped>
.course-registration-container {
  max-width: 900px;
  margin: 2rem auto;
  padding: 1.5rem;
  border-radius: var(--p-card-border-radius);
  box-shadow: var(--p-card-shadow);
}

.p-mb-4 {
  margin-bottom: 1.5rem !important;
}

.p-d-flex {
  display: flex;
}

.p-jc-end {
  justify-content: flex-end;
}

.p-mr-2 {
  margin-right: 0.5rem !important;
}

.p-mr-3 {
  margin-right: 1rem !important;
}
</style>