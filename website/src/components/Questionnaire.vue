<template>
  <div class="questionnaire" aria-label="Questionnaire page">
    <h1 class="title">Bonjour !</h1>
    <!-- Affiche l'avatar sélectionné si disponible, sinon l'image par défaut -->
    <img :src="selectedAvatarUrl || require('../assets/jeunefemme.png')" alt="Avatar" :class="imageClass" />

    <div v-if="currentQuestionIndex < questions.length" class="question-container">
      <div class="text-with-button">
        <p class="sub-title">{{ questions[currentQuestionIndex].text }}</p>
        <button class="small-button" @click="repeatQuestion">Écouter le texte</button>
      </div>

      <!-- Affichage des inputs en fonction du type de question -->
      <input
        v-if="questions[currentQuestionIndex].type === 'text'"
        type="text"
        v-model="responses[questions[currentQuestionIndex].key]"
        placeholder="Votre réponse"
        class="small-input"
        required
      />
      <input
        v-if="questions[currentQuestionIndex].type === 'number'"
        type="number"
        v-model="responses[questions[currentQuestionIndex].key]"
        placeholder="Votre réponse"
        class="small-input"
        required
      />
      <button class="small-button" @click="startRecognition">🎙️ Parler</button>

      <!-- Bloc de sélection d'avatar pour la question "passions" -->
      <div v-if="questions[currentQuestionIndex].key === 'passions'">
        <!-- Indicateur de chargement pendant la génération -->
        <div v-if="isLoadingImages" class="loading">
          <p>Chargement des avatars...</p>
        </div>
        <!-- Affichage des avatars une fois chargés -->
        <div v-else-if="generatedImages.length > 0 && !selectedAvatarUrl" class="avatar-selection">
          <h2>Choisissez votre avatar :</h2>
          <div class="avatars-grid">
            <img
              v-for="(img, index) in generatedImages"
              :key="index"
              :src="img"
              alt="Option d'avatar"
              class="avatar-option"
              @click="selectAvatar(img)"
            />
          </div>
        </div>
      </div>

      <div class="button-group">
        <button @click="nextQuestion">Suivant</button>
        <button class="medium-button" @click="skipQuestion">Je n'ai pas compris / Je ne sais pas</button>
      </div>
    </div>

    <div v-else class="completion-message">
      <button @click="speedGame">Commencer le premier jeu</button>
      <p>Merci d'avoir répondu aux questions !</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

