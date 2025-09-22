<!-- src/views/Rollcall/components/MemberCard.vue -->
<template>
  <button
    @click="$emit('toggle')"
    class="w-full h-12 flex items-center justify-center 
           rounded-lg text-sm font-medium transition-colors"
    :class="selected ? 'bg-green-500 text-white' : 'bg-gray-200 text-gray-800'"
  >
    {{ name }}
  </button>
</template>

<script setup>
defineProps({
  name: String,
  selected: Boolean
})
defineEmits(["toggle"])
</script>
