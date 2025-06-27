const loadDepartments = async () => {
  try {
    const response = await api.get(endpoints.departments)
    // Nếu response.data có trường results thì lấy results, không thì lấy data luôn
    departments.value = Array.isArray(response.data.results) ? response.data.results : response.data
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách khoa', life: 3000 })
  }
}
