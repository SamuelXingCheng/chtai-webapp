<!-- components/home/DownloadSection.vue -->
<template>
  <section class="bg-beige pt-3 pb-3">
      <div class="max-w-7xl mx-auto px-4">
    <div class="bg-white rounded-2xl shadow-md p-8">
    <h2 class="text-2xl font-bold mb-6">下載專區</h2>

        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
            <RouterLink
                v-for="item in downloads"
                :key="item.title"
                :to="item.link"
                class="flex flex-col items-center justify-center bg-gray-50 rounded-xl shadow hover:shadow-md hover:bg-gray-100 transition p-6 text-center"
            >
                <div class="text-4xl mb-2">{{ item.icon }}</div>
                <div class="text-sm font-semibold text-gray-800">{{ item.title }}</div>
            </RouterLink>
        </div>
        </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const downloads = [
  { icon: '📄', title: '歷年週訊', link: '/weekly-news' },
  { icon: '📝', title: '各類申請單', link: '/application-forms' },
]
</script>
