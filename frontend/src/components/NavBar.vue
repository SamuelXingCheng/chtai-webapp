<template>
  <header class="fixed top-0 w-full z-50 bg-[#ffffff]/95 backdrop-blur shadow-sm border-b">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center h-20">
      <!-- Logo 區塊 -->
        <div class="flex items-center gap-2">
            <img src="/logo.png" alt="Logo" class="h-8 w-auto" />
            <span class="text-xl font-bold text-gray-800 whitespace-nowrap">台中市召會</span>
        </div>

      <!-- 導覽選單 -->
      <nav class="hidden md:flex gap-6 text-gray-700 font-medium">
        <a href="#" class="hover:text-blue-600 transition duration-200">首頁</a>
        <a href="#" class="hover:text-blue-600 transition duration-200">系統見證</a>
        <a href="#" class="hover:text-blue-600 transition duration-200">各聚會區</a>
        <a href="#" class="hover:text-blue-600 transition duration-200">生命期刊</a>
      </nav>

      <!-- 語言切換 -->
      <div class="flex items-center gap-3">
        <button class="text-sm text-gray-600 hover:text-blue-600 transition duration-200">中文</button>
        <span class="text-gray-400">|</span>
        <button class="text-sm text-gray-600 hover:text-blue-600 transition duration-200">EN</button>
      </div>
    </div>
  </header>
</template>


<script setup lang="ts">
</script>

<style scoped>
</style>
