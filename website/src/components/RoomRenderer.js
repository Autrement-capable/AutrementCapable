/**
 * RoomRenderer - A class to handle all Three.js operations for room visualization
 * This is completely isolated from Vue to prevent reactivity issues
 */
export default class RoomRenderer {
    constructor(containerElement) {
      this.container = containerElement;
      this.scene = null;
      this.camera = null;
      this.renderer = null;
      this.controls = null;
      this.roomMeshes = {};
      this.furnitureMeshes = [];
      this.directionalLight = null;
      this.light = null;
      this.light2 = null;
      this.ambientLight = null;
      this.peopleMeshes = [];
      this.models3D = {};
      this.loaders = {};
      this.modelMeshes = [];

      this.objectCategories = {
        minimal: ['desk', 'chair', 'lightbulb'],
        moderate: ['desk', 'chair', 'bookshelf', 'plant', 'lightbulb'],
        detailed: ['desk', 'chair', 'bookshelf', 'plant', 'lamp', 'computer', 'lightbulb'],
        bedroom: ['bed', 'nightstand', 'wardrobe', 'lamp', 'lightbulb'],
        livingroom: ['sofa', 'coffeetable', 'tv', 'plant', 'rug', 'lightbulb'],
        office: ['desk', 'chair', 'bookshelf', 'computer', 'lamp', 'filing', 'lightbulb']
      };
      
      this.categoryConfigurations = {
        minimal: {
          desk: { position: [5, 0, 1], scale: 0.2, rotation: [0, 0, 0] },
          chair: { position: [4.6, 0, 2], scale: 0.015, rotation: [0, Math.PI, 0] },
          lightbulb: { position: [0.33, 1.4, 5.55], scale: 0.03, rotation: [0, Math.PI, 0] }
        },
        moderate: {
          desk: { position: [5, 0, 1], scale: 0.2, rotation: [0, 0, 0] },
          chair: { position: [4.6, 0, 2], scale: 0.015, rotation: [0, Math.PI, 0] },
          bookshelf: { position: [2.5, 0, 2], scale: 0.7, rotation: [0, Math.PI/2, 0] },
          plant: { position: [8, 0, 2], scale: 0.5, rotation: [0, 0, 0] },
          lightbulb: { position: [0.33, 1.4, 5.55], scale: 0.03, rotation: [0, Math.PI, 0] }
        },
        detailed: {
          desk: { position: [5, 0, 3], scale: 0.8, rotation: [0, 0, 0] },
          chair: { position: [5, 0, 4.2], scale: 0.7, rotation: [0, Math.PI, 0] },
          bookshelf: { position: [2.5, 0, 2], scale: 0.7, rotation: [0, Math.PI/2, 0] },
          plant: { position: [8, 0, 2], scale: 0.5, rotation: [0, 0, 0] },
          lamp: { position: [5.8, 0, 2.8], scale: 0.4, rotation: [0, Math.PI/4, 0] },
          computer: { position: [5, 0, 2.7], scale: 0.3, rotation: [0, 0, 0] },
          lightbulb: { position: [0.33, 1.4, 5.55], scale: 0.03, rotation: [0, Math.PI, 0] }
        },
        bedroom: {
          bed: { position: [5, 0, 5], scale: 0.9, rotation: [0, Math.PI/2, 0] },
          nightstand: { position: [6.5, 0, 3.5], scale: 0.7, rotation: [0, 0, 0] },
          wardrobe: { position: [2, 0, 2], scale: 0.8, rotation: [0, 0, 0] },
          lamp: { position: [6.5, 0, 3], scale: 0.4, rotation: [0, 0, 0] },
          lightbulb: { position: [0.33, 1.4, 5.55], scale: 0.03, rotation: [0, Math.PI, 0] }
        },
        livingroom: {
          sofa: { position: [5, 0, 7], scale: 0.012, rotation: [0, -Math.PI/2, 0] },
          coffeetable: { position: [5, 0, 5], scale: 0.7, rotation: [0, 0, 0] },
          tv: { position: [5, 0, 2], scale: 0.8, rotation: [0, Math.PI/2, 0] },
          plant: { position: [8, 0, 7], scale: 0.5, rotation: [0, 0, 0] },
          rug: { position: [5, 0, 5], scale: 1.2, rotation: [0, 0, 0] },
          lightbulb: { position: [0.33, 1.4, 5.55], scale: 0.03, rotation: [0, Math.PI, 0] }
        },
        office: {
          desk: { position: [5, 0, 3], scale: 0.8, rotation: [0, 0, 0] },
          chair: { position: [5, 0, 4.2], scale: 0.7, rotation: [0, Math.PI, 0] },
          bookshelf: { position: [2, 0, 2], scale: 0.7, rotation: [0, Math.PI/2, 0] },
          computer: { position: [5, 0, 2.7], scale: 0.3, rotation: [0, 0, 0] },
          lamp: { position: [5.8, 0, 2.8], scale: 0.4, rotation: [0, Math.PI/4, 0] },
          filing: { position: [8, 0, 2], scale: 0.7, rotation: [0, -Math.PI/4, 0] },
          lightbulb: { position: [0.33, 1.4, 5.55], scale: 0.03, rotation: [0, Math.PI, 0] }
        }
      };
      
      this.room = {
        width: 10,
        depth: 10, 
        height: 3,
        wallColor: '#e0e0e0',
        floorColor: '#ad8a64',
        ceilingColor: '#f5f5f5'
      };
      
      this.lighting = {
        color: '#ffffff',
        intensity: 1.5,
        ambient: true
      };
      
      this.furniture = [];
      
      // Animation frame reference
      this.animationFrameId = null;
      
      // Load Three.js dynamically
      this.loadDependencies();
    }
    
