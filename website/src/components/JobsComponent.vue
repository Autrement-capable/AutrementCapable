<template>
  <div class="job-tinder-container" :class="{ 'high-contrast-mode': highContrastMode }">
    <div v-if="!gameStarted" class="job-welcome-screen">
      <div class="welcome-container">
        <div class="welcome-header">
          <div class="guide-character">
            <img src="@/assets/avatars/guide.png" alt="Guide" class="guide-avatar" />
            <div class="speech-bubble">
              <p>Bienvenue dans le jeu Découvre ton Métier ! Prêt à explorer des carrières passionnantes et à trouver ta voie ?</p>
            </div>
          </div>
          
          <h1 class="main-title">Découvre ton Métier</h1>
          <p class="subtitle">Un jeu pour explorer et trouver ta future carrière</p>
        </div>
        
        <div class="welcome-card">
          <div class="card-icon">🚀</div>
          <h2>Comment jouer ?</h2>
          
          <ol class="instructions-list">
            <li>
              <span class="instruction-step">1</span>
              Chaque carte représente un métier différent
            </li>
            <li>
              <span class="instruction-step">2</span>
              Regarde la vidéo et lis la description
            </li>
            <li>
              <span class="instruction-step">3</span>
              Choisis : 
              <ul class="sub-instructions">
                <li>👍 "Ça me plaît" si le métier t'intéresse</li>
                <li>👎 "Pas pour moi" si ce n'est pas ton truc</li>
                <li>ℹ️ "Détails" pour plus d'informations</li>
              </ul>
            </li>
            <li>
              <span class="instruction-step">4</span>
              À la fin, découvre les métiers qui t'ont plu
            </li>
          </ol>
          
          <button @click="startGame" class="start-button">
            <span class="btn-icon">🎮</span>
            <span class="btn-text">Commencer à explorer</span>
          </button>
        </div>
      </div>
    </div>
    <!-- Animation badge débloqué -->
    <div v-if="showBadgeUnlock" class="badge-unlock-overlay">
      <div class="badge-unlock-animation">
        <div class="badge-icon">🏆</div>
        <h2>Badge débloqué !</h2>
        <h3>{{ badgeData.name }}</h3>
        <p>{{ badgeData.description }}</p>
        <button @click="closeBadgeAnimation" class="close-animation-btn">Continuer</button>
      </div>
    </div>

    <!-- En-tête -->
    <div class="tinder-header">
      <h1 class="tinder-title">Découvre ton métier</h1>
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
        <span class="progress-text">{{ currentIndex + 1 }}/{{ batchSize }}</span>
      </div>
    </div>

    <!-- Zone des cartes -->
    <div class="cards-area">
      <transition name="swipe">
        <div v-if="currentMetier" class="job-card">
          <div class="job-card-inner">
            <h2 class="job-title">{{ currentMetier.name }}</h2>
            
            <div class="job-media">
              <!-- Intégration YouTube -->
              <div class="job-media">
                <!-- Intégration YouTube -->
                <div class="video-player">
                  <video 
                    v-if="currentMetier.video"
                    :src="getVideoSource(currentMetier.video)"
                    :poster="currentMetier.poster"
                    controls
                    preload="metadata"
                    class="video-element"
                  >
                    Votre navigateur ne supporte pas la lecture de vidéos.
                  </video>
                  <div v-else class="video-placeholder">
                    <div class="placeholder-icon">🎬</div>
                    <p>Vidéo non disponible</p>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="job-description">
              <p>{{ currentMetier.description }}</p>
            </div>
            
            <div class="job-skills">
              <div v-for="(skill, index) in currentMetier.skills" :key="index" class="skill-tag">
                {{ skill }}
              </div>
            </div>
          </div>
          
          <div class="card-actions">
            <button @click="likeJob" class="action-btn like-btn">
              <span class="action-icon">👍</span>
              <span class="action-text">Ça me plaît</span>
            </button>
            <button @click="showDetails" class="action-btn info-btn">
              <span class="action-icon">ℹ️</span>
              <span class="action-text">Détails</span>
            </button>
            <button @click="dislikeJob" class="action-btn dislike-btn">
              <span class="action-icon">👎</span>
              <span class="action-text">Pas pour moi</span>
            </button>
          </div>
        </div>
        
        <div v-else-if="batchCompleted" class="batch-complete-card">
          <h2>Lot terminé !</h2>
          <p>Tu as découvert {{ batchSize }} métiers.</p>
          <p v-if="likedJobs.length > 0">Tu as aimé {{ getLikedJobsInCurrentBatch() }} métier(s).</p>
          <p>Souhaites-tu continuer à découvrir d'autres métiers ?</p>
          <div class="batch-actions">
            <button @click="loadNextBatch" class="action-btn continue-btn">
              <span class="action-icon">▶️</span>
              <span class="action-text">Continuer</span>
            </button>
            <button @click="finishAndShowResults" class="action-btn finish-btn">
              <span class="action-icon">🏁</span>
              <span class="action-text">Terminer</span>
            </button>
          </div>
        </div>
        
        <div v-else-if="allJobsSeen" class="all-jobs-seen-card">
          <h2>Bravo !</h2>
          <p>Tu as découvert tous les métiers disponibles.</p>
          <p v-if="likedJobs.length > 0">Tu as aimé {{ likedJobs.length }} métier(s) au total.</p>
          <button @click="goToDashboard" class="action-btn dashboard-btn">
            <span class="action-icon">🏠</span>
            <span class="action-text">Retour à l'accueil</span>
          </button>
        </div>
        
        <div v-else class="loading-card">
          <div class="loading-spinner"></div>
          <p>Chargement des métiers...</p>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import { metiersData } from '@/data/metiersData.js'

