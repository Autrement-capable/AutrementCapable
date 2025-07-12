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
            </div>
          </transition>
        </div>
        
        <!-- Animation simple pour chaque jeu -->
        <div class="visual-animation">
          <!-- Animation selon le type de jeu -->
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
          
          <div v-else-if="gameId === 'jobs-game'" class="animation-jobs-cards">
            <div class="job-card-animation">
              <div class="job-card-front">👩‍🔬</div>
              <div class="job-card-shadow"></div>
            </div>
            <div class="swipe-arrows">
              <div class="swipe-left">👎</div>
              <div class="swipe-right">👍</div>
            </div>
          </div>
          
          <div v-else-if="gameId === 'speed-game'" class="animation-speed-typing">
            <div class="keyboard-animation">
              <div class="keyboard-icon">⌨️</div>
              <div class="typing-effect">
                <span class="typed-text">abc</span>
                <span class="typing-cursor">|</span>
              </div>
            </div>
          </div>
          
          <div v-else-if="gameId === 'scenarios-game'" class="animation-scenarios">
            <div class="scenario-map">
              <div class="scenario-path"></div>
              <div class="scenario-nodes">
                <div class="scenario-node node-1">1</div>
                <div class="scenario-node node-2">2</div>
                <div class="scenario-node node-3">3</div>
              </div>
            </div>
            <div class="dialogue-bubbles">
              <div class="bubble bubble-left">👋</div>
              <div class="bubble bubble-right">😊</div>
            </div>
          </div>
          
          <div v-else class="animation-welcome-icon"></div>
        </div>
        
        <!-- Contrôle de navigation simplifié -->
        <div class="guide-controls">
          <button 
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
      
      // Bibliothèque des contenus de jeux - UNE SEULE PAGE
      gamesContent: {
        'skills-wheel': {
          title: '🎯 Mes Compétences',
          steps: [
            `<h2>Salut ! Je suis Léo 👋</h2>
              <p><strong>🎡 Tu vas tourner une roue magique !</strong></p>
              <br>
              <p>🔄 <strong>Clique</strong> pour tourner la roue</p>
              <p>💪 <strong>Dis</strong> si tu es fort dans ce domaine</p>
              <p>🌱 <strong>Ou</strong> si tu veux t'améliorer</p>
              <br>
              <p><strong>✨ Il n'y a pas de bonne ou mauvaise réponse !</strong></p>
              <p>Sois juste honnête avec toi-même 😊</p>`
          ]
        },
        'shape-sequence': {
          title: '🧩 Suites de Formes',
          steps: [
            `<h2>Salut ! Je suis Léo 👋</h2>
              <p><strong>🧩 Tu vas jouer avec des formes !</strong></p>
              <br>
              <p>👀 <strong>Regarde</strong> bien les formes</p>
              <p>🤔 <strong>Trouve</strong> la logique</p>
              <p>✅ <strong>Choisis</strong> la forme qui manque</p>
              <br>
              <p><strong>✨ Prends ton temps pour réfléchir !</strong></p>
              <p>Tu peux réussir ! 💪</p>`
          ]
        },
        'sensory-environment': {
          title: '🌈 Mon Espace Parfait',
          steps: [
            `<h2>Salut ! Je suis Léo 👋</h2>
              <p><strong>🏠 Tu vas créer ton espace idéal !</strong></p>
              <br>
              <p>💡 <strong>Change la lumière</strong> (douce ou forte)</p>
              <p>🎨 <strong>Choisis les couleurs</strong> qui te plaisent</p>
              <p>🔊 <strong>Règle les sons</strong> (ou le silence)</p>
              <br>
              <p><strong>✨ Choisis ce qui te fait du bien !</strong></p>
              <p>Il n'y a pas de règles ! 😊</p>`
          ]
        },
        'jobs-game': {
          title: '💼 Découvre les Métiers',
          steps: [
            `<h2>Salut ! Je suis Léo 👋</h2>
              <p><strong>🃏 On va explorer des métiers !</strong></p>
              <br>
              <p>👀 <strong>Regarde</strong> chaque métier</p>
              <p>👍 <strong>Dis</strong> si ça te plaît</p>
              <p>👎 <strong>Ou</strong> si ce n'est pas pour toi</p>
              <br>
              <p><strong>✨ Découvre ce qui t'intéresse !</strong></p>
              <p>Il y a plein de métiers différents 🌟</p>`
          ]
        },
        'speed-game': {
          title: '⌨️ Jeu de Vitesse',
          steps: [
            `<h2>Salut ! Je suis Léo 👋</h2>
              <p><strong>📱 Tu vas taper sur le clavier !</strong></p>
              <br>
              <p>👀 <strong>Lis</strong> le mot à l'écran</p>
              <p>⌨️ <strong>Tape-le</strong> le plus vite possible</p>
              <p>⏰ <strong>Attention</strong> au temps !</p>
              <br>
              <p><strong>✨ Vas-y à ton rythme !</strong></p>
              <p>Tu vas devenir plus rapide ! 💪</p>`
          ]
        },
        'scenarios-game': {
          title: '🎭 Aventure des Scénarios',
          steps: [
            `<h2>Salut ! Je suis Léo 👋</h2>
              <p><strong>🗺️ Tu vas vivre des aventures sociales !</strong></p>
              <br>
              <p>📖 <strong>Lis</strong> la situation</p>
              <p>👂 <strong>Écoute</strong> les conversations</p>
              <p>💭 <strong>Choisis</strong> ta réponse</p>
              <br>
              <p><strong>✨ Chaque choix développe tes compétences !</strong></p>
              <p>Apprends à bien communiquer ! 🌟</p>`
          ]
        }
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
      return require('@/assets/flamou/hey.png'); // Assurez-vous que ce chemin est correct
    }
  },
  methods: {
    // Initialisation des animations
    startAnimation() {
      setTimeout(() => {
        this.animationStarted = true;
      }, 100);
    },
    
    // Navigation simplifiée (plus besoin de nextStep/previousStep)
    
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
  max-width: 700px;
  min-height: 500px;
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
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 4px solid white;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  object-fit: cover;
}

