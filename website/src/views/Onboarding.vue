<template>
  <div class="onboarding-container">
    <!-- Space Background Component -->
    <SpaceBackground
      v-if="currentStep >= 1"
      :theme="selectedTheme"
      :animationsEnabled="true"
      class="background-container"
    />

    <!-- Progress indicator -->
    <div v-if="currentStep > 1" class="progress-bar">
      <div
        class="progress-indicator"
        :style="{ width: progressPercentage + '%' }"
      ></div>
    </div>

    <!-- Main Content Container -->
    <div class="content-container">
      <!-- Step 1: Theme Selection -->
      <div v-if="currentStep === 1" class="step-container theme-selection">
        <!-- <h1 class="step-title">Choisis ton thème préféré</h1> -->
        <div class="flamou-container">
          <img
            :src="flamouImages.happy"
            alt="Flamou heureux"
            class="flamou-image"
          />
          <div class="flamou-speech-bubble">
            <p>
              Bonjour ! Je m'appelle Flamou. Commençons par choisir un thème que
              tu aimes !
            </p>
          </div>
        </div>
        <div class="themes-grid">
          <div
            v-for="theme in availableThemes"
            :key="theme.id"
            class="theme-card"
            :class="{ selected: selectedTheme === theme.id }"
            @click="selectTheme(theme.id)"
          >
            <div class="theme-emoji">{{ theme.emoji }}</div>
            <p class="theme-name">{{ theme.name }}</p>
          </div>
        </div>
        <div class="navigation-buttons">
          <button
            class="next-button"
            @click="nextStep"
            :disabled="!selectedTheme"
          >
            Continuer
          </button>
        </div>
      </div>

      <!-- Step 2: Age Input -->
      <div v-if="currentStep === 2" class="step-container">
        <h1 class="step-title">Quel âge as-tu ?</h1>
        <div class="flamou-container">
          <img
            :src="flamouImages.normal"
            alt="Flamou normal"
            class="flamou-image"
          />
          <div class="flamou-speech-bubble">
            <p>
              Peux-tu me dire quel âge tu as ? Tu peux utiliser les boutons + et
              - pour choisir.
            </p>
          </div>
        </div>
        <div class="input-container age-input-container">
          <button @click="decrementAge" class="age-button decrease-button">
            -
          </button>
          <input
            type="number"
            v-model="responses.age"
            class="age-input"
            placeholder="Ton âge"
            min="1"
            max="99"
          />
          <button @click="incrementAge" class="age-button increase-button">
            +
          </button>
        </div>
        <div class="navigation-buttons">
          <button class="back-button" @click="previousStep">Retour</button>
          <button
            class="next-button"
            @click="nextStep"
            :disabled="!responses.age || responses.age < 1"
          >
            Continuer
          </button>
        </div>
      </div>

      <!-- Step 3: Nickname Input -->
      <div v-if="currentStep === 3" class="step-container">
        <h1 class="step-title">Quel est ton surnom ?</h1>
        <div class="flamou-container">
          <img
            :src="flamouImages.normal"
            alt="Flamou normal"
            class="flamou-image"
          />
          <div class="flamou-speech-bubble">
            <p>Comment aimerais-tu qu'on t'appelle ? Entre ton surnom ici.</p>
          </div>
        </div>
        <div class="input-container">
          <input
            type="text"
            v-model="responses.nickname"
            class="nickname-input"
            placeholder="Ton surnom"
            maxlength="20"
          />
        </div>
        <div class="navigation-buttons">
          <button class="back-button" @click="previousStep">Retour</button>
          <button
            class="next-button"
            @click="nextStep"
            :disabled="!responses.nickname"
          >
            Continuer
          </button>
        </div>
      </div>

      <!-- Step 4: Gender Selection -->
      <div v-if="currentStep === 4" class="step-container">
        <h1 class="step-title">Ton personnage est...</h1>
        <div class="flamou-container">
          <img
            :src="flamouImages.interesting"
            alt="Flamou intéressé"
            class="flamou-image"
          />
          <div class="flamou-speech-bubble">
            <p>
              Maintenant, créons ton avatar ! Est-ce que ton personnage est un
              garçon, une fille, ou tu préfères ne pas choisir ?
            </p>
          </div>
        </div>
        <div class="gender-container">
          <div
            class="gender-option"
            :class="{ selected: responses.avatarGender === 'boy' }"
            @click="responses.avatarGender = 'boy'"
          >
            <div class="gender-image boy-image">👦</div>
            <p>Garçon</p>
          </div>
          <div
            class="gender-option"
            :class="{ selected: responses.avatarGender === 'girl' }"
            @click="responses.avatarGender = 'girl'"
          >
            <div class="gender-image girl-image">👧</div>
            <p>Fille</p>
          </div>
          <div
            class="gender-option"
            :class="{ selected: responses.avatarGender === 'neutral' }"
            @click="responses.avatarGender = 'neutral'"
          >
            <div class="gender-image neutral-image">🤖</div>
            <p>Je ne veux pas choisir</p>
          </div>
        </div>
        <div class="help-text">
          <p>Tu peux choisir ce que tu préfères. Tu peux aussi passer.</p>
        </div>
        <div class="navigation-buttons">
          <button class="back-button" @click="previousStep">Retour</button>
          <button class="next-button" @click="nextStep">Continuer</button>
        </div>
      </div>

      <!-- Step 5: Accessories Selection -->
      <div v-if="currentStep === 5" class="step-container">
        <h1 class="step-title">Choisis ce que ton personnage porte</h1>
        <div class="flamou-container">
          <img
            :src="flamouImages.normal"
            alt="Flamou normal"
            class="flamou-image"
          />
          <div class="flamou-speech-bubble">
            <p>
              Tu peux choisir ce que ton personnage porte. C'est toi qui
              choisis.
            </p>
          </div>
        </div>
        <div class="accessories-container">
          <div
            class="accessory-option"
            :class="{ selected: accessories.includes('casque') }"
            @click="toggleAccessory('casque')"
          >
            <div class="accessory-image">🎧</div>
            <p>Casque</p>
          </div>
          <div
            class="accessory-option"
            :class="{ selected: accessories.includes('casquette') }"
            @click="toggleAccessory('casquette')"
          >
            <div class="accessory-image">🧢</div>
            <p>Casquette</p>
          </div>
          <div
            class="accessory-option"
            :class="{ selected: accessories.includes('lunettes') }"
            @click="toggleAccessory('lunettes')"
          >
            <div class="accessory-image">👓</div>
            <p>Lunettes</p>
          </div>
          <div
            class="accessory-option"
            :class="{ selected: accessories.includes('sac à dos') }"
            @click="toggleAccessory('sac à dos')"
          >
            <div class="accessory-image">🎒</div>
            <p>Sac à dos</p>
          </div>
          <div
            class="accessory-option"
            :class="{ selected: accessories.length === 0 }"
            @click="accessories = []"
          >
            <div class="accessory-image">❌</div>
            <p>Rien</p>
          </div>
        </div>
        <div class="navigation-buttons">
          <button class="back-button" @click="previousStep">Retour</button>
          <button class="skip-button" @click="skipStep">
            Je ne sais pas / Je veux passer
          </button>
          <button class="next-button" @click="nextStep">Continuer</button>
        </div>
      </div>

      <!-- Step 6: Color Selection -->
      <div v-if="currentStep === 6" class="step-container">
        <h1 class="step-title">Quelle est ta couleur préférée ?</h1>
        <div class="flamou-container">
          <img
            :src="flamouImages.interesting"
            alt="Flamou intéressé"
            class="flamou-image"
          />
          <div class="flamou-speech-bubble">
            <p>
              Choisis la couleur que tu aimes le plus. Elle servira à décorer
              ton personnage.
            </p>
          </div>
        </div>
        <div class="colors-container">
          <div
            v-for="color in availableColors"
            :key="color.id"
            class="color-option"
            :class="{ selected: responses.avatarColor === color.name }"
            :style="{ backgroundColor: color.hex }"
            @click="responses.avatarColor = color.name"
          ></div>
        </div>
        <div class="navigation-buttons">
          <button class="back-button" @click="previousStep">Retour</button>
          <button class="skip-button" @click="skipColorStep">
            Je ne sais pas
          </button>
          <button class="next-button" @click="nextStep">Continuer</button>
        </div>
      </div>

      <!-- Step 7: Passion Selection -->
      <div v-if="currentStep === 7" class="step-container">
        <h1 class="step-title">Qu'est-ce que tu aimes faire ?</h1>
        <div class="flamou-container">
          <img
            :src="flamouImages.happy"
            alt="Flamou heureux"
            class="flamou-image"
          />
          <div class="flamou-speech-bubble">
            <p>
              Choisis ce que tu aimes le plus. Il n'y a pas de mauvaise réponse.
            </p>
          </div>
        </div>
        <div class="passions-container">
          <div
            v-for="passion in availablePassions"
            :key="passion.id"
            class="passion-option"
            :class="{ selected: responses.avatarPassion === passion.name }"
            @click="responses.avatarPassion = passion.name"
          >
            <div class="passion-image">{{ passion.emoji }}</div>
            <p>{{ passion.name }}</p>
          </div>
        </div>
        <div class="navigation-buttons">
          <button class="back-button" @click="previousStep">Retour</button>
          <button class="skip-button" @click="skipPassionStep">
            Je ne sais pas
          </button>
          <button class="next-button" @click="nextStep">Continuer</button>
        </div>
      </div>

      <!-- Step 8: Expression Selection -->
      <div v-if="currentStep === 8" class="step-container">
        <h1 class="step-title">Ton personnage a quelle expression ?</h1>
        <div class="flamou-container">
          <img
            :src="flamouImages.interesting"
            alt="Flamou intéressé"
            class="flamou-image"
          />
          <div class="flamou-speech-bubble">
            <p>Choisis le visage qui te ressemble ou que tu préfères.</p>
          </div>
        </div>
        <div class="expressions-container">
          <div
            v-for="expression in availableExpressions"
            :key="expression.id"
            class="expression-option"
            :class="{
              selected: responses.avatarExpression === expression.name,
            }"
            @click="responses.avatarExpression = expression.name"
          >
            <div class="expression-emoji">{{ expression.emoji }}</div>
            <p>{{ expression.name }}</p>
          </div>
        </div>
        <div class="navigation-buttons">
          <button class="back-button" @click="previousStep">Retour</button>
          <button class="skip-button" @click="skipExpressionStep">
            Je ne sais pas
          </button>
          <button class="next-button" @click="nextStep">Continuer</button>
        </div>
      </div>

      <!-- Step 9: Generating Avatars -->
      <div v-if="currentStep === 9" class="step-container">
        <h1 class="step-title">Génération de tes avatars</h1>
        <div class="flamou-container">
          <img
            :src="flamouImages.interesting"
            alt="Flamou intéressé"
            class="flamou-image animated-bounce"
          />
          <div class="flamou-speech-bubble">
            <p>
              {{ loadingText }} Patiente un peu, nous créons tes personnages...
            </p>
          </div>
        </div>
        <div class="loading-container">
          <div class="loading-spinner"></div>
          <p class="loading-text">{{ loadingText }}</p>
        </div>
      </div>

      <!-- Step 10: Avatar Selection -->
      <div v-if="currentStep === 10" class="step-container">
        <h1 class="step-title">Choisis ton avatar préféré</h1>
        <div class="flamou-container">
          <img
            :src="flamouImages.happy"
            alt="Flamou heureux"
            class="flamou-image"
          />
          <div class="flamou-speech-bubble">
            <p>Voici tes avatars ! Clique sur celui que tu préfères.</p>
          </div>
        </div>
        <div class="avatars-container">
          <div
            v-for="(avatar, index) in generatedAvatars"
            :key="index"
            class="avatar-option"
            :class="{ selected: selectedAvatarIndex === index }"
            @click="selectedAvatarIndex = index"
          >
            <img :src="avatar" alt="Avatar option" class="avatar-image" />
          </div>
        </div>
        <div class="navigation-buttons">
          <button class="back-button" @click="previousStep">Retour</button>
          <button
            class="next-button"
            @click="nextStep"
            :disabled="selectedAvatarIndex === null"
          >
            Continuer
          </button>
        </div>
      </div>
      <!-- Step 11: Récapitulatif et création du compte -->
      <div v-if="currentStep === 11" class="step-container summary-container">
        <h1 class="step-title">Récapitulatif</h1>
        <div class="flamou-container">
          <img
            :src="flamouImages.happy"
            alt="Flamou heureux"
            class="flamou-image"
          />
          <div class="flamou-speech-bubble">
            <p>
              Super ! Vérifie si tout est correct avant de créer ton compte.
            </p>
          </div>
        </div>

        <div class="summary-content">
          <div class="summary-avatar">
            <img
              :src="selectedAvatarUrl"
              alt="Avatar sélectionné"
              class="selected-avatar-image"
            />
          </div>

          <div class="summary-details">
            <div class="summary-item">
              <span class="summary-label">Surnom:</span>
              <span class="summary-value">{{ responses.nickname }}</span>
            </div>

            <div class="summary-item">
              <span class="summary-label">Âge:</span>
              <span class="summary-value">{{ responses.age }} ans</span>
            </div>

            <div class="summary-item">
              <span class="summary-label">Thème préféré:</span>
              <span class="summary-value">
                {{ getThemeName(selectedTheme) }}
              </span>
            </div>

            <div class="summary-item">
              <span class="summary-label">Genre:</span>
              <span class="summary-value">
                {{ getGenderLabel(responses.avatarGender) }}
              </span>
            </div>

            <div
              class="summary-item"
              v-if="
                responses.avatarAccessories &&
                responses.avatarAccessories !== 'none'
              "
            >
              <span class="summary-label">Accessoires:</span>
              <span class="summary-value">
                {{ responses.avatarAccessories.replace(/,/g, ', ') }}
              </span>
            </div>

            <div class="summary-item" v-if="responses.avatarColor">
              <span class="summary-label">Couleur préférée:</span>
              <span class="summary-value">{{ responses.avatarColor }}</span>
            </div>

            <div
              class="summary-item"
              v-if="
                responses.avatarPassion && responses.avatarPassion !== 'none'
              "
            >
              <span class="summary-label">Passion:</span>
              <span class="summary-value">{{ responses.avatarPassion }}</span>
            </div>

            <div class="summary-item" v-if="responses.avatarExpression">
              <span class="summary-label">Expression:</span>
              <span class="summary-value">
                {{ responses.avatarExpression }}
              </span>
            </div>
          </div>
        </div>

        <div class="navigation-buttons">
          <button class="back-button" @click="previousStep">Modifier</button>
          <button
            class="create-account-button"
            @click="createAccountAndStartGame"
            :disabled="isRegistering"
          >
            {{ isRegistering ? 'Création en cours...' : 'Créer mon compte' }}
          </button>
        </div>

        <div v-if="registrationError" class="error-message">
          {{ registrationError }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SpaceBackground from '@/components/SpaceBackground.vue'
import { AzureOpenAI } from 'openai'
import AuthService from '@/services/AuthService'

export default {
  name: 'UserOnboarding',
  components: {
    SpaceBackground,
  },
  data() {
    return {
      currentStep: 1,
      selectedTheme: 'cosmic',
      accessories: [],
      loadingText: 'Création de ton avatar...',
      loadingProgress: 0,
      selectedAvatarIndex: null,
      generatedAvatars: [],
      flamouImages: {
        happy: require('@/assets/flamou/happy.png'),
        normal: require('@/assets/flamou/normal.png'),
        interesting: require('@/assets/flamou/intresting.png'),
        sleepy: require('@/assets/flamou/blased.png'),
      },
      availableThemes: [
        { id: 'cosmic', name: 'Espace', emoji: '🌌' },
        { id: 'ocean', name: 'Océan', emoji: '🌊' },
        { id: 'cyberpunk', name: 'Cyberpunk', emoji: '🤖' },
        { id: 'forest', name: 'Forêt', emoji: '🌳' },
        { id: 'snow', name: 'Neige', emoji: '❄️' },
      ],
      availableColors: [
        { id: 'blue', name: 'bleu', hex: '#1a73e8' },
        { id: 'green', name: 'vert', hex: '#34a853' },
        { id: 'red', name: 'rouge', hex: '#ea4335' },
        { id: 'purple', name: 'violet', hex: '#9c27b0' },
        { id: 'orange', name: 'orange', hex: '#ff9800' },
        { id: 'white', name: 'blanc', hex: '#ffffff' },
        { id: 'black', name: 'noir', hex: '#202124' },
      ],
      availablePassions: [
        { id: 'games', name: 'jeux vidéo', emoji: '🎮' },
        { id: 'art', name: 'dessin ou peinture', emoji: '🎨' },
        { id: 'music', name: 'musique', emoji: '🎵' },
        { id: 'space', name: 'espace', emoji: '🚀' },
        { id: 'animals', name: 'animaux', emoji: '🐶' },
      ],
      availableExpressions: [
        { id: 'happy', name: 'souriant', emoji: '😀' },
        { id: 'calm', name: 'calme', emoji: '😐' },
        { id: 'excited', name: 'très content', emoji: '🤩' },
        { id: 'tired', name: 'fatigué', emoji: '😴' },
      ],
      responses: {
        age: 18,
        nickname: '',
        avatarGender: null,
        avatarAccessories: null,
        avatarColor: null,
        avatarPassion: null,
        avatarExpression: null,
      },
      totalSteps: 11,
      isRegistering: false,
      registrationError: null,
    }
  },
  computed: {
    progressPercentage() {
      return ((this.currentStep - 1) / (this.totalSteps - 1)) * 100
    },
    selectedAvatarUrl() {
      if (
        this.selectedAvatarIndex !== null &&
        this.generatedAvatars.length > this.selectedAvatarIndex
      ) {
        return this.generatedAvatars[this.selectedAvatarIndex]
      }
      return null
    },
  },
  methods: {
    selectTheme(themeId) {
      this.selectedTheme = themeId
    },
    incrementAge() {
      if (this.responses.age < 99) {
        this.responses.age++
      }
    },
    decrementAge() {
      if (this.responses.age > 1) {
        this.responses.age--
      }
    },
    toggleAccessory(accessory) {
      const index = this.accessories.indexOf(accessory)
      if (index === -1) {
        this.accessories.push(accessory)
      } else {
        this.accessories.splice(index, 1)
      }
      this.responses.avatarAccessories = this.accessories.join(',')
    },
    nextStep() {
      // Set accessory response before moving to next step
      if (this.currentStep === 5) {
        this.responses.avatarAccessories =
          this.accessories.length > 0 ? this.accessories.join(',') : 'none'
      }

      // Move to next step
      this.currentStep++

      // If on the avatar generation step, trigger avatar generation
      if (this.currentStep === 9) {
        this.generateAvatars()
      }
    },
    previousStep() {
      if (this.currentStep > 1) {
        this.currentStep--
      }
    },
    skipStep() {
      if (this.currentStep === 5) {
        this.accessories = []
        this.responses.avatarAccessories = 'none'
      }
      this.nextStep()
    },
    skipColorStep() {
      this.responses.avatarColor = null
      this.nextStep()
    },
    skipPassionStep() {
      this.responses.avatarPassion = 'none'
      this.nextStep()
    },
    skipExpressionStep() {
      this.responses.avatarExpression = null
      this.nextStep()
    },
    async generateAvatars() {
      this.generatedAvatars = []
      this.loadingProgress = 0
      const url = process.env.VUE_APP_AZURE_OPENAI_ENDPOINT
      const apiKey = process.env.VUE_APP_AZURE_OPENAI_API_KEY

      this.loadingText = 'Création de ton avatar...'
      try {
        // Configuration du client Azure OpenAI
        const client = new AzureOpenAI({
          apiKey: apiKey,
          endpoint: url,
          apiVersion: '2024-02-01',
          dangerouslyAllowBrowser: true,
        })

        // Générer 3 avatars différents
        for (let i = 0; i < 3; i++) {
          this.loadingText = `Création de l'avatar ${i + 1}/3...`

          // Construction du prompt basé sur les choix de l'avatar
          const gender =
            this.responses.avatarGender === 'boy'
              ? 'masculin'
              : this.responses.avatarGender === 'girl'
                ? 'féminin'
                : 'neutre'

          const accessoriesText =
            this.responses.avatarAccessories !== 'none'
              ? `portant les accessoires suivants : ${this.responses.avatarAccessories.replace(/,/g, ', ')}`
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

          const prompt = `
Créer une illustration numérique en style cartoon réaliste 2D, traits doux,
palette de couleurs naturelle et harmonieuse, rendu propre et professionnel.

Fond : blanc uni pur (#FFFFFF), sans motif, sans dégradé, sans ombre.
Aucun objet, décor, texte ou palette de couleurs autour du personnage.

Personnage : de genre ${gender}, ${accessoriesText}, ${colorText}, ${passionText}, ${expressionText}.
Vue de face, position debout, proportions naturelles,
cadré et centré dans l’image, bien éclairé, détails soignés sur vêtements et accessoires.

Objectif : obtenir un avatar haut de gamme, isolé sur fond blanc, prêt pour un détourage automatique et une utilisation professionnelle ou commerciale.
`.trim()

          console.log(
            `Envoi de la requête ${i + 1} à l'API Azure OpenAI DALL-E…`,
          )
          console.log('Prompt:', prompt)

          try {
            // Appel à l'API DALL-E via Azure
            const result = await client.images.generate({
              model: 'dall-e-3', // le nom de votre déploiement DALL-E 3
              prompt: prompt,
              n: 1,
            })

            // Traitement du résultat pour obtenir l'URL de l'image
            const resultJson = JSON.parse(JSON.stringify(result))
            const imageUrl = resultJson.data[0].url

            this.generatedAvatars.push(imageUrl)
            console.log(`Image ${i + 1} générée:`, imageUrl)

            // Mettre à jour la progression
            this.loadingProgress = ((i + 1) / 3) * 100

            // Ajouter un délai entre les requêtes pour éviter les limitations d'API
            if (i < 2) {
              await new Promise((resolve) => setTimeout(resolve, 1000))
            }
          } catch (error) {
            console.error(
              `Erreur lors de la génération de l'image ${i + 1}:`,
              error,
            )
            // Ajouter une image de remplacement en cas d'erreur
            this.generatedAvatars.push(
              `/images/avatars/fallback-avatar-${i + 1}.jpg`,
            )
          }
        }

        // Après la génération de tous les avatars, passer à l'étape de sélection
        setTimeout(() => {
          this.currentStep = 10
        }, 1000)
      } catch (error) {
        console.error(
          'Erreur générale lors de la génération des avatars:',
          error,
        )
        this.loadingText = 'Une erreur est survenue. Réessayons...'

        // Fallback à des avatars prédéfinis en cas d'erreur globale
        setTimeout(() => {
          this.generatedAvatars = [
            '/images/avatars/fallback-avatar-1.jpg',
            '/images/avatars/fallback-avatar-2.jpg',
            '/images/avatars/fallback-avatar-3.jpg',
          ]
          this.currentStep = 10
        }, 2000)
      }
    },
    // Cette méthode n'est plus utilisée, remplacée par l'appel API réel
    // simulateAvatarGeneration(index) {
    //   // In a real implementation, this would be a call to OpenAI's API
    //   return new Promise((resolve) => {
    //     setTimeout(() => {
    //       // For this simulation, we're using placeholder images
    //       // In a real implementation, you would use the response from OpenAI
    //       this.generatedAvatars.push(`/images/avatars/generated-avatar-${index + 1}.jpg`);
    //
    //       this.loadingProgress = ((index + 1) / 3) * 100;
    //       this.loadingText = `Création de l'avatar ${index + 1}/3...`;
    //
    //       resolve();
    //     }, 2000); // Simulate API delay
    //   });
    // },
    getThemeName(themeId) {
      const theme = this.availableThemes.find((t) => t.id === themeId)
      return theme ? theme.name : ''
    },

    getGenderLabel(gender) {
      if (gender === 'boy') return 'Garçon'
      if (gender === 'girl') return 'Fille'
      return 'Neutre'
    },

    async createAccountAndStartGame() {
      if (this.isRegistering) return

      this.isRegistering = true
      this.registrationError = null

      try {
        // Prepare user data for registration
        const userData = {
          first_name: this.responses.nickname,
          last_name: '', // Optional
          age: parseInt(this.responses.age),
        }

        // Save the user's data in localStorage for profile creation later
        localStorage.setItem(
          'user_profile',
          JSON.stringify({
            name: this.responses.nickname,
            age: this.responses.age,
            theme: this.selectedTheme,
            avatar: this.selectedAvatarUrl,
            avatarGender: this.responses.avatarGender,
            avatarAccessories: this.responses.avatarAccessories,
            avatarColor: this.responses.avatarColor,
            avatarPassion: this.responses.avatarPassion,
            avatarExpression: this.responses.avatarExpression,
          }),
        )

        console.log('user data', userData)

        // Register with passkey
        const result = await AuthService.registerWithPasskey(userData)

        console.log('Passkey registration successful:', result)

        this.$router.push('/dashboard')
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

    finishOnboarding() {
      this.nextStep()
    },
  },
}
</script>

<style scoped>
@font-face {
  font-family: 'GlacialIndifference';
  src: url('@/assets/fonts/GlacialIndifference-Regular.otf') format('opentype');
  font-weight: normal;
  font-style: normal;
}

.onboarding-container {
  width: 100%;
  height: 100vh;
  position: relative;
  overflow: hidden;
  font-family: 'Roboto', 'Arial', sans-serif;
  color: #ffffff;
}

.background-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}

.progress-bar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 8px;
  background-color: rgba(255, 255, 255, 0.2);
  z-index: 10;
}

.progress-indicator {
  height: 100%;
  background-color: #4285f4;
  transition: width 0.3s ease-in-out;
}

.content-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  padding: 20px;
  box-sizing: border-box;
  z-index: 1;
}

