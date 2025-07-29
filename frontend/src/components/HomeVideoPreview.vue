<template>
  <section class="bg-white rounded-xl shadow p-4 space-y-4">
    <h2 class="text-lg font-semibold text-gray-800 flex items-center gap-2">
      <svg class="w-5 h-5 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
        <path d="M4 4l12 6-12 6V4z" />
      </svg>
      本週影音精選
    </h2>

    <!-- 影片卡片列表 -->
    <!-- 影片卡片容器改為 grid 2欄 -->
    <div class="grid grid-cols-2 sm:grid-cols-3 gap-4">
        <div
            v-for="video in previewVideos"
            :key="video.id"
            class="bg-[#F8F8F8] rounded-xl shadow p-3 space-y-2 cursor-pointer hover:shadow-md transition"
            @click="openVideo(video.videoUrl)"
        >
            <!-- 封面圖維持 16:9 比例 -->
            <div class="relative aspect-w-16 aspect-h-9 rounded-lg overflow-hidden group">
            <img
                :src="video.coverImage"
                :alt="video.title"
                class="object-cover w-full h-full"
            />
            <!-- 播放圖示 -->
            <div class="absolute inset-0 flex items-center justify-center bg-black/40 opacity-0 group-hover:opacity-100 transition">
                <svg class="w-10 h-10 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M6 4l10 6-10 6V4z" />
                </svg>
            </div>
            </div>

            <!-- 標題與來源 -->
            <div class="text-sm font-semibold text-gray-800 leading-snug line-clamp-2">{{ video.title }}</div>
            <div class="text-xs text-gray-500 truncate">{{ video.source }}</div>
        </div>
    </div>



    <!-- 查看更多按鈕 -->
    <router-link to="/video-wall" class="block text-center text-sm text-blue-600 font-medium hover:underline mt-2">
      查看更多影音內容 →
    </router-link>
    <FloatingPlayer ref="floatingPlayerRef" />
  </section>
</template>

<script setup>
import { ref } from 'vue'
import FloatingPlayer from '../components/FloatingPlayer.vue' // 確保路徑正確

const floatingPlayerRef = ref()

const previewVideos = ref([
  {
    id: 'abc123',
    title: '2024十二月半年度訓練（第一週信息 禱研背講）',
    source: '台中市召會',
    videoUrl: 'https://www.youtube.com/watch?v=9HuKURB5fSo',
    coverImage: 'https://img.youtube.com/vi/9HuKURB5fSo/0.jpg',
  },
  {
    id: 'def456',
    title: '出埃及記的基督（詩歌MV）',
    source: '臺灣福音書房',
    videoUrl: 'https://www.youtube.com/watch?v=DEF456XYZ',
    coverImage: 'https://img.youtube.com/vi/DEF456XYZ/0.jpg',
  },
])

const openVideo = (url) => {
  floatingPlayerRef.value?.open(url)
}
</script>