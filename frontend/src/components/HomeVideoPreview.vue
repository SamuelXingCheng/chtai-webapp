<template>
  <section class="bg-white rounded-xl shadow p-4 space-y-8">
    <!-- 本週信息影音精選 -->
    <section class="space-y-4">
      <h2 class="text-lg font-semibold text-gray-800 flex items-center gap-2">
        <svg class="w-5 h-5 text-blue-500" fill="currentColor" viewBox="0 0 20 20"><path d="M4 4l12 6-12 6V4z" /></svg>
        一年七次特會訓練 精選
      </h2>
      <VideoGrid :videos="infoVideos" @play="openVideo" />
    </section>

    <!-- 兒少影音精選 -->
    <section class="space-y-4">
      <h2 class="text-lg font-semibold text-gray-800 flex items-center gap-2">
        <svg class="w-5 h-5 text-yellow-500" fill="currentColor" viewBox="0 0 20 20"><path d="M4 4l12 6-12 6V4z" /></svg>
        兒少影音 精選
      </h2>
      <VideoGrid :videos="childrenVideos" @play="openVideo" />
    </section>

    <!-- 福音詩歌精選 - 嵌入 SoundCloud -->
    <section class="space-y-4">
      <h2 class="text-lg font-semibold text-gray-800 flex items-center gap-2">
        <svg class="w-5 h-5 text-red-500" fill="currentColor" viewBox="0 0 20 20"><path d="M4 4l12 6-12 6V4z" /></svg>
        福音詩歌 精選
      </h2>
        <!-- ✅ 嵌入播放器 -->
        <div class="rounded-xl overflow-hidden shadow">
            <iframe
            id="sc-player"
            width="100%"
            height="300"
            scrolling="no"
            frameborder="no"
            allow="autoplay"
            :src="soundcloudEmbedUrl"
            class="rounded-xl"
            ></iframe>
        </div>
    </section>

    <FloatingPlayer ref="floatingPlayerRef" />
  </section>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { collection, getDocs } from 'firebase/firestore'
import { db } from '../firebase'

import FloatingPlayer from '../components/FloatingPlayer.vue'
import VideoGrid from '../components/VideoGrid.vue'

const floatingPlayerRef = ref()

// 類別影片資料
const infoVideos = ref([])
const childrenVideos = ref([])
const gospelVideos = ref([])

// SoundCloud 連結
const soundcloudEmbedUrl =
  'https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/playlists/1871928719&color=%23D9D9D9&auto_play=false&hide_related=true&show_comments=false&show_user=false&show_reposts=false&show_teaser=false&visual=false'

// 開啟浮動播放器
const openVideo = (url) => {
  floatingPlayerRef.value?.open(url)
}

// 載入 Firestore 中的 videos collection
const loadVideos = async () => {
  try {
    const snapshot = await getDocs(collection(db, 'videos'))
    const allVideos = snapshot.docs.map(doc => doc.data())

    // 分類（記得和 Firestore 裡的 category 一致）
    infoVideos.value = allVideos.filter(v => v.category === '當週信息')
    childrenVideos.value = allVideos.filter(v => v.category === '兒少影音')
    gospelVideos.value = allVideos.filter(v => v.category === '福音影音')
  } catch (err) {
    console.error('載入影片失敗：', err)
  }
}

onMounted(() => {
  loadVideos()
})
</script>
