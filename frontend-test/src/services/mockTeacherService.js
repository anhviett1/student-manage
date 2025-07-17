// src/services/mockTeacherService.js
// This file simulates API calls for teacher-related data

const mockSemesters = [
  { id: 1, name: 'Học kỳ 1 2024-2025' },
  { id: 2, name: 'Học kỳ 2 2024-2025' },
  { id: 3, name: 'Học kỳ Hè 2025' },
];

const mockTeachers = [
  { id: 1, full_name: 'Giáo viên A', teacher_id: 'GV001', email: 'gva@example.com', department_id: 1, department_name: 'CNTT' },
  { id: 2, full_name: 'Giáo viên B', teacher_id: 'GV002', email: 'gvb@example.com', department_id: 2, department_name: 'Điện tử' },
];

const mockCourses = [
  { id: 101, name: 'Cấu trúc dữ liệu và giải thuật', code: 'CS101', credits: 3 },
  { id: 102, name: 'Lập trình hướng đối tượng', code: 'CS102', credits: 3 },
  { id: 103, name: 'Cơ sở dữ liệu', code: 'CS103', credits: 3 },
  { id: 104, name: 'Mạng máy tính', code: 'IT201', credits: 4 },
];

const mockClasses = [
  { id: 201, name: 'CNTT1 K20', department_id: 1 },
  { id: 202, name: 'CNTT2 K20', department_id: 1 },
  { id: 203, name: 'ĐTVT1 K21', department_id: 2 },
];

const mockStudents = [
  { id: 1001, full_name: 'Nguyễn Văn An', student_id: 'SV001', email: 'an@example.com', phone_number: '0901112222', gender: 'male', major_name: 'Công nghệ phần mềm', class_name: 'CNTT1 K20', class_id: 201 },
  { id: 1002, full_name: 'Trần Thị Bình', student_id: 'SV002', email: 'binh@example.com', phone_number: '0903334444', gender: 'female', major_name: 'Hệ thống thông tin', class_name: 'CNTT1 K20', class_id: 201 },
  { id: 1003, full_name: 'Lê Văn Cường', student_id: 'SV003', email: 'cuong@example.com', phone_number: '0905556666', gender: 'male', major_name: 'Công nghệ phần mềm', class_name: 'CNTT2 K20', class_id: 202 },
  { id: 1004, full_name: 'Phạm Thu Dung', student_id: 'SV004', email: 'dung@example.com', phone_number: '0907778888', gender: 'female', major_name: 'Kỹ thuật điện tử', class_name: 'ĐTVT1 K21', class_id: 203 },
];

const mockScores = [
  { id: 1, student_id: 1001, course_id: 101, semester_id: 1, score: 8.5, notes: 'Tốt', score_id: 'score1' },
  { id: 2, student_id: 1002, course_id: 101, semester_id: 1, score: 7.0, notes: 'Khá', score_id: 'score2' },
  { id: 3, student_id: 1001, course_id: 102, semester_id: 1, score: null, notes: null }, // Example: no score yet
  { id: 4, student_id: 1003, course_id: 102, semester_id: 1, score: 7.8, notes: 'Khá tốt', score_id: 'score3' },
];

// Schedule assignments for teacher 1
const mockTeacherAssignments = {
  '1_1': [ // Teacher 1, Semester 1
    { id: 1, teacher_id: 1, course_id: 101, course_name: 'Cấu trúc dữ liệu và giải thuật', course_code: 'CS101', class_id: 201, class_name: 'CNTT1 K20', semester_id: 1, semester_name: 'Học kỳ 1 2024-2025', day_of_week: 'Thứ Hai', start_time: '08:00', end_time: '09:30', room: 'A201' },
    { id: 2, teacher_id: 1, course_id: 102, course_name: 'Lập trình hướng đối tượng', course_code: 'CS102', class_id: 201, class_name: 'CNTT1 K20', semester_id: 1, semester_name: 'Học kỳ 1 2024-2025', day_of_week: 'Thứ Ba', start_time: '10:00', end_time: '11:30', room: 'B305' },
  ],
  '1_2': [ // Teacher 1, Semester 2
    { id: 3, teacher_id: 1, course_id: 103, course_name: 'Cơ sở dữ liệu', course_code: 'CS103', class_id: 202, class_name: 'CNTT2 K20', semester_id: 2, semester_name: 'Học kỳ 2 2024-2025', day_of_week: 'Thứ Tư', start_time: '13:00', end_time: '14:30', room: 'A102' },
  ]
};


