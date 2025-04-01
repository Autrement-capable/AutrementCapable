<template>
  <div class="environment-container">
    <!-- Écran de bienvenue optimisé et plus compact -->
    <div v-if="!activityStarted" class="welcome-screen">
      <div class="welcome-content">
        <h1>Découvre ton environnement préféré</h1>
        
        <p class="intro-text">Tu vas découvrir ce que tu aimes et ce que tu n'aimes pas.</p>
        
        <div class="activity-explanation">
          <h2>Comment jouer?</h2>
          
          <div class="explanation-steps">
            <div class="explanation-step">
              <div class="step-number">1</div>
              <div class="step-content">
                <h3>Choisi 1 espace parmi 5</h3>
                <div class="step-image">
                  <img src="/images/maison_coloré.png" alt="Maisons colorées" />
                </div>
              </div>
            </div>
            
            <div class="explanation-step">
              <div class="step-number">2</div>
              <div class="step-content">
                <h3>Change les couleurs et les sons</h3>
                <div class="step-image">
                  <img src="/images/son_couleur_reglage.png" alt="Contrôles" />
                </div>
              </div>
            </div>
            
            <div class="explanation-step">
              <div class="step-number">3</div>
              <div class="step-content">
                <h3>Dis comment tu te sens</h3>
                <div class="step-image">
                  <img src="/images/emotions.png" alt="Émotions" />
                </div>
              </div>
            </div>
          </div>
          
          <div class="important-note">
            <h3>Souviens-toi</h3>
            <div class="important-points">
              <p>Tu peux prendre ton temps.</p>
              <p>Il n'y a pas de bonnes ou mauvaises réponses.</p>
              <p>Tu peux faire une pause quand tu veux.</p>
            </div>
          </div>
        </div>
        
        <button @click="startActivity" class="primary-button">
          Commencer l'aventure
        </button>
      </div>
    </div>
    
    <!-- Section principale avec les environnements -->
    <div v-else class="main-interface">      
      <!-- Sélecteur d'environnement (désormais visible) -->
      <div v-if="showEnvironmentSelector" class="environment-selector-overlay">
        <div class="environment-selector-container">
          <h2>Choisis ton espace</h2>
          <div class="environment-selector">
            <div 
              v-for="(env, index) in environments" 
              :key="index"
              @click="selectEnvironment(index); hideEnvironmentSelector();"
              :class="['environment-card', { active: currentEnvironmentIndex === index }]"
            >
              <div class="env-card-header">
                <div class="env-icon">{{ env.icon }}</div>
                <img :src="env.imageSrc" class="env-card-image" alt="Environnement" />
              </div>
              <h3>{{ env.name }}</h3>
              <p>{{ env.shortDescription }}</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Visualisation 3D de l'environnement -->
      <div class="environment-view">
        <div class="room-visualization" ref="container"></div>
        
        <!-- Instructions du guide -->
        <div v-if="showGuide" class="guide-overlay">
          <div class="guide-content">
            <h3>{{ currentGuide.title }}</h3>
            <p>{{ currentGuide.description }}</p>
            <button @click="dismissGuide" class="guide-button">Continuer</button>
          </div>
        </div>
        
        <!-- Contrôles de l'environnement actuel -->
        <div class="environment-controls">
          <div class="environment-header">
            <h2>{{ currentEnvironment.name }}</h2>
            <button @click="toggleEnvironmentSelector" class="guide-button">
              Changer
            </button> 
          </div>
          
          <p class="env-description">{{ currentEnvironment.description }}</p>
          
          <!-- Onglets de contrôles -->
          <div class="control-tabs">
            <button 
              v-for="tab in controlTabs" 
              :key="tab.id"
              @click="selectTab(tab.id)"
              :class="'tab-button'"
            >
              {{ tab.label }}
            </button>
          </div>
          
          <!-- Contenu des onglets -->
          <div class="tab-content">
            <!-- Onglet Lumière -->
            <div v-if="activeControlTab === 'light'" class="control-panel">
              <div class="control-group">
                <h3>Luminosité</h3>
                <div class="slider-control">
                  <div class="slider-labels">
                    <span>Sombre</span>
                    <span>Lumineux</span>
                  </div>
                  <input 
                    type="range" 
                    v-model.number="lightIntensity" 
                    min="0.2" 
                    max="8" 
                    step="0.1" 
                    @change="updateLighting" 
                  />
                </div>
                
                <div class="control-item">
                  <label>Couleur de la lumière:</label>
                  <div class="light-presets">
                    <button 
                      v-for="(preset, idx) in lightPresets" 
                      :key="idx"
                      @click="selectLightPreset(preset)"
                      :class="['preset-btn', { selected: lightColor === preset.color }]"
                      :style="{ backgroundColor: preset.color }"
                    >
                      <span>{{ preset.name }}</span>
                    </button>
                  </div>
                </div>
                
                <div class="toggle-control">
                  <label>
                    <input type="checkbox" v-model="ambientLight" @change="updateLighting" />
                    <span>Lumière ambiante douce</span>
                  </label>
                </div>
                
                <div class="tab-navigation">
                  <button @click="saveCurrentCustomization('light')" class="guide-button">
                    Sauvegarder
                  </button>
                </div>
              </div>
            </div>
            
            <!-- Onglet Couleurs -->
            <div v-if="activeControlTab === 'colors'" class="control-panel">
              <div class="control-group">
                <h3>Palette de couleurs</h3>
                <div class="color-palettes">
                  <div 
                    v-for="(palette, index) in colorPalettes" 
                    :key="index"
                    @click="selectColorPalette(palette)"
                    :class="['color-palette', { selected: isCurrentPalette(palette) }]"
                  >
                    <div class="palette-preview">
                      <div class="color-preview" :style="{ backgroundColor: palette.wall }"></div>
                      <div class="color-preview" :style="{ backgroundColor: palette.floor }"></div>
                      <div class="color-preview" :style="{ backgroundColor: palette.ceiling }"></div>
                    </div>
                    <span>{{ palette.name }}</span>
                  </div>
                </div>
                
                <div class="control-item">
                  <label>Niveau de contraste:</label>
                  <div class="radio-group">
                    <label><input type="radio" v-model="contrastLevel" value="low" @change="updateContrastLevel"> Doux</label>
                    <label><input type="radio" v-model="contrastLevel" value="medium" @change="updateContrastLevel"> Moyen</label>
                    <label><input type="radio" v-model="contrastLevel" value="high" @change="updateContrastLevel"> Fort</label>
                  </div>
                </div>
                
                <div class="tab-navigation">
                  <button @click="saveCurrentCustomization('colors')" class="guide-button">
                    Sauvegarder
                  </button>
                </div>
              </div>
            </div>
            
            <!-- Onglet Sons -->
            <div v-if="activeControlTab === 'sounds'" class="control-panel">
              <div class="control-group">
                <h3>Ambiance sonore</h3>
                <div class="control-item">
                  <label>Type d'ambiance:</label>
                  <select v-model="selectedAmbience" @change="updateAmbientSound">
                    <option value="none">Silence</option>
                    <option value="whitenoise">Bruit blanc</option>
                    <option value="nature">Sons de la nature</option>
                    <option value="cafe">Café tranquille</option>
                    <option value="crowd">Environnement animé</option>
                  </select>
                </div>
                
                <div class="slider-control">
                  <label>Volume: {{ Math.round(soundVolume * 100) }}%</label>
                  <input 
                    type="range" 
                    v-model.number="soundVolume" 
                    min="0" 
                    max="1" 
                    step="0.05" 
                    @change="updateSoundVolume" 
                    :disabled="selectedAmbience === 'none'"
                  />
                </div>
                
                <div class="slider-control">
                  <label>Personnes présentes: {{ peopleCount }}</label>
                  <input 
                    type="range" 
                    v-model.number="peopleCount" 
                    min="0" 
                    max="15" 
                    step="1" 
                    @change="updatePeopleCount" 
                  />
                </div>
                
                <div class="tab-navigation">
                  <button @click="saveCurrentCustomization('sounds')" class="guide-button">
                    Sauvegarder
                  </button>
                </div>
              </div>
            </div>
            
            <!-- Onglet Feedback -->
            <div v-if="activeControlTab === 'feedback'" class="control-panel">
              <div class="control-group">
                <h3>Votre ressenti</h3>
                <p>Comment vous sentiriez-vous dans cet environnement?</p>
                
                <div class="mood-selection">
                  <div 
                    v-for="mood in moods" 
                    :key="mood.value"
                    @click="selectMood(mood.value)"
                    :class="['mood-option', { selected: getCurrentFeedback().mood === mood.value }]"
                  >
                    <div class="mood-emoji">{{ mood.emoji }}</div>
                    <div class="mood-label">{{ mood.label }}</div>
                  </div>
                </div>
                
                <div class="control-item">
                  <label>Commentaires sur cet environnement:</label>
                  <textarea 
                    v-model="getCurrentFeedback().comments" 
                    rows="3" 
                    placeholder="Décrivez ce que vous aimez ou n'aimez pas...">
                  </textarea>
                </div>
                
                <div class="tab-navigation">
                  <button @click="saveFeedback" class="primary-button2" :disabled="!getCurrentFeedback().mood">
                    Enregistrer mon ressenti
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div class="finish-exploration">
            <button @click="showFeedbackMessage = true" class="primary-button">
              Terminer et voir mes préférences
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Message de confirmation -->
    <div v-if="showFeedbackMessage" class="feedback-overlay">
      <div class="feedback-message">
        <h3>Félicitations!</h3>
        <p>Vous avez exploré l'environnement sensoriel.</p>
        <div class="preference-summary">
          <h4>Résumé de vos préférences:</h4>
          <p><strong>Environnement préféré:</strong> {{ getFavoriteEnvironment() }}</p>
          <p><strong>Ambiance lumineuse préférée:</strong> {{ getLightPreference() }}</p>
          <p><strong>Préférence sonore:</strong> {{ getSoundPreference() }}</p>
        </div>
        <div class="recommendation-box">
          <h4>Recommandations personnalisées</h4>
          <p>D'après vos préférences, voici quelques conseils pour créer un environnement adapté à vos besoins sensoriels:</p>
          <ul>
            <li>{{ getPersonalizedRecommendation(1) }}</li>
            <li>{{ getPersonalizedRecommendation(2) }}</li>
            <li>{{ getPersonalizedRecommendation(3) }}</li>
          </ul>
        </div>
        <button @click="showFeedbackMessage = false" class="secondary-button">Retour à l'exploration</button>
        <button @click="restartExploration" class="primary-button">Recommencer l'exploration</button>
      </div>
    </div>
    
    <!-- Audio pour l'ambiance sonore -->
    <audio ref="ambientAudio" loop preload="auto" v-show="false"></audio>
  </div>
