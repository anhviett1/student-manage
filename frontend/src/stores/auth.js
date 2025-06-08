import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api, { endpoints } from '@/config/api'
import { useToast } from '@/composables/useToast'

export const useAuthStore = defineStore('auth', () => {
  const { addToast } = useToast()
  const token = ref(localStorage.getItem('access_token') || null)
  const refreshTokenValue = ref(localStorage.getItem('refresh_token') || null)
  const user = ref(null)
  const isLoading = ref(false)
  const errorMessage = ref(null)

  const isAuthenticated = computed(() => !!token.value)
  const userRole = computed(() => user.value?.role || null)
  const isAdmin = computed(() => userRole.value === 'admin')
  const isTeacher = computed(() => userRole.value === 'teacher')
  const isStudent = computed(() => userRole.value === 'student')

  const hasRole = (role) => {
    return userRole.value === role
  }

  const setToken = (access, refresh) => {
    token.value = access
    refreshTokenValue.value = refresh
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
    api.defaults.headers.common['Authorization'] = `Bearer ${access}`
  }

  const clearAuth = () => {
    token.value = null
    refreshTokenValue.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    delete api.defaults.headers.common['Authorization']
  }

  async function login(credentials) {
    isLoading.value = true
    errorMessage.value = null
    try {
      const response = await api.post(endpoints.login, credentials)
      const { access, refresh } = response.data
      setToken(access, refresh)
      await fetchCurrentUser()
      addToast({
        severity: 'success',
        summary: 'Đăng Nhập',
        detail: 'Đăng nhập thành công',
        life: 3000,
      })
      return response.data
    } catch (error) {
      errorMessage.value = error.response?.data?.detail || 'Đăng nhập thất bại'
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

  async function register(userData) {
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

  async function logout() {
    isLoading.value = true
    errorMessage.value = null
    try {
      await api.post(endpoints.logout, { refresh_token: refreshTokenValue.value })
      addToast({
        severity: 'success',
        summary: 'Đăng Xuất',
        detail: 'Đăng xuất thành công',
        life: 3000,
      })
    } catch (error) {
      console.warn('Logout error:', error)
    } finally {
      clearAuth()
      isLoading.value = false
    }
  }

  async function fetchCurrentUser() {
    if (!token.value) return null
    isLoading.value = true
    errorMessage.value = null
    try {
      const response = await api.get(endpoints.userProfile)
      user.value = response.data
      return response.data
    } catch (error) {
      errorMessage.value = error.response?.data?.detail || 'Không thể tải thông tin người dùng'
      clearAuth()
      throw error
    } finally {
      isLoading.value = false
    }
  }

  async function refreshAccessToken() {
    if (!refreshTokenValue.value) return null
    isLoading.value = true
    errorMessage.value = null
    try {
      const response = await api.post(endpoints.refreshToken, {
        refresh: refreshTokenValue.value,
      })
      const { access, refresh } = response.data
      setToken(access, refresh || refreshTokenValue.value)
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

  api.interceptors.response.use(
    (response) => response,
    async (error) => {
      if (error.response?.status === 401 && !error.config._retry) {
        error.config._retry = true
        try {
          await refreshAccessToken()
          return api(error.config)
        } catch (refreshError) {
          return Promise.reject(refreshError)
        }
      }
      return Promise.reject(error)
    }
  )

  return {
    token,
    refreshToken: refreshTokenValue,
    user,
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