<template>
  <div
    v-if="visible"
    class="fixed z-50 shadow-xl rounded-lg overflow-hidden bg-black transition-all duration-300"
    @transitionend="handleTransitionEnd"
    :style="{
      width: minimized ? '64px' : `${playerSize.width}px`,
      height: minimized ? '64px' : `${playerSize.height}px`,
      left: `${position.x}px`,
      top: `${position.y}px`,
      borderRadius: minimized ? '9999px' : '0.75rem',
    }"
  >
    <!-- 拖曳區（僅限上方 bar 可拖曳） -->
    <div
      class="absolute top-0 left-0 w-full h-6 cursor-move z-10"
      @mousedown="startDrag"
    ></div>

    <!-- 影片或小球圖示 -->
    <div v-if="!minimized" class="w-full h-full">
      <iframe
        class="w-full h-full"
        :src="embedUrl"
        frameborder="0"
        allow="autoplay; encrypted-media"
        allowfullscreen
      ></iframe>
    </div>
    <div
    v-else
    class="w-full h-full flex items-center justify-center text-white text-2xl bg-gray-800 cursor-pointer"
    @click="restorePlayer"
    >
    ▶
    </div>

    <!-- 控制列 -->
    <div class="absolute top-1 right-1 flex gap-1 z-20" v-if="!minimized">
      <button
        @click.stop="toggleSize"
        class="bg-black/60 text-white text-xs px-2 py-1 rounded hover:bg-black/80"
      >
        {{ isLarge ? '縮小' : '放大' }}
      </button>
        <button
        @click.stop="minimize"
        class="bg-black/60 text-white text-xs px-2 py-1 rounded hover:bg-black/80"
        >
        最小化
        </button>
      <button
        @click.stop="close"
        class="bg-black/60 text-white text-xs px-2 py-1 rounded hover:bg-red-600"
      >
        ✕
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const visible = ref(false)
const embedUrl = ref('')
const isLarge = ref(false)
const minimized = ref(false)

// 播放器尺寸
const playerSize = ref({ width: 320, height: 180 })
const defaultSize = { width: 320, height: 180 }
const largeSize = { width: 640, height: 360 }

const paddingRight = 10
const paddingBottom = 40

// 初始位置在右下角
const position = ref({ x: window.innerWidth - 340, y: window.innerHeight - 220 })

const open = (videoUrl) => {
  const id = getYoutubeId(videoUrl)
  embedUrl.value = `https://www.youtube.com/embed/${id}?autoplay=1`
  visible.value = true
  minimized.value = false
  isLarge.value = false
  playerSize.value = defaultSize
  // 初始化位置
  position.value = {
    x: window.innerWidth - defaultSize.width - paddingRight,
    y: window.innerHeight - defaultSize.height - paddingBottom,
  }
  requestAnimationFrame(() => adjustWithinWindow())
}

const close = () => {
  visible.value = false
  embedUrl.value = ''
}

const toggleSize = () => {
  isLarge.value = !isLarge.value
  playerSize.value = isLarge.value ? getResponsiveSize() : defaultSize

  // ✨ 新增這段：當變為非放大狀態（縮小）後，自動貼角落
  if (!isLarge.value) {
    requestAnimationFrame(() => {
      moveToNearestCorner()
    })
  }

  requestAnimationFrame(() => {
    adjustWithinWindow()
  })
}


const getResponsiveSize = () => {
  const padding = 40
  const maxWidth = window.innerWidth - padding
  const maxHeight = window.innerHeight - padding
  const ratio = 16 / 9

  let width = Math.min(640, maxWidth)
  let height = width / ratio

  if (height > maxHeight) {
    height = maxHeight
    width = height * ratio
  }

  return { width, height }
}

// 擷取 YouTube ID
function getYoutubeId(url) {
  const match = url.match(/[?&]v=([^&]+)/)
  return match ? match[1] : ''
}

// 拖曳邏輯（僅拖 header）
let dragging = false
let offsetX = 0
let offsetY = 0

const startDrag = (e) => {
  dragging = true
  offsetX = e.clientX - position.value.x
  offsetY = e.clientY - position.value.y
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
}

