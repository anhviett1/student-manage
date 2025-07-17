<template>
  <div class="enrollments-page">
    <h2 class="p-text-primary p-mb-4">Quản lý Đăng ký môn học</h2>

    <div class="p-mb-4 p-flex p-justify-content-between p-align-center">
      <p-button label="Thêm đăng ký mới" icon="pi pi-plus" @click="openNewEnrollmentDialog" />
    </div>

    <BaseTable
      :data="enrollments"
      :columns="enrollmentTableColumns"
      :loading="loadingEnrollments"
      :enable-pagination="true"
      :current-page="pagination.currentPage"
      :total-records="pagination.totalRecords"
      :items-per-page="pagination.itemsPerPage"
      @page-change="onPageChange"
    >
      <template #actions="{ item }">
        <p-button icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm p-mr-1" @click="editEnrollment(item)" />
        <p-button icon="pi pi-trash" class="p-button-rounded p-button-text p-button-danger p-button-sm" @click="confirmDeleteEnrollment(item)" />
      </template>
    </BaseTable>

    <p-dialog v-model:visible="enrollmentDialogVisible" modal :header="dialogHeader" :style="{ width: '50vw' }" :breakpoints="{'960px': '75vw', '641px': '100vw'}">
      <EnrollmentForm
        :initial-data="selectedEnrollment"
        :is-edit-mode="isEditMode"
        :is-loading="savingEnrollment"
        :students="students"
        :courses="courses"
        :semesters="semesters"
        @submit="saveEnrollment"
        @cancel="enrollmentDialogVisible = false"
      />
    </p-dialog>

    <ConfirmationDialog
      :is-visible="deleteEnrollmentDialogVisible"
      title="Xác nhận xóa đăng ký"
      :message="`Bạn có chắc chắn muốn xóa đăng ký môn học '${enrollmentToDelete?.course_name}' của sinh viên '${enrollmentToDelete?.student_name}' không?`"
      @confirm="deleteEnrollment"
      @cancel="deleteEnrollmentDialogVisible = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useNotificationStore } from '@/stores/notification';
import BaseTable from '@/components/common/BaseTable.vue'; // Giả định đường dẫn
import ConfirmationDialog from '@/components/common/ConfirmationDialog.vue'; // Giả định đường dẫn
import EnrollmentForm from './EnrollmentForm.vue'; // Đường dẫn đến EnrollmentForm.vue

// PrimeVue Components
import PButton from 'primevue/button';
import PDialog from 'primevue/dialog';

// --- Giả lập API cho Đăng ký môn học ---
const enrollmentApi = {
  getEnrollments: async (page, limit) => {
    const allEnrollments = [
      { id: 1, student_id: 1, student_name: 'Nguyễn Văn A', student_code: 'SV001', course_id: 101, course_name: 'Lập trình Web', semester_id: 1, semester_name: 'HK1 2023-2024', enrollment_date: '2023-09-01' },
      { id: 2, student_id: 2, student_name: 'Trần Thị B', student_code: 'SV002', course_id: 102, course_name: 'Cấu trúc dữ liệu', semester_id: 1, semester_name: 'HK1 2023-2024', enrollment_date: '2023-09-02' },
      { id: 3, student_id: 1, student_name: 'Nguyễn Văn A', student_code: 'SV001', course_id: 103, course_name: 'Kinh tế vi mô', semester_id: 2, semester_name: 'HK2 2023-2024', enrollment_date: '2024-02-05' },
      { id: 4, student_id: 3, student_name: 'Lê Văn C', student_code: 'SV003', course_id: 101, course_name: 'Lập trình Web', semester_id: 2, semester_name: 'HK2 2023-2024', enrollment_date: '2024-02-06' },
      { id: 5, student_id: 2, student_name: 'Trần Thị B', student_code: 'SV002', course_id: 104, course_name: 'Toán cao cấp A1', semester_id: 1, semester_name: 'HK1 2023-2024', enrollment_date: '2023-09-03' },
    ];
    const start = (page - 1) * limit;
    const end = start + limit;
    return new Promise(resolve => setTimeout(() => {
      resolve({
        data: allEnrollments.slice(start, end),
        total: allEnrollments.length
      });
    }, 500));
  },
  createEnrollment: async (enrollmentData) => {
    console.log('Creating enrollment:', enrollmentData);
    return new Promise(resolve => setTimeout(() => resolve({ success: true, id: Math.floor(Math.random() * 1000) }), 300));
  },
  updateEnrollment: async (id, enrollmentData) => {
    console.log(`Updating enrollment ${id}:`, enrollmentData);
    return new Promise(resolve => setTimeout(() => resolve({ success: true }), 300));
  },
  deleteEnrollment: async (id) => {
    console.log('Deleting enrollment with ID:', id);
    return new Promise(resolve => setTimeout(() => resolve({ success: true }), 300));
  }
};

