<template>
  <div class="activity-view">
    <h1>Lịch Sử Hoạt Động</h1>
    <div class="filters">
      <input v-model="filters.search" placeholder="Tìm kiếm..." @input="fetchActivities" />
      <select v-model="filters.activity_type" @change="fetchActivities">
        <option value="">Tất cả loại hoạt động</option>
        <option v-for="type in activityTypes" :key="type.value" :value="type.value">{{ type.label }}</option>
      </select>
      <input type="date" v-model="filters.start_date" @change="fetchActivities" />
      <input type="date" v-model="filters.end_date" @change="fetchActivities" />
      <button @click="exportActivities">Xuất Excel</button>
    </div>
    <table>
      <thead>
        <tr>
          <th>Người dùng</th>
          <th>Loại hoạt động</th>
          <th>Mô tả</th>
          <th>IP Address</th>
          <th>Ngày tạo</th>
          <th>Ngày cập nhật</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="activity in activities" :key="activity.id">
          <td>{{ activity.user.username }}</td>
          <td>{{ activity.activity_type_display }}</td>
          <td>{{ activity.description || '-' }}</td>
          <td>{{ activity.ip_address || '-' }}</td>
          <td>{{ formatDate(activity.created_at) }}</td>
          <td>{{ formatDate(activity.updated_at) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api, { endpoints } from '@/services/api';
import { format } from 'date-fns';

interface Activity {
  id: number;
  user: {
    username: string;
  };
  activity_type_display: string;
  description: string | null;
  ip_address: string | null;
  created_at: string;
  updated_at: string;
}

const activities = ref<Activity[]>([]);

const filters = ref({
  activity_type: '',
  start_date: '',
  end_date: '',
  search: '',
});

const activityTypes = [
  { value: 'login', label: 'Đăng nhập' },
  { value: 'logout', label: 'Đăng xuất' },
  { value: 'create', label: 'Tạo mới' },
  { value: 'update', label: 'Cập nhật' },
  { value: 'delete', label: 'Xóa' },
  { value: 'view', label: 'Xem' },
];

const fetchActivities = async () => {
  try {
    const params: Record<string, string> = {};
    if (filters.value.activity_type) params.activity_type = filters.value.activity_type;
    if (filters.value.start_date) params.start_date = filters.value.start_date;
    if (filters.value.end_date) params.end_date = filters.value.end_date;
    if (filters.value.search) params.search = filters.value.search;

    const response = await api.get(endpoints.activities, { params });
    activities.value = response.data;
  } catch (error) {
    console.error('Error fetching activities:', error);
  }
};

const exportActivities = async () => {
  try {
    const params: Record<string, string> = {};
    if (filters.value.activity_type) params.activity_type = filters.value.activity_type;
    if (filters.value.start_date) params.start_date = filters.value.start_date;
    if (filters.value.end_date) params.end_date = filters.value.end_date;
    if (filters.value.search) params.search = filters.value.search;

    const response = await api.get(endpoints.activities + 'export/', {
      params,
      responseType: 'blob',
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `activities_${new Date().toISOString().slice(0, 10)}.xlsx`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (error) {
    console.error('Error exporting activities:', error);
  }
};

const formatDate = (dateStr: string) => {
  return format(new Date(dateStr), 'dd/MM/yyyy HH:mm');
};

onMounted(() => {
  fetchActivities();
});
</script>

<style scoped>
.activity-view {
  padding: 20px;
}
.filters {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}
button {
  padding: 8px 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: #45a049;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
th {
  background-color: #f2f2f2;
}
</style>
