import { Application, Assets, Sprite } from "pixi.js";

export async function createPixiApp(containerId: string) {
  const app = new Application();
  await app.init({ background: "#1099bb", resizeTo: window });
  

  const container = document.getElementById(containerId);
  if (!container) {
    console.error(`Element #${containerId} not found!`);
    return;
  }
  container.appendChild(app.canvas);

  const but_texture = await Assets.load("/assets/button.png");
  const but = new Sprite(but_texture);
  but.anchor.set(0.5);
  but.position.set(app.screen.width / 2, app.screen.height / 2 + 200);
  but.interactive = true;
  app.stage.addChild(but);

  but.on("pointerdown", () => {
    console.log("Button clicked!");
  });
}
