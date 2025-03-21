<template>
    <div class="game-container" :class="{ 'high-contrast-mode': highContrastMode }">
      <div class="game-header">
        <!-- Barre de progression -->
        <div class="progress-bar">
          <div class="progress-step" :class="{ 'completed': phase !== 'intro' }">
            <div class="step-icon">📖</div>
            <div class="step-label">Introduction</div>
          </div>
          <div class="progress-connector"></div>
          <div class="progress-step" :class="{ 'completed': phase === 'choix' || feedback }">
            <div class="step-icon">💬</div>
            <div class="step-label">Dialogue</div>
          </div>
          <div class="progress-connector"></div>
          <div class="progress-step" :class="{ 'completed': feedback }">
            <div class="step-icon">🤔</div>
            <div class="step-label">Décision</div>
          </div>
        </div>
        
        <!-- Titre du scénario -->
        <h1 v-if="scenario" class="scenario-title">
          <span class="title-decoration">★</span>
          {{ scenario.titre }}
          <span class="title-decoration">★</span>
        </h1>
      </div>
  
      <div v-if="scenario" class="game-content">
        <!-- Panneau d'introduction -->
        <div v-if="phase === 'intro'" class="intro-panel">
          <div class="story-card">
            <div class="story-header">La situation</div>
            <p class="story-text">{{ scenario.contexteIntro }}</p>
            <button @click="startDialogue" class="action-button start-button">
              <span class="button-icon">▶️</span>
              <span class="button-text">Commencer</span>
            </button>
          </div>
          
          <!-- Illustration -->
          <div class="scene-illustration">
            <img :src="getSceneImage()" alt="Illustration de la scène" class="scene-image" />
          </div>
        </div>
  
        <!-- Zone de dialogue -->
        <div v-else class="dialogue-zone">
          <!-- Bulle de narration pour guider -->
          <div v-if="dialogueIndex === 0 && phase === 'dialogue'" class="narrator-bubble">
            <p>Observe la conversation et décide comment tu réagirais...</p>
          </div>
          
          <!-- Bulles de dialogue -->
          <transition-group name="dialogue-appear" tag="div" class="dialogue-container">
            <div v-for="(dialogue, index) in visibleDialogues" :key="index" class="dialogue"
              :class="getDialogueClass(dialogue.personnage)">
              <div class="character-avatar">
                <img :src="getAvatarPath(dialogue.avatar)" :alt="dialogue.personnage" />
                <div class="character-name">{{ dialogue.personnage }}</div>
              </div>
              <div class="speech-bubble">
                <p>{{ dialogue.texte }}</p>
              </div>
            </div>
          </transition-group>
  
          <!-- Bouton pour avancer dans le dialogue -->
          <button v-if="dialogueIndex < scenario.contexte.length - 1 && phase === 'dialogue'" 
                  @click="showNextDialogue" 
                  class="action-button next-button">
            <span class="button-text">Suivant</span>
            <span class="button-icon">👉</span>
          </button>
  
          <!-- Question et choix -->
          <div v-if="phase === 'choix'" class="choice-panel">
            <div class="question-box">
              <h2 class="question-text">{{ scenario.question }}</h2>
            </div>
            
            <div class="choices-container">
              <button 
                v-for="(reponse, index) in scenario.reponses" 
                :key="index" 
                @click="choisirReponse(reponse)"
                class="choice-button"
                :class="{ 'selected': selectedChoice === index }"
                :style="{ '--delay': index * 0.2 + 's' }">
                {{ reponse.texte }}
              </button>
            </div>
          </div>
  
          <!-- Feedback après la sélection -->
          <div v-if="feedback" class="feedback-panel">
            <div class="feedback-content">
              <div class="feedback-icon">✅</div>
              <p class="feedback-message">{{ feedback }}</p>
              <div class="feedback-animation"></div>
            </div>
            
            <!-- <div class="skills-gained">
              <h3>Super-pouvoirs gagnés !</h3>
              <div v-if="lastChoiceSkills.length > 0" class="skills-list">
                <div v-for="(skill, index) in lastChoiceSkills" :key="index" class="skill-item"
                     :style="{ '--index': index }">
                  <div class="skill-icon">{{ getSkillIcon(skill.name) }}</div>
                  <div class="skill-info">
                    <div class="skill-name">{{ getSkillDisplayName(skill.name) }}</div>
                    <div class="skill-points" :class="{ 'negative': skill.value < 0 }">
                      {{ skill.value > 0 ? '+' : '' }}{{ skill.value }} points
                    </div>
                  </div>
                </div>
              </div>
              <p v-else class="no-skills">Pas de super-pouvoirs gagnés cette fois...</p>
            </div> -->
          </div>
        </div>
      </div>
      
      <!-- Contrôles d'accessibilité -->
      <div class="accessibility-controls">
        <button @click="toggleSound" class="accessibility-button">
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
  
      <!-- Message de chargement -->
      <div v-if="!scenario" class="loading-container">
        <div class="loading-animation"></div>
        <p>Chargement de l'aventure...</p>
      </div>
    </div>
  </template>
  
  <script>
  import { scenarios } from '@/data/data.js';
  const avatars = require.context('@/assets/avatars/', false, /\.png$/);
  
  export default {
    name: "ScenarioPage",
    props: {
      id: String,
    },
    data() {
      return {
        scenario: null,
        feedback: null,
        phase: 'intro',
        dialogueIndex: 0,
        selectedChoice: null,
        lastChoiceSkills: [],
        soundEnabled: true,
        highContrastMode: false,
        textSizeLevel: 0, // 0 = normal, -1 = small, 1 = large
        completedScenarios: []
      };
    },
    computed: {
      visibleDialogues() {
        return this.scenario ? this.scenario.contexte.slice(0, this.dialogueIndex + 1) : [];
      }
    },
    created() {
      this.loadProgress();
      this.loadScenario();
      this.loadAccessibilitySettings();
    },
    mounted() {
      // Ajouter un écouteur d'événement pour la navigation (quand on quitte le composant)
      window.addEventListener('beforeunload', this.stopSpeech);
    },
    beforeUnmount() {
      // S'assurer que la synthèse vocale est arrêtée quand le composant est détruit
      this.stopSpeech();
      // Supprimer l'écouteur d'événement
      window.removeEventListener('beforeunload', this.stopSpeech);
    },
    watch: {
      $route(to, from) {
        if (to.params.id !== from.params.id) {
          this.stopSpeech();
          this.loadScenario();
          this.phase = 'intro';
          this.feedback = null;
          this.dialogueIndex = 0;
          this.selectedChoice = null;
          this.lastChoiceSkills = [];
        }
      },
      highContrastMode() {
        this.saveAccessibilitySettings();
      },
      textSizeLevel() {
        this.saveAccessibilitySettings();
        this.applyTextSize();
      },
      soundEnabled() {
        this.saveAccessibilitySettings();
        if (!this.soundEnabled) {
          this.stopSpeech();
        }
      }
    },
    methods: {
      loadProgress() {
        const completedIds = localStorage.getItem('completedScenarios');
        if (completedIds) {
          this.completedScenarios = JSON.parse(completedIds).map(id => parseInt(id));
        }
      },
      
      loadAccessibilitySettings() {
        const settings = localStorage.getItem('accessibilitySettings');
        if (settings) {
          const { soundEnabled, highContrastMode, textSizeLevel } = JSON.parse(settings);
          this.soundEnabled = soundEnabled;
          this.highContrastMode = highContrastMode;
          this.textSizeLevel = textSizeLevel;
          this.applyTextSize();
        }
      },
      
      saveAccessibilitySettings() {
        const settings = {
          soundEnabled: this.soundEnabled,
          highContrastMode: this.highContrastMode,
          textSizeLevel: this.textSizeLevel
        };
        localStorage.setItem('accessibilitySettings', JSON.stringify(settings));
      },
      
      applyTextSize() {
        const container = document.querySelector('.game-container');
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
      
      toggleSound() {
        this.soundEnabled = !this.soundEnabled;
      },
      
      toggleHighContrast() {
        this.highContrastMode = !this.highContrastMode;
      },
      
      increaseTextSize() {
        if (this.textSizeLevel < 1) {
          this.textSizeLevel++;
        }
      },
      
      decreaseTextSize() {
        if (this.textSizeLevel > -1) {
          this.textSizeLevel--;
        }
      },
      
      loadScenario() {
        const scenarioId = parseInt(this.id);
        console.log("Chargement du scénario ID:", scenarioId);
        this.scenario = scenarios.find(s => s.id === scenarioId);
        
        if (!this.scenario) {
          console.error("Scénario non trouvé !");
        } else {
          if (this.soundEnabled) {
            this.readAloud(this.scenario.contexteIntro);
          }
          console.log("Scénario chargé:", this.scenario);
          console.log("Réponses disponibles:", this.scenario.reponses);
          
          // Effet d'apparition progressive du texte
          this.animateText();
        }
      },
      
      animateText() {
        // Animation de texte qui apparaît progressivement (pourrait être implémentée avec JavaScript)
        // Cette fonction est un placeholder pour une future animation
      },
      
      startDialogue() {
        this.phase = 'dialogue';
        this.dialogueIndex = 0;
        
        this.playSound('button');
        
        if (this.scenario.contexte.length > 0 && this.soundEnabled) {
          this.readAloud(this.scenario.contexte[0].texte);
        }
      },
      
      showNextDialogue() {
        console.log("showNextDialogue appelée");
        console.log("dialogueIndex:", this.dialogueIndex);
        console.log("Longueur contexte:", this.scenario.contexte.length);
        this.playSound('next');
        
        if (this.dialogueIndex < this.scenario.contexte.length - 1) {
          this.dialogueIndex++;
          
          if (this.soundEnabled) {
            this.readAloud(this.scenario.contexte[this.dialogueIndex].texte);
          }
        } else {
          this.phase = 'choix';
          
          if (this.soundEnabled) {
            this.readAloud(this.scenario.question);
          }
        }
        if (this.dialogueIndex >= this.scenario.contexte.length - 1) {
          console.log("Passage à la phase choix");
          this.phase = 'choix';
          
          console.log("Phase actuelle:", this.phase);
          console.log("Réponses disponibles:", this.scenario.reponses);
        }
      },
      
      choisirReponse(reponse) {
        this.selectedChoice = this.scenario.reponses.indexOf(reponse);
        this.feedback = `Tu as choisi : "${reponse.texte}"`;
        
        this.playSound('choice');
        
        if (this.soundEnabled) {
          this.readAloud(`Tu as choisi : ${reponse.texte}`);
        }
        
        // Extraire et afficher les compétences gagnées
        this.lastChoiceSkills = this.extractSkills(reponse);
        
        // Enregistrer les compétences
        this.enregistrerSoftSkills(reponse);
        
        // Marquer ce scénario comme complété
        this.markScenarioCompleted();
        
        // Navigation au scénario suivant ou à la page de résultats
        setTimeout(() => {
          this.stopSpeech();
          const nextId = parseInt(this.id) + 1;
          
          if (scenarios.some(s => s.id === nextId)) {
            this.$router.push({ name: "ScenarioPage", params: { id: nextId } });
          } else {
            this.$router.push({ name: "ResultsPage" });
          }
        }, 6000); // Temps plus long pour voir les animations et les compétences gagnées
      },
      
      markScenarioCompleted() {
        const currentId = parseInt(this.id);
        
        if (!this.completedScenarios.includes(currentId)) {
          this.completedScenarios.push(currentId);
          localStorage.setItem('completedScenarios', JSON.stringify(this.completedScenarios));
        }
      },
      
      extractSkills(reponse) {
        const skills = [];
        
        // Extraire les compétences positives
        if (reponse.skills) {
          Object.entries(reponse.skills).forEach(([name, value]) => {
            skills.push({ name, value, type: 'positive' });
          });
        }
        
        // Extraire les pénalités (compétences négatives)
        if (reponse.penalties) {
          Object.entries(reponse.penalties).forEach(([name, value]) => {
            skills.push({ name, value: -value, type: 'negative' });
          });
        }
        
        // Trier par valeur (du plus grand au plus petit)
        return skills.sort((a, b) => Math.abs(b.value) - Math.abs(a.value));
      },
      
      readAloud(text) {
        if ('speechSynthesis' in window && this.soundEnabled) {
          // Arrêter toute synthèse vocale en cours
          this.stopSpeech();
          
          const utterance = new SpeechSynthesisUtterance(text);
          utterance.lang = 'fr-FR';
          utterance.rate = 1;
          utterance.pitch = 1;
          window.speechSynthesis.speak(utterance);
        }
      },
      
      stopSpeech() {
        if ('speechSynthesis' in window) {
          window.speechSynthesis.cancel();
        }
      },
      
      playSound(type) {
        // Cette fonction pourrait jouer différents sons selon le type d'action
        // Par exemple: 'button', 'next', 'choice', 'success'
        if (!this.soundEnabled) return;
        
        // Implémentation de base avec l'API Audio
        // Pour une implémentation complète, il faudrait ajouter les fichiers audio
        const sounds = {
          button: 'button_click.mp3',
          next: 'next_dialog.mp3',
          choice: 'choice_made.mp3',
          success: 'success.mp3'
        };
        
        console.log(`Le son "${sounds[type]}" serait joué pour l'action "${type}"`);
        // Si vous avez les fichiers audio, décommentez ce code
        /*
        try {
          const sound = new Audio(require(`@/assets/sounds/${sounds[type]}`));
          sound.play();
        } catch (e) {
          console.log('Son non disponible:', e);
        }
        */
      },
      
      enregistrerSoftSkills(reponse) {
        // Récupérer les compétences déjà enregistrées ou initialiser un objet vide
        const savedSkills = JSON.parse(localStorage.getItem('userSoftSkills')) || {};
        
        // Traiter les compétences positives
        if (reponse.skills) {
          for (const [skill, points] of Object.entries(reponse.skills)) {
            savedSkills[skill] = (savedSkills[skill] || 0) + points;
          }
        }
        
        // Traiter les pénalités (compétences négatives)
        if (reponse.penalties) {
          for (const [skill, points] of Object.entries(reponse.penalties)) {
            savedSkills[skill] = (savedSkills[skill] || 0) - points;
            // Éviter les scores négatifs
            if (savedSkills[skill] < 0) savedSkills[skill] = 0;
          }
        }
        
        // Sauvegarder les compétences mises à jour
        localStorage.setItem('userSoftSkills', JSON.stringify(savedSkills));
      },
      
      getAvatarPath(filename) {
        if (!filename) return require('@/assets/avatars/toi.png');
        
        const path = `./${filename}`;
        try {
          return avatars(path);
        } catch {
          return require('@/assets/avatars/toi.png');
        }
      },
      
      getDialogueClass(personnage) {
        return personnage === "Toi" ? "dialogue-right" : "dialogue-left";
      },
      
      getSceneImage() {
        // Idéalement, vous auriez des images spécifiques pour chaque scénario
        // Voici quelques exemples de correspondance scénario-image
        const sceneImages = {
          1: require('@/assets/avatars/personne_agee.png'), // exemple
          2: require('@/assets/avatars/femme-caissiere.png'), // exemple
          // Ajoutez d'autres correspondances selon vos scénarios
        };
        
        const scenarioId = parseInt(this.id);
        return sceneImages[scenarioId] || require('@/assets/avatars/toi.png');
      },
      
      getSkillIcon(skillName) {
        // Association d'emojis aux compétences
        const skillIcons = {
          assertivite: '🗣️',
          communication: '💬',
          empathie: '❤️',
          espritEquipe: '👥',
          initiative: '🚀',
          adaptabilite: '🔄',
          responsabilite: '🛡️',
          creativite: '💡',
          observation: '👁️',
          diplomatie: '🤝',
          patience: '⏳',
          confianceEnSoi: '💪',
          inclusion: '🌈',
          mediation: '☮️',
          coaching: '📚',
          ecouteActive: '👂',
          soutien: '🤲',
          reflexionRapide: '⚡',
          negociation: '🔍',
          gestionStress: '😌',
          anticipation: '🔮',
          apprentissage: '🧠'
        };
        
        return skillIcons[skillName] || '✨';
      },
      
      getSkillDisplayName(skillName) {
        // Noms des compétences formatés pour l'affichage
        const skillNames = {
          assertivite: "Assertivité",
          communication: "Communication",
          empathie: "Empathie",
          espritEquipe: "Esprit d'équipe",
          initiative: "Initiative",
          adaptabilite: "Adaptabilité",
          responsabilite: "Responsabilité",
          creativite: "Créativité",
          observation: "Observation",
          diplomatie: "Diplomatie",
          patience: "Patience",
          confianceEnSoi: "Confiance en soi",
          inclusion: "Inclusion",
          mediation: "Médiation",
          coaching: "Coaching",
          ecouteActive: "Écoute active",
          soutien: "Soutien",
          reflexionRapide: "Réflexion rapide",
          negociation: "Négociation",
          gestionStress: "Gestion du stress",
          anticipation: "Anticipation",
          apprentissage: "Apprentissage"
        };
        
        return skillNames[skillName] || skillName;
      }
    }
  };
  </script>
  
  <style scoped>
  /* Container principal */
  .game-container {
    font-family: 'Comic Sans MS', 'Chalkboard SE', 'Marker Felt', sans-serif;
    max-width: 900px;
    margin: 20px auto;
    padding: 20px;
    background-color: #f8f9fa;
    border-radius: 20px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    position: relative;
    overflow: hidden;
  }
  
  /* Adaptation mode contraste élevé */
  .game-container.high-contrast-mode {
    background-color: #000;
    color: #fff;
  }
  
  /* Adaptations de taille de texte */
  .game-container.text-small {
    font-size: 0.9em;
  }
  
  .game-container.text-large {
    font-size: 1.2em;
  }
  
  /* En-tête du jeu */
  .game-header {
    margin-bottom: 20px;
    padding-top: 40px; /* Ajouter un espace en haut du header pour les contrôles d'accessibilité */
    position: relative;
  }
  
  /* Barre de progression */
  .progress-bar {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 15px;
    margin-top: 10px;
    position: relative;
    z-index: 50; /* Z-index inférieur aux contrôles d'accessibilité */
  }
  
  .progress-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    width: 80px;
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
    z-index: 2;
  }
  
  .step-label {
    font-size: 0.8rem;
    color: #6c757d;
  }
  
  .progress-connector {
    height: 2px;
    background-color: #ced4da;
    flex-grow: 1;
    margin: 0 -10px;
    position: relative;
    top: -20px;
    z-index: 1;
  }
  
  .progress-step.completed .step-icon {
    background-color: #4CAF50;
    color: white;
    border-color: #4CAF50;
  }
  
  .progress-step.completed .step-label {
    color: #4CAF50;
    font-weight: bold;
  }
  
  /* Titre du scénario */
  .scenario-title {
    text-align: center;
    font-size: 2rem;
    color: #2C3E50;
    margin: 15px 0;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
  }
  
  .title-decoration {
    color: #FFD700;
    margin: 0 10px;
  }
  
  /* Contenu du jeu */
  .game-content {
    background-color: white;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
    position: relative;
  }
  
  .intro-panel {
    display: flex;
    flex-direction: column;
    padding: 20px;
  }

  /* Ajoutez cette règle ou modifiez-la si elle existe déjà */
  .story-card {
    display: flex;
    flex-direction: column;
    background-color: #f8f9fa;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
    position: relative;
    overflow: hidden;
  }
  
  .story-header {
    font-size: 1.3rem;
    font-weight: bold;
    color: #495057;
    margin-bottom: 15px;
    text-align: center;
  }
  
  .story-text {
    font-size: 1.1rem;
    line-height: 1.6;
    color: #343a40;
    margin-bottom: 20px;
    position: relative;
    z-index: 2;
  }
  
  .scene-illustration {
    display: flex;
    justify-content: center;
    margin-top: 10px;
  }

  .scene-image {
    max-width: 100%;
    max-height: 250px;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }
  
  /* Zone de dialogue */
  .dialogue-zone {
    padding: 20px;
    position: relative;
  }
  
  .narrator-bubble {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 10px 15px;
    margin-bottom: 15px;
    text-align: center;
    border-left: 4px solid #6c757d;
    font-style: italic;
    color: #495057;
    animation: fadeIn 0.5s ease-out;
  }
  
  .dialogue-container {
    min-height: 250px;
    position: relative;
  }
  
  .dialogue {
    display: flex;
    margin-bottom: 20px;
    align-items: flex-start;
    animation: slideIn 0.5s ease-out;
  }
  
  .dialogue-left {
    align-self: flex-start;
  }
  
  .dialogue-right {
    flex-direction: row-reverse;
    align-self: flex-end;
  }
  
  .character-avatar {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 0 10px;
  }
  
  .character-avatar img {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid #f8f9fa;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
  }
  
  .character-name {
    font-size: 0.8rem;
    margin-top: 5px;
    text-align: center;
    color: #6c757d;
    max-width: 80px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .speech-bubble {
    position: relative;
    background-color: #e9f5ff;
    border-radius: 15px;
    padding: 12px 15px;
    max-width: 70%;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  }
  
  .dialogue-right .speech-bubble {
    background-color: #e6f7e6;
  }
  
  .speech-bubble:before {
    content: '';
    position: absolute;
    top: 20px;
    width: 0;
    height: 0;
    border: 10px solid transparent;
  }
  
  .dialogue-left .speech-bubble:before {
    left: -20px;
    border-right-color: #e9f5ff;
  }
  
  .dialogue-right .speech-bubble:before {
    right: -20px;
    border-left-color: #e6f7e6;
  }
  
  .speech-bubble p {
    margin: 0;
    font-size: 1rem;
    line-height: 1.5;
    color: #343a40;
  }
  
  /* Animations de dialogue */
  .dialogue-appear-enter-active {
    transition: all 0.5s ease;
  }
  
  .dialogue-appear-enter-from {
    opacity: 0;
    transform: translateY(20px);
  }
  
  /* Bouton d'action */
  .action-button {
    display: inline-flex; /* Changez flex à inline-flex */
    align-items: center;
    justify-content: center;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 50px;
    padding: 10px 20px;
    font-size: 1.1rem;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
    margin: 15px auto;
    width: auto;
    height: auto;
  }
  
  .action-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
  }
  
  .action-button:active {
    transform: translateY(1px);
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
  }
  
  .button-icon {
    margin: 0 8px;
  }
  
  .start-button {
    background-color: #28a745;
  }
  
  .next-button {
    background-color: #17a2b8;
  }
  
  /* Panneau de choix */
  .choice-panel {
    margin-top: 20px;
  }
  
  .question-box {
    background-color: #f8f9fa;
    border-left: 5px solid #6c757d;
    padding: 15px;
    margin-bottom: 20px;
    border-radius: 8px;
  }
  
  .question-text {
    font-size: 1.2rem;
    font-weight: bold;
    color: #343a40;
    margin: 0;
  }

  .choices-container {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .choice-button {
    background-color: #f8f9fa;
    border: 2px solid #dee2e6;
    border-radius: 12px;
    padding: 15px;
    text-align: left;
    font-size: 1rem;
    color: #495057;
    cursor: pointer;
    transition: all 0.3s ease;
    animation: fadeIn 0.5s ease-out forwards;
    animation-delay: var(--delay);
    opacity: 0;
    position: relative;
    overflow: hidden;
  }

  .choice-button:hover {
    border-color: #007bff;
    background-color: #f0f7ff;
    transform: translateX(5px);
  }

  .choice-button:active {
    transform: translateX(2px);
  }

  .choice-button.selected {
    border-color: #28a745;
    background-color: #e6f7e6;
    pointer-events: none;
  }

  .choice-button.selected:after {
    content: '✓';
    position: absolute;
    right: 15px;
    top: 50%;
    transform: translateY(-50%);
    color: #28a745;
    font-weight: bold;
  }

  /* Panneau de feedback */
  .feedback-panel {
    margin-top: 20px;
    animation: fadeIn 0.5s ease-out;
  }

  .feedback-content {
    background-color: #e6f7e6;
    border-radius: 12px;
    padding: 15px;
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    position: relative;
  }

  .feedback-icon {
    font-size: 2rem;
    margin-right: 15px;
    color: #28a745;
  }

  .feedback-message {
    font-size: 1.1rem;
    color: #343a40;
    flex-grow: 1;
    margin: 0;
  }

  .feedback-animation {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    pointer-events: none;
    z-index: 10;
  }

  /* Compétences gagnées */
  .skills-gained {
    background-color: #f8f9fa;
    border-radius: 12px;
    padding: 15px;
    margin-top: 15px;
  }

  .skills-gained h3 {
    text-align: center;
    color: #495057;
    margin-top: 0;
    margin-bottom: 15px;
    font-size: 1.2rem;
  }

  .skills-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .skill-item {
    display: flex;
    align-items: center;
    background-color: white;
    border-radius: 8px;
    padding: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    animation: slideUp 0.5s ease-out forwards;
    animation-delay: calc(var(--index) * 0.2s);
    opacity: 0;
    transform: translateY(20px);
  }

  .skill-icon {
    font-size: 1.5rem;
    margin-right: 12px;
    width: 40px;
    height: 40px;
    background-color: #f0f7ff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .skill-info {
    flex-grow: 1;
  }

  .skill-name {
    font-weight: bold;
    color: #343a40;
    margin-bottom: 2px;
  }

  .skill-points {
    font-size: 0.9rem;
    color: #28a745;
  }

  .skill-points.negative {
    color: #dc3545;
  }

  .no-skills {
    text-align: center;
    color: #6c757d;
    font-style: italic;
  }

  /* Contrôles d'accessibilité */
  .accessibility-controls {
    position: absolute;
    top: 0px;
    right: 10px;
    display: flex;
    gap: 5px;
    z-index: 100;
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

  /* Animation de chargement */
  .loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 300px;
  }

  .loading-animation {
    width: 50px;
    height: 50px;
    border: 5px solid #f3f3f3;
    border-top: 5px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 15px;
  }

  /* Animations */
  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  /* Styles pour le mode contraste élevé */
  .high-contrast-mode .game-content {
    background-color: #222;
    border: 1px solid #fff;
  }

  .high-contrast-mode .story-card,
  .high-contrast-mode .narrator-bubble,
  .high-contrast-mode .question-box,
  .high-contrast-mode .skills-gained {
    background-color: #333;
    color: #fff;
  }

  .high-contrast-mode .speech-bubble {
    background-color: #444;
    color: #fff;
  }

  .high-contrast-mode .speech-bubble:before {
    border-right-color: #444;
    border-left-color: #444;
  }

  .high-contrast-mode .choice-button {
    background-color: #333;
    border-color: #666;
    color: #fff;
  }

  .high-contrast-mode .choice-button:hover {
    border-color: #fff;
    background-color: #444;
  }

  .high-contrast-mode .choice-button.selected {
    border-color: #fff;
    background-color: #444;
  }

  /* Responsive design */
  @media (max-width: 768px) {
    .game-container {
      margin: 10px;
      padding: 15px;
    }
    
    .scenario-title {
      font-size: 1.5rem;
    }
    
    .story-text {
      font-size: 1rem;
    }
    
    .dialogue {
      margin-bottom: 10px;
    }
    
    .character-avatar img {
      width: 50px;
      height: 50px;
    }
    
    .speech-bubble {
      max-width: 85%;
    }
    
    .choice-button {
      padding: 12px;
    }
    
    .progress-bar {
      flex-wrap: wrap;
      justify-content: space-around;
    }
    
    .progress-connector {
      display: none;
    }
    
    .progress-step {
      margin: 5px;
    }
  }

  /* Tailles de texte différentes pour accessibilité */
  .text-small .story-text,
  .text-small .speech-bubble p,
  .text-small .question-text,
  .text-small .choice-button,
  .text-small .feedback-message {
    font-size: 0.9rem;
  }

  .text-large .story-text,
  .text-large .speech-bubble p,
  .text-large .question-text,
  .text-large .choice-button,
  .text-large .feedback-message {
    font-size: 1.2rem;
  }
</style>
