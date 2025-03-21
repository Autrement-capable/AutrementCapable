<template>
  <div class="environment-container">
    <div class="controls-panel">
      <h2>Personnalisation de l'espace</h2>
      
      <!-- Room Dimensions -->
      <div class="control-group">
        <h3>Dimensions</h3>
        <div class="control-item">
          <label style="text-align: center; padding-top: 15px;">Largeur: {{ roomWidth }}m</label>
          <div class="button-group">
            <button @click="adjustDimension('roomWidth', -0.5)" class="btn-small-dim">-</button>
            <button @click="adjustDimension('roomWidth', 0.5)" class="btn-small-dim">+</button>
          </div>
        </div>

        <div class="control-item">
          <label style="text-align: center; padding-top: 15px;">Profondeur: {{ roomDepth }}m</label>
          <div class="button-group">
            <button @click="adjustDimension('roomDepth', -0.5)" class="btn-small-dim">-</button>
            <button @click="adjustDimension('roomDepth', 0.5)" class="btn-small-dim">+</button>
          </div>
        </div>

        <div class="control-item">
          <label style="text-align: center; padding-top: 15px;">Hauteur: {{ roomHeight }}m</label>
          <div class="button-group">
            <button @click="adjustDimension('roomHeight', -0.1)" class="btn-small-dim">-</button>
            <button @click="adjustDimension('roomHeight', 0.1)" class="btn-small-dim">+</button>
          </div>
        </div>
      </div>
      
      <!-- Colors -->
      <div class="control-group">
        <h3>Couleurs</h3>
        <div class="control-item">
          <label>Murs:</label>
          <input type="color" v-model="wallColor" @change="updateColors" />
        </div>
        <div class="control-item">
          <label>Sol:</label>
          <input type="color" v-model="floorColor" @change="updateColors" />
        </div>
        <div class="control-item">
          <label>Plafond:</label>
          <input type="color" v-model="ceilingColor" @change="updateColors" />
        </div>
      </div>
      
      <!-- Lighting -->
      <div class="control-group">
        <h3>Éclairage</h3>
        <div class="control-item">
          <label>Couleur:</label>
          <input type="color" v-model="lightColor" @change="updateLighting" />
        </div>
        <div class="control-item">
          <label>Intensité: {{ lightIntensity }}</label>
          <input type="range" v-model.number="lightIntensity" min="0" max="5" step="0.1" @change="updateLighting" />
        </div>
        <div class="control-item">
          <label>Lumière ambiante</label>
          <input type="checkbox" v-model="ambientLight" @change="updateLighting" />
        </div>
      </div>
      
      <!-- Furniture -->
      <div class="control-group">
        <h3>Meubles</h3>
        <div class="control-item">
          <label>Type:</label>
          <select v-model="selectedFurniture">
            <option value="desk">Bureau</option>
            <option value="chair">Chaise</option>
            <option value="sofa">Canapé</option>
            <option value="bookshelf">Bibliothèque</option>
          </select>
        </div>
        <button @click="addFurniture" class="btn">Ajouter meuble</button>
        
        <div v-if="furniture.length > 0" class="furniture-list">
          <h4>Meubles dans la pièce:</h4>
          <ul>
            <li v-for="(item, index) in furniture" :key="index">
              {{ getFurnitureName(item.type) }}
              <button @click="removeFurniture(index)" class="btn-small">Supprimer</button>
            </li>
          </ul>
        </div>
      </div>
      
      <!-- Ambient Noise -->
      <div class="control-group">
        <h3>Ambiance sonore</h3>
        <div class="control-item">
          <label>Personnes dans la pièce: {{ peopleCount }}</label>
          <input type="range" v-model.number="peopleCount" min="0" max="20" step="1" @change="updateAmbientNoise" />
        </div>
        <div class="control-item">
          <label>Son actif</label>
          <input type="checkbox" v-model="soundEnabled" @change="updateAmbientNoise" />
        </div>
      </div>
      
      <!-- Presets -->
      <div class="control-group">
        <h3>Configurations prédéfinies</h3>
        <div class="preset-buttons">
          <button @click="applyPreset('bedroom')" class="btn">Chambre</button>
          <button @click="applyPreset('office')" class="btn">Bureau</button>
          <button @click="applyPreset('livingroom')" class="btn">Salon</button>
          <button @click="applyPreset('gamingRoom')" class="btn">Salle de jeux</button>
        </div>
      </div>
    </div>
    
    <div class="room-visualization" ref="container"></div>
    
    <!-- Audio for ambient noise -->
    <audio ref="ambientAudio" loop preload="auto" v-show="false"></audio>
  </div>
