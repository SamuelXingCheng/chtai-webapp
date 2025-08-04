<!-- components/SearchWeekSelector.vue -->
<script setup lang="ts">
import { ref, computed, defineProps, defineEmits } from 'vue'
import {
  Combobox,
  ComboboxInput,
  ComboboxOptions,
  ComboboxOption
} from '@headlessui/vue'
const props = defineProps({
  messages: {
    type: Array,
    required: true
  }
})

console.log('props.messages:', props.messages)

const emit = defineEmits(['select'])

const query = ref('')
const selected = ref(null)

const filteredMessages = computed(() => {
  if (!query.value) return props.messages
  return props.messages.filter((msg: any) =>
    msg.title.toLowerCase().includes(query.value.toLowerCase()) ||
    msg.htmlContent.toLowerCase().includes(query.value.toLowerCase())
  )
})

function handleSelect(msg: any) {
  selected.value = msg
  emit('select', msg)
}



</script>

<template>
  <div class="w-full">
    <Combobox v-model="selected" @update:modelValue="handleSelect">
      <div class="relative">
        <ComboboxInput
          v-model="query"
          class="w-full border border-gray-300 rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="🔍 搜尋週訊標題或內文關鍵字..."
        />
        <ComboboxOptions
          class="absolute z-50 left-0 mt-2 w-full bg-white border rounded-md shadow-lg max-h-60 overflow-y-auto"
        >
          <template v-if="filteredMessages.length > 0">
            <ComboboxOption
              v-for="msg in filteredMessages"
              :key="msg.id"
              :value="msg"
              class="px-4 py-2 hover:bg-blue-100 cursor-pointer"
            >
              <div class="font-medium">{{ msg.title }}</div>
              <div class="text-sm text-gray-500 truncate">
                {{ msg.htmlContent.slice(0, 50) }}...
              </div>
            </ComboboxOption>
          </template>
          <template v-else>
            <div class="px-4 py-2 text-gray-500">找不到相關週訊</div>
          </template>
        </ComboboxOptions>
      </div>
    </Combobox>
  </div>
</template>
