<template>
  <div class="system-config-section card">
    <div class="header">
      <h2 class="section-title">Cấu Hình Hệ Thống</h2>
      <Button
        label="Django Admin"
        icon="pi pi-external-link"
        text
        @click="goToDjangoAdmin"
        class="django-admin-button"
        aria-label="Truy cập Django Admin"
      />
    </div>
    <h3 class="subsection-title">Cấu hình trường hiển thị</h3>
    <table class="config-table">
      <thead>
        <tr class="config-header">
          <th class="config-th">Trường</th>
          <th v-for="role in roles" :key="role" class="config-th">
            {{ role }}
            <Checkbox
              :inputId="'checkall-' + role"
              :checked="isAllChecked(role)"
              :indeterminate="isIndeterminate(role)"
              @change="toggleCheckAll(role, $event)"
              :aria-label="'Chọn tất cả trường cho vai trò ' + role"
            />
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(field, key) in localFieldMap" :key="key" class="config-row">
          <td class="config-td">{{ field.label }}</td>
          <td v-for="role in roles" :key="role" class="config-td">
            <Checkbox v-model="field.roles" :value="role" :aria-label="'Hiển thị trường ' + field.label + ' cho vai trò ' + role" />
          </td>
        </tr>
      </tbody>
    </table>
    <div class="config-actions">
      <Button
        label="Lưu cấu hình"
        icon="pi pi-save"
        @click="saveConfig"
        class="save-config-button"
        aria-label="Lưu cấu hình trường hiển thị"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import Button from 'primevue/button';
import Checkbox from 'primevue/checkbox';
import { useToast } from 'primevue/usetoast';

const props = defineProps({
  fieldMap: {
    type: Object,
    required: true
  },
  roles: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(['save-field-config']);

const toast = useToast();

const localFieldMap = ref({});

watch(() => props.fieldMap, (newVal) => {
  // Deep clone the fieldMap to avoid direct mutation of prop
  localFieldMap.value = JSON.parse(JSON.stringify(newVal));
}, { immediate: true, deep: true });

const goToDjangoAdmin = () => {
  window.open('YOUR_DJANGO_ADMIN_URL', '_blank'); // Thay thế bằng URL Django Admin thực tế của bạn
};

const isAllChecked = (role) => {
  const allFieldsForRole = Object.values(localFieldMap.value).filter(field => field.visible);
  if (allFieldsForRole.length === 0) return false;
  return allFieldsForRole.every(field => field.roles.includes(role));
};

const isIndeterminate = (role) => {
  const allFieldsForRole = Object.values(localFieldMap.value).filter(field => field.visible);
  if (allFieldsForRole.length === 0) return false;
  const checkedCount = allFieldsForRole.filter(field => field.roles.includes(role)).length;
  return checkedCount > 0 && checkedCount < allFieldsForRole.length;
};

const toggleCheckAll = (role, event) => {
  const isChecked = event.checked;
  for (const key in localFieldMap.value) {
    if (localFieldMap.value[key].visible) { // Only toggle visible fields
      const index = localFieldMap.value[key].roles.indexOf(role);
      if (isChecked && index === -1) {
        localFieldMap.value[key].roles.push(role);
      } else if (!isChecked && index !== -1) {
        localFieldMap.value[key].roles.splice(index, 1);
      }
    }
  }
};

const saveConfig = () => {
  // Emit the updated field map to the parent
  emit('save-field-config', localFieldMap.value);
  toast.add({ severity: 'success', summary: 'Thành công', detail: 'Cấu hình trường đã được lưu', life: 3000 });
};
</script>

<style scoped>
/* Styles from ProfileView.vue related to System Config */
.system-config-section {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  font-size: 1.6em;
  color: #333;
  margin: 0;
}

.subsection-title {
  font-size: 1.2em;
  color: #555;
  margin-top: 25px;
  margin-bottom: 15px;
}

.config-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.config-th, .config-td {
  padding: 12px 15px;
  border: 1px solid #ddd;
  text-align: left;
}

.config-th {
  background-color: #f2f2f2;
  font-weight: bold;
  color: #444;
  white-space: nowrap; /* Prevent header wrapping */
}

.config-th:first-child {
  width: 30%; /* Adjust as needed */
}

.config-row:nth-child(even) {
  background-color: #f9f9f9;
}

.config-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>