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
  width: var(--sidebar-width);
  background-color: #2c3e50;
  color: white;
  padding: 1rem;
  transition: transform 0.3s ease;
  transform: translateX(-100%);
  position: fixed;
  height: 100%;
  z-index: 1000;
}

.sidebar.open {
  transform: translateX(0);
}

.sidebar-toggle {
  position: absolute;
  top: 1rem;
  right: -2rem;
  background-color: #2c3e50;
  color: white;
  padding: 0.5rem;
  border-radius: 0 5px 5px 0;
  cursor: pointer;
}

.sidebar-header {
  margin-bottom: 2rem;
}

.sidebar-brand {
  font-size: 1.5rem;
  font-weight: 600;
  color: white;
  text-decoration: none;
  display: flex;
  align-items: center;
}

.sidebar-nav {
  list-style: none;
  padding: 0;
}

.nav-link {
  color: white;
  text-decoration: none;
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.nav-link:hover {
  background-color: #34495e;
}
</style>
