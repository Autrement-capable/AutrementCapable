<template>
  <!-- Début du template - tout le contenu avant neural-progress-map reste inchangé -->
  <div v-if="showBadgeUnlockAnimation" class="badge-unlock-overlay">
    <div class="badge-unlock-animation">
      <div class="badge-icon" v-if="newlyUnlockedBadge">{{ newlyUnlockedBadge.icon }}</div>
      <h2>Badge débloqué !</h2>
      <h3 v-if="newlyUnlockedBadge">{{ newlyUnlockedBadge.title }}</h3>
      <p v-if="newlyUnlockedBadge">{{ newlyUnlockedBadge.description }}</p>
      <button @click="closeBadgeAnimation" class="close-animation-btn">Continuer</button>
    </div>
  </div>
  <div 
    class="rewards-container" 
    :class="[{ 'high-contrast': highContrastMode }, themeClass]"
    :style="getScrollbarStyle()"
  >
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

    <div class="next-activity" v-if="hasUnlockedBadges || nextBadge" ref="nextActivitySection">
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
            :class="{ 'play-button-highlight': highlightPlayButtonBool }"
            @click="goToGame(nextBadge.gameRoute)"
            ref="playButton"
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
          <!-- Affichage du pourcentage de complétion si disponible -->
          <div v-if="badge.completion !== undefined" class="badge-completion">
            <div class="badge-completion-bar">
              <div class="badge-completion-fill" :style="{ width: Math.round((badge.completion || 0) * 100) + '%' }"></div>
            </div>
            <span class="badge-completion-text">{{ Math.round((badge.completion || 0) * 100) }}%</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Nouvelle organisation de la carte de progression -->
    <div class="neural-progress-map">
      <!-- Chemin des jeux à gauche -->
      <div class="games-path">
        <!-- Jeu de Vitesse -->
        <div class="games-path">
          <!-- Jeu de Vitesse -->
          <div class="game-node" 
            :class="{'game-unlocked': badges[1].unlocked, 'game-active': badges[1].id === nextBadge.id && !badges[1].unlocked}"
            @click="showBadgeDetails(badges[1])"
          >
            <div class="game-node-icon" :style="{ backgroundColor: badges[1].unlocked ? badges[1].iconColor : '#555' }">
              <div v-if="!badges[1].unlocked" class="game-node-lock">🔒</div>
              <span class="game-node-emoji">{{ badges[1].icon }}</span>
            </div>
            
            <!-- Connexion vers le profil -->
            <div class="game-to-profile-connection" :class="{'connection-active': badges[1].unlocked}"></div>
            
            <!-- Indicateur si c'est le prochain jeu -->
            <!-- <div v-if="badges[1].id === nextBadge.id && !badges[1].unlocked" class="game-next-indicator">
              <div class="game-pulse-circle"></div>
            </div> -->
          </div>
          
          <!-- Jeu 2 -->
          <div class="game-node" 
            :class="{'game-unlocked': badges[2].unlocked, 'game-active': badges[2].id === nextBadge.id && !badges[2].unlocked}"
            @click="showBadgeDetails(badges[2])"
          >
            <div class="game-node-icon" :style="{ backgroundColor: badges[2].unlocked ? badges[2].iconColor : '#555' }">
              <div v-if="!badges[2].unlocked" class="game-node-lock">🔒</div>
              <span class="game-node-emoji">{{ badges[2].icon }}</span>
            </div>
            <div class="game-to-profile-connection" :class="{'connection-active': badges[2].unlocked}"></div>
            <!-- <div v-if="badges[2].id === nextBadge.id && !badges[2].unlocked" class="game-next-indicator">
              <div class="game-pulse-circle"></div>
            </div> -->
          </div>
          
          <!-- Jeu 3 -->
          <div class="game-node" 
            :class="{'game-unlocked': badges[3].unlocked, 'game-active': badges[3].id === nextBadge.id && !badges[3].unlocked}"
            @click="showBadgeDetails(badges[3])"
          >
            <div class="game-node-icon" :style="{ backgroundColor: badges[3].unlocked ? badges[3].iconColor : '#555' }">
              <div v-if="!badges[3].unlocked" class="game-node-lock">🔒</div>
              <span class="game-node-emoji">{{ badges[3].icon }}</span>
            </div>
            <div class="game-to-profile-connection" :class="{'connection-active': badges[3].unlocked}"></div>
            <!-- <div v-if="badges[3].id === nextBadge.id && !badges[3].unlocked" class="game-next-indicator">
              <div class="game-pulse-circle"></div>
            </div> -->
          </div>
          
          <!-- Jeu 4 -->
          <div class="game-node" 
            :class="{'game-unlocked': badges[4].unlocked, 'game-active': badges[4].id === nextBadge.id && !badges[4].unlocked}"
            @click="showBadgeDetails(badges[4])"
          >
            <div class="game-node-icon" :style="{ backgroundColor: badges[4].unlocked ? badges[4].iconColor : '#555' }">
              <div v-if="!badges[4].unlocked" class="game-node-lock">🔒</div>
              <span class="game-node-emoji">{{ badges[4].icon }}</span>
            </div>
            <div class="game-to-profile-connection" :class="{'connection-active': badges[4].unlocked}"></div>
            <!-- <div v-if="badges[4].id === nextBadge.id && !badges[4].unlocked" class="game-next-indicator">
              <div class="game-pulse-circle"></div>
            </div> -->
          </div>
          
          <!-- Jeu 5 -->
          <div class="game-node" 
            :class="{'game-unlocked': badges[5].unlocked, 'game-active': badges[5].id === nextBadge.id && !badges[5].unlocked}"
            @click="showBadgeDetails(badges[5])"
          >
            <div class="game-node-icon" :style="{ backgroundColor: badges[5].unlocked ? badges[5].iconColor : '#555' }">
              <div v-if="!badges[5].unlocked" class="game-node-lock">🔒</div>
              <span class="game-node-emoji">{{ badges[5].icon }}</span>
            </div>
            <div class="game-to-profile-connection" :class="{'connection-active': badges[5].unlocked}"></div>
            <!-- <div v-if="badges[5].id === nextBadge.id && !badges[5].unlocked" class="game-next-indicator">
              <div class="game-pulse-circle"></div>
            </div> -->
          </div>
          
          <!-- Jeu 6 -->
          <div class="game-node" 
            :class="{'game-unlocked': badges[7].unlocked, 'game-active': badges[7].id === nextBadge.id && !badges[7].unlocked}"
            @click="showBadgeDetails(badges[7])"
          >
            <div class="game-node-icon" :style="{ backgroundColor: badges[7].unlocked ? badges[7].iconColor : '#555' }">
              <div v-if="!badges[7].unlocked" class="game-node-lock">🔒</div>
              <span class="game-node-emoji">{{ badges[7].icon }}</span>
            </div>
            <div class="game-to-profile-connection" :class="{'connection-active': badges[7].unlocked}"></div>
            <!-- <div v-if="badges[7].id === nextBadge.id && !badges[7].unlocked" class="game-next-indicator">
              <div class="game-pulse-circle"></div>
            </div> -->
          </div>
        </div>
      </div>
        
      <div class="main-path">
        <div class="main-path-container">
          <!-- Profil -->
          <div class="main-node profile-node">
            <div class="main-node-icon" :class="{'node-complete': getNodeCompletion(0)}">
              <span class="node-emoji">👤</span>
              <div class="node-completion-circle">
                <svg viewBox="0 0 36 36">
                  <path class="node-progress-bg"
                    d="M18 2.0845
                      a 15.9155 15.9155 0 0 1 0 31.831
                      a 15.9155 15.9155 0 0 1 0 -31.831"
                  />
                  <path class="node-progress-fill"
                    d="M18 2.0845
                      a 15.9155 15.9155 0 0 1 0 31.831
                      a 15.9155 15.9155 0 0 1 0 -31.831"
                    :stroke-dasharray="`${getNodeCompletion(0) ? 100 : 0}, 100`"
                  />
                </svg>
              </div>
              <span class="node-label">Profil</span>
            </div>
          </div>
          
          <div class="main-connection horizontal" :class="{'connection-active': getNodeCompletion(9)}"></div>
          
          <div class="main-node cv-node">
            <div class="main-node-icon" :class="{'node-complete': getNodeCompletion(6)}">
              <span class="node-emoji">📄</span>
              <div class="node-completion-circle">
                <svg viewBox="0 0 36 36">
                  <path class="node-progress-bg"
                    d="M18 2.0845
                      a 15.9155 15.9155 0 0 1 0 31.831
                      a 15.9155 15.9155 0 0 1 0 -31.831"
                  />
                  <path class="node-progress-fill"
                    d="M18 2.0845
                      a 15.9155 15.9155 0 0 1 0 31.831
                      a 15.9155 15.9155 0 0 1 0 -31.831"
                    :stroke-dasharray="`${getNodeCompletion(6) ? 100 : 0}, 100`"
                  />
                </svg>
              </div>
              <span class="node-label">CV</span>
            </div>
          </div>
          
          <div class="main-connection horizontal" :class="{'connection-active': getNodeCompletion(6)}"></div>
          
          <div class="main-node formation-node">
            <div class="main-node-icon" :class="{'node-complete': getNodeCompletion(8)}">
              <span class="node-emoji">🎓</span>
              <div class="node-completion-circle">
                <svg viewBox="0 0 36 36">
                  <path class="node-progress-bg"
                    d="M18 2.0845
                      a 15.9155 15.9155 0 0 1 0 31.831
                      a 15.9155 15.9155 0 0 1 0 -31.831"
                  />
                  <path class="node-progress-fill"
                    d="M18 2.0845
                      a 15.9155 15.9155 0 0 1 0 31.831
                      a 15.9155 15.9155 0 0 1 0 -31.831"
                    :stroke-dasharray="`${getNodeCompletion(8) ? 100 : 0}, 100`"
                  />
                </svg>
              </div>
              <span class="node-label">Formation</span>
            </div>
          </div>
        </div>
      </div>
        
      <!-- Indicateur de progression global reste inchangé -->
      <div class="progress-indicator">
        <div class="progress-percentage">{{ Math.round(progressPercentage) }}%</div>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: `${progressPercentage}%` }"></div>
        </div>
        <div class="progress-label">Avancement du parcours</div>
      </div>
    </div>

    <!-- Boutons d'action -->
    <div class="action-buttons">
      <button 
        class="action-button generate-cv-button" 
        @click="generateCV"
        :class="{ 'locked-button': !cvUnlocked }"
      >
        <span class="button-icon">📄</span>
        Créer mon CV
        <span v-if="!cvUnlocked" class="lock-icon">🔒</span>
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
  </div>
  <guide-avatar
    v-if="internalShowGuide"
    guide-name="Flamou"
    :forced-message="profileGuideMessage"
    :forced-options="profileGuideOptions"
    :force-show-message="profileTourActive || forceShowGuide"
    :custom-position="guideCustomPosition"
    :active-section-id="profileTourActive ? profileTourSections[profileTourStep].id : null"
    context="profile"
    :auto-show-delay="0"
    :class="{ 'guide-top-left': !profileTourActive && !forceShowGuide }"
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
import AuthService from '@/services/AuthService.js'