    async loadDependencies() {
      try {
        const THREE = await import('three');
        const { OrbitControls } = await import('three/examples/jsm/controls/OrbitControls.js');
        const { GLTFLoader } = await import('three/examples/jsm/loaders/GLTFLoader.js');
        
        // Store modules
        this.THREE = THREE;
        this.OrbitControls = OrbitControls;

        this.loaders.gltf = new GLTFLoader();        
        
        // Initialize scene
        this.initScene();
        this.createRoom();
        this.startAnimation();
        
        // Add window resize handler
        window.addEventListener('resize', this.handleResize.bind(this));
      } catch (error) {
        console.error("Failed to load Three.js:", error);
      }
    }
    
    initScene() {
      const { THREE, OrbitControls } = this;
      
      // Create scene
      this.scene = new THREE.Scene();
      this.scene.background = new THREE.Color('#1a1a1a');
      // Create camera
      this.camera = new THREE.PerspectiveCamera(
        75,
        this.container.clientWidth / this.container.clientHeight,
        0.1,
        1000
      );
      
      const { width, height, depth } = this.room;
      this.camera.position.set(width, height/2 + 3, depth * 1.5);
      this.camera.lookAt(width/2, height/2, depth/2);
      
      // Create renderer
      this.renderer = new THREE.WebGLRenderer({ antialias: true });
      this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
      this.renderer.shadowMap.enabled = true;
      
      // Clear any existing canvas
      while (this.container.firstChild) {
        this.container.removeChild(this.container.firstChild);
      }
      
      this.container.appendChild(this.renderer.domElement);
      
      // Add controls
      this.controls = new OrbitControls(this.camera, this.renderer.domElement);
      this.controls.enableDamping = true;
      this.controls.dampingFactor = 0.05;
      
      // Add lighting
      this.setupLighting();
    }
    
