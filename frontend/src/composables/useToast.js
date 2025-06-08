import { ref, onUnmounted } from 'vue'

const toasts = ref([])
const toastIdCounter = ref(0)

export function useToast() {
  const addToast = ({ severity = 'info', summary = '', detail = '', life = 3000 }) => {
    const id = ++toastIdCounter.value
    const toast = {
      id,
      severity: normalizeSeverity(severity),
      summary,
      detail,
      life,
      progress: 100,
    }

    toasts.value.push(toast)

    const startTime = Date.now()
    const interval = setInterval(() => {
      const elapsed = Date.now() - startTime
      toast.progress = Math.max(0, 100 - (elapsed / life) * 100)
      if (elapsed >= life) {
        clearInterval(interval)
        removeToast(id)
      }
    }, 16)

    setTimeout(() => {
      removeToast(id)
      clearInterval(interval)
    }, life)

    return id
  }

  const removeToast = (id) => {
    const index = toasts.value.findIndex((toast) => toast.id === id)
    if (index !== -1) {
      toasts.value.splice(index, 1)
    }
  }

  const normalizeSeverity = (severity) => {
    const validSeverities = ['success', 'info', 'warn', 'error']
    return validSeverities.includes(severity) ? severity : 'info'
  }

  onUnmounted(() => {
    toasts.value = []
  })

  return {
    toasts,
    addToast,
    removeToast,
  }
}