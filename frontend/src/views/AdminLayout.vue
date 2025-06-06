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
  height: 100vh;
  width: 100vw;  
  overflow: hidden;
}

.sidebar {
  width: 250px;
  background: #2c3e50;
  color: white;
  padding: 1rem;
  height: 100vh;
  overflow-y: auto;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #f5f6fa;
  height: 100vh;
  overflow: hidden;
}

.top-bar {
  background: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: flex-end;
}

.content {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
}

</style> 