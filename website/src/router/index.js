import { createRouter, createWebHistory } from "vue-router";
import StartButton from "../components/StartButton.vue";
import AccountCreation from "../components/AccountCreation.vue";
import Explanation from "../components/Explanation.vue";
import LoginPage from "../components/LoginPage.vue";
import PersonalTest from "../components/PersonalTest.vue";
import UserQuestionnaire from "../components/Questionnaire.vue";
// import GameLogic from "../components/GameLogic.vue";
import GameSpeed from "../components/GameSpeed.vue";
import GameShape from "../components/GameShape.vue";
import GameMemory from "../components/GameMemory.vue";
// import CompDashboard from "../components/CompDashboard.vue";
import CvPreview from "../components/CvPreview.vue";
import PostsList from "../components/forum/PostsList.vue";
import Post from "../components/forum/PostPage.vue";
import Forum from "../components/forum/ForumPage.vue";
import CoursePage from "../components/CoursePage.vue";
import ShapeSequenceGame from "../components/ShapeSequenceGame.vue";
import MetierCard from "../components/MetierPage.vue";
import SoudeurCard from "../components/SoudeurCard.vue";
import JardinerCard from "@/components/JardinerCard.vue";
import CoiffeurCard from "@/components/CoiffeurCard.vue";
import Environment from "@/components/Environment.vue";
import ScenarioList from "@/components/ScenarioList.vue";
import ScenarioPage from "@/components/ScenarioPage.vue";
import GameDashboard from '@/components/GameDashboard.vue';
import HomePage from '@/components/HomePage.vue';
import GamePage from '@/components/GamePage.vue';
import ResultsPage from '@/components/ResultsPage.vue';
import FormationPage from "@/components/FormationPage.vue";
import RewardsPage from "@/components/RewardsPage.vue";
import SkillsWheelPage from "@/components/SkillsWheelPage.vue";
import ImmersiveDashboard from "@/components/ImmersiveDashboard.vue";
import UserProfile from "@/views/UserProfile.vue";

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
    path: "/immersive-dashboard",
    name: "ImmersiveDashboard",
    component: ImmersiveDashboard,
  },
  {
    path: "/home-page",
    name: "HomePage",
    component: HomePage,
  },
  {
    path: "/user-profile",
    name: "UserProfile",
    component: UserProfile,
  },
  {
    path: "/game-page",
    name: "GamePage",
    component: GamePage,
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
    path: "/cv-preview",
    name: "CvPreview",
    component: CvPreview,
  },
  {
    path: "/forum",
    name: "forum",
    component: Forum,
  },
  {
    path: "/forum/posts/:category/",
    name: "postsList",
    component: PostsList,
    props: true,
  },
  {
    path: "/forum/posts/:category/:id",
    name: "post",
    component: Post,
    props: true,
  },
  {
    path: "/courses",
    name: "CoursePage",
    component: CoursePage,
  },
  {
    path: "/metier/:metierId",
    name: "MetierCard",
    component: MetierCard,
    props: true,
  },
  {
    path: "/metier/soudeur",
    name: "SoudeurCard",
    component: SoudeurCard,
  },
  {
    path: "/metier/jardinier",
    name: "JardinerCard",
    component: JardinerCard,
  },
  {
    path: "/metier/coiffeur",
    name: "CoiffeurCard",
    component: CoiffeurCard,
  },
  {
    path: "/environment",
    name: "Environment",
    component: Environment,
  },
  {
    path: "/scenarios",
    name: "ScenarioList",
    component: ScenarioList,
  },
  {
    path: "/scenarios/:urlName",
    name: "ScenarioPage",
    component: ScenarioPage,
    props: true,
  },
  {
    path: '/resultats',
    name: 'ResultsPage',
    component: ResultsPage
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: GameDashboard
  },
  {
    path: '/formation',
    name: 'FormationPage',
    component: FormationPage
  },
  {
    path: '/badges',
    name: 'RewardsPage',
    component: RewardsPage
  },
  {
    path: '/roue-des-competences',
    name: 'SkillsWheelPage',
    component: SkillsWheelPage
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
