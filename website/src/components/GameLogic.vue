<template>
  <div>
    <h2>Trouve la forme correcte !</h2>
    <div id="question">
      <img src="../assets/gameLogic/circle.png" alt="Question" />
    </div>
    <div id="options">
      <div
        v-for="(option, index) in options"
        :key="index"
        @click="checkAnswer(option)"
        class="option"
      >
        <img :src="option.image" :alt="'Option ' + (index + 1)" />
      </div>
    </div>
    <div v-if="feedback" :class="feedbackClass">{{ feedback }}</div>
    <button v-if="gameFinished" @click="finishGame">Finir le jeu</button>
  </div>
</template>

<script>
export default {
  name: "LogicGame",
  data() {
    return {
      // Liste dynamique des options
      options: [
        { id: 1, image: require("../assets/gameLogic/option1.png"), isCorrect: false },
        { id: 2, image: require("../assets/gameLogic/option2.png"), isCorrect: false },
        { id: 3, image: require("../assets/gameLogic/option3.png"), isCorrect: true }, // Exemple de bonne réponse
        { id: 4, image: require("../assets/gameLogic/option4.png"), isCorrect: false },
        { id: 5, image: require("../assets/gameLogic/option5.png"), isCorrect: false },
        { id: 6, image: require("../assets/gameLogic/option6.png"), isCorrect: false },
      ],
      feedback: "",
      gameFinished: false,
    };
  },
  computed: {
    feedbackClass() {
      return this.feedback === "Bonne réponse !" ? "correct" : "incorrect";
    },
  },
  methods: {
    checkAnswer(option) {
      if (option.isCorrect) {
        this.feedback = "Bonne réponse !";
        this.gameFinished = true;
      } else {
        this.feedback = "Mauvaise réponse, essaie encore.";
      }
    },
    finishGame() {
      alert("Jeu terminé. Bravo !");
      // Redirection ou autre action ici
    },
  },
};
</script>

<style>
#question img {
  width: 100px;
  margin-bottom: 20px;
}
#options {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
}
.option img {
  width: 80px;
  cursor: pointer;
  margin: 10px;
}
.correct {
  color: green;
  font-weight: bold;
}
.incorrect {
  color: red;
  font-weight: bold;
}
button {
  padding: 1em 2em;
  font-size: 1em;
  background-color: #007BFF;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 20px;
}
</style>
