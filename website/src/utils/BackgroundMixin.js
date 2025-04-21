import { BackgroundManager } from '@/utils/BackgroundManager';
import SpaceBackground from '@/components/SpaceBackground.vue';
import StaticBackgrounds from '@/components/StaticBackgrounds.vue';

export const BackgroundMixin = {
  components: {
    SpaceBackground,
    StaticBackgrounds
  },
  
  data() {
    return {
      currentTheme: 'cosmic',
      animationsEnabled: true
    };
  },
  
  created() {
    // Chargement des paramètres de thème et d'animation
    this.loadBackgroundSettings();
    
    // Écouter les changements d'animation ou de thème
    window.addEventListener('storage', this.handleStorageChange);
  },
  
  beforeUnmount() {
    // Nettoyage lors de la destruction du composant
    window.removeEventListener('storage', this.handleStorageChange);
  },
  
  methods: {
    loadBackgroundSettings() {
      this.currentTheme = BackgroundManager.getCurrentTheme();
      this.animationsEnabled = BackgroundManager.areAnimationsEnabled();
    },
    
    handleStorageChange(event) {
      // Mettre à jour les paramètres si localStorage change
      if (event.key === 'dashboard-theme') {
        this.currentTheme = event.newValue || 'cosmic';
      } else if (event.key === 'dashboard-animations') {
        this.animationsEnabled = event.newValue === 'true';
      }
    },
    
    toggleAnimations() {
      this.animationsEnabled = BackgroundManager.toggleAnimations();
    },
    
    changeTheme(theme) {
      if (BackgroundManager.setCurrentTheme(theme)) {
        this.currentTheme = theme;
      }
    }
  }
};

export default BackgroundMixin;