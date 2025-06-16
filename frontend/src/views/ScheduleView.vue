<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { usePermissions } from '@/composables/usePermissions'
import api from '@/services/api'

const toast = useToast()
const {
  isAdmin,
  isTeacher,
  isStudent,
  isAdminOrTeacher,
  canViewSchedules,
  canEditSchedules,
  canDeleteSchedules,
  canImportSchedules,
  canExportSchedules,
  canViewStudentSchedule,
  canViewTeacherSchedule
} = usePermissions()

const schedules = ref([])



<template>
  <div class="card">
    <TabView>
      <!-- Tab for Students -->
      <TabPanel header="Lịch Học Của Tôi" v-if="isStudent">
        <DataTable
          v-if="canViewStudentSchedule"
          :value="mySchedules"
          :loading="loading"
          // ... existing code ...
        >
          <!-- ... existing code ... -->
        </DataTable>
      </TabPanel>

      <!-- Tab for Teachers -->
      <TabPanel header="Lịch Giảng Dạy" v-if="isTeacher">
        <DataTable
          v-if="canViewTeacherSchedule"
          :value="teacherSchedules"
          :loading="loading"
          // ... existing code ...
        >
          <!-- ... existing code ... -->
        </DataTable>
      </TabPanel>

      <!-- Tab for Admins -->
      <TabPanel header="Quản Lý Lịch Học" v-if="isAdmin">
        <div class="header">
          <h2>Quản lý lịch học</h2>
          <div class="action-buttons">
            <Button
              v-if="canEditSchedules"
              icon="pi pi-plus"
              label="Thêm lịch học"
              @click="openNew"
            />
            <Button
              v-if="canImportSchedules"
              icon="pi pi-upload"
              label="Import"
              @click="openImport"
            />
            <Button
              v-if="canExportSchedules"
              icon="pi pi-download"
              label="Export"
              @click="exportCSV"
            />
          </div>
        </div>

        <DataTable
          v-if="canViewSchedules"
          :value="schedules"
          :loading="loading"
          // ... existing code ...
        >
          <Column>
            <template #body="{ data }">
              <Button
                v-if="canEditSchedules && !data.is_deleted"
                icon="pi pi-pencil"
                outlined
                rounded
                severity="info"
                @click="editSchedule(data)"
                v-tooltip="'Sửa thông tin'"
              />
              <Button
                v-if="canDeleteSchedules && !data.is_deleted"
                icon="pi pi-trash"
                outlined
                rounded
                severity="danger"
                class="mr-2"
                @click="confirmDelete(data)"
                v-tooltip="'Xóa mềm'"
              />
              <Button
                v-if="canDeleteSchedules && data.is_deleted"
                icon="pi pi-undo"
                outlined
                rounded
                severity="success"
                @click="restoreSchedule(data)"
                v-tooltip="'Khôi phục'"
              />
            </template>
          </Column>
        </DataTable>
      </TabPanel>
    </TabView>
  </div>
</template>
// ... existing code ...
</script> 