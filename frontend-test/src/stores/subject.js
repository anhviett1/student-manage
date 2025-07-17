// src/stores/subject.js
import { defineStore } from 'pinia';
import { fetchSubjects, createSubject, updateSubject, deleteSubject } from '@/services/mockSubjectService'; // Tạo mockSubjectService

export const useSubjectStore = defineStore('subject', {
  state: () => ({
    subjects: [],
    loading: false,
    error: null,
    selectedSubject: null,
  }),
  getters: {
    getSubjects: (state) => state.subjects,
    getSubjectById: (state) => (id) => state.subjects.find(s => s.id === id),
  },
  actions: {
    async loadSubjects() {
      this.loading = true;
      this.error = null;
      try {
        this.subjects = await fetchSubjects();
      } catch (err) {
        this.error = 'Không thể tải danh sách môn học.';
        console.error('Error loading subjects:', err);
      } finally {
        this.loading = false;
      }
    },
    async addSubject(subjectData) {
      this.loading = true;
      this.error = null;
      try {
        const newSubject = await createSubject(subjectData);
        this.subjects.push(newSubject);
        return true;
      } catch (err) {
        this.error = 'Không thể thêm môn học.';
        console.error('Error adding subject:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    async modifySubject(id, subjectData) {
      this.loading = true;
      this.error = null;
      try {
        const updatedSubject = await updateSubject(id, subjectData);
        const index = this.subjects.findIndex(s => s.id === id);
        if (index !== -1) {
          this.subjects[index] = updatedSubject;
        }
        return true;
      } catch (err) {
        this.error = 'Không thể cập nhật môn học.';
        console.error('Error updating subject:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    async removeSubject(id) {
      this.loading = true;
      this.error = null;
      try {
        await deleteSubject(id);
        this.subjects = this.subjects.filter(s => s.id !== id);
        return true;
      } catch (err) {
        this.error = 'Không thể xóa môn học.';
        console.error('Error deleting subject:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    setSelectedSubject(subjectItem) {
      this.selectedSubject = subjectItem;
    },
    clearSelectedSubject() {
      this.selectedSubject = null;
    }
  },
});