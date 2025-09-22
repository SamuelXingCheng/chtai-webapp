const API_URL =
  import.meta.env.VITE_ROLLCALL_API_URL || "https://citcnew.org.tw/attendance-helper"


// 抓名單（改成打本地 local_members.php）
export async function fetchMembers(meeting, date) {
  const res = await fetch(
    `${API_URL}/src/routes/local_members.php?district=永和&item_id=${meeting}&date=${date}`
  )
  const data = await res.json()
  if (!Array.isArray(data.members)) {
    throw new Error("名單格式錯誤")
  }
  return data.members
}

// 🚫 舊的：直接打中央，不建議前端再用（直接呼叫 central_attendance.php）
export async function submitRollcall({ district, meeting_type, member_ids, attend = 1, date }) {
  const formData = new FormData()
  formData.append("district", district)          // 小區
  formData.append("meeting_type", meeting_type)  // 聚會類型代碼 (例: 37 主日)
  formData.append("attend", attend)              // 1 出席, 0 缺席, "" 取消
  formData.append("date", date)                  // YYYY-MM-DD

  member_ids.forEach(id => formData.append("member_ids[]", id))

  const res = await fetch(`${API_URL}/src/routes/central_attendance.php`, {
    method: "POST",
    body: formData
  })

  return res.json()
}

// ✅ 呼叫本地 attendance_submit.php
export async function submitAttendance({ district, meeting_type, member_ids, attend = 1, date }) {
  const formData = new FormData()
  formData.append("district", district)
  formData.append("meeting_type", meeting_type)
  formData.append("attend", attend)
  formData.append("date", date)
  member_ids.forEach(id => formData.append("member_ids[]", id))

  const res = await fetch(`${API_URL}/src/routes/attendance_submit.php`, {
    method: "POST",
    body: formData
  })
  return res.json()
}