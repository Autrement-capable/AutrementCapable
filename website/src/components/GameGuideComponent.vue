<template>
  <transition name="fade">
    <div v-if="isVisible" class="central-guide-overlay">
      <div class="central-guide-container" :class="{ 'animate-in': animationStarted }">
        <!-- Léo au centre -->
        <div class="guide-character-container">
          <img :src="guideImage" alt="Léo" class="guide-character" />
          <div class="guide-character-shadow"></div>
        </div>
        
        <!-- Titre du jeu avec animation -->
        <h1 class="game-title">{{ gameTitle }}</h1>
        
        <!-- Contenu explicatif qui change au fur et à mesure -->
        <div class="guide-content">
          <!-- Étape active avec animation d'entrée -->
          <transition name="slide-fade" mode="out-in">
            <div :key="currentStepIndex" class="explanation-step">
              <div class="step-content" v-html="currentStepContent"></div>
              <div v-if="showStepCounter" class="step-counter">
                <span class="current-step">{{ currentStepIndex + 1 }}</span>
                <span class="total-steps">/ {{ totalSteps }}</span>
              </div>
            </div>
          </transition>
        </div>
        
        <!-- Animations CSS basées sur l'étape actuelle -->
        <div class="visual-animation" :class="'animation-step-' + currentStepIndex">
          <!-- Animation pour l'introduction (étape 0) -->
          <div v-if="currentStepIndex === 0" class="animation-intro">
            <div class="animation-welcome-icon"></div>
          </div>
          
          <!-- Animation pour la première étape (étape 1) -->
          <div v-else-if="currentStepIndex === 1" class="animation-step1">
            <div v-if="gameId === 'skills-wheel'" class="animation-wheel">
              <div class="wheel-center"></div>
              <div class="wheel-segment" v-for="n in 8" :key="n"></div>
              <div class="wheel-pointer"></div>
            </div>
            <div v-else-if="gameId === 'shape-sequence'" class="animation-shapes">
              <div class="shape shape-square"></div>
              <div class="shape shape-circle"></div>
              <div class="shape shape-triangle"></div>
              <div class="shape shape-question">?</div>
            </div>
            <div v-else-if="gameId === 'sensory-environment'" class="animation-environment">
              <div class="environment-room"></div>
              <div class="environment-controls">
                <div class="control-light"></div>
                <div class="control-sound"></div>
                <div class="control-color"></div>
              </div>
            </div>
          </div>
          
          <!-- Animation pour la deuxième étape (étape 2) -->
          <div v-else-if="currentStepIndex === 2" class="animation-step2">
            <div v-if="gameId === 'skills-wheel'" class="animation-options">
              <div class="option-bubble option-strength">💪</div>
              <div class="option-bubble option-improve">🌱</div>
              <div class="option-bubble option-difficulty">🔍</div>
            </div>
            <div v-else-if="gameId === 'shape-sequence'" class="animation-logic">
              <div class="logic-pattern">
                <div class="pattern-shape pattern-circle"></div>
                <div class="pattern-shape pattern-triangle"></div>
                <div class="pattern-shape pattern-circle"></div>
                <div class="pattern-shape pattern-triangle"></div>
              </div>
              <div class="logic-arrow">→</div>
              <div class="logic-brain"></div>
            </div>
            <div v-else-if="gameId === 'sensory-environment'" class="animation-environment-adjust">
              <div class="environment-slider"></div>
              <div class="environment-colors">
                <div class="color-swatch swatch-warm"></div>
                <div class="color-swatch swatch-neutral"></div>
                <div class="color-swatch swatch-cool"></div>
              </div>
            </div>
          </div>
          
          <!-- Animation pour la dernière étape -->
          <div v-else-if="currentStepIndex === totalSteps - 1" class="animation-final">
            <div class="animation-badge">
              <div class="badge-center">
                <span v-if="gameId === 'skills-wheel'">🎯</span>
                <span v-else-if="gameId === 'shape-sequence'">🧩</span>
                <span v-else-if="gameId === 'sensory-environment'">🌈</span>
                <span v-else>🏆</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Contrôles de navigation -->
        <div class="guide-controls">
          <button 
            v-if="currentStepIndex > 0" 
            @click="previousStep" 
            class="nav-button prev-button"
          >
            <span class="nav-icon">◀</span>
            <span class="nav-text">Précédent</span>
          </button>
          
          <button 
            v-if="currentStepIndex < totalSteps - 1" 
            @click="nextStep" 
            class="nav-button next-button"
          >
            <span class="nav-text">Suivant</span>
            <span class="nav-icon">▶</span>
          </button>
          
          <button 
            v-if="currentStepIndex === totalSteps - 1" 
            @click="startGame" 
            class="nav-button start-button"
          >
            <span class="nav-icon">🎮</span>
            <span class="nav-text">Commencer à jouer</span>
          </button>
        </div>
        
        <!-- Bouton pour passer l'introduction -->
        <button v-if="!forceShow" @click="skipIntro" class="skip-button">
          Passer l'introduction
        </button>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'GameGuide',
  props: {
    // ID du jeu pour récupérer les explications spécifiques
    gameId: {
      type: String,
      required: true
    },
    // Si on force l'affichage du guide (impossible à passer)
    forceShow: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      isVisible: true,
      animationStarted: false,
      currentStepIndex: 0,
      autoProgressTimer: null,
      showStepCounter: true,
      
      // Bibliothèque des contenus de jeux
      gamesContent: {
        'skills-wheel': {
          title: 'Roulette des Compétences',
          steps: [
            `<h2>Bienvenue dans la Roulette des Compétences!</h2>
              <p>Je suis Léo, et je vais t'aider à découvrir tes forces et tes domaines d'amélioration de manière ludique.</p>
              <p>Ce jeu va te permettre de faire le point sur tes compétences et de mieux te connaître!</p>`,
            
            `<h2>Étape 1: Tourne la roue</h2>
              <p>Pour commencer, tu vas simplement tourner la roue en cliquant sur le bouton.</p>
              <p>La roue sélectionnera aléatoirement une compétence à évaluer.</p>
              <div class="animation-hint">🔄 La roue tourne et s'arrête sur une compétence</div>`,
            
            `<h2>Étape 2: Évalue tes compétences</h2>
              <p>Pour chaque compétence qui apparaît, tu devras indiquer:</p>
              <ul>
                <li><strong>💪 Je la possède</strong> - Tu te sens à l'aise avec cette compétence</li>
                <li><strong>🌱 Je veux la développer</strong> - Tu souhaites progresser dans ce domaine</li>
                <li><strong>🔍 J'ai du mal avec</strong> - C'est un point de difficulté pour toi</li>
              </ul>`,
            
            `<h2>Étape 3: Découvre ton bilan</h2>
              <p>À la fin du jeu, tu verras un résumé de tes forces et de tes axes d'amélioration.</p>
              <p>Tu pourras même gagner un badge "Explorateur de Compétences" si tu complètes l'ensemble du jeu!</p>`,
            
            `<h2>Tu es prêt à commencer?</h2>
              <p>C'est parti pour découvrir tes talents et tes points d'amélioration!</p>
              <p>Clique sur le bouton ci-dessous pour démarrer le jeu.</p>`
          ]
        },
        'shape-sequence': {
          title: 'Séquences de Formes',
          steps: [
            `<h2>Bienvenue dans les Séquences de Formes!</h2>
              <p>Je suis Léo, et je vais t'accompagner dans ce jeu qui va stimuler ton sens de l'observation et ton raisonnement logique.</p>
              <p>Prêt à relever le défi?</p>`,
            
            `<h2>Étape 1: Observe la séquence</h2>
              <p>Une série de formes va s'afficher à l'écran. Ton défi est de bien observer leur ordre et leur logique.</p>
              <p>Chaque séquence suit un motif ou une règle spécifique.</p>`,
            
            `<h2>Étape 2: Trouve la logique</h2>
              <p>Analyse les formes pour identifier la règle qui détermine leur enchaînement:</p>
              <ul>
                <li>Est-ce une alternance?</li>
                <li>Y a-t-il une répétition?</li>
                <li>Les formes suivent-elles un ordre précis?</li>
              </ul>
              <p>C'est comme résoudre une énigme!</p>`,
            
            `<h2>Étape 3: Choisis la bonne forme</h2>
              <p>Une fois que tu as compris la logique, sélectionne parmi les options proposées la forme qui devrait remplacer le point d'interrogation.</p>
              <p>Sois attentif, car chaque niveau devient progressivement plus difficile!</p>`,
            
            `<h2>Tu es prêt à tester ta logique?</h2>
              <p>Ce jeu va entraîner ton cerveau et t'aider à développer tes capacités d'analyse.</p>
              <p>Tu pourras même gagner un badge "Expert des formes" si tu réussis assez de niveaux!</p>
              <p>Clique sur le bouton ci-dessous pour commencer.</p>`
          ]
        },
        'sensory-environment': {
          title: 'Découvre ton environnement préféré',
          steps: [
            `<h2>Bienvenue dans l'exploration d'environnements!</h2>
              <p>Je suis Léo, et je vais t'aider à découvrir ce que tu aimes et ce que tu n'aimes pas dans ton environnement.</p>
              <p>Ce jeu va te permettre de mieux comprendre tes préférences sensorielles de manière interactive!</p>`,
            
            `<h2>Étape 1: Choisis un espace</h2>
              <p>Tu vas commencer par choisir un environnement parmi plusieurs possibilités:</p>
              <ul>
                <li>Espace de concentration</li>
                <li>Espace de détente</li>
                <li>Espace social contrôlé</li>
              </ul>
              <p>Chaque espace a des caractéristiques différentes que tu pourras explorer.</p>`,
            
            `<h2>Étape 2: Personnalise ton environnement</h2>
              <p>Tu pourras modifier différents éléments comme:</p>
              <ul>
                <li><strong>La lumière</strong> - Intensité et couleur</li>
                <li><strong>Les couleurs</strong> - Des murs, du sol et du plafond</li>
                <li><strong>Les sons</strong> - Différentes ambiances sonores</li>
                <li><strong>Les personnes</strong> - Nombre de personnes présentes</li>
              </ul>
              <p>Ajuste les réglages jusqu'à ce que tu te sentes bien!</p>`,
            
            `<h2>Étape 3: Exprime ton ressenti</h2>
              <p>Après la personnalisation, tu indiqueras comment tu te sens dans cet environnement:</p>
              <ul>
                <li>Es-tu calme? Concentré? Confortable?</li>
                <li>Ou peut-être mal à l'aise ou surstimulé?</li>
              </ul>
              <p>Tu pourras aussi ajouter des commentaires pour expliquer ce que tu aimes ou n'aimes pas.</p>`,
            
            `<h2>Étape 4: Découvre tes préférences</h2>
              <p>À la fin, tu recevras un résumé de tes préférences sensorielles et des recommandations personnalisées.</p>
              <p>Ces informations t'aideront à créer des environnements adaptés à tes besoins!</p>`,
            
            `<h2>Tu es prêt à explorer?</h2>
              <p>Souviens-toi: tu peux prendre ton temps, il n'y a pas de bonnes ou mauvaises réponses.</p>
              <p>Clique sur le bouton ci-dessous pour commencer l'aventure!</p>`
          ]
        }
        // Vous pourrez ajouter d'autres jeux ici
      }
    };
  },
  computed: {
    // Titre du jeu
    gameTitle() {
      const gameInfo = this.gamesContent[this.gameId];
      return gameInfo ? gameInfo.title : 'Jeu interactif';
    },
    
    // Contenu de l'étape actuelle
    currentStepContent() {
      const gameInfo = this.gamesContent[this.gameId];
      if (!gameInfo || !gameInfo.steps || gameInfo.steps.length === 0) {
        return '<p>Information sur le jeu non disponible</p>';
      }
      
      return gameInfo.steps[Math.min(this.currentStepIndex, gameInfo.steps.length - 1)];
    },
    
    // Nombre total d'étapes
    totalSteps() {
      const gameInfo = this.gamesContent[this.gameId];
      return gameInfo && gameInfo.steps ? gameInfo.steps.length : 0;
    },
    
    // Image du guide
    guideImage() {
      return require('@/assets/avatars/guide.png'); // Assurez-vous que ce chemin est correct
    }
  },
  methods: {
    // Initialisation des animations
    startAnimation() {
      setTimeout(() => {
        this.animationStarted = true;
      }, 100);
    },
    
    // Navigation entre les étapes
    nextStep() {
      if (this.currentStepIndex < this.totalSteps - 1) {
        this.currentStepIndex++;
      }
    },
    
    previousStep() {
      if (this.currentStepIndex > 0) {
        this.currentStepIndex--;
      }
    },
    
    // Démarrer le jeu
    startGame() {
      this.$emit('start-game');
      this.isVisible = false;
    },
    
    // Passer l'introduction
    skipIntro() {
      if (this.forceShow) return;
      
      // Sauvegarder la préférence de l'utilisateur
      this.saveUserPreference();
      this.$emit('skip-intro');
      this.isVisible = false;
    },
    
    // Sauvegarder la préférence de l'utilisateur
    saveUserPreference() {
      const gameIntroPreferences = JSON.parse(localStorage.getItem('gameIntroPreferences') || '{}');
      gameIntroPreferences[this.gameId] = { skipped: true };
      localStorage.setItem('gameIntroPreferences', JSON.stringify(gameIntroPreferences));
    },
    
    // Réinitialiser le guide
    resetGuide() {
      this.currentStepIndex = 0;
      this.isVisible = true;
      this.animationStarted = false;
      this.startAnimation();
    }
  },
  created() {
    // Vérifier les préférences de l'utilisateur
    if (!this.forceShow) {
      const gameIntroPreferences = JSON.parse(localStorage.getItem('gameIntroPreferences') || '{}');
      const preference = gameIntroPreferences[this.gameId];
      
      if (preference && preference.skipped) {
        this.isVisible = false;
        this.$emit('already-skipped');
      }
    }
  },
  mounted() {
    this.startAnimation();
  },
  beforeUnmount() {
    if (this.autoProgressTimer) {
      clearTimeout(this.autoProgressTimer);
    }
  }
};
</script>

