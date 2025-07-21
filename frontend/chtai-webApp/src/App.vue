<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <div id="app">
    <!-- 可放 Navbar、Header 等固定項目 -->
    <RouterView />
    <!-- 可放 Footer -->
  </div>
</template>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
