// src/api/students.js
import apiClient from './apiClient';

export default {
  getAllStudent() {
    return apiClient.get('/students/'); // url: /api/v1/students/
  },
  getStudentById(id) {
    return apiClient.get(`/students/${id}/`); // url: /api/v1/students/{id}/
  },
  createStudent(studentData) {
    return apiClient.post('/students/', studentData);
  },
  updateStudent(id, studentData) {
    return apiClient.put(`/students/${id}/`, studentData);
  },
  deleteStudent(id) {
    return apiClient.delete(`/students/${id}/`);
  },
  // Ví dụ xuất sinh viên riêng nếu có endpoint khác
  // exportStudentsData(filters = {}) {
  //   return apiClient.get('/students/export/', { params: filters, responseType: 'blob' });
  // },
};