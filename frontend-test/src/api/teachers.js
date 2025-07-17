// src/api/teachers.js
import apiClient from './apiClient';

export default {
  getAllTeacher() {
    return apiClient.get('/teachers/'); 
  },
  getTeacherById(id) {
    return apiClient.get(`/teachers/${id}/`); 
  },
  createTeacher(teacherData) {
    return apiClient.post('/teachers/', teacherData);
  },
  updateTeacher(id, teacherData) {
    return apiClient.put(`/teachers/${id}/`, teacherData);
  },
  deleteTeacher(id) {
    return apiClient.delete(`/teachers/${id}/`);
  },
  // Nếu có endpoint export điểm riêng cho app_score:
  // exportScoresToExcel(filters = {}) {
  //   return apiClient.get('/scores/export/', { params: filters, responseType: 'blob' });
  // },
};