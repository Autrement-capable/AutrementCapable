// roomGame.js
import * as PIXI from 'pixi.js';

class RoomGame {
    constructor(container, config = {}) {
        this.container = container;
        this.app = null;
        this.character = null;
        this.bed = null;
        this.book = null;
        this.desk = null;
        this.wardrobe = null;
        this.background = null;
        this.eventCallback = null;
        this.isMoving = false;
        this.targetPos = null;
        this.speed = config.speed || 3;
        
        // Configuration des objets avec des valeurs par défaut
        this.objectsConfig = {
          background: {
            width: config.background?.width || null, // Par défaut ajusté à l'écran
            height: config.background?.height || null, // Par défaut ajusté à l'écran
            x: config.background?.x || 0,
            y: config.background?.y || 0
          },
          character: {
            width: config.character?.width || 60,
            height: config.character?.height || 60,
            x: config.character?.x || null, // Sera défini au centre par défaut
            y: config.character?.y || null  // Sera défini au centre par défaut
          },
          bed: {
            width: config.bed?.width || 240,
            height: config.bed?.height || 120,
            x: config.bed?.x || (1200 * 0.7),
            y: config.bed?.y || (600 * 0.6)
          },
          book: {
            width: config.book?.width || 60,
            height: config.book?.height || 80,
            x: config.book?.x || (1200 * 0.3),
            y: config.book?.y || (600 * 0.7)
          },
          desk: {
            width: config.desk?.width || 180,
            height: config.desk?.height || 90,
            x: config.desk?.x || (1200 * 0.2),
            y: config.desk?.y || (600 * 0.5)
          },
          wardrobe: {
            width: config.wardrobe?.width || 120,
            height: config.wardrobe?.height || 240,
            x: config.wardrobe?.x || (1200 * 0.8),
            y: config.wardrobe?.y || (600 * 0.3)
          }
        };
        
        // Stocker les valeurs numériques primitives pour éviter les problèmes de référence
        this._characterX = 0;
        this._characterY = 0;
        
        // Debug pour tracer d'où viennent les NaN
        this.debugMode = config.debugMode || false;
      }

      async init(callback) {
        try {
          console.log("Démarrage de l'initialisation");
          this.eventCallback = callback;
          
          // 1. Créer l'application PIXI basique
          const app = new PIXI.Application();
          await app.init({
            width: this.container.clientWidth || 800,
            height: this.container.clientHeight || 600,
            backgroundColor: "#f1f1f1",
            antialias: true
          });
          
          // 2. Ajouter le canvas au conteneur
          this.container.appendChild(app.canvas);
          this.app = app;
          
          console.log("Application PIXI initialisée avec dimensions:", app.screen.width, "x", app.screen.height);
          
          // 3. Activer le tri par z-index pour le stage
          app.stage.sortableChildren = true;
          
          // 4. Créer le fond d'abord (pour qu'il soit en arrière-plan)
          await this.createBackground();
          
          // 5. Créer les objets de la chambre
          await this.createRoomObjects();
          
          // 6. Créer le personnage
          await this.createCharacter();
          
          // 7. Notifier le redimensionnement
          if (this.eventCallback) {
            this.eventCallback('resize', {
              width: app.screen.width,
              height: app.screen.height
            });
          }
          
          // 8. Démarrer la boucle de jeu
          this._gameLoopBound = this.gameLoop.bind(this);
          app.ticker.add(this._gameLoopBound);
          
          console.log("Initialisation terminée avec succès");
          return true;
        } catch (error) {
          console.error("Erreur lors de l'initialisation:", error);
          this.destroy();
          return false;
        }
      }
    

