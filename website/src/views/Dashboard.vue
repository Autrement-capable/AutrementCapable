<template>
  <div class="dashboard" :class="{ 'achievements-unlocked': hasNewAchievement }">
    
    <!-- Animation de badge débloqué -->
    <div v-if="showBadgeUnlockAnimation" class="badge-unlock-overlay">
      <div class="badge-unlock-animation" :class="{ 'special-celebration': newlyUnlockedBadge && newlyUnlockedBadge.id === 9 }">
        <div class="badge-icon" v-if="newlyUnlockedBadge">{{ newlyUnlockedBadge.icon }}</div>
        <h2 v-if="newlyUnlockedBadge && newlyUnlockedBadge.id === 9">🎉 Félicitations ! 🎉</h2>
        <h2 v-else>Badge débloqué !</h2>
        <h3 v-if="newlyUnlockedBadge">{{ newlyUnlockedBadge.title }}</h3>
        <p v-if="newlyUnlockedBadge && newlyUnlockedBadge.id === 9">
          Bravo ! Tu as terminé tous les jeux disponibles ! Tu es maintenant prêt à créer ton CV professionnel. 🌟
        </p>
        <p v-else-if="newlyUnlockedBadge">{{ newlyUnlockedBadge.description }}</p>
        <button @click="closeBadgeAnimation" class="close-animation-btn" :class="{ 'celebration-btn': newlyUnlockedBadge && newlyUnlockedBadge.id === 9 }">
          Continuer
        </button>
      </div>
    </div>
    <!-- Guide Avatar pour guider l'utilisateur -->
    <guide-avatar
      v-if="!showRewardsModal"
      guide-name="Flamou"
      :forced-message="guideMessage"
      :forced-options="guideOptions"
      :force-show-message="guideForceShow"
      :context="guideContext"
      :auto-show-delay="0"
      :custom-position="guidePosition"
      class="guide-top-left"
      @option-selected="handleGuideOptionSelected"
      @guide-opened="prepareGuideForRediscovery"
      @guide-dismissed="resetGuideState"
      @restart-dashboard-tour="restartDashboardTour"
    />

    <space-background v-if="animationsEnabled" :theme="currentTheme" />
    <static-backgrounds v-else :theme="currentTheme" />
    <!-- La structure principale -->
    <div class="dashboard-container">
      <!-- Avatar central avec cercle de progression amélioré -->
      <div
        class="avatar-container"
        @click="interactWithAvatar"
        :class="{ 'avatar-pulse': avatarAnimating }"
      >
        <div
          v-if="highlightAvatar && isFirstVisit && !profileTourCompleted"
          class="avatar-highlight-effect"
          @click="interactWithAvatar"
        >
          <div class="pulse-ring"></div>
          <div class="hint-arrow">
            <span class="arrow">↓</span>
            <span class="hint-text">Clique ici!</span>
          </div>
        </div>
        <div class="progress-ring-container">
          <svg class="progress-ring" width="300" height="260">
            <!-- Background glow effect -->
            <filter id="glow">
              <feGaussianBlur stdDeviation="3.5" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>

            <!-- Background blur circle -->
            <circle
              class="progress-ring-blur"
              fill="transparent"
              stroke-width="15"
              r="120"
              cx="130"
              cy="130"
              stroke="url(#blurGradient)"
              filter="url(#glow)"
            />

            <!-- Background circle -->
            <circle
              class="progress-ring-circle-bg"
              stroke="#2a2a3a"
              fill="transparent"
              stroke-width="12"
              r="120"
              cx="130"
              cy="130"
            />

            <!-- Progress circle - Now with animation! -->
            <circle
              class="progress-ring-circle"
              stroke="url(#progressGradient)"
              stroke-linecap="round"
              fill="transparent"
              stroke-width="12"
              r="120"
              cx="130"
              cy="130"
              :style="{ strokeDashoffset: calculateProgressOffset() }"
            />

            <defs>
              <linearGradient
                id="progressGradient"
                x1="0%"
                y1="0%"
                x2="100%"
                y2="0%"
              >
                <stop offset="0%" stop-color="#4FC3F7">
                  <animate
                    attributeName="stop-color"
                    values="#4FC3F7;#7C4DFF;#FF4081;#4FC3F7"
                    dur="8s"
                    repeatCount="indefinite"
                  />
                </stop>
                <stop offset="50%" stop-color="#7C4DFF">
                  <animate
                    attributeName="stop-color"
                    values="#7C4DFF;#FF4081;#4FC3F7;#7C4DFF"
                    dur="8s"
                    repeatCount="indefinite"
                  />
                </stop>
                <stop offset="100%" stop-color="#FF4081">
                  <animate
                    attributeName="stop-color"
                    values="#FF4081;#4FC3F7;#7C4DFF;#FF4081"
                    dur="8s"
                    repeatCount="indefinite"
                  />
                </stop>
              </linearGradient>

              <linearGradient
                id="blurGradient"
                x1="0%"
                y1="0%"
                x2="100%"
                y2="0%"
              >
                <stop offset="0%" stop-color="rgba(79, 195, 247, 0.3)">
                  <animate
                    attributeName="stop-color"
                    values="rgba(79, 195, 247, 0.3);rgba(124, 77, 255, 0.3);rgba(255, 64, 129, 0.3);rgba(79, 195, 247, 0.3)"
                    dur="8s"
                    repeatCount="indefinite"
                  />
                </stop>
                <stop offset="100%" stop-color="rgba(255, 64, 129, 0.3)">
                  <animate
                    attributeName="stop-color"
                    values="rgba(255, 64, 129, 0.3);rgba(79, 195, 247, 0.3);rgba(124, 77, 255, 0.3);rgba(255, 64, 129, 0.3)"
                    dur="8s"
                    repeatCount="indefinite"
                  />
                </stop>
              </linearGradient>
            </defs>
          </svg>
        </div>

        <div class="avatar-image-container">
          <img src="@/assets/pdp.png" alt="Avatar" class="avatar-image" />
          <div class="level-badge">Niveau {{ calculateLevel() }}</div>
          <div class="avatar-glow" :class="{ pulse: avatarAnimating }"></div>
        </div>
      </div>

      <div class="current-level-badge">
        <img
          :src="getCurrentBadgeImage()"
          :alt="`Badge niveau ${calculateLevel()}`"
          class="current-badge-image"
          @click="handleBadgeClick"
        />
      </div>

      <div v-if="badgeNeedsEvolution" class="badge-evolution-text">
        Clique 10 fois sur le badge pour l'évoluer ({{ badgeClickCount }}/10)
      </div>

      <!-- Bouton Commencer à jouer -->
      <div class="play-button-container">
        <button
          class="play-button"
          @mouseenter="handlePlayButtonHover(true)"
          @mouseleave="handlePlayButtonHover(false)"
          @mousedown=";(playButtonPressed = true), $event.stopPropagation()"
          @mouseup=";(playButtonPressed = false), $event.stopPropagation()"
          @click="startPlaying()"
          :class="{ hovered: playButtonHovered, pressed: playButtonPressed }"
        >
          <div class="button-glow"></div>
          <span class="button-text">Commencer à jouer</span>
          <div class="button-border"></div>
        </button>
      </div>

      <!-- Animation de récompense -->
      <div class="achievement-popup" v-if="showAchievement">
        <div class="achievement-icon">🏆</div>
        <div class="achievement-text">
          <h3>Nouvelle réalisation!</h3>
          <p>{{ currentAchievement }}</p>
        </div>
      </div>

      <rewards-component
        v-if="showRewardsModal"
        :current-theme="currentTheme"
        :animations-enabled="animationsEnabled"
        :progress="progress"
        :show-profile-guide="true"
        @close="closeRewardsModal"
        @generate-cv="handleGenerateCV"
        @view-profile="handleViewProfile"
      />

      <!-- Onglet de contrôle du thème -->
      <div class="theme-tab" @click="toggleThemeMenu">
        <div class="theme-tab-icon">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            width="24"
            height="24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <circle cx="12" cy="12" r="5" />
            <line x1="12" y1="1" x2="12" y2="3" />
            <line x1="12" y1="21" x2="12" y2="23" />
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
            <line x1="1" y1="12" x2="3" y2="12" />
            <line x1="21" y1="12" x2="23" y2="12" />
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
          </svg>
        </div>
      </div>

      <!-- Sélecteur de thème modifié avec transition -->
      <div
        class="theme-selector"
        :class="{ 'theme-selector-visible': themeMenuVisible }"
      >
        <div
          class="theme-option"
          v-for="theme in availableThemes"
          :key="theme.value"
          @click="changeTheme(theme.value)"
          :class="{ active: currentTheme === theme.value }"
        >
          <div class="theme-icon" :class="theme.value"></div>
          <span>{{ theme.label }}</span>
        </div>

        <div
          class="theme-option animation-toggle"
          @click="toggleAnimations"
          :class="{ active: animationsEnabled }"
        >
          <div class="theme-icon animation-icon"></div>
          <span>
            {{ animationsEnabled ? 'Animations ON' : 'Animations OFF' }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SpaceBackground from '@/components/SpaceBackground.vue'
import StaticBackgrounds from '@/components/StaticBackgrounds.vue'
import RewardsComponent from '@/components/RewardsComponent.vue'
import GuideAvatar from '@/components/GuideComponent.vue'
import UserJourneyService from '@/services/UserJourneyService.js'
import { eventBus } from '@/utils/eventBus'

export default {
  name: 'UserDashboard',
  components: {
    SpaceBackground,
    StaticBackgrounds,
    RewardsComponent,
    GuideAvatar,
  },
  data() {
    return {
      themeMenuVisible: false,
      currentTheme: 'cosmic',
      availableThemes: [
        { value: 'cosmic', label: 'Cosmic' },
        { value: 'ocean', label: 'Ocean' },
        { value: 'cyberpunk', label: 'Cyberpunk' },
        { value: 'forest', label: 'Forêt' },
        { value: 'snow', label: 'Neige' },
      ],
      progress: 0,
      activeSection: null,
      avatarAnimating: false,
      showAvatarInteraction: false,
      activeModal: null,
      showAchievement: false,
      hasNewAchievement: false,
      showRewardsModal: false,
      currentAchievement: '',
      animationsEnabled: true,
      playButtonHovered: false,
      playButtonPressed: false,
      profileTourCompleted: false,
      achievements: [
        'Explorateur Curieux',
        'Premier Pas',
        'Maître du Temps',
        'Briseur de Barrières',
        'Esprit Créatif',
      ],
      guideContext: 'dashboard',
      guideMessage:
        "Salut ! Je suis Flamou, ton guide. Bienvenue sur ton tableau de bord personnel ! C'est ici que tu pourras suivre ta progression, accéder à ton profil et commencer les jeux.",
      guideOptions: [
        { text: 'Comment utiliser le dashboard ?', action: 'explainDashboard' },
      ],
      guideForceShow: true,
      highlightAvatar: false,
      isFirstVisit: false,
      guidePosition: {
        position: 'fixed',
        top: '20px',
        left: '20px',
        zIndex: 2000,
      },
      guideTourStep: 0,
      highlightedElement: null,
      showGuideArrow: false,
      levelBadges: [
        {
          level: 1,
          name: 'Apprenti',
          description: 'Tu as fait tes premiers pas dans ton parcours !',
          image: () => require('@/assets/badges/badge1.png'),
        },
        {
          level: 2,
          name: 'Explorateur',
          description:
            'Tu commences à explorer les différentes activités disponibles.',
          image: () => require('@/assets/badges/badge2.png'),
        },
        {
          level: 3,
          name: 'Aventurier',
          description:
            "Tu progresses rapidement dans ton parcours d'apprentissage !",
          image: () => require('@/assets/badges/badge3.png'),
        },
        {
          level: 4,
          name: 'Champion',
          description:
            'Tu as atteint un niveau impressionnant, continue ainsi !',
          image: () => require('@/assets/badges/badge4.png'),
        },
        {
          level: 5,
          name: 'Maître',
          description: 'Tu es devenu un véritable maître dans ton parcours !',
          image: () => require('@/assets/badges/badge5.png'),
        },
        {
          level: 6,
          name: 'Légende',
          description: 'Tu es maintenant une légende !',
          image: () => require('@/assets/badges/badge6.png'),
        },
      ],
      activeBadgeTooltip: null,
      tooltipStyle: {
        top: '0px',
        left: '0px',
      },
      badgeClickCount: 0,
      badgeNeedsEvolution: false,
      lastEvolvedLevel: 0,
      showBadgeUnlockAnimation: false,
      newlyUnlockedBadge: null,
      userBadges: [],
    }
  },
  created() {
    // Écouter les événements via eventBus
    // eventBus.on('hide-dashboard-guide', () => {
    //   this.guideForceShow = false;
    // });
  },
  beforeUnmount() {
    eventBus.off('hide-dashboard-guide')
    window.removeEventListener('resize', this.updateGuidePosition)
    this.removeAllHighlights()
  },
  watch: {
    isFirstVisit(newVal) {
      if (newVal && !this.showRewardsModal) {
        this.guideForceShow = true
        this.$nextTick(() => {
          this.updateGuidePosition()
        })
      }
    },

    showRewardsModal(newVal) {
      if (!newVal && this.isFirstVisit) {
        this.guideForceShow = true
        this.$nextTick(() => {
          this.updateGuidePosition()
        })
      }
    },
  },
  methods: {
    /**
     * Vérifie si tous les jeux sont terminés pour débloquer le badge "Tous les jeux finis"
     */
    async checkAllGamesCompleted() {
      try {
        // Charger les badges depuis localStorage
        const savedBadges = localStorage.getItem('userBadges');
        if (!savedBadges) return;

        this.userBadges = JSON.parse(savedBadges);
        
        // IDs des badges de jeux (excluant le profil, CV et formation)
        const gameIds = [1, 2, 3, 4, 5, 7];
        
        // Vérifier si tous les jeux sont terminés
        const allGamesCompleted = gameIds.every(id => {
          const badge = this.userBadges.find(badge => badge.id === id);
          return badge && badge.unlocked;
        });

        // Trouver le badge "Tous les jeux finis"
        const allGamesCompletedBadge = this.userBadges.find(badge => badge.id === 9);
        
        if (allGamesCompleted && allGamesCompletedBadge && !allGamesCompletedBadge.unlocked) {
          // Débloquer le badge
          allGamesCompletedBadge.unlocked = true;
          allGamesCompletedBadge.dateUnlocked = new Date().toISOString().split('T')[0];
          
          // Sauvegarder dans localStorage
          localStorage.setItem('userBadges', JSON.stringify(this.userBadges));
          
          // Déclencher l'animation après un petit délai
          setTimeout(() => {
            this.newlyUnlockedBadge = allGamesCompletedBadge;
            this.showBadgeUnlockAnimation = true;
          }, 1000);

          // Mettre à jour la progression
          this.updateProgress();
        }
      } catch (error) {
        console.error('Erreur lors de la vérification des badges:', error);
      }
    },

    /**
     * Met à jour la progression basée sur les badges débloqués
     */
    updateProgress() {
      if (this.userBadges && this.userBadges.length > 0) {
        const unlockedCount = this.userBadges.filter(badge => badge.unlocked).length;
        const totalCount = this.userBadges.length;
        this.progress = Math.round((unlockedCount / totalCount) * 100);
      }
    },

    /**
     * Ferme l'animation de badge
     */
    closeBadgeAnimation() {
      this.showBadgeUnlockAnimation = false;
      this.newlyUnlockedBadge = null;
    },

    getCurrentBadgeImage() {
      // Obtenir le niveau actuel
      const currentLevel = this.calculateLevel()

      // Vérifier si le badge doit évoluer (seulement à partir du niveau 2)
      if (
        currentLevel > this.lastEvolvedLevel &&
        !this.badgeNeedsEvolution &&
        currentLevel > 1
      ) {
        this.badgeNeedsEvolution = true
        this.badgeClickCount = 0
      }

      // Trouver le badge le plus élevé débloqué
      const highestUnlockedBadge = this.levelBadges
        .filter(
          (badge) =>
            badge.level <=
            (this.badgeNeedsEvolution ? this.lastEvolvedLevel : currentLevel),
        )
        .sort((a, b) => b.level - a.level)[0]

      if (highestUnlockedBadge) {
        return highestUnlockedBadge.image(true)
      }

      // Badge par défaut si aucun badge n'est débloqué
      return this.levelBadges[0].image(false)
    },

    handleBadgeClick() {
      if (this.badgeNeedsEvolution) {
        this.badgeClickCount++

        // Animer le badge lors du clic
        const badgeElement = document.querySelector('.current-badge-image')
        if (badgeElement) {
          badgeElement.classList.add('badge-click-animation')
          setTimeout(() => {
            badgeElement.classList.remove('badge-click-animation')
          }, 300)
        }

        // Si 10 clics atteints, faire évoluer le badge
        if (this.badgeClickCount >= 10) {
          this.evolveBadge()
        }
      }
    },

    evolveBadge() {
      // Mettre à jour le dernier niveau évolué
      this.lastEvolvedLevel = this.calculateLevel()
      this.badgeNeedsEvolution = false

      // Animation spéciale pour l'évolution
      const badgeElement = document.querySelector('.current-badge-image')
      if (badgeElement) {
        badgeElement.classList.add('badge-evolve-animation')
        setTimeout(() => {
          badgeElement.classList.remove('badge-evolve-animation')
        }, 1000)
      }
    },

    // Méthode pour fermer le guide
    dismissGuide() {
      this.guideForceShow = false

      // Réinitialiser l'étape du tutoriel à 0
      this.guideTourStep = 0

      // Préparer le guide avec un message pour redécouvrir le dashboard
      this.guideMessage =
        'Salut ! Je suis Flamou, ton guide. Clique sur moi si tu veux redécouvrir le dashboard !'
      this.guideOptions = [
        { text: 'Comment utiliser le dashboard ?', action: 'explainDashboard' },
      ]

      // Gérer les surbrillances comme avant
      const profileTourCompleted =
        localStorage.getItem('profile-tour-completed') === 'true'
      const isInProfileStep = this.guideTourStep === 6

      if (!isInProfileStep || profileTourCompleted) {
        this.highlightAvatar = false
        this.removeAllHighlights()
      }
    },

    prepareGuideForRediscovery() {
      const profileTourCompleted =
        localStorage.getItem('profile-tour-completed') === 'true'

      if (profileTourCompleted) {
        // Message adapté pour proposer de redécouvrir le dashboard
        this.guideMessage =
          'Salut ! Souhaites-tu redécouvrir les fonctionnalités du dashboard ?'
        this.guideOptions = [
          {
            text: 'Oui, montre-moi tout !',
            action: 'restartDashboardTour',
            keepOpen: true,
          },
          { text: 'Non merci', action: 'dismissGuide' },
        ]
        this.guideForceShow = true
      }
    },

    resetGuideState() {
      this.guideTourStep = 0
      this.guideMessage =
        'Salut ! Je suis Flamou, ton guide. Clique sur moi si tu veux redécouvrir le dashboard !'
      this.guideOptions = [
        { text: 'Comment utiliser le dashboard ?', action: 'explainDashboard' },
      ]
      this.guideForceShow = false
      this.removeAllHighlights()
    },

    restartDashboardTour() {
      // Réinitialiser l'étape du tutoriel
      this.guideTourStep = 0

      // Réactiver le guide et commencer le tutoriel
      this.guideForceShow = true
      this.explainDashboard()

      // Mettre à jour la position du guide si nécessaire
      this.$nextTick(() => {
        this.updateGuidePosition()
      })
    },

    advanceTutorial() {
      // Incrémenter l'étape du tutoriel
      this.guideTourStep++

      // Retirer les surlignages précédents
      this.removeAllHighlights()

      // Définir le contenu en fonction de l'étape actuelle
      switch (this.guideTourStep) {
        case 1: // Explications sur l'anneau de progression autour de l'avatar
          this.guideMessage =
            "L'avatar au centre représente ton personnage. L'anneau autour montre ta progression globale, et le niveau affiché augmente au fur et à mesure que tu gagnes des badges !"
          this.guideOptions = [
            { text: 'Suivant', action: 'advanceTutorial', keepOpen: true },
          ]
          this.highlightElement('.progress-ring-container', true)
          break

        case 2: // Explications sur le bouton des thèmes
          this.guideMessage =
            'Ce bouton te permet de changer le thème visuel de ton tableau de bord. Tu peux choisir parmi plusieurs ambiances selon tes préférences mais aussi désactiver les animations.'
          this.guideOptions = [
            { text: 'Suivant', action: 'advanceTutorial', keepOpen: true },
          ]
          this.highlightElement('.theme-tab')
          break

        case 3: // Explications sur le bouton d'accessibilité
          this.guideMessage =
            "Le bouton d'accessibilité te permet d'adapter l'interface à tes besoins spécifiques, comme modifier la taille du texte ou les contrastes de couleurs."
          this.guideOptions = [
            { text: 'Suivant', action: 'advanceTutorial', keepOpen: true },
          ]
          this.highlightElement('.accessibility-widget')
          break

        case 4: // Explications sur le bouton plein écran
          this.guideMessage =
            'Ce bouton te permet de passer en mode plein écran pour une expérience plus immersive, sans distractions.'
          this.guideOptions = [
            { text: 'Suivant', action: 'advanceTutorial', keepOpen: true },
          ]
          this.highlightElement('.fullscreen-button')
          break

        case 5: // Explications sur le bouton "Commencer à jouer"
          this.guideMessage =
            'Le bouton "Commencer à jouer" sera ton point de départ pour accéder aux différentes activités et jeux disponibles.'
          this.guideOptions = [
            { text: 'Suivant', action: 'advanceTutorial', keepOpen: true },
          ]
          this.highlightElement('.play-button')
          break

        case 6: // Invitation à débloquer le premier badge
          this.guideMessage =
            'Maintenant que tu connais les bases, découvre ton profil pour débloquer ton premier badge !'
          this.guideOptions = [
            {
              text: 'Comment accéder à mon profil ?',
              action: 'showProfileHelp',
              keepOpen: true,
            },
          ]
          break

        default:
          this.dismissGuide()
          break
      }
    },

    highlightElement(selector, isSpecial = false) {
      const element = document.querySelector(selector)
      if (element) {
        // Retirer les surlignages précédents
        this.removeAllHighlights()

        // Obtenir les coordonnées de l'élément
        const rect = element.getBoundingClientRect()

        // Créer un élément de surbrillance
        const highlight = document.createElement('div')
        highlight.className = 'guide-highlight'

        // Détecter si l'élément est rond (avatar, boutons ronds)
        const isRound =
          selector.includes('avatar-container') ||
          selector.includes('progress-ring-container') ||
          selector.includes('theme-tab') ||
          selector.includes('theme-icon') ||
          selector.includes('fullscreen-button') ||
          selector.includes('accessibility-widget')

        // Positionner la surbrillance
        highlight.style.position = 'fixed'
        highlight.style.top = `${rect.top - 5}px`
        highlight.style.left = `${rect.left - 5}px`
        highlight.style.width = `${rect.width + 10}px`
        highlight.style.height = `${rect.height + 10}px`
        highlight.style.border = '3px solid #76ff03'

        // Appliquer un rayon de bordure approprié selon la forme de l'élément
        if (isRound) {
          // Pour les éléments ronds comme l'avatar, utiliser 50%
          highlight.style.borderRadius = '50%'
        } else if (selector.includes('play-button')) {
          // Pour le bouton jouer qui a un rayon précis
          highlight.style.borderRadius = '30px'
        } else {
          // Pour les autres éléments, conserver un rayon par défaut
          highlight.style.borderRadius = '12px'
        }

        highlight.style.boxShadow = '0 0 15px rgba(118, 255, 3, 0.7)'
        highlight.style.pointerEvents = 'none'
        highlight.style.zIndex = '1050'

        // Ajouter une animation si c'est l'élément spécial (avatar)
        if (isSpecial) {
          highlight.style.animation = 'highlight-pulse 2s ease-out infinite'

          // Ajouter une flèche si nécessaire
          if (this.showGuideArrow) {
            const arrow = document.createElement('div')
            arrow.className = 'guide-arrow'
            arrow.textContent = '↓'
            arrow.style.position = 'fixed'
            arrow.style.top = `${rect.top - 40}px`
            arrow.style.left = `${rect.left + rect.width / 2}px`
            arrow.style.transform = 'translateX(-50%)'
            arrow.style.color = '#76ff03'
            arrow.style.fontSize = '36px'
            arrow.style.fontWeight = 'bold'
            arrow.style.textShadow = '0 0 10px rgba(118, 255, 3, 0.7)'
            arrow.style.animation = 'bounce 2s ease infinite'
            arrow.style.zIndex = '1051'

            document.body.appendChild(arrow)
          }
        }

        // Ajouter au DOM
        document.body.appendChild(highlight)

        // Stocker l'élément surligné
        this.highlightedElement = selector

        // Ne pas utiliser scrollIntoView pour les éléments déjà visibles
        // ou pour les éléments en bas de l'écran (thème, bouton accessibilité, etc.)
        const isBottomElement =
          selector.includes('theme') ||
          selector.includes('fullscreen') ||
          selector.includes('accessibility') ||
          selector.includes('play-button')

        // Vérifier si l'élément est déjà visible dans la fenêtre
        const isVisible =
          rect.top >= 0 &&
          rect.bottom <= window.innerHeight &&
          rect.left >= 0 &&
          rect.right <= window.innerWidth

        // Faire défiler uniquement si nécessaire et pas pour les éléments du bas
        if (!isBottomElement && !isVisible) {
          // Défilement plus doux avec une marge
          window.scrollTo({
            top: window.scrollY + rect.top - 200, // 200px de marge en haut
            behavior: 'smooth',
          })
        }
      }
    },

    // Méthode pour retirer tous les surlignages
    removeAllHighlights() {
      // Retirer les surlignages
      const highlights = document.querySelectorAll('.guide-highlight')
      highlights.forEach((el) => el.remove())

      // Retirer les flèches
      const arrows = document.querySelectorAll('.guide-arrow')
      arrows.forEach((el) => el.remove())

      // Réinitialiser l'état
      this.highlightedElement = null
      this.showGuideArrow = false
    },

    // Méthode pour expliquer le bouton de jeu
    explainPlayButton() {
      this.guideMessage =
        "Pour commencer à jouer et gagner des badges, clique sur le bouton 'Commencer à jouer' en bas de l'écran."
      this.guideOptions = [
        { text: 'Je comprends !', action: 'dismissGuide', keepOpen: true },
      ]
      // Désactiver la mise en évidence de l'avatar
      this.highlightAvatar = false

      // Scroll automatique vers le bouton de jeu si nécessaire
      this.$nextTick(() => {
        const playButton = document.querySelector('.play-button')
        if (playButton) {
          playButton.scrollIntoView({ behavior: 'smooth', block: 'center' })
        }
      })
    },

    showProfileHelp() {
      this.guideMessage =
        "Pour accéder à ton profil et voir tes badges, clique sur ton avatar au centre de l'écran. C'est là que tu pourras découvrir tes réalisations !"
      this.guideOptions = [
        {
          text: "D'accord, je vais essayer !",
          action: 'dismissGuide',
          keepOpen: true,
        },
      ]
      // Conserver la mise en évidence de l'avatar
      this.highlightAvatar = true
      this.showGuideArrow = true
      this.highlightElement('.avatar-container', true)

      // Scroll automatique vers l'avatar si nécessaire
      this.$nextTick(() => {
        const avatarElement = document.querySelector('.avatar-container')
        if (avatarElement) {
          avatarElement.scrollIntoView({ behavior: 'smooth', block: 'center' })
        }
      })
    },

    finalizeHelp() {
      // Fermer la bulle du guide
      this.guideForceShow = false

      // Conserver la mise en évidence et la flèche pour guider l'utilisateur
      // vers l'avatar (ne pas les supprimer)
      this.highlightAvatar = true
      this.showGuideArrow = true

      // Réappliquer la mise en évidence pour s'assurer qu'elle est visible
      this.$nextTick(() => {
        this.highlightElement('.avatar-container', true)
      })
    },

    forceGuideDisplay() {
      if (this.isFirstVisit && !this.showRewardsModal) {
        this.guideForceShow = true
        this.updateGuidePosition()

        // Émettre un événement via eventBus pour informer le guide qu'il doit s'afficher
        eventBus.emit('force-guide-display')
      }
    },
    updateGuidePosition() {
      // Si le guide est en mode conversation (bulle visible)
      if (this.guideForceShow && this.isFirstVisit) {
        // Attendre que le DOM soit rendu
        this.$nextTick(() => {
          const avatarElement = document.querySelector('.avatar-container')
          if (avatarElement) {
            const rect = avatarElement.getBoundingClientRect()

            // Positionner le guide à droite de l'avatar et centré verticalement
            this.guidePosition = {
              position: 'fixed',
              top: `${rect.top + rect.height / 2 - 30}px`,
              left: `${rect.right + 20}px`,
              zIndex: 2000,
            }
          }
        })
      } else {
        // Position par défaut quand la bulle n'est pas affichée
        this.guidePosition = {
          position: 'fixed',
          top: '20px',
          left: '20px',
          zIndex: 2000,
        }
      }
    },
    // Nouvelle méthode pour expliquer le dashboard
    explainDashboard() {
      // Réinitialiser le compteur d'étapes si l'utilisateur a terminé le tour
      const profileTourCompleted =
        localStorage.getItem('profile-tour-completed') === 'true'

      if (profileTourCompleted) {
        // Réinitialiser les options pour qu'elles soient disponibles après
        this.guideTourStep = 0

        // Définir un message d'introduction plus court pour les utilisateurs expérimentés
        this.guideMessage =
          'Le dashboard est ton espace personnel. Tu peux y voir ton avatar, ta progression, changer le thème et accéder aux jeux.'
        this.guideOptions = [
          {
            text: 'Montrer les fonctionnalités',
            action: 'advanceTutorial',
            keepOpen: true,
          },
          { text: 'Commencer à jouer', action: 'startPlaying', keepOpen: true },
          {
            text: "Merci, j'ai compris !",
            action: 'dismissGuide',
            keepOpen: true,
          },
        ]
      } else {
        // Comportement standard pour les nouveaux utilisateurs
        this.guideTourStep = 0
        this.advanceTutorial()
      }
    },

    // Vérifier si c'est la première visite de l'utilisateur
    checkFirstVisit() {
      const hasVisitedBefore = localStorage.getItem('hasVisitedDashboard')
      this.isFirstVisit = !hasVisitedBefore

      // Vérifier si le tour du profil a été complété
      this.profileTourCompleted =
        localStorage.getItem('profile-tour-completed') === 'true'

      if (!hasVisitedBefore) {
        localStorage.setItem('hasVisitedDashboard', 'true')

        // Mettre à jour l'étape dans le service de parcours utilisateur
        if (typeof UserJourneyService !== 'undefined') {
          UserJourneyService.updateStep(
            UserJourneyService.STEPS.DASHBOARD_INTRO,
          )
        }
      }
    },

    // Méthode pour gérer les options sélectionnées dans le guide
    handleGuideOptionSelected(option) {
      if (option.action === 'finalizeHelp') {
        // Action spéciale pour finaliser l'aide et garder les effets visuels
        this.finalizeHelp()
        return
      }

      // Pour toutes les autres actions
      if (option.action && typeof this[option.action] === 'function') {
        this[option.action]()
      } else {
        console.warn(`L'action "${option.action}" n'est pas définie.`)
      }
    },

    toggleThemeMenu() {
      this.themeMenuVisible = !this.themeMenuVisible

      // Ajout d'une sensation tactile
      if (window.navigator && window.navigator.vibrate) {
        window.navigator.vibrate(50)
      }

      // Stocker la préférence dans localStorage
      localStorage.setItem(
        'theme-menu-visible',
        this.themeMenuVisible.toString(),
      )
    },

    changeTheme(theme) {
      this.currentTheme = theme

      // Optional: store the selected theme in localStorage to persist across sessions
      localStorage.setItem('dashboard-theme', theme)

      // Optional: trigger achievement for first theme change
      if (!this.themeChangeAchieved && theme !== 'cosmic') {
        this.themeChangeAchieved = true
      }
    },

    // Keep all existing methods
    calculateProgressOffset() {
      const circumference = 2 * Math.PI * 120
      return circumference - (circumference * this.progress) / 100
    },

    calculateLevel() {
      return Math.floor(this.progress / 10) + 1
    },

    generateParticleStyle() {
      const duration = 1 + Math.random() * 1.5
      const delay = Math.random() * 0.5
      const size = 3 + Math.random() * 4
      const halfSize = size / 2

      return {
        left: `calc(50% - ${halfSize}px)`,
        top: `calc(50% - ${halfSize}px)`,
        width: `${size}px`,
        height: `${size}px`,
        transform: 'scale(0)',
        opacity: '0',
        animation: `particleExpand ${duration}s ease ${delay}s infinite`,
      }
    },

    // Génère un style aléatoire pour les particules d'arrière-plan
    randomParticleStyle() {
      return {
        left: `${Math.random() * 100}%`,
        top: `${Math.random() * 100}%`,
        animationDelay: `${Math.random() * 5}s`,
        animationDuration: `${5 + Math.random() * 10}s`,
        opacity: Math.random() * 0.5,
        transform: `scale(${0.5 + Math.random() * 1.5})`,
      }
    },

    interactWithAvatar() {
      this.avatarAnimating = true
      this.showRewardsModal = true

      // Animation plus longue pour un meilleur effet
      setTimeout(() => {
        this.avatarAnimating = false
      }, 1000)

      // Mettre à jour l'étape dans le service de parcours utilisateur
      try {
        if (typeof UserJourneyService !== 'undefined') {
          UserJourneyService.updateStep(UserJourneyService.STEPS.PROFILE_INTRO)
        }
      } catch (error) {
        console.error(
          "Erreur lors de la mise à jour de l'étape du parcours:",
          error,
        )
      }

      // Mettre à jour la position du guide si nécessaire
      if (this.isFirstVisit && !this.showRewardsModal) {
        this.updateGuidePosition()
      }

      // Envoyer un événement via eventBus
      eventBus.emit('profile-opened')

      // Masquer le guide du dashboard quand on ouvre la modal du profil
      this.guideForceShow = false
      eventBus.emit('hide-dashboard-guide')

      // Propriété pour suivre si la modal a été ouverte
      localStorage.setItem('hasOpenedProfile', 'true')
    },

    // Nouvelle méthode pour fermer le modal de récompenses
    closeRewardsModal() {
      this.showRewardsModal = false
      if (this.isFirstVisit) {
        this.guideForceShow = true
      }
    },

    handleGenerateCV() {
      // Déclenche un accomplissement et ferme le modal
      this.closeRewardsModal()
    },

    handleViewProfile() {
      this.closeRewardsModal()
    },

    // Voir les réalisations
    viewAchievements() {
      this.showAvatarInteraction = false
      this.activeModal = 'achievements'
    },

    // Déclenche une animation de réalisation
    triggerAchievement(achievement) {
      this.currentAchievement = achievement
      this.showAchievement = true
      this.hasNewAchievement = true

      // Animation de progression
      const oldProgress = this.progress
      const newProgress = Math.min(100, oldProgress + 5)

      // Animation progressive du changement
      const step = 0.5
      const duration = 2000 // 2 secondes
      const steps = (newProgress - oldProgress) / step
      const interval = duration / steps

      const progressAnimation = setInterval(() => {
        if (this.progress < newProgress) {
          this.progress += step
        } else {
          clearInterval(progressAnimation)
        }
      }, interval)

      // Faire disparaître l'animation après 3 secondes
      setTimeout(() => {
        this.showAchievement = false
      }, 3000)

      // Réinitialiser l'effet de fond
      setTimeout(() => {
        this.hasNewAchievement = false
      }, 4000)
    },

    toggleAnimations() {
      this.animationsEnabled = !this.animationsEnabled

      localStorage.setItem(
        'dashboard-animations',
        this.animationsEnabled.toString(),
      )

      if (window.navigator && window.navigator.vibrate) {
        window.navigator.vibrate(50)
      }

      this.$emit('toggle-animations', !this.animationsEnabled)
    },

    handlePlayButtonHover(isHovered) {
      this.playButtonHovered = isHovered
      if (!isHovered) {
        this.playButtonPressed = false
      }
    },

    startPlaying() {
      // Haptic feedback if available
      if (window.navigator && window.navigator.vibrate) {
        window.navigator.vibrate(50)
      }

      // Trigger achievement
      this.triggerAchievement('Premier Pas')

      // Liste des jeux disponibles
      const gameRoutes = [
        //  '/roue-des-competences',
        //  '/scenarios',
        '/environment',
        //  '/metiers',
        //  '/shape-sequence-game',
        //  '/game-speed',
      ]

      // Sélectionner un jeu au hasard
      const randomIndex = Math.floor(Math.random() * gameRoutes.length)
      const selectedGame = gameRoutes[randomIndex]

      // Rediriger vers le jeu sélectionné
      this.$router.push(selectedGame)
    },
  },
  mounted() {
    this.checkAllGamesCompleted();

    // Check if the showBadges query parameter exists
    if (
      this.$route.query.showBadges === 'true' ||
      this.$route.query.showBadges === true
    ) {
      this.showRewardsModal = true
      const newQuery = { ...this.$route.query }
      delete newQuery.showBadges
      this.$router.replace({ query: newQuery })
    }

    const savedTheme = localStorage.getItem('dashboard-theme')
    if (
      savedTheme &&
      this.availableThemes.some((theme) => theme.value === savedTheme)
    ) {
      this.currentTheme = savedTheme
    }

    const savedAnimationPref = localStorage.getItem('dashboard-animations')
    if (savedAnimationPref !== null) {
      this.animationsEnabled = savedAnimationPref === 'true'
    }

    this.themeChangeAchieved = false
    this.profileTourCompleted =
      localStorage.getItem('profile-tour-completed') === 'true'

    // Vérifier si c'est la première visite
    this.checkFirstVisit()

    // Mettre à jour la position du guide
    this.updateGuidePosition()

    // Recalculer la position lors du redimensionnement de la fenêtre
    window.addEventListener('resize', this.updateGuidePosition)

    if (this.isFirstVisit && !this.showRewardsModal) {
      // S'assurer que guideForceShow est bien à true
      this.guideForceShow = true

      // Attendre un peu pour s'assurer que le composant est bien monté
      setTimeout(() => {
        // Déclencher à nouveau la mise à jour du message pour forcer l'affichage
        this.guideMessage = this.guideMessage + ' ' // Ajouter un espace pour forcer le changement
        this.guideForceShow = true
      }, 300)
    }

    // Ajouter ces styles pour les animations du guide
    const style = document.createElement('style')
    style.textContent = `
      @keyframes highlight-pulse {
        0% {
          opacity: 0.7;
          box-shadow: 0 0 15px rgba(118, 255, 3, 0.5);
          transform: scale(0.99);
        }
        50% {
          opacity: 0.9;
          box-shadow: 0 0 20px rgba(118, 255, 3, 0.8);
          transform: scale(1);
        }
        100% {
          opacity: 0.7;
          box-shadow: 0 0 15px rgba(118, 255, 3, 0.5);
          transform: scale(0.99);
        }
      }

      @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
          transform: translateX(-50%) translateY(0);
        }
        40% {
          transform: translateX(-50%) translateY(-15px);
        }
        60% {
          transform: translateX(-50%) translateY(-7px);
        }
      }
    `
    document.head.appendChild(style)
  },
}
</script>

<style scoped>
.dashboard {
  position: relative;
  width: 100%;
  height: 100vh;
  color: white;
  overflow: hidden;
  font-family: 'Nunito', sans-serif;
  transition: all 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  background: transparent;
}

.dashboard-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background:
    radial-gradient(
      circle at 30% 40%,
      rgba(76, 0, 153, 0.2) 0%,
      rgba(76, 0, 153, 0) 50%
    ),
    radial-gradient(
      circle at 70% 60%,
      rgba(63, 0, 113, 0.2) 0%,
      rgba(63, 0, 113, 0) 60%
    ),
    radial-gradient(
      circle at 50% 50%,
      rgba(0, 51, 102, 0.2) 0%,
      rgba(0, 51, 102, 0) 70%
    );
  filter: blur(30px);
  opacity: 0.8;
  z-index: 0;
  animation: nebulaShift 60s ease-in-out infinite alternate;
}

