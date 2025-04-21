import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '@/views/LoginPage.vue'
import Onboarding from '@/views/Onboarding.vue'
import Environment from '@/views/Environment.vue'
import FormationPage from '@/views/FormationPage.vue'
import SkillsWheelPage from '@/views/SkillsWheelPage.vue'
import Dashboard from '@/views/Dashboard.vue'
import UserProfile from '@/views/UserProfile.vue'

// Scenarios
import ScenarioList from '@/views/ScenarioList.vue'
import ScenarioPage from '@/views/ScenarioPage.vue'
import ResultsPage from '@/views/ResultsPage.vue'

// Hard skills mini games
import GameSpeed from '@/views/skillGames/GameSpeed.vue'
import GameShape from '@/views/skillGames/GameShape.vue'
import ShapeSequenceGame from '@/views/skillGames/ShapeSequenceGame.vue'

// Tinder des metiers
import TinderMetiers from '@/components/JobsComponent.vue'
import MetierPage from '@/views/MetierPage.vue'
import SoudeurCard from '@/components/jobsCards/SoudeurCard.vue'
import JardinerCard from '@/components/jobsCards/JardinerCard.vue'
import CoiffeurCard from '@/components/jobsCards/CoiffeurCard.vue'

const routes = [
  {
    path: '/',
    name: 'onboarding',
    component: Onboarding,
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
    path: '/game-speed',
    name: 'GameSpeed',
    component: GameSpeed,
  },
  {
    path: '/game-shape',
    name: 'GameShape',
    component: GameShape,
  },
  {
    path: '/shape-sequence-game',
    name: 'ShapeSequenceGame',
    component: ShapeSequenceGame,
  },
  {
    path: '/metier',
    name: 'TinderMetiers',
    component: TinderMetiers,
  },
  {
    path: '/metier/:metierId',
    name: 'MetierPage',
    component: MetierPage,
    props: true,
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
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
