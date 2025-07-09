<template>
  <PopUp
    v-if="showGameModal"
    message="Souhaites-tu continuer à jouer à ce jeu ?"
    :image="flamouImage"
    :redirect="getRandomGameRoute()"
    buttonConfirm="Non"
    buttonCancel="Oui"
    :visible="showGameModal"
    @close="closeModal"
  />
  
  <!-- Félicitations de Flamou -->
  <div v-if="showFlamouCongratulations" class="flamou-congratulations-overlay">
    <div class="flamou-congratulations-container">
      <img :src="flamouCongratulationsImage" alt="Flamou" class="flamou-congratulations-image" />
      <div class="flamou-speech-bubble">
        <p>{{ flamouCongratulationsMessage }}</p>
        <div class="flamou-timer" v-if="showFlamouTimer">
          <div class="flamou-timer-bar">
            <div 
              class="flamou-timer-fill"
              :style="{ width: flamouTimerProgress + '%' }"
            ></div>
          </div>
          <div class="flamou-timer-text">{{ Math.ceil(flamouTimeLeft / 1000) }}s</div>
        </div>
      </div>
    </div>
  </div>
  
  <div class="job-discovery-container">
    <!-- Animation badge débloqué -->
    <div v-if="showBadgeUnlockAnimation" class="badge-unlock-overlay">
      <div class="badge-unlock-animation">
        <div class="badge-icon">🏆</div>
        <h2>Badge débloqué !</h2>
        <h3>{{ badgeData.name }}</h3>
        <p>{{ badgeData.description }}</p>
        <button @click="closeBadgeAnimation" class="close-animation-btn">
          Continuer
        </button>
      </div>
    </div>

    <!-- Header avec personnage guide
    <div class="guide-character" v-if="!gameStarted">
      <img src="@/assets/avatars/guide.png" alt="Guide" class="guide-avatar" />
      <div class="speech-bubble">
        <p>Bienvenue dans le jeu Découvre ton Métier ! Swipe à gauche ou à droite pour explorer des carrières passionnantes et trouver ta voie.</p>
      </div>
    </div>

    <div class="game-header">
      <h1 class="main-title">Découvre ton Métier</h1>
      <p class="subtitle" v-if="!gameStarted">Explore les métiers qui correspondent à tes intérêts et compétences</p>
    </div>
    
     Écran d'accueil
    <div class="welcome-screen" v-if="!gameStarted">
      <div class="welcome-card">
        <div class="card-icon">🚀</div>
        <h2>Comment jouer ?</h2>
        <ol class="instructions-list">
          <li>
            <span class="instruction-step">1</span>
            Chaque carte représente un métier différent
          </li>
          <li>
            <span class="instruction-step">2</span>
            Regarde la vidéo et lis la description
          </li>
          <li>
            <span class="instruction-step">3</span>
            Choisis : 
            <ul class="sub-instructions">
              <li>👍 "Ça me plaît" si le métier t'intéresse</li>
              <li>👎 "Pas pour moi" si ce n'est pas ton truc</li>
              <li>ℹ️ "Détails" pour plus d'informations</li>
            </ul>
          </li>
          <li>
            <span class="instruction-step">4</span>
            À la fin, découvre les métiers qui t'ont plu
          </li>
        </ol>
        
        <button @click="startGame" class="start-button">
          <span class="btn-icon">🎮</span>
          <span class="btn-text">Commencer à explorer</span>
        </button>
      </div>
    </div> -->
    <GameGuide
      v-if="!gameStarted"
      gameId="jobs-game"
      :forceShow="true"
      @start-game="startGame"
      @skip-intro="startGame"
    />

    <!-- Zone de jeu principale -->
    <div class="game-playground" v-if="gameStarted && !showResults">
      <!-- Barre de progression -->
      <div class="progress-container">
        <div class="progress-steps">
          <div class="progress-step" :class="{ completed: currentIndex > 0 }">
            <div class="step-icon">🎮</div>
            <div class="step-label">Démarrage</div>
          </div>

          <div class="progress-connector"></div>

          <div
            class="progress-step"
            :class="{ completed: currentIndex >= Math.floor(batchSize / 3) }"
          >
            <div class="step-icon">🏃</div>
            <div class="step-label">En cours</div>
          </div>

          <div class="progress-connector"></div>

          <div
            class="progress-step"
            :class="{
              completed: currentIndex >= Math.floor((batchSize * 2) / 3),
            }"
          >
            <div class="step-icon">🔍</div>
            <div class="step-label">Avancé</div>
          </div>

          <div class="progress-connector"></div>

          <div
            class="progress-step"
            :class="{ completed: currentIndex >= batchSize || batchCompleted }"
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
          <div class="progress-text">{{ currentIndex }} / {{ batchSize }}</div>
        </div>
      </div>

      <!-- Contenu du jeu -->
      <div class="game-content">
        <transition name="card-transition">
          <div v-if="currentMetier" class="job-card">
            <div class="job-card-inner">
              <h2 class="job-title">{{ currentMetier.name }}</h2>

              <div class="job-media">
                <div class="video-player">
                  <video
                    v-if="currentMetier.video"
                    ref="jobVideo"
                    :src="getVideoSource(currentMetier.video)"
                    :poster="currentMetier.poster"
                    controls
                    autoplay
                    muted
                    preload="metadata"
                    class="video-element"
                    @loadeddata="handleVideoLoaded"
                    @play="handleVideoPlay"
                    @error="handleVideoError"
                  >
                    Votre navigateur ne supporte pas la lecture de vidéos.
                  </video>
                  <div v-else class="video-placeholder">
                    <div class="placeholder-icon">🎬</div>
                    <p>Vidéo non disponible</p>
                  </div>
                </div>
              </div>

              <div class="job-description">
                <p>{{ currentMetier.description }}</p>
              </div>

              <div class="job-skills">
                <div
                  v-for="(skill, index) in currentMetier.skills"
                  :key="index"
                  class="skill-tag"
                >
                  {{ skill }}
                </div>
              </div>
            </div>
          </div>

          <div v-else-if="batchCompleted" class="batch-complete-card">
            <div class="card-icon large-icon">🎯</div>
            <h2>Lot terminé !</h2>
            <p>Tu as découvert {{ batchSize }} métiers.</p>
            <p v-if="likedJobs.length > 0">
              Tu as aimé {{ getLikedJobsInCurrentBatch() }} métier(s).
            </p>
            <p>Souhaites-tu continuer à découvrir d'autres métiers ?</p>
          </div>

          <div v-else-if="allJobsSeen" class="all-jobs-seen-card">
            <div class="card-icon large-icon">🏁</div>
            <h2>Bravo !</h2>
            <p>Tu as découvert tous les métiers disponibles.</p>
            <p v-if="likedJobs.length > 0">
              Tu as aimé {{ likedJobs.length }} métier(s) au total.
            </p>
          </div>

          <div v-else class="loading-card">
            <div class="loading-spinner"></div>
            <p>Chargement des métiers...</p>
          </div>
        </transition>
      </div>

      <!-- Actions du jeu -->
      <div class="game-actions">
        <div v-if="currentMetier" class="card-actions">
          <button @click="dislikeJob" class="action-button dislike-button">
            <span class="btn-icon">👎</span>
            <span class="btn-text">Pas pour moi</span>
          </button>

          <button @click="showDetails" class="action-button info-button">
            <span class="btn-icon">ℹ️</span>
            <span class="btn-text">Détails</span>
          </button>

          <button @click="likeJob" class="action-button like-button">
            <span class="btn-icon">👍</span>
            <span class="btn-text">Ça me plaît</span>
          </button>
        </div>

        <div v-if="batchCompleted" class="batch-actions">
          <button @click="loadNextBatch" class="action-button continue-button">
            <span class="btn-icon">▶️</span>
            <span class="btn-text">Continuer</span>
          </button>

          <button
            @click="finishAndShowResults"
            class="action-button finish-button"
          >
            <span class="btn-icon">🏁</span>
            <span class="btn-text">Terminer</span>
          </button>
        </div>

        <div v-if="allJobsSeen" class="home-action">
          <button
            @click="finishAndShowResults"
            class="action-button like-button"
          >
            <span class="btn-icon">❤️</span>
            <span class="btn-text">Voir mes métiers préférés</span>
          </button>
          <button @click="goToDashboard" class="action-button finish-button">
            <span class="btn-icon">🏁</span>
            <span class="btn-text">Terminer</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Écran des résultats -->
    <div class="results-overlay" v-if="showResults">
      <div class="results-modal">
        <div class="results-header">
          <div class="results-title-container">
            <div class="results-title-icon">🏆</div>
            <h2 class="results-title">Tes métiers préférés</h2>
          </div>
          <p class="results-subtitle">Voici les métiers qui t'ont intéressé</p>
        </div>

        <div v-if="likedJobs.length > 0" class="liked-jobs-grid">
          <div
            v-for="(job, index) in likedJobs"
            :key="index"
            class="liked-job-item"
          >
            <div class="liked-job-media">
              <img
                :src="job.poster || '@/assets/job-placeholder.jpg'"
                alt="Métier"
                class="liked-job-img"
              />
              <div class="play-overlay">▶️</div>
            </div>
            <div class="liked-job-info">
              <h3>{{ job.name }}</h3>
              <button @click="goToJobDetails(job)" class="view-button">
                <span class="btn-icon">👁️</span>
                <span class="btn-text">Voir détails</span>
              </button>
            </div>
          </div>
        </div>

        <div v-else class="no-liked-jobs">
          <div class="card-icon large-icon">🔍</div>
          <p>Tu n'as pas encore sélectionné de métiers qui te plaisent.</p>
          <p>Continue à explorer pour découvrir des métiers intéressants !</p>
        </div>

        <div class="results-actions">
          <button @click="restartGame" class="action-button restart-button">
            <span class="btn-icon">🔄</span>
            <span class="btn-text">Rejouer</span>
          </button>

          <button @click="goToNextGame" class="action-button next-game-button">
            <span class="btn-icon">🎮</span>
            <span class="btn-text">Jeu suivant</span>
          </button>

          <button @click="goToDashboard" class="action-button home-button">
            <span class="btn-icon">🏠</span>
            <span class="btn-text">Accueil</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { metiersData } from '@/data/metiersData.js'
