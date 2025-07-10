<template>
  <div class="card" v-if="canViewClasses">
    <Toast />
    <TabView>
      <!-- Tab 1: Thông Tin Lớp (chỉ cho giáo viên/sinh viên, nếu cần) -->
      <TabPanel header="Thông Tin Lớp" v-if="isTeacher || isStudent">
        <div class="profile-section">
          <div class="profile-header">
            <h2>Thông Tin Lớp</h2>
            <Button
              icon="pi pi-pencil"
              label="Chỉnh Sửa"
              severity="primary"
              @click="openEdit"
              v-if="!isEditing && canEditClasses"
              v-tooltip="'Chỉnh sửa thông tin lớp'"
            />
          </div>
          <div v-if="!isEditing" class="profile-details">
            <div class="detail-item"><label>Mã Lớp:</label><span>{{ classDetail.class_id }}</span></div>
            <div class="detail-item"><label>Tên Lớp:</label><span>{{ classDetail.class_name }}</span></div>
            <div class="detail-item"><label>Mô Tả:</label><span>{{ classDetail.description }}</span></div>
            <div class="detail-item"><label>Khoa:</label><span>{{ classDetail.department?.department_name }}</span></div>
            <div class="detail-item"><label>Số Tín Chỉ:</label><span>{{ classDetail.credits }}</span></div>
            <div class="detail-item"><label>Học Kỳ:</label><span>{{ classDetail.semester?.semester_name }}</span></div>
            <div class="detail-item"><label>Môn Học:</label><span>{{ classDetail.subject?.subject_name }}</span></div>
            <div class="detail-item"><label>Giảng Viên:</label><span>{{ classDetail.teacher?.last_name }} {{ classDetail.teacher?.first_name }}</span></div>
            <div class="detail-item"><label>Trạng Thái:</label><Tag :severity="getStatusSeverity(classDetail.status)" :value="getStatusLabel(classDetail.status)" /></div>
            <div class="detail-item"><label>Hoạt Động:</label><Tag :severity="classDetail.is_active ? 'success' : 'warning'" :value="classDetail.is_active ? 'Có' : 'Không'" /></div>
          </div>
          <div v-else class="edit-form">
            <!-- Form chỉnh sửa tương tự dialog bên dưới -->
            <div class="field">
              <label for="class_id">Mã Lớp</label>
              <InputText id="class_id" v-model="classDetail.class_id" disabled />
            </div>
            <div class="field">
              <label for="class_name">Tên Lớp</label>
              <InputText id="class_name" v-model="classDetail.class_name" :class="{ 'p-invalid': errors.class_name }" />
              <small class="p-error" v-if="errors.class_name">{{ errors.class_name }}</small>
            </div>
            <div class="field">
              <label for="description">Mô Tả</label>
              <Textarea id="description" v-model="classDetail.description" rows="4" />
            </div>
            <div class="field">
              <label for="department">Khoa</label>
              <Dropdown id="department" v-model="classDetail.department" :options="departments" optionLabel="department_name" optionValue="department_id" placeholder="Chọn khoa" />
            </div>
            <div class="field">
              <label for="credits">Số Tín Chỉ</label>
              <InputNumber id="credits" v-model="classDetail.credits" :min="1" :class="{ 'p-invalid': errors.credits }" />
              <small class="p-error" v-if="errors.credits">{{ errors.credits }}</small>
            </div>
            <div class="field">
              <label for="is_active">Đang Hoạt Động</label>
              <InputSwitch id="is_active" v-model="classDetail.is_active" />
            </div>
            <div class="field">
              <label for="semester">Học Kỳ</label>
              <Dropdown id="semester" v-model="classDetail.semester" :options="semesters" optionLabel="semester_name" optionValue="semester_id" placeholder="Chọn học kỳ" :class="{ 'p-invalid': errors.semester }" />
              <small class="p-error" v-if="errors.semester">{{ errors.semester }}</small>
            </div>
            <div class="field">
              <label for="subject">Môn Học</label>
              <Dropdown id="subject" v-model="classDetail.subject" :options="subjects" optionLabel="subject_name" optionValue="subject_id" placeholder="Chọn môn học" :class="{ 'p-invalid': errors.subject }" />
              <small class="p-error" v-if="errors.subject">{{ errors.subject }}</small>
            </div>
            <div class="field">
              <label for="teacher">Giảng Viên</label>
              <Dropdown id="teacher" v-model="classDetail.teacher" :options="teachers" optionLabel="last_name" optionValue="teacher_id" placeholder="Chọn giảng viên" />
            </div>
            <div class="buttons">
              <Button label="Hủy" icon="pi pi-times" text @click="cancelEdit" />
              <Button label="Lưu" icon="pi pi-check" @click="saveClassDetail" />
            </div>
      </div>
    </div>
      </TabPanel>
      <!-- Tab 2: Quản Lý Lớp Học (admin/giáo viên) -->
      <TabPanel header="Quản Lý Lớp Học" v-if="canViewClasses">
        <div class="header">
          <h2>Quản Lý Lớp Học</h2>
          <div class="action-buttons">
            <Button v-if="canEditClasses" icon="pi pi-plus" label="Thêm Lớp" severity="primary" class="mr-2" @click="openNew" v-tooltip="'Thêm lớp mới'" />
            <Button v-if="canExportData" icon="pi pi-download" label="Export" severity="success" @click="exportClasses" v-tooltip="'Xuất danh sách lớp'" />
            <Button icon="pi pi-filter" label="Lớp Active" severity="info" class="mr-2" @click="loadActiveClasses" v-tooltip="'Lọc lớp đang hoạt động'" />
          </div>
        </div>
        <div class="filter-bar">
          <div class="filter-group">
            <Dropdown v-model="filters.status" :options="statusOptions" optionLabel="label" optionValue="value" placeholder="Lọc trạng thái" class="filter-dropdown mr-2" @change="loadClasses" />
            <Dropdown v-model="filters.department" :options="departments" optionLabel="department_name" optionValue="department_id" placeholder="Lọc khoa" class="filter-dropdown mr-2" @change="loadClasses" />
            <Dropdown v-model="filters.semester" :options="semesters" optionLabel="semester_name" optionValue="semester_id" placeholder="Lọc học kỳ" class="filter-dropdown mr-2" @change="loadClasses" />
            <Dropdown v-model="filters.subject" :options="subjects" optionLabel="subject_name" optionValue="subject_id" placeholder="Lọc môn học" class="filter-dropdown mr-2" @change="loadClasses" />
            <InputText v-model="filters.global" placeholder="Tìm mã, tên, mô tả..." class="filter-search" @input="filterClasses" />
          </div>
        </div>
        <DataTable v-if="(classes.length > 0 || loading) && canViewClasses" :value="classes" :loading="loading" dataKey="class_id" :paginator="true" :rows="10" :rowsPerPageOptions="[5, 10, 20]" responsiveLayout="scroll" class="p-datatable-sm">
          <template #empty>
            <div class="empty-message"><i class="pi pi-info-circle" /><span>Không tìm thấy lớp học nào.</span></div>
      </template>
          <template #loading>
            <div class="loading-message"><i class="pi pi-spin pi-spinner" /><span>Đang tải dữ liệu...</span></div>
        </template>
          <Column field="class_id" header="Mã Lớp" sortable style="width: 12%" />
          <Column field="class_name" header="Tên Lớp" sortable style="width: 18%" />
          <Column field="description" header="Mô Tả" sortable style="width: 18%" />
          <Column field="department.department_name" header="Khoa" sortable style="width: 15%" />
          <Column field="credits" header="Tín Chỉ" sortable style="width: 8%" align="center" />
          <Column field="semester.semester_name" header="Học Kỳ" sortable style="width: 12%" align="center" />
          <Column field="subject.subject_name" header="Môn Học" sortable style="width: 12%" align="center" />
          <Column field="status" header="Trạng Thái" sortable style="width: 120px" align="center">
        <template #body="{ data }">
          <Tag :severity="getStatusSeverity(data.status)" :value="getStatusLabel(data.status)" />
        </template>
          </Column>
          <Column field="is_active" header="Hoạt Động" sortable style="width: 110px" align="center">
            <template #body="{ data }">
              <Tag :severity="data.is_active ? 'success' : 'warning'" :value="data.is_active ? 'Có' : 'Không'" />
        </template>
      </Column>
          <Column header="Hành Động" style="width: 15%" align="center">
            <template #body="{ data }">
              <Button
                v-if="canEditClasses && !data.is_deleted"
                icon="pi pi-pencil"
                outlined
                rounded
                class="mr-2"
                severity="info"
                @click="editClass(data)"
                v-tooltip="'Sửa thông tin'"
              />
              <Button
                v-if="canDeleteClasses && !data.is_deleted"
                icon="pi pi-trash"
                outlined
                rounded
                severity="danger"
                class="mr-2"
                @click="confirmDelete(data)"
                v-tooltip="'Xóa mềm'"
              />
              <Button
                v-if="canDeleteClasses && data.is_deleted"
                icon="pi pi-undo"
                outlined
                rounded
                severity="success"
                @click="restoreClass(data)"
                v-tooltip="'Khôi phục'"
              />
            </template>
          </Column>
    </DataTable>
        <div v-else-if="!loading && classes.length === 0 && canViewClasses" class="no-data-message">
          <p>Không có dữ liệu lớp học để hiển thị.</p>
          <Button label="Tải lại" icon="pi pi-refresh" @click="loadClasses" severity="secondary" />
        </div>
        <!-- Dialog thêm/sửa lớp học -->
        <Dialog v-model:visible="classDialog" :header="classObj.class_id ? 'Sửa Lớp' : 'Thêm Lớp'" :style="{ width: '600px' }" :modal="true" class="p-fluid">
      <div class="form-section">
        <h4>Thông Tin Cơ Bản</h4>
        <div class="field">
          <label for="class_id">Mã Lớp</label>
              <InputText id="class_id" v-model="classObj.class_id" :class="{ 'p-invalid': errors.class_id }" :disabled="!!classObj.class_id" />
          <small class="p-error" v-if="errors.class_id">{{ errors.class_id }}</small>
        </div>
        <div class="field">
              <label for="class_name">Tên Lớp</label>
              <InputText id="class_name" v-model="classObj.class_name" :class="{ 'p-invalid': errors.class_name }" />
              <small class="p-error" v-if="errors.class_name">{{ errors.class_name }}</small>
        </div>
        <div class="field">
          <label for="description">Mô Tả</label>
          <Textarea id="description" v-model="classObj.description" rows="4" />
        </div>
        <div class="field">
          <label for="department">Khoa</label>
              <Dropdown id="department" v-model="classObj.department" :options="departments" optionLabel="department_name" optionValue="department_id" placeholder="Chọn khoa" />
        </div>
        <div class="field">
          <label for="credits">Số Tín Chỉ</label>
              <InputNumber id="credits" v-model="classObj.credits" :min="1" :class="{ 'p-invalid': errors.credits }" />
          <small class="p-error" v-if="errors.credits">{{ errors.credits }}</small>
        </div>
        <div class="field">
          <label for="is_active">Đang Hoạt Động</label>
          <InputSwitch id="is_active" v-model="classObj.is_active" />
        </div>
      </div>
      <div class="form-section">
        <h4>Quan Hệ</h4>
        <div class="field">
          <label for="semester">Học Kỳ</label>
              <Dropdown id="semester" v-model="classObj.semester" :options="semesters" optionLabel="semester_name" optionValue="semester_id" placeholder="Chọn học kỳ" :class="{ 'p-invalid': errors.semester }" />
          <small class="p-error" v-if="errors.semester">{{ errors.semester }}</small>
        </div>
        <div class="field">
          <label for="subject">Môn Học</label>
              <Dropdown id="subject" v-model="classObj.subject" :options="subjects" optionLabel="subject_name" optionValue="subject_id" placeholder="Chọn môn học" :class="{ 'p-invalid': errors.subject }" />
          <small class="p-error" v-if="errors.subject">{{ errors.subject }}</small>
        </div>
        <div class="field">
          <label for="teacher">Giảng Viên</label>
              <Dropdown id="teacher" v-model="classObj.teacher" :options="teachers" optionLabel="last_name" optionValue="teacher_id" placeholder="Chọn giảng viên" />
        </div>
        <div class="field">
          <label for="teachers">Danh Sách Giảng Viên</label>
              <MultiSelect id="teachers" v-model="classObj.teachers" :options="teachers" optionLabel="last_name" optionValue="teacher_id" placeholder="Chọn giảng viên" display="chip" />
        </div>
        <div class="field">
          <label for="subjects">Danh Sách Môn Học</label>
              <MultiSelect id="subjects" v-model="classObj.subjects" :options="subjects" optionLabel="subject_name" optionValue="subject_id" placeholder="Chọn môn học" display="chip" />
        </div>
      </div>
      <div class="form-section">
        <h4>Trạng Thái</h4>
        <div class="field">
          <label for="status">Trạng Thái</label>
              <Dropdown id="status" v-model="classObj.status" :options="statusOptions" optionLabel="label" optionValue="value" placeholder="Chọn trạng thái" :class="{ 'p-invalid': errors.status }" />
          <small class="p-error" v-if="errors.status">{{ errors.status }}</small>
        </div>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="hideDialog" />
        <Button label="Lưu" icon="pi pi-check" @click="saveClass" />
      </template>
    </Dialog>
        <!-- Dialog xác nhận xóa mềm -->
        <Dialog v-model:visible="deleteClassDialog" header="Xác Nhận Xóa Mềm" :style="{ width: '400px' }" :modal="true">
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
            <span>Bạn có chắc muốn xóa lớp <b>{{ classObj.class_name }}</b>?</span>
      </div>
      <template #footer>
            <Button label="Hủy" icon="pi pi-times" text @click="deleteClassDialog = false" />
            <Button label="Xóa" icon="pi pi-check" severity="danger" @click="deleteClass" />
      </template>
    </Dialog>
        <!-- Dialog xác nhận xóa cứng -->
        <Dialog v-model:visible="hardDeleteClassDialog" header="Xác Nhận Xóa Cứng" :style="{ width: '400px' }" :modal="true">
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
            <span>Bạn có chắc muốn xóa hoàn toàn lớp <b>{{ classObj.class_name }}</b>? Hành động này không thể hoàn tác.</span>
      </div>
      <template #footer>
            <Button label="Hủy" icon="pi pi-times" text @click="hardDeleteClassDialog = false" />
            <Button label="Xóa" icon="pi pi-check" severity="danger" @click="hardDeleteClass" />
      </template>
    </Dialog>
        <!-- Dialog đổi trạng thái -->
        <Dialog v-model:visible="changeStatusDialog" header="Thay Đổi Trạng Thái" :style="{ width: '400px' }" :modal="true">
      <div class="field">
        <label for="new_status">Trạng Thái Mới</label>
            <Dropdown id="new_status" v-model="newStatus" :options="statusOptions" optionLabel="label" optionValue="value" placeholder="Chọn trạng thái mới" :class="{ 'p-invalid': submitted && !newStatus }" />
        <small class="p-error" v-if="submitted && !newStatus">Vui lòng chọn trạng thái mới.</small>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="changeStatusDialog = false" />
        <Button label="Cập Nhật" icon="pi pi-check" @click="changeStatus" />
      </template>
    </Dialog>
      </TabPanel>
    </TabView>
  </div>
  <div v-else class="access-denied">
    <p>Bạn không có quyền truy cập trang này.</p>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import api, { endpoints } from '@/services/api'
