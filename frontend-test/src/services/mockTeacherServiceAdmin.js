// src/services/mockTeacherServiceAdmin.js
let mockTeachers = [
  { id: 1, full_name: 'Nguyễn Văn A', teacher_id: 'GV001', email: 'gva@example.com', phone_number: '0912345678', department_id: 1, department_name: 'Công nghệ thông tin' },
  { id: 2, full_name: 'Trần Thị B', teacher_id: 'GV002', email: 'gvb@example.com', phone_number: '0987654321', department_id: 2, department_name: 'Điện tử viễn thông' },
  { id: 3, full_name: 'Lê Văn C', teacher_id: 'GV003', email: 'gvc@example.com', phone_number: '0909090909', department_id: 1, department_name: 'Công nghệ thông tin' },
];

export const fetchTeachers = async () => {
  return new Promise(resolve => {
    setTimeout(() => resolve(mockTeachers), 500);
  });
};

export const createTeacher = async (teacherData) => {
  return new Promise(resolve => {
    setTimeout(() => {
      const newId = Math.max(...mockTeachers.map(t => t.id)) + 1;
      const newTeacher = { id: newId, ...teacherData };
      mockTeachers.push(newTeacher);
      resolve(newTeacher);
    }, 500);
  });
};

export const updateTeacher = async (id, teacherData) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const index = mockTeachers.findIndex(t => t.id === id);
      if (index !== -1) {
        mockTeachers[index] = { ...mockTeachers[index], ...teacherData, id };
        resolve(mockTeachers[index]);
      } else {
        reject(new Error('Teacher not found'));
      }
    }, 500);
  });
};

export const deleteTeacher = async (id) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const initialLength = mockTeachers.length;
      mockTeachers = mockTeachers.filter(t => t.id !== id);
      if (mockTeachers.length < initialLength) {
        resolve({ success: true });
      } else {
        reject(new Error('Teacher not found'));
      }
    }, 500);
  });
};