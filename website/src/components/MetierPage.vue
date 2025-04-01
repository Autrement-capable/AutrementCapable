<template>
  <div class="metier-container" :class="{ expanded: isExpanded, 'high-contrast-mode': highContrastMode }">
      <!-- En-tête avec personnage guide -->
      <div class="guide-character">
          <img src="@/assets/avatars/guide.png" alt="Guide" class="guide-avatar" />
          <div class="speech-bubble">
              <p v-if="!isExpanded">Découvre ce métier et ses spécificités. N'hésite pas à en savoir plus !</p>
              <p v-else>Tu peux maintenant explorer toutes les informations sur ce métier.</p>
          </div>
      </div>

      <div class="metier-header">
          <h1 class="metier-title">
              <span class="title-decoration">★</span>
              {{ metierName }}
              <span class="title-decoration">★</span>
          </h1>
      </div>

      <div class="video-container">
          <video controls :poster="posterSrc">
              <source :src="videoSrc" type="video/mp4" />
              Votre navigateur ne supporte pas la vidéo.
          </video>
          <button @click="toggleExpand" class="action-button expand-button">
              <span class="button-icon">{{ isExpanded ? "📁" : "📂" }}</span>
              <span class="button-text">{{ isExpanded ? "Afficher moins" : "En savoir plus" }}</span>
          </button>
      </div>

      <div class="description-card">
          <p class="description-text">{{ description }}</p>
      </div>

      <div v-if="isExpanded" class="additional-info">
          <div class="info-section skills-section">
              <h2 class="section-title">Compétences requises</h2>
              <ul class="skills-list">
                  <li v-for="(skill, index) in skills" :key="index" class="skill-item">
                      <div class="skill-icon">💪</div>
                      <div class="skill-text">{{ skill }}</div>
                  </li>
              </ul>
          </div>

          <div class="info-section environment-section">
              <h2 class="section-title">Environnement de travail</h2>
              <div class="environment-card">
                  <p>{{ workEnvironment }}</p>
              </div>
          </div>

          <div class="info-section job-details-section">
              <h2 class="section-title">Détails du métier</h2>
              <div class="job-details-card" v-html="jobDetails"></div>
          </div>
      </div>

      <div class="button-container">
          <button @click="onLike" class="action-button like-button">
              <span class="button-icon">👍</span>
              <span class="button-text">J'aime</span>
          </button>
          <button @click="onNeutral" class="action-button neutral-button">
              <span class="button-icon">🤔</span>
              <span class="button-text">Je ne sais pas</span>
          </button>
          <button @click="onDislike" class="action-button dislike-button">
              <span class="button-icon">👎</span>
              <span class="button-text">Je n'aime pas</span>
          </button>
      </div>

      <!-- Contrôles d'accessibilité -->
      <div class="accessibility-controls">
          <button @click="toggleSound" class="accessibility-button" aria-label="Activer/désactiver le son">
              <span v-if="soundEnabled">🔊</span>
              <span v-else>🔇</span>
          </button>
          <button @click="toggleHighContrast" class="accessibility-button">
              <span v-if="highContrastMode">🌓</span>
              <span v-else>🌑</span>
          </button>
          <button @click="increaseTextSize" class="accessibility-button">
              A+
          </button>
          <button @click="decreaseTextSize" class="accessibility-button">
              A-
          </button>
      </div>
  </div>
  <div v-if="isExpanded" class="extra-space"></div>
</template>