import { unlockBadge, isBadgeUnlocked } from '@/utils/badges'
import GameGuide from '@/components/GameGuideComponent.vue'
import AuthService from '@/services/AuthService'
import PopUp from '@/components/PopUp.vue'
import { useGameTimer } from '@/services/useGameTimer'
import flamouImage from '@/assets/flamou/intresting.png'
import flamouHappy from '@/assets/flamou/happy.png'
import flamouHappy2 from '@/assets/flamou/happy2.png'
import flamouNormal from '@/assets/flamou/normal.png'
import flamouHey from '@/assets/flamou/hey.png'

export default {
  name: 'JobDiscoveryGame',
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
    const showResults = ref(false)
    const currentIndex = ref(0)
    const currentBatch = ref([])
    const batchSize = ref(5)
    const seenJobs = ref([])
    const likedJobs = ref([])
    const currentBatchIds = ref([])
    const batchCompleted = ref(false)
    const allJobsSeen = ref(false)
    const highContrastMode = ref(false)
    const showBadgeUnlockAnimation = ref(false)
    const badgeJobDiscoveryId = ref(7)
    const jobVideo = ref(null)

    // Variables pour les félicitations de Flamou
    const showFlamouCongratulations = ref(false)
    const flamouCongratulationsImage = ref(flamouNormal)
    const flamouCongratulationsMessage = ref('')
    const flamouTimer = ref(null)
    const flamouTimeLeft = ref(0)
    const flamouTimerProgress = ref(100)
    const showFlamouTimer = ref(false)
    const flamouCompletionTimer = ref(null)
    const autoAdvanceTimer = ref(null)

    // Métier actuel
    const currentMetier = computed(() => {
      if (
        currentBatch.value.length === 0 ||
        currentIndex.value >= currentBatch.value.length
      ) {
        return null
      }
      return currentBatch.value[currentIndex.value]
    })

    watch(currentMetier, async (newMetier) => {
      if (newMetier && newMetier.video) {
        await nextTick() // Attendre que le DOM soit mis à jour
        tryAutoplayVideo()
      }
    })

    function tryAutoplayVideo() {
      if (jobVideo.value) {
        const video = jobVideo.value

        // Réinitialiser la vidéo
        video.currentTime = 0

        // Essayer de lancer la vidéo
        const playPromise = video.play()

        if (playPromise !== undefined) {
          playPromise
            .then(() => {
              console.log('Autoplay réussi')
            })
            .catch((error) => {
              console.log('Autoplay bloqué par le navigateur:', error)
              // Si l'autoplay échoue, on peut essayer sans le son
              video.muted = true
              video.play().catch(() => {
                console.log('Impossible de lancer la vidéo automatiquement')
              })
            })
        }
      }
    }

    // Gestionnaire quand la vidéo est chargée
    function handleVideoLoaded() {
      console.log('Vidéo chargée')
      tryAutoplayVideo()
    }

    // Gestionnaire quand la vidéo commence à jouer
    function handleVideoPlay() {
      console.log('Vidéo en cours de lecture')
    }

    // Gestionnaire d'erreur vidéo
    function handleVideoError(event) {
      console.error('Erreur lors du chargement de la vidéo:', event)
    }

    // Modifier la fonction nextCard pour gérer l'autoplay
    function nextCard() {
      currentIndex.value++

      // Vérifier si tous les métiers du lot ont été vus
      if (currentIndex.value >= currentBatch.value.length) {
        batchCompleted.value = true
      } else {
        // Si il y a un nouveau métier, essayer l'autoplay après un court délai
        setTimeout(() => {
          tryAutoplayVideo()
        }, 100)
      }
    }

    // Données pour le badge
    const badgeData = ref({
      name: 'Explorateur de Métiers',
      description: 'Tu as découvert et aimé plusieurs métiers différents !',
    })

    // Calcul du pourcentage de progression
    const progressPercentage = computed(() => {
      if (batchSize.value === 0) return 0
      // Faire commencer la barre à 0 et atteindre 100% au dernier élément
      return Math.min(100, (currentIndex.value / batchSize.value) * 100)
    })

    // Vérifier si le niveau est complété
    const isBatchComplete = computed(() => {
      return currentIndex.value >= currentBatch.value.length
    })

    // Métiers disponibles (non vus)
    const availableJobs = computed(() => {
      return metiersData.filter((job) => !seenJobs.value.includes(job.id))
    })

    // Fonctions
    function startGame() {
      gameStarted.value = true
      loadSavedData()
      loadInitialBatch()
    }

    function getVideoSource(videoPath) {
      if (!videoPath) {
        return ''
      }
      return videoPath
    }

    function loadSavedData() {
      // Charger les paramètres d'accessibilité
      const accessibilitySettings = localStorage.getItem(
        'accessibilitySettings',
      )
      if (accessibilitySettings) {
        try {
          const settings = JSON.parse(accessibilitySettings)
          highContrastMode.value = settings.highContrast || false
        } catch (e) {
          console.error(
            "Erreur lors du chargement des paramètres d'accessibilité:",
            e,
          )
        }
      }

      // Charger les métiers déjà vus
      const seenJobsData = localStorage.getItem('seen-metiers')
      if (seenJobsData) {
        try {
          seenJobs.value = JSON.parse(seenJobsData)
        } catch (e) {
          console.error('Erreur lors du chargement des métiers vus:', e)
          seenJobs.value = []
        }
      }

      // Charger les métiers aimés
      const likedJobsData = localStorage.getItem('liked-metiers')
      if (likedJobsData) {
        try {
          const likedIds = JSON.parse(likedJobsData)
          likedJobs.value = metiersData.filter((job) =>
            likedIds.includes(job.id),
          )
        } catch (e) {
          console.error('Erreur lors du chargement des métiers aimés:', e)
          likedJobs.value = []
        }
      }
    }

    function saveData() {
      // Sauvegarder les paramètres d'accessibilité
      localStorage.setItem(
        'accessibilitySettings',
        JSON.stringify({
          highContrast: highContrastMode.value,
        }),
      )

      // Sauvegarder les métiers vus
      localStorage.setItem('seen-metiers', JSON.stringify(seenJobs.value))

      // Sauvegarder les métiers aimés
      const likedIds = likedJobs.value.map((job) => job.id)
      localStorage.setItem('liked-metiers', JSON.stringify(likedIds))
    }

    function getLikedJobsInCurrentBatch() {
      return likedJobs.value.filter((job) =>
        currentBatchIds.value.includes(job.id),
      ).length
    }

    function loadInitialBatch() {
      loadNextBatch()
    }

    function loadNextBatch() {
      currentBatch.value = []
      currentIndex.value = 0
      currentBatchIds.value = []
      batchCompleted.value = false

      // Vérifier s'il reste des métiers à montrer
      if (availableJobs.value.length === 0) {
        allJobsSeen.value = true
        return
      }

      // Sélectionner aléatoirement un batch de métiers non vus
      const availBatchSize = Math.min(
        batchSize.value,
        availableJobs.value.length,
      )
      const availableIndices = Array.from(
        { length: availableJobs.value.length },
        (_, i) => i,
      )

      for (let i = 0; i < availBatchSize; i++) {
        const randomIndex = Math.floor(Math.random() * availableIndices.length)
        const selectedIndex = availableIndices.splice(randomIndex, 1)[0]

        // Créer une vraie copie profonde du métier pour éviter les problèmes de référence
        const originalMetier = availableJobs.value[selectedIndex]
        const selectedMetier = JSON.parse(JSON.stringify(originalMetier))

        currentBatch.value.push(selectedMetier)
        currentBatchIds.value.push(selectedMetier.id)
      }
    }

    function likeJob() {
      if (!currentMetier.value) return

      // Ajouter aux métiers vus
      if (!seenJobs.value.includes(currentMetier.value.id)) {
        seenJobs.value.push(currentMetier.value.id)
      }

      // Ajouter aux métiers aimés s'il n'y est pas déjà
      if (!likedJobs.value.some((job) => job.id === currentMetier.value.id)) {
        likedJobs.value.push(currentMetier.value)
      }

      // Envoyer le choix au backend
      sendJobChoiceToBackend(currentMetier.value.name, 'like')

      // Afficher les félicitations de Flamou
      displayFlamouCongratulations('like')

      saveData()
      checkBadges()
      nextCard()
    }

    function dislikeJob() {
      if (!currentMetier.value) return

      // Ajouter uniquement aux métiers vus
      if (!seenJobs.value.includes(currentMetier.value.id)) {
        seenJobs.value.push(currentMetier.value.id)
      }

      // Envoyer le choix au backend
      sendJobChoiceToBackend(currentMetier.value.name, 'dislike')

      // Afficher les félicitations de Flamou
      displayFlamouCongratulations('dislike')

      saveData()
      checkBadges()
      nextCard()
    }

    function unknownJob() {
      if (!currentMetier.value) return

      // Ajouter aux métiers vus
      if (!seenJobs.value.includes(currentMetier.value.id)) {
        seenJobs.value.push(currentMetier.value.id)
      }

      // Envoyer le choix au backend
      sendJobChoiceToBackend(currentMetier.value.name, 'unknown')

      saveData()
      nextCard()
    }

    function sendJobChoiceToBackend(jobName, choiceType) {
      // Mapper les types de choix aux valeurs attendues par le backend
      const choiceTypeMapping = {
        like: 'like',
        dislike: 'dislike',
        unknown: 'unknown',
        skip: 'unknown', // Si on veut gérer les sauts, on peut les mapper à 'unknown'
      }

      const backendChoice = choiceTypeMapping[choiceType]

      // D'abord, récupérer les données existantes
      AuthService.request('get', '/games/jobs')
        .then((response) => {
          // Initialiser une structure par défaut si les données sont invalides
          let currentData =
            response.data && typeof response.data === 'object'
              ? response.data
              : { completion: 0, jobChoices: {} }

          // S'assurer que la structure minimale est présente
          if (!currentData.jobChoices) {
            currentData.jobChoices = {}
          }

          // Ajouter le nouveau choix de métier
          currentData.jobChoices[jobName] = backendChoice

          // Calculer le pourcentage de complétion
          const totalPossibleJobs = metiersData.length
          const answeredJobsCount = Object.keys(currentData.jobChoices).length

          // Calculer et formater le pourcentage (0-100)
          const completionPercentage =
            totalPossibleJobs > 0
              ? Math.min(
                  100,
                  Math.round((answeredJobsCount / totalPossibleJobs) * 100),
                )
              : 0

          currentData.completion = completionPercentage / 100

          console.log('Données à envoyer au backend:', currentData)
          console.log(
            `Complétion: ${completionPercentage}% (${answeredJobsCount}/${totalPossibleJobs} métiers)`,
          )

          // Envoyer les données mises à jour
          return AuthService.request('post', '/games/jobs', currentData)
        })
        .then((response) => {
          console.log(
            'Réponse complète du backend après mise à jour:',
            response,
          )
        })
        .catch((error) => {
          console.error(
            'Erreur lors de la mise à jour des choix de métiers:',
            error,
          )

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
              "Problème d'authentification. Vos choix de métiers seront sauvegardés localement.",
            )
            saveJobChoicesLocally(jobName, backendChoice)
          }
        })
    }

    function saveJobChoicesLocally(jobName, choiceType) {
      // Récupérer les données existantes du localStorage
      let localData = JSON.parse(
        localStorage.getItem('userJobChoices') ||
          '{"completion":0,"jobChoices":{}}',
      )

      // Mettre à jour les données locales
      if (!localData.jobChoices) {
        localData.jobChoices = {}
      }

      // Ajouter le choix de métier
      localData.jobChoices[jobName] = choiceType

      // Calculer le pourcentage de complétion
      const totalPossibleJobs = metiersData.length
      const answeredJobsCount = Object.keys(localData.jobChoices).length

      // Calculer et formater le pourcentage (0-100)
      localData.completion =
        totalPossibleJobs > 0
          ? Math.min(
              100,
              Math.round((answeredJobsCount / totalPossibleJobs) * 100),
            )
          : 0

      // Sauvegarder dans localStorage
      localStorage.setItem('userJobChoices', JSON.stringify(localData))
      console.log('Choix de métiers sauvegardés localement:', localData)
    }

    function showDetails() {
      // if (!currentMetier.value) return;
      // // Rediriger vers la page de détails du métier
      // window.location.href = `/metier/${currentMetier.value.id}`;
    }

    function finishAndShowResults() {
      clearAllTimers()
      showResults.value = true
    }

    function restartGame() {
      clearAllTimers()
      currentIndex.value = 0
      seenJobs.value = []
      likedJobs.value = []
      batchCompleted.value = false
      allJobsSeen.value = false
      showResults.value = false
      showFlamouCongratulations.value = false
      showFlamouTimer.value = false

      saveData()
      loadInitialBatch()
    }

    function goToDashboard() {
      window.location.href = '/dashboard'
    }

    function goToNextGame() {
      window.location.href = '/game-speed'
    }

    function goToJobDetails() {
      // window.location.href = `/metier/${job.id}`;
    }

    function checkBadges() {
      // Vérifier l'obtention de badges en fonction du nombre de métiers vus
      if (seenJobs.value.length >= 5 && !isBadgeUnlocked('explorer_debutant')) {
        unlockBadge(
          'explorer_debutant',
          'Explorateur Débutant',
          'Tu as découvert 5 métiers différents !',
        )
      } else if (
        seenJobs.value.length >= 20 &&
        !isBadgeUnlocked('explorer_avance')
      ) {
        unlockBadge(
          'explorer_avance',
          'Explorateur Avancé',
          'Tu as découvert 20 métiers différents !',
        )
      } else if (
        seenJobs.value.length >= 40 &&
        !isBadgeUnlocked('explorer_expert')
      ) {
        unlockBadge(
          'explorer_expert',
          'Explorateur Expert',
          'Tu as découvert 40 métiers différents !',
        )
      }

      // Vérifier les badges pour les métiers aimés
      if (
        likedJobs.value.length >= 5 &&
        !isBadgeUnlocked(badgeJobDiscoveryId.value)
      ) {
        unlockJobDiscoveryBadge()
      }
    }

    function unlockJobDiscoveryBadge() {
      if (!isBadgeUnlocked(badgeJobDiscoveryId.value)) {
        const badgeUnlocked = unlockBadge(badgeJobDiscoveryId.value)
        if (badgeUnlocked) {
          setTimeout(() => {
            showBadgeUnlockAnimation.value = true
          }, 1500)
        }
      }
    }

    function closeBadgeAnimation() {
      showBadgeUnlockAnimation.value = false
    }

    // Démarrer le timer de Flamou
    function startFlamouTimer(duration = 3000) {
      flamouTimeLeft.value = duration
      flamouTimerProgress.value = 100
      showFlamouTimer.value = true
      
      // Nettoyer le timer existant
      if (flamouTimer.value) {
        clearInterval(flamouTimer.value)
      }
      
      flamouTimer.value = setInterval(() => {
        flamouTimeLeft.value -= 100
        flamouTimerProgress.value = (flamouTimeLeft.value / duration) * 100
        
        if (flamouTimeLeft.value <= 0) {
          clearInterval(flamouTimer.value)
          flamouTimer.value = null
          showFlamouTimer.value = false
          showFlamouCongratulations.value = false
          
          // Démarrer un délai d'attente avant de permettre la prochaine action
          startAutoAdvanceDelay()
        }
      }, 100)
    }
    
    // Démarrer le délai d'attente après la disparition de Flamou
    function startAutoAdvanceDelay() {
      autoAdvanceTimer.value = setTimeout(() => {
        // Permettre la prochaine action (pas d'auto-advance dans ce jeu)
        console.log('Auto-advance delay finished')
      }, 1000) // 1 seconde de délai après la disparition de Flamou
    }
    
    // Nettoyer tous les timers
    function clearAllTimers() {
      if (flamouTimer.value) {
        clearInterval(flamouTimer.value)
        flamouTimer.value = null
      }
      if (flamouCompletionTimer.value) {
        clearTimeout(flamouCompletionTimer.value)
        flamouCompletionTimer.value = null
      }
      if (autoAdvanceTimer.value) {
        clearTimeout(autoAdvanceTimer.value)
        autoAdvanceTimer.value = null
      }
    }

    // Fonction pour afficher les félicitations de Flamou
    function displayFlamouCongratulations(responseType) {
      let messages = []
      let image = flamouNormal
      
      if (responseType === 'like') {
        messages = [
          "Super choix ! Ce métier a l'air génial !",
          "J'adore ta passion pour ce métier !",
          "Excellent ! Tu as l'air d'avoir trouvé quelque chose qui te plaît !",
          "Bravo ! Ce métier pourrait vraiment te correspondre !",
          "Fantastique ! Tu explores bien tes intérêts !",
          "Génial ! Continue à explorer tes passions !",
          "Parfait ! Tu as du goût pour les bons métiers !",
          "Waouh ! Ce métier semble fait pour toi !"
        ]
        image = Math.random() > 0.5 ? flamouHappy : flamouHappy2
      } else if (responseType === 'dislike') {
        messages = [
          "Pas de souci ! Il faut savoir ce qu'on ne veut pas !",
          "C'est bien de connaître ses préférences !",
          "Très bien ! Continue à explorer d'autres options !",
          "Parfait ! Tu affines tes choix !",
          "Excellent ! Tu sais ce qui ne te convient pas !",
          "Bien joué ! Continue à chercher ton métier idéal !",
          "Super ! Tu apprends à mieux te connaître !",
          "Bravo ! Chaque non t'approche de ton oui !"
        ]
        image = Math.random() > 0.5 ? flamouNormal : flamouHey
      }
      
      const randomMessage = messages[Math.floor(Math.random() * messages.length)]
      
      flamouCongratulationsMessage.value = randomMessage
      flamouCongratulationsImage.value = image
      showFlamouCongratulations.value = true
      
      // Démarrer le timer de 3 secondes
      startFlamouTimer(3000)
    }

    // Initialisation
    onMounted(() => {
      // Vérifier que metiersData est correctement importé
      console.log('Nombre de métiers disponibles:', metiersData.length)
    })

    return {
      // État du jeu
      gameStarted,
      showResults,
      currentIndex,
      currentBatch,
      batchSize,
      seenJobs,
      likedJobs,
      currentBatchIds,
      batchCompleted,
      allJobsSeen,
      highContrastMode,

      // Données calculées
      progressPercentage,
      currentMetier,
      availableJobs,

      // Animation du badge
      showBadgeUnlockAnimation,
      badgeData,
      isBatchComplete,
      badgeJobDiscoveryId,

      // Méthodes
      startGame,
      getVideoSource,
      loadSavedData,
      saveData,
      getLikedJobsInCurrentBatch,
      loadInitialBatch,
      loadNextBatch,
      likeJob,
      dislikeJob,
      showDetails,
      nextCard,
      finishAndShowResults,
      restartGame,
      goToDashboard,
      goToNextGame,
      goToJobDetails,
      checkBadges,
      closeBadgeAnimation,
      sendJobChoiceToBackend,
      saveJobChoicesLocally,
      unknownJob,
      jobVideo,
      handleVideoLoaded,
      handleVideoPlay,
      handleVideoError,
      tryAutoplayVideo,
      showGameModal,
      timeRemaining,
      startTimer,
      stopTimer,
      resetTimer,
      getRandomGameRoute,
      closeModal,
      flamouImage,

      // Variables pour les félicitations de Flamou
      showFlamouCongratulations,
      flamouCongratulationsImage,
      flamouCongratulationsMessage,
      displayFlamouCongratulations,
      flamouTimer,
      flamouTimeLeft,
      flamouTimerProgress,
      showFlamouTimer,
      startFlamouTimer,
      clearAllTimers,
    }
  },
}
</script>

