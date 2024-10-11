<template>
  <div id="app" class="app-container">
    <router-view></router-view>
    <div class="accessibility-widget" @click="toggleWidget">
      <i class="icon-accessibility"></i>
    </div>
    <AppFooter />
    <div v-if="showWidget" class="accessibility-options">
      <!-- Add your accessibility options here -->
      <button @click="toggleTextToSpeech">Lire la page</button>
      <button @click="toggleVoiceNavigation">Navigation vocale</button>
      <!-- Other options -->
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
      showWidget: false
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
    }
  }
};
</script>

<style>
.accessibility-widget {
  position: absolute;
  bottom: 80px; /* This ensures it's above the footer */
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
  bottom: 140px; /* Slightly higher to make room for the widget itself */
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
