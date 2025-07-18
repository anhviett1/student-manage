<template>
  <div class="student-management-section" aria-label="Phần quản lý sinh viên">
    <Toast aria-live="polite" />
    <ConfirmDialog aria-live="assertive" />
    <Toolbar class="toolbar">
      <template #start>
        <h2>Quản Lý Sinh Viên</h2>
      </template>
      <template #end>
        <Button
          v-if="canEditStudents"
          icon="pi pi-plus"
          label="Thêm Sinh Viên"
          severity="primary"
          class="mr-2"
          @click="openNew"
          v-tooltip="'Thêm sinh viên mới'"
          aria-label="Thêm sinh viên mới"
        />
        <Button
          v-if="canExportData"
          icon="pi pi-download"
          label="Export"
          severity="success"
          @click="exportStudents"
          v-tooltip="'Xuất danh sách sinh viên'"
          aria-label="Xuất danh sách sinh viên"
        />
      </template>
    </Toolbar>
    <div class="filter-bar">
      <Dropdown
        v-model="filters.status"
        :options="statusOptions"
        optionLabel="label"
        optionValue="value"
        placeholder="Lọc trạng thái"
        class="filter-dropdown mr-2"
        @change="emit('loadStudents', 1, paginatorInfo.rows)"
        aria-label="Lọc theo trạng thái"
      />
      <Dropdown
        v-model="filters.department"
        :options="departments"
        optionLabel="name"
        optionValue="id"
        placeholder="Lọc khoa"
        class="filter-dropdown mr-2"
        @change="emit('loadStudents', 1, paginatorInfo.rows)"
        aria-label="Lọc theo khoa"
      />
      <InputText
        v-model="filters.global"
        placeholder="Tìm mã, tên, email..."
        class="filter-search"
        @input="debouncedLoadStudents"
        aria-label="Tìm kiếm sinh viên"
      />
    </div>
    <DataTable
      v-if="students.length > 0 || loading"
      :value="students"
      :loading="loading"
      dataKey="id"
      lazy
      :paginator="true"
      :rows="paginatorInfo.rows"
      :rowsPerPageOptions="[5, 10, 20]"
      :totalRecords="paginatorInfo.total"
      @page="onPage"
      class="p-datatable-sm"
      aria-label="Bảng quản lý sinh viên"
    >
      <template #empty>
        <div class="empty-message"><i class="pi pi-info-circle" /><span>Không tìm thấy sinh viên nào.</span></div>
      </template>
      <template #loading>
        <div class="loading-message"><ProgressSpinner style="width: 24px; height: 24px;" /><span>Đang tải dữ liệu...</span></div>
      </template>
      <Column field="student_id" header="Mã Sinh Viên" sortable style="width: 12%" />
      <Column field="full_name" header="Họ và Tên" sortable style="width: 18%" />
      <Column field="email" header="Email" sortable style="width: 18%" />
      <Column field="major" header="Chuyên Ngành" sortable style="width: 15%" />
      <Column field="gpa" header="GPA" sortable style="width: 8%" align="center" />
      <Column field="status" header="Trạng Thái" sortable style="width: 12%" align="center">
        <template #body="{ data }"><Tag :severity="getStatusSeverity(data.status)" :value="getStatusLabel(data.status)" /></template>
      </Column>
      <Column field="is_active" header="Hoạt Động" sortable style="width: 10%" align="center">
        <template #body="{ data }"><Tag :severity="data.is_active ? 'success' : 'warning'" :value="data.is_active ? 'Active' : 'Inactive'" /></template>
      </Column>
      <Column header="Hành Động" style="width: 15%" align="center">
        <template #body="{ data }">
          <Button
            v-if="canEditStudents && !data.is_deleted"
            icon="pi pi-pencil"
            outlined
            rounded
            class="mr-2"
            severity="info"
            @click="editStudent(data)"
            v-tooltip="'Sửa thông tin'"
            aria-label="Sửa thông tin sinh viên"
          />
          <Button
            v-if="canDeleteStudents && !data.is_deleted"
            icon="pi pi-trash"
            outlined
            rounded
            severity="danger"
            class="mr-2"
            @click="confirmDelete(data)"
            v-tooltip="'Xóa mềm'"
            aria-label="Xóa mềm sinh viên"
          />
          <Button
            v-if="canDeleteStudents && data.is_deleted"
            icon="pi pi-undo"
            outlined
            rounded
            severity="success"
            @click="confirmRestore(data)"
            v-tooltip="'Khôi phục'"
            aria-label="Khôi phục sinh viên"
          />
          <Button
            icon="pi pi-refresh"
            outlined
            rounded
            severity="secondary"
            @click="openChangeStatus(data)"
            v-tooltip="'Thay đổi trạng thái'"
            aria-label="Thay đổi trạng thái sinh viên"
          />
        </template>
      </Column>
    </DataTable>
    <div v-else-if="!loading && students.length === 0" class="no-data-message">
      <p>Không có dữ liệu sinh viên để hiển thị.</p>
      <Button label="Tải lại" icon="pi pi-refresh" @click="emit('loadStudents', 1, paginatorInfo.rows)" severity="secondary" aria-label="Tải lại danh sách sinh viên" />
    </div>
    <Dialog
      v-model:visible="studentDialog"
      :header="student.id ? 'Sửa Sinh Viên' : 'Thêm Sinh Viên'"
      modal
      class="p-fluid"
      style="width: 600px;"
      aria-labelledby="student-dialog-header"
    >
      <h3 id="student-dialog-header" class="sr-only">{{ student.id ? 'Sửa Sinh Viên' : 'Thêm Sinh Viên' }}</h3>
      <div class="form-section">
        <h4>Thông Tin Cơ Bản</h4>
        <div class="field">
          <label for="student_id">Mã Sinh Viên</label>
          <InputText id="student_id" v-model="student.student_id" :disabled="!!student.id" :class="{ 'p-invalid': errors.student_id }" />
          <small class="p-error" v-if="errors.student_id">{{ errors.student_id }}</small>
        </div>
        <div class="field">
          <label for="first_name">Tên</label>
          <InputText id="first_name" v-model="student.first_name" :class="{ 'p-invalid': errors.first_name }" />
          <small class="p-error" v-if="errors.first_name">{{ errors.first_name }}</small>
        </div>
        <div class="field">
          <label for="last_name">Họ</label>
          <InputText id="last_name" v-model="student.last_name" :class="{ 'p-invalid': errors.last_name }" />
          <small class="p-error" v-if="errors.last_name">{{ errors.last_name }}</small>
        </div>
        <div class="field">
          <label for="email">Email</label>
          <InputText id="email" v-model="student.email" :class="{ 'p-invalid': errors.email }" />
          <small class="p-error" v-if="errors.email">{{ errors.email }}</small>
        </div>
        <div class="field">
          <label for="phone">Số Điện Thoại</label>
          <InputText id="phone" v-model="student.phone" :class="{ 'p-invalid': errors.phone }" />
          <small class="p-error" v-if="errors.phone">{{ errors.phone }}</small>
        </div>
        <div class="field">
          <label for="date_of_birth">Ngày Sinh</label>
          <Calendar id="date_of_birth" v-model="student.date_of_birth" :showIcon="true" dateFormat="yy-mm-dd" :class="{ 'p-invalid': errors.date_of_birth }" />
          <small class="p-error" v-if="errors.date_of_birth">{{ errors.date_of_birth }}</small>
        </div>
        <div class="field">
          <label for="gender">Giới Tính</label>
          <Dropdown id="gender" v-model="student.gender" :options="genderOptions" optionLabel="label" optionValue="value" :class="{ 'p-invalid': errors.gender }" />
          <small class="p-error" v-if="errors.gender">{{ errors.gender }}</small>
        </div>
        <div class="field">
          <label for="address">Địa Chỉ</label>
          <Textarea id="address" v-model="student.address" rows="3" :class="{ 'p-invalid': errors.address }" />
          <small class="p-error" v-if="errors.address">{{ errors.address }}</small>
        </div>
        <div class="field">
          <label for="city">Thành Phố</label>
          <InputText id="city" v-model="student.city" :class="{ 'p-invalid': errors.city }" />
          <small class="p-error" v-if="errors.city">{{ errors.city }}</small>
        </div>
        <div class="field">
          <label for="state">Tỉnh/Thành</label>
          <InputText id="state" v-model="student.state" :class="{ 'p-invalid': errors.state }" />
          <small class="p-error" v-if="errors.state">{{ errors.state }}</small>
        </div>
        <div class="field">
          <label for="country">Quốc Gia</label>
          <InputText id="country" v-model="student.country" :class="{ 'p-invalid': errors.country }" />
          <small class="p-error" v-if="errors.country">{{ errors.country }}</small>
        </div>
      </div>
      <div class="form-section">
        <h4>Thông Tin Học Tập</h4>
        <div class="field">
          <label for="enrollment_date">Ngày Nhập Học</label>
          <Calendar id="enrollment_date" v-model="student.enrollment_date" :showIcon="true" dateFormat="yy-mm-dd" :class="{ 'p-invalid': errors.enrollment_date }" />
          <small class="p-error" v-if="errors.enrollment_date">{{ errors.enrollment_date }}</small>
        </div>
        <div class="field">
          <label for="graduation_date">Ngày Tốt Nghiệp</label>
          <Calendar id="graduation_date" v-model="student.graduation_date" :showIcon="true" dateFormat="yy-mm-dd" :class="{ 'p-invalid': errors.graduation_date }" />
          <small class="p-error" v-if="errors.graduation_date">{{ errors.graduation_date }}</small>
        </div>
        <div class="field">
          <label for="status">Trạng Thái</label>
          <Dropdown id="status" v-model="student.status" :options="statusOptions" optionLabel="label" optionValue="value" :class="{ 'p-invalid': errors.status }" />
          <small class="p-error" v-if="errors.status">{{ errors.status }}</small>
        </div>
        <div class="field">
          <label for="major">Chuyên Ngành</label>
          <InputText id="major" v-model="student.major" :class="{ 'p-invalid': errors.major }" />
          <small class="p-error" v-if="errors.major">{{ errors.major }}</small>
        </div>
        <div class="field">
          <label for="minor">Chuyên Ngành Phụ</label>
          <InputText id="minor" v-model="student.minor" />
        </div>
        <div class="field">
          <label for="department">Khoa</label>
          <Dropdown id="department" v-model="student.department_id" :options="departments" optionLabel="name" optionValue="id" :class="{ 'p-invalid': errors.department_id }" />
          <small class="p-error" v-if="errors.department_id">{{ errors.department_id }}</small>
        </div>
      </div>
      <div class="form-section">
        <h4>Thông Tin Liên Hệ Khẩn Cấp</h4>
        <div class="field">
          <label for="emergency_contact_name">Người Liên Hệ</label>
          <InputText id="emergency_contact_name" v-model="student.emergency_contact_name" :class="{ 'p-invalid': errors.emergency_contact_name }" />
          <small class="p-error" v-if="errors.emergency_contact_name">{{ errors.emergency_contact_name }}</small>
        </div>
        <div class="field">
          <label for="emergency_contact_phone">Số Điện Thoại</label>
          <InputText id="emergency_contact_phone" v-model="student.emergency_contact_phone" :class="{ 'p-invalid': errors.emergency_contact_phone }" />
          <small class="p-error" v-if="errors.emergency_contact_phone">{{ errors.emergency_contact_phone }}</small>
        </div>
        <div class="field">
          <label for="emergency_contact_relationship">Mối Quan Hệ</label>
          <InputText id="emergency_contact_relationship" v-model="student.emergency_contact_relationship" :class="{ 'p-invalid': errors.emergency_contact_relationship }" />
          <small class="p-error" v-if="errors.emergency_contact_relationship">{{ errors.emergency_contact_relationship }}</small>
        </div>
      </div>
      <div class="form-section">
        <h4>Thông Tin Khác</h4>
        <div class="field">
          <label for="profile_picture">Ảnh Đại Diện</label>
          <FileUpload
            id="profile_picture"
            mode="basic"
            accept="image/jpeg,image/png"
            :maxFileSize="2000000"
            @select="handleFileUpload"
            :class="{ 'p-invalid': errors.profile_picture }"
            aria-label="Tải lên ảnh đại diện"
          />
          <small class="p-error" v-if="errors.profile_picture">{{ errors.profile_picture }}</small>
        </div>
        <div class="field">
          <label for="student_id_card">Mã Thẻ Sinh Viên</label>
          <InputText id="student_id_card" v-model="student.student_id_card" :class="{ 'p-invalid': errors.student_id_card }" />
          <small class="p-error" v-if="errors.student_id_card">{{ errors.student_id_card }}</small>
        </div>
        <div class="field">
          <label for="blood_type">Nhóm Máu</label>
          <InputText id="blood_type" v-model="student.blood_type" />
        </div>
        <div class="field">
          <label for="medical_conditions">Tình Trạng Sức Khỏe</label>
          <Textarea id="medical_conditions" v-model="student.medical_conditions" rows="3" />
        </div>
        <div class="field">
          <label for="allergies">Dị Ứng</label>
          <Textarea id="allergies" v-model="student.allergies" rows="3" />
        </div>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="hideDialog" aria-label="Hủy" />
        <Button label="Lưu" icon="pi pi-check" @click="saveStudent" aria-label="Lưu sinh viên" />
      </template>
    </Dialog>
    <Dialog
      v-model:visible="deleteDialog"
      header="Xác Nhận Xóa"
      modal
      style="width: 400px;"
      aria-labelledby="delete-dialog-header"
    >
      <h3 id="delete-dialog-header" class="sr-only">Xác Nhận Xóa</h3>
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span v-if="student">Bạn có chắc muốn xóa sinh viên <b>{{ student.full_name }}</b>?</span>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="deleteDialog = false" aria-label="Hủy" />
        <Button label="Xóa" icon="pi pi-check" severity="danger" @click="deleteStudent" aria-label="Xóa sinh viên" />
      </template>
    </Dialog>
    <Dialog
      v-model:visible="changeStatusDialog"
      header="Thay Đổi Trạng Thái"
      modal
      style="width: 400px;"
      aria-labelledby="change-status-dialog-header"
    >
      <h3 id="change-status-dialog-header" class="sr-only">Thay Đổi Trạng Thái</h3>
      <div class="field">
        <label for="new_status">Trạng Thái Mới</label>
        <Dropdown
          id="new_status"
          v-model="newStatus"
          :options="statusOptions"
          optionLabel="label"
          optionValue="value"
          placeholder="Chọn trạng thái"
          :class="{ 'p-invalid': submitted && !newStatus }"
        />
        <small class="p-error" v-if="submitted && !newStatus">Vui lòng chọn trạng thái mới.</small>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="changeStatusDialog = false" aria-label="Hủy" />
        <Button label="Cập Nhật" icon="pi pi-check" @click="changeStatus" aria-label="Cập nhật trạng thái" />
      </template>
    </Dialog>
    <Dialog
      v-model:visible="restoreDialog"
      header="Xác Nhận Khôi Phục"
      modal
      style="width: 400px;"
      aria-labelledby="restore-dialog-header"
    >
      <h3 id="restore-dialog-header" class="sr-only">Xác Nhận Khôi Phục</h3>
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span v-if="student">Bạn có chắc muốn khôi phục sinh viên <b>{{ student.full_name }}</b>?</span>
      </div>
      <template #footer>
        <Button label="Hủy" icon="pi pi-times" text @click="restoreDialog = false" aria-label="Hủy" />
        <Button label="Khôi phục" icon="pi pi-check" severity="success" @click="restoreStudent" aria-label="Khôi phục sinh viên" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useUserStore } from '@/stores/user';
