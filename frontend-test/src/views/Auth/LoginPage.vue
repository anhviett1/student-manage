<template>
  <div class="p-d-flex p-jc-center p-ai-center" style="min-height: 100vh; background-color: #f2f5f7;">
    <Card style="width: 25rem; overflow: hidden;">
      <template #title>
        <div class="p-text-center">Đăng nhập</div>
      </template>
      <template #content>
        <form @submit.prevent="login" class="p-fluid">
          <div class="p-field">
            <span class="p-float-label">
              <InputText id="username" v-model="username" type="text" required />
              <label for="username">Tên đăng nhập</label>
            </span>
          </div>
          <div class="p-field">
            <span class="p-float-label">
              <Password id="password" v-model="password" :toggleMask="true" required />
              <label for="password">Mật khẩu</label>
            </span>
          </div>
          <Button type="submit" label="Đăng nhập" class="p-mt-3" />
        </form>
      </template>
    </Card>
    <Toast />
  </div>
</template>

<script>
import { useToast } from 'primevue/usetoast';

export default {
  name: 'LoginPage',
  setup() {
    const toast = useToast();
    return { toast };
  },
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async login() {
      // Logic đăng nhập thực tế sẽ gọi API
      console.log('Đăng nhập với:', this.username, this.password);
      try {
        // Giả lập API call
        await new Promise(resolve => setTimeout(resolve, 1000));

        if (this.username === 'admin' && this.password === 'admin') {
          this.toast.add({ severity: 'success', summary: 'Thành công', detail: 'Đăng nhập thành công!', life: 3000 });
          // Chuyển hướng đến Dashboard chính hoặc AdminDashboard
          this.$router.push('/admin/dashboard');
        } else if (this.username === 'teacher' && this.password === 'teacher') {
          this.toast.add({ severity: 'success', summary: 'Thành công', detail: 'Đăng nhập thành công!', life: 3000 });
          this.$router.push('/teacher/dashboard');
        } else if (this.username === 'student' && this.password === 'student') {
          this.toast.add({ severity: 'success', summary: 'Thành công', detail: 'Đăng nhập thành công!', life: 3000 });
          this.$router.push('/student/dashboard');
        }
        else {
          this.toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Tên đăng nhập hoặc mật khẩu không đúng.', life: 3000 });
        }
      } catch (error) {
        this.toast.add({ severity: 'error', summary: 'Lỗi', detail: 'Đã có lỗi xảy ra khi đăng nhập.', life: 3000 });
        console.error('Login error:', error);
      }
    },
  },
};
</script>

<style scoped>

.p-field {
  margin-bottom: 1.5rem;
}
</style>