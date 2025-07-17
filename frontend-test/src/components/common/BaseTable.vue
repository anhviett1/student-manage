<template>
  <div class="base-table-container">
    <p-card>
      <template #content>
        <p-datatable
          :value="data"
          :loading="loading"
          responsiveLayout="scroll"
          stripedRows
          class="p-datatable-gridlines"
          :paginator="enablePagination"
          :rows="itemsPerPage"
          :totalRecords="totalRecords"
          :rowsPerPageOptions="itemsPerPageOptions"
          @page="onPageChange"
          :lazy="lazyLoad"
          :first="(currentPage - 1) * itemsPerPage"
          paginatorTemplate="PrevPageLink CurrentPageReport NextPageLink RowsPerPageDropdown"
          currentPageReportTemplate="Trang {currentPage} / {totalPages} ({totalRecords} bản ghi)"
        >
          <template #empty v-if="!loading">
            <div class="p-text-center p-py-3">Không có dữ liệu.</div>
          </template>
          <template #loading>
            <div class="p-text-center p-py-3 p-flex p-flex-column p-align-center p-gap-2">
              <p-progress-spinner style="width: 50px; height: 50px" strokeWidth="8" animationDuration=".8s" aria-label="Loading"></p-progress-spinner>
              <p class="p-text-lg">Đang tải dữ liệu...</p>
            </div>
          </template>

          <p-column v-for="col in columns" :key="col.field" :field="col.field" :header="col.header" :sortable="col.sortable">
            <template #body="{ data: rowData }">
              {{ formatValue(rowData[col.field], col.type) }}
            </template>
          </p-column>

          <p-column v-if="hasActions" header="Hành động" style="width: 120px; text-align: center;">
            <template #body="{ data: item }">
              <slot name="actions" :item="item"></slot>
            </template>
          </p-column>
        </p-datatable>
      </template>
    </p-card>
  </div>
</template>

<script setup>
import { defineProps, computed, useSlots, defineEmits } from 'vue';

// PrimeVue Components
import PDataTable from 'primevue/datatable';
import PColumn from 'primevue/column';
import PCard from 'primevue/card';
import PProgressSpinner from 'primevue/progressspinner';

const props = defineProps({
  data: { type: Array, default: () => [] },
  columns: { type: Array, required: true, default: () => [] },
  loading: { type: Boolean, default: false },
  enablePagination: { type: Boolean, default: false },
  currentPage: { type: Number, default: 1 },
  totalRecords: { type: Number, default: 0 },
  itemsPerPage: { type: Number, default: 10 },
  itemsPerPageOptions: { type: Array, default: () => [5, 10, 20, 50] },
  lazyLoad: { type: Boolean, default: false }
});

const emit = defineEmits(['page-change', 'sort-change']);

const slots = useSlots();
const hasActions = computed(() => !!slots.actions);

const formatValue = (value, type) => {
  if (value === null || value === undefined) {
    return 'N/A';
  }
  switch (type) {
    case 'date': return new Date(value).toLocaleDateString('vi-VN');
    case 'datetime': return new Date(value).toLocaleString('vi-VN');
    case 'currency': return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(value);
    case 'boolean': return value ? 'Có' : 'Không';
    default: return value;
  }
};

const onPageChange = (event) => {
  emit('page-change', { page: event.page + 1, rows: event.rows });
};
</script>

<style scoped>
.base-table-container {
  width: 100%;
  margin-top: 1.25rem;
}

/* Ghi đè các style của PrimeVue DataTable nếu cần */
.p-datatable-gridlines {
  border-radius: var(--p-border-radius);
  overflow: hidden;
  border: 1px solid var(--p-surface-200); /* Thêm border xung quanh bảng */
}

/* Điều chỉnh padding và font-size cho header và cell để bảng trông gọn gàng hơn */
:deep(.p-datatable .p-column-header .p-column-title) {
  font-weight: var(--p-font-bold);
  color: var(--p-text-color);
  padding: 0.8rem 1rem;
}

:deep(.p-datatable .p-datatable-tbody > tr > td) {
  padding: 0.75rem 1rem;
}

/* Có thể thêm một số media query nếu bảng cần điều chỉnh đặc biệt trên màn hình nhỏ */
@media screen and (max-width: 960px) {
  /* Ví dụ: có thể ẩn một số cột trên màn hình nhỏ nếu cần */
}
</style>