  async createBackground() {
    try {
      console.log("Création du fond...");
      
      // Tenter de charger une image de fond
      const bgTexture = await PIXI.Assets.load('/assets/room-background.png');
      this.background = new PIXI.Sprite(bgTexture);
      
      // Déterminer les dimensions du fond en fonction de la configuration
      const bgWidth = this.objectsConfig.background.width || (this.app.screen.width + 100);
      const bgHeight = this.objectsConfig.background.height || (this.app.screen.height + 100);
      
      // Ajuster le fond selon la configuration
      this.background.width = bgWidth;
      this.background.height = bgHeight;
      this.background.x = this.objectsConfig.background.x;
      this.background.y = this.objectsConfig.background.y;
      
      // Placer le fond au niveau z le plus bas
      this.background.zIndex = -10;
      
      this.background.eventMode = 'static';
      this.background.on('pointerdown', this.onBackgroundClick.bind(this));
      this.app.stage.addChild(this.background);
      
      console.log("Fond créé avec dimensions:", 
                 this.background.width, "x", this.background.height,
                 "à la position", this.background.x, ",", this.background.y);
    } catch (error) {
      console.warn("Fallback: utilisation d'un fond uni:", error);
      // Fallback en cas d'échec: fond uni
      this.background = new PIXI.Sprite(PIXI.Texture.WHITE);
      
      // Même avec le fallback, utiliser la configuration
      const bgWidth = this.objectsConfig.background.width || this.app.screen.width;
      const bgHeight = this.objectsConfig.background.height || this.app.screen.height;
      
      this.background.width = bgWidth;
      this.background.height = bgHeight;
      this.background.x = this.objectsConfig.background.x;
      this.background.y = this.objectsConfig.background.y;
      this.background.tint = 0x87CEEB; // Bleu ciel
      
      // Placer le fond au niveau z le plus bas
      this.background.zIndex = -10;
      
      this.background.eventMode = 'static';
      this.background.on('pointerdown', this.onBackgroundClick.bind(this));
      this.app.stage.addChild(this.background);
      
      console.log("Fond fallback créé avec dimensions:", 
                 this.background.width, "x", this.background.height);
    }
  }
  
  // Méthode pour mettre à jour uniquement le background
  updateBackground(config) {
    if (!this.background || !this.app) {
      console.error("Impossible de mettre à jour le fond: objet non disponible");
      return false;
    }
    
    try {
      console.log("Mise à jour du fond avec la configuration:", config);
      
      // Mettre à jour les dimensions et position
      this.background.width = config.width || (this.app.screen.width + 100);
      this.background.height = config.height || (this.app.screen.height + 100);
      this.background.x = config.x || 0;
      this.background.y = config.y || 0;
      
      // Mettre à jour la référence dans la configuration
      this.objectsConfig.background = {...config};
      
      console.log("Background mis à jour avec dimensions:", 
                 this.background.width, "x", this.background.height,
                 "à la position", this.background.x, ",", this.background.y);
      
      return true;
    } catch (error) {
      console.error("Erreur lors de la mise à jour du fond:", error);
      return false;
    }
  }
  
