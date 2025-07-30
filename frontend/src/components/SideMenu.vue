<template>
  <nav class="api-menu">
    <div v-for="item in menuItems" :key="item.label">
      <router-link
        v-if="!item.children"
        :to="item.to"
        class="menu-item"
        :aria-label="item.label"
      >
        <i :class="item.icon" class="mr-2"></i>
        {{ item.label }}
      </router-link>
      <div v-else class="menu-group" :class="{ 'active-group': isParentActive(item) }">
        <div class="menu-item parent" @click="toggleSubmenu(item.label)">
          <i :class="item.icon" class="mr-2"></i>
          {{ item.label }}
        </div>
        <div class="submenu" v-show="activeSubmenu === item.label">
          <router-link
            v-for="child in item.children"
            :key="child.to"
            :to="child.to"
            class="menu-item submenu-item"
            :aria-label="child.label"
          >
            {{ child.label }}
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed, ref } from 'vue';
import { useRoute } from 'vue-router';
import { usePermissions } from '@/composables/usePermissions';

const route = useRoute();
const { userRole } = usePermissions();
const activeSubmenu = ref(null);

const toggleSubmenu = (label) => {
  activeSubmenu.value = activeSubmenu.value === label ? null : label;
};

const isParentActive = (item) => {
  return item.children?.some(child => route.path.startsWith(child.to));
};