// --- Giả lập API cho các Dropdown trong form ---
// Trong một ứng dụng thực tế, bạn sẽ có các API endpoint riêng biệt cho từng loại này
const lookupApi = {
  getStudents: async () => {
    return new Promise(resolve => setTimeout(() => {
      resolve([
        { id: 1, full_name: 'Nguyễn Văn A', student_id: 'SV001' },
        { id: 2, full_name: 'Trần Thị B', student_id: 'SV002' },
        { id: 3, full_name: 'Lê Văn C', student_id: 'SV003' },
      ]);
    }, 200));
  },
  getCourses: async () => {
    return new Promise(resolve => setTimeout(() => {
      resolve([
        { id: 101, name: 'Lập trình Web', code: 'IT4001' },
        { id: 102, name: 'Cấu trúc dữ liệu', code: 'CS3002' },
        { id: 103, name: 'Kinh tế vi mô', code: 'EC2001' },
        { id: 104, name: 'Toán cao cấp A1', code: 'MA1001' },
      ]);
    }, 200));
  },
  getSemesters: async () => {
    return new Promise(resolve => setTimeout(() => {
      resolve([
        { id: 1, name: 'HK1 2023-2024' },
        { id: 2, name: 'HK2 2023-2024' },
        { id: 3, name: 'HK hè 2024' },
      ]);
    }, 200));
  }
};

const notificationStore = useNotificationStore();

const enrollments = ref([]);
const loadingEnrollments = ref(false);
const enrollmentDialogVisible = ref(false);
const isEditMode = ref(false);
const selectedEnrollment = ref(null);
const dialogHeader = ref('');
const savingEnrollment = ref(false);

const deleteEnrollmentDialogVisible = ref(false);
const enrollmentToDelete = ref(null);

// Dữ liệu cho các dropdown trong form
const students = ref([]);
const courses = ref([]);
const semesters = ref([]);

const pagination = ref({
  currentPage: 1,
  itemsPerPage: 10,
  totalRecords: 0
});

// Định nghĩa cột cho bảng đăng ký
const enrollmentTableColumns = [
  { field: 'id', header: 'ID', type: 'number' },
  { field: 'student_code', header: 'Mã SV', type: 'string' },
  { field: 'student_name', header: 'Tên Sinh viên', type: 'string' },
  { field: 'course_name', header: 'Tên Môn học', type: 'string' },
  { field: 'semester_name', header: 'Học kỳ', type: 'string' },
  { field: 'enrollment_date', header: 'Ngày ĐK', type: 'date' },
];

// --- Lifecycle Hook ---
onMounted(() => {
  fetchEnrollments();
  fetchLookupData(); // Tải dữ liệu cho dropdown khi mount
});

// --- Data Fetching Functions ---
const fetchEnrollments = async () => {
  loadingEnrollments.value = true;
  try {
    const response = await enrollmentApi.getEnrollments(pagination.value.currentPage, pagination.value.itemsPerPage);
    enrollments.value = response.data;
    pagination.value.totalRecords = response.total;
    notificationStore.showToast('Thành công', 'Tải danh sách đăng ký thành công!', 'success');
  } catch (error) {
    console.error('Error fetching enrollments:', error);
    notificationStore.showToast('Lỗi', 'Không thể tải danh sách đăng ký.', 'error');
  } finally {
    loadingEnrollments.value = false;
  }
};

