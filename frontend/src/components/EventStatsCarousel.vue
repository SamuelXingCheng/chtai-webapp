<!-- components/EventStatsCarousel.vue -->
<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { collection, getDocs } from 'firebase/firestore'
import { db } from '../firebase'
import EventCard from '../components/EventCard.vue'

const showDialog = ref(false)

function handleViewEvent(event: any) {
  if (event.canView) {
    const base = import.meta.env.BASE_URL
    const id = event.id
    window.location.href = `${base}register-view?id=${id}`
  } else {
    showDialog.value = true
  }
}

// 日期格式範例：2025-09-13 ~ 2025-09-15
function formatDateRange(start: string, end: string): string {
  if (!start || !end) return ''

  const [sy, sm, sd] = start.split('-')
  const [ey, em, ed] = end.split('-')

  const sYear = sy
  const sMonth = parseInt(sm)
  const sDay = parseInt(sd)
  const eYear = ey
  const eMonth = parseInt(em)
  const eDay = parseInt(ed)

  // 同一天
  if (start === end) {
    return `${sYear}/${sMonth}/${sDay}`
  }

  // 跨年
  if (sYear !== eYear) {
    return `${sYear}/${sMonth}/${sDay} ~ ${eYear}/${eMonth}/${eDay}`
  }

  // 同年不同月
  if (sm !== em) {
    return `${sYear}/${sMonth}/${sDay} ~ ${eMonth}/${eDay}`
  }

  // 同年同月
  return `${sYear}/${sMonth}/${sDay} ~ ${eDay}`
}


const allEvents = ref([])

onMounted(async () => {
  const snapshot = await getDocs(collection(db, 'events'))
  allEvents.value = snapshot.docs.map(doc => {
    const data = doc.data()
    return {
      id: doc.id,
      title: data.title,
      date: formatDateRange(data.startDate, data.endDate),
      count: data.count ?? 0,
      registerUrl: data.registerUrl,
      responseUrl: data.responseUrl,
      canView: typeof data.responseUrl === 'string' && data.responseUrl.length > 0,
      groupName: doc.id, 
      link: `/register?id=${doc.id}`
    }
  })
})

const globalEvents = computed(() =>
  allEvents.value.filter(e => e.groupName.includes('全召會'))
)

const localEvents = computed(() =>
  allEvents.value.filter(e => !e.groupName.includes('全召會'))
)

function shareEvent(event: { title: string; date: string; link: string }) {
  const shareText = `邀請你參加「${event.title}」\n時間：${event.date}\n報名連結：https://yourdomain.com${event.link}`
  const url = `https://line.me/R/msg/text/?${encodeURIComponent(shareText)}`
  window.open(url, '_blank')
}
</script>

<template>
  <div class="bg-white border border-gray-100 shadow-md rounded-xl p-6">
    <h3 class="text-3xl font-semibold text-gray-800 mb-3 flex items-center gap-1">
            重要行動報名與統計
    </h3>
    <!-- 全召會行動 -->
    <div>
        <h3 class="text-xl font-semibold text-gray-800 mb-3 flex items-center gap-1">
            全召會行動
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <EventCard
          v-for="event in globalEvents"
          :key="event.title"
          :event="event"
          @share="shareEvent"
          @view="handleViewEvent"
        />
        </div>
    </div>

    <!-- 專項行動 -->
    <div>
        <h3 class="text-xl font-semibold text-gray-800 mb-3 flex items-center gap-1">
            專項行動
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <EventCard
              v-for="event in localEvents"
              :key="event.title"
              :event="event"
              @share="shareEvent"
              @view="handleViewEvent"
            />
        </div>
    </div>

    <!-- 彈窗提示：目前未開放查看 -->
    <div
      v-if="showDialog"
      class="fixed inset-0 bg-black/30 flex items-center justify-center z-50"
    >
      <div class="bg-white p-6 rounded-lg shadow-lg w-[280px] text-center">
        <p class="text-gray-700 text-base">目前未開放查看</p>
        <button
          class="mt-4 px-4 py-1.5 bg-blue-600 text-white rounded hover:bg-blue-700 transition text-sm"
          @click="showDialog = false"
        >
          關閉
        </button>
      </div>
    </div>
  </div>

  

</template>

