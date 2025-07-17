<template>
  <div class="profile-section card">
    <h3>Thông tin cá nhân</h3>
    <div class="avatar-container">
      <img src="https://via.placeholder.com/150" alt="Avatar người dùng" class="user-avatar" />
    </div>
    <p><strong>Tên:</strong> {{ userName }}</p>
    <p><strong>Email:</strong> {{ userEmail }}</p>
    <button @click="editProfile" class="btn btn-primary">Chỉnh sửa hồ sơ</button>
  </div>
</template>

<script>
export default {
  name: 'ProfileSection',
  props: {
    userName: {
      type: String,
      default: 'Nguyễn Văn A'
    },
    userEmail: {
      type: String,
      default: 'nguyenvana@example.com'
    }
  },
  methods: {
    editProfile() {
      // Phát sự kiện để mở dialog chỉnh sửa hồ sơ
      this.$emit('edit-profile');
    }
  }
};
</script>

<style scoped>
.profile-section {
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  margin-bottom: 20px;
}

.avatar-container {
  text-align: center;
  margin-bottom: 15px;
}

.user-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #eee;
}

h3 {
  color: #333;
  margin-bottom: 15px;
  text-align: center;
}

p {
  margin-bottom: 10px;
  color: #555;
}

.btn {
  display: block;
  width: 100%;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  text-align: center;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  border: none;
}

.btn-primary:hover {
  background-color: #0056b3;
}
</style>