</template>

<script>
// Import our isolated RoomRenderer class
import RoomRenderer from './RoomRenderer';

export default {
  name: 'SensoryEnvironments',
  data() {
    return {
      // Interface state
      activityStarted: false,
      currentEnvironmentIndex: 0,
      activeControlTab: 'light',
      showFeedbackMessage: false,
      rendererInitialized: false,
      showEnvironmentSelector: false,
      
      // Progression du parcours
      currentStep: 1,
      completedTabs: [],
      completedEnvironments: [],
      
      // Guide
      showGuide: false,
      currentGuide: {
        title: '',
        description: ''
      },
      objectCategories: [
        { id: 'minimal', label: 'Minimal' },
        { id: 'moderate', label: 'Modéré' },
        { id: 'detailed', label: 'Détaillé' },
        { id: 'bedroom', label: 'Chambre' },
        { id: 'livingroom', label: 'Salon' },
        { id: 'office', label: 'Bureau' }
      ],

      selectedObjectCategory: 'minimal',
      modelsLoading: false,
      loadingProgress: 0,

      // Onglets de contrôle
      controlTabs: [
        { id: 'light', label: 'Lumière', order: 1 },
        { id: 'colors', label: 'Couleurs', order: 2 },
        { id: 'sounds', label: 'Sons', order: 3 },
        { id: 'feedback', label: 'Ressenti', order: 4 }
      ],
      
      // Données utilisateur
      userData: {
        environmentFeedback: {},
        overallFavorite: null
      },
      
      // Liste des environnements prédéfinis
      environments: [
        {
          name: "Espace de concentration",
          shortDescription: "Environnement optimisé pour le travail intellectuel",
          description: "Un espace conçu pour favoriser la concentration avec un éclairage adapté, des couleurs apaisantes et un minimum de distractions.",
          previewColor: "#4A90E2",
          imageSrc: "/images/concentration_space.png",
          icon: "🧠",
          objectsCategory: "concentration",
          defaultSettings: {
            room: {
              width: 9, 
              depth: 9, 
              height: 3.2,
              wallColor: "#f0f0f5",
              floorColor: "#6a75a3",
              ceilingColor: "#ffffff"
            },
            lighting: {
              color: "#ffffff",
              intensity: 2,
              ambient: true
            },
            sound: {
              type: "whitenoise",
              volume: 0.2,
              peopleCount: 0
            },
            clutter: "minimal"
          }
        },
        {
          name: "Espace de détente",
          shortDescription: "Zone calme pour se ressourcer",
          description: "Un environnement tranquille conçu pour apaiser les sens avec des tons doux, un éclairage tamisé et une ambiance sonore relaxante.",
          previewColor: "#66BB6A",
          imageSrc: "/images/relaxation_space.png",
          icon: "🌿",
          objectsCategory: "detente",
          defaultSettings: {
            room: {
              width: 9, 
              depth: 9, 
              height: 3.2,
              wallColor: "#e6f0f5",
              floorColor: "#d1dde6",
              ceilingColor: "#f0f7fa"
            },
            lighting: {
              color: "#f0f7fa",
              intensity: 1.2,
              ambient: true
            },
            sound: {
              type: "nature",
              volume: 0.3,
              peopleCount: 0
            },
            clutter: "moderate"
          }
        },
        {
          name: "Espace social contrôlé",
          shortDescription: "Pour les interactions en petit groupe",
          description: "Un espace conçu pour des interactions sociales maîtrisées avec un niveau de stimulation modéré et des zones de repli.",
          previewColor: "#FFA726",
          imageSrc: "/images/social_space.png",
          icon: "👥",
          objectsCategory: "social",
          defaultSettings: {
            room: {
              width: 9, 
              depth: 9, 
              height: 3.2,
              wallColor: "#fff9e6",
              floorColor: "#d9c298",
              ceilingColor: "#fffcf0"
            },
            lighting: {
              color: "#ffe0b2",
              intensity: 1.5,
              ambient: true
            },
            sound: {
              type: "cafe",
              volume: 0.4,
              peopleCount: 5
            },
            clutter: "moderate"
          }
        },
        {
          name: "Environnement sensoriel riche",
          shortDescription: "Stimulation sensorielle contrôlée",
          description: "Un environnement avec des stimuli sensoriels variés mais régulables, idéal pour explorer vos préférences sensorielles de façon sécurisée.",
          previewColor: "#AB47BC",
          imageSrc: "/images/sensory_space.png",
          objectsCategory: "sensoriel",
          icon: "✨",
          defaultSettings: {
            room: {
              width: 9, 
              depth: 9, 
              height: 3.2,
              wallColor: "#f0e6f5",
              floorColor: "#9c7fad",
              ceilingColor: "#f7f0fa"
            },
            lighting: {
              color: "#e0b2ff",
              intensity: 1.8,
              ambient: true
            },
            sound: {
              type: "none",
              volume: 0,
              peopleCount: 0
            },
            clutter: "detailed"
          }
        },
        {
          name: "Espace de transition",
          shortDescription: "Simulation d'espace public modéré",
          description: "Cet environnement simule un espace de transition comme un couloir ou un petit espace public avec un niveau de stimulation ajustable.",
          previewColor: "#26C6DA",
          imageSrc: "/images/transition_space.png",
          icon: "🚶",
          objectsCategory: "transition",
          defaultSettings: {
            room: {
              width: 12, 
              depth: 6, 
              height: 3,
              wallColor: "#e8f4f5",
              floorColor: "#90a4ae",
              ceilingColor: "#f5f7f8"
            },
            lighting: {
              color: "#b3e5fc",
              intensity: 1.7,
              ambient: true
            },
            sound: {
              type: "crowd",
              volume: 0.5,
              peopleCount: 10
            },
            clutter: "moderate"
          }
        }
      ],
      
      // Moods pour le feedback
      moods: [
        { value: 'veryCalm', emoji: '😌', label: 'Très calme' },
        { value: 'focused', emoji: '🧠', label: 'Concentré' },
        { value: 'comfortable', emoji: '😊', label: 'Confortable' },
        { value: 'neutral', emoji: '😐', label: 'Neutre' },
        { value: 'uneasy', emoji: '😟', label: 'Mal à l\'aise' },
        { value: 'overwhelmed', emoji: '😣', label: 'Surstimulé' }
      ],
      
      // Paramètres actuels de la pièce
      roomWidth: 10,
      roomDepth: 10,
      roomHeight: 3,
      wallColor: "#e0e0e0",
      floorColor: "#ad8a64",
      ceilingColor: "#f5f5f5",
      
      // Préréglages de taille
      roomSizePreset: "medium",
      ceilingHeightPreset: "medium",
      
      // Paramètres d'éclairage
      lightColor: "#ffffff",
      lightIntensity: 1.5,
      ambientLight: true,
      
      // Préréglages de lumière
      lightPresets: [
        { name: "Neutre", color: "#ffffff" },
        { name: "Chaud", color: "#ffe0b2" },
        { name: "Froid", color: "#b3e5fc" },
        { name: "Doux", color: "#f0e6ff" },
        { name: "Naturel", color: "#fff8e1" }
      ],
      
      // Palettes de couleurs
      colorPalettes: [
        { 
          name: "Neutre", 
          wall: "#e0e0e0", 
          floor: "#ad8a64", 
          ceiling: "#f5f5f5"
        },
        { 
          name: "Apaisant", 
          wall: "#e6f0f5", 
          floor: "#d1dde6", 
          ceiling: "#f0f7fa"
        },
        { 
          name: "Chaleureux", 
          wall: "#fff5e6", 
          floor: "#d9b38c", 
          ceiling: "#fffaf0"
        },
        { 
          name: "Naturel", 
          wall: "#e8f4e5", 
          floor: "#8ba987", 
          ceiling: "#f5f7f5"
        },
        { 
          name: "Concentration", 
          wall: "#f0f0f5", 
          floor: "#6a75a3", 
          ceiling: "#ffffff"
        },
        { 
          name: "Sensoriel doux", 
          wall: "#f8e9e6", 
          floor: "#c8b7b4", 
          ceiling: "#fdf6f5"
        }
      ],
      
      // Niveau de contraste
      contrastLevel: "medium",
      
      // Paramètres audio
      soundEnabled: false,
      soundVolume: 0.5,
      selectedAmbience: "none",
      peopleCount: 0,
      
      // Niveau de détail/encombrement
      clutterLevel: "moderate",
      
      // Meubles
      furniture: [],
      
      // Renderer
      renderer: null
    };
  },
  computed: {
    currentEnvironment() {
      return this.environments[this.currentEnvironmentIndex] || this.environments[0];
    },
    progressPercentage() {
      // Calcule le pourcentage de progression basé sur les environnements complétés
      const totalEnvironments = this.environments.length;
      const completedCount = this.completedEnvironments.length;
      
      // Si l'environnement actuel a des onglets complétés, ajouter une progression partielle
      let partialProgress = 0;
      if (!this.completedEnvironments.includes(this.currentEnvironmentIndex)) {
        const totalTabs = this.controlTabs.length;
        const completedTabs = this.completedTabs.length;
        partialProgress = completedTabs / totalTabs / totalEnvironments;
      }
      
      return (completedCount / totalEnvironments * 100) + (partialProgress * 100);
    },
    isLastEnvironment() {
      return this.currentEnvironmentIndex === this.environments.length - 1;
    }
  },
  mounted() {
    // Initialiser le renderer pour éviter les problèmes de timing
    this.initRenderer();
  },
  beforeUnmount() {
    // Clean up
    if (this.renderer) {
      this.renderer.dispose();
      this.renderer = null;
    }
    
    // Stop audio
    if (this.$refs.ambientAudio) {
      this.$refs.ambientAudio.pause();
    }
  },
  methods: {
    // Initialiser le renderer
    initRenderer() {
      if (this.$refs.container) {
        this.renderer = new RoomRenderer(this.$refs.container);
        
        // Attendre un court délai pour s'assurer que le renderer est prêt
        setTimeout(() => {
          this.rendererInitialized = true;
          // Initialiser avec une pièce vide basique
          this.createBasicRoom();
        }, 500);
      }
    },
    
    // Créer une pièce basique initiale
    createBasicRoom() {
      if (!this.renderer || !this.rendererInitialized) return;
      
      try {
        this.renderer.updateRoom(
          this.roomWidth,
          this.roomDepth,
          this.roomHeight,
          this.wallColor,
          this.floorColor,
          this.ceilingColor
        );
      } catch (error) {
        console.error("Erreur lors de la création de la pièce initiale:", error);
      }
    },
    
    // Commencer l'activité
    startActivity() {
      this.activityStarted = true;
      
      // Initialiser les feedbacks pour tous les environnements
      this.environments.forEach((env, index) => {
        this.userData.environmentFeedback[index] = {
          mood: '',
          comments: '',
          customizations: {}
        };
      });
      
      // S'assurer que le renderer est prêt
      if (!this.rendererInitialized) {
        this.initRenderer();
      }

      this.showEnvironmentSelector = true;
      
      // Attendre un court délai avant de sélectionner l'environnement
      setTimeout(() => {
        this.createBasicRoom();
      }, 300);
    },

    toggleEnvironmentSelector() {
      this.showEnvironmentSelector = !this.showEnvironmentSelector;
    },
    
    // Masquer le sélecteur d'environnements
    hideEnvironmentSelector() {
      this.showEnvironmentSelector = false;
    },
    
    // Sélectionner un environnement
    selectEnvironment(index) {
      this.currentEnvironmentIndex = index;
      const env = this.environments[index];
      
      // Réinitialiser les onglets complétés pour le nouvel environnement
      this.completedTabs = [];
      this.activeControlTab = 'light';
      this.currentStep = 1;
      
      // Appliquer les paramètres par défaut de l'environnement
      const settings = env.defaultSettings;
      
      // Mise à jour des dimensions et couleurs
      this.roomWidth = settings.room.width;
      this.roomDepth = settings.room.depth;
      this.roomHeight = settings.room.height;
      this.wallColor = settings.room.wallColor;
      this.floorColor = settings.room.floorColor;
      this.ceilingColor = settings.room.ceilingColor;
      
      // Mise à jour de l'éclairage
      this.lightColor = settings.lighting.color;
      this.lightIntensity = settings.lighting.intensity;
      this.ambientLight = settings.lighting.ambient;
      
      // Mise à jour du son
      this.selectedAmbience = settings.sound.type;
      this.soundVolume = settings.sound.volume;
      this.peopleCount = settings.sound.peopleCount;
            
      // Déterminer les préréglages de taille
      this.determineSizePresets();
      
      // Vérifier que le renderer est prêt
      if (!this.rendererInitialized) {
        console.warn("Le renderer n'est pas encore initialisé");
        this.initRenderer();
        setTimeout(() => {
          this.selectedObjectCategory = env.objectsCategory || "minimal";
          this.applyEnvironmentChanges();
        }, 500);
      } else {
        this.selectedObjectCategory = env.objectsCategory || "minimal";
        this.applyEnvironmentChanges();
      }

      // Afficher le guide pour le nouvel environnement
      this.showGuideMessage({
        title: "Bienvenue dans " + this.currentEnvironment.name,
        description: "Personnalisez cet environnement selon vos préférences en utilisant les onglets de contrôle."
      });
    },
    
    // Naviguer vers un environnement spécifique
    goToEnvironment(index) {
      // Ne permettre que la navigation vers les environnements déjà complétés ou l'environnement actuel
      if (this.completedEnvironments.includes(index) || index === this.currentEnvironmentIndex) {
        this.selectEnvironment(index);
        
        // Si c'est l'environnement actuel qui n'est pas complété, réinitialiser à l'onglet Lumière
        if (index === this.currentEnvironmentIndex && !this.completedEnvironments.includes(index)) {
          this.activeControlTab = 'light';
          this.currentStep = 1;
          this.completedTabs = [];
        }
      }
    },
    
    // Afficher un message du guide
    showGuideMessage(guide) {
      this.currentGuide = guide;
      this.showGuide = true;
    },
    
    // Fermer le message du guide
    dismissGuide() {
      this.showGuide = false;
    },
    
    // Vérifier si un onglet est accessible
    isTabAccessible(tabId) {
      const tabOrder = this.controlTabs.find(tab => tab.id === tabId).order;
      
      // Si c'est le premier onglet, il est toujours accessible
      if (tabOrder === 1) return true;
      
      // Sinon, vérifier si l'onglet précédent est complété
      const previousTab = this.controlTabs.find(tab => tab.order === tabOrder - 1);
      return this.completedTabs.includes(previousTab.id);
    },
    
    // Sélectionner un onglet
    selectTab(tabId) {
      this.activeControlTab = tabId;
      this.currentStep = this.controlTabs.find(tab => tab.id === tabId).order;
    },
    
    // Compléter l'onglet actuel et passer au suivant
    completeCurrentTab() {
      if (!this.completedTabs.includes(this.activeControlTab)) {
        this.completedTabs.push(this.activeControlTab);
      }
      
      // Trouver l'onglet suivant
      const currentTabOrder = this.controlTabs.find(tab => tab.id === this.activeControlTab).order;
      const nextTab = this.controlTabs.find(tab => tab.order === currentTabOrder + 1);
      
      if (nextTab) {
        this.activeControlTab = nextTab.id;
        this.currentStep++;
        
        // Afficher le guide approprié pour le nouvel onglet
        this.showTabGuide(nextTab.id);
      }
    },
    
    // Aller à l'onglet précédent
    goToPreviousTab() {
      // Trouver l'onglet précédent
      const currentTabOrder = this.controlTabs.find(tab => tab.id === this.activeControlTab).order;
      const prevTab = this.controlTabs.find(tab => tab.order === currentTabOrder - 1);
      
      if (prevTab) {
        this.activeControlTab = prevTab.id;
        this.currentStep--;
      }
    },
    
    // Afficher le guide approprié pour chaque onglet
    showTabGuide(tabId) {
      let guideMessage = {
        title: "",
        description: ""
      };
      
      switch(tabId) {
        case 'colors':
          guideMessage.title = "Personnalisons les couleurs";
          guideMessage.description = "Choisissez une palette de couleurs et un niveau de contraste qui vous semblent agréables pour cet environnement.";
          break;
        case 'sounds':
          guideMessage.title = "Ajustons l'ambiance sonore";
          guideMessage.description = "Sélectionnez le type de son et le volume qui vous conviennent. Vous pouvez aussi ajuster le nombre de personnes présentes.";
          break;
        case 'feedback':
          guideMessage.title = "Comment vous sentez-vous?";
          guideMessage.description = "Maintenant que vous avez personnalisé cet environnement, indiquez votre ressenti et partagez vos impressions.";
          break;
      }
      
      this.showGuideMessage(guideMessage);
    },
    
    // Compléter l'environnement actuel et passer au suivant
    completeEnvironment() {
      // Vérifier que l'environnement n'est pas déjà marqué comme complété
      if (!this.completedEnvironments.includes(this.currentEnvironmentIndex)) {
        this.completedEnvironments.push(this.currentEnvironmentIndex);
      }
      
      // Si c'est le dernier environnement, afficher le résumé
      if (this.isLastEnvironment) {
        this.showFeedbackMessage = true;
      } else {
        // Passer à l'environnement suivant
        this.selectEnvironment(this.currentEnvironmentIndex + 1);
        
        // Afficher le guide d'introduction pour le nouvel environnement
        this.showGuideMessage({
          title: "Découvrons " + this.currentEnvironment.name,
          description: "C'est un nouveau type d'environnement. Commençons par ajuster l'éclairage selon vos préférences."
        });
      }
    },
    
    // Appliquer les changements d'environnement de manière sécurisée
    applyEnvironmentChanges() {
      try {
        // Appliquer tous les changements
        this.updateRoom();
        this.updateLighting();
        this.updateAmbientSound();
        this.updateClutterLevel();
      } catch (error) {
        console.error("Erreur lors de l'application des changements d'environnement:", error);
      }
    },
    
    // Obtenir les données de feedback actuelles de manière sécurisée
    getCurrentFeedback() {
      // S'assurer que l'objet de feedback existe pour l'environnement actuel
      if (!this.userData.environmentFeedback[this.currentEnvironmentIndex]) {
        this.userData.environmentFeedback[this.currentEnvironmentIndex] = {
          mood: '',
          comments: '',
          customizations: {}
        };
      }
      
      return this.userData.environmentFeedback[this.currentEnvironmentIndex];
    },
    
    // Déterminer les préréglages de taille basés sur les dimensions actuelles
    determineSizePresets() {
      // Taille de la pièce
      if (this.roomWidth <= 7) {
        this.roomSizePreset = "small";
      } else if (this.roomWidth <= 10) {
        this.roomSizePreset = "medium";
      } else {
        this.roomSizePreset = "large";
      }
      
      // Hauteur du plafond
      if (this.roomHeight <= 2.6) {
        this.ceilingHeightPreset = "low";
      } else if (this.roomHeight <= 3.2) {
        this.ceilingHeightPreset = "medium";
      } else {
        this.ceilingHeightPreset = "high";
      }
    },
    
    // Sélectionner un préréglage de lumière
    selectLightPreset(preset) {
      this.lightColor = preset.color;
      this.updateLighting();
      this.saveCurrentCustomization('light');
    },
    
    // Vérifier si c'est la palette actuelle
    isCurrentPalette(palette) {
      return this.wallColor === palette.wall && 
             this.floorColor === palette.floor && 
             this.ceilingColor === palette.ceiling;
    },
    
    // Sélectionner une palette de couleurs
    selectColorPalette(palette) {
      this.wallColor = palette.wall;
      this.floorColor = palette.floor;
      this.ceilingColor = palette.ceiling;
      this.updateColors();
      this.saveCurrentCustomization('colors');
    },
    
    // Mettre à jour le niveau de contraste
    updateContrastLevel() {
      // Trouver la palette de base actuelle
      let basePalette = null;
      for (const palette of this.colorPalettes) {
        if (this.isCurrentPalette(palette)) {
          basePalette = palette;
          break;
        }
      }
      
      // Si aucune palette exacte n'est trouvée, utiliser la première
      if (!basePalette) {
        basePalette = this.colorPalettes[0];
      }
      
      // Appliquer le niveau de contraste
      switch(this.contrastLevel) {
        case "low":
          this.wallColor = this.adjustColorSaturation(basePalette.wall, 0.7);
          this.floorColor = this.adjustColorSaturation(basePalette.floor, 0.7);
          this.ceilingColor = this.adjustColorSaturation(basePalette.ceiling, 0.7);
          break;
        case "medium":
          this.wallColor = basePalette.wall;
          this.floorColor = basePalette.floor;
          this.ceilingColor = basePalette.ceiling;
          break;
        case "high":
          this.wallColor = this.adjustColorSaturation(basePalette.wall, 1.3);
          this.floorColor = this.adjustColorSaturation(basePalette.floor, 1.3);
          this.ceilingColor = this.adjustColorSaturation(basePalette.ceiling, 1.3);
          break;
      }
      
      this.updateColors();
      this.saveCurrentCustomization('colors');
    },
    
    // Ajuster la saturation d'une couleur
    adjustColorSaturation(hexColor, factor) {
      // Convertir hex en RGB
      let r = parseInt(hexColor.slice(1, 3), 16);
      let g = parseInt(hexColor.slice(3, 5), 16);
      let b = parseInt(hexColor.slice(5, 7), 16);
      
      // Convertir RGB en HSL
      const max = Math.max(r, g, b) / 255;
      const min = Math.min(r, g, b) / 255;
      r = r / 255;
      g = g / 255;
      b = b / 255;
      
      let h, s, l = (max + min) / 2;
      
      if (max === min) {
        h = s = 0; // achromatique
      } else {
        const d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        
        switch (max) {
          case r: h = (g - b) / d + (g < b ? 6 : 0); break;
          case g: h = (b - r) / d + 2; break;
          case b: h = (r - g) / d + 4; break;
        }
        
        h /= 6;
      }
      
      // Ajuster la saturation
      s = Math.min(1, Math.max(0, s * factor));
      
      // Convertir HSL en RGB
      let r1, g1, b1;
      
      if (s === 0) {
        r1 = g1 = b1 = l; // achromatique
      } else {
        const hue2rgb = (p, q, t) => {
          if (t < 0) t += 1;
          if (t > 1) t -= 1;
          if (t < 1/6) return p + (q - p) * 6 * t;
          if (t < 1/2) return q;
          if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
          return p;
        };
        
        const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
        const p = 2 * l - q;
        
        r1 = hue2rgb(p, q, h + 1/3);
        g1 = hue2rgb(p, q, h);
        b1 = hue2rgb(p, q, h - 1/3);
      }
      
      // Convertir de nouveau en hex
      r = Math.round(r1 * 255);
      g = Math.round(g1 * 255);
      b = Math.round(b1 * 255);
      
      return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
    },
    
    // Mettre à jour l'ambiance sonore
    updateAmbientSound() {
      if (!this.$refs.ambientAudio) return;
      
      // Mise à jour de la source audio en fonction de la sélection
      let audioSrc;
      this.soundEnabled = this.selectedAmbience !== 'none';
      
      switch(this.selectedAmbience) {
        case 'none':
          this.$refs.ambientAudio.pause();
          return;
        case 'whitenoise':
          audioSrc = 'https://cdn.pixabay.com/download/audio/2022/03/10/audio_6629de9d6b.mp3';
          break;
        case 'nature':
          audioSrc = 'https://cdn.pixabay.com/download/audio/2021/08/09/audio_c80427e13b.mp3';
          break;
        case 'cafe':
          audioSrc = 'https://cdn.pixabay.com/download/audio/2022/01/26/audio_31e2b19a63.mp3';
          break;
        case 'crowd':
          audioSrc = 'https://cdn.pixabay.com/download/audio/2021/08/09/audio_8eb4af9c81.mp3';
          break;
      }
      
      // N'actualiser la source que si elle a changé
      if (this.$refs.ambientAudio.src !== audioSrc) {
        this.$refs.ambientAudio.src = audioSrc;
      }
      
      // Appliquer le volume
      this.$refs.ambientAudio.volume = this.soundVolume;
      
      // Lire l'audio si activé
      if (this.soundEnabled) {
        this.$refs.ambientAudio.play().catch(e => console.log('Audio play failed:', e));
      }
      
      this.saveCurrentCustomization('sounds');
    },
    
    // Mettre à jour le volume sonore
    updateSoundVolume() {
      if (!this.$refs.ambientAudio) return;
      
      this.$refs.ambientAudio.volume = this.soundVolume;
      this.saveCurrentCustomization('sounds');
    },
    
    // Mettre à jour le nombre de personnes
    updatePeopleCount() {
      if (this.renderer && this.rendererInitialized) {
        try {
          this.renderer.updatePeople(this.peopleCount);
          this.saveCurrentCustomization('sounds');
        } catch (error) {
          console.error("Erreur lors de la mise à jour des personnes:", error);
        }
      }
    },
    
    // Mettre à jour le niveau de détail/encombrement
    updateClutterLevel() {
      if (!this.renderer || !this.rendererInitialized) return;
      
      try {
        // Indiquer que le chargement est en cours
        this.modelsLoading = true;
        this.loadingProgress = 0;
        
        // Effacer tous les objets existants
        
        // Charger les nouveaux objets selon la catégorie sélectionnée
        this.renderer.loadObjectsByCategory(this.selectedObjectCategory)
          .then(() => {
            // Chargement terminé
            this.modelsLoading = false;
            this.loadingProgress = 100;
            
            // Synchroniser les données
            this.syncFurnitureData();
            this.saveCurrentCustomization('space');
          })
          .catch(error => {
            console.error("Erreur lors du chargement des objets 3D:", error);
            this.modelsLoading = false;
          });
        
      } catch (error) {
        console.error("Erreur lors de la mise à jour du niveau de détail:", error);
        this.modelsLoading = false;
      }
    },

    // Enregistrer le feedback et marquer l'environnement comme complété
    saveFeedback() {
      const feedback = this.getCurrentFeedback();

      console.log("Feedback enregistré:", feedback);
      
      if (!this.completedEnvironments.includes(this.currentEnvironmentIndex)) {
        this.completedEnvironments.push(this.currentEnvironmentIndex);
      }
      
      // Afficher un message de confirmation
      this.showGuideMessage({
        title: "Ressenti enregistré",
        description: "Votre feedback sur cet environnement a été sauvegardé. Vous pouvez explorer d'autres environnements ou terminer l'activité."
      });
    },
    
    // Enregistrer les personnalisations actuelles
    saveCurrentCustomization(category) {
      const feedback = this.getCurrentFeedback();
      
      if (!this.completedTabs.includes(category)) {
        this.completedTabs.push(category);
      }

      if (!feedback.customizations) {
        feedback.customizations = {};
      }
      
      switch(category) {
        case 'light':
          feedback.customizations.light = {
            color: this.lightColor,
            intensity: this.lightIntensity,
            ambient: this.ambientLight
          };
          break;
        case 'colors':
          feedback.customizations.colors = {
            wall: this.wallColor,
            floor: this.floorColor,
            ceiling: this.ceilingColor,
            contrastLevel: this.contrastLevel
          };
          break;
        case 'sounds':
          feedback.customizations.sounds = {
            ambience: this.selectedAmbience,
            volume: this.soundVolume,
            peopleCount: this.peopleCount
          };
          break;
        case 'space':
          feedback.customizations.space = {
            sizePreset: this.roomSizePreset,
            ceilingPreset: this.ceilingHeightPreset,
            clutterLevel: this.clutterLevel,
            width: this.roomWidth,
            depth: this.roomDepth,
            height: this.roomHeight
          };
          break;
      }
    },
    
    // Sélectionner un mood pour le feedback
    selectMood(moodValue) {
      const feedback = this.getCurrentFeedback();
      feedback.mood = moodValue;
    },
    
    // Obtenir l'environnement préféré pour l'affichage
    getFavoriteEnvironment() {
      // Déterminer l'environnement préféré basé sur les feedbacks
      let favoriteEnvironment = null;
      let bestMoodScore = -1;
      
      const positiveMoods = ['veryCalm', 'focused', 'comfortable'];
      
      for (const [index, feedback] of Object.entries(this.userData.environmentFeedback)) {
        if (positiveMoods.includes(feedback.mood)) {
          const score = positiveMoods.indexOf(feedback.mood);
          if (score > bestMoodScore) {
            bestMoodScore = score;
            favoriteEnvironment = parseInt(index);
          }
        }
      }
      
      this.userData.overallFavorite = favoriteEnvironment;
      
      if (favoriteEnvironment !== null) {
        return this.environments[favoriteEnvironment].name;
      }
      return "Non déterminé";
    },
    
    // Obtenir la préférence d'éclairage pour l'affichage
    getLightPreference() {
      const allFeedbacks = this.userData.environmentFeedback;
      const lightPreferences = Object.values(allFeedbacks)
        .filter(fb => fb.customizations && fb.customizations.light)
        .map(fb => fb.customizations.light);
      
      if (lightPreferences.length === 0) return "Non déterminé";
      
      // Calculer l'intensité moyenne préférée
      const avgIntensity = lightPreferences.reduce((sum, pref) => sum + pref.intensity, 0) / lightPreferences.length;
      
      if (avgIntensity < 1.3) return "Éclairage tamisé";
      if (avgIntensity > 1.8) return "Éclairage lumineux";
      return "Éclairage modéré";
    },
    
    // Obtenir la préférence sonore pour l'affichage
    getSoundPreference() {
      const allFeedbacks = this.userData.environmentFeedback;
      const soundPreferences = Object.values(allFeedbacks)
        .filter(fb => fb.customizations && fb.customizations.sounds)
        .map(fb => fb.customizations.sounds);
      
      if (soundPreferences.length === 0) return "Non déterminé";
      
      // Trouver le type d'ambiance le plus fréquent
      const ambienceTypes = soundPreferences.map(pref => pref.ambience);
      const ambienceCounts = {};
      let maxCount = 0;
      let preferredAmbience = "none";
      
      ambienceTypes.forEach(type => {
        ambienceCounts[type] = (ambienceCounts[type] || 0) + 1;
        if (ambienceCounts[type] > maxCount) {
          maxCount = ambienceCounts[type];
          preferredAmbience = type;
        }
      });
      
      switch(preferredAmbience) {
        case "none": return "Préfère le silence";
        case "whitenoise": return "Préfère le bruit blanc";
        case "nature": return "Préfère les sons naturels";
        case "cafe": return "Préfère l'ambiance café tranquille";
        case "crowd": return "Tolère bien l'environnement animé";
        default: return "Préférence variée";
      }
    },
    
    // Obtenir une recommandation personnalisée
    getPersonalizedRecommendation(index) {
      const recommendations = [
        // Recommandations basées sur l'éclairage
        () => {
          const lightPref = this.getLightPreference();
          if (lightPref.includes("tamisé")) {
            return "Privilégiez un éclairage indirect et tamisé dans votre espace quotidien, en évitant les lumières fluorescentes.";
          } else if (lightPref.includes("lumineux")) {
            return "Assurez-vous d'avoir un bon éclairage dans vos espaces de travail, idéalement avec une lumière naturelle ou des lampes à spectre complet.";
          } else {
            return "Optez pour un éclairage modulable que vous pourrez ajuster selon vos activités et votre niveau de fatigue.";
          }
        },
        
        // Recommandations basées sur le son
        () => {
          const soundPref = this.getSoundPreference();
          if (soundPref.includes("silence")) {
            return "Envisagez d'utiliser des bouchons d'oreilles ou un casque anti-bruit dans les environnements bruyants.";
          } else if (soundPref.includes("bruit blanc")) {
            return "Utilisez une application ou un appareil de bruit blanc pour masquer les sons distrayants et améliorer votre concentration.";
          } else if (soundPref.includes("sons naturels")) {
            return "Intégrez des sons de la nature dans votre environnement quotidien pour réduire le stress et améliorer votre bien-être.";
          } else {
            return "Créez des playlists adaptées à différentes activités pour vous aider à réguler votre état sensoriel.";
          }
        },
        
        // Recommandation générale
        () => {
          return "Prenez des pauses sensorielles régulières pour prévenir la fatigue et l'épuisement, particulièrement dans des environnements stimulants.";
        }
      ];
      
      // S'assurer que l'index est valide
      if (index > 0 && index <= recommendations.length) {
        return recommendations[index - 1]();
      }
      
      // Recommandation par défaut
      return recommendations[recommendations.length - 1]();
    },
    
    // Recommencer l'exploration
    restartExploration() {
      // Réinitialiser les données
      this.showFeedbackMessage = false;
      this.completedEnvironments = [];
      this.completedTabs = [];
      this.currentEnvironmentIndex = 0;
      this.currentStep = 1;
      this.activeControlTab = 'light';
      
      // Réinitialiser les feedbacks
      this.environments.forEach((env, index) => {
        this.userData.environmentFeedback[index] = {
          mood: '',
          comments: '',
          customizations: {}
        };
      });
      
      this.showEnvironmentSelector = true;

      // // Sélectionner le premier environnement
      // this.selectEnvironment(0);
      
      // // Afficher le guide d'introduction
      // this.showGuideMessage({
      //   title: "Bienvenue dans " + this.currentEnvironment.name,
      //   description: "Commençons par ajuster la lumière de cet environnement. Utilisez les contrôles pour trouver l'éclairage qui vous convient le mieux."
      // });
    },
    
    // Méthodes de mise à jour du renderer
    updateRoom() {
      if (!this.renderer || !this.rendererInitialized) return;
      
      try {
        this.renderer.updateRoom(
          this.roomWidth,
          this.roomDepth,
          this.roomHeight,
          this.wallColor,
          this.floorColor,
          this.ceilingColor
        );
        
        // Synchroniser les données
        this.syncFurnitureData();
      } catch (error) {
        console.error("Erreur lors de la mise à jour de la pièce:", error);
      }
    },
    
    updateColors() {
      if (!this.renderer || !this.rendererInitialized) return;
      
      try {
        this.renderer.updateRoomColors(
          this.wallColor,
          this.floorColor,
          this.ceilingColor
        );
      } catch (error) {
        console.error("Erreur lors de la mise à jour des couleurs:", error);
      }
    },
    
    updateLighting() {
      if (!this.renderer || !this.rendererInitialized) return;
      
      try {
        this.renderer.updateLighting(
          this.lightColor,
          this.lightIntensity,
          this.ambientLight
        );
        
        this.saveCurrentCustomization('light');
      } catch (error) {
        console.error("Erreur lors de la mise à jour de l'éclairage:", error);
      }
    },
    
    // Synchroniser les données de meubles
    syncFurnitureData() {
      if (!this.renderer || !this.rendererInitialized) return;
      
      try {
        // Obtenir l'état du renderer
        const state = this.renderer.getState();
        
        // Mettre à jour l'état réactif de Vue
        this.furniture = state.furniture;
        
        // Synchroniser également les données de la salle
        this.roomWidth = state.room.width;
        this.roomDepth = state.room.depth;
        this.roomHeight = state.room.height;
        this.wallColor = state.room.wallColor;
        this.floorColor = state.room.floorColor;
        this.ceilingColor = state.room.ceilingColor;
        
        // Et l'éclairage
        this.lightColor = state.lighting.color;
        this.lightIntensity = state.lighting.intensity;
        this.ambientLight = state.lighting.ambient;
      } catch (error) {
        console.error("Erreur lors de la synchronisation des données:", error);
      }
    }
  }
};
</script>

