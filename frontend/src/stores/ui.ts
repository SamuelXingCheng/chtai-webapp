// src/stores/ui.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUIStore = defineStore('ui', {
    state: () => ({
      isReadingFullscreen: false,
      shouldShowReminderRaw: false,
      enableReminder: false, 
    }),
    getters: {
    shouldShowReminder: (state) =>
        state.enableReminder && !state.isReadingFullscreen && state.shouldShowReminderRaw
    },
    actions: {
      toggleReminder(val: boolean) {
        this.shouldShowReminderRaw = val
      }
    }
  })
