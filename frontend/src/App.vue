<!-- src/App.vue -->
<template>
  <div
    :class="[
      ui.isReadingFullscreen ? 'pt-0 bg-[#262626] text-[#eaeaea]' : (ui.shouldShowReminder ? 'pt-[96px]' : 'pt-[48px] bg-beige text-gray-800'),
      'min-h-screen'
    ]"
  >
    <!-- ✅ 只有在非沈浸模式下才顯示 TopBar -->
    <TopBar
      v-if="!ui.isReadingFullscreen"
      v-model="ui.shouldShowReminderRaw"
      @menu-open="handleMenuOpen"
    />
    <router-view />
  </div>
</template>

<script setup lang="ts">
import TopBar from './components/TopBar.vue'
import { useUIStore } from './stores/ui'

const ui = useUIStore()

function handleMenuOpen(open: boolean) {
  if (open) {
    ui.toggleReminder(false)
  } else {
    ui.toggleReminder(true)
  }
}
</script>