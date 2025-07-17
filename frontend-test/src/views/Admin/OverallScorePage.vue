<template>
  <div class="overall-grades-page p-fluid">
    <h2 class="p-text-primary p-mb-4">Tổng quan Điểm số Hệ thống</h2>

    <div class="p-grid p-nogutter p-mb-4">
      <div class="p-col-12 p-md-6 p-lg-3 p-mb-3">
        <p-card class="average-score-card h-full">
          <template #title>
            <i class="pi pi-chart-line p-mr-2"></i> Điểm Trung Bình Chung
          </template>
          <template #content>
            <div v-if="loadingGradesStats" class="p-text-center">
              <p-progress-spinner style="width: 50px; height: 50px" strokeWidth="6" animationDuration=".8s" />
            </div>
            <div v-else class="p-text-center">
              <p class="p-text-6xl p-font-bold p-text-green-500">{{ gradesStats.average_grade ? gradesStats.average_grade.toFixed(2) : 'N/A' }}</p>
              <p class="p-text-sm p-text-color-secondary">Trên tất cả các môn học</p>
            </div>
          </template>
        </p-card>
      </div>
      <div class="p-col-12 p-md-6 p-lg-3 p-mb-3">
        <p-card class="pass-fail-card h-full">
          <template #title>
            <i class="pi pi-check-circle p-mr-2"></i> Tỷ Lệ Đỗ
          </template>
          <template #content>
            <div v-if="loadingGradesStats" class="p-text-center">
              <p-progress-spinner style="width: 50px; height: 50px" strokeWidth="6" animationDuration=".8s" />
            </div>
            <div v-else class="p-text-center">
              <p class="p-text-6xl p-font-bold p-text-blue-500">{{ gradesStats.pass_rate ? gradesStats.pass_rate.toFixed(1) : 'N/A' }}%</p>
              <p class="p-text-sm p-text-color-secondary">Tổng số đăng ký có điểm</p>
            </div>
          </template>
        </p-card>
      </div>
       <div class="p-col-12 p-md-6 p-lg-3 p-mb-3">
        <p-card class="fail-rate-card h-full">
          <template #title>
            <i class="pi pi-times-circle p-mr-2"></i> Tỷ Lệ Trượt
          </template>
          <template #content>
            <div v-if="loadingGradesStats" class="p-text-center">
              <p-progress-spinner style="width: 50px; height: 50px" strokeWidth="6" animationDuration=".8s" />
            </div>
            <div v-else class="p-text-center">
              <p class="p-text-6xl p-font-bold p-text-red-500">{{ gradesStats.fail_rate ? gradesStats.fail_rate.toFixed(1) : 'N/A' }}%</p>
              <p class="p-text-sm p-text-color-secondary">Tổng số đăng ký có điểm</p>
            </div>
          </template>
        </p-card>
      </div>
       <div class="p-col-12 p-md-6 p-lg-3 p-mb-3">
        <p-card class="total-enrollments-card h-full">
          <template #title>
            <i class="pi pi-users p-mr-2"></i> Tổng Số Bản Ghi Điểm
          </template>
          <template #content>
            <div v-if="loadingGradesStats" class="p-text-center">
              <p-progress-spinner style="width: 50px; height: 50px" strokeWidth="6" animationDuration=".8s" />
            </div>
            <div v-else class="p-text-center">
              <p class="p-text-6xl p-font-bold p-text-purple-500">{{ gradesStats.total_enrollments !== undefined ? gradesStats.total_enrollments : 'N/A' }}</p>
              <p class="p-text-sm p-text-color-secondary">Lượt đăng ký đã có điểm</p>
            </div>
          </template>
        </p-card>
      </div>
    </div>

    <div class="p-grid p-nogutter p-mt-4">
      <div class="p-col-12 p-lg-6 p-mb-4">
        <p-card class="grade-distribution-chart-card h-full">
          <template #title>
            <i class="pi pi-chart-pie p-mr-2"></i> Phân Phối Điểm
          </template>
          <template #content>
            <div v-if="loadingGradesStats" class="p-text-center">
              <p-progress-spinner />
            </div>
            <div v-else>
              <p-chart type="pie" :data="gradeDistributionChartData" :options="chartOptions" />
            </div>
          </template>
        </p-card>
      </div>

      <div class="p-col-12 p-lg-6 p-mb-4">
        <p-card class="top-bottom-courses-card h-full">
          <template #title>
            <i class="pi pi-list p-mr-2"></i> Môn Học Nổi Bật Về Điểm Số
          </template>
          <template #content>
            <div v-if="loadingGradesStats" class="p-text-center">
              <p-progress-spinner />
            </div>
            <div v-else>
              <h3 class="p-text-lg p-mb-2 p-text-green-600">Top 5 Môn Học Có Điểm Trung Bình Cao Nhất:</h3>
              <p-data-table :value="gradesStats.top_courses_by_avg_grade" stripedRows responsiveLayout="scroll">
                <p-column field="course_name" header="Tên Môn học"></p-column>
                <p-column field="average_grade" header="Điểm TB" :sortable="true">
                    <template #body="{ data }">
                        {{ data.average_grade ? data.average_grade.toFixed(2) : 'N/A' }}
                    </template>
                </p-column>
              </p-data-table>

              <h3 class="p-text-lg p-mt-4 p-mb-2 p-text-red-600">Top 5 Môn Học Có Tỷ Lệ Trượt Cao Nhất:</h3>
              <p-data-table :value="gradesStats.top_courses_by_fail_rate" stripedRows responsiveLayout="scroll">
                <p-column field="course_name" header="Tên Môn học"></p-column>
                <p-column field="fail_rate" header="Tỷ lệ Trượt" :sortable="true">
                    <template #body="{ data }">
                        {{ data.fail_rate ? data.fail_rate.toFixed(1) : 'N/A' }}%
                    </template>
                </p-column>
              </p-data-table>
            </div>
          </template>
        </p-card>
      </div>
    </div>

    <h3 class="p-text-primary p-mb-3 p-mt-5">Thống kê Người dùng và Phòng ban</h3>
    <div class="p-grid p-nogutter p-mb-4">
        <div class="p-col-12 p-md-6 p-lg-3 p-mb-3">
            <p-card class="user-stats-card h-full">
                <template #title>
                    <i class="pi pi-users p-mr-2"></i> Tổng Người dùng
                </template>
                <template #content>
                    <div v-if="loadingOverallStats" class="p-text-center">
                        <p-progress-spinner style="width: 50px; height: 50px" strokeWidth="6" animationDuration=".8s" />
                    </div>
                    <div v-else class="p-text-center">
                        <p class="p-text-6xl p-font-bold p-text-gray-700">{{ userStats.total_users !== undefined ? userStats.total_users : 'N/A' }}</p>
                        <p class="p-text-sm p-text-color-secondary">Tất cả người dùng hệ thống</p>
                    </div>
                </template>
            </p-card>
        </div>
        <div class="p-col-12 p-md-6 p-lg-3 p-mb-3">
            <p-card class="user-roles-card h-full">
                <template #title>
                    <i class="pi pi-user-plus p-mr-2"></i> Theo Vai trò
                </template>
                <template #content>
                    <div v-if="loadingOverallStats" class="p-text-center">
                        <p-progress-spinner style="width: 50px; height: 50px" strokeWidth="6" animationDuration=".8s" />
                    </div>
                    <ul v-else class="role-list p-0 p-m-0 p-text-left">
                        <li><i class="pi pi-user p-mr-2"></i> Sinh viên: <span class="p-text-bold">{{ userStats.students !== undefined ? userStats.students : 'N/A' }}</span></li>
                        <li><i class="pi pi-briefcase p-mr-2"></i> Giáo viên: <span class="p-text-bold">{{ userStats.teachers !== undefined ? userStats.teachers : 'N/A' }}</span></li>
                        <li><i class="pi pi-id-card p-mr-2"></i> Quản trị viên: <span class="p-text-bold">{{ userStats.admins !== undefined ? userStats.admins : 'N/A' }}</span></li>
                    </ul>
                </template>
            </p-card>
        </div>
         <div class="p-col-12 p-md-6 p-lg-3 p-mb-3">
            <p-card class="department-stats-card h-full">
                <template #title>
                    <i class="pi pi-building p-mr-2"></i> Tổng Khoa/Phòng ban
                </template>
                <template #content>
                    <div v-if="loadingOverallStats" class="p-text-center">
                        <p-progress-spinner style="width: 50px; height: 50px" strokeWidth="6" animationDuration=".8s" />
                    </div>
                    <div v-else class="p-text-center">
                        <p class="p-text-6xl p-font-bold p-text-indigo-500">{{ departmentStats.total_departments !== undefined ? departmentStats.total_departments : 'N/A' }}</p>
                        <p class="p-text-sm p-text-color-secondary">Tổng số phòng ban hoạt động</p>
                    </div>
                </template>
            </p-card>
        </div>
         <div class="p-col-12 p-md-6 p-lg-3 p-mb-3">
            <p-card class="active-department-card h-full">
                <template #title>
                    <i class="pi pi-check-square p-mr-2"></i> Khoa/Phòng ban Hoạt động
                </template>
                <template #content>
                    <div v-if="loadingOverallStats" class="p-text-center">
                        <p-progress-spinner style="width: 50px; height: 50px" strokeWidth="6" animationDuration=".8s" />
                    </div>
                    <div v-else class="p-text-center">
                        <p class="p-text-6xl p-font-bold p-text-teal-500">{{ departmentStats.active_departments !== undefined ? departmentStats.active_departments : 'N/A' }}</p>
                        <p class="p-text-sm p-text-color-secondary">Đang trong trạng thái hoạt động</p>
                    </div>
                </template>
            </p-card>
        </div>
    </div>


    <div class="p-mt-4 p-text-center">
        <small class="p-text-color-secondary">Dữ liệu thống kê được cập nhật định kỳ từ hệ thống.</small>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useNotificationStore } from '@/stores/notification';

