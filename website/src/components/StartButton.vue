<template>
  <div class="start-button" aria-label="Start page">
    <h1 class="main-title">Autrement Capable</h1>
    <button @click="startProcess" aria-label="Commencez le processus">Commencer</button>
    <!-- <button @click="speakText" aria-label="Écoutez le texte">Écouter le texte</button> -->
  </div>
</template>

<script>
export default {
  methods: {
    startProcess() {
      this.$router.push('/account-creation');
    },
    speakText() {
      const text = "Bienvenue sur Autrement Capable. Appuyez sur le bouton Commencer pour démarrer le processus de création de compte.";
      const speech = new SpeechSynthesisUtterance();
      speech.lang = 'fr-FR';
      speech.text = text;
      window.speechSynthesis.speak(speech);
    }
  }
}
</script>

<style>
@import url('@/assets/styles.css');

.start-button {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}
.main-title {
  font-family: 'Glacial Indifference', sans-serif;
  font-weight: bold;
  font-size: 3em;
  margin-bottom: 1em;
}
button {
  padding: 1em 2em;
  font-size: 1.2em;
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
</style>
