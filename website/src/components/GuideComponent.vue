<template>
  <div 
    class="guide-avatar-container" 
    :style="positionStyle"
    :class="{ 'guide-visible': isVisible, 'guide-with-message': showMessage, 'guide-external': position === 'external' }"
  >
    <!-- Avatar du guide -->
    <div class="guide-avatar" @click="toggleMessage">
      <img :src="guideImage" alt="Guide avatar" class="guide-img" />
      <div v-if="hasNewMessage" class="new-message-indicator"></div>
    </div>
    
    <!-- Message du guide (bulle de dialogue) -->
    <div 
      v-if="showMessage" 
      class="guide-message"
      :class="{ 
        'message-visible': showMessage, 
        'message-top': position === 'bottom', 
        'message-bottom': position === 'top',
        'guide-external': position === 'external'
      }"
    >
      <div class="message-content">
        <h3 v-if="showGuideName">{{ guideName }}</h3>
        <p>{{ currentMessage }}</p>
        
        <!-- Options de réponse -->
        <div v-if="displayOptions.length > 0" class="guide-options">
          <button 
            v-for="(option, index) in displayOptions" 
            :key="index"
            class="guide-option-button"
            @click="selectOption(option)"
          >
            {{ option.text }}
          </button>
        </div>
      </div>
      
      <!-- Bouton de fermeture -->
      <button v-if="!forceShowMessage" class="close-message-button" @click="closeMessage">×</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GuideAvatar',
  props: {
    // Nom du guide
    guideName: {
      type: String,
      default: 'Léo'
    },
    // Position (top-right, bottom-left, etc.)
    position: {
      type: String,
      default: 'bottom-right'
    },
    // Contexte actuel pour les messages adaptés
    context: {
      type: String,
      default: 'default'
    },
    // Message forcé à afficher (prioritaire)
    forcedMessage: {
      type: String,
      default: null
    },
    // Options forcées à afficher
    forcedOptions: {
      type: Array,
      default: () => []
    },
    // Si on doit forcer l'affichage du message
    forceShowMessage: {
      type: Boolean,
      default: false
    },
    // Délai avant affichage automatique
    autoShowDelay: {
      type: Number,
      default: 2000
    },
    customPosition: {
      type: Object,
      default: null
    },
    
    // ID de la section active (pour le tour guidé)
    activeSectionId: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      isVisible: true,
      showMessage: false,
      hasNewMessage: true,
      messageTimeout: null,
      messagesMap: {
        default: [
          "Salut ! Je suis là pour t'aider à explorer l'application. Clique sur moi si tu as besoin d'aide !",
          "Tu peux me poser des questions ou explorer l'interface à ton rythme."
        ],
        dashboard: [
          "Bienvenue sur ton tableau de bord ! Ici tu peux accéder à tous les jeux et activités.",
          "Clique sur l'avatar au centre pour accéder à ton profil."
        ],
        profile: [
          "Voici ton profil ! Tu peux voir tes badges et ta progression ici.",
          "Clique sur 'Jouer maintenant' pour commencer une activité."
        ]
      },
      optionsMap: {
        default: [
          { text: "Quels jeux sont disponibles ?", action: "showGames" },
          { text: "Comment gagner des badges ?", action: "explainBadges" }
        ],
        dashboard: [
          { text: "Aller à mon profil", action: "goToProfile" },
          { text: "Explorer les jeux", action: "exploreGames" }
        ],
        profile: [
          { text: "Commencer à jouer", action: "startPlaying" },
          { text: "Découvrir mes badges", action: "exploreBadges" }
        ]
      },
      currentMessageIndex: 0,
      dismissedCount: 0
    };
  },
  computed: {
    // Style de positionnement basé sur la prop position
    positionStyle() {
      // Si une position personnalisée est fournie, l'utiliser
      if (this.customPosition) {
        return this.customPosition;
      }
      
      // Cas spécial pour le positionnement externe (hors du composant parent)
      if (this.position === 'external') {
        return {
          position: 'fixed',  // fixed au lieu de absolute
          top: '50%',
          right: '20px',      // Toujours à droite de l'écran
          transform: 'translateY(-50%)',
          zIndex: '2000'      // z-index élevé pour rester au-dessus de tout
        };
      }
      
      // Positions standard existantes...
      const positions = {
        'top-left': { top: '20px', left: '20px' },
        'top-right': { top: '20px', right: '20px' },
        // ... autres positions ...
      };
      
      return positions[this.position] || positions['bottom-right'];
    },
    
    // Image du guide (peut changer selon le contexte)
    guideImage() {
      // Ici, on pourrait définir différentes images selon le contexte
      return require('@/assets/avatars/guide.png'); // Image par défaut
    },
    
    // Message actuel à afficher
    currentMessage() {
      // Priorité au message forcé s'il existe
      if (this.forcedMessage) {
        return this.forcedMessage;
      }
      
      // Sinon, prendre le message du contexte actuel
      const messages = this.messagesMap[this.context] || this.messagesMap.default;
      return messages[this.currentMessageIndex % messages.length];
    },
    
    // Options à afficher
    displayOptions() {
      // Priorité aux options forcées
      if (this.forcedOptions && this.forcedOptions.length > 0) {
        return this.forcedOptions;
      }
      
      // Sinon, prendre les options du contexte actuel
      return this.optionsMap[this.context] || this.optionsMap.default;
    },
    
    // Si on doit afficher le nom du guide
    showGuideName() {
      return true; // On peut ajouter une logique si nécessaire
    }
  },
  watch: {
    // Surveiller les changements de contexte
    context() {
      // Réinitialiser l'index des messages
      this.currentMessageIndex = 0;
      
      // Afficher une notification
      this.hasNewMessage = true;
    },
    
    // Surveiller les messages forcés
    forcedMessage(newMessage) {
      if (newMessage) {
        this.hasNewMessage = true;
        
        // Afficher automatiquement le message forcé
        if (this.forceShowMessage) {
          this.showMessage = true;
        }
      }
    },
    
    // Surveiller forceShowMessage
    forceShowMessage(newValue) {
      if (newValue) {
        this.showMessage = true;
      }
    }
  },

  // Remplacez beforeDestroy par beforeUnmount
  beforeUnmount() {
    // Nettoyer le timeout
    if (this.messageTimeout) {
      clearTimeout(this.messageTimeout);
    }
  },
  mounted() {
    // Afficher automatiquement le message après un délai si autoShowDelay > 0
    if (this.autoShowDelay > 0) {
      this.messageTimeout = setTimeout(() => {
        this.showMessage = this.forceShowMessage || this.dismissedCount < 2;
      }, this.autoShowDelay);
    }
  },
  methods: {
    /**
     * Positionne le guide près d'un élément spécifique
     * @param {String} selector - Sélecteur CSS de l'élément
     * @param {String} position - Position relative (top, right, bottom, left)
     */
    positionNearElement(selector, position = 'right') {
      const element = document.querySelector(selector);
      if (!element) return;
      
      const rect = element.getBoundingClientRect();
      let newPosition = {};
      
      switch (position) {
        case 'top':
          newPosition = {
            bottom: `${window.innerHeight - rect.top + 20}px`,
            left: `${rect.left + rect.width / 2}px`,
            transform: 'translateX(-50%)'
          };
          break;
        case 'right':
          newPosition = {
            top: `${rect.top + rect.height / 2}px`,
            left: `${rect.right + 20}px`,
            transform: 'translateY(-50%)'
          };
          break;
        case 'bottom':
          newPosition = {
            top: `${rect.bottom + 20}px`,
            left: `${rect.left + rect.width / 2}px`,
            transform: 'translateX(-50%)'
          };
          break;
        case 'left':
          newPosition = {
            top: `${rect.top + rect.height / 2}px`,
            right: `${window.innerWidth - rect.left + 20}px`,
            transform: 'translateY(-50%)'
          };
          break;
      }
      
      this.$emit('position-updated', newPosition);
    },
    // Basculer l'affichage du message
    toggleMessage() {
      // Si on a un message forcé et forceShowMessage est true, ne rien faire
      if (this.forcedMessage && this.forceShowMessage) {
        return;
      }
      
      this.showMessage = !this.showMessage;
      
      if (this.showMessage) {
        // Marquer comme lu
        this.hasNewMessage = false;
      }
    },
    
    // Fermer le message
    closeMessage() {
      // Si on a un message forcé et forceShowMessage est true, ne rien faire
      if (this.forcedMessage && this.forceShowMessage) {
        return;
      }
      
      this.showMessage = false;
      this.dismissedCount++;
    },
    
    // Passer au message suivant
    nextMessage() {
      this.currentMessageIndex++;
    },
    
    // Gérer la sélection d'une option
    selectOption(option) {
      // Émettre un événement avec l'option sélectionnée
      this.$emit('option-selected', option);
      
      // Si l'option n'a pas d'action qui maintient la bulle ouverte, fermer le message
      if (!option.keepOpen) {
        this.showMessage = false;
      }
      
      // Marquer comme lu
      this.hasNewMessage = false;
    }
  }
};
</script>

