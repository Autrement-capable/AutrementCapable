// src/game/Character.js - Gestion du personnage
import * as PIXI from 'pixi.js';

export default class Character {
  init(app, tileMap, startX = 5, startY = 5) {
    this.app = app;
    this.tileMap = tileMap;
    this.tileX = startX;
    this.tileY = startY;
    this.sprite = null;
    this.container = new PIXI.Container();
    this.tileMap.container.addChild(this.container);
    
    this.movementSpeed = 4; // Tiles par seconde
    this.isMoving = false;
    this.targetX = startX;
    this.targetY = startY;
  }

  async loadCharacter() {
    // Créer un personnage simple avec un cercle au lieu de charger une image
    const graphics = new PIXI.Graphics()
      .circle(0, 0, this.tileMap.tileSize / 2 * 0.8)
      .fill(0xFF0000); // Rouge
      
    this.sprite = new PIXI.Sprite(this.app.renderer.generateTexture(graphics));
    this.sprite.anchor.set(0.5);
    
    this.container.addChild(this.sprite);
    this.updatePosition();
    
    return true;
  }

  updatePosition() {
    const tileSize = this.tileMap.tileSize;
    this.sprite.x = (this.tileX + 0.5) * tileSize;
    this.sprite.y = (this.tileY + 0.5) * tileSize;
    
    // Centrer la carte sur le personnage
    this.tileMap.centerOn(this.tileX + 0.5, this.tileY + 0.5);
  }

  moveBy(dx, dy) {
    const newX = this.tileX + dx;
    const newY = this.tileY + dy;
    
    if (this.tileMap.isValidPosition(newX, newY)) {
      this.tileX = newX;
      this.tileY = newY;
      this.updatePosition();
      return true;
    }
    
    return false;
  }

  // Méthodes directionnelles pour faciliter le mouvement
  moveUp() {
    return this.moveBy(0, -1);
  }
  
  moveDown() {
    return this.moveBy(0, 1);
  }
  
  moveLeft() {
    return this.moveBy(-1, 0);
  }
  
  moveRight() {
    return this.moveBy(1, 0);
  }

  // Animation de mouvement fluide (version simplifiée)
  startMovementAnimation(direction) {
    if (this.isMoving) return false;
    
    let success = false;
    
    switch (direction) {
      case 'up':
        success = this.moveUp();
        break;
      case 'down':
        success = this.moveDown();
        break;
      case 'left':
        success = this.moveLeft();
        break;
      case 'right':
        success = this.moveRight();
        break;
    }
    
    return success;
  }
}