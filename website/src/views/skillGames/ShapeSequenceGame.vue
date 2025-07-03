<template>
  <PopUp
    v-if="showGameModal"
    message="Souhaites-tu continuer à jouer ?"
    :image="flamouImage"
    :redirect="getRandomGameRoute()"
    buttonConfirm="Changer de jeux"
    buttonCancel="Rester ici"
    :visible="showGameModal"
    @close="closeModal"
  />
  <div class="shape-game-container">
    <!-- Animation de déblocage du badge -->
    <div v-if="showBadgeUnlockAnimation" class="badge-unlock-overlay">
      <div class="badge-unlock-animation">
        <div class="badge-icon">🔷</div>
        <h2>Badge débloqué !</h2>
        <h3>{{ badgeData.name }}</h3>
        <p>{{ badgeData.description }}</p>
        <button @click="closeBadgeAnimation" class="close-animation-btn">
          Continuer
        </button>
      </div>
    </div>

    <!-- Intégration du GameGuide -->
    <GameGuide
      v-if="!gameStarted"
      gameId="shape-sequence"
      :forceShow="true"
      @start-game="onGuideComplete"
      @skip-intro="onGuideComplete"
    />

    <!-- Zone de jeu principale -->
    <div class="game-playground" v-if="gameStarted && !showResults">
      <!-- Barre de progression -->
      <div class="progress-container">
        <div class="progress-steps">
          <div class="progress-step" :class="{ completed: currentLevel > 0 }">
            <div class="step-icon">🎮</div>
            <div class="step-label">Démarrage</div>
          </div>

          <div class="progress-connector"></div>

          <div
            class="progress-step"
            :class="{
              completed: currentLevel >= Math.floor(levels.length / 3),
            }"
          >
            <div class="step-icon">🏃</div>
            <div class="step-label">En cours</div>
          </div>

          <div class="progress-connector"></div>

          <div
            class="progress-step"
            :class="{
              completed: currentLevel >= Math.floor((levels.length * 2) / 3),
            }"
          >
            <div class="step-icon">🔍</div>
            <div class="step-label">Avancé</div>
          </div>

          <div class="progress-connector"></div>

          <div
            class="progress-step"
            :class="{ completed: currentLevel >= levels.length }"
          >
            <div class="step-icon">🏆</div>
            <div class="step-label">Terminé</div>
          </div>
        </div>

        <div class="progress-bar">
          <div
            class="progress-fill"
            :style="{ width: progressPercentage + '%' }"
          ></div>
          <div class="progress-text">
            {{ currentLevel }} / {{ levels.length }}
          </div>
        </div>
      </div>

      <div class="level-indicator">
        <div class="level-badge">Niveau {{ currentLevel + 1 }}</div>
        <div class="score-badge">Score: {{ score }}</div>
      </div>

      <!-- Contenu du jeu -->
      <div class="game-content">
        <!-- Affichage de la séquence -->
        <div class="sequence-section">
          <div class="sequence-container">
            <div
              v-for="(shape, index) in sequence"
              :key="index"
              class="shape-container"
              :class="{ 'missing-shape': shape === '?' }"
            >
              <img
                v-if="shape !== '?'"
                :src="getShapeImage(shape)"
                :alt="shape"
                class="shape"
              />
              <div v-else class="missing-shape-icon">?</div>
            </div>
          </div>

          <div class="feedback-message" :class="feedbackClass">
            {{ feedback }}
          </div>
        </div>

        <!-- Affichage des options -->
        <div class="options-section">
          <h3 class="options-title">Sélectionne la forme manquante</h3>
          <div class="options-container">
            <div
              v-for="option in options"
              :key="option"
              class="option-item"
              :class="{ disabled: answerSelected }"
              @click="!answerSelected && checkAnswer(option)"
            >
              <img
                :src="getShapeImage(option)"
                :alt="option"
                class="option-image"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Actions du jeu -->
      <div class="game-actions">
        <button
          @click="skipLevel"
          class="action-button skip-button"
          v-if="!answerSelected"
        >
          <span class="btn-icon">⏭️</span>
          <span class="btn-text">Passer ce niveau</span>
        </button>

        <button
          @click="nextLevel"
          class="action-button next-button"
          v-if="answerSelected"
        >
          <span class="btn-icon">▶️</span>
          <span class="btn-text">Niveau suivant</span>
        </button>
      </div>
    </div>

    <!-- Écran des résultats -->
    <div class="results-overlay" v-if="showResults">
      <div class="results-modal">
        <div class="results-header">
          <div class="results-title-container">
            <div class="results-title-icon">🏆</div>
            <h2 class="results-title">Félicitations !</h2>
          </div>
          <p class="results-subtitle">
            Tu as terminé le jeu des Séquences de Formes
          </p>
        </div>

        <div class="results-statistics">
          <div class="stat-item">
            <div class="stat-value">{{ score }}</div>
            <div class="stat-label">Score Total</div>
          </div>

          <div class="stat-item">
            <div class="stat-value">{{ correctAnswers }}</div>
            <div class="stat-label">Réponses Correctes</div>
          </div>

          <div class="stat-item">
            <div class="stat-value">
              {{ Math.floor((correctAnswers / levels.length) * 100) }}%
            </div>
            <div class="stat-label">Précision</div>
          </div>
        </div>

        <p class="result-message">
          {{ getResultMessage() }}
        </p>

        <div class="results-actions">
          <button @click="restartGame" class="action-button restart-button">
            <span class="btn-icon">🔄</span>
            <span class="btn-text">Rejouer</span>
          </button>
          <button @click="goToMetierPage" class="action-button home-button">
            <span class="btn-icon">🏠</span>
            <span class="btn-text">Page des Métiers</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { unlockBadge, isBadgeUnlocked } from '@/utils/badges'
