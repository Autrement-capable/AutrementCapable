<template>
  <div id="app" class="app-container" 
       :class="{ 
         'dyslexia-mode': isDyslexiaMode, 
         'autism-mode': isAutismMode,
         'reduced-motion': isReducedMotion,
         'high-contrast': isHighContrast,
         'predictable-layout': isPredictableLayout
       }">
    <div class="content-wrapper">
      <router-view></router-view>
    </div>
    
    <!-- Widget Button with Icon -->
    <div 
      class="accessibility-widget" 
      @click="toggleWidget" 
      :class="{ 'active': showWidget }"
      aria-label="Options d'accessibilité"
      role="button"
      tabindex="0"
      @keydown.enter="toggleWidget"
    >
      <img src="@/assets/inclusive_icon.png" alt="Accessibilité" class="inclusive-icon" />
      <span class="tooltip">Accessibilité</span>
    </div>

    <!-- Options Panel with Categories -->
    <div v-if="showWidget" class="accessibility-panel">
      <div class="panel-header">
        <h2>Options d'accessibilité</h2>
        <button @click="toggleWidget" class="close-button" aria-label="Fermer">×</button>
      </div>
      
      <div class="panel-tabs">
        <button 
          @click="activeTab = 'general'"
          :class="{ 'active-tab': activeTab === 'general' }"
        >
          Général
        </button>
        <button 
          @click="activeTab = 'autism'"
          :class="{ 'active-tab': activeTab === 'autism' }"
        >
          Autisme
        </button>
        <button 
          @click="activeTab = 'reading'"
          :class="{ 'active-tab': activeTab === 'reading' }"
        >
          Lecture
        </button>
        <button 
          @click="activeTab = 'visual'"
          :class="{ 'active-tab': activeTab === 'visual' }"
        >
          Visuel
        </button>
      </div>
      
      <!-- General Tab -->
      <div v-show="activeTab === 'general'" class="panel-content">
        <div class="option-item">
          <button @click="toggleTextToSpeech" :class="{ 'active-option': isTextToSpeech }">
            <span class="option-icon">🔊</span>
            <span class="option-text">Lire la page</span>
          </button>
        </div>
        <div class="option-item">
          <button @click="toggleVoiceNavigation" :class="{ 'active-option': isVoiceNavigation }">
            <span class="option-icon">🎤</span>
            <span class="option-text">Navigation vocale</span>
          </button>
        </div>
        <div class="option-item">
          <button @click="makeCursorLarger" :class="{ 'active-option': isLargeCursor }">
            <span class="option-icon">👆</span>
            <span class="option-text">Agrandir le curseur</span>
          </button>
        </div>
      </div>
      
      <!-- Autism Tab -->
      <div v-show="activeTab === 'autism'" class="panel-content">
        <div class="option-item">
          <button @click="toggleAutismMode" :class="{ 'active-option': isAutismMode }">
            <span class="option-icon">🧩</span>
            <span class="option-text">Mode autisme</span>
          </button>
          <span class="option-description">Simplifie l'interface et réduit les distractions</span>
        </div>
        <div class="option-item">
          <button @click="toggleReducedMotion" :class="{ 'active-option': isReducedMotion }">
            <span class="option-icon">⏸️</span>
            <span class="option-text">Réduire les animations</span>
          </button>
          <span class="option-description">Désactive les animations qui peuvent être distrayantes</span>
        </div>
        <div class="option-item">
          <button @click="togglePredictableLayout" :class="{ 'active-option': isPredictableLayout }">
            <span class="option-icon">📏</span>
            <span class="option-text">Mise en page prévisible</span>
          </button>
          <span class="option-description">Maintient une structure constante et prévisible</span>
        </div>
        <div class="option-item">
          <button @click="toggleHighContrast" :class="{ 'active-option': isHighContrast }">
            <span class="option-icon">🔆</span>
            <span class="option-text">Contraste élevé</span>
          </button>
          <span class="option-description">Augmente le contraste pour une meilleure lisibilité</span>
        </div>
        <div class="option-item">
          <button @click="toggleQuitZone" :class="{ 'active-option': showQuitZone }">
            <span class="option-icon">🚪</span>
            <span class="option-text">Zone de pause</span>
          </button>
          <span class="option-description">Crée un espace visuel calme en cas de surcharge</span>
        </div>
        <div class="option-item">
          <button @click="toggleAudioFeedback" :class="{ 'active-option': audioFeedbackEnabled }">
            <span class="option-icon">🔊</span>
            <span class="option-text">Retour sonore</span>
          </button>
          <span class="option-description">Sons doux pour confirmer les actions</span>
        </div>
      </div>
      
      <!-- Reading Tab -->
      <div v-show="activeTab === 'reading'" class="panel-content">
        <div class="option-item">
          <button @click="toggleDyslexiaMode" :class="{ 'active-option': isDyslexiaMode }">
            <span class="option-icon">📖</span>
            <span class="option-text">Mode dyslexie</span>
          </button>
        </div>
        <div class="option-item">
          <button @click="toggleTextSize" :class="{ 'active-option': isLargeText }">
            <span class="option-icon">🔍</span>
            <span class="option-text">Agrandir le texte</span>
          </button>
        </div>
        <div class="option-item">
          <button @click="toggleTextSpacing" :class="{ 'active-option': isSpacedText }">
            <span class="option-icon">↔️</span>
            <span class="option-text">Espacer le texte</span>
          </button>
        </div>
        <div class="option-item">
          <button @click="toggleReadingMask" :class="{ 'active-option': showReadingMask }">
            <span class="option-icon">🎭</span>
            <span class="option-text">Masque de lecture</span>
          </button>
        </div>
        <div class="option-item">
          <button @click="toggleReadingGuide" :class="{ 'active-option': showReadingGuide }">
            <span class="option-icon">📏</span>
            <span class="option-text">Guide de lecture</span>
          </button>
        </div>
      </div>
      
      <!-- Visual Tab -->
      <div v-show="activeTab === 'visual'" class="panel-content">
        <div class="option-item">
          <button @click="toggleHighlightClickable" :class="{ 'active-option': isHighlightClickable }">
            <span class="option-icon">👆</span>
            <span class="option-text">Surligner les éléments cliquables</span>
          </button>
        </div>
        <div class="option-item">
          <label class="option-label">Alignement du texte:</label>
          <div class="button-group">
            <button @click="alignText('left')" class="small-button" :class="{ 'active-option': textAlignment === 'left' }">
              Gauche
            </button>
            <button @click="alignText('center')" class="small-button" :class="{ 'active-option': textAlignment === 'center' }">
              Centre
            </button>
            <button @click="alignText('right')" class="small-button" :class="{ 'active-option': textAlignment === 'right' }">
              Droite
            </button>
          </div>
        </div>
        <div class="option-item">
          <button @click="toggleColorTheme" :class="{ 'active-option': colorTheme !== 'default' }">
            <span class="option-icon">🎨</span>
            <span class="option-text">Thème de couleur: {{ colorThemeLabel }}</span>
          </button>
        </div>
      </div>
      
      <div class="panel-footer">
        <button @click="resetAllSettings" class="reset-button">Réinitialiser tous les paramètres</button>
      </div>
    </div>
    
    <!-- Quit Zone for sensory overload -->
    <div v-if="showQuitZone" class="quit-zone" @click="toggleQuitZone">
      <div class="quit-zone-content">
        <h2>Zone de pause</h2>
        <p>Prenez un moment pour vous calmer. Cliquez n'importe où pour revenir.</p>
        <div class="breathing-guide"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      // Panel state
      showWidget: false,
      activeTab: 'general',
      
      // General accessibility
      isTextToSpeech: false,
      isVoiceNavigation: false,
      isLargeCursor: false,
      
      // Autism specific modes
      isAutismMode: false,
      isReducedMotion: false,
      isHighContrast: false,
      isPredictableLayout: false,
      showQuitZone: false,
      
      // Reading modes
      isDyslexiaMode: false,
      isLargeText: false,
      isSpacedText: false,
      showReadingMask: false,
      showReadingGuide: false,
      
      // Visual preferences
      isHighlightClickable: false,
      textAlignment: 'left',
      colorTheme: 'default',
      
      // Speech synthesis
      speechSynthesis: null,
      speechUtterance: null,
      
      // Audio context for feedback sounds
      audioContext: null,
      // Audio feedback preferences
      audioFeedbackEnabled: true
    };
  },
  
  computed: {
    colorThemeLabel() {
      const themes = {
        'default': 'Standard',
        'warm': 'Chaleureux',
        'cool': 'Apaisant',
        'dark': 'Sombre',
        'monochrome': 'Monochrome'
      };
      return themes[this.colorTheme];
    }
  },
  
  mounted() {
    // Load user preferences from localStorage if available
    this.loadUserPreferences();
    
    // Initialize speech synthesis
    if ('speechSynthesis' in window) {
      this.speechSynthesis = window.speechSynthesis;
    }
  },
  
  watch: {
    $route() {
      if (this.isHighlightClickable) {
        this.$nextTick(() => {
          this.highlightClickableElements();
        });
      }
      
      // Apply predictable layout for autism mode when route changes
      if (this.isPredictableLayout) {
        this.$nextTick(() => {
          this.applyPredictableLayout();
        });
      }
    }
  },
  
  methods: {
    toggleWidget() {
      const wasOpen = this.showWidget;
      this.showWidget = !this.showWidget;
      
      // Play a soft sound for feedback if audio is enabled
      if (this.audioFeedbackEnabled) {
        if (this.showWidget) {
          this.playAudioFeedback('open');
        } else if (wasOpen) {
          this.playAudioFeedback('close');
        }
      }
    },
    
    // ===== General Settings =====
    toggleTextToSpeech() {
      this.isTextToSpeech = !this.isTextToSpeech;
      
      if (this.isTextToSpeech) {
        this.readPageContent();
      } else if (this.speechSynthesis) {
        this.speechSynthesis.cancel();
      }
      
      this.saveUserPreferences();
    },
    
    readPageContent() {
      if (!this.speechSynthesis) return;
      
      // Get main content excluding navigation and widgets
      const mainContent = document.querySelector('.content-wrapper');
      if (!mainContent) return;
      
      const textToRead = mainContent.textContent.trim();
      
      // Create utterance with user-friendly settings
      this.speechUtterance = new SpeechSynthesisUtterance(textToRead);
      this.speechUtterance.rate = 0.9; // Slightly slower rate for better comprehension
      this.speechUtterance.pitch = 1;
      
      // Use a French voice if available
      const voices = this.speechSynthesis.getVoices();
      const frenchVoice = voices.find(voice => voice.lang.includes('fr'));
      if (frenchVoice) {
        this.speechUtterance.voice = frenchVoice;
      }
      
      this.speechSynthesis.speak(this.speechUtterance);
    },
    
    toggleVoiceNavigation() {
      this.isVoiceNavigation = !this.isVoiceNavigation;
      
      if (this.isVoiceNavigation) {
        this.initializeVoiceNavigation();
      } else {
        this.disableVoiceNavigation();
      }
      
      this.saveUserPreferences();
    },
    
    initializeVoiceNavigation() {
      // Check if the Web Speech API is supported
      if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        alert('Votre navigateur ne supporte pas la reconnaissance vocale.');
        this.isVoiceNavigation = false;
        return;
      }
      
      // Implementation for voice commands would go here
      // This is a placeholder for actual implementation
    },
    
    disableVoiceNavigation() {
      // Code to disable voice navigation
    },
    
    makeCursorLarger() {
      this.isLargeCursor = !this.isLargeCursor;
      
      if (this.isLargeCursor) {
        document.body.classList.add('large-cursor');
      } else {
        document.body.classList.remove('large-cursor');
      }
      
      this.saveUserPreferences();
    },
    
    // ===== Autism Specific Methods =====
    toggleAutismMode() {
      this.isAutismMode = !this.isAutismMode;
      
      if (this.isAutismMode) {
        // Apply autism-friendly settings
        this.isReducedMotion = true;
        this.isPredictableLayout = true;
        document.body.classList.add('autism-friendly');
        this.applyAutismFriendlyStyles();
        
        // Play audio feedback
        if (this.audioFeedbackEnabled) {
          this.playAudioFeedback('toggle-on');
        }
      } else {
        document.body.classList.remove('autism-friendly');
        
        // Play audio feedback
        if (this.audioFeedbackEnabled) {
          this.playAudioFeedback('toggle-off');
        }
      }
      
      this.saveUserPreferences();
    },
    
    applyAutismFriendlyStyles() {
      // Simplify layout
      this.reduceAnimations();
      this.applyPredictableLayout();
      
      // Apply clearer font and spacing for better readability
      document.body.style.setProperty('--autism-font', '"Open Sans", "Arial", sans-serif');
      document.body.style.setProperty('--autism-line-height', '1.5');
      document.body.style.setProperty('--autism-paragraph-spacing', '1.2em');
    },
    
    toggleReducedMotion() {
      this.isReducedMotion = !this.isReducedMotion;
      this.reduceAnimations();
      this.saveUserPreferences();
    },
    
    reduceAnimations() {
      if (this.isReducedMotion) {
        document.body.classList.add('reduced-motion');
      } else {
        document.body.classList.remove('reduced-motion');
      }
    },
    
    togglePredictableLayout() {
      this.isPredictableLayout = !this.isPredictableLayout;
      this.applyPredictableLayout();
      this.saveUserPreferences();
    },
    
    applyPredictableLayout() {
      if (this.isPredictableLayout) {
        document.body.classList.add('predictable-layout');
        
        // Apply consistent spacing and structure
        const sections = document.querySelectorAll('section, article, div.content-section');
        sections.forEach(section => {
          section.style.margin = '1.5rem 0';
          section.style.padding = '1rem';
          section.style.borderRadius = '8px';
        });
      } else {
        document.body.classList.remove('predictable-layout');
      }
    },
    
    toggleHighContrast() {
      this.isHighContrast = !this.isHighContrast;
      
      if (this.isHighContrast) {
        document.body.classList.add('high-contrast');
      } else {
        document.body.classList.remove('high-contrast');
      }
      
      this.saveUserPreferences();
    },
    
    toggleQuitZone() {
      this.showQuitZone = !this.showQuitZone;
      
      if (this.showQuitZone) {
        // Pause any media and animations when the quit zone is active
        document.querySelectorAll('video, audio').forEach(media => {
          media.pause();
        });
        
        // Stop any running speech synthesis
        if (this.speechSynthesis && this.speechSynthesis.speaking) {
          this.speechSynthesis.cancel();
        }
        
        // Play a very gentle calming sound
        if (this.audioFeedbackEnabled) {
          this.playAudioFeedback('quit-zone');
        }
      }
    },
    
    playAudioFeedback(action) {
      // Create AudioContext only when needed (to avoid autoplay restrictions)
      if (!this.audioContext) {
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
      }
      
      // Different sound profiles based on action type
      let frequency, duration, type, volume;
      
      switch (action) {
        case 'open':
          // Gentle rising tone for opening panel
          frequency = 440; // A4 note (Hz)
          duration = 0.3;  // seconds
          type = 'sine';   // smooth waveform
          volume = 0.1;    // quiet (max is 1.0)
          this.playTone(frequency, frequency + 200, duration, type, volume);
          break;
          
        case 'close':
          // Gentle falling tone for closing panel
          frequency = 440;
          duration = 0.3;
          type = 'sine';
          volume = 0.1;
          this.playTone(frequency + 100, frequency, duration, type, volume);
          break;
          
        case 'toggle-on':
          // Short pleasant tone for enabling a feature
          frequency = 523.25; // C5 note (Hz)
          duration = 0.15;
          type = 'sine';
          volume = 0.1;
          this.playTone(frequency, frequency, duration, type, volume);
          break;
          
        case 'toggle-off':
          // Very soft tone for disabling a feature
          frequency = 392; // G4 note (Hz)
          duration = 0.15;
          type = 'sine';
          volume = 0.08;
          this.playTone(frequency, frequency, duration, type, volume);
          break;
          
        case 'error':
          // Gentle low tone for errors (non-jarring)
          frequency = 330; // E4 note (Hz)
          duration = 0.2;
          type = 'sine';
          volume = 0.1;
          this.playTone(frequency, frequency - 30, duration, type, volume);
          break;
          
        case 'quit-zone':
          // Very soft, calming tone for entering quiet zone
          frequency = 294; // D4 note (Hz)
          duration = 0.5;
          type = 'sine';
          volume = 0.05;
          this.playTone(frequency, frequency, duration, type, volume);
          break;
          
        default:
          // Default gentle feedback
          frequency = 440;
          duration = 0.2;
          type = 'sine';
          volume = 0.08;
          this.playTone(frequency, frequency, duration, type, volume);
      }
    },
    
    playTone(startFreq, endFreq, duration, type = 'sine', volume = 0.1) {
      // Safety check - make sure audioContext exists
      if (!this.audioContext) return;
      
      try {
        // Create oscillator and gain nodes
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        // Set initial values
        oscillator.type = type;
        oscillator.frequency.setValueAtTime(startFreq, this.audioContext.currentTime);
        
        // If start and end frequencies are different, create a frequency ramp
        if (startFreq !== endFreq) {
          oscillator.frequency.linearRampToValueAtTime(
            endFreq, 
            this.audioContext.currentTime + duration
          );
        }
        
        // Set volume with fade in/out to avoid clicks
        gainNode.gain.setValueAtTime(0, this.audioContext.currentTime);
        gainNode.gain.linearRampToValueAtTime(volume, this.audioContext.currentTime + 0.05);
        gainNode.gain.linearRampToValueAtTime(0, this.audioContext.currentTime + duration);
        
        // Connect nodes
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        // Play and automatically stop
        oscillator.start();
        oscillator.stop(this.audioContext.currentTime + duration);
        
        // Cleanup when done
        oscillator.onended = () => {
          oscillator.disconnect();
          gainNode.disconnect();
        };
      } catch (error) {
        console.error('Error playing audio feedback:', error);
      }
    },
    
    // ===== Reading Settings =====
    toggleDyslexiaMode() {
      this.isDyslexiaMode = !this.isDyslexiaMode;
      
      if (this.isDyslexiaMode) {
        document.body.classList.add('dyslexia-mode');
      } else {
        document.body.classList.remove('dyslexia-mode');
      }
      
      this.saveUserPreferences();
    },
    
    toggleTextSize() {
      this.isLargeText = !this.isLargeText;
      
      if (this.isLargeText) {
        document.body.classList.add('large-text');
      } else {
        document.body.classList.remove('large-text');
      }
      
      this.saveUserPreferences();
    },
    
    toggleTextSpacing() {
      this.isSpacedText = !this.isSpacedText;
      
      if (this.isSpacedText) {
        document.body.classList.add('spaced-text');
      } else {
        document.body.classList.remove('spaced-text');
      }
      
      this.saveUserPreferences();
    },
    
    toggleReadingMask() {
      this.showReadingMask = !this.showReadingMask;
      
      if (this.showReadingMask) {
        this.createReadingMask();
      } else {
        this.removeReadingMask();
      }
      
      this.saveUserPreferences();
    },
    
    createReadingMask() {
      const maskTop = document.createElement('div');
      const maskBottom = document.createElement('div');
      const maskLeft = document.createElement('div');
      const maskRight = document.createElement('div');

      maskTop.classList.add('reading-mask-overlay');
      maskBottom.classList.add('reading-mask-overlay');
      maskLeft.classList.add('reading-mask-overlay');
      maskRight.classList.add('reading-mask-overlay');

      maskTop.classList.add('mask-top');
      maskBottom.classList.add('mask-bottom');
      maskLeft.classList.add('mask-left');
      maskRight.classList.add('mask-right');

      document.body.appendChild(maskTop);
      document.body.appendChild(maskBottom);
      document.body.appendChild(maskLeft);
      document.body.appendChild(maskRight);

      document.addEventListener('mousemove', this.updateMaskPosition);
    },

    removeReadingMask() {
      const overlays = document.querySelectorAll('.reading-mask-overlay');
      overlays.forEach(overlay => {
        document.body.removeChild(overlay);
      });
      document.removeEventListener('mousemove', this.updateMaskPosition);
    },

    updateMaskPosition(event) {
      const maskHeight = 150;
      const maskTopPosition = event.clientY - maskHeight / 2;

      const maskTop = document.querySelector('.mask-top');
      const maskBottom = document.querySelector('.mask-bottom');
      const maskLeft = document.querySelector('.mask-left');
      const maskRight = document.querySelector('.mask-right');

      if (maskTop && maskBottom && maskLeft && maskRight) {
        maskTop.style.height = `${maskTopPosition}px`;
        maskBottom.style.top = `${maskTopPosition + maskHeight}px`;
        maskBottom.style.height = `${window.innerHeight - (maskTopPosition + maskHeight)}px`;

        maskLeft.style.height = `${maskHeight}px`;
        maskLeft.style.top = `${maskTopPosition}px`;
        maskRight.style.height = `${maskHeight}px`;
        maskRight.style.top = `${maskTopPosition}px`;
      }
    },
    
    toggleReadingGuide() {
      this.showReadingGuide = !this.showReadingGuide;
      
      if (this.showReadingGuide) {
        this.createReadingGuide();
      } else {
        this.removeReadingGuide();
      }
      
      this.saveUserPreferences();
    },

    createReadingGuide() {
      const guide = document.createElement('div');
      guide.classList.add('reading-guide');
      document.body.appendChild(guide);

      document.addEventListener('mousemove', this.updateGuidePosition);
    },

    removeReadingGuide() {
      const guide = document.querySelector('.reading-guide');
      if (guide) {
        document.body.removeChild(guide);
        document.removeEventListener('mousemove', this.updateGuidePosition);
      }
    },

    updateGuidePosition(event) {
      const guide = document.querySelector('.reading-guide');
      if (guide) {
        const guideHeight = 30;
        const guideWidth = window.innerWidth * 0.5;
        const guideTop = event.clientY - guideHeight / 2;
        const guideLeft = event.clientX - guideWidth / 2;

        guide.style.top = `${guideTop}px`;
        guide.style.left = `${guideLeft}px`;
        guide.style.width = `${guideWidth}px`;
      }
    },
    
    // ===== Visual Settings =====
    toggleHighlightClickable() {
      this.isHighlightClickable = !this.isHighlightClickable;
      this.highlightClickableElements();
      this.saveUserPreferences();
    },

    highlightClickableElements() {
      const clickableElements = document.querySelectorAll('a, button, .small-button, [role="button"]');
      clickableElements.forEach(element => {
        if (this.isHighlightClickable) {
          element.classList.add('highlight-clickable');
        } else {
          element.classList.remove('highlight-clickable');
        }
      });
    },
    
    alignText(alignment) {
      this.textAlignment = alignment;
      
      document.body.classList.remove('align-left', 'align-center', 'align-right');
      document.body.classList.add(`align-${alignment}`);
      
      this.saveUserPreferences();
    },
    
    toggleColorTheme() {
      const themes = ['default', 'warm', 'cool', 'dark', 'monochrome'];
      const currentIndex = themes.indexOf(this.colorTheme);
      const nextIndex = (currentIndex + 1) % themes.length;
      this.colorTheme = themes[nextIndex];
      
      document.body.className = document.body.className.replace(/theme-\w+/g, '');
      document.body.classList.add(`theme-${this.colorTheme}`);
      
      this.saveUserPreferences();
    },
    
    toggleAudioFeedback() {
      this.audioFeedbackEnabled = !this.audioFeedbackEnabled;
      
      // Play feedback only if turning it ON (not when turning it off)
      if (this.audioFeedbackEnabled) {
        this.playAudioFeedback('toggle-on');
      }
      
      this.saveUserPreferences();
    },
    
    // ===== User Preferences =====
    saveUserPreferences() {
      // Save all user preferences to localStorage
      const preferences = {
        isAutismMode: this.isAutismMode,
        isReducedMotion: this.isReducedMotion,
        isPredictableLayout: this.isPredictableLayout,
        isHighContrast: this.isHighContrast,
        isDyslexiaMode: this.isDyslexiaMode,
        isLargeText: this.isLargeText,
        isSpacedText: this.isSpacedText,
        isLargeCursor: this.isLargeCursor,
        isHighlightClickable: this.isHighlightClickable,
        textAlignment: this.textAlignment,
        colorTheme: this.colorTheme,
        audioFeedbackEnabled: this.audioFeedbackEnabled
      };
      
      localStorage.setItem('accessibilityPreferences', JSON.stringify(preferences));
    },
    
    loadUserPreferences() {
      const savedPreferences = localStorage.getItem('accessibilityPreferences');
      
      if (savedPreferences) {
        const preferences = JSON.parse(savedPreferences);
        
        // Apply saved preferences
        Object.keys(preferences).forEach(key => {
          if (this[key] !== undefined) {
            this[key] = preferences[key];
          }
        });
        
        // Apply loaded settings to the UI
        this.$nextTick(() => {
          if (this.isAutismMode) this.applyAutismFriendlyStyles();
          if (this.isReducedMotion) this.reduceAnimations();
          if (this.isPredictableLayout) this.applyPredictableLayout();
          if (this.isHighContrast) document.body.classList.add('high-contrast');
          if (this.isDyslexiaMode) document.body.classList.add('dyslexia-mode');
          if (this.isLargeText) document.body.classList.add('large-text');
          if (this.isSpacedText) document.body.classList.add('spaced-text');
          if (this.isLargeCursor) document.body.classList.add('large-cursor');
          if (this.isHighlightClickable) this.highlightClickableElements();
          
          document.body.classList.add(`align-${this.textAlignment}`);
          document.body.classList.add(`theme-${this.colorTheme}`);
        });
      }
    },
    
    resetAllSettings() {
      // Reset all settings to default
      this.isAutismMode = false;
      this.isReducedMotion = false;
      this.isPredictableLayout = false;
      this.isHighContrast = false;
      this.isDyslexiaMode = false;
      this.isLargeText = false;
      this.isSpacedText = false;
      this.isLargeCursor = false;
      this.isHighlightClickable = false;
      this.showReadingMask = false;
      this.showReadingGuide = false;
      this.textAlignment = 'left';
      this.colorTheme = 'default';
      
      // Remove all applied classes
      document.body.classList.remove(
        'autism-friendly', 'reduced-motion', 'predictable-layout',
        'high-contrast', 'dyslexia-mode', 'large-text', 'spaced-text',
        'large-cursor', 'align-left', 'align-center', 'align-right'
      );
      
      // Remove any applied themes
      document.body.className = document.body.className.replace(/theme-\w+/g, '');
      
      // Remove reading guides and masks
      this.removeReadingMask();
      this.removeReadingGuide();
      
      // Remove clickable highlights
      const clickableElements = document.querySelectorAll('.highlight-clickable');
      clickableElements.forEach(element => {
        element.classList.remove('highlight-clickable');
      });
      
      // Clear saved preferences
      localStorage.removeItem('accessibilityPreferences');
    }
  }
};
</script>

