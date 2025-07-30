<script setup lang="ts">
import { ref } from 'vue'
import EventCard from '../components/EventCard.vue'

const showDialog = ref(false)

function handleViewEvent(event: any) {
  if (event.canView) {
    const base = import.meta.env.BASE_URL // 通常是 '/newsite/' 或 '/'
    const id = event.id
    window.location.href = `${base}register-view?id=${id}`
  } else {
    showDialog.value = true
  }
}

// ✅ 分類好的資料
const globalEvents = ref([
  {
    id: '3',
    title: '全召會事奉特會',
    date: '9/13（主日）',
    count: 78,
    link: '/register?id=3',
    canView: true
  }
])

const localEvents = ref([
  {
    id: '1',
    title: '兒童家長交通',
    date: '8/3（六）上午 9:00',
    count: 41,
    link: '/register?id=2',
    canView: true
  },
  {
    id: '2',
    title: '大專五環交通',
    date: '8/23（六）上午 9:00',
    count: 100,
    link: '/register?id=3',
    canView: false // ❌ 模擬未開放查看
  },
  {
    id: '4',
    title: '青職福音行動',
    date: '7/28（日）下午 3:00',
    count: 23,
    link: '/register?id=1',
    canView: true
  }
])


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