import GameGuide from '@/components/GameGuideComponent.vue'
import AuthService from '@/services/AuthService'
import PopUp from '@/components/PopUp.vue'
import { useGameTimer } from '@/services/useGameTimer'
import flamouImage from '@/assets/flamou/intresting.png'

export default {
  name: 'ShapeSequenceGame',
  components: {
    GameGuide,
    PopUp,
  },
  setup() {
    const {
      showGameModal,
      timeRemaining,
      startTimer,
      stopTimer,
      resetTimer,
      getRandomGameRoute,
      closeModal,
    } = useGameTimer()

    // Variables réactives
    const gameStarted = ref(false)
    const currentLevel = ref(0)
    const sequence = ref([])
    const options = ref([])
    const feedback = ref('')
    const feedbackClass = ref('')
    const answerSelected = ref(false)
    const answerCorrect = ref(false)
    const score = ref(0)
    const correctAnswers = ref(0)
    const showResults = ref(false)
    const showBadgeUnlockAnimation = ref(false)
    const badgeShapeSequenceId = ref(3)
    const levelResults = ref({})

    // Données pour le badge
    const badgeData = ref({
      name: 'Expert des formes',
      description:
        'Tu as reconnu toutes les séquences de formes correctement !',
    })

    // Définir les formes disponibles avec leurs chemins d'image
    const shapes = ['square', 'circle', 'triangle', 'rectangle']
    const shapeImages = {
      square: require('@/assets/shapes/Square.png'),
      circle: require('@/assets/shapes/Circle.png'),
      triangle: require('@/assets/shapes/Triangle.png'),
      rectangle: require('@/assets/shapes/Rectangle.png'),
    }

    // Configuration des niveaux
    const levels = [
      {
        sequence: [
          'rectangle',
          'circle',
          'triangle',
          'rectangle',
          'circle',
          '?',
        ],
        answer: 'triangle',
      },
      {
        sequence: [
          'rectangle',
          'rectangle',
          'triangle',
          'circle',
          'rectangle',
          'rectangle',
          'triangle',
          '?',
        ],
        answer: 'circle',
      },
      { sequence: ['triangle', 'circle', 'triangle', '?'], answer: 'circle' },
      { sequence: ['circle', 'rectangle', 'circle', '?'], answer: 'rectangle' },
      {
        sequence: ['square', 'triangle', 'square', 'triangle', '?'],
        answer: 'square',
      },
      {
        sequence: ['triangle', 'triangle', 'triangle', '?'],
        answer: 'triangle',
      },
      {
        sequence: ['circle', 'square', 'triangle', 'circle', 'square', '?'],
        answer: 'triangle',
      },
      {
        sequence: ['square', 'circle', 'triangle', 'square', 'circle', '?'],
        answer: 'triangle',
      },
      { sequence: ['square', 'square', 'square', '?'], answer: 'square' },
      {
        sequence: ['triangle', 'square', 'circle', 'triangle', 'square', '?'],
        answer: 'circle',
      },
      {
        sequence: ['circle', 'triangle', 'triangle', 'circle', 'triangle', '?'],
        answer: 'triangle',
      },
      { sequence: ['circle', 'square', 'triangle', '?'], answer: 'rectangle' },
    ]

    // Calcul du pourcentage de progression
    const progressPercentage = computed(() => {
      return (currentLevel.value / levels.length) * 100
    })

    const saveResultToBackend = (levelNumber, isCorrect) => {
      // D'abord, récupérer les données existantes
      AuthService.request('get', '/games/shape-sequence')
        .then((response) => {
          // Initialiser une structure par défaut si les données sont invalides
          let currentData =
            response.data && typeof response.data === 'object'
              ? response.data
              : { currentLevel: 0, completion: 0, levelResults: {} }

          // S'assurer que la structure minimale est présente
          if (!currentData.levelResults) {
            currentData.levelResults = {}
          }

          // S'assurer que currentLevel est un nombre valide
          if (
            typeof currentData.currentLevel !== 'number' ||
            isNaN(currentData.currentLevel)
          ) {
            currentData.currentLevel = 0
          }

          // Mettre à jour le niveau actuel si le niveau complété est plus élevé
          if (currentLevel.value + 1 > currentData.currentLevel) {
            currentData.currentLevel = currentLevel.value + 1
          }

          // Ajouter le résultat du niveau actuel
          currentData.levelResults[levelNumber] = isCorrect

          // Calculer le pourcentage de complétion (entre 0 et 1)
          const totalLevels = levels.length // 12 niveaux
          const completionDecimal =
            totalLevels > 0 ? currentData.currentLevel / totalLevels : 0

          // S'assurer que la complétion est un nombre entre 0 et 1 arrondi au centième
          currentData.completion = isNaN(completionDecimal)
            ? 0
            : parseFloat(completionDecimal.toFixed(4))

          console.log(
            `Complétion Shape Sequence: ${(currentData.completion * 100).toFixed(1)}% (${currentData.currentLevel}/${totalLevels} niveaux)`,
          )
          console.log('Données à envoyer au backend:', currentData)

          // Envoyer les données mises à jour
          return AuthService.request(
            'post',
            '/games/shape-sequence',
            currentData,
          )
        })
        .then((response) => {
          console.log(
            'Réponse complète du backend après mise à jour:',
            response,
          )
        })
        .catch((error) => {
          console.error('Erreur lors de la mise à jour des résultats:', error)

          if (error.response) {
            console.error("Réponse d'erreur du serveur:", {
              status: error.response.status,
              statusText: error.response.statusText,
              data: error.response.data,
            })
          }

          // En cas d'erreur d'authentification, sauvegarder localement
          if (
            error.response &&
            (error.response.status === 401 || error.response.status === 403)
          ) {
            console.warn(
              "Problème d'authentification. Vos résultats seront sauvegardés localement.",
            )
            saveResultLocally(levelNumber, isCorrect)
          }
        })
    }

    const saveResultLocally = (levelNumber, isCorrect) => {
      // Récupérer les données existantes du localStorage
      let localData = JSON.parse(
        localStorage.getItem('shapeSequenceResults') ||
          '{"currentLevel":0,"completion":0,"levelResults":{}}',
      )

      // S'assurer que la structure minimale est présente
      if (!localData.levelResults) {
        localData.levelResults = {}
      }

      // S'assurer que currentLevel est un nombre valide
      if (
        typeof localData.currentLevel !== 'number' ||
        isNaN(localData.currentLevel)
      ) {
        localData.currentLevel = 0
      }

      // Mettre à jour le niveau actuel si le niveau complété est plus élevé
      if (currentLevel.value + 1 > localData.currentLevel) {
        localData.currentLevel = currentLevel.value + 1
      }

      // Ajouter le résultat du niveau actuel
      localData.levelResults[levelNumber] = isCorrect

      // Calculer le pourcentage de complétion (entre 0 et 1)
      const totalLevels = levels.length // 12 niveaux
      const completionDecimal =
        totalLevels > 0 ? localData.currentLevel / totalLevels : 0

      // S'assurer que la complétion est un nombre entre 0 et 1
      localData.completion = isNaN(completionDecimal)
        ? 0
        : parseFloat(completionDecimal.toFixed(4))

      console.log(
        `Complétion locale Shape Sequence: ${(localData.completion * 100).toFixed(1)}% (${localData.currentLevel}/${totalLevels} niveaux)`,
      )

      // Sauvegarder dans localStorage
      localStorage.setItem('shapeSequenceResults', JSON.stringify(localData))
      console.log('Résultats sauvegardés localement:', localData)
    }

    const loadSavedResults = () => {
      // Essayer d'abord de récupérer depuis le backend
      AuthService.request('get', '/games/shape-sequence')
        .then((response) => {
          if (response.data && response.data.currentLevel > 0) {
            console.log('Données chargées depuis le backend:', response.data)

            // Charger les données
            const savedData = response.data

            // Mettre à jour le niveau actuel (si le jeu n'est pas encore terminé)
            if (savedData.currentLevel < levels.length) {
              currentLevel.value = savedData.currentLevel
            }

            // Charger les résultats des niveaux
            levelResults.value = savedData.levelResults || {}

            // Recalculer le nombre de réponses correctes
            correctAnswers.value = Object.values(levelResults.value).filter(
              (result) => result === true,
            ).length

            // Recalculer le score (10 points par bonne réponse, -2 points par mauvaise réponse)
            const correctCount = correctAnswers.value
            const incorrectCount =
              Object.keys(levelResults.value).length - correctCount
            score.value = correctCount * 10 - incorrectCount * 2

            // Afficher un message pour indiquer que la progression a été chargée
            console.log(
              `Progression chargée: Niveau ${currentLevel.value + 1}/${levels.length}`,
            )
          }
        })
        .catch(() => {
          // En cas d'erreur, essayer de charger depuis localStorage
          const localData = JSON.parse(
            localStorage.getItem('shapeSequenceResults') || 'null',
          )

          if (localData && localData.currentLevel > 0) {
            console.log('Données chargées depuis localStorage:', localData)

            // Charger les données locales
            if (localData.currentLevel < levels.length) {
              currentLevel.value = localData.currentLevel
            }

            // Charger les résultats des niveaux
            levelResults.value = localData.levelResults || {}

            // Recalculer le nombre de réponses correctes
            correctAnswers.value = Object.values(levelResults.value).filter(
              (result) => result === true,
            ).length

            // Recalculer le score
            const correctCount = correctAnswers.value
            const incorrectCount =
              Object.keys(levelResults.value).length - correctCount
            score.value = correctCount * 10 - incorrectCount * 2

            console.log(
              `Progression locale chargée: Niveau ${currentLevel.value + 1}/${levels.length}`,
            )
          }
        })
    }

    // Méthode pour démarrage du jeu après le guide
    const onGuideComplete = () => {
      gameStarted.value = true
      loadSavedResults()
      loadLevel()
    }

    // Charger un niveau
    const loadLevel = () => {
      if (currentLevel.value >= levels.length) {
        endGame()
        return
      }

      const level = levels[currentLevel.value]
      sequence.value = level.sequence
      options.value = generateOptions(level.answer)
      feedback.value = ''
      feedbackClass.value = ''
      answerSelected.value = false
    }

    // Générer les options pour le niveau actuel
    const generateOptions = (correctShape) => {
      const opts = []
      // Ajouter la bonne réponse
      opts.push(correctShape)

      // Ajouter d'autres formes aléatoires (sans dupliquer)
      while (opts.length < 4) {
        const shape = shapes[Math.floor(Math.random() * shapes.length)]
        if (!opts.includes(shape)) {
          opts.push(shape)
        }
      }

      // Mélanger les options
      return opts.sort(() => Math.random() - 0.5)
    }

    // Obtenir l'image d'une forme
    const getShapeImage = (shape) => {
      return shapeImages[shape]
    }

    // Vérifier la réponse
    const checkAnswer = (selectedShape) => {
      answerSelected.value = true
      const correctShape = levels[currentLevel.value].answer

      if (selectedShape === correctShape) {
        feedback.value = "Bravo ! C'est la bonne réponse !"
        feedbackClass.value = 'feedback-correct'
        answerCorrect.value = true
        score.value += 10
        correctAnswers.value++

        // Sauvegarder le résultat positif
        saveResultToBackend(currentLevel.value + 1, true)
      } else {
        feedback.value =
          "Ce n'est pas la bonne réponse. La bonne réponse était : " +
          correctShape
        feedbackClass.value = 'feedback-incorrect'
        answerCorrect.value = false
        score.value = Math.max(0, score.value - 2) // Pénalité légère

        // Sauvegarder le résultat négatif
        saveResultToBackend(currentLevel.value + 1, false)
      }
    }

    // Passer au niveau suivant
    const nextLevel = () => {
      currentLevel.value++
      loadLevel()
    }

    // Sauter un niveau
    const skipLevel = () => {
      saveResultToBackend(currentLevel.value + 1, false)

      currentLevel.value++
      loadLevel()
    }

    // Redémarrer le jeu
    const restartGame = () => {
      currentLevel.value = 0
      score.value = 0
      correctAnswers.value = 0
      showResults.value = false
      levelResults.value = {}

      // Réinitialiser les données dans le backend
      const resetData = {
        currentLevel: 0,
        completion: 0,
        levelResults: {},
      }

      AuthService.request('post', '/games/shape-sequence', resetData).catch(
        (error) => {
          console.error(
            'Erreur lors de la réinitialisation des données:',
            error,
          )
          localStorage.setItem(
            'shapeSequenceResults',
            JSON.stringify(resetData),
          )
        },
      )

      loadLevel()
    }

    // Terminer le jeu
    const endGame = () => {
      showResults.value = true

      // Calculer les statistiques finales
      // const finalStats = {
      //   currentLevel: levels.length,
      //   completion: 100.0,
      //   levelResults: levelResults.value
      // };

      // Envoyer les statistiques finales au backend
      // AuthService.request('post', '/games/shape-sequence', finalStats)
      //   .catch(error => {
      //     console.error('Erreur lors de la mise à jour des statistiques finales:', error);
      //     localStorage.setItem('shapeSequenceResults', JSON.stringify(finalStats));
      //   });

      // Débloquer le badge si 80% ou plus de réponses correctes
      if (correctAnswers.value / levels.length >= 0.8) {
        unlockCompletionBadge()
      }
    }

    // Débloquer le badge de complétion
    const unlockCompletionBadge = () => {
      if (!isBadgeUnlocked(badgeShapeSequenceId.value)) {
        const badgeUnlocked = unlockBadge(badgeShapeSequenceId.value)
        if (badgeUnlocked) {
          setTimeout(() => {
            showBadgeUnlockAnimation.value = true
          }, 1500)
        }
      }
    }

    // Fermer l'animation du badge
    const closeBadgeAnimation = () => {
      showBadgeUnlockAnimation.value = false
    }

    // Aller à la page des métiers
    const goToMetierPage = () => {
      window.location.href = '/metiers'
    }

    // Obtenir un message de résultat personnalisé
    const getResultMessage = () => {
      const accuracy = correctAnswers.value / levels.length

      if (accuracy >= 0.9) {
        return 'Incroyable ! Tu as un talent naturel pour reconnaître les séquences. Ton cerveau est vraiment bien entraîné !'
      } else if (accuracy >= 0.7) {
        return "Très bien ! Tu as un bon sens de l'observation et de la logique. Continue comme ça !"
      } else if (accuracy >= 0.5) {
        return "Pas mal ! Tu as compris les bases, mais tu peux encore t'améliorer avec de la pratique."
      } else {
        return "C'est un bon début ! Les séquences peuvent être difficiles, mais avec de l'entraînement, tu vas t'améliorer."
      }
    }

    return {
      // État du jeu
      gameStarted,
      currentLevel,
      sequence,
      options,
      feedback,
      feedbackClass,
      answerSelected,
      answerCorrect,
      score,
      correctAnswers,
      showResults,
      levels,
      progressPercentage,
      levelResults,

      // Animation du badge
      showBadgeUnlockAnimation,
      badgeData,
      badgeShapeSequenceId,

      // Méthodes
      onGuideComplete, // Ajout de cette méthode pour le guide
      getShapeImage,
      checkAnswer,
      nextLevel,
      skipLevel,
      restartGame,
      closeBadgeAnimation,
      goToMetierPage,
      getResultMessage,

      saveResultToBackend,
      loadSavedResults,
      saveResultLocally,

      showGameModal,
      timeRemaining,
      startTimer,
      stopTimer,
      resetTimer,
      getRandomGameRoute,
      closeModal,
      flamouImage,
    }
  },
}
</script>

