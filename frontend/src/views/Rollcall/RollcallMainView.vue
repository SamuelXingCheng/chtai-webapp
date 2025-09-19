<!-- src/views/Rollcall/RollcallMainView.vue -->
<template>
  <div>
    <h3 class="text-lg font-bold mb-2">永和小區名單</h3>

    <div v-if="loadingMembers" class="text-gray-500 text-sm">
      名單載入中...
    </div>

    <div v-else class="grid grid-cols-2 gap-3">
      <div
        v-for="m in members"
        :key="m.member_id"
        class="relative border rounded-lg p-3 shadow-sm flex flex-col items-center cursor-pointer hover:shadow-md transition"
        :class="{ 'bg-green-100 border-green-400': selectedMembers.includes(m) }"
        @click="$emit('toggleSelect', m)"
      >
        <span
          class="absolute top-2 right-2 text-xs px-2 py-0.5 rounded-full"
          :class="m.sex === '男' ? 'bg-blue-500 text-white' : 'bg-pink-500 text-white'"
        >
          {{ m.sex }}
        </span>

        <span class="font-medium text-gray-800 mb-2">{{ m.member_name }}</span>

        <span
          class="text-xs px-2 py-1 rounded-full"
          :class="selectedMembers.includes(m) ? 'bg-green-500 text-white' : 'bg-gray-200 text-gray-600'"
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
      @click="$emit('submitRollcall')"
      class="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600"
      :disabled="selectedMembers.length === 0 || loading"
    >
      送出點名
    </button>
  </div>
</template>

<script setup>
defineProps({
  members: Array,
  selectedMembers: Array,
  loading: Boolean,
  loadingMembers: Boolean
})
defineEmits(["submitRollcall", "toggleSelect"])
</script>
