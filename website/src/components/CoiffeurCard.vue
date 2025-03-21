<template>
    <MetierPage
        :metierName="metierData.name"
        :description="metierData.description"
        :videoSrc="metierData.video"
        :posterSrc="metierData.poster"
        :skills="metierData.skills"
        :workEnvironment="metierData.environment"
        :jobDetails="metierData.details"
        :nextRoute="'SoudeurCard'"
    />
</template>

<script>
import MetierPage from "@/components/MetierPage.vue";

export default {
    components: { MetierPage },
    data() {
        return {
            metierData: {
                name: "Coiffeur/Coiffeuse",
                description:
                    "Professionnel du secteur de la beauté, le coiffeur ou la coiffeuse réalise des coupes, des colorations et des soins capillaires. Il ou elle conseille également les clients sur l'entretien et le style de leurs cheveux.",
                video: "/videos/Coiffeur_Coiffeuse.mp4",
                poster: "/images/Coiffeur_Cover.png",
                skills: [
                    "Précision et minutie",
                    "Créativité et sens de l'esthétique",
                    "Bonne capacité d'écoute",
                    "Respect des règles d'hygiène et de sécurité",
                ],
                environment:
                    "Les coiffeurs travaillent dans différents environnements : salons de coiffure, centres de beauté, studios de mode ou parfois à domicile.",
                details: `
                    <h2 style="margin: 10px; text-align: center;">Accueillir et conseiller le client</h2>
                    <p> Le travail commence par l'accueil du client. Le coiffeur écoute ses attentes et évalue la nature des cheveux afin de proposer la coupe, la coloration ou le soin le plus adapté. Le conseil personnalisé est essentiel pour garantir la satisfaction du client.</p>

                    <h2 style="margin: 10px; text-align: center;">Préparer et réaliser la prestation</h2>
                    <p> Avant de procéder à la coupe ou au soin, le coiffeur prépare le matériel (peignes, ciseaux, produits capillaires) et installe le client confortablement. La réalisation de la prestation peut inclure des techniques variées : coupe, brushing, coloration, mèches ou coiffure événementielle. Chaque étape est réalisée avec précision et professionnalisme.</p>

                    <h2 style="margin: 10px; text-align: center;">Entretenir le matériel et les locaux</h2>
                    <p> Après chaque prestation, le coiffeur nettoie et désinfecte les outils et surfaces de travail pour garantir un environnement hygiénique. L'entretien régulier du matériel et des locaux permet de respecter les normes d'hygiène et de sécurité en vigueur.</p>
                `,
            },
        };
    },
};
</script>