</template>

<script>
// Import our isolated RoomRenderer class
import RoomRenderer from './RoomRenderer';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

export default {
  name: 'EnvironmentPage',
  data() {
    return {
      // Room dimensions
      roomWidth: 10,
      roomDepth: 10,
      roomHeight: 3,
      
      // Colors
      wallColor: '#e0e0e0',
      floorColor: '#ad8a64',
      ceilingColor: '#f5f5f5',
      
      // Lighting
      lightColor: '#ffffff',
      lightIntensity: 1.5,
      ambientLight: true,
      
      // Furniture
      selectedFurniture: 'desk',
      furniture: [],
      
      // Ambient noise
      peopleCount: 0,
      soundEnabled: false,
      
      // The renderer instance (not tracked by Vue)
      renderer: null
    };
  },
  mounted() {
    // Create the room renderer instance
    // This instance handles all Three.js work independently of Vue
    this.renderer = new RoomRenderer(this.$refs.container);
    const loader = new GLTFLoader();
    
    loader.load('/chair/scene.gltf', (gltf) => { 
      gltf.scene.scale.set(0.012, 0.012, 0.012);
      gltf.scene.position.set(1.3, 0, 6.3);
      gltf.scene.rotation.y = 4.7;
      this.renderer.scene.add(gltf.scene);
    },
    undefined,
    (error) => {
      console.error("Error loading gltf", error);
    },
    );

    loader.load('/desk/scene.gltf', (gltf) => { 
      gltf.scene.scale.set(0.17, 0.17, 0.17);
      gltf.scene.position.set(0.44, 0, 6);
      gltf.scene.rotation.y = Math.PI / 2;
      this.renderer.scene.add(gltf.scene);
    },
    undefined,
    (error) => {
      console.error("Error loading gltf", error);
    },);

    loader.load('/couch/scene.gltf', (gltf) => { 
      gltf.scene.scale.set(0.013, 0.013, 0.013);
      gltf.scene.position.set(9.4, -0.05, 4.5);
      gltf.scene.rotation.y = 4.7;
      this.renderer.scene.add(gltf.scene);
    },
    undefined,
    (error) => {
      console.error("Error loading gltf", error);
    },);

    // Set up audio for ambient noise
    if (this.$refs.ambientAudio) {
      this.$refs.ambientAudio.volume = 0;
    }
    
    // Initialize with default values and apply preset
    // Let the renderer initialize itself (it will load Three.js)
    setTimeout(() => {
      this.applyPreset('office');
    }, 500);
  },
  beforeUnmount() {
    // Clean up
    if (this.renderer) {
      this.renderer.dispose();
      this.renderer = null;
    }
    
    // Stop audio
    if (this.$refs.ambientAudio) {
      this.$refs.ambientAudio.pause();
    }
  },
  methods: {
    // Update the room dimensions
    updateRoom() {
      if (!this.renderer) return;
      
      this.renderer.updateRoom(
        this.roomWidth,
        this.roomDepth,
        this.roomHeight,
        this.wallColor,
        this.floorColor,
        this.ceilingColor
      );
      
      // Sync furniture data from the renderer
      this.syncFurnitureData();
    },
    
    // Update the room colors
    updateColors() {
      if (!this.renderer) return;
      
      this.renderer.updateRoomColors(
        this.wallColor,
        this.floorColor,
        this.ceilingColor
      );
    },
    
    // Update lighting
    updateLighting() {
      if (!this.renderer) return;
      
      this.renderer.updateLighting(
        this.lightColor,
        this.lightIntensity,
        this.ambientLight
      );
    },
    
    // Add a piece of furniture
    addFurniture() {
      if (!this.renderer) return;
      
      this.renderer.addFurniture(this.selectedFurniture);
      
      // Sync furniture data from the renderer
      this.syncFurnitureData();
    },
    
    // Remove a piece of furniture
    removeFurniture(index) {
      if (!this.renderer) return;
      
      this.renderer.removeFurniture(index);
      
      // Sync furniture data from the renderer
      this.syncFurnitureData();
    },
    
    // Sync the furniture data from the renderer
    syncFurnitureData() {
      if (!this.renderer) return;
      
      // Get state from the renderer (cloned to avoid reactivity issues)
      const state = this.renderer.getState();
      
      // Update Vue's reactive state with the non-reactive renderer state
      this.furniture = state.furniture;
      
      // Also sync room data
      this.roomWidth = state.room.width;
      this.roomDepth = state.room.depth;
      this.roomHeight = state.room.height;
      this.wallColor = state.room.wallColor;
      this.floorColor = state.room.floorColor;
      this.ceilingColor = state.room.ceilingColor;
      
      // And lighting
      this.lightColor = state.lighting.color;
      this.lightIntensity = state.lighting.intensity;
      this.ambientLight = state.lighting.ambient;
    },
    
    // Apply a preset room configuration
    applyPreset(presetName) {
      if (!this.renderer) return;
      
      this.renderer.applyPreset(presetName);
      
      // Sync furniture data from the renderer
      this.syncFurnitureData();
    },
    
    // Update ambient noise
    updateAmbientNoise() {
      if (!this.$refs.ambientAudio) return;
      
      // Update audio source based on people count
      let audioSrc;
      if (this.peopleCount === 0) {
        audioSrc = 'https://cdn.pixabay.com/download/audio/2022/03/10/audio_6629de9d6b.mp3'; // Quiet ambience
      } else if (this.peopleCount < 5) {
        audioSrc = 'https://cdn.pixabay.com/download/audio/2022/01/26/audio_31e2b19a63.mp3'; // Soft cafe
      } else if (this.peopleCount < 10) {
        audioSrc = 'https://cdn.pixabay.com/download/audio/2021/10/08/audio_9e70855640.mp3'; // Medium crowd
      } else {
        audioSrc = 'https://cdn.pixabay.com/download/audio/2021/08/09/audio_8eb4af9c81.mp3'; // Loud crowd
      }
      
      // Only update src if needed to avoid restarting the audio unnecessarily
      if (this.$refs.ambientAudio.src !== audioSrc) {
        this.$refs.ambientAudio.src = audioSrc;
      }
      
      // Update volume and playback
      if (this.soundEnabled && this.peopleCount > 0) {
        this.$refs.ambientAudio.volume = Math.min(0.8, this.peopleCount / 20);
        this.$refs.ambientAudio.play().catch(e => console.log('Audio play failed:', e));
      } else {
        this.$refs.ambientAudio.pause();
      }

      if (this.renderer) {
        this.renderer.updatePeople(this.peopleCount);
      }
    },

    adjustDimension(prop, delta) {
      let min, max;
      if (prop === 'roomWidth' || prop === 'roomDepth') {
        min = 3;
        max = 15;
      } else if (prop === 'roomHeight') {
        min = 2;
        max = 6;
      }
      // Calcule la nouvelle valeur en s'assurant qu'elle reste dans les bornes
      let newValue = this[prop] + delta;
      if (newValue < min) newValue = min;
      if (newValue > max) newValue = max;
      this[prop] = newValue;
      // Met à jour la salle
      this.updateRoom();
    },
    
    // Get furniture display name
    getFurnitureName(type) {
      const names = {
        desk: 'Bureau',
        chair: 'Chaise',
        sofa: 'Canapé',
        bookshelf: 'Bibliothèque'
      };
      return names[type] || type;
    }
  }
};
</script>

