<!-- src/components/TopBar.vue -->
<template>
  <div>
    <!-- 提醒條在上層，吸頂 -->
    <Transition name="slide-fade">
      <div
        v-if="shouldShowReminder"
        class="fixed top-0 w-full z-[60] bg-beige text-sm text-center py-3 px-4 border-b shadow"
      >
        填寫個人資料，解鎖更多功能。
        <RouterLink
          to="/profile"
          class="ml-2 inline-block bg-amber-200 hover:bg-amber-300 text-amber-900 font-medium text-sm px-3 py-1 rounded-md transition"
        >
          立即填寫
        </RouterLink>
      </div>
    </Transition>

    <!-- 導覽列放在提醒條下方，offset 為提醒條高度 -->
    <Navbar
      :class="[
        'fixed w-full z-50 bg-white/95 backdrop-blur shadow-sm border-b transition-all duration-300',
        shouldShowReminder ? 'top-[48px]' : 'top-0'
      ]"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { getAuth, onAuthStateChanged } from 'firebase/auth'
import { doc, getDoc } from 'firebase/firestore'
import { auth, db } from '../firebase'
import Navbar from './NavBar.vue'

const shouldShowReminder = ref(false)

onMounted(() => {
  onAuthStateChanged(auth, async (user) => {
    if (!user) return

    const userRef = doc(db, 'users', user.uid)
    const snap = await getDoc(userRef)

    if (!snap.exists()) {
      console.log('使用者文件不存在，顯示提醒')
      shouldShowReminder.value = true
      return
    }

    const data = snap.data()
    if (localStorage.getItem('profileJustSaved')) {
      console.log('localStorage 檢測到 profileJustSaved，略過提醒')
      shouldShowReminder.value = false
      localStorage.removeItem('profileJustSaved')
    } else if (!data.name || !data.area || !data.sub_area) {
      console.log('使用者資料不完整，顯示提醒')
      shouldShowReminder.value = true

      // ✅ 延長可見時間為 5 秒
      setTimeout(() => {
        shouldShowReminder.value = false
      }, 5000)
    }
  })
})
</script>

<style scoped>
.slide-fade-enter-active {
  transition: all 0.4s ease;
}
.slide-fade-leave-active {
  transition: all 0.3s ease;
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
