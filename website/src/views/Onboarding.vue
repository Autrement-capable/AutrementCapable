<template>
  <div
    class="questionnaire"
    aria-label="Questionnaire page"
    :style="{ backgroundColor: currentBackgroundColor }"
  >
    <h1 class="title">Bonjour !</h1>

    <div
      v-if="currentQuestionIndex < questions.length"
      class="content-container"
    >
      <!-- Section gauche avec avatar et question -->
      <div class="left-section">
        <img
          :src="selectedAvatarUrl || require('../assets/jeunefemme.png')"
          alt="Avatar"
          :class="imageClass"
        />
        <div class="question-container">
          <p class="sub-title">{{ questions[currentQuestionIndex].text }}</p>
          <button
            class="action-button listen-button"
            @click="repeatQuestion"
            aria-label="Écouter la question"
          >
            <span class="icon">🔊</span>
            <span class="button-text">Écouter</span>
          </button>
        </div>
      </div>

      <!-- Section droite avec les réponses -->
      <div class="right-section">
        <!-- Affichage des réponses préconfigurées pour l'âge -->
        <div
          v-if="questions[currentQuestionIndex].key === 'age'"
          class="options-grid"
        >
          <button
            v-for="ageOption in ageOptions.slice(0, 8)"
            :key="ageOption"
            class="option-button"
            @click="selectOption('age', ageOption)"
            :class="{ selected: responses.age === ageOption }"
          >
            {{ ageOption }}
          </button>
          <button
            class="option-button custom"
            @click="showCustomInput = true"
            v-if="!showCustomInput"
          >
            Autre
          </button>
          <div v-if="showCustomInput" class="custom-input-container">
            <input
              type="number"
              v-model="responses.age"
              placeholder="Votre âge"
              class="small-input"
              ref="customAgeInput"
            />
            <button
              class="action-button"
              @click=";(showCustomInput = false), validateResponse('age')"
            >
              OK
            </button>
          </div>
        </div>

        <!-- Choix prédéfinis pour le nom -->
        <div
          v-if="questions[currentQuestionIndex].key === 'name'"
          class="name-options"
        >
          <!-- Option saisie vocale -->
          <div class="voice-input-container" v-if="!showNameInput">
            <button
              class="action-button speak-button"
              @click="startRecognition"
              :class="{ active: isRecognizing }"
            >
              <span class="icon">🎙️</span>
              <span class="button-text">
                {{ isRecognizing ? "J'écoute..." : 'Dites votre nom' }}
              </span>
            </button>
            <div
              v-if="responses.name && !showNameInput && voiceInputActive"
              class="speech-result"
            >
              <p>
                Vous avez dit:
                <strong>{{ responses.name }}</strong>
              </p>
              <div class="confirm-buttons">
                <button
                  class="action-button confirm"
                  @click="validateResponse('name')"
                >
                  C'est correct
                </button>
                <button
                  class="action-button retry"
                  @click=";(responses.name = ''), startRecognition()"
                >
                  Réessayer
                </button>
              </div>
            </div>
          </div>

          <!-- Option saisie texte -->
          <div class="text-input-option">
            <button
              class="option-button text-option"
              @click="startTextInput"
              v-if="!showNameInput"
            >
              Taper mon nom
            </button>
            <div v-if="showNameInput" class="custom-input-container">
              <input
                type="text"
                v-model="responses.name"
                placeholder="Votre nom"
                class="small-input"
                ref="customNameInput"
              />
              <div class="button-group">
                <button class="action-button" @click="confirmTextInput">
                  Confirmer
                </button>
                <button
                  class="action-button cancel-button"
                  @click="cancelTextInput"
                >
                  Annuler
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Options pour le genre de l'avatar -->
        <div
          v-if="questions[currentQuestionIndex].key === 'avatarGender'"
          class="avatar-options-container"
        >
          <div class="options-grid avatar-gender-grid">
            <button
              v-for="option in avatarGenderOptions"
              :key="option.value"
              class="option-button avatar-option"
              @click="selectOption('avatarGender', option.value)"
              :class="{ selected: responses.avatarGender === option.value }"
            >
              <span class="avatar-option-icon">{{ option.icon }}</span>
              <span class="avatar-option-text">{{ option.label }}</span>
            </button>
          </div>
        </div>

        <!-- Options pour les accessoires de l'avatar -->
        <div
          v-if="questions[currentQuestionIndex].key === 'avatarAccessories'"
          class="avatar-options-container"
        >
          <div class="options-grid avatar-accessories-grid">
            <button
              v-for="option in avatarAccessoriesOptions"
              :key="option.value"
              class="option-button avatar-option"
              @click="toggleAvatarAccessory(option.value)"
              :class="{ selected: selectedAccessories.includes(option.value) }"
            >
              <span class="avatar-option-icon">{{ option.icon }}</span>
              <span class="avatar-option-text">{{ option.label }}</span>
            </button>
          </div>
          <div v-if="selectedAccessories.length > 0" class="selected-items">
            <button
              class="action-button confirm-selection"
              @click="
                ;(responses.avatarAccessories = selectedAccessories.join(',')),
                  validateResponse('avatarAccessories')
              "
            >
              Confirmer mes accessoires
            </button>
          </div>
        </div>

        <!-- Options pour la couleur de l'avatar -->
        <div
          v-if="questions[currentQuestionIndex].key === 'avatarColor'"
          class="avatar-options-container"
        >
          <div class="options-grid avatar-color-grid">
            <button
              v-for="option in avatarColorOptions"
              :key="option.value"
              class="option-button avatar-color-option"
              @click="selectOption('avatarColor', option.value)"
              :class="{ selected: responses.avatarColor === option.value }"
              :style="{ backgroundColor: option.hex }"
            >
              <span class="avatar-option-icon">{{ option.icon }}</span>
              <span class="avatar-option-text">{{ option.label }}</span>
            </button>
          </div>
        </div>

        <!-- Options pour les passions de l'avatar -->
        <div
          v-if="questions[currentQuestionIndex].key === 'avatarPassion'"
          class="avatar-options-container"
        >
          <div class="options-grid avatar-passion-grid">
            <button
              v-for="option in avatarPassionOptions"
              :key="option.value"
              class="option-button avatar-option"
              @click="selectOption('avatarPassion', option.value)"
              :class="{ selected: responses.avatarPassion === option.value }"
            >
              <span class="avatar-option-icon">{{ option.icon }}</span>
              <span class="avatar-option-text">{{ option.label }}</span>
            </button>
          </div>
        </div>

        <!-- Options pour l'expression de l'avatar -->
        <div
          v-if="questions[currentQuestionIndex].key === 'avatarExpression'"
          class="avatar-options-container"
        >
          <div class="options-grid avatar-expression-grid">
            <button
              v-for="option in avatarExpressionOptions"
              :key="option.value"
              class="option-button avatar-option"
              @click="selectOption('avatarExpression', option.value)"
              :class="{ selected: responses.avatarExpression === option.value }"
            >
              <span class="avatar-option-icon">{{ option.icon }}</span>
              <span class="avatar-option-text">{{ option.label }}</span>
            </button>
          </div>
        </div>

        <!-- Passions avec options prédéfinies et vocales -->
        <div
          v-if="questions[currentQuestionIndex].key === 'passions'"
          class="passions-container"
        >
          <div class="options-grid">
            <button
              v-for="passion in passionOptions"
              :key="passion"
              class="option-button passion-button"
              @click="selectPassion(passion)"
              :class="{ selected: selectedPassions.includes(passion) }"
            >
              {{ passion }}
            </button>
          </div>

          <div class="voice-input-container" style="margin: 0.5rem 0">
            <button
              class="action-button speak-button"
              @click="startRecognitionForPassions"
              :class="{ active: isRecognizing }"
            >
              <span class="icon">🎙️</span>
              <span class="button-text">
                {{ isRecognizing ? "J'écoute..." : 'Dire' }}
              </span>
            </button>
          </div>

          <div v-if="selectedPassions.length > 0" class="selected-passions">
            <div class="passions-tags">
              <div
                v-for="(passion, index) in selectedPassions.slice(0, 3)"
                :key="index"
                class="passion-tag"
              >
                {{ passion }}
                <button
                  class="remove-button"
                  @click="removePassion(index)"
                  aria-label="Supprimer cette passion"
                >
                  ×
                </button>
              </div>
            </div>
            <button
              class="action-button confirm-passions"
              @click="
                ;(responses.passions = selectedPassions.join(', ')),
                  validateResponse('passions')
              "
            >
              Confirmer
            </button>
          </div>
        </div>

        <div class="navigation-buttons" v-if="!showAvatarSelection">
          <button
            v-if="currentQuestionIndex > 0"
            class="action-button prev-button"
            @click="previousQuestion"
          >
            Précédent
          </button>
          <button
            class="action-button next-button"
            @click="nextQuestion"
            :disabled="!canProceed()"
          >
            Suivant
          </button>
          <button
            v-if="shouldShowSkipButton()"
            class="action-button skip-button"
            @click="skipQuestion"
          >
            Passer cette question
          </button>
        </div>
      </div>
    </div>

    <!-- Sélection d'avatar -->
    <div v-if="showAvatarSelection" class="avatar-selection-container">
      <div v-if="isLoadingImages" class="loading">
        <div class="loading-spinner"></div>
        <p>Création de vos avatars personnalisés...</p>
      </div>
      <div v-else-if="generatedImages.length > 0" class="avatar-selection">
        <h2>Choisissez votre avatar :</h2>
        <div class="avatars-grid">
          <div
            v-for="(img, index) in generatedImages"
            :key="index"
            class="avatar-option-container"
            :class="{ selected: selectedAvatarUrl === img }"
          >
            <img
              :src="img"
              alt="Option d'avatar"
              class="avatar-option"
              @click="selectAvatar(img)"
            />
            <button class="select-avatar-button" @click="selectAvatar(img)">
              Choisir cet avatar
            </button>
          </div>
        </div>
        <button
          v-if="selectedAvatarUrl"
          class="action-button next-button"
          @click="finalizeAvatarSelection"
        >
          Continuer avec cet avatar
        </button>
      </div>
    </div>

    <div
      v-if="currentQuestionIndex >= questions.length && !showAvatarSelection"
      class="completion-message"
    >
      <div v-if="isRegistering" class="loading-spinner">
        <div class="spinner"></div>
        <p>Création de votre compte...</p>
      </div>
      <button
        v-else
        @click="createAccountAndStartGame"
        :disabled="isRegistering"
        class="start-game-button"
      >
        Commencer le premier jeu
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import AuthService from '@/services/AuthService'

