<!-- components/video/LatestVideo.vue -->
<template>
  <section class="bg-beige pt-3 pb-3">
    <div class="max-w-7xl mx-auto px-4">
      <!-- 白底卡片包整個影音區 -->
      <div class="bg-white rounded-2xl shadow-md p-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-8">最新影音</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div
            v-for="video in videos"
            :key="video.id"
            class="bg-[#F8F8F8] rounded-xl shadow-sm hover:shadow-md cursor-pointer transition p-4"
          >
            <div class="aspect-video mb-3 overflow-hidden rounded">
              <img
                :src="video.thumbnail"
                :alt="video.title"
                class="w-full h-full object-cover"
              />
            </div>
            <h3 class="text-gray-700 text-lg font-semibold leading-snug">{{ video.title }}</h3>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>


<script setup lang="ts">
const videos = [
  { id: 1, title: '半年度訓練禱研背講', thumbnail: '/video1.png' },
  { id: 2, title: '晨興加強班', thumbnail: '/video2.png' },
  { id: 3, title: '福音真理聚會', thumbnail: '/video3.png' }
]
</script>
