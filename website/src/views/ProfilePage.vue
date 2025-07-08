<template>
    <div class="profile-container" :class="{ 'high-contrast-mode': highContrastMode }">
      <!-- Animation de déblocage du badge -->
      <div v-if="showBadgeUnlockAnimation" class="badge-unlock-overlay">
        <div class="badge-unlock-animation">
          <div class="badge-icon">{{ newlyUnlockedBadge.icon }}</div>
          <h2>Badge débloqué !</h2>
          <h3>{{ newlyUnlockedBadge.title }}</h3>
          <p>{{ newlyUnlockedBadge.description }}</p>
          <button @click="closeBadgeAnimation" class="close-animation-btn">Continuer</button>
        </div>
      </div>
  
      <!-- Barre de navigation et titre -->
      <div class="profile-header">
        <h1 class="main-title">Mon Profil</h1>
        <p class="subtitle">Apprends à mieux te connaître !</p>

      </div>
  
      <!-- Menu de navigation -->
      <div class="navigation-tabs">
        <button 
          v-for="(tab, index) in tabs" 
          :key="index" 
          @click="currentTab = tab.id" 
          class="tab-button"
          :class="{ 'active': currentTab === tab.id }"
        >
          <span class="tab-icon">{{ tab.icon }}</span>
          <span class="tab-label">{{ tab.name }}</span>
        </button>
      </div>
  
      <!-- Contenu principal -->
      <div class="profile-content">
        <!-- Section Informations Personnelles -->
        <div v-if="currentTab === 'personal'" class="profile-section">
          <h2 class="section-title">
            <span class="section-icon">👤</span>
            Mes Informations
          </h2>
          
          <div class="personal-info-container">
            <div class="avatar-section">
              <div class="avatar-container">
                <AvatarDisplay 
                  size="large" 
                  custom-class="user-avatar"
                  alt-text="Avatar utilisateur"
                  picture-type="avatar"
                />
              </div>
              <div class="level-indicator">
                <div class="level-badge">Niveau {{ calculateLevel() }}</div>
                <div class="exp-bar">
                  <div class="exp-fill" :style="{ width: getExpPercentage() + '%' }"></div>
                </div>
              </div>
            </div>
            
            <div class="info-fields">
              <div class="info-field">
                <label>Prénom</label>
                <div class="field-value">{{ userProfile.firstName }}</div>
              </div>
              
              <div class="info-field">
                <label>Âge</label>
                <div class="field-value">{{ userProfile.age }} ans</div>
              </div>
              
              <div class="info-field">
                <label>Ville</label>
                <div class="field-value">{{ userProfile.city }}</div>
              </div>
              
              <div class="info-field">
                <label>Mes Loisirs</label>
                <div class="hobbies-container">
                  <div v-for="(hobby, index) in userProfile.hobbies" 
                      :key="index" 
                      class="hobby-tag"
                      :data-hobby="hobby">
                    {{ hobby }}
                  </div>
                  <button @click="showHobbyEditor = true" class="add-hobby-button">+</button>
                </div>
              </div>

              <div class="info-field">
                <label>À propos de moi</label>
                <div class="field-value bio">{{ userProfile.bio || "Ajoute une description de toi-même !" }}</div>
                <button @click="showBioEditor = true" class="edit-button">Modifier</button>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Section Compétences -->
        <div v-if="currentTab === 'skills'" class="profile-section">
          <h2 class="section-title">
            <span class="section-icon">🎯</span>
            Mes Points Forts
          </h2>
          
          <div class="skills-container">
            <!-- Remplacer le graphique complexe par une présentation plus simple -->
            <div class="skills-simplified">
              <p class="skills-intro">Ce que je sais bien faire :</p>
              
              <!-- Affichage simplifié des catégories de compétences -->
              <div class="skills-categories-simple">
                <div v-for="(category, catIndex) in skillCategories" :key="catIndex" class="skill-category-simple">
                  <h3 class="category-title-simple">
                    <span class="category-icon-large">{{ category.icon }}</span>
                    {{ category.name }}
                  </h3>
                  
                  <div class="skills-list-simple">
                    <div v-for="skill in getSkillsByCategory(category.id)" :key="skill.id" class="skill-item-simple">
                      <div class="skill-icon-simple" :style="{backgroundColor: getLevelColor(skill.level)}">
                        {{ getSkillIcon(skill.id) }}
                      </div>
                      <div class="skill-info-simple">
                        <div class="skill-name-simple">{{ skill.name }}</div>
                        <!-- Remplacer les niveaux numériques par des étoiles -->
                        <div class="skill-stars">
                          <span v-for="n in 5" :key="n" class="skill-star" :class="{ 'filled': n <= skill.level }">★</span>
                        </div>
                        <!-- Ajouter une description simple du niveau -->
                        <div class="skill-level-simple" v-html="getSimpleSkillLevel(skill.level)"></div>
                      </div>
                    </div>
                    
                    <div v-if="getSkillsByCategory(category.id).length === 0" class="empty-category-simple">
                      Tu découvriras tes points forts en jouant aux jeux !
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Section Intérêts Professionnels -->
        <div v-if="currentTab === 'career'" class="profile-section">
          <h2 class="section-title">
            <span class="section-icon">💼</span>
            Mes Intérêts Professionnels
          </h2>
          
          <div class="careers-container">
            <div v-if="likedJobs.length > 0" class="liked-jobs-section">
              <h3 class="subsection-title">Métiers qui m'intéressent</h3>
              <div class="jobs-grid">
                <div v-for="job in likedJobs" :key="job.id" class="job-card">
                  <div class="job-image-container">
                    <img :src="job.poster || 'src/assets/job-placeholder.jpg'" alt="Métier" class="job-image" />
                  </div>
                  <div class="job-info">
                    <h4 class="job-title">{{ job.name }}</h4>
                    <div class="job-skills">
                      <div v-for="(skill, index) in job.skills.slice(0, 3)" :key="index" class="job-skill-tag">
                        {{ skill }}
                      </div>
                      <div v-if="job.skills.length > 3" class="job-skill-more">+{{ job.skills.length - 3 }}</div>
                    </div>
                    <button @click="viewJobDetails(job)" class="view-job-button">
                      Voir détails
                    </button>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-else class="empty-job-interests">
              <div class="empty-icon">💼</div>
              <p>Tu n'as pas encore sélectionné de métiers qui t'intéressent.</p>
              <button @click="goToJobDiscovery" class="action-button">
                Découvrir des métiers
              </button>
            </div>
            
            <div class="career-skills-match">
              <h3 class="subsection-title">Mes compétences professionnelles</h3>
              <div class="career-skills-grid">
                <div v-for="(skill, index) in topCareerSkills" :key="index" class="career-skill-card">
                  <div class="career-skill-icon">{{ getSkillIcon(skill.id) }}</div>
                  <div class="career-skill-info">
                    <div class="career-skill-name">{{ skill.name }}</div>
                    <div class="career-skill-match">
                      Correspond à {{ skill.matchingJobs }} métiers
                    </div>
                  </div>
                </div>
                
                <div v-if="topCareerSkills.length === 0" class="empty-career-skills">
                  Joue aux jeux pour découvrir tes compétences professionnelles !
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Section CV et Présentation -->
        <div v-if="currentTab === 'cv'" class="profile-section">
          <h2 class="section-title">
            <span class="section-icon">📄</span>
            Mon CV et Ma Présentation
          </h2>
          
          <div class="cv-container">
            <div class="cv-preview" :class="'cv-style-' + currentCVStyle" :style="{ '--cv-color': currentCVColor }">
							<div class="cv-header">
								<h3 class="cv-name">{{ userProfile.firstName }} {{ userProfile.lastName }}</h3>
								<div class="cv-contact">{{ userProfile.age }} ans | {{ userProfile.city }}</div>
							</div>
              
              <div class="cv-section">
                <h4 class="cv-section-title">Mes points forts</h4>
                <div class="cv-strength-grid">
                  <div v-for="(skill, index) in topSkills" :key="index" class="cv-skill-item">
                    <div class="cv-skill-icon">{{ getSkillIcon(skill.id) }}</div>
                    <div class="cv-skill-name">{{ skill.name }}</div>
                  </div>
                  
                  <div v-if="topSkills.length === 0" class="cv-empty-section">
                    Joue aux jeux pour découvrir tes points forts !
                  </div>
                </div>
              </div>
              
              <div class="cv-section">
                <h4 class="cv-section-title">Métiers qui m'intéressent</h4>
                <div class="cv-jobs-list">
                  <div v-for="(job, index) in likedJobs.slice(0, 3)" :key="index" class="cv-job-item">
                    <div class="cv-job-name">{{ job.name }}</div>
                  </div>
                  
                  <div v-if="likedJobs.length === 0" class="cv-empty-section">
                    Explore des métiers pour compléter cette section !
                  </div>
                </div>
              </div>
              
              <div class="cv-section">
                <h4 class="cv-section-title">À propos de moi</h4>
                <div class="cv-bio">{{ userProfile.bio || "Ajoute une description de toi-même !" }}</div>
              </div>
              
              <div class="cv-actions">
                <button @click="printCV" class="cv-button print-button">
                  <span class="button-icon">🖨️</span>
                  Imprimer
                </button>
                <button @click="downloadCV" class="cv-button download-button">
                  <span class="button-icon">💾</span>
                  Télécharger
                </button>
              </div>
            </div>
            
            <div class="cv-customize">
              <h3 class="customize-title">Personnaliser mon CV</h3>
              <div class="customize-options">
                <div class="customize-option">
                  <label>Style de CV</label>
                  <div class="style-options">
                    <button 
                      v-for="(style, index) in cvStyles" 
                      :key="index" 
                      @click="selectCVStyle(style.id)"
                      class="style-button"
                      :class="{ 'active': currentCVStyle === style.id }"
                    >
                      {{ style.name }}
                    </button>
                  </div>
                </div>
                
                <div class="customize-option">
                  <label>Couleur principale</label>
                  <div class="color-options">
                    <div 
                      v-for="(color, index) in cvColors" 
                      :key="index"
                      @click="selectCVColor(color.value)"
                      class="color-button"
                      :class="{ 'active': currentCVColor === color.value }"
                      :style="{ backgroundColor: color.value }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Modales -->
      <!-- Éditeur de biographie -->
      <div v-if="showBioEditor" class="modal-overlay">
        <div class="modal-content">
          <h3 class="modal-title">Modifier ma description</h3>
          <textarea 
            v-model="editedBio" 
            class="bio-textarea" 
            placeholder="Parle de toi, de ce que tu aimes..."
          ></textarea>
          <div class="modal-actions">
            <button @click="showBioEditor = false" class="modal-button cancel-button">Annuler</button>
            <button @click="saveBio" class="modal-button save-button">Enregistrer</button>
          </div>
        </div>
      </div>
  
      <!-- Éditeur de loisirs -->
      <div v-if="showHobbyEditor" class="modal-overlay">
        <div class="modal-content">
          <h3 class="modal-title">Modifier mes loisirs</h3>
          <div class="hobby-editor">
            <div class="current-hobbies">
              <div 
                v-for="(hobby, index) in editedHobbies" 
                :key="index" 
                class="hobby-editor-item"
              >
                <span class="hobby-name">{{ hobby }}</span>
                <button @click="removeHobby(index)" class="remove-hobby-button">✕</button>
              </div>
            </div>
            <div class="add-hobby-form">
              <input 
                v-model="newHobby" 
                class="hobby-input" 
                placeholder="Ajoute un loisir..."
                @keyup.enter="addHobby"
              />
              <button @click="addHobby" class="add-button">Ajouter</button>
            </div>
          </div>
          <div class="modal-actions">
            <button @click="showHobbyEditor = false" class="modal-button cancel-button">Annuler</button>
            <button @click="saveHobbies" class="modal-button save-button">Enregistrer</button>
          </div>
        </div>
      </div>
  
      <!-- Détails du badge -->
      <div v-if="selectedBadge" class="modal-overlay" @click="closeModal">
        <div class="badge-modal" @click.stop>
          <button class="close-button" @click="closeModal">×</button>
  
          <div class="badge-detail-content">
            <div
              class="badge-detail-icon"
              :style="{ backgroundColor: selectedBadge.iconColor || '#e0e0e0' }"
            >
              <span class="badge-detail-emoji">{{ selectedBadge.icon }}</span>
            </div>
  
            <h2 class="badge-detail-title">{{ selectedBadge.title }}</h2>
  
            <p class="badge-detail-description">
              {{ selectedBadge.unlocked ? selectedBadge.description : (selectedBadge.hint || 'Continue à jouer pour débloquer ce badge !') }}
            </p>
  
            <div v-if="selectedBadge.unlocked" class="badge-achievement">
              <div class="achievement-date">
                Obtenu le: {{ formatDate(selectedBadge.dateUnlocked) }}
              </div>
              <div class="achievement-game">
                Dans: {{ selectedBadge.game }}
              </div>
            </div>
            <div v-else class="badge-locked-info">
              <div class="badge-hint">
                <span class="hint-icon">💡</span>
                <p>{{ selectedBadge.hint || 'Continue à jouer pour débloquer ce badge !' }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Guide d'aide contextuel -->
      <div class="profile-guide" v-if="showGuide">
        <div class="guide-character">
          <img src="@/assets/flamou/hey.png" alt="Guide" class="guide-avatar" />
        </div>
        <div class="guide-bubble">
          <p>{{ guideMessage }}</p>
          <button @click="dismissGuide" class="guide-dismiss-button">Compris !</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted, computed, nextTick } from 'vue';
  import html2pdf from 'html2pdf.js';
  import defaultAvatar from '@/assets/pdp.png';
  import AvatarDisplay from '@/components/AvatarDisplay.vue';
  
  export default {
    name: 'UserProfile',
    components: {
      AvatarDisplay,
    },
    setup() {
      // État du profil
      const userProfile = ref({
        firstName: 'Lucas',
        lastName: 'Martin',
        age: 16,
        city: 'Lyon',
        avatar: defaultAvatar,
        bio: "Je suis quelqu'un de curieux et j'aime découvrir de nouvelles choses. Je m'intéresse particulièrement aux jeux vidéo et à la musique.",
        hobbies: ['Jeux vidéo', 'Musique', 'Dessin', 'Natation'],
        experience: 150, // Points d'expérience pour calculer le niveau
      });
  
      // États des onglets de navigation
      const tabs = [
        { id: 'personal', name: 'Informations', icon: '👤' },
        { id: 'skills', name: 'Compétences', icon: '🎯' },
        { id: 'career', name: 'Métiers', icon: '💼' },
        { id: 'cv', name: 'Mon CV', icon: '📄' },
      ];
      const currentTab = ref('personal');
  
      // États pour les éditeurs et modales
      const showBioEditor = ref(false);
      const editedBio = ref(userProfile.value.bio);
      const showHobbyEditor = ref(false);
      const editedHobbies = ref([...userProfile.value.hobbies]);
      const newHobby = ref('');
      const selectedAvatar = ref(userProfile.value.avatar);
      const selectedBadge = ref(null);
  
      // États pour l'animation de badge
      const showBadgeUnlockAnimation = ref(false);
      const newlyUnlockedBadge = ref(null);
  
      // État d'accessibilité
      const highContrastMode = ref(false);
      const soundEnabled = ref(true);
      const textSizeLevel = ref(0); // 0 = normal, -1 = petit, 1 = grand
  
      // État du guide contextuel
      const showGuide = ref(true);
      const guideMessage = ref("Bienvenue sur ton profil ! Ici, tu peux voir tes informations, compétences, badges et préférences. Explore les différents onglets pour en savoir plus sur toi !");
  
      // Badges (simulés)
      const badges = ref([
        {
          id: 0,
          title: 'Explorateur du Profil',
          description: 'Tu as découvert ton profil avec succès !',
          icon: '🧭',
          iconColor: '#FF5722',
          unlocked: true,
          game: 'Profil',
          dateUnlocked: '2023-06-15',
        },
        {
          id: 1,
          title: 'Maître de la vitesse',
          description: 'Tu as terminé le jeu de vitesse avec un score parfait !',
          icon: '⚡',
          iconColor: '#F44336',
          unlocked: true,
          dateUnlocked: '2023-06-16',
          game: 'Jeu de Vitesse',
        },
        {
          id: 2,
          title: 'Maître des scénarios',
          description: 'Tu as brillamment résolu ton premier scénario social !',
          icon: '🎭',
          iconColor: '#9C27B0',
          unlocked: false,
          hint: 'Complète tous les scénarios sociaux',
          game: 'Jeu des Scénarios',
        },
        {
          id: 3,
          title: 'Expert des formes',
          description: 'Tu as reconnu toutes les séquences de formes correctement !',
          icon: '🔷',
          iconColor: '#2196F3',
          unlocked: false,
          hint: 'Termine le jeu des formes avec un score parfait',
          game: 'Jeu des Formes',
        },
        {
          id: 4,
          title: 'Explorateur de compétences',
          description: 'Tu as exploré et identifié tes points forts !',
          icon: '🎯',
          iconColor: '#3F51B5',
          unlocked: false,
          hint: 'Termine la Roulette des Compétences',
          game: 'Roulette des Compétences',
        },
      ]);
  
      // Réussites (simulées)
      const achievements = ref([
        {
          title: "Premier jeu terminé !",
          description: "Tu as terminé ton premier jeu avec succès.",
          date: "2023-06-15",
          icon: "🎮"
        },
        {
          title: "Vitesse impressionnante",
          description: "Tu as atteint 30 mots par minute dans le jeu de vitesse.",
          date: "2023-06-18",
          icon: "⚡"
        }
      ]);
  
      // Métiers aimés (simulés)
      const likedJobs = ref([
        {
          id: 4,
          name: "Webdesigner",
          description: "Conçoit l'apparence visuelle et l'expérience utilisateur des sites web et applications mobiles.",
          poster: "path/to/webdesigner.jpg",
          skills: ["Créativité", "Codage HTML/CSS", "Sens esthétique", "Ergonomie"]
        },
        {
          id: 20,
          name: "Fleuriste",
          description: "Compose et vend des bouquets et arrangements floraux pour différentes occasions en travaillant avec des fleurs fraîches.",
          poster: "path/to/fleuriste.jpg",
          skills: ["Créativité artistique", "Connaissance des fleurs", "Service client", "Rapidité d'exécution"]
        }
      ]);
  
      // Catégories de compétences
      const skillCategories = ref([
        { id: 'communication', name: 'Communication', color: '#FF5722', icon: '💬' },
        { id: 'interpersonnel', name: 'Relations Sociales', color: '#E91E63', icon: '👥' },
        { id: 'adaptation', name: 'Adaptation', color: '#9C27B0', icon: '🔄' },
        { id: 'professionnelles', name: 'Organisationnelles', color: '#673AB7', icon: '📊' },
        { id: 'personnelles', name: 'Personnelles', color: '#3F51B5', icon: '🧠' }
      ]);
  
      // Compétences (simulées depuis les jeux)
      const skills = ref([
        { id: 'communication', name: 'Communication', level: 4, category: 'communication' },
        { id: 'empathie', name: 'Empathie', level: 3, category: 'interpersonnel' },
        { id: 'adaptabilite', name: 'Adaptabilité', level: 4, category: 'adaptation' },
        { id: 'creativite', name: 'Créativité', level: 5, category: 'adaptation' },
        { id: 'organisation', name: 'Organisation', level: 2, category: 'professionnelles' },
        { id: 'autonomie', name: 'Autonomie', level: 3, category: 'personnelles' }
      ]);
  
      // Styles de CV
      const cvStyles = ref([
        { id: 'simple', name: 'Simple' },
        { id: 'creative', name: 'Créatif' },
        { id: 'professional', name: 'Professionnel' }
      ]);
      const currentCVStyle = ref('simple');
  
      // Couleurs de CV
      const cvColors = ref([
        { name: 'Bleu', value: '#2196F3' },
        { name: 'Vert', value: '#4CAF50' },
        { name: 'Violet', value: '#9C27B0' },
        { name: 'Orange', value: '#FF9800' },
        { name: 'Rouge', value: '#F44336' }
      ]);
      const currentCVColor = ref('#2196F3');

      // Calculer le niveau de l'utilisateur
      const calculateLevel = () => {
        return Math.floor(userProfile.value.experience / 100) + 1;
      };
  
      // Obtenir le pourcentage d'expérience pour le niveau suivant
      const getExpPercentage = () => {
        const currentExp = userProfile.value.experience % 100;
        return (currentExp / 100) * 100;
      };
  
      // Obtenir les compétences d'une catégorie spécifique
      const getSkillsByCategory = (categoryId) => {
        return skills.value.filter(skill => skill.category === categoryId);
      };
  
      // Obtenir la couleur correspondant au niveau de compétence
      const getLevelColor = (level) => {
        const colors = [
          '#F44336', // niveau 1 - rouge
          '#FF9800', // niveau 2 - orange
          '#FFC107', // niveau 3 - jaune
          '#4CAF50', // niveau 4 - vert
          '#2196F3'  // niveau 5 - bleu
        ];
        return colors[Math.min(level, 5) - 1] || colors[0];
      };
  
      // Obtenir le nom du niveau de compétence
      const getSkillLevelName = (level) => {
        const levels = [
          'Débutant',
          'Apprenti',
          'Intermédiaire',
          'Avancé',
          'Expert'
        ];
        return levels[Math.min(level, 5) - 1] || levels[0];
      };

      const getSimpleSkillLevel = (level) => {
        const levels = [
          { text: "Je débute", class: "level-debut" },
          { text: "Je progresse", class: "level-progres" },
          { text: "Je suis fort", class: "level-fort" },
          { text: "Je suis très fort", class: "level-fort" },
          { text: "Super champion !", class: "level-super" }
        ];
        
        // Retourner l'objet pour le niveau (1-5)
        const simpleLevel = levels[Math.min(level, 5) - 1] || levels[0];
        return `<span class="${simpleLevel.class}">${simpleLevel.text}</span>`;
      };
  
      // Obtenir une icône pour une compétence
      const getSkillIcon = (skillId) => {
        const icons = {
          'communication': '📣',
          'empathie': '❤️',
          'adaptabilite': '🦎',
          'creativite': '💡',
          'organisation': '📋',
          'autonomie': '🦅',
          'assertivite': '🗣️',
          'diplomatie': '🤝',
          'ecouteActive': '👂',
          'responsabilite': '🛡️',
          'confianceEnSoi': '💪'
        };
        return icons[skillId] || '✨';
      };
  
      // Formater une date
      const formatDate = (dateString) => {
        if (!dateString) return '';
        const options = { day: 'numeric', month: 'long', year: 'numeric' };
        const date = new Date(dateString);
        return date.toLocaleDateString('fr-FR', options);
      };
  
      // Meilleures compétences
      const topSkills = computed(() => {
        return [...skills.value]
          .sort((a, b) => b.level - a.level)
          .slice(0, 5);
      });
  
      // Compétences professionnelles les plus pertinentes
      const topCareerSkills = computed(() => {
        // Dans une vraie application, ici on ferait un calcul basé sur les métiers aimés
        return [
          { id: 'creativite', name: 'Créativité', matchingJobs: 5 },
          { id: 'communication', name: 'Communication', matchingJobs: 3 },
          { id: 'adaptabilite', name: 'Adaptabilité', matchingJobs: 2 }
        ];
      });
  
      // --- Méthodes pour les modales ---
      // Sauvegarder la bio
      const saveBio = () => {
        userProfile.value.bio = editedBio.value;
        showBioEditor.value = false;
        saveUserProfile();
      };
  
      // Ajouter un hobby
      const addHobby = () => {
        if (newHobby.value.trim()) {
          editedHobbies.value.push(newHobby.value.trim());
          newHobby.value = '';
        }
      };
  
      // Supprimer un hobby
      const removeHobby = (index) => {
        editedHobbies.value.splice(index, 1);
      };
  
      // Sauvegarder les hobbies
      const saveHobbies = () => {
        userProfile.value.hobbies = [...editedHobbies.value];
        showHobbyEditor.value = false;
        saveUserProfile();
      };
  
      // Sélectionner un style de CV
      const selectCVStyle = (styleId) => {
        currentCVStyle.value = styleId;
      };
  
      // Sélectionner une couleur de CV
      const selectCVColor = (colorValue) => {
        currentCVColor.value = colorValue;
      };
  
      // --- Méthodes pour les badges ---
      // Afficher les détails d'un badge
      const showBadgeDetails = (badge) => {
        selectedBadge.value = badge;
      };
  
      // Fermer la modale de badge
      const closeModal = () => {
        selectedBadge.value = null;
      };
  
      // --- Méthodes pour le CV ---
      // Imprimer le CV
      const printCV = () => {
        // Créer une feuille de style temporaire pour l'impression
        const style = document.createElement('style');
        style.id = 'print-style';
        
        style.innerHTML = `
            @media print {
            @page {
                margin: 0;
                size: A4;
            }
            body {
                margin: 1cm;
            }
            /* Cacher les en-têtes et pieds de page du navigateur */
            html {
                height: 100%;
            }
            /* Cacher les éléments qui ne font pas partie du CV */
            .profile-header,
            .navigation-tabs,
            .accessibility-controls,
            .cv-customize,
            .cv-actions,
            .profile-guide {
                display: none !important;
            }
            }
        `;
        
        document.head.appendChild(style);
        window.print();
        
        // Nettoyer après l'impression
        setTimeout(() => {
            const printStyle = document.getElementById('print-style');
            if (printStyle) printStyle.remove();
        }, 1000);
     };
  
      // Télécharger le CV
      const downloadCV = () => {
        // Vérifier si html2pdf est disponible
        if (typeof html2pdf === 'undefined') {
            alert("La bibliothèque de génération PDF n'est pas disponible. Veuillez rafraîchir la page.");
            return;
        }
        
        const cvElement = document.querySelector('.cv-preview');
        if (!cvElement) {
            alert("Impossible de générer le CV. Veuillez réessayer.");
            return;
        }

        // Clone l'élément pour ne pas modifier l'original
        const cvClone = cvElement.cloneNode(true);
        
        // Supprimer les boutons d'action du clone
        const actionsElement = cvClone.querySelector('.cv-actions');
        if (actionsElement) actionsElement.remove();
        
        // Options pour la génération du PDF
        const options = {
            margin: [10, 10, 10, 10],
            filename: `cv_${userProfile.value.firstName}_${userProfile.value.lastName}.pdf`,
            image: { type: 'jpeg', quality: 0.98 },
            html2canvas: { scale: 2, useCORS: true },
            jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
        };
        
        // Afficher un message de chargement
        const loadingMessage = document.createElement('div');
        loadingMessage.style.position = 'fixed';
        loadingMessage.style.top = '50%';
        loadingMessage.style.left = '50%';
        loadingMessage.style.transform = 'translate(-50%, -50%)';
        loadingMessage.style.padding = '20px';
        loadingMessage.style.background = '#3f51b5';
        loadingMessage.style.color = 'white';
        loadingMessage.style.borderRadius = '10px';
        loadingMessage.style.zIndex = '9999';
        loadingMessage.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
        loadingMessage.innerText = 'Génération du CV en cours...';
        document.body.appendChild(loadingMessage);
        
        // Générer le PDF
        html2pdf()
            .set(options)
            .from(cvClone)
            .save()
            .then(() => {
            document.body.removeChild(loadingMessage);
            })
            .catch(error => {
            console.error('Erreur lors de la génération du PDF:', error);
            alert('Une erreur est survenue lors de la génération du PDF.');
            document.body.removeChild(loadingMessage);
            });
        };
  
      // --- Méthodes de navigation ---
      // Voir les détails d'un métier
      const viewJobDetails = (job) => {
        // Redirection vers la page de détails du métier
        alert(`Affichage des détails pour le métier: ${job.name}`);
      };
  
      // Aller à la page de découverte des métiers
      const goToJobDiscovery = () => {
        // Redirection vers la page de découverte des métiers
        window.location.href = '/metiers';
      };
  
      // --- Méthodes d'accessibilité ---
      // Activer/désactiver le son
      const toggleSound = () => {
        soundEnabled.value = !soundEnabled.value;
        saveAccessibilitySettings();
      };
  
      // Activer/désactiver le mode contraste élevé
      const toggleHighContrast = () => {
        highContrastMode.value = !highContrastMode.value;
        saveAccessibilitySettings();
      };
  
      // Augmenter la taille du texte
      const increaseTextSize = () => {
        if (textSizeLevel.value < 1) {
          textSizeLevel.value++;
          applyTextSize();
          saveAccessibilitySettings();
        }
      };
  
      // Diminuer la taille du texte
      const decreaseTextSize = () => {
        if (textSizeLevel.value > -1) {
          textSizeLevel.value--;
          applyTextSize();
          saveAccessibilitySettings();
        }
      };
  
      // Appliquer la taille de texte
      const applyTextSize = () => {
        const container = document.querySelector('.profile-container');
        if (!container) return;
        
        container.classList.remove('text-small', 'text-large');
        
        if (textSizeLevel.value === -1) {
          container.classList.add('text-small');
        } else if (textSizeLevel.value === 1) {
          container.classList.add('text-large');
        }
      };
  
      // --- Méthodes de stockage ---
      // Sauvegarder le profil utilisateur
      const saveUserProfile = () => {
        localStorage.setItem('userProfile', JSON.stringify(userProfile.value));
      };
  
      // Charger le profil utilisateur
      const loadUserProfile = () => {
      };
  
      // Sauvegarder les paramètres d'accessibilité
      const saveAccessibilitySettings = () => {
        const settings = {
          highContrastMode: highContrastMode.value,
          soundEnabled: soundEnabled.value,
          textSizeLevel: textSizeLevel.value
        };
        localStorage.setItem('accessibilitySettings', JSON.stringify(settings));
      };
  
      // Charger les paramètres d'accessibilité
      const loadAccessibilitySettings = () => {
        const savedSettings = localStorage.getItem('accessibilitySettings');
        if (savedSettings) {
          const settings = JSON.parse(savedSettings);
          highContrastMode.value = settings.highContrastMode || false;
          soundEnabled.value = settings.soundEnabled !== undefined ? settings.soundEnabled : true;
          textSizeLevel.value = settings.textSizeLevel || 0;
          applyTextSize();
        }
      };
  
      // --- Méthodes relatives au guide ---
      // Fermer le guide
      const dismissGuide = () => {
        showGuide.value = false;
        localStorage.setItem('profileGuideShown', 'true');
      };
  
      // Animation de fermeture de badge
      const closeBadgeAnimation = () => {
        showBadgeUnlockAnimation.value = false;
      };
  
      // --- Méthodes de visualisation ---
      // Initialiser le graphique des compétences
      const initSkillsChart = () => {
        const ctx = document.getElementById('skillsChart');
        if (!ctx) return;   
      };
  
      // --- Hooks du cycle de vie ---
      onMounted(() => {
        // Charger les données
        loadUserProfile();
        loadAccessibilitySettings();
        
        // Vérifier si le guide a déjà été affiché
        const guideShown = localStorage.getItem('profileGuideShown');
        if (guideShown === 'true') {
          showGuide.value = false;
        }
        
        // Initialiser le graphique des compétences après le chargement du DOM
        nextTick(() => {
          if (currentTab.value === 'skills') {
            initSkillsChart();
          }
        });
        
        // Charger les compétences
        loadSkills();
        loadBadges();
        
        // Vérifier s'il y a un badge nouvellement débloqué
        checkNewlyUnlockedBadge();
      });
  
      // --- Autres méthodes de chargement de données ---
      // Charger les compétences
      const loadSkills = () => {
        // Dans une vraie application, charger depuis localStorage ou API
        const savedSkills = localStorage.getItem('userSoftSkills');
        if (savedSkills) {
          try {
            const parsedSkills = JSON.parse(savedSkills);
            // Transformer les données au format attendu par le composant
            const mappedSkills = [];
            
            for (const [skillId, value] of Object.entries(parsedSkills)) {
              // Déterminer la catégorie en fonction de l'ID de compétence
              let category = 'personnelles'; // par défaut
              
              if (['assertivite', 'communication', 'diplomatie', 'ecouteActive', 'negociation', 'franchise'].includes(skillId)) {
                category = 'communication';
              } else if (['empathie', 'espritEquipe', 'soutien', 'mediation', 'inclusion', 'coaching'].includes(skillId)) {
                category = 'interpersonnel';
              } else if (['adaptabilite', 'initiative', 'reflexionRapide', 'gestionStress', 'creativite'].includes(skillId)) {
                category = 'adaptation';
              } else if (['responsabilite', 'anticipation', 'observation', 'apprentissage', 'gestionTemps', 'decision'].includes(skillId)) {
                category = 'professionnelles';
              }
              
              // Nom de la compétence
              const skillName = getSkillDisplayName(skillId);
              
              // Niveau (normalisé entre 1 et 5)
              const level = Math.max(1, Math.min(5, Math.ceil(value / 3)));
              
              mappedSkills.push({
                id: skillId,
                name: skillName,
                level: level,
                category: category
              });
            }
            
            skills.value = mappedSkills;
          } catch (error) {
            console.error("Erreur lors du chargement des compétences:", error);
          }
        }
      };
  
      // Obtenir le nom d'affichage d'une compétence
      const getSkillDisplayName = (skillId) => {
        const displayNames = {
          assertivite: "Assertivité",
          communication: "Communication",
          diplomatie: "Diplomatie",
          ecouteActive: "Écoute active",
          negociation: "Négociation",
          franchise: "Franchise",
          empathie: "Empathie",
          espritEquipe: "Esprit d'équipe",
          soutien: "Soutien",
          mediation: "Médiation",
          inclusion: "Inclusion",
          coaching: "Coaching",
          adaptabilite: "Adaptabilité",
          initiative: "Initiative",
          reflexionRapide: "Réflexion rapide",
          gestionStress: "Gestion du stress",
          creativite: "Créativité",
          responsabilite: "Responsabilité",
          anticipation: "Anticipation",
          observation: "Observation",
          apprentissage: "Apprentissage",
          gestionTemps: "Gestion du temps",
          decision: "Prise de décision",
          confianceEnSoi: "Confiance en soi",
          autonomie: "Autonomie",
          patience: "Patience",
          curiosite: "Curiosité",
          pragmatisme: "Pragmatisme",
          assurance: "Assurance"
        };
        
        return displayNames[skillId] || skillId;
      };
  
      // Charger les badges
      const loadBadges = () => {
        const savedBadges = localStorage.getItem('userBadges');
        if (savedBadges) {
          try {
            badges.value = JSON.parse(savedBadges);
          } catch (error) {
            console.error("Erreur lors du chargement des badges:", error);
          }
        }
      };
  
      // Vérifier s'il y a un badge nouvellement débloqué
      const checkNewlyUnlockedBadge = () => {
        const newBadgeInfo = localStorage.getItem('newUnlockedBadge');
        if (newBadgeInfo) {
          try {
            // Récupérer et afficher l'animation du badge
            newlyUnlockedBadge.value = JSON.parse(newBadgeInfo);
            showBadgeUnlockAnimation.value = true;
            
            // Supprimer l'information pour ne pas la réafficher
            localStorage.removeItem('newUnlockedBadge');
          } catch (error) {
            console.error("Erreur lors de la vérification du nouveau badge:", error);
          }
        }
      };
  
      // Observer les changements d'onglet
      const watchTabChanges = () => {
        // Initialiser le graphique quand on passe à l'onglet compétences
        if (currentTab.value === 'skills') {
          nextTick(() => {
            initSkillsChart();
          });
        }
      };

  
      return {
        // Données d'état
        userProfile,
        defaultAvatar,
        currentTab,
        tabs,
        badges,
        achievements,
        likedJobs,
        skillCategories,
        skills,
        showBioEditor,
        editedBio,
        showHobbyEditor,
        editedHobbies,
        newHobby,
        selectedAvatar,
        highContrastMode,
        soundEnabled,
        textSizeLevel,
        cvStyles,
        currentCVStyle,
        cvColors,
        currentCVColor,
        selectedBadge,
        showBadgeUnlockAnimation,
        newlyUnlockedBadge,
        showGuide,
        guideMessage,
        topSkills,
        topCareerSkills,
        
        // Méthodes
        getSimpleSkillLevel,
        calculateLevel,
        getExpPercentage,
        getSkillsByCategory,
        getLevelColor,
        getSkillLevelName,
        getSkillIcon,
        formatDate,
        saveBio,
        addHobby,
        removeHobby,
        saveHobbies,
        showBadgeDetails,
        closeModal,
        selectCVStyle,
        selectCVColor,
        printCV,
        downloadCV,
        viewJobDetails,
        goToJobDiscovery,
        toggleSound,
        toggleHighContrast,
        increaseTextSize,
        decreaseTextSize,
        closeBadgeAnimation,
        dismissGuide,
        watchTabChanges,
      };
    }
  };
  </script>
  
  <style scoped>
  /* Base Styles */
  .profile-container {
    font-family: 'Comic Sans MS', 'Chalkboard SE', 'Marker Felt', sans-serif;
    max-width: 1100px;
    margin: 0 auto;
    padding: 20px;
    color: #333;
    min-height: 100vh;
    position: relative;
  }
  
  /* Adaptations d'accessibilité */
  .profile-container.high-contrast-mode {
    background-color: #000;
    color: #fff;
  }
  
  .profile-container.text-small {
    font-size: 0.9rem;
  }
  
  .profile-container.text-large {
    font-size: 1.2rem;
  }
  
  /* Header */
  .profile-header {
    margin-bottom: 30px;
    position: relative;
  }
  
  .main-title {
    font-size: 2.5rem;
    color: #3f51b5;
    text-align: center;
    margin-bottom: 10px;
  }
  
  .subtitle {
    font-size: 1.2rem;
    color: #666;
    text-align: center;
    margin: 0;
  }

  /* Styles pour la section compétences simplifiée */