<style scoped>
.environment-container {
  height: 100vh;
  overflow: hidden
;}

/* Écran de bienvenue */
.welcome-screen {
  position: absolute;
  width: 100%;
  height: 100%;
  background: #f0f6ff;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.welcome-content {
  background: white;
  padding: 20px;
  border-radius: 20px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  max-width: 900px; /* Plus large */
  width: 92%;
  text-align: center;
}

.welcome-content h1 {
  color: #2b6bff;
  margin-bottom: 10px;
  font-size: 2rem;
  font-weight: bold;
}

.welcome-image {
  margin: 5px auto 15px;
}

.intro-text {
  font-size: 1.2rem;
  color: #444;
  line-height: 1.3;
  margin-bottom: 15px;
  font-weight: 500;
}

.welcome-content p {
  margin-bottom: 30px;
  color: #555;
  line-height: 1.5;
}

.object-categories {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}

.category-option {
  width: calc(33% - 7px);
  background: #f8f8f8;
  border: 2px solid #ddd;
  border-radius: 8px;
  padding: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
}

.category-option:hover {
  background: #f0f0f0;
  transform: translateY(-2px);
}

.category-option.selected {
  border-color: #2b6bff;
  background: #e6f0ff;
}

.category-icon {
  font-size: 24px;
  background: white;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
}

