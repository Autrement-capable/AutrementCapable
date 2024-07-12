<template>
  <div class="explanation" aria-label="Explanation page">
    <h1 class="title">Pourquoi créer un compte ?</h1>
    <div class="text-with-button">
      <p>Créer un compte te permet de personnaliser ton expérience et de suivre tes progrès.</p>
      <button class="small-button" @click="speakText" aria-label="Écoutez le texte">Écouter le texte</button>
    </div>
    <button @click="goToTest" aria-label="Compris, aller à la phase de test">Compris</button>
  </div>
</template>

<script>
export default {
  name: 'UserExplanation',
  methods: {
    goToTest() {
      // this.$router.push('/personal-test');
      this.$router.push('/login');
    },
    speakText() {
      const text = "Créer un compte te permet de personnaliser tes expérience, de suivre tes progrès et d’accéder à toutes les fonctionnalités de notre plateforme de manière sécurisée.";
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
  background-color: #f5f5f5;
  padding: 20px;
  height: 100vh;
}
.title {
  font-family: 'Glacial Indifference', sans-serif;
  font-weight: bold;
  margin-top: 15%;
}
p {
  font-size: 1.5em;
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
  padding: 0.5em 1em;
  font-size: 0.8em;
}
</style>
