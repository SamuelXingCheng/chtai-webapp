<!-- components/WeeklyReader.vue -->
<template>
  <div class="max-w-7xl mx-auto px-4 py-8 space-y-6">
    <h1 class="text-2xl font-bold text-gray-800">週訊閱讀 Demo</h1>

    <!-- 週訊選單 -->
    <div class="flex flex-wrap gap-3">
      <button
        v-for="msg in weeklyMessages"
        :key="msg.id"
        @click="selectMessage(msg)"
        :class="[
          'px-4 py-2 rounded border',
          selectedMessage?.id === msg.id
            ? 'bg-blue-600 text-white'
            : 'bg-white text-gray-700 hover:bg-gray-100'
        ]"
      >
        {{ msg.title }}
      </button>
    </div>

    <!-- 主內容區：右欄為搜尋 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <!-- 📖 HTML 內文（主體） -->
      <div class="md:col-span-3">
        <h2 class="text-lg font-semibold mb-2">📰 HTML 內文</h2>
        <div
          class="prose max-w-none border p-4 bg-white rounded shadow overflow-y-auto h-[500px]"
          v-html="selectedMessage?.htmlContent"
        ></div>
      </div>

      <!-- 🔍 搜尋 + 週訊選擇（工具列） -->
      <div class="md:col-span-1">
        <h2 class="text-lg font-semibold mb-2">🔍 搜尋週訊</h2>
        <SearchWeekSelector
          :messages="weeklyMessages"
          @select="selectMessage"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { weeklyMessages } from '../mock/weeklyMessages'
import SearchWeekSelector from './SearchWeekSelector.vue'

const selectedMessage = ref(weeklyMessages[0])
const searchQuery = ref('')

function selectMessage(msg: any) {
  selectedMessage.value = msg
}
</script>

<style scoped>
.prose h2 {
  @apply text-xl font-bold;
}
.prose ul {
  @apply list-disc pl-5;
}
</style>
