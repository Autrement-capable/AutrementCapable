<template>
  <div class="scenario-list-container">
    <!-- 📝 Titre Principal -->
    <h1>📜 Liste des Scénarios</h1>

    <!-- 📝 Simple Liste des Scénarios -->
    <ul class="scenario-list">
      <li v-for="scenario in scenarios" :key="scenario.id" class="scenario-item">
        {{ scenario.titre }}
      </li>
    </ul>

    <!-- 🚀 Bouton Commencer Scénario 1 -->
    <div class="start-container">
      <button @click="startFirstScenario" class="start-button">
        🚀 Commencer l'Aventure
      </button>
    </div>
  </div>
</template>

<script>
import { scenarios } from '@/data/data.js';

export default {
  data() {
    return {
      scenarios,
    };
  },
  methods: {
    startFirstScenario() {
      localStorage.setItem('userSoftSkills', JSON.stringify({}));
      this.$router.push({ name: 'ScenarioPage', params: { id: 1 } });
    }
  }
};
</script>

<style scoped>
/* 🌟 Container principal */
.scenario-list-container {
  font-family: Arial, sans-serif;
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

/* 📝 Titre */
h1 {
  font-size: 2.2rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 20px;
}

/* 📜 Liste des Scénarios */
.scenario-list {
  list-style-type: none;
  padding: 0;
  margin-bottom: 30px;
}

/* 📝 Éléments de la liste */
.scenario-item {
  font-size: 1.2rem;
  font-weight: 500;
  color: #333;
  padding: 10px;
  border-bottom: 1px solid #ddd;
  transition: background-color 0.3s;
}

/* 📝 Survol des Scénarios */
.scenario-item:hover {
  background-color: #e7f5ff;
}

/* 🚀 Bouton Commencer */
.start-container {
  margin-top: 20px;
}

.start-button {
    padding: 12px 24px;
    font-size: 1.2rem;
    font-weight: bold;
    color: white;
    background-color: #28a745;
    border-radius: 10px;
    transition: background-color 0.3s;
    display: inline-block;
    width: auto;
    max-width: 250px;
    height: auto;
    text-align: center;
    margin: 10px auto;
    line-height: normal;
}

.start-button:hover {
    background-color: #218838;
}
</style>
