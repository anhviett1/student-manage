// src/services/mockSubjectService.js
let mockSubjects = [
  { id: 101, name: 'Cấu trúc dữ liệu và giải thuật', code: 'CS101', credits: 3, department_id: 1, department_name: 'Công nghệ thông tin' },
  { id: 102, name: 'Lập trình hướng đối tượng', code: 'CS102', credits: 3, department_id: 1, department_name: 'Công nghệ thông tin' },
  { id: 103, name: 'Cơ sở dữ liệu', code: 'CS103', credits: 3, department_id: 1, department_name: 'Công nghệ thông tin' },
  { id: 104, name: 'Mạng máy tính', code: 'IT201', credits: 4, department_id: 2, department_name: 'Điện tử viễn thông' },
];

export const fetchSubjects = async () => {
  return new Promise(resolve => {
    setTimeout(() => resolve(mockSubjects), 500);
  });
};

export const createSubject = async (subjectData) => {
  return new Promise(resolve => {
    setTimeout(() => {
      const newId = Math.max(...mockSubjects.map(s => s.id)) + 1;
      const newSubject = { id: newId, ...subjectData };
      mockSubjects.push(newSubject);
      resolve(newSubject);
    }, 500);
  });
};

export const updateSubject = async (id, subjectData) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const index = mockSubjects.findIndex(s => s.id === id);
      if (index !== -1) {
        mockSubjects[index] = { ...mockSubjects[index], ...subjectData, id };
        resolve(mockSubjects[index]);
      } else {
        reject(new Error('Subject not found'));
      }
    }, 500);
  });
};

export const deleteSubject = async (id) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const initialLength = mockSubjects.length;
      mockSubjects = mockSubjects.filter(s => s.id !== id);
      if (mockSubjects.length < initialLength) {
        resolve({ success: true });
      } else {
        reject(new Error('Subject not found'));
      }
    }, 500);
  });
};