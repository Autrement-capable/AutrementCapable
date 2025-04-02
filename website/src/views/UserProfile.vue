<template>
  <!-- Utiliser soit le fond animé soit le fond statique en fonction de la propriété animationsEnabled -->
  <space-background v-if="animationsEnabled" :theme="currentTheme" />
  <static-backgrounds v-else :theme="currentTheme" />
  
  <div class="profile-container" :class="{ 'high-contrast': highContrastMode }">
    <!-- En-tête avec avatar et message de bienvenue -->
    <div class="profile-header">
      <div class="avatar-container">
        <img :src="userProfile.avatar" alt="Avatar" class="user-avatar" />
        <div class="level-badge">Niveau {{userProfile.level}}</div>
      </div>
      <div class="welcome-message">
        <h1>Salut {{userProfile.firstName}} ! 👋</h1>
        <p>Super de te revoir aujourd'hui !</p>
      </div>
    </div>

    <!-- Onglets de navigation -->
    <div class="profile-tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        @click="activeTab = tab.id"
        :class="{ active: activeTab === tab.id }"
        class="tab-button"
      >
        <span class="tab-icon">{{tab.icon}}</span>
        <span class="tab-label">{{tab.label}}</span>
      </button>
    </div>

    <!-- Contenu du profil -->
    <div class="tab-content">
      <!-- Onglet Informations -->
      <div v-if="activeTab === 'info'" class="info-tab">
        <div class="info-cards">
          <!-- Carte Informations Personnelles -->
          <div class="info-card">
            <div class="card-header">
              <h2>🧩 Mes informations</h2>
              <button class="edit-button" @click="editPersonalInfo">✏️</button>
            </div>
            <div class="card-content">
              <div class="info-item">
                <span class="info-label">Prénom:</span>
                <span class="info-value">{{userProfile.firstName}}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Nom:</span>
                <span class="info-value">{{userProfile.lastName}}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Âge:</span>
                <span class="info-value">{{userProfile.age}} ans</span>
              </div>
              <div class="info-item">
                <span class="info-label">Ville:</span>
                <span class="info-value">{{userProfile.city}}</span>
              </div>
            </div>
          </div>

          <!-- Carte Centres d'intérêt -->
          <div class="info-card">
            <div class="card-header">
              <h2>🎮 Mes centres d'intérêt</h2>
              <button class="edit-button" @click="editInterests">✏️</button>
            </div>
            <div class="card-content">
              <div class="interests-container">
                <div 
                  v-for="interest in userProfile.interests" 
                  :key="interest"
                  class="interest-tag"
                >
                  {{interest}}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Bouton pour générer le CV -->
        <div class="cv-generator-container">
          <button @click="generateCV" class="generate-cv-button">
            <span class="button-icon">📄</span>
            <span class="button-text">Générer mon CV</span>
          </button>
        </div>
      </div>

      <!-- Onglet Paramètres -->
      <div v-if="activeTab === 'settings'" class="settings-tab">
        <h2 class="section-title">Mes paramètres</h2>
        
        <div class="settings-card">
          <h3>Accessibilité</h3>
          <div class="setting-item">
            <label for="contrast-toggle">Mode contraste élevé</label>
            <div class="toggle-switch">
              <input 
                type="checkbox" 
                id="contrast-toggle" 
                v-model="highContrastMode"
                @change="saveAccessibilitySettings"
              >
              <span class="toggle-slider"></span>
            </div>
          </div>
          <div class="setting-item">
            <label for="text-size">Taille du texte</label>
            <div class="setting-controls">
              <button @click="decreaseTextSize" class="text-size-button">A-</button>
              <button @click="increaseTextSize" class="text-size-button">A+</button>
            </div>
          </div>
          <!-- Ajout du paramètre d'animation -->
          <div class="setting-item">
            <label for="animation-toggle">Animations de fond</label>
            <div class="toggle-switch">
              <input 
                type="checkbox" 
                id="animation-toggle" 
                v-model="animationsEnabled"
                @change="toggleAnimations"
              >
              <span class="toggle-slider"></span>
            </div>
          </div>
        </div>
        
        <div class="settings-card">
          <h3>Gestion du compte</h3>
          <div class="setting-item device-switch">
            <p>Changer d'appareil</p>
            <button @click="switchDevice" class="switch-device-button">
              <span class="button-icon">📱</span>
              <span class="button-text">Transférer mon compte</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Message de confirmation pour le CV -->
    <div v-if="showCVMessage" class="cv-message">
      <div class="cv-message-content">
        <div class="message-icon">✅</div>
        <h3>Super !</h3>
        <p>Ton CV a été généré et sauvegardé !</p>
        <button @click="showCVMessage = false" class="close-message-button">Continuer</button>
      </div>
    </div>

    <!-- Message de confirmation pour le transfert d'appareil -->
    <div v-if="showTransferCode" class="transfer-overlay">
      <div class="transfer-modal">
        <h3>Code de transfert</h3>
        <div class="transfer-code">{{ transferCode }}</div>
        <p>Entre ce code sur ton nouvel appareil pour y retrouver ton compte.</p>
        <div class="transfer-timer">Expire dans: {{ transferTimeLeft }} secondes</div>
        <button @click="cancelTransfer" class="close-transfer-button">Fermer</button>
      </div>
    </div>
  </div>
