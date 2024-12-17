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

        <!-- Nouvelle section qui apparaît si isExpanded est vrai -->
        <div v-if="isExpanded" class="additional-info">
            <h2>Compétences requises</h2>
            <ul>
                <li style="margin: 20px;">Précision et minutie</li>
                <li style="margin: 20px;">Maîtrise des techniques de soudure</li>
                <li style="margin: 20px;">Bonne condition physique</li>
                <li style="margin: 20px;">Respect des règles de sécurité</li>
            </ul>
            <h2>Environnement de travail</h2>
            <p>
                Les soudeurs travaillent dans divers environnements : chantiers de construction,
                usines de fabrication, secteurs de l'aéronautique ou encore en maintenance.
            </p>
            <p style="margin-top: 10px;">
                Synonymes : Opérateur / opératrice en techniques de soudage
            </p>
            <p style="margin-top: 10px;">
                Secteurs professionnels : Automobile, Bâtiment et travaux publics (btp), Construction aéronautique, ferroviaire et navale, Énergie, Mécanique
            </p>
            <p style="margin-top: 10px;">
                Centres d'intérêt : J'aime bouger, Je veux travailler de mes mains
            </p>

            <h2>Le métier</h2>
            <h2 style="margin-top: 10px;">Étudier le plan</h2>
            <p>
                Du chauffe-eau à la centrale nucléaire, le soudage permet d'assembler les pièces métalliques d'objets de toutes tailles et de toutes natures. Selon les entreprises, la même personne peut être amenée à fabriquer les pièces du produit à réaliser. Elle utilise alors les techniques de découpe des métaux, de déformation (par emboutissage, perçage...). Dans tous les cas, le travail de soudage démarre par la prise de consignes auprès de la hiérarchie, de l'étude du plan d'ensemble de l'ouvrage à réaliser, et des parties à assembler.
            </p>
            <h2 style="margin: 10px;">Préparer le travail</h2>
            <p>
                Les documents techniques indiquent le procédé à utiliser (soudage à l'arc, semi-automatique, avec fil fourré, plasma...) et les caractéristiques des métaux utilisés (acier, inox, cuivre, alliage), susceptibles de subir des déformations, par exemple. Avant de procéder à la soudure, il faut préparer la surface par ponçage, grattage, etc. Sur un chantier, il faut aussi se cordonner avec les autres corps de métiers.
            </p>
            <h2 style="margin: 10px;">Régler les machines et contrôler la qualité</h2>
            <p>
                Après l'installation et le réglage de leur matériel, les soudeurs revêtent les équipements de protection (gants, masque à verre filtrant...) puis attaquent les opérations de soudage proprement dites. Dernière étape : contrôler la qualité du travail effectué pour éviter toute fuite ou casse.
            </p>
        </div>

        <!-- Ajout d'une div vide pour "descendre plus bas" -->
        
        <div class="button-container">
            <button>J'aime</button>
            <button>Je ne sais pas</button>
            <button>Je n'aime pas</button>
        </div>
    </div>
    <div v-if="isExpanded" class="extra-space"></div>
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
            posterSrc: "/images/Soudeur_Cover.png",
            isExpanded: false, // Variable pour suivre l'état
        };
    },
    methods: {
        toggleExpand() {
            this.isExpanded = !this.isExpanded;

            // Si l'état est étendu, descendre en bas de la section
            this.$nextTick(() => {
                if (this.isExpanded && this.$refs.additionalInfo) {
                    this.$refs.additionalInfo.scrollIntoView({
                        behavior: "smooth",
                        block: "end",
                    });
                }
            });
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

.button-container {
    display: flex;
    justify-content: space-evenly;
    margin-top: 20px;
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