<style>
:root {
  --primary-color: #007BFF;
  --secondary-color: #6c757d;
  --autism-font: "Open Sans", "Arial", sans-serif;
  --autism-line-height: 1.5;
  --autism-paragraph-spacing: 1.2em;
  --panel-bg: #ffffff;
  --panel-text: #333333;
  --panel-border: #e0e0e0;
  --button-hover: #0056b3;
  --transition-duration: 0.3s;
}

body {
  cursor: default;
  transition: background-color var(--transition-duration), color var(--transition-duration);
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
}

.content-wrapper {
  flex: 1;
}

/* ===== Accessibility Widget ===== */
.accessibility-widget {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: var(--primary-color);
  color: white;
  padding: 8px;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
  transition: transform 0.2s ease-in-out, background-color 0.2s ease;
}

.accessibility-widget:hover {
  transform: scale(1.1);
}

.accessibility-widget.active {
  background-color: #0056b3;
}

.inclusive-icon {
  width: 36px;
  height: 36px;
}

.tooltip {
  position: absolute;
  top: -40px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 12px;
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s, visibility 0.3s;
}

.accessibility-widget:hover .tooltip {
  opacity: 1;
  visibility: visible;
}

/* ===== Accessibility Panel ===== */
.accessibility-panel {
  position: fixed;
  bottom: 100px;
  right: 20px;
  background-color: var(--panel-bg);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
  border-radius: 12px;
  width: 320px;
  max-height: 70vh;
  overflow-y: auto;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  border: 1px solid var(--panel-border);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid var(--panel-border);
}

