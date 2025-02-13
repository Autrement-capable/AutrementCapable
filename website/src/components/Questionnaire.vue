<template>
  <div class="questionnaire" aria-label="Questionnaire page">
    <h1 class="title">Bonjour !</h1>
    <img :src="generatedImageUrl || require('../assets/jeunefemme.png')" alt="Questionnaire" class="image" />
    <div v-if="currentQuestionIndex < questions.length" class="question-container">
      <div class="text-with-button">
        <p class="sub-title">{{ questions[currentQuestionIndex].text }}</p>
        <button class="small-button" @click="repeatQuestion">Ecouter le texte</button>
      </div>
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
      generatedImageUrl: null,
      backgroundColors: ['#e0f7fa', '#e8f5e9', '#fce4ec', '#fff3e0', '#ede7f6', '#f9fbe7'],
      questions: [
        { text: '🎂 Quel âge as-tu ?', key: 'age', type: 'number' },
        { text: '👤 Comment voudrais-tu qu\'on t\'appelle ?', key: 'name', type: 'text' },
        { text: '🎨 Quelles sont tes passions ?', key: 'passions', type: 'text', icon: 'passion-icon.png' },
        // { text: '🏥 Possèdes-tu une maladie / trouble ?', key: 'condition', type: 'text' },
        // { text: '😊 Comment te sens-tu aujourd\'hui ?', key: 'currentMood', type: 'text' },
        // { text: '😃 Qu\'est-ce qui te rend heureux(se) ?', key: 'happiness', type: 'text' },
        // { text: '👨‍👩‍👧‍👦 Qui sont les personnes qui te soutiennent le plus ?', key: 'supportNetwork', type: 'text' },
        // { text: '🏃 Quelles sont tes activités préférées ?', key: 'favoriteActivities', type: 'text' },
        // { text: '😃 Aimes-tu faire rire les autres ?', key: 'funny', type: 'text' },
        // { text: '📚 Quelles compétences aimerais-tu améliorer ?', key: 'skillsToImprove', type: 'text' },
        // { text: '💖 Quelles sont les valeurs qui te tiennent à cœur ?', key: 'values', type: 'text' },
        // { text: '🌅 Qu\'est-ce qui te motive à te lever chaque jour ?', key: 'motivations', type: 'text' },
        // { text: '🌟 Quels sont tes rêves pour le futur ?', key: 'dreams', type: 'text' },
        // { text: '💪 Quelles sont tes forces et tes talents ?', key: 'strengths', type: 'text' },
        // { text: '🤝 Comment te sens-tu dans tes relations avec les autres ?', key: 'relationships', type: 'text' },
        // { text: '🗣️ Qu\'attends-tu des autres pour te sentir bien ?', key: 'expectationsFromOthers', type: 'text' },
        // { text: '💼 Quelles sont tes aspirations professionnelles ?', key: 'careerAspirations', type: 'text' },
        // { text: '🔮 Comment te vois-tu dans 5 ans ?', key: 'futureSelf', type: 'text' },
        // { text: '💼 Quels métiers t\'intéressent le plus ?', key: 'interestedJobs', type: 'text' },
        // { text: '♿ Quelles adaptations te facilitent la vie quotidienne ?', key: 'adaptations', type: 'text' },
        // { text: '🚧 Quels obstacles rencontres-tu souvent ?', key: 'obstacles', type: 'text' },
        // { text: '🆘 Comment pouvons-nous t\'aider à surmonter ces obstacles ?', key: 'overcomingObstacles', type: 'text' }
      ],
      responses: {
        age: '',
        name: '',
        condition: '',
        currentMood: '',
        happiness: '',
        favoriteActivities: '',
        passions: '',
        strengths: '',
        skillsToImprove: '',
        values: '',
        motivations: '',
        dreams: '',
        supportNetwork: '',
        relationships: '',
        expectationsFromOthers: '',
        careerAspirations: '',
        futureSelf: '',
        interestedJobs: '',
        adaptations: '',
        obstacles: '',
        overcomingObstacles: ''
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
  methods: {
    speedGame() {
      this.$router.push('/game-speed');
    },
    async nextQuestion() {
      if (this.responses[this.questions[this.currentQuestionIndex].key] !== '') {
        if (this.questions[this.currentQuestionIndex].key === 'passions') {
          await this.generatePicture(this.responses.passions);
        }
        this.currentQuestionIndex++;
        this.updateBackgroundColor();
      } else {
        alert("Veuillez répondre à la question avant de passer à la suivante.");
      }
    },
    async generatePicture(passions) {
      const url = process.env.VUE_APP_AZURE_OPENAI_ENDPOINT;
      const apiKey = process.env.VUE_APP_AZURE_OPENAI_API_KEY;

      const prompt = `Un avatar conçu pour accompagner un utilisateur en situation de handicap neurodéveloppemental (ADHD, autisme, etc.) pour un parcours d’orientation. Il est vu de face, avec une expression amicale et engageante, prêt à poser des questions. Son apparence et son langage corporel montrent son enthousiasme pour ${passions}, avec des vêtements, accessoires ou éléments visuels directement liés à cet univers. Sa passion est : ${passions}. L’avatar doit dégager de la bienveillance et de la curiosité, avec un regard expressif et captivant. Le fond est neutre ou légèrement inspiré par ${passions}, afin de ne pas distraire du personnage principal. L’éclairage est doux et professionnel, adapté à une utilisation digitale.`;

      console.log("Envoi de la requête à l'API Azure OpenAI...");
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

        // Extraction de l'URL de l'image générée
        const imageUrl = response.data.data[0].url;
        console.log("URL de l'image générée :", imageUrl);
        // Mise à jour de la propriété pour afficher l'image générée
        this.generatedImageUrl = imageUrl;
      } catch (error) {
        console.error("Erreur lors de la génération de l'image :", error);
      }
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
    },
  },
}
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
  height: 100vh;
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

.image {
  width: 200px;
  height: 230px;
  margin: 20px;
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

button {
  margin-top: 20px;
  padding: 1em 2em;
  font-size: 1em;
  background-color: #007BFF;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin: 0.5em;
  transition: transform 0.3s ease, background-color 0.3s ease;
}

button:focus {
  outline: 2px solid #0056b3;
}

button:hover {
  transform: scale(1.05);
  background-color: #0056b3;
}

.small-button {
  padding: 0.5em;
  font-size: 0.8em;
}

.medium-button {
  padding: 0.5em 1em;
  font-size: 0.8em;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.completion-message {
  font-size: 1.2em;
  margin-top: 20px;
}
</style>