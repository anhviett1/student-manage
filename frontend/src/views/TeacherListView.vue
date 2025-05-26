<template>
  <div class="card">
    <div class="card-header">
      <h2>Giáo Viên</h2>
      <Button @click="openNew" severity="success" icon="pi pi-plus" label="Thêm Giáo Viên" />
    </div>

    <DataTable
      :value="teachers"
      :paginator="true"
      :rows="10"
      :loading="loading"
      dataKey="id"
      :filters="filters"
      filterDisplay="menu"
      :globalFilterFields="['name', 'email', 'teacher_id']"
      responsiveLayout="scroll"
    >
      <template #empty>
        <div class="text-center p-4">
          <p>Không tìm thấy giáo viên nào.</p>
        </div>
      </template>

      <template #loading>
        <div class="text-center p-4">
          <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
        </div>
      </template>

      <Column field="teacher_id" header="Mã Giáo Viên" sortable style="min-width: 12rem">
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            @input="filterCallback()"
            placeholder="Tìm theo mã"
            class="p-column-filter"
          />
        </template>
      </Column>

      <Column field="name" header="Họ Tên" sortable style="min-width: 14rem">
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            @input="filterCallback()"
            placeholder="Tìm theo tên"
            class="p-column-filter"
          />
        </template>
      </Column>

      <Column field="email" header="Email" sortable style="min-width: 14rem">
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            @input="filterCallback()"
            placeholder="Tìm theo email"
            class="p-column-filter"
          />
        </template>
      </Column>

      <Column field="phone" header="Số Điện Thoại" sortable style="min-width: 12rem">
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            @input="filterCallback()"
            placeholder="Tìm theo số điện thoại"
            class="p-column-filter"
          />
        </template>
      </Column>

      <Column field="subject" header="Môn Học" sortable style="min-width: 12rem">
        <template #body="{ data }">
          {{ data.subject?.name || 'Chưa phân công' }}
        </template>
      </Column>

      <Column :exportable="false" style="min-width: 8rem">
        <template #body="{ data }">
          <Button icon="pi pi-pencil" outlined rounded class="mr-2" @click="editTeacher(data)" />
          <Button icon="pi pi-trash" outlined rounded severity="danger" @click="confirmDeleteTeacher(data)" />
        </template>
      </Column>
    </DataTable>

    <Dialog v-model:visible="teacherDialog" :style="{ width: '450px' }" header="Thông Tin Giáo Viên" :modal="true" class="p-fluid">
      <div class="field">
        <label for="name">Họ Tên</label>
        <InputText id="name" v-model.trim="teacher.name" required autofocus :class="{ 'p-invalid': submitted && !teacher.name }" />
        <small class="p-error" v-if="submitted && !teacher.name">Vui lòng nhập họ tên.</small>
      </div>
      <div class="field">
        <label for="email">Email</label>
        <InputText id="email" v-model.trim="teacher.email" required :class="{ 'p-invalid': submitted && !teacher.email }" />
        <small class="p-error" v-if="submitted && !teacher.email">Vui lòng nhập email.</small>
      </div>
      <div class="field">
        <label for="phone">Số Điện Thoại</label>
        <InputText id="phone" v-model.trim="teacher.phone" required :class="{ 'p-invalid': submitted && !teacher.phone }" />
        <small class="p-error" v-if="submitted && !teacher.phone">Vui lòng nhập số điện thoại.</small>
      </div>
      <div class="field">
        <label for="subject">Môn Học</label>
        <Dropdown
          id="subject"
          v-model="teacher.subject"
          :options="subjects"
          optionLabel="name"
          placeholder="Chọn môn học"
          :class="{ 'p-invalid': submitted && !teacher.subject }"
        />
        <small class="p-error" v-if="submitted && !teacher.subject">Vui lòng chọn môn học.</small>
      </div>

      <template #footer>
        <Button label="Hủy" icon="pi pi-times" outlined @click="hideDialog" />
        <Button label="Lưu" icon="pi pi-check" @click="saveTeacher" />
      </template>
    </Dialog>

    <Dialog v-model:visible="deleteTeacherDialog" :style="{ width: '450px' }" header="Xác Nhận" :modal="true">
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span v-if="teacher">Bạn có chắc chắn muốn xóa giáo viên <b>{{ teacher.name }}</b>?</span>
      </div>
      <template #footer>
        <Button label="Không" icon="pi pi-times" outlined @click="deleteTeacherDialog = false" />
        <Button label="Có" icon="pi pi-check" severity="danger" @click="deleteTeacher" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { api } from '@/services/api'

const toast = useToast()
const teachers = ref([])
const subjects = ref([])
const teacherDialog = ref(false)
const deleteTeacherDialog = ref(false)
const teacher = ref({})
const submitted = ref(false)
const loading = ref(true)
const filters = ref({})

onMounted(async () => {
  await Promise.all([loadTeachers(), loadSubjects()])
})

const loadTeachers = async () => {
  try {
    loading.value = true
    teachers.value = await api.getTeachers()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách giáo viên', life: 3000 })
  } finally {
    loading.value = false
  }
}

const loadSubjects = async () => {
  try {
    subjects.value = await api.getSubjects()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách môn học', life: 3000 })
  }
}

const openNew = () => {
  teacher.value = {}
  submitted.value = false
  teacherDialog.value = true
}

const hideDialog = () => {
  teacherDialog.value = false
  submitted.value = false
}

const editTeacher = (data) => {
  teacher.value = { ...data }
  teacherDialog.value = true
}

const confirmDeleteTeacher = (data) => {
  teacher.value = data
  deleteTeacherDialog.value = true
}

const saveTeacher = async () => {
  submitted.value = true

  if (teacher.value.name?.trim() && teacher.value.email?.trim() && teacher.value.phone?.trim()) {
    try {
      if (teacher.value.id) {
        await api.updateTeacher(teacher.value.id, teacher.value)
        toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật giáo viên thành công', life: 3000 })
      } else {
        await api.createTeacher(teacher.value)
        toast.add({ severity: 'success', summary: 'Thành công', detail: 'Thêm giáo viên thành công', life: 3000 })
      }

      teacherDialog.value = false
      teacher.value = {}
      await loadTeachers()
    } catch (error) {
      toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể lưu thông tin giáo viên', life: 3000 })
    }
  }
}

const deleteTeacher = async () => {
  try {
    await api.deleteTeacher(teacher.value.id)
    deleteTeacherDialog.value = false
    teacher.value = {}
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa giáo viên thành công', life: 3000 })
    await loadTeachers()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa giáo viên', life: 3000 })
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