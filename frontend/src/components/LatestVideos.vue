<template>
  <section class="max-w-7xl mx-auto px-4 py-12">
    <h2 class="text-2xl font-bold mb-6">最新影音</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div v-for="video in videos" :key="video.id" class="bg-white rounded shadow p-4">
        <img :src="video.thumbnail" :alt="video.title" class="mb-2 rounded" />
        <h3 class="font-semibold text-lg">{{ video.title }}</h3>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const videos = [
  { id: 1, title: '半年度訓練禱研背講', thumbnail: '/video1.png' },
  { id: 2, title: '週中得勝班', thumbnail: '/video2.png' },
  { id: 3, title: '福音真理聚會', thumbnail: '/video3.png' }
]
</script>
