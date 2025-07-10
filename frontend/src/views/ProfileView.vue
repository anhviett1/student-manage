<template>
  <!-- Main Container -->
  <div class="profile-container" aria-label="Trang quản lý hồ sơ người dùng">

    <!-- Toast and ConfirmDialog for notifications -->
    <Toast aria-live="polite" />
    <ConfirmDialog aria-live="assertive" />

    <!-- Router View for Change Password -->
    <Transition name="fade">
      <router-view v-if="$route.name === 'profile-change-password'" />
      <div v-else>
        <!-- Admin Tabs -->
        <div v-if="userRole === 'admin' || userRole === 'superuser'" class="tab-view-container">
          <TabView v-model:activeIndex="activeTabIndex" scrollable class="tab-view" aria-label="Tab điều hướng quản lý">
            <!-- Profile Tab -->
            <TabPanel header="Hồ Sơ Cá Nhân">
              <!-- Profile Header -->
              <div class="card-header">
                <h2 class="card-title">Thông Tin Cá Nhân</h2>
                <div class="header-buttons">
                  <Button
                    :label="isEditMode ? 'Chế độ Xem' : 'Chỉnh sửa'"
                    :icon="isEditMode ? 'pi pi-eye' : 'pi pi-pencil'"
                    :severity="isEditMode ? 'secondary' : 'primary'"
                    @click="handleProfileViewEditClick"
                    class="mode-toggle-button"
                    :disabled="!canEditProfile"
                    :aria-label="isEditMode ? 'Chuyển sang chế độ xem' : 'Chuyển sang chế độ chỉnh sửa'"
                  />
                  <Button
                    label="Đổi mật khẩu"
                    icon="pi pi-key"
                    severity="warning"
                    @click="navigateToChangePassword"
                    class="mode-toggle-button"
                    aria-label="Chuyển đến trang đổi mật khẩu"
                  />
                </div>
              </div>

              <!-- Avatar Section -->
              <div class="avatar-section">
                <div
                  class="avatar-wrapper"
                  @click="canEditProfile && isEditMode ? triggerFileInput() : null"
                  :aria-label="canEditProfile && isEditMode ? 'Chọn ảnh đại diện' : 'Ảnh đại diện'"
                  role="button"
                  tabindex="0"
                  @keydown.enter="canEditProfile && isEditMode ? triggerFileInput() : null"
                >
                  <img
                    v-if="userProfile.profile_picture"
                    :src="userProfile.profile_picture"
                    alt="Ảnh đại diện"
                    class="avatar-preview"
                  />
                  <img
                    v-else-if="userRole === 'admin' && adminDefaultImg"
                    :src="adminDefaultImg"
                    alt="Ảnh mặc định admin"
                    class="avatar-preview"
                  />
                  <div v-else class="avatar-placeholder">Không có ảnh</div>
                  <input
                    ref="fileInput"
                    type="file"
                    accept="image/*"
                    class="hidden"
                    @change="onFileChange"
                    aria-label="Tải lên ảnh đại diện"
                  />
                </div>
                <Dialog v-model:visible="showCropper" header="Cắt ảnh đại diện" modal class="avatar-dialog" aria-labelledby="cropper-header">
                  <h3 id="cropper-header" class="sr-only">Cắt ảnh đại diện</h3>
                  <Cropper
                    v-if="tempImage"
                    :src="tempImage"
                    :stencil-props="{ aspectRatio: 1 }"
                    :autoZoom="true"
                    :stencil-component="'circle-stencil'"
                    @change="onCrop"
                    aria-label="Công cụ cắt ảnh đại diện"
                  />
                  <template #footer>
                    <Button label="Hủy" @click="showCropper = false" class="cancel-button" aria-label="Hủy cắt ảnh" />
                    <Button label="Lưu" @click="saveCroppedImage" aria-label="Lưu ảnh đã cắt" />
                  </template>
                </Dialog>
              </div>

              <!-- Profile Table -->
              <table class="profile-table">
                <tbody>
                  <tr v-for="(value, key) in filteredUserProfile" :key="key" class="profile-row">
                    <td class="profile-key">{{ getFieldLabel(key) }}</td>
                    <td class="profile-value">
                      <template v-if="isEditable(key) && isEditMode">
                        <component
                          :is="getInputComponent(key)"
                          v-model="editProfile[key]"
                          v-bind="getInputProps(key, value)"
                          class="profile-input"
                          :aria-label="getFieldLabel(key)"
                          :aria-describedby="`desc-${key}`"
                        />
                      </template>
                      <template v-else-if="key === 'password'">
                        <div class="password-display">
                          <span>{{ showPassword ? (value || '••••••••') : '••••••••' }}</span>
                          <Button
                            :icon="showPassword ? 'pi pi-eye-slash' : 'pi pi-eye'"
                            text
                            size="small"
                            @click="togglePasswordVisibility"
                            class="toggle-password-button"
                            aria-label="Hiển thị hoặc ẩn mật khẩu"
                          />
                        </div>
                      </template>
                      <template v-else>
                        <span>{{ isObject(value) ? formatObjectValue(key, value) : formatValue(key, value) }}</span>
                      </template>
                      <small :id="`desc-${key}`" class="field-description">{{ getFieldDescription(key) }}</small>
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
                  class="save-button"
                  :disabled="!canEditProfile"
                  aria-label="Lưu thông tin hồ sơ"
                />
                <Button
                  type="submit"
                  label="Hủy"
                  icon="pi pi-check"
                  :loading="isLoading"
                  class="delete-button"
                  :disabled="!canEditProfile"
                  aria-label="Hủy thông tin"
                />
              </div>
            </TabPanel>

            <!-- User Management Tab -->
            <TabPanel header="Quản Lý Người Dùng">
              <div class="user-management-content">
                <div class="header">
                  <h2 class="section-title">Quản Lý Người Dùng</h2>
                  <Button
                    icon="pi pi-plus"
                    label="Thêm Người Dùng"
                    severity="primary"
                    @click="openNewUser"
                    class="add-user-button"
                    aria-label="Thêm người dùng mới"
                  />
                </div>
                <div class="filter-bar">
                  <Dropdown
                    v-model="userFilters.role"
                    :options="roleOptions"
                    optionLabel="label"
                    optionValue="value"
                    placeholder="Lọc theo vai trò"
                    class="filter-dropdown"
                    showClear
                    @change="loadUsers"
                    aria-label="Lọc theo vai trò"
                  />
                  <InputText
                    v-model="userFilters.search"
                    placeholder="Tìm theo tên, email..."
                    class="filter-input"
                    @input="debouncedLoadUsers"
                    aria-label="Tìm kiếm người dùng"
                  />
                </div>
                <DataTable
                  :value="usersList"
                  :loading="isLoading"
                  dataKey="id"
                  paginator
                  :rows="paginatorInfo.rows"
                  :rowsPerPageOptions="[5, 10, 20]"
                  :totalRecords="paginatorInfo.total"
                  :lazy="true"
                  @page="onPage"
                  class="user-table"
                  aria-label="Bảng danh sách người dùng"
                >
                  <template #empty>
                    <div class="empty-table" aria-live="polite">Không tìm thấy người dùng nào.</div>
                  </template>
                  <template #loading>
                    <div class="loading-table" aria-live="polite">Đang tải dữ liệu...</div>
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
                        class="action-button"
                        aria-label="Sửa người dùng"
                      />
                      <Button
                        icon="pi pi-trash"
                        outlined
                        rounded
                        severity="danger"
                        @click="confirmDeleteUser(data)"
                        class="action-button"
                        aria-label="Xóa người dùng"
                      />
                    </template>
                  </Column>
                </DataTable>
                <Dialog
                  v-model:visible="userStore.userDialog"
                  :header="userStore.isEditing ? 'Sửa Người Dùng' : 'Thêm Người Dùng'"
                  modal
                  class="user-dialog"
                  aria-labelledby="user-dialog-header"
                >
                  <h3 id="user-dialog-header" class="sr-only">{{ userStore.isEditing ? 'Sửa Người Dùng' : 'Thêm Người Dùng' }}</h3>
                  <div class="field">
                    <label for="username" class="field-label">Tên Đăng Nhập</label>
                    <InputText
                      id="username"
                      v-model.trim="userStore.userForm.username"
                      class="field-input"
                      :class="{ 'invalid': userStore.userErrors.username }"
                      aria-describedby="username-desc"
                    />
                    <small id="username-desc" class="field-error" v-if="userStore.userErrors.username">{{ userStore.userErrors.username }}</small>
                  </div>
                  <div class="field">
                    <label for="email" class="field-label">Email</label>
                    <InputText
                      id="email"
                      v-model.trim="userStore.userForm.email"
                      type="email"
                      class="field-input"
                      :class="{ 'invalid': userStore.userErrors.email }"
                      aria-describedby="email-desc"
                    />
                    <small id="email-desc" class="field-error" v-if="userStore.userErrors.email">{{ userStore.userErrors.email }}</small>
                  </div>
                  <div class="field">
                    <label for="role" class="field-label">Vai Trò</label>
                    <Dropdown
                      id="role"
                      v-model="userStore.userForm.role"
                      :options="roleOptions"
                      optionLabel="label"
                      optionValue="value"
                      placeholder="Chọn vai trò"
                      class="field-input"
                      :class="{ 'invalid': userStore.userErrors.role }"
                      aria-describedby="role-desc"
                    />
                    <small id="role-desc" class="field-error" v-if="userStore.userErrors.role">{{ userStore.userErrors.role }}</small>
                  </div>
                  <div class="field">
                    <label for="password" class="field-label">Mật Khẩu</label>
                    <Password
                      id="password"
                      v-model="userStore.userForm.password"
                      :required="!userStore.isEditing"
                      :feedback="false"
                      toggleMask
                      :placeholder="userStore.isEditing ? 'Bỏ trống nếu không đổi' : 'Nhập mật khẩu'"
                      class="field-input"
                      :class="{ 'invalid': userStore.userErrors.password }"
                      aria-describedby="password-desc"
                    />
                    <small id="password-desc" class="field-error" v-if="userStore.userErrors.password">{{ userStore.userErrors.password }}</small>
                  </div>
                  <div class="field-checkbox">
                    <Checkbox id="is_active" v-model="userStore.userForm.is_active" :binary="true" aria-label="Trạng thái hoạt động" />
                    <label for="is_active" class="checkbox-label">Hoạt động</label>
                  </div>
                  <template #footer>
                    <Button label="Hủy" icon="pi pi-times" text @click="userStore.userDialog = false" aria-label="Hủy" />
                    <Button :label="userStore.isEditing ? 'Cập Nhật' : 'Tạo'" icon="pi pi-check" @click="handleUserSubmit" :aria-label="userStore.isEditing ? 'Cập nhật người dùng' : 'Tạo người dùng'" />
                  </template>
                </Dialog>
              </div>
            </TabPanel>

            <!-- Field Config Tab -->
            <TabPanel header="Cấu Hình Hệ Thống">
              <div class="field-config">
                <div class="header">
                  <h2 class="section-title">Cấu Hình Hệ Thống</h2>
                  <Button
                    label="Django Admin"
                    icon="pi pi-external-link"
                    text
                    @click="goToDjangoAdmin"
                    class="django-admin-button"
                    aria-label="Truy cập Django Admin"
                  />
                </div>
                <h3 class="subsection-title">Cấu hình trường hiển thị</h3>
                <table class="config-table">
                  <thead>
                    <tr class="config-header">
                      <th class="config-th">Trường</th>
                      <th v-for="role in roles" :key="role" class="config-th">
                        {{ role }}
                        <Checkbox
                          :inputId="'checkall-' + role"
                          :checked="isAllChecked(role)"
                          :indeterminate="isIndeterminate(role)"
                          @change="toggleCheckAll(role, $event)"
                          :aria-label="'Chọn tất cả trường cho vai trò ' + role"
                        />
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(field, key) in fieldMap" :key="key" class="config-row">
                      <td class="config-td">{{ field.label }}</td>
                      <td v-for="role in roles" :key="role" class="config-td">
                        <Checkbox v-model="field.roles" :value="role" :aria-label="'Hiển thị trường ' + field.label + ' cho vai trò ' + role" />
                      </td>
                    </tr>
                  </tbody>
                </table>
                <div class="config-actions">
                  <Button
                    label="Lưu cấu hình"
                    icon="pi pi-save"
                    @click="saveFieldConfig"
                    class="save-config-button"
                    aria-label="Lưu cấu hình trường hiển thị"
                  />
                </div>
              </div>
            </TabPanel>
          </TabView>
        </div>

        <!-- Teacher/Student Profile -->
        <div v-else-if="userRole === 'teacher' || userRole === 'student'" class="teacher-student-profile">
          <!-- Profile Header -->
          <div class="card-header">
            <h2 class="card-title">Thông Tin Cá Nhân</h2>
            <div class="header-buttons">
              <Button
                :label="isEditMode ? 'Chế độ Xem' : 'Chỉnh sửa'"
                :icon="isEditMode ? 'pi pi-eye' : 'pi pi-pencil'"
                :severity="isEditMode ? 'secondary' : 'primary'"
                @click="handleProfileViewEditClick"
                class="mode-toggle-button"
                :disabled="!canEditProfile"
                :aria-label="isEditMode ? 'Chuyển sang chế độ xem' : 'Chuyển sang chế độ chỉnh sửa'"
              />
              <Button
                label="Đổi mật khẩu"
                icon="pi pi-key"
                severity="warning"
                @click="navigateToChangePassword"
                class="mode-toggle-button"
                aria-label="Chuyển đến trang đổi mật khẩu"
              />
            </div>
          </div>

          <!-- Avatar Section -->
          <div class="avatar-section">
            <div
              class="avatar-wrapper"
              @click="canEditProfile && isEditMode ? triggerFileInput() : null"
              :aria-label="canEditProfile && isEditMode ? 'Chọn ảnh đại diện' : 'Ảnh đại diện'"
              role="button"
              tabindex="0"
              @keydown.enter="canEditProfile && isEditMode ? triggerFileInput() : null"
            >
              <img
                v-if="userProfile.profile_picture"
                :src="userProfile.profile_picture"
                alt="Ảnh đại diện"
                class="avatar-preview"
              />
              <img
                v-else-if="userRole === 'admin' && adminDefaultImg"
                :src="adminDefaultImg"
                alt="Ảnh mặc định admin"
                class="avatar-preview"
              />
              <div v-else class="avatar-placeholder">Không có ảnh</div>
              <input
                ref="fileInput"
                type="file"
                accept="image/*"
                class="hidden"
                @change="onFileChange"
                aria-label="Tải lên ảnh đại diện"
              />
            </div>
            <Dialog v-model:visible="showCropper" header="Cắt ảnh đại diện" modal class="avatar-dialog" aria-labelledby="cropper-header">
              <h3 id="cropper-header" class="sr-only">Cắt ảnh đại diện</h3>
              <Cropper
                v-if="tempImage"
                :src="tempImage"
                :stencil-props="{ aspectRatio: 1 }"
                :autoZoom="true"
                :stencil-component="'circle-stencil'"
                @change="onCrop"
                aria-label="Công cụ cắt ảnh đại diện"
              />
              <template #footer>
                <Button label="Hủy" @click="showCropper = false" class="cancel-button" aria-label="Hủy cắt ảnh" />
                <Button label="Lưu" @click="saveCroppedImage" aria-label="Lưu ảnh đã cắt" />
              </template>
            </Dialog>
          </div>

          <!-- Profile Table -->
          <table class="profile-table">
            <tbody>
              <tr v-for="(value, key) in filteredUserProfile" :key="key" class="profile-row">
                <td class="profile-key">{{ getFieldLabel(key) }}</td>
                <td class="profile-value">
                  <template v-if="isEditable(key) && isEditMode">
                    <component
                      :is="getInputComponent(key)"
                      v-model="editProfile[key]"
                      v-bind="getInputProps(key, value)"
                      class="profile-input"
                      :aria-label="getFieldLabel(key)"
                      :aria-describedby="`desc-${key}`"
                    />
                  </template>
                  <template v-else-if="key === 'password'">
                    <div class="password-display">
                      <span>{{ showPassword ? (value || '••••••••') : '••••••••' }}</span>
                      <Button
                        :icon="showPassword ? 'pi pi-eye-slash' : 'pi pi-eye'"
                        text
                        size="small"
                        @click="togglePasswordVisibility"
                        class="toggle-password-button"
                        aria-label="Hiển thị hoặc ẩn mật khẩu"
                      />
                    </div>
                  </template>
                  <template v-else>
                    <span>{{ isObject(value) ? formatObjectValue(key, value) : formatValue(key, value) }}</span>
                  </template>
                  <small :id="`desc-${key}`" class="field-description">{{ getFieldDescription(key) }}</small>
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
              class="save-button"
              :disabled="!canEditProfile"
              aria-label="Lưu thông tin hồ sơ"
            />
            <Button
              type="button"
              label="Hủy"
              icon="pi pi-times"
              :loading="false"
              @click="cancelEdit"
              class="delete-button"
              :disabled="!canEditProfile"
              aria-label="Hủy chỉnh sửa"
            />
          </div>
        </div>

        <!-- Fallback -->
        <div v-else class="fallback">
          <p v-if="isLoading" class="loading-text" aria-live="polite">Đang tải thông tin...</p>
          <p v-else class="error-text" aria-live="assertive">Bạn không có quyền truy cập hoặc thông tin không hợp lệ.</p>
        </div>

        <!-- Detail Dialog -->
        <Dialog
          v-model:visible="showDetailListDialog"
          modal
          :draggable="false"
          class="custom-dialog"
          style="width: 50vw;"
          :breakpoints="{ '1199px': '75vw', '575px': '90vw' }"
          aria-labelledby="detail-dialog-header"
        >
          <template #header>
            <div class="dialog-header-custom">
              <i class="pi pi-info-circle dialog-header-icon"></i>
              <span id="detail-dialog-header">Chi Tiết Hồ Sơ</span>
            </div>
          </template>
          <div class="dialog-content">
            <div v-for="(value, key) in userProfile" :key="key" class="dialog-row">
              <div v-if="fieldMap[key] && (fieldMap[key].roles.includes(userRole) || userRole === 'admin')">
                <strong class="dialog-label">{{ getFieldLabel(key) }}:</strong>
                <span class="dialog-value">{{ isObject(value) ? formatObjectValue(key, value) : formatValue(key, value) }}</span>
              </div>
            </div>
          </div>
          <template #footer>
            <Button
              label="Đóng"
              icon="pi pi-times"
              @click="showDetailListDialog = false"
              class="cancel-button"
              aria-label="Đóng dialog chi tiết hồ sơ"
            />
          </template>
        </Dialog>
      </div>
    </Transition>
  </div>
