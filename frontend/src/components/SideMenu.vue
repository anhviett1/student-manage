<template>
  <nav class="dashboard-menu">
    <div v-for="item in menuItems" :key="item.label">
      <router-link
        v-if="!item.children"
        :to="item.to"
        class="menu-item"
      >
        <i :class="item.icon" class="mr-2"></i>
        {{ item.label }}
      </router-link>
      <div v-else class="menu-group">
        <div class="menu-item parent">
          <i :class="item.icon" class="mr-2"></i>
          {{ item.label }}
        </div>
        <div class="submenu">
          <router-link
            v-for="child in item.children"
            :key="child.to"
            :to="child.to"
            class="menu-item submenu-item"
          >
            {{ child.label }}
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue';
import { usePermissions } from '@/composables/usePermissions';

const { userRole } = usePermissions();

const menuItems = computed(() => {
  if (!userRole.value) return [];
  if (userRole.value === 'admin') {
    return [
      { to: '/admin-dashboard', label: 'Tổng Quan', icon: 'pi pi-home' },
      {
        label: 'Quản lý Sinh viên', icon: 'pi pi-users',
        children: [
          { to: '/admin-dashboard/students', label: 'Danh sách sinh viên' },
          { to: '/admin-dashboard/student-view', label: 'Xem chi tiết' },
        ],
      },
      {
        label: 'Quản lý Giảng viên', icon: 'pi pi-user-plus',
        children: [
          { to: '/admin-dashboard/teachers', label: 'Danh sách giảng viên' },
          { to: '/admin-dashboard/teacher-view', label: 'Xem chi tiết' },
        ],
      },
      { to: '/admin-dashboard/profile', label: 'Hồ sơ cá nhân', icon: 'pi pi-user' },
      {
        label: 'Quản lý Lớp học', icon: 'pi pi-book',
        children: [
          { to: '/admin-dashboard/classes', label: 'Danh sách lớp học' },
          { to: '/admin-dashboard/class-view', label: 'Xem chi tiết' },
        ],
      },
      {
        label: 'Quản lý Môn học', icon: 'pi pi-file',
        children: [
          { to: '/admin-dashboard/subjects', label: 'Danh sách môn học' },
          { to: '/admin-dashboard/subject-view', label: 'Xem chi tiết' },
        ],
      },
      {
        label: 'Quản lý Ghi danh', icon: 'pi pi-check-square',
        children: [
          { to: '/admin-dashboard/enrollments', label: 'Danh sách ghi danh' },
          { to: '/admin-dashboard/enrollment-view', label: 'Xem chi tiết' },
        ],
      },
      {
        label: 'Quản lý Học kỳ', icon: 'pi pi-calendar',
        children: [
          { to: '/admin-dashboard/semesters', label: 'Học kỳ đang hoạt động' },
          { to: '/admin-dashboard/finished-semesters', label: 'Học kỳ đã kết thúc' },
        ],
      },
      { to: '/admin-dashboard/scores', label: 'Quản lý Điểm số', icon: 'pi pi-chart-bar' },
      { to: '/admin-dashboard/schedules', label: 'Thời khóa biểu', icon: 'pi pi-clock' },
      { to: '/admin-dashboard/departments', label: 'Quản lý Khoa', icon: 'pi pi-building' },
      { to: '/admin-dashboard/activities', label: 'Lịch sử hoạt động', icon: 'pi pi-history' },
    ];
  }
  if (userRole.value === 'teacher') {
    return [
      { to: '/teacher-dashboard', label: 'Tổng Quan', icon: 'pi pi-home' },
      { to: '/teacher-dashboard/profile', label: 'Hồ sơ cá nhân', icon: 'pi pi-user' },
      {
        label: 'Lớp học', icon: 'pi pi-book',
        children: [
          { to: '/teacher-dashboard/classes', label: 'Danh sách lớp học' },
          { to: '/teacher-dashboard/class-view', label: 'Xem chi tiết' },
        ],
      },
      {
        label: 'Môn học', icon: 'pi pi-file',
        children: [
          { to: '/teacher-dashboard/subjects', label: 'Danh sách môn học' },
          { to: '/teacher-dashboard/subject-view', label: 'Xem chi tiết' },
        ],
      },
      { to: '/teacher-dashboard/scores', label: 'Quản lý Điểm số', icon: 'pi pi-chart-bar' },
      { to: '/teacher-dashboard/schedules', label: 'Thời khóa biểu', icon: 'pi pi-clock' },
      { to: '/teacher-dashboard/activities', label: 'Lịch sử hoạt động', icon: 'pi pi-history' },
    ];
  }
  if (userRole.value === 'student') {
    return [
      { to: '/student-dashboard', label: 'Tổng Quan', icon: 'pi pi-home' },
      { to: '/student-dashboard/profile', label: 'Hồ sơ cá nhân', icon: 'pi pi-user' },
      { to: '/student-dashboard/my-scores', label: 'Điểm số', icon: 'pi pi-chart-bar' },
      { to: '/student-dashboard/my-schedules', label: 'Thời khóa biểu', icon: 'pi pi-clock' },
      {
        label: 'Ghi danh', icon: 'pi pi-check-square',
        children: [
          { to: '/student-dashboard/my-enrollments', label: 'Danh sách ghi danh' },
        ],
      },
      { to: '/student-dashboard/activities', label: 'Lịch sử hoạt động', icon: 'pi pi-history' },
    ];
  }
  return [];
});
</script>

<style scoped>
.dashboard-menu {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem 0;
}
.menu-item {
  padding: 0.75rem 1.25rem;
  color: #fff;
  text-decoration: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.2s ease;
}
.menu-item i {
  color: #ffffff;
  font-size: 1.1rem;
}
.menu-item:hover,
.menu-item:focus {
  background: #34495e;
  transform: translateX(4px);
}
.menu-item.router-link-exact-active {
  background: #3b82f6;
  color: #fff;
  font-weight: 600;
}
.menu-group .submenu {
  margin-left: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.menu-item.parent {
  font-weight: bold;
  cursor: default;
  background: none;
  color: #fff;
  padding-left: 1.25rem;
}
.submenu-item {
  font-size: 0.95rem;
  background: none;
  color: #fff;
  padding-left: 0.5rem;
}
</style>