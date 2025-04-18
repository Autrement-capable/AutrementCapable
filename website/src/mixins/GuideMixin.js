import { UserJourneyService } from '@/services/UserJourneyService';

export const GuideAvatarMixin = {
  data() {
    return {
      // États liés au guide
      guideVisible: true,
      guideContext: 'default',
      guideForcedMessage: null,
      guideForcedOptions: [],
      guideForceShow: false,
      guideAutoShowDelay: 1500, // délai avant affichage automatique en ms
      // États liés au parcours utilisateur
      currentJourneyStep: 0,
      completedGames: [],
      currentGame: null
    };
  },
  
  created() {
    // Initialiser les données du parcours utilisateur
    this.initUserJourneyData();
    
    // Définir le contexte en fonction de la route actuelle
    this.setGuideContextFromRoute();
    
    // Mettre à jour la dernière route visitée
    UserJourneyService.updateLastVisitedRoute(this.$route.path);
    
    // Si la page est un jeu, définir le jeu courant
    this.detectCurrentGame();
  },
  
  methods: {
    /**
     * Initialise les données du parcours utilisateur
     */
    initUserJourneyData() {
      const state = UserJourneyService.getState();
      this.currentJourneyStep = state.currentStep;
      this.completedGames = state.completedGames;
    },
    
    /**
     * Définit le contexte du guide en fonction de la route actuelle
     */
    setGuideContextFromRoute() {
      const path = this.$route.path;
      
      if (path === '/dashboard' || path === '/') {
        this.guideContext = 'dashboard';
      } else if (path === '/user-profile') {
        this.guideContext = 'profile';
      } else if (path.includes('/scenario')) {
        this.guideContext = 'scenario';
      } else if (path.includes('/roue-des-competences')) {
        this.guideContext = 'skills';
      } else if (path.includes('/metier')) {
        this.guideContext = 'metier';
      } else if (path.includes('/game-')) {
        this.guideContext = 'games';
      } else if (path.includes('/environment')) {
        this.guideContext = 'environment';
      } else {
        this.guideContext = 'default';
      }
      
      // Récupérer des messages et options contextuels
      this.updateContextualContent();
    },
    
    /**
     * Met à jour le contenu contextuel (messages et options)
     */
    updateContextualContent() {
      const messages = UserJourneyService.getContextualMessages(this.guideContext, this.currentJourneyStep);
      const suggestions = UserJourneyService.getContextualSuggestions(this.guideContext, this.currentJourneyStep);
      
      if (messages && messages.length > 0) {
        this.guideForcedMessage = messages[0]; // Utiliser le premier message
      }
      
      if (suggestions && suggestions.length > 0) {
        this.guideForcedOptions = suggestions;
      }
    },
    
    /**
     * Détecte le jeu actuel en fonction de la route
     */
    detectCurrentGame() {
      const path = this.$route.path;
      
      // Correspondance entre routes et identifiants de jeux
      const gameMapping = {
        '/scenarios': 'scenarios',
        '/roue-des-competences': 'skills-wheel',
        '/metier': 'metiers',
        '/game-speed': 'game-speed',
        '/shape-sequence-game': 'shape-game',
        '/environment': 'environment'
      };
      
      // Trouver la correspondance exacte ou partielle
      let gameId = gameMapping[path];
      
      if (!gameId) {
        // Chercher une correspondance partielle
        for (const [route, id] of Object.entries(gameMapping)) {
          if (path.includes(route)) {
            gameId = id;
            break;
          }
        }
      }
      
      this.currentGame = gameId;
    },
    
    /**
     * Marque le jeu actuel comme complété
     */
    completeCurrentGame() {
      if (this.currentGame) {
        UserJourneyService.completeGame(this.currentGame);
        // Mettre à jour les données locales
        this.initUserJourneyData();
        // Mettre à jour le contenu contextuel
        this.updateContextualContent();
        
        // Afficher un message de félicitations
        this.showCompletionMessage();
      }
    },
    
    /**
     * Affiche un message de félicitations
     */
    showCompletionMessage() {
      this.guideForcedMessage = "Félicitations ! Tu as terminé ce jeu avec succès.";
      this.guideForcedOptions = [
        { text: "Continuer mon parcours", action: "continueJourney" },
        { text: "Voir ma progression", action: "showProgress" }
      ];
      this.guideForceShow = true;
      
      // Réinitialiser après un délai
      setTimeout(() => {
        this.guideForceShow = false;
        this.updateContextualContent();
      }, 5000);
    },
    
    /**
     * Traite une option sélectionnée par l'utilisateur
     */
    handleGuideOptionSelected(option) {
      console.log("Option sélectionnée:", option);
      
      // Exécuter l'action associée à l'option
      if (option.action && typeof this[option.action] === 'function') {
        this[option.action](option);
      }
      
      // Naviguer vers la route si elle est spécifiée
      if (option.route) {
        this.$router.push(option.route);
      }
    },
    
    /**
     * Guide l'utilisateur vers la prochaine étape de son parcours
     */
    continueJourney() {
      // Déterminer la prochaine étape en fonction de l'état actuel
      const nextGame = UserJourneyService.getNextRecommendedGame();
      
      if (nextGame) {
        // Proposer le prochain jeu
        this.guideForcedMessage = `Je te suggère d'essayer ${nextGame.name} maintenant. Tu veux y aller ?`;
        this.guideForcedOptions = [
          { text: "Oui, allons-y", route: nextGame.route },
          { text: "Non, pas maintenant", action: "declineNextGame" }
        ];
        this.guideForceShow = true;
      } else {
        // Tous les jeux sont complétés
        this.guideForcedMessage = "Félicitations ! Tu as terminé tous les jeux du parcours.";
        this.guideForcedOptions = [
          { text: "Voir mon profil", route: "/user-profile" },
          { text: "Explorer librement", action: "exploreFreely" }
        ];
        this.guideForceShow = true;
      }
    },
    
    /**
     * Affiche la progression de l'utilisateur
     */
    showProgress() {
      const progress = UserJourneyService.getProgressPercentage();
      const completedGames = UserJourneyService.getCompletedGames();
      const totalGames = UserJourneyService.GAMES.length;
      
      this.guideForcedMessage = `Tu as complété ${completedGames.length} jeux sur ${totalGames} (${progress}% du parcours).`;
      
      const incompleteGames = UserJourneyService.getIncompleteGames();
      if (incompleteGames.length > 0) {
        this.guideForcedOptions = incompleteGames.slice(0, 3).map(game => ({
          text: `Essayer ${game.name}`,
          route: game.route
        }));
        
        if (incompleteGames.length > 3) {
          this.guideForcedOptions.push({
            text: "Voir plus de jeux",
            action: "showMoreGames"
          });
        }
      } else {
        this.guideForcedOptions = [
          { text: "Super !", action: "exploreFreely" }
        ];
      }
      
      this.guideForceShow = true;
    },
    
    /**
     * Affiche les jeux recommandés à l'utilisateur
     */
    suggestGames() {
      const incompleteGames = UserJourneyService.getIncompleteGames();
      
      if (incompleteGames.length === 0) {
        this.guideForcedMessage = "Tu as déjà complété tous les jeux. Bravo !";
        this.guideForcedOptions = [
          { text: "Merci !", action: "exploreFreely" }
        ];
      } else {
        this.guideForcedMessage = "Voici d'autres jeux que tu pourrais essayer :";
        this.guideForcedOptions = incompleteGames.slice(0, 4).map(game => ({
          text: game.name,
          route: game.route
        }));
      }
      
      this.guideForceShow = true;
    },
    
    /**
     * Actions spécifiques en fonction du contexte
     */
    showGameRules() {
      // Afficher les règles du jeu actuel
      if (this.currentGame === 'scenarios') {
        this.guideForcedMessage = "Dans ce jeu, tu vas rencontrer des situations de la vie quotidienne et tu devras choisir comment réagir. Tes choix influenceront tes compétences sociales !";
      } else if (this.currentGame === 'skills-wheel') {
        this.guideForcedMessage = "Tourne la roue pour découvrir différentes compétences et indique ton niveau de maîtrise pour chacune d'elles. Cela t'aidera à mieux te connaître !";
      } else if (this.currentGame === 'metiers') {
        this.guideForcedMessage = "Découvre différents métiers et indique ceux qui t'intéressent. Tu peux aussi obtenir plus d'informations sur chaque métier.";
      } else if (this.currentGame === 'game-speed') {
        this.guideForcedMessage = "Teste ta vitesse de frappe ! Tape le texte qui apparaît à l'écran le plus rapidement et précisément possible.";
      } else if (this.currentGame === 'shape-game') {
        this.guideForcedMessage = "Observe attentivement les formes qui apparaissent et retrouve la forme manquante dans la séquence.";
      } else {
        this.guideForcedMessage = "Explore ce jeu à ton rythme. Je suis là si tu as besoin d'aide !";
      }
      
      this.guideForcedOptions = [
        { text: "Compris !", action: "dismissMessage" },
        { text: "Besoin d'aide supplémentaire", action: "showMoreHelp" }
      ];
      
      this.guideForceShow = true;
    },
    
    /**
     * Affiche plus d'aide sur le jeu actuel
     */
    showMoreHelp() {
      // Aide supplémentaire en fonction du jeu
      if (this.currentGame === 'scenarios') {
        this.guideForcedMessage = "Prends ton temps pour lire chaque situation et les options de réponse. Il n'y a pas de bonne ou mauvaise réponse absolue, mais certains choix peuvent développer différentes compétences.";
      } else if (this.currentGame === 'skills-wheel') {
        this.guideForcedMessage = "Sois honnête dans ton auto-évaluation ! C'est le meilleur moyen d'identifier tes forces et tes axes d'amélioration.";
      } else {
        this.guideForcedMessage = "N'hésite pas à explorer toutes les fonctionnalités du jeu. L'important est d'apprendre et de t'améliorer à ton rythme.";
      }
      
      this.guideForcedOptions = [
        { text: "Merci pour ces conseils", action: "dismissMessage" }
      ];
      
      this.guideForceShow = true;
    },
    
    /**
     * Masque le message forcé
     */
    dismissMessage() {
      this.guideForceShow = false;
      // Réinitialiser les messages et options
      setTimeout(() => {
        this.updateContextualContent();
      }, 300);
    },
    
    /**
     * Permet à l'utilisateur d'explorer librement
     */
    exploreFreely() {
      this.guideForcedMessage = "N'hésite pas à explorer toutes les fonctionnalités de la plateforme à ton rythme. Je suis toujours là si tu as besoin d'aide !";
      this.guideForcedOptions = [
        { text: "Voir mon tableau de bord", route: "/dashboard" },
        { text: "Merci !", action: "dismissMessage" }
      ];
      this.guideForceShow = true;
    },
    
    /**
     * Décline la suggestion de prochain jeu
     */
    declineNextGame() {
      this.guideForcedMessage = "Pas de problème ! Tu peux explorer à ton rythme. Je serai là quand tu auras besoin de moi.";
      this.guideForcedOptions = [
        { text: "Voir mon tableau de bord", route: "/dashboard" },
        { text: "Merci !", action: "dismissMessage" }
      ];
      this.guideForceShow = true;
    }
  }
};

export default GuideAvatarMixin;