</template>

<script setup>
// Imports
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';
import { useUserStore } from '@/stores/user';
import { useAuthStore } from '@/stores/auth';
import { usePermissions } from '@/composables/usePermissions';
import { gsap } from 'gsap';
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';
import Toast from 'primevue/toast';
import ConfirmDialog from 'primevue/confirmdialog';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import Calendar from 'primevue/calendar';
import Textarea from 'primevue/textarea';
import Checkbox from 'primevue/checkbox';
import Password from 'primevue/password';
import Tag from 'primevue/tag';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Dialog from 'primevue/dialog';
import { Cropper } from 'vue-advanced-cropper';
import 'vue-advanced-cropper/dist/style.css';
import adminDefaultImg from '@/assets/images/admin.png';

// State and Computed
const router = useRouter();
const toast = useToast();
const confirm = useConfirm();
const userStore = useUserStore();
const authStore = useAuthStore();
const { isAdmin, isOwnerOrAdmin } = usePermissions();

const userRole = computed(() => authStore.user?.role || null);
const canEditProfile = computed(() => userProfile.value ? isAdmin.value || isOwnerOrAdmin(userProfile.value, 'id') : false);
const isLoading = ref(false);
const showDetailListDialog = ref(false);
const isEditMode = ref(true);
const activeTabIndex = ref(0);
const userProfile = ref({});
const editProfile = ref({});
const usersList = ref([]);
const userFilters = ref({ search: '', role: null });
const paginatorInfo = ref({ rows: 10, page: 1, total: 0 });
const showCropper = ref(false);
const tempImage = ref(null);
const croppedImage = ref(null);
const fileInput = ref(null);
const showPassword = ref(false);

