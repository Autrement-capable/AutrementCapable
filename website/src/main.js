import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "./style.css";
import "./assets/styles.css";
import "@mdi/font/css/materialdesignicons.css";
import * as PIXI from "pixi.js";

if (process.env.NODE_ENV === "development") {
  window.PIXI = PIXI;
}

// if (!process.env.SERVER_URL) {
//   console.warn(
//     "Please set the SERVER_URL environment variable. Defaulting to http://localhost:5000"
//   );
//   App.globalProperties.$serverUrl = "http://localhost:5000";
// } else {
//   App.globalProperties.$serverUrl = process.env.SERVER_URL;
// }
createApp(App).use(router).mount("#app");
