// Modifications à apporter au fichier Game.js
import TileMap from './TileMap';
import Character from './Character';
import InteractiveObject from './InteractiveObject';
import Pathfinding from './Pathfinding';
import * as PIXI from 'pixi.js';

export default class Game {
  async init(canvasContainer) {
    // Créer l'application PixiJS selon la méthode recommandée pour v8
    this.app = new PIXI.Application();
    
    // Initialiser avec les options
    await this.app.init({
      backgroundColor: 0x000000,
      resizeTo: canvasContainer,
    });
    
    // Ajouter le canvas au conteneur
    canvasContainer.appendChild(this.app.canvas);
    
    this.tileMap = null;
    this.character = null;
    this.keysPressed = {};
    this.objects = []; // Liste des objets interactifs
    this.pathfinding = null; // Système de pathfinding
    this.currentPath = []; // Chemin actuel suivi par le personnage
    this.pathMarkers = new PIXI.Container(); // Conteneur pour visualiser le chemin
    this.followingPath = false; // Indique si le personnage suit un chemin
    
    this.mapWidth = 20;
    this.mapHeight = 15;
    
    // Variable pour éviter de déclencher l'interaction plusieurs fois
    this.interactionCooldown = false;
    
    // Garder une référence aux contrôles pour pouvoir les détacher
    this.keyDownHandler = this.handleKeyDown.bind(this);
    this.keyUpHandler = this.handleKeyUp.bind(this);
    this.clickHandler = this.handleClick.bind(this);
    
    // NOUVEAU: Empêcher les mouvements diagonaux
    this.lastMoveDirection = null;
    this.inputQueue = [];
  }

  async initialize() {
    // Créer et initialiser la carte
    this.tileMap = new TileMap();
    this.tileMap.init(this.app);
    await this.tileMap.loadTileTextures();
    this.tileMap.generateMap(this.mapWidth, this.mapHeight);
    
    // Initialiser le pathfinding
    this.pathfinding = new Pathfinding(this.tileMap);
    
    // Ajouter le conteneur de marqueurs de chemin
    this.tileMap.container.addChild(this.pathMarkers);
    
    // Créer et initialiser le personnage
    this.character = new Character();
    this.character.init(this.app, this.tileMap, 10, 12); // Position de départ près de l'entrée
    await this.character.loadCharacter();
    
    // Créer les objets interactifs
    await this.createInteractiveObjects();
    
    // Configurer les contrôles
    this.setupControls();
    
    // Démarrer la boucle de jeu
    this.app.ticker.add(this.gameLoop.bind(this));
    
    // Message de bienvenue
    setTimeout(() => {
      this.character.showMessage("Bienvenue dans votre maison ! Cliquez sur une case pour vous déplacer ou appuyez sur E pour interagir avec les objets.", 5000);
    }, 500);
  }
  
  async createInteractiveObjects() {
    // Créer un objet interactif pour chaque emplacement d'objet dans la carte
    for (const objectInfo of this.tileMap.objectPositions) {
      const object = new InteractiveObject(
        this.app,
        this.tileMap,
        objectInfo.x,
        objectInfo.y,
        objectInfo.type,
        objectInfo.roomName
      );
      
      this.objects.push(object);
    }
  }

  setupControls() {
    // Ajouter les écouteurs d'événements pour le clavier
    window.addEventListener('keydown', this.keyDownHandler);
    window.addEventListener('keyup', this.keyUpHandler);
    
    // Ajouter l'écouteur de clic pour le déplacement
    this.app.canvas.addEventListener('click', this.clickHandler);
  }

  removeControls() {
    // Supprimer les écouteurs d'événements
    window.removeEventListener('keydown', this.keyDownHandler);
    window.removeEventListener('keyup', this.keyUpHandler);
    this.app.canvas.removeEventListener('click', this.clickHandler);
  }

  handleKeyDown(e) {
    const key = e.key.toLowerCase();
    
    // Si la touche n'est pas déjà pressée, l'ajouter
    if (!this.keysPressed[key]) {
      this.keysPressed[key] = true;
      
      // Ajouter à la file d'attente des entrées pour le mouvement séquentiel
      if (['arrowup', 'arrowdown', 'arrowleft', 'arrowright', 'z', 'q', 's', 'd', 'w', 'a'].includes(key)) {
        if (!this.inputQueue.includes(key)) {
          this.inputQueue.push(key);
          
          // Annuler le suivi de chemin automatique quand l'utilisateur utilise le clavier
          this.clearPath();
        }
      }
    }
    
    // Interaction avec la touche E
    if (key === 'e') {
      this.triggerInteraction();
    }
    
    // Empêcher le défilement de la page avec les touches fléchées
    if (['arrowup', 'arrowdown', 'arrowleft', 'arrowright', ' '].includes(key)) {
      e.preventDefault();
    }
  }

  handleKeyUp(e) {
    const key = e.key.toLowerCase();
    this.keysPressed[key] = false;
    
    // Retirer de la file d'attente
    const index = this.inputQueue.indexOf(key);
    if (index !== -1) {
      this.inputQueue.splice(index, 1);
    }
  }
  
  handleClick(e) {
    // Annuler toute entrée clavier en cours
    this.inputQueue = [];
    
    // Calculer les coordonnées du clic dans le repère du jeu
    const rect = this.app.canvas.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const clickY = e.clientY - rect.top;
    
    // Convertir en coordonnées de la grille de jeu
    const tileSize = this.tileMap.tileSize * this.tileMap.container.scale.x;
    const offsetX = this.tileMap.container.x;
    const offsetY = this.tileMap.container.y;
    
    const gridX = Math.floor((clickX - offsetX) / tileSize);
    const gridY = Math.floor((clickY - offsetY) / tileSize);
    
    // Vérifier si la position est valide
    if (this.tileMap.isValidPosition(gridX, gridY)) {
      // Trouver un chemin vers la destination
      this.findPathToDestination(gridX, gridY);
    }
  }
  