<style scoped>
/* Base Styles */
.job-discovery-container {
  font-family: 'Comic Sans MS', 'Chalkboard SE', 'Marker Felt', sans-serif;
  max-width: 1100px;
  margin: 0 auto;
  padding: 20px;
  color: #333;
  min-height: 100vh;
}

/* Game Header */
.game-header {
  text-align: center;
  margin-bottom: 30px;
}

.main-title {
  font-size: 2.5rem;
  color: #ff6b6b;
  margin-bottom: 10px;
  text-align: center;
  position: relative;
  padding-bottom: 10px;
}

.main-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 4px;
  background-color: #4ecdc4;
  border-radius: 2px;
}

.subtitle {
  font-size: 1.2rem;
  color: #666;
  margin: 0;
}

/* Guide Character */
.guide-character {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
}

.guide-avatar {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  border: 3px solid #ffc107;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.speech-bubble {
  position: relative;
  background-color: #fff;
  border-radius: 15px;
  padding: 15px;
  margin-left: 15px;
  box-shadow: 0 3px 5px rgba(0, 0, 0, 0.1);
  max-width: 70%;
}

.speech-bubble:before {
  content: '';
  position: absolute;
  left: -10px;
  top: 50%;
  transform: translateY(-50%);
  border-width: 10px 10px 10px 0;
  border-style: solid;
  border-color: transparent #fff transparent transparent;
}