.step-container {
  background-color: rgba(0, 0, 0, 0.7);
  border-radius: 20px;
  padding: 30px;
  max-width: 800px;
  width: 100%;
  text-align: center;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
  animation: fadeIn 0.5s ease-in-out;
}

.step-title {
  font-size: 2rem;
  margin-bottom: 20px;
  color: #ffffff;
}

.subtitle {
  font-size: 1.2rem;
  margin-bottom: 20px;
  color: #e0e0e0;
}

.navigation-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
}

.back-button,
.next-button,
.skip-button {
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.back-button {
  background-color: transparent;
  color: #ffffff;
  border: 2px solid #ffffff;
}

.next-button {
  background-color: #4285f4;
  color: white;
}

.next-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.skip-button {
  background-color: transparent;
  color: #ffffff;
  text-decoration: underline;
}

.back-button:hover,
.skip-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.next-button:hover:not(:disabled) {
  background-color: #2a75e5;
}

/* Theme Selection Styles */
.themes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.theme-card {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid transparent;
}

.theme-card.selected {
  border-color: #4285f4;
  background-color: rgba(66, 133, 244, 0.2);
}

.theme-card:hover:not(.selected) {
  background-color: rgba(255, 255, 255, 0.2);
}

.theme-emoji {
  font-size: 5rem;
  margin-bottom: 15px;
}

.theme-name {
  font-size: 1.2rem;
  color: #ffffff;
}

/* Age and Nickname Input Styles */
.input-container {
  display: flex;
  justify-content: center;
  margin: 30px 0;
}

.age-input-container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.age-button {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: rgba(66, 133, 244, 0.8);
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  margin: 0 15px;
}

.age-button:hover {
  background-color: rgba(66, 133, 244, 1);
  transform: scale(1.1);
}

.age-button:active {
  transform: scale(0.95);
}

.age-input {
  width: 120px;
  padding: 15px;
  font-size: 1.5rem;
  text-align: center;
  border-radius: 8px;
  border: none;
  background-color: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  transition: all 0.2s ease;
}

.age-input:focus {
  outline: none;
  box-shadow: 0 0 0 2px #4285f4;
}

.nickname-input {
  width: 300px;
  padding: 15px;
  font-size: 1.5rem;
  text-align: center;
  border-radius: 8px;
  border: none;
  background-color: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  transition: all 0.2s ease;
}

.nickname-input:focus {
  outline: none;
  box-shadow: 0 0 0 2px #4285f4;
}

/* Gender Selection Styles */
.gender-container {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin: 30px 0;
}

.gender-option {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid transparent;
  width: 150px;
}

.gender-option.selected {
  border-color: #4285f4;
  background-color: rgba(66, 133, 244, 0.2);
}

.gender-option:hover:not(.selected) {
  background-color: rgba(255, 255, 255, 0.2);
}

.gender-image {
  font-size: 4rem;
  margin-bottom: 10px;
}

.help-text {
  margin-top: 20px;
  color: #e0e0e0;
  font-style: italic;
}

/* Accessories Selection Styles */
.accessories-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  margin: 30px 0;
}