<script>
export default {
  name: "MetierPage",
  props: {
      metierName: { type: String, required: true },
      description: { type: String, required: true },
      videoSrc: { type: String, required: true },
      posterSrc: { type: String, required: true },
      skills: { type: Array, required: true },
      workEnvironment: { type: String, required: true },
      jobDetails: { type: String, required: true },
      nextRoute: { type: String, default: null },
  },
  data() {
      return {
          isExpanded: false,
          highContrastMode: false,
          textSizeLevel: 0, // 0 = normal, -1 = small, 1 = large
          soundEnabled: true, // Son activé par défaut
          isReading: false,
          speechUtterance: null
      };
  },
  watch: {
      // Observer les changements des propriétés pour mettre à jour la lecture
      metierName() {
          // Si le métier change, arrêter la lecture en cours
          this.stopReading();
          
          // Si la page est développée et le son activé, lancer la lecture du nouveau métier
          if (this.isExpanded && this.soundEnabled) {
              // Petit délai pour s'assurer que les nouvelles données sont bien chargées
              setTimeout(() => {
                  this.readDescriptionAloud();
              }, 300);
          }
      }
  },
  mounted() {
      this.loadAccessibilitySettings();
      
      // Initialiser les voix de synthèse vocale
      if ('speechSynthesis' in window) {
          // Certains navigateurs chargent les voix de manière asynchrone
          if (window.speechSynthesis.getVoices().length === 0) {
              window.speechSynthesis.onvoiceschanged = () => {
                  window.speechSynthesis.getVoices();
              };
          }
      }
      
      // Si la page est déjà développée (par exemple, après navigation), lancer la lecture
      if (this.isExpanded && this.soundEnabled) {
          // Petit délai pour s'assurer que le composant est complètement monté
          setTimeout(() => {
              this.readDescriptionAloud();
          }, 300);
      }
  },
  beforeUnmount() {
      // S'assurer que la lecture est arrêtée lors de la destruction du composant
      this.stopReading();
  },
  methods: {
      toggleExpand() {
          this.isExpanded = !this.isExpanded;
          
          if (this.isExpanded) {
              // Commencer la lecture si le son est activé
              if (this.soundEnabled) {
                  this.readDescriptionAloud();
              }
          } else {
              // Arrêter la lecture si on réduit la vue
              this.stopReading();
              // Faire défiler vers le haut
              window.scrollTo({ top: 0, behavior: 'smooth' });
          }
      },
      navigateToNextMetier() {
          if (this.nextRoute) {
              this.stopReading();
              this.$router.push({ name: this.nextRoute });
          }
      },
      onLike() {
          console.log("User likes this métier!");
          this.navigateToNextMetier();
      },
      onNeutral() {
          console.log("User is neutral about this métier.");
          this.navigateToNextMetier();
      },
      onDislike() {
          console.log("User dislikes this métier.");
          this.navigateToNextMetier();
      },
      // Fonctions d'accessibilité
      toggleHighContrast() {
          this.highContrastMode = !this.highContrastMode;
          this.saveAccessibilitySettings();
      },
      increaseTextSize() {
          if (this.textSizeLevel < 1) {
              this.textSizeLevel++;
              this.applyTextSize();
              this.saveAccessibilitySettings();
          }
      },
      decreaseTextSize() {
          if (this.textSizeLevel > -1) {
              this.textSizeLevel--;
              this.applyTextSize();
              this.saveAccessibilitySettings();
          }
      },
      applyTextSize() {
          const container = document.querySelector('.metier-container');
          if (!container) return;
          
          // Supprimer les classes de taille précédentes
          container.classList.remove('text-small', 'text-large');
          
          // Ajouter la classe appropriée
          if (this.textSizeLevel === -1) {
              container.classList.add('text-small');
          } else if (this.textSizeLevel === 1) {
              container.classList.add('text-large');
          }
      },
      loadAccessibilitySettings() {
          const settings = localStorage.getItem('metierAccessibilitySettings');
          if (settings) {
              const { highContrastMode, textSizeLevel, soundEnabled } = JSON.parse(settings);
              this.highContrastMode = highContrastMode;
              this.textSizeLevel = textSizeLevel;
              if (soundEnabled !== undefined) {
                  this.soundEnabled = soundEnabled;
              }
              this.applyTextSize();
          }
      },
      saveAccessibilitySettings() {
          const settings = {
              highContrastMode: this.highContrastMode,
              textSizeLevel: this.textSizeLevel,
              soundEnabled: this.soundEnabled
          };
          localStorage.setItem('metierAccessibilitySettings', JSON.stringify(settings));
      },
      // Fonctions de gestion du son
      toggleSound() {
          this.soundEnabled = !this.soundEnabled;
          this.saveAccessibilitySettings();
          
          if (!this.soundEnabled) {
              this.stopReading();
          } else if (this.isExpanded) {
              // Si le son est activé et que la page est développée, commencer la lecture
              this.readDescriptionAloud();
          }
      },
      // Fonctions de lecture audio
      readDescriptionAloud() {
          if (!('speechSynthesis' in window) || !this.soundEnabled) {
              return;
          }
          
          // Arrêter toute lecture en cours
          this.stopReading();
          
          // Récupérer les textes à lire
          const detailsTexts = [];
          
          // Titre du métier
          detailsTexts.push(`Métier: ${this.metierName}`);
          
          // Description principale
          detailsTexts.push(this.description);
          
          // Informations supplémentaires si la vue est développée
          if (this.isExpanded) {
              // Compétences requises
              detailsTexts.push(`Compétences requises: ${this.skills.join(', ')}`);
              
              // Environnement de travail
              detailsTexts.push(`Environnement de travail: ${this.workEnvironment}`);
              
              // Détails du métier (nettoyer le HTML)
              const tempDiv = document.createElement('div');
              tempDiv.innerHTML = this.jobDetails;
              detailsTexts.push(`Détails du métier: ${tempDiv.textContent}`);
          }
          
          // Joindre tous les textes avec des pauses
          const textToRead = detailsTexts.join('. ');
          
          // Créer une nouvelle instance de synthèse vocale
          this.speechUtterance = new SpeechSynthesisUtterance(textToRead);
          this.speechUtterance.lang = 'fr-FR';
          this.speechUtterance.rate = 0.9; // Vitesse légèrement plus lente pour une meilleure compréhension
          
          // Utiliser une voix française si disponible
          const voices = window.speechSynthesis.getVoices();
          const frenchVoice = voices.find(voice => voice.lang.includes('fr'));
          if (frenchVoice) {
              this.speechUtterance.voice = frenchVoice;
          }
          
          // Événements pour suivre l'état de la lecture
          this.speechUtterance.onstart = () => {
              this.isReading = true;
          };
          
          this.speechUtterance.onend = () => {
              this.isReading = false;
          };
          
          this.speechUtterance.onerror = () => {
              this.isReading = false;
          };
          
          // Démarrer la lecture
          window.speechSynthesis.speak(this.speechUtterance);
          this.isReading = true;
      },
      stopReading() {
          if ('speechSynthesis' in window) {
              window.speechSynthesis.cancel();
              this.isReading = false;
          }
      }
  }
};
</script>

