<script setup lang="ts">
import { ref } from 'vue'
import EventCard from '../components/EventCard.vue'

// ✅ 分類好的資料
const globalEvents = ref([
  {
    title: '全召會事奉特會',
    date: '9/13（主日）',
    count: 78,
    link: '/register?id=3'
  }
])

const localEvents = ref([
  {
    title: '兒童家長交通',
    date: '8/3（六）上午 9:00',
    count: 41,
    link: '/register?id=2'
  },
  {
    title: '大專五環交通',
    date: '8/23（六）上午 9:00',
    count: 100,
    link: '/register?id=3'
  },
  {
    title: '青職福音行動',
    date: '7/28（日）下午 3:00',
    count: 23,
    link: '/register?id=1'
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
            />
        </div>
    </div>

  </div>
</template>

