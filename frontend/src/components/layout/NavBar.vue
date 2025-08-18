<!-- src/components/layout/NavBar.vue -->
<template>
  <header class="fixed top-0 w-full z-50 bg-[#ffffff]/95 backdrop-blur shadow-sm border-b">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center h-20">
      <!-- Logo 區塊 -->
      <router-link
        to="/"
        class="flex items-center gap-2 hover:opacity-80 transition"
      >
        <img src="/logo.png" alt="Logo" class="h-8 w-auto" />
        <span class="text-xl font-bold text-gray-800 whitespace-nowrap">台中市召會</span>
      </router-link>

      <!-- 導覽選單（桌面版） -->
        <nav class="hidden md:flex gap-6 text-gray-700 font-medium ml-auto mr-8">
            <RouterLink to="/" class="hover:text-blue-600 transition duration-200">首頁</RouterLink>
            <RouterLink to="/beliefs" class="hover:text-blue-600 transition duration-200">認識我們</RouterLink>
            <RouterLink to="/gatherings" class="hover:text-blue-600 transition duration-200">聚會資訊</RouterLink>
            <RouterLink to="/weekly-news" class="hover:text-blue-600 transition duration-200">召會週訊</RouterLink>
        
            <RouterLink
                v-if="isLoggedIn"
                to="/profile"
                class="hover:text-blue-600 transition duration-200"
                >
                個人資料
            </RouterLink>
        </nav>
      <!-- 語言切換（桌面版） -->
        <div class="hidden md:flex items-center gap-3">
            <LoginButton /> 
            <button class="text-sm text-gray-600 hover:text-blue-600">中文</button>
            <span class="text-gray-400">|</span>
            <button class="text-sm text-gray-600 hover:text-blue-600">EN</button>
        </div>

      <!-- 漢堡選單按鈕（手機版） -->
        <div class="flex items-center gap-3 md:hidden">
            <LoginButton /> <!-- 👈 手機版登入按鈕放左邊 -->
            <button @click="isOpen = true" class="text-gray-700 focus:outline-none">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
            </button>
        </div>
    </div>

    <!-- 手機選單遮罩 -->
    <div
      v-if="isOpen"
      class="fixed inset-0 bg-black bg-opacity-40 z-40"
      @click="isOpen = false"
    ></div>

    <!-- 手機側邊選單 -->
    <div
        v-if="isOpen"
        class="fixed top-4 right-4 w-[260px] max-h-[90vh] bg-white z-50 shadow-xl rounded-xl p-6 flex flex-col gap-4 overflow-auto"
    >
        <button class="self-end text-gray-500 hover:text-gray-700 mb-2" @click="isOpen = false">✕</button>

        <RouterLink to="/" class="text-gray-800 font-medium hover:text-blue-600">首頁</RouterLink>
        <RouterLink to="/beliefs" class="text-gray-800 font-medium hover:text-blue-600">認識我們</RouterLink>
        <RouterLink to="/gatherings" class="text-gray-800 font-medium hover:text-blue-600">聚會資訊</RouterLink>
        <RouterLink to="/weekly-news" class="text-gray-800 font-medium hover:text-blue-600">召會週訊</RouterLink>
        <RouterLink
            v-if="isLoggedIn"
            to="/profile"
            class="text-gray-800 font-medium hover:text-blue-600"
            >
            個人資料
        </RouterLink>
        <hr />

        <div class="flex gap-2 pt-2">
        <button class="text-sm text-gray-600 hover:text-blue-600">中文</button>
        <span class="text-gray-400">|</span>
        <button class="text-sm text-gray-600 hover:text-blue-600">EN</button>
        </div>
    </div>
  </header>
</template>

<script setup lang="ts">
    import { ref, onMounted, watch } from 'vue'
    import { getAuth, onAuthStateChanged } from 'firebase/auth'
    import { RouterLink } from 'vue-router'
    import LoginButton from '../../components/auth/LoginButton.vue'

    const emit = defineEmits<{
      (e: 'menu-open', value: boolean): void
    }>()

    const isOpen = ref(false)
    const isLoggedIn = ref(false)

    watch(isOpen, (val) => {
      emit('menu-open', val)
    })

    onMounted(() => {
        const auth = getAuth()
        onAuthStateChanged(auth, (user) => {
            isLoggedIn.value = !!user
        })
    })

</script>