<style scoped>
/* Base Styles */
.shape-game-container {
  font-family: 'Comic Sans MS', 'Chalkboard SE', 'Marker Felt', sans-serif;
  max-width: 1100px;
  margin: 0 auto;
  padding: 20px;
  color: #333;
  min-height: 100vh;
}

/* Animation du badge débloqué */
.badge-unlock-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1100;
  animation: fadeIn 0.5s ease-out;
}

.badge-unlock-animation {
  background-color: #fff;
  border-radius: 20px;
  padding: 30px;
  text-align: center;
  max-width: 400px;
  box-shadow: 0 0 30px rgba(33, 150, 243, 0.6); /* Couleur bleue pour le thème des formes */
  animation: scaleIn 0.5s ease-out;
}

.badge-unlock-animation .badge-icon {
  font-size: 80px;
  margin-bottom: 20px;
  animation: pulse 2s infinite;
  color: #2196f3; /* Bleu pour le thème des formes */
}

.badge-unlock-animation h2 {
  color: #2196f3;
  font-size: 2rem;
  margin-bottom: 10px;
}

.badge-unlock-animation h3 {
  color: #333;
  font-size: 1.5rem;
  margin-bottom: 15px;
}

.badge-unlock-animation p {
  color: #666;
  margin-bottom: 20px;
}

