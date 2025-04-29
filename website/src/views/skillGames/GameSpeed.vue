<template>
  <div class="speed-game-container">
    <!-- Animation de déblocage du badge -->
    <div v-if="showBadgeUnlockAnimation" class="badge-unlock-overlay">
      <div class="badge-unlock-animation">
        <div class="badge-icon">⚡</div>
        <h2>Badge débloqué !</h2>
        <h3>{{ badgeData.name }}</h3>
        <p>{{ badgeData.description }}</p>
        <button @click="closeBadgeAnimation" class="close-animation-btn">Continuer</button>
      </div>
    </div>

    <!-- Header avec personnage guide -->
    <!-- <div class="guide-character" v-if="!gameStarted">
      <img src="@/assets/avatars/guide.png" alt="Guide" class="guide-avatar" />
      <div class="speech-bubble">
        <p>Bienvenue dans le jeu de vitesse ! Teste ta rapidité de frappe et ta précision à différents niveaux de difficulté.</p>
      </div>
    </div>

    <div class="game-header">
      <h1 class="main-title">Jeu de Vitesse</h1>
      <p class="subtitle" v-if="!gameStarted">Améliore ta vitesse de frappe et ta concentration</p>
    </div> -->
    
    <!-- Écran d'accueil -->
    <!-- <div class="welcome-screen" v-if="!gameStarted">
      <div class="welcome-card">
        <div class="card-icon">⚡</div>
        <h2>Comment jouer ?</h2>
        <ol class="instructions-list">
          <li><span class="instruction-step">1</span> Tape le texte qui apparaît à l'écran le plus rapidement possible</li>
          <li><span class="instruction-step">2</span> La difficulté augmente progressivement avec des mots puis des phrases</li>
          <li><span class="instruction-step">3</span> Fais attention au timer ! Plus tu avances, plus le défi est grand</li>
        </ol>
        <button @click="startGame" class="start-button">
          <span class="btn-icon">🎮</span>
          <span class="btn-text">Commencer à jouer</span>
        </button>
      </div>
    </div> -->
    <GameGuide
      v-if="!gameStarted"
      gameId="speed-game"
      :forceShow="true"
      @start-game="startGame"
      @skip-intro="startGame"
    />
    
    <!-- Zone de jeu principale -->
    <div class="game-playground" v-if="gameStarted && !showResults">
      <!-- Barre de progression -->
      <div class="progress-container">
        <div class="progress-steps">
          <div class="progress-step" :class="{ 'completed': currentLevel > 0 }">
            <div class="step-icon">🎮</div>
            <div class="step-label">Démarrage</div>
          </div>
          
          <div class="progress-connector"></div>
          
          <div class="progress-step" :class="{ 'completed': currentLevel >= Math.floor(levels.length/3) }">
            <div class="step-icon">🏃</div>
            <div class="step-label">En cours</div>
          </div>
          
          <div class="progress-connector"></div>
          
          <div class="progress-step" :class="{ 'completed': currentLevel >= Math.floor(levels.length*2/3) }">
            <div class="step-icon">🔍</div>
            <div class="step-label">Avancé</div>
          </div>
          
          <div class="progress-connector"></div>
          
          <div class="progress-step" :class="{ 'completed': currentLevel >= levels.length }">
            <div class="step-icon">🏆</div>
            <div class="step-label">Terminé</div>
          </div>
        </div>
        
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
          <div class="progress-text">{{ currentLevel + 1 }} / {{ levels.length }}</div>
        </div>
      </div>

      <div class="level-indicator">
        <div class="level-badge">Niveau {{ currentLevel + 1 }}: {{ levels[currentLevel].type }}</div>
        <div class="timer-badge" :class="{ 'warning': timeLeft <= 10, 'danger': timeLeft <= 5 }">
          Temps: {{ timeLeft }}s
        </div>
      </div>
      
              <!-- Contenu du jeu -->
      <div class="game-content">
        <!-- Compte à rebours avant le niveau -->
        <div v-if="countdownActive" class="countdown-overlay">
          <div class="countdown-value">{{ countdownValue }}</div>
        </div>
        
        <div class="typing-section">
          <div class="typing-challenge">
            <div class="typing-target">
              <div class="target-text">
                <span 
                  v-for="(char, index) in targetText" 
                  :key="index"
                  :class="{
                    'correct-char': index < inputValue.length && char === inputValue[index],
                    'incorrect-char': index < inputValue.length && char !== inputValue[index],
                    'current-char': index === inputValue.length,
                    'pending-char': index > inputValue.length
                  }"
                >{{ char }}</span>
              </div>
            </div>

            <div class="typing-input-container">
              <input 
                ref="inputField" 
                type="text" 
                class="typing-input" 
                v-model="inputValue" 
                @input="checkInput" 
                :disabled="levelCompleted || countdownActive"
                placeholder="Tape ici..."
                autocomplete="off"
                autocorrect="off"
                autocapitalize="off"
                spellcheck="false"
              />
            </div>
          </div>
          
          <div class="feedback-message" :class="feedbackClass" v-if="feedback">
            {{ feedback }}
          </div>
        </div>
      </div>
      
      <!-- Stats du jeu -->
      <div class="stats-container">
        <div class="stat-item">
          <div class="stat-label">Précision</div>
          <div class="stat-value">{{ accuracy }}%</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">WPM</div>
          <div class="stat-value">{{ wpm }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">Erreurs</div>
          <div class="stat-value">{{ mistakes }}</div>
        </div>
      </div>
      
      <!-- Boutons d'action -->
      <div class="game-actions">
        <button v-if="levelCompleted" @click="nextLevel" class="action-button next-button">
          <span class="btn-icon">▶️</span>
          <span class="btn-text">Niveau suivant</span>
        </button>
        
        <button @click="restartLevel" class="action-button restart-button" v-if="!levelCompleted">
          <span class="btn-icon">🔄</span>
          <span class="btn-text">Recommencer</span>
        </button>
        
        <button @click="endGame" class="action-button end-button">
          <span class="btn-icon">🏁</span>
          <span class="btn-text">Terminer</span>
        </button>
      </div>
    </div>
    
    <!-- Écran des résultats -->
    <div class="results-overlay" v-if="showResults">
      <div class="results-modal">
        <div class="results-header">
          <div class="results-title-container">
            <div class="results-title-icon">🏆</div>
            <h2 class="results-title">Félicitations !</h2>
          </div>
          <p class="results-subtitle">Voici un résumé de ta performance</p>
        </div>
        
        <div class="results-statistics">
          <div class="stat-item">
            <div class="stat-value">{{ finalScore }}</div>
            <div class="stat-label">Score Total</div>
          </div>
          
          <div class="stat-item">
            <div class="stat-value">{{ averageWpm }}</div>
            <div class="stat-label">WPM Moyen</div>
          </div>
          
          <div class="stat-item">
            <div class="stat-value">{{ totalAccuracy }}%</div>
            <div class="stat-label">Précision</div>
          </div>
        </div>
        
        <p class="result-message">
          {{ getResultMessage() }}
        </p>
        
        <div class="results-actions">
          <button @click="restartGame" class="action-button restart-button">
            <span class="btn-icon">🔄</span>
            <span class="btn-text">Rejouer</span>
          </button>
          <button @click="goToNextGame" class="action-button next-game-button">
            <span class="btn-icon">🎮</span>
            <span class="btn-text">Prochain jeu</span>
          </button>
          <button @click="goToDashboard" class="action-button home-button">
            <span class="btn-icon">🏠</span>
            <span class="btn-text">Retour à l'accueil</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { unlockBadge, isBadgeUnlocked } from '@/utils/badges';
import GameGuide from '@/components/GameGuideComponent.vue';

export default {
  name: 'GameSpeed',
  components: {
    GameGuide
  },

  data() {
    return {
      gameStarted: false,
      showResults: false,
      currentLevel: 0,
      inputValue: '',
      targetText: '',
      timeLeft: 0,
      timer: null,
      levelTimer: null,
      mistakes: 0,
      wpm: 0,
      accuracy: 100,
      feedback: '',
      feedbackClass: '',
      levelCompleted: false,
      gameStartTime: null,
      levelStartTime: null,
      levelResults: [],
      showBadgeUnlockAnimation: false,
      badgeSpeedMasterId: 1,
      countdownInterval: null,
      badgeData: {
        name: "Maître de la vitesse",
        description: "Tu as terminé le jeu de vitesse avec une excellente performance !"
      },
      countdownActive: false,
      countdownValue: 3,
      // Structure des niveaux avec une difficulté progressive
      levels: [
        // Un mot court unique pour commencer facilement
        { 
          type: 'Mot court', 
          text: 'chat',
          timeLimit: 5
        },
        // Un mot long unique
        { 
          type: 'Mot long', 
          text: 'informatique',
          timeLimit: 10
        },
        // Une phrase très courte
        { 
          type: 'Phrase courte', 
          text: 'Le chat dort.',
          timeLimit: 10
        },
        // Une phrase un peu plus longue
        { 
          type: 'Phrase moyenne', 
          text: 'Il fait beau aujourd\'hui.',
          timeLimit: 12
        },
        // Quelques mots courts
        { 
          type: 'Mots courts', 
          text: 'chat chien arbre pomme soleil',
          timeLimit: 15
        },
        // Quelques mots longs
        { 
          type: 'Mots longs', 
          text: 'développement technologie communication',
          timeLimit: 20
        },
        // Phrase plus complexe
        { 
          type: 'Phrase complexe', 
          text: 'Les nouvelles technologies évoluent rapidement dans notre monde.',
          timeLimit: 25
        },
        // Un petit paragraphe pour finir
        { 
          type: 'Paragraphe', 
          text: 'La vitesse de frappe est une compétence utile. Elle permet de gagner du temps et d\'être plus efficace. Avec de la pratique, on peut tous s\'améliorer.',
          timeLimit: 30
        }
      ]
    };
  },
  computed: {
    // Calcul du pourcentage de progression dans les niveaux
    progressPercentage() {
      return (this.currentLevel / this.levels.length) * 100;
    },
    
    // Mise en forme du texte cible avec coloration des caractères tapés
    formattedTargetText() {
      if (!this.targetText) return '';
      
      const typedLength = this.inputValue.length;
      let result = '';
      
      for (let i = 0; i < this.targetText.length; i++) {
        if (i < typedLength) {
          // Caractère déjà tapé
          if (this.inputValue[i] === this.targetText[i]) {
            // Caractère correct - vert
            result += `<span class="correct-char">${this.targetText[i]}</span>`;
          } else {
            // Caractère incorrect - rouge
            result += `<span class="incorrect-char">${this.targetText[i]}</span>`;
          }
        } else if (i === typedLength) {
          // Position actuelle du curseur - souligné et en surbrillance
          result += `<span class="current-char">${this.targetText[i]}</span>`;
        } else {
          // Caractère pas encore tapé - normal
          result += `<span class="pending-char">${this.targetText[i]}</span>`;
        }
      }
      
      return result;
    },
    
    // Résultats finaux pour l'écran de résultat
    finalScore() {
      // Calcul du score total en fonction du WPM moyen et de la précision
      return Math.round(this.averageWpm * (this.totalAccuracy / 100));
    },
    
    averageWpm() {
      if (this.levelResults.length === 0) return 0;
      
      const totalWpm = this.levelResults.reduce((sum, result) => sum + result.wpm, 0);
      return Math.round(totalWpm / this.levelResults.length);
    },
    
    totalAccuracy() {
      if (this.levelResults.length === 0) return 100;
      
      const totalAccuracy = this.levelResults.reduce((sum, result) => sum + result.accuracy, 0);
      return Math.round(totalAccuracy / this.levelResults.length);
    }
  },
  beforeUnmount() {
    // Nettoyer les timers avant de quitter la page
    this.clearTimers();
  },
  methods: {
    // Démarrer le jeu
    startGame() {
      this.gameStarted = true;
      this.gameStartTime = new Date();
      this.loadLevel();
    },
    
    // Charger un niveau
    loadLevel() {
      if (this.currentLevel >= this.levels.length) {
        this.endGame();
        return;
      }
      
      this.targetText = this.levels[this.currentLevel].text;
      this.timeLeft = this.levels[this.currentLevel].timeLimit;
      this.inputValue = '';
      this.mistakes = 0;
      this.wpm = 0;
      this.accuracy = 100;
      this.feedback = '';
      this.feedbackClass = '';
      this.levelCompleted = false;
      
      // Démarrer le compte à rebours avant de commencer le niveau
      this.startCountdown();
    },
    
    // Démarrer le compte à rebours de 3 secondes
    startCountdown() {
      this.countdownActive = true;
      this.countdownValue = 3;
      
      // Nettoyer un éventuel intervalle existant
      if (this.countdownInterval) {
        clearInterval(this.countdownInterval);
      }
      
      this.countdownInterval = setInterval(() => {
        this.countdownValue--;
        
        if (this.countdownValue <= 0) {
          clearInterval(this.countdownInterval);
          this.countdownInterval = null;
          this.countdownActive = false;
          
          // Une fois le compte à rebours terminé, ALORS démarrer le niveau et le timer
          this.levelStartTime = new Date();
          this.startLevelTimer();
          
          // Mettre le focus sur le champ de saisie
          this.$nextTick(() => {
            if (this.$refs.inputField) {
              this.$refs.inputField.focus();
            }
          });
        }
      }, 1000);
    },
    
    // Démarrer le timer du niveau
    startLevelTimer() {
      this.clearTimers();
      
      this.timer = setInterval(() => {
        if (this.timeLeft > 0) {
          this.timeLeft--;
        } else {
          // Le temps est écoulé
          this.clearTimers();
          if (!this.levelCompleted) {
            this.showTimesUpFeedback();
          }
        }
      }, 1000);
    },
    
    // Vérifier l'entrée de l'utilisateur
    checkInput() {
      const input = this.inputValue;
      const target = this.targetText;
      
      // Vérifier si le niveau est déjà complété
      if (this.levelCompleted) return;
      
      // Calculer les erreurs
      let currentMistakes = 0;
      for (let i = 0; i < input.length; i++) {
        if (i >= target.length || input[i] !== target[i]) {
          currentMistakes++;
        }
      }
      
      this.mistakes = currentMistakes;
      
      // Calculer la précision
      const accuracy = input.length > 0
        ? Math.max(0, Math.round(((input.length - currentMistakes) / input.length) * 100))
        : 100;
      this.accuracy = accuracy;
      
      // Calculer le WPM (mots par minute)
      const timeElapsed = (new Date() - this.levelStartTime) / 1000 / 60;
      const wordsTyped = input.length / 5;
      this.wpm = timeElapsed > 0 ? Math.round(wordsTyped / timeElapsed) : 0;
      
      this.$nextTick(() => {
        this.inputValue = this.inputValue.slice();
      });
      
      // Vérifier si le niveau est complété
      if (input === target) {
        this.completeLevel();
      }
    },
    
    // Compléter le niveau actuel
    completeLevel() {
      this.levelCompleted = true;
      this.clearTimers();
      
      // Enregistrer les résultats du niveau
      this.levelResults.push({
        level: this.currentLevel + 1,
        wpm: this.wpm,
        accuracy: this.accuracy,
        mistakes: this.mistakes,
        time: this.levels[this.currentLevel].timeLimit - this.timeLeft // temps utilisé
      });
      
      // Afficher un feedback positif
      this.feedback = "Excellent ! Niveau complété !";
      this.feedbackClass = "feedback-correct";
      
      // Débloquer le badge si c'est le dernier niveau et si la performance est bonne
      if (this.currentLevel === this.levels.length - 1 && this.accuracy >= 90) {
        this.unlockSpeedMasterBadge();
      }
    },
    
    // Afficher un message quand le temps est écoulé
    showTimesUpFeedback() {
      this.feedback = "Temps écoulé !";
      this.feedbackClass = "feedback-incorrect";
      
      // Enregistrer les résultats incomplets
      this.levelResults.push({
        level: this.currentLevel + 1,
        wpm: this.wpm,
        accuracy: this.accuracy,
        mistakes: this.mistakes,
        time: this.levels[this.currentLevel].timeLimit // temps maximal utilisé
      });
      
      // Permettre de passer au niveau suivant même si celui-ci n'est pas complété
      this.levelCompleted = true;
    },
    
    // Passer au niveau suivant
    nextLevel() {
      this.currentLevel++;
      this.loadLevel();
    },
    
    // Recommencer le niveau actuel
    restartLevel() {
      this.loadLevel();
    },
    
    // Terminer le jeu et afficher les résultats
    endGame() {
      this.clearTimers();
      this.showResults = true;
    },
    
    // Redémarrer tout le jeu
    restartGame() {
      this.currentLevel = 0;
      this.levelResults = [];
      this.showResults = false;
      this.gameStartTime = new Date();
      this.loadLevel();
    },
    
    // Nettoyer les timers
    clearTimers() {
      if (this.timer) {
        clearInterval(this.timer);
        this.timer = null;
      }
      if (this.levelTimer) {
        clearInterval(this.levelTimer);
        this.levelTimer = null;
      }
      if (this.countdownInterval) {
        clearInterval(this.countdownInterval);
        this.countdownInterval = null;
      }
    },
    
    // Aller au jeu suivant (GameShape)
    goToNextGame() {
      this.$router.push('/game-shape');
    },
    
    // Retourner au tableau de bord
    goToDashboard() {
      this.$router.push('/dashboard');
    },
    
    // Débloquer le badge de maître de la vitesse
    unlockSpeedMasterBadge() {
      if (!isBadgeUnlocked(this.badgeSpeedMasterId)) {
        const badgeUnlocked = unlockBadge(this.badgeSpeedMasterId);
        if (badgeUnlocked) {
          setTimeout(() => {
            this.showBadgeUnlockAnimation = true;
          }, 1500);
        }
      }
    },
    
    // Fermer l'animation du badge
    closeBadgeAnimation() {
      this.showBadgeUnlockAnimation = false;
    },
    
    // Obtenir un message personnalisé selon la performance
    getResultMessage() {
      const accuracy = this.totalAccuracy;
      const wpm = this.averageWpm;
      
      if (accuracy >= 95 && wpm >= 40) {
        return "Impressionnant ! Ta vitesse et ta précision sont exceptionnelles. Tu as un vrai talent pour la frappe rapide !";
      } else if (accuracy >= 90 && wpm >= 30) {
        return "Très bonne performance ! Tu as une excellente combinaison de vitesse et de précision.";
      } else if (accuracy >= 80 && wpm >= 20) {
        return "Bon travail ! Avec un peu plus de pratique, tu pourras encore améliorer ta vitesse tout en maintenant une bonne précision.";
      } else if (accuracy >= 70) {
        return "Tu te débrouilles bien ! Continue à t'entraîner pour améliorer ta vitesse et ta précision.";
      } else {
        return "C'est un bon début ! La vitesse de frappe s'améliore avec la pratique régulière. N'hésite pas à réessayer !";
      }
    }
  }
};
</script>

<style scoped>
/* Base Styles */
.speed-game-container {
  font-family: 'Comic Sans MS', 'Chalkboard SE', 'Marker Felt', sans-serif;
  max-width: 1100px;
  margin: 0 auto;
  padding: 20px;
  color: #333;
  min-height: 100vh;
}

/* Game Header */
.game-header {
  text-align: center;
  margin-bottom: 30px;
}

.main-title {
  font-size: 2.5rem;
  color: #2196F3; /* Bleu pour le thème du jeu de vitesse */
  margin-bottom: 10px;
  text-align: center;
  position: relative;
  padding-bottom: 10px;
}

.main-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 4px;
  background-color: #FF9800;
  border-radius: 2px;
}

