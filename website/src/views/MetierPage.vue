<template>
  <div
    class="metier-container"
    :class="{ expanded: isExpanded, 'high-contrast-mode': highContrastMode }"
  >
    <!-- En-tête avec personnage guide -->
    <div class="guide-character">
      <img src="@/assets/avatars/guide.png" alt="Guide" class="guide-avatar" />
      <div class="speech-bubble">
        <p>
          Découvre ce métier et ses spécificités. Utilise les boutons ci-dessous pour donner ton avis !
        </p>
      </div>
    </div>

    <div class="metier-header">
      <h1 class="metier-title">
        <span class="title-decoration">★</span>
        {{ metierName }}
        <span class="title-decoration">★</span>
      </h1>
    </div>

    <div class="video-container">
      <video controls :poster="posterSrc" autoplay>
        <source :src="videoSrc" type="video/mp4" />
        Votre navigateur ne supporte pas la vidéo.
      </video>
    </div>

    <div class="description-card">
      <p class="description-text">{{ description }}</p>
    </div>

    <div class="additional-info">
      <div class="info-section skills-section">
        <h2 class="section-title">Compétences requises</h2>
        <ul class="skills-list">
          <li v-for="(skill, index) in skills" :key="index" class="skill-item">
            <div class="skill-icon">💪</div>
            <div class="skill-text">{{ skill }}</div>
          </li>
        </ul>
      </div>

      <div class="info-section environment-section">
        <h2 class="section-title">Environnement de travail</h2>
        <div class="environment-card">
          <p>{{ workEnvironment }}</p>
        </div>
      </div>

      <div class="info-section job-details-section">
        <h2 class="section-title">Détails du métier</h2>
        <div class="job-details-card" v-html="jobDetails"></div>
      </div>
    </div>

    <div class="button-container">
      <button @click="onLike" class="action-button like-button">
        <span class="button-icon">👍</span>
        <span class="button-text">J'aime</span>
      </button>
      <button @click="onNeutral" class="action-button neutral-button">
        <span class="button-icon">🤔</span>
        <span class="button-text">Je ne sais pas</span>
      </button>
      <button @click="onDislike" class="action-button dislike-button">
        <span class="button-icon">👎</span>
        <span class="button-text">Je n'aime pas</span>
      </button>
    </div>

    <!-- Contrôles d'accessibilité -->
    <div class="accessibility-controls">
      <button
        @click="toggleSound"
        class="accessibility-button"
        aria-label="Activer/désactiver le son"
      >
        <span v-if="soundEnabled">🔊</span>
        <span v-else>🔇</span>
      </button>
      <button @click="toggleHighContrast" class="accessibility-button">
        <span v-if="highContrastMode">🌓</span>
        <span v-else>🌑</span>
      </button>
    </div>
  </div>
  <div class="extra-space"></div>
</template>