/* global webkitSpeechRecognition */
export default {
  name: 'UserOnboarding',
  data() {
    return {
      currentQuestionIndex: 0,
      generatedImages: [],
      selectedAvatarUrl: '',
      isLoadingImages: false,
      showAvatarSelection: false,
      showCustomInput: false,
      showNameInput: false,
      voiceInputActive: false,
      backgroundColors: [
        '#e0f7fa',
        '#e8f5e9',
        '#fce4ec',
        '#fff3e0',
        '#ede7f6',
        '#f9fbe7',
      ],
      currentBackgroundColor: '#e0f7fa',
      isRegistering: false,
      registrationError: null,
      questions: [
        { text: '🎂 Quel âge as-tu ?', key: 'age', type: 'number' },
        {
          text: "👤 Comment voudrais-tu qu'on t'appelle ?",
          key: 'name',
          type: 'text',
        },
        {
          text: '👦 Veux-tu que ton avatar soit...',
          key: 'avatarGender',
          type: 'choice',
        },
        {
          text: '🧢 Quels accessoires aimes-tu porter ou utiliser ?',
          key: 'avatarAccessories',
          type: 'multichoice',
        },
        {
          text: '🎨 Choisis une couleur principale pour ton avatar',
          key: 'avatarColor',
          type: 'choice',
        },
        {
          text: "🌟 Qu'est-ce que tu préfères parmi ces passions ?",
          key: 'avatarPassion',
          type: 'choice',
        },
        {
          text: '😊 Ton avatar est plutôt...',
          key: 'avatarExpression',
          type: 'choice',
        },
        {
          text: '🎨 Quelles sont tes passions ?',
          key: 'passions',
          type: 'text',
          icon: 'passion-icon.png',
        },
      ],
      ageOptions: [12, 14, 16, 18, 20, 22, 24, 26],
      passionOptions: [
        'Musique',
        'Sport',
        'Lecture',
        'Jeux vidéo',
        'Dessin',
        'Cuisine',
        'Animaux',
        'Nature',
      ],
      avatarGenderOptions: [
        { label: 'Un garçon', value: 'boy', icon: '👦' },
        { label: 'Une fille', value: 'girl', icon: '👧' },
        { label: 'Neutre / Je ne sais pas', value: 'neutral', icon: '🤖' },
      ],
      avatarAccessoriesOptions: [
        { label: 'Casque audio', value: 'headphones', icon: '🎧' },
        { label: 'Casquette', value: 'cap', icon: '🧢' },
        { label: 'Sac à dos', value: 'backpack', icon: '🎒' },
        { label: 'Lunettes', value: 'glasses', icon: '👓' },
        { label: 'Rien de spécial', value: 'none', icon: '🚫' },
      ],
      avatarColorOptions: [
        { label: 'Bleu', value: 'blue', icon: '🔵', hex: '#1e88e5' },
        { label: 'Vert', value: 'green', icon: '🟢', hex: '#43a047' },
        { label: 'Rouge', value: 'red', icon: '🔴', hex: '#e53935' },
        { label: 'Violet', value: 'purple', icon: '🟣', hex: '#8e24aa' },
        { label: 'Orange', value: 'orange', icon: '🟠', hex: '#fb8c00' },
        { label: 'Blanc', value: 'white', icon: '⚪', hex: '#f5f5f5' },
        { label: 'Noir', value: 'black', icon: '⚫', hex: '#424242' },
      ],
      avatarPassionOptions: [
        { label: 'Jeux vidéo', value: 'videogames', icon: '🎮' },
        { label: 'Dessin / Peinture', value: 'art', icon: '🎨' },
        { label: 'Musique', value: 'music', icon: '🎵' },
        { label: 'Espace / Science', value: 'science', icon: '🚀' },
        { label: 'Nature / Animaux', value: 'nature', icon: '🏞️' },
      ],
      avatarExpressionOptions: [
        { label: 'Souriant', value: 'smiling', icon: '😄' },
        { label: 'Sérieux', value: 'serious', icon: '😐' },
        { label: 'Calme', value: 'calm', icon: '🧘‍♂️' },
        { label: 'Très joyeux', value: 'very_happy', icon: '🤩' },
      ],
      selectedPassions: [],
      selectedAccessories: [],
      responses: {
        age: '',
        name: '',
        avatarGender: '',
        avatarAccessories: '',
        avatarColor: '',
        avatarPassion: '',
        avatarExpression: '',
        passions: '',
      },
      recognition: null,
      isRecognizing: false,
    }
  },
  mounted() {
    this.updateBackgroundColor()
    this.setupSpeechRecognition()
  },
  computed: {
    imageClass() {
      return this.selectedAvatarUrl ? 'image-selected' : 'image-default'
    },
  },
  methods: {
    setupSpeechRecognition() {
      if ('webkitSpeechRecognition' in window) {
        this.recognition = new webkitSpeechRecognition()
        this.recognition.lang = 'fr-FR'
        this.recognition.continuous = false
        this.recognition.interimResults = false

        this.recognition.onstart = () => {
          console.log('Recognition started')
          this.isRecognizing = true
        }

        this.recognition.onresult = (event) => {
          const transcript =
            event.results[event.resultIndex][0].transcript.trim()
          console.log('Recognition result:', transcript)

          const currentKey = this.questions[this.currentQuestionIndex].key
          if (currentKey === 'passions') {
            // Pour les passions, on ajoute à la liste des passions sélectionnées
            const passionsArray = transcript.split(',').map((p) => p.trim())
            passionsArray.forEach((passion) => {
              if (passion && !this.selectedPassions.includes(passion)) {
                this.selectedPassions.push(passion)
              }
            })
          } else {
            // Pour les autres questions, on assigne directement la valeur
            this.responses[currentKey] = transcript
          }

          this.isRecognizing = false
          this.recognition.stop()
        }

        this.recognition.onerror = (event) => {
          console.error('Recognition error:', event.error)
          this.isRecognizing = false
        }

        this.recognition.onend = () => {
          console.log('Recognition ended')
          this.isRecognizing = false
        }
      } else {
        console.error('webkitSpeechRecognition not supported in this browser.')
      }
    },

    async createAccountAndStartGame() {
      if (this.isRegistering) return

      this.isRegistering = true
      this.registrationError = null

      try {
        // Prepare user data for registration
        const userData = {
          first_name: this.responses.name,
          last_name: '', // Optional
          age: parseInt(this.responses.age),
        }

        // Save the user's data in localStorage for profile creation later
        localStorage.setItem(
          'user_profile',
          JSON.stringify({
            name: this.responses.name,
            age: this.responses.age,
            passions: this.responses.passions,
            avatar: this.selectedAvatarUrl,
            avatarGender: this.responses.avatarGender,
            avatarAccessories: this.responses.avatarAccessories,
            avatarColor: this.responses.avatarColor,
            avatarPassion: this.responses.avatarPassion,
            avatarExpression: this.responses.avatarExpression,
          })
        )

        // Register with passkey
        const result = await AuthService.registerWithPasskey(userData)

        console.log('Passkey registration successful:', result)

        // Navigate to the first game
        this.$router.push('/game-speed')
      } catch (error) {
        console.error('Registration error:', error)
        this.registrationError =
          error.message || 'Failed to create account. Please try again.'

        // Show error message to user
        alert(this.registrationError)
      } finally {
        this.isRegistering = false
      }
    },

    toggleAvatarAccessory(accessory) {
      const index = this.selectedAccessories.indexOf(accessory)

      // Si l'accessoire est "none", on vide les autres accessoires
      if (accessory === 'none') {
        this.selectedAccessories = ['none']
        return
      }

      // Si on ajoute un accessoire et que "none" est sélectionné, on retire "none"
      if (index === -1 && this.selectedAccessories.includes('none')) {
        this.selectedAccessories = [accessory]
        return
      }

      // Sinon, on ajoute ou retire l'accessoire normalement
      if (index === -1) {
        this.selectedAccessories.push(accessory)
      } else {
        this.selectedAccessories.splice(index, 1)
      }
    },

    selectOption(key, value) {
      this.responses[key] = value
      if (key === 'age') {
        this.showCustomInput = false
      }
    },

    validateResponse(key) {
      if (this.responses[key]) {
        if (key === 'passions') {
          this.generatePicture()
        }
      }
    },

    selectPassion(passion) {
      if (!this.selectedPassions.includes(passion)) {
        this.selectedPassions.push(passion)
      } else {
        this.removePassion(this.selectedPassions.indexOf(passion))
      }
    },

    removePassion(index) {
      this.selectedPassions.splice(index, 1)
    },

    startRecognition() {
      if (this.recognition && !this.isRecognizing) {
        this.voiceInputActive = true
        this.showNameInput = false
        this.recognition.start()
      }
    },

    startTextInput() {
      this.showNameInput = true
      this.voiceInputActive = false
      this.responses.name = ''
      // Focus sur le champ de saisie
      this.$nextTick(() => {
        if (this.$refs.customNameInput) {
          this.$refs.customNameInput.focus()
        }
      })
    },

    confirmTextInput() {
      if (this.responses.name && this.responses.name.trim() !== '') {
        this.showNameInput = false
        this.validateResponse('name')
      }
    },

    cancelTextInput() {
      this.showNameInput = false
      this.responses.name = ''
    },

    startRecognitionForPassions() {
      if (this.recognition && !this.isRecognizing) {
        this.recognition.start()
      }
    },

    previousQuestion() {
      if (this.currentQuestionIndex > 0) {
        this.currentQuestionIndex--
        this.updateBackgroundColor()
      }
    },

    canProceed() {
      const currentKey = this.questions[this.currentQuestionIndex].key

      // Pour les accessoires, on vérifie si au moins un accessoire est sélectionné
      if (currentKey === 'avatarAccessories') {
        return this.selectedAccessories.length > 0
      }

      // Pour les autres questions, on vérifie si une réponse existe
      return this.responses[currentKey] !== ''
    },

    nextQuestion() {
      const currentKey = this.questions[this.currentQuestionIndex].key

      if (!this.canProceed()) {
        this.repeatQuestion()
        return
      }

      // Si on est sur la question des accessoires, on sauvegarde les accessoires sélectionnés
      if (currentKey === 'avatarAccessories') {
        this.responses.avatarAccessories = this.selectedAccessories.join(',')
      }

      if (currentKey === 'passions' && !this.showAvatarSelection) {
        this.generatePicture()
        return
      }

      this.currentQuestionIndex++
      this.updateBackgroundColor()
      this.showCustomInput = false
      this.showNameInput = false
      this.showAvatarSelection = false
    },

    shouldShowSkipButton() {
      const currentKey = this.questions[this.currentQuestionIndex].key
      // On peut sauter les questions des accessoires, de la passion et des passions générales
      return ['avatarAccessories', 'avatarPassion', 'passions'].includes(
        currentKey
      )
    },

    skipQuestion() {
      const currentKey = this.questions[this.currentQuestionIndex].key

      if (this.shouldShowSkipButton()) {
        if (currentKey === 'avatarAccessories') {
          this.responses.avatarAccessories = 'none'
          this.selectedAccessories = ['none']
        } else if (currentKey === 'avatarPassion') {
          this.responses.avatarPassion = 'none'
        } else if (currentKey === 'passions') {
          this.responses.passions = ''
        }

        this.currentQuestionIndex++
        this.updateBackgroundColor()
        this.showCustomInput = false
        this.showNameInput = false
      } else {
        // Pour les autres questions, on rappelle qu'elles sont obligatoires
        this.repeatQuestion()
      }
    },

    repeatQuestion() {
      const text = this.questions[this.currentQuestionIndex].text
      const speech = new SpeechSynthesisUtterance()
      speech.lang = 'fr-FR'
      speech.text = text.replace(
        /🎂|👤|🎨|👦|🧢|🌟|😊|🎮|🎧|🎒|👓|🚫|🔵|🟢|🔴|🟣|🟠|⚪|⚫||🚀|🏞️/gu,
        ''
      ) // Enlever les emojis pour la lecture
      window.speechSynthesis.speak(speech)
    },

    async generatePicture() {
      this.showAvatarSelection = true
      const url = process.env.VUE_APP_AZURE_OPENAI_ENDPOINT
      const apiKey = process.env.VUE_APP_AZURE_OPENAI_API_KEY

      // Construction du prompt basé sur les choix de l'avatar
      const gender =
        this.responses.avatarGender === 'boy'
          ? 'masculin'
          : this.responses.avatarGender === 'girl'
          ? 'féminin'
          : 'neutre'

      const accessoriesText =
        this.responses.avatarAccessories !== 'none'
          ? `portant les accessoires suivants : ${this.responses.avatarAccessories.replace(
              /,/g,
              ', '
            )}`
          : 'sans accessoires particuliers'

      const colorText = this.responses.avatarColor
        ? `avec des tons dominants de ${this.responses.avatarColor}`
        : ''

      const passionText =
        this.responses.avatarPassion !== 'none'
          ? `reflétant la passion pour : ${this.responses.avatarPassion}`
          : ''

      const expressionText = this.responses.avatarExpression
        ? `avec une expression ${this.responses.avatarExpression}`
        : ''

      const prompt = `Créer une illustration numérique en style cartoon réaliste, avec des traits doux, une palette de couleurs naturelle et harmonieuse.
      Le fond est gris clair, épuré et minimaliste.
      Le personnage est de genre ${gender}, ${accessoriesText}, ${colorText}, ${passionText}, ${expressionText}.
      Le style visuel est moderne, avec des proportions naturelles (pas de déformation type Funko Pop), un rendu propre et professionnel, comme une illustration d'avatar haut de gamme.
      Le personnage est vu de face, en position debout, bien éclairé, avec des détails soignés sur les vêtements et les accessoires.
      L'objectif est de produire un visuel prêt pour une utilisation professionnelle ou commerciale.`

      console.log("Envoi de la requête à l'API Azure OpenAI...")
      console.log('Prompt:', prompt)

      this.generatedImages = []
      this.isLoadingImages = true

      for (let i = 0; i < 3; i++) {
        try {
          const response = await axios.post(
            url,
            { prompt, n: 1 },
            {
              headers: {
                'Content-Type': 'application/json',
                'api-key': apiKey,
              },
            }
          )
          const imageUrl = response.data.data[0].url
          this.generatedImages.push(imageUrl)
          console.log(`Image ${i + 1} générée:`, imageUrl)
        } catch (error) {
          console.error("Erreur lors de la génération de l'image :", error)
        }
      }
      this.isLoadingImages = false
    },

    selectAvatar(imgUrl) {
      this.selectedAvatarUrl = imgUrl
      console.log('Avatar sélectionné :', imgUrl)
    },

    finalizeAvatarSelection() {
      this.showAvatarSelection = false
      this.nextQuestion()
    },

    updateBackgroundColor() {
      const colorIndex =
        this.currentQuestionIndex % this.backgroundColors.length
      this.currentBackgroundColor = this.backgroundColors[colorIndex]
    },
  },
}
</script>