import { useToast } from 'primevue/usetoast';
import { debounce } from 'lodash';
import { saveAs } from 'file-saver';
import Toolbar from 'primevue/toolbar';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';
import Dropdown from 'primevue/dropdown';
import Calendar from 'primevue/calendar';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Tag from 'primevue/tag';
import Dialog from 'primevue/dialog';
import ProgressSpinner from 'primevue/progressspinner';
import ConfirmDialog from 'primevue/confirmdialog';
import FileUpload from 'primevue/fileupload';
import Toast from 'primevue/toast';
import api, { endpoints } from '@/services/api';

const props = defineProps({
  students: { type: Array, required: true },
  filters: { type: Object, required: true },
  paginatorInfo: { type: Object, required: true },
  departments: { type: Array, required: true },
});
const emit = defineEmits(['update:students', 'loadStudents', 'loadDepartments']);

const userStore = useUserStore();
const toast = useToast();

const student = ref({
  student_id: '',
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  date_of_birth: null,
  gender: 'M',
  address: '',
  city: '',
  state: '',
  country: '',
  enrollment_date: new Date(),
  graduation_date: null,
  status: 'active',
  major: '',
  minor: '',
  emergency_contact_name: '',
  emergency_contact_phone: '',
  emergency_contact_relationship: '',
  student_id_card: '',
  blood_type: '',
  medical_conditions: '',
  allergies: '',
  department_id: null,
  is_active: true,
});
const studentDialog = ref(false);
const deleteDialog = ref(false);
const changeStatusDialog = ref(false);
const restoreDialog = ref(false);
const newStatus = ref('');
const submitted = ref(false);
const loading = ref(false);
const errors = ref({});

