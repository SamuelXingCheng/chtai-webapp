<!-- views/ApplicationForms.vue -->
<template>
  <section class="max-w-4xl mx-auto mt-10 px-4">
    <h1 class="text-2xl font-bold mb-6">📄 申請單下載</h1>

    <div class="space-y-6">
      <!-- 接待申請單 -->
      <div class="bg-white shadow rounded-lg p-4">
        <h2 class="text-xl font-semibold mb-2">📝 接待申請單</h2>
        <p class="text-gray-600 text-sm mb-3">請填寫並交由區負責人處理</p>
        <a
          href="/downloads/接待申請單.pdf"
          target="_blank"
          class="text-blue-600 hover:underline"
        >下載 PDF →</a>
      </div>

      <!-- 借用申請單 -->
      <div class="bg-white shadow rounded-lg p-4">
        <h2 class="text-xl font-semibold mb-2">🏠 借用申請單</h2>
        <p class="text-gray-600 text-sm mb-3">借用聚會場所請填寫本單</p>
        <a
          href="/downloads/借用申請單.pdf"
          target="_blank"
          class="text-blue-600 hover:underline"
        >下載 PDF →</a>
      </div>
    </div>
  </section>
</template>
