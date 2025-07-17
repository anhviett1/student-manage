<template>
  <p-card class="stats-card p-h-full">
    <template #content>
      <div class="p-flex p-align-center p-justify-between p-gap-2">
        <div class="stats-content">
          <div class="p-text-secondary p-text-uppercase p-text-sm p-mb-1">{{ title }}</div>
          <div class="p-text-900 p-text-3xl p-text-bold">{{ value }}</div>
        </div>
        <div :class="['stats-icon', iconBackgroundClass]">
          <i :class="['mdi', icon, 'p-text-4xl']"></i>
        </div>
      </div>
    </template>
    <template #footer v-if="trendText">
      <div :class="['p-text-sm', trendClass]">
        <i :class="['mdi', trendIcon, 'p-mr-1']"></i> {{ trendText }}
      </div>
    </template>
  </p-card>
</template>

<script setup>
import { defineProps } from 'vue';

// PrimeVue Components
import PCard from 'primevue/card';

defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [String, Number],
    required: true
  },
  icon: {
    type: String, // Ví dụ: 'mdi-account-group-outline'
    default: 'mdi-information-outline'
  },
  iconBackgroundClass: {
    type: String, // Ví dụ: 'bg-blue-100 p-text-blue-600' (PrimeFlex color classes)
    default: 'bg-surface-100 p-text-color-secondary'
  },
  trendText: {
    type: String,
    default: ''
  },
  trendClass: {
    type: String, // Ví dụ: 'p-text-green-500' hoặc 'p-text-red-500'
    default: 'p-text-secondary'
  },
  trendIcon: {
    type: String, // Ví dụ: 'mdi-arrow-up' hoặc 'mdi-arrow-down'
    default: ''
  }
});
</script>

<style scoped>
.stats-card {
  height: 100%;
  border-radius: var(--p-card-border-radius); /* Sử dụng biến CSS của PrimeVue Aura */
  box-shadow: var(--p-card-shadow); /* Sử dụng biến CSS của PrimeVue Aura */
  padding: 1.25rem; /* Padding bên trong card */
}

.stats-content {
  flex-grow: 1; /* Cho phép nội dung văn bản chiếm không gian còn lại */
}

.stats-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 64px; /* Kích thước icon */
  height: 64px;
  border-radius: var(--p-border-radius-xl); /* Làm tròn icon hơn */
  flex-shrink: 0; /* Ngăn icon bị co lại */
}

/* Các lớp màu nền và màu chữ như bg-blue-100, p-text-blue-600 là từ PrimeFlex.
   Đảm bảo bạn đã import PrimeFlex trong main.js.
   Nếu không, bạn cần định nghĩa các biến CSS này trong file CSS toàn cục của mình.
   Ví dụ trong src/assets/styles/main.css:
   :root {
       --blue-100: #e3f2fd;
       --blue-600: #1e88e5;
       --green-100: #e8f5e9;
       --green-600: #43a047;
       --orange-100: #ffe0b2;
       --orange-600: #fb8c00;
       --purple-100: #ede7f6;
       --purple-600: #673ab7;
       --red-500: #ef5350;
   }
*/
</style>