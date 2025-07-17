// src/api/auth.js
import apiClient from './apiClient';

export default {
  login(credentials) {
    return apiClient.post('/token/', credentials); // url: /api/v1/token/
  },
  refreshToken(refreshToken) {
    return apiClient.post('/token/refresh/', { refresh: refreshToken }); // url: /api/v1/token/refresh/
  },
  verifyToken(token) {
    return apiClient.post('/token/verify/', { token: token }); // url: /api/v1/token/verify/
  },
  logout() {
    return apiClient.post('/users/logout/'); // url: /api/v1/users/logout/
  },
  getProfile() {
    return apiClient.get('/users/profile/'); // url: /api/v1/users/profile/
  },
  changePassword(data) {
    return apiClient.post('/users/change-password/', data); // url: /api/v1/users/change-password/
  },
  uploadAvatar(formData) {
    // Lưu ý: Đối với upload file, cần thiết lập Content-Type là 'multipart/form-data'
    // Axios sẽ tự động làm điều này nếu bạn truyền FormData object
    return apiClient.post('/users/avatar/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }); // url: /api/v1/users/avatar/
  },
};