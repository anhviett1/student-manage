import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api, { endpoints } from '@/config/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isTeacher = computed(() => user.value?.role === 'teacher')
  const isStudent = computed(() => user.value?.role === 'student')

  const hasRole = (requiredRole) => {
    if (requiredRole === 'admin') return isAdmin.value
    if (requiredRole === 'teacher') return isTeacher.value
    if (requiredRole === 'student') return isStudent.value
    return false
  }

  async function login(credentials) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post(endpoints.login, credentials)
      token.value = response.data.token
      localStorage.setItem('token', token.value)
      await getCurrentUser()
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Login failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function register(userData) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post(endpoints.register, userData)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Registration failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    loading.value = true
    error.value = null
    try {
      await api.post(endpoints.logout)
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      token.value = null
      user.value = null
      localStorage.removeItem('token')
      loading.value = false
    }
  }

  async function getCurrentUser() {
    if (!token.value) return null
    loading.value = true
    error.value = null
    try {
      const response = await api.get(endpoints.userProfile)
      user.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to get user profile'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function refreshToken() {
    if (!token.value) return null
    loading.value = true
    error.value = null
    try {
      const response = await api.post(endpoints.refreshToken)
      token.value = response.data.token
      localStorage.setItem('token', token.value)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to refresh token'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    token,
    user,
    loading,
    error,
    isAuthenticated,
    isAdmin,
    isTeacher,
    isStudent,
    hasRole,
    login,
    register,
    logout,
    getCurrentUser,
    refreshToken
  }
}) 