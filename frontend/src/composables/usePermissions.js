import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

/**
 * Composable cung cấp các quyền truy cập dựa trên vai trò và quyền của người dùng.
 * Luôn là nguồn đáng tin cậy duy nhất cho việc kiểm tra quyền trong toàn bộ ứng dụng.
 */
export function usePermissions() {
  const authStore = useAuthStore()

  // --- 1. Quyền dựa trên vai trò (Role-based) ---
  const isAuthenticated = computed(() => authStore.isAuthenticated)
  const isAdmin = computed(() => ['admin', 'superuser'].includes(authStore.user?.role))
  const isTeacher = computed(() => authStore.user?.role === 'teacher')
  const isStudent = computed(() => authStore.user?.role === 'student')
  const isAdminOrTeacher = computed(() => isAdmin.value || isTeacher.value)

  // --- 2. Quyền xem các mục menu trong Sidebar ---
  // Logic này quyết định mục nào sẽ hiển thị trên menu chính.
  // Các view con có thể có logic phân quyền chi tiết hơn.
  const canViewStudents = computed(() => isAdminOrTeacher.value)
  const canViewTeachers = computed(() => isAdmin.value)
  const canViewClasses = computed(() => isAdminOrTeacher.value)
  const canViewSubjects = computed(() => isAdminOrTeacher.value)
  const canViewEnrollments = computed(() => isAdminOrTeacher.value)
  const canViewSemesters = computed(() => isAdminOrTeacher.value)
  const canViewScores = computed(() => isAuthenticated.value) // Mọi người đã đăng nhập đều có thể xem mục này
  const canViewSchedules = computed(() => isAuthenticated.value) // Mọi người đã đăng nhập đều có thể xem mục này
  const canViewDepartments = computed(() => isAdminOrTeacher.value)
  const canViewUsers = computed(() => isAdmin.value)

  // --- 3. Quyền CRUD (Create, Read, Update, Delete) ---
  /**
   * Kiểm tra quyền đọc cho mọi user, quyền ghi chỉ cho admin.
   * Tương tự IsAdminOrReadOnly của Django.
   * @param {string} method - HTTP method: 'GET', 'POST', 'PUT', 'DELETE', etc.
   */
  const isPermissionAdminOrReadOnly = (method) => {
    const SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
    if (SAFE_METHODS.includes(method.toUpperCase())) {
      return isAuthenticated.value
    }
    return isAuthenticated.value && isAdmin.value
  }

  // --- 4. Quyền trên đối tượng (Object-level) ---
  /**
   * Kiểm tra user hiện tại có phải là chủ sở hữu của đối tượng hoặc là admin không.
   * @param {object} obj - Đối tượng cần kiểm tra, phải có trường 'user' hoặc id.
   * @param {string} [ownerKey='user'] - Tên của trường chứa id của chủ sở hữu.
   */
  const isOwnerOrAdmin = (obj, ownerKey = 'user') => {
    if (!isAuthenticated.value || !obj) return false
    if (isAdmin.value) return true

    const currentUserId = authStore.user?.id
    if (!currentUserId) return false

    let objOwnerId = null
    const ownerData = obj[ownerKey]

    if (ownerData) {
      // Nếu ownerData là object (vd: { id: 1, ... })
      if (typeof ownerData === 'object' && ownerData !== null && 'id' in ownerData) {
        objOwnerId = ownerData.id
        // Nếu ownerData là id trực tiếp (vd: 1)
      } else {
        objOwnerId = ownerData
      }
    }

    return objOwnerId !== null && objOwnerId === currentUserId
  }

  // --- 5. Quyền theo model của Django (Django Model Permissions) ---
  /**
   * Kiểm tra quyền model cụ thể từ danh sách permissions của user.
   * @param {string} codename - Codename của quyền (vd: 'can_manage_scores').
   * @param {string} appLabel - App label của Django (vd: 'app_score').
   */
  const hasModelPermission = (codename, appLabel) => {
    if (!isAuthenticated.value) return false
    const permissions = authStore.user?.permissions || []
    const fullPerm = `${appLabel}.${codename}`
    return permissions.includes(fullPerm)
  }

  // Ví dụ cụ thể hóa:
  const canManageScores = (appLabel) => hasModelPermission('can_manage_scores', appLabel)

  // --- 6. Quyền đặc biệt ---
  /**
   * Cho phép sinh viên xem điểm của chính mình.
   * @param {object} scoreObject - Đối tượng điểm, chứa thông tin user.
   */
  const canViewOwnScores = (scoreObject) => {
    if (!isStudent.value || !scoreObject) return false
    return isOwnerOrAdmin(scoreObject) // Tận dụng lại logic isOwnerOrAdmin
  }

  return {
    // Trạng thái xác thực
    isAuthenticated,

    // Vai trò
    isAdmin,
    isTeacher,
    isStudent,
    isAdminOrTeacher,

    // Quyền xem menu
    canViewStudents,
    canViewTeachers,
    canViewClasses,
    canViewSubjects,
    canViewEnrollments,
    canViewSemesters,
    canViewScores,
    canViewSchedules,
    canViewDepartments,
    canViewUsers,

    // Quyền CRUD & Object-level
    isPermissionAdminOrReadOnly,
    isOwnerOrAdmin,

    // Quyền Model Django
    hasModelPermission,
    canManageScores,

    // Quyền đặc biệt
    canViewOwnScores,
  }
}
