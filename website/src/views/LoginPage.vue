<template>
  <div class="login-page" :class="{ 'animations-unlocked': hasNewAchievement }">
    
    <!-- Arrière-plans dynamiques -->
    <space-background v-if="animationsEnabled" :theme="currentTheme" />
    <static-backgrounds v-else :theme="currentTheme" />

    <!-- Container principal -->
    <div class="login-container">


      <!-- Formulaire de connexion -->
      <div class="login-form-container">
        <!-- Titre dans le container -->
        <div class="form-header">
          <h2 class="form-title">Bienvenue</h2>
          <h3 class="form-subtitle">de retour</h3>
          <p class="form-description">Connectez-vous pour continuer votre aventure</p>
        </div>
        
        <form @submit.prevent="handleLogin" class="login-form">
          
          <!-- Champ nom d'utilisateur -->
          <div class="input-group">
      <div class="input-box">
        <input 
          type="text" 
                placeholder="Nom d'utilisateur ou email" 
          v-model="credentials.username_or_email" 
          required 
          :disabled="isLoading" 
                class="form-input"
        />
              <div class="input-icon">
        <i class="mdi mdi-account"></i>
              </div>
            </div>
      </div>
      
          <!-- Champ mot de passe -->
          <div class="input-group">
      <div class="input-box">
        <input 
          type="password" 
                placeholder="Mot de passe" 
          v-model="credentials.password" 
          required 
          :disabled="isLoading" 
                class="form-input"
        />
              <div class="input-icon">
        <i class="mdi mdi-lock"></i>
              </div>
            </div>
      </div>
      
          <!-- Message d'erreur -->
      <div class="error-message" v-if="errorMessage">
            <i class="mdi mdi-alert-circle"></i>
            <span>{{ errorMessage }}</span>
      </div>
      
          <!-- Options Remember me / Forgot password -->
          <div class="form-options">
            <label class="checkbox-label">
              <input type="checkbox" v-model="rememberMe" class="checkbox-input" />
              <span class="checkbox-custom"></span>
              <span class="checkbox-text">Se souvenir de moi</span>
        </label>
            <a href="#" @click.prevent="goToPasswordReset" class="forgot-link">
              Mot de passe oublié?
            </a>
      </div>
      
          <!-- Bouton de connexion principal -->
          <button 
            type="submit" 
            class="login-btn primary-btn" 
            :disabled="isLoading"
            :class="{ 'loading': isLoading }"
          >
            <span v-if="isLoading" class="loading-spinner">
              <i class="mdi mdi-loading mdi-spin"></i>
            </span>
            <span v-else class="btn-text">
              <i class="mdi mdi-login"></i>
              Se connecter
            </span>
      </button>
      
          <!-- Bouton passkey -->
      <button 
        v-if="supportsPasskeys" 
        type="button" 
        @click="loginWithPasskey" 
            class="login-btn passkey-btn" 
        :disabled="isLoading"
            :class="{ 'loading': isPasskeyLoading }"
      >
            <span v-if="isPasskeyLoading" class="loading-spinner">
              <i class="mdi mdi-loading mdi-spin"></i>
            </span>
            <span v-else class="btn-text">
              <i class="mdi mdi-fingerprint"></i>
              Connexion avec passkey
            </span>
      </button>
      
          <!-- Lien vers inscription -->
          <div class="register-prompt">
            <p>
              Pas encore de compte? 
              <a href="#" @click.prevent="goToRegister" class="register-link">
                Créer un compte
              </a>
            </p>
          </div>
        </form>
      </div>

      <!-- Onglet de contrôle du thème -->
      <div class="theme-tab" @click="toggleThemeMenu">
        <div class="theme-tab-icon">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            width="24"
            height="24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <circle cx="12" cy="12" r="5" />
            <line x1="12" y1="1" x2="12" y2="3" />
            <line x1="12" y1="21" x2="12" y2="23" />
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
            <line x1="1" y1="12" x2="3" y2="12" />
            <line x1="21" y1="12" x2="23" y2="12" />
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
          </svg>
        </div>
      </div>

      <!-- Sélecteur de thème -->
      <div
        class="theme-selector"
        :class="{ 'theme-selector-visible': themeMenuVisible }"
      >
        <div
          class="theme-option"
          v-for="theme in availableThemes"
          :key="theme.value"
          @click="changeTheme(theme.value)"
          :class="{ active: currentTheme === theme.value }"
        >
          <div class="theme-icon" :class="theme.value"></div>
          <span>{{ theme.label }}</span>
        </div>

        <div
          class="theme-option animation-toggle"
          @click="toggleAnimations"
          :class="{ active: animationsEnabled }"
        >
          <div class="theme-icon animation-icon">
            <i class="mdi mdi-play" v-if="animationsEnabled"></i>
            <i class="mdi mdi-pause" v-else></i>
          </div>
          <span>
            {{ animationsEnabled ? 'Animations ON' : 'Animations OFF' }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AuthService from '@/services/AuthService';
import { browserSupportsWebAuthn } from '@simplewebauthn/browser';
import SpaceBackground from '@/components/SpaceBackground.vue';
import StaticBackgrounds from '@/components/StaticBackgrounds.vue';

export default {
  name: 'LoginPage',
  components: {
    SpaceBackground,
    StaticBackgrounds
  },
  data() {
    return {
      credentials: {
        username_or_email: '',
        password: ''
      },
      rememberMe: false,
      isLoading: false,
      isPasskeyLoading: false,
      errorMessage: '',
      supportsPasskeys: false,
      
      // Thèmes et arrière-plans
      themeMenuVisible: false,
      currentTheme: 'cosmic',
      availableThemes: [
        { value: 'cosmic', label: 'Cosmic' },
        { value: 'ocean', label: 'Ocean' },
        { value: 'cyberpunk', label: 'Cyberpunk' },
        { value: 'forest', label: 'Forêt' },
        { value: 'snow', label: 'Neige' },
      ],
      animationsEnabled: true,
      hasNewAchievement: false
    }
  },
  mounted() {
    // Check if browser supports WebAuthn/passkeys
    try {
      this.supportsPasskeys = browserSupportsWebAuthn();
    } catch (error) {
      console.error('Error checking WebAuthn support:', error);
      this.supportsPasskeys = false;
    }
    
    // Pre-fill username if remembered
    const rememberedUsername = localStorage.getItem('remembered_username');
    if (rememberedUsername) {
      this.credentials.username_or_email = rememberedUsername;
      this.rememberMe = true;
    }

    // Charger les préférences de thème
    this.loadThemeSettings();
  },
  methods: {
    async handleLogin() {
      if (this.isLoading) return;
      
      this.isLoading = true;
      this.errorMessage = '';
      
      try {
        // Call login method from AuthService
        await AuthService.login(this.credentials);
        
        // Save username if remember me is checked
        if (this.rememberMe) {
          localStorage.setItem('remembered_username', this.credentials.username_or_email);
        } else {
          localStorage.removeItem('remembered_username');
        }
        
        // Redirect to the original destination or dashboard
        const redirectTo = this.$route.query.redirect || '/dashboard';
        this.$router.push(redirectTo);
      } catch (error) {
        console.error('Login error:', error);
        this.errorMessage = error.response?.data?.detail || 'Nom d\'utilisateur ou mot de passe invalide';
      } finally {
        this.isLoading = false;
      }
    },
    
    async loginWithPasskey() {
      if (this.isPasskeyLoading) return;
      
      this.isPasskeyLoading = true;
      this.errorMessage = '';
      
      try {
        // Use passkey authentication
        await AuthService.authenticateWithPasskey();
        
        // Redirect to the original destination or dashboard
        const redirectTo = this.$route.query.redirect || '/dashboard';
        this.$router.push(redirectTo);
      } catch (error) {
        console.error('Passkey login error:', error);
        this.errorMessage = 'Échec de l\'authentification passkey. Veuillez réessayer ou utiliser le mot de passe.';
      } finally {
        this.isPasskeyLoading = false;
      }
    },
    
    goToPasswordReset() {
      this.$router.push('/password-reset');
    },
    
    goToRegister() {
      this.$router.push('/account-creation');
    },

    // Gestion des thèmes
    loadThemeSettings() {
      const savedTheme = localStorage.getItem('dashboard-theme');
      if (savedTheme && this.availableThemes.some(theme => theme.value === savedTheme)) {
        this.currentTheme = savedTheme;
      }

      const savedAnimationPref = localStorage.getItem('dashboard-animations');
      if (savedAnimationPref !== null) {
        this.animationsEnabled = savedAnimationPref === 'true';
      }
    },

    toggleThemeMenu() {
      this.themeMenuVisible = !this.themeMenuVisible;
    },

    changeTheme(theme) {
      this.currentTheme = theme;
      localStorage.setItem('dashboard-theme', theme);
      this.themeMenuVisible = false;
    },

    toggleAnimations() {
      this.animationsEnabled = !this.animationsEnabled;
      localStorage.setItem('dashboard-animations', this.animationsEnabled.toString());
    }
  }
}
</script>

<style scoped>
/* Variables pour les thèmes */
:root {
  --primary-color: #7c4dff;
  --primary-light: #b085ff;
  --primary-dark: #4527a0;
  --success-color: #4caf50;
  --error-color: #f44336;
  --warning-color: #ff9800;
  --text-primary: #333333;
  --text-secondary: rgba(102, 102, 102, 0.8);
  --background-blur: rgba(255, 255, 255, 1.0);
  --border-color: rgba(255, 255, 255, 0.3);
  --shadow-color: rgba(0, 0, 0, 0.2);
  --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Page principale */
.login-page {
  position: relative;
  min-height: 100vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  box-sizing: border-box;
  overflow: hidden;
}

/* Container principal */
.login-container {
  position: relative;
  z-index: 10;
  max-width: 440px;
  width: 100%;
  margin: 0 auto;
}

/* En-tête */
.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  line-height: 1.2;
}

.title-text {
  color: var(--text-primary);
  display: block;
}

.title-accent {
  color: var(--primary-color);
  display: block;
  background: linear-gradient(45deg, var(--primary-color), var(--primary-light));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.login-subtitle {
  color: var(--text-secondary);
  font-size: 1.1rem;
  margin: 0;
}

/* Container du formulaire */
.login-form-container {
  background: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  transition: var(--transition);
}

/* En-tête du formulaire */
.form-header {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f0f0f0;
}

.form-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 0.25rem 0;
}

.form-subtitle {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--primary-color);
  margin: 0 0 0.5rem 0;
}

