<template>
  <div class="adventure-map">
    <div v-if="showBadgeAnimation" class="badge-unlock-overlay">
      <div class="badge-unlock-animation">
        <div class="badge-icon">🎭</div>
        <h2>Badge débloqué !</h2>
        <h3>Maître des scénarios</h3>
        <p>Vous avez brillamment résolu tous les scénarios sociaux !</p>
        <button @click="closeBadgeAnimation" class="close-animation-btn">Continuer</button>
      </div>
    </div>
    <!-- En-tête avec personnage guide -->
    <div class="guide-character">
      <img src="@/assets/avatars/guide.png" alt="Guide" class="guide-avatar" />
      <div class="speech-bubble">
        <p>Bienvenue dans ton aventure de compétences ! Choisis un défi à relever !</p>
      </div>
    </div>

    <!-- Carte des scénarios -->
    <div class="map-container">
      <div class="path-background"></div>
      
      <svg class="scenario-paths" width="100%" height="100%">
        <path v-for="(path, index) in pathsData" 
              :key="'path-'+index" 
              :d="path" 
              class="scenario-path"
              :class="{ 'completed-path': isPathCompleted(index) }">
        </path>
      </svg>
      <div class="scenarios-path">
        <div v-for="(scenario, index) in scenarios" :key="scenario.id" 
            class="scenario-node" 
            :class="{ 'completed': isCompleted(scenario.id), 'active': isActive(scenario.id) }"
            :style="{ 'top': getNodePosition(index).top + '%', 'left': getNodePosition(index).left + '%' }">
          
          <router-link 
            :to="{ name: 'ScenarioPage', params: { urlName: scenario.urlName } }"
            class="scenario-link"
            :class="{ 'disabled': !canAccess(scenario.id) }">
            
            <!-- Icône du scénario -->
            <div class="scenario-icon">
              <span class="scenario-number">{{ scenario.id }}</span>
              <img :src="getScenarioIcon(scenario)" :alt="scenario.titre" class="icon-image" />
            </div>
            
            <!-- Info-bulle au survol -->
            <div class="scenario-tooltip">
              <h3>{{ scenario.titre }}</h3>
              <p class="scenario-description">{{ getShortDescription(scenario) }}</p>
              <div class="skills-preview">
                <span v-for="skill in getMainSkills(scenario)" :key="skill" class="skill-tag">{{ skill }}</span>
              </div>
            </div>
          </router-link>
          
          <!-- Indicateur de progression -->
          <div v-if="isCompleted(scenario.id)" class="completion-badge">✓</div>
          <div v-else-if="isActive(scenario.id)" class="active-indicator"></div>
        </div>
      </div>
    </div>

    <!-- Bouton de démarrage pour le premier scénario -->
    <div class="action-container">
      <button v-if="!hasStarted" @click="startAdventure" class="start-adventure-btn">
        <span class="btn-icon">🚀</span>
        <span class="btn-text">Commencer l'aventure</span>
      </button>
      
      <button v-else-if="hasCompletedAll" @click="resetAdventure" class="reset-adventure-btn">
        <span class="btn-icon">🔄</span>
        <span class="btn-text">Recommencer l'aventure</span>
      </button>
      
      <router-link v-else-if="nextScenarioId" :to="{ name: 'ScenarioPage', params: { urlName: getNextScenarioUrlName() } }" class="continue-adventure-btn">
        <span class="btn-icon">➡️</span>
        <span class="btn-text">Continuer l'aventure</span>
      </router-link>
      
      <router-link v-if="hasProgress" :to="{ name: 'RewardsPage' }" class="view-skills-btn">
        <span class="btn-icon">🏆</span>
        <span class="btn-text">Voir mes badges</span>
      </router-link>
    </div>
    
    <!-- Mode accessibilité -->
    <div class="accessibility-container">
      <button @click="toggleAccessibilityMode" class="accessibility-toggle">
        <span v-if="accessibilityMode">Mode standard</span>
        <span v-else>Mode accessible</span>
        <span class="toggle-icon">👁️</span>
      </button>
      
      <!-- Version liste accessible -->
      <div v-if="accessibilityMode" class="accessible-list">
        <h2>Liste des défis</h2>
        <ul>
          <li v-for="scenario in scenarios" :key="scenario.id" class="accessible-item">
            Défi {{scenario.id}}: {{ scenario.titre }}
            <span v-if="isCompleted(scenario.id)" class="completion-text"> - Complété ✓</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { scenarios } from '@/data/data.js';

