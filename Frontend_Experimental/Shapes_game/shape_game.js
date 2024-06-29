//const
const color_list = [
  "red",
  "blue",
  "green",
  "yellow",
  "purple",
  "orange",
  "brown",
  "gray",
];
const shape_list = [
  "circle",
  "square",
  "triangle",
  "star",
  "rectangle",
  "oval",
  "trapezoid",
];

const max_rounds = 8; // how many rounds the game will last
const time_per_round = 2; // how many seconds the player has to remember the shape
const dup_chance = 0.5; // how likely the new shape to be same as the old shape

//DOM elements
const start_button = document.getElementById("startButton");
const game_area = document.getElementById("gameArea");
const shape_container = document.getElementById("shapeContainer");
const options = document.getElementById("options");

//variables
let old_shape = []; // pair of shape and color
let current_shape = []; // pair of shape and color
let score = 0;
let time = null;
let round = 0;

//functions
function generate_shape(old_shape, dup_chance) {
  if (old_shape.length > 0 && Math.random() < dup_chance) {
    return old_shape;
  } else {
    let shape = shape_list[Math.floor(Math.random() * shape_list.length)];
    let color = color_list[Math.floor(Math.random() * color_list.length)];
    return [shape, color];
  }
}

function getAnswer(selected_option) {
  console.log("Selected option: " + selected_option);
  // not really need but the int param should be the index - 1(param starts from 1) of this array to see that the user has selected
  const option_list = [
    "Same as before",
    "Same shape, different color",
    "Same color, different shape",
    "Totally different",
  ];
  if (selected_option > option_list.length || selected_option < 1) {
    return;
  }
  let correct_option = -1;
  if (old_shape[0] == current_shape[0] && old_shape[1] == current_shape[1]) {
    correct_option = 1;
  } else if (old_shape[0] == current_shape[0]) {
    correct_option = 2;
  } else if (old_shape[1] == current_shape[1]) {
    correct_option = 3;
  } else {
    correct_option = 4;
  }
  if (selected_option == correct_option) {
    score++;
  } else {
    console.log(
      "Wrong answer. Right answer was: " + option_list[correct_option - 1]
    );
  }
  StartGame();
}

// this is where we show the image that needs to be remembered
function generateImage() {
  return new Promise((resolve) => {
    // Wrap the function logic in a Promise
    options.classList.add("hidden");
    old_shape = generate_shape(old_shape, 0);
    // remove old classes from the shape container
    shape_container.className = "";
    shape_container.classList.add(old_shape[0]);
    shape_container.classList.add(old_shape[1]);
    // the whole reason this and next func returns a promise and the main func is async
    setTimeout(() => {
      shape_container.className = "";
      resolve(); // Resolve the promise after the timeout
    }, time_per_round * 1000); // used to time the picture show in the begining
  });
}

//this is where we show a second image and ask the player to select the correct answer
function generateOptions() {
  return new Promise((resolve) => {
    current_shape = generate_shape(old_shape, dup_chance);
    // remove old classes from the shape container
    shape_container.classList.add(current_shape[0]);
    shape_container.classList.add(current_shape[1]);
    options.classList.remove("hidden");
    resolve();
  });
}

function GameOver() {
  game_area.classList.add("hidden");
  start_button.classList.remove("hidden");
  alert("Game Over! Your score is: " + score);
  score = 0;
  round = 0;
  time = null;
  current_shape = [];
  old_shape = [];
}

//Main game loop
async function StartGame() {
  if (round >= max_rounds) {
    GameOver();
    return;
  }
  if (time == null) {
    time = new Date();
  }
  round++;
  start_button.classList.add("hidden");
  game_area.classList.remove("hidden");
  await generateImage();
  await generateOptions();
}
