<template>
  <button
    @click="signInWithGoogle"
    class="flex items-center gap-2 bg-white border border-gray-300 px-4 py-2 rounded-md shadow hover:shadow-md transition"
  >
    <img src="/icon/9.png" alt="登入 Icon" class="w-5 h-5" />
    <span class="text-sm text-gray-700 font-medium">登入</span>
  </button>
</template>

<script setup lang="ts">
import { auth, provider } from '../firebase'
import { signInWithPopup } from 'firebase/auth'
import { useRouter } from 'vue-router'

const router = useRouter()

const signInWithGoogle = async () => {
  try {
    const result = await signInWithPopup(auth, provider)
    const user = result.user
    console.log('✅ 已登入使用者：', user.displayName)
    // 這裡可以導向到首頁或其他頁面
    router.push('/')
  } catch (error) {
    console.error('❌ 登入失敗：', error)
  }
}
</script>
