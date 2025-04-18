<template>
  <transition name="avatar-fade">
    <div v-if="showGuide" class="guide-avatar-container" :class="{ 'is-mini': mini }">
      <div class="avatar-wrapper" @click="toggleExpand">
        <img :src="avatarImage" alt="Guide" class="guide-avatar" :class="{ 'pulse': isAnimating }" />
        <div v-if="!expanded && hasUnreadMessage" class="notification-badge">!</div>
      </div>
      
      <transition name="bubble-fade">
        <div v-if="expanded || forceShowMessage" class="speech-bubble" :class="{ 'mini-bubble': mini }">
          <div class="bubble-header">
            <span class="guide-name">{{ guideName }}</span>
          </div>
          
          <div class="bubble-content">
            <p>{{ currentMessage }}</p>
            
            <div v-if="currentOptions.length > 0" class="guide-options">
              <button 
                v-for="(option, index) in currentOptions" 
                :key="index" 
                @click="selectOption(option)" 
                class="option-button"
              >
                {{ option.text }}
              </button>
            </div>
            
            <div v-if="showControls" class="guide-controls">
              <button 
                v-if="hasPrevious" 
                @click="previousMessage" 
                class="control-button previous-button"
              >
                ← Précédent
              </button>
              <button 
                v-if="hasNext" 
                @click="nextMessage" 
                class="control-button next-button"
              >
                Suivant →
              </button>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'GuideAvatar',
  props: {
    guideName: {
      type: String,
      default: 'Leo'
    },
    avatarImage: {
      type: String,
      default: () => require('@/assets/avatars/guide.png')
    },
    context: {
      type: String,
      default: 'dashboard'
    },
    allowClose: {
      type: Boolean,
      default: true
    },
    allowMinimize: {
      type: Boolean,
      default: true
    },
    forcedMessage: {
      type: String,
      default: null
    },
    forcedOptions: {
      type: Array,
      default: () => []
    },
    forceShowMessage: {
      type: Boolean,
      default: false
    },
    showControls: {
      type: Boolean,
      default: true
    },
    autoShowDelay: {
      type: Number,
      default: 1500
    }
  },
  data() {
    return {
      showGuide: false,
      expanded: false,
      messageIndex: 0,
      isAnimating: false,
      mini: false,
      hasUnreadMessage: false,
      intervalId: null,
      // État du parcours utilisateur stocké localement
      userJourney: {
        currentStep: 0,
        completedGames: [],
        visitedScreens: [],
        needsHelp: false
      }
    };
  },
  computed: {
    currentMessage() {
      if (this.forcedMessage) {
        return this.forcedMessage;
      }
      
      const messages = this.getContextMessages();
      return messages[this.messageIndex] || "Je suis là pour t'aider ! Que veux-tu faire ?";
    },
    currentOptions() {
      if (this.forcedOptions && this.forcedOptions.length > 0) {
        return this.forcedOptions;
      }
      
      return this.getContextOptions();
    },
    hasPrevious() {
      if (this.forcedMessage) return false;
      return this.messageIndex > 0;
    },
    hasNext() {
      if (this.forcedMessage) return false;
      const messages = this.getContextMessages();
      return this.messageIndex < messages.length - 1;
    }
  },
  created() {
    // Charger l'état du parcours utilisateur depuis le localStorage
    this.loadUserJourney();
    
    // Afficher l'avatar après un court délai
    setTimeout(() => {
      this.showGuide = true;
      
      // Animer pour attirer l'attention
      this.pulseAnimation();
      
      // Afficher automatiquement le message après un délai défini
      if (this.autoShowDelay > 0) {
        setTimeout(() => {
          this.expanded = true;
          this.hasUnreadMessage = false;
        }, this.autoShowDelay);
      } else {
        this.hasUnreadMessage = true;
      }
    }, 500);
    
    // Démarrer un intervalle pour rappeler occasionnellement à l'utilisateur
    this.startReminderInterval();
  },
  beforeUnmount() {
    // Nettoyer l'intervalle lors de la destruction du composant
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  },
  methods: {
    toggleExpand() {
      this.expanded = !this.expanded;
      if (this.expanded) {
        this.hasUnreadMessage = false;
      }
      // Notifie le parent que l'avatar a été cliqué
      this.$emit('avatar-clicked', this.expanded);
    },
    closeGuide() {
      this.showGuide = false;
      this.$emit('guide-closed');
    },
    minimize() {
      this.mini = true;
      this.expanded = false;
      this.$emit('guide-minimized');
    },
    maximize() {
      this.mini = false;
      this.expanded = true;
      this.$emit('guide-maximized');
    },
    nextMessage() {
      const messages = this.getContextMessages();
      if (this.messageIndex < messages.length - 1) {
        this.messageIndex++;
      }
      this.$emit('message-changed', this.messageIndex);
    },
    previousMessage() {
      if (this.messageIndex > 0) {
        this.messageIndex--;
      }
      this.$emit('message-changed', this.messageIndex);
    },
    selectOption(option) {
      // IMPORTANT: Modification ici pour corriger l'erreur
      // Envoyer l'option sélectionnée au parent au lieu d'exécuter l'action directement
      this.$emit('option-selected', option);
      
      // Gérer les aspects locaux du composant uniquement
      
      // Si l'option a une route, naviguer vers cette route
      if (option.route) {
        this.$router.push(option.route);
      }
      
      // Si l'option a un nouveau message, le définir
      if (option.nextMessage !== undefined) {
        this.messageIndex = option.nextMessage;
      }
      
      // REMARQUE: Nous avons supprimé this[option.action]() car ces méthodes sont dans le parent
    },
    pulseAnimation() {
      this.isAnimating = true;
      setTimeout(() => {
        this.isAnimating = false;
      }, 1000);
    },
    startReminderInterval() {
      // Rappel toutes les 45 secondes si l'utilisateur n'interagit pas
      this.intervalId = setInterval(() => {
        if (!this.expanded && !this.hasUnreadMessage) {
          this.hasUnreadMessage = true;
          this.pulseAnimation();
        }
      }, 45000);
    },
    getContextMessages() {
      // Récupérer les messages adaptés au contexte actuel
      const allMessages = {
        dashboard: [
          "Bienvenue dans ton tableau de bord ! Clique sur ton avatar au centre pour commencer ton aventure.",
          "Regarde tous les jeux disponibles ! Lequel voudrais-tu essayer en premier ?",
          "Pour progresser, commence par explorer ton profil en cliquant sur l'avatar central.",
          "N'oublie pas de consulter tes badges en cliquant sur ton avatar."
        ],
        profile: [
          "Voici ton profil ! Tu peux voir tes compétences et tes badges ici.",
          "Pour continuer ton aventure, clique sur \"Jouer maintenant\" dans la section \"Ma prochaine activité\".",
          "Tu peux personnaliser ton profil en cliquant sur le bouton d'édition."
        ],
        scenario: [
          "Dans ce jeu, tu vas pouvoir mettre en pratique tes compétences sociales.",
          "N'hésite pas à prendre ton temps pour réfléchir à chaque situation.",
          "Si tu veux essayer un autre jeu, tu peux toujours y revenir plus tard !"
        ],
        skills: [
          "Ce jeu te permet de découvrir tes forces et tes axes d'amélioration.",
          "Tourne la roue pour découvrir une compétence et indiquer ton niveau !",
          "Tu peux faire une pause et reprendre plus tard si tu le souhaites."
        ],
        metier: [
          "Découvre différents métiers qui pourraient t'intéresser !",
          "Tu peux liker les métiers qui t'intéressent ou passer à un autre.",
          "N'hésite pas à explorer tous les métiers pour élargir tes horizons."
        ],
        games: [
          "Ces mini-jeux sont conçus pour te faire découvrir différentes compétences.",
          "Tu peux choisir celui qui t'intéresse le plus, ou les essayer tous !",
          "Chaque jeu te permettra de gagner des badges. Collecte-les tous !"
        ],
        environment: [
          "Tu peux personnaliser ton environnement ici !",
          "Choisis le thème qui te plaît le plus pour te sentir à l'aise.",
          "Bravo ! Tu as presque terminé ton parcours de découverte."
        ],
        default: [
          "Je suis là pour t'aider ! Clique sur moi si tu as besoin de conseils.",
          "N'hésite pas à explorer toutes les fonctionnalités disponibles.",
          "Tu progresses bien, continue comme ça !"
        ]
      };
      
      return allMessages[this.context] || allMessages.default;
    },
    getContextOptions() {
      // Options adaptées au contexte actuel
      const allOptions = {
        dashboard: [
          { text: "Comment commencer ?", nextMessage: 0 },
          { text: "Voir mon profil", route: "/user-profile" },
          { text: "Explorer les jeux", action: "showGamesInfo" }
        ],
        profile: [
          { text: "Jouer maintenant", action: "startNextGame" },
          { text: "Voir mes badges", action: "showBadges" },
          { text: "Retour au tableau de bord", route: "/dashboard" }
        ],
        games: [
          { text: "Jouer aux scénarios", route: "/scenarios" },
          { text: "Découvrir les métiers", route: "/metier" },
          { text: "Tester mes compétences", route: "/roue-des-competences" }
        ],
        default: [
          { text: "Retour au tableau de bord", route: "/dashboard" },
          { text: "Voir mon parcours", action: "showProgress" }
        ]
      };
      
      // Ajouter une option pour changer de jeu si on est dans un jeu
      if (['scenario', 'skills', 'metier'].includes(this.context)) {
        return [
          { text: "Continuer ce jeu", nextMessage: 0 },
          { text: "Essayer un autre jeu", action: "suggestOtherGame" },
          { text: "Voir mon parcours", action: "showProgress" }
        ];
      }
      
      return allOptions[this.context] || allOptions.default;
    },
    loadUserJourney() {
      // Charger l'état du parcours utilisateur depuis le localStorage
      const savedJourney = localStorage.getItem('userJourney');
      if (savedJourney) {
        try {
          this.userJourney = JSON.parse(savedJourney);
        } catch (error) {
          console.error('Erreur de chargement du parcours utilisateur:', error);
        }
      }
    },
    saveUserJourney() {
      // Sauvegarder l'état du parcours utilisateur dans le localStorage
      localStorage.setItem('userJourney', JSON.stringify(this.userJourney));
    },
    addCompletedGame(gameId) {
      // Ajouter un jeu à la liste des jeux complétés
      if (!this.userJourney.completedGames.includes(gameId)) {
        this.userJourney.completedGames.push(gameId);
        this.saveUserJourney();
      }
    },
    addVisitedScreen(screenId) {
      // Ajouter un écran à la liste des écrans visités
      if (!this.userJourney.visitedScreens.includes(screenId)) {
        this.userJourney.visitedScreens.push(screenId);
        this.saveUserJourney();
      }
    },
    updateCurrentStep(step) {
      // Mettre à jour l'étape actuelle du parcours
      this.userJourney.currentStep = step;
      this.saveUserJourney();
    }
    // Remarque: Nous avons retiré les méthodes qui sont en conflit avec le parent comme showGamesInfo, startNextGame, etc.
    // Ces méthodes doivent être implémentées dans le composant parent et non dans le guide
  }
};
</script>

