<!-- src/views/RollcallLiffView.vue -->
<template>
  <div class="min-h-screen bg-gray-100 pt-20"> <!-- 保留導航列空間 -->
    <div class="min-h-screen bg-gray-100 flex items-center justify-center">
      <div class="bg-white shadow-lg rounded-xl p-6 w-full max-w-sm">
        <h2 class="text-xl font-bold mb-4 text-center">中央點名系統</h2>

        <!-- 驗證碼登入區 -->
        <div v-if="!loginSuccess">
          <div class="mb-4 text-center">
            <img
              v-if="captchaUrl"
              :src="captchaUrl"
              alt="驗證碼"
              class="mx-auto border rounded mb-2"
            />
            <button class="text-sm text-blue-600 underline" @click="loadCaptcha">
              重新取得驗證碼
            </button>
          </div>

          <form @submit.prevent="submitLogin" class="space-y-3">
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
        </div>

        <!-- 名單點名區 -->
        <div v-else>
          <h3 class="text-lg font-bold mb-2">永和小區名單</h3>

          <div v-if="loadingMembers" class="text-gray-500 text-sm">
            名單載入中...
          </div>

          <!-- 卡片樣式 -->
          <div v-else class="grid grid-cols-2 gap-3">
            <div
              v-for="m in members"
              :key="m.member_id"
              class="relative border rounded-lg p-3 shadow-sm flex flex-col items-center cursor-pointer hover:shadow-md transition"
              :class="{ 'bg-green-100 border-green-400': selectedMembers.includes(m) }"
              @click="toggleSelect(m)"
            >
              <!-- 性別標籤 -->
              <span
                class="absolute top-2 right-2 text-xs px-2 py-0.5 rounded-full"
                :class="m.sex === '男'
                  ? 'bg-blue-500 text-white'
                  : 'bg-pink-500 text-white'"
              >
                {{ m.sex }}
              </span>

              <!-- 名字 -->
              <span class="font-medium text-gray-800 mb-2">{{ m.member_name }}</span>

              <!-- 勾選狀態 -->
              <span
                class="text-xs px-2 py-1 rounded-full"
                :class="selectedMembers.includes(m)
                  ? 'bg-green-500 text-white'
                  : 'bg-gray-200 text-gray-600'"
              >
                {{ selectedMembers.includes(m) ? "已選" : "未選" }}
              </span>
            </div>
          </div>

          <h4 class="mt-4 font-bold">已選清單</h4>
          <ul class="text-sm mb-3">
            <li v-for="m in selectedMembers" :key="m.member_id">
              {{ m.member_name }}
            </li>
          </ul>

          <button
            @click="submitRollcall"
            class="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600"
            :disabled="selectedMembers.length === 0 || loading"
          >
            送出點名
          </button>
        </div>

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
    if (data.loggedIn) {
      loginSuccess.value = true
      message.value = "✅ " + data.message
      loadMembers()
    } else {
      message.value = "⚠️ " + data.message
      loadCaptcha()
    }
  } catch (err) {
    message.value = "❌ 檢查登入狀態失敗：" + err.message
    loadCaptcha()
  }
}

// 抓驗證碼
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
    if (result.success || result.status === "success") {
      loginSuccess.value = true
      message.value = "✅ 登入成功，可以開始點名"
      loadMembers()
    } else {
      message.value = "❌ 登入失敗：" + (result.message || "請檢查驗證碼")
    }
  } catch (err) {
    message.value = "❌ 連線錯誤：" + err.message
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
    console.log("中央回傳資料：", data)

    if (Array.isArray(data.members)) {
      members.value = data.members
      message.value = "✅ 名單載入完成"
    } else {
      message.value = "❌ 名單資料格式不正確"
    }
  } catch (err) {
    message.value = "❌ 載入名單錯誤：" + err.message
  } finally {
    loadingMembers.value = false
  }
}

// 送出點名
async function submitRollcall() {
  try {
    const payload = {
      userId: liff.getDecodedIDToken()?.sub || "testUser",
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
    if (result.success) {
      message.value = "✅ 點名成功並同步中央"
    } else if (result.need_captcha) {
      message.value = "⚠️ 點名已記錄，但需要驗證碼才能同步中央"
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