export default {
  name: 'JobComponent',
  data() {
    return {
      allJobs: metiersData,
      currentBatch: [],
      currentIndex: 0,
      batchSize: 3,
      seenJobs: [],
      likedJobs: [],
      currentBatchIds: [], // IDs des métiers dans le lot actuel
      batchCompleted: false,
      allJobsSeen: false,
      showResults: false,
      highContrastMode: false,
      showBadgeUnlock: false,
      badgeData: {
        name: "",
        description: ""
      },
      gameStarted: false,
    }
  },
  computed: {
    currentMetier() {
      if (this.currentBatch.length === 0 || this.currentIndex >= this.currentBatch.length) {
        return null;
      }
      return this.currentBatch[this.currentIndex];
    },
    progressPercentage() {
      if (this.batchSize === 0) return 0;
      return Math.min(100, ((this.currentIndex + 1) / this.batchSize) * 100);
    },
    availableJobs() {
      // Filtrer les métiers qui n'ont pas encore été vus
      return this.allJobs.filter(job => !this.seenJobs.includes(job.id));
    }
  },
  created() {
    // Vérifier que metiersData est correctement importé
    console.log("Vérification de l'importation:", this.allJobs);
    console.log("Premier métier importé:", this.allJobs.length > 0 ? this.allJobs[0] : "Aucun métier");
    
    // Vérifier si l'URL vidéo est présente dans les données importées
    if (this.allJobs.length > 0) {
      const firstJob = this.allJobs[0];
      console.log("URL vidéo du premier métier:", firstJob.videoUrl);
    }
    
    this.loadSavedData();
    this.loadInitialBatch();
  },
  methods: {
    startGame() {
      this.gameStarted = true;
    },
    // Convertir l'URL YouTube en URL d'intégration
    getVideoSource(videoPath) {
      if (!videoPath) {
        return '';
      }
      return videoPath;
    },
    
    loadSavedData() {
      // Charger les paramètres d'accessibilité
      const accessibilitySettings = localStorage.getItem('accessibilitySettings');
      if (accessibilitySettings) {
        try {
          const settings = JSON.parse(accessibilitySettings);
          this.highContrastMode = settings.highContrast || false;
        } catch (e) {
          console.error('Erreur lors du chargement des paramètres d\'accessibilité:', e);
        }
      }
      
      // Charger les métiers déjà vus
      const seenJobsData = localStorage.getItem('seen-metiers');
      if (seenJobsData) {
        try {
          this.seenJobs = JSON.parse(seenJobsData);
        } catch (e) {
          console.error('Erreur lors du chargement des métiers vus:', e);
          this.seenJobs = [];
        }
      }
      
      // Charger les métiers aimés
      const likedJobsData = localStorage.getItem('liked-metiers');
      if (likedJobsData) {
        try {
          const likedIds = JSON.parse(likedJobsData);
          this.likedJobs = this.allJobs.filter(job => likedIds.includes(job.id));
        } catch (e) {
          console.error('Erreur lors du chargement des métiers aimés:', e);
          this.likedJobs = [];
        }
      }
    },
    saveData() {
      // Sauvegarder les paramètres d'accessibilité
      localStorage.setItem('accessibilitySettings', JSON.stringify({
        highContrast: this.highContrastMode
      }));
      
      // Sauvegarder les métiers vus
      localStorage.setItem('seen-metiers', JSON.stringify(this.seenJobs));
      
      // Sauvegarder les métiers aimés
      const likedIds = this.likedJobs.map(job => job.id);
      localStorage.setItem('liked-metiers', JSON.stringify(likedIds));
    },
    
    // Obtenir le nombre de métiers aimés dans le lot actuel
    getLikedJobsInCurrentBatch() {
      return this.likedJobs.filter(job => this.currentBatchIds.includes(job.id)).length;
    },
    
    loadInitialBatch() {
      this.loadNextBatch();
    },

    loadNextBatch() {
      this.currentBatch = [];
      this.currentIndex = 0;
      this.currentBatchIds = [];
      this.batchCompleted = false;
      
      // Vérifier s'il reste des métiers à montrer
      if (this.availableJobs.length === 0) {
        this.allJobsSeen = true;
        return;
      }
      
      // Sélectionner aléatoirement un batch de métiers non vus
      const batchSize = Math.min(this.batchSize, this.availableJobs.length);
      const availableIndices = Array.from({ length: this.availableJobs.length }, (_, i) => i);
      
      for (let i = 0; i < batchSize; i++) {
        const randomIndex = Math.floor(Math.random() * availableIndices.length);
        const selectedIndex = availableIndices.splice(randomIndex, 1)[0];
        
        // Créer une vraie copie profonde du métier pour éviter les problèmes de référence
        const originalMetier = this.availableJobs[selectedIndex];
        const selectedMetier = JSON.parse(JSON.stringify(originalMetier));
        
        console.log(`Métier sélectionné: ${selectedMetier.name}, URL: ${selectedMetier.videoUrl}`);
        
        this.currentBatch.push(selectedMetier);
        this.currentBatchIds.push(selectedMetier.id);
      }
    },

    likeJob() {
      if (!this.currentMetier) return;
      
      // Ajouter aux métiers vus
      if (!this.seenJobs.includes(this.currentMetier.id)) {
        this.seenJobs.push(this.currentMetier.id);
      }
      
      // Ajouter aux métiers aimés s'il n'y est pas déjà
      if (!this.likedJobs.some(job => job.id === this.currentMetier.id)) {
        this.likedJobs.push(this.currentMetier);
      }
      
      this.saveData();
      this.checkBadges();
      this.nextCard();
    },
    dislikeJob() {
      if (!this.currentMetier) return;
      
      // Ajouter uniquement aux métiers vus
      if (!this.seenJobs.includes(this.currentMetier.id)) {
        this.seenJobs.push(this.currentMetier.id);
      }
      
      this.saveData();
      this.checkBadges();
      this.nextCard();
    },
    showDetails() {
      if (!this.currentMetier) return;
      
      // Rediriger vers la page de détails du métier
      this.$router.push({ name: 'MetierDetail', params: { id: this.currentMetier.id } });
    },
    nextCard() {
      this.currentIndex++;
      
      // Vérifier si tous les métiers du lot ont été vus
      if (this.currentIndex >= this.currentBatch.length) {
        this.batchCompleted = true;
      }
    },
    finishAndShowResults() {
      this.$router.push({ name: 'Dashboard' });
    },
    closeResults() {
      this.showResults = false;
      this.loadNextBatch();
    },
    goToDashboard() {
      this.$router.push({ name: 'Dashboard' });
    },
    goToJobDetails(job) {
      this.$router.push({ name: 'MetierDetail', params: { id: job.id } });
    },
    toggleHighContrast() {
      this.highContrastMode = !this.highContrastMode;
      this.saveData();
    },
    checkBadges() {
      // Vérifier l'obtention de badges en fonction du nombre de métiers vus
      if (this.seenJobs.length >= 5 && !this.hasBadge('explorer_debutant')) {
        this.unlockBadge('explorer_debutant', 'Explorateur Débutant', 'Tu as découvert 5 métiers différents !');
      } else if (this.seenJobs.length >= 20 && !this.hasBadge('explorer_avance')) {
        this.unlockBadge('explorer_avance', 'Explorateur Avancé', 'Tu as découvert 20 métiers différents !');
      } else if (this.seenJobs.length >= 40 && !this.hasBadge('explorer_expert')) {
        this.unlockBadge('explorer_expert', 'Explorateur Expert', 'Tu as découvert 40 métiers différents !');
      }
      
      // Vérifier les badges pour les métiers aimés
      if (this.likedJobs.length >= 3 && !this.hasBadge('passionne_debutant')) {
        this.unlockBadge('passionne_debutant', 'Passionné Débutant', 'Tu as trouvé 3 métiers qui te plaisent !');
      } else if (this.likedJobs.length >= 10 && !this.hasBadge('passionne_avance')) {
        this.unlockBadge('passionne_avance', 'Passionné Avancé', 'Tu as trouvé 10 métiers qui te plaisent !');
      }
    },
    hasBadge(badgeId) {
      // Vérifier si l'utilisateur a déjà obtenu ce badge
      try {
        const userBadges = JSON.parse(localStorage.getItem('user-badges') || '[]');
        return userBadges.includes(badgeId);
      } catch (e) {
        console.error('Erreur lors de la vérification des badges:', e);
        return false;
      }
    },
    unlockBadge(badgeId, name, description) {
      try {
        // Sauvegarder le badge dans le localStorage
        const userBadges = JSON.parse(localStorage.getItem('user-badges') || '[]');
        userBadges.push(badgeId);
        localStorage.setItem('user-badges', JSON.stringify(userBadges));
        
        // Afficher l'animation de badge débloqué
        this.badgeData = {
          name: name,
          description: description
        };
        this.showBadgeUnlock = true;
      } catch (e) {
        console.error('Erreur lors du déblocage du badge:', e);
      }
    },
    closeBadgeAnimation() {
      this.showBadgeUnlock = false;
    }
  }
}
</script>

