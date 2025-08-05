<!-- src/components/VideoGrid.vue -->
<template>
  <div class="grid grid-cols-2 sm:grid-cols-3 gap-4">
    <div
      v-for="video in videos"
      :key="video.id"
      class="bg-[#F8F8F8] rounded-xl shadow p-3 space-y-2 cursor-pointer hover:shadow-md transition"
      @click="$emit('play', video.videoUrl)"
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
      <div class="text-sm font-semibold text-gray-800 leading-snug line-clamp-2">
        {{ video.title }}
      </div>
      <!-- <div class="text-xs text-gray-500 truncate">
        {{ video.source }}
      </div> -->
    </div>
  </div>
</template>

<script setup>
defineProps({
  videos: {
    type: Array,
    required: true,
  },
})
</script>
