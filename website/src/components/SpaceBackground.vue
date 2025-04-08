<!-- SpaceBackground.vue -->
<template>
  <div class="space-background" :class="[theme, { 'animations-disabled': !animationsEnabled }]">
    <!-- Container for all space elements -->
    <div class="space-elements">
      <!-- Dynamic space elements based on the selected theme -->
      <template v-if="theme === 'cosmic'">
        <!-- Comets -->
        <div class="crowd-container">
          <div v-for="i in 150" :key="`crowd-${i}`" class="crowd-dot" :style="getCrowdDotStyle()"></div>
        </div>
        <div class="comet comet-1"></div>
        <div class="comet comet-2"></div>
        <div class="cometInverse comet-3"></div>
        <div class="comet comet-4"></div>
        <div class="cometInverse comet-5"></div>
        
        <!-- Galaxy -->
        <div class="galaxy galaxy-1"></div>
        
        <!-- Planets -->
        <div class="planet planet-1">
          <div class="planet-rings"></div>
        </div>
        
        <div class="planet planet-2">
          <div class="planet-atmosphere"></div>
          <div class="planet-storm"></div>
        </div>
        
        <div class="planet planet-3">
          <div class="planet-ice-caps"></div>
          <div class="planet-moons">
            <div class="planet-moon moon-1"></div>
            <div class="planet-moon moon-2"></div>
          </div>
        </div>
      </template>

      <!-- Ocean theme elements -->
      <template v-else-if="theme === 'ocean'">
        
        <!-- Light Rays -->
        <div class="light-ray light-ray-1"></div>
        <div class="light-ray light-ray-2"></div>
        <div class="light-ray light-ray-3"></div>
        
        <!-- Bubbles - Enhanced and more -->
        <div class="bubble bubble-1"></div>
        <div class="bubble bubble-2"></div>
        <div class="bubble bubble-3"></div>
        <div class="bubble bubble-4"></div>
        <div class="bubble bubble-5"></div>
        <div class="bubble bubble-6"></div>
        <div class="bubble bubble-7"></div>
        <div class="bubble bubble-8"></div>
        <div class="bubble bubble-9"></div>
        <div class="bubble bubble-10"></div>
        <div class="bubble bubble-11"></div>
        <div class="bubble bubble-12"></div>
        
        <!-- Particles du plancton -->
        <div class="plankton-container">
          <div v-for="i in 40" :key="`plankton-${i}`" class="plankton"></div>
        </div>
        
        <!-- Coral Reef - Enhanced -->
        <div class="coral coral-1">
          <div class="coral-branch branch-1"></div>
          <div class="coral-branch branch-2"></div>
          <div class="coral-branch branch-3"></div>
        </div>
        
        <div class="coral coral-2">
          <div class="coral-branch branch-1"></div>
          <div class="coral-branch branch-2"></div>
        </div>
        
        <!-- Fish School -->
        <div class="fish-school fish-school-1">
          <div v-for="i in 8" :key="`school-1-fish-${i}`" class="school-fish"></div>
        </div>
        
        <div class="fish-school fish-school-2">
          <div v-for="i in 12" :key="`school-2-fish-${i}`" class="school-fish"></div>
        </div>

        <div class="shark">
          <div class="shark-body">
            <!-- Éléments du visage -->
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
          <!-- Ombre du requin -->
          <div class="shark-shadow"></div>
          <!-- Bulles occasionnelles -->
          <div class="shark-bubbles">
            <div class="shark-bubble bubble-shark-1"></div>
            <div class="shark-bubble bubble-shark-2"></div>
            <div class="shark-bubble bubble-shark-3"></div>
          </div>
        </div>
        <!-- Individual Fish - Enhanced -->
        <div class="fish fish-1">
          <div class="fish-tail"></div>
        </div>
        <div class="fish fish-2">
          <div class="fish-tail"></div>
        </div>
        <div class="fish fish-3">
          <div class="fish-tail"></div>
        </div>
        <div class="fish fish-4">
          <div class="fish-tail"></div>
        </div>
        
        <!-- Seaweed - Enhanced -->
        <div class="seaweed seaweed-1">
          <div class="seaweed-strand"></div>
          <div class="seaweed-strand"></div>
          <div class="seaweed-strand"></div>
        </div>
        
        <div class="seaweed seaweed-2">
          <div class="seaweed-strand"></div>
          <div class="seaweed-strand"></div>
        </div>
        
        <div class="seaweed seaweed-3">
          <div class="seaweed-strand"></div>
          <div class="seaweed-strand"></div>
          <div class="seaweed-strand"></div>
          <div class="seaweed-strand"></div>
        </div>
        
        <!-- Jellyfish -->
        <div class="jellyfish jellyfish-1">
          <div class="jellyfish-head"></div>
          <div class="jellyfish-tentacles">
            <div class="tentacle"></div>
            <div class="tentacle"></div>
            <div class="tentacle"></div>
            <div class="tentacle"></div>
            <div class="tentacle"></div>
          </div>
        </div>
        
        <div class="jellyfish jellyfish-2">
          <div class="jellyfish-head"></div>
          <div class="jellyfish-tentacles">
            <div class="tentacle"></div>
            <div class="tentacle"></div>
            <div class="tentacle"></div>
            <div class="tentacle"></div>
            <div class="tentacle"></div>
          </div>
        </div>

        <!-- Whale -->
        <div class="whale">
          <div class="whale-body">
            <div class="whale-head"></div>
            <div class="whale-eye"></div>
            <div class="whale-mouth"></div>
            <div class="whale-fin whale-fin-dorsal"></div>
            <div class="whale-fin whale-fin-pectoral"></div>
            <div class="whale-fin whale-fin-tail"></div>
            <div class="whale-pattern"></div>
            <div class="whale-blowhole"></div>
            <!-- Whale spout (only appears occasionally) -->
            <div class="whale-spout"></div>
          </div>
          <!-- Subtle water displacement effect -->
          <div class="whale-water-displacement"></div>
          <!-- Bubbles trail -->
          <div class="whale-bubbles">
            <div class="whale-bubble bubble-whale-1"></div>
            <div class="whale-bubble bubble-whale-2"></div>
            <div class="whale-bubble bubble-whale-3"></div>
            <div class="whale-bubble bubble-whale-4"></div>
            <div class="whale-bubble bubble-whale-5"></div>
          </div>
        </div>
        
        <!-- Sea floor -->
        <div class="sea-floor">
          <div class="sand-dune sand-dune-1"></div>
          <div class="sand-dune sand-dune-2"></div>
          <div class="sand-dune sand-dune-3"></div>
        </div>
      </template>
      
      <!-- Cyberpunk theme elements - ENHANCED -->
      <template v-else-if="theme === 'cyberpunk'">
        <!-- Rain Effect -->
        <div class="cyber-rain">
          <div v-for="i in 15" :key="`rain-${i}`" class="rain-drop" :style="getRainDropStyle(i)"></div>
        </div>
        
        <!-- Neon Signs -->
        <div class="neon-sign neon-sign-1">DIGITAL DREAMS</div>
        <div class="neon-sign neon-sign-2">NEURAL LINK</div>
        <div class="neon-sign neon-sign-3">CYBER ZONE</div>
        
        <!-- Grid lines - Enhanced 3D -->
        <div class="grid-container">
          <div class="grid-horizontal" v-for="i in 6" :key="`h-${i}`"></div>
          <div class="grid-vertical" v-for="i in 6" :key="`v-${i}`"></div>
        </div>
        
        <!-- City Silhouette -->
        <div class="cyber-city">
          <div v-for="i in 7" :key="`building-${i}`" class="city-building"></div>
        </div>
        
        <!-- Flying data cubes - Enhanced -->
        <div class="data-cube data-cube-1">
          <div class="cube-face"></div>
          <div class="cube-face"></div>
          <div class="cube-face"></div>
          <div class="cube-face"></div>
          <div class="cube-face"></div>
          <div class="cube-face"></div>
        </div>
        
        <div class="data-cube data-cube-2">
          <div class="cube-face"></div>
          <div class="cube-face"></div>
          <div class="cube-face"></div>
          <div class="cube-face"></div>
          <div class="cube-face"></div>
          <div class="cube-face"></div>
        </div>
        
        <!-- Data Stream -->
        <div class="data-stream data-stream-1"></div>
        <div class="data-stream data-stream-2"></div>
        <div class="data-stream data-stream-3"></div>
        
        <!-- Circuit paths - Enhanced -->
        <div class="circuit circuit-1">
          <div class="circuit-node" v-for="i in 3" :key="`circuit-1-node-${i}`"></div>
        </div>
        
        <div class="circuit circuit-2">
          <div class="circuit-node" v-for="i in 4" :key="`circuit-2-node-${i}`"></div>
        </div>
        
        <!-- Holographic displays - Enhanced -->
        <div class="hologram hologram-1">
          <div class="hologram-content">
            <div class="hologram-line" v-for="i in 3" :key="`hologram-1-line-${i}`"></div>
          </div>
        </div>
        
        <div class="hologram hologram-3">
          <div class="hologram-ring"></div>
          <div class="hologram-ring"></div>
        </div>
        
        <!-- Glitch Effect Overlay -->
        <div class="glitch-overlay"></div>
      </template>

      <!-- Forest theme elements -->
      <template v-else-if="theme === 'forest'">
        <!-- Rayons de soleil filtrant à travers les feuilles -->
        <div class="sunbeam sunbeam-1"></div>
        <div class="sunbeam sunbeam-2"></div>
        <div class="sunbeam sunbeam-3"></div>
        
        <!-- Brouillard forestier -->
        <div class="forest-mist forest-mist-1"></div>
        <div class="forest-mist forest-mist-2"></div>
        <div class="forest-mist forest-mist-3"></div>

        <!-- Feuilles qui tombent -->
        <div class="leaves-container">
          <div v-for="i in 8" :key="`leaf-${i}`" class="falling-leaf" :style="getFallingLeafStyle(i)"></div>
        </div>
        
        <!-- Arbres en arrière-plan -->
        <div class="tree-layer tree-layer-bg">
          <div class="tree tree-bg-1">
            <div class="tree-trunk"></div>
            <div class="tree-canopy"></div>
          </div>
          <div class="tree tree-bg-2">
            <div class="tree-trunk"></div>
            <div class="tree-canopy"></div>
          </div>
          <div class="tree tree-bg-3">
            <div class="tree-trunk"></div>
            <div class="tree-canopy"></div>
          </div>
          <div class="tree tree-bg-4">
            <div class="tree-trunk"></div>
            <div class="tree-canopy"></div>
          </div>
          <div class="tree tree-bg-5">
            <div class="tree-trunk"></div>
            <div class="tree-canopy"></div>
          </div>
        </div>
        
        <!-- Arbres au premier plan -->
        <div class="tree-layer tree-layer-fg">
          <div class="tree tree-fg-1">
            <div class="tree-trunk"></div>
            <div class="tree-canopy"></div>
          </div>
          <div class="tree tree-fg-2">
            <div class="tree-trunk"></div>
            <div class="tree-canopy"></div>
          </div>
        </div>
        
        <!-- Papillons -->
        <div class="butterfly butterfly-1">
          <div class="butterfly-wing wing-left"></div>
          <div class="butterfly-wing wing-right"></div>
        </div>
        <div class="butterfly butterfly-2">
          <div class="butterfly-wing wing-left"></div>
          <div class="butterfly-wing wing-right"></div>
        </div>
        <div class="butterfly butterfly-3">
          <div class="butterfly-wing wing-left"></div>
          <div class="butterfly-wing wing-right"></div>
        </div>
        
        <!-- Oiseaux volants -->
        <div class="bird bird-1"></div>
        <div class="bird bird-2"></div>
        <div class="bird bird-3"></div>
        
        <!-- Fleurs et champignons -->
        <div class="forest-floor">
          <div class="mushroom mushroom-1">
            <div class="mushroom-cap"></div>
            <div class="mushroom-stem"></div>
          </div>
          <div class="mushroom mushroom-2">
            <div class="mushroom-cap"></div>
            <div class="mushroom-stem"></div>
          </div>
          <div class="mushroom mushroom-3">
            <div class="mushroom-cap"></div>
            <div class="mushroom-stem"></div>
          </div>
          
          <div class="flower flower-1">
            <div class="flower-center"></div>
            <div class="flower-petal"></div>
            <div class="flower-petal"></div>
            <div class="flower-petal"></div>
            <div class="flower-petal"></div>
            <div class="flower-petal"></div>
            <div class="flower-stem"></div>
          </div>
          <div class="flower flower-2">
            <div class="flower-center"></div>
            <div class="flower-petal"></div>
            <div class="flower-petal"></div>
            <div class="flower-petal"></div>
            <div class="flower-petal"></div>
            <div class="flower-petal"></div>
            <div class="flower-stem"></div>
          </div>
          <div class="flower flower-3">
            <div class="flower-center"></div>
            <div class="flower-petal"></div>
            <div class="flower-petal"></div>
            <div class="flower-petal"></div>
            <div class="flower-petal"></div>
            <div class="flower-petal"></div>
            <div class="flower-stem"></div>
          </div>
          
          <!-- Herbes et fougères -->
          <div class="grass-patch grass-patch-1">
            <div class="grass-blade" v-for="i in 8" :key="`grass-1-${i}`"></div>
          </div>
          <div class="grass-patch grass-patch-2">
            <div class="grass-blade" v-for="i in 10" :key="`grass-2-${i}`"></div>
          </div>
          <div class="grass-patch grass-patch-3">
            <div class="grass-blade" v-for="i in 6" :key="`grass-3-${i}`"></div>
          </div>
          
          <div class="fern fern-1">
            <div class="fern-stem"></div>
            <div class="fern-leaf fern-leaf-1"></div>
            <div class="fern-leaf fern-leaf-2"></div>
            <div class="fern-leaf fern-leaf-3"></div>
            <div class="fern-leaf fern-leaf-4"></div>
          </div>
          <div class="fern fern-2">
            <div class="fern-stem"></div>
            <div class="fern-leaf fern-leaf-1"></div>
            <div class="fern-leaf fern-leaf-2"></div>
            <div class="fern-leaf fern-leaf-3"></div>
            <div class="fern-leaf fern-leaf-4"></div>
          </div>
        </div>
        
        <!-- Lucioles scintillantes -->
        <div class="firefly-container">
          <div v-for="i in 15" :key="`firefly-${i}`" class="firefly" :style="getFireflyStyle(i)"></div>
        </div>
      </template>
    </div>
  </div>
