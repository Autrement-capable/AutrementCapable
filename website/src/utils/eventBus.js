import mitt from 'mitt'

// Créer une instance de mitt pour servir d'Event Bus
export const eventBus = mitt()

/*
Guide d'utilisation:

1. Importer l'eventBus dans les composants qui doivent communiquer:
   import { eventBus } from '@/utils/eventBus'

2. Émettre des événements:
   eventBus.emit('nom-evenement', données)

3. Écouter des événements:
   eventBus.on('nom-evenement', callback)

4. Nettoyer les écouteurs:
   eventBus.off('nom-evenement', callback)
   
   OU pour tout supprimer pour un événement spécifique:
   eventBus.off('nom-evenement')

Événements utilisés dans le parcours guidé:

- 'profile-opened': émis quand l'utilisateur ouvre son profil
- 'profile-closed': émis quand l'utilisateur ferme son profil
- 'badge-unlocked': émis quand un badge est débloqué
- 'highlight-play-button': émis pour mettre en évidence le bouton jouer
- 'hide-dashboard-guide': émis pour masquer le guide dans le dashboard
- 'show-profile-guide': émis pour afficher le guide dans le profil
- 'journey-step-updated': émis quand une étape du parcours est mise à jour
*/