// src/components/GameCanvas.vue
<template>
  <div class="game-canvas-container" ref="gameContainer"></div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import Game from '../game/game';

export default {
  name: 'GameCanvas',
  setup() {
    const gameContainer = ref(null);
    let game = null;

    onMounted(async () => {
      // Initialiser le jeu lorsque le composant est monté
      if (gameContainer.value) {
        game = new Game();
        await game.init(gameContainer.value); // Appel asynchrone
        await game.initialize();
        
        // Gérer le redimensionnement
        window.addEventListener('resize', handleResize);
      }
    });

    onBeforeUnmount(() => {
      // Nettoyer les ressources lorsque le composant est démonté
      if (game) {
        game.destroy();
      }
      window.removeEventListener('resize', handleResize);
    });

    const handleResize = () => {
      if (game) {
        game.resize();
      }
    };

    return {
      gameContainer
    };
  }
};
</script>

<style scoped>
.game-canvas-container {
  width: 100%;
  height: 100%;
  overflow: hidden;
  background-color: #000;
}
</style>