</template>
  
<script>
export default {
  name: 'SpaceBackground',
  props: {
    // Available themes: 'cosmic', 'ocean', 'cyberpunk', 'forest'
    theme: {
      type: String,
      default: 'cosmic',
      validator: (value) => ['cosmic', 'ocean', 'cyberpunk', 'forest'].includes(value)
    },
    animationsEnabled: {
      type: Boolean,
      default: true
    }
  },
  methods: {
    getRainDropStyle(index) {
      // Distribute raindrops evenly across the screen
      const leftPosition = (index * 3.33) % 100; // Spread across screen width
      const topPosition = Math.random() * -100; // Random starting heights
      const animationDelay = Math.random() * 1.5; // Random animation delays
      
      return {
        left: `${leftPosition}%`,
        top: `${topPosition}px`,
        animationDelay: `${animationDelay}s`
      };
    },

    getFallingLeafStyle(index) {
      const leafTypes = ['maple', 'oak', 'aspen', 'elm'];
      const leafType = leafTypes[index % leafTypes.length];
      const leftPosition = (index * 8) % 100;
      const topPosition = (index * -15) % -100;
      const animationDelay = Math.random() * 10;
      const rotationStart = Math.random() * 360;
      const scale = 0.5 + Math.random() * 0.5;
      
      return {
        left: `${leftPosition}%`,
        top: `${topPosition}px`,
        animationDelay: `${animationDelay}s`,
        transform: `rotate(${rotationStart}deg) scale(${scale})`,
        '--leaf-type': `'${leafType}'`
      };
    },
    
    getFireflyStyle() {
      const leftPosition = Math.random() * 100;
      const topPosition = Math.random() * 100;
      const size = 2 + Math.random() * 4;
      const duration = 5 + Math.random() * 10;
      const delay = Math.random() * 10;
      
      return {
        left: `${leftPosition}%`,
        top: `${topPosition}%`,
        width: `${size}px`,
        height: `${size}px`,
        animationDuration: `${duration}s`,
        animationDelay: `${delay}s`
      };
    },

    getCrowdDotStyle() {
      const leftPosition = Math.random() * 100;
      const topPosition = Math.random() * 100;
      const size = 1 + Math.random() * 2; // Petits points
      const opacity = 0.2 + Math.random() * 0.4; // Faible opacité
      const animationDelay = Math.random() * 5; // Délais variés pour le scintillement

      return {
        left: `${leftPosition}%`,
        top: `${topPosition}%`,
        width: `${size}px`,
        height: `${size}px`,
        opacity: opacity,
        animationDelay: `${animationDelay}s`
      };
    },

  }
};
</script>
  
<style scoped>
/* Variables globales */
:root {
  /* Animation communes */
  --transition-speed: 0.3s;
}

/* Styles de base pour l'arrière-plan spatial */
.space-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  overflow: hidden;
  contain: layout paint style;
}

/* Container pour tous les éléments spatiaux */
.space-elements {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 1;
  will-change: transform;
}

/* 
* STYLES DU THÈME COSMIQUE 
*/
.cosmic {
  background: radial-gradient(ellipse at center, #0f2027 0%, #090a0f 100%);
}

.cosmic::before,
.cosmic::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: block;
  background-position: 0 0;
  background-repeat: repeat;
  z-index: 0;
}

