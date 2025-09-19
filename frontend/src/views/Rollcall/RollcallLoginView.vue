<!-- src/views/Rollcall/RollcallLoginView.vue -->
<template>
  <div>
    <div class="mb-4 text-center">
      <img
        v-if="captchaUrl"
        :src="captchaUrl"
        alt="驗證碼"
        class="mx-auto border rounded mb-2"
      />
      <button class="text-sm text-blue-600 underline" @click="$emit('loadCaptcha')">
        重新取得驗證碼
      </button>
    </div>

    <form @submit.prevent="$emit('submitLogin')" class="space-y-3">
      <input
        :value="verifyCode"
        @input="$emit('update:verifyCode', $event.target.value)"
        type="text"
        placeholder="驗證碼"
        class="w-full border rounded px-3 py-2"
      />
      <button
        type="submit"
        class="w-full bg-green-500 text-white py-2 px-4 rounded-lg hover:bg-green-600 disabled:bg-gray-300"
        :disabled="loading"
      >
        {{ loading ? "登入中..." : "登入" }}
      </button>
    </form>
  </div>
</template>

<script setup>
defineProps({
  captchaUrl: String,
  verifyCode: String,
  loading: Boolean
})
defineEmits(["update:verifyCode", "submitLogin", "loadCaptcha"])
</script>
