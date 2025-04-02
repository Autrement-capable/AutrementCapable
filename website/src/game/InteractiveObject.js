import * as PIXI from 'pixi.js';

export default class InteractiveObject {
  constructor(app, tileMap, x, y, type, roomName) {
    this.app = app;
    this.tileMap = tileMap;
    this.x = x;
    this.y = y;
    this.type = type;
    this.roomName = roomName;
    this.tileSize = tileMap.tileSize;
    
    this.sprite = null;
    this.interactionText = null;
    this.state = 'idle'; // États possibles: idle, active, used
    
    this.container = new PIXI.Container();
    this.tileMap.container.addChild(this.container);
    
    this.init();
  }
  
  init() {
    // Créer le sprite de l'objet
    const graphics = new PIXI.Graphics();
    
    // Différentes apparences selon le type d'objet
    switch(this.type) {
      case 'canapé':
        graphics.fill(0x8080FF); // Bleu pour le canapé
        graphics.rect(-this.tileSize/2, -this.tileSize/3, this.tileSize, this.tileSize/2);
        break;
      case 'télévision':
        graphics.fill(0x000000); // Noir pour la TV
        graphics.rect(-this.tileSize/3, -this.tileSize/3, this.tileSize*2/3, this.tileSize*2/3);
        // Écran
        graphics.fill(0x87CEEB); // Bleu ciel pour l'écran
        graphics.rect(-this.tileSize/3 + 2, -this.tileSize/3 + 2, this.tileSize*2/3 - 4, this.tileSize*2/3 - 4);
        break;
      case 'bibliothèque':
        graphics.fill(0x8B4513); // Brun pour la bibliothèque
        graphics.rect(-this.tileSize/2, -this.tileSize/2, this.tileSize, this.tileSize);
        // Étagères
        graphics.setStrokeStyle(1, 0x000000);
        for (let i = 1; i < 4; i++) {
          graphics.moveTo(-this.tileSize/2, -this.tileSize/2 + i*this.tileSize/4);
          graphics.lineTo(this.tileSize/2, -this.tileSize/2 + i*this.tileSize/4);
        }
        break;
      case 'réfrigérateur':
        graphics.fill(0xFFFFFF); // Blanc pour le frigo
        graphics.rect(-this.tileSize/3, -this.tileSize/2, this.tileSize*2/3, this.tileSize);
        // Poignée
        graphics.fill(0x808080);
        graphics.rect(this.tileSize/4, -this.tileSize/3, this.tileSize/10, this.tileSize*2/3);
        break;
      case 'four':
        graphics.fill(0x808080); // Gris pour le four
        graphics.rect(-this.tileSize/2, -this.tileSize/3, this.tileSize, this.tileSize*2/3);
        // Porte du four
        graphics.fill(0x000000);
        graphics.rect(-this.tileSize/3, -this.tileSize/4, this.tileSize*2/3, this.tileSize/2);
        break;
      case 'lit':
        graphics.fill(0x8B4513); // Brun pour le cadre de lit
        graphics.rect(-this.tileSize/2, -this.tileSize/2, this.tileSize, this.tileSize);
        // Matelas
        graphics.fill(0xFFFFFF);
        graphics.rect(-this.tileSize/2 + 2, -this.tileSize/2 + 2, this.tileSize - 4, this.tileSize - 4);
        // Oreiller
        graphics.fill(0xDDDDFF);
        graphics.rect(-this.tileSize/3, -this.tileSize/2 + 5, this.tileSize*2/3, this.tileSize/4);
        break;
      case 'douche':
        graphics.fill(0xADD8E6); // Bleu clair pour la douche
        graphics.rect(-this.tileSize/2, -this.tileSize/2, this.tileSize, this.tileSize);
        // Pommeau
        graphics.fill(0xC0C0C0);
        graphics.circle(0, -this.tileSize/3, this.tileSize/6);
        break;
      default:
        // Objet générique
        graphics.fill(0x808080);
        graphics.rect(-this.tileSize/3, -this.tileSize/3, this.tileSize*2/3, this.tileSize*2/3);
    }
    
    this.sprite = new PIXI.Sprite(this.app.renderer.generateTexture(graphics));
    this.sprite.anchor.set(0.5);
    this.container.addChild(this.sprite);
    
    // Texte d'interaction (initialement caché)
    this.createInteractionText();
    
    // Positionner l'objet
    this.updatePosition();
  }
  