<style scoped>
.guide-avatar-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.guide-avatar-container.is-mini {
  bottom: 10px;
  right: 10px;
}

.avatar-wrapper {
  position: relative;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.avatar-wrapper:hover {
  transform: scale(1.05);
}

.guide-avatar {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  border: 3px solid #ffc107;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.is-mini .guide-avatar {
  width: 50px;
  height: 50px;
}

.guide-avatar.pulse {
  animation: avatarPulse 1s ease-in-out;
}

.notification-badge {
  position: absolute;
  top: 0;
  right: 0;
  width: 22px;
  height: 22px;
  background-color: #ff5722;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 14px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  animation: badgePulse 2s infinite;
}

.speech-bubble {
  position: relative;
  background-color: #fff;
  border-radius: 15px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 3px 15px rgba(0, 0, 0, 0.2);
  max-width: 350px;
  width: 300px;
  margin-right: 20px;
}

.mini-bubble {
  width: 250px;
  padding: 10px;
  margin-right: 10px;
}

.speech-bubble:after {
  content: '';
  position: absolute;
  bottom: -10px;
  right: 25px;
  border-width: 10px 10px 0;
  border-style: solid;
  border-color: #fff transparent transparent;
}

.bubble-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 5px;
  border-bottom: 1px solid #eee;
}