.cosmic::before {
  background-image: 
    radial-gradient(1px 1px at 10% 30%, var(--cosmic-star-color) 50%, transparent 100%),
    radial-gradient(1px 1px at 20% 70%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    radial-gradient(1px 1px at 30% 40%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
    radial-gradient(1px 1px at 40% 80%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
    radial-gradient(1px 1px at 50% 20%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    radial-gradient(1px 1px at 60% 60%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
    radial-gradient(1px 1px at 70% 10%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
    radial-gradient(1px 1px at 80% 50%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    radial-gradient(1px 1px at 90% 90%, rgba(255, 255, 255, 0.7) 50%, transparent 100%);
  background-size: 400% 400%;
  animation: starsFloat 300s linear infinite;
}

.cosmic::after {
  background-image: 
    radial-gradient(2px 2px at 15% 25%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    radial-gradient(2px 2px at 35% 65%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
    radial-gradient(2px 2px at 45% 35%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
    radial-gradient(2px 2px at 55% 75%, rgba(255, 255, 255, 0.8) 50%, transparent 100%),
    radial-gradient(2px 2px at 65% 15%, rgba(255, 255, 255, 0.7) 50%, transparent 100%),
    radial-gradient(2px 2px at 75% 55%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
    radial-gradient(2px 2px at 85% 85%, rgba(255, 255, 255, 0.8) 50%, transparent 100%);
  background-size: 200% 200%;
  animation: starsFloat 200s linear infinite, starsTwinkle 10s ease-in-out infinite alternate;
}

.crowd-container {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: 1;
  /* Ajoute un dégradé sombre sur les bords pour mieux intégrer la foule */
  mask-image: radial-gradient(ellipse at center, black 60%, transparent 95%);
  -webkit-mask-image: radial-gradient(ellipse at center, black 60%, transparent 95%);
}

/* Points lumineux de la foule */
.crowd-dot {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.7); /* Blanc légèrement transparent */
  box-shadow: 0 0 3px rgba(255, 255, 255, 0.5);
  animation: crowdShimmer 3s ease-in-out infinite alternate;
}

/* Comètes */
.comet {
  position: absolute;
  width: 4px;
  height: 4px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  box-shadow: 
    0 0 20px 2px rgba(255, 255, 255, 0.6),
    0 0 40px 6px rgba(115, 215, 255, 0.4);
  z-index: 2;
  opacity: 0;
  animation: cometAnimation 12s linear infinite;
  will-change: transform, opacity;
}

.comet::after {
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

.cometInverse {
  position: absolute;
  width: 4px;
  height: 4px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  box-shadow: 
    0 0 20px 2px rgba(255, 255, 255, 0.6),
    0 0 40px 6px rgba(115, 215, 255, 0.4);
  z-index: 2;
  opacity: 0;
  animation: cometAnimationInverse 12s linear infinite;
}

.cometInverse::after {
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

.comet-1 { top: 15%; left: -5%; animation-delay: 2s; }
.comet-2 { top: 35%; left: -10%; width: 3px; height: 3px; animation-duration: 15s; }
.comet-3 { top: 35%; left: -8%; width: 5px; height: 5px; animation-delay: 1s; animation-duration: 18s; }
.comet-4 { top: 62%; left: -18%; animation-delay: 3s; }
.comet-5 { top: 70%; left: -18%; animation-delay: 4s; }

/* Galaxie */
.galaxy {
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
  animation: galaxyPulse 15s ease-in-out infinite alternate;
  will-change: opacity, transform;
}

.galaxy::before, .galaxy::after {
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
  transform-origin: center;
  animation: galaxyRotate 80s linear infinite;
}

.galaxy::after {
  transform: rotate(180deg);
  filter: blur(8px);
  opacity: 0.5;
  animation-duration: 120s;
  animation-direction: reverse;
}

/* Planètes (style de base) */
.planet {
  position: absolute;
  border-radius: 50%;
  z-index: 3;
  box-shadow: inset -15px -15px 40px rgba(0, 0, 0, 0.5);
  will-change: transform;
}

/* Planète violette avec anneaux */
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
  animation: planetFloat 120s linear infinite;
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
  animation: ringsRotate 200s linear infinite;
}

/* Planète rouge gazeuse */
.planet-2 {
  width: 100px;
  height: 100px;
  top: 65%;
  right: 5%;
  background: radial-gradient(
    circle at 40% 40%,
    #ff6b5b 0%,
    #d32f2f 30%,
    #b71c1c 60%,
    #7f0000 100%
  );
  box-shadow: 0 0 30px rgba(255, 100, 80, 0.4);
  transform: rotate(10deg);
  animation: planetFloat2 150s linear infinite;
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
  animation: atmospherePulse 8s ease-in-out infinite alternate;
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
  animation: stormSpin 30s linear infinite;
}

/* Planète de glace */
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
  animation: planetFloat3 180s linear infinite;
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
  animation: moonsOrbit 60s linear infinite;
}

/* Lunes individuelles */
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

/* 
* STYLES DU THÈME OCÉAN
*/
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

/* Requin amélioré */
.shark {
  position: absolute;
  width: 220px;
  height: 80px;
  top: 35%;
  right: -250px;
  z-index: 4;
  animation: sharkSwimImproved 60s linear infinite;
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
  animation: sharkBodyMove 4s ease-in-out infinite;
}

/* Yeux du requin */
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

/* Branchies */
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

/* Bouche */
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

/* Nageoire dorsale */
.shark-dorsal-fin {
  position: absolute;
  width: 50px;
  height: 40px;
  background: #2c3e50;
  top: -35px;
  left: 80px;
  clip-path: polygon(0 100%, 60% 0, 100% 100%);
  z-index: 1;
  animation: sharkDorsalFinMove 3s ease-in-out infinite;
}

/* Nageoire pectorale */
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
  animation: sharkPectoralFinMove 3s ease-in-out infinite alternate;
}

/* Nageoire pelvienne */
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
  animation: sharkPelvicFinMove 3s ease-in-out infinite alternate;
  animation-delay: 0.5s;
}

/* Queue */
.shark-tail {
  position: absolute;
  width: 60px;
  height: 50px;
  top: 15px;
  right: 0;
  z-index: 2;
  animation: sharkTailWagImproved 1.5s ease-in-out infinite alternate;
}

.shark-tail-fin {
  position: absolute;
  width: 60px;
  height: 50px;
  background: #34495e;
  clip-path: polygon(0 40%, 50% 0, 50% 100%, 0 60%);
}

/* Ombre du requin */
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

/* Bulles du requin */
.shark-bubbles {
  position: absolute;
  top: 25px;
  left: 40px;
}

.shark-bubble {
  position: absolute;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  box-shadow: 0 0 5px rgba(255, 255, 255, 0.5), inset 0 0 5px rgba(255, 255, 255, 0.5);
  animation: sharkBubbleRise 3s ease-in-out infinite;
  opacity: 0;
}

.bubble-shark-1 {
  width: 8px;
  height: 8px;
  left: 0;
  animation-delay: 0s;
}

.bubble-shark-2 {
  width: 6px;
  height: 6px;
  left: 10px;
  animation-delay: 1s;
}

.bubble-shark-3 {
  width: 4px;
  height: 4px;
  left: 5px;
  animation-delay: 2s;
}

/* Animations améliorées */
@keyframes sharkSwimImproved {
  0% { 
    transform: translateX(0) translateY(0) rotate(0deg); 
    opacity: 0; 
  }
  3% { opacity: 1; }
  15% { 
    transform: translateX(-15vw) translateY(5vh) rotate(2deg);
  }
  30% { 
    transform: translateX(-30vw) translateY(-2vh) rotate(-1deg);
  }
  48% { 
    transform: translateX(-48vw) translateY(3vh) rotate(0deg);
  }
  50% {
    transform: translateX(-50vw) translateY(0);
  }
  65% { 
    transform: translateX(-65vw) translateY(-5vh) rotate(-2deg);
  }
  80% { 
    transform: translateX(-80vw) translateY(2vh) rotate(1deg);
  }
  97% { 
    transform: translateX(-97vw) translateY(-3vh) rotate(0deg);
    opacity: 1; 
  }
  100% { 
    transform: translateX(-100vw) translateY(0);
    opacity: 0; 
  }
}

@keyframes sharkBodyMove {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}

@keyframes sharkTailWagImproved {
  0% { transform: rotate(-10deg); }
  100% { transform: rotate(10deg); }
}

@keyframes sharkDorsalFinMove {
  0%, 100% { transform: rotate(0deg); }
  50% { transform: rotate(2deg); }
}

@keyframes sharkPectoralFinMove {
  0% { transform: rotate(-5deg); }
  100% { transform: rotate(15deg); }
}

@keyframes sharkPelvicFinMove {
  0% { transform: rotate(-3deg); }
  100% { transform: rotate(10deg); }
}

@keyframes sharkBubbleRise {
  0% { 
    transform: translateY(0) translateX(0); 
    opacity: 0;
  }
  10% { opacity: 0.8; }
  100% { 
    transform: translateY(-40px) translateX(-10px);
    opacity: 0;
  }
}

/* Whale */
.whale {
  position: absolute;
  width: 350px;
  height: 120px;
  top: 65%;
  left: 100px;
  z-index: 2;
  animation: whaleSwim 90s linear infinite;
  transform-style: preserve-3d;
  transform: scaleX(-1);
}

.whale-body {
  position: absolute;
  width: 300px;
  height: 100px;
  background: linear-gradient(to bottom,
    #1a3a63 0%,
    #274875 40%,
    #2c5188 70%,
    #3a5fa0 85%,
    #4a6fb0 100%);
  border-radius: 40% 60% 60% 40% / 60% 60% 40% 40%;
  box-shadow: inset 0 -10px 20px rgba(0, 0, 0, 0.3);
  transform-origin: center;
  animation: whaleBodyMove 8s ease-in-out infinite;
  z-index: 2;
}

.whale-head {
  position: absolute;
  width: 120px;
  height: 80px;
  top: 10px;
  left: -30px;
  background: #274875;
  border-radius: 40% 20% 20% 40% / 50%;
  transform: rotate(-5deg);
}

.whale-eye {
  position: absolute;
  width: 12px;
  height: 12px;
  background: #000;
  border-radius: 50%;
  top: 30px;
  left: 30px;
  z-index: 3;
}

.whale-eye::after {
  content: '';
  position: absolute;
  width: 4px;
  height: 4px;
  background: #fff;
  border-radius: 50%;
  top: 2px;
  left: 2px;
  opacity: 0.8;
}

.whale-mouth {
  position: absolute;
  width: 60px;
  height: 10px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 50%;
  top: 70px;
  left: 10px;
  transform: rotate(-5deg);
}

.whale-blowhole {
  position: absolute;
  width: 10px;
  height: 5px;
  background: rgba(0, 0, 0, 0.4);
  border-radius: 50%;
  top: 5px;
  left: 50px;
  transform: rotate(-5deg);
}

.whale-spout {
  position: absolute;
  width: 5px;
  height: 40px;
  background: linear-gradient(to top, 
    rgba(255, 255, 255, 0.8) 0%,
    rgba(200, 240, 255, 0.5) 50%,
    rgba(200, 240, 255, 0) 100%);
  top: -40px;
  left: 52px;
  filter: blur(1px);
  opacity: 0;
  animation: whaleSpout 20s ease-in-out infinite;
  z-index: 1;
}

.whale-fin {
  position: absolute;
  background: #1a3a63;
  z-index: 1;
}

.whale-fin-dorsal {
  width: 50px;
  height: 40px;
  top: -30px;
  left: 160px;
  border-radius: 80% 0 0 0;
  transform-origin: bottom right;
  animation: whaleDorsalFinMove 8s ease-in-out infinite;
}

.whale-fin-pectoral {
  width: 70px;
  height: 25px;
  top: 60px;
  left: 80px;
  border-radius: 50% 50% 0 50%;
  transform: rotate(-30deg);
  transform-origin: top left;
  animation: whalePectoralFinMove 6s ease-in-out infinite alternate;
}

.whale-fin-tail {
  width: 70px;
  height: 60px;
  top: 20px;
  right: -30px;
  border-radius: 0 50% 0 50%;
  transform-origin: left center;
  animation: whaleTailMove 4s ease-in-out infinite alternate;
}

.whale-pattern {
  position: absolute;
  width: 200px;
  height: 50px;
  top: 30px;
  left: 50px;
  background: repeating-linear-gradient(
    to bottom,
    transparent,
    transparent 5px,
    rgba(255, 255, 255, 0.1) 5px,
    rgba(255, 255, 255, 0.1) 10px
  );
  border-radius: 40% 60% 60% 40% / 60%;
  opacity: 0.5;
}

.whale-water-displacement {
  position: absolute;
  width: 400px;
  height: 30px;
  background: radial-gradient(
    ellipse at center,
    rgba(255, 255, 255, 0.3) 0%,
    rgba(255, 255, 255, 0.1) 50%,
    transparent 100%
  );
  border-radius: 50%;
  bottom: -15px;
  left: -50px;
  filter: blur(8px);
  opacity: 0.5;
  z-index: 1;
  transform: scaleX(1.5);
}

.whale-bubbles {
  position: absolute;
  top: 40px;
  right: -20px;
  z-index: 1;
}

.whale-bubble {
  position: absolute;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  box-shadow: 0 0 5px rgba(255, 255, 255, 0.5), inset 0 0 5px rgba(255, 255, 255, 0.5);
  animation: whaleBubbleRise 4s ease-in-out infinite;
  opacity: 0;
}

.bubble-whale-1 {
  width: 12px;
  height: 12px;
  right: 0;
  animation-delay: 0s;
}

.bubble-whale-2 {
  width: 8px;
  height: 8px;
  right: 15px;
  animation-delay: 0.8s;
}

.bubble-whale-3 {
  width: 6px;
  height: 6px;
  right: 5px;
  top: 10px;
  animation-delay: 1.6s;
}

.bubble-whale-4 {
  width: 10px;
  height: 10px;
  right: 20px;
  top: -5px;
  animation-delay: 2.4s;
}

.bubble-whale-5 {
  width: 7px;
  height: 7px;
  right: 10px;
  top: 15px;
  animation-delay: 3.2s;
}

/* Whale animations */
@keyframes whaleSwim {
  0% {
    transform: translateX(calc(100vw + 100px)) translateY(0);
    opacity: 0;
  }
  5% {
    transform: translateX(calc(100vw)) translateY(0);
    opacity: 1;
  }
  45% {
    transform: translateX(200px) translateY(-50px);
  }
  48% {
    transform: translateX(150px) translateY(-30px);
    opacity: 1;
  }
  50% {
    transform: translateX(0) translateY(0);
    opacity: 0;
  }
  100% {
    transform: translateX(0) translateY(0);
    opacity: 0;
  }
}

@keyframes whaleBodyMove {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}

@keyframes whaleDorsalFinMove {
  0%, 100% { transform: rotate(0deg); }
  50% { transform: rotate(-5deg); }
}

@keyframes whalePectoralFinMove {
  0% { transform: rotate(-20deg); }
  100% { transform: rotate(-40deg); }
}

@keyframes whaleTailMove {
  0% { transform: rotate(-10deg); }
  100% { transform: rotate(10deg); }
}

@keyframes whaleSpout {
  0%, 90%, 100% { 
    height: 0;
    opacity: 0;
  }
  92% {
    height: 40px;
    opacity: 0.8;
  }
  96% {
    height: 60px;
    opacity: 0.5;
  }
  98% {
    height: 70px;
    opacity: 0.2;
  }
}

@keyframes whaleBubbleRise {
  0% {
    transform: translateY(0) translateX(0);
    opacity: 0;
  }
  10% {
    opacity: 0.8;
  }
  100% {
    transform: translateY(-60px) translateX(-20px);
    opacity: 0;
  }
}

/* Rayons de lumière */
.light-ray {
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
  animation: lightRayFlicker 8s ease-in-out infinite alternate;
  will-change: opacity;
}

.light-ray-1 { left: 25%; transform: rotate(20deg) translateX(-50%); }
.light-ray-2 { left: 60%; transform: rotate(-15deg) translateX(-50%); animation-delay: 2s; }
.light-ray-3 { left: 80%; width: 100px; transform: rotate(-25deg) translateX(-50%); animation-delay: 4s; }

/* Bulles */
.bubble {
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
  animation: bubbleRise 15s ease-in infinite;
  opacity: 0;
  z-index: 3;
  backdrop-filter: blur(2px);
  will-change: transform, opacity;
}

.bubble::after {
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
.bubble-1, .bubble-6 { width: 30px; height: 30px; }
.bubble-2, .bubble-9 { width: 20px; height: 20px; }
.bubble-3, .bubble-10 { width: 40px; height: 40px; }
.bubble-4, .bubble-11 { width: 15px; height: 15px; }
.bubble-5, .bubble-12 { width: 25px; height: 25px; }
.bubble-7 { width: 18px; height: 18px; }
.bubble-8 { width: 22px; height: 22px; }

/* Positionnement des bulles avec délais variés */
.bubble { bottom: calc(-1 * var(--size, 20px)); }
.bubble-1 { left: 20%; --size: 30px; animation-delay: 0s; }
.bubble-2 { left: 35%; --size: 20px; animation-delay: 3s; }
.bubble-3 { left: 55%; --size: 40px; animation-delay: 6s; }
.bubble-4 { left: 70%; --size: 15px; animation-delay: 9s; }
.bubble-5 { left: 85%; --size: 25px; animation-delay: 12s; }
.bubble-6 { left: 45%; --size: 35px; animation-delay: 15s; }
.bubble-7 { left: 25%; --size: 18px; animation-delay: 18s; }
.bubble-8 { left: 15%; --size: 22px; animation-delay: 4s; }
.bubble-9 { left: 40%; --size: 28px; animation-delay: 8s; }
.bubble-10 { left: 60%; --size: 32px; animation-delay: 11s; }
.bubble-11 { left: 75%; --size: 14px; animation-delay: 7s; }
.bubble-12 { left: 90%; --size: 24px; animation-delay: 14s; }

/* Particules de plancton */
.plankton-container {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 2;
}

.plankton {
  position: absolute;
  width: 2px;
  height: 2px;
  background: rgba(210, 230, 255, 0.6);
  border-radius: 50%;
  filter: blur(1px);
  animation: planktonFloat 20s linear infinite;
}

.plankton:nth-child(4n+1) { background: rgba(180, 220, 255, 0.5); }
.plankton:nth-child(4n+2) { background: rgba(150, 210, 255, 0.4); }
.plankton:nth-child(4n+3) { background: rgba(120, 200, 255, 0.6); }

/* Positionnement du plancton avec des délais variés */
.plankton:nth-child(1) { top: 10%; left: 15%; animation-delay: 0s; }
.plankton:nth-child(2) { top: 20%; left: 25%; animation-delay: 1s; }
.plankton:nth-child(3) { top: 30%; left: 35%; animation-delay: 2s; }
.plankton:nth-child(4) { top: 40%; left: 45%; animation-delay: 3s; }
.plankton:nth-child(5) { top: 50%; left: 55%; animation-delay: 4s; }
/* Pour la suite, on peut utiliser nth-child de manière systématique */

/* Coraux */
.coral {
  position: absolute;
  bottom: 0;
  z-index: 2;
  transform-origin: bottom center;
  animation: coralSway 8s ease-in-out infinite alternate;
}

.coral-1 {
  width: 150px;
  height: 120px;
  right: 10%;
}

.coral-2 {
  width: 180px;
  height: 150px;
  left: 5%;
  animation-delay: 3s;
}

.coral-branch {
  position: absolute;
  bottom: 0;
  border-radius: 50% 50% 0 0;
  filter: blur(1px);
  transform-origin: bottom center;
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

/* Dimensions et positions des branches de corail */
.coral-1 .branch-1 { width: 40px; height: 100px; left: 20px; animation: coralBranchSway 10s ease-in-out infinite alternate; }
.coral-1 .branch-2 { width: 60px; height: 120px; left: 70px; animation: coralBranchSway 12s ease-in-out infinite alternate; animation-delay: 1s; }
.coral-1 .branch-3 { width: 50px; height: 90px; left: 40px; animation: coralBranchSway 9s ease-in-out infinite alternate; animation-delay: 2s; }

.coral-2 .branch-1 { width: 70px; height: 130px; left: 30px; animation: coralBranchSway 11s ease-in-out infinite alternate; }
.coral-2 .branch-2 { width: 50px; height: 100px; left: 100px; animation: coralBranchSway 13s ease-in-out infinite alternate; animation-delay: 2s; }

/* Bancs de poissons */
.fish-school {
  position: absolute;
  width: 200px;
  height: 100px;
  z-index: 3;
  animation: schoolSwim 30s linear infinite;
}

.fish-school-1 {
  top: 25%;
  left: -200px;
}

.fish-school-2 {
  top: 55%;
  left: -200px;
  animation-delay: 12s;
}

.school-fish {
  position: absolute;
  width: 15px;
  height: 8px;
  border-radius: 50% 60% 60% 50% / 50%;
  transform: skew(-30deg);
  animation: schoolFishMove 5s ease-in-out infinite;
}

.fish-school-1 .school-fish { background: rgba(100, 180, 255, 0.7); }
.fish-school-2 .school-fish { background: rgba(180, 210, 255, 0.7); }

/* Positions des poissons dans les bancs */
.fish-school-1 .school-fish:nth-child(8n+1) { top: 10%; left: 20%; animation-delay: 0s; }
.fish-school-1 .school-fish:nth-child(8n+2) { top: 40%; left: 30%; animation-delay: 0.2s; }
.fish-school-1 .school-fish:nth-child(8n+3) { top: 70%; left: 25%; animation-delay: 0.4s; }
.fish-school-1 .school-fish:nth-child(8n+4) { top: 25%; left: 60%; animation-delay: 0.6s; }
.fish-school-1 .school-fish:nth-child(8n+5) { top: 55%; left: 70%; animation-delay: 0.8s; }
.fish-school-1 .school-fish:nth-child(8n+6) { top: 15%; left: 80%; animation-delay: 1.0s; }
.fish-school-1 .school-fish:nth-child(8n+7) { top: 45%; left: 50%; animation-delay: 1.2s; }
.fish-school-1 .school-fish:nth-child(8n+8) { top: 65%; left: 45%; animation-delay: 1.4s; }

.fish-school-2 .school-fish:nth-child(8n+1) { top: 20%; left: 10%; animation-delay: 0s; }
.fish-school-2 .school-fish:nth-child(8n+2) { top: 50%; left: 20%; animation-delay: 0.2s; }
.fish-school-2 .school-fish:nth-child(8n+3) { top: 80%; left: 15%; animation-delay: 0.4s; }
.fish-school-2 .school-fish:nth-child(8n+4) { top: 35%; left: 50%; animation-delay: 0.6s; }
.fish-school-2 .school-fish:nth-child(8n+5) { top: 65%; left: 60%; animation-delay: 0.8s; }
.fish-school-2 .school-fish:nth-child(8n+6) { top: 25%; left: 70%; animation-delay: 1.0s; }
.fish-school-2 .school-fish:nth-child(8n+7) { top: 55%; left: 40%; animation-delay: 1.2s; }
.fish-school-2 .school-fish:nth-child(8n+8) { top: 75%; left: 35%; animation-delay: 1.4s; }


/* Poissons individuels */
.fish {
  position: absolute;
  z-index: 3;
  border-radius: 70% 30% 30% 70% / 50%;
  animation: fishSwim 25s linear infinite;
  will-change: transform;
}

.fish-1 {
  width: 40px;
  height: 20px;
  top: 30%;
  left: -40px;
  background: linear-gradient(to right, 
    rgba(50, 150, 255, 0.9) 0%, 
    rgba(0, 191, 255, 0.8) 60%, 
    rgba(0, 191, 255, 0.4) 100%);
}

.fish-2 {
  width: 30px;
  height: 15px;
  top: 45%;
  left: -40px;
  background: linear-gradient(to right, 
    rgba(255, 165, 0, 0.9) 0%, 
    rgba(255, 165, 0, 0.8) 60%, 
    rgba(255, 165, 0, 0.4) 100%);
  animation-delay: 5s;
}

.fish-3 {
  width: 50px;
  height: 25px;
  top: 60%;
  left: -60px;
  background: linear-gradient(to right, 
    rgba(255, 105, 180, 0.9) 0%, 
    rgba(255, 105, 180, 0.8) 60%, 
    rgba(255, 105, 180, 0.4) 100%);
  animation-delay: 10s;
}

.fish-4 {
  width: 45px;
  height: 22px;
  top: 75%;
  left: -55px;
  background: linear-gradient(to right, 
    rgba(120, 220, 255, 0.9) 0%, 
    rgba(100, 200, 240, 0.8) 60%, 
    rgba(80, 180, 220, 0.4) 100%);
  animation-delay: 15s;
}

.fish-tail {
  position: absolute;
  width: 15px;
  height: 100%;
  top: 0;
  right: -8px;
  background: inherit;
  border-radius: 0 50% 50% 0 / 50%;
  transform-origin: left center;
  animation: fishTailWag 0.6s ease-in-out infinite alternate;
  will-change: transform;
}

/* Algues */
.seaweed {
  position: absolute;
  z-index: 1;
  display: flex;
  justify-content: space-around;
  transform-origin: bottom center;
  bottom: 0;
}

.seaweed-1 { width: 100px; height: 150px; left: 15%; }
.seaweed-2 { width: 80px; height: 120px; left: 60%; }
.seaweed-3 { width: 120px; height: 180px; left: 35%; }

.seaweed-strand {
  width: 18px;
  height: 100%;
  background: linear-gradient(to top, 
    rgba(34, 139, 34, 0.9) 0%, 
    rgba(50, 160, 50, 0.7) 50%, 
    rgba(70, 190, 70, 0.4) 100%);
  border-radius: 50% 50% 0 0;
  transform-origin: bottom center;
  position: relative;
  animation: seaweedSway 10s ease-in-out infinite alternate;
  will-change: transform;
}

.seaweed-strand::after {
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

/* Délais d'animation pour les algues */
.seaweed-1 .seaweed-strand:nth-child(1) { animation-delay: 0s; }
.seaweed-1 .seaweed-strand:nth-child(2) { animation-delay: 1.5s; }
.seaweed-1 .seaweed-strand:nth-child(3) { animation-delay: 3s; }
.seaweed-2 .seaweed-strand:nth-child(1) { animation-delay: 2s; }
.seaweed-2 .seaweed-strand:nth-child(2) { animation-delay: 4s; }
.seaweed-3 .seaweed-strand:nth-child(1) { animation-delay: 1s; }
.seaweed-3 .seaweed-strand:nth-child(2) { animation-delay: 2.5s; }
.seaweed-3 .seaweed-strand:nth-child(3) { animation-delay: 4s; }
.seaweed-3 .seaweed-strand:nth-child(4) { animation-delay: 5.5s; }

/* Méduses */
.jellyfish {
  position: absolute;
  z-index: 3;
  animation: jellyfishFloat 30s ease-in-out infinite;
}

.jellyfish-1 {
  top: 20%;
  right: 20%;
}

.jellyfish-2 {
  top: 40%;
  left: 30%;
  animation-delay: 15s;
}

.jellyfish-head {
  width: 50px;
  height: 40px;
  background: radial-gradient(
    ellipse at 50% 40%, 
    rgba(255, 100, 255, 0.8) 0%, 
    rgba(200, 100, 255, 0.6) 50%, 
    rgba(150, 100, 255, 0.4) 100%);
  border-radius: 50% 50% 45% 45%;
  box-shadow: 0 0 15px rgba(200, 150, 255, 0.5);
  animation: jellyfishPulse 2s ease-in-out infinite alternate;
}

.jellyfish-tentacles {
  position: absolute;
  top: 35px;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 60px;
}

.tentacle {
  position: absolute;
  top: 0;
  width: 4px;
  height: 50px;
  background: linear-gradient(to bottom, 
    rgba(255, 100, 255, 0.8) 0%, 
    rgba(200, 100, 255, 0.5) 50%, 
    rgba(150, 100, 255, 0.2) 100%);
  border-radius: 4px;
  animation: tentacleWave 3s ease-in-out infinite;
}

.tentacle:nth-child(5n+1) { left: 10%; animation-delay: 0s; }
.tentacle:nth-child(5n+2) { left: 30%; animation-delay: 0.6s; }
.tentacle:nth-child(5n+3) { left: 50%; animation-delay: 1.2s; }
.tentacle:nth-child(5n+4) { left: 70%; animation-delay: 1.8s; }
.tentacle:nth-child(5n+5) { left: 90%; animation-delay: 2.4s; }

/* Fond marin */
.sea-floor {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 30px;
  z-index: 1;
}

.sand-dune {
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

/* 
* STYLES DU THÈME CYBERPUNK
*/
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

/* Effet de pluie */
.cyber-rain {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: 3;
  pointer-events: none;
}

.rain-drop {
  position: absolute;
  top: -100px;
  width: 1px;
  height: 30px;
  background: linear-gradient(to bottom, 
    rgba(0, 255, 255, 0) 0%, 
    rgba(0, 255, 255, 0.6) 50%, 
    rgba(0, 255, 255, 0) 100%);
  animation: rainFall 1.5s linear infinite;
  will-change: transform;
}

.rain-drop:nth-child(3n) {
  background: linear-gradient(to bottom, 
    rgba(255, 0, 128, 0) 0%, 
    rgba(255, 0, 128, 0.5) 50%, 
    rgba(255, 0, 128, 0) 100%);
}

/* Enseignes néon */
.neon-sign {
  position: absolute;
  font-family: 'Orbitron', sans-serif;
  font-weight: bold;
  letter-spacing: 2px;
  z-index: 5;
  animation: neonFlicker 3s infinite alternate;
  will-change: opacity;
}

.neon-sign-1 {
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

.neon-sign-2 {
  top: 40%;
  left: 5%;
  font-size: 18px;
  color: #00ffff;
  text-shadow: 
    0 0 5px #00ffff, 
    0 0 10px #00ffff, 
    0 0 15px #00ffff, 
    0 0 20px #00ffff;
  animation-delay: 1s;
}

.neon-sign-3 {
  bottom: 15%;
  right: 40%;
  font-size: 20px;
  color: #ff8800;
  text-shadow: 
    0 0 5px #ff8800, 
    0 0 10px #ff8800, 
    0 0 15px #ff8800, 
    0 0 20px #ff8800;
  animation-delay: 2s;
}

/* Grille 3D améliorée */
.grid-container {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  perspective: 1000px;
  transform-style: preserve-3d;
  animation: gridRotate 60s linear infinite;
  z-index: 3;
  will-change: transform;
}

.grid-horizontal, .grid-vertical {
  position: absolute;
  background: rgba(0, 255, 255, 0.15);
}

.grid-horizontal {
  width: 200%;
  height: 1px;
  left: -50%;
  transform: translateZ(calc(var(--i, 0) * 50px));
}

.grid-vertical {
  height: 200%;
  width: 1px;
  top: -50%;
  transform: translateZ(calc(var(--i, 0) * 50px));
}

.grid-horizontal:nth-child(odd), 
.grid-vertical:nth-child(odd) {
  background: rgba(255, 0, 128, 0.15);
  box-shadow: 0 0 15px rgba(255, 0, 128, 0.5);
}

/* Silhouette de ville */
.cyber-city {
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

.city-building {
  position: relative;
  bottom: 0;
  width: calc(100% / 8);
  background: linear-gradient(to top, 
    rgba(0, 0, 20, 0.9) 0%, 
    rgba(20, 20, 40, 0.8) 100%);
  animation: buildingLights 4s infinite alternate;
  will-change: background;
}

.city-building::before {
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
  animation: buildingWindowsScroll 30s linear infinite;
}

/* Hauteurs variées pour les bâtiments */
.city-building:nth-child(8n+1) { height: 65%; animation-delay: 0.1s; }
.city-building:nth-child(8n+2) { height: 85%; animation-delay: 0.2s; }
.city-building:nth-child(8n+3) { height: 70%; animation-delay: 0.3s; }
.city-building:nth-child(8n+4) { height: 90%; animation-delay: 0.4s; }
.city-building:nth-child(8n+5) { height: 60%; animation-delay: 0.5s; }
.city-building:nth-child(8n+6) { height: 80%; animation-delay: 0.6s; }
.city-building:nth-child(8n+7) { height: 75%; animation-delay: 0.7s; }
.city-building:nth-child(8n+8) { height: 95%; animation-delay: 0.8s; }

/* Cubes de données améliorés */
.data-cube {
  position: absolute;
  width: 40px;
  height: 40px;
  transform-style: preserve-3d;
  animation: cubeFly 20s linear infinite;
  z-index: 4;
  will-change: transform;
}

.data-cube-1 {
  top: 30%;
  left: -50px;
}

.data-cube-2 {
  top: 50%;
  left: -50px;
  animation-delay: 5s;
}

.data-cube-3 {
  top: 70%;
  left: -50px;
  animation-delay: 10s;
}

.cube-face {
  position: absolute;
  width: 40px;
  height: 40px;
  background: rgba(255, 0, 128, 0.2);
  border: 1px solid rgba(255, 0, 128, 0.8);
  box-shadow: 0 0 20px rgba(255, 0, 128, 0.5);
}

.data-cube:nth-child(even) .cube-face {
  background: rgba(0, 255, 255, 0.2);
  border: 1px solid rgba(0, 255, 255, 0.8);
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
}

/* Positionnement des faces du cube */
.cube-face:nth-child(1) { transform: translateZ(20px); }
.cube-face:nth-child(2) { transform: rotateX(180deg) translateZ(20px); }
.cube-face:nth-child(3) { transform: rotateY(90deg) translateZ(20px); }
.cube-face:nth-child(4) { transform: rotateY(-90deg) translateZ(20px); }
.cube-face:nth-child(5) { transform: rotateX(90deg) translateZ(20px); }
.cube-face:nth-child(6) { transform: rotateX(-90deg) translateZ(20px); }

/* Flux de données */
.data-stream {
  position: absolute;
  height: 3px;
  background: linear-gradient(to right, 
    rgba(0, 255, 255, 0) 0%, 
    rgba(0, 255, 255, 0.8) 50%, 
    rgba(0, 255, 255, 0) 100%);
  z-index: 3;
  animation: dataStreamPulse 8s infinite;
}

.data-stream-1 {
  width: 60%;
  top: 25%;
  left: -10%;
  transform: rotate(10deg);
}

.data-stream-2 {
  width: 40%;
  top: 45%;
  right: -5%;
  transform: rotate(-15deg);
  animation-delay: 1.5s;
}

.data-stream-3 {
  width: 70%;
  bottom: 35%;
  left: -5%;
  transform: rotate(5deg);
  animation-delay: 3s;
}

/* Circuits améliorés */
.circuit {
  position: absolute;
  height: 2px;
  background: linear-gradient(to right, 
    rgba(0, 255, 255, 0) 0%, 
    rgba(0, 255, 255, 1) 50%, 
    rgba(0, 255, 255, 0) 100%);
  z-index: 3;
  animation: circuitPulse 8s infinite alternate;
}

.circuit-1 {
  width: 30%;
  top: 20%;
  left: 10%;
  transform: rotate(30deg);
}

.circuit-2 {
  width: 40%;
  bottom: 30%;
  right: 5%;
  transform: rotate(-15deg);
  animation-delay: 2.5s;
}

.circuit-node {
  position: absolute;
  width: 6px;
  height: 6px;
  background: rgba(0, 255, 255, 0.8);
  border-radius: 50%;
  top: 50%;
  transform: translateY(-50%);
  animation: nodeFlash 2s ease-in-out infinite alternate;
}

/* Positions des nœuds de circuit */
.circuit-1 .circuit-node:nth-child(3n+1) { left: 10%; animation-delay: 0.2s; }
.circuit-1 .circuit-node:nth-child(3n+2) { left: 50%; animation-delay: 0.6s; }
.circuit-1 .circuit-node:nth-child(3n+3) { left: 90%; animation-delay: 1.0s; }

.circuit-2 .circuit-node:nth-child(4n+1) { left: 5%; animation-delay: 0.1s; }
.circuit-2 .circuit-node:nth-child(4n+2) { left: 35%; animation-delay: 0.5s; }
.circuit-2 .circuit-node:nth-child(4n+3) { left: 65%; animation-delay: 0.9s; }
.circuit-2 .circuit-node:nth-child(4n+4) { left: 95%; animation-delay: 1.3s; }

/* Hologrammes améliorés */
.hologram {
  position: absolute;
  border-radius: 5px;
  z-index: 4;
  animation: hologramFlicker 5s infinite alternate;
}

.hologram-1 {
  width: 120px;
  height: 80px;
  top: 30%;
  right: 15%;
}

.hologram-3 {
  width: 100px;
  height: 100px;
  top: 15%;
  left: 40%;
  animation-delay: 0.7s;
}

.hologram-content {
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

.hologram-line {
  height: 2px;
  background: rgba(0, 255, 255, 0.5);
  animation: hologramLineScan 2s infinite linear;
}

.hologram-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  border: 1px solid rgba(0, 255, 255, 0.5);
  animation: hologramRingExpand 3s infinite;
}

.hologram-3 .hologram-ring:nth-child(1) { animation-delay: 0s; }
.hologram-3 .hologram-ring:nth-child(2) { animation-delay: 1s; }

/* Overlay glitch */
.glitch-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    rgba(255, 0, 128, 0.03) 50%, 
    rgba(0, 255, 255, 0.03) 50%
  );
  background-size: 100% 4px;
  z-index: 10;
  pointer-events: none;
  opacity: 0.3;
  animation: glitchEffect 10s infinite;
}

/* 
* STYLES DU THÈME FORÊT
*/
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

/* Rayons de soleil */
.sunbeam {
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
  animation: sunbeamFlicker 12s ease-in-out infinite alternate;
  will-change: opacity;
}

.sunbeam-1 { left: 25%; transform: rotate(20deg) translateX(-50%); }
.sunbeam-2 { left: 60%; transform: rotate(-15deg) translateX(-50%); animation-delay: 3s; }
.sunbeam-3 { left: 80%; width: 60px; transform: rotate(-25deg) translateX(-50%); animation-delay: 6s; }

/* Brouillard forestier */
.forest-mist {
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
  animation: mistFloat 30s ease-in-out infinite alternate;
  will-change: transform;
}

.forest-mist-1 { bottom: 25%; left: -10%; height: 20%; }
.forest-mist-2 { bottom: 5%; left: 30%; height: 15%; animation-delay: 5s; }
.forest-mist-3 { bottom: 15%; left: -20%; height: 30%; animation-delay: 10s; }

/* Feuilles qui tombent */
.leaves-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 4;
  pointer-events: none;
}

.falling-leaf {
  position: absolute;
  width: 25px;
  height: 25px;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  opacity: 0.8;
  animation: leafFall 15s linear infinite;
  will-change: transform, opacity;
  top: -20px;
}

/* Types de feuilles */
.falling-leaf:nth-child(4n+1) {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath fill='%2374a12e' d='M50,0 C60,30 80,50 100,50 C80,60 60,80 50,100 C40,80 20,60 0,50 C20,50 40,30 50,0'/%3E%3C/svg%3E");
}

.falling-leaf:nth-child(4n+2) {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath fill='%2392b93b' d='M20,0 C60,15 80,40 100,50 C80,70 60,90 50,100 C25,90 10,70 0,50 C10,35 15,15 20,0'/%3E%3C/svg%3E");
}

.falling-leaf:nth-child(4n+3) {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath fill='%235a8a23' d='M50,0 C70,20 90,40 100,50 C70,70 60,90 50,100 C40,80 20,60 0,50 C10,40 30,20 50,0'/%3E%3C/svg%3E");
}

.falling-leaf:nth-child(4n+4) {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath fill='%23aec74a' d='M30,0 C60,20 90,30 100,50 C90,70 70,90 50,100 C30,70 10,40 0,50 C20,30 25,10 30,0'/%3E%3C/svg%3E");
}

.falling-leaf:nth-child(3n) { animation-duration: 18s; }
.falling-leaf:nth-child(3n+1) { animation-duration: 12s; }

/* Couches d'arbres */
.tree-layer {
  position: absolute;
  width: 100%;
  bottom: 0;
  left: 0;
  z-index: 2;
}

.tree-layer-bg {
  height: 70%;
  filter: blur(2px);
  opacity: 0.7;
  z-index: 1;
}

.tree-layer-fg {
  height: 85%;
  z-index: 3;
}

/* Arbres */
.tree {
  position: absolute;
  bottom: 0;
}

.tree-trunk {
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

.tree-canopy {
  position: absolute;
  border-radius: 50%;
  z-index: 2;
}

/* Propriétés pour différents arbres */
.tree-bg-1 { left: 5%; height: 75%; width: 150px; }
.tree-bg-1 .tree-trunk { width: 18px; height: 30%; }
.tree-bg-1 .tree-canopy {
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

.tree-bg-2 { left: 25%; height: 65%; width: 120px; }
.tree-bg-2 .tree-trunk { width: 15px; height: 35%; }
.tree-bg-2 .tree-canopy {
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

.tree-bg-3 { left: 45%; height: 80%; width: 140px; }
.tree-bg-3 .tree-trunk { width: 20px; height: 25%; }
.tree-bg-3 .tree-canopy {
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

.tree-bg-4 { left: 65%; height: 70%; width: 130px; }
.tree-bg-4 .tree-trunk { width: 16px; height: 30%; }
.tree-bg-4 .tree-canopy {
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

.tree-bg-5 { left: 85%; height: 75%; width: 140px; }
.tree-bg-5 .tree-trunk { width: 18px; height: 25%; }
.tree-bg-5 .tree-canopy {
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

.tree-fg-1 { left: 60%; height: 85%; width: 160px; }
.tree-fg-1 .tree-trunk { width: 20px; height: 35%; }
.tree-fg-1 .tree-canopy {
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

.tree-fg-2 { left: 30%; height: 70%; width: 150px; }
.tree-fg-2 .tree-trunk { width: 18px; height: 30%; }
.tree-fg-2 .tree-canopy {
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

/* Les autres arbres suivent le même modèle... */

/* Papillons */
.butterfly {
  position: absolute;
  width: 20px;
  height: 20px;
  z-index: 4;
  animation: butterflyFlight 30s linear infinite;
  will-change: transform, opacity;
}

.butterfly-1 { top: 30%; left: -20px; }
.butterfly-2 { top: 45%; left: -20px; animation-delay: 5s; }
.butterfly-3 { top: 60%; left: -20px; animation-delay: 10s; }

.butterfly-wing {
  position: absolute;
  width: 10px;
  height: 15px;
  border-radius: 100% 100% 0 100%;
  transform-origin: 100% 50%;
}

.butterfly-1 .butterfly-wing { background: linear-gradient(to bottom, #ff9933, #ffcc00); }
.butterfly-2 .butterfly-wing { background: linear-gradient(to bottom, #66ccff, #99ffff); }
.butterfly-3 .butterfly-wing { background: linear-gradient(to bottom, #ff66b3, #ff99cc); }

.wing-left {
  left: 0;
  transform: scaleX(-1) rotate(-30deg);
  animation: wingBeatLeft 0.3s ease-in-out infinite alternate;
  will-change: transform;
}

.wing-right {
  right: 0;
  transform: rotate(30deg);
  animation: wingBeatRight 0.3s ease-in-out infinite alternate;
  will-change: transform;
}

/* Oiseaux */
.bird {
  position: absolute;
  width: 30px;
  height: 8px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 30'%3E%3Cpath fill='%23333' d='M50,0 C40,0 25,15 0,20 C25,25 40,30 50,30 C60,30 75,25 100,20 C75,15 60,0 50,0'/%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  z-index: 4;
  animation: birdFlight 40s linear infinite;
  will-change: transform, opacity;
}

.bird-1 { top: 20%; left: -30px; }
.bird-2 { top: 15%; left: -30px; animation-delay: 15s; }
.bird-3 { top: 25%; left: -30px; animation-delay: 30s; }

/* Éléments du sol forestier */
.forest-floor {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 20%;
  z-index: 3;
}

/* Champignons */
.mushroom {
  position: absolute;
  bottom: 0;
  z-index: 4;
}

.mushroom-1 { left: 38%; height: 40px; }
.mushroom-2 { left: 65%; height: 35px; }
.mushroom-3 { left: 25%; height: 45px; }

.mushroom-cap {
  position: absolute;
  width: 30px;
  height: 15px;
  border-radius: 100% 100% 0 0;
  bottom: 15px;
  left: 50%;
  transform: translateX(-50%);
}

.mushroom-stem {
  position: absolute;
  width: 10px;
  height: 20px;
  background: #f5e9d9;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 30% 30% 0 0;
}

.mushroom-1 .mushroom-cap { background: linear-gradient(to bottom, #e05d5d, #b33f3f); }
.mushroom-2 .mushroom-cap { background: linear-gradient(to bottom, #e08a5d, #b36a3f); }
.mushroom-3 .mushroom-cap { background: linear-gradient(to bottom, #5d9de0, #3f7db3); }

/* Fleurs */
.flower {
  position: absolute;
  bottom: 0;
  z-index: 3;
}

.flower-1 { left: 50%; height: 50px; }
.flower-2 { left: 75%; height: 45px; }
.flower-3 { left: 15%; height: 40px; }

.flower-center {
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

.flower-petal {
  position: absolute;
  width: 12px;
  height: 15px;
  border-radius: 50%;
  bottom: 30px;
  left: 50%;
  transform-origin: center bottom;
  z-index: 1;
}

.flower-petal:nth-child(2) { transform: translateX(-50%) rotate(0deg); }
.flower-petal:nth-child(3) { transform: translateX(-50%) rotate(72deg); }
.flower-petal:nth-child(4) { transform: translateX(-50%) rotate(144deg); }
.flower-petal:nth-child(5) { transform: translateX(-50%) rotate(216deg); }
.flower-petal:nth-child(6) { transform: translateX(-50%) rotate(288deg); }

.flower-stem {
  position: absolute;
  width: 3px;
  height: 30px;
  background: #5c9e31;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
}

.flower-1 .flower-petal { background: linear-gradient(to bottom, #ff80bf, #ff1a8c); }
.flower-2 .flower-petal { background: linear-gradient(to bottom, #80bfff, #1a8cff); }
.flower-3 .flower-petal { background: linear-gradient(to bottom, #ffbf80, #ff8c1a); }

/* Herbes */
.grass-patch {
  position: absolute;
  bottom: 0;
  width: 80px;
  height: 40px;
  z-index: 3;
}

.grass-patch-1 { left: 5%; }
.grass-patch-2 { left: 30%; }
.grass-patch-3 { left: 60%; }

.grass-blade {
  position: absolute;
  bottom: 0;
  width: 5px;
  height: 30px;
  background: linear-gradient(to top, #5c9e31, #7bc143);
  border-radius: 0 100% 0 0;
  transform-origin: bottom center;
  animation: grassSway 3s ease-in-out infinite alternate;
  will-change: transform;
}

/* Fougères */
.fern {
  position: absolute;
  bottom: 0;
  height: 60px;
  width: 50px;
  z-index: 3;
}

.fern-1 { left: 40%; }
.fern-2 { left: 85%; }

.fern-stem {
  position: absolute;
  width: 3px;
  height: 100%;
  background: var(--forest-green-dark);
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
}

.fern-leaf {
  position: absolute;
  width: 20px;
  height: 10px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 50'%3E%3Cpath fill='%235c9e31' d='M0,0 C20,10 40,25 60,20 C80,15 90,0 100,0 C100,10 80,40 60,45 C40,50 20,30 0,50 L0,0'/%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
  left: 50%;
  transform-origin: left center;
}

.fern-leaf-1 { top: 10%; transform: translateX(0) rotate(-30deg); }
.fern-leaf-2 { top: 30%; transform: translateX(0) rotate(-20deg); }
.fern-leaf-3 { top: 50%; transform: translateX(0) scaleX(-1) rotate(20deg); }
.fern-leaf-4 { top: 70%; transform: translateX(0) scaleX(-1) rotate(30deg); }

/* Lucioles */
.firefly-container {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: 5;
  pointer-events: none;
}

.firefly {
  position: absolute;
  width: 4px;
  height: 4px;
  background: #ffff99;
  border-radius: 50%;
  filter: blur(1px);
  box-shadow: 0 0 10px 2px rgba(255, 255, 153, 0.8);
  animation: fireflyGlow 3s ease-in-out infinite alternate, fireflyHover 20s linear infinite;
  will-change: opacity, transform;
}

.animations-disabled * {
  animation-play-state: paused !important;
  transition: none !important;
}

/* Optionnel: Style pour les éléments qui devraient être complètement figés */
.animations-disabled .space-elements * {
  animation: none !important;
  transform: none !important;
}


/* 
* ANIMATIONS 
*/

/* Animations communes */
@keyframes fadeInOut {
  0%, 100% { opacity: 0; }
  50% { opacity: 1; }
}

/* Animations du thème Cosmic */
@keyframes starsFloat {
  0% { background-position: 0% 0%; }
  100% { background-position: 100% 100%; }
}

@keyframes starsTwinkle {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 1; }
}

@keyframes cometAnimation {
  0% {
    transform: translate(0, 0) rotate(5deg);
    opacity: 0;
  }
  5% { opacity: 1; }
  95% { opacity: 1; }
  100% {
    transform: translate(calc(100vw + 200px), 20vh) rotate(5deg);
    opacity: 0;
  }
}

@keyframes cometAnimationInverse {
  0% {
    transform: translate(calc(100vw + 200px), 20vh) rotate(185deg);
    opacity: 0;
  }
  5% { opacity: 1; }
  95% { opacity: 1; }
  100% {
    transform: translate(0, 0) rotate(185deg);
    opacity: 0;
  }
}

@keyframes galaxyPulse {
  0% { transform: rotate(-25deg) scale(1); opacity: 0.7; }
  50% { transform: rotate(-25deg) scale(1.05); opacity: 0.8; }
  100% { transform: rotate(-25deg) scale(1); opacity: 0.7; }
}

@keyframes galaxyRotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes planetFloat {
  0% { transform: translate(0, 0) rotate(-15deg); }
  25% { transform: translate(-10px, 15px) rotate(-15deg); }
  50% { transform: translate(-5px, 25px) rotate(-15deg); }
  75% { transform: translate(5px, 15px) rotate(-15deg); }
  100% { transform: translate(0, 0) rotate(-15deg); }
}

@keyframes ringsRotate {
  0% { transform: translate(-50%, -50%) rotate(-15deg); }
  100% { transform: translate(-50%, -50%) rotate(345deg); }
}

@keyframes planetFloat2 {
  0% { transform: translate(0, 0) rotate(10deg); }
  25% { transform: translate(-30px, 20px) rotate(10deg); }
  50% { transform: translate(-60px, 0) rotate(10deg); }
  75% { transform: translate(-30px, -20px) rotate(10deg); }
  100% { transform: translate(0, 0) rotate(10deg); }
}

@keyframes atmospherePulse {
  0% { opacity: 0.6; transform: scale(1); }
  100% { opacity: 0.9; transform: scale(1.1); }
}

@keyframes stormSpin {
  0% { transform: rotate(0deg) translateX(10px) rotate(0deg); }
  100% { transform: rotate(360deg) translateX(10px) rotate(-360deg); }
}

@keyframes planetFloat3 {
  0% { transform: translate(0, 0); }
  25% { transform: translate(20px, 15px); }
  50% { transform: translate(40px, 0); }
  75% { transform: translate(20px, -15px); }
  100% { transform: translate(0, 0); }
}

@keyframes moonsOrbit {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Animations du thème Océan */
@keyframes lightRayFlicker {
  0%, 100% { opacity: 0.4; filter: blur(15px); }
  50% { opacity: 0.6; filter: blur(12px); }
}

@keyframes bubbleRise {
  0% {
    transform: translateY(0) translateX(0) rotate(0deg);
    opacity: 0;
  }
  10% { opacity: 0.8; }
  90% { opacity: 0.5; }
  100% {
    transform: translateY(-100vh) translateX(20px) rotate(360deg);
    opacity: 0;
  }
}

@keyframes planktonFloat {
  0% { transform: translate(0, 0); opacity: 0; }
  10% { opacity: 0.6; }
  90% { opacity: 0.4; }
  100% { transform: translate(var(--tx, 20px), var(--ty, -50px)); opacity: 0; }
}

@keyframes coralSway {
  0% { transform: rotate(-2deg); }
  100% { transform: rotate(2deg); }
}

@keyframes coralBranchSway {
  0% { transform: rotate(-5deg); }
  100% { transform: rotate(5deg); }
}

@keyframes schoolSwim {
  0% { transform: translateX(0) rotate(0deg); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translateX(calc(100vw + 200px)) rotate(0deg); opacity: 0; }
}

@keyframes schoolFishMove {
  0% { transform: translateX(0) translateY(0) skew(-30deg); }
  25% { transform: translateX(5px) translateY(-3px) skew(-25deg); }
  50% { transform: translateX(0) translateY(0) skew(-30deg); }
  75% { transform: translateX(-5px) translateY(3px) skew(-35deg); }
  100% { transform: translateX(0) translateY(0) skew(-30deg); }
}

@keyframes fishSwim {
  0% { transform: translateX(0) skew(-30deg); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translateX(calc(100vw + 100px)) skew(-30deg); opacity: 0; }
}

@keyframes fishTailWag {
  0% { transform: rotate(-15deg); }
  100% { transform: rotate(15deg); }
}

@keyframes seaweedSway {
  0% { transform: rotate(-10deg); }
  50% { transform: rotate(0deg); }
  100% { transform: rotate(10deg); }
}

@keyframes jellyfishFloat {
  0% { transform: translateY(0) translateX(0); }
  25% { transform: translateY(-30px) translateX(20px); }
  50% { transform: translateY(0) translateX(40px); }
  75% { transform: translateY(30px) translateX(20px); }
  100% { transform: translateY(0) translateX(0); }
}

@keyframes jellyfishPulse {
  0% { transform: scaleX(1) scaleY(1); }
  50% { transform: scaleX(1.1) scaleY(0.9); }
  100% { transform: scaleX(1) scaleY(1); }
}

@keyframes tentacleWave {
  0% { transform: rotate(-10deg); }
  50% { transform: rotate(10deg); }
  100% { transform: rotate(-10deg); }
}

/* Animations du thème Cyberpunk */
@keyframes gridRotate {
  0% { transform: rotateX(60deg) rotateZ(0deg); }
  100% { transform: rotateX(60deg) rotateZ(360deg); }
}

@keyframes rainFall {
  0% { transform: translateY(0) translateX(0); opacity: 0.7; }
  100% { transform: translateY(calc(100vh + 100px)) translateX(20px); opacity: 0; }
}

@keyframes neonFlicker {
  0%, 92%, 100% { opacity: 1; }
  90%, 96% { opacity: 0.8; }
}

@keyframes buildingLights {
  0%, 100% { background: linear-gradient(to top, rgba(0, 0, 20, 0.9) 0%, rgba(20, 20, 40, 0.8) 100%); }
  50% { background: linear-gradient(to top, rgba(5, 5, 25, 0.9) 0%, rgba(25, 25, 45, 0.8) 100%); }
}

@keyframes buildingWindowsScroll {
  0% { background-position: 0 0; }
  100% { background-position: 0 100%; }
}

@keyframes cubeFly {
  0% { transform: translateX(0) rotateY(0deg) rotateX(0deg); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translateX(calc(100vw + 50px)) rotateY(360deg) rotateX(360deg); opacity: 0; }
}

@keyframes dataStreamPulse {
  0% { 
    opacity: 0.8;
    transform: var(--rotation, rotate(0deg)) scale(1);
    background-position: -100% 0;
  }
  50% {
    opacity: 1;
    transform: var(--rotation, rotate(0deg)) scale(1);
    background-position: 0% 0;
  }
  100% { 
    opacity: 0.8;
    transform: var(--rotation, rotate(0deg)) scale(1);
    background-position: 200% 0;
  }
}

@keyframes circuitPulse {
  0% { 
    opacity: 0.3;
    transform: var(--rotation, rotate(0deg)) scale(1);
    background-position: -100% 0;
  }
  100% { 
    opacity: 0.8;
    transform: var(--rotation, rotate(0deg)) scale(1.05);
    background-position: 200% 0;
  }
}

@keyframes nodeFlash {
  0%, 100% { opacity: 0.7; box-shadow: 0 0 5px rgba(0, 255, 255, 0.7); }
  50% { opacity: 1; box-shadow: 0 0 15px rgba(0, 255, 255, 1); }
}

@keyframes hologramFlicker {
  0%, 100% { opacity: 0.7; box-shadow: 0 0 10px rgba(0, 255, 255, 0.3); }
  25% { opacity: 0.9; box-shadow: 0 0 20px rgba(0, 255, 255, 0.6); }
  50% { opacity: 0.5; box-shadow: 0 0 5px rgba(0, 255, 255, 0.2); }
  75% { opacity: 0.8; box-shadow: 0 0 15px rgba(0, 255, 255, 0.5); }
}

@keyframes hologramLineScan {
  0% { transform: translateY(0); opacity: 0.7; }
  100% { transform: translateY(calc(100% - 2px)); opacity: 0.3; }
}

@keyframes hologramRingExpand {
  0% { width: 0; height: 0; opacity: 0.8; }
  100% { width: 100%; height: 100%; opacity: 0; }
}

@keyframes glitchEffect {
  0%, 100% { opacity: 0.5; transform: translateX(0); background-position: 0 0; }
  5%, 10% { opacity: 0.6; transform: translateX(-5px); background-position: -5px 0; }
  15% { opacity: 0.5; transform: translateX(0); background-position: 0 0; }
  20% { opacity: 0.4; transform: translateX(5px); background-position: 5px 0; }
  25% { opacity: 0.5; transform: translateX(0); background-position: 0 0; }
  30%, 35% { opacity: 0.6; transform: translateY(-5px); background-position: 0 -5px; }
  40% { opacity: 0.5; transform: translateY(0); background-position: 0 0; }
  70% { opacity: 0.5; transform: translateY(0); background-position: 0 0; }
  75%, 80% { opacity: 0.6; transform: translateX(3px); background-position: 3px 0; }
  85% { opacity: 0.4; transform: translateX(-3px); background-position: -3px 0; }
  90% { opacity: 0.5; transform: translateX(0); background-position: 0 0; }
}

/* Animations du thème Forêt */
@keyframes sunbeamFlicker {
  0%, 100% { opacity: 0.4; filter: blur(10px); }
  50% { opacity: 0.6; filter: blur(8px); }
}

@keyframes mistFloat {
  0% { transform: translateX(0) translateY(0); }
  50% { transform: translateX(20px) translateY(-10px); }
  100% { transform: translateX(0) translateY(0); }
}

@keyframes leafFall {
  0% { transform: translateY(0) translateX(0) rotate(0deg); opacity: 0; }
  10% { opacity: 0.8; }
  90% { opacity: 0.7; }
  100% { transform: translateY(calc(100vh + 50px)) translateX(100px) rotate(360deg); opacity: 0; }
}

@keyframes butterflyFlight {
  0% { transform: translateX(0) translateY(0) rotate(0deg); opacity: 0; }
  10% { opacity: 1; }
  40% { transform: translateX(40vw) translateY(-20vh) rotate(5deg); }
  60% { transform: translateX(60vw) translateY(10vh) rotate(-5deg); }
  90% { opacity: 1; }
  100% { transform: translateX(calc(100vw + 50px)) translateY(0) rotate(0deg); opacity: 0; }
}

@keyframes wingBeatLeft {
  0% { transform: scaleX(-1) rotate(-30deg); }
  100% { transform: scaleX(-1) rotate(-80deg); }
}

@keyframes wingBeatRight {
  0% { transform: rotate(30deg); }
  100% { transform: rotate(80deg); }
}

@keyframes birdFlight {
  0% { transform: translateX(0) translateY(0); opacity: 0; }
  10% { opacity: 1; }
  30% { transform: translateX(30vw) translateY(10vh); }
  70% { transform: translateX(70vw) translateY(-5vh); }
  90% { opacity: 1; }
  100% { transform: translateX(calc(100vw + 30px)) translateY(0); opacity: 0; }
}

@keyframes grassSway {
  0% { transform: rotate(-5deg); }
  100% { transform: rotate(5deg); }
}

@keyframes fireflyGlow {
  0%, 100% { opacity: 0.3; box-shadow: 0 0 5px 1px rgba(255, 255, 153, 0.5); }
  50% { opacity: 0.8; box-shadow: 0 0 15px 3px rgba(255, 255, 153, 0.8); }
}

@keyframes fireflyHover {
  0% { transform: translate(0, 0); }
  25% { transform: translate(20px, -15px); }
  50% { transform: translate(5px, -25px); }
  75% { transform: translate(-10px, -10px); }
  100% { transform: translate(0, 0); }
}
</style>