import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

/**
 * usePermissions composable: Provides role and permission helpers for the frontend.
 * Inspired by backend permissions.py.
 */
export function usePermissions() {
  const authStore = useAuthStore()

  // --- Role-based permissions ---
  const isAuthenticated = computed(() => authStore.isAuthenticated)
  const isAdmin = computed(() => ['admin'].includes(authStore.user?.role))
  const isTeacher = computed(() => authStore.user?.role === 'teacher')
  const isStudent = computed(() => authStore.user?.role === 'student')
  const isAdminOrTeacher = computed(() => isAdmin.value || isTeacher.value)

  // --- CRUD permissions (Admin or ReadOnly) ---
  const isPermissionAdminOrReadOnly = (method) => {
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
    const currentUserId = authStore.user?.id
    if (!currentUserId) return false
    let objOwnerId = null
    const ownerData = obj[ownerKey]
    if (ownerData) {
      if (typeof ownerData === 'object' && ownerData !== null && 'id' in ownerData) {
        objOwnerId = ownerData.id
      } else {
        objOwnerId = ownerData
      }
    }
    return objOwnerId !== null && objOwnerId === currentUserId
  }

  // --- Model permission (Django style) ---
  const hasModelPermission = (codename, appLabel) => {
    if (!isAuthenticated.value) return false
    const permissions = authStore.user?.permissions || []
    const fullPerm = `${appLabel}.${codename}`
    return permissions.includes(fullPerm)
  }

  // --- Special permissions ---
  const canManageScores = (appLabel) => hasModelPermission('can_manage_scores', appLabel)
  const canManageSubjects = (appLabel) => hasModelPermission('can_manage_subjects', appLabel)
  const canViewSubjectScores = (appLabel) => hasModelPermission('can_view_subject_scores', appLabel)

  // --- Student: view own scores ---
  const canViewOwnScores = (scoreObject) => {
    if (!isStudent.value || !scoreObject) return false
    return isOwnerOrAdmin(scoreObject)
  }

  // --- Expose role for convenience ---
  const userRole = computed(() => authStore.user?.role || 'guest')

  return {
    isAuthenticated,
    isAdmin,
    isTeacher,
    isStudent,
    isAdminOrTeacher,
    isPermissionAdminOrReadOnly,
    isOwnerOrAdmin,
    hasModelPermission,
    canManageScores,
    canManageSubjects,
    canViewSubjectScores,
    canViewOwnScores,
    userRole,
  }
} 