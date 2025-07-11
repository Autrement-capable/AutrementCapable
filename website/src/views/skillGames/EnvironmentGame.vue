<template>
  <div class="environment-container">
    <GameGuide
      v-if="!activityStarted"
      gameId="sensory-environment"
      :forceShow="true"
      @start-game="startActivity"
      @skip-intro="startActivity"
    />

    <!-- Section principale avec les environnements -->
    <div v-else class="main-interface">
      <!-- Popup d'explication de Flamou -->
      <div v-if="showFlamouExplanation" class="flamou-explanation-overlay">
        <div class="flamou-explanation-container">
          <div class="flamou-character">
            <img :src="flamouImage" alt="Flamou" class="flamou-avatar" />
          </div>
          <div class="flamou-speech-bubble">
            <h2>{{ flamouExplanation.title }}</h2>
            <p>{{ flamouExplanation.message }}</p>
            <div class="flamou-instructions">
              <h3>Ce que tu vas faire :</h3>
              <ul>
                <li v-for="(instruction, index) in flamouExplanation.instructions" :key="index">
                  {{ instruction }}
                </li>
              </ul>
            </div>
            <button @click="startExploration" class="flamou-continue-button">
              {{ flamouExplanation.buttonText }}
            </button>
          </div>
        </div>
      </div>

      <!-- Visualisation plein écran du RoomRenderer -->
      <div class="fullscreen-renderer">
        <!-- Visualisation de la pièce en plein écran -->
        <div class="room-visualization" ref="container"></div>

        <!-- Questions séquentielles en bas de l'écran -->
        <div v-if="showQuestion" class="question-overlay">
          <div class="question-container">
            <h3>{{ currentQuestion.title }}</h3>
            <p>{{ currentQuestion.description }}</p>

            <!-- Conteneur de contrôles dynamiques en fonction du type de question -->
            <div class="question-controls">
              <!-- Lumière -->
              <div
                v-if="currentQuestion.type === 'light'"
                class="control-group"
              >
                <div class="big-button-group">
                  <button
                    @click="((lightIntensity = 0.8), updateLighting())"
                    :class="['big-button', { active: lightIntensity <= 1.2 }]"
                  >
                    <div class="big-button-icon">🌙</div>
                    <div class="big-button-label">Douce</div>
                  </button>

                  <button
                    @click="((lightIntensity = 2), updateLighting())"
                    :class="[
                      'big-button',
                      { active: lightIntensity > 1.2 && lightIntensity < 3 },
                    ]"
                  >
                    <div class="big-button-icon">☀️</div>
                    <div class="big-button-label">Normale</div>
                  </button>

                  <button
                    @click="((lightIntensity = 4), updateLighting())"
                    :class="['big-button', { active: lightIntensity >= 3 }]"
                  >
                    <div class="big-button-icon">🔆</div>
                    <div class="big-button-label">Forte</div>
                  </button>
                </div>
              </div>

              <!-- Couleur de lumière -->
              <div
                v-if="currentQuestion.type === 'lightColor'"
                class="control-group"
              >
                <div class="color-buttons">
                  <button
                    v-for="(preset, idx) in lightPresets"
                    :key="idx"
                    @click="selectLightPreset(preset)"
                    :class="[
                      'color-button',
                      { active: lightColor === preset.color },
                    ]"
                    :style="{ backgroundColor: preset.color }"
                  >
                    <span class="color-button-label">{{ preset.name }}</span>
                  </button>
                </div>
              </div>

              <!-- Couleurs de la pièce -->
              <div
                v-if="currentQuestion.type === 'colors'"
                class="control-group"
              >
                <div class="color-palettes">
                  <div
                    v-for="(palette, index) in colorPalettes"
                    :key="index"
                    @click="selectColorPalette(palette)"
                    :class="[
                      'color-palette',
                      { selected: isCurrentPalette(palette) },
                    ]"
                  >
                    <div class="palette-preview">
                      <div
                        class="color-preview"
                        :style="{ backgroundColor: palette.wall }"
                      ></div>
                      <div
                        class="color-preview"
                        :style="{ backgroundColor: palette.floor }"
                      ></div>
                      <div
                        class="color-preview"
                        :style="{ backgroundColor: palette.ceiling }"
                      ></div>
                    </div>
                    <span>{{ palette.name }}</span>
                  </div>
                </div>
              </div>

              <!-- Sons -->
              <div
                v-if="currentQuestion.type === 'sounds'"
                class="control-group"
              >
                <div class="sound-options">
                  <div
                    v-for="(sound, index) in soundOptions"
                    :key="index"
                    @click="selectSound(sound.value)"
                    :class="[
                      'sound-option',
                      { active: selectedAmbience === sound.value },
                    ]"
                  >
                    <div class="sound-icon">{{ sound.icon }}</div>
                    <div class="sound-label">{{ sound.label }}</div>
                  </div>
                </div>
                <div v-if="selectedAmbience !== 'none'" class="slider-control">
                  <label>Volume: {{ Math.round(soundVolume * 100) }}%</label>
                  <input
                    type="range"
                    v-model.number="soundVolume"
                    min="0"
                    max="1"
                    step="0.05"
                    @change="updateSoundVolume"
                  />
                </div>
              </div>

              <!-- Personnes -->
              <div
                v-if="currentQuestion.type === 'people'"
                class="control-group"
              >
                <div class="people-count-control">
                  <label>Nombre de personnes: {{ peopleCount }}</label>
                  <div class="people-selection">
                    <button
                      v-for="count in peopleOptions"
                      :key="count"
                      @click="((peopleCount = count), updatePeopleCount())"
                      :class="[
                        'people-button',
                        { active: peopleCount === count },
                      ]"
                    >
                      {{ count }}
                    </button>
                  </div>
                </div>
              </div>

              <!-- Ressenti -->
              <div v-if="currentQuestion.type === 'mood'" class="control-group">
                <div class="mood-selection">
                  <div
                    v-for="mood in moods"
                    :key="mood.value"
                    @click="selectMood(mood.value)"
                    :class="[
                      'mood-option',
                      { selected: getCurrentFeedback().mood === mood.value },
                    ]"
                  >
                    <div class="mood-emoji">{{ mood.emoji }}</div>
                    <div class="mood-label">{{ mood.label }}</div>
                  </div>
                </div>

                <div class="control-item">
                  <label>Commentaires courts:</label>
                  <textarea
                    v-model="getCurrentFeedback().comments"
                    placeholder="Ce que j'aime ou n'aime pas..."
                  ></textarea>
                </div>
              </div>
            </div>

            <div class="question-navigation">
              <button
                v-if="currentQuestionIndex > 0"
                @click="previousQuestion()"
                class="nav-button prev-button"
              >
                Précédent
              </button>
              <button
                v-if="currentQuestionIndex < questions.length - 1"
                @click="nextQuestion()"
                class="nav-button next-button"
              >
                Suivant
              </button>
              <button
                v-if="currentQuestionIndex === questions.length - 1"
                @click="finishExploration()"
                class="nav-button finish-button"
              >
                Terminer
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Messages d'aide et guides contextuels -->
      <div v-if="showGuide" class="guide-overlay">
        <div class="guide-content">
          <h3>{{ currentGuide.title }}</h3>
          <p>{{ currentGuide.description }}</p>
          <button @click="dismissGuide" class="guide-button">Continuer</button>
        </div>
      </div>

      <!-- Flamou Loading overlay for 3D models -->
      <div v-if="modelsLoading" class="flamou-loading-overlay">
        <div class="flamou-loading-container">
          <div class="flamou-loading-character">
            <img :src="flamouImage" alt="Flamou" class="flamou-loading-avatar" />
            <div class="loading-speech-bubble">
              <div class="loading-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
          
          <div class="flamou-loading-content">
            <h3>{{ getCurrentLoadingMessage() }}</h3>
            <div class="flamou-loading-bar">
              <div
                class="flamou-loading-progress"
                :style="{ width: loadingProgress + '%' }"
              ></div>
            </div>
            <div class="flamou-loading-text">
              {{ Math.round(loadingProgress) }}% - {{ getCurrentLoadingDetail() }}
            </div>
            <div v-if="currentLoadingItem" class="flamou-loading-item">
              {{ currentLoadingItem }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Popup de choix Flamou -->
    <div v-if="showFlamouChoice" class="flamou-choice-overlay">
      <div class="flamou-choice-container">
        <div class="flamou-character">
          <img :src="flamouImage" alt="Flamou" class="flamou-avatar" />
        </div>
        <div class="flamou-speech-bubble">
          <h2>{{ getCompletionMessage() }}</h2>
          <p>{{ getCompletionDescription() }}</p>
          
          <div class="flamou-choices">
            <div v-if="!isLastEnvironment" class="choice-option" @click="goToNextRoom">
              <div class="choice-icon">🏠</div>
              <h3>Explorer la {{ getNextRoomNumber() }}ème salle</h3>
              <p>Découvre un nouvel environnement avec d'autres paramètres à personnaliser</p>
            </div>
            
            <div class="choice-option" @click="changeGame">
              <div class="choice-icon">🎮</div>
              <h3>Changer de jeu</h3>
              <p>Passe à une autre activité pour continuer ton exploration</p>
            </div>

            <div class="choice-option" @click="returnToDashboard">
              <div class="choice-icon">🏡</div>
              <h3>Retour au tableau de bord</h3>
              <p>Reviens au menu principal pour voir ton profil et tes progrès</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Audio pour l'ambiance sonore -->
    <audio ref="ambientAudio" loop preload="auto" v-show="false"></audio>
  </div>
</template>

<script>
// Import our isolated RoomRenderer class
import RoomRenderer from '../../roomRenderer/RoomRenderer.js'
import whiteNoiseAudio from '@/assets/sounds/white_noise.mp3'
import NatureAudio from '@/assets/sounds/nature.mp3'
import CafeAudio from '@/assets/sounds/cafe.mp3'
import CrowdAudio from '@/assets/sounds/crowd.mp3'
import GameGuide from '@/components/GameGuideComponent.vue'
import AuthService from '@/services/AuthService'
import flamouNormalImage from '@/assets/flamou/normal.png'

export default {
  name: 'SensoryEnvironments',
  components: {
    GameGuide,
  },
  data() {
    return {
      // Interface state
      activityStarted: false,
      currentEnvironmentIndex: 0,
      showFlamouChoice: false,
      rendererInitialized: false,
      showFlamouExplanation: false,
      currentLoadingItem: '',
      showQuestion: false,
      currentQuestionIndex: 0,
      currentRoomName: '',
      completedRooms: new Set(),

      // Questions séquentielles
      questions: [
        {
          type: 'sounds',
          title: 'Ambiance sonore?',
          description: "Quel type de son te met à l'aise?",
        },
        {
          type: 'light',
          title: 'Intensité de lumière?',
          description: "Choisis l'intensité qui te convient le mieux.",
        },
        {
          type: 'lightColor',
          title: 'Couleur de lumière?',
          description: 'Quelle teinte de lumière préfères-tu?',
        },
        {
          type: 'colors',
          title: 'Couleurs de la pièce?',
          description: 'Choisis une palette de couleur qui te plaît.',
        },
        {
          type: 'people',
          title: 'Personnes présentes?',
          description: 'Combien de personnes autour de toi peux-tu suporter?',
        },
        {
          type: 'mood',
          title: 'Comment te sens-tu?',
          description: 'Ton ressenti dans cet environnement.',
        },
      ],

      // Options de son
      soundOptions: [
        { value: 'none', icon: '🔇', label: 'Silence' },
        { value: 'whitenoise', icon: '📻', label: 'Bruit blanc' },
        { value: 'nature', icon: '🌳', label: 'Nature' },
        { value: 'cafe', icon: '☕', label: 'Café' },
        { value: 'crowd', icon: '👥', label: 'Bureau' },
      ],
      peopleOptions: [0, 1, 3, 5, 10],

      // Guide
      showGuide: false,
      currentGuide: {
        title: '',
        description: '',
      },

      // Loading
      modelsLoading: false,
      loadingProgress: 0,

      // Données utilisateur
      userData: {
        environmentFeedback: {},
        overallFavorite: null,
      },

      // Liste des environnements prédéfinis
      environments: [
        {
          name: 'Espace Polyvalent (Concentration & Détente)',
          shortDescription:
            'Environnement modulable pour travail et relaxation',
          description:
            'Un espace hybride offrant des zones dédiées à la concentration intellectuelle et à la détente sensorielle, avec des paramètres personnalisables.',
          previewColor: '#7986CB', // A blend color
          imageSrc: '/images/concentration_space.png', // Placeholder, ideally a new image like '/images/polyvalent_space.png'
          icon: '🛋️', // Icône canapé
          objectsCategory: 'polyvalent', // New category for RoomRenderer
          defaultSettings: {
            room: {
              width: 9,
              depth: 9,
              height: 3.2,
              wallColor: '#eaf0f5', // Blend of '#f0f0f5' (concentration) and '#e6f0f5' (détente)
              floorColor: '#a0a8c4', // Blend of '#6a75a3' (concentration) and '#d1dde6' (détente)
              ceilingColor: '#f8fafc', // Blend of '#ffffff' (concentration) and '#f0f7fa' (détente)
            },
            lighting: {
              color: '#f8f8ff', // Slightly off-white, between '#ffffff' and '#f0f7fa'
              intensity: 1.6, // Average of 2 (concentration) and 1.2 (détente)
              ambient: true,
            },
            sound: {
              type: 'whitenoise', // Default to 'whitenoise'
              volume: 0.25, // Average of 0.2 (concentration) and 0.3 (détente)
              peopleCount: 0,
            },
            clutter: 'moderate', // To accommodate items from both zones
          },
        },
        {
          name: 'Espace social contrôlé',
          shortDescription: 'Pour les interactions en petit groupe',
          description:
            'Un espace conçu pour des interactions sociales maîtrisées avec un niveau de stimulation modéré et des zones de repli.',
          previewColor: '#FFA726',
          imageSrc: '/images/social_space.png',
          icon: '👥',
          objectsCategory: 'social',
          defaultSettings: {
            room: {
              width: 9,
              depth: 9,
              height: 3.2,
              wallColor: '#fff9e6',
              floorColor: '#d9c298',
              ceilingColor: '#fffcf0',
            },
            lighting: {
              color: '#ffe0b2',
              intensity: 1.5,
              ambient: true,
            },
            sound: {
              type: 'cafe',
              volume: 0.4,
              peopleCount: 0,
            },
            clutter: 'moderate',
          },
        },
      ],

      // Moods pour le feedback
      moods: [
        { value: 'veryCalm', emoji: '😌', label: 'Très calme' },
        { value: 'focused', emoji: '🧠', label: 'Concentré' },
        { value: 'comfortable', emoji: '😊', label: 'Confortable' },
        { value: 'neutral', emoji: '😐', label: 'Neutre' },
        { value: 'uneasy', emoji: '😟', label: "Mal à l'aise" },
        { value: 'overwhelmed', emoji: '😣', label: 'Surstimulé' },
      ],

      // Paramètres actuels de la pièce
      roomWidth: 9,
      roomDepth: 9,
      roomHeight: 3.2,
      wallColor: '#e0e0e0',
      floorColor: '#ad8a64',
      ceilingColor: '#f5f5f5',

      // Paramètres d'éclairage
      lightColor: '#ffffff',
      lightIntensity: 1.5,
      ambientLight: true,

      // Préréglages de lumière
      lightPresets: [
        { name: 'Neutre', color: '#ffffff' },
        { name: 'Chaud', color: '#ffe0b2' },
        { name: 'Froid', color: '#b3e5fc' },
        { name: 'Doux', color: '#f0e6ff' },
        { name: 'Naturel', color: '#fff8e1' },
      ],

      // Palettes de couleurs
      colorPalettes: [
        {
          name: 'Neutre',
          wall: '#e0e0e0',
          floor: '#ad8a64',
          ceiling: '#f5f5f5',
        },
        {
          name: 'Apaisant',
          wall: '#e6f0f5',
          floor: '#d1dde6',
          ceiling: '#f0f7fa',
        },
        {
          name: 'Chaleureux',
          wall: '#fff5e6',
          floor: '#d9b38c',
          ceiling: '#fffaf0',
        },
        {
          name: 'Naturel',
          wall: '#e8f4e5',
          floor: '#8ba987',
          ceiling: '#f5f7f5',
        },
        {
          name: 'Concentration',
          wall: '#f0f0f5',
          floor: '#6a75a3',
          ceiling: '#ffffff',
        },
        {
          name: 'Sensoriel doux',
          wall: '#f8e9e6',
          floor: '#c8b7b4',
          ceiling: '#fdf6f5',
        },
      ],

      // Paramètres audio
      soundEnabled: false,
      soundVolume: 0.5,
      selectedAmbience: 'none',
      peopleCount: 0,

      // Renderer
      renderer: null,

      // Flamou explanation data
      flamouImage: flamouNormalImage,
      flamouExplanation: {
        title: 'Salut ! Je suis Flamou 👋',
        message: 'Je vais t\'aider à découvrir quel environnement te convient le mieux pour te sentir à l\'aise et bien concentré(e).',
        instructions: [
          'Tu vas explorer un espace virtuel en 3D',
          'Je vais te poser des questions sur tes préférences',
          'Tu pourras ajuster la lumière, les couleurs et les sons',
          'À la fin, tu auras des conseils personnalisés !'
        ],
        buttonText: 'C\'est parti ! 🚀'
      },

      // Messages de chargement Flamou
      loadingMessages: [
        'Je prépare ton nouvel espace... 🏗️',
        'J\'installe les meubles parfaits pour toi ! 🪑',
        'Je règle l\'éclairage comme tu l\'aimes... 💡',
        'Presque fini ! Je fais les derniers ajustements... ✨',
        'Ton environnement sera bientôt prêt ! 🎨'
      ],
      loadingDetails: [
        'Création de l\'ambiance...',
        'Positionnement des objets...',
        'Optimisation de l\'éclairage...',
        'Finalisation des détails...',
        'Dernières touches magiques...'
      ],
    }
  },
  computed: {
    currentEnvironment() {
      return (
        this.environments[this.currentEnvironmentIndex] || this.environments[0]
      )
    },
    currentQuestion() {
      return this.questions[this.currentQuestionIndex] || this.questions[0]
    },
    isLastEnvironment() {
      return this.currentEnvironmentIndex >= this.environments.length - 1
    },
  },
  mounted() {
    this.initRenderer()
  },
  beforeUnmount() {
    // Clean up
    if (this.renderer) {
      this.renderer.dispose()
      this.renderer = null
    }

    // Stop audio
    if (this.$refs.ambientAudio) {
      this.$refs.ambientAudio.pause()
    }
  },
  methods: {
    async resetAllData() {
      // try {
      //   // Réinitialiser au backend avec le nouveau format
      //   const emptyPayload = {
      //     completion: 0,
      //     message: "Success",
      //     roomData: []
      //   }

      //   await AuthService.request('post', '/games/room-env', emptyPayload)
      //   console.log('Données réinitialisées au backend')
      // } catch (error) {
      //   console.warn('Impossible de réinitialiser au backend, réinitialisation locale uniquement')
      // }

      // Réinitialiser le Set des rooms complétées
      this.completedRooms.clear()

      // Réinitialiser localStorage
      localStorage.removeItem('roomEnvironmentData')
      localStorage.removeItem('completedRooms')

      console.log('Toutes les données ont été réinitialisées')
    },

    async loadSavedRoomData() {
      // Ne charger que si le Set est vide, pour éviter d'écraser les données en cours
      if (this.completedRooms.size > 0) {
        console.log('Completed rooms already in memory, skipping load')
        return
      }

      try {
        const response = await AuthService.request('get', '/games/room-env')
        if (
          response.data &&
          response.data.roomData &&
          Array.isArray(response.data.roomData) &&
          response.data.roomData.length > 0
        ) {
          // Restaurer le Set des rooms complétées à partir des données du backend
          this.completedRooms.clear()
          response.data.roomData.forEach((roomData) => {
            this.completedRooms.add(roomData.room)
          })
          console.log('Loaded completed rooms from backend:', Array.from(this.completedRooms))
        }
      } catch (error) {
        console.warn(
          'Impossible de charger depuis le backend, tentative locale...',
        )

        // Charger depuis localStorage
        const localPayload = JSON.parse(
          localStorage.getItem('roomEnvironmentData') || '{"roomData": []}',
        )
        const savedCompletedRooms = JSON.parse(
          localStorage.getItem('completedRooms') || '[]',
        )

        if (
          localPayload.roomData &&
          Array.isArray(localPayload.roomData) &&
          localPayload.roomData.length > 0
        ) {
          // Restaurer le Set des rooms complétées depuis les données locales
          this.completedRooms.clear()
          localPayload.roomData.forEach((roomData) => {
            this.completedRooms.add(roomData.room)
          })
          console.log('Loaded completed rooms from local:', Array.from(this.completedRooms))
        } else if (savedCompletedRooms.length > 0) {
          // Fallback: utiliser l'ancien format si disponible
          this.completedRooms.clear()
          savedCompletedRooms.forEach((roomName) => {
            this.completedRooms.add(roomName)
          })
          console.log('Loaded completed rooms from fallback:', Array.from(this.completedRooms))
        }
      }
    },

    calculateCompletion() {
      const totalRooms = 2 // Focus Room et Open Room
      const completedRoomsArray = Array.from(this.completedRooms)
      const completedCount = completedRoomsArray.length

      console.log('=== Calculate Completion Debug ===')
      console.log('Total rooms expected:', totalRooms)
      console.log('Completed rooms array:', completedRoomsArray)
      console.log('Completed count:', completedCount)

      // Vérification spécifique des rooms attendues
      const expectedRooms = ['Focus Room', 'Open Room']
      const hasAllExpectedRooms = expectedRooms.every((room) =>
        this.completedRooms.has(room),
      )

      console.log('Expected rooms:', expectedRooms)
      console.log('Has all expected rooms:', hasAllExpectedRooms)
      
      expectedRooms.forEach(room => {
        console.log(`Has "${room}":`, this.completedRooms.has(room))
      })

      if (completedCount === 0) return 0
      if (completedCount === 1) return 0.5
      if (completedCount >= 2 || hasAllExpectedRooms) return 1.0

      const result = Math.min(completedCount / totalRooms, 1.0)
      console.log('Final result:', result)
      return result
    },

    mapEnvironmentToRoomName(environmentName) {
      // Mapping plus strict avec trim pour éviter les problèmes d'espaces
      const cleanName = environmentName.trim()

      const mapping = {
        'Espace Polyvalent (Concentration & Détente)': 'Focus Room',
        'Espace social contrôlé': 'Open Room',
      }

      const result = mapping[cleanName] || 'Focus Room'

      console.log(`Mapping environment "${cleanName}" to room "${result}"`)
      return result
    },

    // Mapper l'intensité lumineuse numérique vers les valeurs API
    mapLightIntensity(intensity) {
      if (intensity <= 1.2) return 'low'
      if (intensity >= 3) return 'high'
      return 'normal'
    },

    // Mapper la couleur de lumière hex vers les présets API
    mapLightColor(colorHex) {
      const mapping = {
        '#ffffff': 'neutral',
        '#ffe0b2': 'hot',
        '#b3e5fc': 'cold',
        '#f0e6ff': 'soft',
        '#fff8e1': 'natural',
      }
      return mapping[colorHex] || 'neutral'
    },

    // Mapper les couleurs de room vers les palettes API
    mapRoomColor(wallColor, floorColor, ceilingColor) {
      // Comparer avec les palettes définies
      const palettes = this.colorPalettes
      for (let palette of palettes) {
        if (
          palette.wall === wallColor &&
          palette.floor === floorColor &&
          palette.ceiling === ceilingColor
        ) {
          const mapping = {
            Neutre: 'neutral',
            Apaisant: 'chill',
            Chaleureux: 'hot',
            Naturel: 'natural',
            Concentration: 'focus',
            'Sensoriel doux': 'soft',
          }
          return mapping[palette.name] || 'neutral'
        }
      }
      return 'neutral'
    },

    // Mapper le type d'ambiance sonore
    mapNoiseType(selectedAmbience) {
      const mapping = {
        none: 'silence',
        whitenoise: 'white noise',
        nature: 'natural',
        cafe: 'coffee',
        crowd: 'working',
      }
      return mapping[selectedAmbience] || 'silence'
    },

    // Mapper le mood utilisateur
    mapUserFeedback(mood) {
      const mapping = {
        veryCalm: 'very calm',
        focused: 'focused',
        comfortable: 'comfortable',
        neutral: 'neutral',
        uneasy: 'uncomfortable',
        overwhelmed: 'overstimulated',
      }
      return mapping[mood] || 'neutral'
    },

    // Construire les données à envoyer au backend
    buildRoomData(roomName) {
      const feedback = this.getCurrentFeedback()

      return {
        room: roomName,
        completion: 1.0,
        lightIntensity: this.mapLightIntensity(this.lightIntensity),
        lightColor: this.mapLightColor(this.lightColor),
        roomColor: this.mapRoomColor(
          this.wallColor,
          this.floorColor,
          this.ceilingColor,
        ),
        noiseType: this.mapNoiseType(this.selectedAmbience),
        noiseVolume: Math.round(this.soundVolume * 10),
        peopleInRoom: this.peopleCount,
        userFeedback: this.mapUserFeedback(feedback.mood),
        commentary: feedback.comments || '',
      }
    },

    // Sauvegarder les données d'une room au backend
    async saveRoomToBackend(roomName, roomData) {
      console.log(`Saving room: "${roomName}"`)
      console.log('Completed rooms before adding:', Array.from(this.completedRooms))
      
      this.completedRooms.add(roomName)
      console.log('Completed rooms after adding:', Array.from(this.completedRooms))
      
      const globalCompletion = this.calculateCompletion()
      console.log('Global completion:', globalCompletion)

      try {
        // Récupérer les données existantes
        let existingRoomData = []
        try {
          const response = await AuthService.request('get', '/games/room-env')
          if (
            response.data &&
            response.data.roomData &&
            Array.isArray(response.data.roomData)
          ) {
            existingRoomData = response.data.roomData
          }
        } catch (getError) {
          console.log(
            "Aucune donnée existante trouvée, création d'un nouveau dataset",
          )
        }

        // Supprimer l'ancienne version de cette room si elle existe
        existingRoomData = existingRoomData.filter(
          (room) => room.room !== roomName,
        )

        // Ajouter la nouvelle room data (roomData.completion reste à 1.0)
        existingRoomData.push(roomData)

        // Construire le payload final avec completion globale
        const payload = {
          completion: globalCompletion, // Completion globale basée sur nombre de rooms
          message: 'Success',
          roomData: existingRoomData,
        }

        const response = await AuthService.request(
          'post',
          '/games/room-env',
          payload,
        )
        console.log(
          `Données sauvegardées avec succès pour ${roomName}:`,
          response.data,
        )
        console.log(
          `Progression: ${this.completedRooms.size}/2 rooms complétées (${globalCompletion * 100}%)`,
        )
      } catch (error) {
        console.error(`Erreur lors de la sauvegarde pour ${roomName}:`, error)

        if (error.response) {
          console.error("Réponse d'erreur du serveur:", {
            status: error.response.status,
            statusText: error.response.statusText,
            data: error.response.data,
          })
        }

        // Sauvegarde locale en cas d'erreur
        this.saveRoomLocally(roomName, roomData, globalCompletion)
      }
    },

    // Sauvegarder localement en cas d'erreur backend
    saveRoomLocally(roomName, roomData, globalCompletion) {
      try {
        // Récupérer les données locales existantes
        let localPayload = JSON.parse(
          localStorage.getItem('roomEnvironmentData') ||
            '{"completion": 0, "message": "Success", "roomData": []}',
        )

        // S'assurer que la structure est correcte
        if (!localPayload.roomData || !Array.isArray(localPayload.roomData)) {
          localPayload.roomData = []
        }

        // Supprimer l'ancienne version de cette room si elle existe
        localPayload.roomData = localPayload.roomData.filter(
          (room) => room.room !== roomName,
        )

        // Ajouter la nouvelle room data (roomData.completion reste à 1.0)
        localPayload.roomData.push(roomData)

        // Mettre à jour SEULEMENT la completion globale
        localPayload.completion = globalCompletion

        // Sauvegarder
        localStorage.setItem(
          'roomEnvironmentData',
          JSON.stringify(localPayload),
        )

        // Sauvegarder aussi le Set des rooms complétées
        const completedRoomsArray = Array.from(this.completedRooms)
        localStorage.setItem(
          'completedRooms',
          JSON.stringify(completedRoomsArray),
        )

        console.log(
          `Données sauvegardées localement pour ${roomName}:`,
          localPayload,
        )
      } catch (error) {
        console.error('Erreur lors de la sauvegarde locale:', error)
      }
    },

    // Initialiser le renderer
    initRenderer() {
      if (this.$refs.container) {
        this.renderer = new RoomRenderer(this.$refs.container)

        // Set up loading progress callback
        this.renderer.setLoadingProgressCallback(
          (progress, total, currentItem) => {
            this.loadingProgress = progress
            this.currentLoadingItem = currentItem || ''

            // If progress is 100%, wait a moment before hiding the loading indicator
            if (progress >= 100) {
              setTimeout(() => {
                this.modelsLoading = false
              }, 500) // Short delay to ensure everything is rendered
            }
          },
        )

        // Attendre un court délai pour s'assurer que le renderer est prêt
        setTimeout(() => {
          this.rendererInitialized = true
          // Initialiser avec une pièce vide basique
          this.createBasicRoom()
        }, 500)
      }
    },

    // Créer une pièce basique initiale
    createBasicRoom() {
      if (!this.renderer || !this.rendererInitialized) return

      try {
        this.renderer.updateRoom(
          this.roomWidth,
          this.roomDepth,
          this.roomHeight,
          this.wallColor,
          this.floorColor,
          this.ceilingColor,
        )
      } catch (error) {
        console.error('Erreur lors de la création de la pièce initiale:', error)
      }
    },

    // Commencer l'activité
    async startActivity() {
      this.activityStarted = true
      await this.loadSavedRoomData()

      // Initialiser les feedbacks pour tous les environnements
      this.environments.forEach((env, index) => {
        this.userData.environmentFeedback[index] = {
          mood: '',
          comments: '',
          customizations: {},
        }
      })

      // S'assurer que le renderer est prêt
      if (!this.rendererInitialized) {
        this.initRenderer()
      }

      // Afficher l'explication de Flamou au lieu du sélecteur d'environnement
      this.showFlamouExplanation = true

      // Attendre un court délai avant de créer la pièce de base
      setTimeout(() => {
        this.createBasicRoom()
      }, 300)
    },

    // Navigation des questions
    nextQuestion() {
      // Sauvegarder les personnalisations actuelles
      this.saveCurrentCustomization(this.currentQuestion.type)

      // Passer à la question suivante
      if (this.currentQuestionIndex < this.questions.length - 1) {
        this.currentQuestionIndex++
      }
    },

    previousQuestion() {
      // Revenir à la question précédente
      if (this.currentQuestionIndex > 0) {
        this.currentQuestionIndex--
      }
    },

    // Finaliser l'exploration
    async finishExploration() {
      console.log('=== Finish Exploration Debug ===')
      console.log('Current environment:', this.currentEnvironment.name)
      console.log('Current environment index:', this.currentEnvironmentIndex)
      console.log('Current room name before check:', this.currentRoomName)
      
      // Vérifier que currentRoomName est bien défini
      if (!this.currentRoomName) {
        console.error('currentRoomName est vide! Recalcul...')
        this.currentRoomName = this.mapEnvironmentToRoomName(
          this.currentEnvironment.name,
        )
        console.log('New room name after mapping:', this.currentRoomName)
      }

      // Construire et sauvegarder les données de la room actuelle
      const roomData = this.buildRoomData(this.currentRoomName)
      console.log('Room data to save:', roomData)
      
      await this.saveRoomToBackend(this.currentRoomName, roomData)

      // Afficher le popup de choix Flamou
      this.showFlamouChoice = true
      this.showQuestion = false
    },

    // Commencer l'exploration avec Flamou
    startExploration() {
      this.showFlamouExplanation = false
      // Sélectionner automatiquement le premier environnement (Espace Polyvalent)
      this.selectEnvironment(0)
    },

    // Aller à la salle suivante
    goToNextRoom() {
      this.showFlamouChoice = false
      // Sélectionner l'environnement suivant
      const nextIndex = this.currentEnvironmentIndex + 1
      if (nextIndex < this.environments.length) {
        this.selectEnvironment(nextIndex)
      }
    },

    // Changer de jeu
    changeGame() {
      this.showFlamouChoice = false
      
      // Liste des jeux disponibles (excluant le jeu actuel)
      const availableGames = [
        '/roue-des-competences',
        '/scenarios', 
        '/metiers',
        '/shape-sequence-game',
        '/game-speed'
      ]
      
      // Sélectionner un jeu au hasard
      const randomIndex = Math.floor(Math.random() * availableGames.length)
      const selectedGame = availableGames[randomIndex]
      
      // Rediriger vers le jeu sélectionné
      this.$router.push(selectedGame)
    },

    // Retourner au tableau de bord
    returnToDashboard() {
      this.showFlamouChoice = false
      this.$router.push('/dashboard')
    },

    // Obtenir le message de completion dynamique
    getCompletionMessage() {
      const envNumber = this.currentEnvironmentIndex + 1
      
      if (this.isLastEnvironment) {
        return `Fantastique ! Tu as exploré tous les environnements ! 🎊`
      } else {
        return `Super ! Tu as terminé l'environnement ${envNumber} ! 🎉`
      }
    },

    // Obtenir la description de completion dynamique
    getCompletionDescription() {
      if (this.isLastEnvironment) {
        return `Tu as exploré tous les espaces disponibles et découvert tes préférences sensorielles. Félicitations pour ce parcours complet !`
      } else {
        return `Tu as bien exploré tes préférences sensorielles dans cet espace. Tu peux maintenant découvrir un nouvel environnement ou choisir une autre activité.`
      }
    },

    // Obtenir le numéro de la prochaine salle
    getNextRoomNumber() {
      return this.currentEnvironmentIndex + 2
    },

    // Sélectionner un environnement
    async selectEnvironment(index) {
      this.currentEnvironmentIndex = index
      const env = this.environments[index]

      this.currentRoomName = this.mapEnvironmentToRoomName(env.name)

      await this.loadSavedRoomData()

      // Show loading overlay
      this.modelsLoading = true
      this.loadingProgress = 0
      this.currentLoadingItem = 'Initialisation...'

      // Réinitialiser l'index de question
      this.currentQuestionIndex = 0

      // Appliquer les paramètres par défaut de l'environnement
      const settings = env.defaultSettings

      // Mise à jour des dimensions et couleurs
      this.roomWidth = settings.room.width
      this.roomDepth = settings.room.depth
      this.roomHeight = settings.room.height
      this.wallColor = settings.room.wallColor
      this.floorColor = settings.room.floorColor
      this.ceilingColor = settings.room.ceilingColor

      // Mise à jour de l'éclairage
      this.lightColor = settings.lighting.color
      this.lightIntensity = settings.lighting.intensity
      this.ambientLight = settings.lighting.ambient

      // Mise à jour du son
      this.selectedAmbience = settings.sound.type
      this.soundVolume = settings.sound.volume

      // S'assurer que le peopleCount est correctement réinitialisé et appliqué
      const newPeopleCount = settings.sound.peopleCount || 0
      this.peopleCount = newPeopleCount

      // Vérifier que le renderer est prêt
      if (!this.rendererInitialized) {
        console.warn("Le renderer n'est pas encore initialisé")
        this.initRenderer()
        setTimeout(() => {
          this.selectedObjectCategory = env.objectsCategory || 'minimal'
          this.applyEnvironmentChanges()
        }, 500)
      } else {
        this.selectedObjectCategory = env.objectsCategory || 'minimal'
        this.applyEnvironmentChanges()
      }

      // Afficher la première question après un délai
      setTimeout(() => {
        this.showQuestion = true
      }, 2000)
    },

    // Afficher un message du guide
    showGuideMessage(guide) {
      this.currentGuide = guide
      this.showGuide = true
    },

    // Fermer le message du guide
    dismissGuide() {
      this.showGuide = false
    },

    // Appliquer les changements d'environnement de manière sécurisée
    applyEnvironmentChanges() {
      try {
        this.updateRoom()
        this.updateLighting()
        this.updateAmbientSoundWithoutCompletion()
        this.updateClutterLevel()
      } catch (error) {
        console.error(
          "Erreur lors de l'application des changements d'environnement:",
          error,
        )
      }
    },

    // Version de updateAmbientSound qui ne marque pas l'étape comme complétée
    updateAmbientSoundWithoutCompletion() {
      if (!this.$refs.ambientAudio) return

      // Mise à jour de la source audio en fonction de la sélection
      let audioSrc
      this.soundEnabled = this.selectedAmbience !== 'none'

      switch (this.selectedAmbience) {
        case 'none':
          this.$refs.ambientAudio.pause()
          return
        case 'whitenoise':
          audioSrc = whiteNoiseAudio
          break
        case 'nature':
          audioSrc = NatureAudio
          break
        case 'cafe':
          audioSrc = CafeAudio
          break
        case 'crowd':
          audioSrc = CrowdAudio
          break
      }

      // N'actualiser la source que si elle a changé
      if (this.$refs.ambientAudio.src !== audioSrc) {
        this.$refs.ambientAudio.src = audioSrc
      }

      // Appliquer le volume
      this.$refs.ambientAudio.volume = this.soundVolume

      // Lire l'audio si activé
      if (this.soundEnabled) {
        this.$refs.ambientAudio
          .play()
          .catch((e) => console.log('Audio play failed:', e))
      }

      // Mettre à jour également le nombre de personnes
      if (this.renderer && this.rendererInitialized) {
        try {
          this.renderer.updatePeople(this.peopleCount)
        } catch (error) {
          console.error('Erreur lors de la mise à jour des personnes:', error)
        }
      }
    },

    // Sélection d'ambiance sonore
    selectSound(value) {
      this.selectedAmbience = value
      this.updateAmbientSound()
    },

    // Obtenir les données de feedback actuelles de manière sécurisée
    getCurrentFeedback() {
      // S'assurer que l'objet de feedback existe pour l'environnement actuel
      if (!this.userData.environmentFeedback[this.currentEnvironmentIndex]) {
        this.userData.environmentFeedback[this.currentEnvironmentIndex] = {
          mood: '',
          comments: '',
          customizations: {},
        }
      }

      return this.userData.environmentFeedback[this.currentEnvironmentIndex]
    },

    // Sélectionner un préréglage de lumière
    selectLightPreset(preset) {
      this.lightColor = preset.color
      this.updateLighting()
    },

    // Vérifier si c'est la palette actuelle
    isCurrentPalette(palette) {
      return (
        this.wallColor === palette.wall &&
        this.floorColor === palette.floor &&
        this.ceilingColor === palette.ceiling
      )
    },

    // Sélectionner une palette de couleurs
    selectColorPalette(palette) {
      this.wallColor = palette.wall
      this.floorColor = palette.floor
      this.ceilingColor = palette.ceiling
      this.updateColors()
      this.saveCurrentCustomization('colors')
    },

    // Mettre à jour l'ambiance sonore
    updateAmbientSound() {
      if (!this.$refs.ambientAudio) return

      // Mise à jour de la source audio en fonction de la sélection
      let audioSrc
      this.soundEnabled = this.selectedAmbience !== 'none'

      switch (this.selectedAmbience) {
        case 'none':
          this.$refs.ambientAudio.pause()
          return
        case 'whitenoise':
          audioSrc = whiteNoiseAudio
          break
        case 'nature':
          audioSrc = NatureAudio
          break
        case 'cafe':
          audioSrc = CafeAudio
          break
        case 'crowd':
          audioSrc = CrowdAudio
          break
      }

      // N'actualiser la source que si elle a changé
      if (this.$refs.ambientAudio.src !== audioSrc) {
        this.$refs.ambientAudio.src = audioSrc
      }

      // Appliquer le volume
      this.$refs.ambientAudio.volume = this.soundVolume

      // Lire l'audio si activé
      if (this.soundEnabled) {
        this.$refs.ambientAudio
          .play()
          .catch((e) => console.log('Audio play failed:', e))
      }

      this.saveCurrentCustomization('sounds')
    },

    // Mettre à jour le volume sonore
    updateSoundVolume() {
      if (!this.$refs.ambientAudio) return

      this.$refs.ambientAudio.volume = this.soundVolume
      this.saveCurrentCustomization('sounds')
    },

    // Mettre à jour le nombre de personnes
    updatePeopleCount() {
      if (this.renderer && this.rendererInitialized) {
        try {
          this.renderer.updatePeople(this.peopleCount)
          this.saveCurrentCustomization('people')
        } catch (error) {
          console.error('Erreur lors de la mise à jour des personnes:', error)
        }
      }
    },

    // Mettre à jour le niveau de détail/encombrement
    updateClutterLevel() {
      if (!this.renderer || !this.rendererInitialized) return

      try {
        // Indiquer que le chargement est en cours
        this.modelsLoading = true
        this.loadingProgress = 0
        this.currentLoadingItem = ''

        // Charger les nouveaux objets selon la catégorie sélectionnée
        this.renderer
          .loadObjectsByCategory(this.selectedObjectCategory)
          .then(() => {
            setTimeout(() => {
              this.modelsLoading = false
            }, 500)
            // Synchroniser les données
            this.syncFurnitureData()
          })
          .catch((error) => {
            console.error('Erreur lors du chargement des objets 3D:', error)
            this.modelsLoading = false
          })
      } catch (error) {
        console.error(
          'Erreur lors de la mise à jour du niveau de détail:',
          error,
        )
        this.modelsLoading = false
      }
    },

    // Enregistrer les personnalisations actuelles
    saveCurrentCustomization(category) {
      const feedback = this.getCurrentFeedback()

      if (!feedback.customizations) {
        feedback.customizations = {}
      }

      switch (category) {
        case 'light':
          feedback.customizations.light = {
            intensity: this.lightIntensity,
            ambient: this.ambientLight,
          }
          break
        case 'lightColor':
          feedback.customizations.lightColor = {
            color: this.lightColor,
          }
          break
        case 'colors':
          feedback.customizations.colors = {
            wall: this.wallColor,
            floor: this.floorColor,
            ceiling: this.ceilingColor,
          }
          break
        case 'sounds':
          feedback.customizations.sounds = {
            ambience: this.selectedAmbience,
            volume: this.soundVolume,
          }
          break
        case 'people':
          feedback.customizations.people = {
            peopleCount: this.peopleCount,
          }
          break
      }
    },

    // Sélectionner un mood pour le feedback
    selectMood(moodValue) {
      const feedback = this.getCurrentFeedback()
      feedback.mood = moodValue
    },

    // Obtenir la préférence d'éclairage pour l'affichage
    getLightPreference() {
      const feedback = this.getCurrentFeedback()

      if (!feedback.customizations || !feedback.customizations.light) {
        return 'Non déterminé'
      }

      const intensity = feedback.customizations.light.intensity

      if (intensity < 1.3) return 'Éclairage tamisé'
      if (intensity > 1.8) return 'Éclairage lumineux'
      return 'Éclairage modéré'
    },

    // Obtenir la préférence sonore pour l'affichage
    getSoundPreference() {
      const feedback = this.getCurrentFeedback()

      if (!feedback.customizations || !feedback.customizations.sounds) {
        return 'Non déterminé'
      }

      const ambience = feedback.customizations.sounds.ambience

      switch (ambience) {
        case 'none':
          return 'Préfère le silence'
        case 'whitenoise':
          return 'Préfère le bruit blanc'
        case 'nature':
          return 'Préfère les sons naturels'
        case 'cafe':
          return "Préfère l'ambiance café tranquille"
        case 'crowd':
          return "Tolère bien l'environnement animé"
        default:
          return 'Préférence non déterminée'
      }
    },

    // Obtenir une recommandation personnalisée
    getPersonalizedRecommendation(index) {
      const recommendations = [
        // Recommandations basées sur l'éclairage
        () => {
          const lightPref = this.getLightPreference()
          if (lightPref.includes('tamisé')) {
            return 'Privilégiez un éclairage indirect et tamisé dans votre espace quotidien, en évitant les lumières fluorescentes.'
          } else if (lightPref.includes('lumineux')) {
            return "Assurez-vous d'avoir un bon éclairage dans vos espaces de travail, idéalement avec une lumière naturelle ou des lampes à spectre complet."
          } else {
            return 'Optez pour un éclairage modulable que vous pourrez ajuster selon vos activités et votre niveau de fatigue.'
          }
        },

        // Recommandations basées sur le son
        () => {
          const soundPref = this.getSoundPreference()
          if (soundPref.includes('silence')) {
            return "Envisagez d'utiliser des bouchons d'oreilles ou un casque anti-bruit dans les environnements bruyants."
          } else if (soundPref.includes('bruit blanc')) {
            return 'Utilisez une application ou un appareil de bruit blanc pour masquer les sons distrayants et améliorer votre concentration.'
          } else if (soundPref.includes('sons naturels')) {
            return 'Intégrez des sons de la nature dans votre environnement quotidien pour réduire le stress et améliorer votre bien-être.'
          } else {
            return 'Créez des playlists adaptées à différentes activités pour vous aider à réguler votre état sensoriel.'
          }
        },

        // Recommandation sur la présence de personnes
        () => {
          const feedback = this.getCurrentFeedback()
          if (feedback.customizations && feedback.customizations.people) {
            const count = feedback.customizations.people.peopleCount
            if (count === 0) {
              return 'Vous semblez préférer les environnements calmes et peu peuplés. Privilégiez des espaces de travail et de repos isolés.'
            } else if (count <= 3) {
              return "Vous semblez à l'aise dans des petits groupes. Favorisez des rencontres en comité restreint plutôt que de grandes assemblées."
            } else {
              return "Vous semblez à l'aise dans des environnements animés. N'hésitez pas à aménager des espaces de calme pour vous ressourcer quand nécessaire."
            }
          }
          return "Prenez des pauses sensorielles régulières pour prévenir la fatigue et l'épuisement, particulièrement dans des environnements stimulants."
        },
      ]

      // S'assurer que l'index est valide
      if (index > 0 && index <= recommendations.length) {
        return recommendations[index - 1]()
      }

      // Recommandation par défaut
      return "Prenez des pauses sensorielles régulières pour prévenir la fatigue et l'épuisement, particulièrement dans des environnements stimulants."
    },

    // Recommencer l'exploration (si nécessaire)
    restartExploration() {
      this.resetAllData()
      // Réinitialiser les données
      this.showFlamouChoice = false
      this.currentEnvironmentIndex = 0
      this.currentQuestionIndex = 0
      this.showQuestion = false
      this.currentRoomName = ''

      // Réinitialiser les personnes à zéro
      this.peopleCount = 0
      if (this.renderer && this.rendererInitialized) {
        this.renderer.updatePeople(0)
      }

      // Réinitialiser l'audio
      if (this.$refs.ambientAudio) {
        this.$refs.ambientAudio.pause()
        this.selectedAmbience = 'none'
        this.soundEnabled = false
      }

      // Réinitialiser les feedbacks
      this.environments.forEach((env, index) => {
        this.userData.environmentFeedback[index] = {
          mood: '',
          comments: '',
          customizations: {},
        }
      })

      this.showFlamouExplanation = true
    },

    // Méthodes de mise à jour du renderer
    updateRoom() {
      if (!this.renderer || !this.rendererInitialized) return

      try {
        this.renderer.updateRoom(
          this.roomWidth,
          this.roomDepth,
          this.roomHeight,
          this.wallColor,
          this.floorColor,
          this.ceilingColor,
        )

        // Synchroniser les données
        this.syncFurnitureData()
      } catch (error) {
        console.error('Erreur lors de la mise à jour de la pièce:', error)
      }
    },

    updateColors() {
      if (!this.renderer || !this.rendererInitialized) return

      try {
        this.renderer.updateRoomColors(
          this.wallColor,
          this.floorColor,
          this.ceilingColor,
        )
      } catch (error) {
        console.error('Erreur lors de la mise à jour des couleurs:', error)
      }
    },

    updateLighting() {
      if (!this.renderer || !this.rendererInitialized) return

      try {
        this.renderer.updateLighting(
          this.lightColor,
          this.lightIntensity,
          this.ambientLight,
        )

        this.saveCurrentCustomization('light')
      } catch (error) {
        console.error("Erreur lors de la mise à jour de l'éclairage:", error)
      }
    },

    // Synchroniser les données de meubles
    syncFurnitureData() {
      if (!this.renderer || !this.rendererInitialized) return

      try {
        // Obtenir l'état du renderer
        const state = this.renderer.getState()

        // Synchroniser les données de la salle
        this.roomWidth = state.room.width
        this.roomDepth = state.room.depth
        this.roomHeight = state.room.height
        this.wallColor = state.room.wallColor
        this.floorColor = state.room.floorColor
        this.ceilingColor = state.room.ceilingColor

        // Et l'éclairage
        this.lightColor = state.lighting.color
        this.lightIntensity = state.lighting.intensity
        this.ambientLight = state.lighting.ambient
      } catch (error) {
        console.error('Erreur lors de la synchronisation des données:', error)
      }
    },

    // Obtenir le message de chargement actuel basé sur le pourcentage
    getCurrentLoadingMessage() {
      const progress = this.loadingProgress
      if (progress < 20) return this.loadingMessages[0]
      if (progress < 40) return this.loadingMessages[1]
      if (progress < 60) return this.loadingMessages[2]
      if (progress < 80) return this.loadingMessages[3]
      return this.loadingMessages[4]
    },

    // Obtenir le détail de chargement actuel
    getCurrentLoadingDetail() {
      const progress = this.loadingProgress
      if (progress < 20) return this.loadingDetails[0]
      if (progress < 40) return this.loadingDetails[1]
      if (progress < 60) return this.loadingDetails[2]
      if (progress < 80) return this.loadingDetails[3]
      return this.loadingDetails[4]
    },
  },
}
</script>

<style scoped>
.environment-container {
  height: 100vh;
  overflow: hidden;
}

/* Écran de bienvenue */
.welcome-screen {
  position: absolute;
  width: 100%;
  height: 100%;
  background: #f0f6ff;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.welcome-content {
  background: white;
  padding: 20px;
  border-radius: 20px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  max-width: 900px; /* Plus large */
  width: 92%;
  text-align: center;
}

.welcome-content h1 {
  color: #2b6bff;
  margin-bottom: 10px;
  font-size: 2rem;
  font-weight: bold;
  text-align: center;
}

.intro-text {
  font-size: 1.2rem;
  color: #444;
  line-height: 1.3;
  margin-bottom: 15px;
  text-align: center;
  font-weight: 500;
}

.activity-explanation {
  text-align: center;
  margin: 15px 0 20px;
}

.activity-explanation h2 {
  font-size: 1.4rem;
  color: #2b6bff;
  margin-bottom: 15px;
  background: #f0f6ff;
  padding: 8px 15px;
  border-radius: 10px;
  display: inline-block;
}

.explanation-steps {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  gap: 15px;
  margin: 15px 0;
}

.explanation-step {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #f8f8f8;
  padding: 10px;
  border-radius: 15px;
  width: 30%;
  min-width: 200px;
  max-width: 250px;
}

.step-number {
  background: #2b6bff;
  color: white;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.step-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  flex-grow: 1;
}

.step-content h3 {
  margin: 0 0 5px;
  font-size: 1.1rem;
  color: #333;
  line-height: 1.2;
}

.step-image {
  align-self: center;
  margin-top: 8px;
  width: 50%;
}

.important-note {
  background: #fff5e6;
  border: 3px solid #ffcc80;
  padding: 12px 15px;
  margin-top: 20px;
  border-radius: 15px;
  text-align: center;
}

.important-note h3 {
  color: #ff8f00;
  margin: 0 0 8px;
  font-size: 1.2rem;
  text-align: center;
}

.important-points {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}

.important-note p {
  margin: 5px 0;
  color: #555;
  font-size: 1rem;
  line-height: 1.3;
}

/* Interface principale */
.main-interface {
  height: 100vh;
  overflow: hidden;
  position: relative;
}

/* Fullscreen RoomRenderer */
.fullscreen-renderer {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.room-visualization {
  width: 100%;
  height: 100%;
  position: relative;
}

/* Questions overlay */
.question-overlay {
  position: absolute;
  bottom: 20px;
  left: 20px;
  width: 460px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(5px);
  border: 2px solid #4caf50;
  border-radius: 18px;
  padding: 20px 22px;
  animation: fadeIn 0.3s ease-out;
  z-index: 50;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.question-container {
  width: 100%;
}

.question-container h3 {
  color: #2b6bff;
  margin: 0 0 8px 0;
  font-size: 1.3rem;
  text-align: center;
  font-weight: bold;
}

.question-container p {
  color: #555;
  margin: 0 0 15px 0;
  font-size: 1rem;
  text-align: center;
}

.question-controls {
  margin-bottom: 15px;
}

.question-navigation {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 15px;
}

.nav-button {
  padding: 8px 16px;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-weight: bold;
  font-size: 0.95rem;
  transition: all 0.2s;
}

.prev-button {
  background: #e0e0e0;
  color: #555;
}

.next-button,
.finish-button {
  background: #4caf50;
  color: white;
}

.finish-button {
  background: #2b6bff;
}

.nav-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
}

/* Contrôle de lumière */
.big-button-group {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 15px;
}

.big-button {
  flex: 1;
  background: white;
  border: 2px solid #ddd;
  border-radius: 10px;
  padding: 15px 8px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.big-button.active {
  border-color: #4caf50;
  background: #e8f5e9;
  transform: scale(1.03);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.big-button-icon {
  font-size: 1.8rem;
  margin-bottom: 8px;
}

.big-button-label {
  font-size: 1rem;
  font-weight: 500;
  color: #444;
}

/* Boutons de couleur */
.color-buttons {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-top: 10px;
}

.color-button {
  aspect-ratio: 1/1;
  border: 2px solid transparent;
  border-radius: 10px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.2s;
}

.color-button.active {
  border-color: #4caf50;
  transform: scale(1.05);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.color-button-label {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  font-size: 0.9rem;
  padding: 4px 0;
  font-weight: 500;
  text-align: center;
}

/* Palettes de couleurs */
.color-palettes {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 15px;
}

.color-palette {
  cursor: pointer;
  border: 2px solid transparent;
  border-radius: 10px;
  padding: 8px;
  transition: all 0.2s;
  background: white;
}

.color-palette.selected {
  border-color: #4caf50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.3);
  transform: scale(1.03);
}

.palette-preview {
  display: flex;
  height: 30px;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 6px;
}

.color-preview {
  flex: 1;
  height: 100%;
}

.color-palette span {
  display: block;
  text-align: center;
  font-size: 0.9rem;
  color: #555;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Options de son */
.sound-options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 15px;
}

.sound-option {
  background: white;
  border: 2px solid #ddd;
  border-radius: 10px;
  padding: 12px 5px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.sound-option.active {
  border-color: #4caf50;
  background: #e8f5e9;
  transform: scale(1.03);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.sound-icon {
  font-size: 1.8rem;
  margin-bottom: 6px;
}

.sound-label {
  font-size: 0.95rem;
  font-weight: 500;
  color: #444;
  text-align: center;
}

.slider-control {
  margin: 15px auto;
  max-width: 340px;
  text-align: center;
}

.slider-control label {
  display: block;
  margin-bottom: 6px;
  font-size: 1rem;
  color: #555;
  font-weight: 500;
}

.slider-control input {
  width: 100%;
  height: 14px;
}

/* Contrôle de personnes */
.people-count-control {
  text-align: center;
  margin-bottom: 15px;
}

.people-count-control label {
  display: block;
  margin-bottom: 10px;
  font-size: 1rem;
  color: #444;
  font-weight: 500;
}

.people-selection {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 6px;
  margin-top: 10px;
}

.people-button {
  width: 100%;
  aspect-ratio: 1/1;
  background: white;
  border: 2px solid #ddd;
  border-radius: 50%;
  font-size: 1rem;
  font-weight: bold;
  color: #555;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  max-width: 45px;
  margin: 0 auto;
}

.people-button.active {
  border-color: #4caf50;
  background: #e8f5e9;
  color: #4caf50;
  transform: scale(1.05);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.people-button.active {
  border-color: #4caf50;
  background: #e8f5e9;
  color: #4caf50;
  transform: scale(1.05);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* Mood selection */
.mood-selection {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-top: 10px;
  margin-bottom: 15px;
}

.mood-option {
  background: white;
  border: 2px solid #ddd;
  border-radius: 10px;
  padding: 12px 5px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}

.mood-option.selected {
  border-color: #4caf50;
  background: #e8f5e9;
  transform: scale(1.03);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.mood-emoji {
  font-size: 1.8rem;
  margin-bottom: 6px;
}

.mood-label {
  font-size: 0.95rem;
  font-weight: 500;
  color: #444;
}

.control-item {
  margin: 0 auto;
  max-width: 100%;
}

.control-item label {
  display: block;
  margin-bottom: 6px;
  font-size: 1rem;
  color: #555;
}

.control-item textarea {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: none;
  font-family: inherit;
  font-size: 0.9rem;
  height: 50px;
}

/* Guide overlay */
.guide-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  z-index: 100;
  padding-top: 10%; /* Espace en haut */
  backdrop-filter: blur(3px); /* Effet de flou léger */
  animation: fadeIn 0.3s ease-out;
  will-change: opacity;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.guide-content {
  background: linear-gradient(to bottom, #ffffff, #f7f9ff);
  padding: 20px 25px;
  border-radius: 20px;
  max-width: 500px;
  width: 90%;
  text-align: center;
  box-shadow:
    0 10px 30px rgba(0, 0, 0, 0.1),
    0 0 0 1px rgba(58, 87, 232, 0.1);
  border-top: 4px solid #4caf50;
  position: relative;
  animation: slideDown 0.4s ease-out;
  transform-origin: top center;
  will-change: transform, opacity;
}

@keyframes slideDown {
  from {
    transform: translateY(-20px) scale(0.95);
    opacity: 0;
  }
  to {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
}

.guide-content::before {
  content: '💡'; /* Icône d'ampoule */
  position: absolute;
  top: -15px;
  left: 20px;
  font-size: 24px;
  background: white;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.guide-content h3 {
  margin: 0 0 12px;
  color: #2b6bff;
  font-size: 1.3rem;
  font-weight: bold;
}

.guide-content p {
  margin: 0 0 20px;
  color: #555;
  font-size: 1.05rem;
  line-height: 1.4;
}

.guide-button {
  padding: 10px 20px;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  transition:
    transform 0.2s,
    background 0.2s;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}

/* Flamou Loading overlay */
.flamou-loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(43, 107, 255, 0.9) 0%, rgba(76, 175, 80, 0.9) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
  animation: fadeIn 0.3s ease-out;
}

.flamou-loading-container {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
  padding: 30px;
  border-radius: 20px;
  max-width: 500px;
  width: 90%;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  border: 3px solid #4caf50;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.flamou-loading-character {
  position: relative;
  margin-bottom: 20px;
  animation: floatBounce 2s ease-in-out infinite;
}

@keyframes floatBounce {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-15px);
  }
}

.flamou-loading-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 4px solid #4caf50;
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.3);
}

.loading-speech-bubble {
  position: absolute;
  top: -10px;
  right: -20px;
  background: white;
  padding: 8px 12px;
  border-radius: 15px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
  border: 2px solid #4caf50;
}

.loading-speech-bubble::before {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 15px;
  width: 0;
  height: 0;
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-top: 8px solid white;
}

.loading-dots {
  display: flex;
  gap: 4px;
  align-items: center;
}

.loading-dots span {
  width: 6px;
  height: 6px;
  background: #4caf50;
  border-radius: 50%;
  animation: loadingDots 1.4s ease-in-out infinite both;
}

.loading-dots span:nth-child(1) { animation-delay: -0.32s; }
.loading-dots span:nth-child(2) { animation-delay: -0.16s; }
.loading-dots span:nth-child(3) { animation-delay: 0s; }

@keyframes loadingDots {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1.2);
    opacity: 1;
  }
}

.flamou-loading-content {
  width: 100%;
}

.flamou-loading-content h3 {
  margin: 0 0 20px 0;
  color: #2b6bff;
  font-size: 1.4rem;
  font-weight: bold;
  animation: textGlow 2s ease-in-out infinite alternate;
}

@keyframes textGlow {
  from {
    text-shadow: 0 0 5px rgba(43, 107, 255, 0.3);
  }
  to {
    text-shadow: 0 0 10px rgba(43, 107, 255, 0.6);
  }
}

.flamou-loading-bar {
  height: 12px;
  background: #e0e0e0;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 15px;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.flamou-loading-progress {
  height: 100%;
  background: linear-gradient(45deg, #4caf50, #45a049, #4caf50);
  background-size: 200% 200%;
  border-radius: 6px;
  transition: width 0.3s ease;
  animation: progressShimmer 2s linear infinite;
}

@keyframes progressShimmer {
  0% {
    background-position: 200% 50%;
  }
  100% {
    background-position: -200% 50%;
  }
}

.flamou-loading-text {
  font-size: 1rem;
  color: #555;
  margin-bottom: 10px;
  font-weight: 500;
}

.flamou-loading-item {
  font-size: 0.9rem;
  color: #777;
  font-style: italic;
  opacity: 0.8;
}

/* Flamou choice popup */
.flamou-choice-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(3px);
  animation: fadeIn 0.3s ease-out;
}

.flamou-choice-container {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
  padding: 30px;
  border-radius: 20px;
  max-width: 800px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  border: 3px solid #4caf50;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  animation: slideInUp 0.5s ease-out;
}

.flamou-choices {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 20px;
  width: 100%;
  max-width: 800px;
}

.choice-option {
  background: white;
  border: 3px solid #e0e0e0;
  border-radius: 15px;
  padding: 25px 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.choice-option:hover {
  border-color: #4caf50;
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(76, 175, 80, 0.2);
}

.choice-option:active {
  transform: translateY(-2px);
}

.choice-icon {
  font-size: 3rem;
  margin-bottom: 15px;
  display: block;
}

.choice-option h3 {
  color: #2b6bff;
  margin: 0 0 10px 0;
  font-size: 1.3rem;
  font-weight: bold;
}

.choice-option p {
  color: #666;
  margin: 0;
  font-size: 1rem;
  line-height: 1.4;
}

/* Flamou explanation popup */
.flamou-explanation-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  backdrop-filter: blur(3px);
  animation: fadeIn 0.3s ease-out;
}

.flamou-explanation-container {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
  padding: 30px;
  border-radius: 20px;
  max-width: 700px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  border: 3px solid #4caf50;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  animation: slideInUp 0.5s ease-out;
}

@keyframes slideInUp {
  from {
    transform: translateY(50px) scale(0.9);
    opacity: 0;
  }
  to {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
}

.flamou-character {
  margin-bottom: 20px;
  animation: bounce 1s ease-in-out infinite alternate;
}

@keyframes bounce {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(-10px);
  }
}

.flamou-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 4px solid #4caf50;
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.3);
}

.flamou-speech-bubble {
  background: white;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  position: relative;
  max-width: 100%;
}

.flamou-speech-bubble::before {
  content: '';
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 15px solid transparent;
  border-right: 15px solid transparent;
  border-bottom: 15px solid white;
}

.flamou-speech-bubble h2 {
  color: #2b6bff;
  margin: 0 0 15px 0;
  font-size: 1.8rem;
  font-weight: bold;
}

.flamou-speech-bubble p {
  color: #555;
  margin: 0 0 20px 0;
  font-size: 1.1rem;
  line-height: 1.5;
}

.flamou-instructions {
  background: #f0f6ff;
  padding: 20px;
  border-radius: 12px;
  margin: 20px 0;
  border-left: 4px solid #2b6bff;
}

.flamou-instructions h3 {
  color: #2b6bff;
  margin: 0 0 15px 0;
  font-size: 1.2rem;
  font-weight: bold;
}

.flamou-instructions ul {
  margin: 0;
  padding-left: 20px;
  text-align: left;
}

.flamou-instructions li {
  color: #444;
  margin-bottom: 8px;
  font-size: 1rem;
  line-height: 1.4;
}

.flamou-continue-button {
  background: linear-gradient(45deg, #4caf50, #45a049);
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 50px;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
  margin-top: 10px;
}

.flamou-continue-button:hover {
  background: linear-gradient(45deg, #45a049, #3d8b40);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
}

.flamou-continue-button:active {
  transform: translateY(0);
  box-shadow: 0 2px 10px rgba(76, 175, 80, 0.3);
}

/* Boutons */
.primary-button {
  width: auto;
  min-width: 200px;
  max-width: 300px;
  padding: 12px 20px;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  font-size: 1.2rem;
  font-weight: bold;
  transition:
    transform 0.2s,
    background 0.2s;
  margin: 15px auto 0;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.primary-button:hover {
  background: #3d8b40;
  transform: scale(1.03);
}

/* Responsive */
@media screen and (max-width: 768px) {
  .question-overlay {
    max-height: 50%;
  }

  .big-button-group,
  .color-buttons,
  .sound-options {
    flex-wrap: wrap;
    gap: 10px;
  }

  .big-button,
  .color-button,
  .sound-option {
    width: calc(50% - 10px);
    max-width: 120px;
  }

  .color-palette {
    width: calc(50% - 15px);
  }

  .mood-option {
    width: calc(50% - 15px);
  }

  .guide-content {
    width: 95%;
    padding: 15px 20px;
  }

  .flamou-explanation-container {
    width: 95%;
    padding: 20px;
  }

  .flamou-avatar {
    width: 100px;
    height: 100px;
  }

  .flamou-speech-bubble h2 {
    font-size: 1.5rem;
  }

  .flamou-speech-bubble p {
    font-size: 1rem;
  }

  .flamou-choice-container {
    width: 95%;
    padding: 20px;
  }

  .flamou-choices {
    grid-template-columns: 1fr;
    gap: 15px;
    max-width: 100%;
  }

  .choice-option {
    padding: 20px 15px;
  }

  .choice-icon {
    font-size: 2.5rem;
  }

  .choice-option h3 {
    font-size: 1.2rem;
  }

  .flamou-loading-container {
    width: 95%;
    padding: 20px;
  }

  .flamou-loading-avatar {
    width: 80px;
    height: 80px;
  }

  .flamou-loading-content h3 {
    font-size: 1.2rem;
  }
}

@media screen and (max-width: 480px) {
  .big-button-group,
  .color-buttons,
  .sound-options,
  .people-buttons {
    flex-direction: column;
    align-items: center;
  }

  .big-button,
  .color-button,
  .sound-option,
  .people-button {
    width: 80%;
    max-width: none;
  }

  .color-palettes {
    flex-direction: column;
    align-items: center;
  }

  .color-palette {
    width: 80%;
    max-width: none;
  }

  .mood-option {
    width: calc(50% - 10px);
  }

  .question-container h3 {
    font-size: 1.1rem;
  }

  .question-container p {
    font-size: 0.9rem;
  }
}
</style>