.accessory-option {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid transparent;
  width: 120px;
}

.accessory-option.selected {
  border-color: #4285f4;
  background-color: rgba(66, 133, 244, 0.2);
}

.accessory-option:hover:not(.selected) {
  background-color: rgba(255, 255, 255, 0.2);
}

.accessory-image {
  font-size: 3rem;
  margin-bottom: 10px;
}

/* Color Selection Styles */
.colors-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  margin: 30px 0;
}

.color-option {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 4px solid transparent;
}

.color-option.selected {
  border-color: #ffffff;
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.5);
}

.color-option:hover:not(.selected) {
  transform: scale(1.1);
}

/* Passion Selection Styles */
.passions-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  margin: 30px 0;
}

.passion-option {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid transparent;
  width: 140px;
}

.passion-option.selected {
  border-color: #4285f4;
  background-color: rgba(66, 133, 244, 0.2);
}

.passion-option:hover:not(.selected) {
  background-color: rgba(255, 255, 255, 0.2);
}

.passion-image {
  font-size: 3.5rem;
  margin-bottom: 10px;
}

/* Expression Selection Styles */
.expressions-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  margin: 30px 0;
}

.expression-option {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid transparent;
  width: 120px;
}

.expression-option.selected {
  border-color: #4285f4;
  background-color: rgba(66, 133, 244, 0.2);
}

