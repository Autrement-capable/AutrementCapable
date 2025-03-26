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
        <!-- Bubbles -->
        <div class="bubble bubble-1"></div>
        <div class="bubble bubble-2"></div>
        <div class="bubble bubble-3"></div>
        <div class="bubble bubble-4"></div>
        <div class="bubble bubble-5"></div>
        <div class="bubble bubble-6"></div>
        <div class="bubble bubble-7"></div>
        
        <!-- Coral -->
        <div class="coral coral-1"></div>
        
        <!-- Fish -->
        <div class="fish fish-1"></div>
        <div class="fish fish-2"></div>
        <div class="fish fish-3"></div>
        
        <!-- Seaweed -->
        <div class="seaweed seaweed-1">
          <div class="seaweed-strand"></div>
          <div class="seaweed-strand"></div>
          <div class="seaweed-strand"></div>
        </div>
        
        <div class="seaweed seaweed-2">
          <div class="seaweed-strand"></div>
          <div class="seaweed-strand"></div>
        </div>
      </template>
      
      <!-- Cyberpunk theme elements -->
      <template v-else-if="theme === 'cyberpunk'">
        <!-- Grid lines -->
        <div class="grid-container">
          <div class="grid-horizontal" v-for="i in 10" :key="`h-${i}`"></div>
          <div class="grid-vertical" v-for="i in 10" :key="`v-${i}`"></div>
        </div>
        
        <!-- Flying data cubes -->
        <div class="data-cube data-cube-1"></div>
        <div class="data-cube data-cube-2"></div>
        <div class="data-cube data-cube-3"></div>
        
        <!-- Circuit paths -->
        <div class="circuit circuit-1"></div>
        <div class="circuit circuit-2"></div>
        
        <!-- Holographic displays -->
        <div class="hologram hologram-1"></div>
        <div class="hologram hologram-2"></div>
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
   * OCEAN THEME STYLES
   */
  .ocean {
    background: radial-gradient(ellipse at center, #042843 0%, #010e1a 100%);
  }
  
  .ocean::before,
  .ocean::after {
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
  
  .ocean::before {
    background-image: 
      radial-gradient(1px 1px at 10% 30%, rgba(173, 216, 230, 0.7) 50%, transparent 100%),
      radial-gradient(1px 1px at 20% 70%, rgba(173, 216, 230, 0.6) 50%, transparent 100%),
      radial-gradient(1px 1px at 30% 40%, rgba(173, 216, 230, 0.5) 50%, transparent 100%);
    background-size: 400% 400%;
    animation: bubbleFloat 300s linear infinite;
  }
  
  .bubble {
    position: absolute;
    border-radius: 50%;
    background: radial-gradient(
      circle at 30% 30%,
      rgba(255, 255, 255, 0.8) 0%,
      rgba(173, 216, 230, 0.4) 30%,
      rgba(173, 216, 230, 0.1) 60%,
      transparent 100%
    );
    box-shadow: 0 0 10px rgba(173, 216, 230, 0.3), inset 0 0 10px rgba(255, 255, 255, 0.3);
    animation: bubbleRise 15s ease-in infinite;
    opacity: 0;
  }
  
  .bubble-1 {
    width: 30px;
    height: 30px;
    left: 20%;
    bottom: -30px;
    animation-delay: 0s;
  }
  
  .bubble-2 {
    width: 20px;
    height: 20px;
    left: 35%;
    bottom: -20px;
    animation-delay: 3s;
  }
  
  .bubble-3 {
    width: 40px;
    height: 40px;
    left: 55%;
    bottom: -40px;
    animation-delay: 6s;
  }
  
  .bubble-4 {
    width: 15px;
    height: 15px;
    left: 70%;
    bottom: -15px;
    animation-delay: 9s;
  }
  
  .bubble-5 {
    width: 25px;
    height: 25px;
    left: 85%;
    bottom: -25px;
    animation-delay: 12s;
  }
  
  .bubble-6 {
    width: 35px;
    height: 35px;
    left: 45%;
    bottom: -35px;
    animation-delay: 15s;
  }
  
  .bubble-7 {
    width: 18px;
    height: 18px;
    left: 25%;
    bottom: -18px;
    animation-delay: 18s;
  }
  
  .coral {
    position: absolute;
    z-index: 2;
  }
  
  .coral-1 {
    width: 150px;
    height: 120px;
    bottom: 0;
    right: 10%;
    background: radial-gradient(
      ellipse at bottom,
      rgba(255, 127, 80, 0.7) 0%,
      rgba(255, 127, 80, 0.3) 60%,
      transparent 100%
    );
    filter: blur(3px);
    transform-origin: bottom center;
    animation: coralSway 8s ease-in-out infinite alternate;
  }
  
  .fish {
    position: absolute;
    z-index: 3;
  }
  
  .fish-1 {
    width: 40px;
    height: 20px;
    top: 30%;
    left: -40px;
    background: linear-gradient(to right, transparent, rgba(0, 191, 255, 0.6) 40%, rgba(0, 191, 255, 0.8) 60%, transparent);
    border-radius: 50%;
    transform: skew(-30deg);
    animation: fishSwim 25s linear infinite;
  }
  
  .fish-2 {
    width: 30px;
    height: 15px;
    top: 45%;
    left: -30px;
    background: linear-gradient(to right, transparent, rgba(255, 165, 0, 0.6) 40%, rgba(255, 165, 0, 0.8) 60%, transparent);
    border-radius: 50%;
    transform: skew(-30deg);
    animation: fishSwim 20s linear infinite;
    animation-delay: 5s;
  }
  
  .fish-3 {
    width: 50px;
    height: 25px;
    top: 60%;
    left: -50px;
    background: linear-gradient(to right, transparent, rgba(255, 105, 180, 0.6) 40%, rgba(255, 105, 180, 0.8) 60%, transparent);
    border-radius: 50%;
    transform: skew(-30deg);
    animation: fishSwim 30s linear infinite;
    animation-delay: 10s;
  }
  
  .seaweed {
    position: absolute;
    z-index: 1;
    display: flex;
    justify-content: space-around;
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
  
  .seaweed-strand {
    width: 20px;
    height: 100%;
    background: linear-gradient(to top, rgba(34, 139, 34, 0.8), rgba(34, 139, 34, 0.1));
    border-radius: 50% 50% 0 0;
    transform-origin: bottom center;
    animation: seaweedSway 10s ease-in-out infinite alternate;
  }
  
  .seaweed-1 .seaweed-strand:nth-child(1) { animation-delay: 0s; }
  .seaweed-1 .seaweed-strand:nth-child(2) { animation-delay: 1.5s; }
  .seaweed-1 .seaweed-strand:nth-child(3) { animation-delay: 3s; }
  .seaweed-2 .seaweed-strand:nth-child(1) { animation-delay: 2s; }
  .seaweed-2 .seaweed-strand:nth-child(2) { animation-delay: 4s; }
  
  /*
   * CYBERPUNK THEME STYLES
   */
  .cyberpunk {
    background: linear-gradient(to bottom, #111a2e 0%, #0a0a1e 100%);
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
    background-size: 20px 20px;
    animation: gridPulse 5s infinite alternate;
  }
  
  .grid-container {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    perspective: 1000px;
    transform-style: preserve-3d;
    animation: gridRotate 60s linear infinite;
  }
  
  .grid-horizontal, .grid-vertical {
    position: absolute;
    background: rgba(0, 255, 255, 0.2);
    box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
  }
  
  .grid-horizontal {
    width: 100%;
    height: 1px;
    left: 0;
    transform: translateZ(calc(var(--i) * 50px));
  }
  
  .grid-horizontal:nth-child(1) { top: 10%; --i: 1; animation-delay: 0.1s; }
  .grid-horizontal:nth-child(2) { top: 20%; --i: 2; animation-delay: 0.2s; }
  .grid-horizontal:nth-child(3) { top: 30%; --i: 3; animation-delay: 0.3s; }
  .grid-horizontal:nth-child(4) { top: 40%; --i: 4; animation-delay: 0.4s; }
  .grid-horizontal:nth-child(5) { top: 50%; --i: 5; animation-delay: 0.5s; }
  .grid-horizontal:nth-child(6) { top: 60%; --i: 6; animation-delay: 0.6s; }
  .grid-horizontal:nth-child(7) { top: 70%; --i: 7; animation-delay: 0.7s; }
  .grid-horizontal:nth-child(8) { top: 80%; --i: 8; animation-delay: 0.8s; }
  .grid-horizontal:nth-child(9) { top: 90%; --i: 9; animation-delay: 0.9s; }
  .grid-horizontal:nth-child(10) { top: 100%; --i: 10; animation-delay: 1s; }
  
  .grid-vertical {
    height: 100%;
    width: 1px;
    top: 0;
    transform: translateZ(calc(var(--i) * 50px));
  }
  
  .grid-vertical:nth-child(11) { left: 10%; --i: 1; animation-delay: 0.1s; }
  .grid-vertical:nth-child(12) { left: 20%; --i: 2; animation-delay: 0.2s; }
  .grid-vertical:nth-child(13) { left: 30%; --i: 3; animation-delay: 0.3s; }
  .grid-vertical:nth-child(14) { left: 40%; --i: 4; animation-delay: 0.4s; }
  .grid-vertical:nth-child(15) { left: 50%; --i: 5; animation-delay: 0.5s; }
  .grid-vertical:nth-child(16) { left: 60%; --i: 6; animation-delay: 0.6s; }
  .grid-vertical:nth-child(17) { left: 70%; --i: 7; animation-delay: 0.7s; }
  .grid-vertical:nth-child(18) { left: 80%; --i: 8; animation-delay: 0.8s; }
  .grid-vertical:nth-child(19) { left: 90%; --i: 9; animation-delay: 0.9s; }
  .grid-vertical:nth-child(20) { left: 100%; --i: 10; animation-delay: 1s; }
  
  .data-cube {
    position: absolute;
    width: 40px;
    height: 40px;
    background: rgba(255, 0, 128, 0.2);
    box-shadow: 0 0 20px rgba(255, 0, 128, 0.5);
    border: 1px solid rgba(255, 0, 128, 0.8);
    transform-style: preserve-3d;
    animation: cubeFly 15s linear infinite;
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
  
  .circuit {
    position: absolute;
    height: 2px;
    background: linear-gradient(to right, rgba(0, 255, 255, 0) 0%, rgba(0, 255, 255, 1) 50%, rgba(0, 255, 255, 0) 100%);
    animation: circuitPulse 5s infinite alternate;
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
  
  .hologram {
    position: absolute;
    border-radius: 5px;
    background: rgba(0, 255, 255, 0.1);
    box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
    border: 1px solid rgba(0, 255, 255, 0.5);
    animation: hologramFlicker 3s infinite alternate;
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
  
  /* Animations for all themes */
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
  
  @keyframes planetFloat3 {
    0% { transform: translate(0, 0); }
    25% { transform: translate(20px, 15px); }
    50% { transform: translate(40px, 0); }
    75% { transform: translate(20px, -15px); }
    100% { transform: translate(0, 0); }
  }
  
  @keyframes atmospherePulse {
    0% { opacity: 0.6; transform: scale(1); }
    100% { opacity: 0.9; transform: scale(1.1); }
  }
  
  @keyframes stormSpin {
    0% { transform: rotate(0deg) translateX(10px) rotate(0deg); }
    100% { transform: rotate(360deg) translateX(10px) rotate(-360deg); }
  }
  
  @keyframes moonsOrbit {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  /* Ocean theme animations */
  @keyframes bubbleFloat {
    0% { background-position: 0% 0%; }
    100% { background-position: 100% 100%; }
  }
  
  @keyframes bubbleRise {
    0% {
      transform: translateY(0) translateX(0);
      opacity: 0;
    }
    10% {
      opacity: 0.8;
    }
    90% {
      opacity: 0.5;
    }
    100% {
      transform: translateY(-100vh) translateX(20px);
      opacity: 0;
    }
  }
  
  @keyframes coralSway {
    0% { transform: scaleY(1) rotate(0deg); }
    100% { transform: scaleY(1.05) rotate(5deg); }
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
  
  @keyframes seaweedSway {
    0% { transform: rotate(-10deg); }
    100% { transform: rotate(10deg); }
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
  
  @keyframes cubeFly {
    0% {
      transform: translateX(0) rotateY(0deg);
      opacity: 0;
    }
    10% {
      opacity: 1;
    }
    90% {
      opacity: 1;
    }
    100% {
      transform: translateX(calc(100vw + 50px)) rotateY(360deg);
      opacity: 0;
    }
  }
  
  @keyframes circuitPulse {
    0% { 
      opacity: 0.3;
      transform: rotate(var(--rotation, 0deg)) scale(1);
      background-position: -100% 0;
    }
    100% { 
      opacity: 0.8;
      transform: rotate(var(--rotation, 0deg)) scale(1.05);
      background-position: 200% 0;
    }
  }
  
  @keyframes hologramFlicker {
    0%, 100% { 
      opacity: 0.5;
      box-shadow: 0 0 5px rgba(0, 255, 255, 0.3);
    }
    25% { 
      opacity: 0.8;
      box-shadow: 0 0 20px rgba(0, 255, 255, 0.6);
    }
    50% { 
      opacity: 0.4;
      box-shadow: 0 0 10px rgba(0, 255, 255, 0.2);
    }
    75% { 
      opacity: 0.7;
      box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
    }
  }
  </style>