import { defineStore } from 'pinia'
import api, { endpoints } from '@/config/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    users: [],
    currentUser: null,
    loading: false,
    error: null
  }),

  actions: {
    async fetchUsers() {
      this.loading = true
      try {
        const response = await api.get(endpoints.users)
        this.users = response.data
        return this.users
      } catch (error) {
        this.error = error.response?.data?.message || 'Error fetching users'
        throw error
      } finally {
        this.loading = false
      }
    },

    async createUser(userData) {
      this.loading = true
      try {
        const response = await api.post(endpoints.users, userData)
        this.users.push(response.data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Error creating user'
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateUser(userId, userData) {
      this.loading = true
      try {
        const response = await api.put(`${endpoints.users}${userId}/`, userData)
        const index = this.users.findIndex(user => user.id === userId)
        if (index !== -1) {
          this.users[index] = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Error updating user'
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteUser(userId) {
      this.loading = true
      try {
        await api.delete(`${endpoints.users}${userId}/`)
        this.users = this.users.filter(user => user.id !== userId)
      } catch (error) {
        this.error = error.response?.data?.message || 'Error deleting user'
        throw error
      } finally {
        this.loading = false
      }
    },

    async getCurrentUser() {
      this.loading = true
      try {
        const response = await api.get(endpoints.userProfile)
        this.currentUser = response.data
        return this.currentUser
      } catch (error) {
        this.error = error.response?.data?.message || 'Error fetching current user'
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateProfile(userData) {
      this.loading = true
      try {
        const response = await api.put(endpoints.userProfile, userData)
        this.currentUser = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Error updating profile'
        throw error
      } finally {
        this.loading = false
      }
    },

    async changePassword(passwordData) {
      this.loading = true
      try {
        await api.post(endpoints.changePassword, passwordData)
      } catch (error) {
        this.error = error.response?.data?.message || 'Error changing password'
        throw error
      } finally {
        this.loading = false
      }
    }
  },

  getters: {
    getUserById: (state) => (userId) => {
      return state.users.find(user => user.id === userId)
    },
    isAdmin: (state) => {
      return state.currentUser?.role === 'admin'
    },
    isTeacher: (state) => {
      return state.currentUser?.role === 'teacher'
    },
    isStudent: (state) => {
      return state.currentUser?.role === 'student'
    }
  }
}) 