import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  base: '/newsite/',
  plugins: [vue()],
  optimizeDeps: {
    include: ['pdfjs-dist/build/pdf.worker.entry'],
  },
})
