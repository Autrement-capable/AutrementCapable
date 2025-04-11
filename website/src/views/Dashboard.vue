<template>
  <div
    class="dashboard"
    :class="{
      'achievements-unlocked': hasNewAchievement,
    }"
  >
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
        @close="closeRewardsModal"
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

export default {
  name: 'UserDashboard',
  components: {
    SpaceBackground,
    StaticBackgrounds,
    RewardsComponent,
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
      ],
      progress: 37,
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
      achievements: [
        'Explorateur Curieux',
        'Premier Pas',
        'Maître du Temps',
        'Briseur de Barrières',
        'Esprit Créatif',
      ],
    }
  },
  methods: {
    toggleThemeMenu() {
      this.themeMenuVisible = !this.themeMenuVisible

      // Ajout d'une sensation tactile
      if (window.navigator && window.navigator.vibrate) {
        window.navigator.vibrate(50)
      }

      // Stocker la préférence dans localStorage
      localStorage.setItem(
        'theme-menu-visible',
        this.themeMenuVisible.toString()
      )
    },

    changeTheme(theme) {
      this.currentTheme = theme

      // Optional: store the selected theme in localStorage to persist across sessions
      localStorage.setItem('dashboard-theme', theme)

      // Optional: trigger achievement for first theme change
      if (!this.themeChangeAchieved && theme !== 'cosmic') {
        this.triggerAchievement('Explorateur de Mondes')
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
      this.showRewardsModal = true // Show the rewards modal instead of the interaction menu

      // Animation plus longue pour un meilleur effet
      setTimeout(() => {
        this.avatarAnimating = false
      }, 1000)
    },

    // Nouvelle méthode pour fermer le modal de récompenses
    closeRewardsModal() {
      this.showRewardsModal = false
    },

    // Personnalisation de l'avatar
    customizeAvatar() {
      this.showAvatarInteraction = false
      this.activeModal = 'customize'
      this.triggerAchievement('Esprit Créatif')
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
        this.animationsEnabled.toString()
      )

      if (window.navigator && window.navigator.vibrate) {
        window.navigator.vibrate(50)
      }

      this.$emit('toggle-animations', !this.animationsEnabled)
    },

    handlePlayButtonHover(isHovered) {
      this.playButtonHovered = isHovered;
      if (!isHovered) {
        this.playButtonPressed = false;
      }
    },

    startPlaying() {
      console.log('Commençons à jouer!')

      // Haptic feedback if available
      if (window.navigator && window.navigator.vibrate) {
        window.navigator.vibrate(50)
      }

      // Trigger achievement
      this.triggerAchievement('Premier Pas')
    },
  },
  mounted() {
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

    // Simulate a reward after a certain time
    setTimeout(() => {
      const randomAchievement =
        this.achievements[Math.floor(Math.random() * this.achievements.length)]
      this.triggerAchievement(randomAchievement)
    }, 5000)
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
  background: radial-gradient(
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
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3), 0 0 15px rgba(79, 195, 247, 0.3);
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
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5), 0 0 20px rgba(168, 111, 220, 0.4);
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
  transition: transform 0.6s ease, opacity 0.6s ease;
  z-index: 2;
  pointer-events: none;
}

.play-button.hovered {
  transform: translateY(-5px) scale(1.03);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3), 0 0 15px rgba(249, 71, 136, 0.3),
    0 0 15px rgba(100, 149, 248, 0.3), 0 0 15px rgba(177, 82, 199, 0.3);
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
}
</style>
