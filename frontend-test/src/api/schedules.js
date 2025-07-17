
import apiClient from './apiClient';

export default {
  getAllSchedule() {
    return apiClient.get('/schedules/'); 
  },
  getScheduleById(id) {
    return apiClient.get(`/schedules/${id}/`); 
  },
  createSchedule(scheduleData) {
    return apiClient.post('/schedules/', scheduleData);
  },
  updateSchedule(id, scheduleData) {
    return apiClient.put(`/schedules/${id}/`, scheduleData);
  },
  deleteSchedule(id) {
    return apiClient.delete(`/schedules/${id}/`);
  },
  // Nếu có endpoint export điểm riêng cho app_score:
  // exportScoresToExcel(filters = {}) {
  //   return apiClient.get('/scores/export/', { params: filters, responseType: 'blob' });
  // },
};