<template>
  <div class="profile-container card">
    <Toast />
    <ConfirmDialog />
    
    <!-- Show ChangePasswordView when on change-password route -->
    <router-view v-if="$route.name === 'profile-change-password'" />
    
    <!-- Show main profile content when not on change-password route -->
    <template v-else>
      <!-- Admin Navigation Tabs -->
      <div v-if="userRole === 'admin'" class="admin-tabs">
        <TabView v-model:activeIndex="activeTabIndex">
          <TabPanel header="Hồ Sơ Cá Nhân">
            <div class="profile-content">
              <div class="card-header">
                <h2>Thông Tin Cá Nhân</h2>
                <div class="header-buttons">
                  <Button
                    :label="isEditMode ? 'Chế độ Xem' : 'Chỉnh sửa'"
                    :icon="isEditMode ? 'pi pi-eye' : 'pi pi-pencil'"
                    :severity="isEditMode ? 'secondary' : 'primary'"
                    @click="handleProfileViewEditClick"
                    class="mode-toggle-button"
                    :disabled="!canEditProfile"
                  />
                  <Button
                    label="Đổi mật khẩu"
                    icon="pi pi-key"
                    severity="warning"
                    @click="navigateToChangePassword"
                    class="mode-toggle-button"
                  />
                </div>
              </div>

              <template v-if="!showFieldConfig && !showUserTable">
                <div class="avatar-section">
                  <div class="avatar-wrapper" @click="canUploadAvatar && isEditMode ? triggerFileInput() : null">
                    <img
                      v-if="userProfile.profile_picture"
                      :src="userProfile.profile_picture"
                      alt="Avatar"
                      class="avatar-preview"
                    />
                    <img
                      v-else-if="userRole === 'admin' && adminDefaultImg"
                      :src="adminDefaultImg"
                      alt="Admin Default"
                      class="avatar-preview"
                    />
                    <div v-else class="avatar-placeholder">Không có ảnh</div>
                    <input
                      ref="fileInput"
                      type="file"
                      accept="image/*"
                      style="display:none"
                      @change="onFileChange"
                    />
                  </div>
                </div>

                <Dialog v-model:visible="showCropper" header="Cắt ảnh đại diện" modal>
                  <Cropper
                    v-if="tempImage"
                    :src="tempImage"
                    :stencil-props="{ aspectRatio: 1 }"
                    :autoZoom="true"
                    :stencil-component="'circle-stencil'"
                    @change="onCrop"
                  />
                  <template #footer>
                    <Button label="Hủy" @click="showCropper = false" />
                    <Button label="Lưu" @click="saveCroppedImage" />
                  </template>
                </Dialog>

                <table class="profile-table">
                  <tbody>
                    <tr v-for="(value, key) in filteredUserProfile" :key="key">
                      <td class="profile-key">{{ getFieldLabel(key) }}</td>
                      <td class="profile-value">
                        <template v-if="isEditable(key) && isEditMode">
                          <component
                            :is="getInputComponent(key)"
                            v-model="editProfile[key]"
                            v-bind="getInputProps(key, value)"
                          />
                        </template>
                        <template v-else>
                          <span v-if="isObject(value)">{{ formatObjectValue(key, value) }}</span>
                          <span v-else-if="key === 'password'">
                            <div class="password-display">
                              <span>{{ showPassword ? (userProfile.password || '••••••••') : '••••••••' }}</span>
                              <Button
                                :icon="showPassword ? 'pi pi-eye-slash' : 'pi pi-eye'"
                                text
                                size="small"
                                @click="togglePasswordVisibility"
                                class="password-toggle-btn"
                              />
                            </div>
                          </span>
                          <span v-else>{{ formatValue(key, value) }}</span>
                        </template>
                        <small class="field-description">{{ getFieldDescription(key) }}</small>
                      </td>
                    </tr>
                  </tbody>
                </table>

                <div class="form-actions" v-if="isEditMode">
                  <Button
                    type="submit"
                    label="Lưu"
                    icon="pi pi-check"
                    :loading="isLoading"
                    @click="updateProfile"
                    class="submit-button"
                    :disabled="!canEditProfile"
                  />
                </div>
              </template>
            </div>
          </TabPanel>

          <TabPanel header="Quản Lý Người Dùng">
            <div class="user-management-content">
              <div class="header">
                <h2>Quản Lý Người Dùng</h2>
                <Button
                  icon="pi pi-plus"
                  label="Thêm Người Dùng"
                  severity="primary"
                  @click="openNewUser"
                  v-tooltip="'Thêm người dùng mới'"
                />
              </div>

              <div class="filter-bar">
                <div class="filter-group">
                  <Dropdown
                    v-model="userFilters.role"
                    :options="roleOptions"
                    optionLabel="label"
                    optionValue="value"
                    placeholder="Lọc theo vai trò"
                    class="filter-dropdown"
                    showClear
                    @change="loadUsers"
                  />
                  <InputText
                    v-model="userFilters.search"
                    placeholder="Tìm theo tên, email..."
                    class="filter-search"
                    @input="onSearchInput"
                  />
                </div>
              </div>

              <DataTable
                v-if="usersList.length > 0 || userStore.isLoading"
                :value="usersList"
                :loading="userStore.isLoading"
                dataKey="id"
                paginator
                :rows="10"
                :rowsPerPageOptions="[5, 10, 20]"
                responsiveLayout="scroll"
                class="p-datatable-sm"
              >
                <template #empty>
                  <div class="empty-message">Không tìm thấy người dùng nào.</div>
                </template>
                <template #loading>
                  <div class="loading-message">Đang tải dữ liệu...</div>
                </template>
                <Column field="id" header="ID" sortable style="width: 8%" />
                <Column field="username" header="Tên Đăng Nhập" sortable style="width: 20%" />
                <Column field="email" header="Email" sortable style="width: 25%" />
                <Column field="role" header="Vai Trò" sortable style="width: 15%">
                  <template #body="{ data }">
                    <Tag :severity="getRoleSeverity(data.role)" :value="data.role" />
                  </template>
                </Column>
                <Column field="is_active" header="Trạng Thái" sortable style="width: 12%">
                  <template #body="{ data }">
                    <Tag :severity="data.is_active ? 'success' : 'danger'" :value="data.is_active ? 'Active' : 'Inactive'" />
                  </template>
                </Column>
                <Column header="Hành Động" style="width: 15%" align="center">
                  <template #body="{ data }">
                    <Button
                      icon="pi pi-pencil"
                      outlined
                      rounded
                      severity="info"
                      @click="editUser(data)"
                      v-tooltip="'Sửa'"
                    />
                    <Button
                      icon="pi pi-trash"
                      outlined
                      rounded
                      severity="danger"
                      class="ml-2"
                      @click="confirmDeleteUser(data)"
                      v-tooltip="'Xóa'"
                    />
                  </template>
                </Column>
              </DataTable>

              <!-- Fallback when no data and not loading -->
              <div v-else-if="!userStore.isLoading && usersList.length === 0" class="no-data-message">
                <p>Không có dữ liệu người dùng để hiển thị.</p>
                <Button 
                  label="Tải lại" 
                  icon="pi pi-refresh" 
                  @click="loadUsers"
                  severity="secondary"
                />
              </div>

              <!-- Create/Edit User Dialog -->
              <Dialog
                v-model:visible="userDialog"
                :header="isEditing ? 'Sửa Người Dùng' : 'Thêm Người Dùng'"
                :style="{ width: '500px' }"
                modal
                class="p-fluid"
              >
                <div class="field">
                  <label for="username">Tên Đăng Nhập</label>
                  <InputText id="username" v-model.trim="userForm.username" required :class="{ 'p-invalid': userErrors.username }" />
                  <small class="p-error" v-if="userErrors.username">{{ userErrors.username }}</small>
                </div>
                <div class="field">
                  <label for="email">Email</label>
                  <InputText id="email" v-model.trim="userForm.email" type="email" required :class="{ 'p-invalid': userErrors.email }" />
                  <small class="p-error" v-if="userErrors.email">{{ userErrors.email }}</small>
                </div>
                <div class="field">
                  <label for="role">Vai Trò</label>
                  <Dropdown
                    id="role"
                    v-model="userForm.role"
                    :options="roleOptions"
                    optionLabel="label"
                    optionValue="value"
                    placeholder="Chọn vai trò"
                    required
                    :class="{ 'p-invalid': userErrors.role }"
                  />
                  <small class="p-error" v-if="userErrors.role">{{ userErrors.role }}</small>
                </div>
                <div class="field">
                  <label for="password">Mật Khẩu</label>
                  <Password
                    id="password"
                    v-model="userForm.password"
                    :required="!isEditing"
                    :feedback="false"
                    toggleMask
                    :placeholder="isEditing ? 'Bỏ trống nếu không đổi' : 'Nhập mật khẩu'"
                    :class="{ 'p-invalid': userErrors.password }"
                  />
                  <small class="p-error" v-if="userErrors.password">{{ userErrors.password }}</small>
                </div>
                <div class="field-checkbox">
                  <Checkbox id="is_active" v-model="userForm.is_active" :binary="true" />
                  <label for="is_active" class="ml-2">Hoạt động</label>
                </div>
                <template #footer>
                  <Button label="Hủy" icon="pi pi-times" text @click="hideUserDialog" />
                  <Button :label="isEditing ? 'Cập Nhật' : 'Tạo'" icon="pi pi-check" @click="handleUserSubmit" />
                </template>
              </Dialog>
            </div>
          </TabPanel>

          <TabPanel header="Cấu Hình Hệ Thống">
            <div class="system-config-content">
              <div class="header">
                <h2>Cấu Hình Hệ Thống</h2>
                <div class="action-buttons">
                  <Button
                    label="Django Admin"
                    icon="pi pi-external-link"
                    text
                    @click="goToDjangoAdmin"
                    v-tooltip="'Go to Django Admin'"
                  />
                </div>
              </div>

              <div class="field-config-admin">
                <h3>Cấu hình trường hiển thị cho từng vai trò</h3>
                <table>
                  <thead>
                    <tr>
                      <th>Trường</th>
                      <th v-for="role in roles" :key="role">
                        {{ role }}
                        <Checkbox
                          :inputId="'checkall-' + role"
                          :checked="isAllChecked(role)"
                          :indeterminate="isIndeterminate(role)"
                          @change="toggleCheckAll(role, $event)"
                        />
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(field, key) in fieldMap" :key="key">
                      <td>{{ field.label }}</td>
                      <td v-for="role in roles" :key="role">
                        <Checkbox v-model="field.roles" :value="role" />
                      </td>
                    </tr>
                  </tbody>
                </table>
                <div class="admin-config-actions">
                  <Button label="Lưu cấu hình" icon="pi pi-save" @click="saveFieldConfig" class="p-button-success" />
                </div>
              </div>
            </div>
          </TabPanel>
        </TabView>
      </div>

      <!-- Teacher/Student Profile - Show System Configuration -->
      <div v-else-if="userRole === 'teacher' || userRole === 'student'" class="teacher-student-profile">
        <div class="card-header">
          <h2>Thông Tin Cá Nhân</h2>
          <div class="header-buttons">
            <Button
              :label="isEditMode ? 'Chế độ Xem' : 'Chỉnh sửa'"
              :icon="isEditMode ? 'pi pi-eye' : 'pi pi-pencil'"
              :severity="isEditMode ? 'secondary' : 'primary'"
              @click="handleProfileViewEditClick"
              class="mode-toggle-button"
              :disabled="!canEditProfile"
            />
            <Button
              label="Đổi mật khẩu"
              icon="pi pi-key"
              severity="warning"
              @click="navigateToChangePassword"
              class="mode-toggle-button"
            />
          </div>
        </div>

        <template v-if="!showFieldConfig && !showUserTable">
          <div class="avatar-section">
            <div class="avatar-wrapper" @click="canUploadAvatar && isEditMode ? triggerFileInput() : null">
              <img
                v-if="userProfile.profile_picture"
                :src="userProfile.profile_picture"
                alt="Avatar"
                class="avatar-preview"
              />
              <div v-else class="avatar-placeholder">Không có ảnh</div>
              <input
                ref="fileInput"
                type="file"
                accept="image/*"
                style="display:none"
                @change="onFileChange"
              />
            </div>
          </div>

          <Dialog v-model:visible="showCropper" header="Cắt ảnh đại diện" modal>
            <Cropper
              v-if="tempImage"
              :src="tempImage"
              :stencil-props="{ aspectRatio: 1 }"
              :autoZoom="true"
              :stencil-component="'circle-stencil'"
              @change="onCrop"
            />
            <template #footer>
              <Button label="Hủy" @click="showCropper = false" />
              <Button label="Lưu" @click="saveCroppedImage" />
            </template>
          </Dialog>

          <table class="profile-table">
            <tbody>
              <tr v-for="(value, key) in filteredUserProfile" :key="key">
                <td class="profile-key">{{ getFieldLabel(key) }}</td>
                <td class="profile-value">
                  <template v-if="isEditable(key) && isEditMode">
                    <component
                      :is="getInputComponent(key)"
                      v-model="editProfile[key]"
                      v-bind="getInputProps(key, value)"
                    />
                  </template>
                  <template v-else>
                    <span v-if="isObject(value)">{{ formatObjectValue(key, value) }}</span>
                    <span v-else-if="key === 'password'">
                      <div class="password-display">
                        <span>{{ showPassword ? (userProfile.password || '••••••••') : '••••••••' }}</span>
                        <Button
                          :icon="showPassword ? 'pi pi-eye-slash' : 'pi pi-eye'"
                          text
                          size="small"
                          @click="togglePasswordVisibility"
                          class="password-toggle-btn"
                        />
                      </div>
                    </span>
                    <span v-else>{{ formatValue(key, value) }}</span>
                  </template>
                  <small class="field-description">{{ getFieldDescription(key) }}</small>
                </td>
              </tr>
            </tbody>
          </table>

          <div class="form-actions" v-if="isEditMode">
            <Button
              type="submit"
              label="Lưu"
              icon="pi pi-check"
              :loading="isLoading"
              @click="updateProfile"
              class="submit-button"
              :disabled="!canEditProfile"
            />
          </div>
        </template>

        <!-- System Configuration for Teacher/Student -->
        <div v-if="showFieldConfig" class="system-config-content">
          <div class="header">
            <h2>Cấu Hình Hệ Thống</h2>
          </div>

          <div class="field-config-admin">
            <h3>Cấu hình trường hiển thị cho từng vai trò</h3>
            <table>
              <thead>
                <tr>
                  <th>Trường</th>
                  <th v-for="role in roles" :key="role">
                    {{ role }}
                    <Checkbox
                      :inputId="'checkall-' + role"
                      :checked="isAllChecked(role)"
                      :indeterminate="isIndeterminate(role)"
                      @change="toggleCheckAll(role, $event)"
                    />
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(field, key) in fieldMap" :key="key">
                  <td>{{ field.label }}</td>
                  <td v-for="role in roles" :key="role">
                    <Checkbox v-model="field.roles" :value="role" />
                  </td>
                </tr>
              </tbody>
            </table>
            <div class="admin-config-actions">
              <Button label="Lưu cấu hình" icon="pi pi-save" @click="saveFieldConfig" class="p-button-success" />
            </div>
          </div>
        </div>
      </div>

      <!-- Detail Dialog -->
      <Dialog
        v-model:visible="showDetailListDialog"
        modal
        :draggable="false"
        class="custom-dialog"
        :style="{ width: '50vw' }"
        :breakpoints="{ '1199px': '75vw', '575px': '90vw' }"
      >
        <template #header>
          <div class="dialog-header-custom">
            <i class="pi pi-info-circle" style="font-size: 1.5rem; margin-right: 0.75rem;"></i>
            Chi Tiết Hồ Sơ
          </div>
        </template>

        <div class="p-fluid">
          <div class="p-field" v-for="(value, key) in userProfile" :key="key">
            <div v-if="fieldMap[key] && (fieldMap[key].roles.includes(userRole) || userRole === 'admin')">
              <strong>{{ getFieldLabel(key) }}:</strong>
              <span>{{ isObject(value) ? formatObjectValue(key, value) : formatValue(key, value) }}</span>
            </div>
          </div>
        </div>

        <template #footer>
          <Button
            label="Đóng"
            icon="pi pi-times"
            @click="showDetailListDialog = false"
            class="p-button-text dialog-button-margin"
          />
        </template>
      </Dialog>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useUserStore } from '@/stores/user'
