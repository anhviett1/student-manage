import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { useToast } from '@/composables/useToast'

export const useAuthStore = defineStore('auth', () => {
  const { addToast } = useToast()
  const user = ref(null)
  const token = ref(localStorage.getItem('token'))
  const permissions = ref([])
  const isSuperuser = ref(false)
  const isLoading = ref(false)
  const errorMessage = ref(null)

  const isAuthenticated = computed(() => !!token.value)
  const userRole = computed(() => user.value?.role)

  const hasPermission = (permission) => {
    if (isSuperuser.value) return true
    if (permissions.value.includes('*')) return true
    return permissions.value.includes(permission)
  }

  const fetchUserRole = async () => {
    try {
      const response = await axios.get('/api/v1/users/auth/role/')
      permissions.value = response.data.permissions
      isSuperuser.value = response.data.is_superuser
      return response.data
    } catch (error) {
      console.error('Error fetching user role:', error)
      throw error
    }
  }

  const login = async (credentials) => {
    try {
      const response = await axios.post('/api/v1/users/auth/login/', credentials)
      token.value = response.data.access
      localStorage.setItem('token', response.data.access)
      axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
      
      // Fetch user role and permissions after login
      await fetchUserRole()
      
      addToast({
        severity: 'success',
        summary: 'Đăng Nhập',
        detail: 'Đăng nhập thành công',
        life: 3000,
      })
      
      return response.data
    } catch (error) {
      console.error('Login error:', error)
      addToast({
        severity: 'error',
        summary: 'Lỗi',
        detail: error.response?.data?.error || 'Đăng nhập thất bại',
        life: 3000,
      })
      throw error
    }
  }

  const logout = async () => {
    try {
      await axios.post('/api/v1/users/auth/logout/')
      addToast({
        severity: 'success',
        summary: 'Đăng Xuất',
        detail: 'Đăng xuất thành công',
        life: 3000,
      })
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      token.value = null
      user.value = null
      permissions.value = []
      isSuperuser.value = false
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    }
  }

  const register = async (userData) => {
    try {
      const response = await axios.post('/api/v1/users/auth/register/', userData)
      addToast({
        severity: 'success',
        summary: 'Đăng Ký',
        detail: 'Đăng ký tài khoản thành công',
        life: 3000,
      })
      return response.data
    } catch (error) {
      console.error('Registration error:', error)
      addToast({
        severity: 'error',
        summary: 'Lỗi',
        detail: error.response?.data?.error || 'Đăng ký thất bại',
        life: 3000,
      })
      throw error
    }
  }

  const fetchUserProfile = async () => {
    try {
      const response = await axios.get('/api/v1/users/auth/profile/')
      user.value = response.data
      return response.data
    } catch (error) {
      console.error('Error fetching user profile:', error)
      throw error
    }
  }

  const updateUserProfile = async (profileData) => {
    try {
      const response = await axios.patch('/api/v1/users/auth/profile/', profileData)
      user.value = response.data.data
      addToast({
        severity: 'success',
        summary: 'Thành Công',
        detail: 'Cập nhật hồ sơ thành công',
        life: 3000,
      })
      return response.data
    } catch (error) {
      console.error('Error updating user profile:', error)
      addToast({
        severity: 'error',
        summary: 'Lỗi',
        detail: error.response?.data?.error || 'Cập nhật hồ sơ thất bại',
        life: 3000,
      })
      throw error
    }
  }

  const uploadAvatar = async (file) => {
    try {
      const formData = new FormData()
      formData.append('avatar', file)
      const response = await axios.post('/api/v1/users/auth/avatar/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      if (user.value) {
        user.value.avatar = response.data.avatar_url
      }
      addToast({
        severity: 'success',
        summary: 'Thành Công',
        detail: 'Cập nhật ảnh đại diện thành công',
        life: 3000,
      })
      return response.data
    } catch (error) {
      console.error('Error uploading avatar:', error)
      addToast({
        severity: 'error',
        summary: 'Lỗi',
        detail: error.response?.data?.error || 'Cập nhật ảnh đại diện thất bại',
        life: 3000,
      })
      throw error
    }
  }

  return {
    user,
    token,
    permissions,
    isSuperuser,
    isLoading,
    errorMessage,
    isAuthenticated,
    userRole,
    hasPermission,
    login,
    logout,
    register,
    fetchUserProfile,
    updateUserProfile,
    uploadAvatar,
    fetchUserRole
  }
})