.category-description {
  flex-grow: 1;
}

.category-description p {
  margin: 0;
  color: #555;
  font-size: 0.9rem;
  line-height: 1.4;
}

.category-label {
  font-size: 0.9rem;
  color: #555;
}

.loading-indicator {
  margin-top: 15px;
  padding: 10px;
  background: #f8f8f8;
  border-radius: 8px;
}

.loading-bar {
  height: 8px;
  background: #eee;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 5px;
}

.loading-progress {
  height: 100%;
  background: #2b6bff;
  border-radius: 4px;
  transition: width 0.3s ease;
}

.loading-text {
  font-size: 0.8rem;
  color: #666;
  text-align: center;
}

.activity-explanation {
  text-align: center;
  margin: 15px 0 20px;
}

.activity-explanation h2 {
  font-size: 1.4rem;
  color: #2b6bff;
  margin-bottom: 15px;
  background: #f0f6ff;
  padding: 8px 15px;
  border-radius: 10px;
  display: inline-block;
}

.explanation-steps {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  gap: 15px;
  margin: 15px 0;
}

.explanation-step {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #f8f8f8;
  padding: 10px;
  border-radius: 15px;
  width: 30%;
  min-width: 200px;
  max-width: 250px;
}

.step-number {
  background: #2b6bff;
  color: white;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.step-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  flex-grow: 1;
}

