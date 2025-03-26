<!-- SpaceBackground.vue -->
<template>
  <div class="space-background" :class="theme">
    <!-- Container for all space elements -->
    <div class="space-elements">
      <!-- Dynamic space elements based on the selected theme -->
      <template v-if="theme === 'cosmic'">
        <!-- Comets -->
        <div class="comet comet-1"></div>
        <div class="comet comet-2"></div>
        <div class="comet comet-3"></div>
        <div class="comet comet-4"></div>
        <div class="comet comet-5"></div>
        
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
          <div v-for="i in 30" :key="`rain-${i}`" class="rain-drop" :style="getRainDropStyle(i)"></div>
        </div>
        
        <!-- Neon Signs -->
        <div class="neon-sign neon-sign-1">DIGITAL DREAMS</div>
        <div class="neon-sign neon-sign-2">NEURAL LINK</div>
        <div class="neon-sign neon-sign-3">CYBER ZONE</div>
        
        <!-- Grid lines - Enhanced 3D -->
        <div class="grid-container">
          <div class="grid-horizontal" v-for="i in 8" :key="`h-${i}`"></div>
          <div class="grid-vertical" v-for="i in 8" :key="`v-${i}`"></div>
        </div>
        
        <!-- City Silhouette -->
        <div class="cyber-city">
          <div v-for="i in 8" :key="`building-${i}`" class="city-building"></div>
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
    </div>
  </div>
</template>
  
<script>
export default {
  name: 'SpaceBackground',
  props: {
    // Available themes: 'cosmic', 'ocean', 'cyberpunk'
    theme: {
      type: String,
      default: 'cosmic',
      validator: (value) => ['cosmic', 'ocean', 'cyberpunk'].includes(value)
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
  }
};
</script>
  
<style scoped>
/* Base space background styles */
.space-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  overflow: hidden;
}

/* Container for all space elements */
.space-elements {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 1;
}

/* 
* COSMIC THEME STYLES 
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
  right: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
  display: block;
  background-position: 0 0;
  background-repeat: repeat;
  z-index: 0;
}

.cosmic::before {
  background-image: 
    radial-gradient(1px 1px at 10% 30%, rgba(255, 255, 255, 0.9) 50%, transparent 100%),
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

/* Styles for the comets */
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

.comet-1 {
  top: 15%;
  left: -5%;
  animation-delay: 2s;
}

.comet-2 {
  top: 35%;
  left: -10%;
  width: 3px;
  height: 3px;
  animation-delay: 7s;
  animation-duration: 15s;
}

.comet-3 {
  top: 65%;
  left: -8%;
  width: 5px;
  height: 5px;
  animation-delay: 13s;
  animation-duration: 18s;
}

.comet-4 {
  top: 62%;
  left: -18%;
  animation-delay: 11s;
}

.comet-5 {
  top: 70%;
  left: -18%;
  animation-delay: 4s;
}

/* Styles for the galaxy */
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
    radial-gradient(
      ellipse at center,
      rgba(255, 255, 255, 0.1) 0%,
      transparent 60%
    ),
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

/* Styles for the planets */
.planet-1 {
  position: absolute;
  width: 80px;
  height: 80px;
  top: 15%;
  right: 37%;
  background: 
    radial-gradient(
      circle at 30% 30%,
      #7a4dbc 0%,
      #522b99 30%,
      #3c1777 60%,
      #2c1155 100%
    );
  border-radius: 50%;
  box-shadow: 
    inset -15px -15px 40px rgba(0, 0, 0, 0.5),
    0 0 20px rgba(120, 70, 230, 0.3);
  z-index: 3;
  transform: rotate(-15deg);
  animation: planetFloat 120s linear infinite;
}

/* Rings for the purple planet */
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

/* Styles for the red gaseous planet */
.planet-2 {
  position: absolute;
  width: 100px;
  height: 100px;
  top: 65%;
  right: 5%;
  background: 
    radial-gradient(
      circle at 40% 40%,
      #ff6b5b 0%,
      #d32f2f 30%,
      #b71c1c 60%,
      #7f0000 100%
    );
  border-radius: 50%;
  box-shadow: 
    inset -20px -20px 60px rgba(0, 0, 0, 0.6),
    0 0 30px rgba(255, 100, 80, 0.4);
  z-index: 2;
  transform: rotate(10deg);
  animation: planetFloat2 150s linear infinite;
}

