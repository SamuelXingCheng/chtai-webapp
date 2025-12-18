<!-- src/views/AttendanceView.vue -->
<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100">
    <div class="bg-white rounded-xl shadow-lg p-6 w-80 text-center">
      <h2 class="text-lg font-bold mb-4">台中市召會出勤系統</h2>

      <div v-if="qrTokenFromUrl" class="mb-4 p-2 bg-blue-50 border border-blue-200 rounded-lg text-xs text-blue-600">
        已偵測到辦公室 QR Code，將優先進行掃碼打卡
      </div>

      <div v-if="loading" class="text-gray-500">正在取得定位...</div>

      <div v-else>
        <p class="text-sm text-gray-700">目前位置</p>

        <div class="w-full h-60 mt-2 rounded-lg overflow-hidden shadow">
          <iframe
            v-if="location.lat && location.lng"
            :src="`https://www.google.com/maps?q=${location.lat},${location.lng}&hl=zh-TW&z=16&output=embed`"
            class="w-full h-full border-0"
            allowfullscreen=""
            loading="lazy"
          ></iframe>
        </div>

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

  <div v-if="showResultModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-xl shadow-lg p-6 w-96 text-center">
      <h3 class="text-lg font-bold mb-4">打卡結果</h3>
      <div :class="['rounded-lg p-3 mb-4 text-left', modalTitle === '⚠️ 待主管審核' ? 'bg-yellow-50 border border-yellow-400' : 'bg-green-50 border border-green-400']">
        <p class="text-sm text-gray-800 whitespace-pre-line">{{ resultMessage }}</p>
      </div>
      <template v-if="modalTitle === '⚠️ 待主管審核'">
        <div class="bg-gray-50 border border-blue-300 rounded-lg p-3 mb-4 text-left">
          <p class="text-sm font-semibold text-gray-800">
            👉 請複製下方文字並轉傳給主管：
            <span v-for="(sup, i) in supervisors" :key="sup.user_id">
              {{ sup.name }}<span v-if="i < supervisors.length - 1">、</span>
            </span>
          </p>
        </div>
        <div class="bg-gray-50 border border-blue-300 rounded-lg p-3 mb-4 text-left text-sm text-gray-700 break-words">
          <p>弟兄您好，以下是待審核的打卡資料：</p>
          <p>員工：{{ employeeName }}</p>
          <p>打卡時間：{{ attendanceTime }}</p>
          <p>外地打卡原因：{{ attendanceReason }}</p>
          <p>打卡地圖：{{ mapUrl }}</p>
          <p class="mt-2 font-semibold">主管審核連結：</p>
          <p>{{ approvalUrl }}</p>
          <p>請您協助審核，謝謝！</p>
        </div>
        <button @click="copyMessage" class="w-full bg-yellow-500 text-white py-2 px-4 rounded-lg hover:bg-yellow-600 mb-3 flex items-center justify-center gap-2">
          複製審核文字
        </button>
      </template>
      <button @click="showResultModal = false" class="mt-4 text-sm text-gray-500 underline">關閉</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";

const location = ref({ lat: null, lng: null });
const loading = ref(true);
const submittingMode = ref(null);
const qrTokenFromUrl = ref(null); // ✨ 新增：QR Token

// Modal 狀態
const showResultModal = ref(false);
const resultMessage = ref("");
const approvalUrl = ref("");
const supervisors = ref([]);
const modalTitle = ref("");

// 員工資訊
const employeeName = ref("");
const attendanceTime = ref("");
const attendanceReason = ref("");
const mapUrl = ref("");

// API 設定
const API_BASE = import.meta.env.VITE_API_URL || "https://citcnew.org.tw/attendance-helper"; 
const LIFF_ID = "2008097735-moxnzwdM";

// ✨ 多據點設定
const LOCATIONS = [
  { lat: Number(import.meta.env.VITE_COMPANY_LAT) || 24.13384, lng: Number(import.meta.env.VITE_COMPANY_LNG) || 120.68162 },
  { lat: Number(import.meta.env.VITE_COMPANY_LAT_2) || 24.188632, lng: Number(import.meta.env.VITE_COMPANY_LNG_2) || 120.607218 }
];
const ALLOWED_RADIUS = Number(import.meta.env.VITE_ALLOWED_RADIUS) || 100;

