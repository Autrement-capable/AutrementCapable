<template>
  <div class="questionnaire" aria-label="Questionnaire page">
    <h1 class="title">Questionnaire</h1>
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
      <p>Merci d'avoir répondu aux questions !</p>
    </div>
  </div>
</template>

<script>
/* global webkitSpeechRecognition */
export default {
  name: 'UserQuestionnaire',
  data() {
    return {
      currentQuestionIndex: 0,
      questions: [
        { text: 'Quel âge as-tu ?', key: 'age', type: 'number' },
        { text: 'Comment voudrais-tu qu\'on t\'appelle ?', key: 'name', type: 'text' },
        { text: 'Possèdes-tu une maladie / trouble ?', key: 'condition', type: 'text' },
        { text: 'Comment te sens-tu aujourd\'hui ?', key: 'currentMood', type: 'text' },
        { text: 'Qu\'est-ce qui te rend heureux(se) ?', key: 'happiness', type: 'text' },
        { text: 'Quelles sont tes activités préférées ?', key: 'favoriteActivities', type: 'text' },
        { text: 'Quelles passions aimerais-tu développer ?', key: 'passions', type: 'text' },
        { text: 'Quelles sont tes forces et tes talents ?', key: 'strengths', type: 'text' },
        { text: 'Quelles compétences aimerais-tu améliorer ?', key: 'skillsToImprove', type: 'text' },
        { text: 'Quelles sont les valeurs qui te tiennent à cœur ?', key: 'values', type: 'text' },
        { text: 'Qu\'est-ce qui te motive à te lever chaque jour ?', key: 'motivations', type: 'text' },
        { text: 'Quels sont tes rêves pour le futur ?', key: 'dreams', type: 'text' },
        { text: 'Qui sont les personnes qui te soutiennent le plus ?', key: 'supportNetwork', type: 'text' },
        { text: 'Comment te sens-tu dans tes relations avec les autres ?', key: 'relationships', type: 'text' },
        { text: 'Qu\'attends-tu des autres pour te sentir bien ?', key: 'expectationsFromOthers', type: 'text' },
        { text: 'Quelles sont tes aspirations professionnelles ?', key: 'careerAspirations', type: 'text' },
        { text: 'Comment te vois-tu dans 5 ans ?', key: 'futureSelf', type: 'text' },
        { text: 'Quels métiers t\'intéressent le plus ?', key: 'interestedJobs', type: 'text' },
        { text: 'Quelles adaptations te facilitent la vie quotidienne ?', key: 'adaptations', type: 'text' },
        { text: 'Quels obstacles rencontres-tu souvent ?', key: 'obstacles', type: 'text' },
        { text: 'Comment pouvons-nous t\'aider à surmonter ces obstacles ?', key: 'overcomingObstacles', type: 'text' }
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
    nextQuestion() {
      if (this.responses[this.questions[this.currentQuestionIndex].key] !== '') {
        this.currentQuestionIndex++;
        console.log('Moved to next question');
      } else {
        alert("Veuillez répondre à la question avant de passer à la suivante.");
      }
    },
    skipQuestion() {
      this.currentQuestionIndex++;
      console.log('Skipped to next question');
    },
    repeatQuestion() {
      const text = this.questions[this.currentQuestionIndex].text;
      console.log('Repeating question:', text);
      const speech = new SpeechSynthesisUtterance();
      speech.lang = 'fr-FR';
      speech.text = text;
      window.speechSynthesis.speak(speech);
    },
    startRecognition() {
      if (this.recognition && !this.isRecognizing) {
        console.log('Starting recognition');
        this.recognition.start();
      } else {
        console.log('Recognition already in progress or not supported');
      }
    }
  }
}
</script>

<style scoped>
@import url('@/assets/styles.css');

.questionnaire {
  text-align: center;
  background-color: #f5f5f5;
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
}

.question-container {
  margin-top: 10%;
  margin-bottom: 15px;
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
