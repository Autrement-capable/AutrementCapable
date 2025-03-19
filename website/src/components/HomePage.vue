<!-- src/views/HomePage.vue -->
<template>
    <div class="home">
      <h1>Bienvenue sur notre site</h1>
      <p>Cliquez sur "Jouer" dans la navigation pour lancer le jeu top-down!</p>
      <div class="game-preview">
        <img src="/game-preview.jpg" alt="Aperçu du jeu" v-if="false">
        <div class="preview-placeholder">
          <p>Aperçu du jeu</p>
        </div>
      </div>
      <router-link to="/game-page" class="play-button">
        JOUER MAINTENANT
      </router-link>
    </div>
  </template>
  
  <script>
  export default {
    name: 'HomePage'
  }
  </script>
  
  <style scoped>
  .home {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .game-preview {
    margin: 30px auto;
    width: 100%;
    max-width: 600px;
    height: 300px;
    border-radius: 8px;
    overflow: hidden;
  }
  
  .preview-placeholder {
    width: 100%;
    height: 100%;
    background: #e0e0e0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    color: #666;
  }
  
  .play-button {
    display: inline-block;
    background-color: #42b983;
    color: white;
    padding: 15px 30px;
    border-radius: 30px;
    font-weight: bold;
    text-decoration: none;
    font-size: 18px;
    transition: all 0.3s ease;
    margin-top: 20px;
  }
  
  .play-button:hover {
    background-color: #3aa876;
    transform: scale(1.05);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
  </style>