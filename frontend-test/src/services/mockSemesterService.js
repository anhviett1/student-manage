// src/services/mockSemesterService.js
let mockSemesters = [
  { id: 1, name: 'Học kỳ 1 2024-2025', start_date: '2024-09-01', end_date: '2024-12-31' },
  { id: 2, name: 'Học kỳ 2 2024-2025', start_date: '2025-01-15', end_date: '2025-05-30' },
  { id: 3, name: 'Học kỳ Hè 2025', start_date: '2025-06-15', end_date: '2025-08-15' },
];

export const fetchSemesters = async () => {
  return new Promise(resolve => {
    setTimeout(() => resolve(mockSemesters), 500);
  });
};

export const createSemester = async (semesterData) => {
  return new Promise(resolve => {
    setTimeout(() => {
      const newId = Math.max(...mockSemesters.map(s => s.id)) + 1;
      const newSemester = { id: newId, ...semesterData };
      mockSemesters.push(newSemester);
      resolve(newSemester);
    }, 500);
  });
};

export const updateSemester = async (id, semesterData) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const index = mockSemesters.findIndex(s => s.id === id);
      if (index !== -1) {
        mockSemesters[index] = { ...mockSemesters[index], ...semesterData, id };
        resolve(mockSemesters[index]);
      } else {
        reject(new Error('Semester not found'));
      }
    }, 500);
  });
};

export const deleteSemester = async (id) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const initialLength = mockSemesters.length;
      mockSemesters = mockSemesters.filter(s => s.id !== id);
      if (mockSemesters.length < initialLength) {
        resolve({ success: true });
      } else {
        reject(new Error('Semester not found'));
      }
    }, 500);
  });
};