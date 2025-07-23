import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

import LandingPage from '../components/LandingPage.vue';
import Login from '../components/auth/Login.vue'
import Register from '../components/auth/Register.vue'
import AdminDashboard from '../components/admin/AdminDashboard.vue'
import UserDashboard from '../components/user/UserDashboard.vue'
import PaymentPortal from '../components/PaymentPortal.vue'
import ParkingLotDetails from '../components/admin/ParkingLotDetails.vue' // Import new component

const routes = [
  { path: '/', name: 'landing', component: LandingPage },
  { path: '/login', name: 'login', component: Login },
  { path: '/register', name: 'register', component: Register },
  {
    path: '/admin/dashboard',
    name: 'admin-dashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/user/dashboard',
    name: 'user-dashboard',
    component: UserDashboard,
    meta: { requiresAuth: true },
  },
  {
    path: '/payment/:resId/:parkingCost',
    name: 'payment',
    component: PaymentPortal,
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: '/admin/parking-lots/:lotId',
    name: 'admin-parking-lot-details',
    component: ParkingLotDetails,
    props: true,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  await authStore.initializeAuth()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next({ name: 'login' })
  }

  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    // Redirect non-admins trying to access admin routes
    return next({ name: 'user-dashboard' })
  }

  if ((to.name === 'login' || to.name === 'register') && authStore.isAuthenticated) {
    // Redirect logged-in users away from login/register
    return next(authStore.isAdmin ? { name: 'admin-dashboard' } : { name: 'user-dashboard' })
  }

  next()
})

export default router