    setupLighting() {
      const { THREE } = this;
      const { height, depth  } = this.room;
      const { color, intensity, ambient } = this.lighting;

      this.light = new THREE.PointLight(0xffffff, 1, 500, 0.2);
      this.light.position.set(0.28, height/2, depth/2);
      this.scene.add(this.light);
      
      // Ambient light
      this.ambientLight = new THREE.AmbientLight(color, intensity * 0.5);
      if (ambient) {
        this.scene.add(this.ambientLight);
      }
    }
    
    updateLighting(color, intensity, ambient) {
      // Update stored values
      this.lighting.color = color;
      this.lighting.intensity = intensity;
      this.lighting.ambient = ambient;
      
      // Update lights

      if (this.light) {
        this.light.color.set(color);
        this.light.intensity = intensity;
      }

      if (this.ambientLight) {
        this.ambientLight.color.set(color);
        
        // Add or remove based on ambient setting
        if (ambient && !this.scene.children.includes(this.ambientLight)) {
          this.scene.add(this.ambientLight);
        } else if (!ambient && this.scene.children.includes(this.ambientLight)) {
          this.scene.remove(this.ambientLight);
        }
      }
    }

    loadModel(modelName, position = [0, 0, 0], scale = 1, rotation = [0, 0, 0]) {
      // Définir le chemin du modèle basé sur son nom
      const modelPath = this.getModelPath(modelName);
      
      return new Promise((resolve, reject) => {
        // Vérifier si le loader est disponible
        if (!this.loaders.gltf) {
          reject("GLTFLoader n'est pas initialisé");
          return;
        }
        
        this.loaders.gltf.load(
          modelPath,
          (gltf) => {
            const model = gltf.scene;
            
            // Appliquer l'échelle
            model.scale.set(scale, scale, scale);
            
            // Appliquer la position
            model.position.set(position[0], position[1], position[2]);
            
            // Appliquer la rotation (en radians)
            model.rotation.set(rotation[0], rotation[1], rotation[2]);
            
            // Ajouter des ombres pour tous les objets du modèle
            model.traverse((node) => {
              if (node.isMesh) {
                node.castShadow = true;
                node.receiveShadow = true;
              }
            });
            
            // Ajouter à la scène
            this.scene.add(model);
            
            // Stocker dans modelMeshes pour pouvoir le supprimer plus tard
            this.modelMeshes.push(model);
            
            // Stocker la référence du modèle
            this.models3D[modelName] = model;
            
            resolve(model);
          },
          // Fonction de progression (optionnelle)
          (xhr) => {
            const percentage = (xhr.loaded / xhr.total) * 100;
            console.log(`${modelName} : ${Math.round(percentage)}% chargé`);
          },
          // Fonction d'erreur
          (error) => {
            console.error(`Erreur lors du chargement du modèle ${modelName}:`, error);
            reject(error);
          }
        );
      });
    }

    getModelPath(modelName) {
      
      // Mapping des noms de modèles vers leurs fichiers
      const modelPaths = {
        // Mobilier de base
        desk: '/desk/scene.gltf',
        chair: '/chair/scene.gltf',
        bookshelf: 'furniture/bookshelf.glb',
        sofa: '/couch/scene.gltf',
        lightbulb: '/light_bulb/scene.gltf',
        
        // Objets supplémentaires
        plant: 'decor/plant.glb',
        lamp: 'decor/desk_lamp.glb',
        computer: 'tech/computer.glb',
        tv: 'tech/tv.glb',
        
        // Mobilier de chambre
        bed: 'furniture/bed.glb',
        nightstand: 'furniture/nightstand.glb',
        wardrobe: 'furniture/wardrobe.glb',
        
        // Mobilier de salon
        coffeetable: 'furniture/coffee_table.glb',
        rug: 'decor/rug.glb',
        
        // Objets de bureau
        filing: 'furniture/filing_cabinet.glb'
      };
      
      // Si le modèle n'est pas dans notre mapping, utiliser un modèle par défaut
      const modelFile = modelPaths[modelName] || 'furniture/default_box.glb';
      
      return modelFile;
    }

