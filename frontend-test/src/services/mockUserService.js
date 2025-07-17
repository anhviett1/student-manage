// src/services/mockUserService.js
let mockUsers = [
  { id: 1, username: 'admin', email: 'admin@example.com', role: 'admin' },
  { id: 2, username: 'teacher', email: 'teacher@example.com', role: 'teacher' },
  { id: 3, username: 'student', email: 'student@example.com', role: 'student' },
];

export const fetchUsers = async () => {
  return new Promise(resolve => {
    setTimeout(() => resolve(mockUsers), 500);
  });
};

export const createUser = async (userData) => {
  return new Promise(resolve => {
    setTimeout(() => {
      const newId = Math.max(...mockUsers.map(u => u.id)) + 1;
      const newUser = { id: newId, ...userData };
      mockUsers.push(newUser);
      resolve(newUser);
    }, 500);
  });
};

export const updateUser = async (id, userData) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const index = mockUsers.findIndex(u => u.id === id);
      if (index !== -1) {
        mockUsers[index] = { ...mockUsers[index], ...userData, id };
        resolve(mockUsers[index]);
      } else {
        reject(new Error('User not found'));
      }
    }, 500);
  });
};

export const deleteUser = async (id) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const initialLength = mockUsers.length;
      mockUsers = mockUsers.filter(u => u.id !== id);
      if (mockUsers.length < initialLength) {
        resolve({ success: true });
      } else {
        reject(new Error('User not found'));
      }
    }, 500);
  });
};