import { saveAs } from 'file-saver'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import Tag from 'primevue/tag'
import InputNumber from 'primevue/inputnumber'
import InputSwitch from 'primevue/inputswitch'
import MultiSelect from 'primevue/multiselect'

const toast = useToast()

const classes = ref([])
const classObj = ref({})
const classDetail = ref({})
const classDialog = ref(false)
const deleteClassDialog = ref(false)
const hardDeleteClassDialog = ref(false)
const changeStatusDialog = ref(false)
const isEditing = ref(false)
const loading = ref(false)
const errors = ref({})
const newStatus = ref('')
const submitted = ref(false)
const departments = ref([])
const semesters = ref([])
const subjects = ref([])
const teachers = ref([])
const filters = reactive({
  global: '',
  status: 'active',
  department: null,
  semester: null,
  subject: null,
})

const canExportData = computed(() => isAdmin.value)
    
const statusOptions = [
  { label: 'Đang hoạt động', value: 'active' },
  { label: 'Không hoạt động', value: 'inactive' },
  { label: 'Đang chờ duyệt', value: 'pending' }
]

onMounted(async () => {
    await Promise.all([
      loadClasses(),
      loadSemesters(),
      loadSubjects(),
      loadTeachers(),
      loadDepartments()
    ])
  // Nếu là giáo viên/sinh viên, load classDetail (ví dụ lấy lớp đầu tiên)
  if (isTeacher.value || isStudent.value) {
    if (classes.value.length > 0) {
      classDetail.value = { ...classes.value[0] }
    }
  }
})

