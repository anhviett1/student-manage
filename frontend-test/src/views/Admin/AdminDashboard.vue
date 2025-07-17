<template>
  <div class="p-p-4">
    <h1><i class="pi pi-chart-line p-mr-2"></i>Admin Dashboard</h1>
    <p>Tổng quan hệ thống và các số liệu thống kê quan trọng.</p>

    <div class="p-grid p-gap-3 p-mb-4">
      <div class="p-col-12 p-md-6 p-lg-3">
        <Card class="dashboard-card">
          <template #title>Tổng số Sinh viên</template>
          <template #content>
            <div class="p-text-center">
              <i class="pi pi-user" style="font-size: 2.5rem; color: var(--primary-color);"></i>
              <p class="count-number">{{ stats.totalStudents }}</p>
            </div>
          </template>
        </Card>
      </div>
      <div class="p-col-12 p-md-6 p-lg-3">
        <Card class="dashboard-card">
          <template #title>Tổng số Giáo viên</template>
          <template #content>
            <div class="p-text-center">
              <i class="pi pi-users" style="font-size: 2.5rem; color: var(--green-500);"></i>
              <p class="count-number">{{ stats.totalTeachers }}</p>
            </div>
          </template>
        </Card>
      </div>
      <div class="p-col-12 p-md-6 p-lg-3">
        <Card class="dashboard-card">
          <template #title>Tổng số Lớp học</template>
          <template #content>
            <div class="p-text-center">
              <i class="pi pi-book" style="font-size: 2.5rem; color: var(--orange-500);"></i>
              <p class="count-number">{{ stats.totalClasses }}</p>
            </div>
          </template>
        </Card>
      </div>
      <div class="p-col-12 p-md-6 p-lg-3">
        <Card class="dashboard-card">
          <template #title>Tổng số Môn học</template>
          <template #content>
            <div class="p-text-center">
              <i class="pi pi-clone" style="font-size: 2.5rem; color: var(--blue-500);"></i>
              <p class="count-number">{{ stats.totalSubjects }}</p>
            </div>
          </template>
        </Card>
      </div>
    </div>

    <h2>Thống kê chi tiết</h2>
    <div class="p-card p-p-4">
      <p>Các biểu đồ và báo cáo chi tiết về sinh viên, giáo viên, điểm số sẽ được tích hợp tại đây.</p>
      <div class="p-d-flex p-jc-center p-ai-center" style="height: 200px; border: 1px dashed #ccc; border-radius: 8px;">
        <p>Biểu đồ thống kê sẽ hiển thị tại đây</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminDashboard',
  data() {
    return {
      stats: {
        totalStudents: 0,
        totalTeachers: 0,
        totalClasses: 0,
        totalSubjects: 0,
      },
    };
  },
  mounted() {
    this.fetchDashboardStats();
  },
  methods: {
    async fetchDashboardStats() {
      // Giả lập việc lấy dữ liệu từ API
      await new Promise(resolve => setTimeout(resolve, 500));
      this.stats = {
        totalStudents: 1500,
        totalTeachers: 120,
        totalClasses: 80,
        totalSubjects: 45,
      };
    },
  },
};
</script>

<style scoped>
.dashboard-card {
  height: 100%;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.count-number {
  font-size: 2.5rem;
  font-weight: bold;
  margin-top: 10px;
  color: var(--text-color);
}
</style>