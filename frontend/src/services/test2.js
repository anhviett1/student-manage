import axios from 'axios'

// Create axios instance with default config
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add request interceptor to add auth token
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

// Add response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // Handle 401 Unauthorized error
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        // Try to refresh token
        const refreshToken = localStorage.getItem('refresh_token')
        if (!refreshToken) {
          throw new Error('No refresh token available')
        }

        const response = await axios.post('/api/v1/token/refresh/', {
          refresh: refreshToken,
        })

        const { access } = response.data
        localStorage.setItem('token', access)
        api.defaults.headers.common['Authorization'] = `Bearer ${access}`

        // Retry the original request
        originalRequest.headers.Authorization = `Bearer ${access}`
        return api(originalRequest)
      } catch (refreshError) {
        // If refresh token fails, logout user
        localStorage.removeItem('token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

// API endpoints
export const endpoints = {
  // Auth endpoints
  auth: {
    login: '/api/v1/users/auth/login/',
    logout: '/api/v1/users/auth/logout/',
    register: '/api/v1/users/auth/register/',
    role: '/api/v1/users/auth/role/',
    profile: '/api/v1/users/auth/profile/',
    changePassword: '/api/v1/users/auth/change-password/',
    avatar: '/api/v1/users/auth/avatar/',
  },

  // User endpoints
  users: {
    list: '/api/v1/users/',
    detail: (id) => `/api/v1/users/${id}/`,
    me: '/api/v1/users/me/',
  },

  // Student endpoints
  students: {
    list: '/api/v1/students/',
    detail: (id) => `/api/v1/students/${id}/`,
    me: '/api/v1/students/me/',
  },

  // Teacher endpoints
  teachers: {
    list: '/api/v1/teachers/',
    detail: (id) => `/api/v1/teachers/${id}/`,
    me: '/api/v1/teachers/me/',
  },

  // Class endpoints
  classes: {
    list: '/api/v1/classes/',
    detail: (id) => `/api/v1/classes/${id}/`,
  },

  // Subject endpoints
  subjects: {
    list: '/api/v1/subjects/',
    detail: (id) => `/api/v1/subjects/${id}/`,
  },

  // Score endpoints
  scores: {
    list: '/api/v1/scores/',
    detail: (id) => `/api/v1/scores/${id}/`,
    upload: '/api/v1/scores/upload/',
  },

  // Enrollment endpoints
  enrollments: {
    list: '/api/v1/enrollments/',
    detail: (id) => `/api/v1/enrollments/${id}/`,
  },

  // Activity endpoints
  activities: {
    list: '/api/v1/activities/',
    detail: (id) => `/api/v1/activities/${id}/`,
  },

  // Semester endpoints
  semesters: {
    list: '/api/v1/semesters/',
    detail: (id) => `/api/v1/semesters/${id}/`,
  },

  // Department endpoints
  departments: {
    list: '/api/v1/departments/',
    detail: (id) => `/api/v1/departments/${id}/`,
  },
}

export default api