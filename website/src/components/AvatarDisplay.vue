<template>
  <div class="avatar-display-container">
    <!-- Affichage de l'image si disponible -->
    <img
      v-if="avatarUrl"
      :src="avatarUrl"
      :alt="altText"
      :class="avatarClass"
      @error="handleImageError"
      @load="handleImageLoad"
    />
    <!-- Avatar générique si pas d'image -->
    <div
      v-else
      :class="`${avatarClass} generic-avatar`"
      :title="altText"
    >
      <span class="generic-avatar-icon">👤</span>
    </div>
    <!-- Indicateur de chargement -->
    <div v-if="isLoading && avatarUrl" class="avatar-loading">
      <div class="loading-spinner"></div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import PictureService from '@/services/PictureService'

export default {
  name: 'AvatarDisplay',
  props: {
    // Taille de l'avatar
    size: {
      type: String,
      default: 'medium' // small, medium, large
    },
    // Classes CSS additionnelles
    customClass: {
      type: String,
      default: ''
    },
    // Texte alternatif
    altText: {
      type: String,
      default: 'Avatar utilisateur'
    },
    // Type d'image à récupérer
    pictureType: {
      type: String,
      default: 'avatar'
    },
    // Fallback local (utilisé si PictureService échoue)
    fallbackLocal: {
      type: Boolean,
      default: true
    }
  },
  setup(props) {
    const avatarUrl = ref(null)
    const isLoading = ref(true)
    const loadError = ref(false)

    // Classes CSS basées sur la taille
    const avatarClass = computed(() => {
      const sizeClass = {
        small: 'avatar-small',
        medium: 'avatar-medium',
        large: 'avatar-large'
      }[props.size]

      return `avatar-image ${sizeClass} ${props.customClass}`
    })

    // Fonction pour charger l'avatar depuis PictureService
    const loadAvatarFromService = async () => {
      try {
        isLoading.value = true
        loadError.value = false

        // Récupérer l'avatar depuis PictureService
        const avatarBlob = await PictureService.retrievePicture(null, props.pictureType, 'url')
        
        if (avatarBlob) {
          avatarUrl.value = avatarBlob
          console.log('Avatar loaded from PictureService')
        } else {
          throw new Error('No avatar returned from service')
        }
      } catch (error) {
        console.log('Failed to load avatar from service:', error)
        loadError.value = true
        
        // Fallback vers localStorage si activé
        if (props.fallbackLocal) {
          loadAvatarFromLocalStorage()
        }
      } finally {
        isLoading.value = false
      }
    }

    // Fonction pour charger l'avatar depuis localStorage
    const loadAvatarFromLocalStorage = () => {
      try {
        const userProfile = localStorage.getItem('user_profile')
        
        if (userProfile) {
          const profile = JSON.parse(userProfile)
          if (profile.avatar) {
            avatarUrl.value = profile.avatar
            console.log('Avatar loaded from localStorage')
            return
          }
        }
        
        // Si pas d'avatar dans localStorage, garder l'image par défaut
        console.log('No avatar found in localStorage, using default')
      } catch (error) {
        console.error('Error loading avatar from localStorage:', error)
      }
    }

    // Gestion des erreurs de chargement d'image
    const handleImageError = () => {
      console.log('Image failed to load, showing generic avatar')
      avatarUrl.value = null
      loadError.value = true
    }

    // Gestion du chargement réussi
    const handleImageLoad = () => {
      isLoading.value = false
      loadError.value = false
    }

    // Fonction publique pour recharger l'avatar
    const reloadAvatar = () => {
      loadAvatarFromService()
    }

    // Charger l'avatar au montage
    onMounted(() => {
      loadAvatarFromService()
    })

    return {
      avatarUrl,
      isLoading,
      loadError,
      avatarClass,
      handleImageError,
      handleImageLoad,
      reloadAvatar
    }
  }
}
</script>

<style scoped>
.avatar-display-container {
  position: relative;
  display: inline-block;
}

.avatar-image {
  object-fit: cover;
  transition: all 0.3s ease;
  border-radius: 50%;
}

.avatar-small {
  width: 40px;
  height: 40px;
}

.avatar-medium {
  width: 100px;
  height: 100px;
}

.avatar-large {
  width: 200px;
  height: 200px;
}

.avatar-loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  width: 100%;
  height: 100%;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #f3f3f3;
  border-top: 2px solid #4285f4;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Avatar générique */
.generic-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  transition: all 0.3s ease;
  cursor: pointer;
  border: 3px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.generic-avatar:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.generic-avatar-icon {
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

/* Tailles d'icône pour l'avatar générique */
.avatar-small .generic-avatar-icon {
  font-size: 20px;
}

.avatar-medium .generic-avatar-icon {
  font-size: 50px;
}

.avatar-large .generic-avatar-icon {
  font-size: 100px;
}

/* Styles adaptatifs */
@media (max-width: 768px) {
  .avatar-small {
    width: 35px;
    height: 35px;
  }

  .avatar-medium {
    width: 80px;
    height: 80px;
  }

  .avatar-large {
    width: 150px;
    height: 150px;
  }

  /* Ajustements pour l'avatar générique sur mobile */
  .avatar-small .generic-avatar-icon {
    font-size: 18px;
  }

  .avatar-medium .generic-avatar-icon {
    font-size: 40px;
  }

  .avatar-large .generic-avatar-icon {
    font-size: 75px;
  }
}
</style> 