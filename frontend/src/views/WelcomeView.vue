<template>
  <div class="welcome-container">
    <div class="welcome-content">
      <h1>Chào Mừng Đến Với Hệ Thống Quản Lý Sinh Viên</h1>
      <p>Hệ thống quản lý sinh viên toàn diện, giúp bạn dễ dàng theo dõi và quản lý thông tin sinh viên.</p>
      <div class="welcome-actions">
        <router-link to="/login" class="btn btn-primary">Đăng Nhập</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
// Component logic here
</script>

<style scoped>
.welcome-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f4f6f9 0%, #e9ecef 100%);
  padding: 2rem;
}

.welcome-content {
  max-width: 800px;
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

p {
  font-size: 1.2rem;
  color: #4a5568;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.welcome-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn {
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background: #2563eb;
  transform: translateY(-2px);
}
</style> 