.form-description {
  color: var(--text-secondary);
  font-size: 1rem;
  margin: 0;
}

.login-form-container:hover {
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
  transform: translateY(-2px);
}

/* Groupes d'input */
.input-group {
  margin-bottom: 1.5rem;
}

.input-box {
  position: relative;
  width: 100%;
}

.form-input {
  width: 100%;
  height: 56px;
  background: #f8f8f8;
  border: 2px solid #d0d0d0;
  border-radius: 14px;
  padding: 0 20px 0 60px;
  font-size: 1rem;
  color: var(--text-primary);
  transition: var(--transition);
  outline: none;
  box-sizing: border-box;
}

.form-input::placeholder {
  color: var(--text-secondary);
}

.form-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(124, 77, 255, 0.2);
  background: #ffffff;
}

.form-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.input-icon {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
  font-size: 1.2rem;
  transition: var(--transition);
}

.form-input:focus + .input-icon {
  color: var(--primary-color);
}

/* Message d'erreur */
.error-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(244, 67, 54, 0.1);
  border: 1px solid rgba(244, 67, 54, 0.3);
  border-radius: 10px;
  padding: 0.75rem 1rem;
  margin-bottom: 1rem;
  color: #ff6b6b;
  font-size: 0.9rem;
}

.error-message i {
  font-size: 1.1rem;
}

