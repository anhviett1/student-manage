// src/services/mockScoreService.js
let mockScores = [
  { id: 1, student_id: 1001, course_id: 101, semester_id: 1, score: 8.5, notes: 'Hoàn thành tốt' },
  { id: 2, student_id: 1002, course_id: 101, semester_id: 1, score: 7.0, notes: 'Khá' },
  { id: 3, student_id: 1001, course_id: 102, semester_id: 1, score: 9.2, notes: 'Xuất sắc' },
  { id: 4, student_id: 1003, course_id: 103, semester_id: 2, score: 6.8, notes: 'Đạt' },
];

export const fetchScores = async () => {
  return new Promise(resolve => {
    setTimeout(() => resolve(mockScores), 500);
  });
};

export const createScore = async (scoreData) => {
  return new Promise(resolve => {
    setTimeout(() => {
      const newId = Math.max(...mockScores.map(s => s.id)) + 1;
      const newScore = { id: newId, ...scoreData };
      mockScores.push(newScore);
      resolve(newScore);
    }, 500);
  });
};

export const updateScore = async (id, scoreData) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const index = mockScores.findIndex(s => s.id === id);
      if (index !== -1) {
        mockScores[index] = { ...mockScores[index], ...scoreData, id };
        resolve(mockScores[index]);
      } else {
        reject(new Error('Score not found'));
      }
    }, 500);
  });
};

export const deleteScore = async (id) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const initialLength = mockScores.length;
      mockScores = mockScores.filter(s => s.id !== id);
      if (mockScores.length < initialLength) {
        resolve({ success: true });
      } else {
        reject(new Error('Score not found'));
      }
    }, 500);
  });
};