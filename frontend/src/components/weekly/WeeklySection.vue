<!-- components/weekly/WeeklySection.vue -->
<template>
  <!-- ✅ 加上 id 屬性供 ScrollSpy 使用 -->
  <section :id="`section-${index}`" class="space-y-4 scroll-mt-[120px]">
    <!-- ✅ 額外設立錨點（為 scroll 對齊用） -->
    <div
      :id="`category-anchor-${section.category}-${index}`"
      class="h-[1px] scroll-mt-[120px]"
    />

    <!-- 🚫 原本這個有 id 的分類標籤移除 id -->
    <div
      class="inline-block rounded px-2 py-1 text-xs font-bold text-white bg-amber-700"
    >
      {{ categoryLabel }}
    </div>

    <!-- 標題 -->
    <h2
      v-if="section.title"
      class="text-4xl font-semibold text-amber-800 dark:text-[#C19960] border-b pb-1"
    >
      {{ section.title }}
    </h2>
    <p
      v-if="section.subtitle"
      class="text-lg text-gray-600 dark:text-gray-400"
    >
      {{ section.subtitle }}
    </p>

    <!-- 一般段落 -->
    <div v-if="section.type === 'text'" class="space-y-2">

      <!-- ✅ 特殊：家聚會牧養材料，含 subsections -->
      <div v-if="section.sections" class="space-y-6">
        <div v-for="(sub, i) in section.sections" :key="i" class="space-y-2">
          <h3 v-if="sub.heading" class="text-xl font-semibold text-amber-700">
            {{ sub.heading }}
          </h3>

          <!-- 段落：只對非空行加 li -->
          <ul class="list-disc pl-6 space-y-1">
            <li
              v-for="(line, j) in sub.paragraphs.flatMap(p => p.split('\n')).filter(l => l.trim() !== '')"
              :key="j"
              class="leading-relaxed text-justify"
            >
              {{ line }}
            </li>
          </ul>
        </div>
      </div>


      <!-- ✅ 特殊：本週晨興進度申言主題 -->
      <ul
        v-else-if="section.title?.includes('本週晨興進度申言主題')"
        class="list-none pl-0 space-y-2"
      >
        <li
          v-for="(para, i) in paragraphs"
          :key="i"
          class="leading-relaxed text-justify"
        >
          {{ para }}
        </li>
      </ul>

      <!-- 其他一般 text -->
      <template v-else>
        <p
          v-for="(para, i) in paragraphs"
          :key="i"
          :class="['leading-relaxed whitespace-pre-line rounded-md px-3 py-2 text-justify',
            section.title?.includes('家聚會牧養材料') ? '' : (i % 2 === 1 ? 'bg-[#B3884E]/30' : '')
          ]"
        >
          {{ para }}
        </p>
      </template>
    </div>






    <!-- 多圖區塊 -->
    <div v-if="section.type === 'image'" class="space-y-2">
      <p
        v-for="(para, i) in imageParagraphs"
        :key="i"
        :class="[
          'leading-relaxed whitespace-pre-line rounded-md px-3 py-2',
          i % 2 === 1 ? 'bg-[#B3884E]/50' : ''
        ]"
      >
        {{ para }}
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
      <li
        v-for="(item, i) in section.items"
        :key="i"
        :class="[
          'leading-relaxed whitespace-pre-line rounded-md px-3 py-2',
          i % 2 === 1 ? 'bg-[#B3884E]/50' : ''
        ]"
      >
        {{ item }}
      </li>
    </ul>

    <!-- 多層次報告事項 -->
    <div v-if="section.type === 'report'" class="space-y-1">
      <p
        v-for="(line, i) in reportLines"
        :key="i"
        :class="[
          getReportLineClass(line),
          'whitespace-pre-line rounded-md px-3 py-2',
          i % 2 === 1 ? 'bg-[#B3884E]/50' : ''
        ]"
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
    category?: string
  },
  index: number
}>()

const paragraphs = computed(() => {
  if (props.section.type !== 'text' || !props.section.content) return []
  return props.section.content
    .split('\n')
    .map(p => p.trim())
    .filter(p => p.length > 0)
})

const imageParagraphs = computed(() => {
  if (props.section.type !== 'image' || !props.section.content) return []
  return props.section.content
    .split('\n')
    .map(p => p.trim())
    .filter(p => p.length > 0)
})

const reportLines = computed(() => {
  if (props.section.type !== 'report' || !props.section.content) return []
  const raw = props.section.content
  const withBreaks = raw
    .replace(/([^\n]|^)([一二三四五六七八九十])、/g, '\n$2、')
    .replace(/([^\n]|^)([０-９\d]{1,2})、/g, '\n$2、')
    .replace(/([^\n]|^)[①-⑩]/g, '\n$&')
  return withBreaks
    .split('\n')
    .map(line => line.trim())
    .filter(line => line.length > 0)
})

const categoryMap: Record<string, string> = {
  truth: '真理材料',
  report: '報導見證',
  announcement: '報告與代禱'
}

const categoryKey = computed(() => props.section.category || '')

const categoryLabel = computed(() => categoryMap[categoryKey.value] || '')

function getReportLineClass(line: string) {
  if (/^\(\d+\)/.test(line)) return 'ml-8'
  if (/^\d+\./.test(line)) return 'ml-4'
  if (/^[一二三四五六七八九十]/.test(line)) return 'mt-4 font-semibold'
  return ''
}
</script>
