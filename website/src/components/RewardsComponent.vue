<template>
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

    <!-- Progression globale -->
    <div class="progress-container">
      <h2 class="section-title">Mon parcours</h2>
      <div class="progress-bar-container">
        <div
          class="progress-bar"
          :style="{ width: `${progressPercentage}%` }"
        ></div>
      </div>
      <p class="progress-text">
        <strong>{{ unlockedBadgesCount }}</strong> activités terminées sur <strong>{{ totalBadgesCount }}</strong>
      </p>
    </div>

    <!-- Message si aucun badge -->
    <div class="empty-state" v-if="!hasUnlockedBadges">
      <div class="empty-badge-icon">🏅</div>
      <h2>Pas encore de badges !</h2>
      <p>Participe aux jeux et activités pour gagner tes premiers badges.</p>
      <button @click="$router.push('/dashboard')" class="start-button">
        Commencer à jouer
      </button>
    </div>

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
  </div>
</template>

<script>
export default {
  name: 'RewardsComponent',
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
    }
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
          id: 1,
          title: 'Maître de la vitesse',
          description:
            'Tu as terminé le jeu de vitesse avec un score parfait !',
          icon: '⚡',
          iconColor: '#F44336',
          unlocked: true,
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
  created() {
    // Chargement des préférences d'accessibilité
    this.loadAccessibilitySettings()

    // On pourrait aussi chargement les badges depuis localStorage
    this.loadBadges()
  },
  methods: {
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

    goToGame(route) {
      this.closeModal()
      this.$router.push(route)
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
  background-color: rgba(30, 30, 45, 0.85);
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

/* Section de progression */
.progress-container {
  background-color: rgba(255, 255, 255, 0.05);
  padding: 20px;
  border-radius: 16px;
  margin-bottom: 24px;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.section-title {
  font-size: 22px;
  color: #4fc3f7;
  margin-top: 0;
  margin-bottom: 16px;
  text-align: center;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.progress-bar-container {
  height: 24px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 8px;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #4caf50, #8bc34a);
  border-radius: 12px;
  transition: width 1s ease;
  box-shadow: 0 0 10px rgba(76, 175, 80, 0.5);
}

.progress-text {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.9);
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

.status-unlocked {
  color: #4caf50;
  text-shadow: 0 0 4px rgba(76, 175, 80, 0.5);
}

.status-locked {
  color: #9e9e9e;
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

.play-button, .play-now-button, .share-button {
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

.play-button, .play-now-button {
  background-color: #4caf50;
}

.share-button {
  background-color: #2196f3;
}

.play-button:hover, .play-now-button:hover, .share-button:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
}

/* Animations */
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

@keyframes pulse {
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
.high-contrast .progress-container,
.high-contrast .empty-state,
.high-contrast .badge-achievement,
.high-contrast .badge-locked-info,
.high-contrast .badge-modal {
  background-color: #222;
  border: 2px solid #fff;
}

.high-contrast .user-detail-item {
  background-color: #333;
  border: 1px solid #fff;
}

.high-contrast .progress-bar-container {
  background-color: #333;
  border: 1px solid #fff;
}

.high-contrast .progress-bar {
  background: #fff;
}

.high-contrast .section-title,
.high-contrast .welcome-title,
.high-contrast .badge-title,
.high-contrast .badge-detail-title,
.high-contrast .next-activity-info h3 {
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
}
</style>