  async createRoomObjects() {
    try {
      // Fonction utilitaire pour créer un objet avec une texture ou un fallback
      const createObject = async (type, config) => {
        let sprite;
        
        try {
          // Essayer de charger une texture depuis une URL
          const textureUrls = {
            'bed': '/assets/bed.png',
            'book': '/assets/book.png',
            'desk': '/assets/desk.png',
            'wardrobe': '/assets/wardrobe.png'
          };
          
          if (textureUrls[type]) {
            const texture = await PIXI.Assets.load(textureUrls[type]);
            sprite = new PIXI.Sprite(texture);
          } else {
            throw new Error("Type d'objet non reconnu");
          }
        } catch (error) {
          console.warn(`Fallback: utilisation d'un sprite de base pour ${type}:`, error);
          
          // Fallback: créer un sprite coloré simple
          sprite = new PIXI.Sprite(PIXI.Texture.WHITE);
          const colors = {
            'bed': 0x8B4513, // Marron
            'book': 0x0000FF, // Bleu
            'desk': 0x808080, // Gris
            'wardrobe': 0xF5DEB3 // Beige
          };
          sprite.tint = colors[type] || 0xFFFFFF;
        }
        
        // Configurer le sprite avec les dimensions et positions personnalisées
        sprite.width = config.width;
        sprite.height = config.height;
        sprite.x = config.x;
        sprite.y = config.y;
        sprite.eventMode = 'static';
        sprite.cursor = 'pointer';
        sprite.on('pointerdown', (e) => {
          e.stopPropagation();
          this.onObjectClick(type);
        });
        
        // Définir un z-index positif pour que les objets soient au-dessus du fond
        sprite.zIndex = 1;
        
        this.app.stage.addChild(sprite);
        console.log(`${type} créé à`, sprite.x, sprite.y, `avec dimensions`, sprite.width, 'x', sprite.height);
        
        return sprite;
      };
      
      // Créer chaque objet avec les configurations spécifiées
      this.bed = await createObject('bed', this.objectsConfig.bed);
      this.book = await createObject('book', this.objectsConfig.book);
      this.desk = await createObject('desk', this.objectsConfig.desk);
      this.wardrobe = await createObject('wardrobe', this.objectsConfig.wardrobe);
      
    } catch (error) {
      console.error("Erreur lors de la création des objets:", error);
      
      // Fallback si la méthode principale échoue
      console.log("Utilisation du fallback pour les objets");
      
      // Lit (rectangle marron)
      this.bed = new PIXI.Sprite(PIXI.Texture.WHITE);
      this.bed.width = this.objectsConfig.bed.width;
      this.bed.height = this.objectsConfig.bed.height;
      this.bed.tint = 0x8B4513; // Marron
      this.bed.x = this.objectsConfig.bed.x;
      this.bed.y = this.objectsConfig.bed.y;
      this.bed.eventMode = 'static';
      this.bed.cursor = 'pointer';
      this.bed.on('pointerdown', (e) => {
        e.stopPropagation();
        this.onObjectClick('bed');
      });
      this.app.stage.addChild(this.bed);
      
      // Livre (rectangle bleu)
      this.book = new PIXI.Sprite(PIXI.Texture.WHITE);
      this.book.width = this.objectsConfig.book.width;
      this.book.height = this.objectsConfig.book.height;
      this.book.tint = 0x0000FF; // Bleu
      this.book.x = this.objectsConfig.book.x;
      this.book.y = this.objectsConfig.book.y;
      this.book.eventMode = 'static';
      this.book.cursor = 'pointer';
      this.book.on('pointerdown', (e) => {
        e.stopPropagation();
        this.onObjectClick('book');
      });
      this.app.stage.addChild(this.book);
      
      // Bureau (rectangle gris)
      this.desk = new PIXI.Sprite(PIXI.Texture.WHITE);
      this.desk.width = this.objectsConfig.desk.width;
      this.desk.height = this.objectsConfig.desk.height;
      this.desk.tint = 0x808080; // Gris
      this.desk.x = this.objectsConfig.desk.x;
      this.desk.y = this.objectsConfig.desk.y;
      this.desk.eventMode = 'static';
      this.desk.cursor = 'pointer';
      this.desk.on('pointerdown', (e) => {
        e.stopPropagation();
        this.onObjectClick('desk');
      });
      this.app.stage.addChild(this.desk);
      
      // Armoire (rectangle beige)
      this.wardrobe = new PIXI.Sprite(PIXI.Texture.WHITE);
      this.wardrobe.width = this.objectsConfig.wardrobe.width;
      this.wardrobe.height = this.objectsConfig.wardrobe.height;
      this.wardrobe.tint = 0xF5DEB3; // Beige
      this.wardrobe.x = this.objectsConfig.wardrobe.x;
      this.wardrobe.y = this.objectsConfig.wardrobe.y;
      this.wardrobe.eventMode = 'static';
      this.wardrobe.cursor = 'pointer';
      this.wardrobe.on('pointerdown', (e) => {
        e.stopPropagation();
        this.onObjectClick('wardrobe');
      });
      this.app.stage.addChild(this.wardrobe);
    }
  }
  
  async createCharacter() {
    try {
      console.log("Chargement du sprite du personnage...");
      
      // Créer le personnage avec un sprite
      const texture = await PIXI.Assets.load('https://pixijs.com/assets/bunny.png');
      this.character = new PIXI.Sprite(texture);
      
      // Ajuster la taille du sprite selon la configuration
      this.character.width = this.objectsConfig.character.width;
      this.character.height = this.objectsConfig.character.height;
      
      // Centrer le point d'ancrage pour une rotation correcte
      this.character.anchor.set(0.5);
      
      // Initialiser les positions avec des valeurs de configuration ou par défaut
      this._characterX = this.objectsConfig.character.x !== null 
        ? this.objectsConfig.character.x 
        : this.app.screen.width / 2;
        
      this._characterY = this.objectsConfig.character.y !== null 
        ? this.objectsConfig.character.y 
        : this.app.screen.height / 2;
      
      // Définir la position initiale
      this.character.x = this._characterX;
      this.character.y = this._characterY;
      
      this.app.stage.addChild(this.character);
      
      console.log("Personnage créé à", this._characterX, this._characterY, 
                  "avec dimensions", this.character.width, "x", this.character.height);
      
      // Notifier la position initiale
      if (this.eventCallback) {
        this.eventCallback('characterMove', {
          x: this._characterX,
          y: this._characterY
        });
      }
    } catch (error) {
      // Code de fallback existant...
        console.error("Erreur lors de la création du personnage:", error);
    }
  }
  
