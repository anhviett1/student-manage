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
    path: '/admin-dashboard',
    component: () => import('../views/dashboard/AdminDashboardView.vue'),
    meta: { requiresAuth: true, title: 'Bảng điều khiển quản trị viên' },
    children: [
      { path: '', name: 'AdminProfile', component: () => import('../views/profile/ProfileView.vue'), meta: { permission: 'hasProfilePermission' } },
      { path: 'students', name: 'StudentManagement', component: () => import('../views/student/StudentManagement.vue'), meta: { permission: 'hasStudentChangePermission' } },
      { path: 'student/:id', name: 'StudentProfile', component: () => import('../views/student/StudentProfile.vue'), meta: { permission: 'hasProfilePermission' } },
      { path: 'student-view', name: 'StudentView', component: () => import('../views/student/StudentView.vue'), meta: { permission: 'hasStudentChangePermission' } },
      { path: 'teachers', name: 'TeacherManagement', component: () => import('../views/teacher/TeacherManagement.vue'), meta: { permission: 'hasTeacherChangePermission' } },
      { path: 'teacher/:id', name: 'TeacherProfile', component: () => import('../views/teacher/TeacherProfile.vue'), meta: { permission: 'hasProfilePermission' } },
      { path: 'teacher-view', name: 'TeacherView', component: () => import('../views/teacher/TeacherView.vue'), meta: { permission: 'hasTeacherChangePermission' } },
      { path: 'classes', name: 'ClassManagement', component: () => import('../views/class/ClassManagement.vue'), meta: { permission: 'hasClassPermission' } },
      { path: 'class/:id', name: 'ClassInfo', component: () => import('../views/class/ClassInfo.vue'), meta: { permission: 'hasClassPermission' } },
      { path: 'class-view', name: 'ClassView', component: () => import('../views/class/ClassView.vue'), meta: { permission: 'hasClassPermission' } },
      { path: 'subjects', name: 'SubjectManagement', component: () => import('../views/subject/SubjectManagement.vue'), meta: { permission: 'hasSubjectPermission' } },
      { path: 'subject-view', name: 'SubjectView', component: () => import('../views/subject/SubjectView.vue'), meta: { permission: 'hasSubjectPermission' } },
      { path: 'scores', name: 'ScoreManagement', component: () => import('../views/score/ScoreManagement.vue'), meta: { permission: 'hasScorePermission' } },
      { path: 'score-view', name: 'ScoreView', component: () => import('../views/score/ScoreView.vue'), meta: { permission: 'hasScorePermission' } },
      { path: 'schedules', name: 'ScheduleManagement', component: () => import('../views/schedule/ScheduleManagement.vue'), meta: { permission: 'hasSchedulePermission' } },
      { path: 'schedule-view', name: 'ScheduleView', component: () => import('../views/schedule/ScheduleView.vue'), meta: { permission: 'hasSchedulePermission' } },
      { path: 'enrollments', name: 'EnrollmentManagement', component: () => import('../views/enrollment/EnrollmentManagement.vue'), meta: { permission: 'hasEnrollmentPermission' } },
      { path: 'enrollment-view', name: 'EnrollmentView', component: () => import('../views/enrollment/EnrollmentView.vue'), meta: { permission: 'hasEnrollmentPermission' } },
      { path: 'semesters', name: 'SemesterManagement', component: () => import('../views/semester/ActiveSemesters.vue'), meta: { permission: 'hasSemesterPermission' } },
      { path: 'finished-semesters', name: 'FinishedSemesters', component: () => import('../views/semester/FinishedSemesters.vue'), meta: { permission: 'hasSemesterPermission' } },
      { path: 'semester-view', name: 'SemesterView', component: () => import('../views/semester/SemesterView.vue'), meta: { permission: 'hasSemesterPermission' } },
      { path: 'departments', name: 'DepartmentManagement', component: () => import('../views/department/DepartmentView.vue'), meta: { permission: 'hasDepartmentPermission' } },
      { path: 'activities', name: 'ActivityView', component: () => import('../views/misc/ActivityView.vue'), meta: { permission: 'hasActivityPermission' } },
    ],
  },
  // Teacher Dashboard
  {
    path: '/teacher-dashboard',
    component: () => import('../views/dashboard/TeacherDashboardView.vue'),
    meta: { requiresAuth: true, title: 'Bảng điều khiển giảng viên' },
    children: [
      { path: '', name: 'TeacherProfile', component: () => import('../views/profile/ProfileView.vue') },
      { path: 'classes', name: 'TeacherClassManagement', component: () => import('../views/class/ClassManagement.vue') },
      { path: 'class/:id', name: 'TeacherClassInfo', component: () => import('../views/class/ClassInfo.vue') },
      { path: 'class-view', name: 'TeacherClassView', component: () => import('../views/class/ClassView.vue') },
      { path: 'subjects', name: 'TeacherSubjectManagement', component: () => import('../views/subject/SubjectManagement.vue') },
      { path: 'subject-view', name: 'TeacherSubjectView', component: () => import('../views/subject/SubjectView.vue') },
      { path: 'scores', name: 'TeacherScoreManagement', component: () => import('../views/score/ScoreManagement.vue') },
      { path: 'score-view', name: 'TeacherScoreView', component: () => import('../views/score/ScoreView.vue') },
      { path: 'schedules', name: 'TeacherScheduleManagement', component: () => import('../views/schedule/ScheduleManagement.vue') },
      { path: 'schedule-view', name: 'TeacherScheduleView', component: () => import('../views/schedule/ScheduleView.vue')},
      { path: 'activities', name: 'TeacherActivityView', component: () => import('../views/misc/ActivityView.vue') },
    ],
  },
  // Student Dashboard
  {
    path: '/student-dashboard',
    component: () => import('../views/dashboard/StudentDashboardView.vue'),
    meta: { requiresAuth: true, title: 'Bảng điều khiển sinh viên' },
    children: [
      { path: '', name: 'StudentProfile', component: () => import('../views/profile/ProfileView.vue') },
      { path: 'my-scores', name: 'MyScores', component: () => import('../views/score/MyScores.vue') },
      { path: 'my-schedules', name: 'MySchedules', component: () => import('../views/schedule/MySchedules.vue') },
      { path: 'my-enrollments', name: 'MyEnrollments', component: () => import('../views/enrollment/MyEnrollments.vue') },
      { path: 'activities', name: 'StudentActivityView', component: () => import('../views/misc/ActivityView.vue') },
    ],
  },
  // Not Found
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