import { useAuthStore } from '@/stores/auth'
import { useConfirm } from 'primevue/useconfirm'

import FileUpload from 'primevue/fileupload'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Dropdown from 'primevue/dropdown'
import Calendar from 'primevue/calendar'
import Textarea from 'primevue/textarea'
import Dialog from 'primevue/dialog'
import Checkbox from 'primevue/checkbox'
import Password from 'primevue/password'
import Tag from 'primevue/tag'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import ConfirmDialog from 'primevue/confirmdialog'
import { Cropper } from 'vue-advanced-cropper'
import 'vue-advanced-cropper/dist/style.css'
import adminDefaultImg from '@/assets/images/admin.png'

const router = useRouter()
const toast = useToast()
const userStore = useUserStore()
const authStore = useAuthStore()
const confirm = useConfirm()

const isLoading = ref(false)
const showDetailListDialog = ref(false)
const isEditMode = ref(true) // Mặc định hiển thị ở chế độ chỉnh sửa
const showPassword = ref(false)
const activeTabIndex = ref(0)

const showFieldConfig = ref(false)
const showUserTable = ref(false)

const userProfile = ref({})
const editProfile = ref({})
const userList = ref([])
const selectedUserId = ref(null)

const showCropper = ref(false)
const tempImage = ref(null)
const croppedImage = ref(null)

