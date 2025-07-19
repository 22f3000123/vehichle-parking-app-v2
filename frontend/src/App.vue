<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <router-link to="/" class="navbar-brand">Parking App</router-link>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <!-- For Logged Out Users -->
            <template v-if="!authStore.isAuthenticated">
              <li class="nav-item">
                <router-link to="/login" class="nav-link">Login</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/register" class="nav-link">Register</router-link>
              </li>
            </template>
            <!-- For Logged In Users -->
            <template v-else>
              <li class="nav-item" v-if="authStore.isAdmin">
                <router-link to="/admin/dashboard" class="nav-link">Admin Dashboard</router-link>
              </li>
              <li class="nav-item" v-else>
                <router-link to="/user/dashboard" class="nav-link">Dashboard</router-link>
              </li>
              <li class="nav-item">
                <a href="#" @click.prevent="logout" class="nav-link">Logout</a>
              </li>
            </template>
          </ul>
        </div>
      </div>
    </nav>
    <div class="container mt-4">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useAuthStore } from './stores/auth';
import { useRouter } from 'vue-router';
import apiClient from './services/api';

const authStore = useAuthStore();
const router = useRouter();

onMounted(() => {
  authStore.initializeAuth();
});

const logout = async () => {
  try {
    await apiClient.post('/logout');
  } catch (error) {
    console.error('Logout failed on server:', error);
  } finally {
    authStore.logout();
    router.push('/login');
  }
};
</script>
