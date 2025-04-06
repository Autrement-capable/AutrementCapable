<template>
  <space-background v-if="animationsEnabled" :theme="currentTheme" />
  <static-backgrounds v-else :theme="currentTheme" />
  
  <div class="rewards-container" :class="{ 'high-contrast': highContrastMode }">
    <h1 class="main-title">Mes Badges</h1>
    
    <!-- Contrôles d'accessibilité -->
    <div class="accessibility-controls">
      <button @click="toggleContrast" class="accessibility-btn" aria-label="Changer le mode contraste">
        <span v-if="highContrastMode">🌓</span><span v-else>🌑</span>
      </button>
      <!-- Bouton pour activer/désactiver les animations -->
      <button @click="toggleAnimations" class="accessibility-btn" aria-label="Activer/désactiver les animations">
        <span v-if="animationsEnabled">🎬</span><span v-else>📷</span>
      </button>
    </div>

    <!-- Message de célébration -->
    <div class="celebration-box" v-if="hasUnlockedBadges">
      <div class="celebration-icon">🎉</div>
      <div class="celebration-text">
        <h2>Bravo !</h2>
        <p>Vous avez débloqué {{ unlockedBadgesCount }} badge{{ unlockedBadgesCount > 1 ? 's' : '' }} !</p>
      </div>
    </div>
    
    <!-- Message si aucun badge -->
    <div class="empty-state" v-if="!hasUnlockedBadges">
      <div class="empty-badge-icon">🏅</div>
      <h2>Pas encore de badges !</h2>
      <p>Participez aux jeux et activités pour gagner vos premiers badges.</p>
      <button @click="$router.push('/dashboard')" class="start-button">Commencer à jouer</button>
    </div>

    <!-- Progression globale -->
    <div class="progress-container" v-if="hasUnlockedBadges">
      <h2>Ma progression</h2>
      <div class="progress-bar-container">
        <div class="progress-bar" :style="{ width: `${progressPercentage}%` }"></div>
      </div>
      <p class="progress-text">{{ unlockedBadgesCount }} / {{ totalBadgesCount }} badges obtenus</p>
    </div>

    <!-- Grille des badges -->
    <div class="badges-grid">
      <div 
        v-for="badge in badges" 
        :key="badge.id" 
        class="badge-card"
        :class="{ 'unlocked': badge.unlocked, 'locked': !badge.unlocked }"
        @click="showBadgeDetails(badge)"
      >
        <div class="badge-icon" :style="{ backgroundColor: badge.iconColor || '#e0e0e0' }">
          <div v-if="!badge.unlocked" class="lock-overlay">🔒</div>
          <span class="badge-emoji">{{ badge.icon }}</span>
        </div>
        <div class="badge-info">
          <h3>{{ badge.title }}</h3>
          <p v-if="badge.unlocked">{{ badge.description }}</p>
          <p v-else>Badge verrouillé</p>
        </div>
      </div>
    </div>

    <!-- Détails du badge (modal) -->
    <div v-if="selectedBadge" class="badge-modal-overlay" @click="closeModal">
      <div class="badge-modal" @click.stop>
        <button class="close-button" @click="closeModal">×</button>
        
        <div class="badge-detail-content" :class="{ 'unlocked': selectedBadge.unlocked }">
          <div class="badge-detail-icon" :style="{ backgroundColor: selectedBadge.iconColor || '#e0e0e0' }">
            <span class="badge-detail-emoji">{{ selectedBadge.icon }}</span>
          </div>
          
          <h2>{{ selectedBadge.title }}</h2>
          
          <p v-if="selectedBadge.unlocked" class="badge-description">
            {{ selectedBadge.description }}
          </p>
          <p v-else class="badge-locked-message">
            {{ selectedBadge.hint || "Continuez à jouer pour débloquer ce badge !" }}
          </p>
          
          <div v-if="selectedBadge.unlocked" class="badge-achievement">
            <div class="achievement-date">
              Obtenu le: {{ formatDate(selectedBadge.dateUnlocked) }}
            </div>
            <div class="achievement-game">
              {{ selectedBadge.game }}
            </div>
          </div>
          
          <div class="badge-actions">
            <button 
              v-if="!selectedBadge.unlocked" 
              @click="goToGame(selectedBadge.gameRoute)" 
              class="play-button"
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
import SpaceBackground from '@/components/SpaceBackground.vue';
import StaticBackgrounds from '@/components/StaticBackgrounds.vue';
import { BackgroundManager } from '@/utils/BackgroundManager';

