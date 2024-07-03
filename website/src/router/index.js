import { createRouter, createWebHistory } from 'vue-router'
import StartButton from '../components/StartButton.vue'
import AccountCreation from '../components/AccountCreation.vue'
import Explanation from '../components/Explanation.vue'
import PersonalTest from '../components/PersonalTest.vue'
import UserQuestionnaire from '../components/Questionnaire.vue'
import GameSpeed from '../components/GameSpeed.vue'
import GameShape from '../components/GameShape.vue'
import GameMemory from '../components/GameMemory.vue'
import CompDashboard from '../components/CompDashboard.vue'

const routes = [
  {
    path: '/',
    name: 'StartButton',
    component: StartButton
  },
  {
    path: '/account-creation',
    name: 'AccountCreation',
    component: AccountCreation
  },
  {
    path: '/explanation',
    name: 'Explanation',
    component: Explanation
  },
  {
    path: '/personal-test',
    name: 'PersonalTest',
    component: PersonalTest
  },
  {
    path: '/questionnaire',
    name: 'Questionnaire',
    component: UserQuestionnaire
  },
  {
    path: '/game-speed',
    name: 'GameSpeed',
    component: GameSpeed
  },
  {
    path: '/game-shape',
    name: 'GameShape',
    component: GameShape
  },
  {
    path: '/game-memory',
    name: 'GameMemory',
    component: GameMemory
  },
  {
    path: '/dashboard',
    name: 'CompDashboard',
    component: CompDashboard
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
