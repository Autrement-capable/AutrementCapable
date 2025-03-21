// RoomDashboard.vue
<template>
  <div>
    <div ref="pixiContainer" class="pixi-container"></div>
    <div v-if="debug" class="debug-info">
      <p>Status: {{ status }}</p>
      <p>Character: {{ characterInfo }}</p>
      
      <div class="config-panel">
        <h3>Configuration du fond</h3>
        <div class="object-config">
          <h4>Background</h4>
          <div class="config-row">
            <label>
              Largeur:
              <input type="number" v-model.number="spriteConfig.background.width" />
            </label>
            <label>
              Hauteur:
              <input type="number" v-model.number="spriteConfig.background.height" />
            </label>
          </div>
          <div class="config-row">
            <label>
              Position X:
              <input type="number" v-model.number="spriteConfig.background.x" />
            </label>
            <label>
              Position Y:
              <input type="number" v-model.number="spriteConfig.background.y" />
            </label>
          </div>
          <button @click="applyBackgroundOnly" class="action-button">Appliquer au fond</button>
        </div>
        
        <h3>Configuration des objets</h3>
        <div v-for="(object, objectName) in objectsConfig" :key="objectName" class="object-config">
          <h4>{{ objectName }}</h4>
          <div class="config-row">
            <label>
              Largeur:
              <input type="number" v-model.number="spriteConfig[objectName].width" @change="updateConfig" />
            </label>
            <label>
              Hauteur:
              <input type="number" v-model.number="spriteConfig[objectName].height" @change="updateConfig" />
            </label>
          </div>
          <div class="config-row">
            <label>
              Position X:
              <input type="number" v-model.number="spriteConfig[objectName].x" @change="updateConfig" />
            </label>
            <label>
              Position Y:
              <input type="number" v-model.number="spriteConfig[objectName].y" @change="updateConfig" />
            </label>
          </div>
        </div>
      </div>
      
      <div class="action-buttons">
        <button @click="reinitGame" class="action-button">Réinitialiser le jeu</button>
        <button @click="applyConfig" class="action-button">Appliquer toute la configuration</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RoomDashboard',
  data() {
    return {
      width: 0,
      height: 0,
      debug: false, // Activer le débogage
      characterInfo: 'Non initialisé',
      gameInstance: null,
      status: 'Initialisation...',
      initAttempts: 0,
      maxInitAttempts: 3,
      spriteConfig: {
        background: {
          width: 1200,  // Par défaut: largeur de l'écran
          height: 600,  // Par défaut: hauteur de l'écran
          x: 0,
          y: 0
        },
        character: {
          width: 60,
          height: 60,
          x: 510,  // Sera défini au centre par défaut
          y: 360   // Sera défini au centre par défaut
        },
        bed: {
          width: 240,
          height: 120,
          x: 500,
          y: 230
        },
        book: {
          width: 60,
          height: 80,
          x: 360,  // 1200 * 0.3
          y: 420   // 600 * 0.7
        },
        desk: {
          width: 180,
          height: 90,
          x: 770,  // 1200 * 0.2
          y: 300   // 600 * 0.5
        },
        wardrobe: {
          width: 240,
          height: 240,
          x: 160,  // 1200 * 0.8
          y: 180   // 600 * 0.3
        }
      }
    };
  },
  computed: {
    // Liste des objets configurables (excluant le background qui a son propre panneau)
    objectsConfig() {
      const { ...rest } = this.spriteConfig;
      return rest;
    }
  },
  mounted() {
    // Initialisation différée pour laisser le DOM se rendre
    setTimeout(() => {
      this.initGame();

      setTimeout(() => {
        console.log("Forcage d'une reinitialisation");
        this.reinitGame();
        }, 50);
    }, 50); // Délai plus long pour s'assurer que le DOM est prêt
  },
  beforeUnmount() {
    this.destroyGame();
  },
  methods: {
    async initGame() {
      this.status = 'Démarrage du jeu...';
      
      const container = this.$refs.pixiContainer;
      if (!container) {
        this.status = 'Erreur: Conteneur non trouvé';
        return;
      }
      
      try {
        this.status = 'Chargement du module...';
        
        // Supprimer toute instance précédente
        this.destroyGame();
        
        // Démarrer le jeu dans un module externe
        const module = await import('./roomGame.js');
        const GameClass = module.default;
        
        this.status = 'Création de l\'instance...';
        
        // Passer la configuration des sprites au constructeur
        this.gameInstance = new GameClass(container, this.spriteConfig);
        
        this.status = 'Initialisation...';
        
        // Initialiser le jeu avec callback pour les événements
        const success = await this.gameInstance.init((type, data) => {
          if (type === 'resize') {
            this.width = data.width;
            this.height = data.height;
          } else if (type === 'characterMove') {
            this.characterInfo = `(${Math.round(data.x)}, ${Math.round(data.y)})`;
            
            // Mettre à jour les coordonnées du personnage dans la configuration
            this.spriteConfig.character.x = Math.round(data.x);
            this.spriteConfig.character.y = Math.round(data.y);
          } else if (type === 'interaction') {
            // Déclencher l'événement vers le parent
            this.$emit('object-interaction', data);
          }
        });
        
        if (success) {
          this.status = 'Jeu en cours d\'exécution';
          this.initAttempts = 0;
        } else {
          this.status = 'Échec de l\'initialisation';
          this.retryInitIfNeeded();
        }
      } catch (error) {
        this.status = `Erreur: ${error.message}`;
        console.error('Échec de l\'initialisation du jeu:', error);
        this.retryInitIfNeeded();
      }
    },
    
    retryInitIfNeeded() {
      this.initAttempts++;
      if (this.initAttempts < this.maxInitAttempts) {
        this.status = `Nouvelle tentative ${this.initAttempts}/${this.maxInitAttempts}...`;
        setTimeout(() => {
          this.initGame();
        }, 1000);
      } else {
        this.status = 'Échec après plusieurs tentatives';
      }
    },
    
    destroyGame() {
      if (this.gameInstance) {
        try {
          this.gameInstance.destroy();
          this.status = 'Jeu détruit';
        } catch (error) {
          console.error('Erreur lors de la destruction du jeu:', error);
          this.status = 'Erreur lors de la destruction';
        }
        this.gameInstance = null;
      }
    },
    
    reinitGame() {
      this.initAttempts = 0;
      this.initGame();
    },
    
    updateConfig() {
      // Cette méthode est appelée lorsque les valeurs dans les champs sont modifiées
      console.log('Configuration mise à jour:', JSON.stringify(this.spriteConfig));
    },
    
    applyConfig() {
      // Appliquer les changements de configuration en réinitialisant le jeu
      this.status = 'Application de la nouvelle configuration...';
      this.reinitGame();
    },
    
    applyBackgroundOnly() {
      // Applique uniquement les changements du background sans réinitialiser le jeu
      if (this.gameInstance && this.gameInstance.updateBackground) {
        this.status = 'Mise à jour du fond...';
        
        const success = this.gameInstance.updateBackground(this.spriteConfig.background);
        
        if (success) {
          this.status = 'Fond mis à jour avec succès';
        } else {
          this.status = 'Erreur lors de la mise à jour du fond';
        }
      } else {
        this.status = 'Le jeu n\'est pas initialisé ou ne supporte pas la mise à jour du fond';
      }
    }
  }
};
</script>

<style scoped>
.pixi-container {
  width: 1200px;
  height: 600px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  position: relative;
}

.debug-info {
  margin-top: 10px;
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 8px;
  font-family: monospace;
}

.action-buttons {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.action-button {
  padding: 8px 15px;
  background-color: #4682b4;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}

.action-button:hover {
  background-color: #3a6d96;
}

.config-panel {
  margin: 15px 0;
  padding: 15px;
  background-color: #e6e6e6;
  border-radius: 6px;
}

.config-panel h3 {
  margin-top: 0;
  padding-bottom: 8px;
  border-bottom: 1px solid #ccc;
  color: #333;
}

.object-config {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.object-config h4 {
  margin-top: 0;
  margin-bottom: 10px;
  text-transform: capitalize;
  color: #4682b4;
}

.config-row {
  display: flex;
  gap: 15px;
  margin-bottom: 12px;
}

.config-row label {
  display: flex;
  flex-direction: column;
  flex: 1;
  font-size: 0.9em;
  color: #555;
}

.config-row input {
  margin-top: 4px;
  padding: 6px 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-family: monospace;
}

.config-row input:focus {
  outline: none;
  border-color: #4682b4;
  box-shadow: 0 0 0 2px rgba(70, 130, 180, 0.2);
}
</style>