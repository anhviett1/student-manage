// src/api/scores.js
import apiClient from './apiClient';

export default {
  getAllScores() {
    return apiClient.get('/scores/'); // url: /api/v1/scores/
  },
  getScoreById(id) {
    return apiClient.get(`/scores/${id}/`); // url: /api/v1/scores/{id}/
  },
  createScore(scoreData) {
    return apiClient.post('/scores/', scoreData);
  },
  updateScore(id, scoreData) {
    return apiClient.put(`/scores/${id}/`, scoreData);
  },
  deleteScore(id) {
    return apiClient.delete(`/scores/${id}/`);
  },
  // Nếu có endpoint export điểm riêng cho app_score:
  // exportScoresToExcel(filters = {}) {
  //   return apiClient.get('/scores/export/', { params: filters, responseType: 'blob' });
  // },
};