const fileInput = ref(null)

const roles = ['admin', 'teacher', 'student']

// User Management Variables
const userDialog = ref(false)
const isEditing = ref(false)
const userForm = ref({
  id: null,
  username: '',
  email: '',
  role: 'student',
  password: '',
  is_active: true,
})
const userErrors = ref({})
const userFilters = ref({
  search: '',
  role: null,
})
let searchTimeout = null

const roleOptions = [
  { label: 'Admin', value: 'admin' },
  { label: 'Teacher', value: 'teacher' },
  { label: 'Student', value: 'student' },
]

// Use ref instead of computed for usersList
const usersList = ref([])

// Function to update usersList
const updateUsersList = () => {
  const users = userStore.users
  console.log('updateUsersList - raw users:', users)
  console.log('updateUsersList - users type:', typeof users)
  console.log('updateUsersList - isArray:', Array.isArray(users))
  
  if (!users) {
    console.log('updateUsersList - setting empty array (no users)')
    usersList.value = []
    return
  }
  
  if (Array.isArray(users)) {
    console.log('updateUsersList - setting array directly:', users)
    usersList.value = users
    return
  }
  
  if (users.results && Array.isArray(users.results)) {
    console.log('updateUsersList - setting results array:', users.results)
    usersList.value = users.results
    return
  }
  
  if (users.length !== undefined) {
    const spreadArray = [...users]
    console.log('updateUsersList - setting spread array:', spreadArray)
    usersList.value = spreadArray
    return
  }
  
  console.log('updateUsersList - setting empty array (fallback)')
  usersList.value = []
}

