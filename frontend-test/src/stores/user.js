// src/stores/user.js
import { defineStore } from 'pinia';
import { fetchUsers, createUser, updateUser, deleteUser } from '@/services/mockUserService'; // Tạo mockUserService

export const useUserStore = defineStore('user', {
  state: () => ({
    users: [],
    loading: false,
    error: null,
    selectedUser: null,
  }),
  getters: {
    getUsers: (state) => state.users,
    getUserById: (state) => (id) => state.users.find(u => u.id === id),
  },
  actions: {
    async loadUsers() {
      this.loading = true;
      this.error = null;
      try {
        this.users = await fetchUsers();
      } catch (err) {
        this.error = 'Không thể tải danh sách người dùng.';
        console.error('Error loading users:', err);
      } finally {
        this.loading = false;
      }
    },
    async addUser(userData) {
      this.loading = true;
      this.error = null;
      try {
        const newUser = await createUser(userData);
        this.users.push(newUser);
        return true;
      } catch (err) {
        this.error = 'Không thể thêm người dùng.';
        console.error('Error adding user:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    async modifyUser(id, userData) {
      this.loading = true;
      this.error = null;
      try {
        const updatedUser = await updateUser(id, userData);
        const index = this.users.findIndex(u => u.id === id);
        if (index !== -1) {
          this.users[index] = updatedUser;
        }
        return true;
      } catch (err) {
        this.error = 'Không thể cập nhật người dùng.';
        console.error('Error updating user:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    async removeUser(id) {
      this.loading = true;
      this.error = null;
      try {
        await deleteUser(id);
        this.users = this.users.filter(u => u.id !== id);
        return true;
      } catch (err) {
        this.error = 'Không thể xóa người dùng.';
        console.error('Error deleting user:', err);
        return false;
      } finally {
        this.loading = false;
      }
    },
    setSelectedUser(userItem) {
      this.selectedUser = userItem;
    },
    clearSelectedUser() {
      this.selectedUser = null;
    }
  },
});