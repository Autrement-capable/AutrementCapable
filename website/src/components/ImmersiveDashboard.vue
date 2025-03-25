<template>
  <div class="dashboard" :class="{ 'achievements-unlocked': hasNewAchievement }">
    <!-- Effet de particules en arrière-plan -->
    <div class="particles-container">
      <div v-for="i in 30" :key="'particle-'+i" class="particle" :style="randomParticleStyle()"></div>
    </div>

    <!-- La structure principale -->
    <div class="dashboard-container">
      <!-- Section Formations -->
      <div class="section formations" @mouseenter="activeSection = 'formations'" @mouseleave="activeSection = null">
        <div class="section-content" :class="{ 'active': activeSection === 'formations' }">
            <div class="button-particles" v-if="activeSection === 'formations'">
            <div v-for="i in 8" :key="'formation-particle-'+i" class="button-particle" 
                :style="generateParticleStyle()"></div>
            </div>
            <div class="button-ring"></div>
            <div class="icon-container" @click="openSection('formations')">
            <div class="glow-effect" :class="{ 'pulse': activeSection === 'formations' }"></div>
            <div class="icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="64" height="64" fill="none" stroke="currentColor">
                <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 4c1.86 0 3.41 1.28 3.86 3H8.14c.45-1.72 2-3 3.86-3zm-4 6h8v2h-8v-2zm0 4h8v2h-8v-2z" stroke-width="1.5"/>
                </svg>
            </div>
            <span class="tooltip">Formations</span>
            <div class="notification" v-if="notifications.formations > 0">{{ notifications.formations }}</div>
            </div>
        </div>
    </div>

      <!-- Section Badges -->
      <div class="section badges" @mouseenter="activeSection = 'badges'" @mouseleave="activeSection = null">
				<div class="section-content" :class="{ 'active': activeSection === 'badges' }">
					<div class="button-particles" v-if="activeSection === 'badges'">
						<div v-for="i in 8" :key="'badge-particle-'+i" class="button-particle" 
								:style="generateParticleStyle()"></div>
					</div>
					<div class="button-ring"></div>
					<div class="icon-container" @click="openSection('badges')">
						<div class="glow-effect" :class="{ 'pulse': activeSection === 'badges' }"></div>
						<div class="icon">
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="64" height="64" fill="none" stroke="currentColor">
								<circle cx="12" cy="8" r="7" stroke-width="1.5"/>
								<path d="M15.5 14l2 8-5.5-3-5.5 3 2-8" stroke-width="1.5"/>
							</svg>
						</div>
						<span class="tooltip">Badges</span>
						<div class="notification" v-if="notifications.badges > 0">{{ notifications.badges }}</div>
					</div>
				</div>
			</div>

      <!-- Section Jeux -->
      <div class="section games" @mouseenter="activeSection = 'games'" @mouseleave="activeSection = null">
				<div class="section-content" :class="{ 'active': activeSection === 'games' }">
					<div class="button-particles" v-if="activeSection === 'games'">
						<div v-for="i in 8" :key="'game-particle-'+i" class="button-particle" 
								:style="generateParticleStyle()"></div>
					</div>
					<div class="button-ring"></div>
					<div class="icon-container" @click="openSection('games')">
						<div class="glow-effect" :class="{ 'pulse': activeSection === 'games' }"></div>
						<div class="icon">
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="64" height="64" fill="none" stroke="currentColor">
								<path d="M17 4H7a5 5 0 0 0-5 5v6a5 5 0 0 0 5 5h10a5 5 0 0 0 5-5V9a5 5 0 0 0-5-5z" stroke-width="1.5"/>
								<path d="M10 10H8v2H6v2h2v2h2v-2h2v-2h-2v-2zM17.5 15a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3zM15 11a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z" stroke-width="1.5"/>
							</svg>
						</div>
						<span class="tooltip">Jeux</span>
						<div class="notification" v-if="notifications.games > 0">{{ notifications.games }}</div>
					</div>
				</div>
			</div>

      <!-- Section Profil - Plus Immersive! -->
      <div class="section profile" 
				@mouseenter="activeSection = 'profile'" 
				@mouseleave="activeSection = null"
				:class="{ 'profile-highlight': activeSection === 'profile' }">
			<div class="section-content" :class="{ 'active': activeSection === 'profile' }">
				<div class="button-particles" v-if="activeSection === 'profile'">
					<div v-for="i in 8" :key="'profile-particle-'+i" class="button-particle" 
							:style="generateParticleStyle()"></div>
				</div>
				<div class="button-ring"></div>
				<div class="icon-container" @click="openSection('profile')">
					<div class="glow-effect" :class="{ 'pulse': activeSection === 'profile' }"></div>
					<div class="icon profile-icon" :class="{ 'profile-active': activeSection === 'profile' }">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="64" height="64" fill="none" stroke="currentColor">
							<circle cx="12" cy="8" r="5" stroke-width="1.5"/>
							<path d="M20 21v-2a6 6 0 0 0-6-6H10a6 6 0 0 0-6 6v2" stroke-width="1.5"/>
						</svg>
					</div>
					<span class="tooltip tooltip-profile">Profil</span>
					<div class="notification" v-if="notifications.profile > 0">{{ notifications.profile }}</div>
				</div>
			</div>
		</div>

      <!-- Avatar central avec cercle de progression amélioré -->
      <div class="avatar-container" @click="interactWithAvatar" :class="{ 'avatar-pulse': avatarAnimating }">
        <div class="progress-ring-container">
          <svg class="progress-ring" width="300" height="260">
            <!-- Background glow effect -->
            <filter id="glow">
              <feGaussianBlur stdDeviation="3.5" result="blur"/>
              <feComposite in="SourceGraphic" in2="blur" operator="over"/>
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
              <linearGradient id="progressGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#4FC3F7">
                  <animate attributeName="stop-color" 
                           values="#4FC3F7;#7C4DFF;#FF4081;#4FC3F7" 
                           dur="8s" 
                           repeatCount="indefinite"/>
                </stop>
                <stop offset="50%" stop-color="#7C4DFF">
                  <animate attributeName="stop-color" 
                           values="#7C4DFF;#FF4081;#4FC3F7;#7C4DFF" 
                           dur="8s" 
                           repeatCount="indefinite"/>
                </stop>
                <stop offset="100%" stop-color="#FF4081">
                  <animate attributeName="stop-color" 
                           values="#FF4081;#4FC3F7;#7C4DFF;#FF4081" 
                           dur="8s" 
                           repeatCount="indefinite"/>
                </stop>
              </linearGradient>
              
              <linearGradient id="blurGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="rgba(79, 195, 247, 0.3)">
                  <animate attributeName="stop-color" 
                           values="rgba(79, 195, 247, 0.3);rgba(124, 77, 255, 0.3);rgba(255, 64, 129, 0.3);rgba(79, 195, 247, 0.3)" 
                           dur="8s" 
                           repeatCount="indefinite"/>
                </stop>
                <stop offset="100%" stop-color="rgba(255, 64, 129, 0.3)">
                  <animate attributeName="stop-color" 
                           values="rgba(255, 64, 129, 0.3);rgba(79, 195, 247, 0.3);rgba(124, 77, 255, 0.3);rgba(255, 64, 129, 0.3)" 
                           dur="8s" 
                           repeatCount="indefinite"/>
                </stop>
              </linearGradient>

              <linearGradient id="formationsGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#4FC3F7">
                <animate attributeName="stop-color" 
                        values="#4FC3F7;#29B6F6;#03A9F4;#4FC3F7" 
                        dur="4s" 
                        repeatCount="indefinite"/>
                </stop>
                <stop offset="100%" stop-color="#03A9F4">
                <animate attributeName="stop-color" 
                        values="#03A9F4;#4FC3F7;#29B6F6;#03A9F4" 
                        dur="4s" 
                        repeatCount="indefinite"/>
                </stop>
            </linearGradient>
            
            <linearGradient id="badgesGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#7C4DFF">
                <animate attributeName="stop-color" 
                        values="#7C4DFF;#651FFF;#6200EA;#7C4DFF" 
                        dur="4s" 
                        repeatCount="indefinite"/>
                </stop>
                <stop offset="100%" stop-color="#6200EA">
                <animate attributeName="stop-color" 
                        values="#6200EA;#7C4DFF;#651FFF;#6200EA" 
                        dur="4s" 
                        repeatCount="indefinite"/>
                </stop>
            </linearGradient>
            
            <linearGradient id="gamesGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#FF4081">
                <animate attributeName="stop-color" 
                        values="#FF4081;#F50057;#C51162;#FF4081" 
                        dur="4s" 
                        repeatCount="indefinite"/>
                </stop>
                <stop offset="100%" stop-color="#C51162">
                <animate attributeName="stop-color" 
                        values="#C51162;#FF4081;#F50057;#C51162" 
                        dur="4s" 
                        repeatCount="indefinite"/>
                </stop>
            </linearGradient>
            
            <linearGradient id="profileGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#1DE9B6">
                <animate attributeName="stop-color" 
                        values="#1DE9B6;#00BFA5;#00897B;#1DE9B6" 
                        dur="4s" 
                        repeatCount="indefinite"/>
                </stop>
                <stop offset="100%" stop-color="#00897B">
                <animate attributeName="stop-color" 
                        values="#00897B;#1DE9B6;#00BFA5;#00897B" 
                        dur="4s" 
                        repeatCount="indefinite"/>
                </stop>
            </linearGradient>

            </defs>
          </svg>
        </div>

        <div class="avatar-image-container">
          <div class="avatar-effects">
            <div class="avatar-effect-circle" v-for="i in 3" :key="'effect-'+i"></div>
          </div>
          <img src="@/assets/jeunefemme.png" alt="Avatar" class="avatar-image" />
          <div class="level-badge">Niveau {{ calculateLevel() }}</div>
          <div class="avatar-glow" :class="{ 'pulse': avatarAnimating }"></div>
        </div>
        
        <div class="avatar-interaction" v-if="showAvatarInteraction">
          <div class="interaction-option" @click.stop="customizeAvatar">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor">
              <path d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18z" stroke-width="1.5"/>
              <path d="M8 14s1.5 2 4 2 4-2 4-2" stroke-width="1.5"/>
              <circle cx="9" cy="9" r="1" stroke-width="1.5"/>
              <circle cx="15" cy="9" r="1" stroke-width="1.5"/>
            </svg>
            <span>Personnaliser</span>
          </div>
          <div class="interaction-option" @click.stop="viewAchievements">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor">
              <path d="M12 15l-2-5 4-3-4 1-3 1 5 1 3 5h-3z" stroke-width="1.5"/>
              <path d="M19 9l-7 1-2-3h5l4 2z" stroke-width="1.5"/>
              <path d="M4 11l5-3 2 5-3 3-4-5z" stroke-width="1.5"/>
            </svg>
            <span>Réalisations</span>
          </div>
        </div>
      </div>
      
      <!-- Animation de récompense -->
      <div class="achievement-popup" v-if="showAchievement">
        <div class="achievement-icon">🏆</div>
        <div class="achievement-text">
          <h3>Nouvelle réalisation!</h3>
          <p>{{ currentAchievement }}</p>
        </div>
      </div>
      
      <!-- Écran modal pour afficher les sections -->
      <div class="modal" v-if="activeModal" @click="closeModal">
        <div class="modal-content" :class="activeModal" @click.stop>
          <button class="close-button" @click="closeModal">×</button>
          <h2>{{ getModalTitle() }}</h2>
          <div class="modal-body">
            <p>Contenu de la section {{ activeModal }}</p>
            <!-- Le contenu sera dynamique selon la section -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ImmersiveDashboard',
  data() {
    return {
      progress: 67, // Progression globale en pourcentage
      activeSection: null,
      avatarAnimating: false,
      showAvatarInteraction: false,
      activeModal: null,
      showAchievement: false,
      hasNewAchievement: false,
      currentAchievement: '',
      notifications: {
        formations: 3,
        badges: 1,
        games: 2,
        profile: 0
      },
      achievements: [
        'Explorateur Curieux',
        'Premier Pas',
        'Maître du Temps',
        'Briseur de Barrières',
        'Esprit Créatif'
      ]
    };
  },
  methods: {
    // Calcule l'offset pour le cercle de progression
    calculateProgressOffset() {
      const circumference = 2 * Math.PI * 120;
      return circumference - (circumference * this.progress) / 100;
    },
    
    // Calcule le niveau actuel basé sur la progression
    calculateLevel() {
      return Math.floor(this.progress / 10) + 1;
    },

    generateParticleStyle() {
			const duration = 1 + Math.random() * 1.5;
			const delay = Math.random() * 0.5;
			const size = 3 + Math.random() * 4;
			
			return {
				left: 'calc(50% - ' + (size / 2) + 'px)',
				top: 'calc(50% - ' + (size / 2) + 'px)',
				width: size + 'px',
				height: size + 'px',
				transform: 'scale(0)',
				opacity: '0',
				animation: `particleExpand ${duration}s ease ${delay}s infinite`
			};
		},

    
    // Génère un style aléatoire pour les particules d'arrière-plan
    randomParticleStyle() {
      return {
        left: `${Math.random() * 100}%`,
        top: `${Math.random() * 100}%`,
        animationDelay: `${Math.random() * 5}s`,
        animationDuration: `${5 + Math.random() * 10}s`,
        opacity: Math.random() * 0.5,
        transform: `scale(${0.5 + Math.random() * 1.5})`
      };
    },
    
    // Interaction avec l'avatar - Animation améliorée
    interactWithAvatar() {
      this.avatarAnimating = true;
      this.showAvatarInteraction = !this.showAvatarInteraction;
      
      // Animation plus longue pour un meilleur effet
      setTimeout(() => {
        this.avatarAnimating = false;
      }, 1000);
    },
    
    // Ouvre une section spécifique
    openSection(section) {
			// Create a ripple effect element
			const ripple = document.createElement('div');
			ripple.className = 'button-ripple';
			
			// Find the section element
			const sectionEl = document.querySelector(`.section.${section} .section-content`);
			if (sectionEl) {
				sectionEl.appendChild(ripple);
				
				// Trigger ripple animation
				setTimeout(() => {
					ripple.remove();
				}, 600);
				
				// Add haptic feedback if available
				if (window.navigator && window.navigator.vibrate) {
					window.navigator.vibrate(50);
				}
			}
			
			this.activeModal = section;
			
			// Animation speciale pour le profil
			if (section === 'profile') {
				this.triggerProfileAnimation();
			}
			
			// Create a flash effect
			this.createButtonFlash(section);
			
			// Réduire la notification
			if (this.notifications[section] > 0) {
				this.notifications[section]--;
			}
		},

		createButtonFlash(section) {
			const flash = document.createElement('div');
			flash.className = `button-flash ${section}-flash`;
			
			const sectionEl = document.querySelector(`.section.${section}`);
			if (sectionEl) {
				sectionEl.appendChild(flash);
				
				setTimeout(() => {
					flash.remove();
				}, 500);
			}
		},
    
    // Animation spéciale pour le profil
    triggerProfileAnimation() {
      this.avatarAnimating = true;
      setTimeout(() => {
        this.avatarAnimating = false;
      }, 1000);
    },
    
    // Ferme le modal
    closeModal() {
      this.activeModal = null;
    },
    
    // Obtient le titre du modal
    getModalTitle() {
      const titles = {
        formations: 'Mes Formations',
        badges: 'Mes Badges',
        games: 'Mes Jeux',
        profile: 'Mon Profil'
      };
      return titles[this.activeModal] || 'Section';
    },
    
    // Personnalisation de l'avatar
    customizeAvatar() {
      this.showAvatarInteraction = false;
      this.activeModal = 'customize';
      this.triggerAchievement('Esprit Créatif');
    },
    
    // Voir les réalisations
    viewAchievements() {
      this.showAvatarInteraction = false;
      this.activeModal = 'achievements';
    },
    
    // Déclenche une animation de réalisation
    triggerAchievement(achievement) {
      this.currentAchievement = achievement;
      this.showAchievement = true;
      this.hasNewAchievement = true;
      
      // Animation de progression
      const oldProgress = this.progress;
      const newProgress = Math.min(100, oldProgress + 5);
      
      // Animation progressive du changement
      const step = 0.5;
      const duration = 2000; // 2 secondes
      const steps = (newProgress - oldProgress) / step;
      const interval = duration / steps;
      
      const progressAnimation = setInterval(() => {
        if (this.progress < newProgress) {
          this.progress += step;
        } else {
          clearInterval(progressAnimation);
        }
      }, interval);
      
      // Faire disparaître l'animation après 3 secondes
      setTimeout(() => {
        this.showAchievement = false;
      }, 3000);
      
      // Réinitialiser l'effet de fond
      setTimeout(() => {
        this.hasNewAchievement = false;
      }, 4000);
    }
  },
  mounted() {
    // Simuler des notifications périodiques
    setInterval(() => {
      const sections = ['formations', 'badges', 'games', 'profile'];
      const randomSection = sections[Math.floor(Math.random() * sections.length)];
      
      if (Math.random() > 0.7) {
        this.notifications[randomSection]++;
      }
    }, 30000);
    
    // Simuler une récompense après un certain temps
    setTimeout(() => {
      const randomAchievement = this.achievements[Math.floor(Math.random() * this.achievements.length)];
      this.triggerAchievement(randomAchievement);
    }, 5000);
  }
};
</script>

