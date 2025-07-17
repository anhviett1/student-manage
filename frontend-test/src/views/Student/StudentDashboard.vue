<template>
  <div>
    <h1>Trang quản lý khóa học của sinh viên</h1>
    <CourseRegistrationForm />
    <MyScheduleCard />
    <MyScoreTable />
  </div>
</template>

<script setup>
import CourseRegistrationForm from '@/components/student/CourseRegistrationForm.vue';
import MyScheduleCard from '@/components/student/MyScheduleCard.vue';
import MyScoreTable from '@/components/student/MyScoreTable.vue';
</script>