<template>
  <div class="dashboard" :class="{ 'achievements-unlocked': hasNewAchievement, 'games-zoomed': gamesZoomed }">
    <space-background :theme="currentTheme" />
    <!-- La structure principale -->
    <div class="dashboard-container">
      <div class="click-outside-overlay" v-if="gamesZoomed" @click="exitGamesZoom"></div>
      <!-- Section Formations -->
      <div class="section formations" @mouseenter="activeSection = 'formations'" @mouseleave="activeSection = null">
        <div class="section-content" ref="formationsContent" :class="{ 'active': activeSection === 'formations' }">
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
				<div class="section-content" ref="badgesContent" :class="{ 'active': activeSection === 'badges' }">
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
        <div class="section-content" ref="gamesContent" :class="{ 'active': activeSection === 'games' }">
          <div class="button-particles" v-if="activeSection === 'games'">
            <div v-for="i in 8" :key="'game-particle-'+i" class="button-particle" 
              :style="generateParticleStyle()"></div>
          </div>
          <div class="button-ring"></div>
          <div class="icon-container" @click="toggleGamesOrbit">
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

        <!-- Games Orbit Buttons -->
        <div class="game-orbit" v-if="showGamesOrbit">
          <div v-for="(game, index) in gamesList" :key="game.id"
              class="game-orbit-button"
              :class="{'game-orbit-appear': showGamesOrbit}"
              :style="calculateOrbitPosition(index, gamesList.length)">
            <div class="game-orbit-content" @click.stop="selectGame(game)">
              <div class="game-icon">
                <i :class="game.icon"></i>
              </div>
              <div class="game-title">{{ game.title }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Section Profil - Plus Immersive! -->
      <div class="section profile" @mouseenter="activeSection = 'profile'" @mouseleave="activeSection = null" :class="{ 'profile-highlight': activeSection === 'profile' }">
        <div class="section-content" ref="profileContent" :class="{ 'active': activeSection === 'profile' }">
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
            <span class="tooltip">Profil</span>
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
      <div class="theme-selector">
        <div class="theme-option" 
             v-for="theme in availableThemes" 
             :key="theme.value"
             @click="changeTheme(theme.value)"
             :class="{ 'active': currentTheme === theme.value }">
          <div class="theme-icon" :class="theme.value"></div>
          <span>{{ theme.label }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SpaceBackground from '@/components/SpaceBackground.vue';

export default {
  name: 'ImmersiveDashboard',
  components: {
    SpaceBackground
  },
  data() {
    return {
      currentTheme: 'cosmic',
      availableThemes: [
        { value: 'cosmic', label: 'Cosmic' },
        { value: 'ocean', label: 'Ocean' },
        { value: 'cyberpunk', label: 'Cyberpunk' },
        { value: 'forest', label: 'Forêt' }
      ],
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
      showGamesOrbit: false,
      gamesList: [
        { id: 1, title: 'Roue Competences', icon: 'game-icon-galaxy', url: '/roue-des-competences' },
        { id: 2, title: 'Scenarios', icon: 'game-icon-puzzle', url: '/scenarios' },
        { id: 3, title: 'Métiers', icon: 'game-icon-memory', url: '/metier/soudeur' },
        { id: 4, title: 'Environnement', icon: 'game-icon-asteroid', url: '/environment' },
        { id: 5, title: 'Galaxy Match', icon: 'game-icon-quiz' },
      ],
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

    changeTheme(theme) {
      this.currentTheme = theme;
      
      // Optional: store the selected theme in localStorage to persist across sessions
      localStorage.setItem('dashboard-theme', theme);
      
      // Optional: trigger achievement for first theme change
      if (!this.themeChangeAchieved && theme !== 'cosmic') {
        this.triggerAchievement('Explorateur de Mondes');
        this.themeChangeAchieved = true;
      }
    },

    enterGamesZoom() {      
      // Ajouter une classe pour l'animation de zoom au lieu de manipuler le DOM
      this.$nextTick(() => {
        // Utiliser Vue nextTick pour s'assurer que le DOM est mis à jour
        document.querySelector('.section.games').classList.add('games-button-active');
        
        // Utiliser haptic feedback si disponible
        if (window.navigator && window.navigator.vibrate) {
          window.navigator.vibrate(50);
        }
        
        // Mettre à jour l'état
        this.gamesZoomed = true;
        this.activeSection = 'games';
        this.showGamesOrbit = true;
        
        // Réduire la notification si présente
        if (this.notifications.games > 0) {
          this.notifications.games--;
        }
      });
    },

    // Exit games zoom mode
    exitGamesZoom() {
      document.querySelector('.section.games').classList.remove('games-button-active');
      
      this.gamesZoomed = false;
      this.showGamesOrbit = false;
      
      // Haptic feedback léger pour la sortie
      if (window.navigator && window.navigator.vibrate) {
        window.navigator.vibrate([30, 20, 30]);
      }
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
      const halfSize = size / 2;
      
      return {
        left: `calc(50% - ${halfSize}px)`,
        top: `calc(50% - ${halfSize}px)`,
        width: `${size}px`,
        height: `${size}px`,
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

    toggleGamesOrbit() {
      const sectionEl = this.$refs.gamesContent;
  
      if (sectionEl) {

        sectionEl.classList.add('button-animate');
        
        // Utiliser requestAnimationFrame pour une animation plus fluide
        requestAnimationFrame(() => {
          // Utiliser haptic feedback si disponible
          if (window.navigator && window.navigator.vibrate) {
            window.navigator.vibrate(50);
          }

          // Remove the class after animation completes
          setTimeout(() => {
            sectionEl.classList.remove('button-animate');
          }, 400);
        });
      }
      
      // Basculer l'état des jeux
      if (!this.gamesZoomed) {
        this.enterGamesZoom();
      } else {
        this.exitGamesZoom();
      }
    },


    selectGame(game) {
      // If a game is selected, hide the orbit
      this.showGamesOrbit = false;

      if (game.url) {
        // Si vous utilisez Vue Router
        this.$router.push(game.url);

        // Show achievement for first game played
        if (Math.random() > 0.5) {
          this.triggerAchievement('Joueur Stellaire');
        }
      }
      
      // Open the modal with game details
      this.activeModal = 'game-' + game.id;
      
      // Show achievement for first game played
      if (Math.random() > 0.5) {
        this.triggerAchievement('Joueur Stellaire');
      }
    },

    calculateOrbitPosition(index, total) {
      // Calculate the angle for this item
      const angle = (index / total) * Math.PI * 2;
      
      // Calculate radius - distance from center
      const radius = 120; // Adjust as needed
      
      // Calculate x and y position using sine and cosine
      const x = Math.cos(angle) * radius;
      const y = Math.sin(angle) * radius;
      
      // Delay for sequential appearance animation
      const delay = index * 0.08;
      
      return {
        transform: `translate(${x}px, ${y}px)`,
        transitionDelay: `${delay}s`
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
			const sectionEl = this.$refs[`${section}Content`] || 
                    document.querySelector(`.section.${section} .section-content`);
      if (sectionEl) {
        const ripple = document.createElement('div');
        ripple.className = 'button-ripple';
        
        // Add the ripple to the section
        sectionEl.appendChild(ripple);
        
        // Use requestAnimationFrame for smoother animation
        requestAnimationFrame(() => {
          // Add haptic feedback if available
          if (window.navigator && window.navigator.vibrate) {
            window.navigator.vibrate(50);
          }
          
          // Remove the ripple after animation completes
          setTimeout(() => {
            if (ripple.parentNode === sectionEl) {
              sectionEl.removeChild(ripple);
            }
          }, 600);
        });
      }

      if (section === 'formations') {
        this.$router.push('/formation');

        // Réduire la notification
        if (this.notifications[section] > 0) {
          this.notifications[section]--;
        }
        return;
      }

      if (section === 'profile') {
        this.$router.push('/user-profile');
        
        // Réduire la notification
        if (this.notifications[section] > 0) {
          this.notifications[section]--;
        }
        return;
      }

      if (section === 'badges') {
        this.$router.push('/badges');
 
        // Réduire la notification
        if (this.notifications[section] > 0) {
          this.notifications[section]--;
        }
        return;
      }
			
			// Special handling for games section
      if (section === 'games') {
        this.toggleGamesOrbit();
        return;
      }
      
      // Normal modal opening for other sections
      this.activeModal = section;
      
      // Animation speciale pour le profil
      if (section === 'profile') {
        this.triggerProfileAnimation();
      }
			
			// Réduire la notification
			if (this.notifications[section] > 0) {
				this.notifications[section]--;
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

    const savedTheme = localStorage.getItem('dashboard-theme');
    if (savedTheme && this.availableThemes.some(theme => theme.value === savedTheme)) {
      this.currentTheme = savedTheme;
    }
    
    // Flag to track theme change achievement
    this.themeChangeAchieved = false;
    
    // Simulate notifications periodically
    setInterval(() => {
      const sections = ['formations', 'badges', 'games', 'profile'];
      const randomSection = sections[Math.floor(Math.random() * sections.length)];
      
      if (Math.random() > 0.7) {
        this.notifications[randomSection]++;
      }
    }, 30000);
    
    // Simulate a reward after a certain time
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
  z-index: 10;
}

.theme-selector {
  position: absolute;
  bottom: 20px;
  left: 20px;
  display: flex;
  gap: 15px;
  background: rgba(30, 30, 45, 0.7);
  border-radius: 12px;
  padding: 10px 15px;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
  z-index: 20;
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
  background: linear-gradient(135deg, #7C4DFF 0%, #0D47A1 100%);
  box-shadow: 0 0 10px rgba(124, 77, 255, 0.5);
}

.theme-icon.ocean {
  background: linear-gradient(135deg, #4FC3F7 0%, #0D47A1 100%);
  box-shadow: 0 0 10px rgba(79, 195, 247, 0.5);
}

.theme-icon.cyberpunk {
  background: linear-gradient(135deg, #FF4081 0%, #AB47BC 100%);
  box-shadow: 0 0 10px rgba(255, 64, 129, 0.5);
}

.theme-icon.forest {
  background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%);
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

/* Add animation for changing themes */
@keyframes nebulaShift {
  0% { transform: scale(1) rotate(0deg); }
  50% { transform: scale(1.2) rotate(5deg); }
  100% { transform: scale(1) rotate(10deg); }
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

.click-outside-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 35; /* Below game orbit buttons but above other elements */
  cursor: pointer;
  background: transparent;
}

.game-orbit {
  position: absolute;
  width: 0;
  height: 0;
  top: 25%;
  left: 25%;
  z-index: 50;
  pointer-events: none;
}

.game-orbit-button {
  position: absolute;
  width: 80px;
  height: 80px;
  transform: translate(-50%, -50%);
  transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275),
              opacity 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  opacity: 0;
  pointer-events: all;
  perspective: 1000px;
  will-change: transform, opacity;
}

.game-orbit-button.game-orbit-appear {
  opacity: 1;
}

.game-orbit-content {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background: rgba(30, 30, 45, 0.7);
  backdrop-filter: blur(5px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
  border: 2px solid rgba(255, 64, 129, 0.3);
  box-shadow: 
    0 5px 15px rgba(0, 0, 0, 0.3),
    0 0 10px rgba(255, 64, 129, 0.3);
  transform-style: preserve-3d;
  transform: scale(0);
  animation: gameButtonAppear 0.5s forwards;
  will-change: transform;
}

@keyframes gameButtonAppear {
  0% { transform: scale(0) rotate(-45deg); }
  50% { transform: scale(1.1) rotate(15deg); }
  100% { transform: scale(1) rotate(0deg); }
}

.game-orbit-content:hover {
  transform: translateZ(10px) scale(1.1);
  box-shadow: 
    0 8px 20px rgba(0, 0, 0, 0.4),
    0 0 15px rgba(255, 64, 129, 0.5);
  border-color: rgba(255, 64, 129, 0.6);
}

.game-orbit-content:active {
  transform: translateZ(5px) scale(0.95);
}

.game-icon {
  font-size: 24px;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 5px;
}

.game-icon i {
  display: inline-block;
  width: 24px;
  height: 24px;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.game-icon-quiz {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='24' height='24' fill='none' stroke='white' stroke-width='2'%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z'/%3E%3Cpath d='M12 16v-1'/%3E%3Cpath d='M12 13c.5 0 1-.5 1-1v-1c0-.5-.5-1-1-1s-1 .5-1 1v1c0 .5.5 1 1 1z'/%3E%3C/svg%3E");
}

.game-icon-puzzle {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='24' height='24' fill='none' stroke='white' stroke-width='2'%3E%3Cpath d='M4 9h5V4H4v5z'/%3E%3Cpath d='M9 9h5V4H9v5z'/%3E%3Cpath d='M14 9h5V4h-5v5z'/%3E%3Cpath d='M4 14h5V9H4v5z'/%3E%3Cpath d='M14 14h5V9h-5v5z'/%3E%3Cpath d='M4 19h5v-5H4v5z'/%3E%3Cpath d='M9 19h5v-5H9v5z'/%3E%3Cpath d='M14 19h5v-5h-5v5z'/%3E%3C/svg%3E");
}

.game-icon-memory {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='24' height='24' fill='none' stroke='white' stroke-width='2'%3E%3Cpath d='M3 6l9 4 9-4-9-4-9 4z'/%3E%3Cpath d='M3 10l9 4 9-4'/%3E%3Cpath d='M3 14l9 4 9-4'/%3E%3C/svg%3E");
}

.game-icon-asteroid {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='24' height='24' fill='none' stroke='white' stroke-width='2'%3E%3Cpath d='M15 11.5c0 1.38-1.12 2.5-2.5 2.5S10 12.88 10 11.5 11.12 9 12.5 9s2.5 1.12 2.5 2.5z'/%3E%3Cpath d='M10 8l2-4 2 4'/%3E%3Cpath d='M14 8l2-3 2 3'/%3E%3Cpath d='M6 8l2-3 2 3'/%3E%3Cpath d='M20 15c-1-1-2.5-1-3.5 0s-2.5 1-3.5 0-2.5-1-3.5 0-2.5 1-3.5 0-2.5-1-3.5 0'/%3E%3C/svg%3E");
}

.game-icon-galaxy {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='24' height='24' fill='none' stroke='white' stroke-width='2'%3E%3Ccircle cx='12' cy='12' r='9'/%3E%3Ccircle cx='12' cy='12' r='4'/%3E%3Cpath d='M5 5l3 3'/%3E%3Cpath d='M5 19l3-3'/%3E%3Cpath d='M19 5l-3 3'/%3E%3Cpath d='M19 19l-3-3'/%3E%3C/svg%3E");
}

.game-title {
  font-size: 10px;
  color: white;
  text-align: center;
  padding: 0 5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
  opacity: 0.8;
}

.games-zoomed .section.games {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) scale(1.5);
  z-index: 50;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.button-animate {
  position: relative;
  overflow: visible;
}

.button-animate::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 64, 129, 0.8) 0%, rgba(255, 64, 129, 0) 70%);
  transform: translate(-50%, -50%) scale(0);
  opacity: 0;
  pointer-events: none;
  will-change: transform, opacity;
  animation: optimizedButtonFlash 0.4s cubic-bezier(0.215, 0.61, 0.355, 1) forwards;
}

.button-animate::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 5px;
  height: 5px;
  background: white;
  border-radius: 50%;
  transform: translate(-50%, -50%) scale(0);
  opacity: 0.7;
  pointer-events: none;
  will-change: transform, opacity;
  animation: optimizedRippleEffect 0.4s cubic-bezier(0.215, 0.61, 0.355, 1) forwards;
}

.games-button-active {
  transform: scale(1.1);
  z-index: 50;
}

@keyframes optimizedButtonFlash {
  0% {
    transform: translate(-50%, -50%) scale(0.8);
    opacity: 0;
  }
  50% {
    opacity: 0.5;
  }
  100% {
    transform: translate(-50%, -50%) scale(1.2);
    opacity: 0;
  }
}

@keyframes optimizedRippleEffect {
  0% {
    transform: translate(-50%, -50%) scale(0);
    opacity: 0.7;
  }
  100% {
    transform: translate(-50%, -50%) scale(15);
    opacity: 0;
  }
}

.games-zoomed .section:not(.games) {
  opacity: 0.3;
  filter: blur(3px);
  transform: scale(0.8);
  pointer-events: none;
}

/* Dim avatar when games are zoomed */
.games-zoomed .avatar-container {
  opacity: 0.4;
  transform: scale(0.8);
  filter: blur(2px);
  pointer-events: none;
}

/* Adjust game orbit positioning when zoomed */
.games-zoomed .game-orbit {
  position: fixed;
  top: 25%;
  left: 25%;
  transform: translate(-50%, -50%);
  z-index: 60;
}

.games-zoomed .game-orbit-button {
  transform: translate(-50%, -50%) scale(1.2);
  transition-delay: 0.2s;
}

.games-zoomed .game-orbit-button:nth-child(1) { transform: translate(-50%, -50%) translateY(-180px) scale(1.2); }
.games-zoomed .game-orbit-button:nth-child(2) { transform: translate(-50%, -50%) translateX(155px) translateY(-90px) scale(1.2); }
.games-zoomed .game-orbit-button:nth-child(3) { transform: translate(-50%, -50%) translateX(155px) translateY(90px) scale(1.2); }
.games-zoomed .game-orbit-button:nth-child(4) { transform: translate(-50%, -50%) translateY(180px) scale(1.2); }
.games-zoomed .game-orbit-button:nth-child(5) { transform: translate(-50%, -50%) translateX(-155px) translateY(90px) scale(1.2); }

.games-zoomed:before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at center, rgba(30, 30, 60, 0.3) 0%, rgba(10, 10, 30, 0.8) 100%);
  z-index: 10;
  animation: fadeIn 0.5s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.games-zoomed .game-orbit-content {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4),
              0 0 20px rgba(255, 64, 129, 0.6);
  border-color: rgba(255, 64, 129, 0.8);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
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
  will-change: transform, opacity;
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
  width: 170px;
  height: 170px;
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
  top: 18%;
  left: 18%;
}

.formations .section-content {
  background: linear-gradient(135deg, rgba(30, 30, 45, 0.7) 0%, rgba(30, 50, 80, 0.7) 100%);
}

.badges {
  top: 18%;
  right: 18%;
}

.badges .section-content {
  background: linear-gradient(135deg, rgba(30, 30, 45, 0.7) 0%, rgba(60, 30, 80, 0.7) 100%);
}

.games {
  bottom: 18%;
  left: 18%;
}

.games .section-content {
  background: linear-gradient(135deg, rgba(30, 30, 45, 0.7) 0%, rgba(80, 30, 50, 0.7) 100%);
}

.profile {
  bottom: 18%;
  right: 18%;
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
  width: 110px;
  height: 110px;
  border-radius: 50%;
  background: rgba(30, 30, 45, 0.6);
  backdrop-filter: blur(5px);
  display: flex;
  justify-content: center;
  align-items: center;
  transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275),
              background 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275),
              box-shadow 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  cursor: pointer;
  border: 2px solid rgba(255, 255, 255, 0.1);
  box-shadow: 
    0 10px 20px rgba(0, 0, 0, 0.2),
    0 5px 15px rgba(0, 0, 0, 0.1),
    inset 0 0 10px rgba(255, 255, 255, 0.05);
  transform-style: preserve-3d;
  overflow: visible;
  will-change: transform;
}

.formations .glow-effect.pulse,
.badges .glow-effect.pulse,
.games .glow-effect.pulse,
.profile .glow-effect.pulse {
  will-change: transform, opacity, box-shadow;
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
  will-change: opacity;
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
    transform: scale(1);
    opacity: 0.7;
  }
  100% {
    transform: scale(2);
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
  transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275),
              filter 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  filter: drop-shadow(0 2px 5px rgba(0, 0, 0, 0.5));
  transform-style: preserve-3d;
  will-change: transform, filter;
}

.section-content:hover .icon {
  transform: translateZ(15px) scale(1.15);
  filter: drop-shadow(0 5px 10px rgba(0, 0, 0, 0.7)) brightness(1.2);
}

.icon svg {
  width: 80px; /* Augmenté de 64px (implicite dans le HTML) à 80px */
  height: 80px; /* Augmenté de 64px (implicite dans le HTML) à 80px */
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
  width: 110%;
  height: 110%;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    rgba(64, 196, 255, 0.3) 0%,
    rgba(124, 77, 255, 0.3) 50%,
    rgba(255, 64, 129, 0.3) 100%
  );
  filter: blur(10px);
  opacity: 0.6;
  transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275), 
              opacity 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  z-index: 1;
  will-change: transform, opacity;
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
  will-change: transform, opacity;
}

@keyframes pulsate {
  0% { transform: scale(0.9); opacity: 0.6; }
  50% { transform: scale(1.1); opacity: 0.8; }
  100% { transform: scale(0.9); opacity: 0.6; }
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
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  font-weight: 500;
  letter-spacing: 0.5px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  z-index: 100;
  visibility: visible;
  left: 50%;
  transform: translateX(-50%) translateY(10px);
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
  transform: translateX(-50%) translateY(0);
  visibility: visible;
  display: block;

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
  will-change: transform, opacity;
  transform: translateZ(0);
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
    width: 80px;
    height: 80px;
  }

  .section {
    width: 130px;
    height: 130px;
  }
  
  .icon svg {
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

  .game-orbit-button {
    width: 60px;
    height: 60px;
  }
  
  .game-orbit-content {
    width: 50px;
    height: 50px;
  }
  
  .game-icon {
    font-size: 18px;
    margin-bottom: 2px;
  }
  
  .game-title {
    font-size: 8px;
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
}
</style>