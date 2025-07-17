// src/stores/teacher.js
import { defineStore } from 'pinia';
import { fetchTeachers, createTeacher, updateTeacher, deleteTeacher } from '@/services/mockTeacherServiceAdmin'; // Tạo mockTeacherServiceAdmin

export const useTeacherStore = defineStore('teacher', {
  state: () => ({
    teachers: [],
    loading: false,
    error: null,
    selectedTeacher: null,
  }),
  getters: {
    getTeachers: (state) => state.teachers,
    getTeacherById: (state) => (id) => state.teachers.find(t => t.id === id),
  },
  actions: {
    async loadTeachers() {
      this.loading = true;
      this.error = null;
      try {
        this.teachers = await fetchTeachers();
      } catch (err) {
        this.error = 'Không thể tải danh sách giáo viên.';
        console.error('Error loading teachers:', err);
      } finally {
        this.loading = false;
      }
    },
    async addTeacher(teacherData) {
      this.loading = true;
      this.error = null;
      try {
        const newTeacher = await createTeacher(teacherData);
        this.teachers.push(newTeacher);
        return true;
      } catch (err) {
        this.error = 'Không thể thêm giáo viên.';
        console.error('Error adding teacher:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    async modifyTeacher(id, teacherData) {
      this.loading = true;
      this.error = null;
      try {
        const updatedTeacher = await updateTeacher(id, teacherData);
        const index = this.teachers.findIndex(t => t.id === id);
        if (index !== -1) {
          this.teachers[index] = updatedTeacher;
        }
        return true;
      } catch (err) {
        this.error = 'Không thể cập nhật giáo viên.';
        console.error('Error updating teacher:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    async removeTeacher(id) {
      this.loading = true;
      this.error = null;
      try {
        await deleteTeacher(id);
        this.teachers = this.teachers.filter(t => t.id !== id);
        return true;
      } catch (err) {
        this.error = 'Không thể xóa giáo viên.';
        console.error('Error deleting teacher:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    setSelectedTeacher(teacherItem) {
      this.selectedTeacher = teacherItem;
    },
    clearSelectedTeacher() {
      this.selectedTeacher = null;
    }
  },
});