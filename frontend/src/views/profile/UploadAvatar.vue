<template>
  <div class="upload-avatar-section" aria-label="Phần tải lên ảnh đại diện">
    <Toast aria-live="polite" />
    <ConfirmDialog aria-live="assertive" />
    
    <div class="card">
      <h2>Ảnh Đại Diện</h2>
      
      <div class="avatar-preview-section">
        <div class="current-avatar">
          <div class="avatar-container">
            <img 
              v-if="profilePicture" 
              :src="profilePicture" 
              alt="Ảnh đại diện hiện tại"
              class="current-avatar-img"
            />
            <img
              v-else-if="userRole === 'admin' && adminDefaultImg"
              :src="adminDefaultImg"
              alt="Ảnh mặc định admin"
              class="current-avatar-img"
            />
            <div v-else class="no-avatar">
              <i class="pi pi-user" />
              <span>Chưa có ảnh đại diện</span>
            </div>
          </div>
        </div>
        
        <div class="new-avatar" v-if="canEdit">
          <h3>Ảnh mới:</h3>
          <div class="upload-area" @click="triggerFileInput" @drop="handleDrop" @dragover.prevent>
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              @change="handleFileSelect"
              style="display: none"
              aria-label="Chọn file ảnh"
            />
            <div v-if="!previewImage" class="upload-placeholder">
              <i class="pi pi-upload" />
              <p>Click để chọn ảnh hoặc kéo thả file vào đây</p>
              <p class="upload-hint">Hỗ trợ: JPG, PNG, GIF (tối đa 5MB)</p>
            </div>
            <div v-else class="preview-container">
              <img :src="previewImage" alt="Xem trước ảnh" class="preview-image" />
              <Button
                icon="pi pi-times"
                rounded
                severity="danger"
                class="remove-preview"
                @click="removePreview"
                aria-label="Xóa ảnh xem trước"
              />
            </div>
          </div>
        </div>
      </div>
      
      <div class="upload-actions" v-if="canEdit">
        <Button
          icon="pi pi-upload"
          label="Tải lên ảnh"
          severity="primary"
          :loading="uploading"
          :disabled="!selectedFile || uploading"
          @click="uploadAvatar"
          class="mr-2"
          aria-label="Tải lên ảnh đại diện"
        />
        <Button
          icon="pi pi-times"
          label="Hủy"
          severity="secondary"
          outlined
          @click="resetForm"
          :disabled="uploading"
          aria-label="Hủy thay đổi"
        />
      </div>
      
      <div v-if="uploadProgress > 0 && uploadProgress < 100" class="upload-progress">
        <ProgressBar :value="uploadProgress" />
        <span class="progress-text">{{ uploadProgress }}%</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';
import  api,{ endpoints } from '@/services/api';
import Button from 'primevue/button';
import Toast from 'primevue/toast';
import ConfirmDialog from 'primevue/confirmdialog';
import ProgressBar from 'primevue/progressbar';
import adminDefaultImg from '@/assets/images/admin.png';

const baseUrl = 'http://localhost:8000' || 'http://127.0.0.1:8000' || import.meta.env.VITE_API_BASE_URL;

const props = defineProps({
  profilePicture: { type: String, default: null },
  userRole: { type: String, required: true },
  canEdit: { type: Boolean, default: false },
});

const emit = defineEmits(['update:avatar']);

const toast = useToast();
const confirm = useConfirm();

const fileInput = ref(null);
const selectedFile = ref(null);
const previewImage = ref(null);
const uploading = ref(false);
const uploadProgress = ref(0);

watch(() => props.profilePicture, (newVal) => {
  previewImage.value = newVal;
});

const triggerFileInput = () => {
  if (!props.canEdit || !fileInput.value) {
    toast.add({ severity: 'info', summary: 'Thông báo', detail: 'Bạn không có quyền tải lên ảnh đại diện.', life: 3000 });
    return;
  }
  fileInput.value.click();
};

const handleFileSelect = (event) => {
  const file = event.target.files[0];
  if (file) {
    validateAndSetFile(file);
  }
};

const handleDrop = (event) => {
  event.preventDefault();
  if (!props.canEdit) {
    toast.add({ severity: 'info', summary: 'Thông báo', detail: 'Bạn không có quyền tải lên ảnh đại diện.', life: 3000 });
    return;
  }
  const file = event.dataTransfer.files[0];
  if (file) {
    validateAndSetFile(file);
  }
};

