import { createRouter, createWebHistory } from 'vue-router'
import BookAppointment from '../views/BookAppointment.vue'
import AppointmentsList from '../views/AppointmentsList.vue'

const routes = [
  { path: '/', component: BookAppointment },
  { path: '/appointments', component: AppointmentsList }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
