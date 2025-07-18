<template>
  <div class="enrollment-view-container" aria-label="Trang quản lý đăng ký">
    <Toast aria-live="polite" />
    <ConfirmDialog aria-live="assertive" />
    <TabView v-model:activeIndex="activeTabIndex" scrollable class="tab-view" aria-label="Tab điều hướng quản lý đăng ký">
      <TabPanel header="Đăng Ký Của Tôi" v-if="isStudent">
        <MyEnrollments :myEnrollments="myEnrollments" :selectedSemester="selectedSemester" :globalFilter="globalFilter" :paginatorInfo="paginatorInfo" @update:myEnrollments="myEnrollments = $event" @loadMyEnrollments="loadMyEnrollments" />
      </TabPanel>
      <TabPanel header="Quản Lý Đăng Ký" v-if="isAdminOrTeacher">
        <EnrollmentManagement :enrollments="enrollments" :filters="filters" :paginatorInfo="paginatorInfo" @update:enrollments="enrollments = $event" @loadEnrollments="loadEnrollments" />
      </TabPanel>
    </TabView>
    <div v-if="!canViewEnrollments && !isStudent" class="access-denied">
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
import MyEnrollments from '@/components/MyEnrollments.vue';
import EnrollmentManagement from '@/components/EnrollmentManagement.vue';
import api, { endpoints } from '@/services/api';

const userStore = useUserStore();
const toast = useToast();

const activeTabIndex = ref(0);
const myEnrollments = ref([]);
const enrollments = ref([]);
const selectedSemester = ref(null);
const globalFilter = ref('');
const filters = ref({
  status: null,
  semester: null,
  global: '',
});
const paginatorInfo = ref({ rows: 10, page: 1, total: 0 });

const isStudent = computed(() => userStore.isStudent);
const isAdminOrTeacher = computed(() => userStore.isAdmin || userStore.isTeacher);
const canViewEnrollments = computed(() => userStore.isAdmin || userStore.isTeacher);

onMounted(async () => {
  gsap.from('.enrollment-view-container', { opacity: 0, y: 50, duration: 0.8, ease: 'power2.out' });
  if (isStudent.value) {
    await loadMyEnrollments();
  }
  if (isAdminOrTeacher.value) {
    await loadEnrollments();
  }
});

const loadMyEnrollments = async (page = 1, rows = paginatorInfo.value.rows) => {
  if (!isStudent.value) return;
  try {
    const params = {
      page,
      page_size: rows,
      semester_id: selectedSemester.value || undefined,
      search: globalFilter.value || undefined,
    };
    const response = await api.get(endpoints.enrollments, { params });
    myEnrollments.value = Array.isArray(response.data.results) ? response.data.results : response.data;
    paginatorInfo.value.total = response.data.count || myEnrollments.value.length;
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải đăng ký', life: 3000 });
    myEnrollments.value = [];
  }
};

const loadEnrollments = async (page = 1, rows = paginatorInfo.value.rows) => {
  if (!isAdminOrTeacher.value) return;
  try {
    const params = {
      page,
      page_size: rows,
      status: filters.value.status || undefined,
      semester_id: filters.value.semester || undefined,
      search: filters.value.global || undefined,
    };
    const response = await api.get(endpoints.enrollments, { params });
    enrollments.value = Array.isArray(response.data.results) ? response.data.results : response.data;
    paginatorInfo.value.total = response.data.count || enrollments.value.length;
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải đăng ký', life: 3000 });
    enrollments.value = [];
  }
};
</script>

<style scoped>
.enrollment-view-container {
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