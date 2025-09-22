<!-- src/views/Rollcall/RollcallLoginView.vue -->
<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="bg-white rounded-lg shadow-lg p-6 w-80 relative">
      <!-- 關閉按鈕 -->
      <button class="absolute top-2 right-2 text-gray-500 hover:text-gray-700"
              @click="$emit('close')">
        ✖
      </button>

      <h3 class="text-lg font-bold mb-4 text-center">協助連上中央點名系統</h3>

      <div class="mb-4 text-center">
        <img v-if="captchaUrl"
             :src="captchaUrl"
             alt="驗證碼"
             class="mx-auto border rounded mb-2" />
        <button class="text-sm text-blue-600 underline" @click="$emit('loadCaptcha')">
          點擊重新取得驗證碼
        </button>
      </div>

      <form @submit.prevent="$emit('submitLogin')" class="space-y-3">
        <input
          :value="verifyCode"
          @input="$emit('update:verifyCode', $event.target.value)"
          type="text"
          placeholder="輸入驗證碼"
          class="w-full border rounded px-3 py-2"
        />
        <button type="submit"
                class="w-full bg-green-500 text-white py-2 px-4 rounded-lg hover:bg-green-600 disabled:bg-gray-300"
                :disabled="loading">
          {{ loading ? "登入中..." : "登入" }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
defineProps({
  captchaUrl: String,
  verifyCode: String,
  loading: Boolean
})
defineEmits(["update:verifyCode", "submitLogin", "loadCaptcha", "close"])
</script>
