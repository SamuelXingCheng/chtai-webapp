<!-- components/lifeStudy/LifeStudyReader.vue -->
<template>
  <div
    :class="[
      immersive
        ? 'fixed inset-0 z-50 bg-[#262626] text-[#eaeaea] overflow-y-auto px-6 py-10'
        : 'max-w-7xl mx-auto bg-beige px-4 sm:px-6 lg:px-8 py-8',
      'space-y-6 transition-all duration-300'
    ]"
  >
    <!-- ✅ 標題列 -->
    <div
      ref="titleRow"
      class="sticky z-40 bg-inherit px-6 py-2 flex flex-wrap items-center justify-between gap-4"
      :style="{ top: headerTopPx }"
    >
      <h1 :style="{ fontSize}" class="font-bold text-blue-700 whitespace-normal sm:whitespace-nowrap">
        {{ mergedTitle || '生命讀經載入中…' }}
      </h1>
    </div>

    <!-- ✅ 導覽列 -->
    <div
      ref="navRow"
      class="sticky z-30 bg-beige py-2 border-b"
      :style="{ top: navTopPx }"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-wrap justify-between items-center gap-3">
          <div class="overflow-x-auto text-sm whitespace-nowrap space-x-2">
            <span
              v-for="day in allDays"
              :key="day.day"
              class="inline-block px-2 py-1 border border-amber-700 text-amber-700 rounded-full bg-white hover:bg-amber-100 transition shadow-sm cursor-pointer"
              @click="scrollTo(day.day)"
            >第{{ day.day }}天</span>
          </div>

          <div class="flex items-center gap-2 flex-wrap">
            <span class="text-sm text-gray-600">字體大小：</span>
            <button @click="decreaseFontSize" class="px-2 py-1 text-sm rounded border bg-white hover:bg-gray-100 cursor-pointer">A-</button>
            <button @click="increaseFontSize" class="px-2 py-1 text-sm rounded border bg-white hover:bg-gray-100 cursor-pointer">A+</button>
            <button @click="toggleFullscreen" class="px-3 py-1 text-sm rounded border bg-white hover:bg-gray-100 cursor-pointer">沉浸閱讀</button>
          </div>
        </div>
      </div>
    </div>

    <!-- ✅ 內文區塊：提供 scrollPaddingTop 給原生錨點 -->
    <main
      class="w-full prose max-w-none space-y-6"
      :style="{ scrollPaddingTop: baseOffsetPx }"
    >
      <section
        v-for="(day, idx) in allDays"
        :key="day.day"
        :id="`day-${day.day}`"
        class="border-b pb-1 rounded overflow-hidden bg-white shadow"
        :style="{ scrollMarginTop: baseOffsetPx }"
      >
        <h2
          :ref="el => setH2Ref(idx, el)"
          class="text-lg font-semibold text-white bg-amber-700 px-3 py-2 rounded-md shadow inline-block mt-3 ml-3"
        >
          第{{ day.day }}天｜{{ day.label }}｜{{ day.verse }}
        </h2>

        <div class="px-5 py-0.5 space-y-1">
          <p
            v-for="(para, i) in day.display"
            :key="i"
            :class="[
              'leading-relaxed whitespace-pre-line rounded-md px-2 py-1.5 text-justify mt-0.5',
              para.isHeading ? 'font-semibold indent-0' : 'indent-8',
              (!para.isHeading && para.bodyIndex % 2 === 1) ? 'bg-[#B3884E]/50' : '',
              ui.isReadingFullscreen ? 'text-[#eaeaea]' : 'text-black'
            ]"
            :style="{ fontSize: fontSize + 'px' }"
          >
            {{ para.text }}
          </p>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed, nextTick, watch } from 'vue'
import { useUIStore } from '../../stores/ui'
const ui = useUIStore()

/* ---------------- 基本狀態 ---------------- */
const fontSize = ref(18)
const mergedTitle = ref('')
const allDays = ref<any[]>([])

/* ---------------- 吸頂列高度（動態量測） ---------------- */
const titleRow = ref<HTMLElement|null>(null)
const navRow   = ref<HTMLElement|null>(null)

const headerOffset = computed(() => (ui.shouldShowReminder ? 96 : 48)) // TopBar / 提醒條高度
const headerTopPx  = computed(() => `${headerOffset.value}px`)

const titleH = ref(0)
const navH   = ref(0)

const EPS = 1

/* ---------------- 量測後的自動校正工具 ---------------- */
// 等佈局穩定（確保 ResizeObserver / 版面已更新）
const afterLayout = () =>
  new Promise<void>(r => requestAnimationFrame(() => requestAnimationFrame(() => r())))

// 只要有 h2 正被 sticky 覆蓋（top 介於 0 與目標之間），就補償捲動把它完全藏起來
function adjustForOverlap() {
  let bestIdx = -1
  let bestDelta = 0
  h2Refs.value.forEach((h2, idx) => {
    if (!h2) return
    const h = h2Heights.value[idx] ?? defaultH2Height.value
    const stickyBottom = baseOffset.value
    const targetTop = baseOffset.value - h
    const top = h2.getBoundingClientRect().top

    // 原本：if (top > 0 && top < stickyBottom) { ... }
    // 放寬一點，滑動時更穩
    if (top > -EPS && top < stickyBottom + EPS) {
      const delta = top - targetTop
      if (bestIdx === -1 || Math.abs(delta) < Math.abs(bestDelta)) {
        bestIdx = idx
        bestDelta = delta
      }
    }
  })
  if (bestIdx !== -1 && Math.abs(bestDelta) > 0.5) {
    window.scrollBy({ top: bestDelta }) // 無動畫，避免晃動
  }
}