.step-content h3 {
  margin: 0 0 5px;
  font-size: 1.1rem;
  color: #333;
  line-height: 1.2;
}

.step-image {
  align-self: center;
  margin-top: 8px;
  width: 50%;
}

.step-content p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.important-note {
  background: #fff5e6;
  border: 3px solid #ffcc80;
  padding: 12px 15px;
  margin-top: 20px;
  border-radius: 15px;
  text-align: center;
}

.important-note h3 {
  color: #ff8f00;
  margin: 0 0 8px;
  font-size: 1.2rem;
}

.important-note p {
  margin: 5px 0;
  color: #555;
  font-size: 1rem;
  line-height: 1.3;
}

.important-note p:last-child {
  margin-bottom: 0;
}

.important-points {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}

.important-point {
  background: rgba(255, 255, 255, 0.7);
  padding: 5px 10px;
  border-radius: 8px;
  flex: 1;
  min-width: 150px;
  max-width: 200px;
}

/* Interface principale */
.main-interface {
  height: 100vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* Barre de progression */
.progress-bar-container {
  padding: 15px;
  background: white;
  border-bottom: 1px solid #e9ecef;
}

.progress-steps {
  display: flex;
  justify-content: space-between;
  position: relative;
  margin-bottom: 10px;
}

.progress-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 20%;
  position: relative;
  z-index: 2;
}

