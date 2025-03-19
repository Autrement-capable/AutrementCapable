<template>
  <div class="results-container">
    <h1>Vos résultats</h1>

    <div v-if="!hasCompletedScenarios" class="incomplete-message">
      <p>Vous n'avez pas encore complété les scénarios.</p>
      <router-link :to="{ name: 'ScenarioPage', params: { id: 1 } }" class="start-button">
        Commencer les scénarios
      </router-link>
    </div>

    <div v-else class="results-content">
      <div class="results-summary">
        <h2>Vos compétences</h2>
        <p>Voici les compétences que vous avez développées à travers les différents scénarios :</p>
      </div>

      <div class="skills-categories">
        <!-- Communication -->
        <div class="skills-category">
          <h3>Communication</h3>
          <div class="skills-list">
            <div v-for="(value, skill) in communicationSkills" :key="skill" class="skill-item">
              <div class="skill-header">
                <span class="skill-name">{{ getSkillDisplayName(skill) }}</span>
                <span class="skill-score">{{ value }} pts</span>
              </div>
              <div class="skill-bar-container">
                <div class="skill-bar" :style="{ width: getBarWidth(value) + '%' }"></div>
              </div>
              <div class="skill-level">{{ getSkillLevel(value) }}</div>
            </div>
          </div>
        </div>

        <!-- Interpersonnel -->
        <div class="skills-category">
          <h3>Compétences interpersonnelles</h3>
          <div class="skills-list">
            <div v-for="(value, skill) in interpersonnelSkills" :key="skill" class="skill-item">
              <div class="skill-header">
                <span class="skill-name">{{ getSkillDisplayName(skill) }}</span>
                <span class="skill-score">{{ value }} pts</span>
              </div>
              <div class="skill-bar-container">
                <div class="skill-bar" :style="{ width: getBarWidth(value) + '%' }"></div>
              </div>
              <div class="skill-level">{{ getSkillLevel(value) }}</div>
            </div>
          </div>
        </div>

        <!-- Adaptation -->
        <div class="skills-category">
          <h3>Adaptation</h3>
          <div class="skills-list">
            <div v-for="(value, skill) in adaptationSkills" :key="skill" class="skill-item">
              <div class="skill-header">
                <span class="skill-name">{{ getSkillDisplayName(skill) }}</span>
                <span class="skill-score">{{ value }} pts</span>
              </div>
              <div class="skill-bar-container">
                <div class="skill-bar" :style="{ width: getBarWidth(value) + '%' }"></div>
              </div>
              <div class="skill-level">{{ getSkillLevel(value) }}</div>
            </div>
          </div>
        </div>

        <!-- Professionnelles -->
        <div class="skills-category">
          <h3>Compétences professionnelles</h3>
          <div class="skills-list">
            <div v-for="(value, skill) in professionnellesSkills" :key="skill" class="skill-item">
              <div class="skill-header">
                <span class="skill-name">{{ getSkillDisplayName(skill) }}</span>
                <span class="skill-score">{{ value }} pts</span>
              </div>
              <div class="skill-bar-container">
                <div class="skill-bar" :style="{ width: getBarWidth(value) + '%' }"></div>
              </div>
              <div class="skill-level">{{ getSkillLevel(value) }}</div>
            </div>
          </div>
        </div>

        <!-- Personnelles -->
        <div class="skills-category">
          <h3>Qualités personnelles</h3>
          <div class="skills-list">
            <div v-for="(value, skill) in personnellesSkills" :key="skill" class="skill-item">
              <div class="skill-header">
                <span class="skill-name">{{ getSkillDisplayName(skill) }}</span>
                <span class="skill-score">{{ value }} pts</span>
              </div>
              <div class="skill-bar-container">
                <div class="skill-bar" :style="{ width: getBarWidth(value) + '%' }"></div>
              </div>
              <div class="skill-level">{{ getSkillLevel(value) }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="top-skills">
        <h3>Vos points forts</h3>
        <div class="top-skills-list">
          <div v-for="(skill, index) in topSkills" :key="index" class="top-skill-item">
            <div class="top-skill-icon">🌟</div>
            <div class="top-skill-info">
              <div class="top-skill-name">{{ getSkillDisplayName(skill.name) }}</div>
              <div class="top-skill-score">{{ skill.value }} points - {{ getSkillLevel(skill.value) }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="action-buttons">
        <button class="reset-button" @click="resetSkills">Réinitialiser les résultats</button>
        <router-link :to="{ name: 'ScenarioPage', params: { id: 1 } }" class="restart-button">
          Recommencer les scénarios
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
// Importer les fonctions depuis skills-list.js
import { getSkillLevel } from '@/data/skills-list';

export default {
  name: 'ResultsPage',
  data() {
    return {
      skills: {},
      hasCompletedScenarios: false,
      // Structure des catégories de compétences pour le filtrage
      skillCategories: {
        communication: ['assertivite', 'communication', 'diplomatie', 'ecouteActive', 'negociation', 'franchise'],
        interpersonnel: ['empathie', 'espritEquipe', 'soutien', 'mediation', 'inclusion', 'coaching'],
        adaptation: ['adaptabilite', 'initiative', 'reflexionRapide', 'gestionStress', 'creativite'],
        professionnelles: ['responsabilite', 'anticipation', 'observation', 'apprentissage', 'gestionTemps', 'decision'],
        personnelles: ['confianceEnSoi', 'autonomie', 'patience', 'curiosite', 'pragmatisme', 'assurance']
      },
      // Noms d'affichage des compétences
      skillDisplayNames: {
        assertivite: 'Assertivité',
        communication: 'Communication',
        diplomatie: 'Diplomatie',
        ecouteActive: 'Écoute active',
        negociation: 'Négociation',
        franchise: 'Franchise',
        empathie: 'Empathie',
        espritEquipe: 'Esprit d\'équipe',
        soutien: 'Soutien',
        mediation: 'Médiation',
        inclusion: 'Inclusion',
        coaching: 'Coaching',
        adaptabilite: 'Adaptabilité',
        initiative: 'Initiative',
        reflexionRapide: 'Réflexion rapide',
        gestionStress: 'Gestion du stress',
        creativite: 'Créativité',
        responsabilite: 'Responsabilité',
        anticipation: 'Anticipation',
        observation: 'Observation',
        apprentissage: 'Apprentissage',
        gestionTemps: 'Gestion du temps',
        decision: 'Prise de décision',
        confianceEnSoi: 'Confiance en soi',
        autonomie: 'Autonomie',
        patience: 'Patience',
        curiosite: 'Curiosité',
        pragmatisme: 'Pragmatisme',
        assurance: 'Assurance'
      }
    };
  },
  computed: {
    // Filtrer les compétences par catégorie
    communicationSkills() {
      return this.filterSkillsByCategory('communication');
    },
    interpersonnelSkills() {
      return this.filterSkillsByCategory('interpersonnel');
    },
    adaptationSkills() {
      return this.filterSkillsByCategory('adaptation');
    },
    professionnellesSkills() {
      return this.filterSkillsByCategory('professionnelles');
    },
    personnellesSkills() {
      return this.filterSkillsByCategory('personnelles');
    },
    // Top 5 des compétences par score
    topSkills() {
      const skillsArray = Object.entries(this.skills)
        .map(([name, value]) => ({ name, value }))
        .sort((a, b) => b.value - a.value)
        .slice(0, 9);
      
      return skillsArray;
    }
  },
  created() {
    this.loadSkills();
  },
  methods: {
    loadSkills() {
      const savedSkills = localStorage.getItem('userSoftSkills');
      if (savedSkills) {
        this.skills = JSON.parse(savedSkills);
        this.hasCompletedScenarios = Object.keys(this.skills).length > 0;
      }
    },
    resetSkills() {
      if (confirm("Êtes-vous sûr de vouloir réinitialiser tous vos résultats ?")) {
        localStorage.removeItem('userSoftSkills');
        this.skills = {};
        this.hasCompletedScenarios = false;
      }
    },
    filterSkillsByCategory(category) {
      const result = {};
      const categorySkills = this.skillCategories[category];
      
      if (categorySkills) {
        categorySkills.forEach(skill => {
          if (this.skills[skill] !== undefined) {
            result[skill] = this.skills[skill];
          }
        });
      }
      
      return result;
    },
    getSkillDisplayName(skill) {
      return this.skillDisplayNames[skill] || skill;
    },
    getBarWidth(value) {
      // Maximum est 20 points (pour la visualisation)
      const maxValue = 20;
      return Math.min(value / maxValue * 100, 100);
    },
    getSkillLevel(score) {
      // Utiliser la fonction importée
      return getSkillLevel(score);
    }
  }
};
</script>

<style scoped>
.results-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  color: #343a40;
  margin-bottom: 30px;
  font-size: 2.5rem;
}

.incomplete-message {
  text-align: center;
  padding: 30px;
  background-color: #e9ecef;
  border-radius: 8px;
  margin-bottom: 20px;
}

.incomplete-message p {
  font-size: 1.2rem;
  margin-bottom: 20px;
  color: #495057;
}

.start-button {
  display: inline-block;
  padding: 12px 24px;
  background-color: #28a745;
  color: white;
  border-radius: 6px;
  text-decoration: none;
  font-weight: bold;
  transition: background-color 0.3s;
}

.start-button:hover {
  background-color: #218838;
}

.results-summary {
  margin-bottom: 30px;
  padding: 15px;
  background-color: #e9ecef;
  border-radius: 8px;
  text-align: center;
}

.results-summary h2 {
  color: #343a40;
  margin-bottom: 10px;
}

.results-summary p {
  color: #6c757d;
}

.skills-categories {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.skills-category {
  background-color: white;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.skills-category h3 {
  color: #495057;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #dee2e6;
  font-size: 1.2rem;
}

.skills-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.skill-item {
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 6px;
}

.skill-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.skill-name {
  font-weight: bold;
  color: #495057;
}

.skill-score {
  color: #6c757d;
}

.skill-bar-container {
  height: 10px;
  background-color: #e9ecef;
  border-radius: 5px;
  overflow: hidden;
  margin-bottom: 5px;
}

.skill-bar {
  height: 100%;
  background-color: #007bff;
  border-radius: 5px;
}

.skill-level {
  text-align: right;
  font-size: 0.8rem;
  color: #6c757d;
}

.top-skills {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.top-skills h3 {
  color: #495057;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #dee2e6;
}

.top-skills-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
}

.top-skill-item {
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 6px;
  gap: 10px;
}

.top-skill-icon {
  font-size: 1.5rem;
}

.top-skill-info {
  flex-grow: 1;
}

.top-skill-name {
  font-weight: bold;
  color: #495057;
}

.top-skill-score {
  color: #6c757d;
  font-size: 0.9rem;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 20px;
}

.reset-button {
  padding: 10px 20px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

.reset-button:hover {
  background-color: #c82333;
}

.restart-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border-radius: 6px;
  text-decoration: none;
  font-weight: bold;
  transition: background-color 0.3s;
}

.restart-button:hover {
  background-color: #0069d9;
}

@media (max-width: 768px) {
  .skills-categories {
    grid-template-columns: 1fr;
  }
  
  .top-skills-list {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
  }
}
</style>