<script>
export default {
  name: 'MetierPage',
  props: {
    metierName: { type: String, required: true },
    description: { type: String, required: true },
    videoSrc: { type: String, required: true },
    posterSrc: { type: String, required: true },
    skills: { type: Array, required: true },
    workEnvironment: { type: String, required: true },
    jobDetails: { type: String, required: true },
    nextRoute: { type: String, default: null },
  },
  data() {
    return {
      isExpanded: true, // Toujours à true pour montrer tous les détails
      highContrastMode: false,
      textSizeLevel: 0,
      soundEnabled: true,
      isReading: false,
      speechUtterance: null,
    }
  },
  watch: {
    // Observer les changements des propriétés pour mettre à jour la lecture
    metierName() {
      // Si le métier change, arrêter la lecture en cours
      this.stopReading()

      // Si le son est activé, lancer la lecture du nouveau métier
      if (this.soundEnabled) {
        // Petit délai pour s'assurer que les nouvelles données sont bien chargées
        setTimeout(() => {
          this.readDescriptionAloud()
        }, 300)
      }
    },
  },
  mounted() {
    this.loadAccessibilitySettings()

    // Initialiser les voix de synthèse vocale
    if ('speechSynthesis' in window) {
      // Certains navigateurs chargent les voix de manière asynchrone
      if (window.speechSynthesis.getVoices().length === 0) {
        window.speechSynthesis.onvoiceschanged = () => {
          window.speechSynthesis.getVoices()
        }
      }
    }

    // Si le son est activé, lancer la lecture automatiquement
    if (this.soundEnabled) {
      // Petit délai pour s'assurer que le composant est complètement monté
      setTimeout(() => {
        this.readDescriptionAloud()
      }, 300)
    }
    
    // Marquer ce métier comme vu dans le localStorage
    this.markMetierAsSeen();
  },
  beforeUnmount() {
    // S'assurer que la lecture est arrêtée lors de la destruction du composant
    this.stopReading()
  },
  methods: {
    // Marquer le métier comme vu
    markMetierAsSeen() {
      try {
        // Récupérer les métiers déjà vus
        const savedIds = localStorage.getItem('seen-metiers') || '[]';
        const seenIds = JSON.parse(savedIds);
        
        // Extraire le slug à partir des props (via l'URL)
        let slug = '';
        if (this.$route && this.$route.params && this.$route.params.slug) {
          slug = this.$route.params.slug;
        } else {
          // Fallback: obtenir le slug à partir du videoSrc ou d'une autre propriété
          const videoPath = this.videoSrc || '';
          if (videoPath.includes('Soudeur')) {
            slug = 'soudeur';
          } else if (videoPath.includes('Jardinier')) {
            slug = 'jardinier-paysagiste';
          } else if (videoPath.includes('Coiffeur')) {
            slug = 'coiffeur';
          }
        }
        
        // Table de correspondance slug -> id
        const slugToId = {
          'soudeur': 16,
          'jardinier-paysagiste': 11,
          'coiffeur': 10,
          'infographiste': 1,
          'administrateur-reseau': 2,
          'technicien-telecoms-reseau': 3,
          'webdesigner': 4,
          'cuisinier': 5,
          'boucher': 6,
          'boulanger': 7,
          'ingenieur-rd-agroequipement': 8,
          'conducteur-machines-agricoles': 9,
          'horticulteur': 10,
          'tapissier-ameublement': 12,
          'prothesiste-dentaire': 13,
          'mecatronicien': 14,
          'tailleur-couturier': 15
        };
        
        // Si on a trouvé un ID correspondant au slug et qu'il n'est pas déjà dans les métiers vus
        if (slug && slugToId[slug] && !seenIds.includes(slugToId[slug])) {
          seenIds.push(slugToId[slug]);
          localStorage.setItem('seen-metiers', JSON.stringify(seenIds));
          
          // Vérifier si l'utilisateur a vu au moins 3 métiers pour débloquer le badge
          if (seenIds.length >= 3) {
            this.checkBadgeUnlock(seenIds.length);
          }
        }
      } catch (error) {
        console.error('Erreur lors du marquage du métier comme vu:', error);
      }
    },
    
    // Vérifier si un badge peut être débloqué
    checkBadgeUnlock(seenCount) {
      // Importer les fonctions de badge si nécessaire
      try {
        const { unlockBadge, isBadgeUnlocked } = require('@/utils/badges');
        
        // Badge Apprenti des métiers (3 métiers vus)
        if (seenCount >= 3 && !isBadgeUnlocked(7)) {
          unlockBadge(7);
        }
        
        // Badge Chercheur curieux (10 métiers vus)
        if (seenCount >= 10 && !isBadgeUnlocked(3)) {
          unlockBadge(3);
        }
      } catch (error) {
        console.error('Erreur lors de la vérification des badges:', error);
      }
    },
    
    navigateToNextMetier() {
      if (this.nextRoute) {
        this.stopReading()
        this.$router.push({ name: this.nextRoute })
      }
    },
    onLike() {
      console.log('User likes this métier!')
      // Sauvegarder le métier dans les favoris
      this.saveLikedMetier();
      this.navigateToNextMetier()
    },
    onNeutral() {
      console.log('User is neutral about this métier.')
      this.navigateToNextMetier()
    },
    onDislike() {
      console.log('User dislikes this métier.')
      this.navigateToNextMetier()
    },
    
    // Sauvegarder le métier aimé
    saveLikedMetier() {
      try {
        // Récupérer les métiers déjà aimés
        const savedIds = localStorage.getItem('liked-metiers') || '[]';
        const likedIds = JSON.parse(savedIds);
        
        // Extraire le slug à partir des props (via l'URL)
        let slug = '';
        if (this.$route && this.$route.params && this.$route.params.slug) {
          slug = this.$route.params.slug;
        } else {
          // Fallback: obtenir le slug à partir du videoSrc ou d'une autre propriété
          const videoPath = this.videoSrc || '';
          if (videoPath.includes('Soudeur')) {
            slug = 'soudeur';
          } else if (videoPath.includes('Jardinier')) {
            slug = 'jardinier-paysagiste';
          } else if (videoPath.includes('Coiffeur')) {
            slug = 'coiffeur';
          }
        }
        
        // Table de correspondance slug -> id
        const slugToId = {
          'soudeur': 16,
          'jardinier-paysagiste': 11,
          'coiffeur': 10,
          'infographiste': 1,
          'administrateur-reseau': 2,
          'technicien-telecoms-reseau': 3,
          'webdesigner': 4,
          'cuisinier': 5,
          'boucher': 6,
          'boulanger': 7,
          'ingenieur-rd-agroequipement': 8,
          'conducteur-machines-agricoles': 9,
          'horticulteur': 10,
          'tapissier-ameublement': 12,
          'prothesiste-dentaire': 13,
          'mecatronicien': 14,
          'tailleur-couturier': 15
        };
        
        // Si on a trouvé un ID correspondant au slug et qu'il n'est pas déjà dans les métiers aimés
        if (slug && slugToId[slug] && !likedIds.includes(slugToId[slug])) {
          likedIds.push(slugToId[slug]);
          localStorage.setItem('liked-metiers', JSON.stringify(likedIds));
          
          // Vérifier le badge Passionné des métiers (5 métiers aimés)
          if (likedIds.length >= 5) {
            try {
              const { unlockBadge, isBadgeUnlocked } = require('@/utils/badges');
              if (!isBadgeUnlocked(2)) {
                unlockBadge(2);
              }
            } catch (error) {
              console.error('Erreur lors du déblocage du badge:', error);
            }
          }
        }
      } catch (error) {
        console.error('Erreur lors de la sauvegarde du métier aimé:', error);
      }
    },
    
    // Fonctions d'accessibilité
    toggleHighContrast() {
      this.highContrastMode = !this.highContrastMode
      this.saveAccessibilitySettings()
    },
    increaseTextSize() {
      if (this.textSizeLevel < 1) {
        this.textSizeLevel++
        this.applyTextSize()
        this.saveAccessibilitySettings()
      }
    },
    decreaseTextSize() {
      if (this.textSizeLevel > -1) {
        this.textSizeLevel--
        this.applyTextSize()
        this.saveAccessibilitySettings()
      }
    },
    applyTextSize() {
      const container = document.querySelector('.metier-container')
      if (!container) return

      // Supprimer les classes de taille précédentes
      container.classList.remove('text-small', 'text-large')

      // Ajouter la classe appropriée
      if (this.textSizeLevel === -1) {
        container.classList.add('text-small')
      } else if (this.textSizeLevel === 1) {
        container.classList.add('text-large')
      }
    },
    loadAccessibilitySettings() {
      const settings = localStorage.getItem('metierAccessibilitySettings')
      if (settings) {
        const { highContrastMode, textSizeLevel, soundEnabled } =
          JSON.parse(settings)
        this.highContrastMode = highContrastMode
        this.textSizeLevel = textSizeLevel
        if (soundEnabled !== undefined) {
          this.soundEnabled = soundEnabled
        }
        this.applyTextSize()
      }
    },
    saveAccessibilitySettings() {
      const settings = {
        highContrastMode: this.highContrastMode,
        textSizeLevel: this.textSizeLevel,
        soundEnabled: this.soundEnabled,
      }
      localStorage.setItem(
        'metierAccessibilitySettings',
        JSON.stringify(settings)
      )
    },
    // Fonctions de gestion du son
    toggleSound() {
      this.soundEnabled = !this.soundEnabled
      this.saveAccessibilitySettings()

      if (!this.soundEnabled) {
        this.stopReading()
      } else {
        // Si le son est activé, commencer la lecture
        this.readDescriptionAloud()
      }
    },
    // Fonctions de lecture audio
    readDescriptionAloud() {
      if (!('speechSynthesis' in window) || !this.soundEnabled) {
        return
      }

      // Arrêter toute lecture en cours
      this.stopReading()

      // Récupérer les textes à lire
      const detailsTexts = []

      // Titre du métier
      detailsTexts.push(`Métier: ${this.metierName}`)

      // Description principale
      detailsTexts.push(this.description)

      // Informations supplémentaires
      // Compétences requises
      detailsTexts.push(`Compétences requises: ${this.skills.join(', ')}`)

      // Environnement de travail
      detailsTexts.push(`Environnement de travail: ${this.workEnvironment}`)

      // Détails du métier (nettoyer le HTML)
      const tempDiv = document.createElement('div')
      tempDiv.innerHTML = this.jobDetails
      detailsTexts.push(`Détails du métier: ${tempDiv.textContent}`)

      // Joindre tous les textes avec des pauses
      const textToRead = detailsTexts.join('. ')

      // Créer une nouvelle instance de synthèse vocale
      this.speechUtterance = new SpeechSynthesisUtterance(textToRead)
      this.speechUtterance.lang = 'fr-FR'
      this.speechUtterance.rate = 0.9 // Vitesse légèrement plus lente pour une meilleure compréhension

      // Utiliser une voix française si disponible
      const voices = window.speechSynthesis.getVoices()
      const frenchVoice = voices.find((voice) => voice.lang.includes('fr'))
      if (frenchVoice) {
        this.speechUtterance.voice = frenchVoice
      }

      // Événements pour suivre l'état de la lecture
      this.speechUtterance.onstart = () => {
        this.isReading = true
      }

      this.speechUtterance.onend = () => {
        this.isReading = false
      }

      this.speechUtterance.onerror = () => {
        this.isReading = false
      }

      // Démarrer la lecture
      window.speechSynthesis.speak(this.speechUtterance)
      this.isReading = true
    },
    stopReading() {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel()
        this.isReading = false
      }
    },
  },
}
</script>

