// src/services/mockStudentService.js
// This file simulates API calls for student-related data

const mockSemesters = [
  { id: 1, name: 'Học kỳ 1 2024-2025' },
  { id: 2, name: 'Học kỳ 2 2024-2025' },
  { id: 3, name: 'Học kỳ Hè 2025' },
];

const mockAllCourses = [
  { id: 101, name: 'Cấu trúc dữ liệu và giải thuật', code: 'CS101', credits: 3, department_name: 'CNTT', description: 'Môn học cơ bản về cấu trúc dữ liệu và giải thuật.' },
  { id: 102, name: 'Lập trình hướng đối tượng', code: 'CS102', credits: 3, department_name: 'CNTT', description: 'Giới thiệu về các nguyên lý lập trình hướng đối tượng.' },
  { id: 103, name: 'Cơ sở dữ liệu', code: 'CS103', credits: 3, department_name: 'CNTT', description: 'Tìm hiểu về thiết kế và quản lý cơ sở dữ liệu.' },
  { id: 104, name: 'Mạng máy tính', code: 'IT201', credits: 4, department_name: 'ĐTVT', description: 'Cung cấp kiến thức về các mô hình mạng và giao thức.' },
  { id: 105, name: 'Lý thuyết mạch', code: 'EE201', credits: 3, department_name: 'Điện', description: 'Nghiên cứu về các mạch điện tử cơ bản.' },
  { id: 106, name: 'Giải tích 1', code: 'MA101', credits: 4, department_name: 'Toán', description: 'Cung cấp kiến thức toán học cơ bản cho kỹ thuật.' },
];

// Mock already registered courses for student 1 in semester 1
const mockRegisteredCourses = {
  '1_1': [{ student_id: 1, course_id: 101, semester_id: 1 }], // Student 1 registered for CS101 in Semester 1
};

export const fetchSemesters = async () => {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve(mockSemesters);
    }, 500);
  });
};

export const fetchAvailableCoursesForSemester = async (semesterId, studentId) => {
  return new Promise(resolve => {
    setTimeout(() => {
      // Filter out courses already registered by the student for this semester
      const registeredInThisSemester = mockRegisteredCourses[`${studentId}_${semesterId}`] || [];
      const registeredCourseIds = new Set(registeredInThisSemester.map(reg => reg.course_id));

      const available = mockAllCourses.filter(course => !registeredCourseIds.has(course.id));
      resolve(available);
    }, 700);
  });
};

export const registerStudentForCourses = async (registrationData) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      // Simulate successful registration
      console.log('Mock API: Registering courses', registrationData);
      registrationData.forEach(item => {
        const key = `${item.student_id}_${item.semester_id}`;
        if (!mockRegisteredCourses[key]) {
          mockRegisteredCourses[key] = [];
        }
        mockRegisteredCourses[key].push(item);
      });
      resolve({ success: true, message: 'Courses registered successfully' });
    }, 1000); // Simulate network delay
  });
};

export const fetchStudentScores = async (studentId, semesterId = null) => {
  return new Promise(resolve => {
    setTimeout(() => {
      let scores = [
        { id: 1, student_id: studentId, course_id: 101, course_name: 'Cấu trúc dữ liệu và giải thuật', semester_id: 1, semester_name: 'Học kỳ 1 2024-2025', score: 8.5, notes: 'Hoàn thành tốt' },
        { id: 2, student_id: studentId, course_id: 102, course_name: 'Lập trình hướng đối tượng', semester_id: 1, semester_name: 'Học kỳ 1 2024-2025', score: 7.0, notes: 'Khá' },
        { id: 3, student_id: studentId, course_id: 103, course_name: 'Cơ sở dữ liệu', semester_id: 2, semester_name: 'Học kỳ 2 2024-2025', score: 9.2, notes: 'Xuất sắc' },
        { id: 4, student_id: studentId, course_id: 104, course_name: 'Mạng máy tính', semester_id: 2, semester_name: 'Học kỳ 2 2024-2025', score: 6.8, notes: 'Đạt' },
      ];

      if (semesterId) {
        scores = scores.filter(s => s.semester_id === semesterId);
      }
      resolve(scores);
    }, 600);
  });
};

export const fetchStudentSchedule = async (studentId, semesterId) => {
  return new Promise(resolve => {
    setTimeout(() => {
      const scheduleData = [
        {
          id: 1,
          course_name: 'Cấu trúc dữ liệu và giải thuật',
          teacher_name: 'Nguyễn Văn A',
          class_name: 'CNTT1 K20',
          semester_name: 'Học kỳ 1 2024-2025',
          day_of_week: 'Thứ Hai',
          start_time: '08:00',
          end_time: '09:30',
          room: 'A201'
        },
        {
          id: 2,
          course_name: 'Lập trình hướng đối tượng',
          teacher_name: 'Trần Thị B',
          class_name: 'CNTT1 K20',
          semester_name: 'Học kỳ 1 2024-2025',
          day_of_week: 'Thứ Ba',
          start_time: '10:00',
          end_time: '11:30',
          room: 'B305'
        },
        {
          id: 3,
          course_name: 'Cơ sở dữ liệu',
          teacher_name: 'Lê Văn C',
          class_name: 'CNTT1 K20',
          semester_name: 'Học kỳ 2 2024-2025',
          day_of_week: 'Thứ Tư',
          start_time: '13:00',
          end_time: '14:30',
          room: 'A102'
        },
        {
          id: 4,
          course_name: 'Mạng máy tính',
          teacher_name: 'Phạm Thị D',
          class_name: 'CNTT1 K20',
          semester_name: 'Học kỳ 2 2024-2025',
          day_of_week: 'Thứ Năm',
          start_time: '08:00',
          end_time: '10:00',
          room: 'C401'
        }
      ];
      const filteredSchedule = scheduleData.filter(s => s.semester_name === mockSemesters.find(sem => sem.id === semesterId)?.name);
      resolve(filteredSchedule);
    }, 800);
  });
};