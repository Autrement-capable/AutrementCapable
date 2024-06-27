<template>
  <div class="explanation" aria-label="Explanation page">
    <h1 class="title">Pourquoi créer un compte ?</h1>
    <p>Créer un compte vous permet de personnaliser votre expérience, de suivre vos progrès et d’accéder à toutes les fonctionnalités de notre plateforme de manière sécurisée.</p>
    <button @click="goToTest" aria-label="Compris, aller à la phase de test">Compris</button>
    <button @click="speakText" aria-label="Écoutez le texte">Écouter le texte</button>
  </div>
</template>

<script>
export default {
  name: 'UserExplanation',
  methods: {
    goToTest() {
      this.$router.push('/personal-test');
    },
    speakText() {
      const text = "Créer un compte vous permet de personnaliser votre expérience, de suivre vos progrès et d’accéder à toutes les fonctionnalités de notre plateforme de manière sécurisée.";
      const speech = new SpeechSynthesisUtterance();
      speech.lang = 'fr-FR';
      speech.text = text;
      window.speechSynthesis.speak(speech);
    }
  }
}
</script>

<style scoped>
@import url('@/assets/styles.css');

.explanation {
  text-align: center;
  margin-top: 50px;
  background-color: #f5f5f5;
  padding: 20px;
}
.title {
  font-family: 'Glacial Indifference', sans-serif;
  font-weight: bold;
}
p {
  font-size: 1.5em;
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
}
button:focus {
  outline: 2px solid #0056b3;
}
</style>