<style scoped>
.job-tinder-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
}

/* En-tête et barre de progression */
.tinder-header {
  text-align: center;
  margin-bottom: 20px;
}

.tinder-title {
  font-size: 28px;
  color: #ff6b6b;
  margin-bottom: 15px;
}

.progress-bar {
  height: 10px;
  background-color: #e0e0e0;
  border-radius: 5px;
  overflow: hidden;
  position: relative;
  margin-bottom: 20px;
}

.progress-fill {
  height: 100%;
  background-color: #4caf50;
  transition: width 0.3s ease;
}

.progress-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 12px;
  color: #333;
  font-weight: bold;
}

/* Zone des cartes */
.cards-area {
  position: relative;
  height: 600px;
  margin-bottom: 20px;
}

.video-player {
  position: relative;
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  padding-top: 56.25%; /* Ratio 16:9 */
  margin-bottom: 10px;
  border-radius: 8px;
  overflow: hidden;
}

.video-element {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  position: absolute;
  top: 0;
  left: 0;
}

.placeholder-icon {
  font-size: 40px;
  margin-bottom: 10px;
  opacity: 0.5;
}

.job-card {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  margin: 0 auto;
  width: 100%;
  max-width: 800px;
  background-color: white;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.job-card-inner {
  padding: 20px;
}

.job-title {
  font-size: 24px;
  color: #333;
  text-align: center;
  margin: 0 0 15px 0;
}

/* Intégration YouTube */
.job-media {
  margin-bottom: 15px;
  text-align: center;
}

.youtube-embed {
  position: relative;
  width: 100%;
  padding-top: 56.25%; /* Ratio 16:9 */
  margin-bottom: 10px;
  border-radius: 8px;
  overflow: hidden;
}

.youtube-embed iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: none;
}