export default {
  name: 'ScenariosList',
  data() {
    return {
      scenarios,
      completedScenarios: [],
      accessibilityMode: false,
      hasStarted: false,
      pathsData: [],
      showBadgeAnimation: false,
      badgeData: null
    };
  },
  computed: {
    // Prochain scénario à faire
    nextScenarioId() {
      const lastCompleted = Math.max(...this.completedScenarios, 0);
      const next = lastCompleted + 1;
      return this.scenarios.some(s => s.id === next) ? next : null;
    },
    // Tous les scénarios sont-ils complétés ?
    hasCompletedAll() {
      return this.completedScenarios.length === this.scenarios.length;
    },
    // L'utilisateur a-t-il fait au moins un scénario ?
    hasProgress() {
      return this.completedScenarios.length > 0;
    },
  },
  created() {
    this.loadProgress();
    this.$nextTick(() => {
      this.calculatePaths();
      window.addEventListener('resize', this.calculatePaths);
    });
    if (this.$route.query.showBadgeUnlock === 'true') {
      const badgeData = localStorage.getItem('newUnlockedBadge');
      if (badgeData) {
        this.badgeData = JSON.parse(badgeData);
        this.showBadgeAnimation = true;
        localStorage.removeItem('newUnlockedBadge');
      }
    }
  },

  beforeUnmount() {
    // N'oubliez pas de supprimer l'écouteur d'événement
    window.removeEventListener('resize', this.calculatePaths);
  },
  methods: {
    closeBadgeAnimation() {
      this.showBadgeAnimation = false;
    },
    // Charger la progression depuis le localStorage
    loadProgress() {
      const savedSkills = localStorage.getItem('userSoftSkills');
      if (savedSkills) {
        this.hasStarted = true;
        
        // Récupérer les scénarios complétés
        const completedIds = localStorage.getItem('completedScenarios');
        if (completedIds) {
          this.completedScenarios = JSON.parse(completedIds).map(id => parseInt(id));
        }
      }
    },
    
    // Démarrer l'aventure (premier scénario)
    startAdventure() {
      localStorage.setItem('userSoftSkills', JSON.stringify({}));
      localStorage.setItem('completedScenarios', JSON.stringify([]));
      this.hasStarted = true;
      this.completedScenarios = [];
      const firstScenario = this.scenarios.find(s => s.id === 1);
      this.$router.push({ name: 'ScenarioPage', params: { urlName: firstScenario.urlName } });
    },
    
    getNextScenarioUrlName() {
      const nextId = this.nextScenarioId;
      const nextScenario = this.scenarios.find(s => s.id === nextId);
      return nextScenario ? nextScenario.urlName : '';
    },

    // Réinitialiser l'aventure
    resetAdventure() {
      if (confirm("Es-tu sûr de vouloir recommencer toute l'aventure ? Tes données seront réinitialisés !")) {
        localStorage.setItem('userSoftSkills', JSON.stringify({}));
        localStorage.setItem('completedScenarios', JSON.stringify([]));
        this.completedScenarios = [];
        const firstScenario = this.scenarios.find(s => s.id === 1);
        this.$router.push({ name: 'ScenarioPage', params: { urlName: firstScenario.urlName } })
      }
    },
    
    isPathCompleted(pathIndex) {
      const scenarioId = this.scenarios[pathIndex].id;
      return this.isCompleted(scenarioId);
    },

    // Vérifier si un scénario est complété
    isCompleted(scenarioId) {
      return this.completedScenarios.includes(scenarioId);
    },
    
    // Vérifier si un scénario est actif (à faire maintenant)
    isActive(scenarioId) {
      return scenarioId === this.nextScenarioId || 
             (scenarioId === 1 && this.completedScenarios.length === 0);
    },
    
    // Vérifier si l'utilisateur peut accéder à un scénario
    canAccess(scenarioId) {
      // Toujours accès au premier scénario
      if (scenarioId === 1) return true;
      
      // Accès aux scénarios déjà complétés
      if (this.isCompleted(scenarioId)) return true;
      
      // Accès au prochain scénario à faire
      if (scenarioId === this.nextScenarioId) return true;
      
      return false;
    },
    
    // Obtenir une courte description du scénario
    getShortDescription(scenario) {
      // Limiter la description à 100 caractères
      const description = scenario.contexteIntro || '';
      return description.length > 100 
        ? description.substring(0, 97) + '...' 
        : description;
    },

    calculatePaths() {
      const container = document.querySelector('.map-container');
      if (!container) return;
      
      const containerWidth = container.offsetWidth;
      const containerHeight = container.offsetHeight;
      
      const paths = [];
      for (let i = 0; i < this.scenarios.length - 1; i++) {
        const startPos = this.getNodePosition(i);
        const endPos = this.getNodePosition(i + 1);
        
        // Convertir les pourcentages en pixels
        const startX = startPos.left * containerWidth / 100;
        const startY = startPos.top * containerHeight / 100;
        const endX = endPos.left * containerWidth / 100;
        const endY = endPos.top * containerHeight / 100;
        
        // Point de contrôle pour la courbe
        const controlX = (startX + endX) / 2;
        const controlY = Math.min(startY, endY) - 20;
        
        // Créer un chemin incurvé entre les deux points
        const path = `M ${startX} ${startY} Q ${controlX} ${controlY}, ${endX} ${endY}`;
        paths.push(path);
      }
      
      this.pathsData = paths;
    },
    
    // Obtenir les compétences principales développées dans ce scénario
    getMainSkills(scenario) {
      // Extraire et regrouper toutes les compétences du scénario
      const skills = {};
      
      scenario.reponses.forEach(reponse => {
        if (reponse.skills) {
          Object.entries(reponse.skills).forEach(([skill, value]) => {
            skills[skill] = (skills[skill] || 0) + value;
          });
        }
      });
      
      // Sélectionner les 3 principales compétences
      return Object.entries(skills)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 3)
        .map(([skill]) => this.formatSkillName(skill));
    },
    
    // Formater le nom d'une compétence
    formatSkillName(skill) {
      const skillNames = {
        assertivite: "Assertivité",
        communication: "Communication",
        empathie: "Empathie",
        espritEquipe: "Travail d'équipe",
        initiative: "Initiative",
        adaptabilite: "Adaptabilité",
        responsabilite: "Responsabilité",
        creativite: "Créativité",
        observation: "Observation",
        diplomatie: "Diplomatie",
        patience: "Patience",
        confianceEnSoi: "Confiance",
        inclusion: "Inclusion",
        mediation: "Médiation",
        coaching: "Coaching",
        ecouteActive: "Écoute",
        soutien: "Soutien",
        reflexionRapide: "Réflexion",
        negociation: "Négociation",
        gestionStress: "Calme",
        anticipation: "Anticipation",
        apprentissage: "Apprentissage"
      };
      
      return skillNames[skill] || skill;
    },
    
    // Obtenir l'icône associée au scénario
    getScenarioIcon(scenario) {
      // Associer une icône en fonction du thème du scénario 
      // (idéalement, vous auriez des icônes spécifiques pour chaque scénario)
      const iconMapping = {
        1: require('@/assets/avatars/personne_agee.png'),
        2: require('@/assets/avatars/femme-caissiere.png'),
        3: require('@/assets/avatars/passant2.png'),
        4: require('@/assets/avatars/serveur.png'),
        5: require('@/assets/avatars/conducteur.png'),
        6: require('@/assets/avatars/passant2.png'),
        7: require('@/assets/avatars/homme-daffaire.png'),
        8: require('@/assets/avatars/passant2.png'),
        9: require('@/assets/avatars/homme-daffaire.png'), 
        10: require('@/assets/avatars/passant2.png')
      };
      
      return iconMapping[scenario.id] || require('@/assets/avatars/toi.png');
    },
    
    // Obtenir la position d'un nœud sur la carte
    getNodePosition(index) {
      // Créer un chemin sinueux pour les scénarios
      const positions = [
        { top: 20, left: 20 },   // Scénario 1
        { top: 35, left: 35 },   // Scénario 2
        { top: 50, left: 20 },   // Scénario 3
        { top: 65, left: 40 },   // Scénario 4
        { top: 80, left: 20 },   // Scénario 5
        { top: 75, left: 60 },   // Scénario 6
        { top: 55, left: 70 },   // Scénario 7
        { top: 35, left: 80 },   // Scénario 8
        { top: 20, left: 65 },   // Scénario 9
        { top: 10, left: 50 }    // Scénario 10
      ];
      
      // Si l'index existe dans les positions, le retourner, sinon générer aléatoirement
      return positions[index] || { 
        top: 10 + (index * 8) % 80, 
        left: 20 + (index * 15) % 60 
      };
    },
    
    // Activer/désactiver le mode d'accessibilité
    toggleAccessibilityMode() {
      this.accessibilityMode = !this.accessibilityMode;
      
      // Sauvegarder la préférence
      localStorage.setItem('accessibilityMode', this.accessibilityMode);
    }
  }
};
</script>