/* Atmosphere for the red planet */
.planet-2 .planet-atmosphere {
  position: absolute;
  width: 110%;
  height: 110%;
  top: -5%;
  left: -5%;
  border-radius: 50%;
  background: 
    radial-gradient(
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

/* Storm on the red planet */
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

/* Styles for the ice planet */
.planet-3 {
  position: absolute;
  width: 70px;
  height: 70px;
  top: 15%;
  left: 15%;
  background: 
    radial-gradient(
      circle at 50% 50%,
      #b3e5fc 0%,
      #81d4fa 30%,
      #4fc3f7 60%,
      #29b6f6 100%
    );
  border-radius: 50%;
  box-shadow: 
    inset -10px -10px 30px rgba(0, 0, 0, 0.3),
    0 0 25px rgba(79, 195, 247, 0.5);
  z-index: 2;
  animation: planetFloat3 180s linear infinite;
}

/* Ice caps for the ice planet */
.planet-3 .planet-ice-caps {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  border-radius: 50%;
  background: 
    radial-gradient(
      ellipse at 50% 10%,
      rgba(255, 255, 255, 0.9) 0%,
      rgba(255, 255, 255, 0) 50%
    ),
    radial-gradient(
      ellipse at 50% 90%,
      rgba(255, 255, 255, 0.9) 0%,
      rgba(255, 255, 255, 0) 50%
    );
  z-index: 3;
}

/* Moon system for the ice planet */
.planet-3 .planet-moons {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 1;
  animation: moonsOrbit 60s linear infinite;
}

/* Individual moons */
.planet-moon {
  position: absolute;
  background: #e0e0e0;
  border-radius: 50%;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

.moon-1 {
  width: 15px;
  height: 15px;
  top: -30px;
  left: 50%;
  transform: translateX(-50%);
  background: 
    radial-gradient(
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
  background: 
    radial-gradient(
      circle at 30% 30%,
      #e0e0e0 0%,
      #bdbdbd 50%,
      #9e9e9e 100%
    );
}
  
  /*
 * OCEAN THEME STYLES - ENHANCED
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

/* Light rays */
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
  transform: rotate(30deg) translateX(-50%);
  transform-origin: top center;
  filter: blur(15px);
  opacity: 0.4;
  z-index: 2;
  animation: lightRayFlicker 8s ease-in-out infinite alternate;
}

.light-ray-1 {
  left: 25%;
  transform: rotate(20deg) translateX(-50%);
  animation-delay: 0s;
}

.light-ray-2 {
  left: 60%;
  transform: rotate(-15deg) translateX(-50%);
  animation-delay: 2s;
}

.light-ray-3 {
  left: 80%;
  width: 100px;
  transform: rotate(-25deg) translateX(-50%);
  animation-delay: 4s;
}

/* Enhanced bubbles */
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

.bubble-1 { width: 30px; height: 30px; left: 20%; bottom: -30px; animation-delay: 0s; }
.bubble-2 { width: 20px; height: 20px; left: 35%; bottom: -20px; animation-delay: 3s; }
.bubble-3 { width: 40px; height: 40px; left: 55%; bottom: -40px; animation-delay: 6s; }
.bubble-4 { width: 15px; height: 15px; left: 70%; bottom: -15px; animation-delay: 9s; }
.bubble-5 { width: 25px; height: 25px; left: 85%; bottom: -25px; animation-delay: 12s; }
.bubble-6 { width: 35px; height: 35px; left: 45%; bottom: -35px; animation-delay: 15s; }
.bubble-7 { width: 18px; height: 18px; left: 25%; bottom: -18px; animation-delay: 18s; }
.bubble-8 { width: 22px; height: 22px; left: 15%; bottom: -22px; animation-delay: 4s; }
.bubble-9 { width: 28px; height: 28px; left: 40%; bottom: -28px; animation-delay: 8s; }
.bubble-10 { width: 32px; height: 32px; left: 60%; bottom: -32px; animation-delay: 11s; }
.bubble-11 { width: 14px; height: 14px; left: 75%; bottom: -14px; animation-delay: 7s; }
.bubble-12 { width: 24px; height: 24px; left: 90%; bottom: -24px; animation-delay: 14s; }

/* Plankton particles */
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

.plankton:nth-child(4n+1) {
  background: rgba(180, 220, 255, 0.5);
}

.plankton:nth-child(4n+2) {
  background: rgba(150, 210, 255, 0.4);
}

.plankton:nth-child(4n+3) {
  background: rgba(120, 200, 255, 0.6);
}

/* Generate random positions and delays for plankton */
.plankton:nth-child(1) { top: 10%; left: 15%; animation-delay: 0s; }
.plankton:nth-child(2) { top: 20%; left: 25%; animation-delay: 1s; }
.plankton:nth-child(3) { top: 30%; left: 35%; animation-delay: 2s; }
.plankton:nth-child(4) { top: 40%; left: 45%; animation-delay: 3s; }
.plankton:nth-child(5) { top: 50%; left: 55%; animation-delay: 4s; }
/* ... and so on for all plankton elements */

/* Enhanced coral */
.coral {
  position: absolute;
  z-index: 2;
  transform-origin: bottom center;
  animation: coralSway 8s ease-in-out infinite alternate;
}

.coral-1 {
  width: 150px;
  height: 120px;
  bottom: 0;
  right: 10%;
  animation-delay: 0s;
}

.coral-2 {
  width: 180px;
  height: 150px;
  bottom: 0;
  left: 5%;
  animation-delay: 3s;
}

.coral-branch {
  position: absolute;
  bottom: 0;
  background: linear-gradient(to top, 
    rgba(255, 80, 80, 0.8) 0%, 
    rgba(255, 127, 80, 0.7) 50%, 
    rgba(255, 127, 80, 0.3) 100%);
  border-radius: 50% 50% 0 0;
  filter: blur(1px);
  transform-origin: bottom center;
}

.coral-1 .branch-1 {
  width: 40px;
  height: 100px;
  left: 20px;
  animation: coralBranchSway 10s ease-in-out infinite alternate;
}

.coral-1 .branch-2 {
  width: 60px;
  height: 120px;
  left: 70px;
  animation: coralBranchSway 12s ease-in-out infinite alternate;
  animation-delay: 1s;
}

.coral-1 .branch-3 {
  width: 50px;
  height: 90px;
  left: 40px;
  animation: coralBranchSway 9s ease-in-out infinite alternate;
  animation-delay: 2s;
}

.coral-2 .branch-1 {
  width: 70px;
  height: 130px;
  left: 30px;
  background: linear-gradient(to top, 
    rgba(200, 100, 255, 0.8) 0%, 
    rgba(180, 120, 255, 0.7) 50%, 
    rgba(160, 140, 255, 0.3) 100%);
  animation: coralBranchSway 11s ease-in-out infinite alternate;
}

.coral-2 .branch-2 {
  width: 50px;
  height: 100px;
  left: 100px;
  background: linear-gradient(to top, 
    rgba(200, 100, 255, 0.8) 0%, 
    rgba(180, 120, 255, 0.7) 50%, 
    rgba(160, 140, 255, 0.3) 100%);
  animation: coralBranchSway 13s ease-in-out infinite alternate;
  animation-delay: 2s;
}

/* Fish Schools */
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
  animation-delay: 0s;
}

.fish-school-2 {
  top: 55%;
  left: -200px;
  animation-delay: 15s;
}

.school-fish {
  position: absolute;
  width: 15px;
  height: 8px;
  background: rgba(100, 180, 255, 0.7);
  border-radius: 50% 60% 60% 50% / 50%;
  transform: skew(-30deg);
  animation: schoolFishMove 5s ease-in-out infinite;
}

.fish-school-1 .school-fish {
  background: rgba(100, 180, 255, 0.7);
}

.fish-school-2 .school-fish {
  background: rgba(180, 210, 255, 0.7);
}

.fish-school-1 .school-fish:nth-child(1) { top: 10%; left: 20%; animation-delay: 0s; }
.fish-school-1 .school-fish:nth-child(2) { top: 40%; left: 30%; animation-delay: 0.2s; }
.fish-school-1 .school-fish:nth-child(3) { top: 70%; left: 25%; animation-delay: 0.4s; }
.fish-school-1 .school-fish:nth-child(4) { top: 25%; left: 60%; animation-delay: 0.6s; }
.fish-school-1 .school-fish:nth-child(5) { top: 55%; left: 70%; animation-delay: 0.8s; }
.fish-school-1 .school-fish:nth-child(6) { top: 15%; left: 80%; animation-delay: 1.0s; }
.fish-school-1 .school-fish:nth-child(7) { top: 45%; left: 50%; animation-delay: 1.2s; }
.fish-school-1 .school-fish:nth-child(8) { top: 65%; left: 45%; animation-delay: 1.4s; }

.fish-school-2 .school-fish:nth-child(1) { top: 15%; left: 10%; animation-delay: 0.1s; }
.fish-school-2 .school-fish:nth-child(2) { top: 45%; left: 20%; animation-delay: 0.3s; }
.fish-school-2 .school-fish:nth-child(3) { top: 75%; left: 15%; animation-delay: 0.5s; }
.fish-school-2 .school-fish:nth-child(4) { top: 20%; left: 50%; animation-delay: 0.7s; }
.fish-school-2 .school-fish:nth-child(5) { top: 50%; left: 60%; animation-delay: 0.9s; }
.fish-school-2 .school-fish:nth-child(6) { top: 10%; left: 70%; animation-delay: 1.1s; }
.fish-school-2 .school-fish:nth-child(7) { top: 40%; left: 40%; animation-delay: 1.3s; }
.fish-school-2 .school-fish:nth-child(8) { top: 60%; left: 35%; animation-delay: 1.5s; }
.fish-school-2 .school-fish:nth-child(9) { top: 30%; left: 80%; animation-delay: 1.7s; }
.fish-school-2 .school-fish:nth-child(10) { top: 70%; left: 85%; animation-delay: 1.9s; }
.fish-school-2 .school-fish:nth-child(11) { top: 25%; left: 30%; animation-delay: 2.1s; }
.fish-school-2 .school-fish:nth-child(12) { top: 55%; left: 75%; animation-delay: 2.3s; }

/* Enhanced individual fish */
.fish {
  position: absolute;
  z-index: 3;
  animation: fishSwim 25s linear infinite;
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
  border-radius: 70% 30% 30% 70% / 50%;
  animation-delay: 0s;
}

.fish-2 {
  width: 30px;
  height: 15px;
  top: 45%;
  left: -30px;
  background: linear-gradient(to right, 
    rgba(255, 165, 0, 0.9) 0%, 
    rgba(255, 165, 0, 0.8) 60%, 
    rgba(255, 165, 0, 0.4) 100%);
  border-radius: 70% 30% 30% 70% / 50%;
  animation-delay: 5s;
}

.fish-3 {
  width: 50px;
  height: 25px;
  top: 60%;
  left: -50px;
  background: linear-gradient(to right, 
    rgba(255, 105, 180, 0.9) 0%, 
    rgba(255, 105, 180, 0.8) 60%, 
    rgba(255, 105, 180, 0.4) 100%);
  border-radius: 70% 30% 30% 70% / 50%;
  animation-delay: 10s;
}

.fish-4 {
  width: 45px;
  height: 22px;
  top: 75%;
  left: -45px;
  background: linear-gradient(to right, 
    rgba(120, 220, 255, 0.9) 0%, 
    rgba(100, 200, 240, 0.8) 60%, 
    rgba(80, 180, 220, 0.4) 100%);
  border-radius: 70% 30% 30% 70% / 50%;
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
}

/* Seaweed - Enhanced */
.seaweed {
  position: absolute;
  z-index: 1;
  display: flex;
  justify-content: space-around;
  transform-origin: bottom center;
}

.seaweed-1 {
  width: 100px;
  height: 150px;
  bottom: 0;
  left: 15%;
}

.seaweed-2 {
  width: 80px;
  height: 120px;
  bottom: 0;
  left: 60%;
}

.seaweed-3 {
  width: 120px;
  height: 180px;
  bottom: 0;
  left: 35%;
}

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

.seaweed-1 .seaweed-strand:nth-child(1) { animation-delay: 0s; }
.seaweed-1 .seaweed-strand:nth-child(2) { animation-delay: 1.5s; }
.seaweed-1 .seaweed-strand:nth-child(3) { animation-delay: 3s; }
.seaweed-2 .seaweed-strand:nth-child(1) { animation-delay: 2s; }
.seaweed-2 .seaweed-strand:nth-child(2) { animation-delay: 4s; }
.seaweed-3 .seaweed-strand:nth-child(1) { animation-delay: 1s; }
.seaweed-3 .seaweed-strand:nth-child(2) { animation-delay: 2.5s; }
.seaweed-3 .seaweed-strand:nth-child(3) { animation-delay: 4s; }
.seaweed-3 .seaweed-strand:nth-child(4) { animation-delay: 5.5s; }

/* Jellyfish */
.jellyfish {
  position: absolute;
  z-index: 3;
  animation: jellyfishFloat 30s ease-in-out infinite;
}

.jellyfish-1 {
  top: 20%;
  right: 20%;
  animation-delay: 0s;
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

.tentacle:nth-child(1) { left: 10%; animation-delay: 0s; }
.tentacle:nth-child(2) { left: 30%; animation-delay: 0.6s; }
.tentacle:nth-child(3) { left: 50%; animation-delay: 1.2s; }
.tentacle:nth-child(4) { left: 70%; animation-delay: 1.8s; }
.tentacle:nth-child(5) { left: 90%; animation-delay: 2.4s; }

/* Sea floor */
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

.sand-dune-1 {
  left: 0;
  height: 35px;
}

.sand-dune-2 {
  left: 30%;
  height: 25px;
}

.sand-dune-3 {
  left: 70%;
  height: 30px;
}

/*
 * CYBERPUNK THEME STYLES - ENHANCED
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

/* Rain effect */
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

/* Neon signs */
.neon-sign {
  position: absolute;
  font-family: 'Orbitron', sans-serif;
  font-weight: bold;
  letter-spacing: 2px;
  z-index: 5;
  animation: neonFlicker 3s infinite alternate;
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
  animation-delay: 0s;
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

/* Enhanced 3D Grid */
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

/* City silhouette */
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
  height: 100%;
  background: linear-gradient(to top, 
    rgba(0, 0, 20, 0.9) 0%, 
    rgba(20, 20, 40, 0.8) 100%);
  animation: buildingLights 4s infinite alternate;
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

.city-building:nth-child(1) { height: 65%; animation-delay: 0.1s; }
.city-building:nth-child(2) { height: 85%; animation-delay: 0.2s; }
.city-building:nth-child(3) { height: 70%; animation-delay: 0.3s; }
.city-building:nth-child(4) { height: 90%; animation-delay: 0.4s; }
.city-building:nth-child(5) { height: 60%; animation-delay: 0.5s; }
.city-building:nth-child(6) { height: 80%; animation-delay: 0.6s; }
.city-building:nth-child(7) { height: 75%; animation-delay: 0.7s; }
.city-building:nth-child(8) { height: 95%; animation-delay: 0.8s; }

/* Enhanced data cubes */
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
  animation-delay: 0s;
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

.cube-face:nth-child(1) { transform: translateZ(20px); }
.cube-face:nth-child(2) { transform: rotateX(180deg) translateZ(20px); }
.cube-face:nth-child(3) { transform: rotateY(90deg) translateZ(20px); }
.cube-face:nth-child(4) { transform: rotateY(-90deg) translateZ(20px); }
.cube-face:nth-child(5) { transform: rotateX(90deg) translateZ(20px); }
.cube-face:nth-child(6) { transform: rotateX(-90deg) translateZ(20px); }

/* Data stream */
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
  animation-delay: 0s;
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

/* Enhanced circuits */
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
  animation-delay: 0s;
}

.circuit-2 {
  width: 40%;
  bottom: 30%;
  right: 5%;
  transform: rotate(-15deg);
  animation-delay: 2.5s;
}

.circuit-3 {
  width: 25%;
  top: 60%;
  left: 35%;
  transform: rotate(60deg);
  animation-delay: 1.2s;
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

.circuit-1 .circuit-node:nth-child(1) { left: 10%; animation-delay: 0.2s; }
.circuit-1 .circuit-node:nth-child(2) { left: 30%; animation-delay: 0.4s; }
.circuit-1 .circuit-node:nth-child(3) { left: 50%; animation-delay: 0.6s; }
.circuit-1 .circuit-node:nth-child(4) { left: 70%; animation-delay: 0.8s; }
.circuit-1 .circuit-node:nth-child(5) { left: 90%; animation-delay: 1.0s; }

.circuit-2 .circuit-node:nth-child(1) { left: 5%; animation-delay: 0.1s; }
.circuit-2 .circuit-node:nth-child(2) { left: 20%; animation-delay: 0.3s; }
.circuit-2 .circuit-node:nth-child(3) { left: 40%; animation-delay: 0.5s; }
.circuit-2 .circuit-node:nth-child(4) { left: 60%; animation-delay: 0.7s; }
.circuit-2 .circuit-node:nth-child(5) { left: 75%; animation-delay: 0.9s; }
.circuit-2 .circuit-node:nth-child(6) { left: 85%; animation-delay: 1.1s; }
.circuit-2 .circuit-node:nth-child(7) { left: 95%; animation-delay: 1.3s; }

.circuit-3 .circuit-node:nth-child(1) { left: 15%; animation-delay: 0.3s; }
.circuit-3 .circuit-node:nth-child(2) { left: 40%; animation-delay: 0.6s; }
.circuit-3 .circuit-node:nth-child(3) { left: 65%; animation-delay: 0.9s; }
.circuit-3 .circuit-node:nth-child(4) { left: 90%; animation-delay: 1.2s; }

/* Enhanced holograms */
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
  animation-delay: 0s;
}

.hologram-2 {
  width: 150px;
  height: 100px;
  bottom: 20%;
  left: 20%;
  animation-delay: 1.5s;
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

.hologram-3 .hologram-ring:nth-child(1) {
  animation-delay: 0s;
}

.hologram-3 .hologram-ring:nth-child(2) {
  animation-delay: 1s;
}

.hologram-3 .hologram-ring:nth-child(3) {
  animation-delay: 2s;
}

/* Glitch effect overlay */
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
 * ANIMATIONS 
 */

/* Ocean theme animations */
@keyframes waterSurface {
  0% { transform: scaleY(1); opacity: 0.2; }
  50% { transform: scaleY(1.1); opacity: 0.3; }
  100% { transform: scaleY(1); opacity: 0.2; }
}

@keyframes waterSurfaceLines {
  0% { background-position: 0 0; }
  100% { background-position: 100% 0; }
}

@keyframes lightRayFlicker {
  0%, 100% { opacity: 0.4; filter: blur(15px); }
  50% { opacity: 0.6; filter: blur(12px); }
}

@keyframes bubbleRise {
  0% {
    transform: translateY(0) translateX(0) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 0.8;
  }
  90% {
    opacity: 0.5;
  }
  100% {
    transform: translateY(-100vh) translateX(20px) rotate(360deg);
    opacity: 0;
  }
}

@keyframes planktonFloat {
  0% {
    transform: translate(0, 0);
    opacity: 0;
  }
  10% {
    opacity: 0.6;
  }
  90% {
    opacity: 0.4;
  }
  100% {
    transform: translate(var(--tx, 20px), var(--ty, -50px));
    opacity: 0;
  }
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
  0% {
    transform: translateX(0) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateX(calc(100vw + 200px)) rotate(0deg);
    opacity: 0;
  }
}

@keyframes schoolFishMove {
  0% { transform: translateX(0) translateY(0) skew(-30deg); }
  25% { transform: translateX(5px) translateY(-3px) skew(-25deg); }
  50% { transform: translateX(0) translateY(0) skew(-30deg); }
  75% { transform: translateX(-5px) translateY(3px) skew(-35deg); }
  100% { transform: translateX(0) translateY(0) skew(-30deg); }
}

@keyframes fishSwim {
  0% {
    transform: translateX(0) skew(-30deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateX(calc(100vw + 100px)) skew(-30deg);
    opacity: 0;
  }
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

/* Cyberpunk theme animations */
@keyframes gridPulse {
  0% { opacity: 0.1; }
  100% { opacity: 0.3; }
}

@keyframes gridRotate {
  0% { transform: rotateX(60deg) rotateZ(0deg); }
  100% { transform: rotateX(60deg) rotateZ(360deg); }
}

@keyframes rainFall {
  0% {
    transform: translateY(0) translateX(0);
    opacity: 0.7;
  }
  100% {
    transform: translateY(calc(100vh + 100px)) translateX(20px);
    opacity: 0;
  }
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
  0% {
    transform: translateX(0) rotateY(0deg) rotateX(0deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateX(calc(100vw + 50px)) rotateY(360deg) rotateX(360deg);
    opacity: 0;
  }
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
  0%, 100% { 
    opacity: 0.7;
    box-shadow: 0 0 5px rgba(0, 255, 255, 0.7);
  }
  50% { 
    opacity: 1;
    box-shadow: 0 0 15px rgba(0, 255, 255, 1);
  }
}

@keyframes hologramFlicker {
  0%, 100% { 
    opacity: 0.7;
    box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
  }
  25% { 
    opacity: 0.9;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.6);
  }
  50% { 
    opacity: 0.5;
    box-shadow: 0 0 5px rgba(0, 255, 255, 0.2);
  }
  75% { 
    opacity: 0.8;
    box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
  }
}

@keyframes hologramLineScan {
  0% { 
    transform: translateY(0);
    opacity: 0.7;
  }
  100% { 
    transform: translateY(calc(100% - 2px));
    opacity: 0.3;
  }
}

@keyframes hologramRingExpand {
  0% {
    width: 0;
    height: 0;
    opacity: 0.8;
  }
  100% {
    width: 100%;
    height: 100%;
    opacity: 0;
  }
}

@keyframes glitchEffect {
  0%, 100% { 
    opacity: 0.5;
    transform: translateX(0);
    background-position: 0 0;
  }
  5%, 10% { 
    opacity: 0.6;
    transform: translateX(-5px);
    background-position: -5px 0;
  }
  15% { 
    opacity: 0.5;
    transform: translateX(0);
    background-position: 0 0;
  }
  20% { 
    opacity: 0.4;
    transform: translateX(5px);
    background-position: 5px 0;
  }
  25% { 
    opacity: 0.5;
    transform: translateX(0);
    background-position: 0 0;
  }
  30%, 35% { 
    opacity: 0.6;
    transform: translateY(-5px);
    background-position: 0 -5px;
  }
  40% { 
    opacity: 0.5;
    transform: translateY(0);
    background-position: 0 0;
  }
  70% { 
    opacity: 0.5;
    transform: translateY(0);
    background-position: 0 0;
  }
  75%, 80% { 
    opacity: 0.6;
    transform: translateX(3px);
    background-position: 3px 0;
  }
  85% { 
    opacity: 0.4;
    transform: translateX(-3px);
    background-position: -3px 0;
  }
  90% { 
    opacity: 0.5;
    transform: translateX(0);
    background-position: 0 0;
  }
}

/* Original animations for Cosmic theme - kept from original component */
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
    transform: translate(0, 0) rotate(15deg);
    opacity: 0;
  }
  5% {
    opacity: 1;
  }
  95% {
    opacity: 1;
  }
  100% {
    transform: translate(calc(100vw + 200px), 20vh) rotate(15deg);
    opacity: 0;
  }
}

@keyframes galaxyPulse {
  0% {
    transform: rotate(-25deg) scale(1);
    opacity: 0.7;
  }
  50% {
    transform: rotate(-25deg) scale(1.05);
    opacity: 0.8;
  }
  100% {
    transform: rotate(-25deg) scale(1);
    opacity: 0.7;
  }
}

@keyframes galaxyRotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes planetFloat {
  0% {
    transform: translate(0, 0) rotate(-15deg);
  }
  25% {
    transform: translate(-10px, 15px) rotate(-15deg);
  }
  50% {
    transform: translate(-5px, 25px) rotate(-15deg);
  }
  75% {
    transform: translate(5px, 15px) rotate(-15deg);
  }
  100% {
    transform: translate(0, 0) rotate(-15deg);
  }
}

@keyframes ringsRotate {
  0% {
    transform: translate(-50%, -50%) rotate(-15deg);
  }
  100% {
    transform: translate(-50%, -50%) rotate(345deg);
  }
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
</style>