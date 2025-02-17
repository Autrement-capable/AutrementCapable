<template>
    <div v-if="scenario" class="scenario-container">
        <!-- 🎯 TITRE -->
        <h1>{{ scenario.titre }}</h1>

        <!-- 📜 CONTEXTE : Toujours Visible -->
        <div class="intro-section">
            <p class="intro">{{ scenario.contexteIntro }}</p>
            <button v-if="phase === 'intro'" class="start-button" @click="startDialogue">Commencer</button>
        </div>

        <!-- 💬 DIALOGUES Progressifs -->
        <div v-if="phase !== 'intro'" class="conversation">
            <div v-for="(dialogue, index) in visibleDialogues" :key="index" class="dialogue"
                :class="getDialogueClass(dialogue.personnage)">
                <img v-if="dialogue.avatar" :src="getAvatarPath(dialogue.avatar)" :alt="dialogue.personnage"
                    class="avatar" />
                <div class="bubble">
                    <p><strong>{{ dialogue.personnage }} :</strong> {{ dialogue.texte }}</p>
                </div>
            </div>

            <!-- Bouton suivant pour passer au dialogue suivant -->
            <button v-if="dialogueIndex < scenario.contexte.length" class="next-button" @click="showNextDialogue">
                ▶️ Suivant
            </button>

            <!-- Affiche directement les choix en dessous des dialogues -->
            <div v-if="phase === 'choix'" class="button-container">
                <h2 class="question">{{ scenario.question }}</h2>
                <button v-for="(reponse, index) in scenario.reponses" :key="index" @click="choisirReponse(reponse)">
                    {{ reponse.texte }}
                </button>
            </div>
        </div>

        <!-- 📝 FEEDBACK Final -->
        <div v-if="feedback" class="feedback">
            <p>{{ feedback }}</p>
        </div>
    </div>

    <p v-else>Chargement du scénario...</p>
</template>




<script>
import { scenarios } from '@/data/data.js';
const avatars = require.context('@/assets/avatars/', false, /\.svg$/);

export default {
    name: "ScenarioPage",
    props: {
        id: String,
    },
    data() {
        return {
            scenario: null,
            feedback: null,
            phase: 'intro',
            dialogueIndex: 0,
        };
    },
    computed: {
        visibleDialogues() {
            return this.scenario ? this.scenario.contexte.slice(0, this.dialogueIndex + 1) : [];
        }
    },
    created() {
        this.loadScenario();
    },
    watch: {
        $route(to, from) {
            if (to.params.id !== from.params.id) {
                this.loadScenario();
                this.phase = 'intro';
                this.feedback = null;
                this.dialogueIndex = 0;
            }
        }
    },
    methods: {
        loadScenario() {
            const scenarioId = parseInt(this.id);
            this.scenario = scenarios.find(s => s.id === scenarioId);
            if (!this.scenario) {
                console.error("Scénario non trouvé !");
            } else {
                // 🗣️ Lit automatiquement le contexte dès son affichage
                this.readAloud(this.scenario.contexteIntro);
            }
        },
        startDialogue() {
            this.phase = 'dialogue';
            this.dialogueIndex = 0;
            // 🗣️ Lit automatiquement le premier dialogue
            if (this.scenario.contexte.length > 0) {
                this.readAloud(this.scenario.contexte[0].texte);
            }
        },
        showNextDialogue() {
            if (this.dialogueIndex < this.scenario.contexte.length - 1) {
                this.dialogueIndex++;
                // 🗣️ Lit automatiquement chaque réplique au fur et à mesure
                this.readAloud(this.scenario.contexte[this.dialogueIndex].texte);
            } else {
                this.phase = 'choix';
                // 🗣️ Lit automatiquement la question
                this.readAloud(this.scenario.question);
            }
        },
        choisirReponse(reponse) {
            this.feedback = `Vous avez choisi : "${reponse.texte}" ✅`;
            // 🗣️ Lit le choix sélectionné
            this.readAloud(`Vous avez choisi : ${reponse.texte}`);
            this.enregistrerSoftSkills(reponse.skills);

            setTimeout(() => {
                const nextId = parseInt(this.id) + 1;
                if (scenarios.some(s => s.id === nextId)) {
                    this.$router.push({ name: "ScenarioPage", params: { id: nextId } });
                } else {
                    this.feedback = "✅ Vous avez complété tous les scénarios !";
                    this.readAloud(this.feedback);
                }
            }, 5000);
        },
        // 🗣️ Fonction de Synthèse Vocale
        readAloud(text) {
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'fr-FR';
                utterance.rate = 1;
                utterance.pitch = 1;
                window.speechSynthesis.speak(utterance);
            } else {
                console.warn("La synthèse vocale n'est pas supportée par ce navigateur.");
            }
        },
        enregistrerSoftSkills(skills) {
            const savedSkills = JSON.parse(localStorage.getItem('userSoftSkills')) || {};
            for (const [skill, points] of Object.entries(skills)) {
                savedSkills[skill] = (savedSkills[skill] || 0) + points;
            }
            localStorage.setItem('userSoftSkills', JSON.stringify(savedSkills));
            console.log("Soft skills enregistrés :", savedSkills);
        },
        getAvatarPath(filename) {
            const path = `./${filename}`;
            if (avatars.keys().includes(path)) {
                return avatars(path);
            } else {
                return avatars('./toi.svg');
            }
        },
        getDialogueClass(personnage) {
            return personnage === "Toi" ? "dialogue-right" : "dialogue-left";
        }
    }
};
</script>


