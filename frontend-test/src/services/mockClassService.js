// src/services/mockClassService.js
let mockClasses = [
  { id: 201, name: 'CNTT1 K20', department_id: 1, department_name: 'Công nghệ thông tin' },
  { id: 202, name: 'CNTT2 K20', department_id: 1, department_name: 'Công nghệ thông tin' },
  { id: 203, name: 'ĐTVT1 K21', department_id: 2, department_name: 'Điện tử viễn thông' },
];

export const fetchClasses = async () => {
  return new Promise(resolve => {
    setTimeout(() => resolve(mockClasses), 500);
  });
};

export const createClass = async (classData) => {
  return new Promise(resolve => {
    setTimeout(() => {
      const newId = Math.max(...mockClasses.map(c => c.id)) + 1;
      const newClass = { id: newId, ...classData };
      mockClasses.push(newClass);
      resolve(newClass);
    }, 500);
  });
};

export const updateClass = async (id, classData) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const index = mockClasses.findIndex(c => c.id === id);
      if (index !== -1) {
        mockClasses[index] = { ...mockClasses[index], ...classData, id };
        resolve(mockClasses[index]);
      } else {
        reject(new Error('Class not found'));
      }
    }, 500);
  });
};

export const deleteClass = async (id) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const initialLength = mockClasses.length;
      mockClasses = mockClasses.filter(c => c.id !== id);
      if (mockClasses.length < initialLength) {
        resolve({ success: true });
      } else {
        reject(new Error('Class not found'));
      }
    }, 500);
  });
};