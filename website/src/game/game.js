// src/game/game.js
import TileMap from './TileMap';
import Character from './Character';
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
    
    this.mapWidth = 20;
    this.mapHeight = 15;
    
    // Garder une référence aux contrôles pour pouvoir les détacher
    this.keyDownHandler = this.handleKeyDown.bind(this);
    this.keyUpHandler = this.handleKeyUp.bind(this);
  }

  async initialize() {
    // Créer et initialiser la carte
    this.tileMap = new TileMap();
    this.tileMap.init(this.app);
    await this.tileMap.loadTileTextures();
    this.tileMap.generateMap(this.mapWidth, this.mapHeight);
    
    // Créer et initialiser le personnage
    this.character = new Character();
    this.character.init(this.app, this.tileMap);
    await this.character.loadCharacter();
    
    // Configurer les contrôles
    this.setupControls();
    
    // Démarrer la boucle de jeu
    this.app.ticker.add(this.gameLoop.bind(this));
  }

  setupControls() {
    // Ajouter les écouteurs d'événements pour le clavier
    window.addEventListener('keydown', this.keyDownHandler);
    window.addEventListener('keyup', this.keyUpHandler);
  }

  removeControls() {
    // Supprimer les écouteurs d'événements
    window.removeEventListener('keydown', this.keyDownHandler);
    window.removeEventListener('keyup', this.keyUpHandler);
  }

  handleKeyDown(e) {
    this.keysPressed[e.key] = true;
  }

  handleKeyUp(e) {
    this.keysPressed[e.key] = false;
  }

  gameLoop() {
    // Gérer les mouvements du personnage
    if (this.keysPressed['ArrowUp'] || this.keysPressed['z'] || this.keysPressed['w']) {
      this.character.moveUp();
    }
    if (this.keysPressed['ArrowDown'] || this.keysPressed['s']) {
      this.character.moveDown();
    }
    if (this.keysPressed['ArrowLeft'] || this.keysPressed['q'] || this.keysPressed['a']) {
      this.character.moveLeft();
    }
    if (this.keysPressed['ArrowRight'] || this.keysPressed['d']) {
      this.character.moveRight();
    }
  }

  resize() {
    // Mettre à jour les dimensions du jeu si la taille de la fenêtre change
    this.app.resize();
  }

  destroy() {
    // Nettoyer les ressources lors de la destruction du jeu
    this.removeControls();
    this.app.destroy(true, { children: true, texture: true, baseTexture: true });
  }
}