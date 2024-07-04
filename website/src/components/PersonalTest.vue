<template>
  <div class="personal-test" aria-label="Personal test page">
    <h1 class="title">Phase de Test</h1>
    <div class="text-with-button">
      <p>Réponds aux questions suivantes pour que nous puissions mieux comprendre tes valeurs.</p>
      <button @click="speakText" class="small-button" aria-label="Écoutez le texte">Écouter le texte</button>
    </div>
    <button @click="goToQuestionnaire" aria-label="Commencer le questionnaire">Commencer</button>
  </div>
</template>

<script>
export default {
  methods: {
    goToQuestionnaire() {
      this.$router.push('/questionnaire');
    },
    speakText() {
      const text = "Réponds aux questions suivantes pour que nous puissions mieux comprendre tes valeurs.";
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
  background-color: #f5f5f5;
  padding: 20px;
  height: 100vh;
}
.title {
  font-family: 'Glacial Indifference', sans-serif;
  font-weight: bold;
  margin-top: 15%;
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
p {
  font-size: 1.5em;
}
.small-button {
  padding: 0.5em 1em;
  font-size: 0.8em;
}
</style>
