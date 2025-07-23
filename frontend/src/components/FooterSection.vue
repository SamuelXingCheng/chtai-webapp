<template>
  <footer class="bg-gray-100 text-gray-700 mt-16 py-6">
    <div class="max-w-6xl mx-auto px-4 flex flex-col md:flex-row justify-between items-center gap-4 text-sm">

      <!-- 左側資訊欄 -->
      <div class="flex items-center gap-6 flex-wrap justify-center md:justify-start">
        <div class="flex items-center gap-2">
          <span class="text-lg">📍</span>
          <span>台中市召會總執事室 (402)台中市南區復興路三段479號 </span>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-lg">📞</span>
          <span>(04)2222-4283</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-lg">📧</span>
          <span>chtai479@ms9.hinet.net</span>
        </div>
      </div>

      <!-- 右側連結 -->
      <div class="flex items-center gap-1 hover:underline text-blue-700 cursor-pointer">
        <RouterLink to="/about">關於我們 &gt;</RouterLink>
      </div>
    </div>
  </footer>
</template>
