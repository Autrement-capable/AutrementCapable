<template>
  <div class="rewards-container" :class="{ 'high-contrast': highContrastMode }">
    <h1 class="main-title">Mes Badges</h1>
    
    <!-- Contrôles d'accessibilité -->
    <div class="accessibility-controls">
      <button @click="toggleContrast" class="accessibility-btn" aria-label="Changer le mode contraste">
        <span v-if="highContrastMode">🌓</span><span v-else>🌑</span>
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
export default {
  name: 'RewardsPage',
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
          title: 'Mémoire d\'éléphant',
          description: 'Vous avez prouvé que vous avez une mémoire exceptionnelle !',
          icon: '🧠',
          iconColor: '#9C27B0',
          unlocked: false,
          hint: 'Terminez le jeu de mémoire sans aucune erreur',
          game: 'Jeu de Mémoire',
          gameRoute: '/game-memory',
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
      textSizeLevel: 0
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
    
    // On pourrait aussi chargement les badges depuis localStorage
    this.loadBadges();
  },
  methods: {
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
  max-width: 1200px;
  margin: 40px auto 60px; /* Marges réduites */
  padding: 30px 20px; /* Padding ajusté */
  font-family: 'Comic Sans MS', 'Chalkboard SE', 'Marker Felt', sans-serif;
  background-color: #f8f9fa;
  border-radius: 20px; /* Ajout d'un rayon de bordure */
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1); /* Ajout d'une ombre */
  transition: all 0.3s ease;
}

.main-title {
  text-align: center;
  color: #4A4D9E;
  font-size: 2.5rem;
  margin-bottom: 40px; /* Margin augmenté */
  position: relative;
  padding-bottom: 15px; /* Padding augmenté */
}

.main-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 4px;
  background-color: #FFD700;
  border-radius: 2px;
}

/* Ajout d'espace en bas de la page */
.bottom-spacer {
  height: 60px; /* Espace supplémentaire en bas */
}

/* Styles d'accessibilité */
.accessibility-controls {
  position: absolute;
  top: 15px;
  right: 15px;
  display: flex;
  gap: 10px;
  z-index: 10;
}

.accessibility-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background-color: #fff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.accessibility-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3);
}

/* Mode contraste élevé */
.high-contrast {
  color: #FFFFFF;
  background-color: #000000;
}

.high-contrast .main-title {
  color: #FFFFFF;
}

.high-contrast .badge-card {
  background-color: #333333;
  border: 1px solid #FFFFFF;
}

.high-contrast .badge-info h3 {
  color: #FFFFFF;
}

.high-contrast .badge-info p {
  color: #CCCCCC;
}

.high-contrast .badge-modal {
  background-color: #222222;
  border: 2px solid #FFFFFF;
}

/* Boîte de célébration */
.celebration-box {
  display: flex;
  align-items: center;
  background-color: #FFF8E1;
  border-radius: 15px;
  padding: 25px; /* Padding augmenté */
  margin-bottom: 40px; /* Marge augmentée */
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  animation: bounce 0.5s ease;
}

.high-contrast .celebration-box {
  background-color: #333333;
  border: 1px solid #FFFFFF;
}

.celebration-icon {
  font-size: 3.5rem; /* Taille augmentée */
  margin-right: 25px; /* Marge augmentée */
  animation: pulse 2s infinite;
}

.celebration-text h2 {
  margin: 0 0 12px 0; /* Marge augmentée */
  color: #FF9800;
  font-size: 1.8rem; /* Taille augmentée */
}

.high-contrast .celebration-text h2 {
  color: #FFCC00;
}

.celebration-text p {
  font-size: 1.2rem; /* Taille augmentée */
  margin: 0;
}

/* État vide - pas de badges */
.empty-state {
  text-align: center;
  padding: 50px 20px; /* Padding augmenté */
  background-color: #FFFFFF;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  margin-bottom: 40px; /* Marge augmentée */
}

.high-contrast .empty-state {
  background-color: #333333;
}

.empty-badge-icon {
  font-size: 110px; /* Taille augmentée */
  margin-bottom: 25px; /* Marge augmentée */
  opacity: 0.7;
}