.subtitle {
  font-size: 1.2rem;
  color: #666;
  margin: 0;
}

/* Guide Character */
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
  font-size: 1.1rem;
  color: #333;
  line-height: 1.5;
}

/* Animation du badge débloqué */
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
  z-index: 1100;
  animation: fadeIn 0.5s ease-out;
}

.badge-unlock-animation {
  background-color: #fff;
  border-radius: 20px;
  padding: 30px;
  text-align: center;
  max-width: 400px;
  box-shadow: 0 0 30px rgba(33, 150, 243, 0.6); /* Couleur bleue pour le thème du jeu */
  animation: scaleIn 0.5s ease-out;
}

.badge-unlock-animation .badge-icon {
  font-size: 80px;
  margin-bottom: 20px;
  animation: pulse 2s infinite;
  color: #2196F3; /* Bleu pour le thème du jeu */
}

.badge-unlock-animation h2 {
  color: #2196F3;
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
  background-color: #2196F3;
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
  background-color: #1976D2;
  transform: scale(1.05);
}

/* Welcome Screen */
.welcome-screen {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  align-items: center;
  margin: 40px 0;
}

.welcome-card {
  flex: 1;
  min-width: 300px;
  background-color: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 20px;
  color: #2196F3;
}

.welcome-card h2 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 20px;
}

