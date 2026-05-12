import { createRouter, createWebHistory } from 'vue-router'
import RegistrationView from '../views/RegistrationView.vue'
import AdminView from '../views/AdminView.vue'

const routes = [
  { path: '/', component: RegistrationView },
  { path: '/admin', component: AdminView },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
