<template>
  <div id="shape-game-container">
    <button ref="startButton" id="startButton" @click="StartGame">Start Game</button>
    <div ref="gameArea" id="gameArea" class="hidden">
      <div ref="shapeContainer" id="shapeContainer"></div>
      <div ref="options" id="options">
        <button ref="option" class="option" @click="getAnswer(1)">Same as before</button>
        <button ref="option" class="option" @click="getAnswer(2)">
          Same shape, different color
        </button>
        <button ref="option" class="option" @click="getAnswer(3)">
          Same color, different shape
        </button>
        <button ref="option" class="option" @click="getAnswer(4)">Totally different</button>
      </div>
    </div>
    <div>
        <button style="display: inline-block;" @click="memoryGame">Commencer le troisième jeu</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      color_list: ["red", "blue", "green", "yellow", "purple", "orange", "brown", "gray"],
      shape_list: ["circle", "square", "triangle", "star", "rectangle", "oval", "trapezoid"],
      max_rounds: 8,
      time_per_round: 2,
      dup_chance: 0.5,
      old_shape: [],
      current_shape: [],
      score: 0,
      time: null,
      round: 0,
    };
  },
  methods: {
    generate_shape(old_shape, dup_chance) {
      if (old_shape.length > 0 && Math.random() < dup_chance) {
        return old_shape;
      } else {
        let shape = this.shape_list[Math.floor(Math.random() * this.shape_list.length)];
        let color = this.color_list[Math.floor(Math.random() * this.color_list.length)];
        return [shape, color];
      }
    },
    memoryGame() {
      this.$refs.gameArea.classList.add("hidden");
      this.$refs.startButton.classList.remove("hidden");
      alert("Game Over! Your score is: " + this.score);
      this.score = 0;
      this.round = 0;
      this.time = null;
      this.current_shape = [];
      this.old_shape = [];
      
      this.$router.push('/game-memory');
    },
    async getAnswer(selected_option) {
      const option_list = [
        "Same as before",
        "Same shape, different color",
        "Same color, different shape",
        "Totally different",
      ];
      let correct_option = -1;
      if (this.old_shape[0] === this.current_shape[0] && this.old_shape[1] === this.current_shape[1]) {
        correct_option = 1;
      } else if (this.old_shape[0] === this.current_shape[0]) {
        correct_option = 2;
      } else if (this.old_shape[1] === this.current_shape[1]) {
        correct_option = 3;
      } else {
        correct_option = 4;
      }
      if (selected_option === correct_option) {
        this.score++;
      } else {
        console.log("Wrong answer. Right answer was: " + option_list[correct_option - 1]);
      }
      await this.StartGame();
    },
    async generateImage() {
      return new Promise((resolve) => {
        this.$refs.options.classList.add("hidden");
        this.old_shape = this.generate_shape(this.old_shape, 0);
        this.$refs.shapeContainer.className = "";
        this.$refs.shapeContainer.classList.add(this.old_shape[0]);
        this.$refs.shapeContainer.classList.add(this.old_shape[1]);
        setTimeout(() => {
          this.$refs.shapeContainer.className = "";
          resolve();
        }, this.time_per_round * 1000);
      });
    },
    async generateOptions() {
      return new Promise((resolve) => {
        this.current_shape = this.generate_shape(this.old_shape, this.dup_chance);
        this.$refs.shapeContainer.className = "";
        this.$refs.shapeContainer.classList.add(this.current_shape[0]);
        this.$refs.shapeContainer.classList.add(this.current_shape[1]);
        this.$refs.options.classList.remove("hidden");
        resolve();
      });
    },
    async StartGame() {
      if (this.round >= this.max_rounds) {
        this.GameOver();
        return;
      }
      if (this.time === null) {
        this.time = new Date();
      }
      this.round++;
      this.$refs.startButton.classList.add("hidden");
      this.$refs.gameArea.classList.remove("hidden");
      await this.generateImage();
      await this.generateOptions();
    },
    GameOver() {
      this.$refs.gameArea.classList.add("hidden");
      this.$refs.startButton.classList.remove("hidden");
      alert("Game Over! Your score is: " + this.score);
      this.score = 0;
      this.round = 0;
      this.time = null;
      this.current_shape = [];
      this.old_shape = [];
    },
  },
};
</script>

<style>
#shape-game-container {
  font-family: Arial, sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
  text-align: center;
}

.hidden {
  display: none !important;
}

#shapeContainer {
  width: 200px;
  height: 200px;
  margin: 20px auto;
  display: flex;
  justify-content: center;
  align-items: center;
}

#options {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20px auto;
}

.square {
  width: 100px;
  height: 100px;
}

.shape {
  width: 100px;
  height: 100px;
}

.rectangle {
  width: 150px;
}

.circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
}

.triangle {
  width: 0;
  height: 0;
  border-left: 50px solid transparent !important;
  border-right: 50px solid transparent !important;
  border-bottom: 100px solid black;
}

.oval {
  width: 200px;
  height: 100px;
  border-radius: 100px / 50px;
}

.trapezoid {
  border-bottom: 100px solid red;
  border-left: 25px solid transparent !important;
  border-right: 25px solid transparent !important;
  height: 0;
  width: 100px;
}

.star {
  width: 0 !important;
  height: 0 !important;
  border-left: 50px solid transparent !important;
  border-right: 50px solid transparent !important;
  border-bottom: 100px solid red;
  position: relative;
  background-color: unset !important;
}
.star:after {
  width: 0;
  height: 0;
  border-left: 50px solid transparent !important;
  border-right: 50px solid transparent !important;
  border-top: 100px solid red;
  position: absolute;
  content: "";
  top: 30px;
  left: -50px;
}

.red {
  background-color: red;
  border-color: red;
}
.red:after {
  border-color: red;
}

.blue {
  background-color: blue;
  border-color: blue;
}
.blue:after {
  border-color: blue;
}

.green {
  background-color: green;
  border-color: green;
}
.green:after {
  border-color: green;
}

.yellow {
  background-color: yellow;
  border-color: yellow;
}
.yellow:after {
  border-color: yellow;
}

.purple {
  background-color: purple;
  border-color: purple;
}
.purple:after {
  border-color: purple;
}

.orange {
  background-color: orange;
  border-color: orange;
}
.orange:after {
  border-color: orange;
}

.brown {
  background-color: rgb(63, 16, 16);
  border-color: rgb(63, 16, 16);
}
.brown:after {
  border-color: rgb(63, 16, 16);
}

.gray {
  background-color: gray;
  border-color: gray;
}
.gray:after {
  border-color: gray;
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
