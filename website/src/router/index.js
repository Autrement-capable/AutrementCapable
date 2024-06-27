import { createRouter, createWebHistory } from 'vue-router'
import StartButton from '../components/StartButton.vue'
import AccountCreation from '../components/AccountCreation.vue'
import Explanation from '../components/Explanation.vue'
import PersonalTest from '../components/PersonalTest.vue'
import UserQuestionnaire from '../components/Questionnaire.vue'

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
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