.guide-character-shadow {
  position: absolute;
  bottom: -8px;
  left: 15%;
  right: 15%;
  height: 8px;
  background-color: rgba(0, 0, 0, 0.15);
  border-radius: 50%;
  filter: blur(4px);
  transform: scale(1, 0.3);
  animation: shadow-pulse 5s infinite ease-in-out;
}

@keyframes shadow-pulse {
  0%, 100% { transform: scale(1, 0.3); opacity: 0.4; }
  50% { transform: scale(0.8, 0.2); opacity: 0.2; }
}

/* Titre du jeu */
.game-title {
  font-size: 2.2rem;
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
  bottom: -6px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
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
  max-width: 500px;
  text-align: center;
}

.step-content h2 {
  color: #4CAF50;
  margin-bottom: 15px;
  font-size: 1.6rem;
}

.step-content p {
  font-size: 1.2rem;
  line-height: 1.5;
  margin-bottom: 12px;
  color: #333;
}

.step-counter {
  margin-top: 15px;
  font-size: 1rem;
  color: #666;
}

.current-step {
  font-weight: bold;
  color: #2196F3;
  font-size: 1.2rem;
}

/* Animations visuelles simplifiées */
.visual-animation {
  position: absolute;
  width: 150px;
  height: 150px;
  pointer-events: none;
  top: auto;
  right: 10%;
  bottom: 10%;
}

/* Animation d'accueil par défaut */
.animation-welcome-icon {
  position: absolute;
  right: 20px;
  bottom: 20px;
  width: 60px;
  height: 60px;
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
  font-size: 30px;
}

@keyframes pulse-welcome {
  0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 193, 7, 0.7); }
  70% { transform: scale(1.1); box-shadow: 0 0 0 15px rgba(255, 193, 7, 0); }
  100% { transform: scale(1); }
}

