import { createRouter, createWebHistory } from 'vue-router'
import Categories from '../views/Categories.vue'
import Latest from '../views/Latest.vue'
import Top from '../views/Top.vue'
import PostsList from '../views/PostsList.vue'
import Post from '../views/PostPage.vue'

const routes = [
  { path: '/', redirect: '/categories' },
  { path: '/categories', name: 'categories', component: Categories },
  { path: '/posts/:category/', name: 'postsList', component: PostsList, props: true},
  { path: '/posts/:category/:id', name: 'post', component: Post, props: true},
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
