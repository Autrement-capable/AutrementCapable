import { Application, Assets, AnimatedSprite } from "pixi.js";

const mapData = [
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 1, 1, 0, 0, 0],
  [0, 0, 0, 1, 1, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
];

export async function createPixiApp(containerId) {

    const app = new Application();
    await app.init({ background: "#000000", resizeTo: window });
    const container = document.getElementById(containerId);

    container.appendChild(app.canvas);

    const spritesheet = await Assets.load("../../public/slime.json");

    // Generate all the Textures asynchronously
    await spritesheet.parse();
    
    // spritesheet is ready to use!
    const anim = new AnimatedSprite(spritesheet.animations.slime);
    
    // set the animation speed
    anim.animationSpeed = 0.1666;
    // play the animation on a loop
    anim.play();
    // add it to the stage to render
    app.stage.addChild(anim);
};