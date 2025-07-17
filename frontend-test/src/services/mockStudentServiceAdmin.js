// src/services/mockStudentServiceAdmin.js
let mockStudents = [
  { id: 1001, full_name: 'Nguyễn Văn An', student_id: 'SV001', email: 'an@example.com', phone_number: '0901112222', gender: 'male', major_name: 'Công nghệ phần mềm', class_name: 'CNTT1 K20' },
  { id: 1002, full_name: 'Trần Thị Bình', student_id: 'SV002', email: 'binh@example.com', phone_number: '0903334444', gender: 'female', major_name: 'Hệ thống thông tin', class_name: 'CNTT1 K20' },
  { id: 1003, full_name: 'Lê Văn Cường', student_id: 'SV003', email: 'cuong@example.com', phone_number: '0905556666', gender: 'male', major_name: 'Công nghệ phần mềm', class_name: 'CNTT2 K20' },
];

export const fetchStudents = async () => {
  return new Promise(resolve => {
    setTimeout(() => resolve(mockStudents), 500);
  });
};

export const createStudent = async (studentData) => {
  return new Promise(resolve => {
    setTimeout(() => {
      const newId = Math.max(...mockStudents.map(s => s.id)) + 1;
      const newStudent = { id: newId, ...studentData };
      mockStudents.push(newStudent);
      resolve(newStudent);
    }, 500);
  });
};

export const updateStudent = async (id, studentData) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const index = mockStudents.findIndex(s => s.id === id);
      if (index !== -1) {
        mockStudents[index] = { ...mockStudents[index], ...studentData, id };
        resolve(mockStudents[index]);
      } else {
        reject(new Error('Student not found'));
      }
    }, 500);
  });
};

export const deleteStudent = async (id) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const initialLength = mockStudents.length;
      mockStudents = mockStudents.filter(s => s.id !== id);
      if (mockStudents.length < initialLength) {
        resolve({ success: true });
      } else {
        reject(new Error('Student not found'));
      }
    }, 500);
  });
};