</template>
  
<script>
import SpaceBackground from '@/components/SpaceBackground.vue';
import StaticBackgrounds from '@/components/StaticBackgrounds.vue';
import { BackgroundManager } from '@/utils/BackgroundManager';
import { BackgroundMixin } from '@/utils/BackgroundMixin';

export default {
  name: 'UserProfile',
  mixins: [BackgroundMixin],
  components: {
    SpaceBackground,
    StaticBackgrounds
  },
  data() {
    return {
      // Données du profil utilisateur
      userProfile: {
        firstName: "Lucas",
        lastName: "Martin",
        age: 16,
        city: "Lyon",
        level: 3,
        avatar: require('@/assets/jeunefemme.png'), // Chemin à adapter selon votre structure
        interests: ["Jeux vidéo", "Musique", "Dessin", "Programmation", "Animaux"],
        skills: [
          { name: "Créativité", level: 4 },
          { name: "Informatique", level: 5 },
          { name: "Organisation", level: 2 },
          { name: "Communication", level: 3 },
          { name: "Logique", level: 4 }
        ]
      },
      
      // Onglets disponibles
      tabs: [
        { id: 'info', label: 'Mon profil', icon: '👤' },
        { id: 'settings', label: 'Paramètres', icon: '⚙️' }
      ],
      activeTab: 'info',
      
      // Badges
      badges: [
        {
          id: 1,
          title: 'Premier pas',
          description: 'Tu as complété ton profil !',
          icon: '🚀',
          color: '#4CAF50',
          unlocked: true
        },
        {
          id: 2,
          title: 'Explorateur',
          description: 'Tu as exploré toutes les sections de l\'application',
          icon: '🧭',
          color: '#2196F3',
          unlocked: true
        },
        {
          id: 3,
          title: 'Créatif',
          description: 'Tu as partagé tes centres d\'intérêt',
          icon: '🎨',
          color: '#9C27B0',
          unlocked: true
        },
        {
          id: 4,
          title: 'Communiquant',
          description: 'Tu as participé à un atelier de groupe',
          icon: '💬',
          color: '#FF9800',
          unlocked: false
        },
        {
          id: 5,
          title: 'Expert',
          description: 'Tu as atteint le niveau 5',
          icon: '⭐',
          color: '#FFD700',
          unlocked: false
        }
      ],
      
      // Paramètres d'accessibilité
      highContrastMode: false,
      textSizeLevel: 0,
      
      // États pour les interactions
      showCVMessage: false,
      showTransferCode: false,
      transferCode: "123456",
      transferTimeLeft: 60,
      transferInterval: null,
      
      // Paramètres de fond d'écran
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
    badgesProgressPercentage() {
      return (this.unlockedBadgesCount / this.totalBadgesCount) * 100;
    }
  },
  
  created() {
    // Chargement des paramètres d'accessibilité
    this.loadAccessibilitySettings();
    
    // Chargement des paramètres de thème et d'animation
    this.currentTheme = BackgroundManager.getCurrentTheme();
    this.animationsEnabled = BackgroundManager.areAnimationsEnabled();
  },
  
  methods: {
    // Méthode pour activer/désactiver les animations
    toggleAnimations() {
      BackgroundManager.setAnimationsEnabled(this.animationsEnabled);
    },
    
    // Méthodes d'édition (simulées pour l'exemple)
    editPersonalInfo() {
      alert("Fonctionnalité d'édition des informations personnelles à implémenter");
    },
    editInterests() {
      alert("Fonctionnalité d'édition des centres d'intérêt à implémenter");
    },
    editSkills() {
      alert("Fonctionnalité d'édition des compétences à implémenter");
    },
    
    // Génération du CV
    generateCV() {
      // Simulation d'une génération de CV
      setTimeout(() => {
        this.showCVMessage = true;
        // Le message se ferme automatiquement après 5 secondes
        setTimeout(() => {
          this.showCVMessage = false;
        }, 5000);
      }, 1000);
    },
    
    // Changement d'appareil
    switchDevice() {
      this.showTransferCode = true;
      this.transferTimeLeft = 60;
      
      // Compte à rebours
      this.transferInterval = setInterval(() => {
        this.transferTimeLeft--;
        if (this.transferTimeLeft <= 0) {
          this.cancelTransfer();
        }
      }, 1000);
    },
    
    cancelTransfer() {
      clearInterval(this.transferInterval);
      this.showTransferCode = false;
    },

    // Méthodes d'accessibilité
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
    
    increaseTextSize() {
      if (this.textSizeLevel < 3) {
        this.textSizeLevel++;
        this.applyTextSize();
        this.saveAccessibilitySettings();
      }
    },
    
    decreaseTextSize() {
      if (this.textSizeLevel > 0) {
        this.textSizeLevel--;
        this.applyTextSize();
        this.saveAccessibilitySettings();
      }
    },
    
    applyTextSize() {
      document.body.classList.remove('text-size-1', 'text-size-2', 'text-size-3');
      if (this.textSizeLevel > 0) {
        document.body.classList.add(`text-size-${this.textSizeLevel}`);
      }
    }
  }
};
</script>

<style scoped>
/* Styles généraux */

.profile-container {
  font-family: 'Comic Sans MS', 'Chalkboard SE', 'Marker Felt', sans-serif;
  max-width: 900px;
  width: 100%;
  padding: 20px;
  background-color: #f5f8ff;
  border-radius: 20px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  transition: all 0.3s ease;
}
h1, h2, h3 {
  color: #4A4D9E;
  margin-top: 0;
}

button {
  cursor: pointer;
  font-family: inherit;
}

/* En-tête du profil */
.profile-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.avatar-container {
  position: relative;
  margin-right: 20px;
}

.user-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 4px solid #FFD700;
  object-fit: cover;
  background-color: #fff;
}