.close-animation-btn {
  background-color: #2196f3;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 50px;
  font-weight: bold;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.close-animation-btn:hover {
  background-color: #1976d2;
  transform: scale(1.05);
}

/* Game Playground */
.game-playground {
  margin-top: 30px;
}

/* Progress Container */
.progress-container {
  margin-bottom: 30px;
}

.progress-steps {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
}

.progress-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 2;
}

.step-icon {
  width: 40px;
  height: 40px;
  background-color: #e9ecef;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  margin-bottom: 5px;
  border: 2px solid #ced4da;
  position: relative;
}

.step-label {
  font-size: 0.8rem;
  color: #6c757d;
}

.progress-step.completed .step-icon {
  background-color: #2196f3;
  color: white;
  border-color: #2196f3;
}

.progress-step.completed .step-label {
  color: #2196f3;
  font-weight: bold;
}

.progress-connector {
  height: 2px;
  background-color: #ced4da;
  flex-grow: 1;
  margin: 0 -5px;
  position: relative;
  top: -22px;
  z-index: 1;
}

.progress-bar {
  width: 100%;
  height: 16px;
  background-color: #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #2196f3, #03a9f4);
  border-radius: 8px;
  transition: width 0.5s ease;
}

.progress-text {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #333;
  font-weight: bold;
  font-size: 0.75rem;
}

