<!-- src/views/AttendanceView.vue -->
<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100">
    <div class="bg-white rounded-xl shadow-lg p-6 w-80 text-center">
      <h2 class="text-lg font-bold mb-4">台中市召會出勤系統</h2>

      <div v-if="loading" class="text-gray-500">正在取得定位...</div>

      <div v-else>
        <p class="text-sm text-gray-700">目前位置</p>

        <!-- 地圖區塊 -->
        <div class="w-full h-60 mt-2 rounded-lg overflow-hidden shadow">
          <iframe
            v-if="location.lat && location.lng"
            :src="`https://www.google.com/maps?q=${encodeURIComponent(location.lat + ',' + location.lng)}&hl=zh-TW&z=16&output=embed`"
            class="w-full h-full border-0"
            allowfullscreen=""
            loading="lazy"
          ></iframe>
        </div>

        <!-- 打卡按鈕 -->
        <button
          @click="submitAttendance('上班')"
          class="w-full bg-green-500 text-white py-2 px-4 rounded-lg hover:bg-green-600 disabled:bg-gray-300 mt-4 mb-2"
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

  <!-- 打卡結果 Modal -->
  <div
    v-if="showResultModal"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
  >
    <div class="bg-white rounded-xl shadow-lg p-6 w-96 text-center">
      <!-- 標題 -->
      <h3 class="text-lg font-bold mb-4">打卡結果</h3>

      <!-- 框 1：系統提示 -->
      <div class="bg-yellow-50 border border-yellow-400 rounded-lg p-3 mb-4 text-left">
        <p class="text-sm text-gray-800 whitespace-pre-line">
          {{ resultMessage }}
        </p>
      </div>

      <!-- 框 2：轉傳提示 -->
      <div class="bg-gray-50 border border-blue-300 rounded-lg p-3 mb-4 text-left">
        <p class="text-sm font-semibold text-gray-800">
          👉 請複製下方文字並轉傳給所屬主管：
          <span v-for="(sup, i) in supervisors" :key="sup.user_id">
            {{ sup.name }}<span v-if="i < supervisors.length - 1">、</span>
          </span>
        </p>
      </div>

      <!-- 框 3：完整訊息內容 -->
      <div class="bg-gray-50 border border-blue-300 rounded-lg p-3 mb-4 text-left text-sm text-gray-700 break-words">
        <p>弟兄您好，以下是待審核的打卡資料：</p>
        <p>員工：{{ employeeName }}</p>
        <p>打卡時間：{{ attendanceTime }}</p>
        <p>外地打卡原因：{{ attendanceReason }}</p>
        <p class="mt-2 font-semibold">主管審核連結：</p>
        <p>{{ approvalUrl }}</p>
        <p>請您協助審核，謝謝！</p>
      </div>

      <!-- 複製按鈕 -->
      <button
        @click="copyMessage"
        class="w-full bg-yellow-500 text-white py-2 px-4 rounded-lg hover:bg-yellow-600 mb-3 flex items-center justify-center gap-2"
      >
        複製審核文字
      </button>

      <!-- 關閉 -->
      <button
        @click="showResultModal = false"
        class="mt-4 text-sm text-gray-500 underline"
      >
        關閉
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";

const location = ref({ lat: null, lng: null });
const loading = ref(true);
const submittingMode = ref(null);
let liffInstance = null;

// Modal 狀態
const showResultModal = ref(false);
const resultMessage = ref(""); // 框1
const approvalUrl = ref("");   // 框3
const supervisors = ref([]);   // 框2

// 員工資訊
const employeeName = ref("");
const attendanceTime = ref("");
const attendanceReason = ref("");

// 複製的完整文字
const copyText = computed(() => {
  return [
    "弟兄您好，以下是待審核的打卡資料：",
    ``,
    `員工：${employeeName.value}`,
    `打卡時間：${attendanceTime.value}`,
    `外地打卡原因：${attendanceReason.value}`,
    ``,
    `主管審核連結：`,
    approvalUrl.value,
    ``,
    "請您協助審核，謝謝！"
  ].join("\n");
});

// API base
const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";
const LIFF_ID = import.meta.env.VITE_LIFF_ID || "2008097735-moxnzwdM";

// 公司座標 & 半徑（從 .env 讀取，若沒有就用預設值）
const COMPANY_LAT = Number(import.meta.env.VITE_COMPANY_LAT) || 24.13384;
const COMPANY_LNG = Number(import.meta.env.VITE_COMPANY_LNG) || 120.68162;
const ALLOWED_RADIUS = Number(import.meta.env.VITE_ALLOWED_RADIUS) || 200; // 公尺

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
      (pos) => resolve({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
      (err) => {
        if (err.code === 1) reject(new Error("請允許定位權限才能打卡"));
        else reject(new Error("定位失敗，請稍後再試"));
      },
      { enableHighAccuracy: true }
    );
  });
}

// 前端計算距離
function calculateDistance(lat, lng) {
  const R = 6371000;
  const phi1 = (COMPANY_LAT * Math.PI) / 180;
  const phi2 = (lat * Math.PI) / 180;
  const dPhi = ((lat - COMPANY_LAT) * Math.PI) / 180;
  const dLambda = ((lng - COMPANY_LNG) * Math.PI) / 180;

  const a =
    Math.sin(dPhi / 2) ** 2 +
    Math.cos(phi1) * Math.cos(phi2) * Math.sin(dLambda / 2) ** 2;
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

// 複製訊息
function copyMessage() {
  navigator.clipboard.writeText(copyText.value).then(() => {
    alert("✅ 已複製到剪貼簿，請至主管LINE聊天室貼上並送出");
  });
}

// 送出打卡
async function submitAttendance(mode) {
  if (submittingMode.value) return;
  submittingMode.value = mode;
  try {
    const idToken = liff.getDecodedIDToken();
    const distance = calculateDistance(location.value.lat, location.value.lng);

    let reason = null;
    if (distance > ALLOWED_RADIUS) {
      reason = prompt("⚠️ 你不在公司範圍內，請輸入原因：", "外出洽公");
      if (!reason) {
        alert("❌ 未輸入原因，打卡未送出");
        submittingMode.value = null;
        return;
      }
    }

    const payload = {
      userId: idToken.sub,
      mode,
      latitude: location.value.lat,
      longitude: location.value.lng,
      reason: reason,
    };

    const res = await fetch(`${API_BASE}/attendance_api.php`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const text = await res.text();
    let data;
    try {
      data = JSON.parse(text);
    } catch (e) {
      alert("❌ 後端回傳的不是 JSON: " + text);
      return;
    }

    resultMessage.value = data.message || "⚠️ 未知回應";
    approvalUrl.value   = data.approval_url || "";
    supervisors.value   = data.supervisors || [];

    employeeName.value     = data.employee_name || "";
    attendanceTime.value   = data.attendance_time || "";
    attendanceReason.value = data.reason || "";

    showResultModal.value = true;
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
