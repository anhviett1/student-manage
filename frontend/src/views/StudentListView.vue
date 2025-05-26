<template>
  <div class="card">
    <div class="card-header">
      <h2>Students</h2>
      <Button @click="openNew" severity="success" icon="pi pi-plus" label="Add Student" />
    </div>

    <DataTable
      :value="students"
      :paginator="true"
      :rows="10"
      :loading="loading"
      dataKey="id"
      :filters="filters"
      filterDisplay="menu"
      :globalFilterFields="['name', 'email', 'student_id']"
      responsiveLayout="scroll"
    >
      <template #empty>
        <div class="text-center p-4">
          <p>No students found.</p>
        </div>
      </template>

      <template #loading>
        <div class="text-center p-4">
          <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
        </div>
      </template>

      <Column field="student_id" header="Student ID" sortable style="min-width: 12rem">
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            @input="filterCallback()"
            placeholder="Search by ID"
            class="p-column-filter"
          />
        </template>
      </Column>

      <Column field="name" header="Name" sortable style="min-width: 14rem">
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            @input="filterCallback()"
            placeholder="Search by name"
            class="p-column-filter"
          />
        </template>
      </Column>

      <Column field="email" header="Email" sortable style="min-width: 14rem">
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            @input="filterCallback()"
            placeholder="Search by email"
            class="p-column-filter"
          />
        </template>
      </Column>

      <Column field="date_of_birth" header="Date of Birth" sortable style="min-width: 10rem">
        <template #body="{ data }">
          {{ formatDate(data.date_of_birth) }}
        </template>
      </Column>

      <Column :exportable="false" style="min-width: 8rem">
        <template #body="{ data }">
          <Button icon="pi pi-pencil" outlined rounded class="mr-2" @click="editStudent(data)" />
          <Button icon="pi pi-trash" outlined rounded severity="danger" @click="confirmDeleteStudent(data)" />
        </template>
      </Column>
    </DataTable>

    <Dialog v-model:visible="studentDialog" :style="{ width: '450px' }" header="Student Details" :modal="true" class="p-fluid">
      <div class="field">
        <label for="name">Name</label>
        <InputText id="name" v-model.trim="student.name" required autofocus :class="{ 'p-invalid': submitted && !student.name }" />
        <small class="p-error" v-if="submitted && !student.name">Name is required.</small>
      </div>
      <div class="field">
        <label for="email">Email</label>
        <InputText id="email" v-model.trim="student.email" required :class="{ 'p-invalid': submitted && !student.email }" />
        <small class="p-error" v-if="submitted && !student.email">Email is required.</small>
      </div>
      <div class="field">
        <label for="date_of_birth">Date of Birth</label>
        <Calendar id="date_of_birth" v-model="student.date_of_birth" dateFormat="yy-mm-dd" />
      </div>

      <template #footer>
        <Button label="Cancel" icon="pi pi-times" outlined @click="hideDialog" />
        <Button label="Save" icon="pi pi-check" @click="saveStudent" />
      </template>
    </Dialog>

    <Dialog v-model:visible="deleteStudentDialog" :style="{ width: '450px' }" header="Confirm" :modal="true">
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span v-if="student">Are you sure you want to delete <b>{{ student.name }}</b>?</span>
      </div>
      <template #footer>
        <Button label="No" icon="pi pi-times" outlined @click="deleteStudentDialog = false" />
        <Button label="Yes" icon="pi pi-check" severity="danger" @click="deleteStudent" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { api } from '@/services/api'

const toast = useToast()
const students = ref([])
const studentDialog = ref(false)
const deleteStudentDialog = ref(false)
const student = ref({})
const submitted = ref(false)
const loading = ref(true)
const filters = ref({})

onMounted(async () => {
  await loadStudents()
})

const loadStudents = async () => {
  try {
    loading.value = true
    students.value = await api.getStudents()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to load students', life: 3000 })
  } finally {
    loading.value = false
  }
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString()
}

const openNew = () => {
  student.value = {}
  submitted.value = false
  studentDialog.value = true
}

const hideDialog = () => {
  studentDialog.value = false
  submitted.value = false
}

const editStudent = (data) => {
  student.value = { ...data }
  studentDialog.value = true
}

const confirmDeleteStudent = (data) => {
  student.value = data
  deleteStudentDialog.value = true
}

const saveStudent = async () => {
  submitted.value = true

  if (student.value.name?.trim() && student.value.email?.trim()) {
    try {
      if (student.value.id) {
        // Update existing student
        await api.updateStudent(student.value.id, student.value)
        toast.add({ severity: 'success', summary: 'Successful', detail: 'Student Updated', life: 3000 })
      } else {
        // Create new student
        await api.createStudent(student.value)
        toast.add({ severity: 'success', summary: 'Successful', detail: 'Student Created', life: 3000 })
      }

      studentDialog.value = false
      student.value = {}
      await loadStudents()
    } catch (error) {
      toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to save student', life: 3000 })
    }
  }
}

const deleteStudent = async () => {
  try {
    await api.deleteStudent(student.value.id)
    deleteStudentDialog.value = false
    student.value = {}
    toast.add({ severity: 'success', summary: 'Successful', detail: 'Student Deleted', life: 3000 })
    await loadStudents()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to delete student', life: 3000 })
  }
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.card-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: var(--text-color);
}

.confirmation-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

:deep(.p-datatable .p-datatable-header) {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-width: 1px 0 1px 0;
  padding: 1rem;
}

:deep(.p-datatable .p-datatable-thead > tr > th) {
  background: #f8fafc;
  color: #1e293b;
  font-weight: 600;
}

:deep(.p-datatable .p-datatable-tbody > tr > td) {
  padding: 1rem;
}

:deep(.p-datatable .p-datatable-tbody > tr:hover) {
  background: #f1f5f9;
}
</style> 