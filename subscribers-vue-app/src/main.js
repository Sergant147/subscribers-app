import './assets/main.css'
import { createRouter, createWebHistory } from 'vue-router'

import Logged from './pages/Logged.vue'
import Main from './pages/Main.vue'
import Signup from './pages/Signup.vue'
import Login from './pages/Login.vue'
import DoSubscribes from '@/pages/DoSubscribes.vue'
import SetMyURL from '@/pages/SetMyURL.vue'

import { createApp } from 'vue'
import App from './App.vue'
const routes = [
  { component: Logged, path: '/logged', name: 'Logged' },
  { component: Main, path: '/', name: 'Main' },
  { component: Signup, path: '/signup', name: 'Signup' },
  { component: Login, path: '/login', name: 'Login' },
  { component: DoSubscribes, path: '/action', name: 'DoSubscribes' },
  { component: SetMyURL, path: '/urlset', name: 'SetMyURL' },
]
createApp(App)
  .use(createRouter({ routes: routes, history: createWebHistory() }))
  .mount('#app')
