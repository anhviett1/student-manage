// src/stores/score.js
import { defineStore } from 'pinia';
import { fetchScores, createScore, updateScore, deleteScore } from '@/services/mockScoreService'; // Tạo mockScoreService

export const useScoreStore = defineStore('score', {
  state: () => ({
    scores: [],
    loading: false,
    error: null,
    selectedScore: null,
  }),
  getters: {
    getScoresByStudentId: (state) => (studentId) => state.scores.filter(s => s.student_id === studentId),
    getScoresByCourseId: (state) => (courseId) => state.scores.filter(s => s.course_id === courseId),
  },
  actions: {
    async loadScores() {
      this.loading = true;
      this.error = null;
      try {
        this.scores = await fetchScores();
      } catch (err) {
        this.error = 'Không thể tải danh sách điểm.';
        console.error('Error loading scores:', err);
      } finally {
        this.loading = false;
      }
    },
    async addScore(scoreData) {
      this.loading = true;
      this.error = null;
      try {
        const newScore = await createScore(scoreData);
        this.scores.push(newScore);
        return true;
      } catch (err) {
        this.error = 'Không thể thêm điểm.';
        console.error('Error adding score:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    async modifyScore(id, scoreData) {
      this.loading = true;
      this.error = null;
      try {
        const updatedScore = await updateScore(id, scoreData);
        const index = this.scores.findIndex(s => s.id === id);
        if (index !== -1) {
          this.scores[index] = updatedScore;
        }
        return true;
      } catch (err) {
        this.error = 'Không thể cập nhật điểm.';
        console.error('Error updating score:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    async removeScore(id) {
      this.loading = true;
      this.error = null;
      try {
        await deleteScore(id);
        this.scores = this.scores.filter(s => s.id !== id);
        return true;
      } catch (err) {
        this.error = 'Không thể xóa điểm.';
        console.error('Error deleting score:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    setSelectedScore(scoreItem) {
      this.selectedScore = scoreItem;
    },
    clearSelectedScore() {
      this.selectedScore = null;
    }
  },
});