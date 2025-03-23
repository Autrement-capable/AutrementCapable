<template>
  <!-- Inclusion de Font Awesome pour les icônes -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <div class="formations-page">
    <div v-if="showBadgeNotification" class="badge-unlock-overlay">
      <div class="badge-unlock-animation">
        <div class="badge-icon">🎓</div>
        <h2>Badge débloqué !</h2>
        <h3>Première Formation</h3>
        <p>Vous vous êtes inscrit(e) à votre première formation. Félicitations!</p>
        <button @click="showBadgeNotification = false" class="close-animation-btn">Continuer</button>
      </div>
    </div>
    <header>
      <h1>Découvrez des formations adaptées à vos besoins</h1>
      <p class="subtitle">Entrez directement en contact avec les organismes de formation</p>
    </header>

    <!-- Catégories principales -->
    <section class="category-selector">
      <button 
        class="category-button"
        :class="{ active: selectedCategory === 'recommandees' }"
        @click="selectedCategory = 'recommandees'; resetFilters()"
      >
        <i class="fas fa-star category-icon"></i>
        Recommandées pour moi
      </button>
      <button 
        class="category-button"
        :class="{ active: selectedCategory === 'toutes' }"
        @click="selectedCategory = 'toutes'; resetFilters()"
      >
        <i class="fas fa-list category-icon"></i>
        Toutes les formations
      </button>
      <button 
        class="category-button"
        :class="{ active: selectedCategory === 'suivies' }"
        @click="selectedCategory = 'suivies'; resetFilters()"
      >
        <i class="fas fa-bookmark category-icon"></i>
        Mes formations suivies
      </button>
    </section>

    <!-- Nouveau panneau de filtres -->
    <section class="filters-section">
      <div class="filters-toggle" @click="showFilters = !showFilters">
        <i class="fas fa-filter"></i> 
        Filtrer les formations
        <span class="active-filters-count" v-if="activeFiltersCount > 0">{{ activeFiltersCount }}</span>
        <i class="fas" :class="showFilters ? 'fa-chevron-up' : 'fa-chevron-down'"></i>
      </div>
      
      <div class="filters-panel" v-if="showFilters">
        <div class="filters-grid">
          <!-- Filtre par durée -->
          <div class="filter-group">
            <h3><i class="fas fa-clock"></i> Durée</h3>
            <div class="filter-options">
              <label class="filter-option">
                <input type="checkbox" v-model="filters.duration.short"> Courte (&lt; 10h)
              </label>
              <label class="filter-option">
                <input type="checkbox" v-model="filters.duration.medium"> Moyenne (10-20h)
              </label>
              <label class="filter-option">
                <input type="checkbox" v-model="filters.duration.long"> Longue (&gt; 20h)
              </label>
            </div>
          </div>
          
          <!-- Filtre par niveau -->
          <div class="filter-group">
            <h3><i class="fas fa-signal"></i> Niveau</h3>
            <div class="filter-options">
              <label class="filter-option">
                <input type="checkbox" v-model="filters.level.beginner"> Débutant
              </label>
              <label class="filter-option">
                <input type="checkbox" v-model="filters.level.intermediate"> Intermédiaire
              </label>
              <label class="filter-option">
                <input type="checkbox" v-model="filters.level.advanced"> Avancé
              </label>
              <label class="filter-option">
                <input type="checkbox" v-model="filters.level.allLevels"> Tous niveaux
              </label>
            </div>
          </div>
          
          <!-- Filtre par mode de formation -->
          <div class="filter-group">
            <h3><i class="fas fa-map-marker-alt"></i> Modalité</h3>
            <div class="filter-options">
              <label class="filter-option">
                <input type="checkbox" v-model="filters.location.inPerson"> Présentiel
              </label>
              <label class="filter-option">
                <input type="checkbox" v-model="filters.location.remote"> À distance
              </label>
              <label class="filter-option">
                <input type="checkbox" v-model="filters.location.hybrid"> Mixte
              </label>
            </div>
          </div>
          
          <!-- Filtre par certification -->
          <div class="filter-group">
            <h3><i class="fas fa-certificate"></i> Certification</h3>
            <div class="filter-options">
              <label class="filter-option">
                <input type="checkbox" v-model="filters.certification.certified"> Avec certification
              </label>
              <label class="filter-option">
                <input type="checkbox" v-model="filters.certification.notCertified"> Sans certification
              </label>
            </div>
          </div>
          
          <!-- Filtre par compétences -->
          <div class="filter-group wide">
            <h3><i class="fas fa-brain"></i> Compétences développées</h3>
            <div class="filter-options skills-grid">
              <label v-for="skill in availableSkills" :key="skill.id" class="filter-option skill-option">
                <input type="checkbox" v-model="filters.skills[skill.id]"> {{ skill.name }}
              </label>
            </div>
          </div>
          
          <!-- Filtre par adaptations -->
          <div class="filter-group wide">
            <h3><i class="fas fa-universal-access"></i> Adaptations disponibles</h3>
            <div class="filter-options adaptations-grid">
              <label v-for="adaptation in adaptations" :key="adaptation.id" class="filter-option adaptation-option">
                <input type="checkbox" v-model="filters.adaptations[adaptation.id]"> {{ adaptation.name }}
              </label>
            </div>
          </div>
        </div>
        
        <div class="filter-actions">
          <button class="reset-filters-btn" @click="resetFilters()">
            <i class="fas fa-times"></i> Réinitialiser les filtres
          </button>
          <button class="apply-filters-btn" @click="applyFilters()">
            <i class="fas fa-check"></i> Appliquer les filtres
          </button>
        </div>
      </div>
      
      <!-- Tags de filtres actifs -->
      <div class="active-filters" v-if="activeFiltersCount > 0">
        <span class="active-filter-tag" v-for="(tag, index) in activeFiltersTags" :key="index">
          {{ tag.label }}
          <i class="fas fa-times" @click="removeFilter(tag.type, tag.value)"></i>
        </span>
        <button class="clear-all-filters" @click="resetFilters()">
          Effacer tous les filtres
        </button>
      </div>
    </section>

    <!-- Contrôles de tri et vue -->
    <section class="sort-and-view">
      <div class="sort-options">
        <label for="sortBy">Trier par :</label>
        <select id="sortBy" v-model="sortOption">
          <option value="recommended">Recommandation</option>
          <option value="titleAsc">Titre (A-Z)</option>
          <option value="titleDesc">Titre (Z-A)</option>
          <option value="durationAsc">Durée (croissante)</option>
          <option value="durationDesc">Durée (décroissante)</option>
          <option value="dateAsc">Date (plus proche)</option>
          <option value="dateDesc">Date (plus éloignée)</option>
        </select>
      </div>
      
      <div class="view-toggle">
        <button :class="{ active: viewMode === 'card' }" @click="viewMode = 'card'">
          <i class="fas fa-th-large"></i>
        </button>
        <button :class="{ active: viewMode === 'list' }" @click="viewMode = 'list'">
          <i class="fas fa-list"></i>
        </button>
      </div>
    </section>

    <!-- Résultats de recherche et compteur -->
    <section class="search-results-info">
      <p v-if="filteredFormations.length > 0">
        <span class="results-count">{{ filteredFormations.length }}</span> 
        formation{{ filteredFormations.length > 1 ? 's' : '' }} trouvée{{ filteredFormations.length > 1 ? 's' : '' }}
      </p>
      <p v-else>Aucune formation ne correspond à vos critères</p>
    </section>

    <!-- Liste des formations (avec classes conditionnelles selon le mode d'affichage) -->
    <section :class="['formations-list', viewMode === 'list' ? 'list-view' : 'card-view']">
      <transition-group name="formation-item">
        <div 
          v-for="formation in filteredAndSortedFormations" 
          :key="formation.id" 
          class="formation-card"
          @click="toggleFormationDetails(formation.id)"
        >
          <div class="formation-header">
            <div class="entreprise-logo" :style="{ backgroundColor: formation.couleur }">
              <i class="fas" :class="formation.icone"></i>
            </div>
            <div class="formation-info">
              <h2>{{ formation.titre }}</h2>
              <p class="entreprise">{{ formation.entreprise }}</p>
              <div class="formation-badges">
                <span class="badge badge-duree">{{ formation.duree }}</span>
                <span class="badge badge-niveau">{{ formation.niveau }}</span>
                <span v-if="formation.certification" class="badge badge-certification">Certification</span>
                <span class="badge badge-location">{{ formation.localisation }}</span>
                
                <!-- Badge de statut de formation -->
                <span v-if="formationStatuses[formation.id]" 
                      class="badge badge-status" 
                      :class="getStatusClass(formationStatuses[formation.id])">
                  {{ getStatusLabel(formationStatuses[formation.id]) }}
                </span>
              </div>
            </div>
            <div class="formation-actions-preview">
              <button class="preview-button">
                <i class="fas fa-chevron-down arrow-icon" :class="{ 'rotated': expandedFormations.includes(formation.id) }"></i>
              </button>
            </div>
          </div>
          
          <div v-if="expandedFormations.includes(formation.id)" class="formation-details">
            <p class="formation-description">{{ formation.description }}</p>
            
            <div class="formation-competences">
              <h3>Compétences développées :</h3>
              <ul class="competences-list">
                <li v-for="(competence, index) in formation.competences" :key="index" class="competence-item">
                  {{ competence }}
                </li>
              </ul>
            </div>
            
            <div class="entreprise-details">
              <h3>À propos de {{ formation.entreprise }}</h3>
              <p>{{ formation.entrepriseDescription }}</p>
              <div class="entreprise-contact">
                <p><strong>Contact :</strong> {{ formation.contact }}</p>
                <p><strong>Adresse :</strong> {{ formation.adresse }}</p>
                <p v-if="formation.accessibility"><strong>Accessibilité :</strong> {{ formation.accessibility }}</p>
              </div>
            </div>
            
            <!-- Statut actuel de la formation -->
            <div v-if="formationStatuses[formation.id]" class="status-section">
              <h3>Statut actuel :</h3>
              <div class="status-info">
                <div class="status-badge" :class="getStatusClass(formationStatuses[formation.id])">
                  {{ getStatusLabel(formationStatuses[formation.id]) }}
                </div>
                <div class="status-timeline">
                  <div class="timeline-step" :class="{ active: isStatusActive('interested', formation.id) }">
                    <div class="step-icon"><i class="fas fa-heart"></i></div>
                    <div class="step-label">Intéressé(e)</div>
                  </div>
                  <div class="timeline-connector"></div>
                  <div class="timeline-step" :class="{ active: isStatusActive('contacted', formation.id) }">
                    <div class="step-icon"><i class="fas fa-envelope"></i></div>
                    <div class="step-label">Contact pris</div>
                  </div>
                  <div class="timeline-connector"></div>
                  <div class="timeline-step" :class="{ active: isStatusActive('application', formation.id) }">
                    <div class="step-icon"><i class="fas fa-file-alt"></i></div>
                    <div class="step-label">Inscription demandée</div>
                  </div>
                  <div class="timeline-connector"></div>
                  <div class="timeline-step" :class="{ active: isStatusActive('registered', formation.id) }">
                    <div class="step-icon"><i class="fas fa-check-circle"></i></div>
                    <div class="step-label">Inscrit(e)</div>
                  </div>
                </div>
                <div v-if="formationStatusNotes[formation.id]" class="status-notes">
                  <p><strong>Notes :</strong> {{ formationStatusNotes[formation.id] }}</p>
                </div>
                <div class="status-updated">
                  <p>Dernière mise à jour : {{ formationStatusDates[formation.id] || 'Aujourd\'hui' }}</p>
                </div>
              </div>
            </div>
            
            <div class="formation-actions">
              <button 
                v-if="!formationStatuses[formation.id]" 
                class="formation-button interested" 
                @click.stop="updateFormationStatus(formation.id, 'interested')"
              >
                <i class="fas fa-heart"></i> Marquer comme intéressé(e)
              </button>
              <button 
                v-if="!isStatusActive('contacted', formation.id)" 
                class="formation-button contact" 
                @click.stop="contacterEntreprise(formation)"
              >
                <i class="fas fa-envelope"></i> Contacter directement
              </button>
              <button 
                v-if="isStatusActive('contacted', formation.id) && !isStatusActive('application', formation.id)" 
                class="formation-button application" 
                @click.stop="updateFormationStatus(formation.id, 'application')"
              >
                <i class="fas fa-file-alt"></i> Demander l'inscription
              </button>
              <button 
                v-if="formationStatuses[formation.id]" 
                class="formation-button notes" 
                @click.stop="openNotesModal(formation.id)"
              >
                <i class="fas fa-edit"></i> Ajouter une note
              </button>
              <button 
                v-if="isStatusActive('application', formation.id) && !isStatusActive('registered', formation.id)"
                class="formation-button registered" 
                @click.stop="updateFormationStatus(formation.id, 'registered')"
              >
                <i class="fas fa-check-circle"></i> Marquer comme inscrit(e)
              </button>
              <button 
                v-if="formationStatuses[formation.id]" 
                class="formation-button reset" 
                @click.stop="resetFormationStatus(formation.id)"
              >
                <i class="fas fa-redo"></i> Réinitialiser
              </button>
            </div>
            
            <div v-if="formation.prochaineSessions && formation.prochaineSessions.length > 0" class="sessions">
              <h3>Prochaines sessions :</h3>
              <ul class="sessions-list">
                <li v-for="(session, index) in formation.prochaineSessions" :key="index" class="session-item">
                  <div class="session-date">{{ session.date }}</div>
                  <div class="session-places">{{ session.placesDisponibles }} places disponibles</div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </transition-group>
    </section>

    <div v-if="filteredFormations.length === 0" class="no-formations">
      <i class="fas fa-search empty-icon"></i>
      <p>Aucune formation ne correspond à vos critères</p>
      <button class="reset-filters-btn" @click="resetFilters()">
        <i class="fas fa-times"></i> Réinitialiser les filtres
      </button>
    </div>

    <!-- Modal de contact -->
    <div v-if="showContactModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <button class="close-modal" @click="closeModal">×</button>
        <h2>Contacter {{ selectedFormation ? selectedFormation.entreprise : '' }}</h2>
        
        <form @submit.prevent="envoyerMessage">
          <div class="form-group">
            <label for="nom">Votre nom</label>
            <input type="text" id="nom" v-model="contactForm.nom" required>
          </div>
          
          <div class="form-group">
            <label for="email">Votre email</label>
            <input type="email" id="email" v-model="contactForm.email" required>
          </div>
          
          <div class="form-group">
            <label for="telephone">Votre téléphone</label>
            <input type="tel" id="telephone" v-model="contactForm.telephone">
          </div>
          
          <div class="form-group">
            <label for="message">Votre message</label>
            <textarea id="message" v-model="contactForm.message" rows="4" required></textarea>
          </div>
          
          <div class="form-actions">
            <button type="submit" class="submit-button">Envoyer</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal pour les notes -->
    <div v-if="showNotesModal" class="modal-overlay" @click="closeNotesModal">
      <div class="modal-content" @click.stop>
        <button class="close-modal" @click="closeNotesModal">×</button>
        <h2>Ajouter une note pour cette formation</h2>
        
        <form @submit.prevent="saveNotes">
          <div class="form-group">
            <label for="notes">Notes personnelles</label>
            <textarea id="notes" v-model="notesForm.text" rows="6" placeholder="Ex: Entretien téléphonique le 25/03, personne contactée: Marie Dupont, délai de réponse: 1 semaine..."></textarea>
          </div>
          
          <div class="form-group">
            <label>
              <input type="checkbox" v-model="notesForm.reminder"> 
              Me rappeler de suivre ce dossier
            </label>
          </div>
          
          <div v-if="notesForm.reminder" class="form-group">
            <label for="reminderDate">Date de rappel</label>
            <input type="date" id="reminderDate" v-model="notesForm.reminderDate">
          </div>
          
          <div class="form-actions">
            <button type="submit" class="submit-button">Enregistrer</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { unlockBadge, isBadgeUnlocked } from '@/utils/badges';

export default {
  name: 'FormationsPage',
  data() {
    return {
      selectedCategory: 'recommandees',
      badgeFormationId: 8,
      showBadgeNotification: false,
      badgeUnlocked: null,
      expandedFormations: [],
      showContactModal: false,
      showNotesModal: false,
      selectedFormation: null,
      selectedFormationId: null,
      showFilters: false,
      formationStatuses: {}, // Stocke le statut de chaque formation
      formationStatusNotes: {}, // Stocke les notes pour chaque formation
      formationStatusDates: {}, // Stocke les dates de mise à jour de statut
      formationReminders: {}, // Stocke les rappels
      contactForm: {
        nom: '',
        email: '',
        telephone: '',
        message: ''
      },
      notesForm: {
        text: '',
        reminder: false,
        reminderDate: ''
      },
      // Options de tri et d'affichage
      sortOption: 'recommended',
      viewMode: 'list',
      // Filtres
      filters: {
        duration: {
          short: false,    // < 10h
          medium: false,   // 10-20h
          long: false      // > 20h
        },
        level: {
          beginner: false,
          intermediate: false,
          advanced: false,
          allLevels: false
        },
        location: {
          inPerson: false,
          remote: false,
          hybrid: false
        },
        certification: {
          certified: false,
          notCertified: false
        },
        skills: {},
        adaptations: {}
      },
      // Compétences disponibles pour le filtrage
      availableSkills: [
        { id: 'informatique', name: 'Informatique' },
        { id: 'communication', name: 'Communication' },
        { id: 'gestion_stress', name: 'Gestion du stress' },
        { id: 'travail_equipe', name: 'Travail en équipe' },
        { id: 'bureautique', name: 'Bureautique' },
        { id: 'langues', name: 'Langues étrangères' },
        { id: 'creativite', name: 'Créativité' },
        { id: 'organisation', name: 'Organisation' }
      ],
      // Adaptations d'accessibilité disponibles
      adaptations: [
        { id: 'rythme_adapte', name: 'Rythme adapté' },
        { id: 'supports_visuels', name: 'Supports visuels adaptés' },
        { id: 'accompagnement', name: 'Accompagnement personnalisé' },
        { id: 'locaux_accessibles', name: 'Locaux accessibles' },
        { id: 'petits_groupes', name: 'Petits groupes' },
        { id: 'pause_frequente', name: 'Pauses fréquentes' }
      ],
      // Liste des formations
      formations: [
        {
          id: 1,
          titre: "Initiation à l'informatique",
          entreprise: "InfoTech Formation",
          icone: "fa-laptop",
          couleur: "#4285F4",
          description: "Cette formation vous permet d'acquérir les bases de l'informatique dans un environnement adapté et à votre rythme. Notre approche pédagogique est spécialement conçue pour les personnes en situation de handicap neurologique.",
          duree: "10h",
          dureeHeures: 10,
          niveau: "Débutant",
          certification: true,
          localisation: "Paris + À distance",
          modalites: ["presentiel", "distance"],
          recommandee: true,
          entrepriseDescription: "InfoTech Formation est spécialisée dans la formation numérique inclusive. Nos formateurs sont formés aux besoins spécifiques des personnes en situation de handicap.",
          contact: "contact@infotech-formation.fr - 01 23 45 67 89",
          adresse: "15 rue des Lilas, 75020 Paris",
          accessibility: "Locaux entièrement accessibles, supports adaptés, rythme personnalisé",
          adaptationsDisponibles: ["rythme_adapte", "supports_visuels", "locaux_accessibles"],
          prochaineSessions: [
            { date: "15 avril 2025", placesDisponibles: 5 },
            { date: "2 mai 2025", placesDisponibles: 8 }
          ],
          competences: [
            "Utiliser un ordinateur",
            "Naviguer sur internet",
            "Utiliser une messagerie électronique",
            "Créer des documents simples"
          ],
          domainesCompetences: ["informatique", "bureautique"]
        },
        {
          id: 2,
          titre: "Communication professionnelle",
          entreprise: "CommPro",
          icone: "fa-comments",
          couleur: "#ea4335",
          description: "Développez vos compétences en communication pour vous sentir plus à l'aise dans un environnement professionnel. Formation adaptée avec une pédagogie bienveillante et des exercices pratiques.",
          duree: "15h",
          dureeHeures: 15,
          niveau: "Intermédiaire",
          certification: false,
          localisation: "Lyon",
          modalites: ["presentiel"],
          recommandee: true,
          entrepriseDescription: "CommPro est un centre de formation spécialisé dans le développement des compétences relationnelles en milieu professionnel. Notre équipe est sensibilisée à l'inclusion de tous les profils.",
          contact: "formation@commpro.fr - 04 56 78 90 12",
          adresse: "8 avenue de la République, 69002 Lyon",
          accessibility: "Supports visuels adaptés, possibilité d'être accompagné",
          adaptationsDisponibles: ["supports_visuels", "accompagnement", "petits_groupes"],
          prochaineSessions: [
            { date: "22 avril 2025", placesDisponibles: 3 }
          ],
          competences: [
            "Communication verbale claire",
            "Écoute active",
            "Rédaction d'emails professionnels",
            "Prise de parole en groupe"
          ],
          domainesCompetences: ["communication", "travail_equipe"]
        },
        {
          id: 3,
          titre: "Gestion du stress au travail",
          entreprise: "BienÊtre Pro",
          icone: "fa-heart",
          couleur: "#34a853",
          description: "Découvrez des techniques pour gérer le stress et l'anxiété dans votre environnement professionnel. Approche personnalisée selon vos besoins spécifiques.",
          duree: "8h",
          dureeHeures: 8,
          niveau: "Tous niveaux",
          certification: false,
          localisation: "À distance",
          modalites: ["distance"],
          recommandee: true,
          entrepriseDescription: "BienÊtre Pro propose des formations centrées sur le bien-être et l'épanouissement professionnel. Nos méthodes sont inclusives et adaptées à tous les profils.",
          contact: "contact@bienetrepro.fr - 07 12 34 56 78",
          adresse: "Formation en ligne",
          accessibility: "Formations à distance avec supports adaptés et accompagnement individuel",
          adaptationsDisponibles: ["rythme_adapte", "supports_visuels", "accompagnement", "pause_frequente"],
          prochaineSessions: [
            { date: "En continu", placesDisponibles: 12 }
          ],
          competences: [
            "Identifier les sources de stress",
            "Techniques de respiration",
            "Organisation du travail",
            "Établir des limites saines"
          ],
          domainesCompetences: ["gestion_stress", "organisation"]
        },
        {
          id: 4,
          titre: "Excel pour débutants",
          entreprise: "BureauPro",
          icone: "fa-file-excel",
          couleur: "#fbbc05",
          description: "Maîtrisez les fonctionnalités de base d'Excel pour améliorer votre productivité. Formation avec un rythme adapté et des exercices progressifs.",
          duree: "12h",
          dureeHeures: 12,
          niveau: "Débutant",
          certification: true,
          localisation: "Marseille + À distance",
          modalites: ["presentiel", "distance"],
          recommandee: false,
          entrepriseDescription: "BureauPro est un organisme de formation spécialisé dans les outils bureautiques. Notre pédagogie s'adapte aux besoins de chacun avec un suivi personnalisé.",
          contact: "info@bureaupro.fr - 04 91 23 45 67",
          adresse: "25 boulevard National, 13003 Marseille",
          accessibility: "Supports adaptés, possibilité de ralentir le rythme, aide individuelle",
          adaptationsDisponibles: ["rythme_adapte", "supports_visuels", "accompagnement"],
          prochaineSessions: [
            { date: "18 avril 2025", placesDisponibles: 7 },
            { date: "10 mai 2025", placesDisponibles: 9 }
          ],
          competences: [
            "Création de tableaux",
            "Formules de base",
            "Mise en forme conditionnelle",
            "Création de graphiques simples"
          ],
          domainesCompetences: ["informatique", "bureautique"]
        },
        {
          id: 5,
          titre: "Travailler en équipe",
          entreprise: "TeamWork",
          icone: "fa-users",
          couleur: "#7e57c2",
          description: "Développez vos compétences pour mieux collaborer et communiquer en équipe. Méthodes adaptées aux différents profils cognitifs.",
          duree: "20h",
          dureeHeures: 20,
          niveau: "Intermédiaire",
          certification: true,
          localisation: "Lille",
          modalites: ["presentiel"],
          recommandee: false,
          entrepriseDescription: "TeamWork est spécialisé dans le développement des compétences collaboratives et l'inclusion en entreprise. Nos formations sont conçues pour valoriser la neurodiversité.",
          contact: "formations@teamwork.fr - 03 20 45 67 89",
          adresse: "12 rue des Ponts, 59000 Lille",
          accessibility: "Locaux accessibles, méthodologie adaptée aux différents profils",
          adaptationsDisponibles: ["locaux_accessibles", "petits_groupes", "rythme_adapte", "accompagnement"],
          prochaineSessions: [
            { date: "5 mai 2025", placesDisponibles: 4 }
          ],
          competences: [
            "Communication en groupe",
            "Résolution de conflits",
            "Gestion des différences",
            "Partage des tâches"
          ],
          domainesCompetences: ["communication", "travail_equipe", "gestion_stress"]
        },
        {
          id: 6,
          titre: "Création de site web",
          entreprise: "WebDev Academy",
          icone: "fa-code",
          couleur: "#0097a7",
          description: "Apprenez à créer votre propre site web de A à Z. Cette formation vous guidera à travers toutes les étapes nécessaires, du HTML/CSS jusqu'à la mise en ligne.",
          duree: "30h",
          dureeHeures: 30,
          niveau: "Intermédiaire",
          certification: true,
          localisation: "À distance",
          modalites: ["distance"],
          recommandee: false,
          entrepriseDescription: "WebDev Academy est une école en ligne spécialisée dans les métiers du web. Nos formations sont conçues pour être accessibles à tous, avec un rythme personnalisable.",
          contact: "info@webdev-academy.fr - 09 75 12 34 56",
          adresse: "Formation 100% en ligne",
          accessibility: "Plateforme accessible, rythme personnalisable, supports adaptés avec descriptions alternatives",
          adaptationsDisponibles: ["rythme_adapte", "supports_visuels", "pause_frequente"],
          prochaineSessions: [
            { date: "1er avril 2025", placesDisponibles: 10 },
            { date: "15 mai 2025", placesDisponibles: 15 }
          ],
          competences: [
            "HTML et CSS",
            "JavaScript basique",
            "Mise en page responsive",
            "Publication en ligne"
          ],
          domainesCompetences: ["informatique", "creativite"]
        },
        {
          id: 7,
          titre: "Anglais professionnel",
          entreprise: "LinguaPlus",
          icone: "fa-language",
          couleur: "#f06292",
          description: "Améliorez vos compétences en anglais professionnel avec une approche pédagogique adaptée aux différents styles d'apprentissage. Cours en petits groupes avec beaucoup de pratique orale.",
          duree: "25h",
          dureeHeures: 25,
          niveau: "Tous niveaux",
          certification: true,
          localisation: "Paris + À distance",
          modalites: ["presentiel", "distance"],
          recommandee: false,
          entrepriseDescription: "LinguaPlus est un centre de formation linguistique qui propose des cours adaptés aux besoins spécifiques des apprenants. Nos formateurs sont sensibilisés aux différentes neurodiversités.",
          contact: "contact@linguaplus.fr - 01 45 67 89 10",
          adresse: "29 rue des Écoles, 75005 Paris",
          accessibility: "Supports multi-sensoriels, rythme adapté, approche visuelle et pratique",
          adaptationsDisponibles: ["rythme_adapte", "supports_visuels", "petits_groupes", "pause_frequente"],
          prochaineSessions: [
            { date: "20 avril 2025", placesDisponibles: 6 },
            { date: "12 juin 2025", placesDisponibles: 8 }
          ],
          competences: [
            "Conversation professionnelle",
            "Rédaction d'emails et documents",
            "Présentation orale",
            "Vocabulaire technique"
          ],
          domainesCompetences: ["communication", "langues"]
        }
      ]
    };
  },
  computed: {
    // Filtrer les formations selon la catégorie sélectionnée
    filteredFormations() {
      let filtered = [];
      
      // Filtrer d'abord par catégorie principale
      if (this.selectedCategory === 'recommandees') {
        filtered = this.formations.filter(formation => formation.recommandee);
      } else if (this.selectedCategory === 'suivies') {
        filtered = this.formations.filter(formation => this.formationStatuses[formation.id]);
      } else {
        filtered = [...this.formations];
      }
      
      // Appliquer les filtres avancés
      filtered = this.applyAdvancedFilters(filtered);
      
      return filtered;
    },
    
    // Appliquer le tri aux formations filtrées
    filteredAndSortedFormations() {
      let sorted = [...this.filteredFormations];
      
      switch(this.sortOption) {
        case 'titleAsc':
          sorted.sort((a, b) => a.titre.localeCompare(b.titre));
          break;
        case 'titleDesc':
          sorted.sort((a, b) => b.titre.localeCompare(a.titre));
          break;
        case 'durationAsc':
          sorted.sort((a, b) => a.dureeHeures - b.dureeHeures);
          break;
        case 'durationDesc':
          sorted.sort((a, b) => b.dureeHeures - a.dureeHeures);
          break;
        case 'dateAsc':
          sorted.sort((a, b) => {
            const dateA = a.prochaineSessions && a.prochaineSessions.length > 0 ? a.prochaineSessions[0].date : '9999';
            const dateB = b.prochaineSessions && b.prochaineSessions.length > 0 ? b.prochaineSessions[0].date : '9999';
            return dateA.localeCompare(dateB);
          });
          break;
        case 'dateDesc':
          sorted.sort((a, b) => {
            const dateA = a.prochaineSessions && a.prochaineSessions.length > 0 ? a.prochaineSessions[0].date : '0000';
            const dateB = b.prochaineSessions && b.prochaineSessions.length > 0 ? b.prochaineSessions[0].date : '0000';
            return dateB.localeCompare(dateA);
          });
          break;
        case 'recommended':
        default:
          // Conserver l'ordre recommandé
          break;
      }
      
      return sorted;
    },
    
    // Nombre de filtres actifs
    activeFiltersCount() {
      let count = 0;
      
      // Compter les filtres de durée actifs
      count += Object.values(this.filters.duration).filter(v => v).length;
      
      // Compter les filtres de niveau actifs
      count += Object.values(this.filters.level).filter(v => v).length;
      
      // Compter les filtres de localisation actifs
      count += Object.values(this.filters.location).filter(v => v).length;
      
      // Compter les filtres de certification actifs
      count += Object.values(this.filters.certification).filter(v => v).length;
      
      // Compter les filtres de compétences actifs
      count += Object.values(this.filters.skills).filter(v => v).length;
      
      // Compter les filtres d'adaptations actifs
      count += Object.values(this.filters.adaptations).filter(v => v).length;
      
      return count;
    },
    
    // Tags des filtres actifs pour l'affichage
    activeFiltersTags() {
      let tags = [];
      
      // Ajouter les tags de durée
      if (this.filters.duration.short) tags.push({ type: 'duration', value: 'short', label: 'Durée: Courte' });
      if (this.filters.duration.medium) tags.push({ type: 'duration', value: 'medium', label: 'Durée: Moyenne' });
      if (this.filters.duration.long) tags.push({ type: 'duration', value: 'long', label: 'Durée: Longue' });
      
      // Ajouter les tags de niveau
      if (this.filters.level.beginner) tags.push({ type: 'level', value: 'beginner', label: 'Niveau: Débutant' });
      if (this.filters.level.intermediate) tags.push({ type: 'level', value: 'intermediate', label: 'Niveau: Intermédiaire' });
      if (this.filters.level.advanced) tags.push({ type: 'level', value: 'advanced', label: 'Niveau: Avancé' });
      if (this.filters.level.allLevels) tags.push({ type: 'level', value: 'allLevels', label: 'Niveau: Tous niveaux' });
      
      // Ajouter les tags de localisation
      if (this.filters.location.inPerson) tags.push({ type: 'location', value: 'inPerson', label: 'Lieu: Présentiel' });
      if (this.filters.location.remote) tags.push({ type: 'location', value: 'remote', label: 'Lieu: À distance' });
      if (this.filters.location.hybrid) tags.push({ type: 'location', value: 'hybrid', label: 'Lieu: Mixte' });
      
      // Ajouter les tags de certification
      if (this.filters.certification.certified) tags.push({ type: 'certification', value: 'certified', label: 'Avec certification' });
      if (this.filters.certification.notCertified) tags.push({ type: 'certification', value: 'notCertified', label: 'Sans certification' });
      
      // Ajouter les tags de compétences
      for (const [skillId, isActive] of Object.entries(this.filters.skills)) {
        if (isActive) {
          const skill = this.availableSkills.find(s => s.id === skillId);
          if (skill) {
            tags.push({ type: 'skill', value: skillId, label: `Compétence: ${skill.name}` });
          }
        }
      }
      
      // Ajouter les tags d'adaptations
      for (const [adaptationId, isActive] of Object.entries(this.filters.adaptations)) {
        if (isActive) {
          const adaptation = this.adaptations.find(a => a.id === adaptationId);
          if (adaptation) {
            tags.push({ type: 'adaptation', value: adaptationId, label: `Adaptation: ${adaptation.name}` });
          }
        }
      }
      
      return tags;
    }
  },
  mounted() {
    // Chargement des données depuis le localStorage au démarrage
    this.loadFormationData();
    
    // Initialiser les filtres de compétences et d'adaptations comme objets vides
    this.initializeFilters();
    
    // Vérifier les rappels
    this.checkReminders();
  },
  methods: {
    // Méthode pour initialiser les filtres dynamiquement
    initializeFilters() {
      // Initialiser les filtres de compétences
      this.availableSkills.forEach(skill => {
        this.filters.skills[skill.id] = false;
      });
      
      // Initialiser les filtres d'adaptations
      this.adaptations.forEach(adaptation => {
        this.filters.adaptations[adaptation.id] = false;
      });
    },
    
    // Appliquer tous les filtres avancés à un ensemble de formations
    applyAdvancedFilters(formations) {
      return formations.filter(formation => {
        // Filtrer par durée
        if (this.isAnyFilterActive(this.filters.duration)) {
          const durationMatch = (
            (this.filters.duration.short && formation.dureeHeures < 10) ||
            (this.filters.duration.medium && formation.dureeHeures >= 10 && formation.dureeHeures <= 20) ||
            (this.filters.duration.long && formation.dureeHeures > 20)
          );
          if (!durationMatch) return false;
        }
        
        // Filtrer par niveau
        if (this.isAnyFilterActive(this.filters.level)) {
          const levelMatch = (
            (this.filters.level.beginner && formation.niveau === "Débutant") ||
            (this.filters.level.intermediate && formation.niveau === "Intermédiaire") ||
            (this.filters.level.advanced && formation.niveau === "Avancé") ||
            (this.filters.level.allLevels && formation.niveau === "Tous niveaux")
          );
          if (!levelMatch) return false;
        }
        
        // Filtrer par modalité
        if (this.isAnyFilterActive(this.filters.location)) {
          const locationMatch = (
            (this.filters.location.inPerson && formation.modalites.includes("presentiel")) ||
            (this.filters.location.remote && formation.modalites.includes("distance")) ||
            (this.filters.location.hybrid && formation.modalites.includes("presentiel") && formation.modalites.includes("distance"))
          );
          if (!locationMatch) return false;
        }
        
        // Filtrer par certification
        if (this.isAnyFilterActive(this.filters.certification)) {
          const certificationMatch = (
            (this.filters.certification.certified && formation.certification) ||
            (this.filters.certification.notCertified && !formation.certification)
          );
          if (!certificationMatch) return false;
        }
        
        // Filtrer par compétences
        if (this.isAnyFilterActive(this.filters.skills)) {
          const activeSkills = Object.entries(this.filters.skills)
            .filter(([, isActive]) => isActive)
            .map(([skillId]) => skillId);
            
          const skillsMatch = activeSkills.some(skillId => 
            formation.domainesCompetences && formation.domainesCompetences.includes(skillId)
          );
          
          if (!skillsMatch) return false;
        }
        
        // Filtrer par adaptations disponibles
        if (this.isAnyFilterActive(this.filters.adaptations)) {
          const activeAdaptations = Object.entries(this.filters.adaptations)
            .filter(([, isActive]) => isActive)
            .map(([adaptationId]) => adaptationId);
          const adaptationsMatch = activeAdaptations.every(adaptationId => 
            formation.adaptationsDisponibles && formation.adaptationsDisponibles.includes(adaptationId)
          );
          
          if (!adaptationsMatch) return false;
        }
        
        // Si tous les filtres sont passés, inclure cette formation
        return true;
      });
    },
    
    // Vérifier si au moins un filtre est actif dans un groupe
    isAnyFilterActive(filterGroup) {
      return Object.values(filterGroup).some(value => value);
    },
    
    // Appliquer les filtres (juste fermer le panneau)
    applyFilters() {
      this.showFilters = false;
    },
    
    // Réinitialiser tous les filtres
    resetFilters() {
      // Réinitialiser tous les filtres de durée
      Object.keys(this.filters.duration).forEach(key => {
        this.filters.duration[key] = false;
      });
      
      // Réinitialiser tous les filtres de niveau
      Object.keys(this.filters.level).forEach(key => {
        this.filters.level[key] = false;
      });
      
      // Réinitialiser tous les filtres de localisation
      Object.keys(this.filters.location).forEach(key => {
        this.filters.location[key] = false;
      });
      
      // Réinitialiser tous les filtres de certification
      Object.keys(this.filters.certification).forEach(key => {
        this.filters.certification[key] = false;
      });
      
      // Réinitialiser tous les filtres de compétences
      Object.keys(this.filters.skills).forEach(key => {
        this.filters.skills[key] = false;
      });
      
      // Réinitialiser tous les filtres d'adaptations
      Object.keys(this.filters.adaptations).forEach(key => {
        this.filters.adaptations[key] = false;
      });
    },
    
    // Supprimer un filtre spécifique
    removeFilter(type, value) {
      if (type === 'duration' || type === 'level' || type === 'location' || type === 'certification') {
        this.filters[type][value] = false;
      } else if (type === 'skill') {
        this.filters.skills[value] = false;
      } else if (type === 'adaptation') {
        this.filters.adaptations[value] = false;
      }
    },
    
    toggleFormationDetails(id) {
      if (this.expandedFormations.includes(id)) {
        this.expandedFormations = this.expandedFormations.filter(formationId => formationId !== id);
      } else {
        this.expandedFormations.push(id);
      }
    },
    
    contacterEntreprise(formation) {
      this.selectedFormation = formation;
      this.contactForm.message = `Bonjour, je souhaite obtenir plus d'informations concernant votre formation "${formation.titre}".`;
      this.showContactModal = true;
      
      // Mettre à jour le statut automatiquement lorsque le contact est pris
      this.updateFormationStatus(formation.id, 'contacted');
    },
    
    closeModal() {
      this.showContactModal = false;
    },
    
    envoyerMessage() {
      // Simuler l'envoi du message
      alert(`Message envoyé à ${this.selectedFormation.entreprise} !`);
      this.showContactModal = false;
      
      // Réinitialisation du formulaire
      this.contactForm = {
        nom: '',
        email: '',
        telephone: '',
        message: ''
      };
    },
    
    // Méthodes pour le système de statut
    updateFormationStatus(formationId, status) {
      // Mettre à jour le statut
      this.formationStatuses[formationId] = status;
      
      // Enregistrer la date de mise à jour
      this.formationStatusDates[formationId] = new Date().toLocaleDateString();
      
      // Sauvegarder dans le localStorage
      this.saveFormationData();
      
      if (status === 'registered') {
        this.checkAndUnlockFormationBadge();
      }

      // Si c'est un statut de contact, ouvrir automatiquement le modal de notes
      if (status === 'contacted') {
        this.openNotesModal(formationId);
      }
    },
    
    checkAndUnlockFormationBadge() {
      // Vérifier si c'est la première formation à laquelle l'utilisateur s'inscrit
      const isFirstRegistration = Object.values(this.formationStatuses).filter(
        status => status === 'registered'
      ).length === 1;
      
      // Si c'est la première inscription et que le badge n'est pas déjà débloqué
      if (isFirstRegistration && !isBadgeUnlocked(this.badgeFormationId)) {
        // Débloquer le badge
        const badgeUnlocked = unlockBadge(this.badgeFormationId);
        
        if (badgeUnlocked) {
          this.showBadgeNotification = true;
        }
      }
    },

    resetFormationStatus(formationId) {
      // Demander confirmation avant de réinitialiser
      if (confirm("Voulez-vous vraiment réinitialiser le statut de cette formation ?")) {
        // Supprimer le statut, les notes et les rappels associés
        delete this.formationStatuses[formationId];
        delete this.formationStatusNotes[formationId];
        delete this.formationStatusDates[formationId];
        delete this.formationReminders[formationId];
        
        // Sauvegarder les modifications
        this.saveFormationData();
      }
    },
    
    getStatusLabel(status) {
      const labels = {
        'interested': 'Intéressé(e)',
        'contacted': 'Contact pris',
        'application': 'Inscription demandée',
        'registered': 'Inscrit(e)'
      };
      return labels[status] || status;
    },
    
    getStatusClass(status) {
      const classes = {
        'interested': 'status-interested',
        'contacted': 'status-contacted',
        'application': 'status-application',
        'registered': 'status-registered'
      };
      return classes[status] || '';
    },
    
    isStatusActive(status, formationId) {
      const statusOrder = ['interested', 'contacted', 'application', 'registered'];
      const currentStatus = this.formationStatuses[formationId];
      
      if (!currentStatus) return false;
      
      const currentIndex = statusOrder.indexOf(currentStatus);
      const statusIndex = statusOrder.indexOf(status);
      
      // Si le statut actuel est au moins aussi avancé que le statut demandé
      return currentIndex >= statusIndex;
    },
    
    // Gestion des notes
    openNotesModal(formationId) {
      this.selectedFormationId = formationId;
      this.notesForm.text = this.formationStatusNotes[formationId] || '';
      this.notesForm.reminder = !!this.formationReminders[formationId];
      this.notesForm.reminderDate = this.formationReminders[formationId] || '';
      this.showNotesModal = true;
    },
    
    closeNotesModal() {
      this.showNotesModal = false;
      this.selectedFormationId = null;
    },
    
    saveNotes() {
      if (this.selectedFormationId) {
        // Enregistrer les notes
        this.formationStatusNotes[this.selectedFormationId] = this.notesForm.text;
        
        // Gestion du rappel
        if (this.notesForm.reminder && this.notesForm.reminderDate) {
          this.formationReminders[this.selectedFormationId] = this.notesForm.reminderDate;
        } else {
          delete this.formationReminders[this.selectedFormationId];
        }
        
        // Sauvegarder dans le localStorage
        this.saveFormationData();
        
        // Fermer le modal
        this.closeNotesModal();
      }
    },
    
    // Persistance des données
    saveFormationData() {
      // Sauvegarder les données de statut des formations dans le localStorage
      localStorage.setItem('formationStatuses', JSON.stringify(this.formationStatuses));
      localStorage.setItem('formationStatusNotes', JSON.stringify(this.formationStatusNotes));
      localStorage.setItem('formationStatusDates', JSON.stringify(this.formationStatusDates));
      localStorage.setItem('formationReminders', JSON.stringify(this.formationReminders));
    },
    
    loadFormationData() {
      // Charger les données depuis le localStorage
      const savedStatuses = localStorage.getItem('formationStatuses');
      const savedNotes = localStorage.getItem('formationStatusNotes');
      const savedDates = localStorage.getItem('formationStatusDates');
      const savedReminders = localStorage.getItem('formationReminders');
      
      if (savedStatuses) this.formationStatuses = JSON.parse(savedStatuses);
      if (savedNotes) this.formationStatusNotes = JSON.parse(savedNotes);
      if (savedDates) this.formationStatusDates = JSON.parse(savedDates);
      if (savedReminders) this.formationReminders = JSON.parse(savedReminders);
    },
    
    // Vérification des rappels
    checkReminders() {
      const today = new Date().toISOString().split('T')[0];
      let reminders = [];
      
      // Parcourir tous les rappels
      Object.entries(this.formationReminders).forEach(([formationId, reminderDate]) => {
        if (reminderDate <= today) {
          // Trouver la formation correspondante
          const formation = this.formations.find(f => f.id === parseInt(formationId));
          if (formation) {
            reminders.push({
              id: formationId,
              formation: formation.titre,
              entreprise: formation.entreprise
            });
          }
        }
      });
      
      // Si des rappels sont trouvés, afficher une notification
      if (reminders.length > 0) {
        let message = "Vous avez des rappels pour les formations suivantes :\n";
        reminders.forEach(reminder => {
          message += `- ${reminder.formation} (${reminder.entreprise})\n`;
        });
        alert(message);
      }
    }
  }
};
</script>

<style scoped>
/* Styles de base */
.formations-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Nunito', sans-serif;
}