<style scoped>
.environment-container {
  display: flex;
  height: 100vh;
  width: 100%;
  position: relative;
  font-family: 'Glacial Indifference', sans-serif;
}

.controls-panel {
  width: 300px;
  background-color: rgba(255, 255, 255, 0.95);
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  padding: 20px;
  z-index: 10;
}

.room-visualization {
  flex-grow: 1;
  position: relative;
}

h2 {
  text-align: center;
  margin-bottom: 15px;
  color: #333;
}

h3 {
  margin: 10px 0;
  color: #555;
  font-size: 1.1em;
}

.control-group {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.control-item {
  margin: 10px 0;
  display: flex;
  flex-direction: column;
}

.control-item label {
  margin-bottom: 5px;
  font-size: 0.9em;
}

input[type="range"] {
  width: 100%;
}

input[type="color"] {
  width: 100%;
  height: 30px;
}

.btn {
  background-color: #007BFF;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 5px;
}

.btn:hover {
  background-color: #0056b3;
}

.button-group {
  display: inline-flex;
  gap: 5px;
  margin-top: 5px;
  justify-content: center;
  width: 100%;
}

.btn-small-dim {
  background-color: #007BFF;
  color: rgb(255, 255, 255);
  border: none;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
  width: 30px;
  height: 30px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-small {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 2px 6px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8em;
}

.btn-small:hover {
  background-color: #bd2130;
}

.furniture-list {
  margin-top: 10px;
}

.furniture-list ul {
  list-style: none;
  padding-left: 5px;
}

.furniture-list li {
  margin: 5px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.preset-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

select {
  padding: 5px;
  margin-bottom: 8px;
}
</style>