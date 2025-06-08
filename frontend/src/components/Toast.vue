<template>
  <div class="toast-container">
    <TransitionGroup name="toast">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="['toast', `toast-${toast.severity}`]"
        @click="removeToast(toast.id)"
      >
        <div class="toast-content">
          <i :class="getIcon(toast.severity)" class="toast-icon"></i>
          <div class="toast-message">
            <strong class="toast-title">{{ toast.summary || getDefaultTitle(toast.severity) }}</strong>
            <p class="toast-detail">{{ toast.detail }}</p>
          </div>
          <Button
            icon="pi pi-times"
            text
            class="toast-close"
            @click.stop="removeToast(toast.id)"
            v-tooltip="'Close'"
          />
        </div>
        <div class="toast-progress" :style="{ width: toast.progress + '%' }"></div>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useToast } from '@/composables/useToast'
import Button from 'primevue/button'

const { toasts, removeToast } = useToast()

const getIcon = (severity) => {
  switch (severity) {
    case 'success':
      return 'pi pi-check-circle'
    case 'error':
      return 'pi pi-exclamation-circle'
    case 'warn':
      return 'pi pi-exclamation-triangle'
    default:
      return 'pi pi-info-circle'
  }
}

const getDefaultTitle = (severity) => {
  switch (severity) {
    case 'success':
      return 'Thành Công'
    case 'error':
      return 'Lỗi'
    case 'warn':
      return 'Cảnh Báo'
    default:
      return 'Thông Tin'
  }
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 1.5rem;
  right: 1.5rem;
  z-index: 10000;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  width: 400px;
}

.toast {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 1rem;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.toast-content {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.toast-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.toast-message {
  flex: 1;
}

.toast-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.toast-detail {
  font-size: 0.875rem;
  color: #4b5563;
  margin: 0;
}

.toast-close {
  font-size: 1rem;
  color: #6b7280;
  padding: 0.25rem;
}

.toast-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 4px;
  background: #3b82f6;
  transition: width 0.016s linear;
}

.toast-success {
  border-left: 4px solid #10b981;
}

.toast-success .toast-icon {
  color: #10b981;
}

.toast-success .toast-progress {
  background: #10b981;
}

.toast-error {
  border-left: 4px solid #ef4444;
}

.toast-error .toast-icon {
  color: #ef4444;
}

.toast-error .toast-progress {
  background: #ef4444;
}

.toast-warn {
  border-left: 4px solid #f59e0b;
}

.toast-warn .toast-icon {
  color: #f59e0b;
}

.toast-warn .toast-progress {
  background: #f59e0b;
}

.toast-info {
  border-left: 4px solid #3b82f6;
}

.toast-info .toast-icon {
  color: #3b82f6;
}

.toast-info .toast-progress {
  background: #3b82f6;
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateX(50px);
}
</style>