  // Fonction utilitaire pour s'assurer qu'une valeur est un nombre
  ensureNumber(value, defaultValue = 0) {
    // Si c'est déjà un nombre valide, retourner tel quel
    if (typeof value === 'number' && !isNaN(value)) {
      return value;
    }
    
    // Tentative de conversion si c'est un objet PIXI avec valueOf ou toNumber
    try {
      if (value !== null && typeof value === 'object') {
        // Essayer d'obtenir la valeur numérique si possible
        if (typeof value.valueOf === 'function') {
          const converted = Number(value.valueOf());
          if (!isNaN(converted)) {
            return converted;
          }
        }
        
        // Essayer la propriété _value utilisée par certains objets PIXI
        if (value._value !== undefined && typeof value._value === 'number') {
          return value._value;
        }
      }
      
      // Tenter une conversion standard
      const converted = Number(value);
      if (!isNaN(converted)) {
        return converted;
      }
    } catch (error) {
      // Silencieux en mode non-debug
      if (this.debugMode) {
        console.warn(`Erreur lors de la conversion: ${error.message}`);
      }
    }
    
    // En dernier recours, utiliser la valeur par défaut
    if (this.debugMode) {
      console.warn(`Valeur non numérique détectée: ${value}, type: ${typeof value}`);
    }
    return defaultValue;
  }
  
  // Méthodes sécurisées pour obtenir/définir la position
  getCharacterX() {
    return this.ensureNumber(this._characterX, this.app ? this.app.screen.width / 2 : 0);
  }
  
  getCharacterY() {
    return this.ensureNumber(this._characterY, this.app ? this.app.screen.height / 2 : 0);
  }
  
  setCharacterX(value) {
    this._characterX = this.ensureNumber(value);
    if (this.character) {
      this.character.x = this._characterX;
    }
    return this._characterX;
  }
  
  setCharacterY(value) {
    this._characterY = this.ensureNumber(value);
    if (this.character) {
      this.character.y = this._characterY;
    }
    return this._characterY;
  }
  
  gameLoop(delta) {
    // Si on n'est pas en mouvement ou si des objets nécessaires n'existent pas
    if (!this.character || !this.app || !this.isMoving || !this.targetPos) return;
    
    try {
      // Récupérer les positions actuelles de manière sécurisée
      const currentX = this.getCharacterX();
      const currentY = this.getCharacterY();
      
      // Vérifier que les positions cibles sont des nombres valides
      const targetX = this.ensureNumber(this.targetPos.x, currentX);
      const targetY = this.ensureNumber(this.targetPos.y, currentY);
      
      // Calculer la direction et la distance
      const dx = targetX - currentX;
      const dy = targetY - currentY;
      const distance = Math.sqrt(dx*dx + dy*dy);
      
      // Debug occasionnel
      if (this.debugMode && Math.random() < 0.01) {
        console.log("Position actuelle:", {x: currentX, y: currentY});
        console.log("Position cible:", {x: targetX, y: targetY});
        console.log("Distance:", distance);
      }
      
      // Arrivé à destination?
      if (distance < 5) {
        this.isMoving = false;
        if (this.debugMode) {
          console.log("Arrivé à destination");
        }
        return;
      }
      
      // Calculer le mouvement avec une valeur de delta sécurisée
      const safeDelta = this.ensureNumber(delta, 1);
      const speedFactor = this.speed * safeDelta;
      
      if (distance > 0) {
        const dirX = dx / distance;
        const dirY = dy / distance;
        
        const moveX = dirX * speedFactor;
        const moveY = dirY * speedFactor;
        
        // Mettre à jour la position de manière sécurisée
        const newX = this.setCharacterX(currentX + moveX);
        const newY = this.setCharacterY(currentY + moveY);
        
        // Orienter le personnage sans affecter sa dimension
        // Sauvegarde de la largeur originale
        const originalWidth = this.character.width;
        
        if (dx < 0) {
          this.character.scale.x = -1; // Retourner horizontalement
        } else {
          this.character.scale.x = 1; // Normal
        }
        
        // Réappliquer la largeur originale
        this.character.width = originalWidth;
        
        // Notifier le mouvement
        if (this.eventCallback) {
          this.eventCallback('characterMove', {
            x: newX,
            y: newY
          });
        }
      }
    } catch (error) {
      console.error("Erreur dans la boucle de jeu:", error);
      this.isMoving = false;
      
      // Réinitialiser le personnage au centre en cas d'erreur
      if (this.app && this.character) {
        const centerX = this.app.screen.width / 2;
        const centerY = this.app.screen.height / 2;
        this.setCharacterX(centerX);
        this.setCharacterY(centerY);
        
        if (this.eventCallback) {
          this.eventCallback('characterMove', {
            x: centerX,
            y: centerY
          });
        }
      }
    }
  }
    
