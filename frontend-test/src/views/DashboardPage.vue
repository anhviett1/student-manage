<template>
  <div class="p-p-4">
    <h1>Chào mừng bạn đến với Hệ thống quản lý sinh viên!</h1>
    <p>Trang này sẽ chuyển hướng bạn đến dashboard phù hợp với vai trò của bạn.</p>

    <div class="p-d-flex p-flex-wrap p-gap-3 p-mt-4">
      <Card style="width: 20rem; margin-bottom: 2em">
        <template #title>Admin</template>
        <template #content>
          <p class="p-m-0">
            Truy cập bảng điều khiển quản trị để quản lý toàn bộ hệ thống.
          </p>
        </template>
        <template #footer>
          <Button label="Đi tới Admin Dashboard" icon="pi pi-chart-line" @click="$router.push('/admin/dashboard')" />
        </template>
      </Card>

      <Card style="width: 20rem; margin-bottom: 2em">
        <template #title>Giáo viên</template>
        <template #content>
          <p class="p-m-0">
            Truy cập bảng điều khiển giáo viên để quản lý lớp học và điểm số.
          </p>
        </template>
        <template #footer>
          <Button label="Đi tới Teacher Dashboard" icon="pi pi-users" @click="$router.push('/teacher/dashboard')" />
        </template>
      </Card>

      <Card style="width: 20rem; margin-bottom: 2em">
        <template #title>Sinh viên</template>
        <template #content>
          <p class="p-m-0">
            Truy cập bảng điều khiển sinh viên để xem lịch học và điểm số.
          </p>
        </template>
        <template #footer>
          <Button label="Đi tới Student Dashboard" icon="pi pi-user" @click="$router.push('/student/dashboard')" />
        </template>
      </Card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardPage',
  mounted() {
    // Logic thực tế có thể kiểm tra vai trò người dùng đã đăng nhập và tự động chuyển hướng
    // Ví dụ:
    const userRole = localStorage.getItem('userRole'); // Giả sử role được lưu trong localStorage
    if (userRole === 'admin') {
      this.$router.push('/admin/dashboard');
    } else if (userRole === 'teacher') {
      this.$router.push('/teacher/dashboard');
    } else if (userRole === 'student') {
      this.$router.push('/student/dashboard');
    } else {
      // Optionally redirect to login if no role or invalid session
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
.p-card {
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  border-radius: 8px;
}
</style>