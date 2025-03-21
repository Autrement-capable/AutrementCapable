export function unlockBadge(badgeId) {
    const savedBadges = localStorage.getItem('userBadges') || '[]';
    let badges = JSON.parse(savedBadges);
    
    const badgeIndex = badges.findIndex(b => b.id === badgeId);
    
    if (badgeIndex === -1) {
      badges.push({
        id: badgeId,
        unlocked: true,
        dateUnlocked: new Date().toISOString().split('T')[0]
      });
    } else if (!badges[badgeIndex].unlocked) {
      badges[badgeIndex].unlocked = true;
      badges[badgeIndex].dateUnlocked = new Date().toISOString().split('T')[0];
    }
    
    localStorage.setItem('userBadges', JSON.stringify(badges));
  }