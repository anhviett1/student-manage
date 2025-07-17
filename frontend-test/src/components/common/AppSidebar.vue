<template>
  <aside class="app-sidebar p-card">
    <div class="p-card-header p-text-center p-py-3">
      <h3 class="p-text-primary p-text-2xl p-mb-0">{{ title }}</h3>
    </div>
    <p-menu :model="menuItemsModel" class="p-menu-sidebar" />
  </aside>
</template>

<script setup>
import { defineProps, computed } from 'vue';
import { useRouter } from 'vue-router';

// PrimeVue Components
import PMenu from 'primevue/menu';
import PCard from 'primevue/card';

const props = defineProps({
  title: {
    type: String,
    default: 'Menu'
  },
  menuItems: {
    type: Array,
    required: true,
    default: () => []
  }
});

const router = useRouter();

const menuItemsModel = computed(() => {
  return props.menuItems.map(item => ({
    label: item.title,
    icon: item.icon,
    command: () => router.push(item.to),
    class: router.currentRoute.value.path === item.to ? 'router-link-active' : ''
  }));
});
</script>

<style scoped>
.app-sidebar {
  width: 250px;
  background-color: var(--p-surface-0); /* Nền trắng/sáng của PrimeVue */
  color: var(--p-text-color);
  box-shadow: var(--p-card-shadow); /* Shadow của PrimeVue */
  border-radius: var(--p-border-radius);
  padding: 0; /* Loại bỏ padding mặc định của card để menu có thể full width */
  height: 100%; /* Đảm bảo sidebar chiếm hết chiều cao */
  overflow-y: auto; /* Cho phép cuộn nếu nội dung dài */
}

.p-menu-sidebar {
  width: 100%;
  border: none; /* Loại bỏ border mặc định của menu */
  background: transparent; /* Nền trong suốt để card background hiển thị */
  padding: 1rem 0; /* Padding cho toàn bộ menu */
}

/* Ghi đè kiểu dáng cho mục menu đang active */
.p-menu-sidebar :deep(.p-menuitem-link.router-link-active) {
  background-color: var(--p-primary-100); /* Màu nền sáng hơn cho mục đang chọn */
  color: var(--p-primary-color); /* Màu chữ chính của theme */
  font-weight: bold;
}

.p-menu-sidebar :deep(.p-menuitem-link.router-link-active .p-menuitem-icon) {
  color: var(--p-primary-color); /* Màu icon tương ứng */
}
</style>