
import apiClient from './apiClient';

export default {
  getAllDepartment() {
    return apiClient.get('/departments/'); 
  },
  getDepartmentById(id) {
    return apiClient.get(`/departments/${id}/`); 
  },
  createDepartment(departmentData) {
    return apiClient.post('/departments/', departmentData);
  },
  updateDepartment(id, departmentData) {
    return apiClient.put(`/departments/${id}/`, departmentData);
  },
  deleteDepartment(id) {
    return apiClient.delete(`/departments/${id}/`);
  },
  // Nếu có endpoint export điểm riêng cho app_score:
  // exportScoresToExcel(filters = {}) {
  //   return apiClient.get('/scores/export/', { params: filters, responseType: 'blob' });
  // },
};