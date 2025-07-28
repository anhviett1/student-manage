import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

export function usePermissions() {
  const authStore = useAuthStore()

  // --- Role-based permissions ---
  const isAuthenticated = computed(() => authStore.isAuthenticated)
  const isAdmin = computed(() => authStore.user?.role === 'admin' )
  const isTeacher = computed(() => authStore.user?.role === 'teacher')
  const isStudent = computed(() => authStore.user?.role === 'student')
  const isAdminOrTeacher = computed(() => isAdmin.value || isTeacher.value)
  const isAdminOrStudent = computed(() => isAdmin.value || isStudent.value)
  const isTeacherOrStudent = computed(() => isTeacher.value || isStudent.value)
  const isAllRoles = computed(() => isAdmin.value || isTeacher.value || isStudent.value)
  const userRole = computed(() => authStore.user?.role || 'guest')

  // --- CRUD permissions (Admin or ReadOnly) ---
  const isAdminOrReadOnly = (method) => {
    const SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
    if (SAFE_METHODS.includes(method.toUpperCase())) {
      return isAuthenticated.value
    }
    return isAuthenticated.value && isAdmin.value
  }

  // --- Object-level permission: Owner or Admin ---
  const isOwnerOrAdmin = (obj, ownerKey = 'user') => {
    if (!isAuthenticated.value || !obj) return false
    if (isAdmin.value) return true
    const currentUser = authStore.user
    if (!currentUser?.id) return false
    let objOwnerId = null
    const ownerData = obj[ownerKey]
    if (ownerData) {
      if (typeof ownerData === 'object' && ownerData !== null && 'id' in ownerData) {
        objOwnerId = ownerData.id
      } else {
        objOwnerId = ownerData
      }
    }
    return objOwnerId !== null && objOwnerId === currentUser.id
  }

  // --- Object-level permission: Teacher or Admin for Assigned ---
  const isTeacherOrAdminForAssigned = (obj) => {
    if (!isAuthenticated.value || !obj) return false
    if (isAdmin.value) return true
    if (isTeacher.value && obj.teacher?.id === authStore.user?.id) return true
    return false
  }

  // --- Object-level permission: Student or Admin for Assigned ---
  const isStudentOrAdminForAssigned = (obj) => {
    if (!isAuthenticated.value || !obj) return false
    if (isAdmin.value) return true
    if (isStudent.value && obj.student?.id === authStore.user?.id) return true
    return false
  }

  // --- Model-level permission (Django-style) ---
  const hasModelPermission = (codename, appLabel) => {
    if (!isAuthenticated.value) return false
    const permissions = authStore.user?.permissions || []
    const fullPerm = `${appLabel}.${codename}`
    return permissions.includes(fullPerm)
  }

  // --- Application-specific permissions ---
  // 1. Profile permissions
  const hasProfilePermission = (obj) => {
    if (!isAuthenticated.value) return false
    if (isAdmin.value) return true
    return isOwnerOrAdmin(obj)
  }

  // 2. Student permissions
  const hasStudentAddPermission = (appLabel = 'app_student') => hasModelPermission('add_student', appLabel)
  const hasStudentChangePermission = (appLabel = 'app_student') => hasModelPermission('change_student', appLabel)
  const hasStudentDeletePermission = (appLabel = 'app_student') => hasModelPermission('delete_student', appLabel)

  // 3. Teacher permissions
  const hasTeacherAddPermission = (appLabel = 'app_teacher') => hasModelPermission('add_teacher', appLabel)
  const hasTeacherChangePermission = (appLabel = 'app_teacher') => hasModelPermission('change_teacher', appLabel)
  const hasTeacherDeletePermission = (appLabel = 'app_teacher') => hasModelPermission('delete_teacher', appLabel)

  // 4. Class permissions
  const hasClassPermission = (obj, method) => {
    if (!isAuthenticated.value) return false
    if (isAdmin.value) return true
    if (method.toUpperCase() === 'GET') {
      return isTeacher.value && obj.teacher?.id === authStore.user?.id ||
             isStudent.value && obj.students?.some(student => student.id === authStore.user?.id) ||
             isAdmin.value
    }
    return isAdmin.value
  }

  // 5. Department permissions
  const hasDepartmentPermission = (method) => isAdminOrReadOnly(method)

  // 6. Subject permissions
  const hasSubjectPermission = (obj, method) => {
    if (!isAuthenticated.value) return false
    if (method.toUpperCase() === 'GET') {
      return isAdmin.value || isTeacher.value || isStudent.value
    }
    return isAdmin.value || (isTeacher.value && obj.teacher?.id === authStore.user?.id)
  }

  // 7. Score permissions
  const hasScorePermission = (obj, method) => {
    if (!isAuthenticated.value) return false
    if (method.toUpperCase() === 'GET') {
      return isAdmin.value ||
             (isTeacher.value && obj.subject?.teacher?.id === authStore.user?.id) ||
             (isStudent.value && obj.student?.id === authStore.user?.id)
    }
    return isAdmin.value || (isTeacher.value && obj.subject?.teacher?.id === authStore.user?.id)
  }

  // 8. Schedule permissions
  const hasSchedulePermission = (obj, method) => {
    if (!isAuthenticated.value) return false
    if (method.toUpperCase() === 'GET') {
      return isAdmin.value ||
             (isTeacher.value && obj.subject?.teacher?.id === authStore.user?.id) ||
             (isStudent.value && obj.class_room?.students?.some(student => student.id === authStore.user?.id))
    }
    return isAdmin.value
  }

  // 9. Enrollment permissions
  const hasEnrollmentPermission = (obj, method) => {
    if (!isAuthenticated.value) return false
    if (method.toUpperCase() === 'GET') {
      return isAdmin.value ||
             (isTeacher.value && obj.subject?.teacher?.id === authStore.user?.id) ||
             (isStudent.value && obj.student?.id === authStore.user?.id)
    }
    return isAdmin.value || isTeacher.value || isStudent.value
  }

  // 10. Semester permissions
  const hasSemesterPermission = (method) => isAdminOrReadOnly(method)

  // 11. Activity permissions
  const hasActivityPermission = (obj, method) => {
    if (!isAuthenticated.value) return false
    if (method.toUpperCase() === 'GET') {
      return isAdmin.value ||
             (isTeacher.value && obj.created_by?.id === authStore.user?.id) ||
             (isStudent.value && obj.participants?.some(participant => participant.id === authStore.user?.id))
    }
    return isAdmin.value || (isTeacher.value && obj.created_by?.id === authStore.user?.id)
  }

  return {
    isAuthenticated,
    isAdmin,
    isTeacher,
    isStudent,
    isAdminOrTeacher,
    isAdminOrStudent,
    isTeacherOrStudent,
    isAllRoles,
    userRole,
    isAdminOrReadOnly,
    isOwnerOrAdmin,
    isTeacherOrAdminForAssigned,
    isStudentOrAdminForAssigned,
    hasModelPermission,
    hasProfilePermission,
    hasStudentAddPermission,
    hasStudentChangePermission,
    hasStudentDeletePermission,
    hasTeacherAddPermission,
    hasTeacherChangePermission,
    hasTeacherDeletePermission,
    hasClassPermission,
    hasDepartmentPermission,
    hasSubjectPermission,
    hasScorePermission,
    hasSchedulePermission,
    hasEnrollmentPermission,
    hasSemesterPermission,
    hasActivityPermission,
  }
}