    loadObjectsByCategory(category) {
      // D'abord, supprimer tous les modèles existants
      this.clearModels();
      
      // Obtenir la liste des objets pour cette catégorie
      const objects = this.objectCategories[category] || this.objectCategories.minimal;

      const categoryConfig = this.categoryConfigurations[category] || {};
      
      // Charger chaque objet avec sa position prédéfinie
      const loadPromises = objects.map((objectName) => {
        // Utiliser la configuration prédéfinie si disponible, sinon utiliser des valeurs par défaut
        const config = categoryConfig[objectName] || {
          position: [this.room.width/2, 0, this.room.depth/2],
          scale: 0.7,
          rotation: [0, 0, 0]
        };
        
        // Ajuster la position en fonction de la taille de la pièce si nécessaire
        const position = this.adjustPositionToRoomSize(config.position);
        
        // Charger le modèle avec les paramètres définis
        return this.loadModel(objectName, position, config.scale, config.rotation);
      });
      
      return Promise.all(loadPromises);
    }

    adjustPositionToRoomSize(position) {
      // Si la pièce a une taille différente de la taille standard (10x10),
      // on peut ajuster proportionnellement les positions
      const widthRatio = this.room.width / 10;
      const depthRatio = this.room.depth / 10;
      
      return [
        position[0] * widthRatio,
        position[1], // la hauteur (Y) reste inchangée
        position[2] * depthRatio
      ];
    }

    clearModels() {
      // Supprimer tous les modèles de la scène
      this.modelMeshes.forEach(model => {
        this.scene.remove(model);
        
        // Libérer les ressources (important pour éviter les fuites de mémoire)
        if (model) {
          model.traverse((node) => {
            if (node.isMesh) {
              if (node.geometry) node.geometry.dispose();
              
              if (node.material) {
                if (Array.isArray(node.material)) {
                  node.material.forEach(material => material.dispose());
                } else {
                  node.material.dispose();
                }
              }
            }
          });
        }
      });
      
      // Vider le tableau de suivi
      this.modelMeshes = [];
      
      // Réinitialiser le dictionnaire des modèles
      this.models3D = {};
    }

    clearRoomObjects() {
      // Supprimer les meubles
      this.clearFurniture();
      
      // Supprimer les modèles 3D
      this.clearModels();
    }
    
    createRoom() {
      const { THREE } = this;
      const { width, depth, height, wallColor, floorColor, ceilingColor } = this.room;
      
      // Create materials
      const wallMaterial = new THREE.MeshStandardMaterial({ color: wallColor });
      const floorMaterial = new THREE.MeshStandardMaterial({ color: floorColor });
      const ceilingMaterial = new THREE.MeshStandardMaterial({ color: ceilingColor });
      
      // Floor
      const floorGeometry = new THREE.PlaneGeometry(width, depth);
      const floor = new THREE.Mesh(floorGeometry, floorMaterial);
      floor.rotation.x = -Math.PI / 2;
      floor.position.set(width/2, 0, depth/2);
      floor.receiveShadow = true;
      this.roomMeshes.floor = floor;
      this.scene.add(floor);
      
      // Ceiling
      const ceilingGeometry = new THREE.PlaneGeometry(width, depth);
      const ceiling = new THREE.Mesh(ceilingGeometry, ceilingMaterial);
      ceiling.rotation.x = Math.PI / 2;
      ceiling.position.set(width/2, height, depth/2);
      ceiling.receiveShadow = true;
      this.roomMeshes.ceiling = ceiling;
      this.scene.add(ceiling);
      
      // Back wall
      const backWallGeometry = new THREE.PlaneGeometry(width, height);
      const backWall = new THREE.Mesh(backWallGeometry, wallMaterial);
      backWall.position.set(width/2, height/2, 0);
      backWall.receiveShadow = true;
      this.roomMeshes.backWall = backWall;
      this.scene.add(backWall);
      
      // Left wall
      const leftWallGeometry = new THREE.PlaneGeometry(depth, height);
      const leftWall = new THREE.Mesh(leftWallGeometry, wallMaterial);
      leftWall.rotation.y = Math.PI / 2;
      leftWall.position.set(0, height/2, depth/2);
      leftWall.receiveShadow = true;
      this.roomMeshes.leftWall = leftWall;
      this.scene.add(leftWall);
      
      // Right wall
      const rightWallGeometry = new THREE.PlaneGeometry(depth, height);
      const rightWall = new THREE.Mesh(rightWallGeometry, wallMaterial);
      rightWall.rotation.y = -Math.PI / 2;
      rightWall.position.set(width, height/2, depth/2);
      rightWall.receiveShadow = true;
      this.roomMeshes.rightWall = rightWall;
      this.scene.add(rightWall);
    }
    
