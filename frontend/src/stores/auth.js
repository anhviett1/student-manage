import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api, { endpoints } from '@/services/api'
import { useToast } from '@/composables/useToast'

export const useAuthStore = defineStore('auth', () => {
  const { addToast } = useToast()
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('access_token'))
  const refreshToken = ref(localStorage.getItem('refresh_token'))
  const isLoading = ref(false)
  const errorMessage = ref(null)

  const isAuthenticated = computed(() => !!accessToken.value)
  const userRole = computed(() => user.value?.role || null)
  const isAdmin = computed(() => ['admin'].includes(userRole.value))
  const isTeacher = computed(() => userRole.value === 'teacher')
  const isStudent = computed(() => userRole.value === 'student')

  const hasRole = (role) => {
    return userRole.value === role
  }

  const setToken = (access, refresh) => {
    accessToken.value = access
    refreshToken.value = refresh
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
    api.defaults.headers.common['Authorization'] = `Bearer ${access}`
  }

  const clearAuth = () => {
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    delete api.defaults.headers.common['Authorization']
  }

const login = async (credentials) => {
  isLoading.value = true
  errorMessage.value = null
  try {
    if (!credentials.username || !credentials.password) {
      throw new Error('Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu')
    }
    const response = await api.post(endpoints.login, credentials, {
      withCredentials: true,
    })
    const { access, refresh } = response.data
    setToken(access, refresh)
    await fetchCurrentUser()
    addToast({
      severity: 'success',
      summary: 'Đăng Nhập',
      detail: 'Đăng nhập thành công',
      life: 3000,
    })
    return response
  } catch (error) {
    console.error('Login error:', error.response?.status, error.response?.data, error.message)
    const status = error.response?.status
    let message = 'Đăng nhập thất bại'
    if (status === 400) {
      message = 'Dữ liệu không hợp lệ, vui lòng kiểm tra lại'
    } else if (status === 401) {
      message = 'Tên đăng nhập hoặc mật khẩu không đúng'
    } else if (status === 403) {
      message = 'Bạn không có quyền truy cập'
    } else if (!error.response) {
      message = 'Không thể kết nối đến server. Kiểm tra CORS hoặc server.'
    } else {
      message = error.response?.data?.detail || 'Đã có lỗi xảy ra'
    }
    errorMessage.value = message
    addToast({
      severity: 'error',
      summary: 'Lỗi',
      detail: message,
      life: 3000,
    })
    throw error
  } finally {
    isLoading.value = false
  }
}

  const register = async (userData) => {
    isLoading.value = true
    errorMessage.value = null
    try {
      const response = await api.post(endpoints.register, userData)
      addToast({
        severity: 'success',
        summary: 'Đăng Ký',
        detail: 'Đăng ký tài khoản thành công',
        life: 3000,
      })
      return response.data
    } catch (error) {
      errorMessage.value = error.response?.data?.detail || 'Đăng ký thất bại'
      addToast({
        severity: 'error',
        summary: 'Lỗi',
        detail: errorMessage.value,
        life: 3000,
      })
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    isLoading.value = true
    errorMessage.value = null
    try {
      await api.post(endpoints.logout)
      addToast({
        severity: 'success',
        summary: 'Đăng Xuất',
        detail: 'Đăng xuất thành công',
        life: 3000,
      })
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      clearAuth()
      isLoading.value = false
    }
  }

  const fetchCurrentUser = async () => {
    if (!accessToken.value) return null
    isLoading.value = true
    errorMessage.value = null
    try {
      const response = await api.get(endpoints.userProfile)
      console.log('User profile data from backend:', response.data)
      user.value = response.data
      return response.data
    } catch (error) {
      errorMessage.value = error.response?.data?.detail || 'Không thể tải thông tin người dùng'
      
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const refreshAccessToken = async () => {
    if (!refreshToken.value) return null
    isLoading.value = true
    errorMessage.value = null
    try {
      const response = await api.post(endpoints.refreshToken, {
        refresh: refreshToken.value,
      })
      const { access, refresh } = response.data
      setToken(access, refresh || refreshToken.value)
      return response.data
    } catch (error) {
      errorMessage.value = error.response?.data?.detail || 'Không thể làm mới token'
      clearAuth()
      addToast({
        severity: 'error',
        summary: 'Phiên Hết Hạn',
        detail: 'Vui lòng đăng nhập lại',
        life: 3000,
      })
      throw error
    } finally {
      isLoading.value = false
    }
  }

  return {
    user,
    accessToken,
    refreshToken,
    isLoading,
    errorMessage,
    isAuthenticated,
    isAdmin,
    isTeacher,
    isStudent,
    hasRole,
    login,
    register,
    logout,
    fetchCurrentUser,
    refreshAccessToken,
  }
})