/* Options du formulaire */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.checkbox-input {
  display: none;
}

.checkbox-custom {
  width: 18px;
  height: 18px;
  border: 2px solid #d0d0d0;
  border-radius: 4px;
  position: relative;
  transition: var(--transition);
  background: #ffffff;
  display: inline-block;
  flex-shrink: 0;
}

.checkbox-input:checked + .checkbox-custom {
  background: var(--primary-color);
  border-color: var(--primary-color);
}

.checkbox-input:checked + .checkbox-custom::after {
  content: '';
  position: absolute;
  left: 4px;
  top: 1px;
  width: 6px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  color: var(--text-primary);
  font-size: 0.9rem;
}

.checkbox-text {
  user-select: none;
}

.forgot-link {
  color: var(--primary-color);
  text-decoration: none;
  font-size: 0.9rem;
  transition: var(--transition);
}

.forgot-link:hover {
  color: var(--primary-light);
  text-decoration: underline;
}

/* Boutons */
.login-btn {
  width: 100%;
  height: 56px;
  border: none;
  border-radius: 14px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  outline: none;
  position: relative;
  overflow: hidden;
  text-transform: none;
  letter-spacing: 0.3px;
}

.primary-btn {
  background: linear-gradient(135deg, #7c4dff 0%, #b085ff 100%);
  color: white;
  border: none;
  box-shadow: 0 4px 15px rgba(124, 77, 255, 0.3);
}

.primary-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(124, 77, 255, 0.4);
  background: linear-gradient(135deg, #6c3ce0 0%, #9a6fff 100%);
}

.primary-btn:active {
  transform: translateY(0);
  box-shadow: 0 4px 15px rgba(124, 77, 255, 0.5);
}

.passkey-btn {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border: 2px solid #7c4dff;
  color: #7c4dff;
  box-shadow: 0 4px 15px rgba(124, 77, 255, 0.1);
}

.passkey-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
  border-color: #6c3ce0;
  color: #6c3ce0;
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(124, 77, 255, 0.2);
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none !important;
}

