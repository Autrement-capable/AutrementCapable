<template>
  <!-- Inclusion de Font Awesome pour les icônes -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <div class="formations-page">
    <header>
      <h1>Découvrez des formations adaptées à vos besoins</h1>
      <p class="subtitle">Entrez directement en contact avec les organismes de formation</p>
    </header>

    <section class="category-selector">
      <button 
        class="category-button"
        :class="{ active: selectedCategory === 'recommandees' }"
        @click="selectedCategory = 'recommandees'"
      >
        <i class="fas fa-star category-icon"></i>
        Recommandées pour moi
      </button>
      <button 
        class="category-button"
        :class="{ active: selectedCategory === 'toutes' }"
        @click="selectedCategory = 'toutes'"
      >
        <i class="fas fa-list category-icon"></i>
        Toutes les formations
      </button>
    </section>

    <section class="formations-list">
      <transition-group name="formation-item">
        <div 
          v-for="formation in filteredFormations" 
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
              </div>
            </div>
            <div class="formation-actions-preview">
              <button class="preview-button">
                <i class="fas fa-chevron-down arrow-icon"></i>
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
            
            <div class="formation-actions">
              <button class="formation-button contact" @click.stop="contacterEntreprise(formation)">
                <i class="fas fa-envelope"></i> Contacter directement
              </button>
              <button class="formation-button info" @click.stop="demanderInfos(formation)">
                <i class="fas fa-info-circle"></i> Demander plus d'informations
              </button>
              <button class="formation-button inscrire" @click.stop="inscrireFormation(formation)">
                <i class="fas fa-check-circle"></i> S'inscrire
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
      <p>Aucune formation disponible dans cette catégorie</p>
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
  </div>
</template>

