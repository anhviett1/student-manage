<template>
  <div class="card">
    <div class="card-header">
      <h2>Lớp Học</h2>
      <Button @click="openNew" severity="success" icon="pi pi-plus" label="Thêm Lớp" />
    </div>

    <DataTable
      :value="classes"
      :paginator="true"
      :rows="10"
      :loading="loading"
      dataKey="id"
      :filters="filters"
      filterDisplay="menu"
      :globalFilterFields="['name', 'code']"
      responsiveLayout="scroll"
    >
      <template #empty>
        <div class="text-center p-4">
          <p>Không tìm thấy lớp học nào.</p>
        </div>
      </template>

      <template #loading>
        <div class="text-center p-4">
          <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
        </div>
      </template>

      <Column field="code" header="Mã Lớp" sortable style="min-width: 12rem">
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            @input="filterCallback()"
            placeholder="Tìm theo mã lớp"
            class="p-column-filter"
          />
        </template>
      </Column>

      <Column field="name" header="Tên Lớp" sortable style="min-width: 14rem">
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            @input="filterCallback()"
            placeholder="Tìm theo tên lớp"
            class="p-column-filter"
          />
        </template>
      </Column>

      <Column field="semester" header="Học Kỳ" sortable style="min-width: 12rem">
        <template #body="{ data }">
          {{ data.semester?.name || 'Chưa phân công' }}
        </template>
      </Column>

      <Column field="teacher" header="Giáo Viên Chủ Nhiệm" sortable style="min-width: 14rem">
        <template #body="{ data }">
          {{ data.teacher?.name || 'Chưa phân công' }}
        </template>
      </Column>

      <Column field="student_count" header="Số Học Sinh" sortable style="min-width: 10rem">
        <template #body="{ data }">
          {{ data.student_count || 0 }}
        </template>
      </Column>

      <Column :exportable="false" style="min-width: 8rem">
        <template #body="{ data }">
          <Button icon="pi pi-pencil" outlined rounded class="mr-2" @click="editClass(data)" />
          <Button icon="pi pi-trash" outlined rounded severity="danger" @click="confirmDeleteClass(data)" />
        </template>
      </Column>
    </DataTable>

    <Dialog v-model:visible="classDialog" :style="{ width: '450px' }" header="Thông Tin Lớp Học" :modal="true" class="p-fluid">
      <div class="field">
        <label for="code">Mã Lớp</label>
        <InputText id="code" v-model.trim="classData.code" required autofocus :class="{ 'p-invalid': submitted && !classData.code }" />
        <small class="p-error" v-if="submitted && !classData.code">Vui lòng nhập mã lớp.</small>
      </div>
      <div class="field">
        <label for="name">Tên Lớp</label>
        <InputText id="name" v-model.trim="classData.name" required :class="{ 'p-invalid': submitted && !classData.name }" />
        <small class="p-error" v-if="submitted && !classData.name">Vui lòng nhập tên lớp.</small>
      </div>
      <div class="field">
        <label for="semester">Học Kỳ</label>
        <Dropdown
          id="semester"
          v-model="classData.semester"
          :options="semesters"
          optionLabel="name"
          placeholder="Chọn học kỳ"
          :class="{ 'p-invalid': submitted && !classData.semester }"
        />
        <small class="p-error" v-if="submitted && !classData.semester">Vui lòng chọn học kỳ.</small>
      </div>
      <div class="field">
        <label for="teacher">Giáo Viên Chủ Nhiệm</label>
        <Dropdown
          id="teacher"
          v-model="classData.teacher"
          :options="teachers"
          optionLabel="name"
          placeholder="Chọn giáo viên"
          :class="{ 'p-invalid': submitted && !classData.teacher }"
        />
        <small class="p-error" v-if="submitted && !classData.teacher">Vui lòng chọn giáo viên chủ nhiệm.</small>
      </div>

      <template #footer>
        <Button label="Hủy" icon="pi pi-times" outlined @click="hideDialog" />
        <Button label="Lưu" icon="pi pi-check" @click="saveClass" />
      </template>
    </Dialog>

    <Dialog v-model:visible="deleteClassDialog" :style="{ width: '450px' }" header="Xác Nhận" :modal="true">
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span v-if="classData">Bạn có chắc chắn muốn xóa lớp <b>{{ classData.name }}</b>?</span>
      </div>
      <template #footer>
        <Button label="Không" icon="pi pi-times" outlined @click="deleteClassDialog = false" />
        <Button label="Có" icon="pi pi-check" severity="danger" @click="deleteClass" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { api } from '@/services/api'

const toast = useToast()
const classes = ref([])
const semesters = ref([])
const teachers = ref([])
const classDialog = ref(false)
const deleteClassDialog = ref(false)
const classData = ref({})
const submitted = ref(false)
const loading = ref(true)
const filters = ref({})

onMounted(async () => {
  await Promise.all([loadClasses(), loadSemesters(), loadTeachers()])
})

const loadClasses = async () => {
  try {
    loading.value = true
    classes.value = await api.getClasses()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách lớp học', life: 3000 })
  } finally {
    loading.value = false
  }
}

const loadSemesters = async () => {
  try {
    semesters.value = await api.getSemesters()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách học kỳ', life: 3000 })
  }
}

const loadTeachers = async () => {
  try {
    teachers.value = await api.getTeachers()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách giáo viên', life: 3000 })
  }
}

const openNew = () => {
  classData.value = {}
  submitted.value = false
  classDialog.value = true
}

const hideDialog = () => {
  classDialog.value = false
  submitted.value = false
}

const editClass = (data) => {
  classData.value = { ...data }
  classDialog.value = true
}

const confirmDeleteClass = (data) => {
  classData.value = data
  deleteClassDialog.value = true
}

const saveClass = async () => {
  submitted.value = true

  if (classData.value.code?.trim() && classData.value.name?.trim() && classData.value.semester && classData.value.teacher) {
    try {
      if (classData.value.id) {
        await api.updateClass(classData.value.id, classData.value)
        toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật lớp học thành công', life: 3000 })
      } else {
        await api.createClass(classData.value)
        toast.add({ severity: 'success', summary: 'Thành công', detail: 'Thêm lớp học thành công', life: 3000 })
      }

      classDialog.value = false
      classData.value = {}
      await loadClasses()
    } catch (error) {
      toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể lưu thông tin lớp học', life: 3000 })
    }
  }
}

const deleteClass = async () => {
  try {
    await api.deleteClass(classData.value.id)
    deleteClassDialog.value = false
    classData.value = {}
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa lớp học thành công', life: 3000 })
    await loadClasses()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa lớp học', life: 3000 })
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