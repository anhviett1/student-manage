// src/stores/department.js
import { defineStore } from 'pinia';
import { fetchDepartments, createDepartment, updateDepartment, deleteDepartment } from '@/services/mockDepartmentService'; // Tạo mockDepartmentService

export const useDepartmentStore = defineStore('department', {
  state: () => ({
    departments: [],
    loading: false,
    error: null,
    selectedDepartment: null,
  }),
  getters: {
    getDepartments: (state) => state.departments,
    getDepartmentById: (state) => (id) => state.departments.find(d => d.id === id),
  },
  actions: {
    async loadDepartments() {
      this.loading = true;
      this.error = null;
      try {
        this.departments = await fetchDepartments();
      } catch (err) {
        this.error = 'Không thể tải danh sách khoa/bộ môn.';
        console.error('Error loading departments:', err);
      } finally {
        this.loading = false;
      }
    },
    async addDepartment(departmentData) {
      this.loading = true;
      this.error = null;
      try {
        const newDepartment = await createDepartment(departmentData);
        this.departments.push(newDepartment);
        return true;
      } catch (err) {
        this.error = 'Không thể thêm khoa/bộ môn.';
        console.error('Error adding department:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    async modifyDepartment(id, departmentData) {
      this.loading = true;
      this.error = null;
      try {
        const updatedDepartment = await updateDepartment(id, departmentData);
        const index = this.departments.findIndex(d => d.id === id);
        if (index !== -1) {
          this.departments[index] = updatedDepartment;
        }
        return true;
      } catch (err) {
        this.error = 'Không thể cập nhật khoa/bộ môn.';
        console.error('Error updating department:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    async removeDepartment(id) {
      this.loading = true;
      this.error = null;
      try {
        await deleteDepartment(id);
        this.departments = this.departments.filter(d => d.id !== id);
        return true;
      } catch (err) {
        this.error = 'Không thể xóa khoa/bộ môn.';
        console.error('Error deleting department:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    setSelectedDepartment(departmentItem) {
      this.selectedDepartment = departmentItem;
    },
    clearSelectedDepartment() {
      this.selectedDepartment = null;
    }
  },
});