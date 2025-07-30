<!-- src/views/RegisterFormView.vue -->
<script setup lang="ts">
import { useRoute } from 'vue-router'
import { ref, computed, onMounted } from 'vue'
import { doc, getDoc } from 'firebase/firestore'
import { db } from '../firebase'

const route = useRoute()
const id = computed(() => route.query.id as string)

const formUrl = ref<string | null>(null)
const error = ref(false)

onMounted(async () => {
  if (!id.value) {
    error.value = true
    return
  }

  const docRef = doc(db, 'events', id.value)
  const snapshot = await getDoc(docRef)

  if (snapshot.exists()) {
    const data = snapshot.data()
    if (typeof data.registerUrl === 'string' && data.registerUrl.length > 0) {
      formUrl.value = data.registerUrl
    } else {
      error.value = true
    }
  } else {
    error.value = true
  }
})
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

    <div v-else-if="error" class="text-red-600">
      無效的報名連結，請確認活動 ID 是否正確。
    </div>

    <div v-else class="text-gray-500">
      載入中...
    </div>
  </div>
</template>
