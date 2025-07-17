<template>
  <p-dialog
    :visible="isVisible"
    modal
    :header="title"
    :style="{ width: '30rem' }"
    :breakpoints="{ '1199px': '75vw', '575px': '90vw' }"
    @update:visible="cancel"
  >
    <div class="p-text-center p-py-3">
      <i class="mdi mdi-alert-circle-outline p-text-4xl p-text-orange-500 p-mb-3"></i>
      <p class="p-text-lg">{{ message }}</p>
    </div>

    <template #footer>
      <p-button label="Hủy bỏ" icon="pi pi-times" text @click="cancel" />
      <p-button label="Xác nhận" icon="pi pi-check" severity="danger" @click="confirm" />
    </template>
  </p-dialog>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

// PrimeVue Components
import PDialog from 'primevue/dialog';
import PButton from 'primevue/button';

const props = defineProps({
  isVisible: { type: Boolean, required: true },
  title: { type: String, default: 'Xác nhận hành động' },
  message: { type: String, default: 'Bạn có chắc chắn muốn thực hiện hành động này?' }
});

const emit = defineEmits(['confirm', 'cancel']);

const confirm = () => {
  emit('confirm');
};

const cancel = () => {
  emit('cancel');
};
</script>

<style scoped>

</style>