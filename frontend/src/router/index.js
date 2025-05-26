import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/students',
      name: 'students',
      component: () => import('../views/StudentListView.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/teachers',
      name: 'teachers',
      component: () => import('../views/TeacherListView.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/classes',
      name: 'classes',
      component: () => import('../views/ClassListView.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/subjects',
      name: 'subjects',
      component: () => import('../views/SubjectListView.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/enrollments',
      name: 'enrollments',
      component: () => import('../views/EnrollmentListView.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/semesters',
      name: 'semesters',
      component: () => import('../views/SemesterListView.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/scores',
      name: 'scores',
      component: () => import('../views/ScoreListView.vue'),
      meta: { requiresAuth: true, role: 'teacher' }
    },
    {
      path: '/my-scores',
      name: 'my-scores',
      component: () => import('../views/MyScoresView.vue'),
      meta: { requiresAuth: true, role: 'student' }
    },
    {
      path: '/change-password',
      name: 'change-password',
      component: () => import('../views/ChangePasswordView.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = authStore.isAuthenticated()
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.meta.role && !authStore.canAccess(to.meta.role)) {
    // Redirect to home if user doesn't have required role
    next('/')
  } else {
    next()
  }
})

export default router 