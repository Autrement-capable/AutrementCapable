<template>
  <div v-if="showBadgeUnlockAnimation" class="badge-unlock-overlay">
    <div class="badge-unlock-animation">
      <div class="badge-icon" v-if="newlyUnlockedBadge">{{ newlyUnlockedBadge.icon }}</div>
      <h2>Badge débloqué !</h2>
      <h3 v-if="newlyUnlockedBadge">{{ newlyUnlockedBadge.title }}</h3>
      <p v-if="newlyUnlockedBadge">{{ newlyUnlockedBadge.description }}</p>
      <button @click="closeBadgeAnimation" class="close-animation-btn">Continuer</button>
    </div>
  </div>
  <div class="rewards-container" :class="{ 'high-contrast': highContrastMode }">
    <button class="close-modal-btn" @click="$emit('close')"></button>

    <!-- Header - Profil simplifié -->
    <div class="profile-header">
      <div class="avatar-section">
        <img :src="require('@/assets/pdp.png')" alt="Avatar" class="user-avatar" />
        <div class="level-badge">Niveau {{ calculateLevel() }}</div>
      </div>
      <div class="user-info">
        <h1 class="welcome-title">Bonjour {{ userProfile.firstName }} ! 👋</h1>
        <p class="welcome-subtitle">Content de te revoir aujourd'hui !</p>
        <div class="user-details">
          <div class="user-detail-item">
            <span class="detail-label">Âge:</span>
            <span class="detail-value">{{ userProfile.age }} ans</span>
          </div>
          <div class="user-detail-item">
            <span class="detail-label">Ville:</span>
            <span class="detail-value">{{ userProfile.city }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Nouvelle carte de progression -->
    <div class="progress-map-container">
      <h2 class="section-title">Ma carte de progression</h2>
      <div class="progress-stats">
        <div class="progress-stat">
          <span class="stat-number">{{ unlockedBadgesCount }}</span>
          <span class="stat-label">Badges débloqués</span>
        </div>
        <div class="progress-stat">
          <span class="stat-number">{{ totalBadgesCount - unlockedBadgesCount }}</span>
          <span class="stat-label">À débloquer</span>
        </div>
        <div class="progress-stat">
          <span class="stat-number">{{ calculateLevel() }}</span>
          <span class="stat-label">Niveau actuel</span>
        </div>
      </div>
      
      <div class="progress-map">
        <div class="journey-path"></div>
        
        <div
          v-for="badge in badges"
          :key="badge.id"
          class="map-badge-node"
          :class="{ 'unlocked': badge.unlocked, 'active': badge.id === nextBadge.id && !badge.unlocked }"
          @click="showBadgeDetails(badge)"
        >
          <div 
            class="map-badge-icon" 
            :style="{ backgroundColor: badge.unlocked ? badge.iconColor : '#555' }"
          >
            <div v-if="!badge.unlocked" class="map-badge-lock">🔒</div>
            <span class="map-badge-emoji">{{ badge.icon }}</span>
          </div>
          <div class="map-badge-tooltip">
            <div class="tooltip-title">{{ badge.title }}</div>
            <!-- <div class="tooltip-game">{{ badge.game }}</div> -->
            <div class="tooltip-status" :class="badge.unlocked ? 'status-unlocked' : ''">
              {{ badge.unlocked ? 'Obtenu ✅' : 'À débloquer' }}
            </div>
          </div>
          
          <div v-if="badge.id === nextBadge.id && !badge.unlocked" class="map-badge-next">
            <div class="pulse-circle"></div>
            <div class="next-badge-text">Prochaine activité</div>
          </div>
        </div>
      </div>
      
      <div class="map-legend">
        <div class="legend-item">
          <div class="legend-icon unlocked"></div>
          <div class="legend-text">Badges débloqués</div>
        </div>
        <div class="legend-item">
          <div class="legend-icon locked"></div>
          <div class="legend-text">Badges à débloquer</div>
        </div>
        <div class="legend-item">
          <div class="legend-icon active"></div>
          <div class="legend-text">Prochaine activité suggérée</div>
        </div>
      </div>
    </div>

    <!-- Message si aucun badge
    <div class="empty-state" v-if="!hasUnlockedBadges">
      <div class="empty-badge-icon">🏅</div>
      <h2>Pas encore de badges !</h2>
      <p>Participe aux jeux et activités pour gagner tes premiers badges.</p>
    </div> -->

    <!-- Prochaine activité -->
    <div class="next-activity" v-if="hasUnlockedBadges || nextBadge">
      <h2 class="section-title">Ma prochaine activité</h2>
      <div class="next-activity-card">
        <div 
          class="next-activity-icon" 
          :style="{ backgroundColor: nextBadge.iconColor }"
        >
          <span class="activity-emoji">{{ nextBadge.icon }}</span>
        </div>
        <div class="next-activity-info">
          <h3>{{ nextBadge.title }}</h3>
          <p>{{ nextBadge.hint || 'Joue pour débloquer ce badge !' }}</p>
          <button 
            class="play-button"
            @click="goToGame(nextBadge.gameRoute)"
          >
            Jouer maintenant →
          </button>
        </div>
      </div>
    </div>

    <!-- Tous les badges -->
    <div class="all-badges">
      <h2 class="section-title">Mes badges</h2>
      <div class="badges-grid">
        <div 
          v-for="badge in badges" 
          :key="badge.id" 
          class="badge-card"
          :class="{ 'unlocked': badge.unlocked, 'locked': !badge.unlocked }"
          @click="showBadgeDetails(badge)"
        >
          <div 
            class="badge-icon" 
            :style="{ backgroundColor: badge.unlocked ? badge.iconColor : '#e0e0e0' }"
          >
            <div v-if="!badge.unlocked" class="lock-overlay">🔒</div>
            <span class="badge-emoji">{{ badge.icon }}</span>
          </div>
          <h3 class="badge-title">{{ badge.title }}</h3>
          <div class="badge-status">
            <span :class="badge.unlocked ? 'status-unlocked' : 'status-locked'">
              {{ badge.unlocked ? 'Obtenu ✅' : 'À débloquer' }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Boutons d'action -->
    <div class="action-buttons">
      <button class="action-button generate-cv-button" @click="generateCV">
        <span class="button-icon">📄</span>
        Créer mon CV
      </button>
      <button class="action-button profile-button" @click="viewProfile">
        <span class="button-icon">👤</span>
        Mon profil
      </button>
    </div>

    <!-- Détails du badge (modal) -->
    <div v-if="selectedBadge" class="badge-modal-overlay" @click="closeModal">
      <div class="badge-modal" @click.stop>
        <button class="close-button" @click="closeModal">×</button>

        <div class="badge-detail-content">
          <div
            class="badge-detail-icon"
            :style="{ backgroundColor: selectedBadge.iconColor || '#e0e0e0' }"
          >
            <span class="badge-detail-emoji">{{ selectedBadge.icon }}</span>
          </div>

          <h2 class="badge-detail-title">{{ selectedBadge.title }}</h2>

          <p class="badge-detail-description">
            {{ selectedBadge.unlocked ? selectedBadge.description : (selectedBadge.hint || 'Continue à jouer pour débloquer ce badge !') }}
          </p>

          <div v-if="selectedBadge.unlocked" class="badge-achievement">
            <div class="achievement-date">
              Obtenu le: {{ formatDate(selectedBadge.dateUnlocked) }}
            </div>
            <div class="achievement-game">
              Dans: {{ selectedBadge.game }}
            </div>
          </div>
          <div v-else class="badge-locked-info">
            <div class="badge-hint">
              <span class="hint-icon">💡</span>
              <p>{{ selectedBadge.hint || 'Continue à jouer pour débloquer ce badge !' }}</p>
            </div>
            <div class="badge-game">
              Jeu: {{ selectedBadge.game }}
            </div>
          </div>

          <div class="badge-actions">
            <button
              v-if="!selectedBadge.unlocked"
              @click="goToGame(selectedBadge.gameRoute)"
              class="play-now-button"
            >
              Jouer maintenant
            </button>
            <button
              v-if="selectedBadge.unlocked && selectedBadge.shareable"
              @click="shareBadge(selectedBadge)"
              class="share-button"
            >
              Partager ce badge
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Effet de mise en évidence de la prochaine activité -->
    <div v-if="highlightNextActivity" class="next-activity-highlight">
      <div class="highlight-pulse"></div>
      <div class="highlight-arrow">
        <span class="highlight-text">Clique ici !</span>
      </div>
    </div>
  </div>
  <guide-avatar
    v-if="internalShowGuide"
    guide-name="Léo"
    :forced-message="profileGuideMessage"
    :forced-options="profileGuideOptions"
    :force-show-message="profileTourActive || forceShowGuide"
    :custom-position="guideCustomPosition"
    :active-section-id="profileTourActive ? profileTourSections[profileTourStep].id : null"
    context="profile"
    :auto-show-delay="0"
    @option-selected="handleGuideOptionSelected"
    @position-updated="updateGuidePosition"
  />

  <!-- Overlay pour le tour guidé -->
  <div v-if="profileTourActive" class="tour-overlay"></div>
</template>

<script>
import UserJourneyService from '@/services/UserJourneyService.js'
import { eventBus } from '@/utils/eventBus'
import GuideAvatar from '@/components/GuideComponent.vue'

export default {
  name: 'RewardsComponent',
  components: {
    GuideAvatar,
  },
  props: {
    // Passer les props nécessaires depuis le Dashboard
    currentTheme: {
      type: String,
      default: 'cosmic',
    },
    animationsEnabled: {
      type: Boolean,
      default: true,
    },
    progress: {
      type: Number,
      default: 37,
    },
    showProfileGuide: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      userProfile: {
        firstName: 'Lucas',
        lastName: 'Martin',
        age: 16,
        city: 'Lyon',
      },
      badges: [
        {
          id: 0,
          title: 'Explorateur du Profil',
          description: 'Tu as découvert ton profil avec succès !',
          icon: '🧭',
          iconColor: '#FF5722',
          unlocked: false,
          game: 'Profil',
          gameRoute: '/dashboard',
          shareable: true,
          dateUnlocked: '2023-06-15',
          hint: 'Badge déjà obtenu'
        },
        {
          id: 1,
          title: 'Maître de la vitesse',
          description:
            'Tu as terminé le jeu de vitesse avec un score parfait !',
          icon: '⚡',
          iconColor: '#F44336',
          unlocked: false,
          dateUnlocked: '2023-06-16',
          game: 'Jeu de Vitesse',
          gameRoute: '/game-speed',
          shareable: true,
          hint: 'Badge déjà obtenu'
        },
        {
          id: 2,
          title: 'Maître des scénarios',
          description:
            'Tu as brillamment résolu ton premier scénario social !',
          icon: '🎭',
          iconColor: '#9C27B0',
          unlocked: false,
          dateUnlocked: '2023-06-18',
          game: 'Jeu des Scénarios',
          gameRoute: '/scenarios',
          shareable: true,
          hint: 'Badge déjà obtenu'
        },
        {
          id: 3,
          title: 'Expert des formes',
          description:
            'Tu as reconnu toutes les séquences de formes correctement !',
          icon: '🔷',
          iconColor: '#2196F3',
          unlocked: false,
          hint: 'Termine le jeu des formes avec un score parfait',
          game: 'Jeu des Formes',
          gameRoute: '/shape-sequence-game',
          shareable: true,
        },
        {
          id: 4,
          title: 'Explorateur de compétences',
          description:
            'Tu as exploré et identifié tes points forts !',
          icon: '🎯',
          iconColor: '#3F51B5',
          unlocked: false,
          hint: 'Termine la Roulette des Compétences et découvre tes talents',
          game: 'Roulette des Compétences',
          gameRoute: '/roue-des-competences',
          shareable: true,
        },
        {
          id: 5,
          title: "Explorateur d'environnements",
          description: 'Tu as exploré tous les environnements disponibles',
          icon: '🏠',
          iconColor: '#795548',
          unlocked: false,
          hint: "Essaie tous les préréglages dans l'environnement de personnalisation",
          game: 'Environnement',
          gameRoute: '/environment',
          shareable: false,
        },
        {
          id: 6,
          title: 'CV professionnel',
          description:
            'Tu as complété toutes les étapes pour générer un CV professionnel',
          icon: '📄',
          iconColor: '#607D8B',
          unlocked: false,
          dateUnlocked: '2023-06-20',
          game: 'Générateur de CV',
          gameRoute: '/cv-preview',
          shareable: true,
          hint: 'Crée ton CV pour débloquer ce badge'
        },
        {
          id: 7,
          title: 'Apprenti des métiers',
          description: 'Tu as découvert 3 métiers différents',
          icon: '👷',
          iconColor: '#FF9800',
          unlocked: false,
          hint: 'Explore au moins 3 fiches métier',
          game: 'Découverte des métiers',
          gameRoute: '/metier/soudeur',
          shareable: false,
        },
        {
          id: 8,
          title: 'Inscription à une formation',
          description: 'Tu t\'es inscrit à une formation',
          icon: '🎓',
          iconColor: '#FFD700',
          unlocked: false,
          hint: 'Inscris-toi à une formation pour débloquer ce badge',
          game: 'Formations',
          gameRoute: '/formation',
          shareable: true,
        },
      ],
      selectedBadge: null,
      highContrastMode: false,
      textSizeLevel: 0,
      showBadgeUnlockAnimation: false,
      newlyUnlockedBadge: null,
      internalShowGuide: this.showProfileGuide,
      profileTourActive: false,
      profileTourStep: 0,
      profileTourSections: [
        {
          id: 'header',
          name: 'En-tête du profil',
          selector: '.profile-header',
          description: "C'est ton profil personnel ! Tu peux voir ton avatar, ton niveau actuel et tes informations personnelles comme ton âge et ta ville."
        },
        {
          id: 'progress-map',
          name: 'Carte de progression',
          selector: '.progress-map-container',
          description: "Cette carte montre tous tes badges. Les badges débloqués sont en couleur, et les badges à débloquer sont grisés avec un cadenas. Le badge clignotant orange est ta prochaine activité recommandée !"
        },
        {
          id: 'next-activity',
          name: 'Prochaine activité',
          selector: '.next-activity',
          description: "Ici tu trouveras ta prochaine activité recommandée. Clique sur 'Jouer maintenant' pour la commencer et débloquer un nouveau badge !"
        },
        {
          id: 'badges-grid',
          name: 'Mes badges',
          selector: '.all-badges',
          description: "Cette section affiche tous tes badges, débloqués ou non. Clique sur un badge pour voir plus de détails et comment le débloquer si tu ne l'as pas encore."
        },
        {
          id: 'actions',
          name: 'Actions',
          selector: '.action-buttons',
          description: "Ces boutons te permettent de créer ton CV avec les compétences que tu as développées ou d'accéder directement à ton profil complet."
        }
      ],
      
      // Mise à jour des messages et options du guide pour inclure le tour du profil
      profileGuideMessage: "Bienvenue sur ton profil ! Veux-tu que je te fasse visiter pour découvrir toutes les fonctionnalités ?",
      profileGuideOptions: [
        { text: "Oui, montre-moi tout !", action: "startProfileTour" },
      ],
      
      // Flag pour déterminer si le guide doit mettre en évidence des sections
      highlightNextActivity: false,
      
      // Overlay pour le tour guidé
      showTourOverlay: false,
      guideCustomPosition: null,
      forceShowGuide: false
    }
  },
  computed: {
    unlockedBadgesCount() {
      return this.badges.filter((badge) => badge.unlocked).length
    },
    totalBadgesCount() {
      return this.badges.length
    },
    progressPercentage() {
      return (this.unlockedBadgesCount / this.totalBadgesCount) * 100
    },
    hasUnlockedBadges() {
      return this.unlockedBadgesCount > 0
    },
    nextBadge() {
      // Trouve le premier badge non débloqué
      const nextBadge = this.badges.find(badge => !badge.unlocked);
      return nextBadge || this.badges[0]; // Retourne le premier badge si tout est débloqué
    }
  },
  watch: {
    // Observer les changements de la prop showProfileGuide
    showProfileGuide: {
      immediate: true,
      handler(newValue) {
        this.internalShowGuide = newValue;
      }
    }
  },
  created() {
    // Chargement des préférences d'accessibilité
    this.loadAccessibilitySettings()

    // On pourrait aussi chargement les badges depuis localStorage
    this.loadBadges()

    // Vérifie si le badge de profil doit être débloqué
    this.checkProfileBadge()

    // Vérifier si c'est la première fois que l'utilisateur accède au profil
    this.checkFirstProfileVisit();
  },
  mounted() {
    // Vérifier si c'est la première visite du profil
    const hasVisitedProfile = localStorage.getItem('hasVisitedProfile');
    const hasCompletedProfileTour = localStorage.getItem('profile-tour-completed');
    
    // Si c'est la première visite ou si le guide est activé par la prop
    if ((!hasVisitedProfile || this.showProfileGuide) && !hasCompletedProfileTour) {
      setTimeout(() => {
        this.internalShowGuide = true;
        this.forceShowGuide = true;
        this.profileGuideMessage = "Bienvenue sur ton profil ! Veux-tu que je te fasse visiter pour découvrir toutes les fonctionnalités ?";
        this.profileGuideOptions = [
          { text: "Oui, montre-moi tout !", action: "startProfileTour" },
        ];
      }, 800);
    }
    
    // Écouter les évènements pour le redimensionnement de la fenêtre
    window.addEventListener('resize', this.updateHighlights);
    
    // Écouter l'événement pour mettre en évidence le bouton "Jouer maintenant"
    eventBus.on('highlight-play-button', () => {
      this.highlightPlayButton();
    });
  },
  beforeUnmount() {
    // Nettoyer les évènements
    window.removeEventListener('resize', this.updateHighlights);
    eventBus.off('highlight-play-button');
    this.removeHighlights();
  },
  methods: {
    /**
     * Met à jour la position du guide lorsqu'elle est modifiée par le composant guide
     */
    updateGuidePosition(position) {
      this.guideCustomPosition = position;
    },
    /**
     * Met à jour les mises en évidence lors du redimensionnement de la fenêtre
     */
    updateHighlights() {
      if (this.profileTourActive && this.profileTourStep < this.profileTourSections.length) {
        // Récupérer la section actuelle
        const section = this.profileTourSections[this.profileTourStep];
        
        // Mettre à jour la mise en évidence
        this.highlightProfileSection(section.selector);
      }
    },
    /**
     * Démarre le tour guidé du profil
     */
     startProfileTour() {
      
      // Initialiser le tour du profil dans le service
      if (typeof UserJourneyService !== 'undefined') {
        UserJourneyService.startProfileTour();
      }
      
      // Initialiser les variables locales du tour
      this.profileTourStep = 0;
      this.profileTourActive = true;
      
      // Supprimer toutes les mises en évidence existantes pour être sûr
      this.removeHighlights();
      
      // Commencer le tour par la première section
      this.showProfileTourStep();
    },

    /**
     * Affiche l'étape actuelle du tour du profil
     */
     showProfileTourStep() {
      if (!this.profileTourActive) {
        console.error("Le tour du profil n'est pas actif");
        return;
      }
      
      // Vérifier si nous avons dépassé les étapes disponibles
      if (this.profileTourStep >= this.profileTourSections.length) {
        this.endProfileTour();
        return;
      }
      
      // Récupérer la section actuelle
      const currentSection = this.profileTourSections[this.profileTourStep];
      
      // Mettre à jour le message et les options du guide
      this.profileGuideMessage = currentSection.description;
      this.profileGuideOptions = [
        { text: this.profileTourStep === this.profileTourSections.length - 1 ? "Terminer" : "Suivant", action: "nextProfileTourStep" },
        // { text: "Arrêter la visite", action: "endProfileTour" }
      ];
      
      // Forcer l'affichage du guide
      this.internalShowGuide = true;
      this.forceShowGuide = true;
      
      // Mettre en évidence la section actuelle
      this.highlightProfileSection(currentSection.selector);
      
      // Marquer la section comme visitée dans le service
      if (typeof UserJourneyService !== 'undefined') {
        UserJourneyService.markProfileSectionVisited(currentSection.id);
      }
    },

    /**
     * Passe à l'étape suivante du tour du profil
     */
    nextProfileTourStep() {
      // Supprimer la mise en évidence actuelle
      this.removeHighlights();
      
      // Passer à l'étape suivante
      this.profileTourStep++;
      
      // Afficher la nouvelle étape
      this.showProfileTourStep();
    },

    /**
     * Termine le tour du profil
     */
    endProfileTour() {
      // Supprimer les mises en évidence
      this.removeHighlights();
      
      // Mettre à jour l'état
      this.profileTourActive = false;
      
      // Marquer le tour comme terminé dans le service
      if (typeof UserJourneyService !== 'undefined') {
        UserJourneyService.completeProfileTour();
      }
      
      localStorage.setItem('profile-tour-completed', 'true');

      // Vérifier si le badge "Explorateur du Profil" doit être débloqué
      this.checkProfileBadge();

      // Afficher le message de fin du tour
      this.profileGuideMessage = "Tu connais maintenant toutes les sections de ton profil ! Tu peux explorer tes badges et commencer à jouer pour en débloquer de nouveaux.";
      this.profileGuideOptions = [
        { text: "Commencer à jouer", action: "highlightPlayButton" },
        { text: "Merci !", action: "dismissProfileGuide" }
      ];
      this.internalShowGuide = true;
    },

    /**
     * Met en évidence une section du profil
     */
     highlightProfileSection(selector) {
      // D'abord supprimer les mises en évidence existantes
      this.removeHighlights();
      
      // Ajouter une nouvelle mise en évidence
      const element = document.querySelector(selector);
      if (element) {
        // Créer un élément de surbrillance
        const highlight = document.createElement('div');
        highlight.className = 'section-highlight';
        
        // Obtenir les coordonnées de l'élément par rapport au conteneur
        const rect = element.getBoundingClientRect();
        
        // Obtenir la référence du conteneur rewards-container
        const container = document.querySelector('.rewards-container');
        const containerRect = container.getBoundingClientRect();
        
        // Calculer les coordonnées relatives au conteneur
        // et prendre en compte le scroll du conteneur
        const top = rect.top - containerRect.top + container.scrollTop;
        const left = rect.left - containerRect.left + container.scrollLeft;
        
        // Positionner la surbrillance avec les coordonnées relatives
        highlight.style.position = 'absolute';
        highlight.style.top = `${top}px`;
        highlight.style.left = `${left}px`;
        highlight.style.width = `${rect.width}px`;
        highlight.style.height = `${rect.height}px`;
        highlight.style.border = '3px solid #76ff03';
        highlight.style.borderRadius = '16px';
        highlight.style.boxShadow = '0 0 15px rgba(118, 255, 3, 0.7)';
        highlight.style.pointerEvents = 'none';
        highlight.style.zIndex = '1050';
        highlight.style.animation = 'highlight-pulse 2s ease-out infinite';
        
        // Ajouter la surbrillance au conteneur (non au body)
        container.appendChild(highlight);
        
        
        // Calculer où l'élément devrait être visible dans le conteneur
        const elementTopRelativeToContainer = top;
        const elementBottomRelativeToContainer = top + rect.height;
        const containerVisibleTop = container.scrollTop;
        const containerVisibleBottom = container.scrollTop + container.clientHeight;
        
        // Vérifier si l'élément est déjà visible dans la zone visible du conteneur
        if (elementTopRelativeToContainer < containerVisibleTop || elementBottomRelativeToContainer > containerVisibleBottom) {
          // Element n'est pas entièrement visible, faire défiler seulement le conteneur
          container.scrollTo({
            top: elementTopRelativeToContainer - container.clientHeight / 2 + rect.height / 2,
            behavior: 'smooth'
          });
        }
        
        // Position fixe pour le guide - toujours visible à côté du composant
        const rewardsRight = containerRect.right;
        const position = {
          position: 'fixed',
          top: '150px', // Position fixe plus bas pour éviter tout conflit
          left: `${rewardsRight + 10}px`, // 10px à droite du conteneur Rewards
          zIndex: 2500
        };
        
        // Mettre à jour la position du guide
        this.guideCustomPosition = position;
      } else {
        console.error("Élément non trouvé avec le sélecteur :", selector);
      }
    },
    /**
     * Supprime toutes les mises en évidence
     */
     removeHighlights() {
      const container = document.querySelector('.rewards-container');
      if (container) {
        const highlights = container.querySelectorAll('.section-highlight');
        highlights.forEach(highlight => {
          container.removeChild(highlight);
        });
      }
    },

    /**
     * Gère les options sélectionnées dans le guide
     */
    handleGuideOptionSelected(option) {
      if (option.action && typeof this[option.action] === 'function') {
        this[option.action]();
      } else {
        console.warn(`L'action "${option.action}" n'est pas définie.`);
      }
    },
    checkFirstProfileVisit() {
      const hasVisitedProfile = localStorage.getItem('hasVisitedProfile');
      
      if (!hasVisitedProfile) {
        // Si c'est la première visite, on le stocke dans localStorage
        localStorage.setItem('hasVisitedProfile', 'true');
        
        // Mettre à jour l'étape dans le service de parcours utilisateur si disponible
        if (typeof UserJourneyService !== 'undefined') {
          UserJourneyService.updateStep(UserJourneyService.STEPS.PROFILE_INTRO);
        }
      }
    },
    // Fermer le guide du profil
    dismissProfileGuide() {
      this.internalShowGuide = false;
      this.highlightNextActivity = false;
      localStorage.setItem('profile-tour-completed', 'true');
    },
    
    // Mettre en évidence le bouton "Jouer maintenant"
    highlightPlayButton() {
      this.highlightNextActivity = true;
      this.profileGuideMessage = "Clique sur le bouton 'Jouer maintenant' dans cette section pour commencer ton premier jeu !";
    },
    
    // Méthode pour gérer le clic sur le bouton "Jouer maintenant"
    goToGame(route) {
      this.closeModal();
      
      // Mettre à jour l'étape du parcours utilisateur si disponible
      if (typeof UserJourneyService !== 'undefined') {
        UserJourneyService.updateStep(UserJourneyService.STEPS.FIRST_GAME);
      }
      
      // Émettre un événement pour indiquer que l'utilisateur a commencé à jouer
      eventBus.emit('start-game', { route }); // Utiliser eventBus.emit au lieu de $root.$emit
      
      this.$router.push(route);
    },
    checkProfileBadge() {
      // Trouver le badge "Explorateur du Profil" (ID 0)
      const profileBadge = this.badges.find(badge => badge.id === 0)
      
      // // Vérifie si c'est la première visite en cherchant un flag dans localStorage
      // const hasVisitedProfile = localStorage.getItem('hasVisitedProfile')

      // Vérifier si la visite du profil est terminée
      const isProfileVisitCompleted = localStorage.getItem('profile-tour-completed')
      
      if (profileBadge && !profileBadge.unlocked && isProfileVisitCompleted) {
        // Marquer comme visité pour éviter de redéclencher l'animation
        localStorage.setItem('hasVisitedProfile', 'true')
        
        // Débloquer le badge
        profileBadge.unlocked = true
        profileBadge.dateUnlocked = new Date().toISOString().split('T')[0]
        
        // Sauvegarder l'état des badges
        this.saveBadges()
        
        // Déclencher l'animation
        this.newlyUnlockedBadge = profileBadge
        
        // Attendre un peu avant d'afficher l'animation pour permettre au composant de se charger
        setTimeout(() => {
          this.showBadgeUnlockAnimation = true
        }, 1000)
      }
    },

    closeBadgeAnimation() {
      this.showBadgeUnlockAnimation = false
    },

    calculateLevel() {
      return Math.floor(this.progress / 10) + 1;
    },
    
    toggleAnimations() {
      // Émettre un événement pour que le parent puisse mettre à jour son état
      this.$emit('toggle-animations')
    },
    
    loadBadges() {
      // Dans un cas réel, on chargerait les badges depuis localStorage
      // ou depuis une API selon que l'utilisateur est connecté ou non
      const savedBadges = localStorage.getItem('userBadges')
      if (savedBadges) {
        try {
          const badgeData = JSON.parse(savedBadges)
          // Fusionner les données sauvegardées avec nos badges par défaut
          this.badges = this.badges.map((badge) => {
            const savedBadge = badgeData.find((b) => b.id === badge.id)
            if (savedBadge) {
              return { ...badge, ...savedBadge }
            }
            return badge
          })
        } catch (error) {
          console.error('Erreur lors du chargement des badges:', error)
        }
      }

      // Vérification si le badge "collectionneur" devrait être débloqué
      this.checkBadgeCollector()
    },

    checkBadgeCollector() {
      // Vérifier si l'utilisateur a débloqué 5 badges ou plus
      if (this.unlockedBadgesCount >= 5) {
        const collectorBadge = this.badges.find((badge) => badge.id === 8)
        if (collectorBadge && !collectorBadge.unlocked) {
          collectorBadge.unlocked = true
          collectorBadge.dateUnlocked = new Date().toISOString().split('T')[0]
          this.saveBadges()
        }
      }
    },

    saveBadges() {
      // Enregistrer les badges dans localStorage
      localStorage.setItem('userBadges', JSON.stringify(this.badges))
    },

    formatDate(dateString) {
      // Formater une date en format français
      if (!dateString) return ''

      const options = { day: 'numeric', month: 'long', year: 'numeric' }
      const date = new Date(dateString)

      return date.toLocaleDateString('fr-FR', options)
    },

    showBadgeDetails(badge) {
      this.selectedBadge = badge
    },

    closeModal() {
      this.selectedBadge = null
    },

    shareBadge(badge) {
      // Dans un cas réel, cela pourrait ouvrir une boîte de dialogue de partage
      // ou générer un lien à partager
      alert(
        `Partage du badge "${badge.title}" sur les réseaux sociaux`
      )
    },
    
    generateCV() {
      // Dans un cas réel, on redirigerait vers la page de génération de CV
      this.$router.push('/cv-preview')
      
      // Fermer la modal
      this.$emit('close')
    },
    
    viewProfile() {
      // Dans un cas réel, on redirigerait vers la page de profil
      this.$router.push('/profile')
      
      // Fermer la modal
      this.$emit('close')
    },

    // Fonctions d'accessibilité
    loadAccessibilitySettings() {
      const settings = localStorage.getItem('accessibilitySettings')
      if (settings) {
        try {
          const { highContrastMode, textSizeLevel } = JSON.parse(settings)
          this.highContrastMode = highContrastMode
          this.textSizeLevel = textSizeLevel
          this.applyTextSize()
        } catch (error) {
          console.error(
            "Erreur lors du chargement des paramètres d'accessibilité:",
            error
          )
        }
      }
    },

    saveAccessibilitySettings() {
      const settings = {
        highContrastMode: this.highContrastMode,
        textSizeLevel: this.textSizeLevel,
      }
      localStorage.setItem('accessibilitySettings', JSON.stringify(settings))
    },

    toggleContrast() {
      this.highContrastMode = !this.highContrastMode
      this.saveAccessibilitySettings()
    },

    applyTextSize() {
      document.body.classList.remove(
        'text-size-1',
        'text-size-2',
        'text-size-3'
      )
      if (this.textSizeLevel > 0) {
        document.body.classList.add(`text-size-${this.textSizeLevel}`)
      }
    },
  },
}
</script>

<style scoped>
/* Styles de base */
.rewards-container {
  position: absolute;
  max-width: 1000px;
  width: 90%;
  padding: 24px;
  background-color: rgb(30, 30, 45);
  border-radius: 24px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  transition: all 0.3s ease;
  z-index: 1000;
  max-height: 90vh;
  overflow-y: auto;
  color: white;
  font-family: 'Comic Sans MS', 'Chalkboard SE', 'Marker Felt', sans-serif;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Boutons de contrôle */
.close-modal-btn {
  position: absolute;
  width: 24px;
  height: 56px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 10;
  font-size: 14px;
}

.close-modal-btn {
  top: 16px;
  right: 16px;
}

.close-modal-btn:before,
.close-modal-btn:after {
  content: '';
  position: absolute;
  width: 24px;
  height: 3px;
  background-color: white;
  transition: background-color 0.3s ease;
}

.close-modal-btn:before {
  transform: rotate(45deg);
}

.close-modal-btn:after {
  transform: rotate(-45deg);
}

.close-modal-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

/* Header profil */
.profile-header {
  display: flex;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px dashed rgba(255, 255, 255, 0.2);
}

.avatar-section {
  position: relative;
  margin-right: 24px;
}

.user-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 4px solid #ffd700;
  object-fit: cover;
  background-color: #333;
}

.level-badge {
  position: absolute;
  bottom: 0;
  right: 0;
  background-color: #4caf50;
  color: white;
  border-radius: 12px;
  padding: 4px 8px;
  font-size: 16px;
  font-weight: bold;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

.user-info {
  flex: 1;
}

.welcome-title {
  font-size: 28px;
  color: #fff;
  margin: 0 0 4px 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.welcome-subtitle {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.8);
  margin: 0 0 16px 0;
}

.user-details {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.user-detail-item {
  background-color: rgba(255, 255, 255, 0.1);
  padding: 6px 12px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.detail-label {
  font-weight: bold;
  color: rgba(255, 255, 255, 0.7);
}

.detail-value {
  color: white;
}

/* Nouvelle section carte de progression */
.progress-map-container {
  background-color: rgba(255, 255, 255, 0.05);
  padding: 20px;
  border-radius: 16px;
  margin-bottom: 24px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
}

.progress-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
  text-align: center;
}

.progress-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #4fc3f7;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.stat-label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  margin-top: 4px;
}

.progress-map {
  position: relative;
  height: 300px;
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 15px;
  overflow: hidden;
  display: flex;
  justify-content: space-around;
  align-items: center;
  flex-wrap: wrap;
  border: 1px dashed rgba(255, 255, 255, 0.3);
}

.journey-path {
  position: absolute;
  top: 50%;
  left: 0;
  width: 100%;
  height: 8px;
  background: linear-gradient(90deg, rgba(76, 175, 80, 0.8), rgba(76, 175, 80, 0.3));
  transform: translateY(-50%);
  z-index: 1;
  border-radius: 4px;
}

.map-badge-node {
  position: relative;
  z-index: 2;
  cursor: pointer;
  transition: transform 0.3s ease;
  margin: 10px;
}

.map-badge-node:hover {
  transform: scale(1.1);
}

.map-badge-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  position: relative;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
  border: 3px solid transparent;
  transition: all 0.3s ease;
  z-index: 3;
}

.map-badge-node.unlocked .map-badge-icon {
  border-color: #4caf50;
  box-shadow: 0 0 15px rgba(76, 175, 80, 0.5);
}

.map-badge-node.active .map-badge-icon {
  border-color: #ff9800;
  box-shadow: 0 0 20px rgba(255, 152, 0, 0.7);
}

.map-badge-lock {
  position: absolute;
  font-size: 18px;
  background-color: rgba(0, 0, 0, 0.5);
  width: 100%;
  height: 100%;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.map-badge-emoji {
  font-size: 30px;
}

.map-badge-tooltip {
  position: absolute;
  width: 140px;
  background-color: rgba(30, 30, 45, 0.95);
  padding: 8px;
  border-radius: 8px;
  left: 50%;
  transform: translateX(-50%) translateY(10px);
  opacity: 0;
  pointer-events: none;
  transition: all 0.3s ease;
  z-index: 10;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  text-align: center;
}

.map-badge-node:hover .map-badge-tooltip {
  opacity: 1;
  transform: translateX(-50%) translateY(5px);
}

.tooltip-title {
  font-weight: bold;
  font-size: 14px;
  margin-bottom: 4px;
  color: white;
}

.tooltip-game {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 4px;
}

.tooltip-status {
  font-size: 12px;
  color: #9e9e9e;
}

.tooltip-status.status-unlocked {
  color: #4caf50;
  font-weight: bold;
}

.map-badge-next {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 2;
}

.next-badge-text {
  position: absolute;
  top: -30px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #ff9800;
  color: white;
  font-size: 12px;
  padding: 3px 8px;
  border-radius: 10px;
  display: inline-block;
  white-space: nowrap;
  font-weight: bold;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  z-index: 4;
}

.pulse-circle {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 66px;
  height: 66px;
  border-radius: 50%;
  border: 3px solid #ff9800;
  animation: pulse-glow 2s infinite;
  z-index: 2;
}

@keyframes pulse-glow {
  0% {
    transform: translate(-50%, -50%) scale(0.9);
    opacity: 0.7;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.2);
    opacity: 0.4;
  }
  100% {
    transform: translate(-50%, -50%) scale(0.9);
    opacity: 0.7;
  }
}

.map-badge-node.active {
  position: relative;
  z-index: 3;
}

.map-legend {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 10px;
}

.legend-item {
  display: flex;
  align-items: center;
  font-size: 12px;
}

.legend-icon {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  margin-right: 6px;
}

.legend-icon.unlocked {
  background-color: #4caf50;
  border: 2px solid rgba(255, 255, 255, 0.5);
}

.legend-icon.locked {
  background-color: #555;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.legend-icon.active {
  background-color: #ff9800;
  border: 2px solid rgba(255, 255, 255, 0.5);
}

.legend-text {
  color: rgba(255, 255, 255, 0.8);
}

/* Section de progression (ancienne version masquée) */
.progress-container {
  display: none;
}

/* État vide - pas de badges */
.empty-state {
  text-align: center;
  padding: 25px;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  margin-bottom: 24px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.empty-badge-icon {
  font-size: 70px;
  margin-bottom: 15px;
  opacity: 0.7;
}

.empty-state h2 {
  font-size: 24px;
  margin-bottom: 8px;
  color: white;
}

.empty-state p {
  font-size: 18px;
  margin-bottom: 20px;
  color: rgba(255, 255, 255, 0.8);
}

.start-button {
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 25px;
  padding: 12px 24px;
  font-size: 18px;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  font-weight: bold;
}

.start-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
}

/* Prochaine activité */
.next-activity {
  margin-bottom: 24px;
}

.next-activity-card {
  display: flex;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.05);
  padding: 16px;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.next-activity-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.3);
  background-color: rgba(255, 255, 255, 0.08);
}

