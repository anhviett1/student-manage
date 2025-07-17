// src/router/index.js (Cập nhật)
import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { usePermissions } from '@/utils/userPermissions';
import AdminLayout from '@/layouts/AdminLayout.vue';
import AuthLayout from '@/layouts/AuthLayout.vue';
import MainLayout from '@/layouts/MainLayout.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    // ... (routes đăng nhập, trang chủ, etc.)
    {
      path: '/admin',
      component: () => import('@/layouts/AdminLayout.vue'), // Sử dụng AdminLayout
      meta: { requiresAuth: true, requiredRole: 'admin' },
      children: [
        {
          path: '', // Route mặc định cho /admin
          name: 'AdminDashboard',
          component: () => import('@/views/Admin/AdminDashboard.vue')
        },
        {
          path: 'users',
          name: 'ManageUsers',
          component: () => import('@/views/Admin/ManageUsersPage.vue'),
          meta: { requiredPermission: 'app_user.change_user' } // Ví dụ quyền thay đổi user
        },
        {
            path: 'students',
            name: 'ManageStudents',
            component: () => import('@/views/Admin/ManageStudentsPage.vue'),
            meta: { requiredPermission: 'app_student.view_student' }
        },
        {
            path: 'teachers',
            name: 'ManageTeachers',
            component: () => import('@/views/Admin/ManageTeachersPage.vue'),
            meta: { requiredPermission: 'app_teacher.view_teacher' }
        },
        {
            path: 'subjects',
            name: 'ManageSubjects',
            component: () => import('@/views/Admin/ManageSubjectsPage.vue'),
            meta: { requiredPermission: 'app_subject.view_subject' }
        },
        {
            path: 'classes',
            name: 'ManageClasses',
            component: () => import('@/views/Admin/ManageClassesPage.vue'),
            meta: { requiredPermission: 'app_class.view_class' }
        },
        {
            path: 'departments',
            name: 'ManageDepartments',
            component: () => import('@/views/Admin/ManageDepartmentsPage.vue'),
            meta: { requiredPermission: 'app_department.view_department' }
        },
        {
            path: 'semesters',
            name: 'ManageSemesters',
            component: () => import('@/views/Admin/ManageSemestersPage.vue'),
            meta: { requiredPermission: 'app_semester.view_semester' }
        },
        {
            path: 'settings',
            name: 'SystemSettings',
            component: () => import('@/views/Admin/SystemSettingsPage.vue'),
            meta: { requiredPermission: 'app_home.change_settings' } // Quyền riêng cho settings
        },
        // ... các route quản lý khác cho admin
      ]
    },
    // ... (các routes khác cho teacher, student, 404, access-denied)
  ]
});

// Navigation Guards giữ nguyên như đã hướng dẫn
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const { isAuthenticated, isAdmin, isTeacher, isStudent, hasModelPermission } = usePermissions();

  // ... (logic kiểm tra auth, role, permission như cũ)

  next();
});

export default router;