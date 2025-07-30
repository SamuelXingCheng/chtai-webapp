<!-- src/views/RegisterView.vue -->
<script setup lang="ts">
import { useRoute } from 'vue-router'
import { computed } from 'vue'

// ✅ 對應每個活動的 ID 與其 iframe 網址
const iframeMap = {
  '1': 'https://docs.google.com/spreadsheets/d/e/xxxxx1/pubhtml?widget=true&headers=false',
  '2': 'https://docs.google.com/spreadsheets/d/e/xxxxx2/pubhtml?widget=true&headers=false',
  '3': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQFO_Lakd-2u1siVo830N7JAXDki8kDtKfohqMVI6MsiQlkDhlvlW7zjNcktVkc_SW5gBNSE5dlybv_/pubhtml'
}

const route = useRoute()
const id = computed(() => route.query.id as string)
const iframeUrl = computed(() => {
  const baseUrl = iframeMap[id.value]
  return baseUrl ? `${baseUrl}?widget=true&headers=false` : ''
})
</script>

<template>
  <div class="max-w-5xl mx-auto p-4 pt-[50px] space-y-4">
    <h1 class="text-2xl font-bold text-gray-800">報名名單查詢</h1>

    <div v-if="iframeUrl" class="rounded-lg overflow-hidden border shadow">
      <iframe
        :src="iframeUrl"
        width="100%"
        height="800"
        class="w-full"
        frameborder="0"
      ></iframe>
    </div>

    <div v-else class="text-red-600">
      無效的報名連結，請確認活動 ID 是否正確。
    </div>
  </div>
</template>
