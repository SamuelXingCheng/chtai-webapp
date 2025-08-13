<!-- components/weekly/WeeklyReader.vue -->
<template>
  <div
    :class="[
      immersive
        ? 'fixed inset-0 z-50 bg-[#262626] text-[#eaeaea] overflow-y-auto px-6 py-10'
        : 'max-w-7xl mx-auto bg-beige px-4 sm:px-6 lg:px-8 py-8',
      'space-y-6 transition-all duration-300'
    ]"
  >
    <!-- 標題區塊：沉浸模式時隱藏 -->
    <div v-if="!immersive" class="space-y-1">
      <h1 class="text-3xl font-bold text-gray-800">台中市召會週訊</h1>
      <div v-if="weeklyData.title" class="text-3xl text-blue-600 font-semibold">
        {{ weeklyData.title }}
      </div>
    </div>

    <div
      class="sticky top-[75px] z-30 bg-beige"
      v-if="!immersive"
    >
        <div class="w-full py-2 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">

        <!-- 右側：字體大小控制 + 沉浸閱讀 -->
        <div class="flex items-center gap-4">
          <!-- 字體大小控制 -->
          <div class="flex items-center gap-2">
            <span class="text-sm text-gray-600">字體大小：</span>
            <button
              @click="decreaseFontSize"
              class="px-2 py-1 text-sm rounded border bg-white text-black hover:bg-gray-100"
            >
              A-
            </button>
            <button
              @click="increaseFontSize"
              class="px-2 py-1 text-sm rounded border bg-white text-black hover:bg-gray-100"
            >
              A+
            </button>
          </div>

          <!-- 沉浸閱讀按鈕 -->
          <button
            @click="immersive = !immersive"
            class="px-3 py-1 text-sm rounded border bg-white text-black hover:bg-gray-100"
          >
            沉浸閱讀
          </button>
        </div>
      </div>
    </div>


    <!-- 沉浸模式時：只顯示字體控制與切換按鈕 -->
    <div class="px-4 sm:px-6 lg:px-8 flex gap-2 items-center" v-else>
      <span class="text-sm text-[#ccc]">字體大小：</span>
      <button
        @click="decreaseFontSize"
        class="px-2 py-1 text-sm rounded border bg-[#444] text-[#eee]"
      >
        A-
      </button>
      <button
        @click="increaseFontSize"
        class="px-2 py-1 text-sm rounded border bg-[#444] text-[#eee]"
      >
        A+
      </button>
      <button
        @click="immersive = !immersive"
        class="ml-auto px-3 py-1 text-sm rounded border bg-[#444] text-[#eee]"
      >
        返回一般模式
      </button>
    </div>


    <!-- 搜尋功能區塊：沉浸模式時隱藏 -->
    <div v-if="!immersive" class="w-full">
      <SearchWeekSelector
        :messages="weeklyMessages"
        @select="selectMessage"
      />
    </div>

    <!-- JSON 週訊內容區塊，包含快速跳轉導覽 -->
    <div class="relative">
      <WeeklyAnchorNav v-if="!immersive" :sections="weeklyData.sections" :immersive="false" />

      <div
        class="prose max-w-none rounded-xl p-6 transition-all duration-300"
        :class="[
          immersive
            ? 'bg-transparent border-none shadow-none prose-invert'
            : 'bg-white border shadow text-gray-900',
          fontSizeClass
        ]"
        v-if="weeklyData.sections.length"
      >
        <WeeklySection
          v-for="(section, index) in weeklyData.sections"
          :key="index"
          :section="section"
          :index="index"
        />
      </div>
    </div>
    <MobileFloatingTOC :sections="weeklyData.sections" />

  </div>
  <!-- ✅ 沉浸模式下浮動導覽按鈕 -->
  <button
    v-if="immersive"
    class="fixed bottom-6 right-6 z-50 flex items-center gap-2 bg-[#C19960] text-white px-4 py-2 rounded-lg shadow-lg hover:bg-[#ddb574] transition"
    @click="showSidebar = true"
    title="打開導覽"
  >
    <!-- 導覽 Icon（漢堡條） -->
    <svg class="w-5 h-5" fill="none" stroke="white" stroke-width="2" viewBox="0 0 24 24">
    <path d="M4 6h16M4 12h16M4 18h16" />
  </svg>
    <span class="font-semibold text-sm">導覽</span>
  </button>


  <!-- ✅ 側邊導覽欄（Teleport 到 body） -->
  <Teleport to="body">
    <transition name="slide">
      <aside
        v-if="immersive && showSidebar"
        class="fixed top-0 right-0 w-[280px] h-full bg-[#1e1e1e] text-white z-50 p-4 shadow-xl overflow-y-auto"
      >
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-semibold">快速導覽</h2>
          <button @click="showSidebar = false" class="text-white text-2xl font-bold hover:text-gray-300">
            ✕
          </button>
        </div>
        <!-- 🔗 導覽內容 -->
        <WeeklyAnchorNav :sections="weeklyData.sections" :immersive="true" />
      </aside>
    </transition>
  </Teleport>

