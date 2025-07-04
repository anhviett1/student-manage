<template>
    <div class="activity-view">
      <h1>Lịch Sử Hoạt Động</h1>
      <button @click="exportActivities">Xuất Excel</button>
      <table>
        <thead>
          <tr>
            <th>Người dùng</th>
            <th>Loại hoạt động</th>
            <th>Mô tả</th>
            <th>IP Address</th>
            <th>Ngày tạo</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="activity in activities" :key="activity.id">
            <td>{{ activity.user.username }}</td>
            <td>{{ activity.activity_type_display }}</td>
            <td>{{ activity.description || '-' }}</td>
            <td>{{ activity.ip_address || '-' }}</td>
            <td>{{ formatDate(activity.created_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  import api, { endpoints } from '@/api.js';
  import { format } from 'date-fns';
  
  export default {
    name: 'ActivityView',
    data() {
      return {
        activities: [],
      };
    },
    async created() {
      await this.fetchActivities();
    },
    methods: {
      async fetchActivities() {
        try {
          const response = await api.get(endpoints.activities);
          this.activities = response.data;
        } catch (error) {
          console.error('Error fetching activities:', error);
        }
      },
      async exportActivities() {
        try {
          const response = await api.get(endpoints.activities + 'export/', {
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
      },
      formatDate(date) {
        return format(new Date(date), 'dd/MM/yyyy HH:mm');
      },
    },
  };
  </script>
  
  <style scoped>
  .activity-view {
    padding: 20px;
  }
  button {
    margin-bottom: 10px;
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
  th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }
  th {
    background-color: #f2f2f2;
  }
  </style>