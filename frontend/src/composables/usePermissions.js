import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

export function usePermissions() {
  const authStore = useAuthStore()

  // Role checks
  const isSuperuser = computed(() => authStore.isSuperuser)
  const isAdmin = computed(() => authStore.role === 'admin')
  const isTeacher = computed(() => authStore.role === 'teacher')
  const isStudent = computed(() => authStore.role === 'student')

  // Role combinations
  const isAdminOrTeacher = computed(() => isAdmin.value || isTeacher.value)
  const isAdminOrSuperuser = computed(() => isAdmin.value || isSuperuser.value)
  const isTeacherOrStudent = computed(() => isTeacher.value || isStudent.value)

  // Permission checks
  const hasPermission = (permission) => {
    if (isSuperuser.value) return true
    if (authStore.permissions.includes('*')) return true
    return authStore.permissions.includes(permission)
  }

  // Permission combinations
  const hasAnyPermission = (permissions) => {
    return permissions.some(permission => hasPermission(permission))
  }

  const hasAllPermissions = (permissions) => {
    return permissions.every(permission => hasPermission(permission))
  }

  // Common permissions
  const canViewStudents = computed(() => hasPermission('student:view'))
  const canEditStudents = computed(() => hasPermission('student:edit'))
  const canDeleteStudents = computed(() => hasPermission('student:delete'))
  const canImportStudents = computed(() => hasPermission('student:import'))
  const canExportStudents = computed(() => hasPermission('student:export'))

  const canViewTeachers = computed(() => hasPermission('teacher:view'))
  const canEditTeachers = computed(() => hasPermission('teacher:edit'))
  const canDeleteTeachers = computed(() => hasPermission('teacher:delete'))
  const canImportTeachers = computed(() => hasPermission('teacher:import'))
  const canExportTeachers = computed(() => hasPermission('teacher:export'))

  const canViewSubjects = computed(() => hasPermission('subject:view'))
  const canEditSubjects = computed(() => hasPermission('subject:edit'))
  const canDeleteSubjects = computed(() => hasPermission('subject:delete'))
  const canImportSubjects = computed(() => hasPermission('subject:import'))
  const canExportSubjects = computed(() => hasPermission('subject:export'))

  const canViewClasses = computed(() => hasPermission('class:view'))
  const canEditClasses = computed(() => hasPermission('class:edit'))
  const canDeleteClasses = computed(() => hasPermission('class:delete'))
  const canImportClasses = computed(() => hasPermission('class:import'))
  const canExportClasses = computed(() => hasPermission('class:export'))

  const canViewEnrollments = computed(() => hasPermission('enrollment:view'))
  const canEditEnrollments = computed(() => hasPermission('enrollment:edit'))
  const canDeleteEnrollments = computed(() => hasPermission('enrollment:delete'))
  const canImportEnrollments = computed(() => hasPermission('enrollment:import'))
  const canExportEnrollments = computed(() => hasPermission('enrollment:export'))

  const canViewScores = computed(() => hasPermission('score:view'))
  const canEditScores = computed(() => hasPermission('score:edit'))
  const canDeleteScores = computed(() => hasPermission('score:delete'))
  const canImportScores = computed(() => hasPermission('score:import'))
  const canExportScores = computed(() => hasPermission('score:export'))
  const canUploadScores = computed(() => hasPermission('score:upload'))

  const canViewSemesters = computed(() => hasPermission('semester:view'))
  const canEditSemesters = computed(() => hasPermission('semester:edit'))
  const canDeleteSemesters = computed(() => hasPermission('semester:delete'))
  const canImportSemesters = computed(() => hasPermission('semester:import'))
  const canExportSemesters = computed(() => hasPermission('semester:export'))

  // Feature-based permissions
  const canManageUsers = computed(() => isAdminOrSuperuser.value)
  const canManageSystem = computed(() => isAdminOrSuperuser.value)
  const canViewReports = computed(() => isAdminOrTeacher.value)
  const canExportData = computed(() => isAdminOrTeacher.value)
  const canImportData = computed(() => isAdminOrTeacher.value)
  const canManageSettings = computed(() => isAdminOrSuperuser.value)
  const canViewDashboard = computed(() => isAdminOrTeacher.value)
  const canViewAnalytics = computed(() => isAdminOrTeacher.value)

  // Student-specific permissions
  const canViewOwnScores = computed(() => isStudent.value)
  const canViewOwnEnrollments = computed(() => isStudent.value)
  const canViewStudentProfile = computed(() => isStudent.value)
  const canEditStudentProfile = computed(() => isStudent.value)
  const canViewStudentSchedule = computed(() => isStudent.value)
  const canUploadStudentAvatar = computed(() => isStudent.value)

  // Teacher-specific permissions
  const canManageOwnClass = computed(() => isTeacher.value)
  const canManageOwnScores = computed(() => isTeacher.value)
  const canViewOwnStudents = computed(() => isTeacher.value)
  const canViewTeacherSchedule = computed(() => isTeacher.value)
  const canEditTeacherProfile = computed(() => isTeacher.value)
  const canUploadTeacherAvatar = computed(() => isTeacher.value)

  // Admin profile permissions
  const canUploadAdminAvatar = computed(() => isAdmin.value)

  // Department permissions
  const canViewDepartments = computed(() => hasPermission('department:view'))
  const canEditDepartments = computed(() => hasPermission('department:edit'))
  const canDeleteDepartments = computed(() => hasPermission('department:delete'))
  const canImportDepartments = computed(() => hasPermission('department:import'))
  const canExportDepartments = computed(() => hasPermission('department:export'))

  // Schedule permissions
  const canViewSchedules = computed(() => hasPermission('schedule:view'))
  const canEditSchedules = computed(() => hasPermission('schedule:edit'))
  const canDeleteSchedules = computed(() => hasPermission('schedule:delete'))
  const canImportSchedules = computed(() => hasPermission('schedule:import'))
  const canExportSchedules = computed(() => hasPermission('schedule:export'))

  return {
    // Role checks
    isSuperuser,
    isAdmin,
    isTeacher,
    isStudent,
    isAdminOrTeacher,
    isAdminOrSuperuser,
    isTeacherOrStudent,

    // Permission checks
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,

    // Common permissions
    canViewStudents,
    canEditStudents,
    canDeleteStudents,
    canImportStudents,
    canExportStudents,
    canViewTeachers,
    canEditTeachers,
    canDeleteTeachers,
    canImportTeachers,
    canExportTeachers,
    canViewSubjects,
    canEditSubjects,
    canDeleteSubjects,
    canImportSubjects,
    canExportSubjects,
    canViewClasses,
    canEditClasses,
    canDeleteClasses,
    canImportClasses,
    canExportClasses,
    canViewEnrollments,
    canEditEnrollments,
    canDeleteEnrollments,
    canImportEnrollments,
    canExportEnrollments,
    canViewScores,
    canEditScores,
    canDeleteScores,
    canImportScores,
    canExportScores,
    canUploadScores,
    canViewSemesters,
    canEditSemesters,
    canDeleteSemesters,
    canImportSemesters,
    canExportSemesters,

    // Feature-based permissions
    canManageUsers,
    canManageSystem,
    canViewReports,
    canExportData,
    canImportData,
    canManageSettings,
    canViewDashboard,
    canViewAnalytics,

    // Role-specific permissions
    canViewOwnScores,
    canViewOwnEnrollments,
    canViewStudentProfile,
    canEditStudentProfile,
    canViewStudentSchedule,
    canUploadStudentAvatar,
    canManageOwnClass,
    canManageOwnScores,
    canViewOwnStudents,
    canViewTeacherSchedule,
    canEditTeacherProfile,
    canUploadTeacherAvatar,
    canUploadAdminAvatar,

    // Department permissions
    canViewDepartments,
    canEditDepartments,
    canDeleteDepartments,
    canImportDepartments,
    canExportDepartments,

    // Schedule permissions
    canViewSchedules,
    canEditSchedules,
    canDeleteSchedules,
    canImportSchedules,
    canExportSchedules
  }
}
