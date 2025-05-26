<template>
  <div class="card">
    <div class="card-header">
      <h2>Môn Học</h2>
      <Button @click="openNew" severity="success" icon="pi pi-plus" label="Thêm Môn Học" />
    </div>

    <DataTable
      :value="subjects"
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
          <p>Không tìm thấy môn học nào.</p>
        </div>
      </template>

      <template #loading>
        <div class="text-center p-4">
          <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
        </div>
      </template>

      <Column field="code" header="Mã Môn" sortable style="min-width: 12rem">
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            @input="filterCallback()"
            placeholder="Tìm theo mã môn"
            class="p-column-filter"
          />
        </template>
      </Column>

      <Column field="name" header="Tên Môn" sortable style="min-width: 14rem">
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            @input="filterCallback()"
            placeholder="Tìm theo tên môn"
            class="p-column-filter"
          />
        </template>
      </Column>

      <Column field="credits" header="Số Tín Chỉ" sortable style="min-width: 10rem">
        <template #body="{ data }">
          {{ data.credits || 0 }}
        </template>
      </Column>

      <Column field="teacher_count" header="Số Giáo Viên" sortable style="min-width: 12rem">
        <template #body="{ data }">
          {{ data.teacher_count || 0 }}
        </template>
      </Column>

      <Column :exportable="false" style="min-width: 8rem">
        <template #body="{ data }">
          <Button icon="pi pi-pencil" outlined rounded class="mr-2" @click="editSubject(data)" />
          <Button icon="pi pi-trash" outlined rounded severity="danger" @click="confirmDeleteSubject(data)" />
        </template>
      </Column>
    </DataTable>

    <Dialog v-model:visible="subjectDialog" :style="{ width: '450px' }" header="Thông Tin Môn Học" :modal="true" class="p-fluid">
      <div class="field">
        <label for="code">Mã Môn</label>
        <InputText id="code" v-model.trim="subject.code" required autofocus :class="{ 'p-invalid': submitted && !subject.code }" />
        <small class="p-error" v-if="submitted && !subject.code">Vui lòng nhập mã môn.</small>
      </div>
      <div class="field">
        <label for="name">Tên Môn</label>
        <InputText id="name" v-model.trim="subject.name" required :class="{ 'p-invalid': submitted && !subject.name }" />
        <small class="p-error" v-if="submitted && !subject.name">Vui lòng nhập tên môn.</small>
      </div>
      <div class="field">
        <label for="credits">Số Tín Chỉ</label>
        <InputNumber id="credits" v-model="subject.credits" :min="1" :max="10" required :class="{ 'p-invalid': submitted && !subject.credits }" />
        <small class="p-error" v-if="submitted && !subject.credits">Vui lòng nhập số tín chỉ.</small>
      </div>

      <template #footer>
        <Button label="Hủy" icon="pi pi-times" outlined @click="hideDialog" />
        <Button label="Lưu" icon="pi pi-check" @click="saveSubject" />
      </template>
    </Dialog>

    <Dialog v-model:visible="deleteSubjectDialog" :style="{ width: '450px' }" header="Xác Nhận" :modal="true">
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span v-if="subject">Bạn có chắc chắn muốn xóa môn học <b>{{ subject.name }}</b>?</span>
      </div>
      <template #footer>
        <Button label="Không" icon="pi pi-times" outlined @click="deleteSubjectDialog = false" />
        <Button label="Có" icon="pi pi-check" severity="danger" @click="deleteSubject" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { api } from '@/services/api'

const toast = useToast()
const subjects = ref([])
const subjectDialog = ref(false)
const deleteSubjectDialog = ref(false)
const subject = ref({})
const submitted = ref(false)
const loading = ref(true)
const filters = ref({})

onMounted(async () => {
  await loadSubjects()
})

const loadSubjects = async () => {
  try {
    loading.value = true
    subjects.value = await api.getSubjects()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách môn học', life: 3000 })
  } finally {
    loading.value = false
  }
}

const openNew = () => {
  subject.value = {}
  submitted.value = false
  subjectDialog.value = true
}

const hideDialog = () => {
  subjectDialog.value = false
  submitted.value = false
}

const editSubject = (data) => {
  subject.value = { ...data }
  subjectDialog.value = true
}

const confirmDeleteSubject = (data) => {
  subject.value = data
  deleteSubjectDialog.value = true
}

const saveSubject = async () => {
  submitted.value = true

  if (subject.value.code?.trim() && subject.value.name?.trim() && subject.value.credits) {
    try {
      if (subject.value.id) {
        await api.updateSubject(subject.value.id, subject.value)
        toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật môn học thành công', life: 3000 })
      } else {
        await api.createSubject(subject.value)
        toast.add({ severity: 'success', summary: 'Thành công', detail: 'Thêm môn học thành công', life: 3000 })
      }

      subjectDialog.value = false
      subject.value = {}
      await loadSubjects()
    } catch (error) {
      toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể lưu thông tin môn học', life: 3000 })
    }
  }
}

const deleteSubject = async () => {
  try {
    await api.deleteSubject(subject.value.id)
    deleteSubjectDialog.value = false
    subject.value = {}
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa môn học thành công', life: 3000 })
    await loadSubjects()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa môn học', life: 3000 })
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