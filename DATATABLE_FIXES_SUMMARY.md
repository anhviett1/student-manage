# DataTable Fixes Summary

## Vấn đề
Lỗi `TypeError: _data.slice is not a function` xảy ra khi DataTable nhận được object thay vì array. Nguyên nhân là do API response có cấu trúc `{count, next, previous, results}` nhưng code chỉ gán trực tiếp `response.data`.

## Các file đã sửa

### 1. ProfileView.vue
- **Vấn đề**: Quyền hiển thị không đúng - Admin hiển thị user list, Teacher/Student hiển thị system config
- **Giải pháp**: 
  - Tách riêng giao diện cho Admin (có tabs) và Teacher/Student (chỉ hiển thị system config)
  - Thêm conditional rendering cho DataTable
  - Sử dụng ref + watcher cho usersList thay vì computed

### 2. SubjectView.vue
- **Vấn đề**: `subjects.value = response.data` có thể là object
- **Giải pháp**:
  ```javascript
  // Ensure subjects.value is always an array
  if (response.data && Array.isArray(response.data)) {
    subjects.value = response.data
  } else if (response.data && response.data.results && Array.isArray(response.data.results)) {
    subjects.value = response.data.results
  } else {
    subjects.value = []
  }
  ```
- **Thêm**: Conditional rendering cho DataTable và fallback message

### 3. TeacherView.vue
- **Vấn đề**: `teachers.value = response.data.data` có thể không phải array
- **Giải pháp**: Tương tự SubjectView, xử lý nhiều cấu trúc response khác nhau
- **Thêm**: Conditional rendering và fallback message

### 4. StudentView.vue
- **Vấn đề**: `students.value = response.data.data` có thể không phải array
- **Giải pháp**: Tương tự các view khác
- **Thêm**: Conditional rendering và fallback message

## Pattern chung để sửa

### 1. Sửa hàm load data
```javascript
const loadData = async () => {
  try {
    loading.value = true
    const response = await api.get(endpoint, { params })
    
    // Ensure data.value is always an array
    if (response.data && Array.isArray(response.data)) {
      data.value = response.data
    } else if (response.data && response.data.data && Array.isArray(response.data.data)) {
      data.value = response.data.data
    } else if (response.data && response.data.results && Array.isArray(response.data.results)) {
      data.value = response.data.results
    } else {
      data.value = []
    }
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải dữ liệu', life: 3000 })
    data.value = []
  } finally {
    loading.value = false
  }
}
```

### 2. Conditional rendering cho DataTable
```vue
<DataTable
  v-if="(data.length > 0 || loading) && canView"
  :value="data"
  :loading="loading"
  ...
>
  <!-- templates -->
</DataTable>

<!-- Fallback when no data and not loading -->
<div v-else-if="!loading && data.length === 0 && canView" class="no-data-message">
  <p>Không có dữ liệu để hiển thị.</p>
  <Button 
    label="Tải lại" 
    icon="pi pi-refresh" 
    @click="loadData"
    severity="secondary"
  />
</div>
```

### 3. CSS cho no-data-message
```css
.no-data-message {
  text-align: center;
  padding: 3rem;
  color: #666;
  background: #f8f9fa;
  border-radius: 8px;
  margin: 1rem 0;
}

.no-data-message p {
  margin-bottom: 1rem;
  font-size: 1.1rem;
}
```

## Kết quả
- ✅ Không còn lỗi `_data.slice is not a function`
- ✅ DataTable hiển thị đúng với dữ liệu array
- ✅ Fallback UI khi không có dữ liệu
- ✅ Conditional rendering tránh lỗi khi data chưa sẵn sàng
- ✅ Quyền hiển thị đúng theo role (Admin/Teacher/Student)

## Các view cần kiểm tra thêm
- SemesterView.vue
- ScoreView.vue  
- EnrollmentView.vue
- DepartmentView.vue
- ClassView.vue
- ScheduleView.vue

Các view này có thể có cùng vấn đề và cần áp dụng pattern tương tự. 