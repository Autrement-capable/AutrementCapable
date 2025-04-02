<!-- StaticBackgrounds.vue -->
<template>
    <div class="static-background" :class="theme">
      <!-- Container for all static elements -->
      <div class="static-elements">
        <!-- Dynamic space elements based on the selected theme -->
        <template v-if="theme === 'cosmic'">
          <!-- Static Comets -->
          <div class="static-comet comet-1"></div>
          <div class="static-comet comet-2"></div>
          <div class="static-comet comet-3"></div>
          
          <!-- Static Galaxy -->
          <div class="static-galaxy galaxy-1"></div>
          
          <!-- Static Planets -->
          <div class="static-planet planet-1">
            <div class="planet-rings"></div>
          </div>
          
          <div class="static-planet planet-2">
            <div class="planet-atmosphere"></div>
            <div class="planet-storm"></div>
          </div>
          
          <div class="static-planet planet-3">
            <div class="planet-ice-caps"></div>
            <div class="planet-moons">
              <div class="planet-moon moon-1"></div>
              <div class="planet-moon moon-2"></div>
            </div>
          </div>
  
          <!-- Static Stars Background -->
          <div class="static-stars"></div>
        </template>
  
        <!-- Ocean theme static elements -->
        <template v-else-if="theme === 'ocean'">
          <!-- Static Light Rays -->
          <div class="static-light-ray light-ray-1"></div>
          <div class="static-light-ray light-ray-2"></div>
          <div class="static-light-ray light-ray-3"></div>
          
          <!-- Static Bubbles -->
          <div class="static-bubble bubble-1"></div>
          <div class="static-bubble bubble-2"></div>
          <div class="static-bubble bubble-3"></div>
          <div class="static-bubble bubble-4"></div>
          <div class="static-bubble bubble-5"></div>
          <div class="static-bubble bubble-6"></div>
          
          <!-- Static Plankton Particles -->
          <div class="static-plankton-container">
            <div v-for="i in 20" :key="`plankton-${i}`" class="static-plankton"></div>
          </div>
          
          <!-- Static Coral Reef -->
          <div class="static-coral coral-1">
            <div class="coral-branch branch-1"></div>
            <div class="coral-branch branch-2"></div>
            <div class="coral-branch branch-3"></div>
          </div>
          
          <div class="static-coral coral-2">
            <div class="coral-branch branch-1"></div>
            <div class="coral-branch branch-2"></div>
          </div>
          
          <!-- Static Fish School -->
          <div class="static-fish-school fish-school-1">
            <div v-for="i in 5" :key="`school-1-fish-${i}`" class="static-school-fish"></div>
          </div>
          
          <div class="static-fish-school fish-school-2">
            <div v-for="i in 7" :key="`school-2-fish-${i}`" class="static-school-fish"></div>
          </div>
  
          <!-- Static Shark -->
          <div class="static-shark">
            <div class="shark-body">
              <div class="shark-eye"></div>
              <div class="shark-eye shark-eye-shine"></div>
              <div class="shark-gill gill-1"></div>
              <div class="shark-gill gill-2"></div>
              <div class="shark-gill gill-3"></div>
              <div class="shark-mouth"></div>
            </div>
            <div class="shark-dorsal-fin"></div>
            <div class="shark-pectoral-fin"></div>
            <div class="shark-pelvic-fin"></div>
            <div class="shark-tail">
              <div class="shark-tail-fin"></div>
            </div>
            <div class="shark-shadow"></div>
          </div>
  
          <!-- Static Individual Fish -->
          <div class="static-fish fish-1">
            <div class="fish-tail"></div>
          </div>
          <div class="static-fish fish-2">
            <div class="fish-tail"></div>
          </div>
          <div class="static-fish fish-3">
            <div class="fish-tail"></div>
          </div>
          
          <!-- Static Seaweed -->
          <div class="static-seaweed seaweed-1">
            <div class="seaweed-strand"></div>
            <div class="seaweed-strand"></div>
            <div class="seaweed-strand"></div>
          </div>
          
          <div class="static-seaweed seaweed-2">
            <div class="seaweed-strand"></div>
            <div class="seaweed-strand"></div>
          </div>
          
          <!-- Static Jellyfish -->
          <div class="static-jellyfish jellyfish-1">
            <div class="jellyfish-head"></div>
            <div class="jellyfish-tentacles">
              <div class="tentacle"></div>
              <div class="tentacle"></div>
              <div class="tentacle"></div>
              <div class="tentacle"></div>
              <div class="tentacle"></div>
            </div>
          </div>
          
          <!-- Static Sea floor -->
          <div class="static-sea-floor">
            <div class="sand-dune sand-dune-1"></div>
            <div class="sand-dune sand-dune-2"></div>
            <div class="sand-dune sand-dune-3"></div>
          </div>
        </template>
        
        <!-- Cyberpunk theme static elements -->
        <template v-else-if="theme === 'cyberpunk'">
          <!-- Static Rain Effect -->
          <div class="static-cyber-rain">
            <div v-for="i in 10" :key="`rain-${i}`" class="static-rain-drop"></div>
          </div>
          
          <!-- Static Neon Signs -->
          <div class="static-neon-sign neon-sign-1">DIGITAL DREAMS</div>
          <div class="static-neon-sign neon-sign-2">NEURAL LINK</div>
          <div class="static-neon-sign neon-sign-3">CYBER ZONE</div>
          
          <!-- Static Grid lines -->
          <div class="static-grid-container">
            <div class="grid-horizontal" v-for="i in 6" :key="`h-${i}`"></div>
            <div class="grid-vertical" v-for="i in 6" :key="`v-${i}`"></div>
          </div>
          
          <!-- Static City Silhouette -->
          <div class="static-cyber-city">
            <div v-for="i in 7" :key="`building-${i}`" class="static-city-building"></div>
          </div>
          
          <!-- Static Flying data cubes -->
          <div class="static-data-cube data-cube-1">
            <div class="cube-face"></div>
            <div class="cube-face"></div>
            <div class="cube-face"></div>
            <div class="cube-face"></div>
            <div class="cube-face"></div>
            <div class="cube-face"></div>
          </div>
          
          <div class="static-data-cube data-cube-2">
            <div class="cube-face"></div>
            <div class="cube-face"></div>
            <div class="cube-face"></div>
            <div class="cube-face"></div>
            <div class="cube-face"></div>
            <div class="cube-face"></div>
          </div>
          
          <!-- Static Data Stream -->
          <div class="static-data-stream data-stream-1"></div>
          <div class="static-data-stream data-stream-2"></div>
          <div class="static-data-stream data-stream-3"></div>
          
          <!-- Static Circuit paths -->
          <div class="static-circuit circuit-1">
            <div class="circuit-node" v-for="i in 3" :key="`circuit-1-node-${i}`"></div>
          </div>
          
          <div class="static-circuit circuit-2">
            <div class="circuit-node" v-for="i in 4" :key="`circuit-2-node-${i}`"></div>
          </div>
          
          <!-- Static Holographic displays -->
          <div class="static-hologram hologram-1">
            <div class="hologram-content">
              <div class="hologram-line" v-for="i in 3" :key="`hologram-1-line-${i}`"></div>
            </div>
          </div>
          
          <div class="static-hologram hologram-3">
            <div class="hologram-ring"></div>
            <div class="hologram-ring"></div>
          </div>
        </template>
  
        <!-- Forest theme static elements -->
        <template v-else-if="theme === 'forest'">
          <!-- Static Sunbeams -->
          <div class="static-sunbeam sunbeam-1"></div>
          <div class="static-sunbeam sunbeam-2"></div>
          <div class="static-sunbeam sunbeam-3"></div>
          
          <!-- Static Forest mist -->
          <div class="static-forest-mist forest-mist-1"></div>
          <div class="static-forest-mist forest-mist-2"></div>
          <div class="static-forest-mist forest-mist-3"></div>
          
          <!-- Static Falling leaves -->
          <div class="static-leaves-container">
            <div v-for="i in 8" :key="`leaf-${i}`" class="static-falling-leaf" :class="`leaf-type-${i % 4}`"></div>
          </div>
          
          <!-- Static Trees in background -->
          <div class="static-tree-layer tree-layer-bg">
            <div class="static-tree tree-bg-1">
              <div class="tree-trunk"></div>
              <div class="tree-canopy"></div>
            </div>
            <div class="static-tree tree-bg-2">
              <div class="tree-trunk"></div>
              <div class="tree-canopy"></div>
            </div>
            <div class="static-tree tree-bg-3">
              <div class="tree-trunk"></div>
              <div class="tree-canopy"></div>
            </div>
            <div class="static-tree tree-bg-4">
              <div class="tree-trunk"></div>
              <div class="tree-canopy"></div>
            </div>
            <div class="static-tree tree-bg-5">
              <div class="tree-trunk"></div>
              <div class="tree-canopy"></div>
            </div>
          </div>
          
          <!-- Static Trees in foreground -->
          <div class="static-tree-layer tree-layer-fg">
            <div class="static-tree tree-fg-1">
              <div class="tree-trunk"></div>
              <div class="tree-canopy"></div>
            </div>
            <div class="static-tree tree-fg-2">
              <div class="tree-trunk"></div>
              <div class="tree-canopy"></div>
            </div>
          </div>
          
          <!-- Static Butterflies -->
          <div class="static-butterfly butterfly-1">
            <div class="butterfly-wing wing-left"></div>
            <div class="butterfly-wing wing-right"></div>
          </div>
          <div class="static-butterfly butterfly-2">
            <div class="butterfly-wing wing-left"></div>
            <div class="butterfly-wing wing-right"></div>
          </div>
          
          <!-- Static Birds -->
          <div class="static-bird bird-1"></div>
          <div class="static-bird bird-2"></div>
          
          <!-- Static Flowers and mushrooms -->
          <div class="static-forest-floor">
            <div class="static-mushroom mushroom-1">
              <div class="mushroom-cap"></div>
              <div class="mushroom-stem"></div>
            </div>
            <div class="static-mushroom mushroom-2">
              <div class="mushroom-cap"></div>
              <div class="mushroom-stem"></div>
            </div>
            
            <div class="static-flower flower-1">
              <div class="flower-center"></div>
              <div class="flower-petal"></div>
              <div class="flower-petal"></div>
              <div class="flower-petal"></div>
              <div class="flower-petal"></div>
              <div class="flower-petal"></div>
              <div class="flower-stem"></div>
            </div>
            <div class="static-flower flower-2">
              <div class="flower-center"></div>
              <div class="flower-petal"></div>
              <div class="flower-petal"></div>
              <div class="flower-petal"></div>
              <div class="flower-petal"></div>
              <div class="flower-petal"></div>
              <div class="flower-stem"></div>
            </div>
            
            <!-- Static Grass and ferns -->
            <div class="static-grass-patch grass-patch-1">
              <div class="grass-blade" v-for="i in 8" :key="`grass-1-${i}`"></div>
            </div>
            <div class="static-grass-patch grass-patch-2">
              <div class="grass-blade" v-for="i in 10" :key="`grass-2-${i}`"></div>
            </div>
            
            <div class="static-fern fern-1">
              <div class="fern-stem"></div>
              <div class="fern-leaf fern-leaf-1"></div>
              <div class="fern-leaf fern-leaf-2"></div>
              <div class="fern-leaf fern-leaf-3"></div>
              <div class="fern-leaf fern-leaf-4"></div>
            </div>
          </div>
          
          <!-- Static Fireflies -->
          <div class="static-firefly-container">
            <div v-for="i in 10" :key="`firefly-${i}`" class="static-firefly"></div>
          </div>
        </template>
      </div>
    </div>
  </template>
    
  <script>
  export default {
    name: 'StaticBackgrounds',
    props: {
      // Available themes: 'cosmic', 'ocean', 'cyberpunk', 'forest'
      theme: {
        type: String,
        default: 'cosmic',
        validator: (value) => ['cosmic', 'ocean', 'cyberpunk', 'forest'].includes(value)
      }
    }
  };
  </script>
    
  <style scoped>
  /* Styles de base pour tous les arrière-plans statiques */
  .static-background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    overflow: hidden;
  }
  
  .static-elements {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    overflow: hidden;
    pointer-events: none;
    z-index: 1;
  }
  
  /* ======== COSMIC THEME STATIC STYLES ======== */
  .cosmic {
    background: radial-gradient(ellipse at center, #0f2027 0%, #090a0f 100%);
  }
  
  /* Static Stars Background */
  .cosmic .static-stars {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
      radial-gradient(1px 1px at 10% 30%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
      radial-gradient(1px 1px at 20% 70%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
      radial-gradient(1px 1px at 30% 40%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
      radial-gradient(1px 1px at 40% 80%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
      radial-gradient(1px 1px at 50% 20%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
      radial-gradient(1px 1px at 60% 60%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
      radial-gradient(1px 1px at 70% 10%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
      radial-gradient(1px 1px at 80% 50%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
      radial-gradient(1px 1px at 90% 90%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
      radial-gradient(2px 2px at 15% 25%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
      radial-gradient(2px 2px at 35% 65%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
      radial-gradient(2px 2px at 45% 35%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
      radial-gradient(2px 2px at 55% 75%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
      radial-gradient(2px 2px at 65% 15%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
      radial-gradient(2px 2px at 75% 55%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
      radial-gradient(2px 2px at 85% 85%, rgba(255, 255, 255, 0.8) 50%, transparent 100%);
    background-size: 200% 200%;
    opacity: 0.8;
  }
  
  /* Static Comets */
  .static-comet {
    position: absolute;
    width: 4px;
    height: 4px;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 50%;
    box-shadow: 
      0 0 20px 2px rgba(255, 255, 255, 0.6),
      0 0 40px 6px rgba(115, 215, 255, 0.4);
    z-index: 2;
  }
  
  .static-comet::after {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 120px;
    height: 2px;
    background: linear-gradient(to left, 
      rgba(255, 255, 255, 0.8), 
      rgba(160, 220, 255, 0.4), 
      transparent);
    transform: translateX(2px);
    border-radius: 100%;
  }
  
  .comet-1 { top: 15%; left: 10%; transform: rotate(15deg); }
  .comet-2 { top: 35%; left: 25%; width: 3px; height: 3px; transform: rotate(25deg); }
  .comet-3 { top: 62%; left: 50%; transform: rotate(-10deg); }
  
  /* Static Galaxy */
  .static-galaxy {
    position: absolute;
    width: 180px;
    height: 100px;
    top: 75%;
    left: 35%;
    background: radial-gradient(
      ellipse at center,
      rgba(220, 180, 255, 0.6) 0%,
      rgba(140, 100, 255, 0.4) 30%,
      rgba(70, 30, 180, 0.2) 60%,
      transparent 100%
    );
    border-radius: 50%;
    transform: rotate(-25deg) scale(1);
    filter: blur(5px);
    opacity: 0.7;
    z-index: 1;
  }
  
  .static-galaxy::before, .static-galaxy::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: 50%;
    background: 
      radial-gradient(ellipse at center, rgba(255, 255, 255, 0.1) 0%, transparent 60%),
      conic-gradient(
        transparent 0%,
        rgba(130, 90, 220, 0.1) 25%,
        transparent 50%,
        rgba(150, 100, 255, 0.1) 75%,
        transparent 100%
      );
  }
  
  /* Static Planets */
  .static-planet {
    position: absolute;
    border-radius: 50%;
    z-index: 3;
    box-shadow: inset -15px -15px 40px rgba(0, 0, 0, 0.5);
  }
  
  .planet-1 {
    width: 80px;
    height: 80px;
    top: 15%;
    right: 37%;
    background: radial-gradient(
      circle at 30% 30%,
      #7a4dbc 0%,
      #522b99 30%,
      #3c1777 60%,
      #2c1155 100%
    );
    box-shadow: 0 0 20px rgba(120, 70, 230, 0.3);
    transform: rotate(-15deg);
  }
  
  .planet-1 .planet-rings {
    position: absolute;
    width: 130px;
    height: 20px;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) rotate(-15deg);
    border-radius: 50%;
    box-shadow: 
      0 0 0 4px rgba(255, 255, 255, 0.05),
      0 0 0 8px rgba(255, 255, 255, 0.03),
      0 0 0 12px rgba(255, 220, 255, 0.05),
      0 0 0 16px rgba(180, 180, 255, 0.08),
      0 0 0 20px rgba(140, 140, 230, 0.06),
      0 0 0 24px rgba(100, 100, 200, 0.04),
      0 0 0 28px rgba(80, 80, 180, 0.02);
    z-index: 2;
  }
  
  .planet-2 {
    width: 100px;
    height: 100px;
    top: 65%;
    right: 15%;
    background: radial-gradient(
      circle at 40% 40%,
      #ff6b5b 0%,
      #d32f2f 30%,
      #b71c1c 60%,
      #7f0000 100%
    );
    box-shadow: 0 0 30px rgba(255, 100, 80, 0.4);
    transform: rotate(10deg);
  }
  
  .planet-2 .planet-atmosphere {
    position: absolute;
    width: 110%;
    height: 110%;
    top: -5%;
    left: -5%;
    border-radius: 50%;
    background: radial-gradient(
      circle at 50% 50%,
      rgba(255, 107, 91, 0.3) 0%,
      rgba(211, 47, 47, 0.2) 50%,
      rgba(183, 28, 28, 0.1) 70%,
      rgba(127, 0, 0, 0) 100%
    );
    filter: blur(10px);
    opacity: 0.8;
    z-index: 1;
  }
  
  .planet-2 .planet-storm {
    position: absolute;
    width: 40%;
    height: 40%;
    top: 30%;
    left: 20%;
    border-radius: 50%;
    background: rgba(255, 160, 140, 0.4);
    filter: blur(5px);
    z-index: 2;
  }
  
  .planet-3 {
    width: 70px;
    height: 70px;
    top: 15%;
    left: 15%;
    background: radial-gradient(
      circle at 50% 50%,
      #b3e5fc 0%,
      #81d4fa 30%,
      #4fc3f7 60%,
      #29b6f6 100%
    );
    box-shadow: 0 0 25px rgba(79, 195, 247, 0.5);
  }
  
  .planet-3 .planet-ice-caps {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    border-radius: 50%;
    background: 
      radial-gradient(ellipse at 50% 10%, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0) 50%),
      radial-gradient(ellipse at 50% 90%, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0) 50%);
    z-index: 3;
  }
  
  .planet-3 .planet-moons {
    position: absolute;
    width: 100%;
    height: 100%;
    z-index: 1;
  }
  
  .planet-moon {
    position: absolute;
    border-radius: 50%;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
  }
  
  .moon-1 {
    width: 15px;
    height: 15px;
    top: -30px;
    left: 50%;
    transform: translateX(-50%);
    background: radial-gradient(
      circle at 30% 30%,
      #f5f5f5 0%,
      #e0e0e0 50%,
      #bdbdbd 100%
    );
  }
  
  .moon-2 {
    width: 10px;
    height: 10px;
    bottom: -25px;
    left: 30%;
    background: radial-gradient(
      circle at 30% 30%,
      #e0e0e0 0%,
      #bdbdbd 50%,
      #9e9e9e 100%
    );
  }
  
  /* ======== OCEAN THEME STATIC STYLES ======== */
  .ocean {
    background: radial-gradient(ellipse at center, #042843 0%, #010e1a 100%);
    overflow: hidden;
  }
  
  .ocean::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
      linear-gradient(0deg, rgba(0, 35, 75, 0.8) 0%, rgba(4, 40, 67, 0.4) 50%, rgba(10, 50, 90, 0.2) 100%),
      radial-gradient(ellipse at center, rgba(0, 30, 60, 0.2) 0%, rgba(4, 40, 67, 0.5) 70%, rgba(0, 35, 75, 0.7) 100%);
    opacity: 0.7;
    z-index: 0;
  }
  
  /* Static Shark */
  .static-shark {
    position: absolute;
    width: 220px;
    height: 80px;
    top: 35%;
    right: 30%;
    z-index: 4;
    transform-style: preserve-3d;
  }
  
  .shark-body {
    position: absolute;
    width: 150px;
    height: 60px;
    left: 20px;
    top: 10px;
    background: linear-gradient(to bottom,
      #2c3e50 0%,
      #34495e 40%,
      #7f8c8d 80%,
      #ecf0f1 100%);
    border-radius: 80% 40% 40% 80% / 50%;
    z-index: 2;
    transform-origin: center;
  }
  
  .shark-eye {
    position: absolute;
    width: 10px;
    height: 10px;
    background: #000;
    border-radius: 50%;
    top: 15px;
    left: 30px;
    z-index: 3;
  }
  
  .shark-eye-shine {
    width: 4px;
    height: 4px;
    background: #fff;
    left: 33px;
    top: 13px;
    opacity: 0.7;
  }
  
  .shark-gill {
    position: absolute;
    width: 2px;
    height: 15px;
    background: rgba(0, 0, 0, 0.2);
    transform: rotate(15deg);
    z-index: 3;
  }
  
  .gill-1 { top: 20px; left: 50px; }
  .gill-2 { top: 20px; left: 55px; }
  .gill-3 { top: 20px; left: 60px; }
  
  .shark-mouth {
    position: absolute;
    width: 30px;
    height: 5px;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 50%;
    transform: rotate(-5deg);
    top: 30px;
    left: 10px;
  }
  
  .shark-dorsal-fin {
    position: absolute;
    width: 50px;
    height: 40px;
    background: #2c3e50;
    top: -35px;
    left: 80px;
    clip-path: polygon(0 100%, 60% 0, 100% 100%);
    z-index: 1;
  }
  
  .shark-pectoral-fin {
    position: absolute;
    width: 40px;
    height: 30px;
    background: #34495e;
    transform-origin: top left;
    top: 40px;
    left: 70px;
    clip-path: polygon(0 0, 100% 30%, 80% 100%, 0 70%);
    z-index: 1;
    transform: rotate(10deg);
  }

  .shark-pelvic-fin {
    position: absolute;
    width: 25px;
    height: 20px;
    background: #34495e;
    transform-origin: top left;
    top: 45px;
    left: 110px;
    clip-path: polygon(0 0, 100% 30%, 80% 100%, 0 70%);
    z-index: 1;
    transform: rotate(5deg);
  }

  .shark-tail {
    position: absolute;
    width: 60px;
    height: 50px;
    top: 15px;
    right: 0;
    z-index: 2;
    transform: rotate(0deg);
  }

  .shark-tail-fin {
    position: absolute;
    width: 60px;
    height: 50px;
    background: #34495e;
    clip-path: polygon(0 40%, 50% 0, 50% 100%, 0 60%);
  }

  .shark-shadow {
    position: absolute;
    width: 180px;
    height: 60px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 50%;
    top: 85px;
    left: 30px;
    filter: blur(10px);
    transform: scaleX(1.2);
    z-index: 1;
    opacity: 0.5;
  }

  /* Static Light Rays */
  .static-light-ray {
    position: absolute;
    top: -30%;
    width: 150px;
    height: 150%;
    background: linear-gradient(to bottom, 
      rgba(255, 255, 255, 0.6) 0%, 
      rgba(255, 255, 255, 0.3) 40%, 
      rgba(255, 255, 255, 0.1) 70%, 
      transparent 100%);
    transform-origin: top center;
    filter: blur(15px);
    opacity: 0.4;
    z-index: 2;
  }

  .light-ray-1 { left: 25%; transform: rotate(20deg) translateX(-50%); }
  .light-ray-2 { left: 60%; transform: rotate(-15deg) translateX(-50%); }
  .light-ray-3 { left: 80%; width: 100px; transform: rotate(-25deg) translateX(-50%); }

  /* Static Bubbles */
  .static-bubble {
    position: absolute;
    border-radius: 50%;
    background: radial-gradient(
      circle at 30% 30%,
      rgba(255, 255, 255, 0.9) 0%,
      rgba(173, 216, 230, 0.6) 30%,
      rgba(173, 216, 230, 0.2) 60%,
      transparent 100%
    );
    box-shadow: 0 0 10px rgba(173, 216, 230, 0.5), inset 0 0 10px rgba(255, 255, 255, 0.5);
    z-index: 3;
    backdrop-filter: blur(2px);
  }

  .static-bubble::after {
    content: '';
    position: absolute;
    top: 20%;
    left: 20%;
    width: 25%;
    height: 25%;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.7);
    filter: blur(1px);
  }

  /* Définition des tailles et positions des bulles */
  .bubble-1 { width: 30px; height: 30px; left: 20%; bottom: 70%; }
  .bubble-2 { width: 20px; height: 20px; left: 35%; bottom: 40%; }
  .bubble-3 { width: 40px; height: 40px; left: 55%; bottom: 60%; }
  .bubble-4 { width: 15px; height: 15px; left: 70%; bottom: 50%; }
  .bubble-5 { width: 25px; height: 25px; left: 85%; bottom: 30%; }
  .bubble-6 { width: 35px; height: 35px; left: 45%; bottom: 20%; }

  /* Static Plankton */
  .static-plankton-container {
    position: absolute;
    width: 100%;
    height: 100%;
    z-index: 2;
  }

  .static-plankton {
    position: absolute;
    width: 2px;
    height: 2px;
    background: rgba(210, 230, 255, 0.6);
    border-radius: 50%;
    filter: blur(1px);
  }

  .static-plankton:nth-child(4n+1) { background: rgba(180, 220, 255, 0.5); }
  .static-plankton:nth-child(4n+2) { background: rgba(150, 210, 255, 0.4); }
  .static-plankton:nth-child(4n+3) { background: rgba(120, 200, 255, 0.6); }

  /* Static Coral */
  .static-coral {
    position: absolute;
    bottom: 0;
    z-index: 2;
  }

  .static-coral.coral-1 {
    width: 150px;
    height: 120px;
    right: 10%;
  }

  .static-coral.coral-2 {
    width: 180px;
    height: 150px;
    left: 5%;
  }

  .static-coral .coral-branch {
    position: absolute;
    bottom: 0;
    border-radius: 50% 50% 0 0;
    filter: blur(1px);
  }

  .coral-1 .branch-1,
  .coral-1 .branch-2,
  .coral-1 .branch-3 {
    background: linear-gradient(to top, 
      rgba(255, 80, 80, 0.8) 0%, 
      rgba(255, 127, 80, 0.7) 50%, 
      rgba(255, 127, 80, 0.3) 100%);
  }

  .coral-2 .branch-1,
  .coral-2 .branch-2 {
    background: linear-gradient(to top, 
      rgba(200, 100, 255, 0.8) 0%, 
      rgba(180, 120, 255, 0.7) 50%, 
      rgba(160, 140, 255, 0.3) 100%);
  }

  /* Positions des branches de corail */
  .coral-1 .branch-1 { width: 40px; height: 100px; left: 20px; transform: rotate(-5deg); }
  .coral-1 .branch-2 { width: 60px; height: 120px; left: 70px; transform: rotate(5deg); }
  .coral-1 .branch-3 { width: 50px; height: 90px; left: 40px; transform: rotate(0deg); }

  .coral-2 .branch-1 { width: 70px; height: 130px; left: 30px; transform: rotate(0deg); }
  .coral-2 .branch-2 { width: 50px; height: 100px; left: 100px; transform: rotate(-5deg); }

  /* Static Fish Schools */
  .static-fish-school {
    position: absolute;
    width: 200px;
    height: 100px;
    z-index: 3;
  }

  .static-fish-school.fish-school-1 {
    top: 25%;
    left: 30%;
  }

  .static-fish-school.fish-school-2 {
    top: 55%;
    left: 60%;
  }

  .static-school-fish {
    position: absolute;
    width: 15px;
    height: 8px;
    border-radius: 50% 60% 60% 50% / 50%;
    transform: skew(-30deg);
  }

  .fish-school-1 .static-school-fish { background: rgba(100, 180, 255, 0.7); }
  .fish-school-2 .static-school-fish { background: rgba(180, 210, 255, 0.7); }

  /* Positions des poissons dans les bancs */
  .fish-school-1 .static-school-fish:nth-child(1) { top: 10%; left: 20%; }
  .fish-school-1 .static-school-fish:nth-child(2) { top: 40%; left: 30%; }
  .fish-school-1 .static-school-fish:nth-child(3) { top: 70%; left: 25%; }
  .fish-school-1 .static-school-fish:nth-child(4) { top: 25%; left: 60%; }
  .fish-school-1 .static-school-fish:nth-child(5) { top: 55%; left: 70%; }

  .fish-school-2 .static-school-fish:nth-child(1) { top: 20%; left: 10%; }
  .fish-school-2 .static-school-fish:nth-child(2) { top: 50%; left: 20%; }
  .fish-school-2 .static-school-fish:nth-child(3) { top: 80%; left: 15%; }
  .fish-school-2 .static-school-fish:nth-child(4) { top: 35%; left: 50%; }
  .fish-school-2 .static-school-fish:nth-child(5) { top: 65%; left: 60%; }
  .fish-school-2 .static-school-fish:nth-child(6) { top: 25%; left: 70%; }
  .fish-school-2 .static-school-fish:nth-child(7) { top: 55%; left: 40%; }

  /* Static Individual Fish */
  .static-fish {
    position: absolute;
    z-index: 3;
    border-radius: 70% 30% 30% 70% / 50%;
  }

  .static-fish.fish-1 {
    width: 40px;
    height: 20px;
    top: 30%;
    left: 15%;
    background: linear-gradient(to right, 
      rgba(50, 150, 255, 0.9) 0%, 
      rgba(0, 191, 255, 0.8) 60%, 
      rgba(0, 191, 255, 0.4) 100%);
  }

  .static-fish.fish-2 {
    width: 30px;
    height: 15px;
    top: 45%;
    left: 75%;
    background: linear-gradient(to right, 
      rgba(255, 165, 0, 0.9) 0%, 
      rgba(255, 165, 0, 0.8) 60%, 
      rgba(255, 165, 0, 0.4) 100%);
  }

  .static-fish.fish-3 {
    width: 50px;
    height: 25px;
    top: 60%;
    left: 40%;
    background: linear-gradient(to right, 
      rgba(255, 105, 180, 0.9) 0%, 
      rgba(255, 105, 180, 0.8) 60%, 
      rgba(255, 105, 180, 0.4) 100%);
  }

  .static-fish .fish-tail {
    position: absolute;
    width: 15px;
    height: 100%;
    top: 0;
    right: -8px;
    background: inherit;
    border-radius: 0 50% 50% 0 / 50%;
    transform: rotate(0deg);
  }

  /* Static Seaweed */
  .static-seaweed {
    position: absolute;
    z-index: 1;
    display: flex;
    justify-content: space-around;
    bottom: 0;
  }

  .static-seaweed.seaweed-1 { width: 100px; height: 150px; left: 15%; }
  .static-seaweed.seaweed-2 { width: 80px; height: 120px; left: 60%; }

  .static-seaweed .seaweed-strand {
    width: 18px;
    height: 100%;
    background: linear-gradient(to top, 
      rgba(34, 139, 34, 0.9) 0%, 
      rgba(50, 160, 50, 0.7) 50%, 
      rgba(70, 190, 70, 0.4) 100%);
    border-radius: 50% 50% 0 0;
    position: relative;
    transform: rotate(0deg);
  }

  .static-seaweed .seaweed-strand::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
      radial-gradient(circle at 50% 15%, rgba(220, 255, 220, 0.3) 0%, transparent 20%),
      radial-gradient(circle at 50% 35%, rgba(220, 255, 220, 0.3) 0%, transparent 20%),
      radial-gradient(circle at 50% 55%, rgba(220, 255, 220, 0.3) 0%, transparent 20%),
      radial-gradient(circle at 50% 75%, rgba(220, 255, 220, 0.3) 0%, transparent 20%);
    border-radius: 50% 50% 0 0;
  }

  /* Positionnement des strands */
  .seaweed-1 .seaweed-strand:nth-child(1) { transform: rotate(-5deg); }
  .seaweed-1 .seaweed-strand:nth-child(2) { transform: rotate(5deg); }
  .seaweed-1 .seaweed-strand:nth-child(3) { transform: rotate(0deg); }
  .seaweed-2 .seaweed-strand:nth-child(1) { transform: rotate(3deg); }
  .seaweed-2 .seaweed-strand:nth-child(2) { transform: rotate(-3deg); }

  /* Static Jellyfish */
  .static-jellyfish {
    position: absolute;
    z-index: 3;
  }

  .static-jellyfish.jellyfish-1 {
    top: 20%;
    right: 20%;
  }

  .static-jellyfish .jellyfish-head {
    width: 50px;
    height: 40px;
    background: radial-gradient(
      ellipse at 50% 40%, 
      rgba(255, 100, 255, 0.8) 0%, 
      rgba(200, 100, 255, 0.6) 50%, 
      rgba(150, 100, 255, 0.4) 100%);
    border-radius: 50% 50% 45% 45%;
    box-shadow: 0 0 15px rgba(200, 150, 255, 0.5);
  }

  .static-jellyfish .jellyfish-tentacles {
    position: absolute;
    top: 35px;
    left: 50%;
    transform: translateX(-50%);
    width: 40px;
    height: 60px;
  }

  .static-jellyfish .tentacle {
    position: absolute;
    top: 0;
    width: 4px;
    height: 50px;
    background: linear-gradient(to bottom, 
      rgba(255, 100, 255, 0.8) 0%, 
      rgba(200, 100, 255, 0.5) 50%, 
      rgba(150, 100, 255, 0.2) 100%);
    border-radius: 4px;
  }

  .tentacle:nth-child(1) { left: 10%; transform: rotate(5deg); }
  .tentacle:nth-child(2) { left: 30%; transform: rotate(-5deg); }
  .tentacle:nth-child(3) { left: 50%; transform: rotate(0deg); }
  .tentacle:nth-child(4) { left: 70%; transform: rotate(5deg); }
  .tentacle:nth-child(5) { left: 90%; transform: rotate(-5deg); }

  /* Static Sea Floor */
  .static-sea-floor {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 30px;
    z-index: 1;
  }

  .static-sea-floor .sand-dune {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 30px;
    background: linear-gradient(to bottom, 
      rgba(210, 180, 140, 0.6) 0%, 
      rgba(210, 180, 140, 0.8) 100%);
    border-radius: 50% 50% 0 0;
  }

  .sand-dune-1 { left: 0; height: 35px; }
  .sand-dune-2 { left: 30%; height: 25px; }
  .sand-dune-3 { left: 70%; height: 30px; }

  /* ======== CYBERPUNK THEME STATIC STYLES ======== */
  .cyberpunk {
    background: linear-gradient(to bottom, #111a2e 0%, #0a0a1e 100%);
    overflow: hidden;
  }

  .cyberpunk::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
      linear-gradient(rgba(33, 33, 66, 0.2) 1px, transparent 1px),
      linear-gradient(90deg, rgba(33, 33, 66, 0.2) 1px, transparent 1px);
    background-size: 40px 40px;
    z-index: 1;
  }

  .cyberpunk::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(
      ellipse at center,
      rgba(0, 0, 0, 0) 0%,
      rgba(0, 0, 0, 0.5) 100%
    );
    pointer-events: none;
    z-index: 2;
  }

  /* Static Rain Effect */
  .static-cyber-rain {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    z-index: 3;
    pointer-events: none;
  }

  .static-rain-drop {
    position: absolute;
    width: 1px;
    height: 30px;
    background: linear-gradient(to bottom, 
      rgba(0, 255, 255, 0) 0%, 
      rgba(0, 255, 255, 0.6) 50%, 
      rgba(0, 255, 255, 0) 100%);
  }

  .static-rain-drop:nth-child(3n) {
    background: linear-gradient(to bottom, 
      rgba(255, 0, 128, 0) 0%, 
      rgba(255, 0, 128, 0.5) 50%, 
      rgba(255, 0, 128, 0) 100%);
  }

  /* Positioning for raindrops */
  .static-rain-drop:nth-child(1) { top: 10%; left: 10%; }
  .static-rain-drop:nth-child(2) { top: 25%; left: 20%; }
  .static-rain-drop:nth-child(3) { top: 15%; left: 30%; }
  .static-rain-drop:nth-child(4) { top: 40%; left: 40%; }
  .static-rain-drop:nth-child(5) { top: 35%; left: 50%; }
  .static-rain-drop:nth-child(6) { top: 20%; left: 60%; }
  .static-rain-drop:nth-child(7) { top: 45%; left: 70%; }
  .static-rain-drop:nth-child(8) { top: 30%; left: 80%; }
  .static-rain-drop:nth-child(9) { top: 50%; left: 90%; }
  .static-rain-drop:nth-child(10) { top: 65%; left: 15%; }

  /* Static Neon Signs */
  .static-neon-sign {
    position: absolute;
    font-family: 'Orbitron', sans-serif;
    font-weight: bold;
    letter-spacing: 2px;
    z-index: 5;
  }

  .static-neon-sign.neon-sign-1 {
    top: 15%;
    right: 10%;
    font-size: 24px;
    color: #ff00ff;
    text-shadow: 
      0 0 5px #ff00ff, 
      0 0 10px #ff00ff, 
      0 0 15px #ff00ff, 
      0 0 20px #ff00ff;
  }

  .static-neon-sign.neon-sign-2 {
    top: 40%;
    left: 5%;
    font-size: 18px;
    color: #00ffff;
    text-shadow: 
      0 0 5px #00ffff, 
      0 0 10px #00ffff, 
      0 0 15px #00ffff, 
      0 0 20px #00ffff;
  }

  .static-neon-sign.neon-sign-3 {
    bottom: 15%;
    right: 40%;
    font-size: 20px;
    color: #ff8800;
    text-shadow: 
      0 0 5px #ff8800, 
      0 0 10px #ff8800, 
      0 0 15px #ff8800, 
      0 0 20px #ff8800;
  }

  /* Static Grid Container */
  .static-grid-container {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    perspective: 1000px;
    transform-style: preserve-3d;
    z-index: 3;
    transform: rotateX(60deg);
  }

  .static-grid-container .grid-horizontal, 
  .static-grid-container .grid-vertical {
    position: absolute;
    background: rgba(0, 255, 255, 0.15);
  }

  .static-grid-container .grid-horizontal {
    width: 200%;
    height: 1px;
    left: -50%;
  }

  .static-grid-container .grid-vertical {
    height: 200%;
    width: 1px;
    top: -50%;
  }

  .static-grid-container .grid-horizontal:nth-child(1) { top: 16.6%; }
  .static-grid-container .grid-horizontal:nth-child(2) { top: 33.2%; }
  .static-grid-container .grid-horizontal:nth-child(3) { top: 49.8%; }
  .static-grid-container .grid-horizontal:nth-child(4) { top: 66.4%; }
  .static-grid-container .grid-horizontal:nth-child(5) { top: 83%; }
  .static-grid-container .grid-horizontal:nth-child(6) { top: 99.6%; }

  .static-grid-container .grid-vertical:nth-child(7) { left: 16.6%; }
  .static-grid-container .grid-vertical:nth-child(8) { left: 33.2%; }
  .static-grid-container .grid-vertical:nth-child(9) { left: 49.8%; }
  .static-grid-container .grid-vertical:nth-child(10) { left: 66.4%; }
  .static-grid-container .grid-vertical:nth-child(11) { left: 83%; }
  .static-grid-container .grid-vertical:nth-child(12) { left: 99.6%; }

  .static-grid-container .grid-horizontal:nth-child(odd), 
  .static-grid-container .grid-vertical:nth-child(odd) {
    background: rgba(255, 0, 128, 0.15);
    box-shadow: 0 0 15px rgba(255, 0, 128, 0.5);
  }

  /* Static City Silhouette */
  .static-cyber-city {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 25%;
    z-index: 2;
    display: flex;
    justify-content: stretch;
    align-items: flex-end;
  }

  .static-city-building {
    position: relative;
    bottom: 0;
    width: calc(100% / 8);
    background: linear-gradient(to top, 
      rgba(0, 0, 20, 0.9) 0%, 
      rgba(20, 20, 40, 0.8) 100%);
  }

  .static-city-building::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: linear-gradient(to bottom, 
      transparent 85%, 
      rgba(0, 255, 255, 0.3) 85.5%, 
      transparent 86%,
      transparent 92%, 
      rgba(255, 0, 128, 0.3) 92.5%, 
      transparent 93%);
    background-size: 100% 20px;
  }

  /* Heights for buildings */
  .static-city-building:nth-child(1) { height: 65%; }
  .static-city-building:nth-child(2) { height: 85%; }
  .static-city-building:nth-child(3) { height: 70%; }
  .static-city-building:nth-child(4) { height: 90%; }
  .static-city-building:nth-child(5) { height: 60%; }
  .static-city-building:nth-child(6) { height: 80%; }
  .static-city-building:nth-child(7) { height: 75%; }

  /* Static Data Cubes */
  .static-data-cube {
    position: absolute;
    width: 40px;
    height: 40px;
    transform-style: preserve-3d;
    z-index: 4;
    transform: rotateY(45deg) rotateX(45deg);
  }

  .static-data-cube.data-cube-1 {
    top: 30%;
    left: 20%;
  }

  .static-data-cube.data-cube-2 {
    top: 50%;
    right: 20%;
  }

  .static-data-cube .cube-face {
    position: absolute;
    width: 40px;
    height: 40px;
    background: rgba(255, 0, 128, 0.2);
    border: 1px solid rgba(255, 0, 128, 0.8);
    box-shadow: 0 0 20px rgba(255, 0, 128, 0.5);
  }

  .static-data-cube:nth-child(even) .cube-face {
    background: rgba(0, 255, 255, 0.2);
    border: 1px solid rgba(0, 255, 255, 0.8);
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
  }

  /* Cube face positioning */
  .static-data-cube .cube-face:nth-child(1) { transform: translateZ(20px); }
  .static-data-cube .cube-face:nth-child(2) { transform: rotateX(180deg) translateZ(20px); }
  .static-data-cube .cube-face:nth-child(3) { transform: rotateY(90deg) translateZ(20px); }
  .static-data-cube .cube-face:nth-child(4) { transform: rotateY(-90deg) translateZ(20px); }
  .static-data-cube .cube-face:nth-child(5) { transform: rotateX(90deg) translateZ(20px); }
  .static-data-cube .cube-face:nth-child(6) { transform: rotateX(-90deg) translateZ(20px); }

  /* Static Data Stream */
  .static-data-stream {
    position: absolute;
    height: 3px;
    background: linear-gradient(to right, 
      rgba(0, 255, 255, 0) 0%, 
      rgba(0, 255, 255, 0.8) 50%, 
      rgba(0, 255, 255, 0) 100%);
    z-index: 3;
  }

  .static-data-stream.data-stream-1 {
    width: 60%;
    top: 25%;
    left: 10%;
    transform: rotate(10deg);
  }

  .static-data-stream.data-stream-2 {
    width: 40%;
    top: 45%;
    right: 5%;
    transform: rotate(-15deg);
  }

  .static-data-stream.data-stream-3 {
    width: 70%;
    bottom: 35%;
    left: 15%;
    transform: rotate(5deg);
  }

  /* Static Circuits */
  .static-circuit {
    position: absolute;
    height: 2px;
    background: linear-gradient(to right, 
      rgba(0, 255, 255, 0) 0%, 
      rgba(0, 255, 255, 1) 50%, 
      rgba(0, 255, 255, 0) 100%);
    z-index: 3;
  }

  .static-circuit.circuit-1 {
    width: 30%;
    top: 20%;
    left: 10%;
    transform: rotate(30deg);
  }

  .static-circuit.circuit-2 {
    width: 40%;
    bottom: 30%;
    right: 5%;
    transform: rotate(-15deg);
  }

  .static-circuit .circuit-node {
    position: absolute;
    width: 6px;
    height: 6px;
    background: rgba(0, 255, 255, 0.8);
    border-radius: 50%;
    top: 50%;
    transform: translateY(-50%);
    box-shadow: 0 0 8px rgba(0, 255, 255, 0.8);
  }

  /* Circuit node positioning */
  .circuit-1 .circuit-node:nth-child(1) { left: 10%; }
  .circuit-1 .circuit-node:nth-child(2) { left: 50%; }
  .circuit-1 .circuit-node:nth-child(3) { left: 90%; }

  .circuit-2 .circuit-node:nth-child(1) { left: 5%; }
  .circuit-2 .circuit-node:nth-child(2) { left: 35%; }
  .circuit-2 .circuit-node:nth-child(3) { left: 65%; }
  .circuit-2 .circuit-node:nth-child(4) { left: 95%; }

  /* Static Holograms */
  .static-hologram {
    position: absolute;
    border-radius: 5px;
    z-index: 4;
    box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
  }

  .static-hologram.hologram-1 {
    width: 120px;
    height: 80px;
    top: 30%;
    right: 15%;
  }

  .static-hologram.hologram-3 {
    width: 100px;
    height: 100px;
    top: 15%;
    left: 40%;
  }

  .static-hologram .hologram-content {
    width: 100%;
    height: 100%;
    background: rgba(0, 255, 255, 0.1);
    border: 1px solid rgba(0, 255, 255, 0.5);
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    padding: 10px;
    box-sizing: border-box;
  }

  .static-hologram .hologram-line {
    height: 2px;
    background: rgba(0, 255, 255, 0.5);
  }

  .static-hologram .hologram-ring {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    border: 1px solid rgba(0, 255, 255, 0.5);
  }

  .hologram-3 .hologram-ring:nth-child(1) { width: 40%; height: 40%; }
  .hologram-3 .hologram-ring:nth-child(2) { width: 70%; height: 70%; }

  /* ======== FOREST THEME STATIC STYLES ======== */
  .forest {
    background: linear-gradient(to bottom, #123519 0%, #071b0c 100%);
    overflow: hidden;
  }

  .forest::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
      radial-gradient(circle at 50% 100%, rgba(20, 70, 30, 0.6) 0%, rgba(5, 30, 10, 0.2) 70%),
      linear-gradient(rgba(5, 25, 10, 0.5) 0%, rgba(10, 40, 20, 0.3) 100%);
    z-index: 0;
  }

  /* Static Sunbeams */
  .static-sunbeam {
    position: absolute;
    top: -20%;
    width: 80px;
    height: 150%;
    background: linear-gradient(to bottom, 
      rgba(255, 255, 200, 0.7) 0%, 
      rgba(255, 255, 200, 0.4) 30%, 
      rgba(255, 255, 200, 0.1) 70%, 
      transparent 100%);
    transform-origin: top center;
    filter: blur(10px);
    opacity: 0.4;
    z-index: 2;
  }

  .static-sunbeam.sunbeam-1 { left: 25%; transform: rotate(20deg) translateX(-50%); }
  .static-sunbeam.sunbeam-2 { left: 60%; transform: rotate(-15deg) translateX(-50%); }
  .static-sunbeam.sunbeam-3 { left: 80%; width: 60px; transform: rotate(-25deg) translateX(-50%); }

  /* Static Forest Mist */
  .static-forest-mist {
    position: absolute;
    height: 40%;
    width: 100%;
    background: radial-gradient(
      ellipse at center,
      rgba(255, 255, 255, 0.15) 0%,
      rgba(255, 255, 255, 0.05) 60%,
      transparent 100%
    );
    filter: blur(15px);
    z-index: 2;
  }

  .static-forest-mist.forest-mist-1 { bottom: 25%; left: -10%; height: 20%; }
  .static-forest-mist.forest-mist-2 { bottom: 5%; left: 30%; height: 15%; }
  .static-forest-mist.forest-mist-3 { bottom: 15%; left: -20%; height: 30%; }

  /* Static Falling Leaves */
  .static-leaves-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 4;
    pointer-events: none;
  }

  .static-falling-leaf {
    position: absolute;
    width: 25px;
    height: 25px;
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    opacity: 0.8;
  }

  /* Leaf types */
  .static-falling-leaf.leaf-type-0 {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath fill='%2374a12e' d='M50,0 C60,30 80,50 100,50 C80,60 60,80 50,100 C40,80 20,60 0,50 C20,50 40,30 50,0'/%3E%3C/svg%3E");
  }

  .static-falling-leaf.leaf-type-1 {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath fill='%2392b93b' d='M20,0 C60,15 80,40 100,50 C80,70 60,90 50,100 C25,90 10,70 0,50 C10,35 15,15 20,0'/%3E%3C/svg%3E");
  }

  .static-falling-leaf.leaf-type-2 {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath fill='%235a8a23' d='M50,0 C70,20 90,40 100,50 C70,70 60,90 50,100 C40,80 20,60 0,50 C10,40 30,20 50,0'/%3E%3C/svg%3E");
  }

  .static-falling-leaf.leaf-type-3 {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath fill='%23aec74a' d='M30,0 C60,20 90,30 100,50 C90,70 70,90 50,100 C30,70 10,40 0,50 C20,30 25,10 30,0'/%3E%3C/svg%3E");
  }

  /* Leaf positioning */
  .static-falling-leaf:nth-child(1) { top: 10%; left: 10%; transform: rotate(45deg) scale(0.8); }
  .static-falling-leaf:nth-child(2) { top: 15%; left: 25%; transform: rotate(15deg) scale(0.6); }
  .static-falling-leaf:nth-child(3) { top: 25%; left: 40%; transform: rotate(-30deg) scale(0.7); }
  .static-falling-leaf:nth-child(4) { top: 30%; left: 75%; transform: rotate(60deg) scale(0.9); }
  .static-falling-leaf:nth-child(5) { top: 50%; left: 15%; transform: rotate(-15deg) scale(0.5); }
  .static-falling-leaf:nth-child(6) { top: 60%; left: 50%; transform: rotate(25deg) scale(0.7); }
  .static-falling-leaf:nth-child(7) { top: 70%; left: 70%; transform: rotate(-45deg) scale(0.8); }
  .static-falling-leaf:nth-child(8) { top: 80%; left: 30%; transform: rotate(10deg) scale(0.6); }

  /* Static Tree Layers */
  .static-tree-layer {
    position: absolute;
    width: 100%;
    bottom: 0;
    left: 0;
    z-index: 2;
  }

  .static-tree-layer.tree-layer-bg {
    height: 70%;
    filter: blur(2px);
    opacity: 0.7;
    z-index: 1;
  }

  .static-tree-layer.tree-layer-fg {
    height: 85%;
    z-index: 3;
  }

  /* Static Trees */
  .static-tree {
    position: absolute;
    bottom: 0;
  }

  .static-tree .tree-trunk {
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    background: linear-gradient(to top, 
      #4d2b13 0%, 
      #6b3d1c 50%, 
      #5a331a 100%);
    border-radius: 10px 10px 0 0;
    z-index: 1;
  }

  .static-tree .tree-canopy {
    position: absolute;
    border-radius: 50%;
    z-index: 2;
  }

  /* Background trees */
  .static-tree.tree-bg-1 { left: 5%; height: 75%; width: 150px; }
  .static-tree.tree-bg-1 .tree-trunk { width: 18px; height: 30%; }
  .static-tree.tree-bg-1 .tree-canopy {
    width: 130px;
    height: 200px;
    bottom: 25%;
    left: 50%;
    transform: translateX(-50%);
    background: radial-gradient(
      ellipse at center,
      #5d982d 0%,
      #496c1e 70%,
      #3a5618 100%
    );
  }

  .static-tree.tree-bg-2 { left: 25%; height: 65%; width: 120px; }
  .static-tree.tree-bg-2 .tree-trunk { width: 15px; height: 35%; }
  .static-tree.tree-bg-2 .tree-canopy {
    width: 100px;
    height: 160px;
    bottom: 30%;
    left: 50%;
    transform: translateX(-50%);
    background: radial-gradient(
      ellipse at center,
      #6ba835 0%,
      #538029 70%,
      #3a5618 100%
    );
  }

  .static-tree.tree-bg-3 { left: 45%; height: 80%; width: 140px; }
  .static-tree.tree-bg-3 .tree-trunk { width: 20px; height: 25%; }
  .static-tree.tree-bg-3 .tree-canopy {
    width: 120px;
    height: 180px;
    bottom: 20%;
    left: 50%;
    transform: translateX(-50%);
    background: radial-gradient(
      ellipse at center,
      #4d8b2b 0%,
      #3a6a1f 70%,
      #2c4f18 100%
    );
  }

  .static-tree.tree-bg-4 { left: 65%; height: 70%; width: 130px; }
  .static-tree.tree-bg-4 .tree-trunk { width: 16px; height: 30%; }
  .static-tree.tree-bg-4 .tree-canopy {
    width: 110px;
    height: 150px;
    bottom: 30%;
    left: 50%;
    transform: translateX(-50%);
    background: radial-gradient(
      ellipse at center,
      #6ba835 0%,
      #538029 70%,
      #3a5618 100%
    );
  }

  .static-tree.tree-bg-5 { left: 85%; height: 75%; width: 140px; }
  .static-tree.tree-bg-5 .tree-trunk { width: 18px; height: 25%; }
  .static-tree.tree-bg-5 .tree-canopy {
    width: 120px;
    height: 200px;
    bottom: 25%;
    left: 50%;
    transform: translateX(-50%);
    background: radial-gradient(
      ellipse at center,
      #5d982d 0%,
      #496c1e 70%,
      #3a5618 100%
    );
  }

  /* Foreground trees */
  .static-tree.tree-fg-1 { left: 60%; height: 85%; width: 160px; }
  .static-tree.tree-fg-1 .tree-trunk { width: 20px; height: 35%; }
  .static-tree.tree-fg-1 .tree-canopy {
    width: 140px;
    height: 220px;
    bottom: 15%;
    left: 50%;
    transform: translateX(-50%);
    background: radial-gradient(
      ellipse at center,
      #4d8b2b 0%,
      #3a6a1f 70%,
      #2c4f18 100%
    );
  }

  .static-tree.tree-fg-2 { left: 30%; height: 70%; width: 150px; }
  .static-tree.tree-fg-2 .tree-trunk { width: 18px; height: 30%; }
  .static-tree.tree-fg-2 .tree-canopy {
    width: 130px;
    height: 200px;
    bottom: 25%;
    left: 50%;
    transform: translateX(-50%);
    background: radial-gradient(
      ellipse at center,
      #6ba835 0%,
      #538029 70%,
      #3a5618 100%
    );
  }

  /* Static Butterflies */
  .static-butterfly {
    position: absolute;
    width: 20px;
    height: 20px;
    z-index: 4;
  }

  .static-butterfly.butterfly-1 { top: 30%; left: 40%; }
  .static-butterfly.butterfly-2 { top: 45%; left: 65%; }

  .static-butterfly .butterfly-wing {
    position: absolute;
    width: 10px;
    height: 15px;
    border-radius: 100% 100% 0 100%;
    transform-origin: 100% 50%;
  }

  .butterfly-1 .butterfly-wing { background: linear-gradient(to bottom, #ff9933, #ffcc00); }
  .butterfly-2 .butterfly-wing { background: linear-gradient(to bottom, #66ccff, #99ffff); }

  .static-butterfly .wing-left {
    left: 0;
    transform: scaleX(-1) rotate(-30deg);
  }

  .static-butterfly .wing-right {
    right: 0;
    transform: rotate(30deg);
  }

  /* Static Birds */
  .static-bird {
    position: absolute;
    width: 30px;
    height: 8px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 30'%3E%3Cpath fill='%23333' d='M50,0 C40,0 25,15 0,20 C25,25 40,30 50,30 C60,30 75,25 100,20 C75,15 60,0 50,0'/%3E%3C/svg%3E");
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    z-index: 4;
  }

  .static-bird.bird-1 { top: 20%; left: 25%; }
  .static-bird.bird-2 { top: 15%; left: 70%; }

  /* Static Forest Floor */
  .static-forest-floor {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 20%;
    z-index: 3;
  }

  /* Static Mushrooms */
  .static-mushroom {
    position: absolute;
    bottom: 0;
    z-index: 4;
  }

  .static-mushroom.mushroom-1 { left: 38%; height: 40px; }
  .static-mushroom.mushroom-2 { left: 65%; height: 35px; }

  .static-mushroom .mushroom-cap {
    position: absolute;
    width: 30px;
    height: 15px;
    border-radius: 100% 100% 0 0;
    bottom: 15px;
    left: 50%;
    transform: translateX(-50%);
  }

  .static-mushroom .mushroom-stem {
    position: absolute;
    width: 10px;
    height: 20px;
    background: #f5e9d9;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    border-radius: 30% 30% 0 0;
  }

  .static-mushroom.mushroom-1 .mushroom-cap { background: linear-gradient(to bottom, #e05d5d, #b33f3f); }
  .static-mushroom.mushroom-2 .mushroom-cap { background: linear-gradient(to bottom, #e08a5d, #b36a3f); }

  /* Static Flowers */
  .static-flower {
    position: absolute;
    bottom: 0;
    z-index: 3;
  }

  .static-flower.flower-1 { left: 50%; height: 50px; }
  .static-flower.flower-2 { left: 75%; height: 45px; }

  .static-flower .flower-center {
    position: absolute;
    width: 10px;
    height: 10px;
    background: #ffd633;
    border-radius: 50%;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 2;
  }

  .static-flower .flower-petal {
    position: absolute;
    width: 12px;
    height: 15px;
    border-radius: 50%;
    bottom: 30px;
    left: 50%;
    transform-origin: center bottom;
    z-index: 1;
  }

  .static-flower .flower-petal:nth-child(2) { transform: translateX(-50%) rotate(0deg); }
  .static-flower .flower-petal:nth-child(3) { transform: translateX(-50%) rotate(72deg); }
  .static-flower .flower-petal:nth-child(4) { transform: translateX(-50%) rotate(144deg); }
  .static-flower .flower-petal:nth-child(5) { transform: translateX(-50%) rotate(216deg); }
  .static-flower .flower-petal:nth-child(6) { transform: translateX(-50%) rotate(288deg); }

  .static-flower .flower-stem {
    position: absolute;
    width: 3px;
    height: 30px;
    background: #5c9e31;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
  }

  .static-flower.flower-1 .flower-petal { background: linear-gradient(to bottom, #ff80bf, #ff1a8c); }
  .static-flower.flower-2 .flower-petal { background: linear-gradient(to bottom, #80bfff, #1a8cff); }

  /* Static Grass */
  .static-grass-patch {
    position: absolute;
    bottom: 0;
    width: 80px;
    height: 40px;
    z-index: 3;
  }

  .static-grass-patch.grass-patch-1 { left: 5%; }
  .static-grass-patch.grass-patch-2 { left: 30%; }

  .static-grass-patch .grass-blade {
    position: absolute;
    bottom: 0;
    width: 5px;
    height: 30px;
    background: linear-gradient(to top, #5c9e31, #7bc143);
    border-radius: 0 100% 0 0;
    transform-origin: bottom center;
  }

  /* Random grass blade angles */
  .grass-patch-1 .grass-blade:nth-child(1) { left: 10%; transform: rotate(-25deg); }
  .grass-patch-1 .grass-blade:nth-child(2) { left: 20%; transform: rotate(-15deg); }
  .grass-patch-1 .grass-blade:nth-child(3) { left: 30%; transform: rotate(5deg); }
  .grass-patch-1 .grass-blade:nth-child(4) { left: 40%; transform: rotate(-10deg); }
  .grass-patch-1 .grass-blade:nth-child(5) { left: 50%; transform: rotate(15deg); }
  .grass-patch-1 .grass-blade:nth-child(6) { left: 60%; transform: rotate(-5deg); }
  .grass-patch-1 .grass-blade:nth-child(7) { left: 70%; transform: rotate(10deg); }
  .grass-patch-1 .grass-blade:nth-child(8) { left: 80%; transform: rotate(-20deg); }

  .grass-patch-2 .grass-blade:nth-child(1) { left: 5%; transform: rotate(-10deg); }
  .grass-patch-2 .grass-blade:nth-child(2) { left: 15%; transform: rotate(20deg); }
  .grass-patch-2 .grass-blade:nth-child(3) { left: 25%; transform: rotate(-15deg); }
  .grass-patch-2 .grass-blade:nth-child(4) { left: 35%; transform: rotate(5deg); }
  .grass-patch-2 .grass-blade:nth-child(5) { left: 45%; transform: rotate(15deg); }
  .grass-patch-2 .grass-blade:nth-child(6) { left: 55%; transform: rotate(-25deg); }
  .grass-patch-2 .grass-blade:nth-child(7) { left: 65%; transform: rotate(0deg); }
  .grass-patch-2 .grass-blade:nth-child(8) { left: 75%; transform: rotate(10deg); }
  .grass-patch-2 .grass-blade:nth-child(9) { left: 85%; transform: rotate(-5deg); }
  .grass-patch-2 .grass-blade:nth-child(10) { left: 95%; transform: rotate(25deg); }

  /* Static Fern */
  .static-fern {
    position: absolute;
    bottom: 0;
    height: 60px;
    width: 50px;
    z-index: 3;
  }

  .static-fern.fern-1 { left: 40%; }

  .static-fern .fern-stem {
    position: absolute;
    width: 3px;
    height: 100%;
    background: #3a5618;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
  }

  .static-fern .fern-leaf {
    position: absolute;
    width: 20px;
    height: 10px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 50'%3E%3Cpath fill='%235c9e31' d='M0,0 C20,10 40,25 60,20 C80,15 90,0 100,0 C100,10 80,40 60,45 C40,50 20,30 0,50 L0,0'/%3E%3C/svg%3E");
    background-size: contain;
    background-repeat: no-repeat;
    left: 50%;
    transform-origin: left center;
  }

  .static-fern .fern-leaf-1 { top: 10%; transform: translateX(0) rotate(-30deg); }
  .static-fern .fern-leaf-2 { top: 30%; transform: translateX(0) rotate(-20deg); }
  .static-fern .fern-leaf-3 { top: 50%; transform: translateX(0) scaleX(-1) rotate(20deg); }
  .static-fern .fern-leaf-4 { top: 70%; transform: translateX(0) scaleX(-1) rotate(30deg); }

  /* Static Fireflies */
  .static-firefly-container {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    z-index: 5;
    pointer-events: none;
  }

  .static-firefly {
    position: absolute;
    width: 4px;
    height: 4px;
    background: #ffff99;
    border-radius: 50%;
    filter: blur(1px);
    box-shadow: 0 0 10px 2px rgba(255, 255, 153, 0.8);
  }

  /* Firefly positions */
  .static-firefly:nth-child(1) { top: 20%; left: 10%; }
  .static-firefly:nth-child(2) { top: 15%; left: 30%; }
  .static-firefly:nth-child(3) { top: 40%; left: 20%; }
  .static-firefly:nth-child(4) { top: 60%; left: 15%; }
  .static-firefly:nth-child(5) { top: 25%; left: 60%; }
  .static-firefly:nth-child(6) { top: 50%; left: 75%; }
  .static-firefly:nth-child(7) { top: 75%; left: 85%; }
  .static-firefly:nth-child(8) { top: 30%; left: 90%; }
  .static-firefly:nth-child(9) { top: 70%; left: 40%; }
  .static-firefly:nth-child(10) { top: 80%; left: 60%; }
</style>