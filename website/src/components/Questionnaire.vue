<template>
  <div class="questionnaire" aria-label="Questionnaire page">
    <h1 class="title">Questionnaire</h1>
    <div v-if="currentQuestionIndex < questions.length" class="question-container">
      <p>{{ questions[currentQuestionIndex].text }}</p>
      <input 
        v-if="questions[currentQuestionIndex].type === 'text'" 
        type="text" 
        v-model="responses[questions[currentQuestionIndex].key]" 
        placeholder="Votre réponse" 
        required
      />
      <input 
        v-if="questions[currentQuestionIndex].type === 'number'" 
        type="number" 
        v-model="responses[questions[currentQuestionIndex].key]" 
        placeholder="Votre réponse" 
        required
      />
      <button @click="startRecognition">Parler</button>
      <div class="button-group">
        <button @click="nextQuestion">Suivant</button>
        <button @click="repeatQuestion">Je n'ai pas compris / Je ne sais pas</button>
      </div>
    </div>
    <div v-else class="completion-message">
      <p>Merci d'avoir répondu aux questions !</p>
    </div>
  </div>
</template>

<script>
export default {
  /* global webkitSpeechRecognition */
  name: 'UserQuestionnaire',
  data() {
    return {
      currentQuestionIndex: 0,
      questions: [
        { text: 'Quel âge as-tu ?', key: 'age', type: 'number' },
        { text: 'Comment voudrais-tu qu\'on t\'appelle ?', key: 'name', type: 'text' },
        { text: 'Possèdes-tu une maladie / trouble ?', key: 'condition', type: 'text' }
      ],
      responses: {
        age: '',
        name: '',
        condition: ''
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
        this.isRecognizing = true;
      };

      this.recognition.onresult = (event) => {
        const transcript = event.results[event.resultIndex][0].transcript.trim();
        this.responses[this.questions[this.currentQuestionIndex].key] = transcript;
        this.isRecognizing = false;
        this.recognition.stop();
      };

      this.recognition.onerror = (event) => {
        console.error(event.error);
        this.isRecognizing = false;
      };

      this.recognition.onend = () => {
        this.isRecognizing = false;
      };
    }
  },
  methods: {
    nextQuestion() {
      if (this.responses[this.questions[this.currentQuestionIndex].key] !== '') {
        this.currentQuestionIndex++;
      } else {
        alert("Veuillez répondre à la question avant de passer à la suivante.");
      }
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
}
</script>

<style scoped>
@import url('@/assets/styles.css'); /* Assurez-vous que les styles globaux sont importés */

.questionnaire {
  text-align: center;
  margin-top: 50px;
  background-color: #f5f5f5;
  padding: 20px;
}
.title {
  font-family: 'Glacial Indifference', sans-serif;
  font-weight: bold;
}
.question-container {
  margin-bottom: 15px;
}
input {
  padding: 10px;
  width: calc(100% - 22px);
  margin-bottom: 10px;
}
button {
  padding: 1em 2em;
  font-size: 1em;
  background-color: #007BFF;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin: 0.5em;
}
button:focus {
  outline: 2px solid #0056b3;
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