// PrimeVue Components
import PCard from 'primevue/card';
import PProgressSpinner from 'primevue/progressspinner';
import PChart from 'primevue/chart';
import PDataTable from 'primevue/datatable';
import PColumn from 'primevue/column';

// --- API Client (giả lập) ---
const statisticsApi = {
  getOverallStats: async () => {
    // Đây là nơi gọi API StatisticsAPIView của bạn
    // Ví dụ: const response = await axios.get('/api/statistics/');
    // Hiện tại là dữ liệu mô phỏng giống với cấu trúc API đã sửa đổi
    return new Promise(resolve => setTimeout(() => {
      resolve({
        users: {
            total_users: 1500,
            active_users: 1450,
            students: 1200,
            teachers: 250,
            admins: 50,
        },
        departments: {
            total_departments: 15,
            active_departments: 12,
        },
        grades: {
            average_grade: 7.85,
            pass_rate: 92.5,
            fail_rate: 7.5,
            total_enrollments: 1250,
            grade_distribution: {
              'A': 250, 'B': 500, 'C': 300, 'D': 150, 'F': 50
            },
            top_courses_by_avg_grade: [
              { course_name: 'Lập trình Python Nâng cao', average_grade: 9.1 },
              { course_name: 'Trí tuệ nhân tạo cơ bản', average_grade: 8.9 },
              { course_name: 'Thiết kế đồ họa số', average_grade: 8.8 },
              { course_name: 'Cấu trúc dữ liệu và giải thuật', average_grade: 8.7 },
              { course_name: 'Hệ thống quản lý cơ sở dữ liệu', average_grade: 8.5 },
            ],
            top_courses_by_fail_rate: [
              { course_name: 'Giải tích 1', fail_rate: 35.2 },
              { course_name: 'Vật lý Đại cương 1', fail_rate: 28.5 },
              { course_name: 'Đại số tuyến tính', fail_rate: 22.1 },
              { course_name: 'Lý thuyết mạch', fail_rate: 18.0 },
              { course_name: 'Nguyên lý kế toán', fail_rate: 15.5 },
            ]
        }
      });
    }, 800));
  }
};

