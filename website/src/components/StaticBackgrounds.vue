<!-- StaticBackgrounds.vue -->
<template>
    <div class="static-background" :class="theme">
      <!-- Container for all static elements -->
      <div class="static-elements">
        <!-- Dynamic space elements based on the selected theme -->
        <template v-if="theme === 'cosmic'">
          <!-- Static Crowd of Stars -->
          <div class="static-crowd-container">
            <div v-for="i in 150" :key="`crowd-${i}`" class="static-crowd-dot" :style="getStaticCrowdDotStyle(i)"></div>
          </div>
          
          <!-- Static Comets -->
          <div class="static-comet comet-1"></div>
          <div class="static-comet comet-2"></div>
          <div class="static-comet comet-3"></div>
          <div class="static-comet comet-4"></div>
          <div class="static-cometInverse comet-5"></div>
          
          <!-- Static Galaxy -->
          <div class="static-galaxy galaxy-1"></div>
          
          <!-- Static Rocket -->
          <div class="static-rocket-container">
            <div class="static-rocket">
              <div class="rocket-body">
                <div class="rocket-window"></div>
              </div>
              <div class="rocket-nose"></div>
              <div class="rocket-fin rocket-fin-left"></div>
              <div class="rocket-fin rocket-fin-right"></div>
              <div class="rocket-flame-container">
                <div class="rocket-flame flame-core"></div>
                <div class="rocket-flame flame-outer-1"></div>
                <div class="rocket-flame flame-outer-2"></div>
              </div>
            </div>
          </div>

          <!-- Static Satellite -->
          <div class="static-satellite-container">
            <div class="static-satellite">
              <div class="satellite-body">
                <!-- Small details -->
              </div>
              <div class="solar-panels">
                <div class="solar-panel panel-left">
                  <div class="panel-cells"></div>
                </div>
                <div class="solar-panel panel-right">
                  <div class="panel-cells"></div>
                </div>
              </div>
              <div class="satellite-dish">
                <div class="dish-inner"></div>
              </div>
              <div class="satellite-antenna-small"></div>
            </div>
          </div>
          
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

          <!-- Planet 4: Gas Giant with Bands and Spot -->
          <div class="static-planet planet-4">
            <div class="planet-bands">
              <div class="band band-1"></div>
              <div class="band band-2"></div>
              <div class="band band-3"></div>
              <div class="band band-4"></div>
            </div>
            <div class="planet-great-spot"></div>
          </div>

          <!-- Planet 5: Rocky, Cratered Planet with Small Moon -->
          <div class="static-planet planet-5">
            <div class="planet-surface-texture"></div>
            <!-- Add multiple crater divs for detail -->
            <div class="crater crater-1"></div>
            <div class="crater crater-2"></div>
            <div class="crater crater-3"></div>
            <div class="planet-moons moons-p5">
              <div class="planet-moon moon-3"></div>
            </div>
          </div>

          <!-- Planet 6: Distant Icy Body -->
          <div class="static-planet planet-6">
            <div class="planet-haze"></div>
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

        <template v-else-if="theme === 'snow'">
          <!-- Base Sky & Stars -->
          <div class="static-snow-sky">
            <div class="static-stars-layer stars-far"></div>
            <div class="static-stars-layer stars-mid"></div>
            <!-- Optional Moon -->
            <div class="static-moon"></div>
          </div>

          <!-- Static Aurora Borealis -->
          <div class="static-aurora-borealis-container">
            <div class="static-aurora-ribbon ribbon-1"></div>
            <div class="static-aurora-ribbon ribbon-2"></div>
            <div class="static-aurora-ribbon ribbon-3"></div>
            <div class="static-aurora-ribbon ribbon-4"></div>
          </div>

          <!-- Static Mountain Layers -->
          <div class="static-mountains-distant">
            <div class="static-mountain-peak peak-distant-1"></div>
            <div class="static-mountain-peak peak-distant-2"></div>
          </div>
          <div class="static-mountains-mid">
            <div class="static-mountain-peak peak-mid-1">
              <div class="mountain-texture"></div>
            </div>
            <div class="static-mountain-peak peak-mid-2">
              <div class="mountain-texture"></div>
            </div>
            <div class="static-mountain-peak peak-mid-3">
              <div class="mountain-texture"></div>
            </div>
          </div>

          <!-- Static Forest Layers -->
          <div class="static-forest-layer-mid">
            <div v-for="i in 5" :key="`tree-mid-${i}`" class="static-pine-tree tree-mid" :style="getStaticTreeStyle(i, 'mid')">
              <div class="tree-trunk"></div>
              <div class="tree-branch branch-1"><div class="snow-on-branch"></div></div>
              <div class="tree-branch branch-2"><div class="snow-on-branch"></div></div>
              <div class="tree-branch branch-3"><div class="snow-on-branch"></div></div>
            </div>
          </div>

          <!-- Static Mist/Fog -->
          <div class="static-mist-container">
            <div class="static-mist-layer mist-1"></div>
            <div class="static-mist-layer mist-2"></div>
            <div class="static-mist-layer mist-3"></div>
          </div>

          <div class="static-mountains-near">
            <div class="static-mountain-peak peak-near-1">
              <div class="mountain-texture rock-texture"></div>
              <div class="mountain-texture snow-texture"></div>
            </div>
            <div class="static-mountain-peak peak-near-2">
              <div class="mountain-texture rock-texture"></div>
              <div class="mountain-texture snow-texture"></div>
            </div>
          </div>

          <!-- Static Animals -->
          <div class="static-polar-bear-container">
            <div class="static-polar-bear">
              <div class="polar-bear-body">
                <div class="polar-bear-head">
                  <div class="polar-bear-ear polar-bear-ear-left"></div>
                  <div class="polar-bear-ear polar-bear-ear-right"></div>
                  <div class="polar-bear-snout">
                    <div class="polar-bear-nose"></div>
                    <div class="polar-bear-mouth"></div>
                  </div>
                  <div class="polar-bear-eye polar-bear-eye-left">
                    <div class="polar-bear-eye-pupil"></div>
                  </div>
                  <div class="polar-bear-eye polar-bear-eye-right">
                    <div class="polar-bear-eye-pupil"></div>
                  </div>
                </div>
                <div class="polar-bear-torso">
                  <div class="polar-bear-fur-detail fur-detail-1"></div>
                  <div class="polar-bear-fur-detail fur-detail-2"></div>
                  <div class="polar-bear-fur-detail fur-detail-3"></div>
                </div>
                <div class="polar-bear-leg polar-bear-leg-front-left">
                  <div class="polar-bear-paw polar-bear-paw-front-left"></div>
                </div>
                <div class="polar-bear-leg polar-bear-leg-front-right">
                  <div class="polar-bear-paw polar-bear-paw-front-right"></div>
                </div>
                <div class="polar-bear-leg polar-bear-leg-back-left">
                  <div class="polar-bear-paw polar-bear-paw-back-left"></div>
                </div>
                <div class="polar-bear-leg polar-bear-leg-back-right">
                  <div class="polar-bear-paw polar-bear-paw-back-right"></div>
                </div>
              </div>
              <div class="polar-bear-shadow"></div>
            </div>
          </div>
          <div class="static-penguin-container">
            <div class="static-penguin">
              <div class="penguin-body">
                <div class="penguin-head">
                  <div class="penguin-face">
                    <div class="penguin-eye penguin-eye-left">
                      <div class="penguin-eye-pupil"></div>
                    </div>
                    <div class="penguin-eye penguin-eye-right">
                      <div class="penguin-eye-pupil"></div>
                    </div>
                    <div class="penguin-beak"></div>
                  </div>
                </div>
                <div class="penguin-belly"></div>
                <div class="penguin-wing penguin-wing-left"></div>
                <div class="penguin-wing penguin-wing-right"></div>
                <div class="penguin-foot penguin-foot-left"></div>
                <div class="penguin-foot penguin-foot-right"></div>
              </div>
              <div class="penguin-shadow"></div>
            </div>
          </div>

          <!-- Static Snow Ground/Terrain -->
          <div class="static-snow-ground">
            <div class="static-snow-drift drift-large-1"></div>
            <div class="static-snow-drift drift-medium-1"></div>
            <div class="static-snow-drift drift-small-1"></div>
            <div class="static-snow-drift drift-medium-2"></div>
            <div class="static-snow-drift drift-large-2"></div>
          </div>

          <div class="static-forest-layer-near">
            <div v-for="i in 4" :key="`tree-near-${i}`" class="static-pine-tree tree-near" :style="getStaticTreeStyle(i, 'near')">
              <div class="tree-trunk"></div>
              <div class="tree-branch branch-1"><div class="snow-on-branch"></div></div>
              <div class="tree-branch branch-2"><div class="snow-on-branch"></div></div>
              <div class="tree-branch branch-3"><div class="snow-on-branch"></div></div>
              <div class="tree-branch branch-4"><div class="snow-on-branch"></div></div>
            </div>
          </div>

          <!-- Static Snowfall Layers -->
          <div class="static-snowfall-layer-far">
            <div v-for="i in 10" :key="`snow-far-${i}`" class="static-snowflake snow-far" :style="getStaticSnowflakeStyle(i, 'far')"></div>
          </div>
          <div class="static-snowfall-layer-mid">
            <div v-for="i in 8" :key="`snow-mid-${i}`" class="static-snowflake snow-mid" :style="getStaticSnowflakeStyle(i, 'mid')"></div>
          </div>
          <div class="static-snowfall-layer-near">
            <div v-for="i in 6" :key="`snow-near-${i}`" class="static-snowflake snow-near" :style="getStaticSnowflakeStyle(i, 'near')"></div>
          </div>

          <!-- Static Vignette Overlay -->
          <div class="static-vignette-overlay"></div>
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
        validator: (value) => ['cosmic', 'ocean', 'cyberpunk', 'forest', 'snow'].includes(value)
      }
    },
    methods: {
      // Ajouter ces méthodes dans votre composant
      getStaticTreeStyle(index, layer) {
        const baseLeft = (index * (layer === 'near' ? 22 : 18)) + (layer === 'near' ? 5 : 10);
        const randomOffset = (index * 3) % 8 - 4; // Pseudo-aléatoire basé sur l'index
        const left = baseLeft + randomOffset;
        
        const baseScale = layer === 'near' ? 1 + (index % 2) * 0.1 : 0.7 + (index % 3) * 0.1;
        const heightVariation = layer === 'near' ? 80 + (index * 5) % 20 : 50 + (index * 3) % 15;
        
        return {
          left: `${left}%`,
          transform: `scale(${baseScale})`,
          height: `${heightVariation}%`,
          zIndex: layer === 'near' ? 8 : 4
        };
      },

      getStaticCrowdDotStyle(index) {
        const leftPosition = ((index * 7) % 100); // Deterministic positioning based on index
        const topPosition = ((index * 13) % 100); // Different multiplier for more variation
        const size = 1 + ((index % 3) * 0.5); // Sizes between 1px and 2.5px
        const opacity = 0.2 + ((index % 5) * 0.1); // Opacity between 0.2 and 0.6
        
        return {
          left: `${leftPosition}%`,
          top: `${topPosition}%`,
          width: `${size}px`,
          height: `${size}px`,
          opacity: opacity
        };
      },

      getStaticSnowflakeStyle(index, layer) {
        const left = ((index * 10) + (index * 3)) % 100;
        const top = ((index * 7) + 10) % 80;
        
        let scale, opacity, blur, zIndex;
        
        if (layer === 'near') {
          scale = 1 + (index % 5) * 0.1;
          opacity = 0.9;
          blur = '0px';
          zIndex = 18;
        } else if (layer === 'mid') {
          scale = 0.6 + (index % 4) * 0.1;
          opacity = 0.7;
          blur = '1px';
          zIndex = 16;
        } else { // far
          scale = 0.3 + (index % 3) * 0.1;
          opacity = 0.5;
          blur = '2px';
          zIndex = 14;
        }
        
        return {
          left: `${left}%`,
          top: `${top}%`,
          transform: `scale(${scale})`,
          opacity: opacity,
          filter: `blur(${blur})`,
          zIndex: zIndex
        };
      }
    },
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
  
  .static-crowd-container {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: 1;
  mask-image: radial-gradient(ellipse at center, black 60%, transparent 95%);
  -webkit-mask-image: radial-gradient(ellipse at center, black 60%, transparent 95%);
}

