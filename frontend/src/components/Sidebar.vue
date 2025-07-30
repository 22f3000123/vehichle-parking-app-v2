<template>
  <div class="sidebar" :class="{ open: isOpen }">
    <div class="sidebar-toggle" @click="toggleSidebar">
      <v-icon name="fa-bars" fill="#fff"  />
    </div>
    <div class="sidebar-header">
      <router-link to="/" class="sidebar-brand">
        <v-icon name="fa-parking" class="me-2" /> ParkSmart
      </router-link>
    </div>
    <ul class="sidebar-nav">
      <li class="nav-item" v-if="!authStore.isAuthenticated">
        <router-link to="/login" class="nav-link">
          <v-icon name="fa-sign-in-alt" class="me-2" /> Login
        </router-link>
      </li>
      <li class="nav-item" v-if="!authStore.isAuthenticated">
        <router-link to="/register" class="nav-link">
          <v-icon name="fa-user-plus" class="me-2" /> Register
        </router-link>
      </li>
      <li class="nav-item" v-if="authStore.isAdmin">
        <router-link to="/admin/dashboard" class="nav-link">
          <v-icon name="fa-tools" class="me-2" /> Admin Dashboard
        </router-link>
      </li>
      <li class="nav-item" v-else-if="authStore.isAuthenticated">
        <router-link to="/user/dashboard" class="nav-link">
          <v-icon name="fa-tachometer-alt" class="me-2" /> Dashboard
        </router-link>
      </li>
      <li class="nav-item" v-if="authStore.isAuthenticated">
        <a href="#" @click.prevent="logout" class="nav-link">
          <v-icon name="fa-sign-out-alt" class="me-2" /> Logout
        </a>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import apiClient from '../services/api'

const authStore = useAuthStore()
const router = useRouter()
const isOpen = ref(true) 

const emit = defineEmits(['update:isOpen'])

const toggleSidebar = () => {
  isOpen.value = !isOpen.value
  emit('update:isOpen', isOpen.value)
}

const logout = async () => {
  try {
    await apiClient.post('/logout')
  } catch (error) {
    console.error('Logout failed on server:', error)
  } finally {
    authStore.logout()
    router.push('/login')
  }
}
</script>

<style scoped>
.sidebar {
  --sidebar-width: 250px;
  width: var(--sidebar-width);
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 0;
  transition:
    transform 0.4s ease,
    box-shadow 0.4s ease;
  transform: translateX(-100%);
  position: fixed;
  height: 100%;
  z-index: 1000;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.2);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar.open {
  transform: translateX(0);
}

/* Sidebar Toggle Button */
.sidebar-toggle {
  position: absolute;
  top: 1.5rem;
  right: -3rem;
  background-color: #764ba2;
  color: white;
  padding: 0.75rem 0.85rem;
  border-radius: 0 8px 8px 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
  transition:
    background-color 0.3s ease,
    transform 0.2s ease;
}

.sidebar-toggle:hover {
  background-color: #667eea;
}

/* Sidebar Header */
.sidebar-header {
  padding: 1rem 1.5rem;
  margin-bottom: 2.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 1.5rem;
}

.sidebar-brand {
  font-size: 1.8rem;
  font-weight: 700;
  color: white;
  text-decoration: none;
  display: flex;
  align-items: center;
  letter-spacing: 0.5px;
}

.sidebar-brand .v-icon {
  font-size: 1.8rem;
  margin-right: 0.75rem;
}

/* Sidebar Navigation */
.sidebar-nav {
  list-style: none;
  padding: 0 1rem;
  margin: 0;
}

.nav-item {
  margin-bottom: 0.75rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  display: flex;
  align-items: center;
  padding: 0.9rem 1.2rem;
  border-radius: 10px;
  transition:
    background-color 0.3s ease,
    transform 0.2s ease,
    box-shadow 0.3s ease;
  font-weight: 500;
  position: relative;
  overflow: hidden;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.nav-link .v-icon {
  margin-right: 0.8rem;
  font-size: 1.1rem;
}

.router-link-exact-active {
  background: rgba(255, 255, 255, 0.25);
  font-weight: 600;
  box-shadow: inset 3px 0 0 #fff;
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
    box-shadow: none;
  }

  .sidebar.open {
    transform: translateX(0);
  }
}
</style>
