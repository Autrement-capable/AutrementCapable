<template>
  <div id="app" class="app-container" :class="{ 'dyslexia-mode': isDyslexiaMode }">
    <div class="content-wrapper">
      <router-view></router-view>
    </div>
    <div class="accessibility-widget" @click="toggleWidget">
      <i class="icon-accessibility"></i>
    </div>
    <AppFooter />
    <div v-if="showWidget" class="accessibility-options">
      <button @click="toggleTextToSpeech">Lire la page</button>
      <button @click="toggleVoiceNavigation">Navigation vocale</button>
      <button @click="toggleDyslexiaMode">Mode dyslexie</button>
      <button @click="makeCursorLarger">Agrandir le curseur</button>
      <button @click="toggleTextSize">Agrandir le texte</button>
      <button @click="toggleTextSpacing">Espacer le texte</button>
      <button @click="toggleHighlightClickable">Surligner les éléments cliquables</button>
      <button @click="toggleReadingMask">Masque de lecture</button>
      <button @click="toggleReadingGuide">Guide de lecture</button>
      <button @click="alignText('left')">Aligner à gauche</button>
      <button @click="alignText('center')">Aligner au centre</button>
      <button @click="alignText('right')">Aligner à droite</button>
    </div>
  </div>
</template>

<script>
import AppFooter from './components/Footer.vue'

export default {
  name: 'App',
  components: {
    AppFooter
  },
  data() {
    return {
      showWidget: false,
      isDyslexiaMode: false,
      isLargeCursor: false,
    };
  },
  watch: {
    $route() {
      if (this.isHighlightClickable) {
        this.$nextTick(() => {
          this.highlightClickableElements();
        });
      }
    }
  },
  methods: {
    toggleWidget() {
      this.showWidget = !this.showWidget;
    },

    alignText(alignment) {
      document.body.classList.remove('align-left', 'align-center', 'align-right');
      document.body.classList.add(`align-${alignment}`);
    },

    toggleReadingGuide() {
      this.showReadingGuide = !this.showReadingGuide;
      if (this.showReadingGuide) {
        this.createReadingGuide();
      } else {
        this.removeReadingGuide();
      }
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
        const guideHeight = 30; // Adjust the height of the reading guide to be shorter
        const guideWidth = window.innerWidth * 0.5; // Set guide width to 50% of the window width
        const guideTop = event.clientY - guideHeight / 2;
        const guideLeft = event.clientX - guideWidth / 2; // Adjust left position based on the mouse movement

        guide.style.top = `${guideTop}px`;
        guide.style.left = `${guideLeft}px`; // Allow the guide to move horizontally
        guide.style.width = `${guideWidth}px`; // Set the width of the guide
      }
    },

    toggleReadingMask() {
      this.showReadingMask = !this.showReadingMask;
      if (this.showReadingMask) {
        this.createReadingMask();
      } else {
        this.removeReadingMask();
      }
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
      const maskHeight = 150; // Adjust the height of the reading mask here
      const maskTopPosition = event.clientY - maskHeight / 2;

      const maskTop = document.querySelector('.mask-top');
      const maskBottom = document.querySelector('.mask-bottom');
      const maskLeft = document.querySelector('.mask-left');
      const maskRight = document.querySelector('.mask-right');

      maskTop.style.height = `${maskTopPosition}px`;
      maskBottom.style.top = `${maskTopPosition + maskHeight}px`;
      maskBottom.style.height = `${window.innerHeight - (maskTopPosition + maskHeight)}px`;

      // Mask left and right regions
      maskLeft.style.height = `${maskHeight}px`;
      maskLeft.style.top = `${maskTopPosition}px`;
      maskRight.style.height = `${maskHeight}px`;
      maskRight.style.top = `${maskTopPosition}px`;
    },

    toggleTextToSpeech() {
      // Add text-to-speech functionality here
    },

    toggleVoiceNavigation() {
      // Add voice navigation functionality here
    },

    toggleDyslexiaMode() {
      this.isDyslexiaMode = !this.isDyslexiaMode;
      if (this.isDyslexiaMode) {
        document.body.classList.add('dyslexia-mode');
      } else {
        document.body.classList.remove('dyslexia-mode');
      }
    },

    makeCursorLarger() {
      this.isLargeCursor = !this.isLargeCursor;
      if (this.isLargeCursor) {
        document.body.classList.add('large-cursor');
      } else {
        document.body.classList.remove('large-cursor');
      }
    },

    toggleTextSize() {
      document.body.classList.toggle('large-text');
    },

    toggleTextSpacing() {
      document.body.classList.toggle('spaced-text');
    },

    toggleHighlightClickable() {
      this.isHighlightClickable = !this.isHighlightClickable;
      this.highlightClickableElements();
    },

    highlightClickableElements() {
      const clickableElements = document.querySelectorAll('a, button, .small-button');
      clickableElements.forEach(element => {
        if (this.isHighlightClickable) {
          element.classList.add('highlight-clickable');
        } else {
          element.classList.remove('highlight-clickable');
        }
      });
    }
  }
};
</script>

<style>
body {
  cursor: default;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
  padding-bottom: 60px; /* Ajustez cette valeur selon la hauteur exacte de votre footer */
}

.content-wrapper {
  flex: 1;
}

.large-cursor {
  cursor: crosshair;
}

.accessibility-widget {
  position: absolute;
  bottom: 80px;
  right: 20px;
  background-color: #007BFF;
  color: white;
  padding: 10px;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.accessibility-options {
  position: absolute;
  bottom: 140px;
  right: 20px;
  background-color: #FFF;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  padding: 20px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

button {
  padding: 10px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