  onBackgroundClick(event) {
    if (!this.character || !this.app) return;
    
    // Extraire les valeurs de position du clic de manière sécurisée
    let x, y;
    
    try {
      // Tenter d'accéder aux coordonnées en fonction de la structure
      if (event && event.global) {
        if (typeof event.global.x === 'number') {
          x = event.global.x;
        } else if (event.global.x !== undefined) {
          x = parseFloat(event.global.x);
        }
        
        if (typeof event.global.y === 'number') {
          y = event.global.y;
        } else if (event.global.y !== undefined) {
          y = parseFloat(event.global.y);
        }
      }
    } catch (error) {
      console.error("Erreur lors de l'extraction des coordonnées:", error);
    }
    
    // Vérifier et définir avec des valeurs par défaut si nécessaire
    x = this.ensureNumber(x, this.app.screen.width / 2);
    y = this.ensureNumber(y, this.app.screen.height / 2);
    
    console.log("Clic sur le fond:", {x, y});
    
    // Stocker comme valeurs numériques simples
    this.targetPos = { x, y };
    
    this.isMoving = true;
  }
  
  onObjectClick(objectType) {
    if (!this.character || !this.app) return;
    
    let obj;
    
    switch (objectType) {
      case 'bed':
        obj = this.bed;
        break;
      case 'book':
        obj = this.book;
        break;
      case 'desk':
        obj = this.desk;
        break;
      case 'wardrobe':
        obj = this.wardrobe;
        break;
    }
    
    if (!obj) return;
    
    // Calculer la position cible de manière sécurisée
    let x, y;
    
    try {
      x = this.ensureNumber(obj.x, 0) + this.ensureNumber(obj.width, 0) / 2;
      y = this.ensureNumber(obj.y, 0) + this.ensureNumber(obj.height, 0) + 30;
    } catch (error) {
      console.error(`Erreur lors du calcul de la position pour ${objectType}:`, error);
      x = this.app.screen.width / 2;
      y = this.app.screen.height / 2;
    }
    
    console.log(`Clic sur l'objet ${objectType}:`, {x, y});
    
    // Stocker comme valeurs numériques primitives sécurisées
    this.targetPos = { 
      x: this.ensureNumber(x), 
      y: this.ensureNumber(y) 
    };
    
    this.isMoving = true;
    
    // Déclencher l'interaction après un délai
    setTimeout(() => {
      if (!this.character || !this.app) return;
      
      console.log(`Interaction avec ${objectType}`);
      
      if (this.eventCallback) {
        this.eventCallback('interaction', {
          type: objectType,
          action: this.getActionForObject(objectType)
        });
      }
    }, 1000);
  }
  
  getActionForObject(objectType) {
    const actions = {
      'bed': 'sleep',
      'book': 'read',
      'desk': 'work',
      'wardrobe': 'change'
    };
    
    return actions[objectType] || 'interact';
  }
  
  destroy() {
    console.log("Destruction du jeu");
    
    // Supprimer la boucle de jeu
    if (this.app && this.app.ticker && this._gameLoopBound) {
      this.app.ticker.remove(this._gameLoopBound);
      this._gameLoopBound = null;
    }
    
    // Supprimer directement tous les enfants du stage
    if (this.app && this.app.stage) {
      this.app.stage.removeChildren();
    }
    
    // Nullifier les références individuelles
    this.character = null;
    this.wardrobe = null;
    this.desk = null;
    this.book = null;
    this.bed = null;
    this.background = null;
    
    // Détruire l'application complètement
    if (this.app) {
      try {
        this.app.destroy(true, {children: true, texture: true, baseTexture: true});
      } catch (error) {
        console.warn("Erreur lors de la destruction de l'application:", error);
      }
      this.app = null;
    }
    
    // Vider le conteneur
    if (this.container) {
      while (this.container.firstChild) {
        this.container.removeChild(this.container.firstChild);
      }
    }
    
    this.isMoving = false;
    this.targetPos = null;
    this._characterX = 0;
    this._characterY = 0;
    
    console.log("Jeu détruit");
  }
}

export default RoomGame;