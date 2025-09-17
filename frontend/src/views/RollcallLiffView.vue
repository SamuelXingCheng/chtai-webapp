<!-- src/views/RollcallLiffView.vue -->
<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center">
    <div class="bg-white shadow-lg rounded-xl p-6 w-full max-w-sm">
      <h2 class="text-xl font-bold mb-4 text-center">中央點名系統登入</h2>

      <!-- 如果還沒登入，顯示驗證碼區塊 -->
      <div v-if="!loginSuccess" class="mb-4 text-center">
        <img
          v-if="captchaUrl"
          :src="captchaUrl"
          alt="驗證碼"
          class="mx-auto border rounded mb-2"
        />
        <button
          class="text-sm text-blue-600 underline"
          @click="loadCaptcha"
        >
          重新取得驗證碼
        </button>
      </div>

      <!-- 如果還沒登入，顯示登入表單 -->
      <form v-if="!loginSuccess" @submit.prevent="submitLogin" class="space-y-3">
        <input
          v-model="verifyCode"
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

      <!-- 訊息 -->
      <div
        v-if="message"
        class="mt-4 text-center text-sm"
        :class="loginSuccess ? 'text-green-600' : 'text-red-600'"
      >
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import liff from "@line/liff"

const API_URL = import.meta.env.VITE_ROLLCALL_API_URL || "https://citcnew.org.tw/attendance-helper"
const LIFF_ID = import.meta.env.VITE_ROLLCALL_LIFF_ID

// 狀態
const captchaUrl = ref("")
const username = ref("")
const picID = ref("")
const password = ref("")
const verifyCode = ref("")
const loading = ref(false)
const message = ref("")
const loginSuccess = ref(false)

// 初始化
onMounted(async () => {
  await liff.init({ liffId: LIFF_ID })
  if (!liff.isLoggedIn()) {
    liff.login()
    return
  }

  // 先檢查後端 session 狀態
  try {
    const res = await fetch(`${API_URL}/?path=central-session&ts=${Date.now()}`)
    const data = await res.json()
    if (data.loggedIn) {
      loginSuccess.value = true
      message.value = "✅ " + data.message
    } else {
      message.value = "⚠️ " + data.message
      loadCaptcha()
    }
  } catch (err) {
    message.value = "❌ 檢查登入狀態失敗：" + err.message
    loadCaptcha()
  }
})

// 抓驗證碼圖片
async function loadCaptcha() {
  try {
    const res = await fetch(`${API_URL}/?path=central-verify&ts=${Date.now()}`)
    const data = await res.json()
    captchaUrl.value = data.url
    picID.value = data.picID
  } catch (err) {
    message.value = "❌ 無法載入驗證碼：" + err.message
  }
}

// 送出登入
async function submitLogin() {
  loading.value = true
  message.value = ""
  loginSuccess.value = false
  try {
    const res = await fetch(`${API_URL}/?path=central-login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        verifyCode: verifyCode.value,
        picID: picID.value
      })
    })

    const result = await res.json()
    if (result.success || result.status === "success") {
      loginSuccess.value = true
      message.value = "✅ 登入成功，可以開始點名"
    } else {
      message.value = "❌ 登入失敗：" + (result.message || "請檢查帳密與驗證碼")
    }
  } catch (err) {
    message.value = "❌ 連線錯誤：" + err.message
  } finally {
    loading.value = false
  }
}
</script>
