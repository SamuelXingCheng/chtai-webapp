<!-- src/views/Rollcall/RollcallLiffView.vue -->
<template>
  <div class="min-h-screen bg-gray-100 pt-20">
    <div class="min-h-screen bg-gray-100 flex items-center justify-center">
      <div class="bg-white shadow-lg rounded-xl p-6 w-full max-w-sm">
        <h2 class="text-xl font-bold mb-4 text-center">中央點名系統</h2>

        <!-- 驗證碼登入 -->
        <RollcallLoginView
          v-if="!loginSuccess"
          :captchaUrl="captchaUrl"
          :verifyCode="verifyCode"
          :loading="loading"
          @update:verifyCode="verifyCode = $event"
          @submitLogin="submitLogin"
          @loadCaptcha="loadCaptcha"
        />

        <!-- 名單點名 -->
        <RollcallMainView
          v-else
          :members="members"
          :selectedMembers="selectedMembers"
          :loading="loading"
          :loadingMembers="loadingMembers"
          @submitRollcall="submitRollcall"
          @toggleSelect="toggleSelect"
        />

        <!-- 訊息 -->
        <div v-if="message" class="mt-4 text-center text-sm" :class="messageColor">
          {{ message }}
        </div>
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
const members = ref([])
const selectedMembers = ref([])
const loadingMembers = ref(false)

const messageColor = computed(() =>
  loginSuccess.value ? "text-green-600" : "text-red-600"
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
    console.log("checkSession 回傳：", data)

    if (data.loggedIn) {
      loginSuccess.value = true
      message.value = "✅ " + data.message
      loadMembers()
    } else {
      loginSuccess.value = false   // 🔑 確保切回登入頁
      message.value = "⚠️ " + data.message
      loadCaptcha()
    }
  } catch (err) {
    loginSuccess.value = false     // 🔑 發生錯誤也要回登入頁
    message.value = "❌ 檢查登入狀態失敗：" + err.message
    loadCaptcha()
  }
}

// 抓驗證碼
async function loadCaptcha() {
  captchaUrl.value = "" // 🔑 先清空，避免閃舊圖
  try {
    const res = await fetch(`${API_URL}/?path=central-verify&ts=${Date.now()}`)
    const data = await res.json()
    captchaUrl.value = data.url
    picID.value = data.picID
    console.log("驗證碼網址：", captchaUrl.value)
  } catch (err) {
    message.value = "❌ 無法載入驗證碼：" + err.message
  }
}

// 登入
async function submitLogin() {
  loading.value = true
  message.value = ""
  loginSuccess.value = false
  try {
    const res = await fetch(`${API_URL}/?path=central-login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ verifyCode: verifyCode.value, picID: picID.value })
    })
    const result = await res.json()
    console.log("submitLogin 回傳：", result)

    if (result.success || result.status === "success") {
      loginSuccess.value = true
      message.value = "✅ 登入成功，可以開始點名"
      loadMembers()
    } else {
      loginSuccess.value = false   // 🔑 登入失敗 → 回登入頁
      message.value = "❌ 登入失敗：" + (result.message || "請檢查驗證碼")
      loadCaptcha()
    }
  } catch (err) {
    loginSuccess.value = false     // 🔑 連線錯誤也回登入頁
    message.value = "❌ 連線錯誤：" + err.message
    loadCaptcha()
  } finally {
    loading.value = false
  }
}

// 拉名單
async function loadMembers() {
  loadingMembers.value = true
  try {
    const res = await fetch(`${API_URL}/?path=central-members&district=永和`)
    const data = await res.json()
    console.log("loadMembers 回傳：", data)

    if (Array.isArray(data.members)) {
      members.value = data.members
      message.value = "✅ 名單載入完成"
    } else {
      loginSuccess.value = false   // 🔑 異常 → 回登入頁
      message.value = "❌ 名單資料格式不正確"
      loadCaptcha()
    }
  } catch (err) {
    loginSuccess.value = false     // 🔑 發生錯誤 → 回登入頁
    message.value = "❌ 載入名單錯誤：" + err.message
    loadCaptcha()
  } finally {
    loadingMembers.value = false
  }
}

// 送出點名
async function submitRollcall() {
  try {
    const payload = {
      userId: liff.getDecodedIDToken()?.sub || "testUser", // 🔑 修正拼字
      groupId: "永和",
      members: selectedMembers.value.map(m => ({
        memberId: m.member_id,
        status: "出席"
      }))
    }

    const res = await fetch(`${API_URL}/?path=rollcall-submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
    const result = await res.json()
    console.log("submitRollcall 回傳：", result)

    if (result.success) {
      message.value = "✅ 點名成功並同步中央"
    } else if (result.need_captcha) {
      loginSuccess.value = false   // 🔑 如果需要驗證碼，回登入頁
      message.value = "⚠️ 點名已記錄，但需要驗證碼才能同步中央"
      loadCaptcha()
    } else {
      message.value = "❌ 點名失敗：" + (result.message || "")
    }
  } catch (err) {
    message.value = "❌ 點名錯誤：" + err.message
  }
}

// 點擊卡片切換選取
function toggleSelect(m) {
  const idx = selectedMembers.value.findIndex(sel => sel.member_id === m.member_id)
  if (idx >= 0) {
    selectedMembers.value.splice(idx, 1)
  } else {
    selectedMembers.value.push(m)
  }
}
</script>
