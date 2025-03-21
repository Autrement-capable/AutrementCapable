// src/utils/badges.js
export function unlockBadge(badgeId) {
    try {
      // Récupérer les badges existants
      const savedBadges = localStorage.getItem('userBadges');
      let badges = [];
      
      if (savedBadges) {
        badges = JSON.parse(savedBadges);
      }
      
      // Vérifier si le badge existe déjà
      const badgeIndex = badges.findIndex(b => b.id === badgeId);
      
      if (badgeIndex === -1) {
        // Si le badge n'existe pas, l'ajouter
        badges.push({
          id: badgeId,
          unlocked: true,
          dateUnlocked: new Date().toISOString().split('T')[0]
        });
        console.log(`Badge ${badgeId} débloqué !`);
      } else if (!badges[badgeIndex].unlocked) {
        // Si le badge existe mais n'est pas débloqué, le débloquer
        badges[badgeIndex].unlocked = true;
        badges[badgeIndex].dateUnlocked = new Date().toISOString().split('T')[0];
        console.log(`Badge ${badgeId} débloqué !`);
      } else {
        // Le badge est déjà débloqué
        console.log(`Badge ${badgeId} déjà débloqué.`);
        return false; // Aucun changement
      }
      
      // Sauvegarder les badges mis à jour
      localStorage.setItem('userBadges', JSON.stringify(badges));
      return true; // Badge débloqué avec succès
    } catch (error) {
      console.error('Erreur lors du déverrouillage du badge:', error);
      return false;
    }
  }
  
  // Fonction utilitaire pour vérifier si un badge est débloqué
  export function isBadgeUnlocked(badgeId) {
    try {
      const savedBadges = localStorage.getItem('userBadges');
      if (!savedBadges) return false;
      
      const badges = JSON.parse(savedBadges);
      const badge = badges.find(b => b.id === badgeId);
      
      return badge && badge.unlocked;
    } catch (error) {
      console.error('Erreur lors de la vérification du badge:', error);
      return false;
    }
  }
  
  // Fonction utilitaire pour récupérer tous les badges débloqués
  export function getUnlockedBadges() {
    try {
      const savedBadges = localStorage.getItem('userBadges');
      if (!savedBadges) return [];
      
      const badges = JSON.parse(savedBadges);
      return badges.filter(b => b.unlocked);
    } catch (error) {
      console.error('Erreur lors de la récupération des badges:', error);
      return [];
    }
  }