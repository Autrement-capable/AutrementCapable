// src/game/TileMap.js - Gestion de la carte avec des tiles
import * as PIXI from 'pixi.js';

export default class TileMap {
  init(app, tileSize = 32) {
    this.app = app;
    this.tileSize = tileSize;
    this.container = new PIXI.Container();
    this.tilesContainer = new PIXI.Container();
    this.container.addChild(this.tilesContainer);
    this.app.stage.addChild(this.container);
    
    this.tileTextures = {};
    this.map = [];
  }

  // Charger les textures des tiles
  async loadTileTextures() {
    const tileTypes = ['grass', 'water', 'sand', 'stone', 'dirt'];
    
    // Initialiser l'objet des textures
    for (const type of tileTypes) {
      // Version simplifiée pour les tests - utilise une texture de couleur unique
      // au lieu de charger des images
      const color = this.getTileColor(type);
      const graphics = new PIXI.Graphics()
        .rect(0, 0, this.tileSize, this.tileSize)
        .fill(color);
      
      this.tileTextures[type] = this.app.renderer.generateTexture(graphics);
    }
    
    return true;
  }
  
  // Obtenir une couleur pour chaque type de tile
  getTileColor(type) {
    switch(type) {
      case 'grass': return 0x7CFC00; // vert clair
      case 'water': return 0x1E90FF; // bleu
      case 'sand': return 0xFFD700;  // jaune doré
      case 'stone': return 0x808080; // gris
      case 'dirt': return 0x8B4513;  // brun
      default: return 0xFFFFFF;      // blanc par défaut
    }
  }

  // Générer une carte aléatoire simple
  generateMap(width, height) {
    this.mapWidth = width;
    this.mapHeight = height;
    this.map = [];

    for (let y = 0; y < height; y++) {
      const row = [];
      for (let x = 0; x < width; x++) {
        // Simple algorithme pour générer une carte avec de l'herbe et de l'eau
        const rand = Math.random();
        if (rand < 0.7) {
          row.push('grass');
        } else if (rand < 0.9) {
          row.push('sand');
        } else {
          row.push('water');
        }
      }
      this.map.push(row);
    }

    this.renderMap();
  }

  // Afficher la carte
  renderMap() {
    this.tilesContainer.removeChildren();

    for (let y = 0; y < this.mapHeight; y++) {
      for (let x = 0; x < this.mapWidth; x++) {
        const tileType = this.map[y][x];
        const tile = new PIXI.Sprite(this.tileTextures[tileType]);
        
        tile.x = x * this.tileSize;
        tile.y = y * this.tileSize;
        tile.width = this.tileSize;
        tile.height = this.tileSize;
        
        this.tilesContainer.addChild(tile);
      }
    }
  }

  // Vérifier si une position est valide pour le déplacement
  isValidPosition(x, y) {
    // Vérifier si la position est dans les limites de la carte
    if (x < 0 || x >= this.mapWidth || y < 0 || y >= this.mapHeight) {
      return false;
    }
    
    // Vérifier si la tile est traversable (l'eau n'est pas traversable)
    return this.map[y][x] !== 'water';
  }

  // Centrer la vue sur une position
  centerOn(x, y) {
    const centerX = this.app.screen.width / 2;
    const centerY = this.app.screen.height / 2;
    
    this.container.x = centerX - (x * this.tileSize);
    this.container.y = centerY - (y * this.tileSize);
  }
}