const onDrag = (e) => {
  if (!dragging) return
  const newX = e.clientX - offsetX
  const newY = e.clientY - offsetY
  const maxX = window.innerWidth - playerSize.value.width
  const maxY = window.innerHeight - playerSize.value.height
  position.value.x = Math.min(Math.max(0, newX), maxX)
  position.value.y = Math.min(Math.max(0, newY), maxY)
}

const stopDrag = () => {
  dragging = false
  snapToEdges()
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
}

const snapToEdges = () => {
  const threshold = 20
  const maxX = window.innerWidth - playerSize.value.width - paddingRight
  const maxY = window.innerHeight - playerSize.value.height - paddingBottom

  if (position.value.x < threshold) {
    position.value.x = paddingRight
  } else if (position.value.x > maxX - threshold) {
    position.value.x = maxX
  }

  if (position.value.y < threshold) {
    position.value.y = paddingBottom
  } else if (position.value.y > maxY - threshold) {
    position.value.y = maxY
  }
}


const adjustWithinWindow = () => {
  // 如果放大後超出視窗，拉回來
    const maxX = window.innerWidth - playerSize.value.width - paddingRight
    const maxY = window.innerHeight - playerSize.value.height - paddingBottom

    position.value.x = Math.min(Math.max(paddingRight, position.value.x), maxX)
    position.value.y = Math.min(Math.max(paddingBottom, position.value.y), maxY)
}

const moveToNearestCorner = () => {
  const padding = 20
  const width = playerSize.value.width
  const height = playerSize.value.height

  const corners = [
    { x: paddingRight, y: paddingBottom }, // 左上
    { x: window.innerWidth - width - paddingRight, y: paddingBottom }, // 右上
    { x: paddingRight, y: window.innerHeight - height - paddingBottom }, // 左下
    { x: window.innerWidth - width - paddingRight, y: window.innerHeight - height - paddingBottom }, // 右下
  ]

  let closest = corners[0]
  let minDist = Infinity
  for (const c of corners) {
    const dx = position.value.x - c.x
    const dy = position.value.y - c.y
    const dist = dx * dx + dy * dy
    if (dist < minDist) {
      minDist = dist
      closest = c
    }
  }

  position.value = { ...closest }
}

const minimize = () => {
  minimized.value = true
  playerSize.value = { width: 64, height: 64 }
  requestAnimationFrame(() => {
    moveToNearestCorner()
  })
}

const restorePlayer = () => {
  minimized.value = false
  playerSize.value = isLarge.value ? getResponsiveSize() : defaultSize

  requestAnimationFrame(() => {
    if (isLarge.value) {
      position.value = {
        x: window.innerWidth - playerSize.value.width - paddingRight,
        y: window.innerHeight - playerSize.value.height - paddingBottom,
      }
    } else {
      moveToNearestCorner()
    }
  })
}

const handleTransitionEnd = () => {
  if (!visible.value || minimized.value) return

  const maxX = window.innerWidth - playerSize.value.width - paddingRight
  const maxY = window.innerHeight - playerSize.value.height - paddingBottom

  position.value.x = Math.min(Math.max(paddingRight, position.value.x), maxX)
  position.value.y = Math.min(Math.max(paddingBottom, position.value.y), maxY)
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  stopDrag()
  window.removeEventListener('resize', handleResize)
})

const handleResize = () => {
  // 如果最小化，就移動到最近角落即可
  if (minimized.value) {
    requestAnimationFrame(() => moveToNearestCorner())
    return
  }

  // 如果目前是放大狀態，但螢幕不夠寬，則縮小
  const padding = 40
  const screenWidth = window.innerWidth
  const screenHeight = window.innerHeight

  const newLargeSize = getResponsiveSize()
  const canStayLarge = screenWidth >= newLargeSize.width + paddingRight &&
                       screenHeight >= newLargeSize.height + paddingBottom

  if (!canStayLarge && isLarge.value) {
    isLarge.value = false
    playerSize.value = defaultSize
  }

  // 重新調整播放器大小與位置
  if (isLarge.value) {
    playerSize.value = newLargeSize
  }

  requestAnimationFrame(() => {
    adjustWithinWindow()
  })
}


onBeforeUnmount(() => stopDrag())
defineExpose({ open })
</script>
