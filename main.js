import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import tilt from './directives/tilt'
import { wakeBackend } from './api/axios'
import './assets/styles.css'
import './assets/xorazm.css'

wakeBackend()

createApp(App).use(router).directive('tilt', tilt).mount('#app')
