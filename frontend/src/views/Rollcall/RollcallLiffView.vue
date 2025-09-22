<!-- src/views/Rollcall/RollcallLiffView.vue -->
<template>
  <div class="min-h-screen bg-gray-100 pt-20">
    <div class="min-h-screen bg-gray-100 flex items-center justify-center">
      <div class="bg-white shadow-lg rounded-xl p-6 w-full max-w-sm">

        <h2 class="text-xl font-bold mb-4 text-center">台中市召會輔助點名系統</h2>

        <!-- 狀態 + 協助登入 -->
        <div class="flex flex-col items-center space-y-4 mb-6">
          <!-- 狀態提示 -->
          <div class="text-center text-sm"
              :class="loginSuccess ? 'text-green-600' : 'text-yellow-600'">
            {{ loginSuccess ? "🟢 已連線中央點名系統，點名將即時同步"
                            : "⚠️ 未連線中央點名系統，仍可點名，但非即時同步" }}
          </div>

          <!-- 協助登入按鈕 -->
          <div v-if="!loginSuccess" class="text-center">
            <button
              class="bg-yellow-500 text-white px-4 py-2 rounded-lg hover:bg-yellow-600"
              @click="showLoginModal = true"
            >
              連線中央點名系統
            </button>
          </div>
        </div>

        <!-- 名單點名（主要功能交給子元件） -->
        <RollcallMainView
          :loginSuccess="loginSuccess"
        />

        <!-- 訊息 -->
        <div v-if="message" class="mt-4 text-center text-sm" :class="messageColor">
          {{ message }}
        </div>

        <!-- 驗證碼登入 Modal -->
        <RollcallLoginView
          v-if="showLoginModal"
          :captchaUrl="captchaUrl"
          :verifyCode="verifyCode"
          :loading="loading"
          :captchaLoading="captchaLoading"
          @update:verifyCode="verifyCode = $event"
          @submitLogin="submitLogin"
          @loadCaptcha="loadCaptcha"
          @close="showLoginModal = false"
        />

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import liff from "@line/liff"
import RollcallLoginView from "./RollcallLoginView.vue"
import RollcallMainView from "./RollcallMainView.vue"

const API_URL = import.meta.env.VITE_ROLLCALL_API_URL || "https://citcnew.org.tw/attendance-helper"
const LIFF_ID = import.meta.env.VITE_ROLLCALL_LIFF_ID

// 狀態
const captchaUrl = ref("")
const picID = ref("")
const verifyCode = ref("")
const loading = ref(false)
const loginSuccess = ref(false)
const message = ref("")
const showLoginModal = ref(false)
const captchaLoading = ref(false)

const messageColor = computed(() =>
  message.value.includes("❌") ? "text-red-600" :
  message.value.includes("⚠️") ? "text-yellow-600" : "text-green-600"
)

// 初始化
onMounted(async () => {
  await liff.init({ liffId: LIFF_ID })
  if (!liff.isLoggedIn()) {
    liff.login()
    return
  }
  checkSession()
})

// 檢查 session 狀態
async function checkSession() {
  try {
    const res = await fetch(`${API_URL}/?path=central-session&ts=${Date.now()}`)
    const data = await res.json()
    loginSuccess.value = data.loggedIn
    message.value = data.loggedIn ? "✅ " + data.message : "⚠️ " + data.message
  } catch (err) {
    loginSuccess.value = false
    message.value = "❌ 檢查登入狀態失敗：" + err.message
  }
}

// 抓驗證碼
async function loadCaptcha() {
  captchaUrl.value = ""
  captchaLoading.value = true
  try {
    const res = await fetch(`${API_URL}/?path=central-verify&ts=${Date.now()}`)
    const data = await res.json()
    captchaUrl.value = data.url
    picID.value = data.picID
  } catch (err) {
    message.value = "❌ 無法載入驗證碼：" + err.message
  } finally {
    captchaLoading.value = false
  }
}

// 登入中央
async function submitLogin() {
  loading.value = true
  message.value = ""
  try {
    const res = await fetch(`${API_URL}/?path=central-login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ verifyCode: verifyCode.value, picID: picID.value })
    })
    const result = await res.json()
    if (result.success || result.status === "success") {
      loginSuccess.value = true
      message.value = "✅ 登入成功，可以同步中央"
      showLoginModal.value = false
    } else {
      loginSuccess.value = false
      message.value = "❌ 登入失敗：" + (result.message || "請檢查驗證碼")
      loadCaptcha()
    }
  } catch (err) {
    loginSuccess.value = false
    message.value = "❌ 連線錯誤：" + err.message
    loadCaptcha()
  } finally {
    loading.value = false
  }
}
</script>
