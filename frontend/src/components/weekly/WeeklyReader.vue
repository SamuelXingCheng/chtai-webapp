<!-- components/weekly/WeeklyReader.vue -->
<template>
  <div
    :class="[
      immersive
        ? 'fixed inset-0 z-50 bg-[#262626] text-[#eaeaea] overflow-y-auto px-6 py-10'
        : 'max-w-7xl mx-auto bg-beige px-4 sm:px-6 lg:px-8 py-8',
      'space-y-6 transition-all duration-300'
    ]"
  >
    <!-- 標題區塊：沉浸模式時隱藏 -->
    <div v-if="!immersive" class="space-y-1">
      <h1 class="text-3xl font-bold text-gray-800">週訊閱讀</h1>
      <div v-if="selectedMessage" class="text-blue-600 font-semibold">
        週訊：{{ selectedMessage.title }}
      </div>
    </div>

    <!-- 字體大小與沉浸切換按鈕 -->
    <div class="flex gap-2 items-center">
      <span
        class="text-sm"
        :class="immersive ? 'text-[#ccc]' : 'text-gray-600'"
      >
        字體大小：
      </span>
      <button
        @click="decreaseFontSize"
        class="px-2 py-1 text-sm rounded border"
        :class="immersive ? 'bg-[#444] text-[#eee]' : 'bg-white text-black hover:bg-gray-100'"
      >
        A-
      </button>
      <button
        @click="increaseFontSize"
        class="px-2 py-1 text-sm rounded border"
        :class="immersive ? 'bg-[#444] text-[#eee]' : 'bg-white text-black hover:bg-gray-100'"
      >
        A+
      </button>

      <!-- 沉浸閱讀模式切換 -->
      <button
        @click="immersive = !immersive"
        class="ml-auto px-3 py-1 text-sm rounded border"
        :class="immersive ? 'bg-[#444] text-[#eee]' : 'bg-white text-black hover:bg-gray-100'"
      >
        {{ immersive ? '返回一般模式' : '沉浸閱讀' }}
      </button>
    </div>

    <!-- 搜尋功能區塊：沉浸模式時隱藏 -->
    <div v-if="!immersive" class="w-full">
      <SearchWeekSelector
        :messages="weeklyMessages"
        @select="selectMessage"
      />
    </div>

    <!-- 週訊 HTML 內文 -->
    <section
      class="prose prose-lg max-w-none rounded-xl p-6 transition-all duration-300"
      :class="[
        immersive
          ? 'bg-transparent border-none shadow-none prose-invert'
          : 'bg-white border shadow text-gray-900',
      ]"
      :style="{ fontSize: fontSize + 'px' }"
      v-if="selectedMessage"
      v-html="selectedMessage.htmlContent"
    />
  </div>
</template>


<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { weeklyMessages } from '../../mock/weeklyMessages'
import SearchWeekSelector from './SearchWeekSelector.vue'
import { useUIStore } from '../../stores/ui'

const ui = useUIStore()

const selectedMessage = ref(weeklyMessages[0])
const fontSize = ref(18)

const immersive = computed({
  get: () => ui.isReadingFullscreen,
  set: (val) => (ui.isReadingFullscreen = val)
})

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

/* 白天模式標題 */
.prose h1, .prose h2, .prose h3 {
  @apply text-amber-800 dark:text-[#C19960]; /* 深色模式也用 C19960 金棕色 */
}

/* 暗色模式整體文字調整為較柔和的白灰 */
.prose.prose-invert {
  color: #eaeaea; /* RGB(234,234,234) */
}

/* 標題：金棕色 */
.prose.prose-invert h1,
.prose.prose-invert h2,
.prose.prose-invert h3 {
  color: #C19960; /* 替代原本的 yellow-300 */
}

/* 連結：琥珀色 hover 時更亮 */
.prose.prose-invert a {
  color: #e6b86d; /* 金黃色調 */
  text-decoration: underline;
}

/* 粗體：略帶米白 */
.prose.prose-invert strong {
  color: #f5f5f5;
}
</style>

