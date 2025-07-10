import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const routes = [
  {
    path: '/',
    redirect: (to) => {
      const authStore = useAuthStore();
      const role = authStore.user?.role || 'student'; // Mặc định là student nếu role không xác định
      if (role === 'admin') return '/admin-dashboard';
      if (role === 'teacher') return '/teacher-dashboard';
      return '/student-dashboard';
    },
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue'),
    meta: { requiresAuth: false, title: 'Đăng nhập' },
  },
  {
    path: '/admin-dashboard',
    name: 'AdminDashboard',
    component: () => import('../views/AdminDashboardView.vue'),
    meta: { requiresAuth: true, roles: ['admin'], title: 'Bảng điều khiển quản trị viên' },
  },
  {
    path: '/teacher-dashboard',
    name: 'TeacherDashboard',
    component: () => import('../views/TeacherDashboardView.vue'),
    meta: { requiresAuth: true, roles: ['teacher', 'admin'], title: 'Bảng điều khiển giảng viên' },
  },
  {
    path: '/student-dashboard',
    name: 'StudentDashboard',
    component: () => import('../views/StudentDashboardView.vue'),
    meta: { requiresAuth: true, roles: ['student', 'admin'], title: 'Bảng điều khiển sinh viên' },
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('../views/ProfileView.vue'),
    meta: { requiresAuth: true, roles: ['student', 'teacher', 'admin'], title: 'Hồ sơ cá nhân' },
  },
  {
    path: '/students',
    name: 'students',
    component: () => import('../views/StudentView.vue'),
    meta: { requiresAuth: true, roles: ['teacher', 'admin'], title: 'Quản lý Sinh viên' },
  },
  {
    path: '/classes',
    name: 'classes',
    component: () => import('../views/ClassView.vue'),
    meta: { requiresAuth: true, roles: ['teacher', 'admin'], title: 'Quản lý Lớp học' },
  },
  {
    path: '/subjects',
    name: 'subjects',
    component: () => import('../views/SubjectView.vue'),
    meta: { requiresAuth: true, roles: ['teacher', 'admin'], title: 'Quản lý Môn học' },
  },
  {
    path: '/scores',
    name: 'scores',
    component: () => import('../views/ScoreView.vue'),
    meta: { requiresAuth: true, roles: ['student', 'teacher', 'admin'], title: 'Quản lý Điểm số' },
  },
  {
    path: '/schedules',
    name: 'schedules',
    component: () => import('../views/ScheduleView.vue'),
    meta: { requiresAuth: true, roles: ['student', 'teacher', 'admin'], title: 'Thời khóa biểu' },
  },
  {
    path: '/activities',
    name: 'activities',
    component: () => import('../views/ActivityView.vue'),
    meta: { requiresAuth: true, roles: ['teacher', 'admin'], title: 'Lịch sử hoạt động' },
  },
  {
    path: '/enrollments',
    name: 'enrollments',
    component: () => import('../views/EnrollmentView.vue'),
    meta: { requiresAuth: true, roles: ['admin'], title: 'Quản lý Ghi danh' },
  },
  {
    path: '/semesters',
    name: 'semesters',
    component: () => import('../views/SemesterView.vue'),
    meta: { requiresAuth: true, roles: ['admin'], title: 'Quản lý Học kỳ' },
  },
  {
    path: '/departments',
    name: 'departments',
    component: () => import('../views/DepartmentView.vue'),
    meta: { requiresAuth: true, roles: ['admin'], title: 'Quản lý Khoa' },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFoundView.vue'),
    meta: { requiresAuth: false, title: 'Không tìm thấy trang' },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation Guard để kiểm tra quyền truy cập
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const isAuthenticated = authStore.isAuthenticated;
  const userRole = authStore.user?.role || null;

  // Ngăn truy cập /login nếu đã đăng nhập
  if (to.name === 'Login' && isAuthenticated) {
    const role = userRole || 'student';
    return next(
      role === 'admin' ? '/admin-dashboard' :
      role === 'teacher' ? '/teacher-dashboard' : '/student-dashboard'
    );
  }

  // Kiểm tra yêu cầu đăng nhập
  if (to.meta.requiresAuth && !isAuthenticated) {
    return next('/login');
  }

  // Kiểm tra vai trò
  if (to.meta.roles && userRole && !to.meta.roles.includes(userRole)) {
    return next('/'); // Redirect về trang chính nếu không có quyền
  }

  // Cập nhật tiêu đề trang
  document.title = to.meta.title || 'Hệ thống Quản lý Học tập';
  next();
});

export default router;