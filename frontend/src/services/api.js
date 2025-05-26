const API_URL = '/api'

const handleResponse = async (response) => {
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.message || 'Something went wrong')
  }
  return response.json()
}

const getHeaders = () => {
  const token = localStorage.getItem('token')
  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {})
  }
}

export const api = {
  // Auth
  login: async (credentials) => {
    const response = await fetch(`${API_URL}/auth/login/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(credentials)
    })
    return handleResponse(response)
  },

  // Students
  getStudents: async () => {
    const response = await fetch(`${API_URL}/students/`, {
      headers: getHeaders()
    })
    return handleResponse(response)
  },

  createStudent: async (data) => {
    const response = await fetch(`${API_URL}/students/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(data)
    })
    return handleResponse(response)
  },

  updateStudent: async (id, data) => {
    const response = await fetch(`${API_URL}/students/${id}/`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(data)
    })
    return handleResponse(response)
  },

  deleteStudent: async (id) => {
    const response = await fetch(`${API_URL}/students/${id}/`, {
      method: 'DELETE',
      headers: getHeaders()
    })
    return handleResponse(response)
  },

  // Teachers
  getTeachers: async () => {
    const response = await fetch(`${API_URL}/teachers/`, {
      headers: getHeaders()
    })
    return handleResponse(response)
  },

  createTeacher: async (data) => {
    const response = await fetch(`${API_URL}/teachers/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(data)
    })
    return handleResponse(response)
  },

  updateTeacher: async (id, data) => {
    const response = await fetch(`${API_URL}/teachers/${id}/`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(data)
    })
    return handleResponse(response)
  },

  deleteTeacher: async (id) => {
    const response = await fetch(`${API_URL}/teachers/${id}/`, {
      method: 'DELETE',
      headers: getHeaders()
    })
    return handleResponse(response)
  },

  // Classes
  getClasses: async () => {
    const response = await fetch(`${API_URL}/classes/`, {
      headers: getHeaders()
    })
    return handleResponse(response)
  },

  createClass: async (data) => {
    const response = await fetch(`${API_URL}/classes/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(data)
    })
    return handleResponse(response)
  },

  updateClass: async (id, data) => {
    const response = await fetch(`${API_URL}/classes/${id}/`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(data)
    })
    return handleResponse(response)
  },

  deleteClass: async (id) => {
    const response = await fetch(`${API_URL}/classes/${id}/`, {
      method: 'DELETE',
      headers: getHeaders()
    })
    return handleResponse(response)
  },

  // Subjects
  getSubjects: async () => {
    const response = await fetch(`${API_URL}/subjects/`, {
      headers: getHeaders()
    })
    return handleResponse(response)
  },

  createSubject: async (data) => {
    const response = await fetch(`${API_URL}/subjects/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(data)
    })
    return handleResponse(response)
  },

  updateSubject: async (id, data) => {
    const response = await fetch(`${API_URL}/subjects/${id}/`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(data)
    })
    return handleResponse(response)
  },

  deleteSubject: async (id) => {
    const response = await fetch(`${API_URL}/subjects/${id}/`, {
      method: 'DELETE',
      headers: getHeaders()
    })
    return handleResponse(response)
  },

  // Enrollments
  getEnrollments: async () => {
    const response = await fetch(`${API_URL}/enrollments/`, {
      headers: getHeaders()
    })
    return handleResponse(response)
  },

  createEnrollment: async (data) => {
    const response = await fetch(`${API_URL}/enrollments/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(data)
    })
    return handleResponse(response)
  },

  updateEnrollment: async (id, data) => {
    const response = await fetch(`${API_URL}/enrollments/${id}/`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(data)
    })
    return handleResponse(response)
  },

  deleteEnrollment: async (id) => {
    const response = await fetch(`${API_URL}/enrollments/${id}/`, {
      method: 'DELETE',
      headers: getHeaders()
    })
    return handleResponse(response)
  },

  // Semesters
  getSemesters: async () => {
    const response = await fetch(`${API_URL}/semesters/`, {
      headers: getHeaders()
    })
    return handleResponse(response)
  },

  createSemester: async (data) => {
    const response = await fetch(`${API_URL}/semesters/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(data)
    })
    return handleResponse(response)
  },

  updateSemester: async (id, data) => {
    const response = await fetch(`${API_URL}/semesters/${id}/`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(data)
    })
    return handleResponse(response)
  },

  deleteSemester: async (id) => {
    const response = await fetch(`${API_URL}/semesters/${id}/`, {
      method: 'DELETE',
      headers: getHeaders()
    })
    return handleResponse(response)
  },

  // Scores
  getScores: async () => {
    const response = await fetch(`${API_URL}/scores/`, {
      headers: getHeaders()
    })
    return handleResponse(response)
  },

  getMyScores: async () => {
    const response = await fetch(`${API_URL}/scores/my-scores/`, {
      headers: getHeaders()
    })
    return handleResponse(response)
  },

  createScore: async (data) => {
    const response = await fetch(`${API_URL}/scores/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(data)
    })
    return handleResponse(response)
  },

  updateScore: async (id, data) => {
    const response = await fetch(`${API_URL}/scores/${id}/`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(data)
    })
    return handleResponse(response)
  },

  deleteScore: async (id) => {
    const response = await fetch(`${API_URL}/scores/${id}/`, {
      method: 'DELETE',
      headers: getHeaders()
    })
    return handleResponse(response)
  },

  // Profile
  getProfile: async () => {
    const response = await fetch(`${API_URL}/profile/`, {
      headers: getHeaders()
    })
    return handleResponse(response)
  },

  updateProfile: async (data) => {
    const response = await fetch(`${API_URL}/profile/`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(data)
    })
    return handleResponse(response)
  },

  uploadAvatar: async (formData) => {
    const token = localStorage.getItem('token')
    const response = await fetch(`${API_URL}/profile/avatar/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    })
    return handleResponse(response)
  },

  // Change Password
  changePassword: async (passwords) => {
    const response = await fetch(`${API_URL}/change-password/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(passwords)
    })
    return handleResponse(response)
  }
} 