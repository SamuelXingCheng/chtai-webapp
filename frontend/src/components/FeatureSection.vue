<template>
  <section class="max-w-7xl mx-auto px-4 py-12">
    <h2 class="text-2xl font-bold mb-6">應用功能</h2>
    <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
      <div
        v-for="feature in features"
        :key="feature.title"
        class="flex flex-col items-center p-4 bg-white rounded shadow hover:shadow-md transition"
      >
        <img :src="feature.icon" :alt="feature.title" class="w-12 h-12 mb-3" />
        <span class="font-medium">{{ feature.title }}</span>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const features = [
  { title: '行動報名', icon: '/feature1.png' },
  { title: '輔助點名', icon: '/feature2.png' },
  { title: '話語供應', icon: '/feature3.png' },
  { title: '線上奉獻', icon: '/feature4.png' }
  // ...你可繼續補齊其他項目（8格為主）
]
</script>
