<!-- components/weekly/WeeklyAnchorNav.vue -->
<template>
  <div class="hidden xl:block">
    <aside class="fixed top-[120px] right-6 w-[200px] space-y-3 text-sm text-gray-800">
    <div v-for="(item, index) in navItems" :key="index">
        <div
          v-if="item.type === 'title'"
          @click="scrollToCategory(item.key)"
          :class="[
            'text-6xs font-bold mt-4 mb-1 cursor-pointer hover:text-amber-500',
            immersive ? 'text-[#C19960]' : 'text-amber-700'
          ]"
        >
          {{ item.label }}
        </div>
        <div
          v-else-if="item.type === 'link'"
          @click="scrollToSection(item.target)"
          :class="[
            'cursor-pointer hover:text-amber-400 mb-1',
            immersive ? 'text-white/90' : 'text-gray-800'
          ]"
        >
          {{ item.label }}
        </div>
    </div>
    </aside>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps<{ 
  sections: { title: string }[] 
  immersive?: boolean
}>()

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
const categories = [
  { key: 'truth', label: '真理材料' },
  { key: 'report', label: '報導見證' },
  { key: 'announcement', label: '報告與代禱' }
]

const navItems = computed(() => {
  return categories.flatMap(cat => {
    const matchedSections = props.sections
      .map((section, i) => ({ ...section, index: i }))
      .filter(section => section.category === cat.key)

    return [
      { type: 'title', label: cat.label, key: cat.key },
      ...matchedSections.map(section => ({
        type: 'link',
        label: section.title,
        target: section.index
      }))
    ]
  })
})

function scrollToCategory(categoryKey: string) {
  const el = document.querySelector(`[id^="category-anchor-${categoryKey}-"]`)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' })
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