</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUIStore } from '../../stores/ui'
import SearchWeekSelector from './SearchWeekSelector.vue'
import WeeklySection from './WeeklySection.vue'
import { weeklyMessages } from '../../mock/weeklyMessages'
import WeeklyAnchorNav from '../weekly/WeeklyAnchorNav.vue'
import MobileFloatingTOC from '../weekly/MobileFloatingTOC.vue'

const ui = useUIStore()
const fontSize = ref(18)

const immersive = computed({
  get: () => ui.isReadingFullscreen,
  set: (val) => (ui.isReadingFullscreen = val)
})

const showSidebar = ref(false)

function increaseFontSize() {
  fontSize.value = Math.min(fontSize.value + 4, 32)
}
function decreaseFontSize() {
  fontSize.value = Math.max(fontSize.value - 4, 12)
}

const fontSizeClass = computed(() => {
  if (fontSize.value <= 10) return 'prose-xs'
  if (fontSize.value <= 14) return 'prose-sm'
  if (fontSize.value <= 18) return 'prose-base'
  if (fontSize.value <= 22) return 'prose-lg'
  if (fontSize.value <= 26) return 'prose-xl'
  if (fontSize.value <= 30) return 'prose-2xl'
  return 'prose-3xl'
})

// 資料格式
interface Section {
  type: string
  title?: string
  content?: string
  images?: string[]
  items?: string[]
  lines?: string[]
}
interface WeeklyData {
  id: string
  title: string
  sections: Section[]
}

const weeklyData = ref<WeeklyData>({
  id: '',
  title: '',
  sections: []
})

onMounted(async () => {
  try {
    const res = await fetch('/newsite/data/weekly/2025-08-03.json')
    if (!res.ok) {
      console.error('⚠️ 無法載入週訊 JSON：', res.status)
      return
    }

    const data = await res.json()
    weeklyData.value = data
  } catch (err) {
    console.error('❌ 載入週訊資料錯誤：', err)
  }
})

function selectMessage(msg: any) {
  // 可切換週訊版本（若未來支援）
  weeklyData.value = msg
}
</script>

<style scoped>
.prose {
  @apply font-sans text-primary font-normal;
  line-height: 1.75;
}
.prose h1, .prose h2, .prose h3 {
  @apply text-amber-800 dark:text-[#C19960];
}
.prose.prose-invert {
  color: #eaeaea;
}
.prose.prose-invert h1,
.prose.prose-invert h2,
.prose.prose-invert h3 {
  color: #C19960;
}
.prose.prose-invert a {
  color: #e6b86d;
  text-decoration: underline;
}
.prose.prose-invert strong {
  color: #f5f5f5;
}

/* 側邊欄滑出效果 */
.slide-enter-active, .slide-leave-active {
  transition: transform 0.3s ease;
}
.slide-enter-from, .slide-leave-to {
  transform: translateX(100%);
}

</style>