export const fetchSemesters = async () => {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve(mockSemesters);
    }, 500);
  });
};

export const fetchTeacherAssignedClasses = async (teacherId) => {
  return new Promise(resolve => {
    setTimeout(() => {
      // In a real scenario, this would fetch classes the teacher is assigned to teach
      // For mock, let's assume teacher 1 teaches CNTT1 K20 and CNTT2 K20
      const assignedClassIds = mockTeacherAssignments[`${teacherId}_1`]?.map(assign => assign.class_id) || [];
      const assignedClassIds2 = mockTeacherAssignments[`${teacherId}_2`]?.map(assign => assign.class_id) || [];
      const uniqueClassIds = [...new Set([...assignedClassIds, ...assignedClassIds2])];

      const classesForTeacher = mockClasses.filter(cls => uniqueClassIds.includes(cls.id));
      resolve(classesForTeacher);
    }, 600);
  });
};

export const fetchClassRoster = async (classId) => {
  return new Promise(resolve => {
    setTimeout(() => {
      const roster = mockStudents.filter(s => s.class_id === classId);
      resolve(roster);
    }, 700);
  });
};

export const fetchTeacherAssignedCourses = async (teacherId) => {
  return new Promise(resolve => {
    setTimeout(() => {
      // This should return courses the teacher is assigned to teach across all semesters
      let uniqueCourseIds = new Set();
      for (const key in mockTeacherAssignments) {
        if (key.startsWith(`${teacherId}_`)) {
          mockTeacherAssignments[key].forEach(assignment => uniqueCourseIds.add(assignment.course_id));
        }
      }
      const assignedCourses = mockCourses.filter(course => uniqueCourseIds.has(course.id));
      resolve(assignedCourses);
    }, 600);
  });
};

export const fetchStudentsForCourseAndSemester = async (courseId, semesterId) => {
  return new Promise(resolve => {
    setTimeout(() => {
      // Simulate fetching students enrolled in this specific course and semester
      // and their current scores if available
      const studentsInCourse = mockStudents.filter(s =>
        // In a real app, you'd check enrollment records
        // For mock, let's assume all students from CNTT1 K20 and CNTT2 K20 are potentially enrolled
        s.class_id === 201 || s.class_id === 202
      ).map(student => {
        const scoreRecord = mockScores.find(
          s => s.student_id === student.id && s.course_id === courseId && s.semester_id === semesterId
        );
        return {
          ...student,
          current_score: scoreRecord ? scoreRecord.score : null,
          notes: scoreRecord ? scoreRecord.notes : null,
          score_id: scoreRecord ? scoreRecord.id : null // Pass existing score ID for editing
        };
      });
      resolve(studentsInCourse);
    }, 800);
  });
};

export const saveStudentScore = async (scoreData) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      // Simulate saving or updating a score
      console.log('Mock API: Saving score', scoreData);
      if (scoreData.score_id) {
        // Update existing score
        const index = mockScores.findIndex(s => s.id === scoreData.score_id);
        if (index !== -1) {
          mockScores[index] = { ...mockScores[index], ...scoreData };
        }
      } else {
        // Add new score
        const newId = mockScores.length > 0 ? Math.max(...mockScores.map(s => s.id)) + 1 : 1;
        mockScores.push({
          id: newId,
          student_id: scoreData.student_id,
          course_id: scoreData.course_id,
          semester_id: scoreData.semester_id,
          score: scoreData.score,
          notes: scoreData.notes,
          score_id: `score${newId}` // Mock a score_id
        });
      }
      resolve({ success: true, message: 'Score saved successfully' });
    }, 1000);
  });
};

export const fetchTeacherAssignedSubjects = async (teacherId, semesterId) => {
  return new Promise(resolve => {
    setTimeout(() => {
      const assignments = mockTeacherAssignments[`${teacherId}_${semesterId}`] || [];
      resolve(assignments);
    }, 700);
  });
};