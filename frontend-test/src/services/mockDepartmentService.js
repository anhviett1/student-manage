// src/services/mockDepartmentService.js
let mockDepartments = [
  { id: 1, name: 'Công nghệ thông tin', code: 'CNTT', phone: '024-12345678' },
  { id: 2, name: 'Điện tử viễn thông', code: 'ĐTVT', phone: '024-87654321' },
  { id: 3, name: 'Cơ khí', code: 'CK', phone: '024-11223344' },
];

export const fetchDepartments = async () => {
  return new Promise(resolve => {
    setTimeout(() => resolve(mockDepartments), 500);
  });
};

export const createDepartment = async (departmentData) => {
  return new Promise(resolve => {
    setTimeout(() => {
      const newId = Math.max(...mockDepartments.map(d => d.id)) + 1;
      const newDepartment = { id: newId, ...departmentData };
      mockDepartments.push(newDepartment);
      resolve(newDepartment);
    }, 500);
  });
};

export const updateDepartment = async (id, departmentData) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const index = mockDepartments.findIndex(d => d.id === id);
      if (index !== -1) {
        mockDepartments[index] = { ...mockDepartments[index], ...departmentData, id };
        resolve(mockDepartments[index]);
      } else {
        reject(new Error('Department not found'));
      }
    }, 500);
  });
};

export const deleteDepartment = async (id) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const initialLength = mockDepartments.length;
      mockDepartments = mockDepartments.filter(d => d.id !== id);
      if (mockDepartments.length < initialLength) {
        resolve({ success: true });
      } else {
        reject(new Error('Department not found'));
      }
    }, 500);
  });
};