<style scoped>
/* Styles de base */
.central-guide-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.central-guide-container {
  position: relative;
  width: 90%;
  max-width: 900px;
  min-height: 600px;
  max-height: 85vh;
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  padding: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
  transform: scale(0.9);
  opacity: 0;
  overflow: hidden;
  font-family: 'Comic Sans MS', 'Chalkboard SE', 'Marker Felt', sans-serif;
}

.central-guide-container.animate-in {
  transform: scale(1);
  opacity: 1;
  transition: all 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

/* Personnage guide */
.guide-character-container {
  position: relative;
  margin-bottom: 20px;
  transform: translateY(0);
  animation: float-character 5s infinite ease-in-out;
}

@keyframes float-character {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.guide-character {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 5px solid white;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  object-fit: cover;
}

.guide-character-shadow {
  position: absolute;
  bottom: -10px;
  left: 15%;
  right: 15%;
  height: 10px;
  background-color: rgba(0, 0, 0, 0.15);
  border-radius: 50%;
  filter: blur(5px);
  transform: scale(1, 0.3);
  animation: shadow-pulse 5s infinite ease-in-out;
}

@keyframes shadow-pulse {
  0%, 100% { transform: scale(1, 0.3); opacity: 0.4; }
  50% { transform: scale(0.8, 0.2); opacity: 0.2; }
}

/* Titre du jeu */
.game-title {
  font-size: 2.5rem;
  color: #2196F3;
  text-align: center;
  margin: 10px 0 20px;
  position: relative;
  font-weight: bold;
  text-shadow: 2px 2px 0 rgba(0, 0, 0, 0.1);
  animation: title-appear 1s forwards;
}

@keyframes title-appear {
  0% { opacity: 0; transform: translateY(-20px); }
  100% { opacity: 1; transform: translateY(0); }
}

.game-title::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 4px;
  background: linear-gradient(90deg, #2196F3, #4CAF50);
  border-radius: 2px;
}

/* Contenu explicatif */
.guide-content {
  width: 100%;
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  position: relative;
  padding: 20px 0;
  margin-bottom: 20px;
}

.explanation-step {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 0 20px;
}

.step-content {
  max-width: 650px;
  text-align: center;
}

.step-content h2 {
  color: #4CAF50;
  margin-bottom: 15px;
  font-size: 1.8rem;
}

.step-content p {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 15px;
  color: #333;
}

.step-content ul {
  display: inline-block;
  text-align: left;
  padding-left: 20px;
  margin: 15px 0;
}

.step-content li {
  margin-bottom: 10px;
  font-size: 1.05rem;
}

.step-counter {
  margin-top: 20px;
  font-size: 0.9rem;
  color: #666;
}

.current-step {
  font-weight: bold;
  color: #2196F3;
  font-size: 1.1rem;
}

/* Animations CSS par étape */
.visual-animation {
  position: absolute;
  width: 200px;
  height: 200px;
  pointer-events: none;
  top: auto;
  right: 10%;
  bottom: 10%;
}

/* Animation d'introduction */
.animation-intro {
  position: relative;
  width: 100%;
  height: 100%;
}

.animation-welcome-icon {
  position: absolute;
  right: 20px;
  bottom: 20px;
  width: 80px;
  height: 80px;
  background-color: #FFC107;
  border-radius: 50%;
  animation: pulse-welcome 2s infinite;
}

.animation-welcome-icon:before {
  content: '👋';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 40px;
}

@keyframes pulse-welcome {
  0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 193, 7, 0.7); }
  70% { transform: scale(1.1); box-shadow: 0 0 0 15px rgba(255, 193, 7, 0); }
  100% { transform: scale(1); }
}