const genderOptions = [
  { label: 'Nam', value: 'M' },
  { label: 'Nữ', value: 'F' },
  { label: 'Khác', value: 'O' },
];

const statusOptions = [
  { label: 'Đang học', value: 'active' },
  { label: 'Tạm nghỉ', value: 'inactive' },
  { label: 'Đã tốt nghiệp', value: 'graduated' },
  { label: 'Bị đình chỉ', value: 'suspended' },
  { label: 'Nghỉ phép', value: 'on_leave' },
];

const canEditStudents = computed(() => userStore.isAdmin);
const canDeleteStudents = computed(() => userStore.isAdmin);
const canExportData = computed(() => userStore.isAdmin || userStore.isTeacher);

const debouncedLoadStudents = debounce(() => emit('loadStudents', 1, props.paginatorInfo.rows), 500);

onMounted(() => {
  gsap.from('.student-management-section', { opacity: 0, y: 20, duration: 0.5 });
});

const onPage = (event) => {
  emit('loadStudents', event.page + 1, event.rows);
};

const openNew = () => {
  student.value = {
    student_id: '',
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    date_of_birth: null,
    gender: 'M',
    address: '',
    city: '',
    state: '',
    country: '',
    enrollment_date: new Date(),
    graduation_date: null,
    status: 'active',
    major: '',
    minor: '',
    emergency_contact_name: '',
    emergency_contact_phone: '',
    emergency_contact_relationship: '',
    student_id_card: '',
    blood_type: '',
    medical_conditions: '',
    allergies: '',
    department_id: null,
    is_active: true,
  };
  errors.value = {};
  studentDialog.value = true;
};