.step-dot {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #e0e0e0;
  border: 2px solid white;
  margin-bottom: 5px;
  transition: all 0.3s;
}

.progress-step.completed .step-dot {
  background: #4caf50;
}

.progress-step.current .step-dot {
  background: #3a57e8;
  transform: scale(1.2);
  box-shadow: 0 0 0 4px rgba(58, 87, 232, 0.2);
}

.step-label {
  font-size: 0.8rem;
  color: #888;
  text-align: center;
  transition: all 0.3s;
}

.progress-step.current .step-label {
  color: #3a57e8;
  font-weight: 600;
}

.progress-step.completed .step-label {
  color: #4caf50;
}

.progress-line {
  height: 4px;
  background: #e0e0e0;
  position: relative;
  z-index: 1;
  border-radius: 2px;
  overflow: hidden;
}

.progress-filled {
  height: 100%;
  background: #3a57e8;
  transition: width 0.4s ease;
}

/* Sélecteur d'environnement (masqué mais gardé pour la structure) */
.environment-selector {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  margin: 15px 0;
  width: 100%;
}

/* Vue de l'environnement */
.environment-view {
  height: calc(100vh); /* Hauteur totale de la fenêtre moins une marge de sécurité */
  overflow: hidden;
  display: flex;
}

.room-visualization {
  flex-grow: 1;
  position: relative;
}