<style scoped>
.metier-container {
  font-family: 'Comic Sans MS', 'Chalkboard SE', 'Marker Felt', sans-serif;
  max-width: 1000px; /* Déjà à la taille maximale */
  margin: 20px auto;
  padding: 20px;
  background-color: #f5f8ff;
  border-radius: 20px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: all 0.3s ease;
  overflow: hidden;
}

/* Guide character styling - adapté de ScenarioList & SkillsWheelPage */
.guide-character {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
}

.guide-avatar {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  border: 3px solid #ffc107;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.speech-bubble {
  position: relative;
  background-color: #fff;
  border-radius: 15px;
  padding: 15px;
  margin-left: 15px;
  box-shadow: 0 3px 5px rgba(0, 0, 0, 0.1);
  max-width: 70%;
}

.speech-bubble:before {
  content: '';
  position: absolute;
  left: -10px;
  top: 50%;
  transform: translateY(-50%);
  border-width: 10px 10px 10px 0;
  border-style: solid;
  border-color: transparent #fff transparent transparent;
}

.speech-bubble p {
  margin: 0;
  font-size: 1.1rem;
  color: #333;
}

/* En-tête du métier */
.metier-header {
  margin-bottom: 20px;
  text-align: center;
}

.metier-title {
  font-size: 2.2rem;
  color: #3f51b5;
  margin: 0;
  position: relative;
  padding-bottom: 10px;
  display: inline-block;
}

