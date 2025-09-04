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
          @click="submitAttendance"
          class="w-full bg-green-500 text-white py-2 px-4 rounded-lg hover:bg-green-600 disabled:bg-gray-300"
          :disabled="submitting"
        >
          {{ submitting ? "送出中..." : "送出打卡" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

// 狀態
const location = ref({ lat: null, lng: null });
const loading = ref(true);
const submitting = ref(false);

// 初始化 LIFF
const LIFF_ID = "2008053226-j5P2ex8l";

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
        resolve({
          lat: pos.coords.latitude,
          lng: pos.coords.longitude,
        });
      },
      (err) => reject(err),
      { enableHighAccuracy: true }
    );
  });
}

// 送出打卡
async function submitAttendance() {
  submitting.value = true;
  try {
    const liff = await initLiff();
    const profile = await liff.getProfile();

    const payload = {
      userId: profile.userId,
      latitude: location.value.lat,
      longitude: location.value.lng,
      timestamp: new Date().toISOString(),
    };

    await fetch("http://localhost:8000/api/attendance", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    alert("✅ 打卡成功！");
    liff.closeWindow();
  } catch (err) {
    alert("❌ 打卡失敗: " + err.message);
  } finally {
    submitting.value = false;
  }
}

// 頁面載入時就抓定位
onMounted(async () => {
  try {
    location.value = await getLocation();
  } catch (err) {
    alert("⚠️ 定位失敗: " + err.message);
  } finally {
    loading.value = false;
  }
});
</script>

<style>
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Helvetica, Arial, sans-serif;
}
</style>