export default {
  name: 'RewardsComponent',
  components: {
    GuideAvatar,
  },
  props: {
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
          unlocked: true,
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
          unlocked: true,
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
          unlocked: true,
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
          unlocked: true,
          hint: "Essaie tous les préréglages dans l'environnement de personnalisation",
          game: 'Environnement',
          gameRoute: '/environment',
          shareable: true,
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
          description: 'Tu as découvert 5 métiers différents',
          icon: '👷',
          iconColor: '#FF9800',
          unlocked: true,
          hint: 'Explore au moins 5 fiches métier',
          game: 'Découverte des métiers',
          gameRoute: '/metiers',
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
        {
          id: 9,
          title: 'Tous les jeux finis',
          description: 'Bravo ! Tu as terminé tous les jeux disponibles !',
          icon: '🏆',
          iconColor: '#4CAF50',
          unlocked: false,
          hint: 'Termine tous les jeux pour débloquer ce badge',
          game: 'Tous les jeux',
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
          id: 'next-activity',
          name: 'Prochaine activité',
          selector: '.next-activity',
          description: "Ici tu trouveras ta prochaine activité recommandée. C'est en jouant que tu pourras débloquer de nouveaux badges !"
        },
        {
          id: 'badges-grid',
          name: 'Mes badges',
          selector: '.all-badges',
          description: "Cette section affiche tous tes badges, débloqués ou non. Clique sur un badge pour voir plus de détails et comment le débloquer si tu ne l'as pas encore."
        },
        {
          id: 'neural-progress',
          name: 'Carte de progression',
          selector: '.neural-progress-map',
          description: "Cette carte interactive montre ta progression dans le parcours ! À gauche, tu as les jeux que tu peux débloquer. Au centre, tu vois ton avancement principal à travers le profil, le CV et la formation. Les connexions colorées montrent les étapes débloquées."
        },
        {
          id: 'games-path',
          name: 'Chemin des jeux',
          selector: '.games-path',
          description: "Voici les différents jeux disponibles. Chaque jeu débloqué est coloré et connecté à ton profil. Les jeux verrouillés s'ouvriront au fur et à mesure de ta progression !"
        },
        {
          id: 'main-path',
          name: 'Chemin principal',
          selector: '.main-path',
          description: "Ce chemin montre les étapes principales de ton parcours : compléter ton profil, créer ton CV et trouver une formation. Chaque étape se débloque en réalisant les activités précédentes."
        },
        {
          id: 'progress-indicator',
          name: 'Indicateur de progression',
          selector: '.progress-indicator',
          description: "Cet indicateur montre ton pourcentage d'avancement dans l'ensemble du parcours. Plus tu débloques de badges, plus la barre progresse !"
        },
        {
          id: 'actions',
          name: 'Actions',
          selector: '.action-buttons',
          description: "Le bouton 'Mon profil' te permet d'accéder à ton profil complet et le bouton 'Créer mon CV' te permet de générer un CV professionnel basé sur tes compétences. Il sera disponible quand tu auras fini ton parcours !"
        }
      ],
      
      // Mise à jour des messages et options du guide pour inclure le tour du profil
      profileGuideMessage: "Bienvenue sur ton profil ! Veux-tu que je te fasse visiter pour découvrir toutes les fonctionnalités ?",
      profileGuideOptions: [
        { text: "Oui, montre-moi tout !", action: "startProfileTour" },
      ],
      
      // Overlay pour le tour guidé
      showTourOverlay: false,
      guideCustomPosition: {
        position: 'fixed',
        top: '20px',
        left: '20px',
        zIndex: 2500
      },
      forceShowGuide: false,
      highlightPlayButtonBool: false,
      cvUnlocked: false,
    }
  },
  computed: {
    progressPercentage() {
      return (this.unlockedBadgesCount / this.totalBadgesCount) * 100;
    },
    themeClass() {
      return this.currentTheme || localStorage.getItem('dashboard-theme') || 'cosmic';
    },
    unlockedBadgesCount() {
      return this.badges.filter((badge) => badge.unlocked).length
    },
    totalBadgesCount() {
      return this.badges.length
    },
    hasUnlockedBadges() {
      return this.unlockedBadgesCount > 0
    },
    nextBadge() {
      // Trouve le premier badge non débloqué (en excluant le badge "Tous les jeux finis" qui se débloque automatiquement)
      const nextBadge = this.badges.find(badge => !badge.unlocked && badge.id !== 9);
      return nextBadge || this.badges[0];
    }
  },
  watch: {
    internalShowGuide: {
      handler(newValue) {
        if (newValue && !this.profileTourActive && !this.forceShowGuide) {
          this.$nextTick(() => {
            this.positionGuideByCloseButton();
          });
        }
      }
    },
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

    // Charger la progression des jeux pour les badges
    this.fetchGamesProgress();
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
    window.addEventListener('resize', this.calculateNodeConnections);
    window.addEventListener('resize', this.calculateGameToProfileConnections);
    
    // Écouter l'événement pour mettre en évidence le bouton "Jouer maintenant"
    eventBus.on('highlight-play-button', () => {
      this.highlightPlayButton();
    });
    this.$nextTick(() => {
      if (this.internalShowGuide && !this.profileTourActive && !this.forceShowGuide) {
        this.positionGuideByCloseButton();
      }
      this.bubbleObserver = this.maintainBubbleIconDistance();
      
      // Calculer les connexions
      this.calculateNodeConnections();
      this.calculateGameToProfileConnections(); // Calcul initial des nouvelles connexions
    });
  },
  beforeUnmount() {
    // Nettoyer les évènements
    window.removeEventListener('resize', this.updateHighlights);
    window.removeEventListener('resize', this.calculateNodeConnections);
    window.removeEventListener('resize', this.calculateGameToProfileConnections); // Nettoyage du nouvel écouteur
    
    eventBus.off('highlight-play-button');
    this.removeHighlights();
    if (this.bubbleObserver) {
      this.bubbleObserver.disconnect();
    }
  },
  methods: {
    checkAllGamesCompleted() {
      // Vérifier si tous les jeux sont terminés pour débloquer le badge "Tous les jeux finis"
      if (this.canUnlockAllGamesCompleted()) {
        const allGamesCompletedBadge = this.badges.find((badge) => badge.id === 9)
        if (allGamesCompletedBadge && !allGamesCompletedBadge.unlocked) {
          allGamesCompletedBadge.unlocked = true
          allGamesCompletedBadge.dateUnlocked = new Date().toISOString().split('T')[0]
          this.saveBadges()
        }
      }
    },

    /**
     * Vérifie si tous les jeux sont débloqués pour activer le badge "Tous les jeux finis"
     * @returns {boolean} - true si tous les jeux sont débloqués
     */
    canUnlockAllGamesCompleted() {
      // IDs des badges de jeux (excluant le profil, CV, formation et le badge "Tous les jeux finis")
      const gameIds = [1, 2, 3, 4, 5, 7];
      
      // Vérifie si tous les badges de jeux sont débloqués
      return gameIds.every(id => {
        const badge = this.badges.find(badge => badge.id === id);
        return badge && badge.unlocked;
      });
    },

    calculateGameToProfileConnections() {
      // Attendre que le DOM soit chargé
      this.$nextTick(() => {
        // Récupérer l'élément du profil et tous les jeux
        const profileNode = document.querySelector('.profile-node .main-node-icon');
        const gameNodes = document.querySelectorAll('.game-node');
        
        if (!profileNode) {
          console.error("Élément profil introuvable");
          return;
        }
        
        // Récupérer les coordonnées du nœud de profil
        const profileRect = profileNode.getBoundingClientRect();
        const containerRect = document.querySelector('.neural-progress-map').getBoundingClientRect();
        
        // Position du centre du profil relative au conteneur
        const profileCenterX = profileRect.left + profileRect.width / 2 - containerRect.left;
        const profileCenterY = profileRect.top + profileRect.height / 2 - containerRect.top;
        
        // Pour chaque jeu, calculer et ajuster sa connexion vers le profil
        gameNodes.forEach((gameNode) => {
          const connectionToProfile = gameNode.querySelector('.game-to-profile-connection');
          
          if (connectionToProfile) {
            // Cibler spécifiquement l'icône du jeu au lieu du nœud entier
            const gameIconNode = gameNode.querySelector('.game-node-icon');
            // const gameNodeRect = gameNode.getBoundingClientRect();
            const gameIconRect = gameIconNode.getBoundingClientRect();
            
            // Obtenir les coordonnées du centre de l'icône du jeu
            const gameIconCenterX = gameIconRect.left + gameIconRect.width / 2 - containerRect.left;
            const gameIconCenterY = gameIconRect.top + gameIconRect.height / 2 - containerRect.top;
            
            // Calculer la distance et l'angle entre le centre de l'icône et le profil
            const dx = profileCenterX - gameIconCenterX;
            const dy = profileCenterY - gameIconCenterY;
            const distance = Math.sqrt(dx * dx + dy * dy);
            const angle = Math.atan2(dy, dx) * (180 / Math.PI);
            
            // Appliquer la transformation
            connectionToProfile.style.width = `${distance - 25}px`; // Ajuster la longueur
            connectionToProfile.style.transform = `rotate(${angle}deg)`;
            
            // Position absolue pour chaque ligne
            connectionToProfile.style.position = 'absolute';
            connectionToProfile.style.top = `${gameIconCenterY}px`;
            connectionToProfile.style.left = `${gameIconCenterX}px`;
            connectionToProfile.style.transformOrigin = 'left center'; // Point de pivot à gauche
            connectionToProfile.style.zIndex = '5';
          }
        });
      });
    },
    /**
     * Vérifie si un nœud principal est complété 
     * @param {number} nodeId - ID du badge correspondant au nœud
     * @returns {boolean} - true si le nœud est complété
     */
    getNodeCompletion(nodeId) {
      // Trouver le badge correspondant
      const badge = this.badges.find(badge => badge.id === nodeId);
      return badge ? badge.unlocked : false;
    },

    /**
     * Génère la couleur de fond des connexions en fonction de leur état
     * @param {boolean} isActive - Si la connexion est active
     * @returns {object} - Styles CSS pour la connexion
     */
    getConnectionStyle(isActive) {
      return {
        background: isActive 
          ? 'linear-gradient(90deg, #4caf50, rgba(76, 175, 80, 0.3))' 
          : 'rgba(255, 255, 255, 0.2)',
        boxShadow: isActive ? '0 0 8px rgba(76, 175, 80, 0.7)' : 'none'
      };
    },

    /**
     * Vérifie si tous les jeux sont débloqués pour activer le CV
     * @returns {boolean} - true si tous les jeux sont débloqués
     */
    canUnlockCV() {
      // IDs des badges de jeux (excluant le profil, CV et formation)
      const gameIds = [1, 2, 3, 4, 5, 7];
      
      // Vérifie si tous les badges de jeux sont débloqués
      return gameIds.every(id => {
        const badge = this.badges.find(badge => badge.id === id);
        return badge && badge.unlocked;
      });
    },

    /**
     * Vérifie si le CV est débloqué pour activer la formation
     * @returns {boolean} - true si le CV est débloqué
     */
    canUnlockFormation() {
      // Trouver le badge du CV (ID 6)
      const cvBadge = this.badges.find(badge => badge.id === 6);
      return cvBadge && cvBadge.unlocked;
    },

    /**
     * Met à jour les états des badges et connexions après un changement
     * À appeler après avoir débloqué un badge
     */
    updateProgressPath() {
      // Vérifier si tous les jeux sont terminés pour débloquer le badge "Tous les jeux finis"
      if (this.canUnlockAllGamesCompleted()) {
        const allGamesCompletedBadge = this.badges.find(badge => badge.id === 9);
        if (allGamesCompletedBadge && !allGamesCompletedBadge.unlocked) {
          // Marquer le badge "Tous les jeux finis" comme débloqué
          allGamesCompletedBadge.unlocked = true;
          allGamesCompletedBadge.dateUnlocked = new Date().toISOString().split('T')[0];
          
          // Sauvegarder l'état des badges
          this.saveBadges();
          
          // Animation de déblocage de badge
          this.newlyUnlockedBadge = allGamesCompletedBadge;
          setTimeout(() => {
            this.showBadgeUnlockAnimation = true;
          }, 500);
        }
      }
      // Vérifier si tous les jeux sont terminés pour débloquer le CV
      if (this.canUnlockCV()) {
        // Trouver le badge du CV
        const cvBadge = this.badges.find(badge => badge.id === 6);
        if (cvBadge && !cvBadge.unlocked) {
          // Marquer le CV comme débloqué
          cvBadge.unlocked = true;
          cvBadge.dateUnlocked = new Date().toISOString().split('T')[0];
          
          // Activer la fonctionnalité de CV
          this.cvUnlocked = true;
          
          // Sauvegarder l'état des badges
          this.saveBadges();
          
          // Animation de déblocage de badge
          this.newlyUnlockedBadge = cvBadge;
          setTimeout(() => {
            this.showBadgeUnlockAnimation = true;
          }, 1000);
        }
      }
      
      // Vérifier si le CV est terminé pour débloquer la formation
      if (this.canUnlockFormation()) {
        // Trouver le badge de formation
        const formationBadge = this.badges.find(badge => badge.id === 8);
        if (formationBadge && !formationBadge.unlocked) {
          // Ne débloque pas automatiquement la formation,
          // mais active visuellement la connexion entre CV et Formation
          // pour indiquer que l'utilisateur peut s'inscrire à une formation
        }
      }
    },
    // Méthode pour calculer les positions des connexions entre nœuds
    calculateNodeConnections() {
      // Cette méthode est appelée après le rendu du composant
      this.$nextTick(() => {
        const nodes = document.querySelectorAll('.neural-node');
        
        // Pour chaque nœud (sauf le dernier qui n'a pas de connexion sortante)
        for (let i = 0; i < nodes.length - 1; i++) {
          const currentNode = nodes[i];
          const nextNode = nodes[i + 1];
          
          if (currentNode && nextNode) {
            const connection = currentNode.querySelector('.neural-connection');
            
            if (connection) {
              // Récupérer les positions des nœuds
              const currentRect = currentNode.getBoundingClientRect();
              const nextRect = nextNode.getBoundingClientRect();
              
              // Calculer l'angle et la distance entre les nœuds
              const dx = nextRect.left - currentRect.left;
              const dy = nextRect.top - currentRect.top;
              const distance = Math.sqrt(dx * dx + dy * dy);
              const angle = Math.atan2(dy, dx) * (180 / Math.PI);
              
              // Appliquer la transformation
              connection.style.width = `${distance - 60}px`; // Soustraire la taille des icônes
              connection.style.transform = `rotate(${angle}deg)`;
              connection.style.top = '30px'; // Centre de l'icône
              connection.style.left = '30px'; // Centre de l'icône
            }
          }
        }
        
        // Mettre à jour les connexions vers le profil
        this.updateProfileConnections();
      });
    },

    // Mettre à jour les connexions vers le profil
    updateProfileConnections() {
      const profileIcon = document.querySelector('.profile-icon');
      const nodes = document.querySelectorAll('.neural-node');
      
      if (profileIcon && nodes.length > 0) {
        const profileRect = profileIcon.getBoundingClientRect();
        const connectionLines = document.querySelectorAll('.profile-connection-line');
        
        // Sélectionner trois nœuds stratégiques pour les connexions (début, milieu, fin)
        const connectToNodes = [
          nodes[0], // Premier nœud
          nodes[Math.floor(nodes.length / 2)], // Nœud du milieu
          nodes[nodes.length - 1] // Dernier nœud
        ];
        
        // Mettre à jour chaque ligne de connexion
        connectionLines.forEach((line, index) => {
          if (connectToNodes[index]) {
            const nodeRect = connectToNodes[index].getBoundingClientRect();
            
            // Calculer l'angle et la distance
            const dx = nodeRect.left - profileRect.left;
            const dy = nodeRect.top - profileRect.top;
            const distance = Math.sqrt(dx * dx + dy * dy);
            const angle = Math.atan2(dy, dx) * (180 / Math.PI);
            
            // Appliquer la transformation
            line.style.width = `${distance - 40}px`;
            line.style.transform = `rotate(${angle + 180}deg)`;
          }
        });
      }
    },
    getConnectionActive(connectionIndex) {
      // Calculer le nombre minimal de badges débloqués pour activer cette connexion
      const totalConnections = 3; // Nombre de connexions vers le profil
      const badgesPerConnection = Math.ceil(this.totalBadgesCount / totalConnections);
      
      // Déterminer combien de badges doivent être débloqués pour cette connexion
      const requiredBadges = badgesPerConnection * connectionIndex;
      
      // La connexion est active si le nombre de badges débloqués est >= au nombre requis
      return this.unlockedBadgesCount >= requiredBadges;
    },

    // Méthode mise à jour pour calculer le pourcentage de progression
    calculateProgressPercentage() {
      return (this.unlockedBadgesCount / this.totalBadgesCount) * 100;
    },
    getScrollbarStyle() {
      // Définir les couleurs par thème
      const themeColors = {
        cosmic: {
          thumbColor: '#7986cb',
          thumbHoverColor: '#3f51b5',
          trackColor: 'rgba(13, 13, 35, 0.5)'
        },
        light: {
          thumbColor: '#f0f0f0',
          thumbHoverColor: '#e0e0e0',
          trackColor: 'rgba(240, 240, 240, 0.5)'
        },
        ocean: {
          thumbColor: '#4fc3f7',
          thumbHoverColor: '#29b6f6',
          trackColor: 'rgba(13, 71, 161, 0.2)'
        },
        cyberpunk: {
          thumbColor: '#ff4081',
          thumbHoverColor: '#f50057',
          trackColor: 'rgba(171, 71, 188, 0.2)'
        },
        forest: {
          thumbColor: '#66bb6a',
          thumbHoverColor: '#4caf50',
          trackColor: 'rgba(56, 142, 60, 0.2)'
        },
        snow: {
          thumbColor: '#90caf9',
          thumbHoverColor: '#64b5f6',
          trackColor: 'rgba(144, 202, 249, 0.2)'
        }
      };
      
      // Utiliser le thème actuel ou le thème par défaut (cosmic)
      const currentTheme = this.themeClass;
      const colors = themeColors[currentTheme] || themeColors.cosmic;
      
      // Si on est en mode contraste élevé, remplacer les couleurs
      if (this.highContrastMode) {
        return {
          '--scrollbar-thumb': '#ffffff',
          '--scrollbar-thumb-hover': '#e0e0e0',
          '--scrollbar-track': '#333333'
        };
      }
      
      // Retourner les variables CSS
      return {
        '--scrollbar-thumb': colors.thumbColor,
        '--scrollbar-thumb-hover': colors.thumbHoverColor,
        '--scrollbar-track': colors.trackColor
      };
    },
    adjustGuideBubblePosition(position) {
      // Attendre que le DOM soit à jour
      setTimeout(() => {
        // Essayer différents sélecteurs possibles pour la bulle du guide
        const selectors = [
          '.guide-bubble', 
          '.guide-message', 
          '.message-container',
          '.guide-tour-active > div:not(:first-child)',
          '.guide-avatar > div:not(:first-child)'
        ];
        
        let guideBubble = null;
        for (const selector of selectors) {
          guideBubble = document.querySelector(selector);
          if (guideBubble) break;
        }
        
        if (guideBubble) {
          if (position === 'tour') {
            // La bulle est positionnée sous l'icône avec un décalage constant
            guideBubble.style.position = 'absolute';
            guideBubble.style.top = '60px';
            guideBubble.style.left = '0';
            guideBubble.style.marginTop = '0';
            guideBubble.style.marginLeft = '-50%';
            guideBubble.style.transform = 'translateX(0)';
          } else if (position === 'top-left') {
            // En haut à gauche, la bulle est à droite de l'icône
            guideBubble.style.position = 'absolute';
            guideBubble.style.top = '0';
            guideBubble.style.left = '60px';
            guideBubble.style.marginTop = '0';
            guideBubble.style.marginLeft = '0';
            guideBubble.style.transform = 'translateX(0)';
          }
        }
      }, 50);
    },

    // Méthode pour positionner le guide à droite pendant le tour
    positionGuideDuringTour() {
      const rewardsContainer = document.querySelector('.rewards-container');
      if (rewardsContainer) {
        const rect = rewardsContainer.getBoundingClientRect();
        
        this.guideCustomPosition = {
          position: 'fixed',
          top: '80px',
          left: `${rect.right + 20}px`,
          zIndex: 2500
        };

        this.$nextTick(() => {
          const guideElement = document.querySelector('.guide-avatar');
          if (guideElement) {
            Object.assign(guideElement.style, {
              position: 'fixed',
              top: '80px',
              left: `${rect.right + 20}px`,
              zIndex: '2500'
            });
            
            guideElement.classList.remove('guide-top-left');
            guideElement.classList.add('guide-tour-active');
            
            this.adjustGuideBubblePosition('tour');
          }
        });
      }
    },
    /**
     * Positionne le guide en haut à gauche quand la bulle n'est pas ouverte
     */
     positionGuideTopLeft() {
      // Position en haut à gauche
      this.guideCustomPosition = {
        position: 'fixed',
        top: '20px',
        left: '20px',
        zIndex: 2500
      };
      
      // Appliquer directement au DOM
      this.$nextTick(() => {
        const guideElement = document.querySelector('.guide-avatar');
        if (guideElement) {
          Object.assign(guideElement.style, {
            position: 'fixed',
            top: '20px',
            left: '20px',
            zIndex: '2500'
          });
          
          guideElement.classList.add('guide-top-left');
          guideElement.classList.remove('guide-tour-active');
          
          // Ajuster la position de la bulle pour qu'elle soit à droite de l'icône
          this.adjustGuideBubblePosition('top-left');
        }
      });
    },
    /**
     * Positionne le guide près du bouton de fermeture quand la bulle n'est pas ouverte
     */
    positionGuideByCloseButton() {
      // Ne rien faire si le guide est déjà positionné ailleurs (comme pendant le tour)
      if (this.profileTourActive || this.forceShowGuide) {
        return;
      }

      // Trouver le bouton de fermeture
      const closeButton = document.querySelector('.close-modal-btn');
      if (closeButton) {
        const rect = closeButton.getBoundingClientRect();
        
        // Positionner le guide à gauche du bouton fermer
        const position = {
          position: 'fixed',
          top: `${rect.top}px`,
          left: `${rect.left - 75}px`,
          zIndex: 2500
        };
        
        // Mettre à jour la position du guide
        this.guideCustomPosition = position;
      }
    },
    /**
     * Met à jour la position du guide lorsqu'elle est modifiée par le composant guide
     */
     updateGuidePosition(position) {
      if (this.profileTourActive) {
        this.positionGuideDuringTour();
      } else if (this.forceShowGuide) {
        this.guideCustomPosition = position;
      } else {
        this.positionGuideTopLeft();
      }
    },
    /**
     * Met à jour les mises en évidence lors du redimensionnement de la fenêtre
     */
    updateHighlights() {
      if (this.profileTourActive && this.profileTourStep < this.profileTourSections.length) {
        const section = this.profileTourSections[this.profileTourStep];
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
      
      if (this.profileTourStep >= this.profileTourSections.length) {
        this.endProfileTour();
        return;
      }
      
      const currentSection = this.profileTourSections[this.profileTourStep];
      
      this.profileGuideMessage = currentSection.description;
      this.profileGuideOptions = [
        { text: this.profileTourStep === this.profileTourSections.length - 1 ? "Terminer" : "Suivant", action: "nextProfileTourStep" },
      ];
      
      this.internalShowGuide = true;
      this.forceShowGuide = true;
      
      this.highlightProfileSection(currentSection.selector);
      
      this.positionGuideDuringTour();
      
      if (typeof UserJourneyService !== 'undefined') {
        UserJourneyService.markProfileSectionVisited(currentSection.id);
      }
    },

    /**
     * Passe à l'étape suivante du tour du profil
     */
    nextProfileTourStep() {
      this.removeHighlights();
      
      this.profileTourStep++;
      
      this.showProfileTourStep();
    },

    /**
     * Termine le tour du profil
     */
     endProfileTour() {
      this.removeHighlights();
      
      this.profileTourActive = false;
      
      if (typeof UserJourneyService !== 'undefined') {
        UserJourneyService.completeProfileTour();
      }
      
      localStorage.setItem('profile-tour-completed', 'true');

      this.checkProfileBadge();

      this.profileGuideMessage = "Tu connais maintenant toutes les sections de ton profil ! Tu peux explorer tes badges et commencer à jouer pour en débloquer de nouveaux.";
      this.profileGuideOptions = [
        { text: "Commencer à jouer", action: "highlightPlayButton" },
      ];
      this.internalShowGuide = true;
      this.forceShowGuide = true;
      
      const rewardsContainer = document.querySelector('.rewards-container');
      if (rewardsContainer) {
        const rect = rewardsContainer.getBoundingClientRect();
        this.guideCustomPosition = {
          position: 'fixed',
          top: '80px',
          left: `${rect.right + 20}px`,
          zIndex: 2500
        };
        
        this.$nextTick(() => {
          const guideElement = document.querySelector('.guide-avatar');
          if (guideElement) {
            Object.assign(guideElement.style, {
              position: 'fixed',
              top: '80px',
              left: `${rect.right + 20}px`,
              zIndex: '2500'
            });
            
            guideElement.classList.remove('guide-top-left');
            guideElement.classList.add('guide-tour-active');
            
            this.adjustGuideBubblePosition('tour');
          }
        });
      }
    },

    /**
     * Met en évidence une section du profil
     */
    highlightProfileSection(selector) {
      this.removeHighlights();
      
      const element = document.querySelector(selector);
      if (element) {
        const highlight = document.createElement('div');
        highlight.className = 'section-highlight';
        
        const rect = element.getBoundingClientRect();
        
        const container = document.querySelector('.rewards-container');
        const containerRect = container.getBoundingClientRect();
        
        const top = rect.top - containerRect.top + container.scrollTop;
        const left = rect.left - containerRect.left + container.scrollLeft;
        
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
        
        container.appendChild(highlight);
        
        // Amélioration du défilement pour s'assurer que l'élément est bien visible
        const elementTopRelativeToContainer = top;
        const elementBottomRelativeToContainer = top + rect.height;
        const containerVisibleTop = container.scrollTop;
        const containerVisibleBottom = container.scrollTop + container.clientHeight;
        
        // Si l'élément est hors de la zone visible ou partiellement visible
        if (elementTopRelativeToContainer < containerVisibleTop || 
            elementBottomRelativeToContainer > containerVisibleBottom ||
            elementBottomRelativeToContainer - elementTopRelativeToContainer > container.clientHeight) {
          
          // Pour les éléments très grands, on privilégie le haut de l'élément
          if (rect.height > container.clientHeight * 0.7) {
            container.scrollTo({
              top: elementTopRelativeToContainer,
              behavior: 'smooth'
            });
          } else {
            // Pour les éléments plus petits, on centre
            container.scrollTo({
              top: elementTopRelativeToContainer - container.clientHeight / 2 + rect.height / 2,
              behavior: 'smooth'
            });
          }
        }
        
        this.positionGuideDuringTour();
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
        //
        localStorage.setItem('hasVisitedProfile', 'true');
        
        
        if (typeof UserJourneyService !== 'undefined') {
          UserJourneyService.updateStep(UserJourneyService.STEPS.PROFILE_INTRO);
        }
      }
    },
    
    dismissProfileGuide() {
      this.internalShowGuide = false;
      this.highlightPlayButtonBool = false;
      this.forceShowGuide = false; 
      
      
      if (this.$refs.nextActivitySection) {
        this.$refs.nextActivitySection.style.border = '';
        this.$refs.nextActivitySection.style.boxShadow = '';
      }
      
      if (this.$refs.playButton) {
        this.$refs.playButton.classList.remove('play-button-highlight');
      }
      
      localStorage.setItem('profile-tour-completed', 'true');
      
      
      this.$nextTick(() => {
        const guideElement = document.querySelector('.guide-avatar');
        if (guideElement) {
          guideElement.classList.remove('guide-tour-active');
        }
      });
    },

    maintainBubbleIconDistance() {
      const guideElement = document.querySelector('.guide-avatar');
      
      if (guideElement) {
        
        const observer = new MutationObserver(() => {
          // Quand des changements se produisent, réajuster si nécessaire
          if (this.profileTourActive || this.forceShowGuide) {
            // Pendant le tour ou quand forcé, utiliser la position tour
            this.adjustGuideBubblePosition('tour');
            
            // Forcer l'application directe des styles
            const guideBubble = document.querySelector('.guide-avatar > div:not(:first-child)');
            if (guideBubble) {
              guideBubble.style.position = 'absolute';
              guideBubble.style.top = '60px';
              guideBubble.style.marginTop = '0';
            }
          } else {
            // Sinon, utiliser la position top-left
            this.adjustGuideBubblePosition('top-left');
          }
        });
        
        // Observer les modifications d'attributs et de sous-éléments avec une configuration plus sensible
        observer.observe(guideElement, { 
          attributes: true, 
          childList: true,
          subtree: true,
          attributeFilter: ['style', 'class'],
          characterData: true
        });
        
        return observer;
      }
      
      return null;
    },
    
    highlightPlayButton() {
      // Désactiver l'ancien highlight
      this.highlightNextActivity = false;
      
      // Activer notre animation de bouton
      this.highlightPlayButtonBool = true;
      
      // Faire défiler vers la section d'activité si nécessaire
      if (this.$refs.nextActivitySection) {
        // Ajout d'une bordure verte autour de la section
        this.$refs.nextActivitySection.style.border = '3px solid #5ecc02';
        this.$refs.nextActivitySection.style.boxShadow = '0 0 15px rgba(94, 204, 2, 0.7)';
        this.$refs.nextActivitySection.style.borderRadius = '16px';
        
        // Faire défiler vers la section
        const container = document.querySelector('.rewards-container');
        const sectionRect = this.$refs.nextActivitySection.getBoundingClientRect();
        const containerRect = container.getBoundingClientRect();
        
        const scrollTo = sectionRect.top - containerRect.top + container.scrollTop - (container.clientHeight / 2) + (sectionRect.height / 2);
        
        container.scrollTo({
          top: scrollTo,
          behavior: 'smooth'
        });
      }
      
      // Mettre à jour le message du guide
      this.profileGuideMessage = "Maintenant, clique sur le bouton \"Jouer maintenant →\" dans la section \"Ma prochaine activité\" pour commencer ton premier jeu !";
      this.profileGuideOptions = [
        { text: "J'ai compris !", action: "dismissProfileGuide" }
      ];
      this.forceShowGuide = true;
      
      // Conserver la position du guide à droite pour cette dernière étape aussi
      const rewardsContainer = document.querySelector('.rewards-container');
      if (rewardsContainer) {
        const rect = rewardsContainer.getBoundingClientRect();
        this.guideCustomPosition = {
          position: 'fixed',
          top: '80px',
          left: `${rect.right + 20}px`,
          zIndex: 2500
        };
        
        this.$nextTick(() => {
          const guideElement = document.querySelector('.guide-avatar');
          if (guideElement) {
            Object.assign(guideElement.style, {
              position: 'fixed',
              top: '80px',
              left: `${rect.right + 20}px`,
              zIndex: '2500'
            });
            
            guideElement.classList.remove('guide-top-left');
            guideElement.classList.add('guide-tour-active');
            
            this.adjustGuideBubblePosition('tour');
          }
        });
      }
    },
    
    // Méthode pour gérer le clic sur le bouton "Jouer maintenant"
    goToGame(route) {
      this.closeModal();
      
      // Mettre à jour l'étape du parcours utilisateur si disponible
      if (typeof UserJourneyService !== 'undefined') {
        UserJourneyService.updateStep(UserJourneyService.STEPS.FIRST_GAME);
      }
      
      // Émettre un événement pour indiquer que l'utilisateur a commencé à jouer
      eventBus.emit('start-game', { route });
      
      this.$router.push(route);
    },
    checkProfileBadge() {
      // Trouver le badge "Explorateur du Profil" (ID 0)
      const profileBadge = this.badges.find(badge => badge.id === 0)

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

      this.checkBadgeCollector()
      this.checkAllGamesCompleted()

      // Recalculer les connexions après le chargement des badges
      this.$nextTick(() => {
        this.calculateNodeConnections();
      });
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
      // Définir le badge sélectionné
      this.selectedBadge = badge
      
      // Faire remonter le scroll du conteneur tout en haut
      const container = document.querySelector('.rewards-container')
      if (container) {
        container.scrollTo({
          top: 0,
          behavior: 'smooth'
        })
        
        // Désactiver le défilement en ajoutant une classe
        container.classList.add('no-scroll')
      }
    },

    closeModal() {
      this.selectedBadge = null
      
      // Réactiver le défilement
      const container = document.querySelector('.rewards-container')
      if (container) {
        container.classList.remove('no-scroll')
      }
    },

    shareBadge(badge) {
      alert(
        `Partage du badge "${badge.title}" sur les réseaux sociaux`
      )
    },
    
    generateCV() {
      if (!this.cvUnlocked) {
        return
      }
      // Dans un cas réel, on redirigerait vers la page de génération de CV
      this.$router.push('/cv-preview')
      
      // Fermer la modal
      this.$emit('close')
    },
    
    viewProfile() {
      // Dans un cas réel, on redirigerait vers la page de profil
      this.$router.push('/profile-page')
      
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

    async fetchGamesProgress() {
      // Map des endpoints et des indices de badge associés
      const gameEndpoints = [
        { endpoint: '/games/scenario', badgeId: 2 },
        //{ endpoint: '/games/shape-sequence', badgeId: 3 },
        { endpoint: '/games/jobs', badgeId: 7 },
        { endpoint: '/games/speed', badgeId: 1 },
        { endpoint: '/games/abilities', badgeId: 4 },
        { endpoint: '/games/skills', badgeId: 3 },
        { endpoint: '/games/room-env', badgeId: 5 },
      ];
      const updatedBadges = [...this.badges];
      let anyChange = false;
      for (const { endpoint, badgeId } of gameEndpoints) {
        try {
          const response = await AuthService.fetchWithAuth({
            method: 'get',
            url: endpoint,
          });
          // On considère le badge débloqué si completion === 1
          const completion = response.data.completion;
          const badge = updatedBadges.find(b => b.id === badgeId);
          if (badge) {
            badge.completion = completion;
            if (completion >= 1 && !badge.unlocked) {
              badge.unlocked = true;
              badge.dateUnlocked = new Date().toISOString().split('T')[0];
              anyChange = true;
            }
          }
        } catch (error) {
          // L'utilisateur n'a peut-être pas encore joué à ce jeu
          // On ignore l'erreur pour garder l'expérience fluide
        }
      }
      this.badges = updatedBadges;
      if (anyChange) {
        this.saveBadges();
        this.updateProgressPath();
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

/* Bouton de fermeture */
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

/* Prochaine activité */
.next-activity {
  margin-bottom: 24px;
}

.section-title {
  font-size: 22px;
  color: white;
  margin-bottom: 12px;
  font-weight: bold;
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

.play-button-highlight {
  position: relative;
  z-index: 1055;
  background-color: #5ecc02;
  animation: button-pulse 1.5s infinite;
  transform: scale(1.1);
}

@keyframes button-pulse {
  0% {
    box-shadow: 0 0 10px rgba(94, 204, 2, 0.7);
    transform: scale(1.1);
  }
  50% {
    box-shadow: 0 0 20px rgba(94, 204, 2, 1);
    transform: scale(1.15);
  }
  100% {
    box-shadow: 0 0 10px rgba(94, 204, 2, 0.7);
    transform: scale(1.1);
  }
}

/* Carte de progression neurale */
.neural-progress-map {
  display: grid;
  grid-template-columns: 3fr 2fr;
  grid-template-rows: 1fr;
  gap: 20px;
  position: relative;
  width: 100%;
  height: 480px;
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  padding: 25px;
  margin-bottom: 15px;
  overflow: hidden;
  border: 1px dashed rgba(255, 255, 255, 0.3);
}

/* Nœuds de jeu à gauche */
.games-path {
  justify-content: space-around;
  align-items: center;
}

.game-node {
  justify-content: center;
  margin-bottom: 15px;
}

.game-node-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
  border: 3px solid transparent;
  transition: all 0.3s ease;
  z-index: 3;
  margin-right: 15px;
  flex-shrink: 0;
}

.game-node.game-unlocked .game-node-icon {
  border-color: #4caf50;
  box-shadow: 0 0 15px rgba(76, 175, 80, 0.5);
}

.game-node.game-active .game-node-icon {
  border-color: #ff9800;
  box-shadow: 0 0 20px rgba(255, 152, 0, 0.7);
}

.game-node-lock {
  position: absolute;
  font-size: 16px;
  background-color: rgba(0, 0, 0, 0.5);
  width: 100%;
  height: 100%;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.game-node-emoji {
  font-size: 24px;
}

.game-node-icon:hover {
  transform: scale(1.15);
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
}

/* Connexions des jeux vers le profil */
.game-to-profile-connection {
  position: absolute;
  height: 2px;
  background: rgba(255, 255, 255, 0.05);
  z-index: 5;
  transform-origin: left center;
  transition: all 0.4s ease;
  border-radius: 6px;
}

/* Trait en tirets pour les connexions inactives */
.game-to-profile-connection {
  position: absolute;
  height: 3px; /* Plus épais pour meilleure visibilité */
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.15));
  z-index: 5;
  transform-origin: left center;
  transition: all 0.5s ease;
  border-radius: 3px; /* Bords arrondis */
  overflow: hidden; /* Pour l'effet d'animation */
}

.game-to-profile-connection::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.2), transparent);
  animation: shimmer 4s infinite;
}

.game-to-profile-connection.connection-active {
  background: linear-gradient(90deg, #66bb6a, #4caf50);
  box-shadow: 0 0 12px rgba(76, 175, 80, 0.6);
  height: 3px;
  position: relative;
  overflow: hidden;
}

.game-to-profile-connection.connection-active::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.7), transparent);
  animation: flow 2.5s infinite linear;
}

