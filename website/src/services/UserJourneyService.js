/**
 * Extension du UserJourneyService pour le tour guidé du profil
 */
export const UserJourneyService = {
  // Propriétés existantes
  STORAGE_KEY: 'user-guided-journey',
  
  // Étapes du parcours
  STEPS: {
    DASHBOARD_INTRO: 0,
    CLICK_AVATAR: 1,
    PROFILE_INTRO: 2,
    PROFILE_TOUR_COMPLETED: 2.5, // Nouvelle étape pour le tour du profil
    FIRST_GAME: 3,
    CONTINUE_GAMES: 4,
    COMPLETE_GAMES: 5,
    ENVIRONMENT: 6,
    JOURNEY_COMPLETE: 7
  },
  
  // Sections du profil pour le tour guidé
  PROFILE_SECTIONS: [
    {
      id: 'header',
      name: 'En-tête du profil',
      description: "C'est ton profil personnel ! Tu peux voir ton avatar, ton niveau actuel et tes informations personnelles comme ton âge et ta ville."
    },
    {
      id: 'progress-map',
      name: 'Carte de progression',
      description: "Cette carte montre tous tes badges. Les badges débloqués sont en couleur, et les badges à débloquer sont grisés avec un cadenas. Le badge clignotant orange est ta prochaine activité recommandée !"
    },
    {
      id: 'next-activity',
      name: 'Prochaine activité',
      description: "Ici tu trouveras ta prochaine activité recommandée. Clique sur 'Jouer maintenant' pour la commencer et débloquer un nouveau badge !"
    },
    {
      id: 'badges-grid',
      name: 'Mes badges',
      description: "Cette section affiche tous tes badges, débloqués ou non. Clique sur un badge pour voir plus de détails et comment le débloquer si tu ne l'as pas encore."
    },
    {
      id: 'actions',
      name: 'Actions',
      description: "Ces boutons te permettent de créer ton CV avec les compétences que tu as développées ou d'accéder directement à ton profil complet."
    }
  ],
  
  // Liste des jeux existante...
  GAMES: [
    { id: 'scenarios', name: 'Scénarios sociaux', route: '/scenarios' },
    { id: 'skills-wheel', name: 'Roue des compétences', route: '/roue-des-competences' },
    { id: 'metiers', name: 'Découverte des métiers', route: '/metiers' },
    { id: 'game-speed', name: 'Jeu de vitesse', route: '/game-speed' },
    { id: 'shape-game', name: 'Jeu des formes', route: '/shape-sequence-game' },
    { id: 'environment', name: 'Personnalisation', route: '/environment' }
  ],
  
  /**
   * Obtient l'état actuel du parcours ou initialise avec des valeurs par défaut
   */
  getState() {
    try {
      const savedState = localStorage.getItem(this.STORAGE_KEY);
      
      if (savedState) {
        return JSON.parse(savedState);
      }
    } catch (error) {
      console.error('Erreur lors de la récupération de l\'état du parcours:', error);
    }
    
    // État par défaut avec ajout des propriétés pour le tour du profil
    return {
      currentStep: this.STEPS.DASHBOARD_INTRO,
      completedGames: [],
      lastVisitedRoute: null,
      hasSeenGuide: false,
      dismissCount: 0,
      customPreferences: {},
      timestamp: Date.now(),
      profileTourStep: 0,
      profileTourCompleted: false,
      visitedProfileSections: []
    };
  },
  
  /**
   * Sauvegarde l'état du parcours
   */
  saveState(state) {
    try {
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify({
        ...state,
        timestamp: Date.now()
      }));
      return true;
    } catch (error) {
      console.error('Erreur lors de la sauvegarde de l\'état du parcours:', error);
      return false;
    }
  },
  
  /**
   * Met à jour l'étape actuelle du parcours
   */
  updateStep(step) {
    const state = this.getState();
    state.currentStep = step;
    return this.saveState(state);
  },
  
  /**
   * Marque un jeu comme complété
   */
  completeGame(gameId) {
    const state = this.getState();
    
    if (!state.completedGames.includes(gameId)) {
      state.completedGames.push(gameId);
      
      // Mettre à jour l'étape si nécessaire
      if (state.completedGames.length === 1 && state.currentStep === this.STEPS.FIRST_GAME) {
        // Premier jeu complété
        state.currentStep = this.STEPS.CONTINUE_GAMES;
      } else if (state.completedGames.length === this.GAMES.length - 1) {
        // Tous les jeux sauf l'environnement sont complétés
        state.currentStep = this.STEPS.ENVIRONMENT;
      } else if (state.completedGames.length === this.GAMES.length) {
        // Tous les jeux sont complétés
        state.currentStep = this.STEPS.JOURNEY_COMPLETE;
      }
    }
    
    return this.saveState(state);
  },
  
  /**
   * Vérifie si un jeu a été complété
   */
  isGameCompleted(gameId) {
    const state = this.getState();
    return state.completedGames.includes(gameId);
  },
  
  /**
   * Obtient la liste des jeux complétés
   */
  getCompletedGames() {
    const state = this.getState();
    return state.completedGames;
  },
  
  /**
   * Obtient la liste des jeux non complétés
   */
  getIncompleteGames() {
    const state = this.getState();
    return this.GAMES.filter(game => !state.completedGames.includes(game.id));
  },
  
  /**
   * Obtient le prochain jeu recommandé en fonction de l'état actuel
   */
  getNextRecommendedGame() {
    const state = this.getState();
    const incompleteGames = this.getIncompleteGames();
    
    if (incompleteGames.length === 0) {
      return null;
    }
    
    // Si une route précédente existe, suggérer un jeu différent
    const lastRoute = state.lastVisitedRoute;
    if (lastRoute) {
      const differentGames = incompleteGames.filter(game => game.route !== lastRoute);
      if (differentGames.length > 0) {
        return differentGames[0];
      }
    }
    
    return incompleteGames[0];
  },
  
  /**
   * Met à jour la dernière route visitée
   */
  updateLastVisitedRoute(route) {
    const state = this.getState();
    state.lastVisitedRoute = route;
    return this.saveState(state);
  },
  
  /**
   * Obtient la progression globale du parcours en pourcentage
   */
  getProgressPercentage() {
    const state = this.getState();
    const totalGames = this.GAMES.length;
    const completedGames = state.completedGames.length;
    
    return Math.round((completedGames / totalGames) * 100);
  },
  
  /**
   * Vérifie si le tour du profil a été complété
   */
  isProfileTourCompleted() {
    const state = this.getState();
    return state.profileTourCompleted;
  },
  
  /**
   * Démarre le tour guidé du profil
   */
  startProfileTour() {
    const state = this.getState();
    state.profileTourStep = 0;
    state.visitedProfileSections = [];
    return this.saveState(state);
  },
  
  /**
   * Avance à l'étape suivante du tour du profil
   */
  nextProfileTourStep() {
    const state = this.getState();
    state.profileTourStep++;
    
    // Si on a atteint la fin du tour
    if (state.profileTourStep >= this.PROFILE_SECTIONS.length) {
      this.completeProfileTour();
    } else {
      this.saveState(state);
    }
    
    return state.profileTourStep;
  },
  
  /**
   * Marque le tour du profil comme terminé
   */
  completeProfileTour() {
    const state = this.getState();
    state.profileTourCompleted = true;
    
    // Mettre à jour l'étape du parcours si nécessaire
    if (state.currentStep === this.STEPS.PROFILE_INTRO) {
      state.currentStep = this.STEPS.PROFILE_TOUR_COMPLETED;
    }
    
    return this.saveState(state);
  },
  
  /**
   * Marque une section du profil comme visitée
   */
  markProfileSectionVisited(sectionId) {
    const state = this.getState();
    
    if (!state.visitedProfileSections.includes(sectionId)) {
      state.visitedProfileSections.push(sectionId);
      this.saveState(state);
    }
    
    // Vérifier si toutes les sections ont été visitées
    if (state.visitedProfileSections.length === this.PROFILE_SECTIONS.length) {
      this.completeProfileTour();
    }
    
    return state.visitedProfileSections;
  },
  
  /**
   * Obtient les messages contextuels pour le profil selon l'étape du tour
   */
  getProfileTourMessage(sectionId) {
    const section = this.PROFILE_SECTIONS.find(s => s.id === sectionId);
    return section ? section.description : "Explore cette section pour découvrir ses fonctionnalités.";
  },
  
  /**
   * Obtient des messages contextuels en fonction de l'étape actuelle et du contexte
   */
  getContextualMessages(context, step = null) {
    const state = this.getState();
    const currentStep = step !== null ? step : state.currentStep;
    
    // Messages par défaut pour chaque contexte
    const defaultMessages = {
      dashboard: [
        "Bienvenue dans ton tableau de bord ! Clique sur ton avatar au centre pour commencer ton aventure.",
        "Tu peux découvrir différents jeux et activités qui t'aideront à développer tes compétences."
      ],
      profile: [
        "Voici ton profil ! Tu peux voir tes compétences et tes badges ici.",
        "Pour continuer ton aventure, clique sur \"Jouer maintenant\" dans la section \"Ma prochaine activité\"."
      ],
      games: [
        "Tu progresses bien dans ton parcours ! Continue à explorer les différents jeux.",
        "Chaque jeu te permettra de développer des compétences différentes."
      ],
      environment: [
        "Tu peux personnaliser ton environnement ici !",
        "Choisis le thème qui te plaît le plus pour te sentir à l'aise."
      ]
    };
    
    // Messages spécifiques à l'étape du parcours
    const stepMessages = {
      [this.STEPS.DASHBOARD_INTRO]: {
        dashboard: [
          "Bienvenue dans ton parcours guidé ! Je suis là pour t'accompagner.",
          "Pour commencer, clique sur ton avatar au centre de l'écran."
        ]
      },
      [this.STEPS.CLICK_AVATAR]: {
        dashboard: [
          "Super ! Maintenant, clique sur ton avatar au centre pour accéder à ton profil.",
          "C'est là que tu pourras commencer à explorer les différentes activités."
        ]
      },
      [this.STEPS.PROFILE_INTRO]: {
        profile: [
          "Te voilà sur ton profil ! Veux-tu que je te fasse visiter pour te montrer toutes les sections ?",
          "Clique sur \"Oui\" pour découvrir chaque section de ton profil en détail."
        ]
      },
      [this.STEPS.PROFILE_TOUR_COMPLETED]: {
        profile: [
          "Tu connais maintenant toutes les sections de ton profil !",
          "Pour commencer ton aventure, cherche la section \"Ma prochaine activité\" et clique sur \"Jouer maintenant\"."
        ]
      },
      [this.STEPS.FIRST_GAME]: {
        games: [
          "Excellent choix pour ton premier jeu ! Prends ton temps pour l'explorer.",
          "N'hésite pas à me demander de l'aide si tu as des questions."
        ],
        scenarios: [
          "Dans ce jeu, tu vas pouvoir tester tes compétences sociales dans différentes situations.",
          "Réfléchis bien à chaque choix, ils influenceront tes résultats !"
        ],
        skills: [
          "La roue des compétences te permet de mieux te connaître.",
          "Tourne la roue et indique ton niveau pour chaque compétence !"
        ],
        metiers: [
          "Découvre différents métiers qui pourraient t'intéresser !",
          "Tu peux liker ceux qui t'attirent et passer les autres."
        ]
      },
      [this.STEPS.CONTINUE_GAMES]: {
        dashboard: [
          "Bravo pour avoir terminé ton premier jeu ! Il te reste encore d'autres activités à découvrir.",
          "Retourne à ton profil pour choisir une nouvelle activité."
        ],
        profile: [
          "Tu as déjà complété un jeu, c'est super ! Continue sur ta lancée.",
          "Choisis une nouvelle activité dans la section \"Ma prochaine activité\"."
        ],
        games: [
          "Tu avances bien dans ton parcours ! Continue à explorer d'autres jeux.",
          "Chaque jeu te fait développer des compétences différentes."
        ]
      },
      [this.STEPS.ENVIRONMENT]: {
        dashboard: [
          "Tu as presque terminé ton parcours ! Il ne te reste plus qu'à personnaliser ton environnement.",
          "Va dans la section \"Environnement\" pour finaliser ton parcours."
        ],
        environment: [
          "C'est la dernière étape de ton parcours ! Personnalise ton environnement selon tes préférences.",
          "Choisis le thème qui te correspond le mieux."
        ]
      },
      [this.STEPS.JOURNEY_COMPLETE]: {
        dashboard: [
          "Félicitations ! Tu as terminé l'ensemble du parcours guidé.",
          "Tu peux maintenant explorer librement toutes les fonctionnalités de la plateforme."
        ],
        profile: [
          "Bravo ! Tu as complété tous les jeux du parcours.",
          "Regarde toutes les compétences que tu as développées !"
        ]
      }
    };
    
    // Déterminer les messages à afficher
    const stepContextMessages = stepMessages[currentStep] && stepMessages[currentStep][context];
    const defaultContextMessages = defaultMessages[context];
    
    // Retourner les messages spécifiques à l'étape et au contexte, ou les messages par défaut
    return stepContextMessages || defaultContextMessages || [
      "Je suis là pour t'aider dans ton parcours !",
      "N'hésite pas à explorer les différentes fonctionnalités."
    ];
  },
  
  /**
   * Obtient des suggestions d'actions en fonction de l'étape et du contexte
   */
  getContextualSuggestions(context, step = null) {
    const state = this.getState();
    const currentStep = step !== null ? step : state.currentStep;
    
    // Suggérer le prochain jeu à essayer
    const nextGame = this.getNextRecommendedGame();
    
    // Suggestions par défaut
    const defaultSuggestions = {
      dashboard: [
        { text: "Voir mon profil", action: "goToProfile", route: "/user-profile" },
        { text: "Explorer les jeux", action: "exploreGames" }
      ],
      profile: [
        { text: "Jouer maintenant", action: "startNextGame" },
        { text: "Voir mes badges", action: "showBadges" }
      ],
      games: [
        { text: "Continuer ce jeu", action: "continueCurrentGame" },
        { text: "Essayer un autre jeu", action: "suggestOtherGame" }
      ]
    };
    
    // Suggestions spécifiques à l'étape
    const stepSuggestions = {
      [this.STEPS.DASHBOARD_INTRO]: {
        dashboard: [
          { text: "Commencer mon parcours", action: "goToProfile", route: "/user-profile" },
          { text: "Comment ça marche ?", action: "showHelp" }
        ]
      },
      [this.STEPS.CLICK_AVATAR]: {
        dashboard: [
          { text: "Cliquer sur l'avatar central", highlight: "centralAvatar", action: "goToProfile" },
          { text: "En savoir plus", action: "showHelp" }
        ]
      },
      [this.STEPS.PROFILE_INTRO]: {
        profile: [
          { text: "Explorer mon profil en détail", action: "startProfileTour" },
          { text: "Jouer directement", highlight: "playNowButton", action: "startNextGame" }
        ]
      },
      [this.STEPS.PROFILE_TOUR_COMPLETED]: {
        profile: [
          { text: "Jouer maintenant", highlight: "playNowButton", action: "startNextGame" },
          { text: "Voir mes badges en détail", action: "exploreProfile" }
        ]
      },
      [this.STEPS.FIRST_GAME]: {
        games: [
          { text: "Comprendre les règles", action: "showGameRules" },
          { text: "Retourner au profil", route: "/user-profile" }
        ]
      },
      [this.STEPS.CONTINUE_GAMES]: {
        dashboard: [
          { text: "Continuer mon parcours", action: "goToProfile", route: "/user-profile" },
          { text: "Voir ma progression", action: "showProgress" }
        ],
        profile: [
          { text: "Jouer à " + (nextGame ? nextGame.name : "un autre jeu"), action: "startNextGame" },
          { text: "Voir mes compétences", action: "showSkills" }
        ]
      },
      [this.STEPS.ENVIRONMENT]: {
        dashboard: [
          { text: "Personnaliser mon environnement", route: "/environment" },
          { text: "Voir ma progression", action: "showProgress" }
        ],
        environment: [
          { text: "Choisir un thème", highlight: "themeSelector", action: "selectTheme" },
          { text: "Terminer mon parcours", action: "completeJourney" }
        ]
      },
      [this.STEPS.JOURNEY_COMPLETE]: {
        dashboard: [
          { text: "Explorer librement", action: "exploreFreely" },
          { text: "Recommencer le parcours", action: "restartJourney" }
        ]
      }
    };
    
    // Suggestions spécifiques pour le tour du profil
    if (context === 'profile' && !state.profileTourCompleted) {
      return [
        { text: "Faire le tour du profil", action: "startProfileTour" },
        { text: "Plus tard", action: "dismissProfileGuide" }
      ];
    }
    
    // Déterminer les suggestions à afficher
    const stepContextSuggestions = stepSuggestions[currentStep] && stepSuggestions[currentStep][context];
    const defaultContextSuggestions = defaultSuggestions[context];
    
    // Retourner les suggestions spécifiques à l'étape et au contexte, ou les suggestions par défaut
    return stepContextSuggestions || defaultContextSuggestions || [
      { text: "Retour au tableau de bord", route: "/dashboard" },
      { text: "Besoin d'aide ?", action: "showHelp" }
    ];
  },
  
  /**
   * Réinitialise complètement le parcours utilisateur
   */
  resetJourney() {
    return this.saveState({
      currentStep: this.STEPS.DASHBOARD_INTRO,
      completedGames: [],
      lastVisitedRoute: null,
      hasSeenGuide: false,
      dismissCount: 0,
      customPreferences: {},
      timestamp: Date.now(),
      profileTourStep: 0,
      profileTourCompleted: false,
      visitedProfileSections: []
    });
  }
};

export default UserJourneyService;