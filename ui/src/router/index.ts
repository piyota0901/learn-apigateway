import { createRouter, createWebHistory } from 'vue-router'
import { createAuthGuard } from '@auth0/auth0-vue'
import Home from '@/views/Home.vue'
import About from '@/views/About.vue'
import Account from '@/views/Account.vue';

const authGuard = createAuthGuard();

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: "/about",
    name: "About",
    component: About,
    beforeEnter: authGuard
  },
  {
    path: '/account',
    name: 'Account',
    component: Account,
    beforeEnter: authGuard
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router