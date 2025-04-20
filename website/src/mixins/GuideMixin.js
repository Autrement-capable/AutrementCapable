export const GuideAvatarMixin = {
  data() {
    return {
      // États existants...
      guideVisible: true,
      guideContext: 'default',
      guideForcedMessage: null,
      guideForcedOptions: [],
      guideForceShow: false,
      guideAutoShowDelay: 1500,
      currentJourneyStep: 0,
      completedGames: [],
      currentGame: null,
      
      // Nouvel état pour le tour guidé du profil
      profileTourStep: 0,
      profileTourActive: false,
      highlightedSection: null,
      profileSections: [
        {
          id: 'header',
          name: 'En-tête du profil',
          selector: '.profile-header',
          description: "C'est ton profil personnel ! Tu peux voir ton avatar, ton niveau actuel et tes informations personnelles comme ton âge et ta ville."
        },
        {
          id: 'progress-map',
          name: 'Carte de progression',
          selector: '.progress-map-container',
          description: "Cette carte montre tous tes badges. Les badges débloqués sont en couleur, et les badges à débloquer sont grisés avec un cadenas. Le badge clignotant orange est ta prochaine activité recommandée !"
        },
        {
          id: 'next-activity',
          name: 'Prochaine activité',
          selector: '.next-activity',
          description: "Ici tu trouveras ta prochaine activité recommandée. Clique sur 'Jouer maintenant' pour la commencer et débloquer un nouveau badge !"
        },
        {
          id: 'badges-grid',
          name: 'Mes badges',
          selector: '.all-badges',
          description: "Cette section affiche tous tes badges, débloqués ou non. Clique sur un badge pour voir plus de détails et comment le débloquer si tu ne l'as pas encore."
        },
        {
          id: 'actions',
          name: 'Actions',
          selector: '.action-buttons',
          description: "Ces boutons te permettent de créer ton CV avec les compétences que tu as développées ou d'accéder directement à ton profil complet."
        }
      ]
    };
  },
  
  methods: {
    // Méthodes existantes...
    
    /**
     * Démarre le tour guidé du profil
     */
    startProfileTour() {
      this.profileTourActive = true;
      this.profileTourStep = 0;
      this.showProfileTourStep();
      
      // Mettre à jour l'étape du parcours utilisateur
      UserJourneyService.updateStep(UserJourneyService.STEPS.PROFILE_INTRO);
    },
    
    /**
     * Affiche l'étape actuelle du tour du profil
     */
    showProfileTourStep() {
      if (!this.profileTourActive || this.profileTourStep >= this.profileSections.length) {
        this.endProfileTour();
        return;
      }
      
      const section = this.profileSections[this.profileTourStep];
      this.highlightedSection = section.id;
      
      // Forcer l'affichage du guide avec le message approprié
      this.guideForcedMessage = section.description;
      this.guideForcedOptions = [
        { text: "Suivant", action: "nextProfileTourStep" },
        { text: "Terminer le tour", action: "endProfileTour" }
      ];
      
      // Si c'est la dernière étape, changer le texte du bouton
      if (this.profileTourStep === this.profileSections.length - 1) {
        this.guideForcedOptions[0].text = "Terminer";
      }
      
      this.guideForceShow = true;
      
      // Créer un effet de mise en évidence pour la section actuelle
      this.highlightSection(section.selector);
    },
    
    /**
     * Passe à l'étape suivante du tour du profil
     */
    nextProfileTourStep() {
      // Supprimer la mise en évidence actuelle
      this.removeHighlight();
      
      // Passer à l'étape suivante
      this.profileTourStep++;
      
      // Vérifier si on a terminé le tour
      if (this.profileTourStep >= this.profileSections.length) {
        this.endProfileTour();
        return;
      }
      
      // Afficher la nouvelle étape
      this.showProfileTourStep();
    },
    
    /**
     * Termine le tour du profil
     */
    endProfileTour() {
      // Supprimer toutes les mises en évidence
      this.removeHighlight();
      
      this.profileTourActive = false;
      this.highlightedSection = null;
      
      // Afficher un message de fin de tour
      this.guideForcedMessage = "Tu connais maintenant toutes les sections de ton profil ! N'hésite pas à explorer et à cliquer sur 'Jouer maintenant' pour commencer une activité.";
      this.guideForcedOptions = [
        { text: "Compris !", action: "dismissProfileGuide" },
        { text: "Jouer maintenant", action: "highlightPlayButton" }
      ];
      
      // Marquer le tour du profil comme terminé dans le service de parcours utilisateur
      if (typeof UserJourneyService !== 'undefined') {
        // Ajouter une nouvelle propriété pour suivre si le tour du profil a été fait
        const state = UserJourneyService.getState();
        state.hasCompletedProfileTour = true;
        UserJourneyService.saveState(state);
      }
    },
    
    /**
     * Met en évidence une section spécifique
     */
    highlightSection(selector) {
      // Supprimer d'abord toutes les mises en évidence existantes
      this.removeHighlight();
      
      // Ajouter une nouvelle mise en évidence
      setTimeout(() => {
        const element = document.querySelector(selector);
        if (element) {
          // Créer un élément de surbrillance
          const highlight = document.createElement('div');
          highlight.className = 'section-highlight';
          
          // Positionner la surbrillance autour de l'élément
          const rect = element.getBoundingClientRect();
          highlight.style.position = 'absolute';
          highlight.style.top = `${rect.top}px`;
          highlight.style.left = `${rect.left}px`;
          highlight.style.width = `${rect.width}px`;
          highlight.style.height = `${rect.height}px`;
          highlight.style.border = '3px solid #76ff03';
          highlight.style.borderRadius = '16px';
          highlight.style.boxShadow = '0 0 15px rgba(118, 255, 3, 0.7)';
          highlight.style.pointerEvents = 'none';
          highlight.style.zIndex = '1050';
          highlight.style.animation = 'highlight-pulse 2s ease-out infinite';
          
          // Ajouter la surbrillance au DOM
          document.body.appendChild(highlight);
          
          // Faire défiler jusqu'à l'élément si nécessaire
          element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }, 100);
    },
    
    /**
     * Supprime toutes les mises en évidence
     */
    removeHighlight() {
      const highlights = document.querySelectorAll('.section-highlight');
      highlights.forEach(highlight => {
        highlight.parentNode.removeChild(highlight);
      });
    },
    
    /**
     * Met en évidence le bouton "Jouer maintenant"
     */
    highlightPlayButton() {
      this.removeHighlight();
      this.highlightSection('.next-activity .play-button');
      
      this.guideForcedMessage = "Clique sur le bouton 'Jouer maintenant' pour commencer ta prochaine activité recommandée !";
      this.guideForcedOptions = [
        { text: "Compris !", action: "dismissMessage" }
      ];
      this.guideForceShow = true;
    }
  },
  
  // Ajouter un hook de cycle de vie pour détecter quand on est sur la page de profil
  mounted() {
    // Vérifier si on est sur la page de profil
    if (this.guideContext === 'profile') {
      // Vérifier si le tour du profil a déjà été effectué
      if (typeof UserJourneyService !== 'undefined') {
        const state = UserJourneyService.getState();
        if (!state.hasCompletedProfileTour) {
          // Proposer de commencer le tour du profil après un court délai
          setTimeout(() => {
            this.guideForcedMessage = "Bienvenue sur ton profil ! Veux-tu que je te fasse visiter pour te montrer toutes les fonctionnalités ?";
            this.guideForcedOptions = [
              { text: "Oui, je veux découvrir mon profil", action: "startProfileTour" },
              { text: "Non merci, je vais explorer seul", action: "dismissProfileGuide" }
            ];
            this.guideForceShow = true;
          }, 1000);
        }
      }
    }
  },
  
  // Nettoyage des effets visuels lors de la destruction du composant
  beforeDestroy() {
    this.removeHighlight();
  }
};

export default GuideAvatarMixin;