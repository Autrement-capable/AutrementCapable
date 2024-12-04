import { createRouter, createWebHistory } from "vue-router";
import StartButton from "../components/StartButton.vue";
import AccountCreation from "../components/AccountCreation.vue";
import Explanation from "../components/Explanation.vue";
import LoginPage from "../components/LoginPage.vue";
import PersonalTest from "../components/PersonalTest.vue";
import UserQuestionnaire from "../components/Questionnaire.vue";
import GameSpeed from "../components/GameSpeed.vue";
import GameShape from "../components/GameShape.vue";
import GameMemory from "../components/GameMemory.vue";
import CompDashboard from "../components/CompDashboard.vue";
import CvPreview from "../components/CvPreview.vue";
import PostsList from '../components/forum/PostsList.vue';
import Post from '../components/forum/PostPage.vue';
import Forum from '../components/forum/ForumPage.vue';
import CoursePage from "../components/CoursePage.vue";
import ShapeSequenceGame from "../components/ShapeSequenceGame.vue";

const routes = [
  {
    path: "/",
    name: "StartButton",
    component: StartButton,
  },
  {
    path: "/account-creation",
    name: "AccountCreation",
    component: AccountCreation,
  },
  {
    path: "/explanation",
    name: "Explanation",
    component: Explanation,
  },
  {
    path: "/login",
    name: "Login",
    component: LoginPage,
  },
  {
    path: "/personal-test",
    name: "PersonalTest",
    component: PersonalTest,
  },
  {
    path: "/questionnaire",
    name: "Questionnaire",
    component: UserQuestionnaire,
  },
  {
    path: "/game-speed",
    name: "GameSpeed",
    component: GameSpeed,
  },
  {
    path: "/game-shape",
    name: "GameShape",
    component: GameShape,
  },
  {
    path: "/game-memory",
    name: "GameMemory",
    component: GameMemory,
  },
  {
    path: "/shape-sequence-game",
    name: "ShapeSequenceGame",
    component: ShapeSequenceGame,
  },
  {
    path: "/dashboard",
    name: "CompDashboard",
    component: CompDashboard,
  },
  {
    path: "/cv-preview",
    name: "CvPreview",
    component: CvPreview,
  },
  {
    path: '/forum',
    name: 'forum',
    component: Forum,
  },
  {
    path: '/forum/posts/:category/',
    name: 'postsList',
    component: PostsList,
    props: true
  },
  {
    path: '/forum/posts/:category/:id',
    name: 'post',
    component: Post,
    props: true
  },
  {
    path: "/courses",
    name: "CoursePage",
    component: CoursePage,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