.speech-bubble p {
  margin: 0;
  font-size: 1.1rem;
  color: #333;
  line-height: 1.5;
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
  box-shadow: 0 0 30px rgba(255, 107, 107, 0.6);
  animation: scaleIn 0.5s ease-out;
}

.badge-unlock-animation .badge-icon {
  font-size: 80px;
  margin-bottom: 20px;
  animation: pulse 2s infinite;
  color: #ff6b6b;
}

.badge-unlock-animation h2 {
  color: #ff6b6b;
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
  background-color: #ff6b6b;
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
  background-color: #ff5252;
  transform: scale(1.05);
}

/* Welcome Screen */
.welcome-screen {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  align-items: center;
  margin: 40px 0;
  justify-content: center;
}

.welcome-card {
  flex: 1;
  min-width: 300px;
  max-width: 600px;
  background-color: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 20px;
  color: #ff6b6b;
}

.large-icon {
  font-size: 5rem;
  margin-bottom: 20px;
}

.welcome-card h2 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 20px;
}

.instructions-list {
  text-align: left;
  padding-left: 10px;
  margin-bottom: 30px;
}

.instructions-list li {
  margin-bottom: 15px;
  font-size: 1.1rem;
  display: flex;
  align-items: flex-start;
  gap: 15px;
}

