<template>
  <div class="class-view-container" aria-label="Trang quản lý lớp học">
    <Toast aria-live="polite" />
    <ConfirmDialog aria-live="assertive" />
    <TabView v-model:activeIndex="activeTabIndex" scrollable class="tab-view" aria-label="Tab điều hướng quản lý lớp học">
      <TabPanel header="Thông Tin Lớp" v-if="isTeacher || isStudent">
        <ClassInfo :classDetail="classDetail" :isEditing="isEditing" @update:classDetail="classDetail = $event" @update:isEditing="isEditing = $event" />
      </TabPanel>
      <TabPanel header="Quản Lý Lớp Học" v-if="canViewClasses">
        <ClassManagement :classes="classes" :filters="filters" :paginatorInfo="paginatorInfo" @update:classes="classes = $event" @loadClasses="loadClasses" />
      </TabPanel>
    </TabView>
    <div v-if="!canViewClasses" class="access-denied">
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
import ClassInfo from '@/components/ClassInfo.vue';
import ClassManagement from '@/components/ClassManagement.vue';
import api, { endpoints } from '@/services/api';

const userStore = useUserStore();
const toast = useToast();

const activeTabIndex = ref(0);
const classes = ref([]);
const classDetail = ref({});
const isEditing = ref(false);
const filters = ref({
  global: '',
  status: 'active',
  department: null,
  semester: null,
  subject: null,
});
const paginatorInfo = ref({ rows: 10, page: 1, total: 0 });

const isAdmin = computed(() => userStore.isAdmin);
const isTeacher = computed(() => userStore.isTeacher);
const isStudent = computed(() => userStore.isStudent);
const canViewClasses = computed(() => isAdmin.value || isTeacher.value || isStudent.value);

onMounted(async () => {
  gsap.from('.class-view-container', { opacity: 0, y: 50, duration: 0.8, ease: 'power2.out' });
  if (canViewClasses.value) {
    await loadClasses();
    if (isTeacher.value || isStudent.value) {
      await loadClassDetail();
    }
  }
});

const loadClasses = async (page = 1, rows = paginatorInfo.value.rows) => {
  if (!canViewClasses.value) return;
  try {
    const params = {
      page,
      page_size: rows,
      search: filters.value.global || undefined,
      status: filters.value.status || undefined,
      department_id: filters.value.department || undefined,
      semester_id: filters.value.semester || undefined,
      subject_id: filters.value.subject || undefined,
    };
    const response = await api.get(endpoints.classes, { params });
    classes.value = Array.isArray(response.data) ? response.data : response.data.results || [];
    paginatorInfo.value.total = response.data.count || classes.value.length;
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách lớp học', life: 3000 });
    classes.value = [];
  }
};

const loadClassDetail = async () => {
  if (classes.value.length > 0) {
    try {
      const response = await api.get(`${endpoints.classes}${classes.value[0].class_id}/`);
      classDetail.value = response.data;
    } catch (error) {
      toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải thông tin lớp', life: 3000 });
    }
  }
};
</script>

<style scoped>
.class-view-container {
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