    updateRoom(width, depth, height, wallColor, floorColor, ceilingColor) {
      // Store new dimensions
      this.room.width = width;
      this.room.depth = depth;
      this.room.height = height;
      this.room.wallColor = wallColor;
      this.room.floorColor = floorColor;
      this.room.ceilingColor = ceilingColor;
      
      // Remove existing room components
      Object.values(this.roomMeshes).forEach(mesh => {
        if (mesh) this.scene.remove(mesh);
      });
      
      // Create new room
      this.createRoom();
      
      // Update camera and lights
      this.camera.position.set(width, height/2 + 3, depth * 1.5);
      this.camera.lookAt(width/2, height/2, depth/2);
            
      // Update furniture positions
      this.updateFurniturePositions();
    }
    
    updateRoomColors(wallColor, floorColor, ceilingColor) {
      // Update stored colors
      this.room.wallColor = wallColor;
      this.room.floorColor = floorColor;
      this.room.ceilingColor = ceilingColor;
      
      // Update materials
      if (this.roomMeshes.floor) {
        this.roomMeshes.floor.material.color.set(floorColor);
      }
      
      if (this.roomMeshes.ceiling) {
        this.roomMeshes.ceiling.material.color.set(ceilingColor);
      }
      
      if (this.roomMeshes.backWall) {
        this.roomMeshes.backWall.material.color.set(wallColor);
      }
      
      if (this.roomMeshes.leftWall) {
        this.roomMeshes.leftWall.material.color.set(wallColor);
      }
      
      if (this.roomMeshes.rightWall) {
        this.roomMeshes.rightWall.material.color.set(wallColor);
      }
    }
    
    addFurniture(type, fixedX = false, fixedZ = false, customPosition = null) {
      const { THREE } = this;
      if (!THREE) return null;
      
      const { width, depth } = this.room;
      let position, size, color;
      
      // Set properties based on furniture type
      switch(type) {
        case 'desk':
          position = customPosition || [width * 0.6, 0.75, depth * 0.3];
          size = [2, 0.8, 1];
          color = '#8d6e63'; // Brown
          break;
        case 'chair':
          position = customPosition || [width * 0.6, 0.5, depth * 0.5];
          size = [0.8, 1.2, 0.8];
          color = '#616161'; // Dark gray
          break;
        case 'lightbulb':
          position = customPosition || [width * 0.5, 2, depth * 0.5];
          size = [0.2, 0.2, 0.2];
          color = '#ffeb3b'; // Yellow
          break;
        case 'sofa':
          position = customPosition || [width * 0.3, 0.5, depth * 0.8];
          size = [2.5, 0.8, 1];
          color = '#3949ab'; // Blue
          break;
        case 'bookshelf':
          position = customPosition || [width * 0.15, 1, depth * 0.3];
          size = [1.2, 2, 0.4];
          color = '#5d4037'; // Dark brown
          break;
        default:
          position = customPosition || [width/2, 0.5, depth/2];
          size = [1, 1, 1];
          color = '#bbbbbb'; // Light gray
      }
      
      // Create furniture
      const furnitureGeometry = new THREE.BoxGeometry(size[0], size[1], size[2]);
      const furnitureMaterial = new THREE.MeshStandardMaterial({ color });
      const furnitureMesh = new THREE.Mesh(furnitureGeometry, furnitureMaterial);
      
      furnitureMesh.position.set(position[0], position[1], position[2]);
      furnitureMesh.castShadow = true;
      furnitureMesh.receiveShadow = true;
      
      // Add to scene
      this.scene.add(furnitureMesh);
      this.furnitureMeshes.push(furnitureMesh);
      
      // Add to furniture data array
      const furnitureItem = {
        type,
        position,
        size,
        fixedX,
        fixedZ
      };
      
      this.furniture.push(furnitureItem);
      
      // Return index of the added furniture
      return this.furniture.length - 1;
    }
    
