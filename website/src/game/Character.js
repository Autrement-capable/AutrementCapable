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
    
    // Paramètres de mouvement
    this.isMoving = false;
    this.targetX = startX;
    this.targetY = startY;
    this.visualX = startX;
    this.visualY = startY;
    
    // Paramètres de vitesse
    this.movementSpeed = 3; // Vitesse (cases par seconde)
    this.moveDelay = 200; // Délai entre deux mouvements (en ms)
    this.lastMoveTime = 0; // Temps du dernier mouvement
    
    // Direction du personnage (pour savoir où est l'objet à interagir)
    this.direction = 'down'; // 'up', 'down', 'left', 'right'
    
    // Message pour afficher les interactions
    this.messageTextValue = "";
    this.messageContainer = new PIXI.Container();
    this.messageContainer.zIndex = 1000; // S'assurer qu'il apparaît au-dessus de tout
    app.stage.addChild(this.messageContainer);
  }

  async loadCharacter() {
    // Créer un personnage simple avec un indicateur de direction
    const graphics = new PIXI.Graphics();
    
    // Corps du personnage (cercle rouge)
    graphics.fill(0xFF0000); // Rouge
    graphics.circle(0, 0, this.tileMap.tileSize / 2 * 0.7);
    graphics.fill();
    
    // Indicateur de direction (cercle blanc) - placé vers le haut par défaut
    graphics.fill(0xFFFFFF); // Blanc
    graphics.circle(0, -this.tileMap.tileSize / 3 * 0.7, this.tileMap.tileSize / 6);
    graphics.fill();
    
    this.sprite = new PIXI.Sprite(this.app.renderer.generateTexture(graphics));
    this.sprite.anchor.set(0.5);
    
    this.container.addChild(this.sprite);
    this.updatePosition();
    
    // Initialiser le système de message
    this.initMessageSystem();
    
    return true;
  }
  
  initMessageSystem() {
    // Nettoyer le conteneur existant
    this.messageContainer.removeChildren();
    
    // 1. Créer un fond noir semi-transparent plus grand
    this.messageBackground = new PIXI.Graphics();
    this.messageBackground.fill({0x000000: 0.8}); // Noir plus opaque
    this.messageBackground.roundRect(0, 0, this.app.screen.width * 0.7, 80, 10);
    this.messageBackground.fill();
    this.messageContainer.addChild(this.messageBackground);
    
    // 2. Ajouter un texte avec une police plus grande et plus visible
    // Utiliser directement le constructeur PIXI.Text avec un objet pour les options
    this.messageText = new PIXI.Text({
      text: "Message de test",
      style: {
        fontFamily: "Arial",
        fontSize: 18,
        align: "center",
        wordWrap: true,
        wordWrapWidth: this.app.screen.width * 0.65
      }
    });
    
    // Positionner le texte au centre du fond
    this.messageText.x = 15;
    this.messageText.y = 15;
    this.messageContainer.addChild(this.messageText);
    
    // 3. Positionner le conteneur en haut de l'écran de manière plus visible
    this.messageContainer.x = this.app.screen.width * 0.15;
    this.messageContainer.y = 30;
    
    // 4. Ajouter une bordure au message pour le rendre plus visible
    const border = new PIXI.Graphics();
    border.setStrokeStyle (2, 0xFFFFFF, 1); // Ligne blanche
    border.roundRect(0, 0, this.app.screen.width * 0.7, 80, 10);
    this.messageContainer.addChild(border);
    
    // Cacher le message au départ
    this.messageContainer.visible = false;
  }

  updatePosition() {
    const tileSize = this.tileMap.tileSize;
    this.sprite.x = (this.tileX + 0.5) * tileSize;
    this.sprite.y = (this.tileY + 0.5) * tileSize;
    
    // Mise à jour de l'indicateur de direction
    this.updateDirectionIndicator();
  }
  
  updateDirectionIndicator() {
    // Mettre à jour la rotation selon la direction
    switch(this.direction) {
      case 'up':
        this.sprite.rotation = 0; // 0 degré - déjà vers le haut
        break;
      case 'down':
        this.sprite.rotation = Math.PI; // 180 degrés - vers le bas
        break;
      case 'left':
        this.sprite.rotation = -Math.PI / 2; // -90 degrés - vers la gauche
        break;
      case 'right':
        this.sprite.rotation = Math.PI / 2; // 90 degrés - vers la droite
        break;
    }
  }

  moveBy(dx, dy) {
    // Vérifier si le délai de mouvement est passé
    const currentTime = Date.now();
    if (currentTime - this.lastMoveTime < this.moveDelay) {
      return false; // Ne pas bouger si le délai n'est pas écoulé
    }
    
    // Si le personnage est déjà en mouvement, ne pas démarrer un nouveau mouvement
    if (this.isMoving) {
      return false;
    }
    
    // Mettre à jour la direction
    if (dx > 0) this.direction = 'right';
    else if (dx < 0) this.direction = 'left';
    else if (dy > 0) this.direction = 'down';
    else if (dy < 0) this.direction = 'up';
    
    const newX = this.tileX + dx;
    const newY = this.tileY + dy;
    
    if (this.tileMap.isValidPosition(newX, newY)) {
      // Mettre à jour la dernière heure de mouvement
      this.lastMoveTime = currentTime;
      
      // Définir les coordonnées cibles et commencer l'animation
      this.targetX = newX;
      this.targetY = newY;
      this.isMoving = true;
      this.visualX = this.tileX;
      this.visualY = this.tileY;
      this.tileX = newX;
      this.tileY = newY;
      
      // Démarrer l'animation de mouvement
      this.animate();
      
      return true;
    }
    
    // Même si on ne bouge pas, mettre à jour la direction
    this.updateDirectionIndicator();
    return false;
  }
  
  animate() {
    // Animation de déplacement fluide
    const tileSize = this.tileMap.tileSize;
    const startX = (this.visualX + 0.5) * tileSize;
    const startY = (this.visualY + 0.5) * tileSize;
    const endX = (this.targetX + 0.5) * tileSize;
    const endY = (this.targetY + 0.5) * tileSize;
    
    // Durée de l'animation en secondes (1/vitesse)
    const duration = 1 / this.movementSpeed;
    let startTime = null;
    
    const animateStep = (timestamp) => {
      if (!startTime) startTime = timestamp;
      const elapsed = (timestamp - startTime) / 1000; // en secondes
      const progress = Math.min(elapsed / duration, 1);
      
      // Position interpolée
      const currentX = startX + (endX - startX) * progress;
      const currentY = startY + (endY - startY) * progress;
      
      // Mettre à jour la position visuelle
      this.sprite.x = currentX;
      this.sprite.y = currentY;
      
      // Ne plus centrer la carte sur le personnage pendant l'animation
      
      if (progress < 1) {
        // Continuer l'animation
        requestAnimationFrame(animateStep);
      } else {
        // Animation terminée
        this.isMoving = false;
        this.updatePosition();
      }
    };
    
    // Démarrer l'animation
    requestAnimationFrame(animateStep);
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
  
  // Obtenir la position devant le personnage (pour l'interaction)
  getPositionInFront() {
    switch(this.direction) {
      case 'up':
        return { x: this.tileX, y: this.tileY - 1 };
      case 'down':
        return { x: this.tileX, y: this.tileY + 1 };
      case 'left':
        return { x: this.tileX - 1, y: this.tileY };
      case 'right':
        return { x: this.tileX + 1, y: this.tileY };
    }
  }
  
  // Afficher un message
  showMessage(message, duration = 3000) {
    // Mettre à jour le texte du message
    this.messageTextValue = message;
    if (this.messageText) {
      // Mise à jour du texte avec la syntaxe de PIXI v8
      this.messageText.text = message;
    }
    
    // Rendre le conteneur visible
    this.messageContainer.visible = true;
    
    // Assurer que le conteneur est positionné correctement
    this.messageContainer.x = this.app.screen.width * 0.15;
    this.messageContainer.y = 30;
    
    // Amener le conteneur au premier plan
    this.app.stage.addChild(this.messageContainer);
    
    // Cacher le message après un certain temps
    clearTimeout(this.messageTimeout);
    this.messageTimeout = setTimeout(() => {
      this.messageContainer.visible = false;
    }, duration);
  }

  // Animation de mouvement fluide
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