// Watch for changes in userStore.users
watch(() => userStore.users, () => {
  updateUsersList()
}, { deep: true, immediate: true })

const fieldMap = ref({
  id: { label: 'ID', visible: false, description: 'Mã định danh duy nhất của người dùng', roles: [] },
  username: { label: 'Tên đăng nhập', visible: true, description: 'Tên dùng để đăng nhập hệ thống', roles: ['admin', 'teacher', 'student'] },
  password: { label: 'Mật khẩu', visible: true, description: 'Mật khẩu đăng nhập hệ thống', roles: ['admin', 'teacher', 'student'] },
  first_name: { label: 'Tên', visible: true, description: 'Tên của người dùng', roles: ['admin', 'teacher', 'student'] },
  last_name: { label: 'Họ', visible: true, description: 'Họ của người dùng', roles: ['admin', 'teacher', 'student'] },
  full_name: { label: 'Họ và tên', visible: true, description: 'Tên đầy đủ của người dùng', roles: ['admin', 'teacher', 'student'] },
  email: { label: 'Email', visible: true, description: 'Địa chỉ email để liên hệ và đăng nhập', roles: ['admin', 'teacher', 'student'] },
  phone: { label: 'Số điện thoại', visible: true, description: 'Số điện thoại liên hệ', roles: ['admin', 'teacher', 'student'] },
  address: { label: 'Địa chỉ', visible: true, description: 'Địa chỉ hiện tại của người dùng', roles: ['admin', 'teacher', 'student'] },
  birth_date: { label: 'Ngày sinh', visible: true, description: 'Ngày sinh theo định dạng YYYY-MM-DD', roles: ['admin', 'teacher', 'student'] },
  gender: { label: 'Giới tính', visible: true, description: 'Giới tính: Nam, Nữ hoặc Khác', roles: ['admin', 'teacher', 'student'] },
  role: { label: 'Vai trò', visible: true, description: 'Vai trò của người dùng trong hệ thống', roles: ['admin', 'teacher', 'student'] },
  is_active: { label: 'Hoạt động', visible: false, description: 'Trạng thái hoạt động của tài khoản', roles: [] },
  is_staff: { label: 'Nhân viên', visible: false, description: 'Người dùng có phải là nhân viên', roles: [] },
  is_superuser: { label: 'Superuser', visible: false, description: 'Người dùng có quyền quản trị', roles: [] },
  date_joined: { label: 'Ngày tạo tài khoản', visible: false, description: 'Ngày tạo tài khoản người dùng', roles: [] },
  created_at: { label: 'Ngày tạo', visible: false, description: 'Thời điểm tạo tài khoản', roles: [] },
  updated_at: { label: 'Ngày cập nhật', visible: false, description: 'Thời điểm cập nhật thông tin gần nhất', roles: [] },
  profile_picture: { label: 'Ảnh đại diện', visible: false, description: 'Ảnh đại diện của người dùng', roles: [] },
})

