<template>
  <div class="search-filter-bar p-card p-py-3 p-px-4 p-flex p-align-center p-flex-wrap p-gap-3">
    <span class="p-input-icon-left p-flex-1">
      <i class="pi pi-search" />
      <p-input-text
        v-model="searchTermInternal"
        placeholder="Tìm kiếm..."
        class="p-inputtext-lg"
        @input="handleSearchInput"
        @keyup.enter="applyFilters"
      />
    </span>

    <slot name="filters"></slot>

    <p-button label="Áp dụng" icon="pi pi-check" @click="applyFilters" />
    <p-button v-if="hasFilters || searchTermInternal" label="Xóa lọc" icon="pi pi-times" severity="secondary" outlined @click="clearAllFilters" />
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, useSlots } from 'vue';

// PrimeVue Components
import PInputText from 'primevue/inputtext';
import PButton from 'primevue/button';
import PCard from 'primevue/card';

const props = defineProps({
  searchTerm: { type: String, default: '' }
});

const emit = defineEmits(['update:searchTerm', 'apply-filters', 'clear-filters']);

const searchTermInternal = ref(props.searchTerm);
const slots = useSlots();
const hasFilters = slots.filters;

const handleSearchInput = () => {
  emit('update:searchTerm', searchTermInternal.value);
};

const applyFilters = () => {
  emit('apply-filters', {
    searchTerm: searchTermInternal.value,
  });
};

const clearAllFilters = () => {
  searchTermInternal.value = '';
  emit('update:searchTerm', '');
  emit('clear-filters');
};
</script>

<style scoped>

/* Đảm bảo input tìm kiếm chiếm đủ không gian */
.p-input-icon-left {
  width: 100%;
  max-width: 350px; /* Giới hạn độ rộng của ô tìm kiếm */
}
:deep(.p-dropdown), :deep(.p-calendar) {
  width: 150px; 
}

</style>