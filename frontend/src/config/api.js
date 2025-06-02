import axios from 'axios'

// Tạo instance axios với cấu hình mặc định
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// Thêm interceptor để xử lý token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Thêm interceptor để xử lý response
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token hết hạn hoặc không hợp lệ
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API endpoints
export const endpoints = {
  // Auth
  login: '/auth/login/',
  register: '/auth/register/',
  logout: '/auth/logout/',
  refreshToken: '/auth/token/refresh/',
  
  // Users
  users: '/users/',
  userProfile: '/users/me/',
  changePassword: '/users/change-password/',
  
  // Students
  students: '/students/',
  studentDetail: (id) => `/students/${id}/`,
  
  // Courses
  courses: '/courses/',
  courseDetail: (id) => `/courses/${id}/`,
  
  // Classes
  classes: '/classes/',
  classDetail: (id) => `/classes/${id}/`,
  
  // Enrollments
  enrollments: '/enrollments/',
  enrollmentDetail: (id) => `/enrollments/${id}/`,
}

export default api 