.instruction-step {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  background-color: #ff6b6b;
  color: white;
  border-radius: 50%;
  flex-shrink: 0;
}

.sub-instructions {
  list-style-type: none;
  padding-left: 0;
  margin-top: 10px;
}

.sub-instructions li {
  margin-bottom: 8px;
  font-size: 0.95rem;
}

.start-button {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 15px 30px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  margin-top: 20px;
}

.start-button:hover {
  background-color: #388e3c;
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
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
  background-color: #ff6b6b;
  color: white;
  border-color: #ff6b6b;
}

.progress-step.completed .step-label {
  color: #ff6b6b;
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
  background: linear-gradient(90deg, #ff6b6b, #ff8e8e);
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

/* Game Content */
.game-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 30px auto;
  position: relative;
  width: 100%;
  max-width: 800px;
  min-height: 500px;
}

/* Job Card */
.job-card {
  width: 100%;
  background-color: white;
  border-radius: 20px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.5s ease;
}

.job-card-inner {
  padding: 20px;
}

.job-title {
  font-size: 1.8rem;
  color: #ff6b6b;
  text-align: center;
  margin: 0 0 20px 0;
  padding-bottom: 10px;
  border-bottom: 2px solid #f0f0f0;
}

/* Intégration de vidéo */
.job-media {
  margin-bottom: 20px;
  text-align: center;
}

.video-player {
  position: relative;
  width: 100%;
  padding-top: 56.25%; /* Ratio 16:9 */
  margin-bottom: 20px;
  border-radius: 10px;
  overflow: hidden;
  background-color: #f5f5f5;
}

.video-element {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Indicateur de lecture automatique */
.video-player::after {
  content: '▶️ Lecture automatique';
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 0.8rem;
  opacity: 0;
  animation: showAutoplayIndicator 2s ease-in-out;
}

@keyframes showAutoplayIndicator {
  0%,
  100% {
    opacity: 0;
  }
  20%,
  80% {
    opacity: 1;
  }
}

.video-placeholder {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
}

/* Animation pour la transition entre vidéos */
.video-element {
  transition: opacity 0.3s ease;
}

/* Style pour les vidéos en cours de chargement */
.video-element[data-loading='true'] {
  opacity: 0.7;
}

.placeholder-icon {
  font-size: 3rem;
  margin-bottom: 15px;
  opacity: 0.5;
}

.job-description {
  font-size: 1.1rem;
  color: #555;
  margin-bottom: 20px;
  line-height: 1.6;
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 10px;
}

.job-skills {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 15px;
}

.skill-tag {
  background-color: #e8f5e9;
  color: #2e7d32;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: bold;
}

/* Card Actions */
.card-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 20px;
  margin-bottom: 20px;
}

.action-button {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  border: none;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.action-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.like-button {
  background-color: #4caf50;
  color: white;
}

.like-button:hover {
  background-color: #388e3c;
}

.dislike-button {
  background-color: #f44336;
  color: white;
}

.dislike-button:hover {
  background-color: #d32f2f;
}

.info-button {
  background-color: #2196f3;
  color: white;
}

.info-button:hover {
  background-color: #1976d2;
}

/* Batch complete et All jobs seen cards */
.batch-complete-card,
.all-jobs-seen-card,
.loading-card {
  width: 100%;
  max-width: 600px;
  background-color: white;
  border-radius: 20px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  padding: 30px;
  text-align: center;
  animation: fadeIn 0.5s ease;
}

.batch-complete-card h2,
.all-jobs-seen-card h2 {
  font-size: 2rem;
  color: #ff6b6b;
  margin-bottom: 20px;
}

.batch-complete-card p,
.all-jobs-seen-card p {
  font-size: 1.1rem;
  color: #555;
  margin-bottom: 10px;
  line-height: 1.5;
}

.batch-actions,
.home-action {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 30px;
}

.continue-button {
  background-color: #4caf50;
  color: white;
}

.continue-button:hover {
  background-color: #388e3c;
}

.finish-button {
  background-color: #ff9800;
  color: white;
}

.finish-button:hover {
  background-color: #f57c00;
}

.dashboard-button {
  background-color: #607d8b;
  color: white;
}

.dashboard-button:hover {
  background-color: #455a64;
}

/* Loading animation */
.loading-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #ff6b6b;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Card Transition */
.card-transition-enter-active,
.card-transition-leave-active {
  transition: all 0.5s ease;
}

.card-transition-enter-from,
.card-transition-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

/* Results Overlay */
.results-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.5s ease;
}

.results-modal {
  background-color: white;
  border-radius: 20px;
  padding: 30px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
  animation: scaleIn 0.5s ease;
}

.results-header {
  text-align: center;
  margin-bottom: 30px;
}

.results-title-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  margin-bottom: 10px;
}