.loading-spinner {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.loading-spinner i {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Animation pour les icônes MDI */
.mdi-spin {
  animation: spin 1s linear infinite;
}

.btn-text {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Prompt d'inscription */
.register-prompt {
  text-align: center;
  margin-top: 1rem;
}

.register-prompt p {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin: 0;
}

.register-link {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 600;
  transition: var(--transition);
}

.register-link:hover {
  color: var(--primary-light);
  text-decoration: underline;
}

.theme-tab {
  position: fixed;
  bottom: 20px;
  left: 20px;
  width: 52px;
  height: 52px;
  background: rgba(30, 30, 45, 0.7);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  z-index: 30;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(5px);
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.theme-tab:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4);
  background: rgba(40, 40, 60, 0.8);
}

.theme-tab:active {
  transform: scale(0.95);
}

.theme-tab-icon {
  color: white;
  width: 24px;
  height: 24px;
  animation: rotateIcon 10s linear infinite;
}

@keyframes rotateIcon {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.theme-selector {
  position: fixed;
  bottom: 20px;
  left: 80px;
  display: flex;
  gap: 15px;
  background: rgba(30, 30, 45, 0.7);
  border-radius: 12px;
  padding: 10px 15px;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
  z-index: 20;
  transform: translateY(20px) translateX(25px);
  opacity: 0;
  visibility: hidden;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  transform-origin: bottom left;
  pointer-events: none;
}

.theme-selector-visible {
  transform: translateY(0) translateX(0);
  opacity: 1;
  visibility: visible;
  pointer-events: all;
}

.theme-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 8px;
  border-radius: 8px;
}

.theme-option:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-3px);
}

