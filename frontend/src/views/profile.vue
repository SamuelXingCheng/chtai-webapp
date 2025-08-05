<!-- src/views/profile.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { getAuth, onAuthStateChanged } from 'firebase/auth'
import { doc, getDoc, setDoc } from 'firebase/firestore'
import { db } from '../firebase'
import { useRouter } from 'vue-router'

const auth = getAuth()
const router = useRouter()

const loading = ref(true)
const success = ref(false)
const agree = ref(false)
const scrolledToBottom = ref(false)
const policyBox = ref(null)

const form = ref({
  name: '',
  gender: '',
  birth: '',
  id_number: '',
  passport_number: '',
  phone: '',
  area: '',
  sub_area: '',
  email: '',
  meeting_place: '',
  baptized: '',
  identity_group: '',
  service_role: '',
  line_id: '',
  emergency_contact: '',
  emergency_phone: ''
})

let currentUser = null

onMounted(() => {
  onAuthStateChanged(auth, async (user) => {
    if (!user) {
      router.push('/')
      return
    }
    currentUser = user
    const docRef = doc(db, 'users', user.uid)
    const snap = await getDoc(docRef)
    if (snap.exists()) {
      form.value = { ...form.value, ...snap.data() }
    }
    loading.value = false
  })
})

function handleScroll() {
  const el = policyBox.value
  if (!el) return
  const isBottom = el.scrollTop + el.clientHeight >= el.scrollHeight - 5
  if (isBottom) scrolledToBottom.value = true
}

const saveProfile = async () => {
  if (!currentUser || !agree.value) return
  await setDoc(doc(db, 'users', currentUser.uid), form.value, { merge: true })
  success.value = true
  setTimeout(() => {
    router.push('/')
  }, 1500)
}
</script>

