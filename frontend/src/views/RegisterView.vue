<!-- src/views/RegisterView.vue -->
<script setup lang="ts">
import { useRoute } from 'vue-router'
import { computed, ref, onMounted } from 'vue'
import { db } from '../firebase'
import { doc, getDoc } from 'firebase/firestore'

const route = useRoute()
const id = computed(() => route.query.id as string)

const rawUrl = ref('')
const iframeLoaded = ref(false)
const iframeError = ref(false)

const isLoading = ref(true)

const isEmbedUrl = computed(() => rawUrl.value.includes('/pubhtml'))

const iframeUrl = computed(() => {
  if (!isEmbedUrl.value) return ''
  return rawUrl.value.includes('?')
    ? rawUrl.value
    : `${rawUrl.value}?widget=true&headers=false`
})

onMounted(async () => {
  if (!id.value) {
    isLoading.value = false
    return
  }

  const docRef = doc(db, 'events', id.value)
  const snapshot = await getDoc(docRef)

  if (snapshot.exists()) {
    const data = snapshot.data()
    rawUrl.value = data.responseUrl || ''
  }
  isLoading.value = false

})
</script>

<template>
  <div class="max-w-3xl mx-auto p-4 pt-[96px]">
  <div class="bg-white border border-gray-200 shadow-md rounded-xl p-6 space-y-6">
    <!-- 標題 -->
    <h1 class="text-2xl font-bold text-gray-800 text-center">報名名單查詢</h1>

    <!-- 🔄 資料載入中 -->
    <div v-if="isLoading" class="text-gray-400 italic text-center">
      正在查詢活動資訊...
    </div>

    <!-- ✅ iframe 成功載入 -->
    <div
      v-if="iframeUrl && !iframeError"
      class="relative rounded-lg overflow-hidden border shadow"
    >
      <div
        v-if="!iframeLoaded"
        class="absolute inset-0 bg-white/80 flex items-center justify-center z-10"
      >
        <span class="text-gray-500">資料載入中...</span>
      </div>
      <iframe
        :src="iframeUrl"
        width="100%"
        height="900"
        class="w-full block"
        frameborder="0"
        @load="iframeLoaded = true"
        @error="iframeError = true"
      ></iframe>
    </div>

    <!-- 🔗 若不是 iframe 顯示的網址 -->
    <div
      v-if="!isEmbedUrl && rawUrl"
      class="text-center space-y-4"
    >
      <p class="text-gray-700 text-base">
        此報名表無法內嵌顯示，請點擊下方查看原始內容：
      </p>
      <a
        :href="rawUrl"
        target="_blank"
        class="inline-flex items-center gap-1 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 shadow transition text-sm"
      >
        🔗 前往查看原始報名表
      </a>
    </div>

    <!-- ❌ 無效 ID 或找不到 responseUrl -->
    <div
      v-if="!isLoading && !rawUrl"
      class="text-red-600 text-center"
    >
      無效的報名連結，請確認活動 ID 是否正確。
    </div>
  </div>
</div>

</template>