.empty-state h2 {
  font-size: 1.7rem; /* Taille augmentée */
  margin-bottom: 15px; /* Marge augmentée */
  color: #757575;
}

.high-contrast .empty-state h2 {
  color: #FFFFFF;
}

.empty-state p {
  font-size: 1.2rem; /* Taille augmentée */
  margin-bottom: 20px; /* Marge augmentée */
}

.start-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 50px;
  padding: 12px 25px; /* Padding horizontal/vertical ajusté */
  font-size: 1.1rem;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  margin-top: 20px;
  display: inline-block; /* Ajout pour empêcher l'étirement */
  line-height: normal; /* Pour normaliser la hauteur de ligne */
  height: auto; /* Forcer la hauteur à s'adapter au contenu */
}

.start-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
}

.high-contrast .start-button {
  background-color: #FFFFFF;
  color: #000000;
}

/* Barre de progression */
.progress-container {
  text-align: center;
  margin-bottom: 40px; /* Marge augmentée */
  background-color: #FFFFFF;
  padding: 25px; /* Padding augmenté */
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.high-contrast .progress-container {
  background-color: #333333;
}

.progress-container h2 {
  margin-top: 0;
  margin-bottom: 20px; /* Marge augmentée */
  color: #333333;
  font-size: 1.6rem; /* Taille augmentée */
}

.high-contrast .progress-container h2 {
  color: #FFFFFF;
}

.progress-bar-container {
  width: 100%;
  height: 24px; /* Hauteur augmentée */
  background-color: #E0E0E0;
  border-radius: 12px; /* Rayon augmenté */
  overflow: hidden;
  margin-bottom: 15px; /* Marge augmentée */
}

.high-contrast .progress-bar-container {
  background-color: #666666;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #4CAF50, #8BC34A);
  border-radius: 12px; /* Rayon augmenté */
  transition: width 1s ease;
}

.high-contrast .progress-bar {
  background: linear-gradient(90deg, #FFFFFF, #CCCCCC);
}

.progress-text {
  font-size: 1.1rem; /* Taille augmentée */
  color: #757575;
  margin: 5px 0 0; /* Marge ajustée */
}

.high-contrast .progress-text {
  color: #CCCCCC;
}

/* Grille des badges */
.badges-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 25px; /* Gap augmenté */
  margin-bottom: 60px; /* Marge augmentée */
}

.badge-card {
  background-color: #FFFFFF;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 25px; /* Padding augmenté */
  position: relative;
}

.badge-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.badge-card.unlocked {
  border: 2px solid #8BC34A;
}

.badge-card.locked {
  opacity: 0.7;
  filter: grayscale(70%);
}

.high-contrast .badge-card.unlocked {
  border: 2px solid #FFFFFF;
}

.badge-icon {
  position: relative;
  width: 130px; /* Taille augmentée */
  height: 130px; /* Taille augmentée */
  margin-bottom: 20px; /* Marge augmentée */
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.badge-emoji {
  font-size: 65px; /* Taille augmentée */
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
  font-size: 2.2rem; /* Taille augmentée */
  border-radius: 50%;
}

.badge-info {
  text-align: center;
  flex-grow: 1;
}

.badge-info h3 {
  margin-top: 0;
  margin-bottom: 12px; /* Marge augmentée */
  color: #333333;
  font-size: 1.3rem; /* Taille augmentée */
}

.badge-info p {
  margin: 0;
  color: #757575;
  font-size: 1rem; /* Taille augmentée */
  line-height: 1.4; /* Interligne ajouté */
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
  border-radius: 20px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  padding: 35px; /* Padding augmenté */
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  animation: scaleUp 0.3s ease;
}

.close-button {
  position: absolute;
  top: 15px;
  right: 15px;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  width: 30px;
  height: 30px;
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
  width: 160px; /* Taille augmentée */
  height: 160px; /* Taille augmentée */
  margin: 0 auto 25px; /* Marge augmentée */
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.badge-detail-emoji {
  font-size: 85px; /* Taille augmentée */
}

.badge-detail-content h2 {
  color: #333333;
  margin-bottom: 20px; /* Marge augmentée */
  font-size: 1.8rem; /* Taille augmentée */
}

.badge-description {
  color: #555555;
  margin-bottom: 25px; /* Marge augmentée */
  line-height: 1.6; /* Interligne augmenté */
  font-size: 1.1rem; /* Taille augmentée */
}

.badge-locked-message {
  color: #757575;
  font-style: italic;
  margin-bottom: 25px; /* Marge augmentée */
  font-size: 1.1rem; /* Taille augmentée */
}

.badge-achievement {
  background-color: #F5F5F5;
  padding: 20px; /* Padding augmenté */
  border-radius: 12px; /* Rayon augmenté */
  margin-bottom: 25px; /* Marge augmentée */
}

.achievement-date {
  font-weight: bold;
  margin-bottom: 8px; /* Marge augmentée */
  color: #4A4D9E;
  font-size: 1.1rem; /* Taille augmentée */
}

.achievement-game {
  color: #757575;
  font-size: 1.05rem; /* Taille augmentée */
}

.badge-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-top: 25px; /* Marge augmentée */
}

.play-button, .share-button {
  padding: 12px 25px; /* Padding augmenté */
  border: none;
  border-radius: 50px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
  font-size: 1.05rem; /* Taille augmentée */
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
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

/* Animations */
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

@keyframes scaleUp {
  from { transform: scale(0.8); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

/* Tailles de texte variables pour accessibilité */
.text-small {
  font-size: 0.9rem;
}

.text-small .main-title {
  font-size: 2rem;
}

.text-small .badge-info h3 {
  font-size: 1rem;
}

.text-large {
  font-size: 1.2rem;
}

.text-large .main-title {
  font-size: 3rem;
}

.text-large .badge-info h3 {
  font-size: 1.4rem;
}

.text-xlarge {
  font-size: 1.4rem;
}

.text-xlarge .main-title {
  font-size: 3.5rem;
}

.text-xlarge .badge-info h3 {
  font-size: 1.6rem;
}

/* Media queries pour la responsivité */
/* Section complète avec la section media query problématique */
@media (max-width: 768px) {
  .rewards-container {
    margin: 30px auto 50px; /* Marges réduites sur mobile */
    padding: 25px 15px; /* Padding réduit sur mobile */
  }
  
  .badges-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 15px; /* Gap réduit pour mobile */
  }
  
  .badge-detail-icon {
    width: 120px;
    height: 120px;
  }
  
  .badge-actions {
    flex-direction: column;
  }
  
  .play-button, .share-button {
    width: 100%;
    margin-bottom: 10px;
  }
  
  .celebration-box {
    flex-direction: column;
    text-align: center;
    padding: 20px;
  }
  
  .celebration-icon {
    margin-right: 0;
    margin-bottom: 15px;
  }
}

@media (max-width: 480px) {
  .rewards-container {
    margin: 20px auto 40px; /* Marges encore réduites pour petits écrans */
    padding: 20px 10px; /* Padding encore réduit pour petits écrans */
    border-radius: 15px; /* Rayon de bordure réduit */
  }
  
  .badges-grid {
    grid-template-columns: 1fr;
  }
  
  .accessibility-controls {
    top: 10px;
    right: 10px;
    gap: 5px;
  }
  
  .accessibility-btn {
    width: 35px;
    height: 35px;
    font-size: 0.9rem;
  }
  
  .main-title {
    font-size: 2rem;
    margin-bottom: 30px;
  }
  
  .empty-badge-icon {
    font-size: 80px;
  }
}
  
@media (max-width: 480px) {
  .accessibility-controls {
    top: 10px;
    right: 10px;
    gap: 5px;
  }
  
  .accessibility-btn {
    width: 35px;
    height: 35px;
    font-size: 0.9rem;
  }
  
  .main-title {
    font-size: 2rem;
    margin-bottom: 30px;
  }
  
  .empty-badge-icon {
    font-size: 80px;
  }
}
</style>