// 計算最短距離
function getMinDistance(lat, lng) {
  let min = Infinity;
  LOCATIONS.forEach(loc => {
    const d = calculateDistance(lat, lng, loc.lat, loc.lng);
    if (d < min) min = d;
  });
  return min;
}

function calculateDistance(lat1, lng1, lat2, lng2) {
  const R = 6371000;
  const phi1 = (lat1 * Math.PI) / 180;
  const phi2 = (lat2 * Math.PI) / 180;
  const dPhi = ((lat2 - lat1) * Math.PI) / 180;
  const dLambda = ((lng2 - lng1) * Math.PI) / 180;
  const a = Math.sin(dPhi / 2) ** 2 + Math.cos(phi1) * Math.cos(phi2) * Math.sin(dLambda / 2) ** 2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

// 複製與初始化 (略) ...
async function initLiff() {
  const liff = (await import("@line/liff")).default;
  await liff.init({ liffId: LIFF_ID });
  if (!liff.isLoggedIn()) liff.login();
  return liff;
}

function getLocation() {
  return new Promise((resolve, reject) => {
    navigator.geolocation.getCurrentPosition(
      (pos) => resolve({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
      (err) => reject(new Error("定位失敗，請確認已開啟 GPS 與權限")),
      { enableHighAccuracy: true }
    );
  });
}

function copyMessage() {
  const text = `弟兄您好，以下是待審核的打卡資料：\n\n員工：${employeeName.value}\n時間：${attendanceTime.value}\n原因：${attendanceReason.value}\n地圖：${mapUrl.value}\n\n審核連結：${approvalUrl.value}`;
  navigator.clipboard.writeText(text).then(() => alert("✅ 已複製文字"));
}

// ✨ 送出打卡邏輯修改
async function submitAttendance(mode) {
  if (submittingMode.value) return;
  submittingMode.value = mode;

  try {
    const liff = (await import("@line/liff")).default;
    const profile = await liff.getProfile();
    const minDistance = getMinDistance(location.value.lat, location.value.lng);

    let reason = null;
    // 如果沒有 QR Token 且超過距離，才需要詢問原因
    if (!qrTokenFromUrl.value && minDistance > ALLOWED_RADIUS) {
      reason = prompt("⚠️ 您不在辦公區域範圍內，請輸入原因：", "外出洽公");
      if (!reason) {
        submittingMode.value = null;
        return;
      }
    }

    const payload = {
      userId: profile.userId,
      mode,
      latitude: location.value.lat,
      longitude: location.value.lng,
      reason: reason,
      qr_token: qrTokenFromUrl.value // ✨ 傳送 Token 給後端
    };

    const res = await fetch(`${API_BASE}/attendance_api.php`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();
    resultMessage.value = data.message;
    approvalUrl.value = data.approval_url || "";
    supervisors.value = data.supervisors || [];
    employeeName.value = data.employee_name || "";
    attendanceTime.value = data.attendance_time || "";
    attendanceReason.value = data.reason || (qrTokenFromUrl.value ? "辦公室 QR 掃描" : "");
    mapUrl.value = data.map_url || "";

    modalTitle.value = (data.approval_status === 'pending') ? "⚠️ 待主管審核" : "✅ 打卡成功";
    showResultModal.value = true;
  } catch (err) {
    alert("❌ 錯誤: " + err.message);
  } finally {
    submittingMode.value = null;
  }
}

onMounted(async () => {
  try {
    // ✨ 抓取網址中的 qr_token
    const urlParams = new URLSearchParams(window.location.search);
    qrTokenFromUrl.value = urlParams.get('qr_token');

    await initLiff();
    location.value = await getLocation();
  } catch (err) {
    alert("初始化失敗: " + err.message);
  } finally {
    loading.value = false;
  }
});
</script>