.instructions-list {
  text-align: left;
  padding-left: 10px;
  margin-bottom: 30px;
}

.instructions-list li {
  margin-bottom: 15px;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 15px;
}

.instruction-step {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  background-color: #2196F3;
  color: white;
  border-radius: 50%;
  flex-shrink: 0;
}

.start-button {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 15px 30px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  margin-top: 20px;
  width: auto;
  height: auto;
}

.start-button:hover {
  background-color: #388E3C;
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

.btn-icon {
  font-size: 1.3rem;
}

/* Game Playground */
.game-playground {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
}

/* Progress Steps */
.progress-container {
  width: 100%;
  max-width: 800px;
  margin-bottom: 20px;
}

.progress-steps {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
}

.progress-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 2;
}

.step-icon {
  width: 40px;
  height: 40px;
  background-color: #e9ecef;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  margin-bottom: 5px;
  border: 2px solid #ced4da;
  position: relative;
}

.step-label {
  font-size: 0.8rem;
  color: #6c757d;
}

.progress-step.completed .step-icon {
  background-color: #2196F3;
  color: white;
  border-color: #2196F3;
}

.progress-step.completed .step-label {
  color: #2196F3;
}

.progress-connector {
  height: 2px;
  background-color: #ced4da;
  flex-grow: 1;
  margin: 0 -5px;
  position: relative;
  top: -22px;
  z-index: 1;
}

