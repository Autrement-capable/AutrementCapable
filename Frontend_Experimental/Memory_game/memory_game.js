// Util functions for the memory game
function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    // Generate random number between 0 and i (inclusive)
    const j = Math.floor(Math.random() * (i + 1));
    // Swap elements at indices i and j
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

//gets the time that the game took to finish should return a string say minites and seconds (aka 2 minutes 30 seconds)
function GetTimeTaken(startTime) {
  let endTime = new Date();
  let timeDiff = endTime - startTime;
  let seconds = Math.floor(timeDiff / 1000);
  let minutes = Math.floor(seconds / 60);
  seconds = seconds % 60;
  return minutes + " minutes " + seconds + " seconds";
}

function WinGame(startTime) {
  alert("You won the game!");
  let timeTaken = GetTimeTaken(startTime);
  console.log("Time taken to win the game: " + timeTaken);
}

// Initialize the variables
const emojiList = [
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
];

let shuffledEmojiList = shuffleArray(emojiList);

const emojiCount = emojiList.length;

let current_selection = []; // should only max 2 elements

let guessedCards = 0; // Number of flipped cards

let startTime = null;

//Generate the game board
const gameBoard = document.getElementById("memory_game");

// On click event for the game card
function Box_Clicked() {
  // if flipped, do nothing
  if (this.classList.contains("flipped")) {
    return;
  }
  if (startTime === null) {
    startTime = new Date();
  }
  this.classList.toggle("flipped");
  current_selection.push(this);
  if (current_selection.length === 2) {
    if (current_selection[0].innerText === current_selection[1].innerText) {
      guessedCards += 2;
      current_selection = [];
      if (guessedCards === emojiCount) {
        setTimeout(() => {
          WinGame(startTime);
        }, 200);
      }
    }
    // clear the previous selection if full and not matched
    else {
      setTimeout(() => {
        current_selection[0].classList.toggle("flipped");
        current_selection[1].classList.toggle("flipped");
        current_selection = [];
      }, 200);
    }
  }
}
// say the score when the user tries to leave the page
window.addEventListener("beforeunload", function (e) {
  if (guessedCards != emojiCount) {
    console.log(
      "You got " +
        guessedCards / 2 +
        " pairs right. Your time" +
        GetTimeTaken(startTime)
    );
  }
});

for (let i = 0; i < shuffledEmojiList.length; i++) {
  const card = document.createElement("div");
  card.className = "game_card";
  card.innerText = shuffledEmojiList[i];
  gameBoard.appendChild(card);
  card.addEventListener("click", Box_Clicked);
}