<template>
  <div class="bg-gray-50 min-h-screen py-12 px-4">
    <div class="max-w-4xl mx-auto bg-white shadow-md rounded-xl p-8 space-y-10">

      <!-- 標題與說明 -->
      <div>
        <h2 class="text-2xl font-bold text-gray-800 mb-1">填寫個人資料</h2>
        <p class="text-gray-500">
          填寫個人資料可啟用「快速報名」等個人化功能。資料將僅用於召會聚會行動相關用途，並遵守隱私權政策予以保護。您可選擇性填寫，惟部分功能可能受限。
        </p>
      </div>

      <!-- 載入中提示 -->
      <div v-if="loading" class="text-center text-gray-500 py-8">載入中...</div>

      <!-- 表單內容 -->
      <form v-else @submit.prevent="saveProfile" class="space-y-12">

        <!-- 區塊：隱私政策與同意 -->
        <section class="space-y-4">
          <h3 class="text-lg font-semibold text-gray-700 border-b pb-1">隱私權政策</h3>
          <div
            ref="policyBox"
            class="border rounded p-4 max-h-48 overflow-y-scroll text-sm bg-gray-50"
            @scroll="handleScroll"
          >
            <p>歡迎您使用「台中市召會網站」（以下簡稱本網站），為保障您的權益及遵守法律規範，特訂定本隱私權政策如下：</p>

            <p>1. 適用範圍與依據</p>
            <p>　本政策適用於使用本網站所有頁面與服務的訪客與會員，依據中華民國《個人資料保護法》。</p>

            <p>2. 蒐集之個人資料類型與方式</p>
            <p>　包含但不限於姓名、性別、身分證字號、出生年月日、護照號碼、聯絡電話、電子郵件、IP 位址、Cookie 等，透過註冊頁面、留言系統、自動追蹤等方式蒐集。</p>

            <p>3. 蒐集目的與合法性基礎</p>
            <p>　用途包括提供召會聚會活動之快速報名、參與聚會之統計分析等；合法性基礎為使用者同意或契約履行。</p>

            <p>4. 資料使用與分享對象</p>
            <p>　可能分享對象：召會聚會舉辦方（專項服事團、行動服事團）或投保之保險公司；分享前將採取匿名化、合約保障等措施。</p>

            <p>5. 儲存期間與地點</p>
            <p>　個人資料最長保留期間為用途所需後 5 年，資料存放於本地／雲端伺服器，並符合法規跨境傳輸標準。</p>

            <p>6. 資料安全措施</p>
            <p>　採用 SSL/TLS 加密、防火牆、資料存取控管、員工教育與定期安全稽核管理。</p>

            <p>7. 使用者權利與行使方式</p>
            <p>　使用者有權查詢、更正、刪除、撤回同意、申請資料可攜性等，請透過 chtai479@ms9.hinet.net 聯絡，本網站將於 30 天內回覆。</p>

            <p>8. 政策更新與公布方式</p>
            <p>　最後更新日期：2025 年 7 月 25 日。本政策將每年檢討更新，重大更改時會通知使用者並重新取得同意。</p>

            <p>9. 聯絡郵件：chtai479@ms9.hinet.net</p>

            <p class="mt-2">當您填寫並提交此資料，即表示您已閱讀並同意我們的隱私權政策。如有任何問題，請與網站管理者聯繫。</p>
            <div class="h-10"></div>
          </div>
          <label class="flex items-start gap-2 text-sm text-gray-600">
            <input type="checkbox" v-model="agree" required />
            <span>請閱讀完整內容，方可勾選同意。</span>
          </label>
        </section>

        <!-- 區塊一：基本資料 -->
        <section class="space-y-4 bg-gray-50 p-6 rounded-lg">
          <h3 class="text-lg font-semibold text-gray-800 border-b pb-1">基本資料（必填）</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block mb-1 font-medium text-gray-700">姓名 *</label>
              <input v-model="form.name" type="text" class="form-input" required />
            </div>
            <div>
              <label class="block mb-1 font-medium text-gray-700">性別</label>
              <select v-model="form.gender" class="form-input">
                <option disabled value="">請選擇</option>
                <option>男</option>
                <option>女</option>
              </select>
            </div>
            <div>
              <label class="block mb-1 font-medium text-gray-700">大區 *</label>
              <input v-model="form.area" type="text" class="form-input" required />
            </div>
            <div>
              <label class="block mb-1 font-medium text-gray-700">小區 *</label>
              <input v-model="form.sub_area" type="text" class="form-input" required />
            </div>
          </div>
        </section>

        <!-- 區塊二：快速報名功能 -->
        <section class="space-y-4 bg-gray-50 p-6 rounded-lg">
          <h3 class="text-lg font-semibold text-gray-800 border-b pb-1">選填資料：（填寫可啟用「快速報名」功能）</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block mb-1 font-medium text-gray-700">出生年月日</label>
              <input v-model="form.birth" type="date" class="form-input" />
            </div>
            <div>
              <label class="block mb-1 font-medium text-gray-700">身分證字號（台灣）</label>
              <input v-model="form.id_number" type="text" class="form-input" />
            </div>
            <div>
              <label class="block mb-1 font-medium text-gray-700">護照號碼（外籍）</label>
              <input v-model="form.passport_number" type="text" class="form-input" />
            </div>
            <div>
              <label class="block mb-1 font-medium text-gray-700">聯絡電話</label>
              <input v-model="form.phone" type="tel" class="form-input" />
            </div>
            <div>
              <label class="block mb-1 font-medium text-gray-700">電子郵件</label>
              <input v-model="form.email" type="email" class="form-input" />
            </div>
            <div>
              <label class="block mb-1 font-medium text-gray-700">是否已受浸</label>
                <select v-model="form.baptized" class="form-input">
                  <option disabled value="">請選擇</option>
                  <option>是</option>
                  <option>否</option>
                </select>
            </div>
            <!-- 就讀學校 -->
            <div>
              <label class="block mb-1 font-medium text-gray-700">就讀學校</label>
              <input
                v-model="form.school"
                type="text"
                class="w-full border rounded-md px-3 py-2 text-sm shadow-sm focus:ring focus:ring-blue-100"
                placeholder="例：中興"
              />
            </div>

            <!-- 系級 -->
            <div>
              <label class="block mb-1 font-medium text-gray-700">系級</label>
              <input
                v-model="form.department"
                type="text"
                class="w-full border rounded-md px-3 py-2 text-sm shadow-sm focus:ring focus:ring-blue-100"
                placeholder="例：應數三"
              />
            </div>
          </div>
        </section>

        <!-- 區塊三：擴充功能與個人化設定
        <section class="space-y-4 bg-gray-50 p-6 rounded-lg">
          <h3 class="text-lg font-semibold text-gray-800 border-b pb-1">🔧 第三區塊：擴充功能與個人化設定（選填）</h3>
          <p class="text-sm text-gray-500">供後續開發更多功能。</p>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block mb-1 font-medium text-gray-700">所屬會所 / 聚會地點</label>
              <input v-model="form.meeting_place" type="text" class="form-input" />
            </div>
            <div>
              <label class="block mb-1 font-medium text-gray-700">是否已受浸</label>
              <select v-model="form.baptized" class="form-input">
                <option disabled value="">請選擇</option>
                <option>是</option>
                <option>否</option>
              </select>
            </div>
            
            <div>
              <label class="block mb-1 font-medium text-gray-700">LINE ID</label>
              <input v-model="form.line_id" type="text" class="form-input" />
            </div>
            
          </div>
        </section> -->

        <!-- 儲存按鈕 -->
        <div>
          <button
            type="submit"
            :disabled="!agree"
            class="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
          >
            儲存資料
          </button>
          <p v-if="success" class="text-emerald-600 text-center mt-4">
            資料已成功儲存，將返回首頁...
          </p>
        </div>

      </form>
    </div>
  </div>
</template>

<style scoped>
.form-input {
  @apply w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring focus:border-blue-400 bg-white text-gray-800;
}
</style>
