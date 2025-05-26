<template>
  <div class="layout-wrapper">
    <Toast />
    <nav class="navbar">
      <div class="navbar-brand">
        <router-link to="/" class="logo">Student Management</router-link>
      </div>
      <div class="navbar-menu" v-if="authStore.isAuthenticated()">
        <router-link to="/students" class="nav-item">Students</router-link>
        <router-link to="/teachers" class="nav-item">Teachers</router-link>
        <router-link to="/classes" class="nav-item">Classes</router-link>
        <router-link to="/subjects" class="nav-item">Subjects</router-link>
        <router-link to="/enrollments" class="nav-item">Enrollments</router-link>
        <router-link to="/semesters" class="nav-item">Semesters</router-link>
        <router-link to="/scores" class="nav-item">Scores</router-link>
      </div>
      <div class="navbar-end" v-if="authStore.isAuthenticated()">
        <router-link to="/profile" class="nav-item">
          <i class="pi pi-user"></i>
          Profile
        </router-link>
        <Button @click="handleLogout" severity="danger" text>
          <i class="pi pi-sign-out"></i>
          Logout
        </Button>
      </div>
    </nav>

    <main class="main-content">
      <slot></slot>
    </main>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'

const authStore = useAuthStore()
const router = useRouter()
const toast = useToast()

const handleLogout = () => {
  authStore.logout()
  toast.add({ severity: 'success', summary: 'Success', detail: 'Logged out successfully', life: 3000 })
  router.push('/login')
}
</script>

<style scoped>
.layout-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background-color: var(--primary-color);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.navbar-brand {
  font-size: 1.5rem;
  font-weight: bold;
}

.logo {
  color: white;
  text-decoration: none;
}

.navbar-menu {
  display: flex;
  gap: 1.5rem;
}

.navbar-end {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.nav-item {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.nav-item:hover {
  background-color: rgba(255,255,255,0.1);
}

.main-content {
  flex: 1;
  padding: 2rem;
  background-color: #f5f5f5;
}
</style> 