.progress-bar {
  width: 100%;
  height: 16px;
  background-color: #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #2196F3, #03A9F4);
  border-radius: 8px;
  transition: width 0.5s ease;
}

.progress-text {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #333;
  font-weight: bold;
  font-size: 0.75rem;
}

/* Level Indicator */
.level-indicator {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 800px;
  margin-bottom: 20px;
}

.level-badge, .timer-badge {
  background-color: #2196F3;
  color: white;
  padding: 8px 16px;
  border-radius: 50px;
  font-weight: bold;
  font-size: 1rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.timer-badge {
  background-color: #4CAF50;
  transition: background-color 0.3s ease;
}

.timer-badge.warning {
  background-color: #FFC107;
  animation: pulse 1s infinite;
}

.timer-badge.danger {
  background-color: #F44336;
  animation: pulse 0.5s infinite;
}

/* Countdown Overlay */
.countdown-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.7);
  border-radius: 20px;
  z-index: 10;
}

.countdown-value {
  font-size: 8rem;
  font-weight: bold;
  color: white;
  animation: pulseCountdown 1s infinite;
  text-shadow: 0 0 20px rgba(33, 150, 243, 0.8);
}

@keyframes pulseCountdown {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.2); opacity: 0.8; }
  100% { transform: scale(1); opacity: 1; }
}