.level-badge {
  position: absolute;
  bottom: 0;
  right: 0;
  background-color: #4CAF50;
  color: white;
  border-radius: 12px;
  padding: 4px 8px;
  font-size: 0.9rem;
  font-weight: bold;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.welcome-message h1 {
  margin-bottom: 5px;
  font-size: 2rem;
}

.welcome-message p {
  margin: 0;
  font-size: 1.2rem;
  color: #666;
}

/* Onglets de navigation */
.profile-tabs {
  display: flex;
  background-color: #fff;
  border-radius: 15px;
  margin-bottom: 10px;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.tab-button {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 5px;
  background: none;
  border: none;
  transition: all 0.3s ease;
  color: #666;
}

.tab-button.active {
  background-color: #4A4D9E;
  color: white;
}

.tab-icon {
  font-size: 1.8rem;
  margin-bottom: 5px;
}

.tab-label {
  font-size: 1rem;
  font-weight: bold;
}

/* Contenu des onglets */
.tab-content {
  background-color: #fff;
  border-radius: 15px;
  padding: 15px;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
}

.section-title {
  text-align: center;
  margin-bottom: 10px;
  position: relative;
  padding-bottom: 10px;
}

.section-title:after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 3px;
  background-color: #FFD700;
  border-radius: 3px;
}

/* Cartes d'information */
.info-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.info-card {
  background-color: #f9f9f9;
  border-radius: 15px;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #f0f0f0;
}

.card-header h2 {
  margin: 0;
  font-size: 1.3rem;
}

.edit-button {
  background: none;
  border: none;
  font-size: 1.3rem;
  transition: transform 0.2s ease;
}

.edit-button:hover {
  transform: scale(1.2);
}

.card-content {
  padding: 15px;
}

/* Informations personnelles */
.info-item {
  margin-bottom: 10px;
  display: flex;
  gap: 10px;
}

.info-label {
  font-weight: bold;
  color: #666;
  min-width: 70px;
}

.info-value {
  color: #333;
}

/* Centres d'intérêt */
.interests-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.interest-tag {
  background-color: #e3f2fd;
  color: #1976d2;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: bold;
}

/* Compétences */
.skills-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.skill-item {
  width: 100%;
}

.skill-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.skill-name {
  font-weight: bold;
}

.skill-level {
  color: #666;
}

.skill-bar-container {
  width: 100%;
  height: 12px;
  background-color: #e0e0e0;
  border-radius: 6px;
  overflow: hidden;
}

.skill-bar {
  height: 100%;
  background: linear-gradient(90deg, #4A4D9E, #9C27B0);
  border-radius: 6px;
  transition: width 1s ease;
}

/* Bouton de génération de CV */
.cv-generator-container {
  text-align: center;
  margin: 30px 0 10px;
}

.generate-cv-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 15px 30px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 30px;
  font-size: 1.2rem;
  font-weight: bold;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  margin: 0 auto;
}

.generate-cv-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

.button-icon {
  margin-right: 10px;
  font-size: 1.4rem;
}

/* Badges */
.progress-container {
  text-align: center;
  margin-bottom: 30px;
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
}

.progress-container h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
}