// Field Map Configuration
const fieldMap = ref({
  id: { label: 'ID', visible: false, description: 'Mã định danh duy nhất', roles: [] },
  username: { label: 'Tên đăng nhập', visible: true, description: 'Tên dùng để đăng nhập', roles: ['admin', 'teacher', 'student'] },
  password: { label: 'Mật khẩu', visible: true, description: 'Mật khẩu đăng nhập', roles: ['admin', 'teacher', 'student'] },
  first_name: { label: 'Tên', visible: true, description: 'Tên của người dùng', roles: ['admin', 'teacher', 'student'] },
  last_name: { label: 'Họ', visible: true, description: 'Họ của người dùng', roles: ['admin', 'teacher', 'student'] },
  full_name: { label: 'Họ và tên', visible: true, description: 'Tên đầy đủ', roles: ['admin', 'teacher', 'student'] },
  email: { label: 'Email', visible: true, description: 'Địa chỉ email liên hệ', roles: ['admin', 'teacher', 'student'] },
  phone: { label: 'Số điện thoại', visible: true, description: 'Số điện thoại liên hệ', roles: ['admin', 'teacher', 'student'] },
  address: { label: 'Địa chỉ', visible: true, description: 'Địa chỉ hiện tại', roles: ['admin', 'teacher', 'student'] },
  birth_date: { label: 'Ngày sinh', visible: true, description: 'Ngày sinh (YYYY-MM-DD)', roles: ['admin', 'teacher', 'student'] },
  gender: { label: 'Giới tính', visible: true, description: 'Giới tính: Nam, Nữ, Khác', roles: ['admin', 'teacher', 'student'] },
  role: { label: 'Vai trò', visible: true, description: 'Vai trò trong hệ thống', roles: ['admin', 'teacher', 'student'] },
  is_active: { label: 'Hoạt động', visible: false, description: 'Trạng thái hoạt động', roles: [] },
  is_staff: { label: 'Nhân viên', visible: false, description: 'Người dùng là nhân viên', roles: [] },
  is_superuser: { label: 'Superuser', visible: false, description: 'Người dùng có quyền quản trị', roles: [] },
  date_joined: { label: 'Ngày tạo tài khoản', visible: false, description: 'Ngày tạo tài khoản', roles: [] },
  created_at: { label: 'Ngày tạo', visible: false, description: 'Thời điểm tạo tài khoản', roles: [] },
  updated_at: { label: 'Ngày cập nhật', visible: false, description: 'Thời điểm cập nhật gần nhất', roles: [] },
  profile_picture: { label: 'Ảnh đại diện', visible: false, description: 'Ảnh đại diện', roles: [] },
});
const roleOptions = [
  { label: 'Admin', value: 'admin' },
  { label: 'Teacher', value: 'teacher' },
  { label: 'Student', value: 'student' },
];
const roles = ['admin', 'teacher', 'student'];