/* Game Content */
.game-content {
  position: relative;
  width: 100%;
  max-width: 800px;
  background-color: white;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.typing-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.typing-challenge {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.typing-target {
  background-color: #f5f5f5;
  border-radius: 10px;
  padding: 20px;
  font-size: 1.5rem;
  line-height: 1.8;
  min-height: 100px;
  word-wrap: break-word;
  text-align: left;
}

.target-text {
  letter-spacing: 1px;
}

.typing-input-container {
  width: 100%;
}

.typing-input {
  width: 100%;
  padding: 15px;
  font-size: 1.1rem;
  border: 2px solid #ddd;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.typing-input:focus {
  outline: none;
  border-color: #2196F3;
  box-shadow: 0 0 10px rgba(33, 150, 243, 0.3);
}

.typing-input:disabled {
  background-color: #f8f8f8;
  cursor: not-allowed;
}

/* Characters styling */
.correct-char {
  color: #4CAF50;
  font-weight: bold;
  background-color: rgba(76, 175, 80, 0.1);
  border-radius: 2px;
  padding: 0 2px;
}

.incorrect-char {
  color: #F44336;
  font-weight: bold;
  background-color: rgba(244, 67, 54, 0.1);
  text-decoration: underline wavy #F44336;
  border-radius: 2px;
  padding: 0 2px;
}

.current-char {
  background-color: #E3F2FD;
  border-bottom: 2px solid #2196F3;
  animation: blink 1s infinite;
  padding: 0 2px;
  border-radius: 2px;
  font-weight: bold;
}

.pending-char {
  color: #666;
  padding: 0 2px;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Feedback Message */
.feedback-message {
  padding: 15px;
  border-radius: 10px;
  font-weight: bold;
  text-align: center;
  animation: fadeIn 0.5s ease;
}

.feedback-correct {
  background-color: #E8F5E9;
  color: #4CAF50;
}

.feedback-incorrect {
  background-color: #FFEBEE;
  color: #F44336;
}

/* Stats Container */
.stats-container {
  display: flex;
  justify-content: space-around;
  width: 100%;
  max-width: 800px;
  margin-bottom: 20px;
}

.stat-item {
  background-color: white;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 15px;
  text-align: center;
  min-width: 100px;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 1.3rem;
  font-weight: bold;
  color: #2196F3;
}

/* Game Actions */
.game-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.action-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 12px 25px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.action-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

.next-button {
  background-color: #4CAF50;
}

.next-button:hover {
  background-color: #388E3C;
}

.restart-button {
  background-color: #FF9800;
}

.restart-button:hover {
  background-color: #F57C00;
}

.end-button {
  background-color: #F44336;
}

.end-button:hover {
  background-color: #D32F2F;
}

/* Results Overlay */
.results-overlay {
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

.results-modal {
  background-color: white;
  border-radius: 20px;
  padding: 30px;
  max-width: 800px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
  animation: scaleIn 0.5s ease-out;
}

.results-header {
  text-align: center;
  margin-bottom: 30px;
}

.results-title-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  margin-bottom: 10px;
}

.results-title-icon {
  font-size: 2.5rem;
  color: #2196F3;
}

.results-title {
  font-size: 2rem;
  color: #333;
  margin: 0;
}

.results-subtitle {
  font-size: 1.2rem;
  color: #666;
  margin: 0;
}

/* Results Statistics */
.results-statistics {
  display: flex;
  justify-content: space-around;
  margin-bottom: 30px;
}

.results-statistics .stat-item {
  width: 30%;
  padding: 20px;
}

.results-statistics .stat-value {
  font-size: 2rem;
}

.result-message {
  text-align: center;
  font-size: 1.1rem;
  color: #555;
  margin: 25px 0;
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 10px;
  line-height: 1.6;
}

.results-actions {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 15px;
  margin-top: 30px;
}

.next-game-button {
  background-color: #9C27B0;
}

.next-game-button:hover {
  background-color: #7B1FA2;
}

.home-button {
  background-color: #607D8B;
}

.home-button:hover {
  background-color: #455A64;
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

/* Responsive Design */
@media (max-width: 768px) {
  .main-title {
    font-size: 2rem;
  }
  
  .game-content {
    padding: 15px;
  }
  
  .typing-target {
    font-size: 1rem;
    padding: 15px;
  }
  
  .typing-input {
    font-size: 1rem;
    padding: 12px;
  }
  
  .results-statistics {
    flex-direction: column;
    gap: 15px;
    align-items: center;
  }
  
  .results-statistics .stat-item {
    width: 80%;
  }
  
  .game-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .action-button {
    width: 100%;
    max-width: 300px;
  }
}

@media (max-width: 480px) {
  .level-indicator {
    flex-direction: column;
    gap: 10px;
    align-items: center;
  }
  
  .stats-container {
    flex-direction: column;
    gap: 10px;
    align-items: center;
  }
  
  .stat-item {
    width: 80%;
  }
  
  .progress-steps {
    display: none;
  }
  
  .guide-character {
    flex-direction: column;
    text-align: center;
  }
  
  .speech-bubble {
    margin-left: 0;
    margin-top: 15px;
    max-width: 100%;
  }
  
  .speech-bubble:before {
    display: none;
  }
}
</style>