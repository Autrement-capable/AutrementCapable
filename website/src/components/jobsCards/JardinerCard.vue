<template>
  <MetierPage
    :metierName="metierData.name"
    :description="metierData.description"
    :videoSrc="metierData.video"
    :posterSrc="metierData.poster"
    :skills="metierData.skills"
    :workEnvironment="metierData.environment"
    :jobDetails="metierData.details"
    :nextRoute="'CoiffeurCard'"
  />
</template>

<script>
import MetierPage from '@/views/MetierPage.vue'

export default {
  components: { MetierPage },
  data() {
    return {
      metierData: {
        name: 'Jardinier/Jardinière-paysagiste',
        description:
          'Agent du service public ou employé par une entreprise spécialisée, le jardinier-paysagiste crée, aménage et entretient les jardins privatifs ainsi que les espaces verts publics.',
        video: '/videos/Jardinier_Jardinière.mp4',
        poster: '/images/Jardinier_Cover.png',
        skills: [
          'Précision et minutie',
          'Connaissances en botanique',
          'Bonne condition physique',
          'Respect des règles de sécurité',
        ],
        environment:
          'Les jardiniers travaillent dans divers environnements : parcs, jardins privés, espaces verts urbains, domaines forestiers ou terrains de sport.',
        details: `
                    <h2 style="margin: 10px; text-align: center;">Étudier le plan d'aménagement</h2>
                    <p> Le travail commence par la prise de consignes et l'étude du plan d'aménagement des espaces verts. Le jardinier-paysagiste doit analyser les caractéristiques du terrain, le type de sol, l'exposition au soleil et les besoins en irrigation pour choisir les végétaux et les matériaux adaptés.</p>
                    
                    <h2 style="margin: 10px; text-align: center;">Préparer le terrain</h2>
                    <p> Avant la plantation, il est essentiel de préparer le terrain : labourage, désherbage, enrichissement du sol avec des engrais naturels ou du compost. Sur les chantiers d’aménagement, le jardinier doit aussi se coordonner avec d'autres professionnels tels que les maçons pour la pose de murets, terrasses ou allées.</p>
                    
                    <h2 style="margin: 10px; text-align: center;">Planter, entretenir et contrôler</h2>
                    <p> Une fois le terrain préparé, le jardinier procède à la plantation des végétaux en respectant les saisons et les besoins de chaque espèce. L'entretien des espaces verts inclut la taille, l’arrosage, la tonte, le désherbage et la fertilisation. Enfin, le jardinier vérifie régulièrement l’état général des plantations et des infrastructures pour assurer leur durabilité.</p>
                `,
      },
    }
  },
}
</script>
