<template>
    <div class="game-container">
        <h1>Jeu des Séquences de Formes</h1>
        <p>Regarde la séquence et clique sur la forme qui suit selon la logique.</p>

        <!-- Sequence Display -->
        <div class="sequence">
            <div v-for="(shape, index) in sequence" :key="index" class="shape-container">
                <img
                    v-if="shape !== '?'"
                    :src="getShapeImage(shape)"
                    :alt="shape"
                    class="shape"
                />
                <span v-else class="missing">?</span>
            </div>
        </div>

        
        <!-- Options Display -->
        <div class="options">
            <img
                v-for="option in options"
                :key="option"
                :src="getShapeImage(option)"
                :alt="option"
                class="option"
                @click="checkAnswer(option)"
            />
        </div>

        <p>{{ feedback }}</p>
        <button @click="restartGame">Recommencer</button>
        <button @click="MetierPage">Voir la page metier</button>
    </div>
</template>

<script>
import { ref } from "vue";

export default {
    name: "ShapeSequenceGame",
    methods: {
        MetierPage() {
            this.$router.push("/metier");
        },
    },
    setup() {
        // List of shapes with their respective image paths
        const shapes = ["square", "circle", "triangle", "rectangle"];
        const shapeImages = {
            square: require("@/assets/shapes/Square.png"),
            circle: require("@/assets/shapes/Circle.png"),
            triangle: require("@/assets/shapes/Triangle.png"),
            rectangle: require("@/assets/shapes/Rectangle.png"),
        };

        // Level configuration
        const levels = [
            { sequence: ["rectangle", "circle", "triangle", "?", "rectangle"], answer: "circle" },
            { sequence: ["rectangle", "rectangle", "triangle", "circle", "?", "rectangle", "triangle", "circle",], answer: "rectangle"},
            { sequence: ["triangle", "circle", "triangle", "?"], answer: "circle" },
            { sequence: ["circle", "rectangle", "?", "rectangle"], answer: "circle" },
            { sequence: ["square", "triangle", "square", "?", "square"], answer: "triangle" },
            { sequence: ["triangle", "triangle", "triangle", "?"], answer: "triangle" },
            { sequence: ["circle", "square", "triangle", "?", "square", "triangle"], answer: "circle" },
            { sequence: ["circle", "circle", "circle", "?"], answer: "circle" },
            { sequence: ["square", "circle", "triangle", "?", "circle", "triangle"], answer: "square" },
            { sequence: ["square", "square", "square", "?"], answer: "square" },
            { sequence: ["triangle", "square", "circle", "?", "square", "circle"], answer: "triangle" },
            { sequence: ["circle", "triangle", "triangle", "?", "triangle", "triangle"], answer: "circle" },
        ];

        // Reactive state variables
        const currentLevel = ref(0); // Start at level 0
        const sequence = ref([]);
        const options = ref([]);
        const feedback = ref("");

        // Get the image path for a shape
        const getShapeImage = (shape) => shapeImages[shape];

        // Generate options for the missing shape
        const generateOptions = (correctShape) => {
            const opts = [];
            while (opts.length < 3) {
                const shape = shapes[Math.floor(Math.random() * shapes.length)];
                if (shape !== correctShape) {
                    opts.push(shape);
                }
            }
            opts.push(correctShape); // Add correct shape
            return opts.sort(() => Math.random() - 0.5); // Shuffle options
        };

        // Start or restart the game
        const startGame = () => {
            feedback.value = "";

            if (currentLevel.value >= levels.length) {
                feedback.value = "Félicitations, vous avez terminé tous les niveaux !";
                return;
            }

            const levelConfig = levels[currentLevel.value];
            sequence.value = levelConfig.sequence;

            // Generate options including the correct answer
            const correctShape = levelConfig.answer;
            options.value = generateOptions(correctShape);
        };

        // Check the answer
        const checkAnswer = (selectedShape) => {
            const correctShape = levels[currentLevel.value].answer;
            if (selectedShape === correctShape) {
                feedback.value = "Bravo ! Passons au niveau suivant.";
                currentLevel.value++;
                setTimeout(startGame, 1000);
            } else {
                feedback.value = "Mauvaise réponse. Essaie encore !";
            }
        };

        // Restart the game
        const restartGame = () => {
            currentLevel.value = 0;
            startGame();
        };

        // Initialize the game
        startGame();

        return {
            sequence,
            options,
            feedback,
            restartGame,
            checkAnswer,
            getShapeImage,
        };
    },
};
</script>

<style scoped>
.game-container {
    align-items: center;
    font-family: Arial, sans-serif;
    text-align: center;
    margin: 100px;
}

.sequence {
    margin-top: 30px;
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
}

.shape-container {
    width: 80px;
    height: 80px;
    margin: 0 10px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.shape {
    max-width: 100%;
    max-height: 100%;
}

.options {
    padding-top: 60px;
    display: center;
    justify-content: center;
    margin-top: 20px;
}

.option {
    width: 80px;
    height: 80px;
    margin: 0 10px;
    cursor: pointer;
    transition: transform 0.2s;
}

.option:hover {
    transform: scale(1.2);
}

.missing {
    font-size: 2rem;
    font-weight: bold;
    color: gray;
}
</style>