/* Guide overlay */
.guide-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  z-index: 10;
  padding-top: 10%; /* Espace en haut */
  backdrop-filter: blur(3px); /* Effet de flou léger */
  animation: fadeIn 0.3s ease-out;
  will-change: opacity;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.guide-content {
  background: linear-gradient(to bottom, #ffffff, #f7f9ff);
  padding: 20px 25px;
  border-radius: 20px;
  max-width: 500px;
  width: 90%;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(58, 87, 232, 0.1);
  border-top: 4px solid #4caf50;
  position: relative;
  animation: slideDown 0.4s ease-out;
  transform-origin: top center;
  will-change: transform, opacity;
}

@keyframes slideDown {
  from { 
    transform: translateY(-20px) scale(0.95);
    opacity: 0; 
  }
  to { 
    transform: translateY(0) scale(1);
    opacity: 1; 
  }
}

.guide-content::before {
  content: "💡";  /* Icône d'ampoule */
  position: absolute;
  top: -15px;
  left: 20px;
  font-size: 24px;
  background: white;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.guide-content h3 {
  margin: 0 0 12px;
  color: #2b6bff;
  font-size: 1.3rem;
  font-weight: bold;
}

.guide-content p {
  margin: 0 0 20px;
  color: #555;
  font-size: 1.05rem;
  line-height: 1.4;
}

.guide-button {
  padding: 10px 20px;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  transition: transform 0.2s, background 0.2s;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}

/* Contrôles de l'environnement */
.environment-controls {
  width: 320px;
  background: white;
  box-shadow: -2px 0 10px rgba(0, 0, 0, 0.05);
  padding: 10px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.environment-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.environment-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.4rem;
}

.step-indicator {
  text-align: right;
}

.step-indicator span {
  font-size: 0.8rem;
  color: #888;
  margin-bottom: 5px;
  display: block;
}

.step-dots {
  display: flex;
  gap: 5px;
}

.step-dots .step-dot {
  width: 8px;
  height: 8px;
  background: #e0e0e0;
  margin: 0;
}

.step-dots .step-dot.active {
  background: #3a57e8;
}

.env-description {
  margin-bottom: 20px;
  color: #666;
  font-size: 0.9rem;
  line-height: 1.5;
}

/* Onglets de contrôle */
.control-tabs {
  display: flex;
  border-bottom: 1px solid #e9ecef;
  margin-bottom:.0px;
  flex-wrap: wrap;
}

.tab-button {
  padding: 10px 15px;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  font-size: 0.9rem;
  color: #666;
  transition: all 0.2s;
  margin-right: 5px;
}

.tab-button:hover {
  color: #333;
}

.tab-button.active {
  color: #3a57e8;
  border-bottom-color: #3a57e8;
}

.tab-button.completed:not(.active)::after {
  content: "✓";
  position: absolute;
  top: 3px;
  right: 3px;
  font-size: 0.7rem;
  color: #4caf50;
  background: white;
  border-radius: 50%;
  width: 14px;
  height: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tab-button.disabled {
  color: #ccc;
  cursor: not-allowed;
}

/* Contenu des onglets */
.control-panel {
  padding-top: 20px;
}

.control-group {
  margin-bottom: 25px;
}

.control-group h3 {
  margin: 0 0 15px;
  font-size: 1.1rem;
  color: #444;
}

.control-item {
  margin-bottom: 15px;
}

.control-item label {
  display: block;
  margin-bottom: 8px;
  font-size: 0.9rem;
  color: #555;
}

.environment-info {
  margin-top: 20px;
}

.object-info {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
  margin-top: 10px;
}

.environment-objects {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.object-category-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

/* Contrôles pour la lumière */
.light-presets {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 5px;
}

.preset-btn {
  width: calc(33% - 7px);
  height: 40px;
  border: 2px solid transparent;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.2s;
}

.preset-btn.selected {
  border-color: #3a57e8;
  box-shadow: 0 0 0 2px rgba(58, 87, 232, 0.3);
}

.preset-btn span {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  font-size: 0.7rem;
  padding: 2px 0;
  text-align: center;
}

/* Contrôles pour les couleurs */
.color-palettes {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 15px;
}

.color-palette {
  width: calc(33% - 7px);
  cursor: pointer;
  border: 2px solid transparent;
  border-radius: 6px;
  padding: 5px;
  transition: all 0.2s;
}

.color-palette.selected {
  border-color: #3a57e8;
  box-shadow: 0 0 0 2px rgba(58, 87, 232, 0.3);
}

.palette-preview {
  display: flex;
  height: 30px;
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 5px;
}

.color-preview {
  flex: 1;
  height: 100%;
}

.color-palette span {
  display: block;
  text-align: center;
  font-size: 0.8rem;
  color: #555;
}

/* Contrôles génériques */
select, textarea, input[type="text"] {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.9rem;
}

.radio-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.radio-group label {
  display: flex;
  align-items: center;
  margin: 0;
}

.radio-group input {
  margin-right: 8px;
}

.slider-control {
  margin-bottom: 15px;
}

.slider-control label {
  display: block;
  margin-bottom: 5px;
  font-size: 0.9rem;
  color: #555;
}

.slider-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.7rem;
  color: #999;
  margin-top: 5px;
}

.toggle-control {
  display: flex;
  align-items: center;
}

.toggle-control input {
  margin-right: 10px;
}

/* Navigation entre onglets */
.tab-navigation {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.prev-button, .next-button {
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.prev-button {
  background: #f0f0f0;
  border: 1px solid #ddd;
  color: #555;
}

.prev-button:hover {
  background: #e0e0e0;
}

.next-button {
  background: #3a57e8;
  border: 1px solid #304dc9;
  color: white;
}

.next-button:hover {
  background: #304dc9;
}

.next-button:disabled {
  background: #a4b0e5;
  border-color: #a4b0e5;
  cursor: not-allowed;
}

/* Mood selection */
.mood-selection {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
  margin-bottom: 20px;
}

.mood-option {
  width: calc(33% - 7px);
  background: #f8f8f8;
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 10px 5px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}

.mood-option.selected {
  background: #e6f3ff;
  border-color: #3a57e8;
}

.mood-emoji {
  font-size: 1.8em;
  margin-bottom: 5px;
}

.mood-label {
  font-size: 0.8em;
}

/* Boutons */
.primary-button {
  width: auto;
  min-width: 200px;
  max-width: 300px;
  padding: 12px 20px;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  font-size: 1.2rem;
  font-weight: bold;
  transition: transform 0.2s, background 0.2s;
  margin: 15px auto 0;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.primary-button2 {
  width: auto;
  height: 60%;
  padding: 12px 20px;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  font-size: 1.2rem;
  font-weight: bold;
  transition: transform 0.2s, background 0.2s;
  margin: 15px auto 0;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.primary-button:hover {
  background: #3d8b40;
  transform: scale(1.05);
}

.primary-button:disabled {
  background: #a4b0e5;
  cursor: not-allowed;
}

/* Message de feedback */
.feedback-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.feedback-message {
  background: white;
  padding: 30px;
  border-radius: 12px;
  max-width: 600px;
  width: 90%;
  text-align: center;
  max-height: 90vh;
  overflow-y: auto;
}

.feedback-message h3 {
  color: #3a57e8;
  margin-top: 0;
  margin-bottom: 10px;
}

.preference-summary {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin: 20px 0;
  text-align: left;
}

.preference-summary h4 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #444;
}

.preference-summary p {
  margin: 5px 0;
  color: #555;
}

.recommendation-box {
  background: #e6f3ff;
  border-radius: 8px;
  padding: 15px;
  margin: 20px 0;
  text-align: left;
}

.recommendation-box h4 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #3a57e8;
}

.recommendation-box p {
  margin: 5px 0;
  color: #555;
}

.recommendation-box ul {
  padding-left: 20px;
}

.recommendation-box li {
  margin-bottom: 10px;
  color: #333;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: white;
  border-bottom: 1px solid #e9ecef;
}

.main-title {
  margin: 0;
  color: #2b6bff;
  font-size: 1.5rem;
}

.change-env-button {
  padding: 8px 15px;
  background: #3a57e8;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.2s;
}

.change-env-button:hover {
  background: #304dc9;
}

.change-env-button-small {
  padding: 5px 10px;
  background: #f0f0f0;
  color: #555;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s;
}

.change-env-button-small:hover {
  background: #e0e0e0;
}

.environment-selector-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  backdrop-filter: blur(3px);
}

.environment-selector-container {
  background: white;
  padding: 30px;
  border-radius: 12px;
  max-width: 900px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.environment-selector-container h2 {
  color: #2b6bff;
  margin-top: 0;
  margin-bottom: 20px;
  text-align: center;
}

.environment-selector {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  margin: 15px 0;
}

.environment-card {
  flex: 0 1 calc(33.333% - 20px); /* Pour avoir 3 cartes par ligne */
  min-width: 220px; /* Largeur minimale pour les petits écrans */
  max-width: 280px;
  background: #f8f9fa;
  border-radius: 10px;
  overflow: hidden;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  margin-bottom: 15px;
}

.env-card-image {
  height: 160px;
  width: 100%;
  object-fit: cover; /* Pour s'assurer que l'image couvre bien l'espace sans déformation */
  display: block;
  transition: transform 0.3s ease;
}

.environment-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.env-card-header {
  position: relative;
  overflow: hidden; /* Pour masquer le débordement lors du zoom */
}

.environment-card.active {
  border: 2px solid #3a57e8;
}

.env-card-color {
  height: 100px;
  width: 100%;
}

.environment-card h3 {
  margin: 10px 15px;
  color: #333;
}

.environment-card p {
  margin: 0 15px 15px;
  color: #666;
  font-size: 0.9rem;
}

.env-icon {
  position: absolute;
  top: 10px;
  left: 10px;
  font-size: 24px;
  background: rgba(255, 255, 255, 0.9);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.secondary-button {
  padding: 10px 15px;
  background: #f0f0f0;
  color: #555;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
  display: block;
  margin: 0 auto;
}

.secondary-button:hover {
  background: #e0e0e0;
}

.finish-exploration {
  text-align: center;
}

/* Responsive */
@media screen and (max-width: 600px) {
  .main-interface {
    flex-direction: column;
  }
  
  .environment-view {
    flex-direction: column;
  }
  
  .room-visualization {
    height: 50vh;
  }
  
  .environment-controls {
    width: 100%;
    height: auto;
    max-height: 40vh;
  }
  
  .progress-step .step-label {
    display: none;
  }

  .welcome-content h1 {
    font-size: 1.8rem;
  }
  
  .explanation-steps {
    flex-direction: column;
    align-items: center;
  }
  
  .explanation-step {
    width: 90%;
    max-width: none;
  }
  
  .important-points {
    flex-direction: column;
  }
  
  .important-point {
    max-width: none;
  }
  
  .step-content {
    align-items: center;
  }
}
</style>