// GSAP Animations
onMounted(() => {
  gsap.from('.profile-container', {
    opacity: 0,
    y: 50,
    duration: 0.8,
    ease: 'power2.out',
  });
  fetchProfile();
  if (userRole.value === 'admin') loadUsers();
});

// Watch tab changes for animations
watch(activeTabIndex, (newIndex) => {
  if (newIndex === 1 && userRole.value === 'admin') {
    loadUsers();
    gsap.from('.user-management-content', { opacity: 0, x: -30, duration: 0.5 });
  } else if (newIndex === 2) {
    gsap.from('.field-config', { opacity: 0, x: 30, duration: 0.5 });
  }
});

// Profile Functions
const fetchProfile = async (userId = null) => {
  isLoading.value = true;
  try {
    const user = userRole.value === 'admin' && userId
      ? await userStore.fetchUserById(userId)
      : authStore.user || await authStore.fetchCurrentUser();
    userProfile.value = { ...user, password: '••••••••', first_name: user.first_name || '', last_name: user.last_name || '' };
    editProfile.value = { ...userProfile.value };
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải thông tin hồ sơ', life: 3000 });
  } finally {
    isLoading.value = false;
  }
};

const updateProfile = async () => {
  isLoading.value = true;
  try {
    const payload = Object.keys(editProfile.value)
      .filter(key => isEditable(key))
      .reduce((obj, key) => ({ ...obj, [key]: editProfile.value[key] }), {});
    await userStore.updateProfile(payload);
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật hồ sơ thành công', life: 3000 });
    isEditMode.value = false;
    fetchProfile();
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: error.response?.data?.message || 'Cập nhật thất bại', life: 3000 });
  } finally {
    isLoading.value = false;
  }
};

