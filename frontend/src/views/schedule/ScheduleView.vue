<template>
  <div class="schedule-view-container" aria-label="Trang quản lý lịch học">
    <Toast aria-live="polite" />
    <ConfirmDialog aria-live="assertive" />
    <TabView v-model:activeIndex="activeTabIndex" scrollable class="tab-view" aria-label="Tab điều hướng lịch học">
      <TabPanel header="Lịch Học Của Tôi" v-if="isStudent">
        <MySchedules
          :mySchedules="mySchedules"
          :studentFilters="studentFilters"
          :paginatorInfo="paginatorInfo"
          @update:mySchedules="mySchedules = $event"
          @loadMySchedules="loadMySchedules"
        />
      </TabPanel>
      <TabPanel header="Lịch Giảng Dạy" v-if="isTeacher">
        <MySchedules
          :mySchedules="teacherSchedules"
          :studentFilters="teacherFilters"
          :paginatorInfo="paginatorInfo"
          @update:mySchedules="teacherSchedules = $event"
          @loadMySchedules="loadTeacherSchedules"
          isTeacherView
        />
      </TabPanel>
      <TabPanel header="Quản Lý Lịch Học" v-if="isAdmin">
        <ScheduleManagement
          :schedules="schedules"
          :filters="filters"
          :paginatorInfo="paginatorInfo"
          @update:schedules="schedules = $event"
          @loadSchedules="loadSchedules"
        />
      </TabPanel>
    </TabView>
    <div v-if="!canViewSchedules && !isStudent" class="access-denied">
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
import MySchedules from '@/components/MySchedules.vue';
import ScheduleManagement from '@/components/ScheduleManagement.vue';
import api, { endpoints } from '@/services/api';

const userStore = useUserStore();
const toast = useToast();

const activeTabIndex = ref(0);
const mySchedules = ref([]);
const teacherSchedules = ref([]);
const schedules = ref([]);
const studentFilters = ref({ semester: null, status: null, global: '' });
const teacherFilters = ref({ semester: null, status: null, global: '' });
const filters = ref({
  status: null,
  semester: null,
  class_assigned: null,
  teacher: null,
  day_of_week: null,
  global: '',
});
const paginatorInfo = ref({ rows: 10, page: 1, total: 0 });

const isStudent = computed(() => userStore.isStudent);
const isTeacher = computed(() => userStore.isTeacher);
const isAdmin = computed(() => userStore.isAdmin);
const canViewSchedules = computed(() => userStore.isAdmin || userStore.isTeacher);

onMounted(async () => {
  gsap.from('.schedule-view-container', { opacity: 0, y: 50, duration: 0.8, ease: 'power2.out' });
  if (isStudent.value) await loadMySchedules();
  if (isTeacher.value) await loadTeacherSchedules();
  if (isAdmin.value) await loadSchedules();
});

const loadMySchedules = async (page = 1, rows = paginatorInfo.value.rows) => {
  if (!isStudent.value) return;
  try {
    const params = {
      page,
      page_size: rows,
      semester: studentFilters.value.semester || undefined,
      status: studentFilters.value.status || undefined,
      search: studentFilters.value.global || undefined,
      student: userStore.user?.id,
    };
    const response = await api.get(endpoints.schedules, { params });
    mySchedules.value = Array.isArray(response.data.results) ? response.data.results : response.data;
    paginatorInfo.value.total = response.data.count || mySchedules.value.length;
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải lịch học', life: 3000 });
    mySchedules.value = [];
  }
};

const loadTeacherSchedules = async (page = 1, rows = paginatorInfo.value.rows) => {
  if (!isTeacher.value) return;
  try {
    const params = {
      page,
      page_size: rows,
      semester: teacherFilters.value.semester || undefined,
      status: teacherFilters.value.status || undefined,
      search: teacherFilters.value.global || undefined,
      teacher: userStore.user?.id,
    };
    const response = await api.get(endpoints.schedules, { params });
    teacherSchedules.value = Array.isArray(response.data.results) ? response.data.results : response.data;
    paginatorInfo.value.total = response.data.count || teacherSchedules.value.length;
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải lịch giảng dạy', life: 3000 });
    teacherSchedules.value = [];
  }
};

const loadSchedules = async (page = 1, rows = paginatorInfo.value.rows) => {
  if (!isAdmin.value) return;
  try {
    const params = {
      page,
      page_size: rows,
      status: filters.value.status || undefined,
      semester: filters.value.semester || undefined,
      class_assigned: filters.value.class_assigned || undefined,
      teacher: filters.value.teacher || undefined,
      day_of_week: filters.value.day_of_week || undefined,
      search: filters.value.global || undefined,
    };
    const response = await api.get(endpoints.schedules, { params });
    schedules.value = Array.isArray(response.data.results) ? response.data.results : response.data;
    paginatorInfo.value.total = response.data.count || schedules.value.length;
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách lịch học', life: 3000 });
    schedules.value = [];
  }
};
</script>

<style scoped>
.schedule-view-container {
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