<style scoped>
.metier-container {
  font-family: 'Comic Sans MS', 'Chalkboard SE', 'Marker Felt', sans-serif;
  max-width: 1000px; /* Déjà à la taille maximale */
  margin: 20px auto;
  padding: 20px;
  background-color: #f5f8ff;
  border-radius: 20px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: all 0.3s ease;
  overflow: hidden;
}

/* Seulement pour la classe expanded, on ne change pas la taille */
.metier-container.expanded {
  /* Pas de changement de taille */
}

/* Guide character styling - adapté de ScenarioList & SkillsWheelPage */
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
}

/* En-tête du métier */
.metier-header {
  margin-bottom: 20px;
  text-align: center;
}

.metier-title {
  font-size: 2.2rem;
  color: #3f51b5;
  margin: 0;
  position: relative;
  padding-bottom: 10px;
  display: inline-block;
}

.title-decoration {
  color: #FFD700;
  margin: 0 10px;
}

/* Conteneur vidéo */
.video-container {
  margin: 20px auto;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.video-container video {
  width: 90%;
  max-width: 800px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: block;
  margin: 0 auto;
}

/* Carte de description */
.description-card {
  background-color: #fff;
  border-radius: 12px;
  padding: 20px;
  margin: 20px 0;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
}

.description-text {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #333;
  margin: 0;
}

/* Sections d'informations supplémentaires */
.additional-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 30px;
  animation: fadeIn 0.5s ease;
}