// User Management Functions
const loadUsers = async () => {
  isLoading.value = true;
  try {
    usersList.value = (await userStore.fetchAllUsers()).sort((a, b) => a.id - b.id);
    paginatorInfo.value = { rows: usersList.value.length, page: 1, total: usersList.value.length };
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách người dùng', life: 3000 });
  } finally {
    isLoading.value = false;
  }
};

const onPage = (event) => {
  paginatorInfo.value.page = event.page + 1;
  paginatorInfo.value.rows = event.rows;
  loadUsers(event.page + 1, event.rows);
};

const debouncedLoadUsers = () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => loadUsers(), 500);
};
let searchTimeout = null;

const openNewUser = () => {
  userStore.resetUserForm();
  userStore.userDialog = true;
};

const editUser = (user) => {
  userStore.setUserForm({ ...user, password: '' });
  userStore.userDialog = true;
};

const handleUserSubmit = async () => {
  userStore.userErrors = {};
  try {
    if (userStore.isEditing) {
      const payload = { ...userStore.userForm };
      if (!payload.password) delete payload.password;
      await userStore.updateUser(userStore.userForm.id, payload);
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật người dùng thành công', life: 3000 });
    } else {
      await userStore.createUser(userStore.userForm);
      toast.add({ severity: 'success', summary: 'Thành công', detail: 'Tạo người dùng thành công', life: 3000 });
    }
    userStore.userDialog = false;
    loadUsers();
  } catch (error) {
    userStore.userErrors = error.response?.data || {};
    toast.add({ severity: 'error', summary: 'Lỗi', detail: error.response?.data?.detail || 'Lưu người dùng thất bại', life: 3000 });
  }
};

