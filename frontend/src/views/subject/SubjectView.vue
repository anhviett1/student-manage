<template>
  <div class="subject-view-container" aria-label="Trang quản lý môn học">
    <Toast aria-live="polite" />
    <ConfirmDialog aria-live="assertive" />
    <div v-if="isAdmin">
      <TabView v-model:activeIndex="activeTabIndex" scrollable class="tab-view" aria-label="Tab điều hướng môn học">
        <TabPanel header="Quản Lý Môn Học">
          <SubjectManagement
            :subjects="subjects"
            :filters="filters"
            :paginatorInfo="paginatorInfo"
            :departments="departments"
            :semesters="semesters"
            @update:subjects="updateSubjects"
            @loadSubjects="loadSubjects"
            @loadDepartments="loadDepartments"
            @loadSemesters="loadSemesters"
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
import SubjectManagement from '@/components/SubjectManagement.vue';
import api, { endpoints } from '@/services/api';

const userStore = useUserStore();
const toast = useToast();

const activeTabIndex = ref(0);
const subjects = ref([]);
const departments = ref([]);
const semesters = ref([]);
const filters = ref({ status: null, department: null, global: '' });
const paginatorInfo = ref({ rows: 10, page: 1, total: 0 });

const isAdmin = computed(() => userStore.isAdmin);

onMounted(async () => {
  gsap.from('.subject-view-container', { opacity: 0, y: 50, duration: 0.8, ease: 'power2.out' });
  if (isAdmin.value) {
    await Promise.all([loadSubjects(), loadDepartments(), loadSemesters()]);
  }
});

const loadSubjects = async (page = 1, rows = paginatorInfo.value.rows) => {
  try {
    const params = {
      page,
      page_size: rows,
      status: filters.value.status || undefined,
      department_id: filters.value.department || undefined,
      search: filters.value.global || undefined,
    };
    const response = await api.get(endpoints.subjects, { params });
    subjects.value = Array.isArray(response.data.results) ? response.data.results : response.data;
    paginatorInfo.value.total = response.data.count || subjects.value.length;
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách môn học', life: 3000 });
    subjects.value = [];
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

const loadSemesters = async () => {
  try {
    const response = await api.get(endpoints.semesters);
    semesters.value = Array.isArray(response.data.results) ? response.data.results : response.data;
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách học kỳ', life: 3000 });
    semesters.value = [];
  }
};

const updateSubjects = (newSubjects) => {
  subjects.value = newSubjects;
};
</script>

<style scoped>
.subject-view-container {
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