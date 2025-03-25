<template>
  <div class="dashboard" :class="{ 'achievements-unlocked': hasNewAchievement, 'games-zoomed': gamesZoomed }">
    <div class="space-elements">
      
      <!-- Add comets randomly crossing the sky -->
      <div class="comet comet-1"></div>
      <div class="comet comet-2"></div>
      <div class="comet comet-3"></div>
      <div class="comet comet-4"></div>
      <div class="comet comet-5"></div>
      
      <!-- Add a distant galaxy -->
      <div class="galaxy galaxy-1"></div>
      
      <!-- Add a planet with rings -->
      <div class="planet planet-1">
        <div class="planet-rings"></div>
      </div>
      
      <!-- Nouvelle planète rouge gazeuse -->
      <div class="planet planet-2">
        <div class="planet-atmosphere"></div>
        <div class="planet-storm"></div>
      </div>
      
      <!-- Nouvelle planète glacée -->
      <div class="planet planet-3">
        <div class="planet-ice-caps"></div>
        <div class="planet-moons">
          <div class="planet-moon moon-1"></div>
          <div class="planet-moon moon-2"></div>
        </div>
      </div>
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
      <div class="section games" 
           @mouseenter="!gamesZoomed && (activeSection = 'games')" 
           @mouseleave="!gamesZoomed && (activeSection = null)"
           :class="{ 'zoomed': gamesZoomed }">
        <div class="section-content" :class="{ 'active': activeSection === 'games' }">
          <div class="button-particles" v-if="activeSection === 'games' && !gamesZoomed">
            <div v-for="i in 8" :key="'game-particle-'+i" class="button-particle" 
                :style="generateParticleStyle()"></div>
          </div>
          <div class="button-ring"></div>
          <div class="icon-container" @click="handleGamesClick">
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
        
        <!-- Games Zoom View -->
        <div class="games-zoom-container" v-if="gamesZoomed">
          <div class="game-buttons-grid">
            <!-- Example game buttons - you can add more or customize -->
            <div class="game-button" v-for="(game, index) in gamesList" :key="index" @click="selectGame(game)">
              <div class="game-icon">
                <div class="game-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="32" height="32" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <g v-html="game.icon"></g>
                  </svg>
                </div>
              </div>
              <span class="game-name">{{ game.name }}</span>
            </div>
          </div>
          
          <!-- Back button -->
          <div class="back-button" @click="exitGamesZoom">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor">
              <path d="M19 12H5M12 19l-7-7 7-7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>Retour</span>
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
      progress: 37, // Progression globale en pourcentage
      activeSection: null,
      avatarAnimating: false,
      showAvatarInteraction: false,
      activeModal: null,
      showAchievement: false,
      hasNewAchievement: false,
      currentAchievement: '',
      gamesZoomed: false,
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
      ],
      gamesList: [
        { 
          name: 'Quiz Spatial', 
          icon: '<path d="M9 22h6a5 5 0 1 0 0-10H9A5 5 0 0 1 9 2H3"></path><path d="M9 13h6"></path>' 
        },
        { 
          name: 'Puzzle Galactique', 
          icon: '<path d="M21 16V8a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2z"></path><path d="M14 2v2M10 2v2M14 20v2M10 20v2M6 10h12M6 14h12"></path>' 
        },
        { 
          name: 'Astéroïdes', 
          icon: '<circle cx="12" cy="12" r="10"></circle><path d="M8 12a4 4 0 1 0 8 0"></path><circle cx="12" cy="8" r="1"></circle>' 
        },
        { 
          name: 'Explorateur', 
          icon: '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 1 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle>' 
        },
        { 
          name: 'Défis Cosmiques', 
          icon: '<path d="M5 3v18M19 9v12M14 4v17M9 4v17"></path>' 
        },
        { 
          name: 'Mémoire Stellaire', 
          icon: '<path d="M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M3 9v10a2 2 0 0 0 2 2h4m-6-12h18M9 21h10a2 2 0 0 0 2-2V9"></path>' 
        }
      ]
    };
  },
  methods: {
    handleGamesClick() {
      if (!this.gamesZoomed) {
        this.enterGamesZoom();
      } else {
        this.exitGamesZoom();
      }
    },

    enterGamesZoom() {
      // Create a button flash effect
      this.createButtonFlash('games');
      
      // Add haptic feedback if available
      if (window.navigator && window.navigator.vibrate) {
        window.navigator.vibrate(50);
      }
      
      // Set zoomed state
      this.gamesZoomed = true;
      this.activeSection = null;
      
      // Réduire la notification
      if (this.notifications.games > 0) {
        this.notifications.games--;
      }
    },

        // Exit games zoom mode
    exitGamesZoom() {
      this.gamesZoomed = false;
      
      // Add haptic feedback if available
      if (window.navigator && window.navigator.vibrate) {
        window.navigator.vibrate([30, 20, 30]);
      }
    },

    selectGame(game) {
      // Here you would navigate to the specific game
      console.log(`Selected game: ${game.name}`);
      // You could trigger an achievement or other feedback
      this.triggerAchievement('Premier pas dans les jeux');
    },
    
    // Keep all existing methods
    calculateProgressOffset() {
      const circumference = 2 * Math.PI * 120;
      return circumference - (circumference * this.progress) / 100;
    },
    
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
      // Don't open a modal if we're in games zoom mode and it's games section
      if (section === 'games' && this.gamesZoomed) {
        return;
      }
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
  color: white;
  overflow: hidden;
  font-family: 'Nunito', sans-serif;
  transition: background-color 0.5s ease;
  background: radial-gradient(ellipse at center, #0f2027 0%, #090a0f 100%);
}

.dashboard::before,
.dashboard::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
  display: block;
  background-position: 0 0;
  background-repeat: repeat;
  z-index: 0;
}

