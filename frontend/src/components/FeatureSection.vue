<template>
  <section class="bg-beige pt-3 pb-3">
    <div class="max-w-7xl mx-auto px-4">
      <!-- 包一層白底卡片 -->
      <div class="bg-white rounded-2xl shadow-md p-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-8">應用功能</h2>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
          <div
            v-for="feature in features"
            :key="feature.title"
            class="flex flex-col items-center justify-center p-6 bg-[#F8F8F8] rounded-xl shadow-sm cursor-pointer hover:shadow-md transition"
          >
            <img :src="feature.icon" :alt="feature.title" class="w-10 h-10 mb-3" />
            <span class="text-gray-700 font-medium">{{ feature.title }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const features = [
  { title: '行動報名', icon: '/feature1.png' },
  { title: '輔助點名', icon: '/feature2.png' },
  { title: '話語供應', icon: '/feature3.png' },
  { title: '線上奉獻', icon: '/feature4.png' },
  { title: '排班統計', icon: '/feature5.png' },
  { title: '課程管理', icon: '/feature6.png' },
  { title: '禱告提交', icon: '/feature7.png' },
  { title: '出席紀錄', icon: '/feature8.png' }
]
</script>
