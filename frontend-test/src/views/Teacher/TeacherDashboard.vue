<template>
  <div>
    <h1>Trang quản lý của Giáo viên</h1>
    <SubjectAssignmentCard />
    <ClassRosterTable />
    <GradeEntryForm />
  </div>
</template>

<script setup>
import SubjectAssignmentCard from '@/components/teacher/SubjectAssignmentCard.vue';
import ClassRosterTable from '@/components/teacher/ClassRosterTable.vue';
import GradeEntryForm from '@/components/teacher/GradeEntryForm.vue';
</script>