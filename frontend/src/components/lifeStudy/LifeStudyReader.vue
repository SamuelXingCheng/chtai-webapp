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
    <div class="sticky top-[30px] z-40 bg-inherit px-10 py-2 flex flex-wrap items-center justify-between gap-4">
      <!-- 標題 -->
      <h1 class="text-base sm:text-lg font-bold text-blue-700 whitespace-nowrap">
        {{ mergedTitle || '生命讀經載入中…' }}
      </h1>
      
    </div>

    <!-- ✅ 導覽列 -->
    <div class="sticky top-[80px] z-30 bg-beige py-3">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex flex-wrap justify-between items-center gap-4">
            <!-- 天數選單 -->
            <div class="overflow-x-auto text-sm whitespace-nowrap space-x-2">
                <span
                v-for="day in allDays"
                :key="day.day"
                class="inline-block px-2 py-1 border border-amber-700 text-amber-700 rounded-full bg-white hover:bg-amber-100 transition shadow-sm cursor-pointer"
                
                @click="scrollTo(day.day)"
                >
                第{{ day.day }}天
                </span>
            </div>

            <!-- 字體控制 + 沈浸閱讀 -->
            <div class="flex items-center gap-2 flex-wrap">
                <span class="text-sm text-gray-600">字體大小：</span>
                <button @click="decreaseFontSize" class="px-2 py-1 text-sm rounded border bg-white text-black hover:bg-gray-100 cursor-pointer">A-</button>
                <button @click="increaseFontSize" class="px-2 py-1 text-sm rounded border bg-white text-black hover:bg-gray-100 cursor-pointer">A+</button>
                <button @click="toggleFullscreen" class="px-3 py-1 text-sm rounded border bg-white text-black hover:bg-gray-100 cursor-pointer">沉浸閱讀</button>
            </div>
            </div>
        </div>
        </div>


    <!-- ✅ 內文區塊 -->
    <main
    class="w-full prose max-w-none space-y-6"
    
    >
    <section
    v-for="day in allDays"
    :key="day.day"
    :id="`day-${day.day}`"
    class="scroll-mt-[120px] border-b pb-1 rounded overflow-hidden bg-white shadow"
    >

    <h2
    class="text-lg font-semibold text-white bg-amber-700 px-3 py-2 rounded-md shadow inline-block mt-3 ml-3"
    >
    第{{ day.day }}天｜{{ day.label }}｜{{ day.verse }}
    </h2>

    <div class="px-2 py-0.5 space-y-1">
        <p
            v-for="(para, i) in getParagraphs(day.content)"
            :key="i"
            :class="[
            'leading-relaxed whitespace-pre-line rounded-md px-2 py-1.5 indent-8 text-justify mt-0.5',
            i % 2 === 1 ? 'bg-[#B3884E]/50' : '',
            ui.isReadingFullscreen ? 'text-[#eaeaea]' : 'text-black'
            ]"
            :style="{ fontSize: fontSize + 'px' }"
        >
            {{ para }}
        </p>
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

function getParagraphs(content: string): string[] {
  return content
    .split('\n')
    .map(p => p.trim())
    .filter(p => p.length > 0)
}

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
