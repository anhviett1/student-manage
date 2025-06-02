<template>
  <div class="toast-container">
    <TransitionGroup name="toast">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="['toast', toast.type]"
        @click="removeToast(toast.id)"
      >
        <div class="toast-content">
          <i :class="getIcon(toast.type)"></i>
          <span>{{ toast.message }}</span>
        </div>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { useToast } from '@/composables/useToast'

const { toasts, removeToast } = useToast()

const getIcon = (type) => {
  switch (type) {
    case 'success':
      return 'fas fa-check-circle'
    case 'error':
      return 'fas fa-exclamation-circle'
    case 'warning':
      return 'fas fa-exclamation-triangle'
    default:
      return 'fas fa-info-circle'
  }
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.toast {
  min-width: 300px;
  padding: 1rem;
  border-radius: 4px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  display: flex;
  align-items: center;
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.toast i {
  font-size: 1.25rem;
}

.toast.success {
  border-left: 4px solid #2ecc71;
}

.toast.success i {
  color: #2ecc71;
}

.toast.error {
  border-left: 4px solid #e74c3c;
}

.toast.error i {
  color: #e74c3c;
}

.toast.warning {
  border-left: 4px solid #f1c40f;
}

.toast.warning i {
  color: #f1c40f;
}

.toast.info {
  border-left: 4px solid #3498db;
}

.toast.info i {
  color: #3498db;
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style> 