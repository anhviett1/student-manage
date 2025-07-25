import axios from 'axios'

// Base URL từ biến môi trường hoặc mặc định localhost
const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
// Tiền tố cho tất cả API REST, trừ Django Admin
const API_PREFIX = '/api/v1'

// Cấu hình instance axios
const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
  timeout: 15000, 
  withCredentials: true, 
  })

export const endpoints = {
  login: `${API_PREFIX}/token/`,
  logout: `${API_PREFIX}/users/logout/`,
  refreshToken: `${API_PREFIX}/token/refresh/`,
  users: `${API_PREFIX}/users/users/`,
  userProfile: `${API_PREFIX}/users/profile/`,
  changePassword: `${API_PREFIX}/users/change-password/`,
  uploadAvatar: `${API_PREFIX}/users/avatar/`,
  students: `${API_PREFIX}/students/`,
  studentsExport: `${API_PREFIX}/students/export/`,
  studentProfile: `${API_PREFIX}/students/me/`,
  teachers: `${API_PREFIX}/teachers/`,
  teachersExport: `${API_PREFIX}/teachers/export/`,
  teacherProfile: `${API_PREFIX}/teachers/me/`,
  classes: `${API_PREFIX}/classes/`,
  classesExport: `${API_PREFIX}/classes/export/`,
  subjects: `${API_PREFIX}/subjects/`,
  subjectsExport: `${API_PREFIX}/subjects/export/`,
  enrollments: `${API_PREFIX}/enrollments/`,
  enrollmentsExport: `${API_PREFIX}/enrollments/export/`,
  semesters: `${API_PREFIX}/semesters/`,
  semestersExport: `${API_PREFIX}/semesters/export/`,
  scores: `${API_PREFIX}/scores/`,
  scoreExport: `${API_PREFIX}/scores/export/`,
  departments: `${API_PREFIX}/departments/`,
  departmentsExport: `${API_PREFIX}/departments/export/`,
  schedules: `${API_PREFIX}/schedules/`,
  schedulesExport: `${API_PREFIX}/schedules/export/`,
  activities: `${API_PREFIX}/activities/`,
  activitiesExport: `${API_PREFIX}/activities/export/`,
  djangoAdmin: '/admin/',
};

// Interceptor cho request: Thêm token vào header, trừ endpoint Django Admin
api.interceptors.request.use(
  (config) => {
    // Không thêm Authorization cho Django Admin
    if (config.url === endpoints.djangoAdmin) {
      return config
    }

    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    // Đảm bảo Content-Type phù hợp cho FormData
    if (config.data instanceof FormData) {
      config.headers['Content-Type'] = 'multipart/form-data'
    }

    return config
  },
  (error) => Promise.reject(error)
)

// Interceptor cho response: Xử lý lỗi 401 và làm mới token
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // Bỏ qua refresh token cho Django Admin và các request đã retry
    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      originalRequest.url !== endpoints.djangoAdmin
    ) {
      originalRequest._retry = true
      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (!refreshToken) {
          throw new Error('No refresh token available')
        }

        // Gọi API refresh token
        const response = await axios.post(`${BASE_URL}${endpoints.refreshToken}`, {
          refresh: refreshToken,
        })

        const { access, refresh } = response.data
        localStorage.setItem('access_token', access)
        if (refresh) {
          localStorage.setItem('refresh_token', refresh)
        }

        // Cập nhật header Authorization
        api.defaults.headers.Authorization = `Bearer ${access}`
        originalRequest.headers.Authorization = `Bearer ${access}`

        // Thử lại request gốc
        return api(originalRequest)
      } catch (refreshError) {
        // Xóa token và chuyển hướng về login nếu refresh thất bại
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        delete api.defaults.headers.Authorization
        if (!window.location.pathname.includes('/login')) {
          window.location.href = '/login'
        }
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default api