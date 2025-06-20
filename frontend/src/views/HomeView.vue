<template>
  <BaseLayout>
    <div class="home card">
      <div class="header">
        <h1>Chào Mừng Đến Với Hệ Thống Quản Lý Sinh Viên</h1>
        <p class="subtitle">Quản lý thông tin sinh viên, giảng viên và học tập một cách hiệu quả</p>
      </div>
      <div class="content">
        <div class="welcome-section">
          <img src="@/assets/images/login.png" alt="Welcome Illustration" class="welcome-image" />
          <div class="welcome-text">
            <h3>Bắt Đầu Ngay</h3>
            <p>Sử dụng menu điều hướng bên trái để truy cập các chức năng như quản lý sinh viên, giảng viên, môn học, điểm số và nhiều hơn nữa.</p>
            <Button
              label="Khám Phá Chức Năng"
              icon="pi pi-arrow-right"
              severity="primary"
              @click="navigateToStudents"
              class="explore-button"
            />
          </div>
        </div>
        <div class="overview-section">
          <h3>Tổng Quan Hệ Thống</h3>
          <div class="overview-cards">
            <div class="card-item">
              <i class="pi pi-users icon" />
              <h4>Quản Lý Sinh Viên</h4>
              <p>Theo dõi thông tin, điểm số và trạng thái của sinh viên.</p>
              <Button label="Xem Chi Tiết" icon="pi pi-arrow-right" class="p-button-sm" @click="navigateToStudents" />
            </div>
            <div class="card-item">
              <i class="pi pi-briefcase icon" />
              <h4>Quản Lý Giảng Viên</h4>
              <p>Quản lý thông tin và lịch giảng dạy của giảng viên.</p>
              <Button label="Xem Chi Tiết" icon="pi pi-arrow-right" class="p-button-sm" @click="navigateToTeachers" />
            </div>
            <div class="card-item">
              <i class="pi pi-book icon" />
              <h4>Quản Lý Môn Học</h4>
              <p>Tổ chức và theo dõi các môn học trong hệ thống.</p>
              <Button label="Xem Chi Tiết" icon="pi pi-arrow-right" class="p-button-sm" @click="navigateToSubjects" />
            </div>
            <div class="card-item">
               <i class="pi pi-book icon" />
               <h4>Quản Lý Học Kì</h4>
               <p>Tổ chức và theo dõi các học kì trong hệ thống.</p>
               <Button label="Xem Chi Tiết" icon="pi pi-arrow-right" class="p-button-sm" @click="navigateToSemesters" />
             </div>
             <div class="card-item">
               <i class="pi pi-book icon" />
               <h4>Đăng kí</h4>
               <p>Theo dõi đăng kí trong hệ thống.</p>
               <Button label="Xem Chi Tiết" icon="pi pi-arrow-right" class="p-button-sm" @click="navigateToEnrollments" />
             </div>
             <div class="card-item">
               <i class="pi pi-chart-bar icon" />
               <h4>Quản lí điểm</h4>
               <p>Theo dõi, báo cáo và dữ liệu học tập.</p>
               <Button label="Xem Chi Tiết" icon="pi pi-arrow-right" class="p-button-sm" @click="navigateToScores" />
            </div>
            <div class="card-item">
              <i class="pi pi-chart-bar icon" />
              <h4>Django Admin</h4>
              <p>Trang quản trị Django.</p>
              <Button label="Xem Chi Tiết" icon="pi pi-arrow-right" class="p-button-sm" @click="navigateToAdmin" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup>
import { useRouter } from 'vue-router'
import BaseLayout from '@/components/BaseLayout.vue'
import Button from 'primevue/button'

const router = useRouter()

const navigateToStudents = () => {
  router.push('/students')
}

const navigateToTeachers = () => {
  router.push('/teachers')
}

const navigateToSubjects = () => {
  router.push('/subjects')
}

const navigateToScores = () => {
  router.push('/scores')
}

const navigateToSemesters = () => {
  router.push('/semesters')
}

const navigateToEnrollments = () => {
  router.push('/enrollments')
}

const navigateToAdmin = () => {
  router.push('/admin')
}
</script>

<style scoped>
.home {
  padding: 2rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1.2rem;
  color: #6b7280;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.welcome-section {
  display: flex;
  align-items: center;
  gap: 2rem;
  background: #f8fafc;
  padding: 2rem;
  border-radius: 8px;
}

.welcome-image {
  width: 400px;
  height: auto;
  object-fit: contain;
}

.welcome-text {
  flex: 1;
}

.welcome-text h3 {
  font-size: 1.8rem;
  color: #1f2937;
  margin-bottom: 1rem;
}

.welcome-text p {
  font-size: 1rem;
  color: #4b5563;
  margin-bottom: 1.5rem;
}

.explore-button {
  font-size: 1rem;
}

.overview-section {
  padding: 2rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.overview-section h3 {
  font-size: 1.8rem;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.card-item {
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 8px;
  text-align: center;
  transition: transform 0.2s;
}

.card-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-item .icon {
  font-size: 2.5rem;
  color: #3b82f6;
  margin-bottom: 1rem;
}

.card-item h4 {
  font-size: 1.2rem;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.card-item p {
  font-size: 0.9rem;
  color: #6b7280;
}
</style>