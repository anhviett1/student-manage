// src/stores/schedule.js
import { defineStore } from 'pinia';
import { fetchScheduleByStudentId, fetchScheduleByTeacherId, createSchedule, updateSchedule, deleteSchedule } from '@/services/mockScheduleService'; // Tạo mockScheduleService

export const useScheduleStore = defineStore('schedule', {
  state: () => ({
    schedules: [],
    loading: false,
    error: null,
  }),
  getters: {
    getStudentSchedule: (state) => (studentId) => state.schedules.filter(s => s.student_id === studentId),
    getTeacherSchedule: (state) => (teacherId) => state.schedules.filter(s => s.teacher_id === teacherId),
  },
  actions: {
    async loadStudentSchedule(studentId) {
      this.loading = true;
      this.error = null;
      try {
        this.schedules = await fetchScheduleByStudentId(studentId);
      } catch (err) {
        this.error = 'Không thể tải lịch học của sinh viên.';
        console.error('Error loading student schedule:', err);
      } finally {
        this.loading = false;
      }
    },
    async loadTeacherSchedule(teacherId) {
      this.loading = true;
      this.error = null;
      try {
        this.schedules = await fetchScheduleByTeacherId(teacherId);
      } catch (err) {
        this.error = 'Không thể tải lịch dạy của giáo viên.';
        console.error('Error loading teacher schedule:', err);
      } finally {
        this.loading = false;
      }
    },
    async addSchedule(scheduleData) {
      this.loading = true;
      this.error = null;
      try {
        const newSchedule = await createSchedule(scheduleData);
        this.schedules.push(newSchedule);
        return true;
      } catch (err) {
        this.error = 'Không thể thêm lịch.';
        console.error('Error adding schedule:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    async modifySchedule(id, scheduleData) {
      this.loading = true;
      this.error = null;
      try {
        const updatedSchedule = await updateSchedule(id, scheduleData);
        const index = this.schedules.findIndex(s => s.id === id);
        if (index !== -1) {
          this.schedules[index] = updatedSchedule;
        }
        return true;
      } catch (err) {
        this.error = 'Không thể cập nhật lịch.';
        console.error('Error updating schedule:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    async removeSchedule(id) {
      this.loading = true;
      this.error = null;
      try {
        await deleteSchedule(id);
        this.schedules = this.schedules.filter(s => s.id !== id);
        return true;
      } catch (err) {
        this.error = 'Không thể xóa lịch.';
        console.error('Error deleting schedule:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
  },
});