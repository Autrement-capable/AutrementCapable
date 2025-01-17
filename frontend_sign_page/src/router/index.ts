import { createRouter, createWebHistory } from 'vue-router'
import SignIn from '../views/SignIn.vue'
import SignUp from '../views/SignUp.vue'
import ResetPassword from '../views/ResetPassword.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/signin',
      name: 'signin',
      component: SignIn,
      meta: { title: 'Sign In' }
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUp,
      meta: { title: 'Sign Up' }
    },
    {
      path: '/reset-password',
      name: 'reset-password',
      component: ResetPassword,
      meta: { title: 'Reset Password' }
    }
  ]
})

router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title} - Your App Name`
  next()
})

export default router