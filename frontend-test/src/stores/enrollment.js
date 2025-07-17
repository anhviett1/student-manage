// src/stores/enrollment.js
import { defineStore } from 'pinia';
import { fetchEnrollments, createEnrollment, deleteEnrollment } from '@/services/mockEnrollmentService'; // Tạo mockEnrollmentService

export const useEnrollmentStore = defineStore('enrollment', {
  state: () => ({
    enrollments: [],
    loading: false,
    error: null,
  }),
  getters: {
    getEnrollmentsByStudentId: (state) => (studentId) => state.enrollments.filter(e => e.student_id === studentId),
    getEnrollmentsByCourseId: (state) => (courseId) => state.enrollments.filter(e => e.course_id === courseId),
  },
  actions: {
    async loadEnrollments() {
      this.loading = true;
      this.error = null;
      try {
        this.enrollments = await fetchEnrollments();
      } catch (err) {
        this.error = 'Không thể tải danh sách đăng ký môn học.';
        console.error('Error loading enrollments:', err);
      } finally {
        this.loading = false;
      }
    },
    async addEnrollment(enrollmentData) {
      this.loading = true;
      this.error = null;
      try {
        const newEnrollment = await createEnrollment(enrollmentData);
        this.enrollments.push(newEnrollment);
        return true;
      } catch (err) {
        this.error = 'Không thể thêm đăng ký môn học.';
        console.error('Error adding enrollment:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    async removeEnrollment(id) {
      this.loading = true;
      this.error = null;
      try {
        await deleteEnrollment(id);
        this.enrollments = this.enrollments.filter(e => e.id !== id);
        return true;
      } catch (err) {
        this.error = 'Không thể hủy đăng ký môn học.';
        console.error('Error deleting enrollment:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
  },
});