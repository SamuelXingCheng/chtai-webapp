<!-- components/weekly/WeeklyAnchorNav.vue -->
<template>
  <div class="hidden xl:block">
    <!-- 頂端目前章節標題 -->
    <!-- <div
    v-if="currentTitle"
    class="fixed top-[64px] right-[180px] z-40 text-sm text-amber-700 font-semibold bg-white/80 dark:bg-[#262626]/80 px-3 py-2 rounded shadow"
    >
    {{ currentTitle }}
    </div> -->

    <!-- 側邊導覽清單 -->
    <div
      class="fixed right-6 top-[120px] w-52 z-30 transition-opacity duration-300"
      :class="{ 'opacity-0 pointer-events-none': isAtBottom }"
    >
      <ul class="space-y-2 text-sm">
        <li
          v-for="(section, index) in sections"
          :key="index"
          @click="scrollToSection(index)"
          class="cursor-pointer hover:text-amber-700 transition"
          :class="activeIndex === index ? 'text-amber-800 font-bold' : 'text-gray-500'"
        >
          {{ section.title }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'

const props = defineProps<{ sections: { title: string }[] }>()

const activeIndex = ref(0)
const isAtBottom = ref(false)
const currentTitle = ref('')

function scrollToSection(index: number) {
  const el = document.getElementById(`section-${index}`)
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

function handleScroll() {
  const buffer = 120 // 偏移距離，避免遮住標題
  const scrollY = window.scrollY
  const windowHeight = window.innerHeight
  const documentHeight = document.documentElement.scrollHeight

  // 若已到底部則隱藏導覽列
  isAtBottom.value = scrollY + windowHeight >= documentHeight - 100

  // 比對每段位置，更新 activeIndex
  for (let i = 0; i < props.sections.length; i++) {
    const el = document.getElementById(`section-${i}`)
    if (el) {
      const rect = el.getBoundingClientRect()
      const top = rect.top + scrollY - buffer
      const bottom = top + el.offsetHeight
      if (scrollY >= top && scrollY < bottom) {
        activeIndex.value = i
        currentTitle.value = props.sections[i].title
        break
      }
    }
  }
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  handleScroll()
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
ul::-webkit-scrollbar {
  width: 4px;
}
ul::-webkit-scrollbar-thumb {
  background-color: #ccc;
  border-radius: 4px;
}
</style>
