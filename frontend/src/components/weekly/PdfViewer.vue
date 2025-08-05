<!-- src/components/weekly/PdfViewer.vue -->
<template>
  <canvas ref="canvas" class="w-full border" />
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import * as pdfjsLib from 'pdfjs-dist/build/pdf'

// ✅ 使用 CDN 的 worker（避免打包錯誤）
pdfjsLib.GlobalWorkerOptions.workerSrc =
  'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js'

const props = defineProps<{ url: string }>()
const canvas = ref<HTMLCanvasElement | null>(null)

onMounted(() => {
  watch(
    () => props.url,
    () => {
      render()
    },
    { immediate: true }
  )
})

async function render() {
  console.log('[PDFViewer] render start')
  console.log('canvas.value:', canvas.value)
  console.log('props.url:', props.url)

  if (!canvas.value || !props.url) {
    console.warn('⛔️ Canvas 或 URL 尚未就緒，略過 render()')
    return
  }

  try {
    const loadingTask = pdfjsLib.getDocument(props.url)
    const pdf = await loadingTask.promise
    const page = await pdf.getPage(1)
    const ctx = canvas.value.getContext('2d')!
    const viewport = page.getViewport({ scale: 1.5 })

    canvas.value.height = viewport.height
    canvas.value.width = viewport.width

    await page.render({
      canvasContext: ctx,
      viewport,
    }).promise
  } catch (err: any) {
    console.error('❌ 載入 PDF 失敗：', err.message, err)
  }
}
</script>
