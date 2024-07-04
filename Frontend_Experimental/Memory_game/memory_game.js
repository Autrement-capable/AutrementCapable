// Util functions for the memory game
function shuffleArray(array, nb_pairs = 8) {
  // get the first nb_pairs elements of the array
  array = array.slice(0, nb_pairs * 2);
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

//Generate the game board
const gameBoard = document.getElementById("memory_game");

function clearGameBoard() {
  gameBoard.innerHTML = "";
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

const mx_lvl = 4;

let current_lvl = 1;

let shuffledEmojiList = shuffleArray(emojiList, current_lvl * 2);

let emojiCount = shuffledEmojiList.length;

let current_selection = []; // should only max 2 elements

let guessedCards = 0; // Number of flipped cards

let startTime = null;

let TotalTime = []; // for each level there is an element in the arrays (4 for now)

function CheckWin(startTime) {
  console.log("Checking win for level " + current_lvl);
  if (current_lvl === mx_lvl) {
    alert("You won the game!");
    let timeTaken = GetTimeTaken(startTime);
    console.log("Time taken to win the game: " + timeTaken);
    return;
  }

  alert("You won this level!");
  let timeTaken = GetTimeTaken(startTime);
  console.log("Time taken to win the level: " + timeTaken);
  TotalTime.push(timeTaken);
  current_lvl += 1;
  clearGameBoard();
  shuffledEmojiList = shuffleArray(emojiList, current_lvl * 2);
  emojiCount = shuffledEmojiList.length;
  current_selection = [];
  guessedCards = 0;
  startTime = null;
  StartGame();
}

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
          CheckWin(startTime);
        }, 200);
      }
    }
    // clear the previous selection if full and not matched
    else {
      setTimeout(() => {
        current_selection[0].classList.toggle("flipped");
        current_selection[1].classList.toggle("flipped");
        current_selection = [];
      }, 500);
    }
  }
}

function StartGame() {
  for (let i = 0; i < shuffledEmojiList.length; i++) {
    const card = document.createElement("div");
    card.className = "game_card";
    card.innerText = shuffledEmojiList[i];
    gameBoard.appendChild(card);
    card.addEventListener("click", Box_Clicked);
  }
}

StartGame();
