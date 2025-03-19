// src/components/GameControls.vue - Composant pour les contrôles tactiles (optionnel pour mobile)
<template>
  <div class="game-controls" v-if="isMobile">
    <div class="control-pad">
      <button class="control-btn up" @touchstart="emit('move', 'up')" @touchend="emit('stop')">↑</button>
      <button class="control-btn left" @touchstart="emit('move', 'left')" @touchend="emit('stop')">←</button>
      <button class="control-btn right" @touchstart="emit('move', 'right')" @touchend="emit('stop')">→</button>
      <button class="control-btn down" @touchstart="emit('move', 'down')" @touchend="emit('stop')">↓</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  name: 'GameControls',
  setup(props, { emit }) {
    const isMobile = ref(false);

    onMounted(() => {
      // Détecter si l'appareil est mobile
      isMobile.value = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    });

    return {
      isMobile,
      emit
    };
  }
};
</script>

<style scoped>
.game-controls {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 100;
}

.control-pad {
  position: relative;
  width: 150px;
  height: 150px;
}

.control-btn {
  position: absolute;
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  user-select: none;
}

.up { top: 0; left: 50px; }
.left { top: 50px; left: 0; }
.right { top: 50px; right: 0; }
.down { bottom: 0; left: 50px; }
</style>
