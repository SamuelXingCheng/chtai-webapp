<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <div id="app">
    <!-- Tailwind 測試 -->
    <h1 class="text-3xl font-bold underline text-blue-500 text-center my-4">
      Tailwind 已套用成功！
    </h1>

    <!-- Router 畫面 -->
    <RouterView />
  </div>
</template>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
