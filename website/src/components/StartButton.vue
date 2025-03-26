<template>
  <div class="start-button" aria-label="Start page">
    <!-- Show loading spinner during authentication check -->
    <div v-if="checking" class="loading-spinner">
      <div class="spinner"></div>
      <p>Vérification de connexion...</p>
    </div>
    
    <!-- Show content only if no passkey is found or authentication fails -->
    <template v-else>
      <h1 class="main-title">Autrement Capable</h1>
      <button @click="startProcess" aria-label="Commencez le processus">Commencer</button>
      <!-- <button @click="speakText" aria-label="Écoutez le texte">Écouter le texte</button> -->
    </template>
  </div>
</template>

<script>
import AuthService from '@/services/AuthService';

export default {
  data() {
    return {
      checking: true // Start with checking state
    }
  },
  async mounted() {
    // Try to authenticate with passkey on component mount
    await this.checkForExistingPasskeys();
  },
  methods: {
    async checkForExistingPasskeys() {
      try {
        this.checking = true;
        
        // Use browserSupportsWebAuthn from SimpleWebAuthn to check support first
        const { browserSupportsWebAuthn } = await import('@simplewebauthn/browser');
        
        // If browser doesn't support WebAuthn, show the start page
        if (!browserSupportsWebAuthn()) {
          console.log('Browser does not support WebAuthn/passkeys');
          this.checking = false;
          return;
        }
        
        // Try to authenticate with existing passkey
        const result = await AuthService.authenticateWithPasskey();
        
        // If authentication successful, redirect based on onboarding status
        if (!result) {
          this.$router.push('/account-creation');
        } else {
          this.$router.push('/immersive-dashboard');
        }
      } catch (error) {
        // Authentication failed (no passkey found or user cancelled)
        console.log('No passkey found or authentication failed', error);
        this.checking = false;
      }
    },
    
    startProcess() {
      this.$router.push('/account-creation');
    },
    
    speakText() {
      const text = "Bienvenue sur Autrement Capable. Appuyez sur le bouton Commencer pour démarrer le processus de création de compte.";
      const speech = new SpeechSynthesisUtterance();
      speech.lang = 'fr-FR';
      speech.text = text;
      window.speechSynthesis.speak(speech);
    }
  }
}
</script>

<style>
@import url('@/assets/styles.css');

.start-button {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}

.main-title {
  font-family: 'Glacial Indifference', sans-serif;
  font-weight: bold;
  font-size: 3em;
  margin-bottom: 1em;
}

button {
  padding: 1em 2em;
  font-size: 1.2em;
  background-color: #007BFF;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin: 0.5em;
  transition: transform 0.3s ease, background-color 0.3s ease;
}

button:focus {
  outline: 2px solid #0056b3;
}

button:hover {
  transform: scale(1.05);
  background-color: #0056b3;
}

/* Loading spinner styles */
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.spinner {
  border: 4px solid rgba(0, 123, 255, 0.1);
  border-radius: 50%;
  border-top: 4px solid #007BFF;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 1em;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>