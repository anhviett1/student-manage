import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import BaseLayout from '@/components/BaseLayout.vue'
import HomeView from '../views/HomeView.vue'

// Định nghĩa các tuyến đường
const routes = [
  // --- Tuyến đường không yêu cầu xác thực ---
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue'),
    meta: { title: 'Đăng Nhập' },
  },

  // --- Tuyến đường yêu cầu xác thực, sử dụng BaseLayout ---
  {
    path: '/',
    component: BaseLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'home',
        component: HomeView,
        meta: { title: 'Trang Chủ' },
      },
      {
        path: 'users',
        name: 'users',
        component: () => import('../views/UsersView.vue'),
        meta: { title: 'Quản Lý Người Dùng', requiresAdmin: true },
      },
      {
        path: 'profile',
        name: 'profile',
        component: () => import('../views/ProfileView.vue'),
        meta: { title: 'Hồ Sơ Của Tôi' },
      },
      {
        path: 'change-password',
        name: 'change-password',
        component: () => import('../views/ChangePasswordView.vue'),
        meta: { title: 'Đổi Mật Khẩu' },
      },
      {
        path: 'students',
        name: 'students',
        component: () => import('../views/StudentView.vue'),
        meta: { title: 'Quản Lý Sinh Viên' },
      },
      {
        path: 'teachers',
        name: 'teachers',
        component: () => import('../views/TeacherView.vue'),
        meta: { title: 'Quản Lý Giảng Viên' },
      },
      {
        path: 'classes',
        name: 'classes',
        component: () => import('../views/ClassView.vue'),
        meta: { title: 'Quản Lý Lớp Học' },
      },
      {
        path: 'subjects',
        name: 'subjects',
        component: () => import('../views/SubjectView.vue'),
        meta: { title: 'Quản Lý Môn Học' },
      },
      {
        path: 'enrollments',
        name: 'enrollments',
        component: () => import('../views/EnrollmentView.vue'),
        meta: { title: 'Quản Lý Ghi Danh' },
      },
      {
        path: 'semesters',
        name: 'semesters',
        component: () => import('../views/SemesterView.vue'),
        meta: { title: 'Quản Lý Học Kỳ' },
      },
      {
        path: 'scores',
        name: 'scores',
        component: () => import('../views/ScoreView.vue'),
        meta: { title: 'Quản Lý Điểm Số' },
      },
      {
        path: 'schedules',
        name: 'schedules',
        component: () => import('../views/ScheduleView.vue'),
        meta: { title: 'Thời Khóa Biểu' },
      },
      {
        path: 'departments',
        name: 'departments',
        component: () => import('../views/DepartmentView.vue'),
        meta: { title: 'Khoa' },
      },
      // Chuyển hướng đến trang admin của Django
      {
        path: 'admin',
        name: 'admin',
        beforeEnter: () => {
          // Luôn mở trong tab mới để không làm gián đoạn SPA
          window.open('http://127.0.0.1:8000/admin/', '_blank')
          // Quay lại trang trước đó hoặc trang chủ
          return false
        },
        meta: { title: 'Django Admin', requiresAdmin: true },
      },
    ],
  },

  // --- Xử lý các tuyến đường không tồn tại ---
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL || '/'),
  routes,
})

// --- Navigation Guard Toàn Cục ---
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Tải thông tin người dùng nếu đã đăng nhập nhưng chưa có trong store
  if (authStore.isAuthenticated && !authStore.user) {
    try {
      await authStore.fetchCurrentUser()
    } catch {
      await authStore.logout() // Đăng xuất nếu token hỏng
    }
  }

  const isAuthenticated = authStore.isAuthenticated
  const isAdmin = authStore.isAdmin

  if (to.meta.requiresAuth) {
    if (!isAuthenticated) {
      // Nếu yêu cầu đăng nhập nhưng chưa đăng nhập -> chuyển về /login
      return next({ name: 'login', query: { redirect: to.fullPath } })
    }

    if (to.meta.requiresAdmin && !isAdmin) {
      // Nếu yêu cầu quyền admin nhưng không phải admin -> chuyển về /
      return next({ name: 'home' })
    }
  } else if (to.name === 'login' && isAuthenticated) {
    // Nếu đã đăng nhập mà vào /login -> chuyển về /
    return next({ name: 'home' })
  }

  // Cập nhật tiêu đề trang
  document.title = to.meta.title
    ? `${to.meta.title} - Quản Lý Sinh Viên`
    : 'Hệ Thống Quản Lý Sinh Viên'
  next()
})

export default router