  findPathToDestination(destX, destY) {
    // Vérifier si la destination est la même que la position actuelle
    if (this.character.tileX === destX && this.character.tileY === destY) {
      return; // Déjà à destination
    }
    
    // Utiliser le pathfinding pour trouver un chemin
    const path = this.pathfinding.findPath(
      this.character.tileX, 
      this.character.tileY,
      destX, 
      destY
    );
    
    // Si un chemin a été trouvé
    if (path.length > 0) {
      // Supprimer le premier point (position actuelle)
      this.currentPath = path.slice(1);
      this.followingPath = true;

    } else {
      // Afficher un message si aucun chemin n'est trouvé
      this.character.showMessage("Impossible d'atteindre cette destination.", 2000);
    }
  }
  
  clearPath() {
    this.currentPath = [];
    this.followingPath = false;
    this.pathMarkers.removeChildren();
  }
  
  followPath() {
    if (!this.followingPath || this.currentPath.length === 0 || this.character.isMoving) {
      return;
    }
    
    // Récupérer le prochain point du chemin
    const nextPoint = this.currentPath[0];
    
    // Calculer la direction à prendre
    const dx = nextPoint.x - this.character.tileX;
    const dy = nextPoint.y - this.character.tileY;
    
    let moved = false;
    
    // Déplacer le personnage dans la bonne direction
    if (dx > 0) {
      moved = this.character.moveRight();
    } else if (dx < 0) {
      moved = this.character.moveLeft();
    } else if (dy > 0) {
      moved = this.character.moveDown();
    } else if (dy < 0) {
      moved = this.character.moveUp();
    }
    
    // Si le déplacement a réussi, retirer ce point du chemin
    if (moved) {
      this.currentPath.shift();
            
      // Si le chemin est vide, on a atteint la destination
      if (this.currentPath.length === 0) {
        this.followingPath = false;
      }
    } else {
      // Si le déplacement a échoué, annuler le suivi de chemin
      this.clearPath();
    }
  }
  
  triggerInteraction() {
    // Éviter les interactions trop rapides
    if (this.interactionCooldown) return;
    
    this.interactionCooldown = true;
    setTimeout(() => { this.interactionCooldown = false; }, 500);
    
    // Obtenir la position devant le personnage
    const position = this.character.getPositionInFront();
    
    // Chercher un objet à cette position
    const object = this.objects.find(obj => obj.x === position.x && obj.y === position.y);
    
    if (object) {
      // Déclencher l'interaction avec l'objet
      const result = object.interact();
      
      // Afficher le message d'interaction
      this.character.showMessage(result.message, 3000);
    } else {
      // Si pas d'objet à cette position, vérifier si c'est une porte
      const tile = this.tileMap.map[position.y]?.[position.x];
      if (tile === 'door') {
        this.character.showMessage("Vous ouvrez la porte et passez dans l'autre pièce.", 2000);
      }
    }
  }

  gameLoop() {
    // Suivre le chemin si nécessaire
    this.followPath();
    
    // Gestion des mouvements manuels (clavier)
    if (!this.followingPath && !this.character.isMoving && this.inputQueue.length > 0) {
      const currentInput = this.inputQueue[0];
      let moved = false;
      
      // Gérer les mouvements selon la touche la plus récemment pressée
      if (currentInput === 'arrowup' || currentInput === 'z' || currentInput === 'w') {
        moved = this.character.moveUp();
      } else if (currentInput === 'arrowdown' || currentInput === 's') {
        moved = this.character.moveDown();
      } else if (currentInput === 'arrowleft' || currentInput === 'q' || currentInput === 'a') {
        moved = this.character.moveLeft();
      } else if (currentInput === 'arrowright' || currentInput === 'd') {
        moved = this.character.moveRight();
      }
      
      // Si le mouvement est bloqué (par exemple, par un mur), essayer la touche suivante
      if (!moved && this.inputQueue.length > 1) {
        this.inputQueue.shift(); // Retirer la première touche et essayer la suivante au prochain frame
      }
    }
    
    // Mettre à jour les objets interactifs
    for (const object of this.objects) {
      object.update();
      
      // Vérifier si le personnage est près de l'objet pour afficher l'invite d'interaction
      const position = this.character.getPositionInFront();
      if (object.x === position.x && object.y === position.y) {
        object.showInteractionPrompt();
      } else {
        object.hideInteractionPrompt();
      }
    }
  }

  resize() {
    // Mettre à jour les dimensions du jeu si la taille de la fenêtre change
    this.app.resize();
    
    // Repositionner les éléments d'interface
    if (this.character && this.character.messageContainer) {
      this.character.messageContainer.x = this.app.screen.width * 0.1;
      this.character.messageContainer.y = 20;
      
      // Vérifier si messageBackground existe avant d'appeler clear
      if (this.character.messageBackground) {
        this.character.messageBackground.clear();
        this.character.messageBackground.fill({0x000000: 0.7});
        this.character.messageBackground.roundRect(0, 0, this.app.screen.width * 0.8, 60, 10);
        this.character.messageBackground.fill();
      }
      
      // Mettre à jour la largeur maximale du texte
      if (this.character.messageText && this.character.messageText.style) {
        this.character.messageText.style.wordWrapWidth = this.app.screen.width * 0.75;
      }
    }
  }

  destroy() {
    // Nettoyer les ressources lors de la destruction du jeu
    this.removeControls();
    
    // Détruire les objets interactifs
    for (const object of this.objects) {
      object.destroy();
    }
    
    this.app.destroy(true, { children: true, texture: true, baseTexture: true });
  }
}