const confirmDeleteUser = (user) => {
  confirm.require({
    message: `Bạn có chắc muốn xóa người dùng "${user.username}"?`,
    header: 'Xác nhận xóa',
    icon: 'pi pi-exclamation-triangle',
    acceptClass: 'p-button-danger',
    accept: async () => {
      try {
        await userStore.deleteUser(user.id);
        toast.add({ severity: 'success', summary: 'Thành công', detail: 'Xóa người dùng thành công', life: 3000 });
        loadUsers();
      } catch (error) {
        toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Xóa người dùng thất bại', life: 3000 });
      }
    },
    acceptLabel: 'Xóa',
    rejectLabel: 'Hủy',
  });
};

const getRoleSeverity = (role) => {
  if (role === 'admin') return 'danger';
  if (role === 'teacher') return 'info';
  return 'success';
};

// Avatar Functions
const triggerFileInput = () => {
  if (!fileInput.value) return;
  if (!canEditProfile.value) {
    toast.add({ severity: 'info', summary: 'Thông báo', detail: 'Bạn không có quyền tải lên ảnh đại diện.', life: 3000 });
    return;
  }
  fileInput.value.click();
};

const onFileChange = (e) => {
  const file = e.target.files[0];
  if (file) {
    tempImage.value = URL.createObjectURL(file);
    showCropper.value = true;
  }
};

const onCrop = ({ canvas }) => {
  if (canvas) croppedImage.value = canvas.toDataURL('image/jpeg');
};

const saveCroppedImage = async () => {
  if (!croppedImage.value) return;
  const blob = await (await fetch(croppedImage.value)).blob();
  const formData = new FormData();
  formData.append('avatar', blob, 'avatar.jpg');
  await userStore.uploadAvatar(formData);
  showCropper.value = false;
  fetchProfile();
  toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật ảnh đại diện thành công', life: 3000 });
};

// Field Config Functions
const isAllChecked = (role) => Object.values(fieldMap.value).every(field => field.roles.includes(role));
const isIndeterminate = (role) => {
  const total = Object.values(fieldMap.value).length;
  const checked = Object.values(fieldMap.value).filter(field => field.roles.includes(role)).length;
  return checked > 0 && checked < total;
};
const toggleCheckAll = (role, event) => {
  Object.values(fieldMap.value).forEach(field => {
    if (event.checked) {
      if (!field.roles.includes(role)) field.roles.push(role);
    } else {
      field.roles = field.roles.filter(r => r !== role);
    }
  });
};

const saveFieldConfig = () => {
  toast.add({ severity: 'success', summary: 'Thành công', detail: 'Đã cập nhật cấu hình trường hiển thị', life: 3000 });
};

const goToDjangoAdmin = () => {
  toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Chức năng chưa được triển khai', life: 3000 });
};

// Profile Table Functions
const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

const getFieldLabel = (key) => {
  const labels = {
    id: 'ID', username: 'Tên đăng nhập', password: 'Mật khẩu', first_name: 'Tên', last_name: 'Họ',
    full_name: 'Họ và tên', email: 'Email', phone: 'Số điện thoại', address: 'Địa chỉ',
    birth_date: 'Ngày sinh', gender: 'Giới tính', role: 'Vai trò'
  };
  return labels[key] || key;
};

const getFieldDescription = (key) => {
  const descriptions = {
    username: 'Tên dùng để đăng nhập hệ thống',
    password: 'Mật khẩu đăng nhập hệ thống',
    email: 'Địa chỉ email để liên hệ và đăng nhập',
    phone: 'Số điện thoại liên hệ',
    address: 'Địa chỉ hiện tại của người dùng',
    birth_date: 'Ngày sinh theo định dạng YYYY-MM-DD',
    gender: 'Giới tính: Nam, Nữ hoặc Khác',
    role: 'Vai trò của người dùng trong hệ thống'
  };
  return descriptions[key] || '';
};

const isEditable = (key) => ['email', 'first_name', 'last_name', 'phone', 'address', 'birth_date', 'gender'].includes(key) && canEditProfile.value;