const validateAndSetFile = (file) => {
  if (!file.type.startsWith('image/')) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Vui lòng chọn file ảnh hợp lệ', life: 3000 });
    return;
  }
  
  const maxSize = 5 * 1024 * 1024;
  if (file.size > maxSize) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Kích thước file không được vượt quá 5MB', life: 3000 });
    return;
  }
  
  selectedFile.value = file;
  createPreview(file);
};

const createPreview = (file) => {
  const reader = new FileReader();
  reader.onload = (e) => {
    previewImage.value = e.target.result;
  };
  reader.readAsDataURL(file);
};

const removePreview = () => {
  selectedFile.value = null;
  previewImage.value = null;
  if (fileInput.value) {
    fileInput.value.value = '';
  }
};

const uploadAvatar = async () => {
  if (!selectedFile.value) {
    toast.add({ severity: 'warn', summary: 'Cảnh báo', detail: 'Vui lòng chọn ảnh trước khi tải lên', life: 3000 });
    return;
  }
  
  uploading.value = true;
  uploadProgress.value = 0;
  
  try {
    const formData = new FormData();
    formData.append('avatar', selectedFile.value);
    
    const response = await api.post(endpoints.uploadAvatar, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (progressEvent) => {
        uploadProgress.value = Math.round((progressEvent.loaded * 100) / progressEvent.total);
      },
    });
    
    const avatarUrl = `${baseUrl}${response.data.avatar_url}?t=${new Date().getTime()}`;
    toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cập nhật ảnh đại diện thành công', life: 3000 });
    
    emit('update:avatar', avatarUrl);
    resetForm();
    
  } catch (error) {
    console.error('Upload error:', error);
    let errorMessage = 'Có lỗi xảy ra khi tải lên ảnh';
    
    if (error.response?.data?.detail) {
      errorMessage = error.response.data.detail;
    } else if (error.response?.data?.avatar) {
      errorMessage = error.response.data.avatar[0];
    }
    
    toast.add({ severity: 'error', summary: 'Lỗi', detail: errorMessage, life: 5000 });
  } finally {
    uploading.value = false;
    uploadProgress.value = 0;
  }
};

const resetForm = () => {
  selectedFile.value = null;
  previewImage.value = null;
  uploadProgress.value = 0;
  if (fileInput.value) {
    fileInput.value.value = '';
  }
};
</script>

<style scoped>
.upload-avatar-section {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}
.card {
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
}
.card h2 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #1f2937;
  padding: auto;
}
.dark-theme .card h2 {
  color: #f3f4f6;
}
.avatar-preview-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
.current-avatar, .new-avatar {
  flex: 1;
  margin: 0 10px;
}
.current-avatar h3, .new-avatar h3 {
  font-size: 18px;
  margin-bottom: 10px;
  color: #374151;
}
.dark-theme .current-avatar h3, .dark-theme .new-avatar h3 {
  color: #e5e7eb;
}
.avatar-container {
  text-align: center;
}
.current-avatar-img {
  width: 128px;
  height: 128px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #d1d5db;
}
.no-avatar {
  width: 128px;
  height: 128px;
  border-radius: 50%;
  background: #f3f4f6;
  border: 2px solid #d1d5db;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #6b7280;
}
.dark-theme .no-avatar {
  background: #4b5563;
  border-color: #6b7280;
  color: #d1d5db;
}
.upload-area {
  border: 2px dashed #d1d5db;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}
.upload-area:hover {
  border-color: #3b82f6;
  background: #f9fafb;
}
.dark-theme .upload-area {
  border-color: #6b7280;
}
.dark-theme .upload-area:hover {
  background: #374151;
}
.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}
.upload-placeholder i {
  font-size: 24px;
  color: #6b7280;
}
.upload-placeholder p {
  margin: 0;
  color: #374151;
}
.upload-hint {
  font-size: 12px;
  color: #6b7280;
}
.dark-theme .upload-placeholder i, .dark-theme .upload-placeholder p, .dark-theme .upload-hint {
  color: #d1d5db;
}
.preview-container {
  position: relative;
}
.preview-image {
  width: 128px;
  height: 128px;
  border-radius: 8px;
  object-fit: cover;
}
.remove-preview {
  position: absolute;
  top: -10px;
  right: -10px;
}
.upload-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 20px;
}
.upload-progress {
  margin-top: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.progress-text {
  font-size: 14px;
  color: #374151;
}
.dark-theme .progress-text {
  color: #e5e7eb;
}
</style>