const notificationStore = useNotificationStore();

// Dữ liệu cho các phần thống kê
const userStats = ref({});
const departmentStats = ref({});
const gradesStats = ref({});

const loadingOverallStats = ref(true); // Gộp chung loading cho tất cả stats

// Dữ liệu và tùy chọn cho biểu đồ phân phối điểm
const gradeDistributionChartData = ref({
  labels: [],
  datasets: [{
    data: [],
    backgroundColor: ['#42A5F5', '#66BB6A', '#FFA726', '#FFCA28', '#EF5350'], // Màu cho A, B, C, D, F
    hoverBackgroundColor: ['#64B5F6', '#81C784', '#FFB74D', '#FFEE58', '#FF7043']
  }]
});

const chartOptions = ref({
  plugins: {
    legend: {
      position: 'top'
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          let label = context.label || '';
          if (label) {
            label += ': ';
          }
          if (context.parsed !== null) {
            label += context.parsed + ' sinh viên'; // Hoặc percentage
          }
          return label;
        }
      }
    }
  },
  animation: {
    duration: 1000,
    easing: 'easeOutQuart'
  }
});


// --- Lifecycle Hook ---
onMounted(() => {
  fetchOverallStats();
});

// --- Data Fetching Functions ---
const fetchOverallStats = async () => {
  loadingOverallStats.value = true;
  try {
    const data = await statisticsApi.getOverallStats();
    userStats.value = data.users;
    departmentStats.value = data.departments;
    gradesStats.value = data.grades;

    // Chuẩn bị dữ liệu cho biểu đồ phân phối điểm
    const distribution = data.grades.grade_distribution;
    if (distribution) {
      gradeDistributionChartData.value = {
        labels: Object.keys(distribution),
        datasets: [{
          data: Object.values(distribution),
          backgroundColor: ['#42A5F5', '#66BB6A', '#FFA726', '#FFCA28', '#EF5350'],
          hoverBackgroundColor: ['#64B5F6', '#81C784', '#FFB74D', '#FFEE58', '#FF7043']
        }]
      };
    }


    notificationStore.showToast('Thành công', 'Tải dữ liệu thống kê hệ thống thành công!', 'success');
  } catch (error) {
    console.error('Error fetching overall stats:', error);
    notificationStore.showToast('Lỗi', 'Không thể tải dữ liệu thống kê hệ thống.', 'error');
  } finally {
    loadingOverallStats.value = false;
  }
};
</script>

