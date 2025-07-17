<!-- Trang cài đặt hệ thống --><template>
  <div class="system-settings-page p-fluid">
    <p-card class="settings-card">
      <template #title>
        <i class="pi pi-cog p-mr-2"></i> Cài đặt Hệ thống
      </template>
      <template #content>
        <form @submit.prevent="saveSettings" class="p-formgrid p-grid">
          <div class="p-col-12 p-text-bold p-text-lg p-mb-3">Thông tin chung</div>

          <div class="p-col-12 p-md-6">
            <span class="p-float-label p-mb-4">
              <p-input-text id="schoolName" v-model="settings.school_name" :class="{'p-invalid': v$.school_name.$error}" />
              <label for="schoolName">Tên Trường/Tổ chức</label>
            </span>
            <small class="p-error" v-for="error of v$.school_name.$errors" :key="error.$uid">{{ error.$message }}</small>
          </div>

          <div class="p-col-12 p-md-6">
            <span class="p-float-label p-mb-4">
              <p-calendar id="currentAcademicYear" v-model="settings.current_academic_year" view="year" dateFormat="yy" :class="{'p-invalid': v$.current_academic_year.$error}" showIcon />
              <label for="currentAcademicYear">Năm học hiện tại</label>
            </span>
            <small class="p-error" v-for="error of v$.current_academic_year.$errors" :key="error.$uid">{{ error.$message }}</small>
          </div>

          <div class="p-col-12 p-md-6">
            <span class="p-float-label p-mb-4">
              <p-input-text id="adminEmail" v-model="settings.admin_email" :class="{'p-invalid': v$.admin_email.$error}" />
              <label for="adminEmail">Email Quản trị hệ thống</label>
            </span>
            <small class="p-error" v-for="error of v$.admin_email.$errors" :key="error.$uid">{{ error.$message }}</small>
          </div>

          <div class="p-col-12 p-text-bold p-text-lg p-mb-3 p-mt-4">Cài đặt Đăng ký môn học</div>

          <div class="p-col-12 p-md-6">
            <span class="p-float-label p-mb-4">
              <p-calendar id="registrationStartDate" v-model="settings.registration_start_date" dateFormat="dd/mm/yy" :class="{'p-invalid': v$.registration_start_date.$error}" showIcon />
              <label for="registrationStartDate">Ngày bắt đầu đăng ký</label>
            </span>
            <small class="p-error" v-for="error of v$.registration_start_date.$errors" :key="error.$uid">{{ error.$message }}</small>
          </div>

          <div class="p-col-12 p-md-6">
            <span class="p-float-label p-mb-4">
              <p-calendar id="registrationEndDate" v-model="settings.registration_end_date" dateFormat="dd/mm/yy" :class="{'p-invalid': v$.registration_end_date.$error}" showIcon />
              <label for="registrationEndDate">Ngày kết thúc đăng ký</label>
            </span>
            <small class="p-error" v-for="error of v$.registration_end_date.$errors" :key="error.$uid">{{ error.$message }}</small>
          </div>
          
          <div class="p-col-12 p-text-bold p-text-lg p-mb-3 p-mt-4">Cài đặt Bảo mật</div>
          <div class="p-col-12">
            <p-checkbox id="requireStrongPassword" v-model="settings.require_strong_password" :binary="true" />
            <label for="requireStrongPassword" class="p-ml-2">Yêu cầu mật khẩu mạnh (chứa chữ hoa, chữ thường, số, ký tự đặc biệt)</label>
          </div>


          <div class="p-col-12 p-text-center p-mt-5">
            <p-button type="submit" label="Lưu Cài đặt" icon="pi pi-save" :loading="isSaving" />
          </div>
        </form>
      </template>
    </p-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { required, email, minLength, maxLength } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import { useNotificationStore } from '@/stores/notification';

// PrimeVue Components
import PCard from 'primevue/card';
import PInputText from 'primevue/inputtext';
import PCalendar from 'primevue/calendar';
import PCheckbox from 'primevue/checkbox';
import PButton from 'primevue/button';