<script>
export default {
  name: 'FormationsPage',
  data() {
    return {
      selectedCategory: 'recommandees',
      expandedFormations: [],
      showContactModal: false,
      selectedFormation: null,
      contactForm: {
        nom: '',
        email: '',
        telephone: '',
        message: ''
      },
      formations: [
        {
          id: 1,
          titre: "Initiation à l'informatique",
          entreprise: "InfoTech Formation",
          icone: "fa-laptop",
          couleur: "#4285F4",
          description: "Cette formation vous permet d'acquérir les bases de l'informatique dans un environnement adapté et à votre rythme. Notre approche pédagogique est spécialement conçue pour les personnes en situation de handicap neurologique.",
          duree: "10h",
          niveau: "Débutant",
          certification: true,
          localisation: "Paris + À distance",
          recommandee: true,
          entrepriseDescription: "InfoTech Formation est spécialisée dans la formation numérique inclusive. Nos formateurs sont formés aux besoins spécifiques des personnes en situation de handicap.",
          contact: "contact@infotech-formation.fr - 01 23 45 67 89",
          adresse: "15 rue des Lilas, 75020 Paris",
          accessibility: "Locaux entièrement accessibles, supports adaptés, rythme personnalisé",
          prochaineSessions: [
            { date: "15 avril 2025", placesDisponibles: 5 },
            { date: "2 mai 2025", placesDisponibles: 8 }
          ],
          competences: [
            "Utiliser un ordinateur",
            "Naviguer sur internet",
            "Utiliser une messagerie électronique",
            "Créer des documents simples"
          ]
        },
        {
          id: 2,
          titre: "Communication professionnelle",
          entreprise: "CommPro",
          icone: "fa-comments",
          couleur: "#ea4335",
          description: "Développez vos compétences en communication pour vous sentir plus à l'aise dans un environnement professionnel. Formation adaptée avec une pédagogie bienveillante et des exercices pratiques.",
          duree: "15h",
          niveau: "Intermédiaire",
          certification: false,
          localisation: "Lyon",
          recommandee: true,
          entrepriseDescription: "CommPro est un centre de formation spécialisé dans le développement des compétences relationnelles en milieu professionnel. Notre équipe est sensibilisée à l'inclusion de tous les profils.",
          contact: "formation@commpro.fr - 04 56 78 90 12",
          adresse: "8 avenue de la République, 69002 Lyon",
          accessibility: "Supports visuels adaptés, possibilité d'être accompagné",
          prochaineSessions: [
            { date: "22 avril 2025", placesDisponibles: 3 }
          ],
          competences: [
            "Communication verbale claire",
            "Écoute active",
            "Rédaction d'emails professionnels",
            "Prise de parole en groupe"
          ]
        },
        {
          id: 3,
          titre: "Gestion du stress au travail",
          entreprise: "BienÊtre Pro",
          icone: "fa-heart",
          couleur: "#34a853",
          description: "Découvrez des techniques pour gérer le stress et l'anxiété dans votre environnement professionnel. Approche personnalisée selon vos besoins spécifiques.",
          duree: "8h",
          niveau: "Tous niveaux",
          certification: false,
          localisation: "À distance",
          recommandee: true,
          entrepriseDescription: "BienÊtre Pro propose des formations centrées sur le bien-être et l'épanouissement professionnel. Nos méthodes sont inclusives et adaptées à tous les profils.",
          contact: "contact@bienetrepro.fr - 07 12 34 56 78",
          adresse: "Formation en ligne",
          accessibility: "Formations à distance avec supports adaptés et accompagnement individuel",
          prochaineSessions: [
            { date: "En continu", placesDisponibles: 12 }
          ],
          competences: [
            "Identifier les sources de stress",
            "Techniques de respiration",
            "Organisation du travail",
            "Établir des limites saines"
          ]
        },
        {
          id: 4,
          titre: "Excel pour débutants",
          entreprise: "BureauPro",
          icone: "fa-file-excel",
          couleur: "#fbbc05",
          description: "Maîtrisez les fonctionnalités de base d'Excel pour améliorer votre productivité. Formation avec un rythme adapté et des exercices progressifs.",
          duree: "12h",
          niveau: "Débutant",
          certification: true,
          localisation: "Marseille + À distance",
          recommandee: false,
          entrepriseDescription: "BureauPro est un organisme de formation spécialisé dans les outils bureautiques. Notre pédagogie s'adapte aux besoins de chacun avec un suivi personnalisé.",
          contact: "info@bureaupro.fr - 04 91 23 45 67",
          adresse: "25 boulevard National, 13003 Marseille",
          accessibility: "Supports adaptés, possibilité de ralentir le rythme, aide individuelle",
          prochaineSessions: [
            { date: "18 avril 2025", placesDisponibles: 7 },
            { date: "10 mai 2025", placesDisponibles: 9 }
          ],
          competences: [
            "Création de tableaux",
            "Formules de base",
            "Mise en forme conditionnelle",
            "Création de graphiques simples"
          ]
        },
        {
          id: 5,
          titre: "Travailler en équipe",
          entreprise: "TeamWork",
          icone: "fa-users",
          couleur: "#7e57c2",
          description: "Développez vos compétences pour mieux collaborer et communiquer en équipe. Méthodes adaptées aux différents profils cognitifs.",
          duree: "20h",
          niveau: "Intermédiaire",
          certification: true,
          localisation: "Lille",
          recommandee: false,
          entrepriseDescription: "TeamWork est spécialisé dans le développement des compétences collaboratives et l'inclusion en entreprise. Nos formations sont conçues pour valoriser la neurodiversité.",
          contact: "formations@teamwork.fr - 03 20 45 67 89",
          adresse: "12 rue des Ponts, 59000 Lille",
          accessibility: "Locaux accessibles, méthodologie adaptée aux différents profils",
          prochaineSessions: [
            { date: "5 mai 2025", placesDisponibles: 4 }
          ],
          competences: [
            "Communication en groupe",
            "Résolution de conflits",
            "Gestion des différences",
            "Partage des tâches"
          ]
        }
      ]
    };
  },
  computed: {
    filteredFormations() {
      if (this.selectedCategory === 'recommandees') {
        return this.formations.filter(formation => formation.recommandee);
      } else {
        return this.formations;
      }
    }
  },
  methods: {
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
    },
    demanderInfos(formation) {
      this.selectedFormation = formation;
      this.contactForm.message = `Bonjour, pourriez-vous m'envoyer une documentation détaillée sur votre formation "${formation.titre}" ? Merci.`;
      this.showContactModal = true;
    },
    inscrireFormation(formation) {
      this.selectedFormation = formation;
      this.contactForm.message = `Bonjour, je souhaite m'inscrire à votre formation "${formation.titre}". Pourriez-vous m'indiquer la procédure à suivre ? Merci.`;
      this.showContactModal = true;
    },
    closeModal() {
      this.showContactModal = false;
    },
    envoyerMessage() {
      // Ici, vous implémenteriez la logique pour envoyer le message
      // Pour l'instant, nous simulons juste l'envoi
      alert(`Message envoyé à ${this.selectedFormation.entreprise} !`);
      this.showContactModal = false;
      
      // Réinitialisation du formulaire
      this.contactForm = {
        nom: '',
        email: '',
        telephone: '',
        message: ''
      };
    }
  }
};
</script>