// Computed property to generate full_name from first_name and last_name
const computedUserProfile = computed(() => {
  const profile = { ...userProfile.value }
  if (profile.first_name || profile.last_name) {
    profile.full_name = `${profile.last_name || ''} ${profile.first_name || ''}`.trim()
  }
  return profile
})

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

const navigateToChangePassword = () => {
  router.push({ name: 'profile-change-password' })
}

// User Management Functions
const loadUsers = async () => {
  const params = {
    search: userFilters.value.search,
    role: userFilters.value.role,
  }
  try {
    await userStore.fetchUsers(params)
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách người dùng', life: 3000 })
  }
}

const onSearchInput = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    loadUsers()
  }, 500)
}

const openNewUser = () => {
  isEditing.value = false
  userForm.value = {
    id: null,
    username: '',
    email: '',
    role: 'student',
    password: '',
    is_active: true,
  }
  userErrors.value = {}
  userDialog.value = true
}

const editUser = (user) => {
  isEditing.value = true
  userForm.value = { ...user, password: '' } // Clear password for editing
  userErrors.value = {}
  userDialog.value = true
}

const hideUserDialog = () => {
  userDialog.value = false
}

const handleUserSubmit = async () => {
  userErrors.value = {}
  try {
    if (isEditing.value) {
      // Don't send empty password
      const payload = { ...userForm.value }
      if (!payload.password) {
        delete payload.password
      }
      await userStore.updateUser(userForm.value.id, payload)
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật người dùng thành công', life: 3000 })
    } else {
      await userStore.createUser(userForm.value)
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Tạo người dùng thành công', life: 3000 })
    }
    hideUserDialog()
    loadUsers()
  } catch (error) {
    const errorData = error.response?.data
    if (errorData) {
      userErrors.value = errorData
    }
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errorData?.detail || 'Lưu người dùng thất bại', life: 3000 })
  }
}

const confirmDeleteUser = (user) => {
  confirm.require({
    message: `Bạn có chắc muốn xóa người dùng "${user.username}"?`,
    header: 'Xác nhận xóa',
    icon: 'pi pi-exclamation-triangle',
    acceptClass: 'p-button-danger',
    accept: async () => {
      try {
        await userStore.deleteUser(user.id)
        toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa người dùng thành công', life: 3000 })
        loadUsers()
      } catch (error) {
        toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Xóa người dùng thất bại', life: 3000 })
      }
    },
  })
}

const getRoleSeverity = (role) => {
  if (role === 'admin') return 'danger'
  if (role === 'teacher') return 'info'
  return 'success'
}

const goToDjangoAdmin = () => {
  if (!authStore.isAdmin) {
    toast.add({
      severity: 'error',
      summary: 'Lỗi',
      detail: 'Bạn không có quyền truy cập Django Admin',
      life: 3000,
    })
    return
  }
  window.location.href = '/admin/'
}

onMounted(async () => {
  await fetchProfile();
  if (userRole === 'admin') {
    await loadUsers();
  }
});

const fetchUserList = async () => {
  if (userRole === 'admin') {
    try {
      userList.value = await userStore.fetchAllUsers();
      console.log('userList:', userList.value);
    } catch (error) {
      toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách người dùng', life: 3000 });
      console.error('Error fetching user list:', error);
    }
  }
};

const fetchProfile = async (userId = null) => {
  try {
    let user;
    if (userRole === 'admin' && userId) {
      user = await userStore.fetchUserById(userId);
    } else {
      user = authStore.user || await authStore.fetchCurrentUser();
    }
    
    // Ensure we have the basic fields
    userProfile.value = { 
      ...user,
      password: '••••••••', // Add a placeholder password for display
      first_name: user.first_name || '',
      last_name: user.last_name || '',
    };
    editProfile.value = { ...userProfile.value };
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải thông tin hồ sơ', life: 3000 });
    console.error('Error fetching profile:', error);
  }
};

const filteredUserProfile = computed(() => {
  const filtered = {};
  const profile = computedUserProfile.value;
  Object.keys(profile).forEach((key) => {
    const fieldConfig = fieldMap.value[key];
    if (fieldConfig && fieldConfig.visible) {
      filtered[key] = profile[key];
    }
  });
  return filtered;
});

const isEditable = (key) => {
  const editableFields = ['email', 'first_name', 'last_name', 'phone', 'address', 'birth_date', 'gender'];
  return editableFields.includes(key) && canEditProfile;
};

const getInputComponent = (key) => {
  if (key === 'gender') return Dropdown;
  if (key === 'birth_date' || key === 'date_of_birth') return Calendar;
  if (key === 'address') return Textarea;
  return InputText;
};

const getInputProps = (key, value) => {
  if (key === 'gender') {
    return {
      options: [
        { label: 'Nam', value: 'M' },
        { label: 'Nữ', value: 'F' },
        { label: 'Khác', value: 'O' },
      ],
      optionLabel: 'label',
      optionValue: 'value',
      placeholder: 'Chọn giới tính',
    };
  }
  if (key === 'birth_date' || key === 'date_of_birth') {
    const dateValue = value ? new Date(value) : null;
    return {
      dateFormat: 'yy-mm-dd',
      showIcon: true,
      modelValue: dateValue
    };
  }
  if (key === 'address') {
    return {
      rows: 2,
    };
  }
  return {};
};

