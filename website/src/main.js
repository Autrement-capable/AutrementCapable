import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "./style.css";
import "./assets/styles.css";
import "@mdi/font/css/materialdesignicons.css";
import * as PIXI from "pixi.js";

// Importez vos composants globaux ici si nécessaire
import SpaceBackground from '@/components/SpaceBackground.vue'
import StaticBackgrounds from '@/components/StaticBackgrounds.vue'
import BadgesComponent from '@/components/RewardsComponent.vue'
import ProfileComponent from '@/components/ProfileComponent.vue'

if (process.env.NODE_ENV === "development") {
  window.PIXI = PIXI;
}

// Création de l'application
const app = createApp(App);

// Enregistrement des composants globaux (si nécessaire)
app.component('SpaceBackground', SpaceBackground);
app.component('StaticBackgrounds', StaticBackgrounds);
app.component('BadgesComponent', BadgesComponent);
app.component('ProfileComponent', ProfileComponent);

// Montage de l'application
app.use(router).mount("#app");