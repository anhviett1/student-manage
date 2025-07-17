// src/stores/class.js
import { defineStore } from 'pinia';
import { fetchClasses, createClass, updateClass, deleteClass } from '@/services/mockClassService'; // Tạo mockClassService

export const useClassStore = defineStore('class', {
  state: () => ({
    classes: [],
    loading: false,
    error: null,
    selectedClass: null,
  }),
  getters: {
    getClasses: (state) => state.classes,
    getClassById: (state) => (id) => state.classes.find(c => c.id === id),
  },
  actions: {
    async loadClasses() {
      this.loading = true;
      this.error = null;
      try {
        this.classes = await fetchClasses();
      } catch (err) {
        this.error = 'Không thể tải danh sách lớp học.';
        console.error('Error loading classes:', err);
      } finally {
        this.loading = false;
      }
    },
    async addClass(classData) {
      this.loading = true;
      this.error = null;
      try {
        const newClass = await createClass(classData);
        this.classes.push(newClass);
        return true;
      } catch (err) {
        this.error = 'Không thể thêm lớp học.';
        console.error('Error adding class:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    async modifyClass(id, classData) {
      this.loading = true;
      this.error = null;
      try {
        const updatedClass = await updateClass(id, classData);
        const index = this.classes.findIndex(c => c.id === id);
        if (index !== -1) {
          this.classes[index] = updatedClass;
        }
        return true;
      } catch (err) {
        this.error = 'Không thể cập nhật lớp học.';
        console.error('Error updating class:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    async removeClass(id) {
      this.loading = true;
      this.error = null;
      try {
        await deleteClass(id);
        this.classes = this.classes.filter(c => c.id !== id);
        return true;
      } catch (err) {
        this.error = 'Không thể xóa lớp học.';
        console.error('Error deleting class:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    setSelectedClass(classItem) {
      this.selectedClass = classItem;
    },
    clearSelectedClass() {
      this.selectedClass = null;
    }
  },
});