const isObject = (val) => val && typeof val === 'object' && !Array.isArray(val);

const formatObjectValue = (key, value) => {
  if (value && value.name) return value.name;
  return JSON.stringify(value);
};

const formatValue = (key, value) => {
  if (key === 'gender') {
    if (value === 'M') return 'Nam';
    if (value === 'F') return 'Nữ';
    if (value === 'O') return 'Khác';
  }
  if (key === 'role') {
    if (value === 'admin') return 'Quản trị viên';
    if (value === 'teacher') return 'Giáo viên';
    if (value === 'student') return 'Học sinh';
  }
  if (value === null || value === undefined || value === '') return 'N/A';
  if (typeof value === 'boolean') return value ? 'Có' : 'Không';
  if (key.includes('date') && value) {
    try {
      return new Date(value).toLocaleDateString('vi-VN', { year: 'numeric', month: '2-digit', day: '2-digit' });
    } catch (e) {
      return value;
    }
  }
  if (key.includes('time') && value) {
    try {
      return new Date(value).toLocaleTimeString('vi-VN');
    } catch (e) {
      return value;
    }
  }
  return value;
};

const getFieldLabel = (key) => {
  return fieldMap.value[key]?.label || key;
};

const getFieldDescription = (key) => {
  return fieldMap.value[key]?.description || '';
};

// Hàm xử lý click vào nút "Chỉnh sửa" / "Chế độ Xem"
const handleProfileViewEditClick = () => {
  // Khi click vào nút này, đảm bảo ẩn các bảng admin khác
  showFieldConfig.value = false;
  showUserTable.value = false;

  if (isEditMode.value) {
    // Nếu đang ở chế độ chỉnh sửa (nút hiển thị "Chế độ Xem")
    // Chuyển sang chế độ xem và hiển thị dialog chi tiết
    isEditMode.value = false;
    showDetailListDialog.value = true;
  } else {
    // Nếu đang ở chế độ xem (nút hiển thị "Chỉnh sửa")
    // Chuyển sang chế độ chỉnh sửa và ẩn dialog chi tiết
    isEditMode.value = true;
    showDetailListDialog.value = false;
  }
};

const toggleFieldConfig = () => {
  // Khi click "Cấu hình trường", toggle nó và ẩn các phần khác
  showFieldConfig.value = !showFieldConfig.value;
  if (showFieldConfig.value) {
    isEditMode.value = false; // Ẩn chế độ chỉnh sửa/xem chính
    showDetailListDialog.value = false; // Ẩn dialog chi tiết
    showUserTable.value = false; // Ẩn bảng danh sách người dùng
  }
};

const saveFieldConfig = () => {
  toast.add({ severity: 'success', summary: 'Thành công', detail: 'Đã cập nhật cấu hình trường hiển thị', life: 3000 });
};

const updateProfile = async () => {
  isLoading.value = true;
  try {
    const payload = {};
    Object.keys(editProfile.value).forEach((key) => {
      if (isEditable(key)) {
        payload[key] = editProfile.value[key];
      }
    });

    // Ensure first_name and last_name are included if they exist
    if (editProfile.value.first_name !== undefined) {
      payload.first_name = editProfile.value.first_name;
    }
    if (editProfile.value.last_name !== undefined) {
      payload.last_name = editProfile.value.last_name;
    }

    if (userRole === 'admin' && selectedUserId.value) {
      await userStore.updateUserProfile(selectedUserId.value, payload);
      await fetchUserList(); // Cập nhật lại danh sách nếu là admin
    } else {
      await userStore.updateProfile(payload);
    }
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật thông tin thành công', life: 3000 });
    await fetchProfile(selectedUserId.value); // Tải lại profile sau khi update
    isEditMode.value = false; // Sau khi lưu, chuyển về chế độ xem
  } catch (error) {
    let errorMessage = 'Không thể cập nhật thông tin';
    if (error.response?.data?.message) {
      errorMessage = error.response.data.message;
    } else if (error.message) {
      errorMessage = error.message;
    }
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errorMessage, life: 3000 });
    console.error('Update profile error:', error);
  } finally {
    isLoading.value = false;
  }
};

const triggerFileInput = () => {
  if (canEditProfile && isEditMode.value) {
    fileInput.value && fileInput.value.click();
  } else if (!canEditProfile) {
    toast.add({ severity: 'info', summary: 'Thông báo', detail: 'Bạn không có quyền tải lên ảnh đại diện.', life: 3000 });
  }
};

const onFileChange = (e) => {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (event) => {
      tempImage.value = event.target.result;
      showCropper.value = true;
    };
    reader.readAsDataURL(file);
  }
};

const onCrop = ({ canvas }) => {
  if (canvas) {
    croppedImage.value = canvas.toDataURL('image/jpeg');
  }
};

const saveCroppedImage = async () => {
  if (!croppedImage.value) return;
  const blob = await (await fetch(croppedImage.value)).blob();
  const formData = new FormData();
  formData.append('avatar', blob, 'avatar.jpg');
  await userStore.uploadAvatar(formData);
  showCropper.value = false;
  await fetchProfile(selectedUserId.value); // Tải lại profile để cập nhật ảnh
  toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật ảnh đại diện thành công', life: 3000 });
};

