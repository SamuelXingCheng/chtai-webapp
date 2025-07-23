import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

import WeeklyNews from '../views/downloads/WeeklyNews.vue'
import ApplicationForms from '../views/downloads/ApplicationForms.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
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
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
