// src/stores/ui.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUIStore = defineStore('ui', {
    state: () => ({
      isReadingFullscreen: false,
      shouldShowReminderRaw: true
    }),
    getters: {
      shouldShowReminder: (state) =>
        !state.isReadingFullscreen && state.shouldShowReminderRaw
    },
    actions: {
      toggleReminder(val: boolean) {
        this.shouldShowReminderRaw = val
      }
    }
  })