<style scoped>
.overall-grades-page {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.p-mb-4 {
  margin-bottom: 1.5rem !important;
}

.p-mt-4 {
  margin-top: 1.5rem !important;
}

.p-mb-3 {
    margin-bottom: 1rem !important;
}

.p-mt-5 {
    margin-top: 2rem !important;
}

.h-full {
  height: 100%;
}

/* Custom card styles for visual distinction */
.average-score-card /deep/ .p-card-content,
.pass-fail-card /deep/ .p-card-content,
.fail-rate-card /deep/ .p-card-content,
.total-enrollments-card /deep/ .p-card-content,
.user-stats-card /deep/ .p-card-content,
.department-stats-card /deep/ .p-card-content,
.active-department-card /deep/ .p-card-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 120px; /* Đảm bảo chiều cao tối thiểu */
}

.user-roles-card /deep/ .p-card-content {
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 120px;
    padding: 1.5rem; /* Căn chỉnh lại padding cho list */
}

.role-list {
    list-style: none;
    line-height: 2.2;
    font-size: 1.1em;
}

/* Responsive adjustments for columns */
@media screen and (min-width: 992px) {
    .p-lg-3 {
        padding-right: 0.75rem; /* Gap giữa các card */
        padding-left: 0.75rem;
    }
     .p-col-12.p-md-6.p-lg-3:nth-child(4n) { /* Adjust margin for the last card in the row */
        padding-right: 0;
     }
     .p-col-12.p-md-6.p-lg-3:nth-child(4n+1) { /* Adjust margin for the first card in the row */
        padding-left: 0;
     }
}

.grade-distribution-chart-card /deep/ .p-card-content,
.top-bottom-courses-card /deep/ .p-card-content {
  padding-top: 0; /* Remove top padding if desired */
}
</style>