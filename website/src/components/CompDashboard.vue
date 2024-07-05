<template>
  <h1 class="title">Bravo !</h1>
  <button @click="goToCvPreview">Voir mon CV généré !</button>
  <!-- <div class="dashboard" aria-label="Dashboard page"> -->
    <!-- <div v-if="currentQuestionIndex < questions.length" class="question-container">
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
      <div class="button-group">
        <button @click="nextQuestion">Suivant</button>
        <button @click="nextQuestion">Je n'ai pas compris / Je ne sais pas</button>
        <button @click="repeatQuestion">Écoutez le texte</button>
      </div>
    </div>
    <div v-else class="completion-message">
      <button @click="speedGame">Commencer le premier jeu</button>
      <p>Merci d'avoir répondu aux questions !</p>
    </div>
  </div> -->
</template>

<script>
export default {
  name: 'UserQuestionnaire',
  methods: {
    goToCvPreview() {
      this.$router.push('/cv-preview');
    },
  }
}
</script>

<style scoped>
@import url('@/assets/styles.css');

.dashboard {
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
.button-group {
  display: flex;
  justify-content: center;
  gap: 10px;
}
button {
  padding: 1em 2em;
  font-size: 1em;
  background-color: #007BFF;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 20px;
}
button:focus {
  outline: 2px solid #0056b3;
}
.completion-message {
  font-size: 1.2em;
  margin-top: 20px;
}
</style>
