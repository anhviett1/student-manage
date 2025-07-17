// src/services/mockAuthService.js
// This file simulates API calls for authentication

export const loginUser = async (username, password) => {
  return new Promise(resolve => {
    setTimeout(() => {
      // Simulate authentication logic
      if (username === 'admin' && password === 'admin123') {
        resolve({ success: true, message: 'Đăng nhập thành công!', user: { id: 1, role: 'admin', username: 'admin' }, token: 'mock-admin-token' });
      } else if (username === 'teacher' && password === 'teacher123') {
        resolve({ success: true, message: 'Đăng nhập thành công!', user: { id: 1, role: 'teacher', username: 'teacher' }, token: 'mock-teacher-token' });
      } else if (username === 'student' && password === 'student123') {
        resolve({ success: true, message: 'Đăng nhập thành công!', user: { id: 1, role: 'student', username: 'student' }, token: 'mock-student-token' });
      } else {
        resolve({ success: false, message: 'Tên đăng nhập hoặc mật khẩu không đúng.' });
      }
    }, 1000); // Simulate network delay
  });
};

// You might add logout, register, forgot password mock functions here later
export const logoutUser = async () => {
  return new Promise(resolve => {
    setTimeout(() => {
      console.log('Mock API: User logged out');
      resolve({ success: true });
    }, 300);
  });
};