<style scoped>
@import url('@/assets/styles.css');

.questionnaire {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  text-align: center;
  padding: 15px;
  height: 100vh;
  max-height: 100vh;
  overflow: hidden;
  transition: background-color 0.5s ease;
  width: 100%;
  max-width: 100%;
}

.title {
  font-family: 'Glacial Indifference', sans-serif;
  font-weight: bold;
  font-size: 2.2rem;
  margin-top: 0.8rem;
  margin-bottom: 1.5rem;
  color: #333;
}

.content-container {
  display: flex;
  justify-content: space-between;
  width: 95%;
  max-width: 1200px;
  margin: 0 auto;
}

.left-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 40%;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.right-section {
  display: flex;
  flex-direction: column;
  width: 58%;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.image-default {
  width: 180px;
  height: 180px;
  object-fit: contain;
  margin: 0.5rem 0 1.5rem;
  border-radius: 10px;
}

.image-selected {
  width: 200px;
  height: 200px;
  object-fit: contain;
  margin: 0.5rem 0 1.5rem;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.question-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.sub-title {
  font-family: 'Glacial Indifference', sans-serif;
  font-weight: bold;
  font-size: 1.6rem;
  margin-bottom: 1rem;
  color: #333;
  text-align: center;
}

.action-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.7rem 1.3rem;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 50px;
  background-color: #4a90e2;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 3px 5px rgba(0, 0, 0, 0.2);
  margin: 0.5rem;
}

.action-button:hover {
  background-color: #357abd;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.action-button:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.action-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.listen-button {
  background-color: #6d4c41;
}

.listen-button:hover {
  background-color: #5d4037;
}

.speak-button {
  background-color: #009688;
  min-width: 200px;
}

.speak-button:hover {
  background-color: #00796b;
}

.speak-button.active {
  background-color: #f44336;
  animation: pulse 1.5s infinite;
}

.icon {
  margin-right: 8px;
  font-size: 1.2rem;
}

.next-button {
  background-color: #66bb6a;
}

.next-button:hover {
  background-color: #4caf50;
}

.prev-button {
  background-color: #78909c;
}

.prev-button:hover {
  background-color: #607d8b;
}

.skip-button {
  background-color: #ffb74d;
  color: #333;
}

.skip-button:hover {
  background-color: #ffa726;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  width: 100%;
  margin: 0.8rem 0;
}

.avatar-gender-grid,
.avatar-expression-grid {
  grid-template-columns: repeat(3, 1fr);
}

.avatar-color-grid {
  grid-template-columns: repeat(4, 1fr);
}

.avatar-option-container {
  position: relative;
  padding: 5px;
}

.avatar-option-icon {
  font-size: 2rem;
  display: block;
  margin-bottom: 5px;
}

.avatar-option-text {
  display: block;
  font-size: 0.9rem;
}

.avatar-options-container {
  width: 100%;
  margin-top: 1rem;
}

.avatar-color-option {
  color: white;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
  border: 3px solid transparent;
}

.avatar-color-option.selected {
  border-color: #2196f3;
  box-shadow: 0 0 10px rgba(33, 150, 243, 0.5);
}

.selected-items {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
}

.confirm-selection {
  margin-top: 0.5rem;
}

.option-button {
  padding: 12px 8px;
  font-size: 1.1rem;
  background-color: #e0e0e0;
  border: 2px solid #e0e0e0;
  color: #333;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.option-button:hover {
  background-color: #d4d4d4;
  transform: translateY(-2px);
}

.option-button.selected {
  background-color: #bbdefb;
  border-color: #2196f3;
  color: #0d47a1;
  font-weight: bold;
}

.option-button.custom {
  background-color: #ffd54f;
  border-color: #ffd54f;
}

.option-button.custom:hover {
  background-color: #ffca28;
}

.option-button.text-option {
  width: 100%;
  max-width: 300px;
  margin: 0 auto;
}

.passion-button {
  background-color: #e3f2fd;
  border-color: #e3f2fd;
}

.passion-button:hover {
  background-color: #bbdefb;
}

.custom-input-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 300px;
  margin: 1rem auto;
}

