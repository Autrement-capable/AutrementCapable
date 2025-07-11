import { createRouter, createWebHistory } from 'vue-router'
import AuthService from '@/services/AuthService'
import LoginPage from '@/views/LoginPage.vue'
import Onboarding from '@/views/Onboarding.vue'
import FormationPage from '@/views/FormationPage.vue'
import Dashboard from '@/views/Dashboard.vue'
import UserProfile from '@/views/UserProfile.vue'
import DebugPage from '@/views/DebugPage.vue'

// Scenarios
import ScenarioList from '@/views/skillGames/ScenarioMenuGame.vue'
import ScenarioPage from '@/views/skillGames/ScenarioGame.vue'
import ResultsPage from '@/views/ResultsPage.vue'

// Hard skills mini games
import GameSpeed from '@/views/skillGames/GameSpeed.vue'
import ShapeSequenceGame from '@/views/skillGames/ShapeSequenceGame.vue'
import TinderMetiers from '@/views/skillGames/JobsGame.vue'
import SoudeurCard from '@/components/jobsCards/SoudeurCard.vue'
import JardinerCard from '@/components/jobsCards/JardinerCard.vue'
import CoiffeurCard from '@/components/jobsCards/CoiffeurCard.vue'
import SkillsWheelPage from '@/views/skillGames/SkillsWheelGame.vue'
import Environment from '@/views/skillGames/EnvironmentGame.vue'
import ProfilePage from '@/views/ProfilePage.vue'

// Routes qui nécessitent une authentification
const protectedRoutes = [
  'Dashboard',
  'UserProfile',
  'ProfilePage',
  'GameSpeed',
  'ShapeSequenceGame',
  'TinderMetiers',
  'SoudeurCard',
  'JardinerCard',
  'CoiffeurCard',
  'Environment',
  'ScenarioList',
  'ScenarioPage',
  'ResultsPage',
  'FormationPage',
  'SkillsWheelPage',
  'DebugPage',
]

const routes = [
  {
    path: '/',
    redirect: { name: 'Login' },
    name: 'Home',
  },
  {
    path: '/onboarding',
    name: 'Onboarding',
    component: Onboarding,
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
  },
  {
    path: '/user-profile',
    name: 'UserProfile',
    component: UserProfile,
  },
  {
    path: '/profile-page',
    name: 'ProfilePage',
    component: ProfilePage,
  },
  {
    path: '/game-speed',
    name: 'GameSpeed',
    component: GameSpeed,
  },
  {
    path: '/shape-sequence-game',
    name: 'ShapeSequenceGame',
    component: ShapeSequenceGame,
  },
  {
    path: '/metiers',
    name: 'TinderMetiers',
    component: TinderMetiers,
  },
  {
    path: '/metier/soudeur',
    name: 'SoudeurCard',
    component: SoudeurCard,
  },
  {
    path: '/metier/jardinier',
    name: 'JardinerCard',
    component: JardinerCard,
  },
  {
    path: '/metier/coiffeur',
    name: 'CoiffeurCard',
    component: CoiffeurCard,
  },
  {
    path: '/environment',
    name: 'Environment',
    component: Environment,
  },
  {
    path: '/scenarios',
    name: 'ScenarioList',
    component: ScenarioList,
  },
  {
    path: '/scenarios/:urlName',
    name: 'ScenarioPage',
    component: ScenarioPage,
    props: true,
  },
  {
    path: '/resultats',
    name: 'ResultsPage',
    component: ResultsPage,
  },
  {
    path: '/formation',
    name: 'FormationPage',
    component: FormationPage,
  },
  {
    path: '/roue-des-competences',
    name: 'SkillsWheelPage',
    component: SkillsWheelPage,
  },
  {
    path: '/debug',
    name: 'DebugPage',
    component: DebugPage,
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

// Navigation guard global pour vérifier l'authentification
router.beforeEach(async (to, from, next) => {
  // Vérifier si la route nécessite une authentification
  if (protectedRoutes.includes(to.name)) {
    try {
      // Vérifier si l'utilisateur est authentifié
      const authStatus = await AuthService.isAuthenticated()

      if (authStatus.authenticated) {
        // Utilisateur authentifié, laisser passer
        next()
      } else {
        // Utilisateur non authentifié, rediriger vers la page de connexion
        console.log('Accès refusé - Utilisateur non authentifié')
        next({
          name: 'Login',
          query: { redirect: to.fullPath }, // Sauvegarder la destination pour rediriger après connexion
        })
      }
    } catch (error) {
      console.error(
        "Erreur lors de la vérification de l'authentification:",
        error,
      )
      // En cas d'erreur, rediriger vers la page de connexion pour sécurité
      next({
        name: 'Login',
        query: { redirect: to.fullPath },
      })
    }
  } else {
    // Route publique, laisser passer
    next()
  }
})

export default router
