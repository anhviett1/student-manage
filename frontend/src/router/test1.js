import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import BaseLayout from '@/components/BaseLayout.vue'

// Route configurations
const routes = {
  // Public routes
  public: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { title: 'Đăng Nhập' }
    }
  ],

  // Protected routes
  protected: [
    {
      path: '/',
      component: BaseLayout,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('../views/HomeView.vue'),
          meta: { title: 'Trang Chủ' }
        },
        {
          path: 'profile',
          name: 'profile',
          component: () => import('../views/ProfileView.vue'),
          meta: { requiresAuth: true, title: 'Hồ Sơ' }
        },
        {
          path: 'change-password',
          name: 'change-password',
          component: () => import('../views/ChangePasswordView.vue'),
          meta: { requiresAuth: true, title: 'Đổi Mật Khẩu' }
        }
      ]
    }
  ],

  // Admin routes
  admin: [
    {
      path: '/',
      component: BaseLayout,
      meta: { requiresAuth: true, role: 'admin' },
      children: [
        {
          path: 'students',
          name: 'students',
          component: () => import('../views/StudentView.vue'),
          meta: { title: 'Quản Lý Sinh Viên' }
        },
        {
          path: 'teachers',
          name: 'teachers',
          component: () => import('../views/TeacherView.vue'),
          meta: { title: 'Quản Lý Giảng Viên' }
        },
        {
          path: 'classes',
          name: 'classes',
          component: () => import('../views/ClassView.vue'),
          meta: { title: 'Quản Lý Lớp Học' }
        },
        {
          path: 'subjects',
          name: 'subjects',
          component: () => import('../views/SubjectView.vue'),
          meta: { title: 'Quản Lý Môn Học' }
        },
        {
          path: 'enrollments',
          name: 'enrollments',
          component: () => import('../views/EnrollmentView.vue'),
          meta: { title: 'Quản Lý Ghi Danh' }
        },
        {
          path: 'semesters',
          name: 'semesters',
          component: () => import('../views/SemesterView.vue'),
          meta: { title: 'Quản Lý Học Kỳ' }
        }
      ]
    },
    {
      path: '/admin',
      name: 'admin',
      beforeEnter: (to, from, next) => {
        const authStore = useAuthStore()
        if (!authStore.isAuthenticated || !authStore.isAdmin) {
          next('/')
        } else {
          window.location.href = '/admin/'
        }
      },
      meta: { requiresAuth: true, role: 'admin', title: 'Django Admin' }
    }
  ],

  // Teacher routes
  teacher: [
    {
      path: '/',
      component: BaseLayout,
      meta: { requiresAuth: true, role: 'teacher' },
      children: [
        {
          path: 'scores',
          name: 'scores',
          component: () => import('../views/ScoreView.vue'),
          meta: { title: 'Quản Lý Điểm Số' }
        }
      ]
    }
  ],

  // Fallback route
  fallback: [
    {
      path: '/:pathMatch(.*)*',
      redirect: '/'
    }
  ]
}

// Create router instance
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL || '/'),
  routes: [
    ...routes.public,
    ...routes.protected,
    ...routes.admin,
    ...routes.teacher,
    ...routes.fallback
  ]
})

// Navigation guard
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Load user data if authenticated but not loaded
  if (!authStore.user && authStore.isAuthenticated) {
    try {
      await authStore.fetchCurrentUser()
    } catch (error) {
      authStore.logout()
      return next({ name: 'login', query: { redirect: to.fullPath } })
    }
  }

  const isAuthenticated = authStore.isAuthenticated
  const requiredRole = to.meta.role

  // Debug logs
  if (import.meta.env.DEV) {
    console.log('Navigation:', {
      path: to.path,
      requiresAuth: to.meta.requiresAuth,
      isAuthenticated,
      requiredRole,
      hasRole: requiredRole ? authStore.hasRole(requiredRole) : null
    })
  }

  // Check authentication
  if (to.meta.requiresAuth && !isAuthenticated) {
    return next({ name: 'login', query: { redirect: to.fullPath } })
  }

  // Check role
  if (requiredRole && !authStore.hasRole(requiredRole)) {
    return next('/')
  }

  // Update page title
  document.title = to.meta.title 
    ? `${to.meta.title} - Hệ Thống Quản Lý Sinh Viên` 
    : 'Hệ Thống Quản Lý Sinh Viên'

  next()
})

export default router