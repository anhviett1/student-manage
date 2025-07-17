<template>
  <p-card class="class-roster-card">
    <template #title>
      <i class="mdi mdi-account-group-outline p-mr-2"></i> Danh sách sinh viên trong lớp
    </template>
    <template #content>
      <div class="p-formgrid p-grid p-align-center p-mb-4">
        <div class="p-field p-col-12 p-md-6">
          <span class="p-float-label">
            <p-dropdown id="assignedClass" v-model="selectedClassId" :options="assignedClasses" optionLabel="name" optionValue="id" placeholder="Chọn lớp để xem danh sách" @change="loadClassRoster" filter />
            <label for="assignedClass">Lớp được phân công</label>
          </span>
        </div>
      </div>

      <p-data-table :value="classRoster" :paginator="true" :rows="10"
                    responsiveLayout="scroll" :loading="isLoadingRoster">
        <template #empty>
          <div class="p-text-center">Vui lòng chọn một lớp để xem danh sách sinh viên.</div>
        </template>
        <template #loading>
          Đang tải danh sách sinh viên. Vui lòng chờ...
        </template>
        <p-column field="student_id" header="Mã SV"></p-column>
        <p-column field="full_name" header="Họ và Tên"></p-column>
        <p-column field="email" header="Email"></p-column>
        <p-column field="phone_number" header="SĐT"></p-column>
        <p-column field="gender" header="Giới tính">
          <template #body="slotProps">
            {{ formatGender(slotProps.data.gender) }}
          </template>
        </p-column>
        <p-column field="major_name" header="Chuyên ngành"></p-column>
        <p-column field="class_name" header="Lớp"></p-column>
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
import { fetchTeacherAssignedClasses, fetchClassRoster } from '@/services/mockTeacherService'; // Create this mock service

const notificationStore = useNotificationStore();

const assignedClasses = ref([]);
const selectedClassId = ref(null);
const classRoster = ref([]);
const isLoadingRoster = ref(false);

const teacherId = ref(1); // TODO: Replace with actual logged-in teacher ID from auth store

const formatGender = (gender) => {
  switch (gender) {
    case 'male': return 'Nam';
    case 'female': return 'Nữ';
    case 'other': return 'Khác';
    default: return '';
  }
};

// Fetch classes assigned to this teacher
const loadAssignedClasses = async () => {
  try {
    const data = await fetchTeacherAssignedClasses(teacherId.value);
    assignedClasses.value = data;
    if (data.length > 0) {
      selectedClassId.value = data[0].id; // Select the first class by default
      await loadClassRoster();
    }
  } catch (error) {
    notificationStore.showToast('Lỗi', 'error', 'Không thể tải danh sách lớp được phân công.');
    console.error('Error loading assigned classes:', error);
  }
};

const loadClassRoster = async () => {
  if (!selectedClassId.value) {
    classRoster.value = [];
    return;
  }

  isLoadingRoster.value = true;
  try {
    const data = await fetchClassRoster(selectedClassId.value);
    classRoster.value = data;
  } catch (error) {
    notificationStore.showToast('Lỗi', 'error', 'Không thể tải danh sách sinh viên.');
    console.error('Error loading class roster:', error);
    classRoster.value = [];
  } finally {
    isLoadingRoster.value = false;
  }
};

onMounted(() => {
  loadAssignedClasses();
});
</script>

<style scoped>
.class-roster-card {
  max-width: 1200px;
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