<style scoped>
/* Conteneur principal en forme de carte */
.adventure-map {
  font-family: 'Comic Sans MS', 'Chalkboard SE', 'Marker Felt', sans-serif;
  max-width: 900px;
  margin: 20px auto;
  padding: 20px;
  background-color: #f5f8ff;
  border-radius: 20px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  position: relative;
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
  z-index: 1000;
  animation: fadeIn 0.5s ease-out;
}

.badge-unlock-animation {
  background-color: #fff;
  border-radius: 20px;
  padding: 30px;
  text-align: center;
  max-width: 400px;
  box-shadow: 0 0 30px rgba(255, 215, 0, 0.6);
  animation: scaleIn 0.5s ease-out;
}

.badge-icon {
  font-size: 80px;
  margin-bottom: 20px;
  animation: pulse 2s infinite;
}

.badge-unlock-animation h2 {
  color: #FFD700;
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
  background-color: #4CAF50;
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
  background-color: #45a049;
  transform: scale(1.05);
}

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
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

/* Personnage guide */
.guide-character {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
}

.guide-avatar {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  border: 3px solid #FFC107;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.speech-bubble {
  position: relative;
  background-color: #FFF;
  border-radius: 15px;
  padding: 15px;
  margin-left: 15px;
  box-shadow: 0 3px 5px rgba(0, 0, 0, 0.1);
  max-width: 70%;
}