/* Animation de la roue (pour skills-wheel) */
.animation-wheel {
  position: absolute;
  right: 20px;
  bottom: 20px;
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background-color: #f5f5f5;
  border: 3px solid #333;
  animation: spin-wheel 8s infinite cubic-bezier(0.36, 0.07, 0.19, 0.97);
}

.wheel-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 20px;
  height: 20px;
  background-color: #333;
  border-radius: 50%;
  z-index: 2;
}

.wheel-segment {
  position: absolute;
  top: 0;
  left: 50%;
  width: 2px;
  height: 50%;
  background-color: #333;
  transform-origin: bottom center;
}

.wheel-segment:nth-child(1) { transform: translateX(-50%) rotate(0deg); }
.wheel-segment:nth-child(2) { transform: translateX(-50%) rotate(45deg); }
.wheel-segment:nth-child(3) { transform: translateX(-50%) rotate(90deg); }
.wheel-segment:nth-child(4) { transform: translateX(-50%) rotate(135deg); }
.wheel-segment:nth-child(5) { transform: translateX(-50%) rotate(180deg); }
.wheel-segment:nth-child(6) { transform: translateX(-50%) rotate(225deg); }
.wheel-segment:nth-child(7) { transform: translateX(-50%) rotate(270deg); }
.wheel-segment:nth-child(8) { transform: translateX(-50%) rotate(315deg); }

