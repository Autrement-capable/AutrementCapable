<template>
    <div class="metier-container" :class="{ expanded: isExpanded }">
        <h1>{{ metierName }}</h1>
        <div class="video-container">
            <video controls :poster="posterSrc">
                <source :src="videoSrc" type="video/mp4" />
                Votre navigateur ne supporte pas la vidéo.
            </video>
            <p @click="toggleExpand" class="expand-link">
                {{ isExpanded ? "Afficher moins" : "En savoir plus ?" }}
            </p>
        </div>

        <p class="description">{{ description }}</p>

        <div v-if="isExpanded" class="additional-info">
            <h2 style="text-align: center;">Compétences requises</h2>
            <ul>
                <li v-for="(skill, index) in skills" :key="index" style="margin: 20px;">
                    {{ skill }}
                </li>
            </ul>
            <h2 style="text-align: center;">Environnement de travail</h2>
            <p>{{ workEnvironment }}</p>
            <h2 style="text-align: center;">Le métier</h2>
            <div v-html="jobDetails"></div>
        </div>

        <div class="button-container">
            <button @click="onLike">👍 J'aime</button>
            <button @click="onNeutral">🤔 Je ne sais pas</button>
            <button @click="onDislike">👎 Je n'aime pas</button>
        </div>
    </div>
    <div v-if="isExpanded" class="extra-space"></div>
</template>

<script>
export default {
    name: "MetierPage",
    props: {
        metierName: { type: String, required: true },
        description: { type: String, required: true },
        videoSrc: { type: String, required: true },
        posterSrc: { type: String, required: true },
        skills: { type: Array, required: true },
        workEnvironment: { type: String, required: true },
        jobDetails: { type: String, required: true },
        nextRoute: { type: String, default: null },
    },
    data() {
        return {
            isExpanded: false,
        };
    },
    methods: {
        toggleExpand() {
            this.isExpanded = !this.isExpanded;
        },
        navigateToNextMetier() {
            if (this.nextRoute) {
                this.$router.push({ name: this.nextRoute });
            }
        },

        onLike() {
            console.log("User likes this métier!");
            this.navigateToNextMetier();
        },
        onNeutral() {
            console.log("User is neutral about this métier.");
            this.navigateToNextMetier();
        },
        onDislike() {
            console.log("User dislikes this métier.");
            this.navigateToNextMetier();
        },
    },
};
</script>

<style scoped>
.extra-space {
    height: 200px; /* Hauteur ajoutée pour permettre un scroll plus bas */
    background-color: transparent;
}

.metier-container {
    font-family: Arial, sans-serif;
    margin: 20px auto 0;
    text-align: center;
    background-color: #e7e7e7;
    border: 1.5px solid black;
    border-radius: 20px;
    padding: 10px 20px;
    max-width: 700px;
    transition: all 0.3s ease;
}

.metier-container.expanded {
    max-width: 900px; /* La page s'agrandit */
    background-color: #e7e7e7;
    border-color: #000000;
}

.description {
    font-size: 1rem;
    line-height: 1.8;
    max-width: 800px;
    margin: 30px auto 0;
}

.video-container {
    margin: 20px auto;
    max-width: 800px;
}

.additional-info {
    margin-top: 20px;
    text-align: left;
    font-size: 1rem;
    line-height: 1.6;
}

.additional-info h2 {
    margin-top: 10px;
    color: #000000;
}

.button-container button {
    gap: 8px; /* Espacement entre l'emoji et le texte */
    font-size: 1rem;
    padding: 10px 20px;
    border: 1.5px solid #007bff;
    border-radius: 10px;
    background-color: #000000;
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease;
}

.button-container button:hover {
    background-color: #007bff;
    color: white;
}

video {
    width: 90%;
    border: 2px solid #ddd;
    border-radius: 8px;
}

.expand-link {
    color: #007bff;
    cursor: pointer;
    text-decoration: underline;
}

.expand-link:hover {
    color: #0056b3;
}
</style>