// Kiểm tra đã chọn hết chưa
const isAllChecked = (role) => {
  return Object.values(fieldMap.value).every(field => field.roles.includes(role))
}

// Kiểm tra trạng thái indeterminate (chỉ chọn 1 phần)
const isIndeterminate = (role) => {
  const total = Object.values(fieldMap.value).length
  const checked = Object.values(fieldMap.value).filter(field => field.roles.includes(role)).length
  return checked > 0 && checked < total
}

// Toggle check all
const toggleCheckAll = (role, event) => {
  const checked = event.checked
  Object.values(fieldMap.value).forEach(field => {
    if (checked) {
      if (!field.roles.includes(role)) field.roles.push(role)
    } else {
      field.roles = field.roles.filter(r => r !== role)
    }
  })
}

// Watcher for activeTabIndex to load users when switching to user management tab
watch(activeTabIndex, (newIndex) => {
  if (newIndex === 1 && userRole === 'admin') { // User management tab
    loadUsers();
  }
});

// Watcher for userRole to load users when role changes to admin
watch(userRole, (newRole) => {
  if (newRole === 'admin') {
    loadUsers();
  }
}, { immediate: true });
</script>

<style scoped>
.profile-container {
  max-width: 960px;
  margin: 2rem auto;
  padding: 2rem 2.5rem;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 1rem;
}
.card-header h2 {
  font-size: 1.75rem;
  font-weight: 600;
  color: #2c3e50;
}

.header-buttons {
  display: flex;
  gap: 1rem; /* Khoảng cách giữa các nút trong header */
  flex-wrap: wrap; /* Cho phép các nút xuống dòng nếu không đủ chỗ */
  justify-content: flex-end; /* Căn phải các nút */
}

.avatar-section {
  text-align: center;
  margin-bottom: 2rem;
}

.avatar-wrapper {
  display: inline-block;
  cursor: pointer;
  position: relative;
}

.avatar-preview, .avatar-placeholder {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #d1d5db;
  margin-bottom: 1rem;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.95rem;
  color: #9ca3af;
}

.hidden-upload-button {
  display: none; /* Hide the default file upload button */
}

.p-button-sm {
    padding: 0.4rem 1rem;
    font-size: 0.8rem;
    margin-top: 0.5rem; /* Margin for the delete button */
}

.p-button-danger-alt {
  background-color: #ef4444;
  border-color: #ef4444;
}
.p-button-danger-alt:hover {
  background-color: #dc2626;
  border-color: #dc2626;
}


.profile-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 2rem;
  font-size: 0.95rem;
}

.profile-key {
  font-weight: 500;
  color: #34495e;
  padding: 0.75rem 1rem;
  background: #f9fafb;
  width: 220px;
  border-bottom: 1px solid #e5e7eb;
  vertical-align: top;
}