.next-activity-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  flex-shrink: 0;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.activity-emoji {
  font-size: 40px;
}

.next-activity-info {
  flex: 1;
}

.next-activity-info h3 {
  font-size: 20px;
  color: white;
  margin: 0 0 8px 0;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.next-activity-info p {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.8);
  margin: 0 0 16px 0;
}

/* Tous les badges */
.all-badges {
  margin-bottom: 24px;
}

.badges-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 16px;
}

.badge-card {
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.badge-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
  background-color: rgba(255, 255, 255, 0.08);
}

.badge-card.locked {
  opacity: 0.8;
}

.badge-card.unlocked {
  border: 2px solid #4caf50;
  box-shadow: 0 0 10px rgba(76, 175, 80, 0.3);
}

.badge-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
  position: relative;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.lock-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #fff;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  text-shadow: 0 0 4px rgba(0, 0, 0, 0.5);
}

.badge-emoji {
  font-size: 32px;
}

.badge-title {
  font-size: 16px;
  color: white;
  margin: 0 0 8px 0;
  text-align: center;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.badge-status {
  margin-top: 8px;
  font-size: 14px;
  font-weight: bold;
}

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

.badge-unlock-animation h2 {
  color: #FF4081;
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

.close-animation-btn:hover {
  background-color: #D81B60;
  transform: scale(1.05);
}

/* Boutons et actions */
.play-button {
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 8px 16px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
}

.play-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
  background-color: #43a047;
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scaleIn {
  from { transform: scale(0.8); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.next-activity-highlight {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1010;
  pointer-events: none;
}

.highlight-pulse {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: 3px solid #76ff03;
  border-radius: 16px;
  box-shadow: 0 0 15px rgba(118, 255, 3, 0.7);
  animation: highlight-pulse 2s ease-out infinite;
}

.highlight-arrow {
  position: absolute;
  bottom: -10px;
  right: 25%;
  transform: translateX(50%);
  animation: highlight-bounce 2s ease infinite;
}

.highlight-text {
  display: block;
  color: white;
  font-weight: bold;
  font-size: 16px;
  padding: 5px 10px;
  background-color: #58cc02;
  border-radius: 20px;
  white-space: nowrap;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.3);
}

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

.section-highlight {
  position: absolute;
  pointer-events: none;
  z-index: 1050;
  animation: highlight-pulse 2s ease-out infinite;
  border: 3px solid #76ff03;
  border-radius: 16px;
}

@keyframes highlight-bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateX(50%) translateY(0);
  }
  40% {
    transform: translateX(50%) translateY(-15px);
  }
  60% {
    transform: translateX(50%) translateY(-7px);
  }
}

.guide-avatar-container {
  position: absolute;
  z-index: 2000;
  transition: all 0.3s ease;
}

.rewards-container {
  position: absolute;
  z-index: 1090;
}

.guide-container {
  position: fixed;
  z-index: 1100;
}

/* Animation pour le déplacement du guide entre les sections */
@keyframes guide-move {
  0% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
  100% {
    transform: translateY(0);
  }
}

/* Style pour la flèche de guidage */
.guide-arrow {
  position: absolute;
  width: 30px;
  height: 30px;
  background-color: #76ff03;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  box-shadow: 0 0 10px rgba(118, 255, 3, 0.7);
  animation: guide-move 1.5s ease-in-out infinite;
  z-index: 1060;
}

.guide-arrow::before {
  content: '→';
  font-size: 18px;
}

/* Style pour la bulle d'info accompagnant la flèche */
.guide-info-bubble {
  position: absolute;
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 14px;
  white-space: nowrap;
  z-index: 1060;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

.tour-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3);
  z-index: 1040;
  pointer-events: none;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Appliquer l'animation aux éléments du guide */
.guide-element {
  animation: fade-in 0.5s ease-out forwards;
}

.play-button-highlight {
  position: relative;
  z-index: 1055;
  box-shadow: 0 0 20px rgba(118, 255, 3, 0.9);
  transform: scale(1.1);
  transition: all 0.3s ease;
}

/* Animation de pulsation pour attirer l'attention sur un élément */
@keyframes attention-pulse {
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

.attention {
  animation: attention-pulse 1s ease-in-out infinite;
}

/* Boutons d'action */
.action-buttons {
  display: flex;
  gap: 16px;
  margin-top: 24px;
  margin-bottom: 16px;
}

.action-button {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(74, 77, 158, 0.8);
  color: white;
  border: none;
  padding: 16px;
  border-radius: 16px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  gap: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.action-button:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
}

.generate-cv-button {
  background-color: rgba(255, 152, 0, 0.8);
}

.generate-cv-button:hover {
  background-color: rgba(255, 152, 0, 0.9);
}

.profile-button {
  background-color: rgba(33, 150, 243, 0.8);
}

.profile-button:hover {
  background-color: rgba(33, 150, 243, 0.9);
}

.button-icon {
  font-size: 24px;
}

/* Modal de détails de badge */
.badge-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1100;
  backdrop-filter: blur(5px);
}

.badge-modal {
  background-color: rgba(30, 30, 45, 0.95);
  border-radius: 24px;
  padding: 24px;
  max-width: 400px;
  width: 90%;
  position: relative;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
  animation: scaleUp 0.3s ease;
}

.close-button {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.close-button:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

.badge-detail-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.badge-detail-icon {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}

.badge-detail-emoji {
  font-size: 50px;
}

.badge-detail-title {
  font-size: 24px;
  color: white;
  margin: 0 0 8px 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.badge-detail-description {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 16px 0;
}

.badge-achievement, .badge-locked-info {
  background-color: rgba(255, 255, 255, 0.05);
  padding: 16px;
  border-radius: 16px;
  width: 100%;
  margin-bottom: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.achievement-date {
  font-weight: bold;
  color: #4fc3f7;
  margin-bottom: 4px;
  text-shadow: 0 0 5px rgba(79, 195, 247, 0.5);
}

.achievement-game {
  color: rgba(255, 255, 255, 0.8);
}

.badge-hint {
  display: flex;
  align-items: flex-start;
  margin-bottom: 8px;
}

.hint-icon {
  font-size: 24px;
  margin-right: 8px;
  text-shadow: 0 0 5px rgba(255, 215, 0, 0.5);
}

.badge-hint p {
  margin: 0;
  color: rgba(255, 255, 255, 0.9);
  font-size: 16px;
  text-align: left;
}

.badge-game {
  color: rgba(255, 255, 255, 0.8);
  font-style: italic;
  text-align: left;
}

.badge-actions {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-top: 15px;
}

.play-now-button, .share-button {
  padding: 12px 24px;
  border-radius: 24px;
  font-size: 16px;
  font-weight: bold;
  color: white;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.play-now-button {
  background-color: #4caf50;
}

.share-button {
  background-color: #2196f3;
}

.play-now-button:hover, .share-button:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
}

/* Animations supplementaires */
@keyframes scaleUp {
  from {
    transform: scale(0.8);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

/* Mode contraste élevé */
.high-contrast {
  color: white;
  background-color: black;
}

.high-contrast.rewards-container {
  background-color: #000;
  border: 2px solid #fff;
}

.high-contrast .badge-card,
.high-contrast .next-activity-card,
.high-contrast .progress-map-container,
.high-contrast .empty-state,
.high-contrast .badge-achievement,
.high-contrast .badge-locked-info,
.high-contrast .badge-modal,
.high-contrast .progress-map {
  background-color: #222;
  border: 2px solid #fff;
}

.high-contrast .map-badge-node.unlocked .map-badge-icon {
  border-color: #fff;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.7);
}

.high-contrast .user-detail-item {
  background-color: #333;
  border: 1px solid #fff;
}

.high-contrast .progress-bar-container {
  background-color: #333;
  border: 1px solid #fff;
}

.high-contrast .section-title,
.high-contrast .welcome-title,
.high-contrast .badge-title,
.high-contrast .badge-detail-title,
.high-contrast .next-activity-info h3,
.high-contrast .stat-number {
  color: #fff;
  text-shadow: none;
}

/* Media queries pour la responsivité */
@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .avatar-section {
    margin-right: 0;
    margin-bottom: 16px;
  }
  
  .user-details {
    justify-content: center;
  }
  
  .badges-grid {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .next-activity-card {
    flex-direction: column;
    text-align: center;
  }
  
  .next-activity-icon {
    margin-right: 0;
    margin-bottom: 12px;
  }
  
  .progress-stats {
    flex-wrap: wrap;
    gap: 15px;
  }
  
  .progress-map {
    height: auto;
    min-height: 350px;
    padding: 30px 10px;
  }
  
  .map-badge-node {
    margin: 8px;
  }
  
  .map-legend {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
    margin-left: 20px;
  }
}

@media (max-width: 480px) {
  .rewards-container {
    padding: 16px 12px;
    border-radius: 16px;
  }
  
  .badges-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .section-title {
    font-size: 20px;
  }
  
  .welcome-title {
    font-size: 24px;
  }
  
  .welcome-subtitle {
    font-size: 16px;
  }
  
  .map-badge-icon {
    width: 50px;
    height: 50px;
  }
  
  .map-badge-emoji {
    font-size: 24px;
  }
  
  .stat-number {
    font-size: 24px;
  }
  
  .progress-map {
    min-height: 300px;
  }
}
</style>