.button-group {
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 10px;
  width: 100%;
}

.cancel-button {
  background-color: #f44336;
}

.small-input {
  padding: 15px;
  width: 100%;
  font-size: 1.1rem;
  margin-bottom: 10px;
  border: 2px solid #bdbdbd;
  border-radius: 10px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.small-input:focus {
  border-color: #2196f3;
  box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.3);
  outline: none;
}

.voice-input-container {
  margin: 1.5rem 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.speech-result {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 10px;
  width: 100%;
  max-width: 500px;
}

.confirm-buttons {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
  gap: 1rem;
}

.action-button.confirm {
  background-color: #4caf50;
}

.action-button.retry {
  background-color: #ff9800;
}

.selected-passions {
  margin-top: 1.5rem;
  width: 100%;
}

.passions-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  margin: 1rem 0;
}

.passion-tag {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  background-color: #bbdefb;
  border-radius: 20px;
  font-size: 0.9rem;
  color: #0d47a1;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.remove-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  background-color: #0d47a1;
  color: white;
  border: none;
  border-radius: 50%;
  margin-left: 8px;
  cursor: pointer;
  font-size: 0.8rem;
  line-height: 1;
}

.confirm-passions {
  margin-top: 1rem;
}

.navigation-buttons {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  margin-top: 2rem;
  gap: 10px;
}