// Giả lập API cho cài đặt hệ thống
const systemSettingsApi = {
  getSettings: async () => {
    // Mô phỏng lấy cài đặt từ backend
    return new Promise(resolve => setTimeout(() => {
      resolve({
        school_name: 'Đại học ABC',
        current_academic_year: new Date('2024-09-01'), // Lưu dưới dạng Date object
        admin_email: 'admin@truongabc.edu.vn',
        registration_start_date: new Date('2025-08-01'),
        registration_end_date: new Date('2025-08-31'),
        require_strong_password: true,
      });
    }, 500));
  },
  updateSettings: async (newSettings) => {
    // Mô phỏng gửi cài đặt đã cập nhật lên backend
    console.log('Saving system settings:', newSettings);
    return new Promise(resolve => setTimeout(() => resolve({ success: true }), 500));
  }
};

const notificationStore = useNotificationStore();

const settings = reactive({
  school_name: '',
  current_academic_year: null,
  admin_email: '',
  registration_start_date: null,
  registration_end_date: null,
  require_strong_password: false,
});

const isSaving = ref(false);

// Vuelidate rules
const rules = computed(() => ({
  school_name: { required, minLength: minLength(5), maxLength: maxLength(200) },
  current_academic_year: { required },
  admin_email: { required, email, maxLength: maxLength(100) },
  registration_start_date: { required },
  registration_end_date: { required },
  require_strong_password: {}, // Không cần rule đặc biệt cho checkbox
}));

const v$ = useVuelidate(rules, settings);

// --- Lifecycle Hook ---
onMounted(() => {
  fetchSettings();
});

// --- Data Fetching Function ---
const fetchSettings = async () => {
  try {
    const data = await systemSettingsApi.getSettings();
    // Gán dữ liệu fetched vào reactive object
    Object.assign(settings, data);
    notificationStore.showToast('Thành công', 'Tải cài đặt hệ thống thành công!', 'success');
  } catch (error) {
    console.error('Error fetching settings:', error);
    notificationStore.showToast('Lỗi', 'Không thể tải cài đặt hệ thống.', 'error');
  }
};

// --- Form Submission Handler ---
const saveSettings = async () => {
  const result = await v$.value.$validate();
  if (result) {
    isSaving.value = true;
    try {
      // Chuẩn bị dữ liệu gửi đi (chuyển Date objects về định dạng ISO string nếu API yêu cầu)
      const settingsToSave = { ...settings };
      if (settingsToSave.current_academic_year) {
        settingsToSave.current_academic_year = settingsToSave.current_academic_year.getFullYear(); // Chỉ lấy năm
      }
      if (settingsToSave.registration_start_date) {
        settingsToSave.registration_start_date = settingsToSave.registration_start_date.toISOString().split('T')[0];
      }
      if (settingsToSave.registration_end_date) {
        settingsToSave.registration_end_date = settingsToSave.registration_end_date.toISOString().split('T')[0];
      }

      await systemSettingsApi.updateSettings(settingsToSave);
      notificationStore.showToast('Thành công', 'Cài đặt hệ thống đã được lưu!', 'success');
    } catch (error) {
      console.error('Error saving settings:', error);
      notificationStore.showToast('Lỗi', 'Có lỗi xảy ra khi lưu cài đặt.', 'error');
    } finally {
      isSaving.value = false;
    }
  } else {
    notificationStore.showToast('Lỗi nhập liệu', 'Vui lòng kiểm tra lại các trường bị lỗi!', 'error');
  }
};
</script>

<style scoped>
.system-settings-page {
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
}

.settings-card {
  border-radius: var(--p-card-border-radius);
  box-shadow: var(--p-card-shadow);
}

.p-mb-4 {
  margin-bottom: 1.5rem !important;
}

.p-mt-4 {
    margin-top: 1.5rem !important;
}

.p-mt-5 {
    margin-top: 2rem !important;
}

.p-text-bold {
    font-weight: bold;
}

.p-text-lg {
    font-size: 1.125rem; /* ~18px */
}
</style>