.expression-option:hover:not(.selected) {
  background-color: rgba(255, 255, 255, 0.2);
}

.expression-emoji {
  font-size: 3.5rem;
  margin-bottom: 10px;
}

/* Loading Styles */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 40px 0;
}

.loading-spinner {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 6px solid rgba(255, 255, 255, 0.1);
  border-top-color: #4285f4;
  animation: spin 1.5s linear infinite;
}

.loading-text {
  margin-top: 20px;
  font-size: 1.2rem;
  color: #e0e0e0;
}

/* Avatar Selection Styles */
.avatars-container {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin: 30px 0;
}

.avatar-option {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 3px solid transparent;
  width: 180px;
}

.avatar-option.selected {
  border-color: #4285f4;
  background-color: rgba(66, 133, 244, 0.2);
}

.avatar-option:hover:not(.selected) {
  transform: scale(1.05);
}

.summary-container {
  max-width: 700px;
}

.summary-content {
  display: flex;
  margin: 30px 0;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 20px;
}

.summary-avatar {
  flex: 0 0 200px;
  margin-right: 25px;
}

.selected-avatar-image {
  width: 100%;
  height: auto;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.summary-details {
  flex: 1;
  text-align: left;
}

.summary-item {
  margin-bottom: 15px;
  font-size: 1.1rem;
  display: flex;
}

.summary-label {
  font-weight: bold;
  min-width: 150px;
  color: #a0c4ff;
}

.summary-value {
  color: white;
}

.create-account-button {
  background-color: #4caf50;
  color: white;
  padding: 14px 28px;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: bold;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.create-account-button:hover:not(:disabled) {
  background-color: #388e3c;
}

.create-account-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.flamou-container {
  display: flex;
  align-items: center;
  margin: 20px 0;
  justify-content: center;
}

.flamou-image {
  width: 200px;
  height: auto;
  margin-right: 15px;
}

.flamou-speech-bubble {
  position: relative;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 15px;
  padding: 15px;
  max-width: 70%;
  margin-left: 20px;
}

.flamou-speech-bubble:before {
  content: '';
  position: absolute;
  left: -20px;
  top: 50%;
  transform: translateY(-50%);
  border-width: 10px;
  border-style: solid;
  border-color: transparent rgba(255, 255, 255, 0.2) transparent transparent;
}

.flamou-speech-bubble p {
  margin: 0;
  font-size: 1.3rem;
  font-family: 'GlacialIndifference', sans-serif;
  color: white;
}

.animated-bounce {
  animation: bounce 1.5s infinite alternate;
}

@keyframes bounce {
  0% {
    transform: translateY(0);
  }
  100% {
    transform: translateY(-10px);
  }
}
</style>