.theme-option.active {
  background: rgba(255, 255, 255, 0.2);
  box-shadow: 0 0 15px rgba(124, 77, 255, 0.5);
}

.theme-icon {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-bottom: 5px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.theme-option:hover .theme-icon {
  transform: scale(1.1);
  border-color: rgba(255, 255, 255, 0.5);
}

.theme-option.active .theme-icon {
  border-color: white;
  transform: scale(1.1);
}

.theme-icon.cosmic {
  background: linear-gradient(135deg, #7c4dff 0%, #0d47a1 100%);
  box-shadow: 0 0 10px rgba(124, 77, 255, 0.5);
}

.theme-icon.ocean {
  background: linear-gradient(135deg, #4fc3f7 0%, #0d47a1 100%);
  box-shadow: 0 0 10px rgba(79, 195, 247, 0.5);
}

.theme-icon.cyberpunk {
  background: linear-gradient(135deg, #ff4081 0%, #ab47bc 100%);
  box-shadow: 0 0 10px rgba(255, 64, 129, 0.5);
}

.theme-icon.forest {
  background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%);
  box-shadow: 0 0 10px rgba(46, 125, 50, 0.5);
}

.theme-icon.snow {
  background: linear-gradient(135deg, #6ebeff 0%, #eff5ff 100%);
  box-shadow: 0 0 10px rgba(144, 202, 249, 0.5);
}

.theme-option span {
  font-size: 12px;
  opacity: 0.8;
  transition: all 0.3s ease;
  color: white;
}

.theme-option:hover span,
.theme-option.active span {
  opacity: 1;
}

.animation-toggle {
  margin-left: 10px;
  background-color: rgba(30, 30, 45, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.animation-toggle:hover {
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-3px);
}

.animation-toggle.active {
  border-color: #4fc3f7;
  box-shadow: 0 0 15px rgba(79, 195, 247, 0.5);
}

.animation-toggle:not(.active) {
  opacity: 0.7;
}

.animation-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.5rem;
  color: #fff;
}

.animation-icon i {
  transition: all 0.3s ease;
}

.animation-toggle.active .animation-icon i {
  color: #4fc3f7;
}

.animation-toggle:not(.active) .animation-icon i {
  color: #aaa;
}

/* Responsive */
@media (max-width: 768px) {
  .login-container {
    max-width: 100%;
    padding: 0 10px;
  }

  .form-title, .form-subtitle {
    font-size: 1.5rem;
  }

  .login-form-container {
    padding: 1.5rem;
  }

  .theme-selector {
    bottom: 10px;
    left: 70px;
    padding: 5px 10px;
    gap: 10px;
  }

  .theme-tab {
    bottom: 10px;
    left: 10px;
    width: 48px;
    height: 48px;
  }

  .theme-icon {
    width: 20px;
    height: 20px;
  }

  .theme-option span {
    font-size: 10px;
  }

  .form-options {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}

@media (max-width: 480px) {
  .login-page {
    padding: 10px;
  }

  .form-title, .form-subtitle {
    font-size: 1.3rem;
  }

  .form-description {
    font-size: 0.9rem;
  }

  .login-form-container {
    padding: 1.25rem;
  }

  .form-input {
    height: 50px;
    padding: 0 15px 0 50px;
  }

  .input-icon {
    left: 15px;
  }

  .login-btn {
    height: 50px;
  }
}

/* Animations d'entrée */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-header {
  animation: fadeInUp 0.6s ease-out;
}

.login-form-container {
  animation: fadeInUp 0.6s ease-out 0.2s both;
}

.theme-controls {
  animation: fadeInUp 0.6s ease-out 0.4s both;
}

/* Effet de focus pour accessibilité */
.form-input:focus-visible,
.login-btn:focus-visible,
.theme-tab:focus-visible {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}
</style>