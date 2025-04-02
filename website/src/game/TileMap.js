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
    this.objectPositions = []; // Stock les positions des objets interactifs
  }

  // Charger les textures des tiles
  async loadTileTextures() {
    const tileTypes = ['floor', 'wall', 'door', 'object_spot'];
    
    // Créer un loader pour charger les textures externes
    const loader = PIXI.Assets;
    
    // URL pour la texture de mur - remplacez par l'URL de votre texture
    // Note: Si vous utilisez une texture locale, veillez à ce qu'elle soit dans votre dossier d'assets
    
    try {
      // Essayer de charger la texture du mur à partir d'une URL
      const wallTexture = await loader.load('/assets/WallTexture.png');
      
      // Initialiser l'objet des textures
      for (const type of tileTypes) {
        if (type === 'wall') {
          // Utiliser la texture réelle pour le mur
          this.tileTextures[type] = this.prepareWallTexture(wallTexture);
        } else {
          // Pour les autres types, utiliser les graphiques générés comme avant
          const color = this.getTileColor(type);
          const graphics = new PIXI.Graphics();
          
          if (type === 'door') {
            // Texture de porte
            graphics.fill(0x8B4513); // Brun foncé pour le cadre
            graphics.rect(0, 0, this.tileSize, this.tileSize);
            graphics.fill();
            
            // Intérieur de la porte
            graphics.fill(0xCD853F); // Brun plus clair
            graphics.rect(this.tileSize/8, this.tileSize/8, 
                            this.tileSize*3/4, this.tileSize*3/4);
            graphics.fill();
          } else if (type === 'object_spot') {
            // Marqueur pour les emplacements d'objets
            graphics.fill({color: 0x000000, alpha: 0.3}); // Semi-transparent
            graphics.rect(0, 0, this.tileSize, this.tileSize);
            graphics.fill();
            
            // Point central pour indiquer un emplacement d'objet
            graphics.fill({color: 0xFF0000, alpha: 0.5});
            graphics.circle(this.tileSize/2, this.tileSize/2, this.tileSize/8);
            graphics.fill();
          } else {
            // Texture simple pour le sol
            graphics.fill(color);
            graphics.rect(0, 0, this.tileSize, this.tileSize);
            graphics.fill();
            
            // Ajouter quelques détails au sol
            graphics.setStrokeStyle({width: 1, color: 0x000000, alpha: 0.1});
            graphics.moveTo(0, 0);
            graphics.lineTo(this.tileSize, this.tileSize);
            graphics.moveTo(this.tileSize, 0);
            graphics.lineTo(0, this.tileSize);
          }
          
          this.tileTextures[type] = this.app.renderer.generateTexture(graphics);
        }
      }
      
      return true;
    } catch (error) {
      console.error('Erreur lors du chargement de la texture:', error);
      
      // En cas d'erreur, revenir à la génération par défaut pour tous les types
      for (const type of tileTypes) {
        const color = this.getTileColor(type);
        const graphics = new PIXI.Graphics();
        
        // Même code que la version originale pour les textures générées
        if (type === 'wall') {
          // Texture de mur de secours
          graphics.fill(0x8B4513); // Brun pour les murs
          graphics.rect(0, 0, this.tileSize, this.tileSize);
          graphics.fill();
          
          // Dessiner des lignes pour simuler des briques
          graphics.setStrokeStyle({width: 1, color: 0x000000, alpha: 0.3});
          for (let y = 0; y < this.tileSize; y += this.tileSize/4) {
            graphics.moveTo(0, y);
            graphics.lineTo(this.tileSize, y);
          }
          for (let x = 0; x < this.tileSize; x += this.tileSize/4) {
            graphics.moveTo(x, 0);
            graphics.lineTo(x, this.tileSize);
          }
        } else if (type === 'door') {
          // Texture de porte
          graphics.fill(0x8B4513); // Brun foncé pour le cadre
          graphics.rect(0, 0, this.tileSize, this.tileSize);
          graphics.fill();
          
          // Intérieur de la porte
          graphics.fill(0xCD853F); // Brun plus clair
          graphics.rect(this.tileSize/8, this.tileSize/8, 
                          this.tileSize*3/4, this.tileSize*3/4);
          graphics.fill();
        } else if (type === 'object_spot') {
          // Marqueur pour les emplacements d'objets
          graphics.fill({color: 0x000000, alpha: 0.3}); // Semi-transparent
          graphics.rect(0, 0, this.tileSize, this.tileSize);
          graphics.fill();
          
          // Point central pour indiquer un emplacement d'objet
          graphics.fill({color: 0xFF0000, alpha: 0.5});
          graphics.circle(this.tileSize/2, this.tileSize/2, this.tileSize/8);
          graphics.fill();
        } else {
          // Texture simple pour le sol
          graphics.fill(color);
          graphics.rect(0, 0, this.tileSize, this.tileSize);
          graphics.fill();
          
          // Ajouter quelques détails au sol
          graphics.setStrokeStyle({width: 1, color: 0x000000, alpha: 0.1});
          graphics.moveTo(0, 0);
          graphics.lineTo(this.tileSize, this.tileSize);
          graphics.moveTo(this.tileSize, 0);
          graphics.lineTo(0, this.tileSize);
        }
        
        this.tileTextures[type] = this.app.renderer.generateTexture(graphics);
      }
      
      return true;
    }
  }
  
  // Préparer la texture du mur pour l'adapter à la taille des tiles
  prepareWallTexture(texture) {
    // Créer un sprite temporaire avec la texture
    const tempSprite = new PIXI.Sprite(texture);
    
    // Redimensionner le sprite à la taille d'une tile
    tempSprite.width = this.tileSize;
    tempSprite.height = this.tileSize;
    
    // Générer une nouvelle texture à partir de ce sprite
    return this.app.renderer.generateTexture(tempSprite);
  }
  
  // Obtenir une couleur pour chaque type de tile
  getTileColor(type) {
    switch(type) {
      case 'floor': return 0xDEB887; // beige pour le sol
      case 'wall': return 0x8B4513;  // brun pour les murs
      case 'door': return 0xCD853F;  // brun clair pour les portes
      case 'object_spot': return 0x32CD32; // vert pour les objets
      default: return 0xFFFFFF;      // blanc par défaut
    }
  }

  // Générer une maison avec des pièces et des emplacements d'objets
  generateMap(width, height) {
    this.mapWidth = width;
    this.mapHeight = height;
    this.map = [];

    // Initialiser toute la carte avec du sol
    for (let y = 0; y < height; y++) {
      const row = [];
      for (let x = 0; x < width; x++) {
        row.push('floor');
      }
      this.map.push(row);
    }

    // Ajouter les murs extérieurs
    for (let x = 0; x < width; x++) {
      this.map[0][x] = 'wall'; // Mur du haut
      this.map[height-1][x] = 'wall'; // Mur du bas
    }
    
    for (let y = 0; y < height; y++) {
      this.map[y][0] = 'wall'; // Mur de gauche
      this.map[y][width-1] = 'wall'; // Mur de droite
    }

    // Définir les pièces de la maison
    const rooms = [
      { name: "salon", x: 1, y: 1, width: Math.floor(width/2) - 1, height: Math.floor(height/2) - 1 },
      { name: "cuisine", x: Math.floor(width/2) + 1, y: 1, width: Math.floor(width/2) - 2, height: Math.floor(height/2) - 1 },
      { name: "chambre", x: 1, y: Math.floor(height/2) + 1, width: Math.floor(width/2) - 1, height: Math.floor(height/2) - 2 },
      { name: "salle de bain", x: Math.floor(width/2) + 1, y: Math.floor(height/2) + 1, width: Math.floor(width/2) - 2, height: Math.floor(height/2) - 2 }
    ];

    // Ajouter les murs intérieurs
    // Mur horizontal central
    for (let x = 1; x < width - 1; x++) {
      if (x !== Math.floor(width/4) && x !== Math.floor(width*3/4)) { // Laisser des passages pour les portes
        this.map[Math.floor(height/2)][x] = 'wall';
      } else {
        this.map[Math.floor(height/2)][x] = 'door';
      }
    }
    
    // Mur vertical central
    for (let y = 1; y < height - 1; y++) {
      if (y !== Math.floor(height/4) && y !== Math.floor(height*3/4)) { // Laisser des passages pour les portes
        this.map[y][Math.floor(width/2)] = 'wall';
      } else {
        this.map[y][Math.floor(width/2)] = 'door';
      }
    }
    
    // Porte d'entrée en bas
    this.map[height-1][Math.floor(width/2)] = 'door';

    // Placer des objets interactifs dans chaque pièce
    this.objectPositions = [];
    
    for (const room of rooms) {
      // Nombre d'objets à placer dans la pièce
      const objectCount = room.name === "salon" ? 3 : 
                          room.name === "cuisine" ? 2 : 1;
      
      for (let i = 0; i < objectCount; i++) {
        let objectX, objectY;
        let attempts = 0;
        let validPosition = false;
        
        // Essayer de trouver une position valide pour l'objet
        while (!validPosition && attempts < 10) {
          objectX = room.x + 1 + Math.floor(Math.random() * (room.width - 2));
          objectY = room.y + 1 + Math.floor(Math.random() * (room.height - 2));
          
          // Vérifier si la position est libre (pas de mur, porte ou autre objet)
          validPosition = this.map[objectY][objectX] === 'floor';
          
          attempts++;
        }
        
        if (validPosition) {
          this.map[objectY][objectX] = 'object_spot';
          
          // Stocker la position et le type d'objet
          let objectType;
          if (room.name === "salon") {
            objectType = ["canapé", "télévision", "bibliothèque"][i];
          } else if (room.name === "cuisine") {
            objectType = ["réfrigérateur", "four"][i];
          } else if (room.name === "chambre") {
            objectType = "lit";
          } else if (room.name === "salle de bain") {
            objectType = "douche";
          }
          
          this.objectPositions.push({
            x: objectX,
            y: objectY,
            type: objectType,
            roomName: room.name
          });
        }
      }
    }

    this.renderMap();
    
    // Centrer la vue sur la maison entière plutôt que sur le joueur
    this.centerMapOnScreen();
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
    
    // Vérifier si la tile est traversable (les murs ne sont pas traversables)
    return this.map[y][x] !== 'wall';
  }

  // Vérifier s'il y a un objet à une position donnée
  getObjectAtPosition(x, y) {
    return this.objectPositions.find(obj => obj.x === x && obj.y === y);
  }

  // Centrer la vue sur la maison entière
  centerMapOnScreen() {
    const centerX = this.app.screen.width / 2;
    const centerY = this.app.screen.height / 2;
    
    // Calculer le centre de la carte en pixels
    const mapCenterX = (this.mapWidth * this.tileSize) / 2;
    const mapCenterY = (this.mapHeight * this.tileSize) / 2;
    
    // Positionner la carte pour qu'elle soit centrée à l'écran
    this.container.x = centerX - mapCenterX;
    this.container.y = centerY - mapCenterY;
    
    // Ajuster le zoom si nécessaire pour que toute la maison soit visible
    this.adjustZoom();
  }
  
  // Ajuster le zoom pour que toute la maison soit visible
  adjustZoom() {
    const screenWidth = this.app.screen.width;
    const screenHeight = this.app.screen.height;
    const mapWidth = this.mapWidth * this.tileSize;
    const mapHeight = this.mapHeight * this.tileSize;
    
    // Calculer les ratios pour s'assurer que la carte s'adapte à l'écran
    const scaleX = screenWidth / mapWidth;
    const scaleY = screenHeight / mapHeight;
    
    // Utiliser le plus petit ratio pour s'assurer que toute la carte est visible
    const scale = Math.min(scaleX, scaleY) * 0.6; // 0.6 pour laisser une petite marge
    
    // Appliquer le zoom
    this.container.scale.set(scale);
    
    // Réajuster la position après le zoom
    const centerX = this.app.screen.width / 2;
    const centerY = this.app.screen.height / 2;
    const mapCenterX = (this.mapWidth * this.tileSize * scale) / 2;
    const mapCenterY = (this.mapHeight * this.tileSize * scale) / 2;
    
    this.container.x = centerX - mapCenterX;
    this.container.y = centerY - mapCenterY;
  }
}