<style scoped>
.dashboard {
  position: relative;
  width: 100%;
  height: 100vh;
  background-color: #121212;
  color: white;
  overflow: hidden;
  font-family: 'Nunito', sans-serif;
  transition: background-color 0.5s ease;
  background: radial-gradient(circle at center, #1a1a2a 0%, #121212 70%);
}

.dashboard-container {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
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
  width: 6px;
  height: 6px;
  background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 70%);
  border-radius: 50%;
  animation: float infinite;
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
    ) scale(0);
    opacity: 0;
  }
}

.button-ripple {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 5px;
  height: 5px;
  background: white;
  border-radius: 50%;
  transform: translate(-50%, -50%) scale(0);
  animation: rippleEffect 0.6s ease-out;
  opacity: 0.7;
  pointer-events: none;
}

@keyframes rippleEffect {
  0% {
    transform: translate(-50%, -50%) scale(0);
    opacity: 0.7;
  }
  100% {
    transform: translate(-50%, -50%) scale(20);
    opacity: 0;
  }
}

.button-flash {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  opacity: 0;
  pointer-events: none;
  animation: flashEffect 0.5s ease-out;
  z-index: 10;
}

.formations-flash {
  background: radial-gradient(circle, rgba(79, 195, 247, 0.8) 0%, rgba(79, 195, 247, 0) 70%);
}

