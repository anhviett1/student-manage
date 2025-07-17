
import apiClient from './apiClient';

export default {
  getAllSemester() {
    return apiClient.get('/semesters/'); 
  },
  getSemesterById(id) {
    return apiClient.get(`/semesters/${id}/`); 
  },
  createSemester(semesterData) {
    return apiClient.post('/semesters/', semesterData);
  },
  updateSemester(id, semesterData) {
    return apiClient.put(`/semesters/${id}/`, semesterData);
  },
  deleteSemester(id) {
    return apiClient.delete(`/semesters/${id}/`);
  },
  // Nếu có endpoint export điểm riêng cho app_score:
  // exportScoresToExcel(filters = {}) {
  //   return apiClient.get('/scores/export/', { params: filters, responseType: 'blob' });
  // },
};