.info-section {
  background-color: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
}

.section-title {
  font-size: 1.4rem;
  color: #3f51b5;
  margin-top: 0;
  margin-bottom: 15px;
  text-align: center;
}

/* Section compétences */
.skills-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
  list-style: none;
  padding: 0;
}

.skill-item {
  display: flex;
  align-items: center;
  background-color: #f5f8ff;
  padding: 10px 15px;
  border-radius: 10px;
  transition: transform 0.2s ease;
}

.skill-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.skill-icon {
  margin-right: 10px;
  font-size: 1.2rem;
}

.skill-text {
  font-size: 1rem;
}

/* Section environnement de travail */
.environment-card {
  background-color: #f5f8ff;
  border-radius: 10px;
  padding: 15px;
  margin-top: 10px;
}

/* Section détails du métier */
.job-details-card {
  background-color: #f5f8ff;
  border-radius: 10px;
  padding: 15px;
  margin-top: 10px;
}

/* Conteneur de boutons */
.button-container {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 30px;
  flex-wrap: wrap;
}

/* Boutons d'action */
.action-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 20px;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
  font-family: inherit;
}

.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
}

.button-icon {
  margin-right: 8px;
}

.expand-button {
  background-color: #17a2b8;
  color: white;
  margin-top: 15px;
}

.like-button {
  background-color: #28a745;
  color: white;
}

.neutral-button {
  background-color: #6c757d;
  color: white;
}

.dislike-button {
  background-color: #dc3545;
  color: white;
}

/* Espace supplémentaire */
.extra-space {
  height: 100px;
}

/* Contrôles d'accessibilité */
.accessibility-controls {
  position: absolute;
  top: 15px;
  right: 15px;
  display: flex;
  gap: 5px;
  z-index: 50;
}

.accessibility-button {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  border: none;
  background-color: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}

.accessibility-button:hover {
  background-color: #e9ecef;
  transform: scale(1.1);
}

.accessibility-button.active {
  background-color: #007bff;
  color: white;
}

/* Adaptations de taille de texte */
.metier-container.text-small {
  font-size: 0.9em;
}

.metier-container.text-large {
  font-size: 1.2em;
}

/* Mode contraste élevé */
.high-contrast-mode {
  background-color: #000;
  color: #fff;
}

.high-contrast-mode .description-card,
.high-contrast-mode .info-section,
.high-contrast-mode .skill-item,
.high-contrast-mode .environment-card,
.high-contrast-mode .job-details-card,
.high-contrast-mode .speech-bubble {
  background-color: #222;
  color: #fff;
  border: 1px solid #444;
}

.high-contrast-mode .speech-bubble:before {
  border-right-color: #222;
}

.high-contrast-mode .metier-title,
.high-contrast-mode .section-title {
  color: #fff;
}

.high-contrast-mode video {
  border: 2px solid #fff;
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Responsive design */
@media (max-width: 768px) {
  .metier-container {
      padding: 15px;
  }
  
  .metier-title {
      font-size: 1.8rem;
  }
  
  .description-text {
      font-size: 1rem;
  }
  
  .skills-list {
      grid-template-columns: 1fr 1fr;
  }
  
  .button-container {
      flex-direction: column;
      align-items: center;
  }
  
  .action-button {
      width: 80%;
  }
}

@media (max-width: 480px) {
  .skills-list {
      grid-template-columns: 1fr;
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
  
  .guide-avatar {
      width: 60px;
      height: 60px;
  }
}
</style>