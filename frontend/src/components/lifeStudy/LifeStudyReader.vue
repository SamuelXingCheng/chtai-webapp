<!-- components/lifeStudy/LifeStudyReader.vue -->
<template>
  <div
    ref="scrollWrap"
    :class="[
      immersive
        ? 'fixed inset-0 z-50 bg-[#262626] text-[#eaeaea] overflow-y-auto px-6 py-10'
        : 'max-w-7xl mx-auto bg-beige px-4 sm:px-6 lg:px-8 py-8',
      'space-y-6 transition-all duration-300'
    ]"
  >
    <!-- 標題列：一般維持，沈浸用霧面條與淡邊 -->
    <div
      ref="titleRow"
      :class="[
        // 一般：維持 sticky
        // 沉浸：改成 relative，和內容在同一平面
        immersive
          ? 'relative px-6 py-2 flex flex-wrap items-center gap-4 bg-[#262626]'
          : 'sticky z-40 px-6 py-1 flex flex-wrap items-center justify-between gap-4 bg-inherit'
      ]"
      :style="immersive ? {} : { top: headerTopPx }"
    >
      <h1 :style="{ fontSize }"
          :class="[immersive ? 'text-[#C19960]' : 'text-blue-700', 'font-bold whitespace-normal sm:whitespace-nowrap']">
        {{ mergedTitle || '生命讀經載入中…' }}
      </h1>
    </div>

    <!-- 導覽列 -->
  <div
    ref="navRow"
    :class="[
      immersive
        ? 'sticky top-[-2.5rem] z-30 py-[2.5px] bg-[#262626]'
        : 'sticky z-30 py-[3.5px] bg-beige border-b border-neutral-200'
    ]"
    :style="immersive ? {} : { top: navTopPx }"
  >
    <div :class="[immersive ? 'w-full' : 'max-w-7xl mx-auto px-4']">

      <!-- 一列兩欄（桌面版同排，手機版左天數右齒輪） -->
      <div class="flex items-center gap-2 relative sm:static sm:flex-nowrap sm:justify-between">

        <!-- 左：天數列 -->
        <div :class="[
          'flex-1 min-w-0 overflow-x-auto scrollbar-hide',
          immersive ? 'order-1' : 'order-1'
        ]">
          <div class="flex gap-2 w-max">
            <span
              v-for="day in allDays"
              :key="day.day"
              class="shrink-0 px-2 py-1 rounded-full transition shadow-sm cursor-pointer border"
              :class="immersive
                ? 'border-white/15 text-[#C19960] bg-white/5 hover:bg-white/10'
                : 'border-amber-700 text-amber-700 bg-white hover:bg-amber-100'"
              @click="scrollTo(day.day)"
            >
              第{{ day.day }}天
            </span>
          </div>
        </div>

        <!-- 右：手機版齒輪 -->
        <div class="flex-shrink-0 sm:hidden">
          <button
            @click="showFontMenu = !showFontMenu"
            class="p-2 rounded-full border transition hover:bg-white/10"
            :class="immersive ? 'border-white/15 text-[#C19960]' : 'border-neutral-300 text-gray-600'"
            aria-label="閱讀設定"
            title="閱讀設定"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none"
                viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round"
                    d="M4 6h12M4 12h12M4 18h12M18 6h.01M18 12h.01M18 18h.01"/>
            </svg>
          </button>
        </div>

        <!-- 右：桌面版字體控制列 -->
        <div
          class="hidden sm:flex items-center gap-2 flex-nowrap whitespace-nowrap"
          :class="[
            cardOffsetClass,
            immersive ? 'bg-white/5 border border-white/10 rounded-xl p-2'
                      : 'bg-white border border-neutral-200 rounded-xl p-2'
          ]"
        >
          <span :class="[immersive ? 'text-[#C19960]' : 'text-gray-600', 'text-sm']">字體大小：</span>
          <button @click="decreaseFontSize" class="shrink-0 px-2 py-1 text-sm rounded border"
            :class="immersive ? 'bg-white/5 border-white/15 text-[#C19960]' : 'bg-white hover:bg-gray-100'">A-</button>
          <button @click="increaseFontSize" class="shrink-0 px-2 py-1 text-sm rounded border"
            :class="immersive ? 'bg-white/5 border-white/15 text-[#C19960]' : 'bg-white hover:bg-gray-100'">A+</button>
          <button @click="toggleFullscreen" class="shrink-0 px-3 py-1 text-sm rounded border"
            :class="immersive ? 'bg-white/5 border-white/15 text-[#C19960]' : 'bg-white hover:bg-gray-100'">
            {{ immersive ? '返回一般模式' : '沉浸閱讀' }}
          </button>
        </div>
      </div>

      <!-- 手機版展開的字體控制列 -->
      <div v-if="showFontMenu" class="mt-2 flex flex-wrap gap-2 sm:hidden">
        <span :class="[immersive ? 'text-[#C19960]' : 'text-gray-600', 'text-sm']">字體大小：</span>
        <button @click="decreaseFontSize" class="shrink-0 px-2 py-1 text-sm rounded border"
          :class="immersive ? 'bg-white/5 border-white/15 text-[#C19960]' : 'bg-white hover:bg-gray-100'">A-</button>
        <button @click="increaseFontSize" class="shrink-0 px-2 py-1 text-sm rounded border"
          :class="immersive ? 'bg-white/5 border-white/15 text-[#C19960]' : 'bg-white hover:bg-gray-100'">A+</button>
        <button @click="toggleFullscreen" class="shrink-0 px-3 py-1 text-sm rounded border"
          :class="immersive ? 'bg-white/5 border-white/15 text-[#C19960]' : 'bg-white hover:bg-gray-100'">
          {{ immersive ? '返回一般模式' : '沉浸閱讀' }}
        </button>
      </div>

    </div>
  </div>



    <!-- 內容：沈浸=滿版（max-w-none）+ 反色，並把外層 space 的間距吃掉讓它貼合導覽列 -->
    <main
      :class="[
        'w-full space-y-6',
        immersive ? 'prose prose-invert max-w-none -mt-6' : 'prose max-w-none'
      ]"
      :style="{ scrollPaddingTop: baseOffsetPx }"
    >
      <section
        v-for="(day, idx) in allDays"
        :key="day.day"
        :id="`day-${day.day}`"
        :class="[
          immersive
            ? 'border-b border-white/10'                             /* 滿版分節線 */
            : 'border-b pb-1 rounded overflow-hidden bg-white shadow' /* 原樣卡片 */
        ]"
        :style="{ scrollMarginTop: baseOffsetPx }"
      >
        <!-- h2：改用共用偏移（一般：ml-3；沉浸：0） -->
        <h2
          :ref="el => setH2Ref(idx, el)"
          :class="[
            immersive
              ? 'text-[#C19960] border-l-2 border-amber-400 text-lg font-semibold px-3 py-2 inline-flex items-center gap-2 mt-2'
              : 'text-lg font-semibold text-white bg-amber-700 px-3 py-2 rounded-md shadow inline-block mt-3',
            cardOffsetClass
          ]"
        >
          第{{ day.day }}天｜{{ day.label }}｜{{ day.verse }}
        </h2>

        <!-- 段落 -->
        <div :class="['px-5', immersive ? 'py-2' : 'py-0.5', 'space-y-1']">
          <p
            v-for="(para, i) in day.display"
            :key="i"
            :class="[
              'rounded-md px-3 py-2 mt-0.5',
              para.isHeading ? 'font-semibold indent-0' : 'indent-8',
              (!para.isHeading && para.bodyIndex % 2 === 1)
                ? (immersive ? 'bg-[#B3884E]/25' : 'bg-[#B3884E]/50')
                : '',
              immersive ? 'text-neutral-200 leading-relaxed text-justify' : 'text-black leading-relaxed text-justify'
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
const scrollWrap = ref<HTMLElement | null>(null)