    removeFurniture(index) {
      if (index < 0 || index >= this.furniture.length) return;
      
      // Remove from scene
      this.scene.remove(this.furnitureMeshes[index]);
      
      // Remove from arrays
      this.furnitureMeshes.splice(index, 1);
      this.furniture.splice(index, 1);
    }
    
    clearFurniture() {
      // Remove all furniture from scene
      this.furnitureMeshes.forEach(mesh => {
        this.scene.remove(mesh);
      });
      
      // Clear arrays
      this.furnitureMeshes = [];
      this.furniture = [];
    }
    
    updateFurniturePositions() {
      const { width, depth } = this.room;
      
      this.furniture.forEach((item, index) => {
        if (!this.furnitureMeshes[index]) return;
        
        // Calculate new position
        let posX, posZ;
        
        if (item.fixedX) {
          posX = item.position[0];
        } else {
          const relativeX = item.position[0] / width;
          posX = relativeX * width;
        }
        
        if (item.fixedZ) {
          posZ = item.position[2];
        } else {
          const relativeZ = item.position[2] / depth;
          posZ = relativeZ * depth;
        }
        
        // Update position in data
        item.position[0] = posX;
        item.position[2] = posZ;
        
        // Update mesh position
        this.furnitureMeshes[index].position.set(posX, item.position[1], posZ);
      });
    }

