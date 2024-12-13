<template>
    <div class="metier-container">
        <h1>{{ metierName }}</h1>
        <p class="description">{{ description }}</p>

        <div class="video-container">
            <video controls>
                <source :src="videoSrc" type="video/mp4" />
                Votre navigateur ne supporte pas la vidéo.
            </video>
        </div>

        <div class="bubbles-container">
            <div class="bubble">Niveau minimum d'accès: CAP ou équivalent</div>
            <div class="bubble">Salaire débutant: 1802 €</div>
            <div class="bubble">Statut: Statut salarié</div>
        </div>
    </div>
</template>

<script>
export default {
    name: "MetierPage",
    data() {
        return {
            metierName: "Soudeur/Soudeuse",
            description:
                "La soudeuse ou le soudeur assemble, par fusion ou par apport de métal, les différents éléments composant un chauffe-eau, un avion, un pont de plateforme, la tuyauterie d'un barrage dans le cadre d'un chantier de travaux publics... Précision et respect des règles de sécurité sont indispensables.",
            videoSrc: "/videos/Soudeur_Soudeuse.mp4",
        };
    },
};
</script>

<style scoped>
.metier-container {
    font-family: Arial, sans-serif;
    margin: 20px auto 0;
    text-align: center;
    background-color: #e7e7e7;
    border: 1.5px solid black;
    border-radius: 20px;
    padding: 10px 20px;
    max-width: 700px;
}

.description {
    font-size: 1rem;
    line-height: 1.8;
    max-width: 800px;
    margin: 20px auto 0;
}

.video-container {
    margin: 20px auto;
    max-width: 800px;
}

video {
    width: 90%;
    border: 2px solid #ddd;
    border-radius: 8px;
}

.bubbles-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: left;
    gap: 10px;
    margin-top: 20px;
}

.bubble {
    background-color: white;
    border: 1.5px solid black;
    border-radius: 20px;
    padding: 10px 20px;
    font-size: 1rem;
    color: black;
    text-align: center;
}

.back-link {
    display: block;
    margin-top: 20px;
    text-decoration: none;
    font-size: 1rem;
    color: #007bff;
}

.back-link:hover {
    text-decoration: underline;
}
</style>