/* global webkitSpeechRecognition */
export default {
  name: 'UserQuestionnaire',
  data() {
    return {
      currentQuestionIndex: 0,
      // Tableau pour stocker les URL des images générées
      generatedImages: [],
      // URL de l'avatar sélectionné par l'utilisateur
      selectedAvatarUrl: '',
      // Indicateur de chargement pour la génération des images
      isLoadingImages: false,
      backgroundColors: ['#e0f7fa', '#e8f5e9', '#fce4ec', '#fff3e0', '#ede7f6', '#f9fbe7'],
      questions: [
        // Vous pouvez décommenter ou ajouter d'autres questions si nécessaire
        // { text: '🎂 Quel âge as-tu ?', key: 'age', type: 'number' },
        // { text: '👤 Comment voudrais-tu qu\'on t\'appelle ?', key: 'name', type: 'text' },
        { text: '🎨 Quelles sont tes passions ?', key: 'passions', type: 'text', icon: 'passion-icon.png' }
      ],
      responses: {
        age: '',
        name: '',
        passions: ''
      },
      recognition: null,
      isRecognizing: false
    };
  },
  mounted() {
    this.updateBackgroundColor();
    if ('webkitSpeechRecognition' in window) {
      this.recognition = new webkitSpeechRecognition();
      this.recognition.lang = 'fr-FR';
      this.recognition.continuous = true;
      this.recognition.interimResults = false;

      this.recognition.onstart = () => {
        console.log('Recognition started');
        this.isRecognizing = true;
      };

      this.recognition.onresult = (event) => {
        const transcript = event.results[event.resultIndex][0].transcript.trim();
        console.log('Recognition result:', transcript);
        this.responses[this.questions[this.currentQuestionIndex].key] = transcript;
        this.isRecognizing = false;
        this.recognition.stop();
      };

      this.recognition.onerror = (event) => {
        console.error('Recognition error:', event.error);
        this.isRecognizing = false;
      };

      this.recognition.onend = () => {
        console.log('Recognition ended');
        this.isRecognizing = false;
      };
    } else {
      console.error('webkitSpeechRecognition not supported in this browser.');
    }
  },
  computed: {
    imageClass() {
      return this.selectedAvatarUrl ? 'image-selected' : 'image-default';
    }
  },
  methods: {
    speedGame() {
      this.$router.push('/game-speed');
    },
    async nextQuestion() {
      if (this.responses[this.questions[this.currentQuestionIndex].key] === '') {
        alert("Veuillez répondre à la question avant de passer à la suivante.");
        return;
      }
      // Pour la question des passions, générer 3 images puis forcer la sélection
      if (this.questions[this.currentQuestionIndex].key === 'passions') {
        // Si aucune image n'a encore été générée, appeler l'API
        if (this.generatedImages.length === 0) {
          await this.generatePicture(this.responses.passions);
          // Après génération, laisser l'utilisateur choisir (ne pas avancer automatiquement)
          return;
        }
        // Si les images sont générées mais aucune n'a été choisie, empêcher le passage à la question suivante
        if (!this.selectedAvatarUrl) {
          alert("Veuillez choisir un avatar parmi les images proposées.");
          return;
        }
      }
      this.currentQuestionIndex++;
      this.updateBackgroundColor();
    },
    async generatePicture(passions) {
      const url = process.env.VUE_APP_AZURE_OPENAI_ENDPOINT;
      const apiKey = process.env.VUE_APP_AZURE_OPENAI_API_KEY;
      // Construction du prompt
      const prompt = `Un avatar conçu pour accompagner un utilisateur en situation de handicap neurodéveloppemental (ADHD, autisme, etc.). Il est vu de face, avec une expression amicale et engageante, prêt à poser des questions. Son apparence et son langage corporel montrent son enthousiasme pour ${passions}, avec des vêtements, accessoires ou éléments visuels directement liés à cet univers. L’avatar doit dégager de la bienveillance et de la curiosité, avec un regard expressif et captivant. Le fond est neutre et ne contient AUCUN éléments, afin de ne pas distraire du personnage principal. L’éclairage est doux et professionnel, adapté à une utilisation digitale. `;
      console.log("Envoi de la requête à l'API Azure OpenAI...");
      console.log("Prompt :", prompt);

      // Réinitialiser les images et afficher le chargement
      this.generatedImages = [];
      this.isLoadingImages = true;

      // Effectuer 3 requêtes consécutives
      for (let i = 0; i < 3; i++) {
        try {
          const response = await axios.post(
            url,
            { prompt, n: 1 },
            {
              headers: {
                "Content-Type": "application/json",
                "api-key": apiKey
              }
            }
          );
          const imageUrl = response.data.data[0].url;
          this.generatedImages.push(imageUrl);
          console.log(`Image ${i + 1} générée:`, imageUrl);
        } catch (error) {
          console.error("Erreur lors de la génération de l'image :", error);
        }
      }
      this.isLoadingImages = false;
    },
    // Méthode appelée lorsque l'utilisateur clique sur une image pour choisir son avatar
    selectAvatar(imgUrl) {
      this.selectedAvatarUrl = imgUrl;
      console.log("Avatar sélectionné :", imgUrl);
    },
    updateBackgroundColor() {
      const colorIndex = this.currentQuestionIndex % this.backgroundColors.length;
      document.querySelector('.questionnaire').style.backgroundColor = this.backgroundColors[colorIndex];
    },
    skipQuestion() {
      this.currentQuestionIndex++;
      this.updateBackgroundColor();
    },
    repeatQuestion() {
      const text = this.questions[this.currentQuestionIndex].text;
      const speech = new SpeechSynthesisUtterance();
      speech.lang = 'fr-FR';
      speech.text = text;
      window.speechSynthesis.speak(speech);
    },
    startRecognition() {
      if (this.recognition && !this.isRecognizing) {
        this.recognition.start();
      }
    }
  }
};
</script>

<style scoped>
@import url('@/assets/styles.css');

.questionnaire {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  background-color: #e0f7fa;
  padding: 20px;
  min-height: 100vh;
}

.title {
  font-family: 'Glacial Indifference', sans-serif;
  font-weight: bold;
  margin-top: 5%;
}

.sub-title {
  font-family: 'Glacial Indifference', sans-serif;
  font-weight: bold;
  font-size: 2em;
  margin-bottom: 20px;
}

.image-default {
  width: 200px;
  height: 230px;
}

.image-selected {
  width: 300px;
  height: 300px;
}

.question-container {
  margin-top: 2%;
  margin-bottom: 5%;
}

.small-input {
  padding: 10px;
  width: 50%;
  margin-bottom: 10px;
  font-size: 1em;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.small-input:focus {
  border-color: #007BFF;
  box-shadow: 0 0 8px rgba(0, 123, 255, 0.5);
  outline: none;
}

.text-with-button {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
}

.text-with-button p {
  margin-right: 10px;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.medium-button {
  padding: 0.5em 1em;
  font-size: 0.8em;
}

.completion-message {
  font-size: 1.2em;
  margin-top: 20px;
}

/* Styles pour le bloc de sélection d'avatar */
.avatar-selection {
  margin: 20px 0;
}

.avatars-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.avatar-option {
  width: 300px;
  height: 300px;
  object-fit: cover;
  cursor: pointer;
  border: 2px solid transparent;
  border-radius: 10px;
  transition: border-color 0.3s ease;
}

.avatar-option:hover {
  border-color: #007BFF;
}

/* Style pour l'indicateur de chargement */
.loading {
  margin: 20px 0;
  font-size: 1.2em;
  color: #555;
}
</style>
