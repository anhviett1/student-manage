import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const setToken = (newToken) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  const setUser = (newUser) => {
    user.value = newUser
    localStorage.setItem('user', JSON.stringify(newUser))
  }

  const logout = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  const isAuthenticated = () => {
    return !!token.value
  }

  // Role-based access control
  const isAdmin = computed(() => {
    return user.value?.role === 'admin'
  })

  const isTeacher = computed(() => {
    return user.value?.role === 'teacher'
  })

  const isStudent = computed(() => {
    return user.value?.role === 'student'
  })

  const canAccess = (requiredRole) => {
    if (!user.value) return false
    if (requiredRole === 'admin') return isAdmin.value
    if (requiredRole === 'teacher') return isAdmin.value || isTeacher.value
    if (requiredRole === 'student') return true // All authenticated users can access student routes
    return false
  }

  return {
    token,
    user,
    setToken,
    setUser,
    logout,
    isAuthenticated,
    isAdmin,
    isTeacher,
    isStudent,
    canAccess
  }
}) 