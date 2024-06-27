<template>
  <div class="personal-test" aria-label="Personal test page">
    <h1 class="title">Phase de Test</h1>
    <p>Répondez aux questions suivantes pour que nous puissions mieux comprendre vos besoins.</p>
    <button @click="goToQuestionnaire" aria-label="Commencer le questionnaire">Commencer</button>
    <button @click="speakText" aria-label="Écoutez le texte">Écouter le texte</button>
  </div>
</template>

<script>
export default {
  methods: {
    goToQuestionnaire() {
      this.$router.push('/questionnaire');
    },
    speakText() {
      const text = "Répondez aux questions suivantes pour que nous puissions mieux comprendre vos besoins.";
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

.personal-test {
  text-align: center;
  margin-top: 50px;
  background-color: #f5f5f5;
  padding: 20px;
}
.title {
  font-family: 'Glacial Indifference', sans-serif;
  font-weight: bold;
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
p {
  font-size: 1.5em;
}
</style>