.job-welcome-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 1);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 200;
  font-family: 'Arial', sans-serif;
}

.welcome-container {
  width: 100%;
  max-width: 1000px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.welcome-header {
  text-align: center;
  margin-bottom: 30px;
}

.guide-character {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.guide-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 3px solid #ff6b6b;
  margin-right: 15px;
}

.speech-bubble {
  background-color: white;
  border-radius: 15px;
  padding: 15px;
  max-width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  position: relative;
}

.speech-bubble::before {
  content: '';
  position: absolute;
  left: -10px;
  top: 50%;
  transform: translateY(-50%);
  border-width: 10px 10px 10px 0;
  border-style: solid;
  border-color: transparent white transparent transparent;
}

.main-title {
  font-size: 2.5rem;
  color: #ff6b6b;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 1.2rem;
  color: #666;
}

.welcome-card {
  background-color: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
}

.card-icon {
  font-size: 3rem;
  text-align: center;
  margin-bottom: 20px;
  color: #ff6b6b;
}

.welcome-card h2 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

.instructions-list {
  padding-left: 20px;
  margin-bottom: 20px;
}

.instructions-list li {
  margin-bottom: 15px;
  font-size: 1rem;
  display: flex;
  align-items: center;
}

.instruction-step {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  background-color: #ff6b6b;
  color: white;
  border-radius: 50%;
  margin-right: 15px;
  flex-shrink: 0;
}

.sub-instructions {
  margin-top: 10px;
  padding-left: 30px;
  list-style-type: disc;
}

.accessibility-section {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.accessibility-toggle {
  display: flex;
  align-items: center;
  font-size: 0.9rem;
  color: #666;
}

.accessibility-toggle input {
  margin-right: 10px;
}

.start-button {
  display: block;
  width: 100%;
  padding: 15px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.start-button:hover {
  background-color: #45a049;
  transform: translateY(-3px);
}

.btn-icon {
  margin-right: 10px;
  font-size: 1.5rem;
}

.job-description {
  font-size: 16px;
  color: #555;
  margin-bottom: 15px;
  line-height: 1.5;
}

.job-skills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 15px;
}

.skill-tag {
  background-color: #e8f5e9;
  color: #2e7d32;
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 14px;
  font-weight: bold;
}

.card-actions {
  display: flex;
  justify-content: space-around;
  padding: 15px;
  background-color: #f5f5f5;
}

.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 15px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: transform 0.2s, box-shadow 0.2s;
}

.action-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
}

