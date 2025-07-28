<template>
  <!-- 根據提醒條顯示與否調整 padding-top -->
  <div :class="[shouldShowReminder ? 'pt-[96px]' : 'pt-[48px]', 'bg-beige min-h-screen text-gray-800']">
    <TopBar v-model="shouldShowReminder" @menu-open="handleMenuOpen" />
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import TopBar from './components/TopBar.vue'

// 控制提醒條顯示（傳給 TopBar 的 v-model）
const shouldShowReminder = ref(true)

// 記錄「原始是否該提醒」，不會被選單開關影響
const shouldShowReminderRaw = ref(true)

// 每次 TopBar emit 的值都記下來
watch(shouldShowReminder, (val) => {
  shouldShowReminderRaw.value = val
})

// 處理選單打開/關閉
function handleMenuOpen(open: boolean) {
  if (open) {
    shouldShowReminder.value = false // 點開選單就隱藏提醒條
  } else {
    shouldShowReminder.value = shouldShowReminderRaw.value // 關掉時根據原始判斷是否恢復
  }
}
</script>

