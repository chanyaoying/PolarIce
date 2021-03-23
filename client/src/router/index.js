import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
// import helloWorld from '../views/ helloWorld'

Vue.use(VueRouter)

const routes = [{
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import( /* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/manageRoom',
    name: 'manageRoom',
    component: () => import('../views/manageRoom.vue')
  },
  {
    path: '/createRoom',
    name: 'createRoom',
    component: () => import('../views/createRoom.vue')
  },
  {
    path: '/playGame',
    name: 'playGame',
    component: () => import('../views/404.vue')
  },
  {
    path: '/playGame/:roomID',
    name: 'playGame/roomID',
    component: () => import('../views/playGame.vue')
  },
  {
    path: '/playGame/console/:roomID',
    name: 'playGame/console/roomID',
    component: () => import('../views/gameConsole.vue')
  },
  {
    path: '/question/:roomID',
    name: 'question/roomID',
    component: () => import('../views/question.vue')
  },
  {
    path: '/matching/:roomID',
    name: 'matching/roomID',
    component: () => import('../views/matching.vue')
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router