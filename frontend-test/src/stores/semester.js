// src/stores/semester.js
import { defineStore } from 'pinia';
import { fetchSemesters, createSemester, updateSemester, deleteSemester } from '@/services/mockSemesterService'; // Tạo mockSemesterService

export const useSemesterStore = defineStore('semester', {
  state: () => ({
    semesters: [],
    loading: false,
    error: null,
    selectedSemester: null,
  }),
  getters: {
    getSemesters: (state) => state.semesters,
    getSemesterById: (state) => (id) => state.semesters.find(s => s.id === id),
  },
  actions: {
    async loadSemesters() {
      this.loading = true;
      this.error = null;
      try {
        this.semesters = await fetchSemesters();
      } catch (err) {
        this.error = 'Không thể tải danh sách học kỳ.';
        console.error('Error loading semesters:', err);
      } finally {
        this.loading = false;
      }
    },
    async addSemester(semesterData) {
      this.loading = true;
      this.error = null;
      try {
        const newSemester = await createSemester(semesterData);
        this.semesters.push(newSemester);
        return true;
      } catch (err) {
        this.error = 'Không thể thêm học kỳ.';
        console.error('Error adding semester:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    async modifySemester(id, semesterData) {
      this.loading = true;
      this.error = null;
      try {
        const updatedSemester = await updateSemester(id, semesterData);
        const index = this.semesters.findIndex(s => s.id === id);
        if (index !== -1) {
          this.semesters[index] = updatedSemester;
        }
        return true;
      } catch (err) {
        this.error = 'Không thể cập nhật học kỳ.';
        console.error('Error updating semester:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    async removeSemester(id) {
      this.loading = true;
      this.error = null;
      try {
        await deleteSemester(id);
        this.semesters = this.semesters.filter(s => s.id !== id);
        return true;
      } catch (err) {
        this.error = 'Không thể xóa học kỳ.';
        console.error('Error deleting semester:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    setSelectedSemester(semesterItem) {
      this.selectedSemester = semesterItem;
    },
    clearSelectedSemester() {
      this.selectedSemester = null;
    }
  },
});