/* Points de départ et d'arrivée des connexions */
.game-to-profile-connection::after,
.main-connection.horizontal::after {
  content: '';
  position: absolute;
  width: 6px;
  height: 6px;
  background-color: rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  top: 50%;
  transform: translateY(-50%);
  right: 0;
  opacity: 0.7;
}

.game-to-profile-connection::before,
.main-connection.horizontal::before {
  content: '';
  position: absolute;
  width: 6px;
  height: 6px;
  background-color: rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  top: 50%;
  transform: translateY(-50%);
  left: 0;
  opacity: 0.7;
}

.game-to-profile-connection.connection-active::after,
.main-connection.horizontal.connection-active::after,
.game-to-profile-connection.connection-active::before,
.main-connection.horizontal.connection-active::before {
  background-color: #4caf50;
  box-shadow: 0 0 8px rgba(76, 175, 80, 0.8);
  opacity: 1;
}

/* Animations pour les effets de flux */
@keyframes flow {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

@keyframes shimmer {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

/* Amélioration pour l'affichage des connexions lors du survol */
.main-node:hover .main-connection.horizontal,
.game-node:hover .game-to-profile-connection {
  filter: brightness(1.5);
  transform: scale(1.05);
}

/* Animation de pulse pour les connexions actives */
@keyframes connection-pulse {
  0% {
    opacity: 0.8;
    box-shadow: 0 0 5px rgba(76, 175, 80, 0.5);
  }
  50% {
    opacity: 1;
    box-shadow: 0 0 12px rgba(76, 175, 80, 0.8);
  }
  100% {
    opacity: 0.8;
    box-shadow: 0 0 5px rgba(76, 175, 80, 0.5);
  }
}

/* Version plus subtile pour les thèmes clairs */
.light .game-to-profile-connection,
.light .main-connection.horizontal {
  background: linear-gradient(90deg, rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.2));
}

.light .game-to-profile-connection.connection-active,
.light .main-connection.horizontal.connection-active {
  background: linear-gradient(90deg, #66bb6a, #4caf50);
}

/* Responsive pour les petits écrans */
@media (max-width: 768px) {
  .main-connection.horizontal {
    width: 40px;
  }
  
  .game-to-profile-connection,
  .main-connection.horizontal {
    height: 3px;
  }
}

/* Chemin principal (Profil -> CV -> Formation) */
.main-path {
  grid-column: 2;
  grid-row: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  position: relative;
}

.main-path-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.main-node {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 2;
  margin: 0 10px;
}

.profile-node {
  z-index: 10;
  position: relative;
}

.main-node-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #333;
  position: relative;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
  border: 3px solid #555;
  transition: all 0.5s ease;
}

.main-node-icon.node-complete {
  border-color: #4caf50;
  box-shadow: 0 0 20px rgba(76, 175, 80, 0.7);
  background-color: rgba(76, 175, 80, 0.2);
}

.node-emoji {
  font-size: 36px;
  z-index: 3;
}

.node-completion-circle {
  position: absolute;
  width: 100%;
  height: 100%;
}

.node-completion-circle svg {
  width: 100%;
  height: 100%;
}

.node-progress-bg {
  fill: none;
  stroke: rgba(255, 255, 255, 0.1);
  stroke-width: 2.5;
}

.node-progress-fill {
  fill: none;
  stroke: #4fc3f7;
  stroke-width: 2.5;
  stroke-linecap: round;
  transform: rotate(-90deg);
  transform-origin: center;
  transition: stroke-dasharray 1s ease;
}

.node-label {
  position: absolute;
  top: 100%;
  left: 50% + translateX(-50%);
  white-space: nowrap;
  margin-top: 10px;
  font-weight: bold;
  color: #fff;
  font-size: 16px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

/* Connexions horizontales entre les nœuds principaux */
.main-connection.horizontal {
  width: 60px;
  height: 4px; /* Légèrement plus épais pour plus de visibilité */
  background: linear-gradient(to right, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.05));
  margin: 0 5px;
  transition: all 0.5s ease;
  border-radius: 4px; /* Bords arrondis */
  position: relative;
  overflow: hidden; /* Pour l'effet d'animation */
}

/* Animation subtile pour les connexions non-actives */
.main-connection.horizontal::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: shimmer 3s infinite;
}

