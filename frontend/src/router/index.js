import { createRouter, createWebHistory } from 'vue-router'
import ComicView from '../views/ComicView.vue'
import GenerateView from '../views/GenerateView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    // component: () => import(/* webpackChunkName: "about" */ '../views/HomeView.vue')
    component: GenerateView
  },
  {
    path: '/story',
    name: 'story',
    component: ComicView
    
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