const getInputComponent = (key) => {
  if (key === 'gender') return Dropdown;
  if (key === 'birth_date') return Calendar;
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
  if (key === 'birth_date') {
    return { dateFormat: 'yy-mm-dd', showIcon: true, modelValue: value ? new Date(value) : null };
  }
  if (key === 'address') {
    return { rows: 2 };
  }
  return {};
};

const isObject = (val) => val && typeof val === 'object' && !Array.isArray(val);
const formatObjectValue = (key, value) => (value && value.name) ? value.name : JSON.stringify(value);
const formatValue = (key, value) => {
  if (key === 'gender') return { 'M': 'Nam', 'F': 'Nữ', 'O': 'Khác' }[value] || 'N/A';
  if (key === 'role') return { admin: 'Quản trị viên', teacher: 'Giáo viên', student: 'Học sinh' }[value] || 'N/A';
  if (value === null || value === undefined || value === '') return 'N/A';
  if (typeof value === 'boolean') return value ? 'Có' : 'Không';
  if (key.includes('date') && value) {
    try {
      return new Date(value).toLocaleDateString('vi-VN', { year: 'numeric', month: '2-digit', day: '2-digit' });
    } catch (e) {
      return value;
    }
  }
  return value;
};

// Navigation
const navigateToChangePassword = () => router.push({ name: 'profile-change-password' });
const handleProfileViewEditClick = () => {
  isEditMode.value = !isEditMode.value;
  showDetailListDialog.value = !isEditMode.value;
  if (isEditMode.value) {
    gsap.from('.profile-table', { opacity: 0, y: 20, duration: 0.5 });
  }
};

// Computed for Profile Filtering
const filteredUserProfile = computed(() => {
  const profile = { ...userProfile.value, full_name: `${userProfile.value.last_name || ''} ${userProfile.value.first_name || ''}`.trim() };
  return Object.keys(profile)
    .filter(key => fieldMap.value[key]?.visible)
    .reduce((obj, key) => ({ ...obj, [key]: profile[key] }), {});
});
</script>

<style scoped>
/* Screen Reader Only */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  white-space: nowrap;
  border: 0;
}

/* Transitions */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* Profile Container */
.profile-container {
  max-width: 896px; /* 4xl = 896px */
  margin: 0 auto;
  padding: 24px;
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

/* TabView Styles */
.tab-view .p-tabview-nav {
  background-color: #f3f4f6;
  border-bottom: 2px solid #e5e7eb;
  border-radius: 8px 8px 0 0;
}
.tab-view .p-tabview-nav-link {
  padding: 12px 16px;
  font-weight: 500;
  color: #4b5563;
  transition: background-color 0.2s ease, color 0.2s ease;
}
.tab-view .p-tabview-nav-link:hover {
  background-color: #e5e7eb;
  color: #1f2937;
}
.tab-view .p-tabview-nav-link.p-highlight {
  background-color: #3b82f6;
  color: #ffffff;
  border-radius: 6px 6px 0 0;
}
.tab-view .p-tabview-panels {
  padding: 24px;
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 0 0 8px 8px;
}

/* Profile Header */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e5e7eb;
}
.card-header.dark-theme {
  border-bottom-color: #6b7280;
}
.card-title {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
}
.dark-theme .card-title {
  color: #f3f4f6;
}
.header-buttons {
  display: flex;
  gap: 12px;
}
.mode-toggle-button {
  font-size: 14px;
  padding: 8px 16px;
  border-radius: 6px;
  transition: transform 0.2s ease;
}
.mode-toggle-button:hover {
  transform: scale(1.05);
}

/* Avatar Section */
.avatar-section {
  text-align: center;
  margin-bottom: 24px;
}
.avatar-wrapper {
  display: inline-block;
  position: relative;
  cursor: pointer;
  transition: transform 0.2s ease;
}
.avatar-wrapper:hover {
  transform: scale(1.05);
}
.avatar-preview, .avatar-placeholder {
  width: 128px;
  height: 128px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #d1d5db;
  background-color: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  font-size: 14px;
}
.dark-theme .avatar-preview, .dark-theme .avatar-placeholder {
  border-color: #6b7280;
  background-color: #4b5563;
  color: #d1d5db;
}
.avatar-dialog {
  border-radius: 8px;
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.2);
}
.hidden {
  display: none;
}

/* Profile Table */
.profile-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 24px;
}
.profile-row:hover {
  background-color: #f9fafb;
}
.dark-theme .profile-row:hover {
  background-color: #374151;
}
.profile-key {
  font-weight: 500;
  color: #374151;
  padding: 12px;
  background-color: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
  width: 192px;
}
.dark-theme .profile-key {
  color: #e5e7eb;
  background-color: #374151;
  border-bottom-color: #6b7280;
}
.profile-value {
  padding: 12px;
  border-bottom: 1px solid #e5e7eb;
}
.dark-theme .profile-value {
  border-bottom-color: #6b7280;
}
.profile-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
}
.profile-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
}
.dark-theme .profile-input {
  background-color: #374151;
  border-color: #6b7280;
  color: #ffffff;
}
.form-actions {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}
.field-description {
  display: block;
  color: #6b7280;
  font-size: 12px;
  margin-top: 4px;
  font-style: italic;
}
.dark-theme .field-description {
  color: #9ca3af;
}
.password-display {
  display: flex;
  align-items: center;
  gap: 8px;
}
.toggle-password-button {
  font-size: 12px;
}
.save-button {
  padding: 12px 24px;
  border-radius: 6px;
  background-color: #10b981;
  color: #ffffff;
}
.save-button:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