const editStudent = (data) => {
  student.value = {
    ...data,
    date_of_birth: data.date_of_birth ? new Date(data.date_of_birth) : null,
    enrollment_date: data.enrollment_date ? new Date(data.enrollment_date) : null,
    graduation_date: data.graduation_date ? new Date(data.graduation_date) : null,
  };
  errors.value = {};
  studentDialog.value = true;
};

const confirmDelete = (data) => {
  student.value = { ...data };
  deleteDialog.value = true;
};

const confirmRestore = (data) => {
  student.value = { ...data };
  restoreDialog.value = true;
};

const openChangeStatus = (data) => {
  student.value = { ...data };
  newStatus.value = data.status;
  submitted.value = false;
  changeStatusDialog.value = true;
};

const hideDialog = () => {
  studentDialog.value = false;
  errors.value = {};
  student.value = {
    student_id: '',
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    date_of_birth: null,
    gender: 'M',
    address: '',
    city: '',
    state: '',
    country: '',
    enrollment_date: new Date(),
    graduation_date: null,
    status: 'active',
    major: '',
    minor: '',
    emergency_contact_name: '',
    emergency_contact_phone: '',
    emergency_contact_relationship: '',
    student_id_card: '',
    blood_type: '',
    medical_conditions: '',
    allergies: '',
    department_id: null,
    is_active: true,
  };
};

