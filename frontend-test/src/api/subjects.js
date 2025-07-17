
import apiClient from './apiClient';

export default {
  getAllSubject() {
    return apiClient.get('/subjects/'); 
  },
  getSubjectById(id) {
    return apiClient.get(`/subjects/${id}/`); 
  },
  createSubject(subjectData) {
    return apiClient.post('/subjects/', subjectData);
  },
  updateSubject(id, subjectData) {
    return apiClient.put(`/subjects/${id}/`, subjectData);
  },
  deleteSubject(id) {
    return apiClient.delete(`/subjects/${id}/`);
  },
  // Nếu có endpoint export điểm riêng cho app_score:
  // exportScoresToExcel(filters = {}) {
  //   return apiClient.get('/scores/export/', { params: filters, responseType: 'blob' });
  // },
};