const loadClasses = async () => {
  if (!canViewClasses.value) return
  try {
    loading.value = true
    const params = {}
    if (filters.status) params.status = filters.status
    if (filters.department) params.department_id = filters.department
    if (filters.semester) params.semester_id = filters.semester
    if (filters.subject) params.subject_id = filters.subject
    if (filters.global) params.search = filters.global
    const response = await api.get(endpoints.classes, { params })
    if (Array.isArray(response.data)) {
      classes.value = response.data
    } else if (response.data && response.data.results && Array.isArray(response.data.results)) {
      classes.value = response.data.results
    } else {
      classes.value = []
    }
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách lớp học', life: 3000 })
    classes.value = []
  } finally {
    loading.value = false
  }
}

const filterClasses = () => {
  loadClasses()
}

const loadSemesters = async () => {
  try {
    const response = await api.get(endpoints.semesters)
    semesters.value = Array.isArray(response.data) ? response.data : response.data.results || []
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách học kỳ', life: 3000 })
    semesters.value = []
  }
}

const loadSubjects = async () => {
  try {
    const response = await api.get(endpoints.subjects)
    subjects.value = Array.isArray(response.data) ? response.data : response.data.results || []
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách môn học', life: 3000 })
    subjects.value = []
  }
}

const loadTeachers = async () => {
  try {
    const response = await api.get(endpoints.teachers)
    teachers.value = Array.isArray(response.data) ? response.data : response.data.results || []
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách giảng viên', life: 3000 })
    teachers.value = []
  }
}

