export const BackgroundManager = {
    // Obtenir le thème actuel depuis localStorage
    getCurrentTheme() {
      return localStorage.getItem('dashboard-theme') || 'cosmic';
    },
  
    // Vérifier si les animations sont activées
    areAnimationsEnabled() {
      const animationsEnabled = localStorage.getItem('dashboard-animations');
      // Si null, par défaut les animations sont activées
      return animationsEnabled === null ? true : animationsEnabled === 'true';
    },
  
    // Définir le thème actuel
    setCurrentTheme(theme) {
      if (theme && ['cosmic', 'ocean', 'cyberpunk', 'forest'].includes(theme)) {
        localStorage.setItem('dashboard-theme', theme);
        return true;
      }
      return false;
    },
  
    // Activer/désactiver les animations
    setAnimationsEnabled(enabled) {
      localStorage.setItem('dashboard-animations', enabled.toString());
      return true;
    },
  
    // Basculer l'état des animations
    toggleAnimations() {
      const current = this.areAnimationsEnabled();
      this.setAnimationsEnabled(!current);
      return !current;
    }
  };
  
  export default BackgroundManager;