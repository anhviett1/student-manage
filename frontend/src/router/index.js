import { createRouter, createWebHistory } from 'vue-router'
import { usePermissions } from '@/composables/usePermissions'
import { useAppEvents } from '@/composables/useAppEvents'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'Welcome',
    component: () => import('../components/Welcome.vue'),
    meta: { requiresAuth: false, title: 'Chào mừng đến với Hệ thống Quản lý' },
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/auth/LoginView.vue'),
    meta: { requiresAuth: false, title: 'Đăng nhập' },
  },
  {
    path: '/change-password',
    name: 'ChangePassword',
    component: () => import('../views/auth/ChangePasswordView.vue'),
    meta: { requiresAuth: false, title: 'Đổi mật khẩu' },
  },
  // Admin Dashboard
  {
    path: '/admin',
    component: () => import('../views/dashboard/AdminDashboardView.vue'),
    meta: { requiresAuth: true, title: 'Bảng điều khiển quản trị viên' },
    children: [
      { path: '', name: 'AdminProfile', component: () => import('../views/profile/ProfileView.vue') },
      { path: 'student', name: 'StudentManagement', component: () => import('../views/student/StudentManagement.vue') },
      { path: 'student/view', name: 'StudentView', component: () => import('../views/student/StudentView.vue') },
      { path: 'teacher', name: 'TeacherManagement', component: () => import('../views/teacher/TeacherManagement.vue') },
      { path: 'teacher/view', name: 'TeacherView', component: () => import('../views/teacher/TeacherView.vue') },
      { path: 'class', name: 'ClassManagement', component: () => import('../views/class/ClassManagement.vue') },
      { path: 'class/view', name: 'ClassView', component: () => import('../views/class/ClassView.vue') },
      { path: 'subject', name: 'SubjectManagement', component: () => import('../views/subject/SubjectManagement.vue') },
      { path: 'subject/view', name: 'SubjectView', component: () => import('../views/subject/SubjectView.vue') },
      { path: 'enrollment', name: 'EnrollmentManagement', component: () => import('../views/enrollment/EnrollmentManagement.vue') },
      { path: 'enrollment/view', name: 'EnrollmentView', component: () => import('../views/enrollment/EnrollmentView.vue') },
      { path: 'semester', name: 'SemesterManagement', component: () => import('../views/semester/ActiveSemesters.vue') },
      { path: 'score', name: 'ScoreManagement', component: () => import('../views/score/ScoreManagement.vue') },
      { path: 'schedule', name: 'ScheduleManagement', component: () => import('../views/schedule/ScheduleManagement.vue') },
      { path: 'admin/department', name: 'DepartmentManagement', component: () => import('../views/department/DepartmentView.vue') },
      { path: 'activity', name: 'ActivityView', component: () => import('../views/misc/ActivityView.vue') },
    ],
  },
  // Teacher Dashboard
  {
    path: '/teacher',
    component: () => import('../views/dashboard/TeacherDashboardView.vue'),
    meta: { requiresAuth: true, title: 'Bảng điều khiển giảng viên' },
    children: [
      { path: '', name: 'TeacherProfile', component: () => import('../views/profile/ProfileView.vue') },
      { path: 'class', name: 'TeacherClassManagement', component: () => import('../views/class/ClassManagement.vue') },
      { path: 'class/view', name: 'TeacherClassView', component: () => import('../views/class/ClassView.vue') },
      { path: 'subject', name: 'TeacherSubjectManagement', component: () => import('../views/subject/SubjectManagement.vue') },
      { path: 'subject/view', name: 'TeacherSubjectView', component: () => import('../views/subject/SubjectView.vue') },
      { path: 'score', name: 'TeacherScoreManagement', component: () => import('../views/score/ScoreManagement.vue') },
      { path: 'schedule', name: 'TeacherScheduleManagement', component: () => import('../views/schedule/ScheduleManagement.vue') },
      { path: 'activity', name: 'TeacherActivityView', component: () => import('../views/misc/ActivityView.vue') },
    ],
  },
  // Student Dashboard
  {
    path: '/student',
    component: () => import('../views/dashboard/StudentDashboardView.vue'),
    meta: { requiresAuth: true, title: 'Bảng điều khiển sinh viên' },
    children: [
      { path: '', name: 'StudentProfile', component: () => import('../views/profile/ProfileView.vue') },
      { path: 'score', name: 'MyScores', component: () => import('../views/score/MyScores.vue') },
      { path: 'schedule', name: 'MySchedules', component: () => import('../views/schedule/MySchedules.vue') },
      { path: 'enrollment', name: 'MyEnrollments', component: () => import('../views/enrollment/MyEnrollments.vue') },
      { path: 'activity', name: 'StudentActivityView', component: () => import('../views/misc/ActivityView.vue') },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/misc/NotFoundView.vue'),
    meta: { requiresAuth: false, title: 'Không tìm thấy trang' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const { isAuthenticated, isAdmin, isTeacher, isStudent, hasPermission } = usePermissions()
  const { isLoading, notify } = useAppEvents()
  const authStore = useAuthStore()

  isLoading.value = true

  // Redirect authenticated users from Welcome/Login to their dashboard
  if ((to.name === 'Welcome' || to.name === 'Login') && isAuthenticated.value) {
    isLoading.value = false
    if (isAdmin.value) return next('/admin-dashboard')
    if (isTeacher.value) return next('/teacher-dashboard')
    return next('/student-dashboard')
  }

  // Redirect unauthenticated users to Welcome for protected routes
  if (to.meta.requiresAuth && !isAuthenticated.value) {
    isLoading.value = false
    notify({ severity: 'error', summary: 'Lỗi', detail: 'Vui lòng đăng nhập.' })
    return next('/')
  }

  // Check role-based permissions
  const requiredPermission = to.meta.permission
  if (requiredPermission && isAuthenticated.value) {
    const method = to.meta.method || 'GET'
    if (!hasPermission(requiredPermission, null, method)) {
      isLoading.value = false
      notify({ severity: 'error', summary: 'Lỗi', detail: 'Không có quyền truy cập.' })
      return next('/')
    }
  }

  // Set document title dynamically
  document.title = to.meta.title.replace('{$username}', authStore.user?.username || 'Hệ thống Quản lý Học tập')
  isLoading.value = false
  next()
})

router.afterEach(() => {
  const { isLoading } = useAppEvents()
  isLoading.value = false
})

export default router