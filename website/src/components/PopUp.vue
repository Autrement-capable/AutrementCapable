<template>
  <div v-if="visible" class="overlay">
    <div class="popup-box">
      <span class="close-button" @click="closePopup">×</span>
      <img v-if="image" :src="image" alt="Popup Image" class="popup-image" />
      <p>{{ message }}</p>
      <div class="buttons">
        <button @click="cancelAction" class="cancel-btn">
          {{ buttonCancel }}
        </button>
        <button @click="confirmAction" class="confirm-btn">
          {{ buttonConfirm }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const props = defineProps({
  message: {
    type: String,
    default: 'Default popup message',
  },
  image: {
    type: String,
    default: '',
  },
  redirect: {
    type: String,
    default: '/',
  },
  buttonConfirm: {
    type: String,
    default: 'Default Yes',
  },
  buttonCancel: {
    type: String,
    default: 'Default No',
  },
  visible: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits(['close', 'confirm', 'cancel'])

function confirmAction() {
  emit('confirm')

  // Si c'est une fonction ou une méthode, l'exécuter
  if (typeof props.redirect === 'function') {
    const route = props.redirect()
    router.push(route)
  }
  // Sinon, rediriger vers l'URL fournie
  else if (props.redirect.startsWith('/')) {
    router.push(props.redirect)
  }
  // Pour les URLs externes
  else {
    window.location.href = props.redirect
  }
}

function cancelAction() {
  emit('cancel')
  emit('close')
}

function closePopup() {
  emit('close')
}
</script>

<style scoped>
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
  backdrop-filter: blur(3px);
}

.popup-box {
  background-color: white;
  padding: 2rem;
  max-width: 90%;
  width: 500px;
  border-radius: 1.5rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  animation: popupSlideIn 0.3s ease-out;
  position: relative;
}

@keyframes popupSlideIn {
  from {
    transform: scale(0.8) translateY(50px);
    opacity: 0;
  }
  to {
    transform: scale(1) translateY(0);
    opacity: 1;
  }
}

.close-button {
  position: absolute;
  top: 15px;
  right: 20px;
  font-size: 2rem;
  font-weight: bold;
  color: #9c9c9c;
  cursor: pointer;
  transition: color 0.2s ease;
  background-color: transparent;
  border: none;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-button:hover {
  color: #333333;
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 50%;
}

.popup-image {
  max-width: 120px;
  height: auto;
  margin-bottom: 1rem;
  border-radius: 12px;
}

.popup-box p {
  font-size: 1.2rem;
  color: #333;
  margin: 1rem 0 1.5rem 0;
  line-height: 1.5;
  font-weight: 500;
}

.buttons {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
  width: 100%;
  justify-content: center;
}

button {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
  min-width: 120px;
}

.confirm-btn {
  background: linear-gradient(135deg, #f44336, #d32f2f);
  color: white;
}

.confirm-btn:hover {
  background: linear-gradient(135deg, #d32f2f, #c62828);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4);
}

.cancel-btn {
  background: linear-gradient(135deg, #4caf50, #45a049);
  color: white;
}

.cancel-btn:hover {
  background: linear-gradient(135deg, #45a049, #3d8b40);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(244, 67, 54, 0.4);
}

/* Responsive */
@media (max-width: 480px) {
  .popup-box {
    padding: 1.5rem;
    width: 95%;
    max-width: none;
  }

  .popup-box p {
    font-size: 1.1rem;
  }

  .buttons {
    flex-direction: column;
    gap: 0.8rem;
  }

  button {
    width: 100%;
    min-width: auto;
  }
}
</style>
