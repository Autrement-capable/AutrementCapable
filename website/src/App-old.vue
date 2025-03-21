<template>
  <div id="app">
    <!-- Header Section -->
    <section class="header">
      <div class="header-content">
        <h1>Libérez votre potentiel avec Autrement Capable</h1>
        <p>
          L'Association Autrement Capable offre une solution digitale accessible
          à 93% pour les jeunes avec des troubles du neurodéveloppement. Notre
          plateforme soutient les aidants et les professionnels de l'éducation
          et du soin pour aider ces jeunes à se découvrir, à renforcer leur
          confiance en eux, à trouver leur place et à créer leur avenir.
        </p>
        <button>Essayer maintenant</button>
      </div>
      <div class="header-images">
        <!-- Place images or illustrations here -->
      </div>
    </section>

    <!-- Stats Section -->
    <section class="stats">
      <div class="stat">
        <h2>250+</h2>
        <p>Cours avec nos meilleurs mentors</p>
      </div>
      <div class="stat">
        <h2>1000+</h2>
        <p>Utilisateurs satisfaits</p>
      </div>
      <div class="stat">
        <h2>15+</h2>
        <p>Mentors disponibles</p>
      </div>
      <div class="stat">
        <h2>2400+</h2>
        <p>Étudiants actifs</p>
      </div>
    </section>

    <!-- Courses Section -->
    <section class="courses">
      <h2>Réalisations de cette semaine</h2>
      <div class="course-list">
        <div class="course" v-for="index in 5" :key="index">
          <p>Astrology</p>
          <p>11 Courses</p>
        </div>
      </div>
      <button>Voir Plus</button>
    </section>

    <!-- Featured Courses Section -->
    <section class="featured-courses">
      <h2>Les Meilleures Formations pour Vous</h2>
      <div class="course-list">
        <div class="course" v-for="index in 5" :key="index">
          <p>Ronald Richards</p>
          <p>UI/UX Designer</p>
          <p>4.9 ☆ 2400 Students</p>
        </div>
      </div>
      <button>Voir Plus</button>
    </section>

    <!-- Testimonials Section -->
    <section class="testimonials">
      <h2>Ce que Nos Utilisateurs Disent de Nous</h2>
      <div class="testimonial">
        <blockquote>
          "Grâce à Autrement Capable, j'ai découvert mes forces et mes
          passions. Je me sens beaucoup plus confiant pour choisir mon avenir."
        </blockquote>
        <p>- Lucas, 16 ans</p>
      </div>
      <div class="testimonial">
        <blockquote>
          "L'application Autrement Capable m'a vraiment aidé à comprendre ce
          que je veux faire plus tard. Maintenant, j'ai un plan clair pour mon
          futur !"
        </blockquote>
        <p>- Emma, 15 ans</p>
      </div>
      <div class="testimonial">
        <blockquote>
          "Autrement Capable a été un outil incroyable pour ma fille. Elle se
          sent plus valorisée et a enfin trouvé sa voie. Merci pour cette aide
          précieuse !"
        </blockquote>
        <p>- Sophie, maman de Clara, 14 ans</p>
      </div>
    </section>

    <!-- Expert Collaboration Section -->
    <section class="expert-collaboration">
      <h2>Collaboration avec Psychologues, Éducateurs et Professionnels pour une Inclusion Réussie</h2>
      <button>Essayer Autrement Capable</button>
    </section>

    <!-- Footer Section -->
    <footer class="footer">
      <p>
        Nous proposons une solution digitale inclusive pour aider les jeunes en
        situation de handicap à se découvrir, à renforcer leur confiance en
        eux, et à choisir leur avenir.
      </p>
      <div class="footer-links">
        <div>
          <h3>Aide</h3>
          <ul>
            <li>Nous Contacter</li>
            <li>Derniers Articles</li>
            <li>FAQ</li>
          </ul>
        </div>
        <div>
          <h3>Programmes</h3>
          <ul>
            <li>Art & Design</li>
            <li>Business</li>
            <li>Languages</li>
          </ul>
        </div>
        <div>
          <h3>Nous contacter</h3>
          <ul>
            <li>Adresse: 123 rue Pesquet, R7 75001</li>
            <li>Tel: +33 6 45 67 89 00</li>
            <li>Mail: mail@AutrementCapable.com</li>
          </ul>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style scoped>
/* Header styles */
.header {
  /* Styles for the header section */
}
.header-content {
  /* Styles for header content */
}

/* Stats Section styles */
.stats {
  display: flex;
  justify-content: space-around;
}

/* Courses Section styles */
.courses, .featured-courses {
  padding: 20px;
  text-align: center;
}

/* Testimonials Section styles */
.testimonials {
  padding: 20px;
  background-color: #f9f9f9;
  text-align: center;
}

.testimonial {
  margin-bottom: 20px;
}

/* Expert Collaboration Section styles */
.expert-collaboration {
  padding: 20px;
  text-align: center;
  background-color: #e0e0e0;
}

/* Footer styles */
.footer {
  background-color: #333;
  color: #fff;
  padding: 20px;
  text-align: center;
}

.footer-links {
  display: flex;
  justify-content: space-around;
}
</style>