  createInteractionText() {
    // Créer le texte d'interaction
    const style = new PIXI.TextStyle({
      fontFamily: 'Arial',
      fontSize: 12,
      fill: 0xFFFFFF,
      stroke: 0x000000,
      align: 'center'
    });
    
    this.interactionText = new PIXI.Text({ text :'[E] Interagir', style: style });
    this.interactionText.anchor.set(0.5, 1);
    this.interactionText.y = -this.tileSize/2 - 5;
    this.interactionText.visible = false;
    
    this.container.addChild(this.interactionText);
  }
  
  updatePosition() {
    // Mettre à jour la position de l'objet
    this.sprite.x = (this.x + 0.5) * this.tileSize;
    this.sprite.y = (this.y + 0.5) * this.tileSize;
    
    // Centrer le container sur la position de la grille
    this.container.x = 0;
    this.container.y = 0;
  }
  
  showInteractionPrompt() {
    this.interactionText.visible = true;
  }
  
  hideInteractionPrompt() {
    this.interactionText.visible = false;
  }
  
  interact() {
    // Action spécifique à l'objet
    let message = "";
    
    switch(this.type) {
      case 'canapé':
        message = "Vous vous asseyez confortablement sur le canapé.";
        break;
      case 'télévision':
        if (this.state === 'idle') {
          this.state = 'active';
          message = "Vous allumez la télévision. Une émission est en cours.";
          // Changer la couleur de l'écran
          const blueScreen = new PIXI.Graphics()
            .rect(-this.tileSize/3 + 2, -this.tileSize/3 + 2, this.tileSize*2/3 - 4, this.tileSize*2/3 - 4)
            .fill(0x0000FF);
            this.sprite.texture = this.app.renderer.generateTexture(blueScreen);
          // On remplacerait seulement cette partie, mais pour simplifier, on génère une nouvelle texture
        } else {
          this.state = 'idle';
          message = "Vous éteignez la télévision.";
          // Réinitialiser la texture
          this.init();
        }
        break;
      case 'bibliothèque':
        message = "Vous parcourez les livres de la bibliothèque. Vous trouvez un livre intéressant sur PixiJS.";
        break;
      case 'réfrigérateur':
        message = "Vous ouvrez le réfrigérateur. Il contient quelques aliments et boissons.";
        break;
      case 'four':
        if (this.state === 'idle') {
          this.state = 'active';
          message = "Vous allumez le four. Il commence à chauffer.";
        } else {
          this.state = 'idle';
          message = "Vous éteignez le four.";
        }
        break;
      case 'lit':
        message = "Vous vous allongez sur le lit. C'est très confortable.";
        break;
      case 'douche':
        if (this.state === 'idle') {
          this.state = 'active';
          message = "Vous allumez la douche. L'eau commence à couler.";
        } else {
          this.state = 'idle';
          message = "Vous éteignez la douche.";
        }
        break;
      default:
        message = `Vous examinez l'objet.`;
    }
    
    return {
      type: this.type,
      message: message,
      state: this.state
    };
  }
  
  update() {
    // Mise à jour de l'objet (pour les animations, etc.)
    if (this.state === 'active') {
      // Exemple d'animation simple pour objets actifs
      this.sprite.alpha = 0.7 + Math.sin(Date.now() / 200) * 0.3;
    } else {
      this.sprite.alpha = 1.0;
    }
  }
  
  destroy() {
    // Nettoyage des ressources
    this.container.removeChildren();
    this.tileMap.container.removeChild(this.container);
  }
}