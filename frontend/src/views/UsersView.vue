<template>
  <div class="users-view">
    <div class="header">
      <h1 @click="navigateToHome">User Management</h1>
      <button @click="openCreateModal" class="btn-primary">
        <i class="fas fa-plus"></i> Add User
      </button>
    </div>

    <div class="filters">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search users..."
        class="search-input"
      />
      <select v-model="roleFilter" class="role-select">
        <option value="">All Roles</option>
        <option value="admin">Admin</option>
        <option value="teacher">Teacher</option>
        <option value="student">Student</option>
      </select>
    </div>

    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Email</th>
            <th>Role</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>
              <span :class="['role-badge', user.role]">
                {{ user.role }}
              </span>
            </td>
            <td>
              <span :class="['status-badge', user.is_active ? 'active' : 'inactive']">
                {{ user.is_active ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td class="actions">
              <button @click="editUser(user)" class="btn-icon">
                <i class="fas fa-edit"></i>
              </button>
              <button @click="deleteUser(user)" class="btn-icon danger">
                <i class="fas fa-trash"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h2>{{ isEditing ? 'Edit User' : 'Create User' }}</h2>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>Username</label>
            <input v-model="form.username" type="text" required />
          </div>
          <div class="form-group">
            <label>Email</label>
            <input v-model="form.email" type="email" required />
          </div>
          <div class="form-group">
            <label>Role</label>
            <select v-model="form.role" required>
              <option value="admin">Admin</option>
              <option value="teacher">Teacher</option>
              <option value="student">Student</option>
            </select>
          </div>
          <div class="form-group">
            <label>Password</label>
            <input v-model="form.password" type="password" :required="!isEditing" />
          </div>
          <div class="form-group">
            <label>Status</label>
            <select v-model="form.is_active">
              <option :value="true">Active</option>
              <option :value="false">Inactive</option>
            </select>
          </div>
          <div class="modal-actions">
            <button type="button" @click="closeModal" class="btn-secondary">
              Cancel
            </button>
            <button type="submit" class="btn-primary">
              {{ isEditing ? 'Update' : 'Create' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useToast } from '@/composables/useToast'

const userStore = useUserStore()
const { showToast } = useToast()

const users = ref([])
const searchQuery = ref('')
const roleFilter = ref('')
const showModal = ref(false)
const isEditing = ref(false)
const form = ref({
  username: '',
  email: '',
  role: 'student',
  password: '',
  is_active: true
})

const navigateToHome = () => {
  router.push('/')
}

const filteredUsers = computed(() => {
  return users.value.filter(user => {
    const matchesSearch = user.username.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         user.email.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesRole = !roleFilter.value || user.role === roleFilter.value
    return matchesSearch && matchesRole
  })
})

onMounted(async () => {
  await loadUsers()
})

const loadUsers = async () => {
  try {
    users.value = await userStore.fetchUsers()
  } catch (error) {
    showToast('Error loading users', 'error')
  }
}

const openCreateModal = () => {
  isEditing.value = false
  form.value = {
    username: '',
    email: '',
    role: 'student',
    password: '',
    is_active: true
  }
  showModal.value = true
}

const editUser = (user) => {
  isEditing.value = true
  form.value = { ...user, password: '' }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  form.value = {
    username: '',
    email: '',
    role: 'student',
    password: '',
    is_active: true
  }
}

const handleSubmit = async () => {
  try {
    if (isEditing.value) {
      await userStore.updateUser(form.value.id, form.value)
      showToast('User updated successfully', 'success')
    } else {
      await userStore.createUser(form.value)
      showToast('User created successfully', 'success')
    }
    closeModal()
    await loadUsers()
  } catch (error) {
    showToast(error.message || 'Error saving user', 'error')
  }
}

const deleteUser = async (user) => {
  if (confirm(`Are you sure you want to delete user ${user.username}?`)) {
    try {
      await userStore.deleteUser(user.id)
      showToast('User deleted successfully', 'success')
      await loadUsers()
    } catch (error) {
      showToast('Error deleting user', 'error')
    }
  }
}
</script>

<style scoped>
.users-view {
  padding: 1rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.search-input,
.role-select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.table-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.data-table th {
  background: #f8f9fa;
  font-weight: 600;
}

.role-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
}

.role-badge.admin {
  background: #e74c3c;
  color: white;
}

.role-badge.teacher {
  background: #3498db;
  color: white;
}

.role-badge.student {
  background: #2ecc71;
  color: white;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
}

.status-badge.active {
  background: #2ecc71;
  color: white;
}

.status-badge.inactive {
  background: #95a5a6;
  color: white;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.btn-icon {
  padding: 0.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background: #f8f9fa;
}

.btn-icon.danger {
  color: #e74c3c;
}

.btn-primary {
  padding: 0.5rem 1rem;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 100%;
  max-width: 500px;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

.btn-secondary {
  padding: 0.5rem 1rem;
  background: #95a5a6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style> 