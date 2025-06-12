import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { endpoints } from '@/services/api'

// Tạo router với lịch sử trình duyệt
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL || '/'),
  routes: [
    // Trang chủ
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      meta: { requiresAuth: true, title: 'Trang Chủ' },
    },
    // Đăng nhập
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { title: 'Đăng Nhập' },
    },
    // Hồ sơ người dùng
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      meta: { requiresAuth: true, title: 'Hồ Sơ' },
    },
    // Đổi mật khẩu
    {
      path: '/change-password',
      name: 'change-password',
      component: () => import('../views/ChangePasswordView.vue'),
      meta: { requiresAuth: true, title: 'Đổi Mật Khẩu' },
    },
    // Django Admin (external redirect)
    {
      path: '/admin',
      name: 'admin',
      beforeEnter: (to, from, next) => {
        const authStore = useAuthStore()
        if (!authStore.isAuthenticated || !authStore.isAdmin) {
          next('/')
        } else {
          window.location.href = endpoints.djangoAdmin // /admin/
        }
      },
      meta: { requiresAuth: true, role: 'admin', title: 'Django Admin' },
    },
    // Quản lý sinh viên
    {
      path: '/students',
      name: 'students',
      component: () => import('../views/StudentView.vue'),
      meta: { requiresAuth: true, role: 'admin', title: 'Quản Lý Sinh Viên' },
    },
    // Quản lý giảng viên
    {
      path: '/teachers',
      name: 'teachers',
      component: () => import('../views/TeacherView.vue'),
      meta: { requiresAuth: true, role: 'admin', title: 'Quản Lý Giảng Viên' },
    },
    // Quản lý lớp học
    {
      path: '/classes',
      name: 'classes',
      component: () => import('../views/ClassView.vue'),
      meta: { requiresAuth: true, role: 'admin', title: 'Quản Lý Lớp Học' },
    },
    // Quản lý môn học
    {
      path: '/subjects',
      name: 'subjects',
      component: () => import('../views/SubjectView.vue'),
      meta: { requiresAuth: true, role: 'admin', title: 'Quản Lý Môn Học' },
    },
    // Quản lý ghi danh
    {
      path: '/enrollments',
      name: 'enrollments',
      component: () => import('../views/EnrollmentView.vue'),
      meta: { requiresAuth: true, role: 'admin', title: 'Quản Lý Ghi Danh' },
    },
    // Quản lý học kỳ
    {
      path: '/semesters',
      name: 'semesters',
      component: () => import('../views/SemesterView.vue'),
      meta: { requiresAuth: true, role: 'admin', title: 'Quản Lý Học Kỳ' },
    },
    // Quản lý điểm số
    {
      path: '/scores',
      name: 'scores',
      component: () => import('../views/ScoreView.vue'),
      meta: { requiresAuth: true, role: 'teacher', title: 'Quản Lý Điểm Số' },
    },
   
    // Redirect các route không tồn tại về trang chủ
    {
      path: '/:pathMatch(.*)*',
      redirect: '/',
    },
  ],
})

// Navigation guard toàn cục
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Đảm bảo trạng thái xác thực đã được tải
  if (!authStore.user && authStore.isAuthenticated) {
    try {
      await authStore.fetchCurrentUser()
    } catch (error) {
      authStore.logout()
    }
  }

  const isAuthenticated = authStore.isAuthenticated
  const requiredRole = to.meta.role

  // Thêm logs để debug
  console.log('Navigating to:', to.path);
  console.log('Requires Auth:', to.meta.requiresAuth);
  console.log('Is Authenticated:', isAuthenticated);
  console.log('Required Role:', requiredRole);
  if (requiredRole) {
    console.log('User Has Required Role (authStore.hasRole):', authStore.hasRole(requiredRole));
  }

  // Kiểm tra quyền truy cập
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (requiredRole && !authStore.hasRole(requiredRole)) {
    next('/')
  } else {
    // Cập nhật tiêu đề trang
    document.title = to.meta.title ? `${to.meta.title} - Hệ Thống Quản Lý Sinh Viên` : 'Hệ Thống Quản Lý Sinh Viên'
    next()
  }
})

export default router