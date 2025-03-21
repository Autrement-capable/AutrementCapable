<!-- src/views/GamePage.vue -->
<template>
    <div class="game-page">
      <div class="game-container">
        <GameCanvas/>
        <GameControls @move="handleMove" @stop="handleStop"/>
      </div>
      <button @click="goHome" class="back-button">Quitter le jeu</button>
    </div>
  </template>
  
  <script>
  import { useRouter } from 'vue-router';
  import GameCanvas from '@/components/GameCanvas.vue';
  import GameControls from '@/components/GameControls.vue';
  
  export default {
    name: 'GamePage',
    components: {
      GameCanvas,
      GameControls
    },
    setup() {
      const router = useRouter();
  
      const handleMove = (direction) => {
        console.log('Move:', direction);
        // Cette fonction sera reliée au jeu
      };
  
      const handleStop = () => {
        console.log('Stop movement');
        // Cette fonction sera reliée au jeu
      };
  
      const goHome = () => {
        router.push('/');
      };
  
      return {
        handleMove,
        handleStop,
        goHome
      };
    }
  }
  </script>
  
  <style scoped>
  .game-page {
    width: 100%;
    height: 100vh;
    display: flex;
    flex-direction: column;
    background-color: #111;
    position: relative;
  }
  
  .game-container {
    flex: 1;
    position: relative;
    overflow: hidden;
  }
  
  .back-button {
    position: absolute;
    top: 20px;
    right: 20px;
    background-color: rgba(255, 255, 255, 0.2);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
    z-index: 100;
    transition: background-color 0.3s;
  }
  
  .back-button:hover {
    background-color: rgba(255, 255, 255, 0.3);
  }
  </style>