<style scoped>
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

.category-button {
  color: #333; /* Assure que le texte est toujours foncé quand inactif */
}

.category-icon {
  width: 24px;
  height: 24px;
}

.formations-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.formation-card {
  background-color: white;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.formation-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.formation-header {
  display: flex;
  padding: 20px;
  gap: 20px;
  align-items: center;
}

.entreprise-logo {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
}

.formation-info {
  flex: 1;
}

h2 {
  font-size: 1.4rem;
  color: #333;
  margin: 0 0 5px 0;
}

.entreprise {
  font-size: 1rem;
  color: #666;
  margin: 0 0 10px 0;
}

.formation-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.badge {
  padding: 5px 10px;
  border-radius: 50px;
  font-size: 0.8rem;
  font-weight: bold;
}

.badge-duree {
  background-color: #e3f2fd;
  color: #1976d2;
}

.badge-niveau {
  background-color: #e8f5e9;
  color: #388e3c;
}

.badge-certification {
  background-color: #fff8e1;
  color: #ff8f00;
}

.badge-location {
  background-color: #f3e5f5;
  color: #7b1fa2;
}

.formation-actions-preview {
  display: flex;
  align-items: center;
}

.preview-button {
  background: none;
  border: none;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.preview-button:hover {
  transform: scale(1.2);
}

.arrow-icon {
  font-size: 20px;
  color: #666;
}

.formation-details {
  padding: 0 20px 20px 20px;
  border-top: 1px solid #e0e0e0;
  animation: fadeIn 0.3s ease;
}

.formation-description {
  font-size: 1rem;
  color: #666;
  line-height: 1.6;
  margin-bottom: 20px;
}

h3 {
  font-size: 1.1rem;
  color: #333;
  margin: 20px 0 10px 0;
}

.competences-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.competence-item {
  background-color: #f5f5f5;
  padding: 8px 15px;
  border-radius: 50px;
  font-size: 0.9rem;
  color: #555;
}

.entreprise-details {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 10px;
  margin: 20px 0;
}

.entreprise-contact {
  margin-top: 10px;
}

.entreprise-contact p {
  margin: 5px 0;
  font-size: 0.9rem;
}

.formation-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-top: 20px;
}

.formation-button {
  padding: 12px 20px;
  border: none;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.formation-button.contact {
  background-color: #3f51b5;
  color: white;
}

.formation-button.contact:hover {
  background-color: #303f9f;
}

.formation-button.info {
  background-color: #f5f5f5;
  color: #555;
}

.formation-button.info:hover {
  background-color: #e0e0e0;
}

.formation-button.inscrire {
  background-color: #4caf50;
  color: white;
}

.formation-button.inscrire:hover {
  background-color: #388e3c;
}

.sessions {
  margin-top: 20px;
}

.sessions-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.session-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 15px;
  border-bottom: 1px solid #e0e0e0;
  font-size: 0.9rem;
}

.session-item:last-child {
  border-bottom: none;
}

.session-places {
  color: #4caf50;
  font-weight: bold;
}

.no-formations {
  text-align: center;
  padding: 50px 0;
  color: #666;
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 20px;
  opacity: 0.5;
  color: #999;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 15px;
  width: 90%;
  max-width: 500px;
  padding: 30px;
  position: relative;
  max-height: 90vh;
  overflow-y: auto;
}

.close-modal {
  position: absolute;
  top: 15px;
  right: 20px;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #555;
}

input, textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.3s ease;
}

input:focus, textarea:focus {
  border-color: #3f51b5;
  outline: none;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.submit-button {
  padding: 12px 30px;
  background-color: #3f51b5;
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #303f9f;
}

.formation-item-enter-active, .formation-item-leave-active {
  transition: all 0.5s ease;
}

.formation-item-enter-from, .formation-item-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Styles pour améliorer l'accessibilité */
:focus-visible {
  outline: 3px solid #3f51b5;
  outline-offset: 2px;
}

@media (max-width: 768px) {
  .category-selector {
    flex-direction: column;
    align-items: center;
  }
  
  .formation-header {
    flex-direction: column;
    text-align: center;
  }
  
  .formation-info {
    width: 100%;
  }
  
  .formation-badges {
    justify-content: center;
  }
  
  .formation-actions {
    flex-direction: column;
  }
  
  .formation-button {
    width: 100%;
  }
}
</style>