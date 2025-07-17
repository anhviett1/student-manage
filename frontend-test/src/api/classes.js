// src/api/classes.js
import apiClient from './apiClient';

export default {
  getAllClass() {
    return apiClient.get('/classes/'); 
  },
  getClassById(id) {
    return apiClient.get(`/classes/${id}/`); 
  },
  createClass(classData) {
    return apiClient.post('/classes/', classData);
  },
  updateClass(id, classData) {
    return apiClient.put(`/classes/${id}/`, classData);
  },
  deleteClass(id) {
    return apiClient.delete(`/classes/${id}/`);
  },
  // Nếu có endpoint export điểm riêng cho app_score:
  // exportScoresToExcel(filters = {}) {
  //   return apiClient.get('/scores/export/', { params: filters, responseType: 'blob' });
  // },
};