import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';
import PrimeVue from 'primevue/config'; // Import PrimeVue một lần duy nhất
import Aura from '@primevue/themes/aura'; // Import theme preset
import ToastService from 'primevue/toastservice'; // Import ToastService

// CSS của PrimeVue và các icon
import 'primevue/resources/themes/lara-light-indigo/theme.css'; // Hoặc bỏ nếu dùng Aura theme hoàn toàn
import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';
import 'primeflex/primeflex.css'; // PrimeFlex cho layout và utility classes
import '@mdi/font/css/materialdesignicons.css'; // Material Design Icons

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);

app.use(PrimeVue, {
  theme: {
    preset: Aura, // Sử dụng Aura theme làm mặc định
    options: {
      // Bạn có thể tùy chỉnh prefix CSS class, dark mode selector ở đây
      prefix: 'p',
      darkModeSelector: '.app-dark', // Selector để kích hoạt dark mode nếu cần
    }
  },
  // Cấu hình ripple hiệu ứng click
  ripple: true
});

// Đăng ký ToastService cho PrimeVue (quan trọng cho PToast)
app.use(ToastService);

app.mount('#app');