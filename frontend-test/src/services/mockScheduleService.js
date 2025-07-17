// src/services/mockScheduleService.js
let mockSchedules = [
  { id: 1, student_id: 1001, teacher_id: 1, course_id: 101, class_id: 201, semester_id: 1, day_of_week: 'Thứ Hai', start_time: '08:00', end_time: '09:30', room: 'A201' },
  { id: 2, student_id: 1001, teacher_id: 1, course_id: 102, class_id: 201, semester_id: 1, day_of_week: 'Thứ Ba', start_time: '10:00', end_time: '11:30', room: 'B305' },
  { id: 3, student_id: 1002, teacher_id: 1, course_id: 101, class_id: 201, semester_id: 1, day_of_week: 'Thứ Hai', start_time: '08:00', end_time: '09:30', room: 'A201' },
  { id: 4, student_id: null, teacher_id: 2, course_id: 104, class_id: 203, semester_id: 2, day_of_week: 'Thứ Năm', start_time: '08:00', end_time: '10:00', room: 'C401' },
];

export const fetchScheduleByStudentId = async (studentId) => {
  return new Promise(resolve => {
    setTimeout(() => resolve(mockSchedules.filter(s => s.student_id === studentId)), 500);
  });
};

export const fetchScheduleByTeacherId = async (teacherId) => {
  return new Promise(resolve => {
    setTimeout(() => resolve(mockSchedules.filter(s => s.teacher_id === teacherId)), 500);
  });
};

export const createSchedule = async (scheduleData) => {
  return new Promise(resolve => {
    setTimeout(() => {
      const newId = Math.max(...mockSchedules.map(s => s.id)) + 1;
      const newSchedule = { id: newId, ...scheduleData };
      mockSchedules.push(newSchedule);
      resolve(newSchedule);
    }, 500);
  });
};

export const updateSchedule = async (id, scheduleData) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const index = mockSchedules.findIndex(s => s.id === id);
      if (index !== -1) {
        mockSchedules[index] = { ...mockSchedules[index], ...scheduleData, id };
        resolve(mockSchedules[index]);
      } else {
        reject(new Error('Schedule not found'));
      }
    }, 500);
  });
};

export const deleteSchedule = async (id) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const initialLength = mockSchedules.length;
      mockSchedules = mockSchedules.filter(s => s.id !== id);
      if (mockSchedules.length < initialLength) {
        resolve({ success: true });
      } else {
        reject(new Error('Schedule not found'));
      }
    }, 500);
  });
};