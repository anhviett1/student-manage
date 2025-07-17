<template>
  <div class="pagination-controls p-flex p-jc-end p-mt-4">
    <p-paginator
      v-if="totalRecords > 0"
      :rows="itemsPerPage"
      :totalRecords="totalRecords"
      :rowsPerPageOptions="itemsPerPageOptions"
      @page="onPageChange"
      template="PrevPageLink CurrentPageReport NextPageLink RowsPerPageDropdown"
      :currentPageReportTemplate="`Trang {currentPage} / {totalPages} ({totalRecords} bản ghi)`"
    />
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

// PrimeVue Components
import PPaginator from 'primevue/paginator';

const props = defineProps({
  currentPage: { type: Number, required: true },
  totalRecords: { type: Number, required: true },
  itemsPerPage: { type: Number, default: 10 },
  itemsPerPageOptions: { type: Array, default: () => [5, 10, 20, 50] }
});

const emit = defineEmits(['page-change', 'update:currentPage', 'update:itemsPerPage']);

const onPageChange = (event) => {
  emit('page-change', { page: event.page + 1, rows: event.rows });
  emit('update:currentPage', event.page + 1);
  emit('update:itemsPerPage', event.rows);
};
</script>

<style scoped>
.pagination-controls {
  padding: 0.5rem;
  background-color: var(--p-surface-0);
  border-radius: var(--p-border-radius);
  box-shadow: var(--p-shadow-1);
  display: flex; /* Đảm bảo flex để căn chỉnh */
  justify-content: flex-end; /* Căn phải */
  align-items: center; /* Căn giữa theo chiều dọc */
  gap: 1rem; /* Khoảng cách giữa các phần tử */
}


:deep(.p-paginator .p-paginator-current) {
  font-weight: bold;
}
</style>