.static-crowd-dot {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.7);
  box-shadow: 0 0 3px rgba(255, 255, 255, 0.5);
}

/* Static CometInverse */
.static-cometInverse {
  position: absolute;
  width: 4px;
  height: 4px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  box-shadow: 0 0 20px 2px rgba(255, 255, 255, 0.6), 0 0 40px 6px rgba(115, 215, 255, 0.4);
  z-index: 2;
  transform: rotate(185deg);
}

.static-cometInverse::after {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 120px;
  height: 2px;
  background: linear-gradient(to left, rgba(255, 255, 255, 0.8), rgba(160, 220, 255, 0.4), transparent);
  transform: translateX(2px);
  border-radius: 100%;
}

/* Additional comets */
.static-comet.comet-4 { top: 62%; left: 40%; transform: rotate(-10deg); }
.static-cometInverse.comet-5 { top: 70%; left: 55%; }

/* Static Rocket */
.static-rocket-container {
  position: absolute;
  bottom: 20%;
  left: 15%;
  width: 80px;
  height: 150px;
  z-index: 10;
  transform: rotate(45deg);
  transform-origin: center bottom;
}

.static-rocket {
  position: relative;
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 0 15px rgba(255, 165, 0, 0.6));
}

.static-rocket .rocket-body {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 80px;
  background: linear-gradient(to right, #f0f0f0, #c0c0c0, #a0a0a0);
  border-radius: 5px 5px 0 0;
  box-shadow: inset 2px 0 5px rgba(0, 0, 0, 0.3);
}

.static-rocket .rocket-window {
  position: absolute;
  top: 15px;
  left: 50%;
  transform: translateX(-50%);
  width: 18px;
  height: 18px;
  background: radial-gradient(circle at 30% 30%, #a1d1ff, #3a7fbf);
  border-radius: 50%;
  border: 2px solid #707070;
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.5);
}

.static-rocket .rocket-nose {
  position: absolute;
  bottom: 105px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 20px solid transparent;
  border-right: 20px solid transparent;
  border-bottom: 35px solid #e04040;
  filter: drop-shadow(0 -2px 3px rgba(0, 0, 0, 0.3));
}

.static-rocket .rocket-fin {
  position: absolute;
  bottom: 30px;
  width: 0;
  height: 0;
  border-bottom: 30px solid #b03030;
}

.static-rocket .rocket-fin-left {
  left: -5px;
  border-left: 25px solid transparent;
  transform: skewY(15deg);
}

.static-rocket .rocket-fin-right {
  right: -5px;
  border-right: 25px solid transparent;
  transform: skewY(-15deg);
}

.static-rocket .rocket-flame-container {
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 30px;
  height: 60px;
  z-index: -1;
}

.static-rocket .rocket-flame {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 0 0 50% 50%;
  top: 0;
  bottom: auto;
}

.static-rocket .flame-core {
  bottom: 0;
  width: 15px;
  height: 45px;
  background: linear-gradient(to top, #ffffff, #fff8b0, #ffea00);
  opacity: 0.95;
  filter: blur(2px);
}

.static-rocket .flame-outer-1 {
  bottom: 0;
  width: 25px;
  height: 55px;
  background: linear-gradient(to top, #ffcc00, #ffa500, rgba(255, 165, 0, 0.5));
  opacity: 0.8;
  filter: blur(4px);
}

.static-rocket .flame-outer-2 {
  bottom: 0;
  width: 35px;
  height: 65px;
  background: linear-gradient(to top, #ff8c00, #ff4500, rgba(255, 69, 0, 0.3));
  opacity: 0.6;
  filter: blur(8px);
}

/* Static Satellite */
.static-satellite-container {
  position: absolute;
  top: 25%;
  left: 70%;
  width: 120px;
  height: 80px;
  z-index: 5;
  transform: scale(1) rotateZ(0deg);
}

.static-satellite {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
  transform: rotateZ(0deg) rotateY(0deg);
}

.static-satellite .satellite-body {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #c0c0c0, #a0a0a0, #808080);
  border-radius: 4px;
  box-shadow: inset 0 0 8px rgba(0, 0, 0, 0.4);
  background-image: linear-gradient(45deg, rgba(255,255,255,0.05) 25%, transparent 25%, transparent 50%, rgba(255,255,255,0.05) 50%, rgba(255,255,255,0.05) 75%, transparent 75%, transparent);
  background-size: 10px 10px;
}

.static-satellite .solar-panels {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 10px;
}

.static-satellite .solar-panel {
  position: absolute;
  top: 50%;
  width: 50px;
  height: 70px;
  background: linear-gradient(to bottom, #1a237e, #0d113b);
  border: 1px solid #707080;
  border-radius: 2px;
  box-shadow: 0 0 5px rgba(0, 100, 200, 0.2);
}

.static-satellite .panel-left {
  left: -25px;
  transform: translateY(-50%) rotateY(20deg) rotateZ(-5deg);
  transform-origin: right center;
}

.static-satellite .panel-right {
  right: -25px;
  transform: translateY(-50%) rotateY(-20deg) rotateZ(5deg);
  transform-origin: left center;
}

.static-satellite .panel-cells {
  position: absolute;
  inset: 2px;
  background-image:
    repeating-linear-gradient(0deg, rgba(150, 180, 255, 0.15), rgba(150, 180, 255, 0.15) 1px, transparent 1px, transparent 8px),
    repeating-linear-gradient(90deg, rgba(150, 180, 255, 0.15), rgba(150, 180, 255, 0.15) 1px, transparent 1px, transparent 8px);
  opacity: 0.8;
}

.static-satellite .satellite-dish {
  position: absolute;
  top: -5px;
  left: 50%;
  transform: translateX(-50%);
  width: 25px;
  height: 25px;
  background: radial-gradient(circle at 70% 70%, #f0f0f0, #b0b0b0);
  border-radius: 50%;
  box-shadow: inset 2px 2px 5px rgba(0, 0, 0, 0.5);
}

.static-satellite .dish-inner {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 6px;
  height: 6px;
  background: #333;
  border-radius: 50%;
  border: 1px solid #555;
}

.static-satellite .satellite-antenna-small {
  position: absolute;
  bottom: 5px;
  left: 50%;
  transform: translateX(-50%) rotate(10deg);
  width: 2px;
  height: 15px;
  background: #a0a0a0;
  border-radius: 2px 2px 0 0;
}

/* Planet 4: Gas Giant with Bands and Spot */
.static-planet.planet-4 {
  width: 120px;
  height: 120px;
  top: 60%;
  left: 8%;
  background: radial-gradient(
    circle at 40% 60%,
    #f8d7a8 0%,
    #e0ac69 30%,
    #c68642 60%,
    #a0522d 100%
  );
  box-shadow: 0 0 35px rgba(224, 172, 105, 0.3), inset -20px -10px 50px rgba(0, 0, 0, 0.6);
  overflow: hidden;
  z-index: 2;
  transform: translate(0, 0);
}

.static-planet.planet-4 .planet-bands {
  position: absolute;
  width: 150%;
  height: 100%;
  top: 0;
  left: -25%;
  transform-origin: center center;
}

.static-planet.planet-4 .band {
  position: absolute;
  width: 100%;
  left: 0;
  height: 20%;
  opacity: 0.6;
}

.static-planet.planet-4 .band-1 { top: 10%; background: rgba(255, 248, 220, 0.5); height: 15%; }
.static-planet.planet-4 .band-2 { top: 30%; background: rgba(210, 180, 140, 0.6); }
.static-planet.planet-4 .band-3 { top: 55%; background: rgba(160, 82, 45, 0.7); }
.static-planet.planet-4 .band-4 { top: 80%; background: rgba(245, 222, 179, 0.5); height: 15%; }

.static-planet.planet-4 .planet-great-spot {
  position: absolute;
  width: 35%;
  height: 25%;
  top: 55%;
  left: 15%;
  border-radius: 50%;
  filter: blur(3px);
  opacity: 0.8;
  z-index: 4;
  background: rgba(240, 210, 180, 0.6);
}

/* Planet 5: Rocky, Cratered Planet */
.static-planet.planet-5 {
  width: 60px;
  height: 60px;
  top: 20%;
  left: 80%;
  background: radial-gradient(
    circle at 70% 30%,
    #a9a9a9 0%,
    #808080 40%,
    #696969 70%,
    #404040 100%
  );
  box-shadow: 0 0 15px rgba(128, 128, 128, 0.3), inset -10px -5px 25px rgba(0, 0, 0, 0.7);
  z-index: 4;
  overflow: hidden;
  transform: translate(0, 0);
}

.static-planet.planet-5 .planet-surface-texture {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  border-radius: 50%;
  background-image: radial-gradient(rgba(255,255,255,0.05) 1px, transparent 1px);
  background-size: 5px 5px;
  opacity: 0.3;
  z-index: 1;
}

.static-planet.planet-5 .crater {
  position: absolute;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.3);
  box-shadow: inset 1px 1px 2px rgba(0,0,0,0.6), 0 0 1px 1px rgba(255, 255, 255, 0.05);
  z-index: 2;
}

.static-planet.planet-5 .crater-1 { width: 25%; height: 25%; top: 20%; left: 30%; }
.static-planet.planet-5 .crater-2 { width: 15%; height: 15%; top: 55%; left: 60%; }
.static-planet.planet-5 .crater-3 { width: 20%; height: 20%; top: 40%; left: 10%; }

.static-planet.planet-5 .moons-p5 {
  position: absolute;
  width: 150%;
  height: 150%;
  top: -25%;
  left: -25%;
  z-index: 1;
}

.static-planet.planet-5 .moon-3 {
  width: 8px;
  height: 8px;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  background: radial-gradient(circle at 30% 30%, #666, #444, #222);
}

/* Planet 6: Distant Icy Body */
.static-planet.planet-6 {
  width: 40px;
  height: 40px;
  top: 70%;
  left: 60%;
  background: radial-gradient(
    circle at 50% 50%,
    #e0ffff 0%,
    #afeeee 50%,
    #90dcdc 100%
  );
  box-shadow: 0 0 15px rgba(175, 238, 238, 0.6), inset -5px -5px 15px rgba(0, 0, 0, 0.3);
  z-index: 1;
  filter: blur(0.5px);
  transform: translate(0, 0) scale(1);
}

.static-planet.planet-6 .planet-haze {
  position: absolute;
  width: 130%;
  height: 130%;
  top: -15%;
  left: -15%;
  border-radius: 50%;
  background: radial-gradient(
    circle at center,
    rgba(224, 255, 255, 0.2) 0%,
    rgba(175, 238, 238, 0.1) 70%,
    transparent 100%
  );
  filter: blur(5px);
  opacity: 0.7;
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

  /* ======== SNOW THEME STATIC STYLES ======== */
  .snow {
    /* Slightly darker, deeper blue gradient for the base sky */
    background: linear-gradient(to bottom, #1c2a4f 0%, #3a4a7a 50%, #6a86b8 100%);
    overflow: hidden;
  }

  /* --- Sky & Stars --- */
  .static-snow-sky {
    position: absolute;
    inset: 0;
    z-index: 0;
  }

  .static-stars-layer {
    position: absolute;
    inset: 0;
    background-repeat: repeat;
    opacity: 0.6;
  }

  .static-stars-layer.stars-far {
    background-image: radial-gradient(1px 1px at 20% 30%, white, transparent),
                      radial-gradient(1px 1px at 80% 50%, white, transparent),
                      radial-gradient(1px 1px at 50% 80%, white, transparent);
    background-size: 400px 400px;
    opacity: 0.4;
  }

  .static-stars-layer.stars-mid {
    background-image: radial-gradient(1.5px 1.5px at 10% 70%, white, transparent),
                      radial-gradient(1px 1px at 60% 10%, white, transparent),
                      radial-gradient(1.5px 1.5px at 90% 90%, white, transparent);
    background-size: 300px 300px;
    opacity: 0.7;
  }

  .static-moon {
    position: absolute;
    top: 10%;
    left: 5%;
    width: 80px;
    height: 80px;
    background: radial-gradient(
      circle at center,
      rgba(255, 255, 255, 0.8) 0%,
      rgba(255, 255, 255, 0.6) 50%,
      rgba(255, 255, 255, 0.4) 100%
    );
    border-radius: 50%;
    box-shadow: inset -5px -5px rgba(200, 200, 200, 0.5);
  }

  /* --- Aurora Borealis --- */
  .static-aurora-borealis-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 75%;
    overflow: hidden;
    z-index: 1;
    mix-blend-mode: screen;
    filter: blur(18px);
    opacity: 0.9;
  }

  .static-aurora-ribbon {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 180%;
    height: 100%;
    transform-origin: bottom center;
  }

  .static-aurora-ribbon.ribbon-1 {
    background: linear-gradient(to top, transparent 5%, rgba(100, 255, 150, 0.65) 40%, rgba(180, 255, 200, 0.5) 60%, transparent 95%);
    left: -40%;
    transform: translateX(-10%) scaleY(1) skewX(-12deg);
    opacity: 0.65;
  }

  .static-aurora-ribbon.ribbon-2 {
    background: linear-gradient(to top, transparent 10%, rgba(80, 180, 255, 0.6) 50%, rgba(160, 210, 255, 0.4) 70%, transparent 90%);
    left: -25%;
    transform: translateX(5%) scaleY(1.05) skewX(8deg);
    opacity: 0.6;
  }

  .static-aurora-ribbon.ribbon-3 {
    background: linear-gradient(to top, transparent 0%, rgba(190, 100, 255, 0.55) 40%, rgba(220, 170, 255, 0.4) 65%, transparent 85%);
    left: -5%;
    transform: translateX(-5%) scaleY(0.95) skewX(-6deg);
    opacity: 0.55;
  }

  .static-aurora-ribbon.ribbon-4 {
    background: linear-gradient(to top, transparent 5%, rgba(255, 120, 200, 0.65) 45%, rgba(255, 170, 220, 0.5) 65%, transparent 90%);
    left: -15%;
    transform: translateX(8%) scaleY(1.02) skewX(10deg);
    opacity: 0.65;
  }

  /* --- Mountains --- */
  .static-mountains-distant, .static-mountains-mid, .static-mountains-near {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 70%;
  }

  .static-mountains-distant { z-index: 2; height: 50%; opacity: 0.6; filter: blur(3px); }
  .static-mountains-mid { z-index: 3; height: 65%; opacity: 0.8; filter: blur(1px); }
  .static-mountains-near { z-index: 6; height: 75%; }

  .static-mountain-peak {
    position: absolute;
    bottom: 0;
    background-color: #8a9ec4;
    overflow: hidden;
    filter: drop-shadow(5px -5px 10px rgba(0, 0, 0, 0.2));
  }

  /* Jagged shapes using clip-path */
  .static-mountain-peak.peak-distant-1 { left: 5%; width: 40%; height: 80%; clip-path: polygon(0 100%, 20% 40%, 50% 15%, 70% 50%, 100% 100%); background-color: #6a7c9f; }
  .static-mountain-peak.peak-distant-2 { left: 55%; width: 45%; height: 70%; clip-path: polygon(0 100%, 30% 50%, 55% 25%, 80% 60%, 100% 100%); background-color: #788aac; }

  .static-mountain-peak.peak-mid-1 { left: -5%; width: 55%; height: 85%; clip-path: polygon(0 100%, 15% 50%, 40% 20%, 65% 60%, 90% 55%, 100% 100%); }
  .static-mountain-peak.peak-mid-2 { left: 40%; width: 50%; height: 95%; clip-path: polygon(0 100%, 25% 60%, 50% 10%, 75% 55%, 100% 100%); background-color: #93a4cb; }
  .static-mountain-peak.peak-mid-3 { left: 75%; width: 30%; height: 75%; clip-path: polygon(0 100%, 40% 40%, 60% 30%, 100% 100%); }

  .static-mountain-peak.peak-near-1 { left: -10%; width: 60%; height: 90%; clip-path: polygon(0 100%, 20% 45%, 50% 5%, 70% 50%, 100% 100%); background-color: #aab8d3; }
  .static-mountain-peak.peak-near-2 { left: 50%; width: 70%; height: 100%; clip-path: polygon(0 100%, 15% 60%, 40% 15%, 65% 70%, 85% 65%, 100% 100%); background-color: #b5c3dd; }

  /* Example texture for mid mountains */
  .static-mountains-mid .mountain-texture {
    position: absolute;
    inset: 0;
    opacity: 0.3;
    background: linear-gradient(160deg, rgba(255,255,255,0.15) 20%, transparent 50%),
                linear-gradient(20deg, rgba(255,255,255,0.1) 30%, transparent 60%);
  }

  /* Textures for near mountains */
  .static-mountain-peak .rock-texture {
    background: linear-gradient(135deg, rgba(0,0,0,0.1) 0%, transparent 10%),
                linear-gradient(225deg, rgba(0,0,0,0.1) 0%, transparent 10%);
    background-size: 40px 40px;
    opacity: 0.15;
  }

  .static-mountain-peak .snow-texture {
    background: linear-gradient(to bottom, rgba(255,255,255,0.5) 0%, transparent 30%),
                radial-gradient(circle at 30% 20%, rgba(255,255,255,0.3) 5%, transparent 20%);
    opacity: 0.6;
    mix-blend-mode: overlay;
  }

  /* --- Forests --- */
  .static-forest-layer-mid, .static-forest-layer-near {
    position: absolute;
    bottom: 10%;
    left: 0;
    width: 100%;
    height: 35%;
  }

  .static-forest-layer-mid { z-index: 4; height: 25%; bottom: 15%; opacity: 0.7; filter: blur(0.5px); }
  .static-forest-layer-near { z-index: 8; height: 30%; bottom: 5%; }

  .static-pine-tree {
    position: absolute;
    bottom: 0;
    width: 40px;
  }

  .static-pine-tree .tree-trunk {
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 6px;
    height: 25%;
    background: #5a3a22;
    border-radius: 2px 2px 0 0;
    z-index: 1;
  }

  .static-pine-tree .tree-branch {
    position: absolute;
    left: 50%;
    width: 100%;
    background: linear-gradient(to bottom right, #1a4d2e, #10351e);
    clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
    transform-origin: bottom center;
  }

  .static-pine-tree .tree-branch.branch-1 { height: 40%; bottom: 20%; transform: translateX(-50%) scale(1); }
  .static-pine-tree .tree-branch.branch-2 { height: 35%; bottom: 40%; transform: translateX(-50%) scale(0.85); }
  .static-pine-tree .tree-branch.branch-3 { height: 30%; bottom: 60%; transform: translateX(-50%) scale(0.7); }
  .static-pine-tree.tree-near .tree-branch.branch-4 { height: 25%; bottom: 75%; transform: translateX(-50%) scale(0.55); }

  .static-pine-tree .snow-on-branch {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 40%;
    background: rgba(240, 248, 255, 0.8);
    clip-path: polygon(50% 0%, 10% 100%, 90% 100%);
    filter: blur(0.5px);
    border-radius: 3px 3px 0 0;
  }

  /* --- Mist/Fog --- */
  .static-mist-container {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 40%;
    z-index: 5;
    overflow: hidden;
    pointer-events: none;
  }

  .static-mist-layer {
    position: absolute;
    width: 150%;
    height: 60%;
    left: -25%;
    background: radial-gradient(ellipse at center, rgba(180, 190, 210, 0.25) 0%, rgba(150, 160, 180, 0.1) 50%, transparent 80%);
    filter: blur(20px);
    opacity: 0.8;
  }

  .static-mist-layer.mist-1 { bottom: 0; height: 50%; opacity: 0.7; transform: translateX(-5%); }
  .static-mist-layer.mist-2 { bottom: 10%; height: 70%; opacity: 0.6; transform: translateX(5%); }
  .static-mist-layer.mist-3 { bottom: 25%; height: 60%; opacity: 0.5; transform: translateX(-2%); }

  /* --- Animals --- */
  .static-polar-bear-container {
    position: absolute;
    bottom: 8%;
    right: 15%;
    width: 300px;
    height: 220px;
    z-index: 8;
  }

  .static-polar-bear {
    position: relative;
    width: 220px;
    height: 120px;
    transform-style: preserve-3d;
  }

  .static-polar-bear .polar-bear-body {
    position: absolute;
    width: 100%;
    height: 100%;
    transform-origin: center bottom;
    transform: rotate(-1deg);
  }

  .static-polar-bear .polar-bear-head {
    position: absolute;
    width: 75px;
    height: 60px;
    top: -10px;
    left: 10px;
    background: #ffffff;
    border-radius: 50% 70% 60% 40% / 50% 60% 40% 50%;
    box-shadow: 
      -5px -5px 10px rgba(255, 255, 255, 0.8) inset,
      5px 5px 15px rgba(200, 200, 180, 0.4) inset;
    transform-origin: bottom center;
    transform: rotate(-2deg);
    z-index: 3;
  }

  .static-polar-bear .polar-bear-ear {
    position: absolute;
    width: 18px;
    height: 18px;
    background: #ffffff;
    border-radius: 50%;
    z-index: 1;
  }

  .static-polar-bear .polar-bear-ear-left {
    top: -8px;
    left: 15px;
    transform: rotate(-5deg);
  }

  .static-polar-bear .polar-bear-ear-right {
    top: -8px;
    right: 15px;
    transform: rotate(5deg);
  }

  .static-polar-bear .polar-bear-snout {
    position: absolute;
    width: 45px;
    height: 35px;
    background: #ffffff;
    bottom: 0;
    left: 15px;
    border-radius: 60% 60% 70% 70% / 60% 60% 70% 70%;
    transform: translateY(10px);
    z-index: 2;
  }

  .static-polar-bear .polar-bear-nose {
    position: absolute;
    width: 22px;
    height: 14px;
    background: #222222;
    border-radius: 40% 40% 60% 60% / 40% 40% 60% 60%;
    top: 5px;
    left: 50%;
    transform: translateX(-50%);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  .static-polar-bear .polar-bear-mouth {
    position: absolute;
    width: 12px;
    height: 3px;
    background: #333333;
    border-radius: 50%;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
  }

  .static-polar-bear .polar-bear-eye {
    position: absolute;
    width: 10px;
    height: 8px;
    background: #ffffff;
    border-radius: 50%;
    top: 20px;
    z-index: 3;
  }

  .static-polar-bear .polar-bear-eye-left {
    left: 22px;
    transform: rotate(-10deg);
  }

  .static-polar-bear .polar-bear-eye-right {
    right: 22px;
    transform: rotate(10deg);
  }

  .static-polar-bear .polar-bear-eye-pupil {
    position: absolute;
    width: 6px;
    height: 6px;
    top: 1px;
    left: 2px;
    background: #000000;
    border-radius: 50%;
  }

  .static-polar-bear .polar-bear-torso {
    position: absolute;
    width: 220px;
    height: 95px;
    bottom: 35px;
    background: #ffffff;
    border-radius: 60% 70% 55% 40% / 80% 80% 45% 40%;
    box-shadow: 
      -10px -5px 15px rgba(255, 255, 255, 0.6) inset,
      10px 10px 20px rgba(200, 200, 180, 0.3) inset;
    z-index: 2;
    transform-origin: center bottom;
  }

  .static-polar-bear .polar-bear-fur-detail {
    position: absolute;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 50%;
  }

  .static-polar-bear .fur-detail-1 {
    width: 50px;
    height: 30px;
    top: 10px;
    left: 30px;
    transform: rotate(-15deg);
    box-shadow: 2px 5px 10px rgba(255, 255, 255, 0.6);
  }

  .static-polar-bear .fur-detail-2 {
    width: 40px;
    height: 35px;
    top: 25px;
    left: 60px;
    transform: rotate(10deg);
    box-shadow: -2px 3px 8px rgba(255, 255, 255, 0.6);
  }

  .static-polar-bear .fur-detail-3 {
    width: 45px;
    height: 25px;
    top: 15px;
    left: 90px;
    transform: rotate(-5deg);
    box-shadow: 1px 4px 8px rgba(255, 255, 255, 0.6);
  }

  .static-polar-bear .polar-bear-leg {
    position: absolute;
    width: 35px;
    background: #ffffff;
    z-index: 1;
    box-shadow: 
      -2px -2px 5px rgba(255, 255, 255, 0.6) inset,
      2px 2px 8px rgba(200, 200, 180, 0.4) inset;
  }

  .static-polar-bear .polar-bear-leg-front-left {
    height: 55px;
    bottom: 0;
    left: 25px;
    border-radius: 40% 60% 20% 30% / 20% 30% 20% 40%;
    transform: rotate(2deg);
  }

  .static-polar-bear .polar-bear-leg-front-right {
    height: 55px;
    bottom: 0;
    left: 65px;
    border-radius: 60% 40% 30% 20% / 30% 20% 40% 20%;
    transform: rotate(-3deg);
  }

  .static-polar-bear .polar-bear-leg-back-left {
    height: 50px;
    bottom: 0;
    right: 65px;
    border-radius: 40% 60% 20% 30% / 20% 30% 20% 40%;
    transform: rotate(1deg);
  }

  .static-polar-bear .polar-bear-leg-back-right {
    height: 50px;
    bottom: 0;
    right: 25px;
    border-radius: 60% 40% 30% 20% / 30% 20% 40% 20%;
    transform: rotate(-2deg);
  }

  .static-polar-bear .polar-bear-paw {
    position: absolute;
    width: 38px;
    height: 15px;
    background: #ffffff;
    bottom: -8px;
    left: 50%;
    transform: translateX(-50%);
    border-radius: 50% 50% 45% 45%;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
  }

  .static-polar-bear .polar-bear-paw-front-left::after,
  .static-polar-bear .polar-bear-paw-front-right::after,
  .static-polar-bear .polar-bear-paw-back-left::after,
  .static-polar-bear .polar-bear-paw-back-right::after {
    content: '';
    position: absolute;
    width: 30px;
    height: 2px;
    background: rgba(0, 0, 0, 0.15);
    bottom: 2px;
    left: 50%;
    transform: translateX(-50%);
    border-radius: 50%;
  }

  .static-polar-bear .polar-bear-shadow {
    position: absolute;
    width: 180px;
    height: 30px;
    bottom: -15px;
    left: 30px;
    background: rgba(58, 74, 122, 0.15);
    border-radius: 50%;
    filter: blur(8px);
    transform-origin: center;
    transform: scaleX(1);
    z-index: 1;
    opacity: 0.2;
  }

  .static-penguin-container {
    position: absolute;
    bottom: 5%;
    left: 20%;
    width: 200px;
    height: 200px;
    z-index: 8;
  }

  .static-penguin {
    position: relative;
    width: 100px;
    height: 150px;
    transform-style: preserve-3d;
  }

  .static-penguin .penguin-body {
    position: absolute;
    width: 80px;
    height: 130px;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    background: #1a1a2e;
    border-radius: 40% 40% 30% 30%;
    transform-origin: bottom center;
  }

  .static-penguin .penguin-head {
    position: absolute;
    width: 60px;
    height: 55px;
    top: -25px;
    left: 50%;
    transform: translateX(-50%);
    background: #1a1a2e;
    border-radius: 50% 50% 40% 40%;
    z-index: 2;
  }

  .static-penguin .penguin-face {
    position: absolute;
    width: 100%;
    height: 100%;
  }

  .static-penguin .penguin-eye {
    position: absolute;
    width: 12px;
    height: 12px;
    top: 18px;
    background: white;
    border-radius: 50%;
    z-index: 3;
  }

  .static-penguin .penguin-eye-left {
    left: 15px;
    transform: rotate(-10deg);
  }

  .static-penguin .penguin-eye-right {
    right: 15px;
    transform: rotate(10deg);
  }

  .static-penguin .penguin-eye-pupil {
    position: absolute;
    width: 6px;
    height: 6px;
    top: 3px;
    left: 3px;
    background: #000;
    border-radius: 50%;
  }

  .static-penguin .penguin-beak {
    position: absolute;
    width: 15px;
    height: 10px;
    top: 30px;
    left: 50%;
    transform: translateX(-50%);
    background: #ff9e41;
    border-radius: 30% 30% 60% 60%;
    z-index: 2;
  }

  .static-penguin .penguin-belly {
    position: absolute;
    width: 60px;
    height: 90px;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    background: white;
    border-radius: 50% 50% 40% 40%;
    z-index: 1;
  }

  .static-penguin .penguin-wing {
    position: absolute;
    width: 24px;
    height: 70px;
    top: 20px;
    background: #1a1a2e;
    border-radius: 30% 30% 50% 50%;
    transform-origin: top center;
    z-index: 0;
  }

  .static-penguin .penguin-wing-left {
    left: -10px;
    transform: rotate(-15deg);
  }

  .static-penguin .penguin-wing-right {
    right: -10px;
    transform: rotate(15deg);
  }

  .static-penguin .penguin-foot {
    position: absolute;
    width: 25px;
    height: 10px;
    bottom: -8px;
    background: #ff9e41;
    border-radius: 50% 50% 0 0;
    z-index: 0;
    transform-origin: center top;
  }

  .static-penguin .penguin-foot-left {
    left: 10px;
    transform: rotate(-10deg);
  }

  .static-penguin .penguin-foot-right {
    right: 10px;
    transform: rotate(10deg);
  }

  .static-penguin .penguin-shadow {
    position: absolute;
    width: 80px;
    height: 20px;
    bottom: -15px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(58, 74, 122, 0.15);
    border-radius: 50%;
    filter: blur(5px);
    z-index: 0;
  }

  /* --- Snow Ground --- */
  .static-snow-ground {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 25%;
    z-index: 7;
    overflow: hidden;
  }

  .static-snow-drift {
    position: absolute;
    bottom: 0;
    background: linear-gradient(to top, #e8f0ff 0%, #ffffff 50%, #f8faff 100%);
    box-shadow: 0 -5px 15px rgba(106, 134, 184, 0.1);
  }

  .static-snow-drift.drift-large-1 { 
    left: -20%; 
    width: 80%; 
    height: 90%; 
    border-radius: 60% 40% 0 0 / 100% 100% 0 0; 
  }

  .static-snow-drift.drift-medium-1 { 
    left: 30%; 
    width: 50%; 
    height: 70%; 
    border-radius: 50% 50% 0 0 / 100% 100% 0 0; 
    background-color: #f0f8ff; 
  }

  .static-snow-drift.drift-small-1 { 
    left: 65%; 
    width: 30%; 
    height: 50%; 
    border-radius: 70% 30% 0 0 / 100% 100% 0 0; 
  }

  .static-snow-drift.drift-medium-2 { 
    left: 75%; 
    width: 45%; 
    height: 80%; 
    border-radius: 40% 60% 0 0 / 100% 100% 0 0; 
    background-color: #f4faff;
  }

  .static-snow-drift.drift-large-2 { 
    left: 40%; 
    width: 50%; 
    height: 100%; 
    border-radius: 50% 50% 0 0 / 80% 80% 0 0; 
    z-index: -1;
  }

  /* --- Snowfall --- */
  .static-snowfall-layer-far, 
  .static-snowfall-layer-mid, 
  .static-snowfall-layer-near {
    position: absolute;
    inset: 0;
    pointer-events: none;
  }

  .static-snowflake {
    position: absolute;
    background: white;
    border-radius: 50%;
    width: 6px;
    height: 6px;
    opacity: 0.8;
  }

  .snow-far {
    filter: blur(2px);
  }

  .snow-mid {
    filter: blur(1px);
  }

  .snow-near {
    box-shadow: 0 0 5px rgba(255, 255, 255, 0.3);
  }

  .static-vignette-overlay {
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at center, transparent 50%, rgba(10, 15, 30, 0.4) 100%);
    z-index: 20;
    pointer-events: none;
  }
</style>