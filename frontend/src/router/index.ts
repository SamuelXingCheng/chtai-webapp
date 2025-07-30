import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

import WeeklyNews from '../views/downloads/WeeklyNews.vue'
import ApplicationForms from '../views/downloads/ApplicationForms.vue'
import ContactView from '../views/ContactView.vue'
import BeliefsView from '../views/BeliefsView.vue'
import Profile from '../views/Profile.vue'
import RegisterView from '../views/RegisterView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
  },
  {
    path: '/weekly-news',
    name: 'weekly-news',
    component: WeeklyNews,
  },
  {
    path: '/application-forms',
    name: 'application-forms',
    component: ApplicationForms,
  },
  {
    path: '/beliefs',
    name: 'beliefs',
    component: BeliefsView, // 我們的信仰
  },
  {
    path: '/contact',
    name: 'contact',
    component: ContactView, // 聯絡我們
  },
  {
    path: '/register-view',
    name: 'RegisterView',
    component: RegisterView
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