.dashboard::before {
  background-image: 
    /* Original stars */
    radial-gradient(1px 1px at 10% 30%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
    radial-gradient(1px 1px at 20% 70%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    radial-gradient(1px 1px at 30% 40%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
    radial-gradient(1px 1px at 40% 80%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
    radial-gradient(1px 1px at 50% 20%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    radial-gradient(1px 1px at 60% 60%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
    radial-gradient(1px 1px at 70% 10%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
    radial-gradient(1px 1px at 80% 50%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    radial-gradient(1px 1px at 90% 90%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
    
    /* Additional small stars - first layer */
    radial-gradient(1px 1px at 5% 5%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    radial-gradient(1px 1px at 15% 15%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
    radial-gradient(1px 1px at 25% 25%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
    radial-gradient(1px 1px at 35% 35%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    radial-gradient(1px 1px at 45% 45%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
    radial-gradient(1px 1px at 55% 55%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
    radial-gradient(1px 1px at 65% 65%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    radial-gradient(1px 1px at 75% 75%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
    radial-gradient(1px 1px at 85% 85%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
    radial-gradient(1px 1px at 95% 95%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    
    /* Additional small stars - second layer */
    radial-gradient(1px 1px at 7% 92%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    radial-gradient(1px 1px at 12% 82%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
    radial-gradient(1px 1px at 22% 72%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
    radial-gradient(1px 1px at 32% 62%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    radial-gradient(1px 1px at 42% 52%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
    radial-gradient(1px 1px at 52% 42%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
    radial-gradient(1px 1px at 62% 32%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    radial-gradient(1px 1px at 72% 22%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
    radial-gradient(1px 1px at 82% 12%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
    radial-gradient(1px 1px at 92% 7%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    
    /* Additional small stars - third layer */
    radial-gradient(1px 1px at 3% 47%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    radial-gradient(1px 1px at 13% 58%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
    radial-gradient(1px 1px at 23% 36%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
    radial-gradient(1px 1px at 33% 94%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    radial-gradient(1px 1px at 43% 18%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
    radial-gradient(1px 1px at 53% 76%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
    radial-gradient(1px 1px at 63% 27%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    radial-gradient(1px 1px at 73% 83%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
    radial-gradient(1px 1px at 83% 44%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
    radial-gradient(1px 1px at 93% 68%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    
    /* Additional small stars - fourth layer */
    radial-gradient(1px 1px at 8% 38%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
    radial-gradient(1px 1px at 18% 26%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
    radial-gradient(1px 1px at 28% 88%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    radial-gradient(1px 1px at 38% 16%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
    radial-gradient(1px 1px at 48% 64%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
    radial-gradient(1px 1px at 58% 39%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    radial-gradient(1px 1px at 68% 77%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
    radial-gradient(1px 1px at 78% 22%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
    radial-gradient(1px 1px at 88% 63%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    radial-gradient(1px 1px at 98% 33%, rgba(255, 255, 255, 0.7) 50%, transparent 100%);
  background-size: 400% 400%;
  animation: starsFloat 300s linear infinite;
}

.dashboard::after {
  background-image: 
    /* Original larger stars */
    radial-gradient(2px 2px at 15% 25%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    radial-gradient(2px 2px at 35% 65%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
    radial-gradient(2px 2px at 45% 35%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
    radial-gradient(2px 2px at 55% 75%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    radial-gradient(2px 2px at 65% 15%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
    radial-gradient(2px 2px at 75% 55%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
    radial-gradient(2px 2px at 85% 85%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    
    /* Additional medium stars - first layer */
    radial-gradient(2px 2px at 5% 45%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
    radial-gradient(2px 2px at 10% 85%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
    radial-gradient(2px 2px at 20% 5%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    radial-gradient(2px 2px at 25% 50%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
    radial-gradient(2px 2px at 30% 95%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
    radial-gradient(2px 2px at 40% 10%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    radial-gradient(2px 2px at 50% 60%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
    radial-gradient(2px 2px at 60% 5%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
    radial-gradient(2px 2px at 70% 30%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    radial-gradient(2px 2px at 80% 70%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
    radial-gradient(2px 2px at 90% 10%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
    radial-gradient(2px 2px at 95% 40%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    
    /* Some colorful stars - adding variety with blue and gold tints */
    radial-gradient(2.5px 2.5px at 7% 75%, rgba(173, 216, 250, 0.9) 50%, transparent 100%),
    radial-gradient(2.5px 2.5px at 37% 5%, rgba(173, 216, 250, 0.7) 50%, transparent 100%),
    radial-gradient(2.5px 2.5px at 67% 45%, rgba(173, 216, 250, 0.8) 50%, transparent 100%),
    radial-gradient(2.5px 2.5px at 87% 30%, rgba(173, 216, 250, 0.9) 50%, transparent 100%),
    
    radial-gradient(2.5px 2.5px at 22% 35%, rgba(255, 223, 186, 0.8) 50%, transparent 100%),
    radial-gradient(2.5px 2.5px at 52% 85%, rgba(255, 223, 186, 0.7) 50%, transparent 100%),
    radial-gradient(2.5px 2.5px at 82% 25%, rgba(255, 223, 186, 0.9) 50%, transparent 100%),
    
    /* A few bright stars (slightly larger) */
    radial-gradient(3px 3px at 17% 17%, rgba(255, 255, 255, 1) 50%, transparent 100%),
    radial-gradient(3px 3px at 47% 47%, rgba(255, 255, 255, 1) 50%, transparent 100%),
    radial-gradient(3px 3px at 77% 77%, rgba(255, 255, 255, 1) 50%, transparent 100%),
    radial-gradient(3px 3px at 33% 66%, rgba(255, 255, 255, 1) 50%, transparent 100%),
    radial-gradient(3px 3px at 66% 33%, rgba(255, 255, 255, 1) 50%, transparent 100%);
  background-size: 200% 200%;
  animation: starsFloat 200s linear infinite, starsTwinkle 10s ease-in-out infinite alternate;
}

.dashboard-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 30% 40%, rgba(76, 0, 153, 0.2) 0%, rgba(76, 0, 153, 0) 50%),
    radial-gradient(circle at 70% 60%, rgba(63, 0, 113, 0.2) 0%, rgba(63, 0, 113, 0) 60%),
    radial-gradient(circle at 50% 50%, rgba(0, 51, 102, 0.2) 0%, rgba(0, 51, 102, 0) 70%);
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
  justify-content: center;
  align-items: center;
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

/* Styles pour les comètes */
.comet {
  position: absolute;
  width: 4px;
  height: 4px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  box-shadow: 
    0 0 20px 2px rgba(255, 255, 255, 0.6),
    0 0 40px 6px rgba(115, 215, 255, 0.4);
  z-index: 2;
  opacity: 0;
  animation: cometAnimation 12s linear infinite;
}

.comet::after {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 120px;
  height: 2px;
  background: linear-gradient(to left, 
    rgba(255, 255, 255, 0.8), 
    rgba(160, 220, 255, 0.4), 
    transparent);
  transform: translateX(2px);
  border-radius: 100%;
}

.comet-1 {
  top: 15%;
  left: -5%;
  animation-delay: 2s;
}

/* Ajoutons plus de comètes */
.comet-2 {
  top: 35%;
  left: -10%;
  width: 3px;
  height: 3px;
  animation-delay: 7s;
  animation-duration: 15s;
}

.comet-3 {
  top: 65%;
  left: -8%;
  width: 5px;
  height: 5px;
  animation-delay: 13s;
  animation-duration: 18s;
}

.comet-4 {
  top: 62%;
  left: -18%;
  animation-delay: 11s;
}

.comet-5 {
  top: 70%;
  left: -18%;
  animation-delay: 4s;
}

/* Animation pour les comètes */
@keyframes cometAnimation {
  0% {
    transform: translate(0, 0) rotate(15deg);
    opacity: 0;
  }
  5% {
    opacity: 1;
  }
  95% {
    opacity: 1;
  }
  100% {
    transform: translate(calc(100vw + 200px), 20vh) rotate(15deg);
    opacity: 0;
  }
}

/* Styles pour la galaxie */
.galaxy {
  position: absolute;
  width: 180px;
  height: 100px;
  top: 75%;
  left: 35%;
  background: radial-gradient(
    ellipse at center,
    rgba(220, 180, 255, 0.6) 0%,
    rgba(140, 100, 255, 0.4) 30%,
    rgba(70, 30, 180, 0.2) 60%,
    transparent 100%
  );
  border-radius: 50%;
  transform: rotate(-25deg) scale(1);
  filter: blur(5px);
  opacity: 0.7;
  z-index: 1;
  animation: galaxyPulse 15s ease-in-out infinite alternate;
}

.galaxy::before, .galaxy::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 50%;
  background: 
    radial-gradient(
      ellipse at center,
      rgba(255, 255, 255, 0.1) 0%,
      transparent 60%
    ),
    conic-gradient(
      transparent 0%,
      rgba(130, 90, 220, 0.1) 25%,
      transparent 50%,
      rgba(150, 100, 255, 0.1) 75%,
      transparent 100%
    );
  transform-origin: center;
  animation: galaxyRotate 80s linear infinite;
}

.galaxy::after {
  transform: rotate(180deg);
  filter: blur(8px);
  opacity: 0.5;
  animation-duration: 120s;
  animation-direction: reverse;
}

@keyframes galaxyPulse {
  0% {
    transform: rotate(-25deg) scale(1);
    opacity: 0.7;
  }
  50% {
    transform: rotate(-25deg) scale(1.05);
    opacity: 0.8;
  }
  100% {
    transform: rotate(-25deg) scale(1);
    opacity: 0.7;
  }
}

@keyframes galaxyRotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Styles pour la planète */

.planet-1 {
  position: absolute;
  width: 80px;
  height: 80px;
  top: 15%;
  right: 37%;
  background: 
    radial-gradient(
      circle at 30% 30%,
      #7a4dbc 0%,
      #522b99 30%,
      #3c1777 60%,
      #2c1155 100%
    );
  border-radius: 50%;
  box-shadow: 
    inset -15px -15px 40px rgba(0, 0, 0, 0.5),
    0 0 20px rgba(120, 70, 230, 0.3);
  z-index: 3;
  transform: rotate(-15deg);
  animation: planetFloat 120s linear infinite;
}

/* Anneaux pour la planète violette */
.planet-1 .planet-rings {
  position: absolute;
  width: 130px;
  height: 20px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) rotate(-15deg);
  border-radius: 50%;
  box-shadow: 
    0 0 0 4px rgba(255, 255, 255, 0.05),
    0 0 0 8px rgba(255, 255, 255, 0.03),
    0 0 0 12px rgba(255, 220, 255, 0.05),
    0 0 0 16px rgba(180, 180, 255, 0.08),
    0 0 0 20px rgba(140, 140, 230, 0.06),
    0 0 0 24px rgba(100, 100, 200, 0.04),
    0 0 0 28px rgba(80, 80, 180, 0.02);
  z-index: 2;
  animation: ringsRotate 200s linear infinite;
}

/* Styles pour la nouvelle planète rouge gazeuse */
.planet-2 {
  position: absolute;
  width: 100px;
  height: 100px;
  top: 65%;
  right: 5%;
  background: 
    radial-gradient(
      circle at 40% 40%,
      #ff6b5b 0%,
      #d32f2f 30%,
      #b71c1c 60%,
      #7f0000 100%
    );
  border-radius: 50%;
  box-shadow: 
    inset -20px -20px 60px rgba(0, 0, 0, 0.6),
    0 0 30px rgba(255, 100, 80, 0.4);
  z-index: 2;
  transform: rotate(10deg);
  animation: planetFloat2 150s linear infinite;
}

/* Atmosphère pour la planète rouge */
.planet-2 .planet-atmosphere {
  position: absolute;
  width: 110%;
  height: 110%;
  top: -5%;
  left: -5%;
  border-radius: 50%;
  background: 
    radial-gradient(
      circle at 50% 50%,
      rgba(255, 107, 91, 0.3) 0%,
      rgba(211, 47, 47, 0.2) 50%,
      rgba(183, 28, 28, 0.1) 70%,
      rgba(127, 0, 0, 0) 100%
    );
  filter: blur(10px);
  opacity: 0.8;
  z-index: 1;
  animation: atmospherePulse 8s ease-in-out infinite alternate;
}

/* Tempête sur la planète rouge */
.planet-2 .planet-storm {
  position: absolute;
  width: 40%;
  height: 40%;
  top: 30%;
  left: 20%;
  border-radius: 50%;
  background: rgba(255, 160, 140, 0.4);
  filter: blur(5px);
  z-index: 2;
  animation: stormSpin 30s linear infinite;
}

/* Styles pour la nouvelle planète glacée */
.planet-3 {
  position: absolute;
  width: 70px;
  height: 70px;
  top: 15%;
  left: 15%;
  background: 
    radial-gradient(
      circle at 50% 50%,
      #b3e5fc 0%,
      #81d4fa 30%,
      #4fc3f7 60%,
      #29b6f6 100%
    );
  border-radius: 50%;
  box-shadow: 
    inset -10px -10px 30px rgba(0, 0, 0, 0.3),
    0 0 25px rgba(79, 195, 247, 0.5);
  z-index: 2;
  animation: planetFloat3 180s linear infinite;
}

/* Calottes polaires de la planète glacée */
.planet-3 .planet-ice-caps {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  border-radius: 50%;
  background: 
    radial-gradient(
      ellipse at 50% 10%,
      rgba(255, 255, 255, 0.9) 0%,
      rgba(255, 255, 255, 0) 50%
    ),
    radial-gradient(
      ellipse at 50% 90%,
      rgba(255, 255, 255, 0.9) 0%,
      rgba(255, 255, 255, 0) 50%
    );
  z-index: 3;
}

/* Système de lunes pour la planète glacée */
.planet-3 .planet-moons {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 1;
  animation: moonsOrbit 60s linear infinite;
}

/* Lunes individuelles */
.planet-moon {
  position: absolute;
  background: #e0e0e0;
  border-radius: 50%;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

.moon-1 {
  width: 15px;
  height: 15px;
  top: -30px;
  left: 50%;
  transform: translateX(-50%);
  background: 
    radial-gradient(
      circle at 30% 30%,
      #f5f5f5 0%,
      #e0e0e0 50%,
      #bdbdbd 100%
    );
}

.moon-2 {
  width: 10px;
  height: 10px;
  bottom: -25px;
  left: 30%;
  background: 
    radial-gradient(
      circle at 30% 30%,
      #e0e0e0 0%,
      #bdbdbd 50%,
      #9e9e9e 100%
    );
}

/* Ajouter des détails à la planète */
.planet::after {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  border-radius: 50%;
  background: 
    radial-gradient(
      circle at 70% 70%, 
      transparent 0%, 
      rgba(0, 0, 0, 0.4) 100%
    ),
    repeating-conic-gradient(
      rgba(255, 255, 255, 0.03) 0deg,
      rgba(255, 255, 255, 0) 20deg,
      rgba(255, 255, 255, 0.03) 40deg
    );
  opacity: 0.7;
  animation: planetRotate 80s linear infinite;
}

/* Styles pour les anneaux de la planète */
.planet-rings {
  position: absolute;
  width: 130px;
  height: 20px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) rotate(-15deg);
  border-radius: 50%;
  box-shadow: 
    0 0 0 4px rgba(255, 255, 255, 0.05),
    0 0 0 8px rgba(255, 255, 255, 0.03),
    0 0 0 12px rgba(255, 220, 255, 0.05),
    0 0 0 16px rgba(180, 180, 255, 0.08),
    0 0 0 20px rgba(140, 140, 230, 0.06),
    0 0 0 24px rgba(100, 100, 200, 0.04),
    0 0 0 28px rgba(80, 80, 180, 0.02);
  z-index: 2;
  animation: ringsRotate 200s linear infinite;
}

.planet-rings::before {
  content: '';
  position: absolute;
  width: 130px;
  height: 20px;
  top: 0;
  left: 0;
  border-radius: 50%;
  background: linear-gradient(
    to right,
    transparent 0%,
    rgba(200, 180, 255, 0.2) 30%,
    rgba(220, 200, 255, 0.3) 50%,
    rgba(200, 180, 255, 0.2) 70%,
    transparent 100%
  );
  filter: blur(2px);
}

@keyframes planetFloat {
  0% {
    transform: translate(0, 0) rotate(-15deg);
  }
  25% {
    transform: translate(-10px, 15px) rotate(-15deg);
  }
  50% {
    transform: translate(-5px, 25px) rotate(-15deg);
  }
  75% {
    transform: translate(5px, 15px) rotate(-15deg);
  }
  100% {
    transform: translate(0, 0) rotate(-15deg);
  }
}

@keyframes planetRotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes ringsRotate {
  0% {
    transform: translate(-50%, -50%) rotate(-15deg);
  }
  100% {
    transform: translate(-50%, -50%) rotate(345deg);
  }
}

@keyframes planetFloat2 {
  0% { transform: translate(0, 0) rotate(10deg); }
  25% { transform: translate(-30px, 20px) rotate(10deg); }
  50% { transform: translate(-60px, 0) rotate(10deg); }
  75% { transform: translate(-30px, -20px) rotate(10deg); }
  100% { transform: translate(0, 0) rotate(10deg); }
}

@keyframes planetFloat3 {
  0% { transform: translate(0, 0); }
  25% { transform: translate(20px, 15px); }
  50% { transform: translate(40px, 0); }
  75% { transform: translate(20px, -15px); }
  100% { transform: translate(0, 0); }
}

@keyframes atmospherePulse {
  0% { opacity: 0.6; transform: scale(1); }
  100% { opacity: 0.9; transform: scale(1.1); }
}

@keyframes stormSpin {
  0% { transform: rotate(0deg) translateX(10px) rotate(0deg); }
  100% { transform: rotate(360deg) translateX(10px) rotate(-360deg); }
}

@keyframes moonsOrbit {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Games Zoom Styling */
.games-zoomed .section.games {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1000;
  transform: scale(1);
  transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  background: radial-gradient(ellipse at center, rgba(30, 30, 45, 0.95) 0%, rgba(15, 15, 25, 0.98) 70%);
  backdrop-filter: blur(10px);
}

.games-zoomed .dashboard-container > *:not(.games) {
  opacity: 0;
  pointer-events: none;
  transition: all 0.5s ease;
}

.games-zoomed .section.games .section-content {
  position: absolute;
  top: 20px;
  left: 20px;
  transform: scale(0.8);
  transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  z-index: 10;
}

.games-zoom-container {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.game-buttons-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
  max-width: 800px;
  padding: 20px;
}

.game-button {
  width: 130px;
  height: 130px;
  background: rgba(40, 40, 65, 0.6);
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 2px solid rgba(255, 255, 255, 0.1);
  box-shadow: 
    0 10px 20px rgba(0, 0, 0, 0.2),
    inset 0 0 15px rgba(255, 255, 255, 0.05);
  position: relative;
  overflow: hidden;
}

.game-button:before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, 
    rgba(255, 64, 129, 0.1) 0%, 
    rgba(255, 64, 129, 0) 50%, 
    rgba(255, 64, 129, 0.1) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.game-button:hover {
  transform: translateY(-10px) scale(1.05);
  border-color: rgba(255, 64, 129, 0.3);
  box-shadow: 
    0 15px 25px rgba(0, 0, 0, 0.3),
    0 5px 15px rgba(255, 64, 129, 0.2),
    inset 0 0 20px rgba(255, 255, 255, 0.1);
}

.game-button:hover:before {
  opacity: 1;
}

.game-button:active {
  transform: translateY(-5px) scale(0.95);
}

.game-icon {
  width: 60px;
  height: 60px;
  background: rgba(255, 64, 129, 0.2);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 15px;
  color: #FF4081;
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(255, 64, 129, 0.3);
}

.game-button:hover .game-icon {
  background: rgba(255, 64, 129, 0.3);
  transform: scale(1.1);
  box-shadow: 0 5px 20px rgba(255, 64, 129, 0.5);
}

.game-name {
  font-size: 14px;
  font-weight: 600;
  color: white;
  text-align: center;
  transition: all 0.3s ease;
}

.game-button:hover .game-name {
  color: #FF4081;
}

.back-button {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(30, 30, 45, 0.8);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 30px;
  padding: 12px 25px;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 
    0 5px 15px rgba(0, 0, 0, 0.2),
    inset 0 0 10px rgba(255, 255, 255, 0.05);
}

.back-button:hover {
  background: rgba(40, 40, 65, 0.9);
  transform: translateX(-50%) translateY(-5px);
  box-shadow: 
    0 8px 20px rgba(0, 0, 0, 0.3),
    inset 0 0 15px rgba(255, 255, 255, 0.1);
}

.back-button:active {
  transform: translateX(-50%) translateY(-2px);
}

.back-button svg {
  color: #FF4081;
  transition: all 0.3s ease;
}

.back-button:hover svg {
  transform: translateX(-3px);
}

.back-button span {
  font-size: 16px;
  font-weight: 600;
  color: white;
  transition: all 0.3s ease;
}

.back-button:hover span {
  color: #FF4081;
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
  background: radial-gradient(circle, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0) 70%) !important;
  border-radius: 50%;
  animation: floatDust infinite;
  box-shadow: 0 0 6px 2px rgba(111, 168, 220, 0.2);
}

.particle:nth-child(3n) {
  background: radial-gradient(circle, rgba(168, 111, 220, 0.9) 0%, rgba(168, 111, 220, 0) 70%) !important;
  box-shadow: 0 0 8px 2px rgba(168, 111, 220, 0.3);
}

.particle:nth-child(3n+1) {
  background: radial-gradient(circle, rgba(111, 168, 220, 0.9) 0%, rgba(111, 168, 220, 0) 70%) !important;
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
  background: radial-gradient(circle, rgba(111, 168, 220, 0.5) 0%, rgba(111, 168, 220, 0) 70%);
  box-shadow: 0 0 20px rgba(111, 168, 220, 0.5);
}

.badges .glow-effect {
  background: radial-gradient(circle, rgba(168, 111, 220, 0.5) 0%, rgba(168, 111, 220, 0) 70%);
  box-shadow: 0 0 20px rgba(168, 111, 220, 0.5);
}

.games .glow-effect {
  background: radial-gradient(circle, rgba(220, 111, 168, 0.5) 0%, rgba(220, 111, 168, 0) 70%);
  box-shadow: 0 0 20px rgba(220, 111, 168, 0.5);
}

.profile .glow-effect {
  background: radial-gradient(circle, rgba(111, 220, 168, 0.5) 0%, rgba(111, 220, 168, 0) 70%);
  box-shadow: 0 0 20px rgba(111, 220, 168, 0.5);
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

/* Add cosmic pulse to avatar when active */
.avatar-glow.pulse {
  animation: cosmicPulse 1s;
}

/* Animation keyframes */
@keyframes starsFloat {
  0% { background-position: 0% 0%; }
  100% { background-position: 100% 100%; }
}

@keyframes starsTwinkle {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 1; }
}

@keyframes nebulaShift {
  0% { transform: scale(1) rotate(0deg); }
  50% { transform: scale(1.2) rotate(5deg); }
  100% { transform: scale(1) rotate(10deg); }
}

@keyframes planetFloat {
  0% { transform: translate(0, 0); }
  25% { transform: translate(50px, 20px); }
  50% { transform: translate(100px, 0); }
  75% { transform: translate(50px, -20px); }
  100% { transform: translate(0, 0); }
}

@keyframes cometPath {
  0% { transform: translate(0, 0) rotate(15deg); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translate(120vw, 40vh) rotate(15deg); opacity: 0; }
}

@keyframes floatDust {
  0% {
    transform: translateY(0) translateX(0) rotate(0deg);
    opacity: 0;
  }
  10% { opacity: 0.7; }
  90% { opacity: 0.3; }
  100% {
    transform: translateY(-100px) translateX(50px) rotate(360deg);
    opacity: 0;
  }
}

@keyframes cosmicRotate {
  0% { transform: rotate(0deg) scale(1); }
  25% { transform: rotate(90deg) scale(1.05); }
  50% { transform: rotate(180deg) scale(1); }
  75% { transform: rotate(270deg) scale(1.05); }
  100% { transform: rotate(360deg) scale(1); }
}

@keyframes cosmicPulse {
  0% { 
    transform: scale(0.95);
    opacity: 0.5;
    filter: blur(15px);
  }
  50% { 
    transform: scale(1.4);
    opacity: 0.9;
    filter: blur(25px);
  }
  100% { 
    transform: scale(1);
    opacity: 0.7;
    filter: blur(20px);
  }
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
  0% { text-shadow: 0 0 10px rgba(255, 215, 0, 0.7); }
  50% { text-shadow: 0 0 20px rgba(255, 215, 0, 1); }
  100% { text-shadow: 0 0 10px rgba(255, 215, 0, 0.7); }
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
  background: linear-gradient(135deg, #0f1b2a 0%, #1a1a40 100%);
  border: 1px solid rgba(111, 168, 220, 0.2);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.5),
              0 0 20px rgba(111, 168, 220, 0.3);
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

  .game-buttons-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
  
  .game-button {
    width: 110px;
    height: 110px;
  }
  
  .game-icon {
    width: 50px;
    height: 50px;
  }
  
  .game-name {
    font-size: 12px;
  }
}
</style>