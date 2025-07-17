
import apiClient from './apiClient';

export default {
  getAllEnrollment() {
    return apiClient.get('/enrollments/'); 
  },
  getEnrollmentById(id) {
    return apiClient.get(`/enrollments/${id}/`); 
  },
  createEnrollment(enrollmentData) {
    return apiClient.post('/enrollments/', enrollmentData);
  },
  updateEnrollment(id, enrollmentData) {
    return apiClient.put(`/enrollments/${id}/`, enrollmentData);
  },
  deleteEnrollment(id) {
    return apiClient.delete(`/enrollments/${id}/`);
  },
  // Nếu có endpoint export điểm riêng cho app_score:
  // exportScoresToExcel(filters = {}) {
  //   return apiClient.get('/scores/export/', { params: filters, responseType: 'blob' });
  // },
};