.speech-bubble:before {
  content: '';
  position: absolute;
  left: -10px;
  top: 50%;
  transform: translateY(-50%);
  border-width: 10px 10px 10px 0;
  border-style: solid;
  border-color: transparent #FFF transparent transparent;
}

.speech-bubble p {
  margin: 0;
  font-size: 1.2rem;
  color: #333;
}

/* Conteneur de la carte */
.map-container {
  position: relative;
  height: 500px;
  background-color: #e8f4e5;
  border-radius: 15px;
  margin: 20px 0;
  overflow: hidden;
  border: 5px solid #9C7248;
  box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.1);
}

/* Fond de la carte avec motif */
.path-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(circle at 20px 20px, #d4e9f7 2px, transparent 2px),
    radial-gradient(circle at 60px 60px, #d4e9f7 2px, transparent 2px),
    radial-gradient(circle at 100px 40px, #d4e9f7 2px, transparent 2px);
  background-size: 100px 100px;
  opacity: 0.4;
}

.scenario-paths {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  pointer-events: none;
}

/* Conteneur des scénarios */
.scenario-path {
  fill: none;
  stroke: #ccc;
  stroke-width: 5px;
  stroke-linecap: round;
  stroke-dasharray: 10, 5;
  opacity: 0.6;
  animation: dashAnimation 30s linear infinite;
}

.completed-path {
  stroke: #4CAF50;
  opacity: 0.8;
  stroke-dasharray: none;
}

.scenario-node {
  z-index: 2;
  position: absolute;
  width: 70px;
  height: 70px;
  transform: translate(-50%, -50%);
  transition: all 0.3s ease;
}

@keyframes dashAnimation {
  to {
    stroke-dashoffset: -1000;
  }
}

/* Lien vers le scénario */
.scenario-link {
  display: block;
  width: 100%;
  height: 100%;
  text-decoration: none;
  color: inherit;
  transition: transform 0.3s ease;
}

.scenario-link:hover {
  transform: scale(1.1);
}

.scenario-link.disabled {
  pointer-events: none;
  opacity: 0.6;
  filter: grayscale(70%);
}

/* Icône du scénario */
.scenario-icon {
  position: relative;
  width: 100%;
  height: 100%;
  background-color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  border: 3px solid #4CAF50;
  transition: all 0.3s ease;
}

.scenario-number {
  position: absolute;
  top: 5px;
  left: 5px;
  background-color: #FF5722;
  color: white;
  border-radius: 50%;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 14px;
  z-index: 2;
}

.icon-image {
  width: 75%;
  height: 75%;
  object-fit: cover;
  border-radius: 50%;
}

/* Indicateurs d'état */
.completion-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  width: 25px;
  height: 25px;
  background-color: #4CAF50;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  z-index: 3;
}

.active-indicator {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 3px solid #FF9800;
  box-shadow: 0 0 10px #FF9800;
  animation: pulse 2s infinite;
  top: -3px;
  left: -3px;
  z-index: 1;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.7;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Info-bulle */
.scenario-tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%) scale(0);
  width: 220px;
  background-color: white;
  border-radius: 10px;
  padding: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  opacity: 0;
  transition: all 0.3s ease;
  pointer-events: none;
  z-index: 10;
}