const loadDepartments = async () => {
  try {
    const response = await api.get(endpoints.departments)
    if (Array.isArray(response.data)) {
      departments.value = response.data
    } else if (response.data && response.data.results && Array.isArray(response.data.results)) {
      departments.value = response.data.results
    } else {
      departments.value = []
    }
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách khoa', life: 3000 })
    departments.value = []
  }
}

const loadActiveClasses = async () => {
  try {
    loading.value = true
    const response = await api.get('/classes/active/')
    classes.value = response.data
    toast.add({ severity: 'info', summary: 'Thành công', detail: 'Hiển thị các lớp đang hoạt động', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải lớp đang hoạt động', life: 3000 })
  } finally {
    loading.value = false
  }
}

const openNew = () => {
  classObj.value = {
    status: 'active',
    is_active: true,
    credits: 3
  }
  errors.value = {}
  submitted.value = false
  classDialog.value = true
}

const hideDialog = () => {
  classDialog.value = false
  errors.value = {}
  submitted.value = false
}

const editClass = (data) => {
  classObj.value = { ...data }
  errors.value = {}
  submitted.value = false
  classDialog.value = true
}

const confirmDelete = (data) => {
  classObj.value = { ...data }
  deleteClassDialog.value = true
}

const confirmHardDelete = (data) => {
  classObj.value = { ...data }
  hardDeleteClassDialog.value = true
}

const openChangeStatus = (data) => {
  classObj.value = { ...data }
  newStatus.value = data.status
  submitted.value = false
  changeStatusDialog.value = true
}

const validateClass = () => {
  errors.value = {}
  if (!classObj.value.class_id?.trim()) errors.value.class_id = 'Vui lòng nhập mã lớp'
  if (!classObj.value.class_name?.trim()) errors.value.class_name = 'Vui lòng nhập tên lớp'
  if (!classObj.value.credits || classObj.value.credits < 1) errors.value.credits = 'Số tín chỉ phải lớn hơn 0'
  if (!classObj.value.semester) errors.value.semester = 'Vui lòng chọn học kỳ'
  if (!classObj.value.subject) errors.value.subject = 'Vui lòng chọn môn học'
  if (!classObj.value.status) errors.value.status = 'Vui lòng chọn trạng thái'
  if (classObj.value.status === 'active' && !classObj.value.is_active) {
    errors.value.is_active = 'Lớp đang hoạt động phải có trạng thái is_active là True'
  }
}

const saveClass = async () => {
  submitted.value = true
  validateClass()
  if (Object.keys(errors.value).length > 0) return
  try {
    const payload = {
      ...classObj.value,
      teachers: classObj.value.teachers || [],
      subjects: classObj.value.subjects || []
    }
    if (classObj.value.class_id) {
      const updatedClass = (await api.patch(`${endpoints.classes}${classObj.value.class_id}/`, payload)).data
      classes.value = classes.value.map(c => c.class_id === updatedClass.class_id ? updatedClass : c)
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật lớp học thành công', life: 3000 })
    } else {
      const newClass = (await api.post(endpoints.classes, payload)).data
      classes.value.push(newClass)
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Thêm lớp học thành công', life: 3000 })
    }
    classDialog.value = false
    classObj.value = {}
  } catch (error) {
    const errorMsg = error.response?.data?.detail || Object.values(error.response?.data || {}).join(', ') || 'Không thể lưu thông tin lớp học'
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errorMsg, life: 5000 })
  }
}

