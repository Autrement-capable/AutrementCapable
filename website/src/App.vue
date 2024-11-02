<template>
  <div id="app" class="app-container" :class="{ 'dyslexia-mode': isDyslexiaMode }">
    <router-view></router-view>
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
      <div v-if="isDyslexiaMode" class="dyslexia-mode" style="color: red;">Dyslexia Mode Activated</div>
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
  methods: {
    toggleWidget() {
      this.showWidget = !this.showWidget;
    },
    toggleTextToSpeech() {
      // Add text-to-speech functionality here
    },
    toggleVoiceNavigation() {
      // Add voice navigation functionality here
    },
    toggleDyslexiaMode() {
      this.isDyslexiaMode = !this.isDyslexiaMode;
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
      const clickableElements = document.querySelectorAll('a, button');
      clickableElements.forEach(element => {
        element.classList.toggle('highlight-clickable');
      });
    }
  }
};
</script>

<style>
body {
  cursor: default;
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
  gap: 10px;
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