<style scoped>
.guide-avatar-container {
  position: fixed;
  z-index: 1000;
  transition: all 0.3s ease;
}

.guide-avatar-container.guide-external {
  position: fixed;
  z-index: 2500;
}

.guide-message.guide-external {
  position: absolute;
  right: 70px;
  left: auto;
  transform: translateY(-50%);
}

.tour-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3);
  z-index: 1040;
  pointer-events: none;
}

.guide-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: #4caf50;
  cursor: pointer;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: transform 0.3s ease;
  border: 2px solid white;
}

.guide-avatar:hover {
  transform: scale(1.1);
}

.guide-img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.new-message-indicator {
  position: absolute;
  top: 0;
  right: 0;
  width: 15px;
  height: 15px;
  background-color: #ff4081;
  border-radius: 50%;
  border: 2px solid white;
  animation: pulse 2s infinite;
}

.guide-message {
  position: absolute;
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 15px;
  width: 280px;
  max-width: 80vw;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.3s ease;
  z-index: 1001;
  color: #333;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.message-visible {
  opacity: 1;
  transform: translateY(0);
}

.message-content {
  margin-bottom: 10px;
}

.message-content h3 {
  margin-top: 0;
  margin-bottom: 8px;
  color: #4caf50;
  font-size: 18px;
}