.guide-name {
  font-weight: bold;
  color: #4a4d9e;
}

.close-button, .minimize-button, .maximize-button {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #999;
  transition: color 0.2s ease;
}

.close-button:hover, .minimize-button:hover, .maximize-button:hover {
  color: #333;
}

.bubble-content p {
  margin: 0 0 15px;
  line-height: 1.5;
  color: #333;
}

.guide-options {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 15px;
}

.option-button {
  padding: 8px 15px;
  background-color: #f5f8ff;
  border: 1px solid #ddd;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
  color: #333;
}

.option-button:hover {
  background-color: #e3f2fd;
  border-color: #2196f3;
}

.guide-controls {
  display: flex;
  justify-content: space-between;
}

.control-button {
  padding: 5px 10px;
  background-color: transparent;
  border: none;
  color: #2196f3;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9rem;
}

.control-button:hover {
  text-decoration: underline;
}

/* Animations */
@keyframes avatarPulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

@keyframes badgePulse {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.1); opacity: 0.8; }
  100% { transform: scale(1); opacity: 1; }
}

.avatar-fade-enter-active, .avatar-fade-leave-active {
  transition: opacity 0.5s, transform 0.5s;
}

.avatar-fade-enter-from, .avatar-fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

.bubble-fade-enter-active, .bubble-fade-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.bubble-fade-enter-from, .bubble-fade-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

@media (max-width: 768px) {
  .speech-bubble {
    width: calc(100vw - 100px);
    max-width: 300px;
  }
  
  .mini-bubble {
    width: calc(100vw - 120px);
    max-width: 250px;
  }
  
  .guide-avatar {
    width: 60px;
    height: 60px;
  }
  
  .is-mini .guide-avatar {
    width: 40px;
    height: 40px;
  }
}
</style>