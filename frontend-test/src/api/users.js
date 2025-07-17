// src/api/users.js
import apiClient from './apiClient';

export default {
  // Lấy danh sách users (Admin)
  getAllUsers() {
    return apiClient.get('/users/users/'); // url: /api/v1/users/users/
  },
  // Lấy user theo ID (Admin)
  getUserById(id) {
    return apiClient.get(`/users/users/${id}/`); // url: /api/v1/users/users/{id}/
  },
  // Tạo user mới (Admin)
  createUser(userData) {
    return apiClient.post('/users/users/', userData); // url: /api/v1/users/users/
  },
  // Cập nhật user (Admin)
  updateUser(id, userData) {
    return apiClient.put(`/users/users/${id}/`, userData); // url: /api/v1/users/users/{id}/
  },
  // Xóa user (Admin)
  deleteUser(id) {
    return apiClient.delete(`/users/users/${id}/`); // url: /api/v1/users/users/{id}/
  },
  // Lấy thống kê từ app_home
  getStatistics() {
    return apiClient.get('/users/statistics/'); // url: /api/v1/users/statistics/
  },
  // Xuất User
  exportUsersToExcel(filters = {}) {
    return apiClient.get('/users/export/', {
      params: filters,
      responseType: 'blob'
    }); // url: /api/v1/users/export/
  },
  // Quản lý điểm từ app_home (có vẻ là một endpoint admin để quản lý điểm tổng thể)
  getScoreManagementData() {
    return apiClient.get('/users/score-management/'); // url: /api/v1/users/score-management/
  }
};