.wheel-pointer {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 10px solid transparent;
  border-right: 10px solid transparent;
  border-bottom: 20px solid #f44336;
  z-index: 3;
}

@keyframes spin-wheel {
  0% { transform: rotate(0deg); }
  20% { transform: rotate(1800deg); }
  25% { transform: rotate(1805deg); }
  100% { transform: rotate(1805deg); }
}

/* Animation des formes (pour shape-sequence) */
.animation-shapes {
  position: absolute;
  right: 20px;
  bottom: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
}

.shape {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: pop-in 0.5s forwards;
  opacity: 0;
  transform: scale(0.5);
  margin-bottom: 50px;
}

.shape-square {
  background-color: #2196F3;
  animation-delay: 0.2s;
}

.shape-circle {
  background-color: #F44336;
  border-radius: 50%;
  animation-delay: 0.4s;
}

.shape-triangle {
  width: 0;
  height: 0;
  background-color: transparent;
  border-left: 20px solid transparent;
  border-right: 20px solid transparent;
  border-bottom: 40px solid #4CAF50;
  animation-delay: 0.6s;
}

.shape-question {
  background-color: #FFC107;
  border-radius: 10px;
  font-size: 24px;
  font-weight: bold;
  animation-delay: 0.8s;
  animation-name: pulse-question;
  animation-duration: 2s;
  animation-iteration-count: infinite;
  opacity: 1;
  transform: scale(1);
}