    addPerson() {
        const { THREE } = this;
      
        // --- Create the person group and its parts ---
        const personGroup = new THREE.Group();
      
        // --- Dimensions (randomized for variety) ---
        const headSize = THREE.MathUtils.randFloat(0.4, 0.7);       // head cube size
        const bodyWidth = THREE.MathUtils.randFloat(0.4, 0.7);
        const bodyHeight = THREE.MathUtils.randFloat(0.8, 1.3);
        const legHeight = THREE.MathUtils.randFloat(0.3, 0.7);
        const armHeight = THREE.MathUtils.randFloat(0.3, 0.7);
        const armWidth = 0.2;
        const legWidth = 0.2;
      
        // --- Torso (Body) ---
        const bodyGeometry = new THREE.BoxGeometry(bodyWidth, bodyHeight, bodyWidth);
        const bodyMaterial = new THREE.MeshLambertMaterial({ color: '#7b5453' });
        const bodyMesh = new THREE.Mesh(bodyGeometry, bodyMaterial);
        bodyMesh.position.y = bodyHeight / 2; // bottom at 0
        personGroup.add(bodyMesh);
      
        // --- Head ---
        const headGeometry = new THREE.BoxGeometry(headSize, headSize, headSize);
        const headMaterial = new THREE.MeshLambertMaterial({ color: '#6ccdc4' });
        const headMesh = new THREE.Mesh(headGeometry, headMaterial);
        // Position the head on top of the torso (with a small offset)
        headMesh.position.y = bodyHeight + headSize / 2 + 0.1;
        personGroup.add(headMesh);
      
        // --- Arms ---
        const leftArmGeometry = new THREE.BoxGeometry(armWidth, armHeight, armWidth);
        const leftArmMaterial = new THREE.MeshLambertMaterial({ color: 0x00ff00 });
        const leftArm = new THREE.Mesh(leftArmGeometry, leftArmMaterial);
        leftArm.position.x = -(bodyWidth / 2 + armWidth / 2);
        leftArm.position.y = bodyHeight * 0.75;
        personGroup.add(leftArm);
      
        const rightArm = new THREE.Mesh(leftArmGeometry, leftArmMaterial);
        rightArm.position.x = bodyWidth / 2 + armWidth / 2;
        rightArm.position.y = bodyHeight * 0.75;
        personGroup.add(rightArm);
      
        // --- Legs ---
        const legGeometry = new THREE.BoxGeometry(legWidth, legHeight, legWidth);
        const legMaterial = new THREE.MeshLambertMaterial({ color: 0xffff00 });
        const leftLeg = new THREE.Mesh(legGeometry, legMaterial);
        leftLeg.position.x = -bodyWidth / 4;
        leftLeg.position.y = -legHeight / 2; // its bottom is legHeight/2 below group origin
        personGroup.add(leftLeg);
      
        const rightLeg = new THREE.Mesh(legGeometry, legMaterial);
        rightLeg.position.x = bodyWidth / 4;
        rightLeg.position.y = -legHeight / 2;
        personGroup.add(rightLeg);
      
        // --- Eyes ---
        const eyeRadius = 0.05;
        const eyeGeometry = new THREE.SphereGeometry(eyeRadius, 8, 8);
        const eyeMaterial = new THREE.MeshLambertMaterial({ color: 0x000000 });
        const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
        leftEye.position.x = -headSize / 4;
        leftEye.position.y = headMesh.position.y + 0.1;
        leftEye.position.z = headSize / 2 + 0.01;
        personGroup.add(leftEye);
      
        const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
        rightEye.position.x = headSize / 4;
        rightEye.position.y = headMesh.position.y + 0.1;
        rightEye.position.z = headSize / 2 + 0.01;
        personGroup.add(rightEye);
      
        // --- Adjust the group so that the lowest point (feet) is at y = 0 ---
        // Compute the bounding box in the group's current local space.
        const box = new THREE.Box3().setFromObject(personGroup);
        // Calculate the vertical offset needed (if the minimum y is negative, offset upward)
        const offsetY = -box.min.y;
        // Apply the offset to each child so that the bottom becomes 0 in local space
        personGroup.children.forEach(child => {
          child.position.y += offsetY;
        });
      
        // --- Now set the final position of the person in the room ---
        const margin = 0.5;
        const x = margin + Math.random() * (this.room.width - 2 * margin);
        const z = margin + Math.random() * (this.room.depth - 2 * margin);
        // With the adjustment, setting y = 0 will place the feet exactly at the floor level.
        personGroup.position.set(x, 0, z);
      
        // Add the adjusted personGroup to the scene and track it
        this.scene.add(personGroup);
        this.peopleMeshes.push(personGroup);
    }