export default {
  name: 'RewardsPage',
  components: {
    SpaceBackground,
    StaticBackgrounds
  },
  data() {
    return {
      badges: [
        {
          id: 1,
          title: 'Maître de la vitesse',
          description: 'Vous avez terminé le jeu de vitesse avec un score parfait !',
          icon: '⚡',
          iconColor: '#F44336',
          unlocked: false,
          dateUnlocked: '2023-06-16',
          game: 'Jeu de Vitesse',
          gameRoute: '/game-speed',
          shareable: true
        },
        {
          id: 2,
          title: 'Maître des scénarios',
          description: 'Vous avez brillamment résolu votre premier scénario social !',
          icon: '🎭',
          iconColor: '#9C27B0',
          unlocked: false,
          dateUnlocked: '',
          game: 'Jeu des Scénarios',
          gameRoute: '/scenarios',
          shareable: true
        },
        {
          id: 3,
          title: 'Expert des formes',
          description: 'Vous avez reconnu toutes les séquences de formes correctement !',
          icon: '🔷',
          iconColor: '#2196F3',
          unlocked: false,
          hint: 'Terminez le jeu des formes avec un score parfait',
          game: 'Jeu des Formes',
          gameRoute: '/shape-sequence-game',
          shareable: true
        },
        {
          id: 4,
          title: 'Explorateur de compétences',
          description: 'Vous avez exploré et identifié vos points forts et axes de développement !',
          icon: '🎯',
          iconColor: '#3F51B5',
          unlocked: false,
          hint: 'Terminez la Roulette des Compétences et découvrez vos talents',
          game: 'Roulette des Compétences',
          gameRoute: '/roue-des-competences',
          shareable: true
        },
        {
          id: 5,
          title: 'Explorateur d\'environnements',
          description: 'Vous avez exploré tous les environnements disponibles',
          icon: '🏠',
          iconColor: '#795548',
          unlocked: false,
          hint: 'Essayez tous les préréglages dans l\'environnement de personnalisation',
          game: 'Environnement',
          gameRoute: '/environment',
          shareable: false
        },
        {
          id: 6,
          title: 'CV professionnel',
          description: 'Vous avez complété toutes les étapes pour générer un CV professionnel',
          icon: '📄',
          iconColor: '#607D8B',
          unlocked: false,
          dateUnlocked: '2023-06-20',
          game: 'Générateur de CV',
          gameRoute: '/cv-preview',
          shareable: true
        },
        {
          id: 7,
          title: 'Apprenti des métiers',
          description: 'Vous avez découvert 3 métiers différents',
          icon: '👷',
          iconColor: '#FF9800',
          unlocked: false,
          hint: 'Explorez au moins 3 fiches métier',
          game: 'Découverte des métiers',
          gameRoute: '/metier/soudeur',
          shareable: false
        },
        {
          id: 8,
          title: 'Inscription à une formation',
          description: 'Vous vous êtes inscrit à une formation',
          icon: '🎓',
          iconColor: '#FFD700',
          unlocked: false,
          hint: 'Inscrivez-vous à une formation pour débloquer ce badge',
          game: 'Formations',
          gameRoute: '/formation',
          shareable: true
        }
      ],
      selectedBadge: null,
      highContrastMode: false,
      textSizeLevel: 0,

      currentTheme: 'cosmic',
      animationsEnabled: true
    };
  },
  computed: {
    unlockedBadgesCount() {
      return this.badges.filter(badge => badge.unlocked).length;
    },
    totalBadgesCount() {
      return this.badges.length;
    },
    progressPercentage() {
      return (this.unlockedBadgesCount / this.totalBadgesCount) * 100;
    },
    hasUnlockedBadges() {
      return this.unlockedBadgesCount > 0;
    }
  },
  created() {
    // Chargement des préférences d'accessibilité
    this.loadAccessibilitySettings();
    
    this.currentTheme = BackgroundManager.getCurrentTheme();
    this.animationsEnabled = BackgroundManager.areAnimationsEnabled();

    // On pourrait aussi chargement les badges depuis localStorage
    this.loadBadges();
  },
  methods: {
    toggleAnimations() {
      this.animationsEnabled = BackgroundManager.toggleAnimations();
    },
    getCurrentTheme() {
        return localStorage.getItem('dashboard-theme') || 'space';
    },
    loadBadges() {
      // Dans un cas réel, on chargerait les badges depuis localStorage
      // ou depuis une API selon que l'utilisateur est connecté ou non
      const savedBadges = localStorage.getItem('userBadges');
      if (savedBadges) {
        try {
          const badgeData = JSON.parse(savedBadges);
          // Fusionner les données sauvegardées avec nos badges par défaut
          this.badges = this.badges.map(badge => {
            const savedBadge = badgeData.find(b => b.id === badge.id);
            if (savedBadge) {
              return { ...badge, ...savedBadge };
            }
            return badge;
          });
        } catch (error) {
          console.error('Erreur lors du chargement des badges:', error);
        }
      }
      
      // Vérification si le badge "collectionneur" devrait être débloqué
      this.checkBadgeCollector();
    },
    
    checkBadgeCollector() {
      // Vérifier si l'utilisateur a débloqué 5 badges ou plus
      if (this.unlockedBadgesCount >= 5) {
        const collectorBadge = this.badges.find(badge => badge.id === 8);
        if (collectorBadge && !collectorBadge.unlocked) {
          collectorBadge.unlocked = true;
          collectorBadge.dateUnlocked = new Date().toISOString().split('T')[0];
          this.saveBadges();
        }
      }
    },
    
    saveBadges() {
      // Enregistrer les badges dans localStorage
      localStorage.setItem('userBadges', JSON.stringify(this.badges));
    },
    
    formatDate(dateString) {
      // Formater une date en format français
      if (!dateString) return '';
      
      const options = { day: 'numeric', month: 'long', year: 'numeric' };
      const date = new Date(dateString);
      
      return date.toLocaleDateString('fr-FR', options);
    },
    
    showBadgeDetails(badge) {
      this.selectedBadge = badge;
    },
    
    closeModal() {
      this.selectedBadge = null;
    },
    
    goToGame(route) {
      this.closeModal();
      this.$router.push(route);
    },
    
    shareBadge(badge) {
      // Dans un cas réel, cela pourrait ouvrir une boîte de dialogue de partage
      // ou générer un lien à partager
      alert(`Partage du badge "${badge.title}" sur les réseaux sociaux (à implémenter)`);
    },
    
    // Fonctions d'accessibilité
    loadAccessibilitySettings() {
      const settings = localStorage.getItem('accessibilitySettings');
      if (settings) {
        try {
          const { highContrastMode, textSizeLevel } = JSON.parse(settings);
          this.highContrastMode = highContrastMode;
          this.textSizeLevel = textSizeLevel;
          this.applyTextSize();
        } catch (error) {
          console.error('Erreur lors du chargement des paramètres d\'accessibilité:', error);
        }
      }
    },
    
    saveAccessibilitySettings() {
      const settings = {
        highContrastMode: this.highContrastMode,
        textSizeLevel: this.textSizeLevel
      };
      localStorage.setItem('accessibilitySettings', JSON.stringify(settings));
    },
    
    toggleContrast() {
      this.highContrastMode = !this.highContrastMode;
      this.saveAccessibilitySettings();
    },
  }
};
</script>