const fetchLookupData = async () => {
  try {
    students.value = await lookupApi.getStudents();
    courses.value = await lookupApi.getCourses();
    semesters.value = await lookupApi.getSemesters();
  } catch (error) {
    console.error('Error fetching lookup data:', error);
    notificationStore.showToast('Lỗi', 'Không thể tải dữ liệu cần thiết cho form.', 'error');
  }
};

// --- Dialog and Form Control Functions ---
const openNewEnrollmentDialog = () => {
  isEditMode.value = false;
  selectedEnrollment.value = {
    student_id: null, course_id: null, semester_id: null, enrollment_date: null
  };
  dialogHeader.value = 'Thêm Đăng ký Mới';
  enrollmentDialogVisible.value = true;
};

const editEnrollment = (enrollment) => {
  isEditMode.value = true;
  // Sao chép sâu để tránh mutation trực tiếp và đảm bảo dữ liệu mới
  selectedEnrollment.value = { ...enrollment };
  // EnrollmentForm sẽ tự động chuyển đổi chuỗi ngày thành Date objects nhờ watch bên trong nó
  dialogHeader.value = `Chỉnh sửa Đăng ký: ${enrollment.student_name} - ${enrollment.course_name}`;
  enrollmentDialogVisible.value = true;
};

const saveEnrollment = async (formData) => {
  savingEnrollment.value = true;
  try {
    if (isEditMode.value) {
      await enrollmentApi.updateEnrollment(selectedEnrollment.value.id, formData);
      notificationStore.showToast('Thành công', 'Cập nhật đăng ký thành công!', 'success');
    } else {
      await enrollmentApi.createEnrollment(formData);
      notificationStore.showToast('Thành công', 'Thêm đăng ký mới thành công!', 'success');
    }
    enrollmentDialogVisible.value = false;
    await fetchEnrollments(); // Cập nhật lại bảng sau khi lưu
  } catch (error) {
    console.error('Error saving enrollment:', error);
    notificationStore.showToast('Lỗi', 'Có lỗi xảy ra khi lưu đăng ký.', 'error');
  } finally {
    savingEnrollment.value = false;
  }
};

// --- Delete Enrollment Functions ---
const confirmDeleteEnrollment = (enrollment) => {
  enrollmentToDelete.value = enrollment;
  deleteEnrollmentDialogVisible.value = true;
};

const deleteEnrollment = async () => {
  deleteEnrollmentDialogVisible.value = false;
  if (!enrollmentToDelete.value) return;

  loadingEnrollments.value = true; // Hiển thị loading khi xóa
  try {
    await enrollmentApi.deleteEnrollment(enrollmentToDelete.value.id);
    notificationStore.showToast('Thành công', 'Xóa đăng ký thành công!', 'success');
    await fetchEnrollments(); // Cập nhật lại bảng sau khi xóa
  } catch (error) {
    console.error('Error deleting enrollment:', error);
    notificationStore.showToast('Lỗi', 'Không thể xóa đăng ký.', 'error');
  } finally {
    loadingEnrollments.value = false;
    enrollmentToDelete.value = null; // Xóa đối tượng cần xóa
  }
};

// --- Pagination Handler ---
const onPageChange = (event) => {
  pagination.value.currentPage = event.page + 1; // PrimeVue page starts from 0
  pagination.value.itemsPerPage = event.rows;
  fetchEnrollments();
};
</script>

<style scoped>
.enrollments-page {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.p-mb-4 {
  margin-bottom: 1.5rem !important;
}

.p-flex {
    display: flex;
}

.p-justify-content-between {
    justify-content: space-between;
}

.p-align-center {
    align-items: center;
}
</style>