@keyframes pop-in {
  0% { opacity: 0; transform: scale(0.5); }
  70% { opacity: 1; transform: scale(1.1); }
  100% { opacity: 1; transform: scale(1); }
}

@keyframes pulse-question {
  0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 193, 7, 0.7); }
  70% { transform: scale(1.1); box-shadow: 0 0 0 10px rgba(255, 193, 7, 0); }
  100% { transform: scale(1); }
}

/* Animation des options (pour skills-wheel étape 2) */
.animation-options {
  position: absolute;
  right: 30px;
  bottom: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.option-bubble {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30px;
  position: relative;
  opacity: 0;
  animation: slide-in-option 0.5s forwards, float-option 3s infinite ease-in-out;
}

.option-strength {
  background-color: rgba(76, 175, 80, 0.2);
  border: 2px solid #4CAF50;
  animation-delay: 0.2s, 0.7s;
}

.option-improve {
  background-color: rgba(33, 150, 243, 0.2);
  border: 2px solid #2196F3;
  animation-delay: 0.4s, 0.9s;
}

.option-difficulty {
  background-color: rgba(255, 152, 0, 0.2);
  border: 2px solid #FF9800;
  animation-delay: 0.6s, 1.1s;
}

@keyframes slide-in-option {
  0% { transform: translateX(-50px); opacity: 0; }
  100% { transform: translateX(0); opacity: 1; }
}

@keyframes float-option {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

/* Animations pour l'environnement sensoriel */
.animation-environment {
  position: absolute;
  left: 40px;
  top: 50px;
  width: 160px;
  height: 160px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.environment-room {
  width: 120px;
  height: 100px;
  background: linear-gradient(to bottom, #e6f7ff, #ffffff);
  border: 2px solid #80bdff;
  border-radius: 10px;
  position: relative;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  animation: room-appear 1s forwards;
}

.environment-room:before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 30%;
  background-color: #d9e6f2;
  border-radius: 0 0 8px 8px;
}

.environment-controls {
  display: flex;
  justify-content: space-around;
  width: 100%;
  gap: 8px;
}

.control-light, .control-sound, .control-color {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  opacity: 0;
  animation: control-pop 0.5s forwards;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
}

.control-light {
  background-color: #FFC107;
  animation-delay: 0.3s;
}

.control-light:before {
  content: '💡';
  font-size: 20px;
}

.control-sound {
  background-color: #2196F3;
  animation-delay: 0.5s;
}

.control-sound:before {
  content: '🔊';
  font-size: 20px;
}

.control-color {
  background-color: #F44336;
  animation-delay: 0.7s;
}

.control-color:before {
  content: '🎨';
  font-size: 20px;
}

@keyframes room-appear {
  0% { transform: scale(0.8); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}

@keyframes control-pop {
  0% { transform: scale(0); opacity: 0; }
  60% { transform: scale(1.2); }
  100% { transform: scale(1); opacity: 1; }
}

/* Animation pour la personnalisation d'environnement */
.animation-environment-adjust {
  position: absolute;
  left: 40px;
  top: 50px;
  width: 160px;
  height: 160px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.environment-slider {
  width: 140px;
  height: 20px;
  background: linear-gradient(to right, rgba(33, 150, 243, 0.2), rgba(33, 150, 243, 0.8));
  border-radius: 10px;
  position: relative;
  animation: slider-appear 0.5s forwards;
}

.environment-slider:after {
  content: '';
  position: absolute;
  top: -5px;
  left: 50%;
  width: 30px;
  height: 30px;
  background-color: white;
  border: 2px solid #2196F3;
  border-radius: 50%;
  transform: translateX(-50%);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  animation: slider-move 2s infinite alternate;
}

.environment-colors {
  display: flex;
  gap: 10px;
  animation: colors-appear 0.5s forwards;
  animation-delay: 0.3s;
  opacity: 0;
}

.color-swatch {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s;
}

.color-swatch:hover {
  transform: scale(1.1);
}

.swatch-warm {
  background-color: #ffccbc;
}

.swatch-neutral {
  background-color: #e0e0e0;
}

.swatch-cool {
  background-color: #bbdefb;
}

@keyframes slider-appear {
  0% { transform: scaleX(0.5); opacity: 0; }
  100% { transform: scaleX(1); opacity: 1; }
}

@keyframes slider-move {
  0% { left: 20%; }
  100% { left: 80%; }
}

@keyframes colors-appear {
  0% { transform: translateY(20px); opacity: 0; }
  100% { transform: translateY(0); opacity: 1; }
}

/* Animation de la logique (pour shape-sequence étape 2) */
.animation-logic {
  position: absolute;
  right: 30px;
  bottom: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.logic-pattern {
  display: flex;
  gap: 10px;
}

.pattern-shape {
  width: 30px;
  height: 30px;
  animation: highlight-pattern 3s infinite;
}

.pattern-circle {
  background-color: #F44336;
  border-radius: 50%;
  animation-delay: 0s;
}

.pattern-triangle {
  width: 0;
  height: 0;
  background-color: transparent;
  border-left: 15px solid transparent;
  border-right: 15px solid transparent;
  border-bottom: 30px solid #4CAF50;
  animation-delay: 1.5s;
}

.logic-arrow {
  font-size: 30px;
  color: #2196F3;
  margin: 10px 0;
  animation: pulse-arrow 2s infinite;
}

.logic-brain {
  width: 50px;
  height: 50px;
  background-color: #9C27B0;
  border-radius: 25px 25px 10px 10px;
  position: relative;
  animation: pulse-brain 2s infinite alternate;
}

.logic-brain:before, .logic-brain:after {
  content: '';
  position: absolute;
  top: -5px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: #9C27B0;
}

.logic-brain:before {
  left: 5px;
}

.logic-brain:after {
  right: 5px;
}

@keyframes highlight-pattern {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.2); box-shadow: 0 0 10px rgba(0, 0, 0, 0.3); }
}

@keyframes pulse-arrow {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.2); }
}

@keyframes pulse-brain {
  0% { transform: scale(1); }
  100% { transform: scale(1.1); box-shadow: 0 0 15px rgba(156, 39, 176, 0.5); }
}

/* Animation du badge (dernière étape) */
.animation-badge {
  position: absolute;
  right: 30px;
  bottom: 30px;
  width: 120px;
  height: 120px;
}

.badge-center {
  position: absolute;
  width: 80px;
  height: 80px;
  background-color: #FFC107;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  animation: shine-badge 3s infinite;
}

.badge-center::before {
  content: '';
  position: absolute;
  top: -5px;
  left: -5px;
  right: -5px;
  bottom: -5px;
  border-radius: 50%;
  border: 2px dashed #FF9800;
  animation: rotate-ring 10s linear infinite;
}

@keyframes shine-badge {
  0%, 100% { box-shadow: 0 0 0 0 rgba(255, 193, 7, 0.7); }
  50% { box-shadow: 0 0 30px 5px rgba(255, 193, 7, 0.7); }
}

@keyframes rotate-ring {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Hint d'animation */
.animation-hint {
  display: inline-block;
  margin-top: 15px;
  padding: 8px 16px;
  background-color: rgba(33, 150, 243, 0.1);
  border-radius: 20px;
  color: #2196F3;
  font-style: italic;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

/* Contrôles de navigation */
.guide-controls {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
}

.nav-button {
  padding: 12px 20px;
  border-radius: 30px;
  border: none;
  cursor: pointer;
  font-family: inherit;
  font-size: 1rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.2);
}

.prev-button {
  background-color: #E0E0E0;
  color: #333;
}

.prev-button:hover {
  background-color: #BDBDBD;
}

.next-button {
  background-color: #2196F3;
  color: white;
}

.next-button:hover {
  background-color: #1976D2;
  transform: translateY(-2px);
}

.start-button {
  background-color: #4CAF50;
  color: white;
  padding: 15px 25px;
  font-size: 1.1rem;
  animation: pulse 2s infinite;
}

.start-button:hover {
  background-color: #388E3C;
  transform: translateY(-3px);
}

.nav-icon {
  font-size: 1.2rem;
}

/* Bouton pour passer l'introduction */
.skip-button {
  position: absolute;
  top: 20px;
  right: 20px;
  background-color: transparent;
  border: none;
  color: #757575;
  cursor: pointer;
  font-size: 0.9rem;
  padding: 5px 10px;
  text-decoration: underline;
  transition: color 0.2s;
}

.skip-button:hover {
  color: #333;
}

/* Animations de transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.4s ease;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

/* Styles responsifs */
@media (max-width: 768px) {
  .central-guide-container {
    width: 95%;
    padding: 20px;
    min-height: 500px;
  }
  
  .game-title {
    font-size: 2rem;
  }
  
  .guide-character {
    width: 100px;
    height: 100px;
  }
  
  .step-content h2 {
    font-size: 1.5rem;
  }
  
  .step-content p, .step-content li {
    font-size: 1rem;
  }
  
  .visual-animation {
    width: 150px;
    height: 150px;
    right: 5%;
    bottom: 5%;
  }
}

@media (max-width: 480px) {
  .central-guide-container {
    padding: 15px 10px;
  }
  
  .game-title {
    font-size: 1.8rem;
    margin-bottom: 15px;
  }
  
  .guide-character {
    width: 80px;
    height: 80px;
  }
  
  .step-content h2 {
    font-size: 1.3rem;
  }
  
  .step-content p, .step-content li {
    font-size: 0.95rem;
  }
  
  .nav-button {
    padding: 10px 15px;
    font-size: 0.9rem;
  }
  
  .guide-controls {
    gap: 10px;
  }
  
  .visual-animation {
    width: 120px;
    height: 120px;
    bottom: 5%;
    right: 5%;
  }
  
  .animation-wheel, 
  .animation-shapes, 
  .animation-options, 
  .animation-logic,
  .animation-environment,
  .animation-environment-adjust,
  .animation-badge {
    transform: scale(0.7);
  }
  
  .animation-welcome-icon,
  .option-bubble,
  .environment-controls,
  .environment-colors,
  .badge-center {
    transform: scale(0.8);
  }
}

</style>