<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div class="logo">
        <h2>Admin Panel</h2>
      </div>
      <nav class="nav-menu">
        <router-link to="/admin/dashboard" class="nav-item">
          <i class="fas fa-tachometer-alt"></i>
          Dashboard
        </router-link>
        <router-link to="/admin/users" class="nav-item">
          <i class="fas fa-users"></i>
          Users
        </router-link>
        <router-link to="/admin/students" class="nav-item">
          <i class="fas fa-user-graduate"></i>
          Students
        </router-link>
        <router-link to="/admin/courses" class="nav-item">
          <i class="fas fa-book"></i>
          Courses
        </router-link>
        <router-link to="/admin/classes" class="nav-item">
          <i class="fas fa-chalkboard"></i>
          Classes
        </router-link>
      </nav>
    </aside>
    <main class="main-content">
      <header class="top-bar">
        <div class="user-info">
          <span>{{ currentUser?.username }}</span>
          <button @click="logout" class="logout-btn">Logout</button>
        </div>
      </header>
      <div class="content">
        <router-view></router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const currentUser = ref(null)

onMounted(async () => {
  currentUser.value = await authStore.getCurrentUser()
})

const logout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 250px;
  background: #2c3e50;
  color: white;
  padding: 1rem;
}

.logo {
  padding: 1rem 0;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.nav-menu {
  margin-top: 2rem;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 0.8rem 1rem;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  margin-bottom: 0.5rem;
  transition: background 0.3s;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.nav-item.router-link-active {
  background: #3498db;
}

.nav-item i {
  margin-right: 0.8rem;
}

.main-content {
  flex: 1;
  background: #f5f6fa;
}

.top-bar {
  background: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: flex-end;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logout-btn {
  padding: 0.5rem 1rem;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.content {
  padding: 2rem;
}
</style> 