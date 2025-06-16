<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { usePermissions } from '@/composables/usePermissions'
import api from '@/services/api'

const toast = useToast()
const {
  isAdmin,
  isTeacher,
  canViewDepartments,
  canEditDepartments,
  canDeleteDepartments,
  canImportDepartments,
  canExportDepartments
} = usePermissions()

const departments = ref([])
// ... existing code ...

<template>
  <div class="card">
    <div class="header">
      <h2>Quản lý khoa</h2>
      <div class="action-buttons">
        <Button
          v-if="canEditDepartments"
          icon="pi pi-plus"
          label="Thêm khoa"
          @click="openNew"
        />
        <Button
          v-if="canImportDepartments"
          icon="pi pi-upload"
          label="Import"
          @click="openImport"
        />
        <Button
          v-if="canExportDepartments"
          icon="pi pi-download"
          label="Export"
          @click="exportCSV"
        />
      </div>
    </div>

    <DataTable
      v-if="canViewDepartments"
      :value="departments"
      :loading="loading"
      // ... existing code ...
    >
      <Column>
        <template #body="{ data }">
          <Button
            v-if="canEditDepartments && !data.is_deleted"
            icon="pi pi-pencil"
            outlined
            rounded
            severity="info"
            @click="editDepartment(data)"
            v-tooltip="'Sửa thông tin'"
          />
          <Button
            v-if="canDeleteDepartments && !data.is_deleted"
            icon="pi pi-trash"
            outlined
            rounded
            severity="danger"
            class="mr-2"
            @click="confirmDelete(data)"
            v-tooltip="'Xóa mềm'"
          />
          <Button
            v-if="canDeleteDepartments && data.is_deleted"
            icon="pi pi-undo"
            outlined
            rounded
            severity="success"
            @click="restoreDepartment(data)"
            v-tooltip="'Khôi phục'"
          />
        </template>
      </Column>
    </DataTable>
  </div>
</template>
// ... existing code ...
</script> 