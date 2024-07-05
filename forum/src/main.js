import { createApp } from 'vue'
import App from './App.vue'
import router from './router/routes'
import './assets/main.css'
import './assets/fonts.css';
import '@mdi/font/css/materialdesignicons.css';

createApp(App).use(router).mount('#app')
