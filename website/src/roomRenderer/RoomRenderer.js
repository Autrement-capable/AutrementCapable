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
      this.totalModelsToLoad = 0;
      this.loadedModelsCount = 0;
      this.loadingProgress = 0;
      this.onLoadingProgressCallback = null;

      this.objectCategories = {
        polyvalent: ['desk', 'chair', 'bookshelf', 'computer', 'filing', 'lamp1', 'notebook', 'tv', 'tvstand', 'whiteboard', 'sofa', 'rug', 'beanbag', 'plant', 'toi', 'painting1', 'painting2', 'painting3', 'window', 'door'],
        social: ['coffeetable', 'plant', 'speakers', 'ceilingFan', 'meetingTable', 'moi', 'painting1', 'painting2', 'painting3', 'tvstand', 'window', 'door'],
      };
      
      this.categoryConfigurations = {
        // Espace social contrôlé
        social: {
          coffeetable: { position: [6, 1.4, 0.3], scale: 0.25, rotation: [0, 0, 0] },
          plant: { position: [9, 0.25, 1], scale: 0.005, rotation: [0, 0, 0] },
          speakers: { position: [7, 0.8, 2], scale: 0.4, rotation: [0, -Math.PI/6, 0] },
          ceilingFan: { position: [5, 1, 5], scale: 0.3, rotation: [0, Math.PI/2, 0] },
          meetingTable: { position: [5.5, 0.35, 5.5], scale: 0.75, rotation: [0, Math.PI, 0] },
          moi: { position: [9, 0.25, 1], scale: 0.10, rotation: [0, Math.PI/2, 0] },
          painting1: { position: [0, 1.5, 3], scale: 1.7, rotation: [0, Math.PI/2, 0] },
          painting2: { position: [0, 1.5, 10], scale: 1.7, rotation: [0, Math.PI, 0] },
          painting3: { position: [3, 1.5, 0.05], scale: 1.7, rotation: [0, 0, 0] },
          tvstand: { position: [5, 0, 0.5], scale: 0.021, rotation: [0, 0, 0] },
          window: { position: [9.975, 1.8, 3.5], scale: 0.0010, rotation: [Math.PI/2, 0, Math.PI/2] },
          door: { position: [7, 0, 10], scale: 0.022, rotation: [0, 0, 0] },
        },
        polyvalent: {
          // Work zone (left side)
          desk: { position: [4, 0, 1], scale: 0.2, rotation: [0, 0, 0] },
          chair: { position: [3.6, 0, 2], scale: 0.015, rotation: [0, Math.PI, 0] },
          computer: { position: [3.65, 1.28, 1.2], scale: 1, rotation: [0, Math.PI, 0] },
          notebook: { position: [5, 0, 1.8], scale: 0.1, rotation: [0, Math.PI/3, 0] },
          whiteboard: { position: [4, 1.35, 0.1], scale: 2.6, rotation: [0, 0, 0] },
          filing: { position: [9.4, 0, 2], scale: 1.3, rotation: [0, -Math.PI/2, 0] },
          
          // Relaxation zone (right side)
          sofa: { position: [7.5, -0.1, 6], scale: 0.017, rotation: [0, -Math.PI/2, 0] },
          rug: { position: [5, 0, 6], scale: 4.3, rotation: [0, Math.PI/2, 0] },
          beanbag: { position: [1, 0, 9], scale: 16, rotation: [0, Math.PI - 45, 0] },
          tv: { position: [2.5, 1, 6], scale: 1.5, rotation: [0, -Math.PI/2, 0] },
          tvstand: { position: [2.5, 0, 6], scale: 0.021, rotation: [0, -Math.PI/2, 0] },
          
          // Shared elements
          bookshelf: { position: [0.3, 0, 5], scale: 0.9, rotation: [0, Math.PI/2, 0] },
          lamp1: { position: [5, 2.4, 5], scale: 1.2, rotation: [0, Math.PI/4, 0] },
          plant: { position: [9, 0.25, 9], scale: 0.005, rotation: [0, 0, 0] },
          painting1: { position: [0, 1.5, 3], scale: 1.7, rotation: [0, Math.PI/2, 0] },
          painting2: { position: [0, 1.5, 10], scale: 1.7, rotation: [0, Math.PI, 0] },
          painting3: { position: [7, 1.5, 0.05], scale: 1.7, rotation: [0, 0, 0] },
          toi: { position: [2.5, 0.143, 7], scale: 0.015, rotation: [0, -Math.PI/2, 0] },
          window: { position: [9.975, 1.8, 5.5], scale: 0.0010, rotation: [Math.PI/2, 0, Math.PI/2] },
          door: { position: [7, 0, 10], scale: 0.022, rotation: [0, 0, 0] },
        },
      };

      this.room = {
        width: 9,
        depth: 9, 
        height: 3.2,
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

      // Set camera to view the center of the room
      const { width, height, depth } = this.room;
      this.camera.position.set(width / 2, height / 2, depth * 1.5);
      this.controls.target.set(width / 2, height / 2, depth / 2);
      this.controls.update();
      
      // Add lighting
      this.setupLighting();
    }
    
    setupLighting() {
      const { THREE } = this;
      const { width, height, depth  } = this.room;
      const { color, intensity, ambient } = this.lighting;

      this.light = new THREE.PointLight(0xffffff, 1, 500, 0.2);
      this.light.position.set(width/2, height - 0.5, depth/2);
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
      
      const basePath = '/models/';

      // Mapping des noms de modèles vers leurs fichiers
      const modelPaths = {
        // Mobilier de base
        desk: '/desk/scene.gltf',
        chair: '/chair/scene.gltf',
        chair2: '/chair/scene.gltf',
        bookshelf: '/bookshelf/scene.gltf',
        sofa: '/couch/scene.gltf',
        lightbulb: '/light_bulb/scene.gltf',
        lightbulb2: '/light_bulb/scene.gltf',
        lamp1: '/lamp1/scene.gltf',
        meetingTable: '/conference_table/thomas.gltf',
        door: 'door/scene.gltf',
        
        beanbag: '/beanbag/scene.gltf',
        plant: '/plant/scene.gltf',
        lamp: '/light_bulb/scene.gltf',
        computer: '/computer/scene.gltf',
        tv: '/tv/scene.gltf',
        tvstand: '/tv_stand/scene.gltf',
        coffeetable: '/coffemaker/scene.gltf',
        rug: '/rug/scene.gltf',
        filing: '/filing/scene.gltf',
        painting1: '/painting1/scene.gltf',
        painting2: '/painting2/scene.gltf',
        painting3: '/painting3/scene.gltf',
        ceilingFan: '/ceiling_fan/scene.gltf',

        notebook: '/notebook/scene.gltf',
        whiteboard: '/whiteboard/scene.gltf',
        cushion: '/cushion/scene.gltf',
        coffeemaker: '/coffeemaker/scene.gltf',
        moi: '/conference_table/moi.glb',
        toi: '/conference_table/toi.glb',
        window: '/window/scene.gltf',
      };
      
      // Si le modèle n'est pas dans notre mapping, utiliser un modèle par défaut
      const modelFile = modelPaths[modelName];
      
      return basePath + modelFile;
    }

    setLoadingProgressCallback(callback) {
      this.onLoadingProgressCallback = callback;
    }

    loadObjectsByCategory(category) {
      // D'abord, supprimer tous les modèles existants
      this.clearModels();
      
      // Obtenir la liste des objets pour cette catégorie
      const objects = this.objectCategories[category] || this.objectCategories.minimal;
      console.log(`Loading ${objects.length} objects for category: ${category}`);
    
      const categoryConfig = this.categoryConfigurations[category] || {};
      
      this.totalModelsToLoad = objects.length;
      this.loadedModelsCount = 0;
      this.loadingProgress = 0;
    
      if (this.onLoadingProgressCallback) {
        this.onLoadingProgressCallback(0, this.totalModelsToLoad);
      }
    
      // Charger chaque objet avec sa position prédéfinie
      const loadPromises = objects.map((objectName) => {
        // Log which model we're trying to load
        console.log(`Attempting to load model: ${objectName}`);
        
        // Utiliser la configuration prédéfinie si disponible, sinon utiliser des valeurs par défaut
        const config = categoryConfig[objectName] || {
          position: [this.room.width/2, 0, this.room.depth/2],
          scale: 0.7,
          rotation: [0, 0, 0]
        };
        
        // Ajuster la position en fonction de la taille de la pièce si nécessaire
        const position = this.adjustPositionToRoomSize(config.position);
        
        // Get the model path before loading to check if it's correct
        const modelPath = this.getModelPath(objectName);
        console.log(`Model path for ${objectName}: ${modelPath}`);
        
        return this.loadModel(objectName, position, config.scale, config.rotation)
          .then(model => {
            this.loadedModelsCount++;
            this.loadingProgress = (this.loadedModelsCount / this.totalModelsToLoad) * 100;
            
            console.log(`Successfully loaded model: ${objectName} (${this.loadedModelsCount}/${this.totalModelsToLoad})`);
            
            // Notify the Vue component of progress
            if (this.onLoadingProgressCallback) {
              this.onLoadingProgressCallback(
                this.loadingProgress, 
                this.totalModelsToLoad,
                objectName
              );
            }
            return model;
          })
          .catch(error => {
            // Better error handling - still count failed models as "loaded" to avoid stalling
            console.error(`Failed to load model ${objectName}: ${error}`);
            this.loadedModelsCount++;
            this.loadingProgress = (this.loadedModelsCount / this.totalModelsToLoad) * 100;
            
            // Notify about the error but continue loading other models
            if (this.onLoadingProgressCallback) {
              this.onLoadingProgressCallback(
                this.loadingProgress, 
                this.totalModelsToLoad,
                `${objectName} (échec)`
              );
            }
            
            // Return null for failed models instead of rejecting the promise
            return null;
          });
      });
      
      return Promise.all(loadPromises)
        .then(models => {
          console.log(`Completed loading ${models.filter(m => m !== null).length}/${objects.length} models for category ${category}`);
          return models.filter(m => m !== null); // Filter out failed models (null)
        });
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

      // Front wall
      const frontWallGeometry = new this.THREE.PlaneGeometry(width, height);
      const frontWall = new this.THREE.Mesh(frontWallGeometry, wallMaterial);
      frontWall.position.set(width / 2, height / 2, depth);
      frontWall.rotation.y = Math.PI;
      frontWall.receiveShadow = true;
      this.roomMeshes.frontWall = frontWall;
      this.scene.add(frontWall);
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
      this.camera.position.set(width / 2, height / 2, depth * 1.5);
      this.controls.target.set(width / 2, height / 2, depth / 2);
      this.controls.update();
            
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

      if (this.roomMeshes.frontWall) {
        this.roomMeshes.frontWall.material.color.set(wallColor);
      }
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