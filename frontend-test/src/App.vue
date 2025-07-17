<template>
  <div>
    <a href="https://vite.dev" target="_blank">
      <img src="../src/assets/styles/images/logo_min.png" class="logo" alt="Student Manage" />
    </a>
  </div>
  <div id="app">
    <router-view />

    <Toast position="bottom-right" />
  </div>
</template>

<script setup>
import Toast from 'primevue/toast'; // Import Toast component
</script>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
</style>
