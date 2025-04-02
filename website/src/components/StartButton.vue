<template>
  <div class="start-button" aria-label="Start page">
    <!-- Show loading spinner during authentication check -->
    <div v-if="checking" class="loading-spinner">
      <div class="spinner"></div>
      <p>Vérification de connexion...</p>
    </div>
    
    <!-- Show authenticated welcome if user is logged in -->
    <div v-else-if="isAuthenticated" class="authenticated-welcome">
      <h1 class="main-title">Bienvenue sur Autrement Capable</h1>
      <p>Vous êtes déjà connecté</p>
      <button @click="goToDashboard" class="primary-button">Accéder au tableau de bord</button>
      <button @click="logout" class="secondary-button">Se déconnecter</button>
    </div>
    
    <!-- Show authentication options if not authenticated -->
    <div v-else-if="showOptions" class="auth-options">
      <h1 class="main-title">Autrement Capable</h1>
      <div class="options-container">
        <div class="option-card">
          <h2>J'ai déjà un compte</h2>
          <button @click="login" class="primary-button">Se connecter</button>
        </div>
        <div class="option-card">
          <h2>Je suis nouveau</h2>
          <button @click="goToAccountCreation" class="primary-button">Créer un compte</button>
        </div>
      </div>
      <button @click="speakText" class="accessibility-button" aria-label="Écoutez le texte">
        <span class="icon">🔊</span> Écouter
      </button>
    </div>
    
    <!-- Initial welcome screen -->
    <div v-else class="welcome-screen">
      <h1 class="main-title">Autrement Capable</h1>
      <button @click="showAuthOptions" class="primary-button" aria-label="Commencez le processus">Commencer</button>
      <button @click="speakText" class="accessibility-button" aria-label="Écoutez le texte">
        <span class="icon">🔊</span> Écouter
      </button>
    </div>
  </div>
</template>

<script>
import AuthService from '@/services/AuthService';
import { browserSupportsWebAuthn } from '@simplewebauthn/browser';

export default {
  data() {
    return {
      checking: true,
      isAuthenticated: false,
      showOptions: false,
      supportsWebAuthn: false
    }
  },
  async mounted() {
    // Check browser support for WebAuthn
    try {
      this.supportsWebAuthn = browserSupportsWebAuthn();
    } catch (error) {
      console.error('Error checking WebAuthn support:', error);
      this.supportsWebAuthn = false;
    }
    
    // Check if user is already authenticated
    await this.checkAuthentication();
  },
  methods: {
    async checkAuthentication() {
      this.checking = true;
      
      try {
        // First check if we have a valid access token
        if (AuthService.isAuthenticated()) {
          this.isAuthenticated = true;
          this.checking = false;
          return;
        }
        
        // If no valid access token, try to refresh using the cookie
        try {
          await AuthService.refreshAccessToken();
          this.isAuthenticated = true;
        } catch (error) {
          console.log('No valid refresh token found');
          this.isAuthenticated = false;
        }
      } catch (error) {
        console.error('Authentication check failed:', error);
        this.isAuthenticated = false;
      } finally {
        this.checking = false;
      }
    },
    
    showAuthOptions() {
      this.showOptions = true;
    },
    
    async login() {
      try {
        if (this.supportsWebAuthn) {
          // Try to authenticate with passkey
          await AuthService.authenticateWithPasskey();
          this.goToDashboard();
        } else {
          // Redirect to password login page for browsers without WebAuthn support
          this.$router.push('/login');
        }
      } catch (error) {
        console.error('Authentication failed:', error);
        
        // If passkey fails, redirect to password login as fallback
        this.$router.push('/login');
      }
    },
    
    goToAccountCreation() {
      this.$router.push('/account-creation');
    },
    
    goToDashboard() {
      this.$router.push('/dashboard');
    },
    
    async logout() {
      try {
        await AuthService.logout();
        this.isAuthenticated = false;
      } catch (error) {
        console.error('Logout failed:', error);
      }
    },
    
    speakText() {
      let text;
      
      if (this.isAuthenticated) {
        text = "Bienvenue sur Autrement Capable. Vous êtes déjà connecté. Vous pouvez accéder à votre tableau de bord ou vous déconnecter.";
      } else if (this.showOptions) {
        text = "Bienvenue sur Autrement Capable. Si vous avez déjà un compte, cliquez sur Se connecter. Si vous êtes nouveau, cliquez sur Créer un compte.";
      } else {
        text = "Bienvenue sur Autrement Capable. Appuyez sur le bouton Commencer pour démarrer.";
      }
      
      const speech = new SpeechSynthesisUtterance();
      speech.lang = 'fr-FR';
      speech.text = text;
      window.speechSynthesis.speak(speech);
    }
  }
}
</script>

<style scoped>
@import url('@/assets/styles.css');

.start-button {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
  padding: 20px;
}

.main-title {
  font-family: 'Glacial Indifference', sans-serif;
  font-weight: bold;
  font-size: 3em;
  margin-bottom: 1em;
  text-align: center;
}

.welcome-screen, .authenticated-welcome, .auth-options {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 800px;
}

.options-container {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  width: 100%;
  margin: 20px 0;
}

@media (max-width: 768px) {
  .options-container {
    flex-direction: column;
    align-items: center;
  }
}

.option-card {
  background-color: white;
  border-radius: 10px;
  padding: 30px;
  margin: 10px;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  min-width: 250px;
}

.option-card h2 {
  margin-bottom: 20px;
  font-family: 'Glacial Indifference', sans-serif;
}

.primary-button {
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

.secondary-button {
  padding: 1em 2em;
  font-size: 1.2em;
  background-color: #6c757d;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin: 0.5em;
  transition: transform 0.3s ease, background-color 0.3s ease;
}

.accessibility-button {
  padding: 0.8em 1.5em;
  font-size: 1em;
  background-color: #28a745;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon {
  margin-right: 8px;
}

button:focus {
  outline: 2px solid #0056b3;
}

.primary-button:hover {
  transform: scale(1.05);
  background-color: #0056b3;
}

.secondary-button:hover {
  transform: scale(1.05);
  background-color: #5a6268;
}

.accessibility-button:hover {
  transform: scale(1.05);
  background-color: #218838;
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