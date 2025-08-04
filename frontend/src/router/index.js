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
    component: () => import('../views/profile/ChangePassword.vue'),
    meta: { requiresAuth: false, title: 'Đổi mật khẩu' },
  },
  {
    path: '/admin',
    component: () => import('../views/dashboard/AdminDashboardView.vue'),
    meta: { requiresAuth: true, title: 'Bảng điều khiển quản trị viên' },
    children: [
      { path: '', name: 'AdminProfile', component: () => import('../views/profile/ProfileView.vue') },
      { path: 'users', name: 'UserManagement', component: () => import('../components/UserManagement.vue') },
      { path: 'profile', name: 'AdminUserProfile', component: () => import('../views/profile/ProfileView.vue') },
      { path: 'change-password', name: 'AdminChangePassword', component: () => import('../views/profile/ChangePassword.vue') },
      { path: 'upload-avatar', name: 'AdminUploadAvatar', component: () => import('../views/profile/UploadAvatar.vue') },
      { path: 'students', name: 'StudentManagement', component: () => import('../views/student/StudentManagement.vue') },
      { path: 'students/export', name: 'StudentsExport', component: () => import('../views/student/StudentExport.vue') },
      { path: 'student/me', name: 'StudentProfile', component: () => import('../views/student/StudentProfile.vue') },
      { path: 'teachers', name: 'TeacherManagement', component: () => import('../views/teacher/TeacherManagement.vue') },
      { path: 'teachers/export', name: 'TeachersExport', component: () => import('../views/teacher/TeacherExport.vue') },
      { path: 'teacher/me', name: 'TeacherProfile', component: () => import('../views/teacher/TeacherProfile.vue') },
      { path: 'classes', name: 'ClassManagement', component: () => import('../views/class/ClassManagement.vue') },
      { path: 'classes/export', name: 'ClassesExport', component: () => import('../views/class/ClassExport.vue') },
      { path: 'subjects', name: 'SubjectManagement', component: () => import('../views/subject/SubjectManagement.vue') },
      { path: 'subjects/export', name: 'SubjectsExport', component: () => import('../views/subject/SubjectExport.vue') },
      { path: 'enrollments', name: 'EnrollmentManagement', component: () => import('../views/enrollment/EnrollmentManagement.vue') },
      { path: 'enrollments/export', name: 'EnrollmentsExport', component: () => import('../views/enrollment/EnrollmentExport.vue') },
      { path: 'semesters', name: 'SemesterManagement', component: () => import('../views/semester/ActiveSemesters.vue') },
      { path: 'semesters/export', name: 'SemestersExport', component: () => import('../views/semester/SemesterExport.vue') },
      { path: 'scores', name: 'ScoreManagement', component: () => import('../views/score/ScoreManagement.vue') },
      { path: 'scores/export', name: 'ScoreExport', component: () => import('../views/score/ScoreExport.vue') },
      { path: 'departments', name: 'DepartmentManagement', component: () => import('../views/department/DepartmentView.vue') },
      { path: 'departments/export', name: 'DepartmentsExport', component: () => import('../views/department/DepartmentExport.vue') },
      { path: 'schedules', name: 'ScheduleManagement', component: () => import('../views/schedule/ScheduleManagement.vue') },
      { path: 'schedules/export', name: 'SchedulesExport', component: () => import('../views/schedule/ScheduleExport.vue') },
      { path: 'activities', name: 'ActivityView', component: () => import('../views/misc/ActivityView.vue') },
      { path: 'activities/export', name: 'ActivitiesExport', component: () => import('../views/misc/ActivityExport.vue') },
    ],
  },
  // Teacher Dashboard
  {
    path: '/teacher',
    component: () => import('../views/dashboard/TeacherDashboardView.vue'),
    meta: { requiresAuth: true, title: 'Bảng điều khiển giảng viên' },
    children: [
      { path: '', name: 'TeacherProfile', component: () => import('../views/profile/ProfileView.vue') },
      { path: 'profile', name: 'TeacherUserProfile', component: () => import('../views/profile/ProfileView.vue') },
      { path: 'change-password', name: 'TeacherChangePassword', component: () => import('../views/profile/ChangePassword.vue') },
      { path: 'upload-avatar', name: 'TeacherUploadAvatar', component: () => import('../views/profile/UploadAvatar.vue') },
      { path: 'me', name: 'TeacherSelfProfile', component: () => import('../views/teacher/TeacherProfile.vue') },
      { path: 'classes', name: 'TeacherClassManagement', component: () => import('../views/class/ClassManagement.vue') },
      { path: 'classes/export', name: 'TeacherClassesExport', component: () => import('../views/class/ClassExport.vue') },
      { path: 'subjects', name: 'TeacherSubjectManagement', component: () => import('../views/subject/SubjectManagement.vue') },
      { path: 'subjects/export', name: 'TeacherSubjectsExport', component: () => import('../views/subject/SubjectExport.vue') },
      { path: 'scores', name: 'TeacherScoreManagement', component: () => import('../views/score/ScoreManagement.vue') },
      { path: 'scores/export', name: 'TeacherScoreExport', component: () => import('../views/score/ScoreExport.vue') },
      { path: 'schedules', name: 'TeacherScheduleManagement', component: () => import('../views/schedule/ScheduleManagement.vue') },
      { path: 'schedules/export', name: 'TeacherSchedulesExport', component: () => import('../views/schedule/ScheduleExport.vue') },
      { path: 'activities', name: 'TeacherActivityView', component: () => import('../views/misc/ActivityView.vue') },
      { path: 'activities/export', name: 'TeacherActivitiesExport', component: () => import('../views/misc/ActivityExport.vue') },
    ],
  },
  // Student Dashboard
  {
    path: '/student',
    component: () => import('../views/dashboard/StudentDashboardView.vue'),
    meta: { requiresAuth: true, title: 'Bảng điều khiển sinh viên' },
    children: [
      { path: '', name: 'StudentProfile', component: () => import('../views/profile/ProfileView.vue') },
      { path: 'profile', name: 'StudentUserProfile', component: () => import('../views/profile/ProfileView.vue') },
      { path: 'change-password', name: 'StudentChangePassword', component: () => import('../views/profile/ChangePassword.vue') },
      { path: 'upload-avatar', name: 'StudentUploadAvatar', component: () => import('../views/profile/UploadAvatar.vue') },
      { path: 'me', name: 'StudentSelfProfile', component: () => import('../views/student/StudentProfile.vue') },
      { path: 'scores', name: 'MyScores', component: () => import('../views/score/MyScores.vue') },
      { path: 'scores/export', name: 'MyScoresExport', component: () => import('../views/score/ScoreExport.vue') },
      { path: 'schedules', name: 'MySchedules', component: () => import('../views/schedule/MySchedules.vue') },
      { path: 'schedules/export', name: 'MySchedulesExport', component: () => import('../views/schedule/ScheduleExport.vue') },
      { path: 'enrollments', name: 'MyEnrollments', component: () => import('../views/enrollment/MyEnrollments.vue') },
      { path: 'enrollments/export', name: 'MyEnrollmentsExport', component: () => import('../views/enrollment/EnrollmentExport.vue') },
      { path: 'activities', name: 'StudentActivityView', component: () => import('../views/misc/ActivityView.vue') },
      { path: 'activities/export', name: 'StudentActivitiesExport', component: () => import('../views/misc/ActivityExport.vue') },
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
    if (isAdmin.value) return next('/admin')
    if (isTeacher.value) return next('/teacher')
    return next('/student')
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