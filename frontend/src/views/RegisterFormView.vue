<!-- src/views/RegisterFormView.vue -->
<script setup lang="ts">
import { useRoute } from 'vue-router'
import { computed } from 'vue'

// 表單對應表（之後可以改成從 Firebase 或 Google Sheet 抓）
const formMap = {
  '1': 'https://docs.google.com/forms/d/e/1FAIpQLSdNeb76cs6V-FQ5P-guZgh1nZsFRe_s4eRzouxpiDD5y8m3mw/viewform?embedded=true',
  // 之後可加上更多 ID
}

const route = useRoute()
const id = computed(() => route.query.id as string)
const formUrl = computed(() => formMap[id.value])
</script>

<template>
  <div class="max-w-5xl mx-auto pt-[96px] p-4 space-y-6">
    <h1 class="text-2xl font-bold text-gray-800">前往報名</h1>

    <div v-if="formUrl" class="rounded-lg overflow-hidden border shadow">
      <iframe
        :src="formUrl"
        width="100%"
        height="1200"
        class="w-full"
        frameborder="0"
      >
        載入中...
      </iframe>
    </div>

    <div v-else class="text-red-600">
      無效的報名表單 ID，請確認網址正確。
    </div>
  </div>
</template>
