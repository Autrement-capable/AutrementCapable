<template>
  <div class="account-creation" aria-label="Account creation page">
    <h1 class="title">Création de Compte</h1>
    <p>Nous allons devoir vous créer un compte pour accéder aux fonctionnalités de la plateforme.</p>
    <button @click="goToExplanation" aria-label="Suivant pour l'explication">Suivant</button>
    <button @click="speakText" aria-label="Écoutez le texte">Écouter le texte</button>
  </div>
</template>

<script>
export default {
  methods: {
    goToExplanation() {
      this.$router.push('/explanation');
    },
    speakText() {
      const text = "Nous allons devoir vous créer un compte pour accéder aux fonctionnalités de la plateforme.";
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

.account-creation {
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