const deleteClass = async () => {
  try {
    await api.delete(`${endpoints.classes}${classObj.value.class_id}/`)
    classes.value = classes.value.filter(c => c.class_id !== classObj.value.class_id)
    deleteClassDialog.value = false
    classObj.value = {}
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa mềm lớp học thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa lớp học', life: 3000 })
  }
}

const hardDeleteClass = async () => {
  try {
    await api.delete(`${endpoints.classes}${classObj.value.class_id}/hard-delete/`)
    classes.value = classes.value.filter(c => c.class_id !== classObj.value.class_id)
    hardDeleteClassDialog.value = false
    classObj.value = {}
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa hoàn toàn lớp học thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa hoàn toàn lớp học', life: 3000 })
  }
}

const changeStatus = async () => {
  submitted.value = true
  if (!newStatus.value) return
  try {
    const updatedClass = (await api.post(`${endpoints.classes}${classObj.value.class_id}/change-status/`, { status: newStatus.value })).data
    classes.value = classes.value.map(c => c.class_id === updatedClass.class_id ? updatedClass : c)
    changeStatusDialog.value = false
    classObj.value = {}
    newStatus.value = ''
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật trạng thái thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể cập nhật trạng thái', life: 3000 })
  }
}

const restoreClass = async (data) => {
  try {
    const response = await api.post(`${endpoints.classes}${data.class_id}/restore/`)
    toast.add({ severity: 'success', summary: 'Thành công', detail: response.data.message || 'Khôi phục lớp học thành công', life: 3000 })
    await loadClasses()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể khôi phục lớp học', life: 3000 })
  }
}

