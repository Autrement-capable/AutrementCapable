import { ref } from 'vue'

// Classe utilitaire
export const BackgroundManager = {
  getCurrentTheme() {
    return localStorage.getItem('dashboard-theme') || 'cosmic'
  },

  setCurrentTheme(theme) {
    localStorage.setItem('dashboard-theme', theme)
    return theme
  },

  areAnimationsEnabled() {
    const storedValue = localStorage.getItem('dashboard-animations')
    // Si aucune valeur n'est stockée, on retourne true par défaut
    return storedValue === null ? true : storedValue === 'true'
  },

  setAnimationsEnabled(enabled) {
    localStorage.setItem('dashboard-animations', enabled.toString())
    return enabled
  },

  toggleAnimations() {
    const current = this.areAnimationsEnabled()
    return this.setAnimationsEnabled(!current)
  },
}

// Composition function pour Vue 3
export function useBackground() {
  const currentTheme = ref(BackgroundManager.getCurrentTheme())
  const animationsEnabled = ref(BackgroundManager.areAnimationsEnabled())

  const changeTheme = (theme) => {
    currentTheme.value = BackgroundManager.setCurrentTheme(theme)
  }

  const toggleAnimations = () => {
    animationsEnabled.value = BackgroundManager.toggleAnimations()
  }

  const setAnimationsEnabled = (enabled) => {
    animationsEnabled.value = BackgroundManager.setAnimationsEnabled(enabled)
  }

  return {
    currentTheme,
    animationsEnabled,
    changeTheme,
    toggleAnimations,
    setAnimationsEnabled,
  }
}