/* Level Indicator */
.level-indicator {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.level-badge,
.score-badge {
  background-color: #2196f3;
  color: white;
  padding: 8px 16px;
  border-radius: 50px;
  font-weight: bold;
  font-size: 1rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.score-badge {
  background-color: #ff9800;
}

/* Game Content */
.game-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
  margin: 30px 0;
  background-color: white;
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

/* Sequence Section */
.sequence-section {
  text-align: center;
}

.sequence-container {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 20px;
}

.shape-container {
  width: 80px;
  height: 80px;
  background-color: #f5f5f5;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.missing-shape {
  background-color: #e3f2fd;
  border: 2px dashed #2196f3;
  animation: pulse 2s infinite;
}

.missing-shape-icon {
  font-size: 2rem;
  font-weight: bold;
  color: #2196f3;
}

.shape {
  max-width: 80%;
  max-height: 80%;
}

.feedback-message {
  font-size: 1.2rem;
  font-weight: bold;
  margin: 20px 0;
  padding: 10px;
  border-radius: 10px;
  animation: fadeIn 0.5s ease;
}

.feedback-correct {
  color: #4caf50;
  background-color: #e8f5e9;
}

.feedback-incorrect {
  color: #f44336;
  background-color: #ffebee;
}

/* Options Section */
.options-section {
  text-align: center;
}

.options-title {
  font-size: 1.3rem;
  color: #333;
  margin-bottom: 20px;
}

.options-container {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

.option-item {
  width: 100px;
  height: 100px;
  background-color: #f9f9f9;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.option-item:hover:not(.disabled) {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  background-color: #e3f2fd;
}

.option-item.disabled {
  cursor: default;
  opacity: 0.7;
}

.option-image {
  max-width: 80%;
  max-height: 80%;
  transition: all 0.3s ease;
}

/* Game Actions */
.game-actions {
  margin: 20px 0;
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

.action-button {
  padding: 12px 25px;
  border: none;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.skip-button {
  background-color: #9e9e9e;
  color: white;
}

.skip-button:hover {
  background-color: #757575;
}

.next-button {
  background-color: #4caf50;
  color: white;
}

.next-button:hover {
  background-color: #388e3c;
}

.retry-button {
  background-color: #ff9800;
  color: white;
}

.retry-button:hover {
  background-color: #f57c00;
}

/* Results Modal */
.results-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.results-modal {
  background-color: white;
  border-radius: 20px;
  padding: 30px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  animation: slideIn 0.5s ease;
}

.results-header {
  text-align: center;
  margin-bottom: 30px;
}

.results-title-container {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
}

.results-title-icon {
  font-size: 2.5rem;
  margin-right: 15px;
  color: #ff9800;
}

.results-title {
  font-size: 2.2rem;
  color: #2196f3;
  margin: 0;
}

.results-subtitle {
  font-size: 1.2rem;
  color: #666;
  margin: 0;
}

.results-statistics {
  display: flex;
  justify-content: space-around;
  margin: 30px 0;
}

.stat-item {
  text-align: center;
  background-color: #f5f5f5;
  border-radius: 15px;
  padding: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
  width: 28%;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: bold;
  color: #2196f3;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
}

.result-message {
  text-align: center;
  font-size: 1.1rem;
  color: #555;
  margin: 25px 0;
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 10px;
  line-height: 1.5;
}

.results-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}

.restart-button {
  background-color: #2196f3;
  color: white;
}

.restart-button:hover {
  background-color: #1976d2;
}

.home-button {
  background-color: #9e9e9e;
  color: white;
}

.home-button:hover {
  background-color: #757575;
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideIn {
  from {
    transform: translateY(50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

@keyframes scaleIn {
  from {
    transform: scale(0.8);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

/* Responsive Styles */
@media (max-width: 768px) {
  .game-content {
    padding: 15px;
  }

  .sequence-container {
    gap: 10px;
  }

  .shape-container {
    width: 60px;
    height: 60px;
  }

  .option-item {
    width: 80px;
    height: 80px;
  }

  .results-statistics {
    flex-direction: column;
    align-items: center;
    gap: 15px;
  }

  .stat-item {
    width: 80%;
  }
}

@media (max-width: 480px) {
  .shape-container {
    width: 50px;
    height: 50px;
  }

  .option-item {
    width: 70px;
    height: 70px;
  }

  .game-actions {
    flex-direction: column;
    align-items: center;
  }

  .action-button {
    width: 100%;
  }

  .progress-steps {
    display: none;
  }
}

/* Accessibility Enhancements */
.shape-game-container:focus-within {
  outline: 3px solid #2196f3;
}

button:focus {
  outline: 3px solid #2196f3;
  outline-offset: 3px;
}

/* Animation pause for users who prefer reduced motion */
@media (prefers-reduced-motion: reduce) {
  button,
  .option-item,
  .missing-shape,
  .results-modal {
    animation: none !important;
    transition: none !important;
  }
}
</style>