const validateStudent = () => {
  errors.value = {};
  if (!student.value.student_id?.trim()) errors.value.student_id = 'Vui lòng nhập mã sinh viên';
  if (!student.value.first_name?.trim()) errors.value.first_name = 'Vui lòng nhập tên';
  if (!student.value.last_name?.trim()) errors.value.last_name = 'Vui lòng nhập họ';
  if (!student.value.email?.trim()) errors.value.email = 'Vui lòng nhập email';
  else if (!/\S+@\S+\.\S+/.test(student.value.email)) errors.value.email = 'Email không hợp lệ';
  if (student.value.phone && !/^\d{10,11}$/.test(student.value.phone)) errors.value.phone = 'Số điện thoại không hợp lệ';
  if (!student.value.date_of_birth) errors.value.date_of_birth = 'Vui lòng chọn ngày sinh';
  if (!student.value.gender) errors.value.gender = 'Vui lòng chọn giới tính';
  if (!student.value.address?.trim()) errors.value.address = 'Vui lòng nhập địa chỉ';
  if (!student.value.city?.trim()) errors.value.city = 'Vui lòng nhập thành phố';
  if (!student.value.state?.trim()) errors.value.state = 'Vui lòng nhập tỉnh/thành';
  if (!student.value.country?.trim()) errors.value.country = 'Vui lòng nhập quốc gia';
  if (!student.value.enrollment_date) errors.value.enrollment_date = 'Vui lòng chọn ngày nhập học';
  if (!student.value.status) errors.value.status = 'Vui lòng chọn trạng thái';
  if (!student.value.major?.trim()) errors.value.major = 'Vui lòng nhập chuyên ngành';
  if (!student.value.department_id) errors.value.department_id = 'Vui lòng chọn khoa';
  if (!student.value.emergency_contact_name?.trim()) errors.value.emergency_contact_name = 'Vui lòng nhập tên người liên hệ';
  if (!student.value.emergency_contact_phone?.trim()) errors.value.emergency_contact_phone = 'Vui lòng nhập số điện thoại liên hệ';
  else if (!/^\d{10,11}$/.test(student.value.emergency_contact_phone)) errors.value.emergency_contact_phone = 'Số điện thoại liên hệ không hợp lệ';
  if (!student.value.emergency_contact_relationship?.trim()) errors.value.emergency_contact_relationship = 'Vui lòng nhập mối quan hệ';
  if (!student.value.student_id_card?.trim()) errors.value.student_id_card = 'Vui lòng nhập mã thẻ sinh viên';
};