.avatar-selection-container {
  width: 90%;
  max-width: 1000px;
  margin: 1rem auto;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.avatar-selection {
  width: 100%;
}

.avatars-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  margin-top: 1rem;
}

.avatar-option-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: white;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
  max-width: 220px;
}

.avatar-option-container.selected {
  box-shadow: 0 0 0 3px #2196f3, 0 5px 10px rgba(0, 0, 0, 0.25);
  transform: translateY(-3px);
}

.avatar-option {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.avatar-option:hover {
  transform: scale(1.02);
}

.select-avatar-button {
  margin-top: 0.8rem;
  padding: 0.6rem 1.2rem;
  background-color: #9c27b0;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.select-avatar-button:hover {
  background-color: #7b1fa2;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 2rem 0;
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.completion-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 3rem;
  background-color: rgba(255, 255, 255, 0.9);
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 60%;
  max-width: 600px;
}

.start-game-button {
  background-color: #673ab7;
  padding: 1rem 2rem;
  font-size: 1.2rem;
  margin-top: 1.5rem;
}

.start-game-button:hover {
  background-color: #5e35b1;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(244, 67, 54, 0.4);
  }

  70% {
    box-shadow: 0 0 0 10px rgba(244, 67, 54, 0);
  }

  100% {
    box-shadow: 0 0 0 0 rgba(244, 67, 54, 0);
  }
}

/* Responsive adjustments */
@media (max-width: 900px) {
  .content-container {
    flex-direction: column;
    align-items: center;
  }

  .left-section,
  .right-section {
    width: 95%;
    margin-bottom: 1rem;
  }

  .image-default,
  .image-selected {
    width: 150px;
    height: 150px;
  }
}

@media (max-width: 768px) {
  .options-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .title {
    font-size: 1.5rem;
  }

  .sub-title {
    font-size: 1.2rem;
  }

  .options-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .image-default,
  .image-selected {
    width: 120px;
    height: 120px;
  }
}

/* Loading spinner styles */
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 20px 0;
}

.spinner {
  border: 4px solid rgba(0, 123, 255, 0.1);
  border-radius: 50%;
  border-top: 4px solid #007bff;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 1em;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
  transform: none;
}
</style>