/* Connexion horizontale active avec effet de flux */
.main-connection.horizontal.connection-active {
  background: linear-gradient(to right, #43a047, #66bb6a, #81c784);
  box-shadow: 0 0 10px rgba(76, 175, 80, 0.7);
  height: 4px;
  position: relative;
  overflow: hidden;
}

/* Effet de flux pour les connexions actives */
.main-connection.horizontal.connection-active::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.7), transparent);
  animation: flow 2s infinite linear;
}

.main-connection.horizontal::after,
.main-connection.horizontal::before {
  content: '';
  position: absolute;
  width: 6px;
  height: 6px;
  background-color: #4fc3f7;
  border-radius: 50%;
  top: 50%;
  transform: translateY(-50%);
  opacity: 0.8;
  box-shadow: 0 0 4px rgba(79, 195, 247, 0.5);
}

.main-connection.horizontal::after {
  right: -1px;
}

.main-connection.horizontal::before {
  left: -1px;
}

.main-connection.horizontal.connection-active::after,
.main-connection.horizontal.connection-active::before {
  background-color: #81c784;
  box-shadow: 0 0 6px rgba(76, 175, 80, 0.8);
  opacity: 1;
}

/* Effet de survol sur les nœuds */
.main-node:hover .main-connection.horizontal,
.game-node:hover .game-to-profile-connection {
  filter: brightness(1.3);
}