.badges-flash {
  background: radial-gradient(circle, rgba(124, 77, 255, 0.8) 0%, rgba(124, 77, 255, 0) 70%);
}

.games-flash {
  background: radial-gradient(circle, rgba(255, 64, 129, 0.8) 0%, rgba(255, 64, 129, 0) 70%);
}

.profile-flash {
  background: radial-gradient(circle, rgba(29, 233, 182, 0.8) 0%, rgba(29, 233, 182, 0) 70%);
}

@keyframes flashEffect {
  0% {
    opacity: 0;
  }
  50% {
    opacity: 0.5;
  }
  100% {
    opacity: 0;
  }
}

/* Effet d'animation lors d'un nouvel accomplissement */
.achievements-unlocked {
  background: radial-gradient(circle at center, #1a237e 0%, #121240 100%);
  animation: pulseBackground 4s ease;
}

@keyframes pulseBackground {
  0% { background: radial-gradient(circle at center, #1a1a2a 0%, #121212 100%); }
  20% { background: radial-gradient(circle at center, #1a237e 0%, #121240 100%); }
  100% { background: radial-gradient(circle at center, #1a1a2a 0%, #121212 100%); }
}

/* Sections */
.section {
  position: absolute;
  width: 150px;
  height: 150px;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  perspective: 1000px;
  z-index: 10;
}

.section:hover {
  transform: scale(1.1);
}

.section:active {
  transform: scale(0.95);
}

.formations {
  top: 20%;
  left: 20%;
}

.formations .section-content {
  background: linear-gradient(135deg, rgba(30, 30, 45, 0.7) 0%, rgba(30, 50, 80, 0.7) 100%);
}

.badges {
  top: 20%;
  right: 20%;
}

.badges .section-content {
  background: linear-gradient(135deg, rgba(30, 30, 45, 0.7) 0%, rgba(60, 30, 80, 0.7) 100%);
}

.games {
  bottom: 20%;
  left: 20%;
}

.games .section-content {
  background: linear-gradient(135deg, rgba(30, 30, 45, 0.7) 0%, rgba(80, 30, 50, 0.7) 100%);
}

.profile {
  bottom: 20%;
  right: 20%;
  transition: all 0.5s ease;
}

.profile .section-content {
  background: linear-gradient(135deg, rgba(30, 30, 45, 0.7) 0%, rgba(30, 80, 70, 0.7) 100%);
}

/* Mise en évidence spéciale pour la section profil */
.profile-highlight {
  transform: scale(1.1);
  z-index: 5;
}

/* Particules spéciales du profil */
.profile-particles {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

@keyframes profileParticle {
  0% {
    transform: translate(calc(50% - 4px), calc(50% - 4px)) scale(0.2);
    opacity: 0;
  }
  50% {
    opacity: 0.8;
  }
  100% {
    transform: translate(calc(50% - 4px), calc(50% - 4px)) translateX(calc(random(100) * 1px - 50px)) translateY(calc(random(100) * 1px - 50px)) scale(0);
    opacity: 0;
  }
}

.profile-particle:nth-child(1) { animation-delay: 0s; }
.profile-particle:nth-child(2) { animation-delay: 0.3s; }
.profile-particle:nth-child(3) { animation-delay: 0.6s; }
.profile-particle:nth-child(4) { animation-delay: 0.9s; }
.profile-particle:nth-child(5) { animation-delay: 1.2s; }
.profile-particle:nth-child(6) { animation-delay: 1.5s; }
.profile-particle:nth-child(7) { animation-delay: 1.8s; }
.profile-particle:nth-child(8) { animation-delay: 2.1s; }
.profile-particle:nth-child(9) { animation-delay: 2.4s; }
.profile-particle:nth-child(10) { animation-delay: 2.7s; }

.profile-icon {
  transition: all 0.5s ease;
}

.profile-active {
  transform: scale(1.2);
  filter: drop-shadow(0 0 10px rgba(255, 64, 129, 0.7));
}

.section-content {
  width: 85px;
  height: 85px;
  border-radius: 50%;
  background: rgba(30, 30, 45, 0.6);
  backdrop-filter: blur(5px);
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  cursor: pointer;
  border: 2px solid rgba(255, 255, 255, 0.1);
  box-shadow: 
    0 10px 20px rgba(0, 0, 0, 0.2),
    0 5px 15px rgba(0, 0, 0, 0.1),
    inset 0 0 10px rgba(255, 255, 255, 0.05);
  transform-style: preserve-3d;
  overflow: visible;
}

.section-content:active {
  transform: translateZ(5px) scale(0.95);
  transition: all 0.1s ease;
}

.section-content:active .icon {
  transform: translateZ(5px) scale(0.95);
  transition: all 0.1s ease;
}

.section-content:before {
  content: '';
  position: absolute;
  inset: -1px;
  border-radius: 50%;
  background: linear-gradient(45deg, transparent, transparent, rgba(255, 255, 255, 0.1), transparent, transparent);
  z-index: -1;
  animation: gradientRotate 10s linear infinite;
}

@keyframes gradientRotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.section-content.active {
  transform: translateZ(20px) rotateX(10deg);
  background: rgba(40, 40, 65, 0.8);
  box-shadow: 
    0 15px 25px rgba(0, 0, 0, 0.3),
    0 10px 10px rgba(0, 0, 0, 0.2),
    inset 0 0 15px rgba(255, 255, 255, 0.1);
}

.button-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.1);
  top: 0;
  left: 0;
  opacity: 0;
  pointer-events: none;
}

.formations .button-ring {
  border-color: rgba(79, 195, 247, 0.3);
}

.badges .button-ring {
  border-color: rgba(124, 77, 255, 0.3);
}

.games .button-ring {
  border-color: rgba(255, 64, 129, 0.3);
}

.profile .button-ring {
  border-color: rgba(29, 233, 182, 0.3);
}

.section-content:hover .button-ring {
  animation: ringExpand 1.5s infinite;
}

.section-content:hover {
  transform: translateZ(10px) rotateX(5deg) rotateY(5deg);
}

@keyframes ringExpand {
  0% {
    width: 100%;
    height: 100%;
    top: 0%;
    left: 0%;
    opacity: 0.7;
  }
  100% {
    width: 200%;
    height: 200%;
    top: -50%;
    left: -50%;
    opacity: 0;
  }
}

.icon-container {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.icon {
  color: white;
  z-index: 2;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  filter: drop-shadow(0 2px 5px rgba(0, 0, 0, 0.5));
  transform-style: preserve-3d;
}

.section-content:hover .icon {
  transform: translateZ(15px) scale(1.15);
  filter: drop-shadow(0 5px 10px rgba(0, 0, 0, 0.7)) brightness(1.2);
}

/* Thematic icon colors */
.formations .icon svg {
  fill: none;
  /* stroke: url(#formationsGradient); */
  filter: drop-shadow(0 0 5px rgba(79, 195, 247, 0.5));
}

.badges .icon svg {
  fill: none;
  /* stroke: url(#badgesGradient); */
  filter: drop-shadow(0 0 5px rgba(124, 77, 255, 0.5));
}

.games .icon svg {
  fill: none;
  /* stroke: url(#gamesGradient); */
  filter: drop-shadow(0 0 5px rgba(255, 64, 129, 0.5));
}

.profile .icon svg {
  fill: none;
  /* stroke: url(#profileGradient); */
  filter: drop-shadow(0 0 5px rgba(29, 233, 182, 0.5));
}

/* Effet de lueur amélioré */
.glow-effect {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    rgba(64, 196, 255, 0.3) 0%,
    rgba(124, 77, 255, 0.3) 50%,
    rgba(255, 64, 129, 0.3) 100%
  );
  filter: blur(8px);
  opacity: 0.6;
  transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  z-index: 1;
}

.formations .glow-effect {
  background: radial-gradient(circle, rgba(79, 195, 247, 0.3) 0%, rgba(79, 195, 247, 0) 70%);
  box-shadow: 0 0 20px rgba(79, 195, 247, 0.3);
}

.badges .glow-effect {
  background: radial-gradient(circle, rgba(124, 77, 255, 0.3) 0%, rgba(124, 77, 255, 0) 70%);
  box-shadow: 0 0 20px rgba(124, 77, 255, 0.3);
}

.games .glow-effect {
  background: radial-gradient(circle, rgba(255, 64, 129, 0.3) 0%, rgba(255, 64, 129, 0) 70%);
  box-shadow: 0 0 20px rgba(255, 64, 129, 0.3);
}

.profile .glow-effect {
  background: radial-gradient(circle, rgba(29, 233, 182, 0.3) 0%, rgba(29, 233, 182, 0) 70%);
  box-shadow: 0 0 20px rgba(29, 233, 182, 0.3);
}

.glow-effect.pulse {
  animation: pulsate 3s infinite;
  filter: blur(10px);
  opacity: 0.8;
  width: 110%;
  height: 110%;
}

@keyframes pulsate {
  0% { transform: scale(0.9); opacity: 0.6; filter: blur(8px); }
  50% { transform: scale(1.1); opacity: 0.8; filter: blur(10px); }
  100% { transform: scale(0.9); opacity: 0.6; filter: blur(8px); }
}

.formations .glow-effect.pulse {
  animation: formationsPulsate 3s infinite;
}

.badges .glow-effect.pulse {
  animation: badgesPulsate 3s infinite;
}

.games .glow-effect.pulse {
  animation: gamesPulsate 3s infinite;
}

.profile .glow-effect.pulse {
  animation: profilePulsate 3s infinite;
}

@keyframes formationsPulsate {
  0% { transform: scale(0.9); opacity: 0.6; box-shadow: 0 0 20px rgba(79, 195, 247, 0.3); }
  50% { transform: scale(1.2); opacity: 0.8; box-shadow: 0 0 30px rgba(79, 195, 247, 0.5); }
  100% { transform: scale(0.9); opacity: 0.6; box-shadow: 0 0 20px rgba(79, 195, 247, 0.3); }
}

@keyframes badgesPulsate {
  0% { transform: scale(0.9); opacity: 0.6; box-shadow: 0 0 20px rgba(124, 77, 255, 0.3); }
  50% { transform: scale(1.2); opacity: 0.8; box-shadow: 0 0 30px rgba(124, 77, 255, 0.5); }
  100% { transform: scale(0.9); opacity: 0.6; box-shadow: 0 0 20px rgba(124, 77, 255, 0.3); }
}

@keyframes gamesPulsate {
  0% { transform: scale(0.9); opacity: 0.6; box-shadow: 0 0 20px rgba(255, 64, 129, 0.3); }
  50% { transform: scale(1.2); opacity: 0.8; box-shadow: 0 0 30px rgba(255, 64, 129, 0.5); }
  100% { transform: scale(0.9); opacity: 0.6; box-shadow: 0 0 20px rgba(255, 64, 129, 0.3); }
}

@keyframes profilePulsate {
  0% { transform: scale(0.9); opacity: 0.6; box-shadow: 0 0 20px rgba(29, 233, 182, 0.3); }
  50% { transform: scale(1.2); opacity: 0.8; box-shadow: 0 0 30px rgba(29, 233, 182, 0.5); }
  100% { transform: scale(0.9); opacity: 0.6; box-shadow: 0 0 20px rgba(29, 233, 182, 0.3); }
}

/* Tooltip */
.tooltip {
  position: absolute;
  top: -40px;
  background: rgba(10, 10, 20, 0.9);
  color: white;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 14px;
  opacity: 0;
  pointer-events: none;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  white-space: nowrap;
  transform: translateY(10px);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  font-weight: 500;
  letter-spacing: 0.5px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  z-index: 100;
}

.formations .tooltip {
  border-bottom: 2px solid #4FC3F7;
}

.badges .tooltip {
  border-bottom: 2px solid #7C4DFF;
}

.games .tooltip {
  border-bottom: 2px solid #FF4081;
}

.profile .tooltip {
  border-bottom: 2px solid #1DE9B6;
}

.icon-container:hover .tooltip {
  opacity: 1;
  transform: translateY(0);
}

.button-particles {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.button-particle {
  position: absolute;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  opacity: 0;
  pointer-events: none;
}

.formations .button-particle {
  background: radial-gradient(circle, rgba(79, 195, 247, 1) 0%, rgba(79, 195, 247, 0) 70%);
  box-shadow: 0 0 10px rgba(79, 195, 247, 0.5);
}

.badges .button-particle {
  background: radial-gradient(circle, rgba(124, 77, 255, 1) 0%, rgba(124, 77, 255, 0) 70%);
  box-shadow: 0 0 10px rgba(124, 77, 255, 0.5);
}

.games .button-particle {
  background: radial-gradient(circle, rgba(255, 64, 129, 1) 0%, rgba(255, 64, 129, 0) 70%);
  box-shadow: 0 0 10px rgba(255, 64, 129, 0.5);
}

.profile .button-particle {
  background: radial-gradient(circle, rgba(29, 233, 182, 1) 0%, rgba(29, 233, 182, 0) 70%);
  box-shadow: 0 0 10px rgba(29, 233, 182, 0.5);
}

/* Notification */
.notification {
  position: absolute;
  top: -5px;
  right: -5px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 12px;
  font-weight: bold;
  z-index: 10;
  transform: scale(0);
  animation: notificationBounce 0.5s forwards;
}

.formations .notification {
  background: linear-gradient(135deg, #4FC3F7 0%, #29B6F6 100%);
  box-shadow: 0 0 15px rgba(79, 195, 247, 0.7);
}

.badges .notification {
  background: linear-gradient(135deg, #7C4DFF 0%, #651FFF 100%);
  box-shadow: 0 0 15px rgba(124, 77, 255, 0.7);
}

.games .notification {
  background: linear-gradient(135deg, #FF4081 0%, #F50057 100%);
  box-shadow: 0 0 15px rgba(255, 64, 129, 0.7);
}

.profile .notification {
  background: linear-gradient(135deg, #1DE9B6 0%, #00BFA5 100%);
  box-shadow: 0 0 15px rgba(29, 233, 182, 0.7);
}

@keyframes notificationBounce {
  0% { transform: scale(0); }
  50% { transform: scale(1.2); }
  80% { transform: scale(0.9); }
  100% { transform: scale(1); }
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
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
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
  animation: progressRingPulse 4s infinite;
}

@keyframes progressRingPulse {
  0% { stroke-width: 12; filter: drop-shadow(0 0 2px rgba(124, 77, 255, 0.3)); }
  50% { stroke-width: 14; filter: drop-shadow(0 0 8px rgba(124, 77, 255, 0.5)); }
  100% { stroke-width: 12; filter: drop-shadow(0 0 2px rgba(124, 77, 255, 0.3)); }
}

.progress-ring-circle-bg {
  stroke-dasharray: 754;
  stroke-dashoffset: 0;
}

.progress-ring-blur {
  stroke-dasharray: 754;
  stroke-dashoffset: 0;
  animation: blurPulse 4s infinite alternate;
  filter: blur(12px);
}

@keyframes blurPulse {
  0% { stroke-width: 15; filter: blur(10px); }
  100% { stroke-width: 20; filter: blur(15px); }
}

.avatar-image-container {
  position: relative;
  width: 200px;
  height: 200px;
  border-radius: 50%;
  overflow: hidden;
  background-color: #333;
  border: 5px solid rgba(255, 255, 255, 0.1);
  z-index: 2;
  transition: all 0.5s ease;
  box-shadow: 
    0 0 20px rgba(79, 195, 247, 0.3),
    0 0 40px rgba(124, 77, 255, 0.2),
    inset 0 0 15px rgba(255, 255, 255, 0.1);
}

.avatar-image-container:hover {
  transform: scale(1.05);
  box-shadow: 
    0 0 25px rgba(79, 195, 247, 0.5),
    0 0 50px rgba(124, 77, 255, 0.3),
    inset 0 0 20px rgba(255, 255, 255, 0.2);
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
  background: linear-gradient(to right, #4FC3F7, #7C4DFF);
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
  background: linear-gradient(to right, #7C4DFF, #FF4081);
}

.avatar-glow {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    rgba(64, 196, 255, 0.4) 0%,
    rgba(124, 77, 255, 0.4) 50%,
    rgba(255, 64, 129, 0.4) 100%
  );
  filter: blur(15px);
  opacity: 0.5;
  z-index: 1;
  transition: all 0.5s ease;
  animation: slowRotate 8s linear infinite;
}

@keyframes slowRotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.avatar-glow.pulse {
  animation: avatarGlowPulse 1s;
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
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3),
              0 0 15px rgba(79, 195, 247, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
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
  background: linear-gradient(135deg, rgba(30, 30, 45, 0.9) 0%, rgba(30, 30, 60, 0.9) 100%);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 20px;
  z-index: 100;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5),
              0 0 15px rgba(124, 77, 255, 0.4);
  animation: enhancedDropDown 0.7s, enhancedFadeOut 0.7s 2.3s;
  border: 1px solid rgba(255, 255, 255, 0.1);
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
  0% { text-shadow: 0 0 10px rgba(255, 215, 0, 0.7); }
  50% { text-shadow: 0 0 20px rgba(255, 215, 0, 1); }
  100% { text-shadow: 0 0 10px rgba(255, 215, 0, 0.7); }
}

.achievement-text h3 {
  margin: 0 0 8px 0;
  color: #FFD700;
  font-size: 18px;
  letter-spacing: 0.5px;
}

.achievement-text p {
  margin: 0;
  font-size: 16px;
  color: #ffffff;
}

/* Modal pour les sections */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: enhancedFadeIn 0.4s;
  backdrop-filter: blur(5px);
}

@keyframes enhancedFadeIn {
  from { 
    opacity: 0;
    backdrop-filter: blur(0);
  }
  to { 
    opacity: 1;
    backdrop-filter: blur(5px);
  }
}

.modal-content {
  background: linear-gradient(135deg, #1E1E2E 0%, #252540 100%);
  border-radius: 16px;
  width: 80%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
  animation: enhancedScaleIn 0.5s;
  padding: 25px;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3),
              0 0 20px rgba(124, 77, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

@keyframes enhancedScaleIn {
  0% { 
    transform: scale(0.8);
    opacity: 0;
    filter: blur(10px);
  }
  100% { 
    transform: scale(1);
    opacity: 1;
    filter: blur(0);
  }
}

.close-button {
  position: absolute;
  top: 15px;
  right: 15px;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.3s ease;
  line-height: 1;
}

.close-button:hover {
  background: rgba(255, 64, 129, 0.3);
  transform: rotate(90deg);
}

.modal-content h2 {
  margin-top: 0;
  color: #4FC3F7;
  border-bottom: 2px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 15px;
  font-size: 24px;
  letter-spacing: 1px;
}

.modal-body {
  padding: 15px 0;
}

/* Adaptations pour les écrans plus petits */
@media (max-width: 768px) {
  .formations { top: 10%; left: 10%; }
  .badges { top: 10%; right: 10%; }
  .games { bottom: 10%; left: 10%; }
  .profile { bottom: 10%; right: 10%; }
  
  .avatar-container {
    width: 200px;
    height: 200px;
  }
  
  .progress-ring-container {
    width: 220px;
    height: 220px;
  }
  
  .avatar-image-container {
    width: 160px;
    height: 160px;
  }
  
  .section-content {
    width: 60px;
    height: 60px;
  }
}
</style>