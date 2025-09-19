<!-- src/views/Rollcall/components/MemberCard.vue -->
<template>
  <div
    class="relative border rounded-lg p-4 shadow-sm flex flex-col items-center justify-center cursor-pointer hover:shadow-md transition"
    :class="{
      'bg-green-100 border-green-400': selected,
      'bg-gray-100 border-gray-300': !selected
    }"
    @click="$emit('toggle')"
  >
    <!-- 名字 -->
    <span class="font-medium text-gray-800 mb-2">{{ name }}</span>

    <!-- 狀態 -->
    <span
      class="text-xs px-2 py-1 rounded-full"
      :class="selected ? 'bg-green-500 text-white' : 'bg-gray-300 text-gray-600'"
    >
      {{ selected ? "出席" : "未點" }}
    </span>
  </div>
</template>

<script setup>
defineProps({
  name: String,
  selected: Boolean
})
defineEmits(["toggle"])
</script>
