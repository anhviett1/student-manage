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
  login: '/token/',
  register: '/auth/register/',
  logout: '/auth/logout/',
  refreshToken: '/auth/token/refresh/',

  // Profile
  profile: '/profile/',
  profileDetail: (id) => `/profile/${id}/`,
  profileUpdate: '/profile/update/',
  profileDelete: '/profile/delete/',
  profileChangePassword: '/profile/change-password/',
  
  //Admin
  admin: '/admin/',
  adminDetail: (id) => `/admin/${id}/`,
  adminUpdate: '/admin/update/',
  adminDelete: '/admin/delete/',
  adminChangePassword: '/admin/change-password/',
  
  
  // Account
  account: '/account/',
  accountDetail: (id) => `/account/${id}/`,
  accountUpdate: '/account/update/',
  accountDelete: '/account/delete/',
  accountChangePassword: '/account/change-password/',
  
  // Users
  users: '/users/',
  userProfile: '/users/me/',
  changePassword: '/users/change-password/',

  
  // Students
  students: '/students/',
  studentDetail: (id) => `/students/${id}/`,
  studentUpdate: '/students/update/',
  studentDelete: '/students/delete/',
  studentChangePassword: '/students/change-password/',
  
  //Teachers
  teachers: '/teachers/',
  teacherDetail: (id) => `/teachers/${id}/`,
  teacherUpdate: '/teachers/update/',
  teacherDelete: '/teachers/delete/',
  teacherChangePassword: '/teachers/change-password/',
  
  // Courses
  courses: '/courses/',
  courseDetail: (id) => `/courses/${id}/`,
  courseUpdate: '/courses/update/',
  courseDelete: '/courses/delete/',
  courseChangePassword: '/courses/change-password/',
  
  // Classes
  classes: '/classes/',
  classDetail: (id) => `/classes/${id}/`,
  classUpdate: '/classes/update/',
  classDelete: '/classes/delete/',
  classChangePassword: '/classes/change-password/',
  
  // Enrollments
  enrollments: '/enrollments/',
  enrollmentDetail: (id) => `/enrollments/${id}/`,
  enrollmentUpdate: '/enrollments/update/',
  enrollmentDelete: '/enrollments/delete/',
  enrollmentChangePassword: '/enrollments/change-password/',
  
  //Home
  home: '/home/',
  homeDetail: (id) => `/home/${id}/`,

}

export default api 