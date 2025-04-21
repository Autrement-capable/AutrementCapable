<template>
  <MetierPage
    :metierName="metierData.name"
    :description="metierData.description"
    :videoSrc="metierData.video"
    :posterSrc="metierData.poster"
    :skills="metierData.skills"
    :workEnvironment="metierData.environment"
    :jobDetails="metierData.details"
    :nextRoute="'JardinerCard'"
  />
</template>

<script>
import MetierPage from '@/views/MetierPage.vue'

export default {
  components: { MetierPage },
  data() {
    return {
      metierData: {
        name: 'Soudeur/Soudeuse',
        description:
          'La soudeuse ou le soudeur assemble, par fusion ou par apport de métal, les différents éléments...',
        video: '/videos/Soudeur_Soudeuse.mp4',
        poster: '/images/Soudeur_Cover.png',
        skills: [
          'Précision et minutie',
          'Maîtrise des techniques de soudure',
          'Bonne condition physique',
          'Respect des règles de sécurité',
        ],
        environment:
          "Les soudeurs travaillent dans divers environnements : chantiers de construction, usines de fabrication, secteurs de l'aéronautique ou encore en maintenance.",
        details: `
                    <h2 style="margin: 10px; text-align: center;">Étudier le plan</h2>
                    <p> Du chauffe-eau à la centrale nucléaire, le soudage permet d'assembler les pièces métalliques d'objets de toutes tailles et de toutes natures. Selon les entreprises, la même personne peut être amenée à fabriquer les pièces du produit à réaliser. Elle utilise alors les techniques de découpe des métaux, de déformation (par emboutissage, perçage...). Dans tous les cas, le travail de soudage démarre par la prise de consignes auprès de la hiérarchie, de l'étude du plan d'ensemble de l'ouvrage à réaliser, et des parties à assembler.</p>
                    <h2 style="margin: 10px; text-align: center;">Préparer le travail</h2>
                    <p> Les documents techniques indiquent le procédé à utiliser (soudage à l'arc, semi-automatique, avec fil fourré, plasma...) et les caractéristiques des métaux utilisés (acier, inox, cuivre, alliage), susceptibles de subir des déformations, par exemple. Avant de procéder à la soudure, il faut préparer la surface par ponçage, grattage, etc. Sur un chantier, il faut aussi se cordonner avec les autres corps de métiers.</p>
                    <h2 style="margin: 10px; text-align: center;">Régler les machines et contrôler la qualité</h2>
                    <p> Après l'installation et le réglage de leur matériel, les soudeurs revêtent les équipements de protection (gants, masque à verre filtrant...) puis attaquent les opérations de soudage proprement dites. Dernière étape : contrôler la qualité du travail effectué pour éviter toute fuite ou casse.</p>
                `,
      },
    }
  },
}
</script>
