<!-- components/lifeStudy/LifeStudyReader.vue -->
<template>
  <div
    :class="[
      immersive
        ? 'fixed inset-0 z-50 bg-[#262626] text-[#eaeaea] overflow-y-auto px-6 py-10'
        : 'max-w-7xl mx-auto bg-beige px-4 sm:px-6 lg:px-8 py-8 ',
      'space-y-6 transition-all duration-300'
    ]"
  >
    <!-- ✅ 上方標題列與功能列 -->
    <div class="sticky top-[48px] z-40 bg-inherit border-b px-4 py-2 flex flex-wrap items-center justify-between gap-4">
      <!-- 標題 -->
      <h1 class="text-base sm:text-lg font-bold text-blue-700 whitespace-nowrap">
        {{ mergedTitle || '生命讀經載入中…' }}
      </h1>
      <!-- 字體控制 + 沈浸閱讀 -->
      <div class="flex items-center gap-2 flex-wrap">
        <span class="text-sm text-gray-600">字體大小：</span>
        <button @click="decreaseFontSize" class="px-2 py-1 text-sm rounded border bg-white text-black hover:bg-gray-100">A-</button>
        <button @click="increaseFontSize" class="px-2 py-1 text-sm rounded border bg-white text-black hover:bg-gray-100">A+</button>
        <button @click="toggleFullscreen" class="px-3 py-1 text-sm rounded border bg-white text-black hover:bg-gray-100">沉浸閱讀</button>
      </div>
    </div>

    <!-- ✅ 導覽列 -->
    <div class="sticky top-[96px] z-30 bg-inherit border-b">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 overflow-x-auto text-sm text-amber-700 whitespace-nowrap">
        <span
        v-for="day in allDays"
        :key="day.day"
        class="mr-4 cursor-pointer hover:underline"
        @click="scrollTo(day.day)"
        >
        第{{ day.day }}天
        </span>
    </div>
    </div>

    <!-- ✅ 內文區塊 -->
    <main
    class="w-full prose max-w-none space-y-6"
    :style="{ fontSize: fontSize + 'px' }"
    >
    <section
    v-for="day in allDays"
    :key="day.day"
    :id="`day-${day.day}`"
    class="border-b pb-6 rounded overflow-hidden bg-white shadow"
    >
    <h2
    class="text-lg font-semibold text-white bg-amber-700 px-3 py-2 rounded-md shadow inline-block mt-3 ml-1"
    >
    第{{ day.day }}天｜{{ day.label }}｜{{ day.verse }}
    </h2>

    <div class="p-4 space-y-3">
        <div
        class="text-black whitespace-pre-line leading-relaxed"
        v-if="!ui.isReadingFullscreen"
        >
        {{ day.content }}
        </div>
        <div
        class="text-[#eaeaea] whitespace-pre-line leading-relaxed"
        v-else
        >
        {{ day.content }}
        </div>
    </div>
    </section>
    </main>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUIStore } from '../../stores/ui'
const ui = useUIStore()

const fontSize = ref(18)
const mergedTitle = ref('')
const data1 = ref<any>(null)
const data2 = ref<any>(null)
const allDays = ref<any[]>([])

onMounted(async () => {
  try {
    const [res1, res2] = await Promise.all([
      fetch('/newsite/data/life-study/ls_eph_005.json'),
      fetch('/newsite/data/life-study/ls_eph_006.json')
    ])
    if (!res1.ok || !res2.ok) {
      console.error('⚠️ 無法載入生命讀經 JSON:', res1.status, res2.status)
      return
    }
    data1.value = await res1.json()
    data2.value = await res2.json()
    mergedTitle.value = `${data1.value.title} ＋ ${data2.value.title}`
    allDays.value = [...data1.value.days, ...data2.value.days]
  } catch (err) {
    console.error('讀取生命讀經資料失敗:', err)
  }
})

function increaseFontSize() {
  fontSize.value = Math.min(fontSize.value + 4, 32)
}
function decreaseFontSize() {
  fontSize.value = Math.max(fontSize.value - 4, 12)
}
function toggleFullscreen() {
  ui.isReadingFullscreen = !ui.isReadingFullscreen
}
function scrollTo(day: number) {
  const el = document.getElementById(`day-${day}`)
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}
</script>
