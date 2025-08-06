<!-- components/MobileFloatingTOC.vue -->
<template>
  <div class="fixed bottom-6 right-6 z-40 md:hidden">
    <button
      @click="showMenu = !showMenu"
      class="bg-amber-600 text-white rounded-full p-3 shadow-lg"
    >
      ☰
    </button>

    <!-- 選單 -->
    <div
      v-if="showMenu"
      class="absolute bottom-16 right-0 bg-white rounded shadow-lg p-2 w-48 space-y-1"
    >
      <div
        v-for="(section, index) in sections"
        :key="index"
        @click="handleClick(index)"
        class="text-sm px-3 py-2 hover:bg-amber-100 cursor-pointer"
      >
        {{ section.title }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
const props = defineProps<{ sections: { title: string }[] }>()
const showMenu = ref(false)

function handleClick(index: number) {
  const el = document.getElementById(`section-${index}`)
  if (el) {
    const y = el.getBoundingClientRect().top + window.scrollY - 100
    window.scrollTo({ top: y, behavior: 'smooth' })
  }
  showMenu.value = false
}
</script>