.results-title-icon {
  font-size: 2.5rem;
  color: #ff6b6b;
}

.results-title {
  font-size: 2rem;
  color: #333;
  margin: 0;
}

.results-subtitle {
  font-size: 1.2rem;
  color: #666;
  margin: 0;
}

/* Liked Jobs Grid */
.liked-jobs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.liked-job-item {
  background-color: #f5f5f5;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
}

.liked-job-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.liked-job-media {
  position: relative;
  height: 140px;
  overflow: hidden;
}

.liked-job-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.play-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 2.5rem;
  color: white;
  text-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  opacity: 0.8;
  transition:
    opacity 0.3s ease,
    transform 0.3s ease;
}

.liked-job-item:hover .play-overlay {
  opacity: 1;
  transform: translate(-50%, -50%) scale(1.1);
}

.liked-job-info {
  padding: 15px;
}

.liked-job-info h3 {
  font-size: 1.1rem;
  color: #333;
  margin: 0 0 15px 0;
}

.view-button {
  display: block;
  width: 100%;
  padding: 8px 0;
  background-color: #ff6b6b;
  color: white;
  border: none;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
}

.view-button:hover {
  background-color: #ff5252;
}

.no-liked-jobs {
  text-align: center;
  padding: 40px 20px;
  background-color: #f9f9f9;
  border-radius: 15px;
  margin-bottom: 30px;
}