/* User Management */
.user-management-content {
  padding: 24px;
  background-color: #f9fafb;
  border-radius: 8px;
}
.dark-theme .user-management-content {
  background-color: #374151;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.section-title {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
}
.dark-theme .section-title {
  color: #f3f4f6;
}
.filter-bar {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-bottom: 16px;
}
.filter-dropdown {
  width: 192px;
}
.filter-input {
  width: 256px;
  padding: 8px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
}
.dark-theme .filter-input {
  background-color: #374151;
  border-color: #6b7280;
  color: #ffffff;
}
.user-table .p-datatable-tbody > tr > td {
  padding: 12px;
  font-size: 14px;
}
.user-table .p-datatable-thead > tr > th {
  padding: 12px;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  background-color: #f9fafb;
}
.dark-theme .user-table .p-datatable-thead > tr > th {
  color: #e5e7eb;
  background-color: #4b5563;
}
.empty-table, .loading-table {
  text-align: center;
  padding: 16px;
  color: #6b7280;
}
.dark-theme .empty-table, .dark-theme .loading-table {
  color: #d1d5db;
}
.add-user-button {
  padding: 8px 16px;
  border-radius: 6px;
  background-color: #3b82f6;
  color: #ffffff;
}
.action-button {
  margin-right: 8px;
}
.user-dialog {
  width: 100%;
  max-width: 448px;
}
.field {
  margin-bottom: 16px;
}
.field-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 4px;
}
.dark-theme .field-label {
  color: #e5e7eb;
}
.field-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
}
.dark-theme .field-input {
  background-color: #374151;
  border-color: #6b7280;
  color: #ffffff;
}
.field-input.invalid {
  border-color: #ef4444;
}
.field-error {
  color: #ef4444;
  font-size: 12px;
}
.field-checkbox {
  display: flex;
  align-items: center;
}
.checkbox-label {
  margin-left: 8px;
  font-size: 14px;
  color: #374151;
}
.dark-theme .checkbox-label {
  color: #e5e7eb;
}

/* Field Config */
.field-config {
  padding: 24px;
  background-color: #f9fafb;
  border-radius: 8px;
}
.dark-theme .field-config {
  background-color: #374151;
}
.subsection-title {
  font-size: 18px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 16px;
}
.dark-theme .subsection-title {
  color: #e5e7eb;
}
.config-table {
  width: 100%;
  border-collapse: collapse;
}
.config-header {
  background-color: #f3f4f6;
}
.dark-theme .config-header {
  background-color: #4b5563;
}
.config-th {
  padding: 12px;
  text-align: left;
  font-weight: 500;
  color: #374151;
}
.dark-theme .config-th {
  color: #e5e7eb;
}
.config-row:hover {
  background-color: #f9fafb;
}
.dark-theme .config-row:hover {
  background-color: #374151;
}
.config-td {
  padding: 12px;
  border-bottom: 1px solid #e5e7eb;
}
.dark-theme .config-td {
  border-bottom-color: #6b7280;
}
.config-actions {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
.save-config-button {
  padding: 8px 16px;
  border-radius: 6px;
  background-color: #10b981;
  color: #ffffff;
}
.django-admin-button {
  padding: 8px 16px;
  border-radius: 6px;
}

/* Dialog */
.custom-dialog {
  border-radius: 8px;
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.2);
}
.dialog-header-custom {
  display: flex;
  align-items: center;
  background-color: #3b82f6;
  color: #ffffff;
  padding: 16px;
  border-radius: 8px 8px 0 0;
}
.dialog-header-icon {
  margin-right: 12px;
  font-size: 20px;
}
.dialog-content {
  padding: 16px;
}
.dialog-row {
  margin-bottom: 12px;
}
.dialog-label {
  color: #374151;
  font-weight: 500;
}
.dark-theme .dialog-label {
  color: #e5e7eb;
}
.dialog-value {
  margin-left: 8px;
}
.cancel-button {
  padding: 8px 16px;
  border-radius: 6px;
}

/* Fallback */
.fallback {
  text-align: center;
  padding: 24px;
}
.loading-text {
  color: #6b7280;
  animation: pulse 1.5s infinite;
}
.dark-theme .loading-text {
  color: #d1d5db;
}
.error-text {
  color: #ef4444;
  font-weight: 500;
}
.dark-theme .error-text {
  color: #f87171;
}

/* Responsive Design */
@media (max-width: 768px) {
  .tab-view .p-tabview-nav {
    flex-direction: column;
  }
  .tab-view .p-tabview-nav-link {
    border-radius: 6px;
    margin-bottom: 8px;
  }
  .header-buttons {
    flex-direction: column;
    gap: 8px;
  }
  .filter-bar {
    flex-direction: column;
    gap: 8px;
  }
  .filter-dropdown, .filter-input {
    width: 100%;
  }
}

/* Animation Keyframes */
@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}
</style>

