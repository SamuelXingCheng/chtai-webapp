<template>
  <div>
    <!-- 尚未登入時顯示登入按鈕 -->
    <button
      v-if="!currentUser"
      @click="signInWithGoogle"
      class="flex items-center gap-2 bg-white border border-gray-300 px-4 py-2 rounded-md shadow hover:shadow-md transition"
    >
      <img src="/icon/9.png" alt="登入 Icon" class="w-5 h-5" />
      <span class="text-sm text-gray-700 font-medium">登入</span>
    </button>

    <!-- 已登入時顯示使用者資訊與登出按鈕 -->
    <div v-else class="flex items-center gap-3 text-gray-700">
      <img
        v-if="currentUser.photoURL"
        :src="currentUser.photoURL"
        alt="頭像"
        class="w-6 h-6 rounded-full"
      />
      <span class="text-sm font-medium">{{ currentUser.displayName }}</span>
        <button
            @click="signOutUser"
            class="px-3 py-1 text-sm text-gray-600 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200 transition"
            >
            登出
        </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { auth, provider } from '../firebase'
import { signInWithPopup, onAuthStateChanged, signOut } from 'firebase/auth'

const router = useRouter()
const currentUser = ref<any | null>(null)

// 登入
const signInWithGoogle = async () => {
  try {
    const result = await signInWithPopup(auth, provider)
    currentUser.value = result.user
    console.log('✅ 已登入使用者：', result.user.displayName)
    router.push('/')
  } catch (error) {
    console.error('❌ 登入失敗：', error)
  }
}

// 登出
const signOutUser = async () => {
  try {
    await signOut(auth)
    currentUser.value = null
    console.log('🚪 使用者已登出')
    router.push('/')
  } catch (error) {
    console.error('❌ 登出失敗：', error)
  }
}

// 監聽登入狀態
onMounted(() => {
  onAuthStateChanged(auth, (user) => {
    currentUser.value = user
  })
})
</script>