const saveStudent = async () => {
  validateStudent();
  if (Object.keys(errors.value).length > 0) return;
  try {
    const formData = new FormData();
    Object.keys(student.value).forEach((key) => {
      if (student.value[key] !== null && student.value[key] !== undefined) {
        if (['date_of_birth', 'enrollment_date', 'graduation_date'].includes(key) && student.value[key]) {
          formData.append(key, student.value[key].toISOString().split('T')[0]);
        } else {
          formData.append(key, student.value[key]);
        }
      }
    });
    let updatedStudents;
    if (student.value.id) {
      const response = await api.put(`${endpoints.students}${student.value.id}/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      updatedStudents = props.students.map(s => s.id === student.value.id ? response.data : s);
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật sinh viên thành công', life: 3000 });
    } else {
      const response = await api.post(endpoints.students, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      updatedStudents = [...props.students, response.data];
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Thêm sinh viên thành công', life: 3000 });
    }
    emit('update:students', updatedStudents);
    hideDialog();
  } catch (error) {
    const errorMsg = error.response?.data?.detail || Object.values(error.response?.data || {}).join(', ') || 'Không thể lưu sinh viên';
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errorMsg, life: 3000 });
  }
};

const deleteStudent = async () => {
  try {
    await api.delete(`${endpoints.students}${student.value.id}/`);
    const updatedStudents = props.students.filter(s => s.id !== student.value.id);
    emit('update:students', updatedStudents);
    deleteDialog.value = false;
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa sinh viên thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xóa sinh viên', life: 3000 });
  }
};

const restoreStudent = async () => {
  try {
    const response = await api.post(`${endpoints.students}${student.value.id}/restore/`);
    const updatedStudents = props.students.map(s => s.id === student.value.id ? response.data : s);
    emit('update:students', updatedStudents);
    restoreDialog.value = false;
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Khôi phục sinh viên thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: error.response?.data?.error || 'Không thể khôi phục sinh viên', life: 3000 });
  }
};

const changeStatus = async () => {
  submitted.value = true;
  if (!newStatus.value) return;
  try {
    const response = await api.post(`${endpoints.students}${student.value.id}/change-status/`, { status: newStatus.value });
    const updatedStudents = props.students.map(s => s.id === student.value.id ? response.data : s);
    emit('update:students', updatedStudents);
    changeStatusDialog.value = false;
    newStatus.value = '';
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật trạng thái thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể cập nhật trạng thái', life: 3000 });
  }
};

const exportStudents = async () => {
  try {
    const response = await api.get(`${endpoints.students}export/`, { responseType: 'blob' });
    const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
    saveAs(blob, `students_${new Date().toISOString().split('T')[0]}.xlsx`);
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xuất danh sách sinh viên thành công', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể xuất danh sách sinh viên', life: 3000 });
  }
};

const handleFileUpload = (event) => {
  const file = event.files[0];
  if (file) {
    student.value.profile_picture = file;
  }
};

const formatDate = (date) => {
  if (!date) return 'Chưa cập nhật';
  return new Date(date).toLocaleDateString('vi-VN', { year: 'numeric', month: '2-digit', day: '2-digit' });
};

const getStatusLabel = (status) => {
  const map = {
    active: 'Đang học',
    inactive: 'Tạm nghỉ',
    graduated: 'Đã tốt nghiệp',
    suspended: 'Bị đình chỉ',
    on_leave: 'Nghỉ phép',
  };
  return map[status] || status;
};

const getStatusSeverity = (status) => {
  const map = {
    active: 'success',
    inactive: 'warning',
    graduated: 'info',
    suspended: 'danger',
    on_leave: 'secondary',
  };
  return map[status] || 'info';
};
</script>

<style scoped>
.student-management-section {
  padding: 24px;
}
.toolbar {
  margin-bottom: 16px;
}
.filter-bar {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}
.filter-dropdown {
  width: 200px;
}
.filter-search {
  width: 250px;
  padding: 8px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
}
.empty-message, .loading-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px;
  color: #6b7280;
}
.no-data-message {
  text-align: center;
  padding: 48px;
  color: #6b7280;
  background: #f8f9fa;
  border-radius: 8px;
  margin: 16px 0;
}
.form-section {
  margin-bottom: 24px;
}
.form-section h4 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 16px;
}
.field {
  margin-bottom: 16px;
}
.field label {
  font-weight: 500;
  margin-bottom: 4px;
  color: #374151;
}
.field .p-error {
  font-size: 12px;
  color: #ef4444;
}
.confirmation-content {
  display: flex;
  align-items: center;
  gap: 12px;
}
.p-datatable-sm :deep(.p-datatable-tbody > tr > td),
.p-datatable-sm :deep(.p-datatable-thead > tr > th) {
  padding: 12px;
}
.p-datatable-sm :deep(.p-datatable-thead > tr > th) {
  background: #f8f9fa;
  font-size: 14px;
  font-weight: 500;
}
.p-datatable-sm :deep(.p-button) {
  width: 28px;
  height: 28px;
  padding: 0;
  font-size: 14px;
}
</style>