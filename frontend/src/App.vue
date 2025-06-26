<script setup>
import { useAuthStore } from '@/stores/auth'
import { onMounted } from 'vue'

// Khởi tạo auth store để kiểm tra trạng thái đăng nhập
const authStore = useAuthStore()

onMounted(async () => {
  // Nếu đã đăng nhập mà chưa có user, tự động fetch user
  if (authStore.isAuthenticated && !authStore.user) {
    try {
      await authStore.fetchCurrentUser()
    } catch (error) {
      authStore.logout()
    }
  }
})
</script>

<template>
  <div class="app">
    <router-view />
    <!-- Toast notification toàn cục nếu muốn -->
    <Toast position="top-right" />
  </div>
</template>

<style>
/* Import font từ Google Fonts để đồng bộ typography */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Reset CSS */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  color: #1f2937;
  background: #f4f6f9;
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Button styles */
.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: background-color 0.3s, transform 0.1s;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background: #2563eb;
  transform: translateY(-1px);
}

.btn-secondary {
  background: #6b7280;
  color: white;
}

.btn-secondary:hover {
  background: #4b5563;
  transform: translateY(-1px);
}

.btn-danger {
  background: #ef4444;
  color: white;
}

.btn-danger:hover {
  background: #dc2626;
  transform: translateY(-1px);
}

/* Form styles */
.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #34495e;
  font-size: 1rem;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.form-control:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Table styles */
.table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.table th,
.table td {
  padding: 1.25rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.table th {
  background: #f9fafb;
  font-weight: 600;
  color: #1f2937;
}

/* Card styles */
.card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 2rem;
}

/* Badge styles */
.badge {
  padding: 0.375rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
}

.badge-primary {
  background: #3b82f6;
  color: white;
}

.badge-success {
  background: #10b981;
  color: white;
}

.badge-warning {
  background: #f59e0b;
  color: white;
}

.badge-danger {
  background: #ef4444;
  color: white;
}

/* PrimeVue overrides */
:deep(.p-inputtext),
:deep(.p-textarea),
:deep(.p-dropdown),
:deep(.p-calendar .p-inputtext) {
  font-size: 1rem;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  transition: border-color 0.3s, box-shadow 0.3s;
}

:deep(.p-inputtext:focus),
:deep(.p-textarea:focus),
:deep(.p-dropdown:focus),
:deep(.p-calendar .p-inputtext:focus) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

:deep(.p-button) {
  border-radius: 6px;
  font-weight: 500;
  transition: background-color 0.3s, transform 0.1s;
}

:deep(.p-button:hover) {
  transform: translateY(-1px);
}
</style>