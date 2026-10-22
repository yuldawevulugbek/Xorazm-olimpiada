import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import tilt from './directives/tilt'
import './assets/styles.css'
import './assets/xorazm.css'

createApp(App).use(router).directive('tilt', tilt).mount('#app')