const showFontMenu = ref(false)

/* 沉浸狀態 */
const immersive = computed(() => ui.isReadingFullscreen)

/* 基本狀態 */
const fontSize = ref(18)
const mergedTitle = ref('')
const allDays = ref<any[]>([])

/* 吸頂列高度（動態量測） */
const titleRow = ref<HTMLElement|null>(null)
const navRow   = ref<HTMLElement|null>(null)

const headerOffset = computed(() => (ui.shouldShowReminder ? 96 : 48))
const headerTopPx  = computed(() => `${headerOffset.value}px`)

const titleH = ref(0)
const navH   = ref(0)
const EPS = 1

const afterLayout = () =>
  new Promise<void>(r => requestAnimationFrame(() => requestAnimationFrame(() => r())))

function adjustForOverlap() {
  let bestIdx = -1, bestDelta = 0
  h2Refs.value.forEach((h2, idx) => {
    if (!h2) return
    const h = h2Heights.value[idx] ?? defaultH2Height.value
    const stickyBottom = baseOffset.value
    const targetTop = baseOffset.value - h
    const top = h2.getBoundingClientRect().top
    if (top > -EPS && top < stickyBottom + EPS) {
      const delta = top - targetTop
      if (bestIdx === -1 || Math.abs(delta) < Math.abs(bestDelta)) {
        bestIdx = idx
        bestDelta = delta
      }
    }
  })
  if (bestIdx !== -1 && Math.abs(bestDelta) > 0.5) {
    window.scrollBy({ top: bestDelta })
  }
}

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

/* 導覽列頂端：一般模式才需要把 navH 算進 baseOffset */
const navTopPx = computed(() => `${headerOffset.value + titleH.value-2}px`)
const baseOffset = computed(() =>
  (immersive.value ? headerOffset.value : headerOffset.value + titleH.value + navH.value)
)
const baseOffsetPx = computed(() => `${baseOffset.value}px`)

/* 每段 <h2> 的高度量測 */
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
const defaultH2Height = computed(() => h2Heights.value[0] ?? 40)

/* 載入資料（原邏輯） */
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
    await nextTick()
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

/* 字級 / 沉浸切換 */
function increaseFontSize() { fontSize.value = Math.min(fontSize.value + 4, 32) }
function decreaseFontSize() { fontSize.value = Math.max(fontSize.value - 4, 12) }
function toggleFullscreen() { ui.isReadingFullscreen = !ui.isReadingFullscreen }

/* 版面變動後校正 */
watch([fontSize, () => ui.shouldShowReminder], async () => {
  await nextTick()
  await afterLayout()
  adjustForOverlap()
})

/* 精準捲動（點「第N天」） */
function scrollTo(day: number) {
  const idx = allDays.value.findIndex(d => Number(d.day) === Number(day))
  const h2 = h2Refs.value[idx]
  if (!h2) return

  const REVEAL_GAP = 8
  // 沉浸：只扣提醒條；一般：扣 TopBar+標題+導覽
  const offset = immersive.value
    ? headerOffset.value + REVEAL_GAP
    : baseOffset.value + REVEAL_GAP

  if (immersive.value && scrollWrap.value) {
    // 目標在容器內的相對位移
    const wrap = scrollWrap.value
    const delta = h2.getBoundingClientRect().top - wrap.getBoundingClientRect().top
    const target = wrap.scrollTop + (delta - offset)
    wrap.scrollTo({ top: target, behavior: 'smooth' })
  } else {
    const y = h2.getBoundingClientRect().top + window.scrollY - offset
    window.scrollTo({ top: y, behavior: 'smooth' })
  }
}
</script>
