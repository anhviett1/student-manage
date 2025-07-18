import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api, { endpoints } from '@/services/api';
import { useToast } from '@/composables/useToast';
import { useAuthStore } from './auth';

export const useUserStore = defineStore('user', () => {
  const { addToast } = useToast();
  const authStore = useAuthStore();
  const users = ref([]);
  const currentUser = ref(null);
  const isLoading = ref(false);
  const errorMessage = ref(null);

  const isAdmin = computed(() => ['admin'].includes(currentUser.value?.role));
  const isTeacher = computed(() => currentUser.value?.role === 'teacher');
  const isStudent = computed(() => currentUser.value?.role === 'student');

  const getUserById = computed(() => (userId) => {
    return users.value.find((user) => user.id === userId);
  });

  async function fetchUsers(params = {}) {
    if (!authStore.isAdmin) {
      addToast({
        severity: 'error',
        summary: 'Lỗi',
        detail: 'Bạn không có quyền truy cập danh sách người dùng',
        life: 3000,
      });
      return [];
    }
    isLoading.value = true;
    errorMessage.value = null;
    try {
      const response = await api.get(endpoints.users, { params });
      let userData = [];
      if (Array.isArray(response.data)) {
        userData = response.data;
      } else if (response.data && Array.isArray(response.data.results)) {
        userData = response.data.results;
      } else if (response.data && typeof response.data === 'object') {
        userData = Object.values(response.data).filter(item => Array.isArray(item)).flat();
      }
      users.value = userData;
      return userData;
    } catch (error) {
      errorMessage.value = error.response?.data?.detail || 'Không thể tải danh sách người dùng';
      addToast({
        severity: 'error',
        summary: 'Lỗi',
        detail: errorMessage.value,
        life: 3000,
      });
      users.value = [];
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function createUser(userData) {
    if (!authStore.isAdmin) {
      addToast({
        severity: 'error',
        summary: 'Lỗi',
        detail: 'Bạn không có quyền tạo người dùng',
        life: 3000,
      });
      return;
    }
    isLoading.value = true;
    errorMessage.value = null;
    try {
      const response = await api.post(endpoints.users, userData);
      users.value.push(response.data);
      addToast({
        severity: 'success',
        summary: 'Thành Công',
        detail: 'Tạo người dùng mới thành công',
        life: 3000,
      });
      return response.data;
    } catch (error) {
      errorMessage.value = error.response?.data?.detail || 'Không thể tạo người dùng';
      addToast({
        severity: 'error',
        summary: 'Lỗi',
        detail: errorMessage.value,
        life: 3000,
      });
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function updateUser(userId, userData) {
    if (!authStore.isAdmin && currentUser.value?.id !== userId) {
      addToast({
        severity: 'error',
        summary: 'Lỗi',
        detail: 'Bạn không có quyền cập nhật người dùng này',
        life: 3000,
      });
      return;
    }
    isLoading.value = true;
    errorMessage.value = null;
    try {
      const response = await api.put(`${endpoints.users}${userId}/`, userData);
      const index = users.value.findIndex((user) => user.id === userId);
      if (index !== -1) {
        users.value[index] = response.data;
      }
      if (currentUser.value?.id === userId) {
        currentUser.value = response.data;
      }
      addToast({
        severity: 'success',
        summary: 'Thành Công',
        detail: 'Cập nhật người dùng thành công',
        life: 3000,
      });
      return response.data;
    } catch (error) {
      errorMessage.value = error.response?.data?.detail || 'Không thể cập nhật người dùng';
      addToast({
        severity: 'error',
        summary: 'Lỗi',
        detail: errorMessage.value,
        life: 3000,
      });
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function deleteUser(userId) {
    if (!authStore.isAdmin) {
      addToast({
        severity: 'error',
        summary: 'Lỗi',
        detail: 'Bạn không có quyền xóa người dùng',
        life: 3000,
      });
      return;
    }
    isLoading.value = true;
    errorMessage.value = null;
    try {
      await api.delete(`${endpoints.users}${userId}/`);
      users.value = users.value.filter((user) => user.id !== userId);
      addToast({
        severity: 'success',
        summary: 'Thành Công',
        detail: 'Xóa người dùng thành công',
        life: 3000,
      });
    } catch (error) {
      errorMessage.value = error.response?.data?.detail || 'Không thể xóa người dùng';
      addToast({
        severity: 'error',
        summary: 'Lỗi',
        detail: errorMessage.value,
        life: 3000,
      });
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function getCurrentUser() {
    if (!authStore.isAuthenticated) return null;
    isLoading.value = true;
    errorMessage.value = null;
    try {
      const response = await api.get(endpoints.userProfile);
      currentUser.value = response.data;
      return response.data;
    } catch (error) {
      errorMessage.value = error.response?.data?.detail || 'Không thể tải hồ sơ người dùng';
      addToast({
        severity: 'error',
        summary: 'Lỗi',
        detail: errorMessage.value,
        life: 3000,
      });
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function updateProfile(userData) {
    isLoading.value = true;
    errorMessage.value = null;
    try {
      const response = await api.put(endpoints.userProfile, userData);
      currentUser.value = response.data;
      addToast({
        severity: 'success',
        summary: 'Thành Công',
        detail: 'Cập nhật hồ sơ thành công',
        life: 3000,
      });
      return response.data;
    } catch (error) {
      errorMessage.value = error.response?.data?.detail || 'Không thể cập nhật hồ sơ';
      addToast({
        severity: 'error',
        summary: 'Lỗi',
        detail: errorMessage.value,
        life: 3000,
      });
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function changePassword(passwordData) {
    isLoading.value = true;
    errorMessage.value = null;
    try {
      await api.post(endpoints.changePassword, passwordData);
      addToast({
        severity: 'success',
        summary: 'Thành Công',
        detail: 'Đổi mật khẩu thành công',
        life: 3000,
      });
    } catch (error) {
      errorMessage.value = error.response?.data?.detail || 'Không thể đổi mật khẩu';
      addToast({
        severity: 'error',
        summary: 'Lỗi',
        detail: errorMessage.value,
        life: 3000,
      });
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchAllUsers() {
    try {
      const response = await api.get(endpoints.users, { params: { page_size: 9999 } });
      let userData = [];
      if (Array.isArray(response.data)) {
        userData = response.data;
      } else if (response.data && Array.isArray(response.data.results)) {
        userData = response.data.results;
      } else if (response.data && typeof response.data === 'object') {
        userData = Object.values(response.data).filter(item => Array.isArray(item)).flat();
      }
      return userData;
    } catch (error) {
      return [];
    }
  }

  async function fetchUserById(userId) {
    try {
      const response = await api.get(`${endpoints.users}${userId}/`);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  async function updateUserProfile(userId, payload) {
    try {
      const response = await api.put(`${endpoints.users}${userId}/`, payload);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  async function uploadAvatar(formData) {
    try {
      const response = await api.post(endpoints.uploadAvatar, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  async function deleteAvatar() {
    try {
      const response = await api.delete(endpoints.uploadAvatar);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  return {
    users,
    currentUser,
    isLoading,
    errorMessage,
    isAdmin,
    isTeacher,
    isStudent,
    getUserById,
    fetchUsers,
    createUser,
    updateUser,
    deleteUser,
    getCurrentUser,
    updateProfile,
    changePassword,
    fetchAllUsers,
    fetchUserById,
    updateUserProfile,
    uploadAvatar,
    deleteAvatar,
  };
});