<style scoped>
/* Styles de base */
.rewards-container {
  position: relative;
  max-width: 900px;
  margin: 20px auto 30px;
  padding: 15px 10px;
  font-family: 'Comic Sans MS', 'Chalkboard SE', 'Marker Felt', sans-serif;
  background-color: #f8f9fa;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.main-title {
  text-align: center;
  color: #4A4D9E;
  font-size: 1.8rem;
  margin-bottom: 5px;
  position: relative;
  padding-bottom: 8px;
}

.main-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 3px;
  background-color: #FFD700;
  border-radius: 2px;
}

/* Ajout d'espace en bas de la page */
.bottom-spacer {
  height: 30px;
}

/* Styles d'accessibilité */
.accessibility-controls {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  gap: 5px;
  z-index: 10;
}

.accessibility-btn {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: none;
  background-color: #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
  font-size: 0.8rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.accessibility-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

/* Boîte de célébration */
.celebration-box {
  display: flex;
  align-items: center;
  background-color: #FFF8E1;
  border-radius: 10px;
  padding: 15px;
  margin-bottom: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  animation: bounce 0.5s ease;
}

.celebration-icon {
  font-size: 2.2rem;
  margin-right: 15px;
  animation: pulse 2s infinite;
}

.celebration-text h2 {
  margin: 0 0 6px 0;
  color: #FF9800;
  font-size: 1.3rem;
}

.celebration-text p {
  font-size: 0.95rem;
  margin: 0;
}

/* État vide - pas de badges */
.empty-state {
  text-align: center;
  padding: 25px 10px;
  background-color: #FFFFFF;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  margin-bottom: 20px;
}

.empty-badge-icon {
  font-size: 70px;
  margin-bottom: 15px;
  opacity: 0.7;
}

.empty-state h2 {
  font-size: 1.3rem;
  margin-bottom: 8px;
  color: #757575;
}

.empty-state p {
  font-size: 0.95rem;
  margin-bottom: 10px;
}

.start-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 25px;
  padding: 8px 16px;
  font-size: 0.9rem;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  margin-top: 10px;
  display: inline-block;
  line-height: normal;
  height: auto;
}

.start-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15);
}

/* Barre de progression */
.progress-container {
  text-align: center;
  margin-bottom: 10px;
  background-color: #FFFFFF;
  padding: 5px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.progress-container h2 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #333333;
  font-size: 1.2rem;
}