<style scoped>
.scenario-container {
    font-family: Arial, sans-serif;
    margin: 20px auto;
    padding: 20px;
    max-width: 750px;
    background-color: #f9f9f9;
    border-radius: 12px;
    border: 2px solid #ccc;
    text-align: center;
}

/* 🎨 Titre */
h1 {
    font-size: 2rem;
    font-weight: bold;
    color: #2c3e50;
    text-align: center;
    margin-bottom: 15px;
}

/* 📜 Contexte Introductif */
.intro {
    font-size: 1.2rem;
    font-style: italic;
    text-align: justify;
    background-color: #f0f8ff;
    border-left: 5px solid #007bff;
    padding: 12px 20px;
    margin-bottom: 20px;
    border-radius: 8px;
}

/* 🎯 Section Intro */
.intro-section {
    text-align: center;
    padding: 20px;
}

.start-button {
    padding: 12px 24px;
    font-size: 1.2rem;
    font-weight: bold;
    color: white;
    background-color: #28a745;
    border-radius: 10px;
    transition: background-color 0.3s;
    display: inline-block;
    width: auto;
    max-width: 250px;
    height: auto;
    text-align: center;
    margin: 10px auto;
    line-height: normal;
}

.start-button:hover {
    background-color: #218838;
}


/* 💬 Conversations */
.conversation {
    padding: 15px;
    background-color: #f0f8ff;
    border-radius: 12px;
    margin-bottom: 20px;
}

/* Bouton Suivant */
.next-button {
    margin-top: 15px;
    padding: 10px 20px;
    font-size: 1rem;
    font-weight: bold;
    color: white;
    background-color: #007bff;
    border-radius: 10px;
}

.next-button:hover {
    background-color: #0056b3;
}

/* 🗨️ Dialogue */
.dialogue {
    display: flex;
    align-items: flex-start;
    margin-bottom: 12px;
}

.dialogue-right {
    flex-direction: row-reverse;
    text-align: right;
}

/* Avatar */
.avatar {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    margin: 0 10px;
    border: 2px solid #ddd;
    background-color: white;
}

/* Bulle de Dialogue */
.bubble {
    padding: 10px;
    background-color: #fff;
    border-radius: 15px;
    border: 1px solid #ccc;
    font-size: 1rem;
    max-width: 70%;
}

.dialogue-left .bubble {
    background-color: #d0ebff;
}

.dialogue-right .bubble {
    background-color: #d4edda;
}

/* ✅ Boutons de Choix */
.button-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    margin-top: 15px;
    width: 100%;
    max-width: 350px;
    margin-left: auto;
    margin-right: auto;
}

.button-container button {
    padding: 10px 15px;
    font-size: 1rem;
    font-weight: bold;
    border-radius: 8px;
    background-color: #4CAF50;
    color: white;
    border: none;
    width: 100%;
    box-sizing: border-box;
    transition: background-color 0.3s;
}

.button-container button:hover {
    background-color: #45A049;
}


/* 📝 Feedback Final */
.feedback {
    margin-top: 20px;
    padding: 10px;
    font-size: 1.2rem;
    font-weight: bold;
    background-color: #e1f5fe;
    border-radius: 6px;
    text-align: center;
}
</style>