.dashboard-container {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  z-index: 10;
  padding-top: 15vh;
}

.theme-selector {
  position: absolute;
  bottom: 20px;
  left: 80px;
  display: flex;
  gap: 15px;
  background: rgba(30, 30, 45, 0.7);
  border-radius: 12px;
  padding: 10px 15px;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
  z-index: 20;
  transform: translateY(20px) translateX(25px);
  opacity: 0;
  visibility: hidden;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  transform-origin: bottom left;
  pointer-events: none;
}

.theme-selector-visible {
  transform: translateY(0) translateX(0);
  opacity: 1;
  visibility: visible;
  pointer-events: all;
}

.theme-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 8px;
  border-radius: 8px;
}

.theme-option:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-3px);
}

.theme-option.active {
  background: rgba(255, 255, 255, 0.2);
  box-shadow: 0 0 15px rgba(124, 77, 255, 0.5);
}

.theme-icon {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-bottom: 5px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.theme-option:hover .theme-icon {
  transform: scale(1.1);
  border-color: rgba(255, 255, 255, 0.5);
}

.theme-option.active .theme-icon {
  border-color: white;
  transform: scale(1.1);
}

.theme-icon.cosmic {
  background: linear-gradient(135deg, #7c4dff 0%, #0d47a1 100%);
  box-shadow: 0 0 10px rgba(124, 77, 255, 0.5);
}

.theme-icon.ocean {
  background: linear-gradient(135deg, #4fc3f7 0%, #0d47a1 100%);
  box-shadow: 0 0 10px rgba(79, 195, 247, 0.5);
}

.theme-icon.cyberpunk {
  background: linear-gradient(135deg, #ff4081 0%, #ab47bc 100%);
  box-shadow: 0 0 10px rgba(255, 64, 129, 0.5);
}

.theme-icon.forest {
  background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%);
  box-shadow: 0 0 10px rgba(46, 125, 50, 0.5);
}

.theme-icon.snow {
  background: linear-gradient(135deg, #6ebeff 0%, #eff5ff 100%);
  box-shadow: 0 0 10px rgba(144, 202, 249, 0.5);
}

.theme-option span {
  font-size: 12px;
  opacity: 0.8;
  transition: all 0.3s ease;
}

.theme-option:hover span,
.theme-option.active span {
  opacity: 1;
}

.theme-tab {
  position: absolute;
  bottom: 20px;
  left: 20px;
  width: 52px;
  height: 52px;
  background: rgba(30, 30, 45, 0.7);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  z-index: 30;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(5px);
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.theme-tab:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4);
  background: rgba(40, 40, 60, 0.8);
}

.theme-tab:active {
  transform: scale(0.95);
}

.theme-tab-icon {
  color: white;
  width: 24px;
  height: 24px;
  animation: rotateIcon 10s linear infinite;
}

@keyframes rotateIcon {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animation-toggle {
  margin-left: 10px;
  background-color: rgba(30, 30, 45, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.animation-toggle:hover {
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-3px);
}

.animation-toggle.active {
  border-color: #4fc3f7;
  box-shadow: 0 0 15px rgba(79, 195, 247, 0.5);
}

.animation-toggle:not(.active) {
  opacity: 0.7;
}

.animation-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.5rem;
  color: #fff;
}

.animation-icon i {
  transition: all 0.3s ease;
}

.animation-toggle.active .animation-icon i {
  color: #4fc3f7;
}

.animation-toggle:not(.active) .animation-icon i {
  color: #aaa;
}

/* Add animation for changing themes */
@keyframes nebulaShift {
  0% {
    transform: scale(1) rotate(0deg);
  }
  50% {
    transform: scale(1.2) rotate(5deg);
  }
  100% {
    transform: scale(1) rotate(10deg);
  }
}

/* Container principal pour tous les éléments spatiaux */
.space-elements {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 1;
}

/* Animation badge débloqué */
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
  z-index: 3000;
  animation: fadeIn 0.5s ease-out;
}

.badge-unlock-animation {
  background-color: #fff;
  border-radius: 20px;
  padding: 30px;
  text-align: center;
  max-width: 400px;
  box-shadow: 0 0 30px rgba(249, 71, 136, 0.6);
  animation: scaleIn 0.5s ease-out;
}

.badge-unlock-animation.special-celebration {
  background: linear-gradient(135deg, #FFD700, #FFA500, #FF6347);
  box-shadow: 0 0 50px rgba(255, 215, 0, 0.8);
  animation: scaleIn 0.5s ease-out, celebration-glow 2s ease-in-out infinite alternate;
}

.badge-unlock-animation .badge-icon {
  font-size: 80px;
  margin-bottom: 20px;
  animation: pulse 2s infinite;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 120px;
  height: 120px;
  margin: 0 auto 20px;
  border-radius: 50%;
  background-color: #f3f3f3;
}

.special-celebration .badge-icon {
  background: radial-gradient(circle, #FFD700, #FFA500);
  animation: pulse 2s infinite, trophy-bounce 1s ease-in-out infinite alternate;
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.7);
}

.badge-unlock-animation h2 {
  color: #FF4081;
  font-size: 2rem;
  margin-bottom: 10px;
}

.special-celebration h2 {
  color: #8B4513;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  animation: text-celebration 1.5s ease-in-out infinite alternate;
}

.badge-unlock-animation h3 {
  color: #333;
  font-size: 1.5rem;
  margin-bottom: 15px;
}

.special-celebration h3 {
  color: #654321;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
}

.badge-unlock-animation p {
  color: #666;
  margin-bottom: 20px;
}

.special-celebration p {
  color: #4B3621;
  font-weight: 500;
  font-size: 1.1rem;
}

.close-animation-btn {
  background-color: #FF4081;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 50px;
  font-weight: bold;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.close-animation-btn.celebration-btn {
  background: linear-gradient(135deg, #FF6347, #FFD700);
  color: #8B4513;
  font-weight: bold;
  animation: button-celebration 1s ease-in-out infinite alternate;
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.5);
}

.close-animation-btn:hover {
  background-color: #D81B60;
  transform: scale(1.05);
}

.close-animation-btn.celebration-btn:hover {
  background: linear-gradient(135deg, #FFD700, #FF6347);
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(255, 215, 0, 0.7);
}

/* Animations spéciales */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scaleIn {
  from { transform: scale(0.8); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

@keyframes celebration-glow {
  0% { box-shadow: 0 0 50px rgba(255, 215, 0, 0.8); }
  100% { box-shadow: 0 0 70px rgba(255, 165, 0, 1); }
}

@keyframes trophy-bounce {
  0% { transform: scale(1); }
  100% { transform: scale(1.1); }
}

@keyframes text-celebration {
  0% { transform: scale(1); color: #8B4513; }
  100% { transform: scale(1.05); color: #654321; }
}

@keyframes button-celebration {
  0% { transform: scale(1); }
  100% { transform: scale(1.02); }
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

/* Particules en arrière-plan - Plus nombreuses et plus dynamiques */
.particles-container {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.particle {
  position: absolute;
  width: 3px !important;
  height: 3px !important;
  background: radial-gradient(
    circle,
    rgba(255, 255, 255, 0.9) 0%,
    rgba(255, 255, 255, 0) 70%
  ) !important;
  border-radius: 50%;
  animation: floatDust infinite;
  box-shadow: 0 0 6px 2px rgba(111, 168, 220, 0.2);
}

.particle:nth-child(3n) {
  background: radial-gradient(
    circle,
    rgba(168, 111, 220, 0.9) 0%,
    rgba(168, 111, 220, 0) 70%
  ) !important;
  box-shadow: 0 0 8px 2px rgba(168, 111, 220, 0.3);
}

.particle:nth-child(3n + 1) {
  background: radial-gradient(
    circle,
    rgba(111, 168, 220, 0.9) 0%,
    rgba(111, 168, 220, 0) 70%
  ) !important;
  box-shadow: 0 0 8px 2px rgba(111, 168, 220, 0.3);
}

@keyframes float {
  0% {
    transform: translateY(0) translateX(0) rotate(0deg);
    opacity: 0;
  }
  50% {
    opacity: 0.5;
    transform: translateY(-50px) translateX(25px) rotate(180deg);
  }
  100% {
    transform: translateY(-100px) translateX(50px) rotate(360deg);
    opacity: 0;
  }
}

@keyframes particleExpand {
  0% {
    transform: translate(0, 0) scale(0);
    opacity: 0;
  }
  20% {
    opacity: 0.8;
  }
  100% {
    transform: translate(
        calc(cos(var(--angle)) * var(--distance)),
        calc(sin(var(--angle)) * var(--distance))
      )
      scale(0);
    opacity: 0;
  }
}

.current-level-badge {
  position: relative;
  margin-top: 5px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.current-badge-image {
  width: 160px;
  height: 160px;
  object-fit: contain;
  transition: all 0.3s ease;
  filter: drop-shadow(0 5px 15px rgba(255, 215, 0, 0.5));
  cursor: pointer;
}

.current-badge-image:hover {
  transform: scale(1.1);
  filter: drop-shadow(0 8px 20px rgba(255, 215, 0, 0.7));
}

/* Conserver les styles existants pour le tooltip */
.badge-tooltip {
  position: fixed;
  background: rgba(30, 30, 45, 0.95);
  border-radius: 12px;
  padding: 15px;
  max-width: 250px;
  z-index: 1000;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
  transition: all 0.3s ease;
  pointer-events: none;
}

.badge-tooltip:after {
  content: '';
  position: absolute;
  top: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-bottom: 8px solid rgba(30, 30, 45, 0.95);
}

.tooltip-title {
  font-weight: bold;
  font-size: 16px;
  color: white;
  margin-bottom: 8px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.tooltip-description {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 10px;
  line-height: 1.4;
}

.tooltip-requirement {
  font-size: 12px;
  color: #4fc3f7;
  font-style: italic;
}

.badge-evolution-text {
  margin-top: 3px;
  font-size: 14px;
  color: #0062ff;
  text-align: center;
  font-weight: bold;
  animation: pulse-text 1.5s infinite;
}

@keyframes pulse-text {
  0% {
    opacity: 0.7;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0.7;
  }
}

.badge-click-animation {
  animation: badge-click 0.3s ease;
}

@keyframes badge-click {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(0.9);
  }
  100% {
    transform: scale(1);
  }
}

.badge-evolve-animation {
  animation: badge-evolve 1s ease;
}

@keyframes badge-evolve {
  0% {
    transform: scale(1);
    filter: brightness(1);
  }
  50% {
    transform: scale(1.3);
    filter: brightness(1.5);
  }
  100% {
    transform: scale(1);
    filter: brightness(1);
  }
}

/* Bouton pour accéder au parcours */
.parcours-button-container {
  position: absolute;
  bottom: 20px;
  right: 20px;
  z-index: 30;
}

.parcours-button {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(30, 30, 45, 0.7);
  padding: 10px 20px;
  border-radius: 30px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  font-weight: bold;
  cursor: pointer;
  backdrop-filter: blur(5px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
}

.parcours-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.4);
  background: rgba(40, 40, 60, 0.8);
}

.parcours-button-icon {
  font-size: 20px;
}

/* Avatar and Progress Ring - Highly enhanced! */
.avatar-container {
  position: relative;
  width: 240px;
  height: 240px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: all 0.5s ease;
  z-index: 5;
}

.avatar-pulse {
  animation: avatarEnhancedPulse 1s ease;
}

@keyframes avatarEnhancedPulse {
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

.progress-ring-container {
  position: absolute;
  width: 260px;
  height: 260px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  overflow: visible;
}

.progress-ring {
  transform: rotate(-90deg);
  width: 100%;
  height: 100%;
  overflow: visible;
}

.progress-ring-circle {
  transition: stroke-dashoffset 1s ease-in-out;
  transform-origin: 50% 50%;
  stroke-dasharray: 754;
}

.progress-ring-circle-bg {
  stroke-dasharray: 754;
  stroke-dashoffset: 0;
}

.progress-ring-blur {
  stroke-dasharray: 754;
  stroke-dashoffset: 0;
  filter: blur(12px);
}

.avatar-image-container {
  position: relative;
  width: 200px;
  height: 200px;
  border-radius: 50%;
  overflow: hidden;
  z-index: 2;
  transition: all 0.5s ease;
}

.avatar-image-container:hover {
  transform: scale(1.05);
}

.avatar-effects {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 1;
  pointer-events: none;
}

.avatar-effect-circle {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.2);
  opacity: 0;
  animation: circleExpand 3s infinite;
}

.avatar-effect-circle:nth-child(1) {
  animation-delay: 0s;
}

.avatar-effect-circle:nth-child(2) {
  animation-delay: 1s;
}

.avatar-effect-circle:nth-child(3) {
  animation-delay: 2s;
}

@keyframes circleExpand {
  0% {
    width: 40%;
    height: 40%;
    border-color: rgba(79, 195, 247, 0.5);
    opacity: 0.7;
  }
  100% {
    width: 150%;
    height: 150%;
    border-color: rgba(255, 64, 129, 0);
    opacity: 0;
  }
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: all 0.5s ease;
}

.avatar-container:hover .avatar-image {
  transform: scale(1.05);
}

.level-badge {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(to right, #4fc3f7, #7c4dff);
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: bold;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  z-index: 3;
}

/* Effet de mise en évidence de l'avatar */
.avatar-highlight-effect {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 300px;
  height: 300px;
  z-index: 4;
  pointer-events: none;
}

.pulse-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 240px;
  height: 240px;
  border-radius: 50%;
  border: 4px solid #76ff03;
  box-shadow: 0 0 20px rgba(118, 255, 3, 0.7);
  opacity: 0.7;
  animation: pulse-ring 2s ease-out infinite;
}

.hint-arrow {
  position: absolute;
  top: -60px;
  left: 50%;
  transform: translateX(-50%);
  animation: bounce 2s ease infinite;
  text-align: center;
}

.arrow {
  display: block;
  font-size: 36px;
  color: #76ff03;
  text-shadow: 0 0 10px rgba(118, 255, 3, 0.7);
}

.hint-text {
  display: block;
  color: white;
  font-weight: bold;
  font-size: 18px;
  margin-top: 5px;
  padding: 5px 10px;
  background-color: rgba(0, 0, 0, 0.7);
  border-radius: 20px;
  white-space: nowrap;
}

@keyframes pulse-ring {
  0% {
    transform: translate(-50%, -50%) scale(0.9);
    opacity: 0.7;
  }
  50% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.9;
  }
  100% {
    transform: translate(-50%, -50%) scale(0.9);
    opacity: 0.7;
  }
}

@keyframes bounce {
  0%,
  20%,
  50%,
  80%,
  100% {
    transform: translateX(-50%) translateY(0);
  }
  40% {
    transform: translateX(-50%) translateY(-15px);
  }
  60% {
    transform: translateX(-50%) translateY(-7px);
  }
}

/* Styles pour améliorer l'intégration du guide */
.guide-avatar-container {
  z-index: 1050; /* S'assurer que le guide est au-dessus des autres éléments */
}

.guide-top-left {
  position: fixed;
  top: 20px;
  left: 20px;
  z-index: 2000;
}

.speech-bubble {
  background-color: #fff;
  font-family: 'Comic Sans MS', 'Chalkboard SE', 'Marker Felt', sans-serif;
  color: #333;
  border: 2px solid #58cc02; /* Couleur verte de Duolingo */
}

.speech-bubble:after {
  border-color: #fff transparent transparent;
}

.bubble-header {
  border-bottom: 1px solid #58cc02;
}

.guide-name {
  color: #58cc02;
}

.option-button {
  background-color: #fff;
  border: 2px solid #58cc02;
  color: #58cc02;
  font-weight: bold;
  transition: all 0.2s ease;
}

.option-button:hover {
  background-color: #58cc02;
  color: #fff;
}

.avatar-container:hover .level-badge {
  transform: translateX(-50%) translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.4);
  background: linear-gradient(to right, #7c4dff, #ff4081);
}

.avatar-glow {
  background: radial-gradient(
    circle,
    rgba(111, 168, 220, 0.5) 0%,
    rgba(168, 111, 220, 0.5) 50%,
    rgba(220, 111, 168, 0.5) 100%
  );
  filter: blur(20px);
  opacity: 0.7;
  animation: cosmicRotate 15s linear infinite;
}

.avatar-glow.pulse {
  animation: cosmicPulse 1s;
}

@keyframes avatarGlowPulse {
  0% {
    transform: scale(0.95);
    opacity: 0.5;
    filter: blur(15px);
  }
  50% {
    transform: scale(1.2);
    opacity: 0.8;
    filter: blur(20px);
  }
  100% {
    transform: scale(1);
    opacity: 0.5;
    filter: blur(15px);
  }
}

/* Menu d'interaction avec l'avatar */
.avatar-interaction {
  position: absolute;
  top: 110%;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(30, 30, 30, 0.9);
  border-radius: 12px;
  padding: 15px;
  display: flex;
  gap: 25px;
  z-index: 10;
  animation: enhancedSlideUp 0.4s;
  box-shadow:
    0 10px 25px rgba(0, 0, 0, 0.3),
    0 0 15px rgba(79, 195, 247, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.animation-toggle {
  margin-left: 10px;
  background-color: rgba(30, 30, 45, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.animation-toggle:hover {
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-3px);
}

.animation-toggle.active {
  border-color: #4fc3f7;
  box-shadow: 0 0 15px rgba(79, 195, 247, 0.5);
}

.animation-toggle:not(.active) {
  opacity: 0.7;
}

.animation-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.5rem;
  color: #fff;
}

.animation-icon i {
  transition: all 0.3s ease;
}

.animation-toggle.active .animation-icon i {
  color: #4fc3f7;
}

.animation-toggle:not(.active) .animation-icon i {
  color: #aaa;
}

@keyframes enhancedSlideUp {
  from {
    transform: translateX(-50%) translateY(20px);
    opacity: 0;
    filter: blur(5px);
  }
  to {
    transform: translateX(-50%) translateY(0);
    opacity: 1;
    filter: blur(0);
  }
}

.interaction-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  padding: 10px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.interaction-option:hover {
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.interaction-option svg {
  margin-bottom: 8px;
  transition: all 0.3s ease;
}

.interaction-option:hover svg {
  transform: scale(1.1);
  filter: drop-shadow(0 0 5px rgba(79, 195, 247, 0.5));
}

.interaction-option span {
  font-size: 14px;
  font-weight: 500;
}

/* Animation de récompense */
.achievement-popup {
  position: fixed;
  top: 50px;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(
    135deg,
    rgba(30, 30, 45, 0.9) 0%,
    rgba(30, 30, 60, 0.9) 100%
  );
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 20px;
  z-index: 100;
  box-shadow:
    0 10px 25px rgba(0, 0, 0, 0.5),
    0 0 20px rgba(168, 111, 220, 0.4);
}

@keyframes enhancedDropDown {
  0% {
    transform: translateX(-50%) translateY(-50px);
    opacity: 0;
    filter: blur(10px);
  }
  70% {
    transform: translateX(-50%) translateY(10px);
  }
  100% {
    transform: translateX(-50%) translateY(0);
    opacity: 1;
    filter: blur(0);
  }
}

@keyframes enhancedFadeOut {
  0% {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
  100% {
    opacity: 0;
    transform: translateX(-50%) translateY(-20px);
  }
}

.achievement-icon {
  font-size: 40px;
  animation: trophyShine 2s infinite;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.7);
}

@keyframes trophyShine {
  0% {
    text-shadow: 0 0 10px rgba(255, 215, 0, 0.7);
  }
  50% {
    text-shadow: 0 0 20px rgba(255, 215, 0, 1);
  }
  100% {
    text-shadow: 0 0 10px rgba(255, 215, 0, 0.7);
  }
}

.achievement-text h3 {
  color: #a86fdc;
  text-shadow: 0 0 10px rgba(168, 111, 220, 0.7);
}

.achievement-text p {
  margin: 0;
  font-size: 16px;
  color: #ffffff;
}

/* Styles pour le bouton Commencer à jouer */
.play-button-container {
  position: absolute;
  bottom: 90px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 30; /* Plus élevé que les autres éléments */
  pointer-events: auto; /* Le conteneur lui-même ne capture pas les événements */
}

.play-button {
  position: relative;
  padding: 16px 40px;
  font-size: 18px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: white;
  background: linear-gradient(135deg, #f94788 0%, #6495f8 50%, #b152c7 100%);
  border: none;
  border-radius: 30px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
  transform: perspective(1px) translateZ(0);
  width: 320px;
  height: 60px;
  pointer-events: auto; /* Le bouton lui-même capture les événements */
  z-index: 100;
}

.button-text {
  position: relative;
  z-index: 3;
  transition: all 0.3s ease;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.button-border {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 30px;
  z-index: 1;
  transition: all 0.3s ease;
  opacity: 0;
  overflow: hidden;
}

.button-border:before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(135deg, #f94788 0%, #6495f8 50%, #b152c7 100%);
  background-size: 200% 200%;
  border-radius: 32px;
  z-index: 1;
  opacity: 0.6;
}

.button-glow {
  position: absolute;
  width: 100%;
  height: 100%;
  left: 0;
  top: 0;
  background: radial-gradient(
    circle at center,
    rgba(249, 71, 136, 0.8) 0%,
    rgba(100, 149, 248, 0.5) 50%,
    rgba(177, 82, 199, 0.8) 100%
  );
  filter: blur(15px);
  opacity: 0;
  transition: opacity 0.5s ease;
  z-index: 0;
  transform: translateZ(-1px);
}

.play-button:before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    135deg,
    rgba(249, 71, 136, 0.8) 0%,
    rgba(100, 149, 248, 0.8) 50%,
    rgba(177, 82, 199, 0.8) 100%
  );
  border-radius: 30px;
  z-index: 2;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.play-button:after {
  content: '';
  position: absolute;
  left: -50%;
  top: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(
    ellipse at center,
    rgba(255, 255, 255, 0.3) 0%,
    rgba(255, 255, 255, 0) 60%
  );
  opacity: 0;
  transform: scale(0);
  transition:
    transform 0.6s ease,
    opacity 0.6s ease;
  z-index: 2;
  pointer-events: none;
}

.play-button.hovered {
  transform: translateY(-5px) scale(1.03);
  box-shadow:
    0 15px 30px rgba(0, 0, 0, 0.3),
    0 0 15px rgba(249, 71, 136, 0.3),
    0 0 15px rgba(100, 149, 248, 0.3),
    0 0 15px rgba(177, 82, 199, 0.3);
}

.play-button.hovered .button-glow {
  opacity: 0.8;
}

.play-button.hovered .button-text {
  transform: scale(1.05);
}

.play-button.hovered .button-border {
  opacity: 1;
}

.play-button.hovered .button-border:before {
  animation: gradientShift 3s ease infinite;
}

.play-button.pressed {
  transform: translateY(-2px) scale(0.98);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.play-button.pressed:after {
  opacity: 0.5;
  transform: scale(1);
}

@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

/* Adaptations pour les écrans plus petits */
@media (max-width: 768px) {
  .avatar-container {
    width: 200px;
    height: 200px;
    margin-bottom: 80px;
  }

  .progress-ring-container {
    width: 220px;
    height: 220px;
  }

  .avatar-image-container {
    width: 160px;
    height: 160px;
  }

  .theme-selector {
    bottom: 10px;
    right: 10px;
    padding: 5px 10px;
    gap: 10px;
  }

  .theme-icon {
    width: 20px;
    height: 20px;
  }

  .theme-option span {
    font-size: 10px;
  }

  .play-button {
    padding: 12px 30px;
    font-size: 16px;
    width: 240px;
    height: 50px;
  }

  .play-button-container {
    bottom: -100px;
  }

  .current-badge-image {
    width: 70px;
    height: 70px;
  }
}
</style>