    // Update the number of people displayed
    updatePeople(count) {
        // Add new people if count is higher than current number
        while (this.peopleMeshes.length < count) {
            this.addPerson();
        }
        // Remove people if count is lower than current number
        while (this.peopleMeshes.length > count) {
            const person = this.peopleMeshes.pop();
            this.scene.remove(person);
        }
    }
      
    
    applyPreset(presetName) {
      // Clear existing furniture
      this.clearFurniture();
      
      switch(presetName) {
        case 'bedroom':
          this.updateRoom(8, 8, 2.8, '#d1c4e9', '#9e9e9e', '#f5f5f5');
          this.updateLighting('#ffffff', 1.5, true);
          
          // Add bedroom furniture
          var bedIndex = this.addFurniture('sofa', true, true);
          if (bedIndex !== null) {
            this.furniture[bedIndex].position = [4, 0.5, 4];
            this.furnitureMeshes[bedIndex].position.set(4, 0.5, 4);
          }
          
          this.addFurniture('bookshelf');
          this.addFurniture('chair');
          this.addFurniture('desk');
          break;
          
        case 'office':
          this.updateRoom(10, 10, 3, '#e0e0e0', '#ad8a64', '#f5f5f5');
          this.updateLighting('#ffffff', 1.5, true);
          
          // Add office furniture
          this.addFurniture('desk');
          this.addFurniture('chair');
          this.addFurniture('bookshelf');
          break;
          
        case 'livingroom':
          this.updateRoom(12, 10, 3.2, '#f5f5f5', '#8d6e63', '#f5f5f5');
          this.updateLighting('#ffffff', 1.5, true);
          
          // Add living room furniture
          var sofaIndex = this.addFurniture('sofa', true, true);
          if (sofaIndex !== null) {
            this.furniture[sofaIndex].position = [6, 0.5, 7.5];
            this.furnitureMeshes[sofaIndex].position.set(6, 0.5, 7.5);
          }
          
          var sofa2Index = this.addFurniture('sofa', true, true);
          if (sofa2Index !== null) {
            this.furniture[sofa2Index].position = [9, 0.5, 5];
            this.furnitureMeshes[sofa2Index].position.set(9, 0.5, 5);
          }
          break;
          
        case 'gamingRoom':
          this.updateRoom(11, 9, 3, '#263238', '#424242', '#424242');
          this.updateLighting('#ff00ff', 2, true);
          
          // Add gaming room furniture
          var deskIndex = this.addFurniture('desk', true, true);
          if (deskIndex !== null) {
            this.furniture[deskIndex].position = [5.5, 0.75, 3];
            this.furnitureMeshes[deskIndex].position.set(5.5, 0.75, 3);
          }
          
          this.addFurniture('chair');
          this.addFurniture('sofa');
          break;
      }
    }
    
    startAnimation() {
      const animate = () => {
        this.animationFrameId = requestAnimationFrame(animate);
        
        if (this.controls) {
          this.controls.update();
        }
        
        if (this.renderer && this.scene && this.camera) {
          this.renderer.render(this.scene, this.camera);
        }
      };
      
      animate();
    }
    
    stopAnimation() {
      if (this.animationFrameId) {
        cancelAnimationFrame(this.animationFrameId);
        this.animationFrameId = null;
      }
    }
    
    handleResize() {
      if (!this.camera || !this.renderer || !this.container) return;
      
      this.camera.aspect = this.container.clientWidth / this.container.clientHeight;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    }
    
    dispose() {
      // Stop animation
      this.stopAnimation();
      
      // Remove event listeners
      window.removeEventListener('resize', this.handleResize);
      
      this.clearModels();

      // Dispose geometries and materials
      if (this.scene) {
        this.scene.traverse((object) => {
          if (object.geometry) object.geometry.dispose();
          
          if (object.material) {
            if (Array.isArray(object.material)) {
              object.material.forEach(material => material.dispose());
            } else {
              object.material.dispose();
            }
          }
        });
      }
      
      // Dispose renderer
      if (this.renderer) {
        this.renderer.dispose();
      }
      
      // Remove canvas from container
      if (this.container && this.renderer && this.renderer.domElement) {
        this.container.removeChild(this.renderer.domElement);
      }
      
      // Clear references
      this.scene = null;
      this.camera = null;
      this.renderer = null;
      this.controls = null;
      this.roomMeshes = {};
      this.furnitureMeshes = [];
      this.directionalLight = null;
      this.ambientLight = null;
      this.loaders = {};
      this.models3D = {};
    }
    
    // Get current state for Vue
    getState() {
      return {
        room: { ...this.room },
        lighting: { ...this.lighting },
        furniture: this.furniture.map(item => ({ ...item }))
      };
    }
  }