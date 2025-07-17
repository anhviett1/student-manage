// src/api/apiClient.js
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import router from '@/router'; // Import router để chuyển hướng

const apiClient = axios.create({
  // Sử dụng biến môi trường để dễ dàng thay đổi khi deploy
  baseURL: import.meta.env.VITE_APP_API_BASE_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(config => {
  const authStore = useAuthStore();
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

apiClient.interceptors.response.use(response => response, async error => {
  const originalRequest = error.config;
  // Xử lý lỗi 401 (Unauthorized)
  if (error.response.status === 401 && !originalRequest._retry) {
    originalRequest._retry = true;
    const authStore = useAuthStore();
    // Đây là nơi bạn có thể thử làm mới token nếu backend hỗ trợ refresh token
    // For now, let's just log out and redirect to login
    authStore.logout();
    router.push({ name: 'Login' });
  }
  return Promise.reject(error);
});

export default apiClient;