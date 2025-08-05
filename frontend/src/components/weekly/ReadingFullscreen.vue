<!-- components/weekly/ReadingFullscreen.vue -->
<template>
  <Transition name="fade">
    <div
      v-if="visible"
      class="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm text-white overflow-auto"
      @keydown.esc="closeOnEscape"
      tabindex="0"
    >
      <div
        class="min-h-screen flex flex-col items-center justify-center px-6 py-10"
        @click.self="emitClose"
      >
        <div
          class="prose prose-invert prose-lg max-w-3xl w-full bg-[#262626] text-[#eaeaea] rounded-2xl p-8 shadow-lg"
          :style="{ fontSize: fontSize + 'px' }"
          v-html="content"
        />
        <button
          @click="emitClose"
          class="mt-6 text-sm text-white px-4 py-2 border rounded hover:bg-white hover:text-black transition"
        >
          ✕ 離開沉浸模式
        </button>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, watch } from 'vue'
import { useUIStore } from '../../stores/ui'

const ui = useUIStore()

const props = defineProps<{
  visible: boolean
  content: string
  fontSize: number
}>()

const emit = defineEmits(['close'])

function emitClose() {
  emit('close')
}

function closeOnEscape(event: KeyboardEvent) {
  if (event.key === 'Escape') emitClose()
}

onMounted(() => {
  window.addEventListener('keydown', closeOnEscape)
})
onBeforeUnmount(() => {
  window.removeEventListener('keydown', closeOnEscape)
})

watch(
  () => props.visible,
  (val) => {
    ui.isReadingFullscreen = val
  },
  { immediate: true }
)

</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