const openEdit = () => {
  isEditing.value = true
  errors.value = {}
}

const cancelEdit = () => {
  isEditing.value = false
  // reload lại classDetail nếu cần
}

const saveClassDetail = async () => {
  // Tương tự saveClass nhưng cho classDetail
  try {
    // validate và gửi API update
    // ...
    isEditing.value = false
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật thông tin lớp thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể cập nhật thông tin lớp', life: 3000 })
  }
}

const exportClasses = async () => {
  try {
    const response = await api.get(`${endpoints.classes}export/`, { responseType: 'blob' })
    const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    saveAs(blob, `classes_${new Date().toISOString().split('T')[0]}.xlsx`)
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xuất danh sách lớp học thành công', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xuất danh sách lớp học', life: 3000 })
  }
}

const getStatusLabel = (status) => {
  const map = {
    active: 'Đang hoạt động',
    inactive: 'Không hoạt động',
    pending: 'Đang chờ duyệt',
  }
  return map[status] || status
}

const getStatusSeverity = (status) => {
  const map = {
    active: 'success',
    inactive: 'warning',
    pending: 'info',
  }
  return map[status] || 'info'
}
</script>

<style scoped>
.card, .content {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(44, 62, 80, 0.08);
  padding: 2rem;
  margin-bottom: 2rem;
  width: 200%;
}
.header, .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}
.header h2, .card-header h3 {
  font-size: 1.6rem;
  color: #2c3e50;
  margin: 0;
  font-weight: 700;
}
.action-buttons {
  display: flex;
  gap: 0.75rem;
}
.filter-bar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}
.filter-group {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.filter-dropdown {
  width: 200px;
}
.filter-search {
  width: 250px;
}
.empty-message, .loading-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 2rem;
  color: #666;
  font-size: 1.1rem;
}
@media (max-width: 768px) {
  .card, .content {
    padding: 1rem;
  }
  .header h2, .card-header h3 {
    font-size: 1.2rem;
  }
  .filter-search, .filter-dropdown {
    width: 100%;
  }
}
.profile-section {
  max-width: 1600px;
  margin: 0 auto;
}
.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}
.profile-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
}
.detail-item {
  padding: 0.5rem;
}
.detail-item label {
  font-weight: bold;
  margin-right: 0.5rem;
}
.edit-form {
  display: grid;
  gap: 2rem;
}
.field {
  display: flex;
  flex-direction: column;
}
.buttons {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}
.confirmation-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.access-denied {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #ef4444;
}
.no-data-message {
  text-align: center;
  padding: 3rem;
  color: #666;
  background: #f8f9fa;
  border-radius: 8px;
  margin: 1rem 0;
  font-size: 1.6rem;
}
.no-data-message p {
  margin-bottom: 1rem;
  font-size: 1.1rem;
}
.action-buttons, .p-datatable-sm :deep(td .p-button) {
  gap: 0.25rem !important;
}
.p-datatable-sm :deep(td .p-button) {
  min-width: 28px !important;
  height: 28px !important;
  width: 28px !important;
  padding: 0 !important;
  font-size: 0.9rem !important;
  border-radius: 50% !important;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.p-datatable-sm :deep(td .p-button .pi) {
  font-size: 0.9rem !important;
}
.p-datatable-sm :deep(td .p-button:hover) {
  box-shadow: 0 0 0 2px #c7d2fe;
}
.p-datatable-sm :deep(td .p-button + .p-button) {
  margin-left: 0.15rem !important;
}
.p-datatable-sm :deep(td .p-button) {
  margin-right: 0.25rem !important;
}
.p-datatable-sm :deep(td .p-button:last-child) {
  margin-right: 0 !important;
}
@media (max-width: 768px) {
  .p-datatable-sm :deep(td .p-button) {
    min-width: 24px !important;
    height: 24px !important;
    width: 24px !important;
    font-size: 0.8rem !important;
  }
}
.p-datatable-sm :deep(.p-datatable-tbody > tr > td),
.p-datatable-sm :deep(.p-datatable-thead > tr > th) {
  padding: 0.85rem 1.1rem;
}
.p-datatable-sm :deep(.p-datatable-thead > tr > th) {
  background: #f8f9fa;
  font-size: 1rem;
  border-right: 1px solid #f1f1f1;
}
.p-datatable-sm :deep(.p-datatable-tbody > tr > td) {
  border-right: 1px solid #f4f4f4;
}
.p-datatable-sm :deep(.p-datatable-tbody > tr > td:last-child),
.p-datatable-sm :deep(.p-datatable-thead > tr > th:last-child) {
  border-right: none;
}
@media (max-width: 768px) {
  .p-datatable-sm :deep(td),
  .p-datatable-sm :deep(th) {
    padding: 0.5em 0.4em;
  }
}
</style>