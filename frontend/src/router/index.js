import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import BaseLayout from '@/components/BaseLayout.vue'
import HomeView from '../views/HomeView.vue'

// Định nghĩa các tuyến đường
const routes = [
  // --- Tuyến đường không yêu cầu xác thực ---
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { title: 'Trang Chủ' },
  },
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
        path: 'profile',
        name: 'profile',
        component: () => import('../views/ProfileView.vue'),
        meta: { title: 'Hồ Sơ Của Tôi' },
        children: [
          {
            path: 'change-password',
            name: 'profile-change-password',
            component: () => import('../views/ChangePasswordView.vue'),
            meta: { title: 'Đổi Mật Khẩu' },
          }
        ]
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
      {
        path: 'activities',
        name: 'activities',
        component: () => import('../views/ActivityView.vue'),
        meta: { title: 'Trạng thái' },
      },
      // Chuyển hướng đến trang admin của Django
      {
        path: 'admin',
        name: 'admin',
        beforeEnter: () => {
          window.open('http://127.0.0.1:8000/admin/', '_blank')
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
  const isAuthenticated = authStore.isAuthenticated
  const isAdmin = authStore.isAdmin

  // 1) Truy cập '/' → điều hướng theo trạng thái đăng nhập
  if (to.path === '/') {
    if (isAuthenticated && to.name !== 'profile') {
      return next({ name: 'profile' })
    }
    if (!isAuthenticated && to.name !== 'home') {
      return next({ name: 'home' })
    }
    return next() // tránh vòng lặp khi đã ở đúng route
  }

  // 2) Yêu cầu đăng nhập nhưng chưa login → chuyển về login
  if (to.meta.requiresAuth && !isAuthenticated) {
    return next({ name: 'login', query: { redirect: to.fullPath } })
  }

  // 3) Yêu cầu admin nhưng không phải admin → home
  if (to.meta.requiresAdmin && !isAdmin) {
    return next({ name: 'home' })
  }

  // 4) Nếu đã login mà vào /login → chuyển về profile
  if (to.name === 'login' && isAuthenticated) {
    return next({ name: 'profile' })
  }

  // 5) Nếu đã login mà chưa có user (chưa fetch) → fetch user
  if (isAuthenticated && !authStore.user) {
    try {
      await authStore.fetchCurrentUser()
    } catch {
      await authStore.logout()
      return next({ name: 'login' })
    }
  }

  // 6) Cập nhật title trang
  document.title = to.meta.title
    ? `${to.meta.title} - Quản Lý Sinh Viên`
    : 'Hệ Thống Quản Lý Sinh Viên'

  next()
})

export default router
