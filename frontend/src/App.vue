<template>
  <div id="app">
    <Sidebar v-if="!isLandingPage" @update:isOpen="isSidebarOpen = $event" />
    <div :class="{ 'main-content': true, 'sidebar-open': isSidebarOpen && !isLandingPage }">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import { useRoute } from 'vue-router';
import Sidebar from './components/Sidebar.vue';

const route = useRoute();
const isLandingPage = computed(() => route.name === 'landing');
const isSidebarOpen = ref(true);
</script>