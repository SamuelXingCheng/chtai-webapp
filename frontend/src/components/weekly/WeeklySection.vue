<!-- components/weekly/WeeklySection.vue -->
<template>
  <section class="space-y-4">
    <!-- 標題 -->
    <h2
      v-if="section.title"
      class="text-xl font-semibold text-amber-800 dark:text-[#C19960] border-b pb-1"
    >
      {{ section.title }}
    </h2>

    <!-- 一般段落：逐行切段並交錯底色 -->
    <div v-if="section.type === 'text'" class="space-y-2">
      <p
        v-for="(para, i) in paragraphs"
        :key="i"
        :class="[
          'leading-relaxed whitespace-pre-line rounded-md px-3 py-2',
          i % 2 === 1 ? 'bg-[#B3884E]/50' : ''
        ]"
      >
        {{ para }}
      </p>
    </div>

    <!-- 多圖區塊 -->
    <div v-if="section.type === 'image'" class="space-y-2">
      <p class="leading-relaxed whitespace-pre-line">
        {{ section.content }}
      </p>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <img
          v-for="(src, index) in section.images"
          :key="index"
          :src="src"
          class="rounded-lg shadow w-full"
          loading="lazy"
        />
      </div>
    </div>

    <!-- 禱告事項 -->
    <ul
      v-if="section.type === 'prayer'"
      class="list-disc pl-6 space-y-1 leading-relaxed"
    >
      <li v-for="(item, index) in section.items" :key="index">
        {{ item }}
      </li>
    </ul>

    <!-- 多層次報告事項 -->
    <div v-if="section.type === 'report'" class="space-y-1">
      <p
        v-for="(line, index) in section.lines"
        :key="index"
        :class="getReportLineClass(line)"
        class="whitespace-pre-line"
      >
        {{ line }}
      </p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  section: {
    type: string
    title?: string
    content?: string
    images?: string[]
    items?: string[]
    lines?: string[]
  }
}>()

// 分段 content 用於 text 類型
const paragraphs = computed(() => {
  if (props.section.type !== 'text' || !props.section.content) return []
  return props.section.content
    .split('\n')
    .map(p => p.trim())
    .filter(p => p.length > 0)
})

function getReportLineClass(line: string) {
  if (/^\(\d+\)/.test(line)) return 'ml-8 text-sm text-gray-700'
  if (/^\d+\./.test(line)) return 'ml-4 text-base'
  if (/^[一二三四五六七八九十]/.test(line)) return 'mt-4 font-semibold text-base'
  return 'text-base'
}
</script>