/* Indicateur de progression global */
.progress-indicator {
  position: absolute;
  bottom: 15px;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  text-align: center;
}

.progress-percentage {
  font-size: 24px;
  font-weight: bold;
  color: #4fc3f7;
  margin-bottom: 5px;
}

.progress-bar {
  height: 8px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 5px;
  width: 75%;
  margin: 0 auto;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4caf50, #81c784);
  border-radius: 4px;
  transition: width 1s ease;
}

.progress-label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
}

/* Section Badges */
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

.status-unlocked {
  color: #4caf50;
}

.status-locked {
  color: #9e9e9e;
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

.locked-button {
  position: relative;
  opacity: 0.7;
  cursor: not-allowed;
}

.lock-icon {
  position: absolute;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
  font-size: 1.2em;
  margin-left: 8px;
  animation: lock-pulse 2s infinite ease-in-out;
}

@keyframes lock-pulse {
  0% { transform: translateY(-50%) scale(1); }
  50% { transform: translateY(-50%) scale(1.1); }
  100% { transform: translateY(-50%) scale(1); }
}

/* Modal détails badge */
.no-scroll {
  overflow: hidden !important;
}

.badge-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1100;
  backdrop-filter: blur(8px);
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
.high-contrast .empty-state,
.high-contrast .badge-achievement,
.high-contrast .badge-locked-info,
.high-contrast .badge-modal,
.high-contrast .neural-progress-map {
  background-color: #222;
  border: 2px solid #fff;
}

.high-contrast .game-node.game-unlocked .game-node-icon {
  border-color: #fff;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.7);
}

.high-contrast .user-detail-item {
  background-color: #333;
  border: 1px solid #fff;
}

.high-contrast .section-title,
.high-contrast .welcome-title,
.high-contrast .badge-title,
.high-contrast .badge-detail-title,
.high-contrast .next-activity-info h3,
.high-contrast .progress-percentage {
  color: #fff;
  text-shadow: none;
}

/* Version pour le mode accessibilité contraste élevé */
.high-contrast .game-to-profile-connection,
.high-contrast .main-connection.horizontal {
  background: rgba(255, 255, 255, 0.8);
  height: 3px;
}

.high-contrast .game-to-profile-connection::before,
.high-contrast .main-connection.horizontal::before {
  background-image: repeating-linear-gradient(
    to right,
    #000 0px,
    #000 4px,
    #fff 4px,
    #fff 10px
  );
}

.high-contrast .game-to-profile-connection.connection-active,
.high-contrast .main-connection.horizontal.connection-active {
  background: #fff;
  border: 1px solid #000;
}

/* Scrollbar */
.rewards-container {
  scrollbar-width: thin;
  scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track);
}

