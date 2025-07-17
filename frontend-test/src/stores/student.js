// src/stores/student.js
import { defineStore } from 'pinia';
import { fetchStudents, createStudent, updateStudent, deleteStudent } from '@/services/mockStudentServiceAdmin'; // Tạo mockStudentServiceAdmin

export const useStudentStore = defineStore('student', {
  state: () => ({
    students: [],
    loading: false,
    error: null,
    selectedStudent: null,
  }),
  getters: {
    getStudents: (state) => state.students,
    getStudentById: (state) => (id) => state.students.find(s => s.id === id),
  },
  actions: {
    async loadStudents() {
      this.loading = true;
      this.error = null;
      try {
        this.students = await fetchStudents();
      } catch (err) {
        this.error = 'Không thể tải danh sách sinh viên.';
        console.error('Error loading students:', err);
      } finally {
        this.loading = false;
      }
    },
    async addStudent(studentData) {
      this.loading = true;
      this.error = null;
      try {
        const newStudent = await createStudent(studentData);
        this.students.push(newStudent);
        return true;
      } catch (err) {
        this.error = 'Không thể thêm sinh viên.';
        console.error('Error adding student:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    async modifyStudent(id, studentData) {
      this.loading = true;
      this.error = null;
      try {
        const updatedStudent = await updateStudent(id, studentData);
        const index = this.students.findIndex(s => s.id === id);
        if (index !== -1) {
          this.students[index] = updatedStudent;
        }
        return true;
      } catch (err) {
        this.error = 'Không thể cập nhật sinh viên.';
        console.error('Error updating student:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    async removeStudent(id) {
      this.loading = true;
      this.error = null;
      try {
        await deleteStudent(id);
        this.students = this.students.filter(s => s.id !== id);
        return true;
      } catch (err) {
        this.error = 'Không thể xóa sinh viên.';
        console.error('Error deleting student:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    setSelectedStudent(studentItem) {
      this.selectedStudent = studentItem;
    },
    clearSelectedStudent() {
      this.selectedStudent = null;
    }
  },
});