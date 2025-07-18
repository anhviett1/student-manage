<template>
  <div class="score-view-container" aria-label="Trang quản lý điểm">
    <Toast aria-live="polite" />
    <ConfirmDialog aria-live="assertive" />
    <TabView v-model:activeIndex="activeTabIndex" scrollable class="tab-view" aria-label="Tab điều hướng điểm">
      <TabPanel header="Điểm Của Tôi" v-if="isStudent">
        <MyScores
          :myScores="myScores"
          :filters="studentFilters"
          :paginatorInfo="paginatorInfo"
          @update:myScores="myScores = $event"
          @loadMyScores="loadMyScores"
        />
      </TabPanel>
      <TabPanel header="Quản Lý Điểm" v-if="isAdminOrTeacher">
        <ScoreManagement
          :scores="scores"
          :filters="filters"
          :paginatorInfo="paginatorInfo"
          @update:scores="scores = $event"
          @loadScores="loadScores"
        />
      </TabPanel>
    </TabView>
    <div v-if="!canViewScores && !isStudent" class="access-denied">
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
import MyScores from '@/components/MyScores.vue';
import ScoreManagement from '@/components/ScoreManagement.vue';
import api, { endpoints } from '@/services/api';

const userStore = useUserStore();
const toast = useToast();

const activeTabIndex = ref(0);
const myScores = ref([]);
const scores = ref([]);
const studentFilters = ref({ semester: null, global: '' });
const filters = ref({
  status: null,
  semester: null,
  subject: null,
  student: null,
  global: '',
});
const paginatorInfo = ref({ rows: 10, page: 1, total: 0 });

const isStudent = computed(() => userStore.isStudent);
const isAdmin = computed(() => userStore.isAdmin);
const isTeacher = computed(() => userStore.isTeacher);
const isAdminOrTeacher = computed(() => userStore.isAdmin || userStore.isTeacher);
const canViewScores = computed(() => userStore.isAdmin || userStore.isTeacher);

onMounted(async () => {
  gsap.from('.score-view-container', { opacity: 0, y: 50, duration: 0.8, ease: 'power2.out' });
  if (isStudent.value) await loadMyScores();
  if (isAdminOrTeacher.value) await loadScores();
});

const loadMyScores = async (page = 1, rows = paginatorInfo.value.rows) => {
  if (!isStudent.value) return;
  try {
    const params = {
      page,
      page_size: rows,
      semester_id: studentFilters.value.semester || undefined,
      search: studentFilters.value.global || undefined,
      student_id: userStore.user?.id,
    };
    const response = await api.get(endpoints.scores, { params });
    myScores.value = Array.isArray(response.data.results) ? response.data.results : response.data;
    paginatorInfo.value.total = response.data.count || myScores.value.length;
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải điểm số', life: 3000 });
    myScores.value = [];
  }
};

const loadScores = async (page = 1, rows = paginatorInfo.value.rows) => {
  if (!isAdminOrTeacher.value) return;
  try {
    const params = {
      page,
      page_size: rows,
      status: filters.value.status || undefined,
      semester_id: filters.value.semester || undefined,
      subject_id: filters.value.subject || undefined,
      student_id: filters.value.student || undefined,
      search: filters.value.global || undefined,
    };
    const response = await api.get(endpoints.scores, { params });
    scores.value = Array.isArray(response.data.results) ? response.data.results : response.data;
    paginatorInfo.value.total = response.data.count || scores.value.length;
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách điểm', life: 3000 });
    scores.value = [];
  }
};
</script>

<style scoped>
.score-view-container {
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