/* Animation de la roue simplifiée */
.animation-wheel {
  position: absolute;
  right: 20px;
  bottom: 20px;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: #f5f5f5;
  border: 3px solid #333;
  animation: spin-wheel 3s infinite ease-in-out;
}

.wheel-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 15px;
  height: 15px;
  background-color: #333;
  border-radius: 50%;
  z-index: 2;
}

@keyframes spin-wheel {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Animation des formes simplifiée */
.animation-shapes {
  position: absolute;
  right: 20px;
  bottom: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.shape {
  width: 25px;
  height: 25px;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: pop-in 0.5s forwards;
  opacity: 0;
  transform: scale(0.5);
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
  border-left: 12px solid transparent;
  border-right: 12px solid transparent;
  border-bottom: 25px solid #4CAF50;
  animation-delay: 0.6s;
}

.shape-question {
  background-color: #FFC107;
  border-radius: 6px;
  font-size: 16px;
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
  70% { transform: scale(1.1); box-shadow: 0 0 0 8px rgba(255, 193, 7, 0); }
  100% { transform: scale(1); }
}

/* Animation environnement simplifiée */
.animation-environment {
  position: absolute;
  right: 30px;
  bottom: 30px;
  width: 120px;
  height: 120px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.environment-room {
  width: 80px;
  height: 60px;
  background: linear-gradient(to bottom, #e6f7ff, #ffffff);
  border: 2px solid #80bdff;
  border-radius: 8px;
  position: relative;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
  animation: room-appear 1s forwards;
}

.environment-controls {
  display: flex;
  justify-content: space-around;
  width: 100%;
  gap: 6px;
}

.control-light, .control-sound, .control-color {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  opacity: 0;
  animation: control-pop 0.5s forwards;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}

.control-light {
  background-color: #FFC107;
  animation-delay: 0.3s;
}

.control-light:before {
  content: '💡';
  font-size: 16px;
}

.control-sound {
  background-color: #2196F3;
  animation-delay: 0.5s;
}

.control-sound:before {
  content: '🔊';
  font-size: 16px;
}

.control-color {
  background-color: #F44336;
  animation-delay: 0.7s;
}

.control-color:before {
  content: '🎨';
  font-size: 16px;
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

/* Animation métiers simplifiée */
.animation-jobs-cards {
  position: absolute;
  right: 15px;
  bottom: 30px;
  width: 120px;
  height: 120px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.job-card-animation {
  position: relative;
  width: 80px;
  height: 100px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  animation: card-float 3s infinite ease-in-out;
}

.job-card-front {
  font-size: 35px;
  animation: emoji-pulse 2s infinite alternate;
}

.swipe-arrows {
  position: absolute;
  width: 120px;
  display: flex;
  justify-content: space-between;
  margin-top: 110px;
}

.swipe-left, .swipe-right {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  opacity: 0.8;
  animation: arrow-pulse 1.5s infinite alternate;
}

.swipe-left {
  background-color: rgba(244, 67, 54, 0.3);
  animation-delay: 0.75s;
}

.swipe-right {
  background-color: rgba(76, 175, 80, 0.3);
  animation-delay: 0s;
}

@keyframes card-float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

@keyframes emoji-pulse {
  0% { transform: scale(1); }
  100% { transform: scale(1.1); }
}

@keyframes arrow-pulse {
  0% { transform: scale(1); opacity: 0.6; }
  100% { transform: scale(1.2); opacity: 1; }
}

/* Animation vitesse simplifiée */
.animation-speed-typing {
  position: absolute;
  right: 30px;
  bottom: 30px;
  width: 100px;
  height: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.keyboard-animation {
  background-color: #f5f5f5;
  border-radius: 10px;
  width: 90px;
  height: 60px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
  position: relative;
}

.keyboard-icon {
  font-size: 20px;
  position: absolute;
  top: 3px;
  opacity: 0.7;
}

.typing-effect {
  margin-top: 18px;
  font-family: monospace;
  font-size: 14px;
  font-weight: bold;
  color: #2196F3;
}

.typing-cursor {
  animation: cursor-blink 0.8s infinite;
}

@keyframes cursor-blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

/* Animation scénarios simplifiée */
.animation-scenarios {
  position: absolute;
  right: 1px;
  bottom: 5px;
  width: 120px;
  height: 120px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.scenario-map {
  width: 80px;
  height: 60px;
  background: linear-gradient(to bottom, #e8f4e5, #f0f8ff);
  border: 2px solid #9c7248;
  border-radius: 8px;
  position: relative;
  overflow: hidden;
  animation: map-appear 1s forwards;
}

.scenario-path {
  position: absolute;
  top: 50%;
  left: 10%;
  right: 10%;
  height: 2px;
  background: linear-gradient(to right, #4caf50, #2196f3, #ff9800);
  border-radius: 1px;
  animation: path-draw 2s infinite;
}

.scenario-nodes {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.scenario-node {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background-color: #fff;
  border: 2px solid #4caf50;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: bold;
  color: #4caf50;
  animation: node-pulse 2s infinite;
}

.node-2 {
  animation-delay: 0.5s;
}

.node-3 {
  animation-delay: 1s;
}

.dialogue-bubbles {
  display: flex;
  gap: 15px;
  margin-top: 5px;
}

.bubble {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  animation: bubble-bounce 1.5s infinite alternate;
}

.bubble-left {
  background-color: #e9f5ff;
  border: 2px solid #2196f3;
  animation-delay: 0s;
}

.bubble-right {
  background-color: #e6f7e6;
  border: 2px solid #4caf50;
  animation-delay: 0.75s;
}

@keyframes map-appear {
  0% { transform: scale(0.8); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}

@keyframes path-draw {
  0% { background-position: -100% 0; }
  100% { background-position: 100% 0; }
}

@keyframes node-pulse {
  0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.4); }
  50% { transform: scale(1.1); box-shadow: 0 0 0 4px rgba(76, 175, 80, 0); }
}

@keyframes bubble-bounce {
  0% { transform: translateY(0); }
  100% { transform: translateY(-8px); }
}

/* Contrôles de navigation */
.guide-controls {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 15px;
}

.nav-button {
  padding: 10px 18px;
  border-radius: 25px;
  border: none;
  cursor: pointer;
  font-family: inherit;
  font-size: 1rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 6px;
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
  padding: 12px 20px;
  font-size: 1.1rem;
  animation: pulse 2s infinite;
}

.start-button:hover {
  background-color: #388E3C;
  transform: translateY(-3px);
}

.nav-icon {
  font-size: 1.1rem;
}

/* Bouton pour passer l'introduction */
.skip-button {
  position: absolute;
  top: 15px;
  right: 15px;
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
    min-height: 400px;
  }
  
  .game-title {
    font-size: 1.8rem;
  }
  
  .guide-character {
    width: 80px;
    height: 80px;
  }
  
  .step-content h2 {
    font-size: 1.4rem;
  }
  
  .step-content p {
    font-size: 1.1rem;
  }
  
  .visual-animation {
    width: 100px;
    height: 100px;
    right: 5%;
    bottom: 5%;
  }
}

@media (max-width: 480px) {
  .central-guide-container {
    padding: 15px;
  }
  
  .game-title {
    font-size: 1.6rem;
    margin-bottom: 15px;
  }
  
  .guide-character {
    width: 70px;
    height: 70px;
  }
  
  .step-content h2 {
    font-size: 1.2rem;
  }
  
  .step-content p {
    font-size: 1rem;
  }
  
  .nav-button {
    padding: 8px 12px;
    font-size: 0.9rem;
  }
  
  .guide-controls {
    gap: 10px;
  }
  
  .visual-animation {
    width: 80px;
    height: 80px;
    bottom: 5%;
    right: 5%;
  }
}
</style>