.action-icon {
  font-size: 20px;
  margin-bottom: 5px;
}

.like-btn {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.dislike-btn {
  background-color: #ffebee;
  color: #c62828;
}

.info-btn {
  background-color: #e3f2fd;
  color: #1565c0;
}

/* Cartes de fin de lot */
.batch-complete-card,
.all-jobs-seen-card,
.loading-card {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  margin: 0 auto;
  width: 100%;
  max-width: 500px;
  height: 350px;
  background-color: white;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.batch-complete-card h2,
.all-jobs-seen-card h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
}

.batch-complete-card p,
.all-jobs-seen-card p {
  font-size: 16px;
  color: #555;
  margin-bottom: 10px;
}

.batch-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 20px;
}

.continue-btn {
  background-color: #4caf50;
  color: white;
}

.finish-btn {
  background-color: #ff6b6b;
  color: white;
}

.dashboard-btn {
  background-color: #2196f3;
  color: white;
  margin-top: 20px;
}

/* Animation de chargement */
.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #ff6b6b;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Animation de swipe */
.swipe-enter-active {
  transition: all 0.3s ease;
}

.swipe-leave-active {
  transition: all 0.8s cubic-bezier(1.0, 0.5, 0.8, 1.0);
}

.swipe-enter, .swipe-leave-to {
  transform: translateX(20px);
  opacity: 0;
}

/* Résultats */
.results-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.results-container {
  background-color: white;
  border-radius: 15px;
  padding: 30px;
  width: 90%;
  max-width: 800px;
  max-height: 80vh;
  overflow-y: auto;
}

.results-title {
  font-size: 24px;
  color: #ff6b6b;
  text-align: center;
  margin-bottom: 20px;
}

.liked-jobs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.liked-job-item {
  background-color: #f5f5f5;
  border-radius: 10px;
  overflow: hidden;
  position: relative;
}

.liked-job-img {
  width: 100%;
  height: 120px;
  object-fit: cover;
}

.play-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 30px;
  color: white;
  text-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
  opacity: 0.8;
  pointer-events: none;
}

.liked-job-info {
  padding: 15px;
}

.liked-job-info h3 {
  font-size: 16px;
  margin: 0 0 10px 0;
  color: #333;
}

