<template>
  <div class="student-view-container" aria-label="Trang quản lý sinh viên">
    <Toast aria-live="polite" />
    <ConfirmDialog aria-live="assertive" />
    <div v-if="isStudent || isAdminOrTeacher">
      <TabView v-model:activeIndex="activeTabIndex" scrollable class="tab-view" aria-label="Tab điều hướng sinh viên">
        <TabPanel header="Thông Tin Cá Nhân" v-if="isStudent">
          <StudentProfile
            :student="currentStudent"
            @update:student="updateCurrentStudent"
            @loadProfile="loadCurrentStudentProfile"
          />
        </TabPanel>
        <TabPanel header="Quản Lý Sinh Viên" v-if="isAdminOrTeacher">
          <StudentManagement
            :students="students"
            :filters="filters"
            :paginatorInfo="paginatorInfo"
            :departments="departments"
            @update:students="updateStudents"
            @loadStudents="loadStudents"
            @loadDepartments="loadDepartments"
          />
        </TabPanel>
      </TabView>
    </div>
    <div v-else class="access-denied">
      <p>Bạn không có quyền truy cập trang này.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useUserStore } from '@/stores/user';
import { useToast } from 'primevue/usetoast';
import { gsap } from 'gsap';
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';
import Toast from 'primevue/toast';
import ConfirmDialog from 'primevue/confirmdialog';
import StudentProfile from '@/components/StudentProfile.vue';
import StudentManagement from '@/components/StudentManagement.vue';
import api, { endpoints } from '@/services/api';

const userStore = useUserStore();
const toast = useToast();

const activeTabIndex = ref(0);
const currentStudent = ref({});
const students = ref([]);
const departments = ref([]);
const filters = ref({ status: 'active', department: null, global: '' });
const paginatorInfo = ref({ rows: 10, page: 1, total: 0 });

const isStudent = computed(() => userStore.currentUser?.is_student);
const isAdminOrTeacher = computed(() => userStore.isAdmin || userStore.isTeacher);

onMounted(async () => {
  gsap.from('.student-view-container', { opacity: 0, y: 50, duration: 0.8, ease: 'power2.out' });
  if (isStudent.value) {
    await loadCurrentStudentProfile();
  }
  if (isAdminOrTeacher.value) {
    await loadStudents();
    await loadDepartments();
  }
});

const loadCurrentStudentProfile = async () => {
  try {
    if (!userStore.currentUser) {
      await userStore.getCurrentUser();
    }
    currentStudent.value = userStore.currentUser?.student_profile || {};
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải thông tin cá nhân', life: 3000 });
  }
};

const loadStudents = async (page = 1, rows = paginatorInfo.value.rows) => {
  try {
    const params = {
      page,
      page_size: rows,
      status: filters.value.status || undefined,
      department_id: filters.value.department || undefined,
      search: filters.value.global || undefined,
    };
    const response = await api.get(endpoints.students, { params });
    students.value = Array.isArray(response.data.results) ? response.data.results : response.data;
    paginatorInfo.value.total = response.data.count || students.value.length;
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách sinh viên', life: 3000 });
    students.value = [];
  }
};

const loadDepartments = async () => {
  try {
    const response = await api.get(endpoints.departments);
    departments.value = Array.isArray(response.data.results) ? response.data.results : response.data;
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách khoa', life: 3000 });
    departments.value = [];
  }
};

const updateCurrentStudent = (updatedStudent) => {
  currentStudent.value = updatedStudent;
};

const updateStudents = (newStudents) => {
  students.value = newStudents;
};
</script>

<style scoped>
.student-view-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.tab-view .p-tabview-nav {
  background-color: #f3f4f6;
  border-bottom: 2px solid #e5e7eb;
  border-radius: 8px 8px 0 0;
}
.tab-view .p-tabview-nav-link {
  padding: 12px 16px;
  font-weight: 500;
  color: #4b5563;
  transition: background-color 0.2s ease, color 0.2s ease;
}
.tab-view .p-tabview-nav-link:hover {
  background-color: #e5e7eb;
  color: #1f2937;
}
.tab-view .p-tabview-nav-link.p-highlight {
  background-color: #3b82f6;
  color: #ffffff;
  border-radius: 6px 6px 0 0;
}
.tab-view .p-tabview-panels {
  padding: 24px;
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 0 0 8px 8px;
}
.access-denied {
  text-align: center;
  padding: 24px;
  color: #ef4444;
  font-weight: 500;
}
</style>