.panel-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--panel-text);
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: var(--secondary-color);
  padding: 0;
  margin: 0;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.close-button:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.panel-tabs {
  display: flex;
  border-bottom: 1px solid var(--panel-border);
  background-color: #f8f9fa;
}

.panel-tabs button {
  flex: 1;
  background: none;
  border: none;
  padding: 10px;
  cursor: pointer;
  font-size: 14px;
  color: var(--panel-text);
  transition: background-color 0.2s;
}

.panel-tabs button:hover {
  background-color: rgba(0, 123, 255, 0.1);
}

.panel-tabs button.active-tab {
  border-bottom: 2px solid var(--primary-color);
  color: var(--primary-color);
  font-weight: 500;
}

.panel-content {
  padding: 12px 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.option-item {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.option-item button {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  background-color: #f0f0f0;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
  font-size: 14px;
  color: #333;
  text-align: left;
}

.option-item button:hover {
  background-color: #e6e6e6;
}

.option-item button.active-option {
  background-color: rgba(0, 123, 255, 0.15);
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.option-icon {
  font-size: 18px;
}

.option-text {
  flex: 1;
}

.option-description {
  font-size: 12px;
  color: #666;
  margin-left: 32px;
  margin-top: -2px;
}

.button-group {
  display: flex;
  gap: 5px;
}

.small-button {
  padding: 8px 12px;
  font-size: 13px;
  flex: 1;
}

.option-label {
  font-size: 14px;
  color: #555;
  margin-bottom: 4px;
}

.panel-footer {
  padding: 12px 16px;
  border-top: 1px solid var(--panel-border);
  display: flex;
  justify-content: center;
}

.reset-button {
  background-color: #f0f0f0;
  color: #666;
  border: 1px solid #ddd;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.reset-button:hover {
  background-color: #e0e0e0;
}

/* ===== Quit Zone for Sensory Overload ===== */
.quit-zone {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #f5f5f5;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.quit-zone-content {
  max-width: 500px;
  text-align: center;
  padding: 40px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.quit-zone-content h2 {
  margin-top: 0;
  color: #333;
}

.breathing-guide {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: #c9e6ff;
  margin: 24px auto;
  animation: breathing 6s infinite ease-in-out;
}

@keyframes breathing {
  0% { transform: scale(0.9); background-color: #c9e6ff; }
  25% { transform: scale(1); background-color: #94c9ff; }
  60% { transform: scale(0.9); background-color: #c9e6ff; }
  100% { transform: scale(0.9); background-color: #c9e6ff; }
}

/* ===== Various Mode Styles ===== */
/* Autism-friendly mode */
.autism-mode {
  font-family: var(--autism-font);
}

.autism-mode p, 
.autism-mode li, 
.autism-mode span, 
.autism-mode div {
  line-height: var(--autism-line-height);
}

.autism-mode p {
  margin-bottom: var(--autism-paragraph-spacing);
}

.autism-mode a {
  text-decoration: underline;
  font-weight: 500;
}

/* Reduced motion */
.reduced-motion * {
  animation-duration: 0.001ms !important;
  transition-duration: 0.001ms !important;
}

/* Predictable layout */
.predictable-layout * {
  border-radius: 8px;
}

.predictable-layout nav, 
.predictable-layout header, 
.predictable-layout footer {
  position: static !important;
}

/* High contrast mode */
.high-contrast {
  color: black !important;
  background-color: white !important;
}

.high-contrast * {
  color: black !important;
  background-color: white !important;
  border-color: black !important;
}

.high-contrast a, 
.high-contrast button {
  color: #0000EE !important;
  border: 2px solid #0000EE !important;
}

.high-contrast img {
  filter: grayscale(100%) contrast(200%);
}

/* Dyslexia mode */
.dyslexia-mode {
  font-family: 'OpenDyslexic', 'Comic Sans MS', cursive;
  font-size: 1.05em;
  letter-spacing: 0.05em;
  word-spacing: 0.1em;
}

.dyslexia-mode p {
  line-height: 1.7;
}

/* Large text */
.large-text {
  font-size: 120% !important;
}

.large-text h1 {
  font-size: 2.4em !important;
}

.large-text h2 {
  font-size: 2em !important;
}

.large-text h3 {
  font-size: 1.6em !important;
}

/* Spaced text */
.spaced-text {
  letter-spacing: 0.12em;
  word-spacing: 0.16em;
}

.spaced-text p, 
.spaced-text li {
  line-height: 1.8;
}

/* Large cursor */
.large-cursor {
  cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48" fill="none" stroke="black" stroke-width="4"><path d="M12,12 L36,36 M12,36 L36,12"/></svg>') 24 24, auto;
}

/* Text alignment */
.align-left {
  text-align: left;
}

.align-center {
  text-align: center;
}

.align-right {
  text-align: right;
}

/* Highlight clickable elements */
.highlight-clickable {
  box-shadow: 0 0 0 2px #ff9800 !important;
  position: relative;
}

.highlight-clickable::after {
  content: "";
  position: absolute;
  inset: -2px;
  border: 2px solid #ff9800;
  border-radius: 4px;
  pointer-events: none;
}

/* Reading mask and guide */
.reading-mask-overlay {
  position: fixed;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 998;
}

.mask-top {
  top: 0;
  left: 0;
  width: 100%;
}

.mask-bottom {
  bottom: 0;
  left: 0;
  width: 100%;
}

.mask-left {
  left: 0;
  width: 25%;
}

.mask-right {
  right: 0;
  width: 25%;
}

.reading-guide {
  position: fixed;
  height: 30px;
  background-color: rgba(255, 255, 0, 0.2);
  border: 1px solid rgba(255, 215, 0, 0.5);
  z-index: 997;
  pointer-events: none;
}

/* Color Themes */
.theme-warm {
  background-color: #fffaf0;
  color: #5d4037;
}

.theme-warm a {
  color: #d84315;
}

.theme-warm button:not(.active-option) {
  background-color: #ffccbc;
}

.theme-cool {
  background-color: #f1f8ff;
  color: #37474f;
}

.theme-cool a {
  color: #0288d1;
}

.theme-cool button:not(.active-option) {
  background-color: #bbdefb;
}

.theme-dark {
  background-color: #121212;
  color: #e0e0e0;
}

.theme-dark a {
  color: #90caf9;
}

.theme-dark button:not(.active-option) {
  background-color: #2c2c2c;
  color: #e0e0e0;
}

.theme-dark .accessibility-panel {
  background-color: #1e1e1e;
  border-color: #333;
}

.theme-dark .panel-header,
.theme-dark .panel-footer {
  border-color: #333;
}

.theme-dark .panel-header h2 {
  color: #e0e0e0;
}

.theme-dark .panel-tabs {
  background-color: #2c2c2c;
}

.theme-monochrome {
  filter: grayscale(100%);
}

/* Responsive design for mobile */
@media (max-width: 768px) {
  .accessibility-panel {
    width: 90%;
    max-width: 320px;
    max-height: 60vh;
    right: 5%;
  }
  
  .accessibility-widget {
    bottom: 10px;
    right: 10px;
  }
  
  .panel-content {
    padding: 10px;
  }
  
  .option-item button {
    padding: 8px 10px;
  }
}

</style>