.progress-bar-container {
  width: 100%;
  height: 20px;
  background-color: #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 10px;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #4CAF50, #8BC34A);
  border-radius: 10px;
  transition: width 1s ease;
}

.progress-text {
  font-size: 1rem;
  color: #666;
  margin: 5px 0 0;
}

.badges-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
}

.badge-card {
  background-color: #f9f9f9;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  position: relative;
}

.badge-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
}

.badge-card.unlocked {
  border: 2px solid #8BC34A;
}

.badge-card.locked {
  opacity: 0.7;
  filter: grayscale(70%);
}

.badge-icon {
  position: relative;
  width: 80px;
  height: 80px;
  margin-bottom: 15px;
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
  font-size: 1.8rem;
  border-radius: 50%;
}

.badge-info {
  text-align: center;
  flex-grow: 1;
}

.badge-info h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #333;
  font-size: 1.1rem;
}

.badge-info p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

/* Paramètres */
.settings-tab {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.settings-card {
  background-color: #f9f9f9;
  border-radius: 15px;
  padding: 10px;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
}

.settings-card h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
  font-size: 1.2rem;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e0e0e0;
}

.setting-item:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.device-switch {
  flex-direction: column;
  align-items: flex-start;
}

.device-switch p {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
}

/* Interrupteur toggle */
.toggle-switch {
  position: relative;
  width: 60px;
  height: 30px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 34px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 22px;
  width: 22px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .toggle-slider {
  background-color: #4CAF50;
}

input:checked + .toggle-slider:before {
  transform: translateX(30px);
}

/* Boutons de taille de texte */
.setting-controls {
  display: flex;
  gap: 10px;
}

.text-size-button {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background-color: #f0f0f0;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.text-size-button:hover {
  background-color: #e0e0e0;
}

/* Bouton de changement d'appareil */
.switch-device-button {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: bold;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  margin-top: 10px;
}

.switch-device-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.15);
}