.no-liked-jobs p {
  color: #666;
  font-size: 1.1rem;
  margin: 10px 0;
}

.results-actions {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 15px;
  margin-top: 30px;
}

.restart-button {
  background-color: #ff9800;
  color: white;
}

.restart-button:hover {
  background-color: #f57c00;
}

.next-game-button {
  background-color: #9c27b0;
  color: white;
}

.next-game-button:hover {
  background-color: #7b1fa2;
}

.home-button {
  background-color: #607d8b;
  color: white;
}

.home-button:hover {
  background-color: #455a64;
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

/* Félicitations de Flamou */
.flamou-congratulations-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1500;
  animation: fadeIn 0.3s ease-out;
}

.flamou-congratulations-container {
  display: flex;
  align-items: center;
  gap: 20px;
  animation: scaleIn 0.4s ease-out;
}

.flamou-congratulations-image {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 4px solid #ff6b6b;
  background-color: #fff;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
  animation: bounce 0.6s ease-out;
}

.flamou-speech-bubble {
  position: relative;
  background-color: #fff;
  border-radius: 20px;
  padding: 20px 25px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  max-width: 320px;
  border: 3px solid #ff6b6b;
}

.flamou-speech-bubble:before {
  content: '';
  position: absolute;
  left: -15px;
  top: 50%;
  transform: translateY(-50%);
  border-width: 15px 15px 15px 0;
  border-style: solid;
  border-color: transparent #ff6b6b transparent transparent;
}

