<!-- src/views/BeliefsView.vue -->
<template>
  <section class="max-w-4xl mx-auto mt-10 px-4 space-y-10">

    <!-- 🔝 固定在上方的導覽列 -->
    <div class="sticky top-[80px] z-20 bg-white shadow rounded-lg p-4">
      <div class="grid grid-cols-3 gap-3">
        <button
          v-for="(section, i) in sections"
          :key="i"
          @click="scrollToSection(i)"
          class="px-3 py-1 text-sm bg-gray-100 rounded hover:bg-gray-200 transition w-full"
        >
          {{ section?.title }}
        </button>
      </div>
    </div>

    <!-- 內容區塊 -->
    <div
      v-for="(section, i) in sections"
      :key="i"
      :id="`belief-section-${i}`"
      class="bg-white rounded-xl shadow p-8"
    >
      <h1 class="text-2xl font-bold text-gray-800 pb-2 border-b border-gray-300">
        {{ section?.title }}
      </h1>

      <!-- 內文：自動解析 /n -->
      <div class="space-y-4 text-gray-700 leading-relaxed mt-6">
        <p
          v-for="(para, index) in formatParagraphs(section?.paragraphs)"
          :key="index"
          class="text-justify"
        >
          {{ para }}
        </p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface PageData {
  title: string
  paragraphs: string | string[]
}

const sections = ref<PageData[]>([])

onMounted(async () => {
  const files = ['beliefs.json', 'who-we-are.json', 'history.json']
  const results: PageData[] = []

  for (const file of files) {
    const res = await fetch(`/data/about/${file}`)
    const data = await res.json()
    results.push(data)
  }

  sections.value = results
})

// 分段工具
function formatParagraphs(paragraphs: string | string[] | undefined) {
  if (!paragraphs) return []
  if (Array.isArray(paragraphs)) {
    return paragraphs.flatMap(p => p.split(/\n+/)).map(p => p.trim()).filter(Boolean)
  }
  return paragraphs.split(/\n+/).map(p => p.trim()).filter(Boolean)
}

// ✅ 滾動跳轉
function scrollToSection(i: number) {
  const el = document.getElementById(`belief-section-${i}`)
  if (el) {
    const yOffset = -120 // 導航列高度
    const y = el.getBoundingClientRect().top + window.scrollY + yOffset
    window.scrollTo({ top: y, behavior: 'smooth' })
  }
}
</script>
