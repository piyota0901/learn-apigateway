import { createRouter, createWebHistory } from 'vue-router'
import { createAuthGuard } from '@auth0/auth0-vue'
import Home from '@/views/Home.vue'
import Menu from '@/views/Menu.vue'
import Account from '@/views/Account.vue';

const authGuard = createAuthGuard();

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: "/menu",
    name: "Menu",
    component: Menu,
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