.message-content p {
  margin: 0 0 15px 0;
  line-height: 1.4;
  font-size: 14px;
}

.close-message-button {
  position: absolute;
  top: 5px;
  right: 5px;
  width: 20px;
  height: 20px;
  background: rgba(0, 0, 0, 0.1);
  border: none;
  border-radius: 50%;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.3s ease;
}

.close-message-button:hover {
  background: rgba(0, 0, 0, 0.2);
}

.guide-options {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.guide-option-button {
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #e0e0e0;
  border-radius: 20px;
  padding: 8px 16px;
  text-align: left;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s ease;
}

.guide-option-button:hover {
  background-color: #e0e0e0;
}

/* Positionnement de la bulle par rapport à l'avatar */
.message-top {
  bottom: 70px;
  left: 50%;
  transform: translateX(-50%);
}

.message-bottom {
  top: 70px;
  left: 50%;
  transform: translateX(-50%);
}

/* Animation pour l'indicateur de nouveau message */
@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(255, 64, 129, 0.6);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(255, 64, 129, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(255, 64, 129, 0);
  }
}

/* Animation pour la mise en évidence des sections */
@keyframes highlight-pulse {
  0% {
    opacity: 0.7;
    transform: scale(0.98);
  }
  50% {
    opacity: 0.9;
    transform: scale(1);
  }
  100% {
    opacity: 0.7;
    transform: scale(0.98);
  }
}

/* Styles pour la mise en évidence des sections */
.section-highlight {
  position: absolute;
  pointer-events: none;
  z-index: 1050;
  animation: highlight-pulse 2s ease-out infinite;
}

/* Styles responsifs */
@media (max-width: 480px) {
  .guide-message {
    width: 240px;
  }
  
  .guide-avatar {
    width: 50px;
    height: 50px;
  }
  
  .guide-options {
    gap: 5px;
  }
  
  .guide-option-button {
    padding: 6px 12px;
    font-size: 12px;
  }
}
</style>