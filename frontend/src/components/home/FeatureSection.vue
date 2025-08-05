<!-- components/home/FeatureSection.vue -->
<template>
  <section class="bg-beige pt-3 pb-3">
    <div class="max-w-7xl mx-auto px-4">
      <!-- 包一層白底卡片 -->
      <div class="bg-white rounded-2xl shadow-md p-8">
        <h2 class="text-3xl font-bold text-gray-800 mb-8">應用功能</h2>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
          <div
            v-for="feature in features"
            :key="feature.title"
            class="flex flex-col items-center justify-center p-6 bg-[#F8F8F8] rounded-xl shadow-sm cursor-pointer hover:shadow-md transition"
          >
            <img :src="feature.icon" :alt="feature.title" class="w-12 h-12 mb-3" />
            <span class="text-gray-700 font-medium text-xl">{{ feature.title }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const features = [
  { title: '話語供應', icon: '/icon/1.png' },
  { title: '聚會報名', icon: '/icon/2.png' },
  { title: '我要貼文', icon: '/icon/3.png' },
  { title: '影音詩歌', icon: '/icon/4.png' },
  { title: '輔助點名', icon: '/icon/5.png' },
  { title: '按時分糧', icon: '/icon/6.png' },
  { title: '線上奉獻', icon: '/icon/7.png' },
  { title: '聚會時間地點查詢', icon: '/icon/8.png' }
]
</script>