.title-decoration {
  color: #ffd700;
  margin: 0 10px;
}

/* Conteneur vidéo */
.video-container {
  margin: 20px auto;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.video-container video {
  width: 90%;
  max-width: 800px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: block;
  margin: 0 auto;
}

/* Carte de description */
.description-card {
  background-color: #fff;
  border-radius: 12px;
  padding: 20px;
  margin: 20px 0;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
}

.description-text {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #333;
  margin: 0;
}

/* Sections d'informations supplémentaires */
.additional-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 30px;
  animation: fadeIn 0.5s ease;
}

.info-section {
  background-color: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
}

.section-title {
  font-size: 1.4rem;
  color: #3f51b5;
  margin-top: 0;
  margin-bottom: 15px;
  text-align: center;
}

/* Section compétences */
.skills-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
  list-style: none;
  padding: 0;
}

.skill-item {
  display: flex;
  align-items: center;
  background-color: #f5f8ff;
  padding: 10px 15px;
  border-radius: 10px;
  transition: transform 0.2s ease;
}

.skill-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.skill-icon {
  margin-right: 10px;
  font-size: 1.2rem;
}

.skill-text {
  font-size: 1rem;
}

/* Section environnement de travail */
.environment-card {
  background-color: #f5f8ff;
  border-radius: 10px;
  padding: 15px;
  margin-top: 10px;
}