.progress-bar-container {
  width: 100%;
  height: 16px;
  background-color: #E0E0E0;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #4CAF50, #8BC34A);
  border-radius: 8px;
  transition: width 1s ease;
}

.progress-text {
  font-size: 0.9rem;
  color: #757575;
  margin: 3px 0 0;
}

/* Grille des badges */
.badges-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 15px;
  margin-bottom: 30px;
}

.badge-card {
  background-color: #FFFFFF;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px;
  position: relative;
}

.badge-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.badge-card.unlocked {
  border: 1px solid #8BC34A;
}

.badge-card.locked {
  opacity: 0.7;
  filter: grayscale(70%);
}

.badge-icon {
  position: relative;
  width: 80px;
  height: 80px;
  margin-bottom: 12px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.badge-emoji {
  font-size: 40px;
}

.lock-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  border-radius: 50%;
}

.badge-info {
  text-align: center;
  flex-grow: 1;
}

.badge-info h3 {
  margin-top: 0;
  margin-bottom: 6px;
  color: #333333;
  font-size: 1rem;
}

.badge-info p {
  margin: 0;
  color: #757575;
  font-size: 0.85rem;
  line-height: 1.3;
}

/* Modal de détails de badge */
.badge-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.badge-modal {
  background-color: #FFFFFF;
  border-radius: 12px;
  width: 90%;
  max-width: 400px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  padding: 20px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  animation: scaleUp 0.3s ease;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.close-button:hover {
  background-color: #F5F5F5;
}

.badge-detail-content {
  text-align: center;
}

.badge-detail-icon {
  width: 100px;
  height: 100px;
  margin: 0 auto 15px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.badge-detail-emoji {
  font-size: 50px;
}

.badge-detail-content h2 {
  color: #333333;
  margin-bottom: 12px;
  font-size: 1.3rem;
}

.badge-description {
  color: #555555;
  margin-bottom: 15px;
  line-height: 1.4;
  font-size: 0.9rem;
}

.badge-locked-message {
  color: #757575;
  font-style: italic;
  margin-bottom: 15px;
  font-size: 0.9rem;
}

.badge-achievement {
  background-color: #F5F5F5;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.achievement-date {
  font-weight: bold;
  margin-bottom: 5px;
  color: #4A4D9E;
  font-size: 0.9rem;
}

.achievement-game {
  color: #757575;
  font-size: 0.85rem;
}

.badge-actions {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-top: 15px;
}

.play-button, .share-button {
  padding: 8px 16px;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
  font-size: 0.85rem;
}

.play-button {
  background-color: #4CAF50;
  color: white;
}

.share-button {
  background-color: #2196F3;
  color: white;
}

.play-button:hover, .share-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

/* Animations */
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

@keyframes scaleUp {
  from { transform: scale(0.8); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

/* Tailles de texte variables pour accessibilité */
.text-small {
  font-size: 0.8rem;
}

.text-small .main-title {
  font-size: 1.6rem;
}

.text-small .badge-info h3 {
  font-size: 0.9rem;
}

.text-large {
  font-size: 1rem;
}

.text-large .main-title {
  font-size: 2.2rem;
}

.text-large .badge-info h3 {
  font-size: 1.2rem;
}

.text-xlarge {
  font-size: 1.2rem;
}

.text-xlarge .main-title {
  font-size: 2.6rem;
}

.text-xlarge .badge-info h3 {
  font-size: 1.4rem;
}

/* Media queries pour la responsivité */
@media (max-width: 768px) {
  .rewards-container {
    margin: 15px auto 25px;
    padding: 15px 10px;
  }
  
  .badges-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 10px;
  }
  
  .badge-detail-icon {
    width: 90px;
    height: 90px;
  }
  
  .badge-actions {
    flex-direction: column;
  }
  
  .play-button, .share-button {
    width: 100%;
    margin-bottom: 5px;
  }
  
  .celebration-box {
    flex-direction: column;
    text-align: center;
    padding: 5px;
  }
  
  .celebration-icon {
    margin-right: 0;
    margin-bottom: 5px;
  }
}

@media (max-width: 480px) {
  .rewards-container {
    margin: 10px auto 20px;
    padding: 10px 5px;
    border-radius: 8px;
  }
  
  .badges-grid {
    grid-template-columns: 1fr;
  }
  
  .accessibility-controls {
    top: 5px;
    right: 5px;
    gap: 3px;
  }
  
  .accessibility-btn {
    width: 25px;
    height: 25px;
    font-size: 0.8rem;
  }
  
  .main-title {
    font-size: 1.5rem;
    margin-bottom: 5px;
  }
  
  .empty-badge-icon {
    font-size: 60px;
  }
}
</style>