/* 監看 sticky 列高度變化：更新後立即校正 */
let headerRO: ResizeObserver | null = null
onMounted(() => {
  headerRO = new ResizeObserver(async () => {
    titleH.value = titleRow.value?.offsetHeight ?? 0
    navH.value   = navRow.value?.offsetHeight ?? 0
    await afterLayout()
    adjustForOverlap()
  })
  if (titleRow.value) headerRO.observe(titleRow.value)
  if (navRow.value)   headerRO.observe(navRow.value)
})
onBeforeUnmount(() => headerRO?.disconnect())

// 導覽列頂端：貼在標題列下
const navTopPx = computed(() => `${headerOffset.value + titleH.value}px`)

// 不含 h2 的基礎遮擋高度（TopBar + 標題列 + 導覽列 + 緩衝）
const baseOffset = computed(() => headerOffset.value + titleH.value + navH.value)
const baseOffsetPx = computed(() => `${baseOffset.value}px`)

/* ---------------- 每段 <h2> 的高度量測 ---------------- */
const h2Refs = ref<HTMLElement[]>([])
const h2Heights = ref<number[]>([])
const h2Observers: ResizeObserver[] = []

const setH2Ref = (idx: number, el: HTMLElement | null) => {
  if (!el) return
  h2Refs.value[idx] = el
  h2Heights.value[idx] = el.offsetHeight
  const obs = new ResizeObserver(async () => {
    h2Heights.value[idx] = el.offsetHeight
    await afterLayout()
    adjustForOverlap()
  })
  obs.observe(el)
  h2Observers.push(obs)
}
onBeforeUnmount(() => h2Observers.forEach(o => o.disconnect()))

// 還沒量到時的預設 h2 高度（用第一段或 40px 當 fallback）
const defaultH2Height = computed(() => h2Heights.value[0] ?? 40)

// （若要每段各自 scroll-margin-top，可用這個 helper）
// function getSectionScrollMt(idx: number) {
//   const h = h2Heights.value[idx] ?? defaultH2Height.value
//   return `${baseOffset.value + h}px`
// }

/* ---------------- 載入資料（你的原始邏輯） ---------------- */
onMounted(async () => {
  try {
    const [res1, res2] = await Promise.all([
      fetch('/newsite/data/life-study/life_eph_001.json'),
      fetch('/newsite/data/life-study/life_eph_002.json')
    ])
    if (!res1.ok || !res2.ok) {
      console.error('⚠️ 無法載入生命讀經 JSON:', res1.status, res2.status)
      return
    }
    const raw1 = await res1.json()
    const raw2 = await res2.json()
    const doc1 = normalizeDoc(raw1)
    const doc2 = normalizeDoc(raw2)
    mergedTitle.value = `${doc1.title} ＋ ${doc2.title}`
    allDays.value = [...doc1.days, ...doc2.days]
    await nextTick() // 等 DOM 出現，讓 ResizeObserver 開始量測
  } catch (err) {
    console.error('讀取生命讀經資料失敗:', err)
  }
})

function normalizeDoc(doc: any) {
  const days = Array.isArray(doc?.days) ? doc.days : []
  const normDays = days.map((d: any) => {
    const parasFromJson = Array.isArray(d.paragraphs) ? d.paragraphs : null
    let display: Array<{ text: string; isHeading: boolean; bodyIndex: number }> = []
    let bodyIndex = 0
    if (parasFromJson) {
      for (const p of parasFromJson) {
        if (!p || typeof p.text !== 'string') continue
        const isHeading = [1, 2, 3].includes(Number(p.level))
        const text = isHeading
          ? (p.level === 1 ? `${p.marker}、${p.text}`
            : p.level === 2 ? `• ${p.marker}、${p.text}`
            : `- ${p.marker}. ${p.text}`)
          : p.text
        display.push({ text, isHeading, bodyIndex: isHeading ? -1 : bodyIndex++ })
      }
    } else {
      const content = (d.text || d.content || d.contentRaw || '').toString()
      for (const line of content.split('\n').map(s => s.trim()).filter(Boolean)) {
        const isHeading = /^[壹貳參参肆伍陸柒捌玖拾一二三四五六七八九十\d]+[、．.]/.test(line)
        display.push({ text: line, isHeading, bodyIndex: isHeading ? -1 : bodyIndex++ })
      }
    }
    return {
      day: Number(d.day) || 0,
      label: d.label || '',
      verse: d.verse || '',
      content: (d.text?.trim?.() || d.content?.trim?.() || d.contentRaw || ''),
      display
    }
  })
  normDays.sort((a: any, b: any) => a.day - b.day)
  return { title: doc?.title || '', days: normDays }
}

/* ---------------- 文字大小 / 沉浸 ---------------- */
function increaseFontSize() { fontSize.value = Math.min(fontSize.value + 4, 32) }
function decreaseFontSize() { fontSize.value = Math.max(fontSize.value - 4, 12) }
function toggleFullscreen() { ui.isReadingFullscreen = !ui.isReadingFullscreen }

/* ---------------- 字級/提醒條切換後：等佈局穩定再校正 ---------------- */
watch([fontSize, () => ui.shouldShowReminder], async () => {
  await nextTick()
  await afterLayout()
  adjustForOverlap()
})

/* ---------------- 精準捲動（點「第N天」） ---------------- */
function scrollTo(day: number) {
  const idx = allDays.value.findIndex(d => Number(d.day) === Number(day))
  const h2 = h2Refs.value[idx]
  if (!h2) return
  const h = h2Heights.value[idx] ?? defaultH2Height.value
  const REVEAL_GAP = 8;
  const y = h2.getBoundingClientRect().top + window.scrollY - (baseOffset.value + REVEAL_GAP)
  window.scrollTo({ top: y, behavior: 'smooth' })
}
</script>
