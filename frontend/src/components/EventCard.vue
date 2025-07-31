<!-- components/EventCard.vue -->
<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

const props = defineProps<{
  event: {
    id: string
    title: string
    date: string
    count: number
    registerUrl: string
    responseUrl: string
    canView: boolean
    link: string
  }
}>()

const emit = defineEmits(['share', 'view'])
</script>

<template>
  <div class="bg-gray-50 border border-gray-200 rounded-lg p-4 shadow-sm">
    <!-- 活動標題 -->
    <p class="text-base font-semibold text-gray-800">{{ event.title }}</p>

    <!-- 日期 + 前往報名 -->
    <div class="flex justify-between items-center text-sm text-gray-500 mb-1">
      <p>{{ event.date }}</p>
      <router-link
        :to="`/register-form?id=${event.id}`"
        class="inline-flex w-[90px] justify-center items-center gap-1 bg-emerald-500 hover:bg-emerald-600 text-white px-3 py-1.5 rounded-md text-xs md:text-sm shadow transition"
      >
        <!-- 前往報名 → -->
        前往報名
      </router-link>
    </div>

    <!-- 已報名 + 邀請報名 -->
    <div class="flex justify-between items-center text-sm text-gray-500">
      <!-- <p>
        已報名：
        <span class="text-emerald-600 font-bold">{{ event.count }}</span> 位
      </p> -->
      <p class="text-gray-400 italic">報名統計即將開放</p>
      <button
        @click="emit('view', event)"
        class="inline-flex w-[90px] justify-center items-center gap-1 bg-blue-100 hover:bg-blue-200 text-blue-800 px-3 py-1.5 rounded-md text-xs md:text-sm shadow-sm transition"
      >
        誰有報名
        <!-- <svg xmlns="http://www.w3.org/2000/svg" class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
            <path d="M13 7a3 3 0 11-6 0 3 3 0 016 0zM3 14a4 4 0 018 0H3zM16 14a4 4 0 00-3-3.87 5.97 5.97 0 00-.47-.13 6.03 6.03 0 00-.45-.1A4.01 4.01 0 0116 14z" />
        </svg> -->
      </button>
    </div>
  </div>
</template>
