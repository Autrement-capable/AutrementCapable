import { ref, onMounted, onUnmounted } from 'vue'

export function useGameTimer() {
  const showGameModal = ref(false)
  const timeRemaining = ref(10)
  const timer = ref(null)

  const gameRoutes = [
    '/roue-des-competences',
    '/scenarios',
    '/environment',
    '/metiers',
    '/shape-sequence-game',
    '/game-speed',
  ]

  const startTimer = () => {
    timer.value = setInterval(() => {
      timeRemaining.value--

      if (timeRemaining.value <= 0) {
        clearInterval(timer.value)
        showGameModal.value = true
      }
    }, 1000)
  }

  const stopTimer = () => {
    if (timer.value) {
      clearInterval(timer.value)
      timer.value = null
    }
  }

  const resetTimer = () => {
    stopTimer()
    timeRemaining.value = 10
    showGameModal.value = false
  }

  const getRandomGameRoute = () => {
    const randomIndex = Math.floor(Math.random() * gameRoutes.length)
    return gameRoutes[randomIndex]
  }

  const closeModal = () => {
    showGameModal.value = false
    // Redémarrer le timer pour 10 secondes supplémentaires
    resetTimer()
    startTimer()
  }

  // Démarrer automatiquement le timer quand le composable est utilisé
  onMounted(() => {
    startTimer()
  })

  // Nettoyer le timer quand le composant est démonté
  onUnmounted(() => {
    stopTimer()
  })

  return {
    showGameModal,
    timeRemaining,
    startTimer,
    stopTimer,
    resetTimer,
    getRandomGameRoute,
    closeModal,
  }
}
