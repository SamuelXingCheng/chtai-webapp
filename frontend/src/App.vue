<template>
  <!-- 根據提醒條顯示與否調整 padding-top -->
  <div :class="[shouldShowReminder ? 'pt-[96px]' : 'pt-[48px]', 'bg-beige min-h-screen text-gray-800']">
    <TopBar v-model="shouldShowReminder" />
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import TopBar from './components/TopBar.vue'

const shouldShowReminder = ref(true)
</script>
