<!-- src/views/AttendanceView.vue -->
<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100">
    <div class="bg-white rounded-xl shadow-lg p-6 w-80 text-center">
      <h2 class="text-lg font-bold mb-4">台中市召會出勤系統</h2>

      <div v-if="loading" class="text-gray-500">正在取得定位...</div>

      <div v-else>
        <p class="text-sm text-gray-700 mb-2">目前座標：</p>
        <p class="text-xs text-gray-600 mb-4">
          Lat: {{ location.lat }} <br />
          Lng: {{ location.lng }}
        </p>

        <button
          @click="submitAttendance('上班')"
          class="w-full bg-green-500 text-white py-2 px-4 rounded-lg hover:bg-green-600 disabled:bg-gray-300 mb-2"
          :disabled="submittingMode === '上班'"
        >
          {{ submittingMode === '上班' ? "送出中..." : "上班打卡" }}
        </button>

        <button
          @click="submitAttendance('下班')"
          class="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 disabled:bg-gray-300"
          :disabled="submittingMode === '下班'"
        >
          {{ submittingMode === '下班' ? "送出中..." : "下班打卡" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const location = ref({ lat: null, lng: null });
const loading = ref(true);
const submittingMode = ref(null); // "上班" or "下班"
let liffInstance = null;

// API base 取自環境變數
const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";
const LIFF_ID = import.meta.env.VITE_LIFF_ID || "2008053226-j5P2ex8l";

// 初始化 LIFF
async function initLiff() {
  const liff = (await import("@line/liff")).default;
  await liff.init({ liffId: LIFF_ID });
  if (!liff.isLoggedIn()) {
    liff.login();
  }
  return liff;
}

// 取得座標
function getLocation() {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error("瀏覽器不支援定位"));
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        resolve({ lat: pos.coords.latitude, lng: pos.coords.longitude });
      },
      (err) => {
        if (err.code === 1) reject(new Error("請允許定位權限才能打卡"));
        else reject(new Error("定位失敗，請稍後再試"));
      },
      { enableHighAccuracy: true }
    );
  });
}

// 送出打卡
async function submitAttendance(mode) {
  submittingMode.value = mode;
  try {
    const profile = await liffInstance.getProfile();

    const payload = {
      userId: profile.userId,
      mode, // 上班 or 下班
      latitude: location.value.lat,
      longitude: location.value.lng,
    };

    console.log("📡 API URL:", `${API_BASE}/attendance_api.php`);
    console.log("📦 Payload:", payload);

    const res = await fetch(`${API_BASE}/attendance_api.php`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    // 先抓 raw response
    const text = await res.text();
    console.log("🔎 Raw response:", text);

    // 嘗試轉成 JSON
    let data;
    try {
      data = JSON.parse(text);
    } catch (e) {
      alert("❌ 後端回傳的不是 JSON: " + text);
      return;
    }

    alert(data.message || "⚠️ 未知回應");
    if (data.status === "success") {
      liffInstance.closeWindow();
    }
  } catch (err) {
    alert("❌ 打卡失敗: " + err.message);
  } finally {
    submittingMode.value = null;
  }
}


// 頁面載入時
onMounted(async () => {
  try {
    liffInstance = await initLiff();
    location.value = await getLocation();
  } catch (err) {
    alert("⚠️ 初始化失敗: " + err.message);
  } finally {
    loading.value = false;
  }
});
</script>
