<template>
  <div id="memory_game_container">
    <div ref="gameBoard" id="memory_game"></div>
    <button @click="dashboard">Finir le jeu</button>
  </div>
  <div>
  </div>
</template>

<script>
export default {
  name: "MemoryGame",
  data() {
    return {
      emojiList: [
        "😀",
        "😀",
        "😂",
        "😂",
        "😃",
        "😃",
        "😅",
        "😅",
        "😇",
        "😇",
        "😊",
        "😊",
        "😎",
        "😎",
        "😘",
        "😘",
      ],
      mx_lvl: 4,
      current_lvl: 1,
      shuffledEmojiList: [],
      emojiCount: 0,
      current_selection: [],
      isClickBlocked: false,
      guessedCards: 0,
      startTime: null,
      TotalTime: [],
    };
  },
  methods: {
    dashboard() {
      this.$router.push('/dashboard');
    },
    shuffleArray(array, nb_pairs = 8) {
      array = array.slice(0, nb_pairs * 2);
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }
      return array;
    },
    GetTimeTaken(startTime) {
      let endTime = new Date();
      let timeDiff = endTime - startTime;
      let seconds = Math.floor(timeDiff / 1000);
      let minutes = Math.floor(seconds / 60);
      seconds = seconds % 60;
      return minutes + " minutes " + seconds + " seconds";
    },
    clearGameBoard() {
      this.$refs.gameBoard.innerHTML = "";
    },
    CheckWin() {
      console.log("Checking win for level " + this.current_lvl);
      if (this.current_lvl === this.mx_lvl) {
        alert("You won the game!");
        let timeTaken = this.GetTimeTaken(this.startTime);
        console.log("Time taken to win the game: " + timeTaken);
        return;
      }

      alert("You won this level!");
      let timeTaken = this.GetTimeTaken(this.startTime);
      console.log("Time taken to win the level: " + timeTaken);
      this.TotalTime.push(timeTaken);
      this.current_lvl += 1;
      this.clearGameBoard();
      this.shuffledEmojiList = this.shuffleArray(this.emojiList, this.current_lvl * 2);
      this.emojiCount = this.shuffledEmojiList.length;
      this.current_selection = [];
      this.guessedCards = 0;
      this.startTime = null;
      this.StartGame();
    },
    Box_Clicked(card) {
      if (this.isClickBlocked) return; // Step 2: Check the flag before handling the click

      if (card.classList.contains("flipped")) {
        return;
      }
      if (this.startTime === null) {
        this.startTime = new Date();
      }
      card.classList.toggle("flipped");
      this.current_selection.push(card);
      if (this.current_selection.length === 2) {
        this.isClickBlocked = true; // Step 3: Block further clicks
        if (this.current_selection[0].innerText === this.current_selection[1].innerText) {
          this.guessedCards += 2;
          this.current_selection = [];
          if (this.guessedCards === this.emojiCount) {
            setTimeout(() => {
              this.CheckWin();
              this.isClickBlocked = false; // Step 4: Re-enable clicks
            }, 200);
          } else {
            this.isClickBlocked = false; // Re-enable clicks if not all cards guessed
          }
        } else {
          setTimeout(() => {
            this.current_selection[0].classList.toggle("flipped");
            this.current_selection[1].classList.toggle("flipped");
            this.current_selection = [];
            this.isClickBlocked = false; // Step 4: Re-enable clicks
          }, 500);
        }
      } else {
        this.isClickBlocked = false;
      }
    },
    StartGame() {
      this.shuffledEmojiList = this.shuffleArray(this.emojiList, this.current_lvl * 2);
      this.emojiCount = this.shuffledEmojiList.length;
      for (let i = 0; i < this.shuffledEmojiList.length; i++) {
        const card = document.createElement("div");
        card.className = "game_card";
        card.innerText = this.shuffledEmojiList[i];
        this.$refs.gameBoard.appendChild(card);
        card.addEventListener("click", () => this.Box_Clicked(card));
      }
    },
  },
  mounted() {
    this.StartGame();
  },
};
</script>

<style>
:root {
  --container-color: green;
  --game-card-bg-color: #f1f1f1;
  --game-card-backdrop-color: lightgreen;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#memory_game_container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: var(--container-color);
  padding: 40px 60px;
}

#memory_game {
  display: flex;
  flex-wrap: wrap;
  width: 440px;
  height: 440px;
  gap: 10px;
  transform-style: preserve-3d;
  perspective: 500px;
}

.game_card {
  position: relative;
  width: 100px;
  height: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 3em;
  background: var(--game-card-bg-color);
  transition: 0.25s;
  transform: rotateY(180deg);
}
.game_card.flipped {
  transform: rotateY(0deg);
}
.game_card.flipped::after {
  opacity: 0;
}

.game_card::after {
  content: "";
  position: absolute;
  inset: 0;
  background: var(--game-card-backdrop-color);
  opacity: 1;
  transition: 0.25s;
  transform: rotateY(0deg);
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
