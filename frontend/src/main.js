import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min'
import './assets/main.css'

import { OhVueIcon, addIcons } from 'oh-vue-icons'

import {
  FaClock,
  FaHistory,
  FaUserCircle,
  FaInfoCircle,
  FaStar,
  FaCalendar,
  CoChart,
  CoUser,
  FaHourglassHalf,
  FaParking,
  FaRupeeSign,
  FaTools,
  FaUserShield,
  FaUsers,
  FaMapMarkerAlt,
  FaBars,
  FaSignInAlt,
  FaSignOutAlt,
} from 'oh-vue-icons/icons'

addIcons(
  FaHistory,
  FaHourglassHalf,
  FaClock,
  CoUser,
  FaParking,
  FaRupeeSign,
  FaUserCircle,
  FaInfoCircle,
  FaStar,
  FaCalendar,
  CoChart,
  FaTools,
  FaUserShield,
  FaUsers,
  FaMapMarkerAlt,
  FaBars,
  FaSignInAlt,
  FaSignOutAlt,
)

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.component('v-icon', OhVueIcon)

app.mount('#app')
