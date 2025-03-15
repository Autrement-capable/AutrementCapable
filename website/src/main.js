import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'
import './assets/styles.css'
import '@mdi/font/css/materialdesignicons.css';
import * as PIXI from 'pixi.js';

if (process.env.NODE_ENV === 'development') {
    window.PIXI = PIXI;
  }  

createApp(App).use(router).mount('#app')
