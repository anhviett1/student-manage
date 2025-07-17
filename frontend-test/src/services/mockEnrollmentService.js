// src/services/mockEnrollmentService.js
let mockEnrollments = [
  { id: 1, student_id: 1001, course_id: 101, semester_id: 1, enrollment_date: '2024-08-15' },
  { id: 2, student_id: 1002, course_id: 101, semester_id: 1, enrollment_date: '2024-08-16' },
  { id: 3, student_id: 1001, course_id: 102, semester_id: 1, enrollment_date: '2024-08-15' },
  { id: 4, student_id: 1003, course_id: 103, semester_id: 2, enrollment_date: '2025-01-20' },
];

export const fetchEnrollments = async () => {
  return new Promise(resolve => {
    setTimeout(() => resolve(mockEnrollments), 500);
  });
};

export const createEnrollment = async (enrollmentData) => {
  return new Promise(resolve => {
    setTimeout(() => {
      const newId = Math.max(...mockEnrollments.map(e => e.id)) + 1;
      const newEnrollment = { id: newId, ...enrollmentData };
      mockEnrollments.push(newEnrollment);
      resolve(newEnrollment);
    }, 500);
  });
};

export const deleteEnrollment = async (id) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const initialLength = mockEnrollments.length;
      mockEnrollments = mockEnrollments.filter(e => e.id !== id);
      if (mockEnrollments.length < initialLength) {
        resolve({ success: true });
      } else {
        reject(new Error('Enrollment not found'));
      }
    }, 500);
  });
};