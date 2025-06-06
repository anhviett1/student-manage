<template>
  <div class="index">
    <h1>Hệ thống quản lý sinh viên</h1>
    <p>Chào mừng bạn đến với hệ thống quản lý sinh viên của chúng tôi!</p>
    <router-link to="/login">Bắt đầu</router-link>
  </div>
</template>
<script setup>
  
</script>
<style scoped>
.index {
  text-align: center;
  margin-top: 50px;
}
.index h1 {
  font-size: 2em;
  color: #333;
}
.index p {
  font-size: 1.2em;
  color: #666;
} 
.index a {
  display: inline-block;
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 5px;
}
.index a:hover {
  background-color: #0056b3;
}
</style>

