import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/stores/auth'

/**
 * useAppEvents composable: Handles global app events (login, logout, token, toast, loading overlay)
 */
export function useAppEvents() {
  const router = useRouter()
  const toast = useToast()
  const authStore = useAuthStore()
  const isLoading = ref(false)

  // Show toast notification
  const notify = ({ severity = 'info', summary = '', detail = '', life = 3000 }) => {
    toast.add({ severity, summary, detail, life })
  }

  // Show/hide loading overlay
  const showLoading = () => { isLoading.value = true }
  const hideLoading = () => { isLoading.value = false }

  // Login event
  const handleLogin = async (credentials) => {
    try {
      showLoading()
      await authStore.login(credentials)
      notify({ severity: 'success', summary: 'Đăng nhập', detail: 'Đăng nhập thành công!' })
      // Redirect based on role
      const role = authStore.user?.role
      if (role === 'admin') router.push('/admin')
      else if (role === 'teacher') router.push('/teacher')
      else if (role === 'student') router.push('/student')
      else router.push('/')
    } catch (error) {
      notify({ severity: 'error', summary: 'Lỗi', detail: authStore.errorMessage || 'Đăng nhập thất bại!' })
    } finally {
      hideLoading()
    }
  }

  // Logout event
  const handleLogout = async () => {
    try {
      showLoading()
      await authStore.logout()
      notify({ severity: 'success', summary: 'Đăng xuất', detail: 'Đăng xuất thành công!' })
      router.push('/login')
    } catch (error) {
      notify({ severity: 'error', summary: 'Lỗi', detail: 'Đăng xuất thất bại!' })
    } finally {
      hideLoading()
    }
  }

  // Token management (refresh, get, clear)
  const getToken = () => authStore.accessToken
  const refreshToken = async () => {
    try {
      showLoading()
      await authStore.refreshAccessToken()
      notify({ severity: 'success', summary: 'Token', detail: 'Làm mới token thành công!' })
    } catch (error) {
      notify({ severity: 'error', summary: 'Token', detail: 'Làm mới token thất bại!' })
    } finally {
      hideLoading()
    }
  }
  const clearToken = () => authStore.clearAuth()

  return {
    isLoading,
    notify,
    showLoading,
    hideLoading,
    handleLogin,
    handleLogout,
    getToken,
    refreshToken,
    clearToken,
  }
} 