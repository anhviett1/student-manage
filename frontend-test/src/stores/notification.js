// src/stores/notification.js
import { defineStore } from 'pinia';
import { useToast } from 'primevue/usetoast';

export const useNotificationStore = defineStore('notification', {
  id: 'notification',
  state: () => ({
    // No explicit state needed here for toast, useToast handles it
  }),
  actions: {
    showToast(summary, severity, detail, life = 3000) {
      const toast = useToast();
      toast.add({ severity: severity, summary: summary, detail: detail, life: life });
    },
    showSuccess(summary, detail, life = 3000) {
      this.showToast(summary, 'success', detail, life);
    },
    showInfo(summary, detail, life = 3000) {
      this.showToast(summary, 'info', detail, life);
    },
    showWarning(summary, detail, life = 3000) {
      this.showToast(summary, 'warn', detail, life);
    },
    showError(summary, detail, life = 3000) {
      this.showToast(summary, 'error', detail, life);
    },
  },
});