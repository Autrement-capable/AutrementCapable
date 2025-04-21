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

export function resetBadge(badgeId) {
  try {
    // Récupérer les badges existants
    const savedBadges = localStorage.getItem('userBadges');
    if (!savedBadges) {
      console.log('Aucun badge trouvé en stockage.');
      return false;
    }
    
    const badges = JSON.parse(savedBadges);
    
    // Trouver le badge spécifique
    const badgeIndex = badges.findIndex(b => b.id === badgeId);
    
    if (badgeIndex === -1) {
      console.log(`Badge ${badgeId} non trouvé.`);
      return false;
    }
    
    // Vérifier si le badge est déjà verrouillé
    if (!badges[badgeIndex].unlocked) {
      console.log(`Badge ${badgeId} déjà verrouillé.`);
      return false;
    }
    
    // Verrouiller le badge
    badges[badgeIndex].unlocked = false;
    badges[badgeIndex].dateUnlocked = null;
    
    // Sauvegarder les badges mis à jour
    localStorage.setItem('userBadges', JSON.stringify(badges));
    console.log(`Badge ${badgeId} verrouillé avec succès.`);
    return true;
    
  } catch (error) {
    console.error('Erreur lors du verrouillage du badge:', error);
    return false;
  }
}

export function resetBadges(badgeIds = null) {
  try {
    // Récupérer les badges existants
    const savedBadges = localStorage.getItem('userBadges');
    if (!savedBadges) {
      console.log('Aucun badge trouvé en stockage.');
      return false;
    }
    
    const badges = JSON.parse(savedBadges);
    let changesMade = false;
    
    // Mise à jour des badges
    const updatedBadges = badges.map(badge => {
      // Si badgeIds est fourni, vérifier si ce badge doit être réinitialisé
      if (badgeIds === null || badgeIds.includes(badge.id)) {
        if (badge.unlocked) {
          changesMade = true;
          return {
            ...badge,
            unlocked: false,
            dateUnlocked: null
          };
        }
      }
      return badge;
    });
    
    // Si aucun changement n'a été effectué, retourner false
    if (!changesMade) {
      console.log('Aucun badge déverrouillé à réinitialiser.');
      return false;
    }
    
    // Sauvegarder les badges mis à jour
    localStorage.setItem('userBadges', JSON.stringify(updatedBadges));
    console.log(`Badges verrouillés avec succès.`);
    return true;
    
  } catch (error) {
    console.error('Erreur lors du verrouillage des badges:', error);
    return false;
  }
}