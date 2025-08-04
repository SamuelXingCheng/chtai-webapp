<!-- components/WeeklyReader.vue -->
<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
    <!-- 標題區塊 -->
    <div class="space-y-1">
      <h1 class="text-3xl font-bold text-gray-800">週訊閱讀</h1>
      <div v-if="selectedMessage" class="text-blue-600 font-semibold">
        週訊：{{ selectedMessage.title }}
      </div>
    </div>

    <!-- 字體大小調整按鈕 -->
    <div class="flex gap-2 items-center">
      <span class="text-sm text-gray-600">字體大小：</span>
      <button
        @click="decreaseFontSize"
        class="px-2 py-1 text-sm rounded border bg-white hover:bg-gray-100"
      >A-</button>
      <button
        @click="increaseFontSize"
        class="px-2 py-1 text-sm rounded border bg-white hover:bg-gray-100"
      >A+</button>
    </div>

    <!-- 搜尋功能 -->
    <div class="w-full">
      <SearchWeekSelector
        :messages="weeklyMessages"
        @select="selectMessage"
      />
    </div>

    <!-- 週訊 HTML 內文 -->
    <section
      class="prose prose-lg max-w-none bg-white border rounded-xl shadow p-6"
      v-if="selectedMessage"
      v-html="selectedMessage.htmlContent"
      :style="{ fontSize: fontSize + 'px' }">
    </section>
    
    
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { weeklyMessages } from '../mock/weeklyMessages'
import SearchWeekSelector from './SearchWeekSelector.vue'

const selectedMessage = ref(weeklyMessages[0])

const fontSize = ref(18)

function increaseFontSize() {
  fontSize.value = Math.min(fontSize.value + 2, 32)
}
function decreaseFontSize() {
  fontSize.value = Math.max(fontSize.value - 2, 12)
}

function selectMessage(msg: any) {
  selectedMessage.value = msg
}
</script>

<style scoped>
.prose {
  @apply font-sans text-primary font-normal;
  line-height: 1.75;
}
.prose h1, .prose h2, .prose h3 {
  @apply text-amber-800;
}
</style>