header {
  margin-bottom: 30px;
  text-align: center;
}

h1 {
  font-size: 2.2rem;
  color: #3f51b5;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 1.2rem;
  color: #666;
  margin: 0;
}

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
  z-index: 1000;
  animation: fadeIn 0.5s ease-out;
}

.badge-unlock-animation {
  background-color: #fff;
  border-radius: 20px;
  padding: 30px;
  text-align: center;
  max-width: 400px;
  box-shadow: 0 0 30px rgba(63, 81, 181, 0.6);
  animation: scaleIn 0.5s ease-out;
}

.badge-icon {
  font-size: 80px;
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

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scaleIn {
  from { transform: scale(0.8); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

/* Catégories principales */
.category-selector {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 30px;
}

.category-button {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px 25px;
  color: #000000;
  background-color: #f5f5f5;
  border: 2px solid #e0e0e0;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.category-button:hover {
  background-color: #e0e0e0;
  color: #111;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.category-button.active {
  background-color: #3f51b5;
  color: white;
  border-color: #3f51b5;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(63, 81, 181, 0.4);
}

.category-icon {
  width: 24px;
  height: 24px;
}

/* Section des filtres */
.filters-section {
  margin-bottom: 20px;
}

.filters-toggle {
  background-color: #f5f5f5;
  padding: 12px 20px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
}

.filters-toggle:hover {
  background-color: #e0e0e0;
}

.active-filters-count {
  background-color: #3f51b5;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  margin-left: auto;
}

.filters-panel {
  margin-top: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  animation: slideDown 0.3s ease;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.filter-group {
  margin-bottom: 15px;
}

.filter-group.wide {
  grid-column: 1 / -1;
}

.filter-group h3 {
  font-size: 1rem;
  margin-bottom: 10px;
  color: #3f51b5;
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-options {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-option {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 0.9rem;
}

.skills-grid, .adaptations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 8px;
}

.filter-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #e0e0e0;
}

.reset-filters-btn, .apply-filters-btn {
  padding: 8px 15px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: all 0.3s ease;
  border: none;
}

.reset-filters-btn {
  background-color: #f5f5f5;
  color: #666;
}

.reset-filters-btn:hover {
  background-color: #e0e0e0;
}

.apply-filters-btn {
  background-color: #3f51b5;
  color: white;
}

.apply-filters-btn:hover {
  background-color: #303f9f;
}

/* Tags de filtres actifs */
.active-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 15px;
}

.active-filter-tag {
  background-color: #e8eaf6;
  color: #3f51b5;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.active-filter-tag i {
  cursor: pointer;
}

.clear-all-filters {
  background-color: transparent;
  color: #666;
  border: none;
  text-decoration: underline;
  cursor: pointer;
  font-size: 0.9rem;
}

/* Options de tri et vue */
.sort-and-view {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.sort-options {
  display: flex;
  align-items: center;
  gap: 10px;
}

.sort-options label {
  font-weight: bold;
  color: #555;
}

.sort-options select {
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #ccc;
  background-color: white;
  font-size: 0.9rem;
}

.view-toggle {
  display: flex;
  gap: 5px;
}

.view-toggle button {
  width: 36px;
  height: 36px;
  border-radius: 6px;
  color: #000000;
  background-color: #f5f5f5;
  border: 1px solid #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.view-toggle button.active {
  background-color: #3f51b5;
  color: white;
  border-color: #3f51b5;
}

/* Compteur de résultats */
.search-results-info {
  margin-bottom: 20px;
  font-size: 0.95rem;
  color: #666;
}

.results-count {
  font-weight: bold;
  color: #3f51b5;
  font-size: 1.1rem;
}

/* Liste des formations */
.formations-list {
  display: grid;
  gap: 20px;
  margin-bottom: 40px;
}

.card-view {
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}

.list-view {
  grid-template-columns: 1fr;
}

.formation-card {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
}

.formation-card:hover {
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
  transform: translateY(-3px);
}

.formation-header {
  display: flex;
  padding: 15px;
  gap: 15px;
  align-items: center;
  border-bottom: 1px solid #f0f0f0;
}

.entreprise-logo {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.formation-info {
  flex-grow: 1;
}

.formation-info h2 {
  margin: 0 0 5px 0;
  font-size: 1.1rem;
  color: #333;
}

.entreprise {
  color: #666;
  font-size: 0.9rem;
  margin: 0 0 8px 0;
}

.formation-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.badge {
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: bold;
}

.badge-duree {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.badge-niveau {
  background-color: #e3f2fd;
  color: #1565c0;
}

.badge-certification {
  background-color: #fff8e1;
  color: #ff8f00;
}

.badge-location {
  background-color: #f3e5f5;
  color: #7b1fa2;
}

.badge-status {
  margin-left: auto;
}

.status-interested {
  background-color: #e8eaf6;
  color: #3f51b5;
}

.status-contacted {
  background-color: #e0f7fa;
  color: #0097a7;
}

.status-application {
  background-color: #fff9c4;
  color: #fbc02d;
}

.status-registered {
  background-color: #e8f5e9;
  color: #388e3c;
}

.formation-actions-preview {
  display: flex;
  align-items: center;
}

.preview-button {
  background: transparent;
  border: none;
  cursor: pointer;
  color: #777;
  transition: all 0.3s ease;
}

.arrow-icon {
  transition: transform 0.3s ease;
}

.arrow-icon.rotated {
  transform: rotate(180deg);
}

/* Détails de formation */
.formation-details {
  padding: 20px;
  animation: fadeIn 0.3s ease;
}

.formation-description {
  color: #444;
  line-height: 1.5;
  margin-bottom: 20px;
}

.formation-competences h3, 
.entreprise-details h3,
.status-section h3,
.sessions h3 {
  font-size: 1rem;
  color: #3f51b5;
  margin: 20px 0 10px 0;
}

.competences-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.competence-item {
  background-color: #f5f5f5;
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 0.9rem;
  color: #444;
}

.entreprise-details {
  margin: 20px 0;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
  border-left: 4px solid #3f51b5;
}

.entreprise-contact {
  margin-top: 10px;
  font-size: 0.9rem;
}

.entreprise-contact p {
  margin: 5px 0;
}

/* Section de statut */
.status-section {
  margin: 20px 0;
  padding: 15px;
  background-color: #f5f7ff;
  border-radius: 8px;
}

.status-info {
  margin-top: 10px;
}

.status-badge {
  display: inline-block;
  padding: 5px 12px;
  border-radius: 20px;
  font-weight: bold;
  margin-bottom: 15px;
}

.status-timeline {
  display: flex;
  align-items: center;
  margin: 20px 0;
}

.timeline-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  position: relative;
  color: #bdbdbd;
}

.timeline-step.active {
  color: #3f51b5;
}

.step-icon {
  width: 40px;
  height: 40px;
  background-color: #f5f5f5;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
  border: 2px solid #e0e0e0;
  font-size: 1.1rem;
  z-index: 2;
}

.timeline-step.active .step-icon {
  background-color: #e8eaf6;
  border-color: #3f51b5;
  color: #3f51b5;
}

.step-label {
  font-size: 0.8rem;
  text-align: center;
}

.timeline-connector {
  height: 2px;
  background-color: #e0e0e0;
  flex-grow: 1;
  position: relative;
  z-index: 1;
}

.status-notes {
  margin: 15px 0;
  padding: 10px;
  background-color: #fff;
  border-radius: 6px;
  border-left: 3px solid #3f51b5;
}

.status-updated {
  font-size: 0.8rem;
  color: #777;
  text-align: right;
}

/* Boutons d'actions */
.formation-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 20px;
}

.formation-button {
  padding: 10px 15px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: all 0.3s ease;
  border: none;
}

.formation-button.interested {
  background-color: #e8eaf6;
  color: #3f51b5;
}

.formation-button.interested:hover {
  background-color: #c5cae9;
}

.formation-button.contact {
  background-color: #3f51b5;
  color: white;
}

.formation-button.contact:hover {
  background-color: #303f9f;
}

.formation-button.application {
  background-color: #ffecb3;
  color: #ff8f00;
}

.formation-button.application:hover {
  background-color: #ffe082;
}

.formation-button.registered {
  background-color: #c8e6c9;
  color: #388e3c;
}

.formation-button.registered:hover {
  background-color: #a5d6a7;
}

.formation-button.notes {
  background-color: #f5f5f5;
  color: #424242;
}

.formation-button.notes:hover {
  background-color: #e0e0e0;
}

.formation-button.reset {
  background-color: #ffebee;
  color: #c62828;
}

.formation-button.reset:hover {
  background-color: #ffcdd2;
}

/* Sessions */
.sessions-list {
  list-style: none;
  padding: 0;
  margin: 10px 0;
}

.session-item {
  padding: 10px 15px;
  background-color: #f5f5f5;
  border-radius: 6px;
  margin-bottom: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.session-date {
  font-weight: bold;
  color: #333;
}

.session-places {
  font-size: 0.9rem;
  color: #3f51b5;
}

/* Message "pas de formations" */
.no-formations {
  padding: 40px;
  text-align: center;
  background-color: #f9f9f9;
  border-radius: 10px;
  margin: 20px 0;
}

.empty-icon {
  font-size: 3rem;
  color: #bdbdbd;
  margin-bottom: 20px;
}

/* Modals */
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
}

.modal-content {
  background-color: white;
  border-radius: 10px;
  width: 90%;
  max-width: 500px;
  padding: 25px;
  position: relative;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
}

.close-modal {
  position: absolute;
  top: 10px;
  right: 15px;
  background: transparent;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #000000;
}

.form-group input, 
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}

.form-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.submit-button {
  padding: 10px 20px;
  background-color: #3f51b5;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
}

.submit-button:hover {
  background-color: #303f9f;
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideDown {
  from { transform: translateY(-10px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.formation-item-enter-active, .formation-item-leave-active {
  transition: all 0.3s ease;
}

.formation-item-enter-from, .formation-item-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

/* Media Queries pour Responsive */
@media (max-width: 768px) {
  .category-selector {
    flex-direction: column;
    gap: 10px;
  }
  
  .filters-grid {
    grid-template-columns: 1fr;
  }
  
  .sort-and-view {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .formation-header {
    flex-wrap: wrap;
  }
  
  .formation-badges {
    margin-top: 10px;
  }
  
  .status-timeline {
    flex-wrap: wrap;
    gap: 15px;
  }
  
  .timeline-connector {
    display: none;
  }
  
  .formation-actions {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  h1 {
    font-size: 1.8rem;
  }
  
  .subtitle {
    font-size: 1rem;
  }
  
  .category-button {
    font-size: 0.9rem;
    padding: 12px 20px;
  }
  
  .card-view {
    grid-template-columns: 1fr;
  }
}
</style>