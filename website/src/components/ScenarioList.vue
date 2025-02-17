<template>
    <div>
      <h1>📜 Liste des Scénarios</h1>
      <ul>
        <li v-for="scenario in scenarios" :key="scenario.id">
          <router-link :to="{ name: 'ScenarioPage', params: { id: scenario.id }}">
            {{ scenario.titre }}
          </router-link>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import { scenarios } from '@/data/data.js';
  
  export default {
    data() {
      return {
        scenarios,
      };
    }
  };
  </script>
  