/* Section détails du métier */
.job-details-card {
  background-color: #f5f8ff;
  border-radius: 10px;
  padding: 15px;
  margin-top: 10px;
}

/* Conteneur de boutons */
.button-container {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 30px;
  flex-wrap: wrap;
}

/* Boutons d'action */
.action-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 20px;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
  font-family: inherit;
}

.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
}

.button-icon {
  margin-right: 8px;
}

.expand-button {
  background-color: #17a2b8;
  color: white;
  margin-top: 15px;
}

.like-button {
  background-color: #28a745;
  color: white;
}

.neutral-button {
  background-color: #6c757d;
  color: white;
}

.dislike-button {
  background-color: #dc3545;
  color: white;
}

/* Espace supplémentaire */
.extra-space {
  height: 100px;
}

/* Contrôles d'accessibilité */
.accessibility-controls {
  position: absolute;
  top: 15px;
  right: 15px;
  display: flex;
  gap: 5px;
  z-index: 50;
}

.accessibility-button {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  border: none;
  background-color: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}

.accessibility-button:hover {
  background-color: #e9ecef;
  transform: scale(1.1);
}

.accessibility-button.active {
  background-color: #007bff;
  color: white;
}

/* Adaptations de taille de texte */
.metier-container.text-small {
  font-size: 0.9em;
}

.metier-container.text-large {
  font-size: 1.2em;
}

/* Mode contraste élevé */
.high-contrast-mode {
  background-color: #000;
  color: #fff;
}

.high-contrast-mode .description-card,
.high-contrast-mode .info-section,
.high-contrast-mode .skill-item,
.high-contrast-mode .environment-card,
.high-contrast-mode .job-details-card,
.high-contrast-mode .speech-bubble {
  background-color: #222;
  color: #fff;
  border: 1px solid #444;
}

.high-contrast-mode .speech-bubble:before {
  border-right-color: #222;
}

.high-contrast-mode .metier-title,
.high-contrast-mode .section-title {
  color: #fff;
}

.high-contrast-mode video {
  border: 2px solid #fff;
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Responsive design */
@media (max-width: 768px) {
  .metier-container {
    padding: 15px;
  }

  .metier-title {
    font-size: 1.8rem;
  }

  .description-text {
    font-size: 1rem;
  }

  .skills-list {
    grid-template-columns: 1fr 1fr;
  }

  .button-container {
    flex-direction: column;
    align-items: center;
  }

  .action-button {
    width: 80%;
  }
}

@media (max-width: 480px) {
  .skills-list {
    grid-template-columns: 1fr;
  }

  .guide-character {
    flex-direction: column;
    text-align: center;
  }

  .speech-bubble {
    margin-left: 0;
    margin-top: 15px;
    max-width: 100%;
  }

  .speech-bubble:before {
    display: none;
  }

  .guide-avatar {
    width: 60px;
    height: 60px;
  }
}
</style>