.flamou-speech-bubble:after {
  content: '';
  position: absolute;
  left: -9px;
  top: 50%;
  transform: translateY(-50%);
  border-width: 12px 12px 12px 0;
  border-style: solid;
  border-color: transparent #fff transparent transparent;
}

.flamou-speech-bubble p {
  margin: 0;
  font-size: 1.2rem;
  color: #333;
  line-height: 1.4;
  font-weight: bold;
  text-align: center;
}

/* Timer de Flamou */
.flamou-timer {
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.flamou-timer-bar {
  width: 80px;
  height: 5px;
  background-color: #e0e0e0;
  border-radius: 3px;
  overflow: hidden;
}

.flamou-timer-fill {
  height: 100%;
  background: linear-gradient(90deg, #ff6b6b, #ff8e8e);
  border-radius: 3px;
  transition: width 0.1s linear;
}

.flamou-timer-text {
  font-size: 0.9rem;
  color: #666;
  font-weight: bold;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  25% {
    transform: translateY(-10px);
  }
  75% {
    transform: translateY(-5px);
  }
}

/* Responsive styles */
@media (max-width: 768px) {
  .card-actions {
    flex-wrap: wrap;
  }

  .action-button {
    width: 100%;
  }

  .video-player {
    padding-top: 75%; /* Ajuster le ratio pour les petits écrans */
  }

  .instructions-list li {
    align-items: flex-start;
  }

  .instruction-step {
    margin-top: 2px;
  }

  .results-modal {
    width: 95%;
    padding: 20px;
  }

  .liked-jobs-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }

  /* Félicitations de Flamou sur mobile */
  .flamou-congratulations-container {
    flex-direction: column;
    padding: 20px;
  }

  .flamou-congratulations-image {
    width: 100px;
    height: 100px;
  }

  .flamou-speech-bubble {
    max-width: 280px;
    padding: 15px 20px;
  }

  .flamou-speech-bubble:before {
    left: 50%;
    top: -15px;
    transform: translateX(-50%);
    border-width: 0 15px 15px 15px;
    border-color: transparent transparent #ff6b6b transparent;
  }

  .flamou-speech-bubble:after {
    left: 50%;
    top: -9px;
    transform: translateX(-50%);
    border-width: 0 12px 12px 12px;
    border-color: transparent transparent #fff transparent;
  }

  .flamou-speech-bubble p {
    font-size: 1.1rem;
  }
}

@media (max-width: 480px) {
  .main-title {
    font-size: 2rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .guide-character {
    flex-direction: column;
    text-align: center;
  }

  .guide-avatar {
    margin-bottom: 15px;
  }

  .speech-bubble {
    margin-left: 0;
  }

  .speech-bubble:before {
    display: none;
  }

  .progress-steps {
    display: none; /* Cacher les étapes sur très petit écran */
  }

  .liked-jobs-grid {
    grid-template-columns: 1fr;
  }

  /* Félicitations de Flamou sur très petits écrans */
  .flamou-congratulations-image {
    width: 80px;
    height: 80px;
  }

  .flamou-speech-bubble {
    max-width: 250px;
    padding: 12px 16px;
  }

  .flamou-speech-bubble p {
    font-size: 1rem;
  }
}
</style>