.scenario-link:hover .scenario-tooltip {
  transform: translateX(-50%) scale(1);
  opacity: 1;
  bottom: 110%;
}

.scenario-tooltip h3 {
  margin: 0 0 8px;
  font-size: 1.1rem;
  color: #333;
}

.scenario-description {
  font-size: 0.9rem;
  margin-bottom: 8px;
  color: #555;
}

.skills-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.skill-tag {
  background-color: #e3f2fd;
  color: #1976d2;
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
}

/* État des nœuds */
.scenario-node.completed .scenario-icon {
  border-color: #4CAF50;
}

.scenario-node.active .scenario-icon {
  border-color: #FF9800;
}

/* Boutons d'action */
.action-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 15px;
  margin-top: 20px;
}

.start-adventure-btn,
.reset-adventure-btn,
.continue-adventure-btn,
.view-skills-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px 20px;
  border-radius: 50px;
  font-size: 1.2rem;
  font-weight: bold;
  color: white;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  text-decoration: none;
  min-width: 220px;
  max-width: 400px;
  width: auto;
  height: auto;
}

.start-adventure-btn {
  background-color: #4CAF50;
}

.reset-adventure-btn {
  background-color: #F44336;
}

.continue-adventure-btn {
  background-color: #2196F3;
}

.view-skills-btn {
  background-color: #9C27B0;
}

.btn-icon {
  margin-right: 8px;
  font-size: 1.4rem;
}

.start-adventure-btn:hover,
.reset-adventure-btn:hover,
.continue-adventure-btn:hover,
.view-skills-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

.start-adventure-btn:active,
.reset-adventure-btn:active,
.continue-adventure-btn:active,
.view-skills-btn:active {
  transform: translateY(1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Mode accessibilité */
.accessibility-container {
  margin-top: 30px;
  text-align: center;
}

.accessibility-toggle {
  background-color: #607D8B;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  margin: 0 auto;
}

.toggle-icon {
  margin-left: 8px;
}

.accessibility-toggle:hover {
  background-color: #455A64;
}

.accessible-list {
  margin-top: 20px;
  padding: 15px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: left;
}

.accessible-list h2 {
  margin-top: 0;
  font-size: 1.5rem;
  color: #333;
}

.accessible-list ul {
  list-style-type: none;
  padding: 0;
}

.accessible-item {
  padding: 10px;
  border-bottom: 1px solid #eee;
}

.accessible-item a {
  color: #333;
  text-decoration: none;
  display: block;
  font-size: 1.1rem;
}

.accessible-item a:hover {
  color: #2196F3;
}

.accessible-item a.disabled {
  color: #aaa;
  pointer-events: none;
}

.completion-text {
  color: #4CAF50;
  font-weight: bold;
}

/* Responsive */
@media (max-width: 768px) {
  .adventure-map {
    padding: 15px;
  }
  
  .map-container {
    height: 400px;
  }
  
  .scenario-node {
    width: 60px;
    height: 60px;
  }
  
  .guide-avatar {
    width: 60px;
    height: 60px;
  }
  
  .speech-bubble p {
    font-size: 1rem;
  }
  
  .action-container {
    flex-direction: column;
    align-items: center;
  }
  
  .start-adventure-btn,
  .reset-adventure-btn,
  .continue-adventure-btn,
  .view-skills-btn {
    width: 100%;
    max-width: 300px;
  }
}
</style>