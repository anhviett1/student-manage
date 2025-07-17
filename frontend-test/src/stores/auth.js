// src/stores/auth.js
import { defineStore } from 'pinia';
import { loginUser, logoutUser } from '@/services/mockAuthService'; // Sử dụng mockAuthService

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('token') || null,
    isAuthenticated: !!localStorage.getItem('token'),
    loading: false,
    error: null,
  }),
  getters: {
    isAdmin: (state) => state.user?.role === 'admin',
    isTeacher: (state) => state.user?.role === 'teacher',
    isStudent: (state) => state.user?.role === 'student',
  },
  actions: {
    async login(username, password) {
      this.loading = true;
      this.error = null;
      try {
        const response = await loginUser(username, password);
        if (response.success) {
          this.user = response.user;
          this.token = response.token;
          this.isAuthenticated = true;
          localStorage.setItem('user', JSON.stringify(response.user));
          localStorage.setItem('token', response.token);
          return true;
        } else {
          this.error = response.message || 'Đăng nhập thất bại.';
          return false;
        }
      } catch (err) {
        this.error = 'Lỗi kết nối hoặc hệ thống.';
        console.error('Login error:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    async logout() {
      this.loading = true;
      try {
        await logoutUser(); // Call to mock or actual logout API
        this.user = null;
        this.token = null;
        this.isAuthenticated = false;
        localStorage.removeItem('user');
        localStorage.removeItem('token');
        return true;
      } catch (err) {
        this.error = 'Lỗi khi đăng xuất.';
        console.error('Logout error:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    clearError() {
      this.error = null;
    }
  },
});