.view-btn {
  background-color: #2196f3;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 8px 12px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.view-btn:hover {
  background-color: #1976d2;
}

.no-liked-jobs {
  text-align: center;
  padding: 30px;
  color: #555;
}

.results-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 20px;
}

.continue-exploring-btn {
  background-color: #4caf50;
  color: white;
}

/* Animation de badge débloqué */
.badge-unlock-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 200;
}

.badge-unlock-animation {
  background-color: white;
  border-radius: 15px;
  padding: 30px;
  text-align: center;
  max-width: 400px;
  animation: popup 0.5s;
}

@keyframes popup {
  0% {
    transform: scale(0.8);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.badge-icon {
  font-size: 60px;
  margin-bottom: 20px;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

.badge-unlock-animation h2 {
  font-size: 24px;
  color: #ff6b6b;
  margin-bottom: 10px;
}

.badge-unlock-animation h3 {
  font-size: 20px;
  color: #333;
  margin-bottom: 15px;
}

.close-animation-btn {
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 20px;
  transition: background-color 0.2s;
}

.close-animation-btn:hover {
  background-color: #388e3c;
}

/* Contrôles d'accessibilité */
.accessibility-controls {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 90;
}

.accessibility-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background-color: white;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  font-size: 20px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.accessibility-btn:hover {
  background-color: #f5f5f5;
}

/* Mode contraste élevé */
.high-contrast-mode {
  background-color: #000;
  color: #fff;
}

.high-contrast-mode .tinder-title {
  color: #ff9800;
}

.high-contrast-mode .job-card,
.high-contrast-mode .batch-complete-card,
.high-contrast-mode .all-jobs-seen-card,
.high-contrast-mode .loading-card,
.high-contrast-mode .results-container,
.high-contrast-mode .badge-unlock-animation {
  background-color: #222;
  color: #fff;
}

.high-contrast-mode .job-title,
.high-contrast-mode .batch-complete-card h2,
.high-contrast-mode .all-jobs-seen-card h2,
.high-contrast-mode .results-title,
.high-contrast-mode .liked-job-info h3,
.high-contrast-mode .badge-unlock-animation h2,
.high-contrast-mode .badge-unlock-animation h3 {
  color: #ff9800;
}

.high-contrast-mode .job-description,
.high-contrast-mode .batch-complete-card p,
.high-contrast-mode .all-jobs-seen-card p {
  color: #fff;
}

.high-contrast-mode .skill-tag {
  background-color: #333;
  color: #4caf50;
}

.high-contrast-mode .card-actions {
  background-color: #333;
}

.high-contrast-mode .like-btn {
  background-color: #1b5e20;
  color: #fff;
}

.high-contrast-mode .dislike-btn {
  background-color: #b71c1c;
  color: #fff;
}

.high-contrast-mode .info-btn {
  background-color: #0d47a1;
  color: #fff;
}

.high-contrast-mode .liked-job-item {
  background-color: #333;
}

.high-contrast-mode .accessibility-btn {
  background-color: #333;
  color: #fff;
}

/* Responsive design */
@media (max-width: 600px) {
  .liked-jobs-grid {
    grid-template-columns: 1fr;
  }
  
  .results-container {
    padding: 20px;
  }
  
  .action-text {
    font-size: 14px;
  }
  
  .job-card-inner {
    padding: 15px;
  }
  
  .job-title {
    font-size: 20px;
  }
  
  .cards-area {
    position: relative;
    z-index: 100;
  }

  .welcome-container {
    padding: 10px;
  }

  .guide-character {
    flex-direction: column;
    text-align: center;
  }

  .guide-avatar {
    margin-right: 0;
    margin-bottom: 15px;
  }

  .speech-bubble {
    max-width: 100%;
  }

  .main-title {
    font-size: 2rem;
  }

  .subtitle {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .batch-actions {
    flex-direction: column;
    gap: 10px;
  }
  
  .cards-area {
    height: 480px; /* Encore plus petit pour les très petits écrans */
  }
}

@media (max-width: 1200px) {
  .job-tinder-container {
    max-width: 100%;
    padding: 10px;
  }

  .job-card {
    max-width: 100%;
  }

  .video-player {
    max-width: 100%;
  }
}
</style>