const menuItems = computed(() => {
  if (!userRole.value) return [];
  if (userRole.value === 'admin') {
    return [
      {
        to: '/admin/users',
        label: 'Quản lý Người dùng',
        icon: 'pi pi-users',
        children: [
          { to: '/admin/users', label: 'Danh sách người dùng' },
          { to: '/admin/profile', label: 'Hồ sơ cá nhân' },
          { to: '/admin/change-password', label: 'Đổi mật khẩu' },
          { to: '/admin/upload-avatar', label: 'Tải lên ảnh đại diện' },
        ],
      },
      {
        to: '/admin/students',
        label: 'Quản lý Sinh viên',
        icon: 'pi pi-user',
        children: [
          { to: '/admin/students', label: 'Danh sách sinh viên' },
          { to: '/admin/students/export', label: 'Xuất danh sách' },
          { to: '/admin/student/me', label: 'Hồ sơ sinh viên' },
        ],
      },
      {
        to: '/admin/teachers',
        label: 'Quản lý Giảng viên',
        icon: 'pi pi-user-plus',
        children: [
          { to: '/admin/teachers', label: 'Danh sách giảng viên' },
          { to: '/admin/teachers/export', label: 'Xuất danh sách' },
          { to: '/admin/teacher/me', label: 'Hồ sơ giảng viên' },
        ],
      },
      {
        to: '/admin/classes',
        label: 'Quản lý Lớp học',
        icon: 'pi pi-book',
        children: [
          { to: '/admin/classes', label: 'Danh sách lớp học' },
          { to: '/admin/classes/export', label: 'Xuất danh sách' },
        ],
      },
      {
        to: '/admin/subjects',
        label: 'Quản lý Môn học',
        icon: 'pi pi-file',
        children: [
          { to: '/admin/subjects', label: 'Danh sách môn học' },
          { to: '/admin/subjects/export', label: 'Xuất danh sách' },
        ],
      },
      {
        to: '/admin/enrollments',
        label: 'Quản lý Ghi danh',
        icon: 'pi pi-check-square',
        children: [
          { to: '/admin/enrollments', label: 'Danh sách ghi danh' },
          { to: '/admin/enrollments/export', label: 'Xuất danh sách' },
        ],
      },
      {
        to: '/admin/semesters',
        label: 'Quản lý Học kỳ',
        icon: 'pi pi-calendar',
        children: [
          { to: '/admin/semesters', label: 'Danh sách học kỳ' },
          { to: '/admin/semesters/export', label: 'Xuất danh sách' },
        ],
      },
      {
        to: '/admin/scores',
        label: 'Quản lý Điểm số',
        icon: 'pi pi-chart-bar',
        children: [
          { to: '/admin/scores', label: 'Danh sách điểm số' },
          { to: '/admin/scores/export', label: 'Xuất danh sách' },
        ],
      },
      {
        to: '/admin/departments',
        label: 'Quản lý Khoa',
        icon: 'pi pi-building',
        children: [
          { to: '/admin/departments', label: 'Danh sách khoa' },
          { to: '/admin/departments/export', label: 'Xuất danh sách' },
        ],
      },
      {
        to: '/admin/schedules',
        label: 'Quản lý Thời khóa biểu',
        icon: 'pi pi-clock',
        children: [
          { to: '/admin/schedules', label: 'Danh sách thời khóa biểu' },
          { to: '/admin/schedules/export', label: 'Xuất danh sách' },
        ],
      },
      {
        to: '/admin/activities',
        label: 'Quản lý Hoạt động',
        icon: 'pi pi-history',
        children: [
          { to: '/admin/activities', label: 'Danh sách hoạt động' },
          { to: '/admin/activities/export', label: 'Xuất danh sách' },
        ],
      },
    ];
  }
  if (userRole.value === 'teacher') {
    return [
      { to: '/teacher/profile', label: 'Hồ sơ cá nhân', icon: 'pi pi-user' },
      { to: '/teacher/change-password', label: 'Đổi mật khẩu', icon: 'pi pi-lock' },
      { to: '/teacher/upload-avatar', label: 'Tải lên ảnh đại diện', icon: 'pi pi-image' },
      { to: '/teacher/me', label: 'Hồ sơ giảng viên', icon: 'pi pi-user-plus' },
      {
        to: '/teacher/classes',
        label: 'Quản lý Lớp học',
        icon: 'pi pi-book',
        children: [
          { to: '/teacher/classes', label: 'Danh sách lớp học' },
          { to: '/teacher/classes/export', label: 'Xuất danh sách' },
        ],
      },
      {
        to: '/teacher/subjects',
        label: 'Quản lý Môn học',
        icon: 'pi pi-file',
        children: [
          { to: '/teacher/subjects', label: 'Danh sách môn học' },
          { to: '/teacher/subjects/export', label: 'Xuất danh sách' },
        ],
      },
      {
        to: '/teacher/scores',
        label: 'Quản lý Điểm số',
        icon: 'pi pi-chart-bar',
        children: [
          { to: '/teacher/scores', label: 'Danh sách điểm số' },
          { to: '/teacher/scores/export', label: 'Xuất danh sách' },
        ],
      },
      {
        to: '/teacher/schedules',
        label: 'Quản lý Thời khóa biểu',
        icon: 'pi pi-clock',
        children: [
          { to: '/teacher/schedules', label: 'Danh sách thời khóa biểu' },
          { to: '/teacher/schedules/export', label: 'Xuất danh sách' },
        ],
      },
      {
        to: '/teacher/activities',
        label: 'Quản lý Hoạt động',
        icon: 'pi pi-history',
        children: [
          { to: '/teacher/activities', label: 'Danh sách hoạt động' },
          { to: '/teacher/activities/export', label: 'Xuất danh sách' },
        ],
      },
    ];
  }
  if (userRole.value === 'student') {
    return [
      { to: '/student/profile', label: 'Hồ sơ cá nhân', icon: 'pi pi-user' },
      { to: '/student/change-password', label: 'Đổi mật khẩu', icon: 'pi pi-lock' },
      { to: '/student/upload-avatar', label: 'Tải lên ảnh đại diện', icon: 'pi pi-image' },
      { to: '/student/me', label: 'Hồ sơ sinh viên', icon: 'pi pi-user' },
      {
        to: '/student/scores',
        label: 'Điểm số',
        icon: 'pi pi-chart-bar',
        children: [
          { to: '/student/scores', label: 'Danh sách điểm số' },
          { to: '/student/scores/export', label: 'Xuất danh sách' },
        ],
      },
      {
        to: '/student/schedules',
        label: 'Thời khóa biểu',
        icon: 'pi pi-clock',
        children: [
          { to: '/student/schedules', label: 'Danh sách thời khóa biểu' },
          { to: '/student/schedules/export', label: 'Xuất danh sách' },
        ],
      },
      {
        to: '/student/enrollments',
        label: 'Ghi danh',
        icon: 'pi pi-check-square',
        children: [
          { to: '/student/enrollments', label: 'Danh sách ghi danh' },
          { to: '/student/enrollments/export', label: 'Xuất danh sách' },
        ],
      },
      {
        to: '/student/activities',
        label: 'Hoạt động',
        icon: 'pi pi-history',
        children: [
          { to: '/student/activities', label: 'Danh sách hoạt động' },
          { to: '/student/activities/export', label: 'Xuất danh sách' },
        ],
      },
    ];
  }
  return [];
});
</script>

<style scoped>
.api-menu {
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
  cursor: pointer;
  background: none;
  color: #fff;
  padding-left: 1.25rem;
}
.active-group .menu-item.parent {
  background: #3b82f6;
  color: #fff;
  font-weight: 600;
}
.submenu-item {
  font-size: 0.95rem;
  background: none;
  color: #fff;
  padding-left: 0.5rem;
}
</style>