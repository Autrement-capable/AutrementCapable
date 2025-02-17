<template>
    <div v-if="scenario" class="scenario-container">
        <h1>{{ scenario.titre }}</h1>
        <p class="intro">{{ scenario.contexteIntro }}</p>

        <div class="conversation">
            <div v-for="(dialogue, index) in scenario.contexte" :key="index" class="dialogue">
                <p><strong>{{ dialogue.personnage }} :</strong> {{ dialogue.texte }}</p>
            </div>
        </div>

        <h2 class="question">{{ scenario.question }}</h2>
        <div class="button-container">
            <button v-for="(reponse, index) in scenario.reponses" :key="index" @click="choisirReponse(reponse)">
                {{ reponse.texte }}
            </button>
        </div>

        <div v-if="feedback" class="feedback">
            <p>{{ feedback }}</p>
        </div>
    </div>
    <p v-else>Chargement du scénario...</p>
</template>

<script>
import { scenarios } from '@/data/data.js';

export default {
    name: "ScenarioPage",
    props: {
        id: String, // Récupère l'ID depuis l'URL
    },
    data() {
        return {
            scenario: null,
            feedback: null,
        };
    },
    created() {
        // Charge le scénario selon l'ID
        this.loadScenario();
    },
    watch: {
        // Recharge le scénario si l'ID change
        id() {
            this.loadScenario();
        }
    },
    methods: {
        loadScenario() {
            const scenarioId = parseInt(this.id);
            this.scenario = scenarios.find(s => s.id === scenarioId);
            if (!this.scenario) {
                console.error("Scénario non trouvé !");
            }
        },
        choisirReponse(reponse) {
            this.feedback = `Vous avez choisi : "${reponse.texte}" ✅`;

            // Enregistre les compétences dans localStorage
            this.enregistrerSoftSkills(reponse.skills);

            // Passe au scénario suivant
            setTimeout(() => {
                const nextId = parseInt(this.id) + 1;
                const nextScenario = scenarios.find(s => s.id === nextId);
                if (nextScenario) {
                    this.$router.push({ name: "ScenarioPage", params: { id: nextId } });
                } else {
                    this.feedback = "✅ Vous avez complété tous les scénarios !";
                }
            }, 1500);
        },
        enregistrerSoftSkills(skills) {
            const savedSkills = JSON.parse(localStorage.getItem('userSoftSkills')) || {};
            for (const [skill, points] of Object.entries(skills)) {
                savedSkills[skill] = (savedSkills[skill] || 0) + points;
            }
            localStorage.setItem('userSoftSkills', JSON.stringify(savedSkills));
            console.log("Soft skills enregistrés :", savedSkills);
        }
    }
};
</script>

<style scoped>
.scenario-container {
  font-family: Arial, sans-serif;
  margin: 20px auto;
  text-align: center;
  padding: 20px;
  max-width: 750px;
  background-color: #f9f9f9;
  border-radius: 12px;
  border: 2px solid #ccc;
}

.conversation {
  text-align: left;
  padding: 10px;
  margin-bottom: 20px;
  background-color: #eef;
  border-radius: 8px;
}

.dialogue {
  padding: 5px;
  font-size: 1rem;
}

.button-container button {
  font-size: 1rem;
  padding: 10px 20px;
  margin: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.button-container button:hover {
  background-color: #0056b3;
}

.feedback {
  margin-top: 20px;
  padding: 10px;
  font-size: 1.2rem;
  font-weight: bold;
  color: #2c3e50;
  background-color: #e1f5fe;
  border-radius: 6px;
}
</style>