/* Message de génération de CV */
.cv-message {
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
  animation: fadeIn 0.3s ease;
}

.cv-message-content {
  background-color: #fff;
  border-radius: 20px;
  padding: 30px;
  text-align: center;
  max-width: 400px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  animation: scaleIn 0.3s ease;
}

.message-icon {
  font-size: 60px;
  margin-bottom: 15px;
  color: #4CAF50;
}

.cv-message-content h3 {
  color: #333;
  margin-bottom: 10px;
  font-size: 1.5rem;
}

.cv-message-content p {
  color: #666;
  margin-bottom: 20px;
}

.close-message-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.close-message-button:hover {
  background-color: #45a049;
}

/* Modal de transfert d'appareil */
.transfer-overlay {
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
  animation: fadeIn 0.3s ease;
}

.transfer-modal {
  background-color: #fff;
  border-radius: 20px;
  padding: 30px;
  text-align: center;
  max-width: 400px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  animation: scaleIn 0.3s ease;
}

.transfer-modal h3 {
  color: #2196F3;
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 1.5rem;
}

.transfer-code {
  font-size: 2.5rem;
  font-weight: bold;
  letter-spacing: 5px;
  color: #333;
  background-color: #f0f0f0;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.transfer-timer {
  font-weight: bold;
  color: #FF5722;
  margin-bottom: 20px;
}

.close-transfer-button {
  background-color: #FF5722;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.close-transfer-button:hover {
  background-color: #e64a19;
}

/* Mode contraste élevé */
.high-contrast {
  color: #FFFFFF;
  background-color: #000000;
}

.high-contrast .tab-content,
.high-contrast .profile-tabs,
.high-contrast .info-card,
.high-contrast .badge-card,
.high-contrast .settings-card {
  background-color: #222222;
  border: 1px solid #FFFFFF;
}

.high-contrast .card-header {
  background-color: #333333;
}

.high-contrast h1, 
.high-contrast h2, 
.high-contrast h3,
.high-contrast .info-value,
.high-contrast .skill-name,
.high-contrast .badge-info h3 {
  color: #FFFFFF;
}

.high-contrast .info-label,
.high-contrast .skill-level,
.high-contrast .progress-text,
.high-contrast .badge-info p {
  color: #CCCCCC;
}

.high-contrast .skill-bar-container,
.high-contrast .progress-bar-container {
  background-color: #666666;
}

.high-contrast .interest-tag {
  background-color: #555555;
  color: #FFFFFF;
}

.high-contrast .text-size-button {
  background-color: #444444;
  color: #FFFFFF;
}

/* Tailles de texte pour l'accessibilité */
.text-size-1 {
  font-size: 1.1em;
}

.text-size-2 {
  font-size: 1.2em;
}

.text-size-3 {
  font-size: 1.3em;
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

/* Responsive */
@media (max-width: 768px) {
  .profile-container {
    padding: 15px;
  }
  
  .profile-header {
    flex-direction: column;
    text-align: center;
  }
  
  .avatar-container {
    margin-right: 0;
    margin-bottom: 15px;
  }
  
  .info-cards {
    grid-template-columns: 1fr;
  }
  
  .badges-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  }
  
  .tab-button {
    padding: 10px;
  }
  
  .tab-icon {
    font-size: 1.5rem;
  }
  
  .tab-label {
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .welcome-message h1 {
    font-size: 1.6rem;
  }
  
  .badges-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .badge-icon {
    width: 60px;
    height: 60px;
  }
  
  .badge-emoji {
    font-size: 30px;
  }
  
  .setting-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .toggle-switch,
  .setting-controls {
    margin-top: 10px;
  }
}
</style>