.profile-value {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.profile-value .p-inputtext,
.profile-value .p-dropdown,
.profile-value .p-calendar,
.profile-value .p-textarea {
  width: 100%; /* Ensure input fields take full width */
}

.field-description {
  display: block;
  color: #6b7280;
  font-size: 0.78rem;
  margin-top: 0.25rem;
  font-style: italic;
}

/* Các nút điều khiển chế độ và hiển thị */
.mode-toggle-button {
  font-size: 0.85rem;
  padding: 0.45rem 1.2rem;
  border-radius: 6px;
  white-space: nowrap; /* Ngăn không cho chữ trong nút bị xuống dòng */
}

.submit-button {
  font-size: 1rem;
  padding: 0.7rem 2rem;
  border-radius: 6px;
}
.form-actions {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

/* Custom Dialog Styling - vẫn giữ nguyên cho dialog ví dụ */
.custom-dialog .p-dialog-header {
  background-color: #42b983;
  color: white;
  padding: 1.5rem;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.custom-dialog .p-dialog-header-icon {
  color: white;
}

.dialog-header-custom {
  display: flex;
  align-items: center;
  font-size: 1.25rem;
  font-weight: 600;
  color: white;
}

.custom-dialog .p-dialog-content {
  padding: 2rem 2.5rem;
  font-size: 1.05rem;
  color: #333;
}

.custom-dialog .p-dialog-footer {
  background-color: #f8f9fa;
  padding: 1rem 2rem;
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
}

.custom-dialog {
  border-radius: 10px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
}

.dialog-button-margin {
    margin: 0 10px;
}

/* Admin Field Configuration Table */
.field-config-admin {
  margin-top: 2.5rem; /* Tăng khoảng cách từ phần trên */
  padding: 1.5rem;
  background-color: #f3f9f3; /* Lighter green background for admin config */
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.field-config-admin h3 {
  font-size: 1.35rem;
  font-weight: 600;
  color: #2e8b57; /* Darker green */
  margin-bottom: 1.25rem;
  text-align: center;
}

.field-config-admin table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1.5rem;
  table-layout: fixed; /* Giúp các cột có độ rộng cố định */
}

.field-config-admin table th,
.field-config-admin table td {
  padding: 0.8rem 1rem;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

.field-config-admin table th {
  background-color: #e6ffe6; /* Very light green for headers */
  font-weight: 500;
  color: #3c763d;
}

/* Định nghĩa độ rộng cột cho bảng cấu hình */
.field-config-admin table th:first-child,
.field-config-admin table td:first-child {
    width: 40%; /* Cột tên trường */
}
.field-config-admin table th:not(:first-child),
.field-config-admin table td:not(:first-child) {
    width: 20%; /* Các cột vai trò */
    text-align: center; /* Căn giữa checkbox */
}


.field-config-admin table tr:last-child td {
  border-bottom: none;
}

.field-config-admin .p-checkbox {
  display: inline-flex; /* Đảm bảo checkbox hiển thị đúng */
  vertical-align: middle; /* Căn giữa theo chiều dọc */
  align-items: center;
  justify-content: center;
  width: 100%; /* Giúp checkbox chiếm toàn bộ ô để căn giữa */
  height: 100%;
}

.admin-config-actions {
  display: flex;
  justify-content: flex-end;
  padding-top: 1rem;
  border-top: 1px solid #e0e0e0;
}

/* User List Admin Table */
.user-list-admin {
  margin-top: 2.5rem; /* Tăng khoảng cách từ phần trên */
  padding: 1.5rem;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.user-list-admin h3 {
  font-size: 1.35rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 1.25rem;
  text-align: center;
}

.user-list-admin table {
  width: 100%;
  border-collapse: collapse;
}

.user-list-admin table thead {
  background-color: #f3f4f6;
}

.user-list-admin table th,
.user-list-admin table td {
  padding: 0.8rem 1rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.user-list-admin table th {
  font-weight: 500;
  color: #34495e;
}

.user-list-admin table tr:last-child td {
  border-bottom: none;
}

.user-list-admin table button {
  padding: 0.5rem 1rem;
  font-size: 0.8rem;
}

/* Các nút điều khiển tổng thể (không còn là show-user-table-btn riêng lẻ) */
/* Cập nhật selector để áp dụng cho tất cả các nút mode-toggle-button */
.mode-toggle-button {
  font-size: 0.85rem;
  padding: 0.45rem 1.2rem;
  border-radius: 6px;
}

/* Thêm responsive cho header-buttons nếu cần */
@media (max-width: 768px) {
    .header-buttons {
        flex-direction: column; /* Xếp các nút theo cột trên màn hình nhỏ */
        gap: 0.5rem; /* Giảm khoảng cách */
        align-items: stretch; /* Kéo dãn các nút cho đầy đủ chiều rộng */
    }
}

/* Password display styles */
.password-display {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.password-toggle-btn {
  padding: 0.25rem;
  min-width: auto;
  height: auto;
}

.password-toggle-btn:hover {
  background-color: rgba(0, 0, 0, 0.04);
}

/* Admin Tabs Styles */
.admin-tabs {
  width: 100%;
}

.admin-tabs :deep(.p-tabview-nav) {
  background: #f8f9fa;
  border-bottom: 2px solid #e9ecef;
  border-radius: 8px 8px 0 0;
}

.admin-tabs :deep(.p-tabview-nav-link) {
  padding: 1rem 1.5rem;
  font-weight: 500;
  color: #6c757d;
  border: none;
  background: transparent;
  transition: all 0.3s ease;
}

.admin-tabs :deep(.p-tabview-nav-link:hover) {
  background: #e9ecef;
  color: #495057;
}

.admin-tabs :deep(.p-tabview-nav-link.p-highlight) {
  background: #007bff;
  color: white;
  border-radius: 6px 6px 0 0;
}

.admin-tabs :deep(.p-tabview-panels) {
  padding: 2rem;
  background: white;
  border: 1px solid #e9ecef;
  border-top: none;
  border-radius: 0 0 8px 8px;
}

/* User Management Styles */
.user-management-content {
  width: 100%;
}

.user-management-content .header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.user-management-content .header h2 {
  margin: 0;
  font-size: 1.8rem;
  color: #333;
}

.filter-bar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
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

.p-datatable-sm :deep(.p-datatable-tbody > tr > td) {
  padding: 0.75rem;
  font-size: 0.9rem;
}

.p-datatable-sm :deep(.p-datatable-thead > tr > th) {
  background: #f8f9fa;
  padding: 0.75rem;
  font-size: 0.95rem;
}

.empty-message, .loading-message {
  text-align: center;
  padding: 2rem;
  color: #333;
}

.field {
  margin-bottom: 1.2rem;
}

.field-checkbox {
  display: flex;
  align-items: center;
  margin-top: 1rem;
}

.p-error {
  font-size: 0.875rem;
  color: #ef4444;
}

/* System Config Styles */
.system-config-content {
  width: 100%;
}

.system-config-content .header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.system-config-content .header h2 {
  margin: 0;
  font-size: 1.8rem;
  color: #333;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

/* Regular Profile Content */
.regular-profile-content {
  width: 100%;
}

/* Teacher/Student Profile */
.teacher-student-profile {
  width: 100%;
}

.teacher-student-profile .system-config-content {
  margin-top: 2rem;
  padding: 1.5rem;
  background-color: #f8f9fa;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

/* Responsive Design */
@media (max-width: 768px) {
  .admin-tabs :deep(.p-tabview-nav) {
    flex-direction: column;
  }
  
  .admin-tabs :deep(.p-tabview-nav-link) {
    border-radius: 6px;
    margin-bottom: 0.5rem;
  }
  
  .admin-tabs :deep(.p-tabview-nav-link.p-highlight) {
    border-radius: 6px;
  }
  
  .user-management-content .header,
  .system-config-content .header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .filter-group {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-dropdown,
  .filter-search {
    width: 100%;
  }
}

.no-data-message {
  text-align: center;
  padding: 3rem;
  color: #666;
  background: #f8f9fa;
  border-radius: 8px;
  margin: 1rem 0;
}

.no-data-message p {
  margin-bottom: 1rem;
  font-size: 1.1rem;
}
</style>