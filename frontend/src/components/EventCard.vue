<!-- components/EventCard.vue -->
<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

const props = defineProps<{
  event: {
    title: string
    date: string
    count: number
    link: string
  }
}>()

const emit = defineEmits(['share'])
</script>

<template>
  <div class="bg-gray-50 border border-gray-200 rounded-lg p-4 shadow-sm">
    <!-- 活動標題 -->
    <p class="text-base font-semibold text-gray-800">{{ event.title }}</p>

    <!-- 日期 + 前往報名 -->
    <div class="flex justify-between items-center text-sm text-gray-500 mb-1">
      <p>{{ event.date }}</p>
      <a
        :href="event.link"
        class="inline-flex items-center gap-1 bg-emerald-500 hover:bg-emerald-600 text-white px-3 py-1.5 rounded-md text-xs md:text-sm shadow transition"
      >
        前往報名 →
      </a>
    </div>

    <!-- 已報名 + 邀請報名 -->
    <div class="flex justify-between items-center text-sm text-gray-500">
      <p>
        已報名：
        <span class="text-emerald-600 font-bold">{{ event.count }}</span> 位
      </p>
      <button
        @click="emit('share', event)"
        class="inline-flex items-center gap-1 bg-blue-100 hover:bg-blue-200 text-blue-800 px-3 py-1.5 rounded-md text-xs md:text-sm shadow-sm transition"
      >
        邀請報名
        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path d="M12.293 2.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414L13.707 12H11v-2.707l5.293-5.293-4-4z" />
          <path d="M3 5a2 2 0 012-2h5a1 1 0 110 2H5v10h10v-5a1 1 0 112 0v5a2 2 0 01-2 2H5a2 2 0 01-2-2V5z" />
        </svg>
      </button>
    </div>
  </div>
</template>