.rewards-container::-webkit-scrollbar {
  width: 8px;
  height: 8px;
  display: block;
}

.rewards-container::-webkit-scrollbar-track {
  background: var(--scrollbar-track);
  border-radius: 10px;
}

.rewards-container::-webkit-scrollbar-thumb {
  background: var(--scrollbar-thumb);
  border-radius: 10px;
}

.rewards-container::-webkit-scrollbar-thumb:hover {
  background: var(--scrollbar-thumb-hover);
}

/* Tour guidé */
.section-highlight {
  position: absolute;
  pointer-events: none;
  z-index: 1050;
  animation: highlight-pulse 2s ease-out infinite;
  border: 3px solid #76ff03;
  border-radius: 16px;
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

.guide-top-left:not(.force-show-message) {
  position: fixed !important;
  top: 20px !important;
  left: 20px !important;
  z-index: 2500 !important;
}

.guide-tour-active {
  position: fixed !important;
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

/* Responsive */
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
  
  .neural-progress-map {
    height: auto;
    min-height: 350px;
    padding: 20px 15px;
    grid-template-columns: 1fr;
    grid-template-rows: auto auto;
  }
  
  .main-path {
    grid-column: 1;
    grid-row: 2;
    margin-top: 20px;
  }
  
  .main-connection.horizontal {
    width: 40px;
  }
  
  .game-to-profile-connection,
  .main-connection.horizontal {
    height: 2px;
  }
  
  .main-connection.horizontal::before,
  .game-to-profile-connection::before {
    background-image: repeating-linear-gradient(
      to right,
      rgba(255, 255, 255, 0.4) 0px,
      rgba(255, 255, 255, 0.4) 3px,
      transparent 3px,
      transparent 8px
    );
  }
}

@media (max-width: 480px) {
  .rewards-container {
    padding: 16px 12px;
    border-radius: 16px;
    width: 95%;
    max-height: 95vh;
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
  
  .game-node-icon {
    width: 50px;
    height: 50px;
  }
  
  .game-node-emoji {
    font-size: 20px;
  }
  
  .main-node-icon {
    width: 60px;
    height: 60px;
  }
  
  .node-emoji {
    font-size: 28px;
  }
  
  .progress-percentage {
    font-size: 20px;
  }
  
  .neural-progress-map {
    min-height: 300px;
    padding: 15px 10px;
  }
  
  .badge-modal {
    width: 95%;
    padding: 16px;
  }
  
  .badge-detail-icon {
    width: 80px;
    height: 80px;
  }
  
  .badge-detail-emoji {
    font-size: 40px;
  }
}

/* Styles pour la barre de complétion des badges */
.badge-completion {
  margin-top: 4px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.badge-completion-bar {
  width: 48px;
  height: 6px;
  background: #e0e0e0;
  border-radius: 3px;
  overflow: hidden;
}
.badge-completion-fill {
  height: 100%;
  background: linear-gradient(90deg, #4caf50, #8bc34a);
  border-radius: 3px;
  transition: width 0.3s;
}
.badge-completion-text {
  font-size: 0.85em;
  color: #555;
  min-width: 28px;
  text-align: right;
}
</style>