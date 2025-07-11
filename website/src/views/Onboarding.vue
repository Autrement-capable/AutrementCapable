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
            :src="flamouImages.hey"
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
            <div class="gender-image neutral-image">😌</div>
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
            :src="flamouImages.thinking2"
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
              Choisis toutes les activités que tu aimes. Tu peux en sélectionner
              plusieurs !
            </p>
            <div
              v-if="responses.avatarPassions.length > 0"
              class="selected-passions-indicator"
            >
              {{ responses.avatarPassions.length }} passion{{
                responses.avatarPassions.length > 1 ? 's' : ''
              }}
              sélectionnée{{ responses.avatarPassions.length > 1 ? 's' : '' }}
            </div>
          </div>
        </div>
        <div class="passions-container">
          <div
            v-for="passion in currentPassions"
            :key="passion.id"
            class="passion-option"
            :class="{
              selected: responses.avatarPassions.includes(passion.name),
            }"
            @click="togglePassion(passion.name)"
          >
            <div class="passion-image">{{ passion.emoji }}</div>
            <p>{{ passion.name }}</p>
          </div>
        </div>

        <!-- Pagination controls -->
        <div class="passion-pagination">
          <button
            class="pagination-button"
            @click="previousPassionPage"
            :disabled="!canGoToPreviousPassionPage"
          >
            ← Précédent
          </button>

          <div class="pagination-info">
            Page {{ currentPassionPage + 1 }} sur {{ totalPassionPages }}
          </div>

          <button
            class="pagination-button"
            @click="nextPassionPage"
            :disabled="!canGoToNextPassionPage"
          >
            Suivant →
          </button>
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

      <!-- Flamou Popup for Account Explanation -->
      <div
        v-if="showAccountExplanationPopup"
        class="flamou-popup-overlay"
        @click="closeAccountExplanationPopup"
      >
        <div class="flamou-popup-container" @click.stop>
          <div class="flamou-popup-content">
            <div class="flamou-popup-header">
              <img
                :src="flamouImages.interesting"
                alt="Flamou explique"
                class="flamou-popup-image"
              />
              <button
                class="popup-close-button"
                @click="closeAccountExplanationPopup"
              >
                ×
              </button>
            </div>

            <div class="flamou-popup-body">
              <div class="flamou-popup-speech-bubble">
                <!-- <h3>Pourquoi créer un compte sans mot de passe ?</h3>
                <p>
                  Salut ! Je vais t'expliquer pourquoi nous créons ton compte d'une façon spéciale :
                </p>
                <ul>
                  <li>🔒 <strong>Plus sûr</strong> : Pas de mot de passe à retenir ou à perdre</li>
                  <li>⚡ <strong>Plus rapide</strong> : Tu te connectes avec ton empreinte ou ton visage ou ton code d'ordinateur</li>
                  <li>🎯 <strong>Plus simple</strong> : Pas besoin de créer un mot de passe compliqué</li>
                </ul>
                 -->
                <h3>Que va-t-il se passer maintenant ?</h3>
                <div class="steps-explanation">
                  <div class="step-item">
                    <span class="step-number">1</span>
                    <p>Je vais créer ton compte automatiquement</p>
                  </div>
                  <div class="step-item">
                    <span class="step-number">2</span>
                    <p>Nous allons générer tes avatars personnalisés</p>
                  </div>
                  <div class="step-item">
                    <span class="step-number">3</span>
                    <p>Tu pourras choisir ton avatar préféré</p>
                  </div>
                  <div class="step-item">
                    <span class="step-number">4</span>
                    <p>Et hop ! Tu seras prêt(e) à utiliser l'application</p>
                  </div>
                </div>
              </div>

              <div class="popup-buttons">
                <button
                  class="popup-button secondary"
                  @click="closeAccountExplanationPopup"
                >
                  J'ai compris !
                </button>
                <button
                  class="popup-button primary"
                  @click="proceedWithAccountCreation"
                >
                  C'est parti ! 🚀
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 9: Account Creation -->
      <div v-if="currentStep === 9" class="step-container">
        <h1 class="step-title">Création de ton compte</h1>
        <div class="flamou-container">
          <img
            :src="flamouImages.interesting"
            alt="Flamou intéressé"
            class="flamou-image animated-bounce"
          />
          <div class="flamou-speech-bubble">
            <p>
              Parfait ! Maintenant, créons ton compte pour sauvegarder tes
              informations...
            </p>
          </div>
        </div>
        <div class="loading-container">
          <div class="loading-spinner"></div>
          <p class="loading-text">Création de ton compte...</p>
        </div>
      </div>

      <!-- Step 10: Generating Avatars -->
      <div v-if="currentStep === 10" class="step-container">
        <h1 class="step-title">Génération de tes avatars</h1>
        <div class="flamou-container">
          <img
            :src="flamouImages.happy2"
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
          <div v-if="generationProgress > 0" class="generation-progress">
            <div class="progress-bar-container">
              <div
                class="progress-bar-fill"
                :style="{ width: generationProgress + '%' }"
              ></div>
            </div>
            <p class="progress-text">{{ Math.round(generationProgress) }}%</p>
          </div>
        </div>

        <!-- Show error if generation fails -->
        <div v-if="generationError" class="error-container">
          <p class="error-message">{{ generationError }}</p>
          <button class="retry-button" @click="retryAvatarGeneration">
            Réessayer
          </button>
        </div>
      </div>

      <!-- Step 11: Avatar Selection -->
      <div v-if="currentStep === 11" class="step-container">
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
            :key="avatar.id"
            class="avatar-option"
            :class="{ selected: selectedAvatarIndex === index }"
            @click="selectedAvatarIndex = index"
          >
            <img
              :src="avatar.data_url"
              :alt="`Avatar option ${index + 1}`"
              class="avatar-image"
            />
            <div class="avatar-label">Option {{ index + 1 }}</div>
          </div>
        </div>
        <div class="navigation-buttons">
          <button class="back-button" @click="retryAvatarGeneration">
            Générer d'autres avatars
          </button>
          <button
            class="next-button"
            @click="nextStep"
            :disabled="selectedAvatarIndex === null"
          >
            Continuer
          </button>
        </div>
      </div>

      <!-- Step 12: Récapitulatif et finalisation -->
      <div v-if="currentStep === 12" class="step-container summary-container">
        <h1 class="step-title">Récapitulatif</h1>
        <div class="flamou-container">
          <img
            :src="flamouImages.hey"
            alt="Flamou heureux"
            class="flamou-image"
          />
          <div class="flamou-speech-bubble">
            <p>
              Super ! Vérifie si tout est correct avant de finaliser ton profil.
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
                responses.avatarPassions && responses.avatarPassions.length > 0
              "
            >
              <span class="summary-label">Passions:</span>
              <span class="summary-value">
                {{ responses.avatarPassions.join(', ') }}
              </span>
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
            class="finalize-button"
            @click="finalizeProfile"
            :disabled="isFinalizingProfile"
          >
            {{
              isFinalizingProfile
                ? 'Finalisation en cours...'
                : 'Finaliser mon profil'
            }}
          </button>
        </div>

        <div v-if="finalizationError" class="error-message">
          {{ finalizationError }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SpaceBackground from '@/components/SpaceBackground.vue'
import AuthService from '@/services/AuthService'
import { usePicture } from '@/services/PictureService'

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
      generationProgress: 0,
      selectedAvatarIndex: null,
      generatedAvatars: [],
      generationError: null,
      isFinalizingProfile: false,
      finalizationError: null,
      showAccountExplanationPopup: false,

      flamouImages: {
        happy: require('@/assets/flamou/happy.png'),
        happy2: require('@/assets/flamou/happy2.png'),
        normal: require('@/assets/flamou/normal.png'),
        interesting: require('@/assets/flamou/intresting.png'),
        blazed: require('@/assets/flamou/blazed.png'),
        hey: require('@/assets/flamou/hey.png'),
        thinking1: require('@/assets/flamou/thinking1.png'),
        thinking2: require('@/assets/flamou/thinking2.png'),
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
        { id: 'sports', name: 'sport', emoji: '⚽' },
        { id: 'reading', name: 'lecture', emoji: '📚' },
        { id: 'cooking', name: 'cuisine', emoji: '🍳' },
        { id: 'technology', name: 'technologie', emoji: '💻' },
        { id: 'dance', name: 'danse', emoji: '💃' },
        { id: 'photography', name: 'photographie', emoji: '📸' },
        { id: 'science', name: 'sciences', emoji: '🔬' },
        { id: 'travel', name: 'voyages', emoji: '✈️' },
        { id: 'nature', name: 'nature', emoji: '🌿' },
        { id: 'movies', name: 'films et séries', emoji: '🎬' },
        { id: 'fashion', name: 'mode', emoji: '👗' },
        { id: 'gardening', name: 'jardinage', emoji: '🌱' },
        { id: 'crafts', name: 'bricolage', emoji: '🔨' },
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
        avatarPassions: [],
        avatarExpression: null,
      },
      totalSteps: 12, // Updated total steps

      // Pagination for passions
      currentPassionPage: 0,
      passionsPerPage: 9,
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
        return this.generatedAvatars[this.selectedAvatarIndex].data_url
      }
      return null
    },

    // Pagination for passions
    currentPassions() {
      const start = this.currentPassionPage * this.passionsPerPage
      const end = start + this.passionsPerPage
      return this.availablePassions.slice(start, end)
    },

    totalPassionPages() {
      return Math.ceil(this.availablePassions.length / this.passionsPerPage)
    },

    canGoToPreviousPassionPage() {
      return this.currentPassionPage > 0
    },

    canGoToNextPassionPage() {
      return this.currentPassionPage < this.totalPassionPages - 1
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

      // Reset passion pagination when entering passion step
      if (this.currentStep === 7) {
        this.currentPassionPage = 0
      }

      // WTF vlad what black magic control flow is this took me 2 hours to figure out

      // Handle different steps
      if (this.currentStep === 9) {
        // Show explanation popup before account creation
        this.showAccountExplanationPopup = true
      } else if (this.currentStep === 10) {
        // Then generate avatars
        this.generateAvatars()
      }
    },
    previousStep() {
      if (this.currentStep > 1) {
        this.currentStep--

        // Reset passion pagination when entering passion step
        if (this.currentStep === 7) {
          this.currentPassionPage = 0
        }
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
      this.responses.avatarPassions = []
      this.nextStep()
    },
    skipExpressionStep() {
      this.responses.avatarExpression = null
      this.nextStep()
    },

    // Pagination methods for passions
    previousPassionPage() {
      if (this.canGoToPreviousPassionPage) {
        this.currentPassionPage--
      }
    },

    nextPassionPage() {
      if (this.canGoToNextPassionPage) {
        this.currentPassionPage++
      }
    },

    goToPassionPage(pageIndex) {
      if (pageIndex >= 0 && pageIndex < this.totalPassionPages) {
        this.currentPassionPage = pageIndex
      }
    },

    togglePassion(passionName) {
      const index = this.responses.avatarPassions.indexOf(passionName)
      if (index === -1) {
        // Add passion if not already selected
        this.responses.avatarPassions.push(passionName)
      } else {
        // Remove passion if already selected
        this.responses.avatarPassions.splice(index, 1)
      }
    },

    async createAccount() {
      try {
        // Prepare user data for registration
        const userData = {
          first_name: this.responses.nickname,
          last_name: '', // Optional
          age: parseInt(this.responses.age),
        }

        console.log('Creating account with data:', userData)

        // Register with passkey with dummy passkey we will give the info later
        const result = await AuthService.registerWithPasskey()
        console.log('Account creation successful:', result)

        // Possible options ofr the profile update endpoint
        //    first_name: Optional[str]
        //    last_name: Optional[str]
        //    email: Optional[str]
        //    age: Optional[int]
        //    phone_number: Optional[str]
        //    address: Optional[str]
        //    onboarding_complete: Optional[bool]

        // Update user profile with additional data
        const profileData = {
          first_name: this.responses.nickname,
          age: parseInt(this.responses.age),
          onboarding_complete: true, // Mark onboarding as complete
        }
        console.log('Updating profile with data:', profileData)
        // we dont await this call because we dont need its result
        AuthService.request('put', '/user/profile', profileData)
          .then((response) => {
            console.log('Profile updated successfully:', response.data)
          })
          .catch((error) => {
            console.error('Error updating profile:', error)
            // Non-critical error, continue with flow
          })
        // Save avatar creation data
        const avatarData = {
          avatarGender: this.responses.avatarGender,
          avatarAccessories: this.responses.avatarAccessories,
          avatarColor: this.responses.avatarColor,
          avatarPassions: this.responses.avatarPassions,
          avatarExpression: this.responses.avatarExpression,
        }
        // no need to await this call because we dont need its result either
        AuthService.request(
          'post',
          '/user/profile/avatar-creation-data',
          avatarData,
        )
          .then((response) => {
            console.log(
              'Avatar creation data saved successfully:',
              response.data,
            )
          })
          .catch((error) => {
            console.error('Error saving avatar creation data:', error)
            // Non-critical error, continue with flow
          })

        // Move to avatar generation
        this.nextStep()
      } catch (error) {
        console.error('Account creation error:', error)
        alert('Erreur lors de la création du compte. Veuillez réessayer.')
        this.currentStep = 8 // Go back to last step before account creation
      }
    },

    async generateAvatars() {
      this.generatedAvatars = []
      this.generationProgress = 0
      this.generationError = null
      this.loadingText = 'Création de tes avatars...'

      try {
        // Prepare avatar generation request
        const avatarRequest = {
          gender: this.responses.avatarGender || 'neutral',
          accessories: this.responses.avatarAccessories,
          color: this.responses.avatarColor,
          passions: this.responses.avatarPassions,
          expression: this.responses.avatarExpression,
        }

        console.log('Generating avatars with data:', avatarRequest)

        // Simulate progress updates
        const progressInterval = setInterval(() => {
          if (this.generationProgress < 90) {
            this.generationProgress += Math.random() * 10
          }
        }, 1000)

        // Call backend endpoint for avatar generation
        const response = await AuthService.request(
          'post',
          '/avatars/generate',
          avatarRequest,
        )

        clearInterval(progressInterval)
        this.generationProgress = 100

        console.log('Avatar generation response:', response.data)

        if (response.data.avatars && response.data.avatars.length > 0) {
          this.generatedAvatars = response.data.avatars

          // Add a small delay to show completion
          setTimeout(() => {
            this.currentStep = 11 // Move to avatar selection
          }, 1000)
        } else {
          throw new Error('No avatars received from server')
        }
      } catch (error) {
        console.error('Avatar generation error:', error)
        this.generationError =
          error.response?.data?.detail ||
          error.message ||
          'Erreur lors de la génération des avatars'

        // Show fallback avatars or retry option
        this.loadingText = 'Une erreur est survenue...'
      }
    },

    async retryAvatarGeneration() {
      this.currentStep = 10 // Go back to generation step
      await this.generateAvatars()
    },

    async finalizeProfile() {
      if (this.isFinalizingProfile) return

      this.isFinalizingProfile = true
      this.finalizationError = null

      try {
        if (this.selectedAvatarIndex === null) {
          throw new Error('Aucun avatar sélectionné')
        }

        const selectedAvatar = this.generatedAvatars[this.selectedAvatarIndex]
        console.log('Selected avatar:', selectedAvatar)

        // Convert data URL to blob for upload
        const response = await fetch(selectedAvatar.data_url)
        const blob = await response.blob()

        // Create a proper File object with correct mime type
        const avatarFile = new File([blob], 'avatar.png', {
          type: 'image/png',
          lastModified: Date.now(),
        })

        // Upload avatar using PictureService
        const { uploadPicture } = usePicture()

        try {
          const uploadResult = await uploadPicture(avatarFile, 'avatar')
          console.log('Avatar uploaded successfully:', uploadResult)

          // Store the upload result for future reference
          localStorage.setItem(
            'avatar_upload_result',
            JSON.stringify(uploadResult),
          )
        } catch (uploadError) {
          console.error('Error uploading avatar:', uploadError)
          // Non-critical error, but inform user
          this.finalizationError =
            'Avatar sauvegardé localement mais problème lors du téléchargement sur le serveur'
        }

        // Save user profile data in localStorage for potential future use
        localStorage.setItem(
          'user_profile',
          JSON.stringify({
            name: this.responses.nickname,
            age: this.responses.age,
            theme: this.selectedTheme,
            avatar: selectedAvatar.data_url,
            avatarGender: this.responses.avatarGender,
            avatarAccessories: this.responses.avatarAccessories,
            avatarColor: this.responses.avatarColor,
            avatarPassions: this.responses.avatarPassions,
            avatarExpression: this.responses.avatarExpression,
          }),
        )

        // Redirect to dashboard
        this.$router.push('/dashboard')
      } catch (error) {
        console.error('Profile finalization error:', error)
        this.finalizationError =
          error.message ||
          'Erreur lors de la finalisation du profil. Veuillez réessayer.'
      } finally {
        this.isFinalizingProfile = false
      }
    },

    getThemeName(themeId) {
      const theme = this.availableThemes.find((t) => t.id === themeId)
      return theme ? theme.name : ''
    },

    getGenderLabel(gender) {
      if (gender === 'boy') return 'Garçon'
      if (gender === 'girl') return 'Fille'
      return 'Neutre'
    },

    closeAccountExplanationPopup() {
      this.showAccountExplanationPopup = false
      this.createAccount()
    },

    proceedWithAccountCreation() {
      this.showAccountExplanationPopup = false
      this.createAccount()
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
.skip-button,
.retry-button,
.finalize-button {
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

.retry-button {
  background-color: #ff9800;
  color: white;
}

.finalize-button {
  background-color: #4caf50;
  color: white;
}

.back-button:hover,
.skip-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.next-button:hover:not(:disabled) {
  background-color: #2a75e5;
}

.retry-button:hover {
  background-color: #f57c00;
}

.finalize-button:hover:not(:disabled) {
  background-color: #388e3c;
}

.finalize-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
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
  gap: 15px;
  margin: 20px 0;
}

.passion-option {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid transparent;
  width: 120px;
  min-height: 90px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.passion-option.selected {
  border-color: #4285f4;
  background-color: rgba(66, 133, 244, 0.2);
}

.passion-option:hover:not(.selected) {
  background-color: rgba(255, 255, 255, 0.2);
}

.passion-image {
  font-size: 2.5rem;
  margin-bottom: 5px;
}

.passion-option p {
  margin: 0;
  font-size: 0.85rem;
  text-align: center;
  line-height: 1.2;
}

/* Passion Pagination Styles */
.passion-pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin: 20px 0;
  padding: 15px;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
}

.pagination-button {
  padding: 10px 20px;
  border-radius: 8px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  background-color: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 100px;
}

.pagination-button:hover:not(:disabled) {
  background-color: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.pagination-info {
  color: #ffffff;
  font-size: 0.95rem;
  font-weight: 500;
  padding: 8px 16px;
  background-color: rgba(66, 133, 244, 0.2);
  border-radius: 8px;
  border: 1px solid rgba(66, 133, 244, 0.3);
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

/* Generation Progress Styles */
.generation-progress {
  margin-top: 20px;
  width: 100%;
  max-width: 400px;
}

.progress-bar-container {
  width: 100%;
  height: 8px;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background-color: #4285f4;
  transition: width 0.3s ease;
}

.progress-text {
  text-align: center;
  margin-top: 10px;
  font-size: 1rem;
  color: #ffffff;
}

/* Error Styles */
.error-container {
  margin-top: 30px;
  padding: 20px;
  background-color: rgba(244, 67, 54, 0.1);
  border-radius: 8px;
  border: 1px solid rgba(244, 67, 54, 0.3);
}

.error-message {
  color: #ff6b6b;
  font-size: 1rem;
  margin-bottom: 15px;
}

/* Avatar Selection Styles */
.avatars-container {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin: 30px 0;
  flex-wrap: wrap;
}

.avatar-option {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 3px solid transparent;
  width: 200px;
  position: relative;
}

.avatar-option.selected {
  border-color: #4285f4;
  background-color: rgba(66, 133, 244, 0.2);
}

.avatar-option:hover:not(.selected) {
  transform: scale(1.05);
}

.avatar-image {
  width: 100%;
  height: auto;
  border-radius: 8px;
  display: block;
}

.avatar-label {
  margin-top: 10px;
  font-size: 0.9rem;
  color: #ffffff;
  text-align: center;
}

/* Summary Styles */
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

/* Flamou Character Styles */
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

.selected-passions-indicator {
  margin-top: 10px;
  padding: 8px 12px;
  background-color: rgba(66, 133, 244, 0.3);
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
  color: #a0c4ff;
  text-align: center;
  border: 1px solid rgba(66, 133, 244, 0.4);
}

/* Animations */
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

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Flamou Popup Styles */
.flamou-popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-in-out;
}

.flamou-popup-container {
  background-color: rgba(20, 20, 30, 0.95);
  border-radius: 20px;
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7);
  border: 2px solid rgba(66, 133, 244, 0.3);
  animation: slideIn 0.3s ease-out;
}

.flamou-popup-content {
  padding: 0;
}

.flamou-popup-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 30px 10px 30px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.flamou-popup-image {
  width: 80px;
  height: auto;
  border-radius: 50%;
  box-shadow: 0 5px 15px rgba(66, 133, 244, 0.3);
}

.popup-close-button {
  background: none;
  border: none;
  color: #ffffff;
  font-size: 2rem;
  cursor: pointer;
  padding: 0;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.popup-close-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
  transform: scale(1.1);
}

.flamou-popup-body {
  padding: 20px 30px 30px 30px;
}

.flamou-popup-speech-bubble {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 25px;
  margin-bottom: 25px;
  border: 1px solid rgba(66, 133, 244, 0.2);
}

.flamou-popup-speech-bubble h3 {
  color: #a0c4ff;
  margin: 0 0 15px 0;
  font-size: 1.4rem;
  font-weight: bold;
}

.flamou-popup-speech-bubble h4 {
  color: #ffffff;
  margin: 25px 0 15px 0;
  font-size: 1.2rem;
  font-weight: 600;
}

.flamou-popup-speech-bubble p {
  color: #ffffff;
  margin: 0 0 15px 0;
  font-size: 1.1rem;
  line-height: 1.5;
}

.flamou-popup-speech-bubble ul {
  margin: 15px 0;
  padding-left: 0;
  list-style: none;
}

.flamou-popup-speech-bubble li {
  color: #ffffff;
  margin: 10px 0;
  font-size: 1.05rem;
  line-height: 1.4;
  padding-left: 10px;
}

.steps-explanation {
  margin-top: 20px;
}

.step-item {
  display: flex;
  align-items: center;
  margin: 12px 0;
  padding: 10px;
  background-color: rgba(66, 133, 244, 0.1);
  border-radius: 10px;
  border-left: 4px solid #4285f4;
}

.step-number {
  background-color: #4285f4;
  color: white;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 15px;
  flex-shrink: 0;
}

.step-item p {
  margin: 0;
  color: #ffffff;
  font-size: 1rem;
}

.popup-buttons {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
}

.popup-button {
  padding: 12px 24px;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  min-width: 120px;
}

.popup-button.primary {
  background-color: #4285f4;
  color: white;
}

.popup-button.primary:hover {
  background-color: #2a75e5;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(66, 133, 244, 0.4);
}

.popup-button.secondary {
  background-color: transparent;
  color: #ffffff;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.popup-button.secondary:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.5);
}

@keyframes slideIn {
  from {
    transform: translateY(-50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Custom Scrollbar Styles */
.flamou-popup-container::-webkit-scrollbar {
  width: 8px;
}

.flamou-popup-container::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
}

.flamou-popup-container::-webkit-scrollbar-thumb {
  background: linear-gradient(45deg, #4285f4, #a0c4ff);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.flamou-popup-container::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(45deg, #2a75e5, #8ab4f8);
  box-shadow: 0 0 10px rgba(66, 133, 244, 0.5);
}

/* Firefox scrollbar */
.flamou-popup-container {
  scrollbar-width: thin;
  scrollbar-color: #4285f4 rgba(255, 255, 255, 0.1);
}

/* Responsive Design */
@media (max-width: 768px) {
  .flamou-container {
    flex-direction: column;
    text-align: center;
  }

  .flamou-image {
    margin-right: 0;
    margin-bottom: 15px;
  }

  .flamou-speech-bubble {
    margin-left: 0;
    max-width: 90%;
  }

  .flamou-speech-bubble:before {
    display: none;
  }

  .avatars-container {
    flex-direction: column;
    align-items: center;
  }

  .avatar-option {
    width: 250px;
  }

  .summary-content {
    flex-direction: column;
  }

  .summary-avatar {
    margin-right: 0;
    margin-bottom: 20px;
    text-align: center;
  }

  /* Responsive pagination */
  .passion-pagination {
    flex-direction: column;
    gap: 10px;
    padding: 10px;
  }

  .pagination-button {
    width: 100%;
    max-width: 200px;
    margin: 0 auto;
  }

  .pagination-info {
    text-align: center;
    order: -1;
  }

  /* Responsive popup styles */
  .flamou-popup-container {
    width: 95%;
    max-width: none;
    margin: 10px;
  }

  .flamou-popup-header {
    padding: 15px 20px 10px 20px;
  }

  .flamou-popup-body {
    padding: 15px 20px 20px 20px;
  }

  .flamou-popup-speech-bubble {
    padding: 15px;
  }

  .flamou-popup-speech-bubble h3 {
    font-size: 1.2rem;
  }

  .flamou-popup-speech-bubble h4 {
    font-size: 1.1rem;
  }

  .flamou-popup-speech-bubble p,
  .flamou-popup-speech-bubble li {
    font-size: 1rem;
  }

  .step-item {
    flex-direction: column;
    text-align: center;
    padding: 15px;
  }

  .step-number {
    margin-right: 0;
    margin-bottom: 10px;
  }

  .popup-buttons {
    flex-direction: column;
    gap: 10px;
  }

  .popup-button {
    width: 100%;
  }
}
</style>