.skills-simplified {
  width: 100%;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 15px;
}

.skills-intro {
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
  font-weight: bold;
}

.skills-categories-simple {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.skill-category-simple {
  background-color: white;
  border-radius: 15px;
  padding: 15px;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
}

.category-title-simple {
  display: flex;
  align-items: center;
  font-size: 1.5rem;
  margin-top: 0;
  margin-bottom: 15px;
  color: #3f51b5;
}

.category-icon-large {
  font-size: 2rem;
  margin-right: 10px;
}

.skills-list-simple {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.skill-item-simple {
  display: flex;
  align-items: center;
  background-color: #f5f5f5;
  border-radius: 12px;
  padding: 12px;
  transition: transform 0.3s;
}

.skill-item-simple:hover {
  transform: translateY(-3px);
}

.skill-icon-simple {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  margin-right: 15px;
  color: white;
}

.skill-info-simple {
  flex: 1;
}

.skill-name-simple {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 8px;
  color: #333;
}

.skill-stars {
  display: flex;
  gap: 5px;
  margin-bottom: 5px;
}

.skill-star {
  font-size: 1.5rem;
  color: #e0e0e0;
}

.skill-star.filled {
  color: #FFD700; /* Couleur or pour les étoiles remplies */
}

.skill-level-simple {
  font-size: 1rem;
  padding: 4px 12px;
  border-radius: 20px;
  display: inline-block;
  font-weight: bold;
}

/* Couleurs pour les différents niveaux simplifiés */
.level-debut {
  background-color: #E3F2FD;
  color: #1976D2;
}

.level-progres {
  background-color: #E8F5E9;
  color: #388E3C;
}

.level-fort {
  background-color: #FFF3E0;
  color: #E64A19;
}

.level-super {
  background-color: #F3E5F5;
  color: #7B1FA2;
}

.empty-category-simple {
  text-align: center;
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 10px;
  font-size: 1.1rem;
  color: #757575;
}
  
  /* Contrôles d'accessibilité */
  .accessibility-controls {
    position: absolute;
    top: 0;
    right: 0;
    display: flex;
    gap: 5px;
    z-index: 50;
  }
  
  .accessibility-button {
    width: 35px;
    height: 35px;
    border-radius: 50%;
    border: none;
    background-color: #f5f5f5;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    cursor: pointer;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    transition: all 0.2s ease;
  }
  
  .accessibility-button:hover {
    background-color: #e0e0e0;
    transform: scale(1.1);
  }
  
  /* Navigation */
  .navigation-tabs {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 30px;
    background-color: #f5f5f5;
    padding: 10px;
    border-radius: 50px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  }
  
  .tab-button {
    padding: 10px 20px;
    border: none;
    background-color: transparent;
    border-radius: 50px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: bold;
    color: #666;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .tab-button:hover {
    background-color: #e0e0e0;
    color: #3f51b5;
  }
  
  .tab-button.active {
    background-color: #3f51b5;
    color: white;
  }
  
  .tab-icon {
    font-size: 1.2rem;
  }
  
  /* Sections de profil */
  .profile-section {
    margin-bottom: 40px;
    background-color: white;
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
    animation: fadeIn 0.5s ease;
  }
  
  .section-title {
    display: flex;
    align-items: center;
    font-size: 1.8rem;
    color: #3f51b5;
    margin-top: 0;
    margin-bottom: 25px;
    padding-bottom: 15px;
    border-bottom: 2px solid #f5f5f5;
  }
  
  .section-icon {
    font-size: 1.8rem;
    margin-right: 10px;
  }
  
  /* Informations personnelles */
  .personal-info-container {
    display: flex;
    flex-wrap: wrap;
    gap: 30px;
  }
  
  .avatar-section {
    width: 200px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .avatar-container {
    position: relative;
    width: 160px;
    height: 160px;
    margin-bottom: 15px;
  }
  
  .user-avatar {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
    border: 4px solid #3f51b5;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  }
  
  .edit-avatar-button {
    position: absolute;
    bottom: 10px;
    right: 10px;
    width: 35px;
    height: 35px;
    border-radius: 50%;
    background-color: #3f51b5;
    color: white;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 1.2rem;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
  }
  
  .edit-avatar-button:hover {
    transform: scale(1.1);
    background-color: #303f9f;
  }
  
  .level-indicator {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
  }
  
  .level-badge {
    background-color: #4caf50;
    color: white;
    padding: 5px 15px;
    border-radius: 50px;
    font-weight: bold;
    margin-bottom: 10px;
    font-size: 0.9rem;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  }
  
  .exp-bar {
    width: 100%;
    height: 10px;
    background-color: #e0e0e0;
    border-radius: 5px;
    overflow: hidden;
  }
  
  .exp-fill {
    height: 100%;
    background: linear-gradient(90deg, #4caf50, #8bc34a);
    border-radius: 5px;
    transition: width 0.5s ease;
  }
  
  .info-fields {
    flex: 1;
    min-width: 300px;
  }
  
  .info-field {
    margin-bottom: 20px;
  }
  
  .info-field label {
    display: block;
    font-weight: bold;
    color: #3f51b5;
    margin-bottom: 5px;
    font-size: 1.1rem;
  }
  
  .field-value {
    background-color: #f5f5f5;
    padding: 12px 15px;
    border-radius: 10px;
    color: #555;
    font-size: 1rem;
    line-height: 1.4;
  }
  
  .field-value.bio {
    min-height: 80px;
    white-space: pre-wrap;
  }
  
  .edit-button {
    background-color: #4caf50;
    color: white;
    border: none;
    padding: 8px 15px;
    border-radius: 50px;
    font-size: 0.9rem;
    cursor: pointer;
    margin-top: 10px;
    transition: all 0.3s ease;
  }
  
  .edit-button:hover {
    background-color: #388e3c;
  }
  
  .hobbies-container {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 8px;
  }
  
  .hobby-tag {
    background-color: #e3f2fd;
    color: #1976d2;
    padding: 10px 16px;
    border-radius: 50px;
    font-size: 0.95rem;
    transition: all 0.3s ease;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(25, 118, 210, 0.1);
    position: relative;
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
  }

  .hobby-tag:hover {
    background-color: #bbdefb;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.12);
  }

  .hobby-tag:active {
    transform: translateY(0);
    box-shadow: 0 2px 3px rgba(0, 0, 0, 0.1);
  }

  .hobby-tag::before {
    content: '';
    display: inline-block;
    width: 8px;
    height: 8px;
    background-color: #1976d2;
    border-radius: 50%;
    margin-right: 2px;
  }

  /* Icônes spécifiques pour chaque loisir */
  .hobby-tag[data-hobby="Jeux vidéo"]::before {
    content: '🎮';
    background: none;
    width: auto;
    height: auto;
    margin-right: 0;
  }

  .hobby-tag[data-hobby="Musique"]::before {
    content: '🎵';
    background: none;
    width: auto;
    height: auto;
    margin-right: 0;
  }

  .hobby-tag[data-hobby="Dessin"]::before {
    content: '🎨';
    background: none;
    width: auto;
    height: auto;
    margin-right: 0;
  }

  .hobby-tag[data-hobby="Natation"]::before {
    content: '🏊';
    background: none;
    width: auto;
    height: auto;
    margin-right: 0;
  }

  .add-hobby-button {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    background-color: #3f51b5;
    color: white;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
  }

  .add-hobby-button:hover {
    background-color: #303f9f;
    transform: rotate(90deg) scale(1.1);
  }

  /* Animation subtile d'apparition */
  @keyframes fadeInScale {
    from {
      opacity: 0;
      transform: scale(0.8);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }

  .hobby-tag {
    animation: fadeInScale 0.3s ease forwards;
  }

  .add-hobby-button {
    width: 35px;
    height: 35px;
    border-radius: 50%;
    background-color: #3f51b5;
    color: white;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .add-hobby-button:hover {
    background-color: #303f9f;
  }
  
  /* Compétences */
  .skills-container {
    display: flex;
    flex-wrap: wrap;
    gap: 30px;
  }
  
  .skills-chart-container {
    flex: 1;
    min-width: 300px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .skills-wheel {
    width: 300px;
    height: 300px;
    margin-bottom: 20px;
  }
  
  .skills-legend {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px;
    margin-top: 20px;
  }
  
  .legend-item {
    display: flex;
    align-items: center;
    gap: 5px;
    margin-bottom: 8px;
  }
  
  .color-dot {
    width: 15px;
    height: 15px;
    border-radius: 50%;
  }
  
  .legend-label {
    font-size: 0.9rem;
    color: #555;
  }
  
  .skills-lists {
    flex: 2;
    min-width: 300px;
  }
  
  .skill-category {
    margin-bottom: 30px;
  }
  
  .category-title {
    display: flex;
    align-items: center;
    font-size: 1.3rem;
    margin-bottom: 15px;
    padding-bottom: 8px;
    border-bottom: 1px solid #e0e0e0;
  }
  
  .category-icon {
    margin-right: 10px;
  }
  
  .skills-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 15px;
  }
  
  .skill-card {
    display: flex;
    align-items: center;
    background-color: #f9f9f9;
    border-radius: 12px;
    padding: 12px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
  }
  
  .skill-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
  }
  
  .skill-icon {
    width: 45px;
    height: 45px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
    margin-right: 12px;
    flex-shrink: 0;
    color: white;
  }
  
  .skill-info {
    flex: 1;
  }
  
  .skill-name {
    font-weight: bold;
    margin-bottom: 5px;
    color: #333;
    font-size: 0.95rem;
  }
  
  .skill-level {
    font-size: 0.8rem;
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  .skill-bar {
    height: 5px;
    width: 100%;
    background-color: #e0e0e0;
    border-radius: 2px;
    overflow: hidden;
  }
  
  .skill-fill {
    height: 100%;
    transition: width 0.5s ease;
  }
  
  .empty-category {
    grid-column: 1 / -1;
    text-align: center;
    padding: 20px;
    background-color: #f5f5f5;
    border-radius: 10px;
    color: #999;
    font-style: italic;
  }
  
  /* Badges */
  .badges-container {
    display: flex;
    flex-direction: column;
    gap: 30px;
  }
  
  .badges-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
  }
  
  .badge-card {
    background-color: #f9f9f9;
    border-radius: 15px;
    padding: 20px 15px;
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
  }
  
  .badge-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  }
  
  .badge-card.locked {
    opacity: 0.7;
  }
  
  .badge-card.unlocked {
    border: 2px solid #4caf50;
  }
  
  .badge-icon {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 15px;
    position: relative;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
  
  .lock-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.8rem;
    color: white;
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 50%;
  }
  
  .badge-emoji {
    font-size: 2.5rem;
  }
  
  .badge-title {
    font-size: 1rem;
    color: #333;
    margin: 0 0 10px 0;
    text-align: center;
    font-weight: bold;
  }
  
  .badge-status {
    font-size: 0.8rem;
    font-weight: bold;
  }
  
  .status-unlocked {
    color: #4caf50;
  }
  
  .status-locked {
    color: #9e9e9e;
  }
  
  .achievements-section {
    background-color: #f9f9f9;
    border-radius: 15px;
    padding: 20px;
  }
  
  .subsection-title {
    font-size: 1.4rem;
    color: #3f51b5;
    margin-top: 0;
    margin-bottom: 20px;
    text-align: center;
  }
  
  .achievements-list {
    max-height: 300px;
    overflow-y: auto;
    padding-right: 10px;
  }
  
  .achievement-item {
    display: flex;
    margin-bottom: 15px;
    background-color: white;
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
  }
  
  .achievement-item:hover {
    transform: translateX(5px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  .achievement-icon {
    font-size: 2rem;
    margin-right: 15px;
    display: flex;
    align-items: center;
  }
  
  .achievement-details {
    flex: 1;
  }
  
  .achievement-title {
    font-weight: bold;
    color: #333;
    margin-bottom: 5px;
  }
  
  .achievement-description {
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 5px;
  }
  
  .achievement-date {
    color: #9e9e9e;
    font-size: 0.8rem;
    font-style: italic;
  }
  
  .empty-achievements {
    text-align: center;
    padding: 20px;
    color: #999;
    font-style: italic;
  }
  
  /* Intérêts professionnels */
  .careers-container {
    display: flex;
    flex-direction: column;
    gap: 30px;
  }
  
  .liked-jobs-section {
    margin-bottom: 20px;
  }
  
  .jobs-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
  }
  
  .job-card {
    background-color: #f9f9f9;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
  }
  
  .job-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  }
  
  .job-image-container {
    height: 150px;
    overflow: hidden;
  }
  
  .job-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: all 0.5s ease;
  }
  
  .job-card:hover .job-image {
    transform: scale(1.05);
  }
  
  .job-info {
    padding: 15px;
  }
  
  .job-title {
    font-size: 1.1rem;
    color: #3f51b5;
    margin-top: 0;
    margin-bottom: 10px;
    font-weight: bold;
  }
  
  .job-skills {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    margin-bottom: 15px;
  }
  
  .job-skill-tag {
    background-color: #e3f2fd;
    color: #1976d2;
    padding: 4px 8px;
    border-radius: 50px;
    font-size: 0.8rem;
  }
  
  .job-skill-more {
    background-color: #e0e0e0;
    color: #757575;
    padding: 4px 8px;
    border-radius: 50px;
    font-size: 0.8rem;
  }
  
  .view-job-button {
    background-color: #ff9800;
    color: white;
    border: none;
    padding: 8px 15px;
    border-radius: 50px;
    font-size: 0.9rem;
    cursor: pointer;
    width: 100%;
    transition: all 0.3s ease;
  }
  
  .view-job-button:hover {
    background-color: #f57c00;
  }
  
  .empty-job-interests {
    text-align: center;
    padding: 30px;
    background-color: #f9f9f9;
    border-radius: 15px;
  }
  
  .empty-icon {
    font-size: 3rem;
    margin-bottom: 15px;
    color: #9e9e9e;
  }
  
  .empty-job-interests p {
    color: #666;
    margin-bottom: 20px;
  }
  
  .action-button {
    background-color: #ff9800;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 50px;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .action-button:hover {
    background-color: #f57c00;
    transform: translateY(-3px);
  }
  
  .career-skills-match {
    background-color: #f9f9f9;
    border-radius: 15px;
    padding: 20px;
  }
  
  .career-skills-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 15px;
  }
  
  .career-skill-card {
    display: flex;
    align-items: center;
    background-color: white;
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  }
  
  .career-skill-icon {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #e3f2fd;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    margin-right: 12px;
    flex-shrink: 0;
  }
  
  .career-skill-info {
    flex: 1;
  }
  
  .career-skill-name {
    font-weight: bold;
    color: #333;
    margin-bottom: 5px;
  }
  
  .career-skill-match {
    font-size: 0.8rem;
    color: #4caf50;
  }
  
  .empty-career-skills {
    grid-column: 1 / -1;
    text-align: center;
    padding: 15px;
    color: #999;
    font-style: italic;
  }
  
  /* Préférences sensorielles */
  .sensory-container {
    display: flex;
    flex-direction: column;
    gap: 30px;
  }
  
  .sensory-categories {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
  }
  
  .sensory-category {
    background-color: #f9f9f9;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  }
  
  .sensory-preferences {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  
  .preference-item {
    display: flex;
    flex-direction: column;
  }
  
  .preference-label {
    font-weight: bold;
    color: #555;
    margin-bottom: 5px;
  }
  
  .preference-value {
    background-color: white;
    padding: 10px;
    border-radius: 8px;
    color: #333;
  }
  
  .sensory-recommendations {
    background-color: #f9f9f9;
    border-radius: 15px;
    padding: 20px;
  }
  
  .recommendation-list {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  
  .recommendation-item {
    display: flex;
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  }
  
  .recommendation-icon {
    font-size: 1.5rem;
    margin-right: 15px;
    color: #ff9800;
  }
  
  .recommendation-text {
    flex: 1;
    color: #555;
  }
  
  .empty-recommendations {
    text-align: center;
    padding: 15px;
    color: #999;
    font-style: italic;
  }
  
  /* CV et Présentation */
  .cv-container {
    display: flex;
    flex-wrap: wrap;
    gap: 30px;
  }
  
  .cv-preview {
    flex: 2;
    min-width: 300px;
    background-color: white;
    border-radius: 15px;
    padding: 30px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  }

	.cv-preview {
  /* Utiliser la variable CSS pour la couleur principale */
  --cv-color: #2196F3; /* Couleur par défaut */
  transition: all 0.3s ease;
}

/* Appliquer la couleur principale aux éléments du CV */
.cv-name {
  color: var(--cv-color);
}

.cv-section-title {
  color: var(--cv-color);
  border-bottom-color: var(--cv-color);
}

/* Style Simple (par défaut) */
.cv-style-simple {
  font-family: 'Arial', sans-serif;
  padding: 30px;
}

.cv-style-simple .cv-section-title {
  font-size: 1.3rem;
  border-bottom: 1px solid var(--cv-color);
  padding-bottom: 8px;
  color: var(--cv-color);
}

.cv-style-simple .cv-name {
  color: var(--cv-color);
}

.cv-style-simple .cv-job-name {
  color: var(--cv-color);
}

.cv-style-simple .cv-skill-item {
  border-left: 3px solid var(--cv-color);
}

/* Style Créatif */
.cv-style-creative {
  font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
  padding: 25px;
  background-color: #f9f9f9;
  border-radius: 20px;
}

.cv-style-creative .cv-header {
  background-color: var(--cv-color);
  margin: -25px -25px 20px -25px;
  padding: 25px;
  border-radius: 20px 20px 0 0;
  text-align: center;
}

.cv-style-creative .cv-name {
  color: white;
  font-size: 2rem;
}

.cv-style-creative .cv-contact {
  color: rgba(255, 255, 255, 0.9);
}

.cv-style-creative .cv-section-title {
  background-color: rgba(0, 0, 0, 0.05);
  border: none;
  padding: 10px 15px;
  border-radius: 10px;
  font-size: 1.2rem;
}

.cv-style-creative .cv-skill-item,
.cv-style-creative .cv-job-item,
.cv-style-creative .cv-bio {
  border-radius: 15px;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
  border-left: 4px solid var(--cv-color);
}

/* Style Professionnel */
.cv-style-professional {
  font-family: 'Calibri', 'Helvetica', sans-serif;
  padding: 30px;
  border: 1px solid #e0e0e0;
}

.cv-style-professional .cv-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 20px;
  border-bottom: 2px solid var(--cv-color);
}

.cv-style-professional .cv-name {
  font-size: 1.8rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.cv-style-professional .cv-section-title {
  text-transform: uppercase;
  letter-spacing: 1px;
  font-size: 1.1rem;
  font-weight: bold;
  padding-bottom: 10px;
  border-bottom: 1px solid #e0e0e0;
}

.cv-style-professional .cv-section-title::before {
  content: '';
  display: inline-block;
  width: 12px;
  height: 12px;
  background-color: var(--cv-color);
  margin-right: 10px;
}

.cv-style-professional .cv-skill-item,
.cv-style-professional .cv-job-item {
  background-color: white;
  border: 1px solid #e0e0e0;
  padding: 12px;
}

.cv-style-professional .cv-bio {
  background-color: white;
  border: 1px solid #e0e0e0;
  padding: 15px;
}
  
  .cv-header {
    text-align: center;
    margin-bottom: 25px;
    padding-bottom: 15px;
    border-bottom: 2px solid #f5f5f5;
  }
  
  .cv-name {
    font-size: 1.8rem;
    color: #3f51b5;
    margin: 0 0 10px 0;
  }
  
  .cv-contact {
    color: #757575;
  }
  
  .cv-section {
    margin-bottom: 25px;
  }
  
  .cv-section-title {
    color: #3f51b5;
    font-size: 1.3rem;
    margin: 0 0 15px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #e0e0e0;
  }
  
  .cv-strength-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 15px;
  }
  
  .cv-skill-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: #f5f5f5;
    border-radius: 10px;
    padding: 15px 10px;
  }
  
  .cv-skill-icon {
    font-size: 1.8rem;
    margin-bottom: 10px;
  }
  
  .cv-skill-name {
    text-align: center;
    font-size: 0.9rem;
    font-weight: bold;
  }
  
  .cv-jobs-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .cv-job-item {
    background-color: #f5f5f5;
    padding: 12px 15px;
    border-radius: 10px;
  }
  
  .cv-job-name {
    font-weight: bold;
    color: #3f51b5;
  }
  
  .cv-bio {
    background-color: #f5f5f5;
    padding: 15px;
    border-radius: 10px;
    color: #555;
    line-height: 1.5;
  }
  
  .cv-empty-section {
    text-align: center;
    padding: 15px;
    background-color: #f5f5f5;
    border-radius: 10px;
    color: #999;
    font-style: italic;
  }
  
  .cv-actions {
    display: flex;
    justify-content: center;
    gap: 15px;
    margin-top: 25px;
  }
  
  .cv-button {
    padding: 10px 20px;
    border: none;
    border-radius: 50px;
    cursor: pointer;
    font-size: 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.3s ease;
  }
  
  .print-button {
    background-color: #4caf50;
    color: white;
  }
  
  .print-button:hover {
    background-color: #388e3c;
  }
  
  .download-button {
    background-color: #2196f3;
    color: white;
  }
  
  .download-button:hover {
    background-color: #1976d2;
  }
  
  .cv-customize {
    flex: 1;
    min-width: 250px;
    background-color: #f9f9f9;
    border-radius: 15px;
    padding: 20px;
  }
  
  .customize-title {
    font-size: 1.3rem;
    color: #3f51b5;
    margin-top: 0;
    margin-bottom: 20px;
    text-align: center;
  }
  
  .customize-options {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  .customize-option {
    margin-bottom: 20px;
  }
  
  .customize-option label {
    display: block;
    font-weight: bold;
    color: #333;
    margin-bottom: 10px;
  }
  
  .style-options {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }
  
  .style-button {
    background-color: #e0e0e0;
    padding: 8px 15px;
    border: none;
    border-radius: 50px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: all 0.3s ease;
  }
  
  .style-button:hover {
    background-color: #c0c0c0;
  }
  
  .style-button.active {
    background-color: #3f51b5;
    color: white;
  }
  
  .color-options {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }
  
  .color-button {
    width: 35px;
    height: 35px;
    border-radius: 50%;
    border: 2px solid transparent;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .color-button:hover {
    transform: scale(1.1);
  }
  
  .color-button.active {
    border-color: #333;
    transform: scale(1.1);
  }
  
  /* Modales */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    animation: fadeIn 0.3s ease;
  }
  
  .modal-content {
    background-color: white;
    border-radius: 20px;
    padding: 25px;
    width: 90%;
    max-width: 500px;
    max-height: 80vh;
    overflow-y: auto;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    animation: scaleIn 0.4s ease;
  }
  
  .modal-title {
    font-size: 1.5rem;
    color: #3f51b5;
    margin-top: 0;
    margin-bottom: 20px;
    text-align: center;
  }
  
  .bio-textarea {
    width: 100%;
    min-height: 150px;
    padding: 15px;
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    font-family: inherit;
    font-size: 1rem;
    resize: vertical;
    margin-bottom: 20px;
  }
  
  .modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 15px;
    margin-top: 20px;
  }
  
  .modal-button {
    padding: 10px 20px;
    border: none;
    border-radius: 50px;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.3s ease;
  }
  
  .cancel-button {
    background-color: #e0e0e0;
    color: #333;
  }
  
  .cancel-button:hover {
    background-color: #c0c0c0;
  }
  
  .save-button {
    background-color: #4caf50;
    color: white;
  }
  
  .save-button:hover {
    background-color: #388e3c;
  }
  
  .hobby-editor {
    margin-bottom: 20px;
  }
  
  .current-hobbies {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 15px;
  }
  
  .hobby-editor-item {
    background-color: #e3f2fd;
    color: #1976d2;
    padding: 8px 15px;
    border-radius: 50px;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .remove-hobby-button {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background-color: #e0e0e0;
    border: none;
    font-size: 0.8rem;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .remove-hobby-button:hover {
    background-color: #f44336;
    color: white;
  }
  
  .add-hobby-form {
    display: flex;
    gap: 10px;
  }
  
  .hobby-input {
    flex: 1;
    padding: 10px 15px;
    border: 1px solid #e0e0e0;
    border-radius: 50px;
    font-size: 0.9rem;
  }
  
  .add-button {
    background-color: #4caf50;
    color: white;
    border: none;
    padding: 8px 15px;
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .add-button:hover {
    background-color: #388e3c;
  }
  
  .avatar-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 15px;
    margin-bottom: 20px;
  }
  
  .avatar-option {
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid transparent;
    border-radius: 10px;
    padding: 10px;
  }
  
  .avatar-option:hover {
    background-color: #f5f5f5;
  }
  
  .avatar-option.active {
    border-color: #3f51b5;
    background-color: #e8eaf6;
  }
  
  .avatar-preview {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 8px;
  }
  
  .avatar-name {
    font-size: 0.9rem;
    color: #555;
    text-align: center;
  }
  
  /* Détails du badge */
  .badge-modal {
    background-color: white;
    border-radius: 20px;
    padding: 25px;
    max-width: 400px;
    width: 90%;
    position: relative;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    animation: scaleIn 0.4s ease;
  }
  
  .close-button {
    position: absolute;
    top: 15px;
    right: 15px;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background-color: #f5f5f5;
    border: none;
    font-size: 1.2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .close-button:hover {
    background-color: #e0e0e0;
  }
  
  .badge-detail-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .badge-detail-icon {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 20px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  }
  
  .badge-detail-emoji {
    font-size: 3rem;
  }
  
  .badge-detail-title {
    font-size: 1.6rem;
    color: #3f51b5;
    margin: 0 0 15px 0;
  }
  
  .badge-detail-description {
    color: #555;
    margin-bottom: 20px;
    line-height: 1.5;
  }
  
  .badge-achievement {
    background-color: #e8f5e9;
    padding: 15px;
    border-radius: 10px;
    width: 100%;
    margin-bottom: 20px;
  }
  
  .achievement-date {
    font-weight: bold;
    color: #4caf50;
    margin-bottom: 5px;
  }
  
  .achievement-game {
    color: #757575;
  }
  
  .badge-locked-info {
    background-color: #fff8e1;
    padding: 15px;
    border-radius: 10px;
    width: 100%;
  }
  
  .badge-hint {
    display: flex;
    align-items: flex-start;
    gap: 10px;
  }
  
  .hint-icon {
    font-size: 1.5rem;
    color: #ff9800;
  }
  
  /* Animation de déblocage du badge */
  .badge-unlock-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1100;
    animation: fadeIn 0.5s ease-out;
  }
  
  .badge-unlock-animation {
    background-color: white;
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    max-width: 400px;
    box-shadow: 0 0 30px rgba(63, 81, 181, 0.6);
    animation: scaleIn 0.5s ease-out;
  }
  
  .badge-unlock-animation .badge-icon {
    font-size: 5rem;
    margin-bottom: 20px;
    animation: pulse 2s infinite;
  }
  
  .badge-unlock-animation h2 {
    color: #3f51b5;
    font-size: 2rem;
    margin-bottom: 10px;
  }
  
  .badge-unlock-animation h3 {
    color: #333;
    font-size: 1.5rem;
    margin-bottom: 15px;
  }
  
  .badge-unlock-animation p {
    color: #666;
    margin-bottom: 20px;
  }
  
  .close-animation-btn {
    background-color: #3f51b5;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 50px;
    font-weight: bold;
    font-size: 1.1rem;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .close-animation-btn:hover {
    background-color: #303f9f;
    transform: scale(1.05);
  }
  
  /* Guide contextuel */
  .profile-guide {
    position: fixed;
    bottom: 20px;
    right: 20px;
    display: flex;
    align-items: flex-start;
    max-width: 400px;
    z-index: 900;
    animation: slideUp 0.5s ease;
  }
  
  .guide-character {
    margin-right: 10px;
  }
  
  .guide-avatar {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    border: 3px solid #ff9800;
    background-color: white;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  }
  
  .guide-bubble {
    background-color: white;
    border-radius: 15px;
    padding: 15px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    position: relative;
  }
  
  .guide-bubble:before {
    content: '';
    position: absolute;
    left: -10px;
    top: 20px;
    border-width: 10px 10px 10px 0;
    border-style: solid;
    border-color: transparent white transparent transparent;
  }
  
  .guide-bubble p {
    margin: 0 0 15px 0;
    color: #555;
    line-height: 1.5;
  }
  
  .guide-dismiss-button {
    background-color: #ff9800;
    color: white;
    border: none;
    padding: 8px 15px;
    border-radius: 50px;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .guide-dismiss-button:hover {
    background-color: #f57c00;
  }
  
  /* Animations */
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  @keyframes scaleIn {
    from { transform: scale(0.8); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
  }
  
  @keyframes slideUp {
    from { transform: translateY(30px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
  }
  
  @keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
  }
  
  /* Responsive Design */
  @media (max-width: 768px) {
    .personal-info-container {
      flex-direction: column;
      align-items: center;
    }
    
    .avatar-section {
      width: 100%;
      max-width: 200px;
      margin-bottom: 20px;
    }
    
    .navigation-tabs {
      flex-wrap: nowrap;
      overflow-x: auto;
      padding: 10px 5px;
      gap: 5px;
    }
    
    .tab-button {
      padding: 8px 15px;
      white-space: nowrap;
    }
    
    .skills-chart-container {
      width: 100%;
    }
    
    .cv-container {
      flex-direction: column;
    }
    
    .profile-guide {
      bottom: 10px;
      right: 10px;
      max-width: 300px;
    }
    
    .guide-avatar {
      width: 50px;
      height: 50px;
    }
    
    .badge-modal, 
    .modal-content {
      max-width: 90%;
      padding: 15px;
    }
  }
  
  @media (max-width: 480px) {
    .section-title {
      font-size: 1.5rem;
    }
    
    .skills-grid,
    .jobs-grid,
    .badge-grid,
    .career-skills-grid {
      grid-template-columns: 1fr;
    }
    
    .sensory-categories {
      grid-template-columns: 1fr;
    }
    
    .modal-content {
      padding: 15px;
    }
    
    .profile-guide {
      max-width: 90%;
      left: 0;
      right: 0;
      margin: 0 auto;
    }
  }
  
  /* Impression du CV */
  @media print {
    .profile-container {
      padding: 0;
      max-width: 100%;
    }
    
    .profile-header,
    .navigation-tabs,
    .accessibility-controls,
    .cv-customize,
    .cv-actions,
    .profile-guide {
      display: none !important;
    }
    
    .profile-content {
      margin: 0;
      padding: 0;
    }
    
    .profile-section {
      border: none;
      box-shadow: none;
      padding: 0;
      margin: 0;
    }
    
    .cv-preview {
      width: 100%;
      box-shadow: none;
    }
  }
</style>